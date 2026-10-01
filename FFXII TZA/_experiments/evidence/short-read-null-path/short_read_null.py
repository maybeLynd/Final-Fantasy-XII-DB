"""NULL-argument paths of 00866A00 under isolated original execution.

Extends spawn-storage-completion/short-read-execution.json (ASTRA): that set proved
prefix copy + stale tail + cursor advance + boolean-to-count result encoding. It did
not drive the two je 0x866a70 null guards at +0x08 (rcx, the cursor-pointer taken
from the handle global 0x2EAF8E8 by the outer) and +0x0D (rdx, the destination).
This drives both through the real outer entry 0x862590 so the wrapper multiply and
RESULT-global write execute too.

Negative control: 74->75 (je->jne) at 0x866a0B on the positive case must be detected.
No stubs, no live process; all state injected. Reuses ASTRA's PE reader and body JSONs.
"""
import hashlib, json, struct, sys
from pathlib import Path
sys.path.insert(0, 'Database/Tools/work/ASTRA/python-libs')
import unicorn
from unicorn.x86_const import *

W = Path('Database/Tools/work/ASTRA')
ns = {}
s = (W / 'spawn_storage_completion_primary.py').read_text()
exec(compile(s.split('for a in (')[0], '<existing shipping PE reader>', 'exec'), ns)
cat = {}
for n, a in [('adapters', 0x862590), ('file', 0x866A00)]:
    j = json.loads((W / ('spawn-storage-completion-' + n + '.json')).read_text())
    assert j['exe_sha256'] == ns['sha']
    cat[a] = next(b for b in j['bodies'] if int(b['address'], 16) == a)
code = {}; instructions = set()
for a, b in cat.items():
    o = ns['off'](a - ns['ib']); d = ns['raw'][o:o + b['bytes']]
    assert hashlib.sha256(d).hexdigest() == b['sha256']
    assert d == b''.join(bytes.fromhex(i['bytes']) for i in b['instructions'])
    code[a] = d; instructions.update(int(i['address'], 16) for i in b['instructions'])

ENTRY, SP, STOP = 0x862590, 0x60001808, 0x70000000
HANDLE, SOURCE, DEST = 0x30001000, 0x30002000, 0x30003000
VECTOR, RESULT, HANDLE_GLOBAL = 0x1F44D40, 0x2EAF8E0, 0x2EAF8E8
NV = (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RSI, UC_X86_REG_RDI,
      UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15)
def d(v): return struct.pack('<I', v & 0xffffffff)
def q(v): return struct.pack('<Q', v & 0xffffffffffffffff)

def run(name, fd, dest, handle_global, available=8, request=8, cursor=0, patch=None):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    payload = bytes(range(0x31, 0x51)); sentinel = b'\xC7' * 48
    injected = [(HANDLE, d(cursor) + d(1) + b'\xA5' * 24), (SOURCE, payload),
                (DEST, sentinel),
                (VECTOR, q(SOURCE) + q(SOURCE + available) + q(SOURCE + len(payload))),
                (RESULT, d(0x12345678)), (HANDLE_GLOBAL, q(handle_global))]
    bodies = dict(code)
    if patch:
        orig = code[patch[0]]
        bodies[patch[0]] = orig[:patch[1]] + patch[2] + orig[patch[1] + len(patch[2]):]
    pages = set(range(0x60000000, 0x60003000, 4096))
    for a, b in [*bodies.items(), *injected]:
        pages.update(range(a & ~4095, (a + len(b) + 4095) & ~4095, 4096))
    for a in pages: u.mem_map(a, 4096)
    for a, b in [*bodies.items(), *injected]: u.mem_write(a, b)
    saved = {r: 0xA100000000000000 + i for i, r in enumerate(NV)}
    saved.update({UC_X86_REG_XMM6 + i: 0x123456789ABCDEF0123456789ABCDEF ^ i for i in range(10)})
    for r, v in saved.items(): u.reg_write(r, v)
    for r, v in [(UC_X86_REG_RSP, SP), (UC_X86_REG_EFLAGS, 2), (UC_X86_REG_MXCSR, 0x1F80),
                 (UC_X86_REG_RCX, fd), (UC_X86_REG_RDX, dest), (UC_X86_REG_R8, request)]:
        u.reg_write(r, v)
    u.mem_write(SP, q(STOP))
    events = []; visited = []; invalid = []
    def on_code(uc, a, n, _):
        visited.append(hex(a))
        if patch is None:
            assert a in instructions, hex(a)
    def memory(uc, access, a, n, v, _):
        if 0x60000000 <= a and a + n <= 0x60003000: return
        events.append([hex(uc.reg_read(UC_X86_REG_RIP)), 'W' if access == unicorn.UC_MEM_WRITE else 'R',
                       hex(a), n, bytes(uc.mem_read(a, n)).hex() if access != unicorn.UC_MEM_WRITE
                       else int(v & ((1 << (n * 8)) - 1)).to_bytes(n, 'little').hex()])
    def bad(uc, access, a, n, v, _):
        invalid.append([hex(uc.reg_read(UC_X86_REG_RIP)), access, hex(a), n]); return False
    u.hook_add(unicorn.UC_HOOK_CODE, on_code)
    u.hook_add(unicorn.UC_HOOK_MEM_READ | unicorn.UC_HOOK_MEM_WRITE, memory)
    u.hook_add(unicorn.UC_HOOK_MEM_INVALID, bad)
    error = None
    try: u.emu_start(ENTRY, STOP, count=5000)
    except (unicorn.UcError, AssertionError) as e: error = str(e)
    dest_hex = bytes(u.mem_read(DEST, 48)).hex() if dest else None
    writes = [e for e in events if e[1] == 'W']
    return dict(name=name,
                injected=dict(fd=fd, dest=hex(dest), handle_global=hex(handle_global),
                              available=available, request=request, cursor=cursor),
                observed=dict(return_eax=hex(u.reg_read(UC_X86_REG_EAX)),
                              result=hex(struct.unpack('<I', u.mem_read(RESULT, 4))[0]),
                              dest=dest_hex),
                visited=visited, events=events, invalid=invalid, error=error,
                returned=error is None and u.reg_read(UC_X86_REG_RIP) == STOP,
                stack_ok=u.reg_read(UC_X86_REG_RSP) == SP + 8,
                nonvolatile_ok=all(u.reg_read(r) == v for r, v in saved.items()),
                code_unchanged=all(bytes(u.mem_read(a, len(b))) == b for a, b in bodies.items()),
                write_count=len(writes),
                ret0_path_hit='0x866a70' in visited,
                copy_loop_hit='0x866a30' in visited)

