"""Bounded native save/restore source proof; calls abstract normal returns only."""
import hashlib
import json
import struct
import sys
from pathlib import Path
from collections import deque
import capstone

sys.dont_write_bytecode = True
DEP = Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
POLICY = Path('Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py')
members = {m['path']: m for m in json.loads((DEP/'manifest.json').read_bytes())['members']}
sha = lambda b: hashlib.sha256(b).hexdigest()
for n in ('retained/functions.tsv', 'python-deps/pefile.py'):
    assert sha((DEP/n).read_bytes()) == members[n]['sha256']
assert sha(POLICY.read_bytes()) == members['retained/reg_tracking.py']['sha256']
sys.path.insert(0, str(POLICY.parent.resolve()))
import reg_tracking as roles
assert Path(roles.__file__).resolve() == POLICY.resolve()
sys.path.insert(0, str((DEP/'python-deps').resolve()))
import pefile
image = Path('Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
assert sha(image) == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
row = next(l for l in (DEP/'retained/functions.tsv').read_text().splitlines()
           if l.split('\t')[0].lower().lstrip('0x').lstrip('0') == '533b20')
size = int(row.split('\t')[2]); assert size == 9526
ENTRY, RET = 0x533B20, 0x536055
pe = pefile.PE(data=image, fast_load=True)
assert pe.OPTIONAL_HEADER.ImageBase == 0x120000
code = pe.get_data(ENTRY - 0x120000, size)
prior_bytes = Path(__file__).with_name('callee-abi-feasibility.json').read_bytes()
assert sha(prior_bytes) == 'fd6f18459d42082ee93d7166a43ba57c1e7b891279bdb7e51b1e5f6a9a7e0e72'
prior = json.loads(prior_bytes)
assert sha(code) == prior['body_sha256']
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); cs.detail = True


def decode(data):
    values = list(cs.disasm(data, ENTRY))
    assert sum(i.size for i in values) == size
    return {i.address: i for i in values}


def graph(ins):
    out = {}
    for pc, i in ins.items():
        nxt = pc + i.size
        if i.mnemonic.startswith('ret'):
            edges = []
        elif i.group(capstone.CS_GRP_JUMP):
            assert i.operands[0].type == capstone.x86.X86_OP_IMM, 'indirect jump'
            target = i.operands[0].imm
            assert target in ins, 'external or non-boundary jump'
            edges = [target] if i.mnemonic == 'jmp' else [target, nxt]
        else:
            edges = [nxt]
        assert all(e in ins for e in edges), 'incomplete fallthrough'
        out[pc] = edges
    return out


def path(edges, target, removed=None):
    q = deque([(ENTRY, [])]); seen = set()
    while q:
        pc, trail = q.popleft()
        if pc in seen or pc == removed:
            continue
        seen.add(pc); trail = trail + [pc]
        if pc == target:
            return trail
        q.extend((n, trail) for n in edges[pc])
    return None


original = decode(code); edges = graph(original)
assert [pc for pc, i in original.items() if i.mnemonic.startswith('ret')] == [RET]
assert path(edges, RET)
saves = {'rbx': 0x533B20, 'rsi': 0x533B22, 'r13': 0x533B23,
         'r14': 0x533B25, 'r15': 0x533B27}
restores = {'r15': 0x53604D, 'r14': 0x53604F, 'r13': 0x536051,
            'rsi': 0x536053, 'rbx': 0x536054}
for r, pc in saves.items():
    assert original[pc].mnemonic == 'push' and original[pc].op_str == r
    assert path(edges, RET, pc) is None
for r, pc in restores.items():
    assert original[pc].mnemonic == 'pop' and original[pc].op_str == r
    assert r in roles.written(original[pc])
    assert path(edges, RET, pc) is None
assert original[0x533B29].mnemonic == 'sub' and original[0x533B29].op_str == 'rsp, 0x3a0'
assert original[0x536046].mnemonic == 'add' and original[0x536046].op_str == 'rsp, 0x3a0'
assert path(edges, RET, 0x533B29) is None and path(edges, RET, 0x536046) is None
rsp_local = [pc for pc, i in original.items() if 'rsp' in roles.written(i)
             and i.mnemonic != 'call' and not i.mnemonic.startswith('ret')]
