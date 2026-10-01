"""Bounded offline execution of shipping presentation-entry reference lookup.

Reuses the established Unicorn/PE extraction method. Controlled state is injected;
there is no live initialization, resource move, scheduling or native handler proof.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, 'Database/Tools/work/ASTRA/python-libs')
import unicorn
from unicorn.x86_const import *

WORK = Path('Database/Tools/work/ASTRA')
EVID = Path('Database/FFXII TZA/_experiments/evidence')
sources = [WORK/'render-event-primary.json', WORK/'render-event-lookup.json', EVID/'efx-rebase-primary/primary.json', EVID/'capability-policy-falsification/callees.json', EVID/'capability-policy-falsification/primary.json']
catalog = {int(b['address'], 16): b for p in sources
           for b in json.loads(p.read_text())['bodies']}
addresses = (0x51B9E0,0x51F240,0x3AB7F0,0x20E600,0x424230,0x41C760,0x41FCA0,0x4235C0)
raw = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 60)[0]
ib = struct.unpack_from('<Q', raw, pe+48)[0]
assert ib == 0x120000
st = pe+24+struct.unpack_from('<H', raw, pe+20)[0]

def extract(a, n):
    for j in range(struct.unpack_from('<H', raw, pe+6)[0]):
        _, rva, size, disk = struct.unpack_from('<IIII', raw, st+j*40+8)
        d = a-ib-rva
        if 0 <= d and d+n <= size:
            return raw[disk+d:disk+d+n]
    raise ValueError(hex(a))

bodies = {a: extract(a, catalog[a]['bytes']) for a in addresses}
for a, b in bodies.items():
    assert hashlib.sha256(b).hexdigest() == catalog[a]['sha256']
instructions = {int(i['address'], 16) for a in addresses
                for i in catalog[a]['instructions']}
MASK = (1 << 64)-1
SP, STOP = 0x60001808, 0x70000000
STATE, FIELD, UNIT = 0x50010000, 0x50020000, 0x50030000
REGISTRY, ACTOR, SECONDARY = 0x50050000, 0x50060000, 0x50070000
MOVE, ADAPTER, RENDER, SPEED = 0x50080000, 0x50090000, 0x500A0000, 0x500B0000
NV = (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RSI, UC_X86_REG_RDI,
      UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15)
ARGS = (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)

def run(name, entry, args, writes, observations):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    pages = set(range(0x60000000, 0x60003000, 4096))
    for a, data in list(bodies.items())+writes:
        pages.update(range(a & ~4095, (a+len(data)+4095) & ~4095, 4096))
    for a, n in observations:
        pages.update(range(a & ~4095, (a+n+4095) & ~4095, 4096))
    for a in sorted(pages):
        u.mem_map(a, 4096)
    for a, data in bodies.items():
        u.mem_write(a, data)
    for a, data in writes:
        u.mem_write(a, data)
    before = {hex(a): bytes(u.mem_read(a, n)).hex() for a, n in observations}
    saved = {r: 0xA100000000000000+i for i, r in enumerate(NV)}
    saved.update({UC_X86_REG_XMM6+i: 0x123456789ABCDEF0123456789ABCDEF ^ i
                  for i in range(10)})
    for r, v in saved.items():
        u.reg_write(r, v)
    for r, v in zip(ARGS, args):
        u.reg_write(r, v & MASK)
    u.reg_write(UC_X86_REG_RSP, SP)
    u.reg_write(UC_X86_REG_EFLAGS, 2)
    u.reg_write(UC_X86_REG_MXCSR, 0x1F80)
    u.mem_write(SP, struct.pack('<Q', STOP))
    events, calls, visited, invalid = [], [], {}, []

    def code(uc, a, n, _):
        assert a in instructions, 'unexpected instruction '+hex(a)
        visited[hex(a)] = visited.get(hex(a), 0)+1
        if a in bodies:
            calls.append({'event_index': len(events), 'target': hex(a),
                          'args': [hex(uc.reg_read(r)) for r in ARGS]})

    def memory(uc, access, a, n, v, _):
        if 0x60000000 <= a and a+n <= 0x60003000:
            return
        events.append([hex(uc.reg_read(UC_X86_REG_RIP)),
                       'W' if access == unicorn.UC_MEM_WRITE else 'R', hex(a), n,
                       hex(v & ((1 << (n*8))-1)) if access == unicorn.UC_MEM_WRITE
                       else bytes(uc.mem_read(a, n)).hex()])

    def bad(uc, access, a, n, v, _):
        invalid.append([hex(uc.reg_read(UC_X86_REG_RIP)), access, hex(a), n])
        return False

    u.hook_add(unicorn.UC_HOOK_CODE, code)
    u.hook_add(unicorn.UC_HOOK_MEM_READ | unicorn.UC_HOOK_MEM_WRITE, memory)
    u.hook_add(unicorn.UC_HOOK_MEM_INVALID, bad)
    error = None
    try:
        u.emu_start(entry, STOP, count=30000)
    except (unicorn.UcError, AssertionError) as e:
        error = str(e)
    return dict(name=name, entry=hex(entry), args=[hex(v & MASK) for v in args],
                injected_writes=[[hex(a), b.hex()] for a, b in writes],
                before=before, after={hex(a): bytes(u.mem_read(a, n)).hex()
                                     for a, n in observations},
                calls=calls, visited=visited, memory=events, invalid=invalid,
                rax=hex(u.reg_read(UC_X86_REG_RAX)), error=error,
                returned=error is None and u.reg_read(UC_X86_REG_RIP) == STOP,
                stack_ok=u.reg_read(UC_X86_REG_RSP) == SP+8,
                nonvolatile_ok=all(u.reg_read(r) == v for r, v in saved.items()),
                code_unchanged=all(bytes(u.mem_read(a, len(b))) == b
                                   for a, b in bodies.items()))

def q(v):
    return struct.pack('<Q', v & MASK)

def d(v):
    return struct.pack('<I', v & 0xFFFFFFFF)

CONTAINER,TABLE,PAYLOAD,ROOT,RECORD=0x51000000,0x51001000,0x51002000,0x51003000,0x51004000
output=WORK/'render-event-result.json'
out=dict(exe_sha256=sha,unicorn_version=unicorn.__version__,stubs=[],
         source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
         body_sha256={hex(a):hashlib.sha256(b).hexdigest() for a,b in bodies.items()},
         limits=['Injected container/table, render record, root and entry payload; no live initialization.',
                 'Only untagged source-provider paths; tagged resolver and ownership excluded.',
                 'Priority-table fallback not mapped; unexpected reach stops rather than invents its effects.'],cases=[])

def setup(kind=1,refresh=False,source=0x40000000,offset=0x20,cached=0x180000000,table=TABLE,cc=0x2001,ce=0x2009,c4=1,c8=1,entry_flags=0):
    container=bytearray(0x30);container[4:8]=d(kind);container[8:16]=q(table)
    tab=bytearray(0x60);tab[0x30]=2 if refresh else 0
    tab[0x40:0x48]=q(source);tab[0x48:0x50]=q(cached);tab[0x50:0x54]=d(offset)
    payload=bytearray(0x400);payload[0x2C8:0x2CC]=d(entry_flags)
    root=bytearray(0xDB0);root[0xDA8:0xDB0]=q(CONTAINER)
    record=bytearray(0x740);record[0x10:0x14]=d(ROOT)
    record[0xC4:0xC8]=d(c4);record[0xC8:0xCC]=d(c8)
    record[0xCC:0xCE]=struct.pack('<H',cc);record[0xCE:0xD0]=struct.pack('<H',ce)
    return [(CONTAINER,bytes(container)),(TABLE,bytes(tab)),(PAYLOAD,bytes(payload)),
            (ROOT,bytes(root)),(RECORD,bytes(record)),(0x1F83530,q(0))]

def case(name,entry,args,expected,**kw):
    writes=setup(**kw)
    c=run(name,entry,args,writes,[(a,len(b)) for a,b in writes])
    c['parameters']=kw;c['expected_return']=hex(expected)
    out['cases'].append(c);output.write_text(json.dumps(out,indent=2)+'\n')
    assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok'] and c['code_unchanged'] and not c['invalid'],name
    assert int(c['rax'],16)==expected,(name,c['rax'])
    effects=[e for e in c['memory'] if e[1]=='W']
    if kw.get('refresh'):
        value=(kw.get('source',0x40000000)+kw.get('offset',0x20))&0xFFFFFFFF
        if value&0x80000000:value|=0xFFFFFFFF00000000
        assert effects==[['0x51f2b7','W',hex(TABLE+0x48),8,hex(value)]],name
    else:assert effects==[],name
    print(name,c['rax'],len(c['memory']),'events')
    return c

case('cached-full-width-control',0x51B9E0,(CONTAINER,1,0,0),0x180000000)
case('refresh-low-positive',0x51B9E0,(CONTAINER,1,0,0),0x40000020,refresh=True)
if '--feasibility' in sys.argv:
    print('Cached and original refresh-write controls complete.');sys.exit(0)

case('refresh-above2-sign-extension',0x51B9E0,(CONTAINER,1,0,0),0xFFFFFFFF80000020,refresh=True,source=0x80000000)
case('refresh-above4-truncation',0x51B9E0,(CONTAINER,1,0,0),0x40000020,refresh=True,source=0x140000000)
case('refresh-wraps-to-null',0x51B9E0,(CONTAINER,1,0,0),0,refresh=True,offset=0xC0000000)
case('id-high-word-ignored',0x51B9E0,(CONTAINER,0xBEEF0001,0,0),0x180000000)
case('kind0-provider-table',0x51B9E0,(CONTAINER,1,0,0),0x180000000,kind=0)
case('kind2-rejected',0x51B9E0,(CONTAINER,1,0,0),0,kind=2)
case('kind3-rejected',0x51B9E0,(CONTAINER,1,0,0),0,kind=3)
case('null-table-index0',0x51B9E0,(CONTAINER,0,0,0),0,table=0)
case('entry-bit12-clear',0x424230,(RECORD,0,0,0),0,cached=PAYLOAD)
case('entry-bit12-set',0x424230,(RECORD,0,0,0),1,cached=PAYLOAD,entry_flags=0x1000)
case('entry-missing-default-one',0x424230,(RECORD,0,0,0),1,cached=0)
case('entry-id-minus1-default-one',0x424230,(RECORD,0,0,0),1,c4=-1)
case('getter-no-alternate',0x41FCA0,(RECORD,0,0,0),0x2001,c8=-1)
for cc in (0,1,2,0x1001,0x2001,0x2037,0x8000,0xFFFF):
    case('getter-alternate-cc-'+hex(cc),0x41FCA0,(RECORD,0,0,0),0x2009,cc=cc,cached=PAYLOAD)
case('getter-alternate-missing-entry',0x41FCA0,(RECORD,0,0,0),0x2009,cached=0)

writes=setup(table=0)
c=run('null-table-index1-invalid',0x51B9E0,(CONTAINER,1,0,0),writes,[(a,len(b)) for a,b in writes])
c['expected_fault']={'rip':'0x51f2a3','address':'0x30'}
out['cases'].append(c);output.write_text(json.dumps(out,indent=2)+'\n')
assert not c['returned'] and c['invalid'][0][0]=='0x51f2a3' and c['invalid'][0][2]=='0x30'
assert not any(e[1]=='W' for e in c['memory'])
print('Expected invalid-state fault at entry flag read; total',len(out['cases']))