cases = []
def case(**kw):
    r = run(**kw); cases.append(r)
    print(r['name'], 'ret:', r['observed']['return_eax'], 'result:', r['observed']['result'],
          'writes:', r['write_count'], 'ret0:', r['ret0_path_hit'], 'loop:', r['copy_loop_hit'],
          'returned:', r['returned'], 'err:', r['error'])
    return r

# Positive control: normal full read still works and reaches the copy loop.
pos = case(name='full-read-positive', fd=0, dest=DEST, handle_global=HANDLE)
# The two NULL paths, driven through the real outer entry.
nd = case(name='null-dest', fd=0, dest=0, handle_global=HANDLE)
nh = case(name='null-handle-global', fd=0, dest=DEST, handle_global=0)
# Mutant negative control: je->jne at 0x866a0B must change the positive outcome.
mut = case(name='mut-je-to-jne-866a0b', fd=0, dest=DEST, handle_global=HANDLE,
           patch=(0x866A00, 0x0B, b'\x75'))

checks = {
    'positive': (pos['returned'] and pos['copy_loop_hit'] and not pos['ret0_path_hit']
                 and pos['observed']['return_eax'] == '0x8'),
    'null_dest_ret0': (nd['returned'] and nd['ret0_path_hit'] and not nd['copy_loop_hit']
                       and nd['observed']['return_eax'] == '0x0'
                       and nd['observed']['result'] == '0x0'),
    'null_dest_writes': all(e[2] == hex(RESULT) for e in nd['events'] if e[1] == 'W'),
    'null_handle_ret0': (nh['returned'] and nh['ret0_path_hit'] and not nh['copy_loop_hit']
                         and nh['observed']['return_eax'] == '0x0'
                         and nh['observed']['result'] == '0x0'),
    'null_handle_writes': all(e[2] == hex(RESULT) for e in nh['events'] if e[1] == 'W'),
    'mutant_detected': (mut['returned'] and mut['ret0_path_hit'] and not mut['copy_loop_hit']
                        and mut['observed']['return_eax'] == '0x0'),
    'clean_abi': all(c['returned'] and c['stack_ok'] and c['nonvolatile_ok']
                     and c['code_unchanged'] and not c['invalid'] for c in cases),
}
for k, v in checks.items(): print(k, 'PASS' if v else 'FAIL')

out = dict(exe_sha256=ns['sha'], entry=hex(ENTRY),
           bodies=[dict(address=hex(a), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
                   for a, b in code.items()],
           probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           unicorn_version=unicorn.__version__,
           method='B isolated original-code execution', live_game=False, stubs={},
           limits=['Only the NULL-argument guards are new; copy/result semantics come from the sibling ASTRA evidence file.',
                   'Injected vector, handle global, destination and ABI; no live process or filesystem.',
                   'The null paths return 0 after the outer still writes 0 to the RESULT global; "nothing written" refers to the destination and cursor.'],
           checks=checks, cases=cases)
p = W.parent / 'SWE2-ORACLE' / 'short-read-null-execution.json'
p.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8', newline='\n')
print('Saved', p, 'verdict:', 'PASS' if all(checks.values()) else 'FAIL')