assert set(rsp_local) == set(saves.values()) | set(restores.values()) | {0x533B29, 0x536046}
saved_slots = {'r13': [0x3B0, 0x3B8], 'rsi': [0x3B8, 0x3C0], 'rbx': [0x3C0, 0x3C8]}
direct_stack_stores = []; unresolved_stack = []; memory_roles = []
for pc, i in original.items():
    for oi, op in enumerate(i.operands):
        if op.type != capstone.x86.X86_OP_MEM:
            continue
        kind = roles.op_kind(i, op, oi)
        assert kind != '?', (pc, i.mnemonic, i.op_str)
        memory_roles.append({'pc': f'{pc:08X}', 'operand': oi, 'role': kind})
        if kind not in ('w', 'rw') or i.reg_name(op.mem.base) != 'rsp':
            continue
        if op.mem.index:
            unresolved_stack.append(f'{pc:08X}')
            continue
        a, b = op.mem.disp, op.mem.disp + op.size
        assert not any(a < hi and lo < b for lo, hi in saved_slots.values()), (pc, a, b)
        direct_stack_stores.append({'pc': f'{pc:08X}', 'interval': [a, b], 'role': kind})
assert not unresolved_stack
# The real original MOVUPS store invokes the reviewed policy; flags alone are not used.
store = original[0x533B5E]
assert roles.op_kind(store, store.operands[0], 0) == 'w'
for data, expected in ((bytes.fromhex('0f1101'), 'w'),
                       (bytes.fromhex('488d4104'), 'addr'),
                       (bytes.fromhex('f00fc101'), 'rw')):
    c = next(cs.disasm(data, 0x1000))
    oi, op = next((j, o) for j, o in enumerate(c.operands)
                  if o.type == capstone.x86.X86_OP_MEM)
    assert roles.op_kind(c, op, oi) == expected
# A real near conditional branch can skip the epilogue in a same-size private input.
bp = 0x535FC8; assert original[bp].bytes.hex() == '0f82c2e5ffff'
bypass = bytearray(code); before = bytes(bypass[bp-ENTRY:bp-ENTRY+6])
bypass[bp-ENTRY:bp-ENTRY+6] = bytes.fromhex('0f82') + struct.pack('<i', RET - (bp+6))
bi = decode(bypass); be = graph(bi)
witness = path(be, RET, restores['r13']); assert witness is not None
wrong = bytearray(code); offset = restores['r13']-ENTRY
assert bytes(wrong[offset:offset+2]) == bytes.fromhex('415d')
wrong[offset:offset+2] = bytes.fromhex('415c')
wi = decode(wrong)
assert wi[restores['r13']].op_str == 'r12' and 'r13' not in roles.written(wi[restores['r13']])
assert len(original) == len(bi) == len(wi)


def shown(pc):
    i = original[pc]
    return {'pc': f'{pc:08X}', 'bytes': i.bytes.hex(), 'instruction': i.mnemonic+' '+i.op_str}


print(json.dumps({'status': 'STATIC_NORMAL_RETURN_SAVE_RESTORE_CONDITIONAL',
                  'body_sha256': sha(code), 'body_hex': code.hex(), 'catalogue': row,
                  'instruction_count': len(original),
                  'source': [shown(pc) for pc in sorted(set(saves.values()) | set(restores.values()) |
                             {0x533B29, 0x536046, 0x536038, RET})],
                  'normal_cfg': {f'{pc:08X}':[f'{n:08X}' for n in ns] for pc, ns in edges.items()},
                  'save_restore_dominates_local_return': True,
                  'rsp_non_call_writes_exactly_prologue_epilogue': [f'{pc:08X}' for pc in rsp_local],
                  'saved_stack_intervals': saved_slots, 'direct_stack_stores': direct_stack_stores,
                  'memory_roles': memory_roles,
                  'controls': {'bypass_pc': f'{bp:08X}', 'original': before.hex(),
                               'private': bytes(bypass[bp-ENTRY:bp-ENTRY+6]).hex(),
                               'bypass_witness': [f'{pc:08X}' for pc in witness],
                               'wrong_restore_original': '415d', 'wrong_restore_private': '415c',
                               'wrong_restore_detected': True, 'equal_instruction_counts': True,
                               'adapter_store_lea_rmw': True},
                  'tool_identity': {'adapter_path': str(Path(roles.__file__).resolve()),
                                    'adapter_sha256': sha(POLICY.read_bytes()),
                                    'pefile_sha256': sha(Path(pefile.__file__).read_bytes()),
                                    'capstone': capstone.__version__},
                  'implication': 'At the selected entry, every modelled normal local return restores entry RBX/RSI/R13 from its saved slots; no blanket register-preserving callee assumption is needed for this source epilogue.',
                  'limits': 'Calls must return normally with coherent RSP and saved stack bytes; native pointer/callee alias writes, exceptions and other entries are unproved. No actual execution, initialized identity, scheduling, lifetime or presentation claim.'}, indent=2))
