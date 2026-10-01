"""Bounded offline execution of shipping leader capability-policy instructions.

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
sources = [WORK/('cap-policy-'+n+'.json') for n in ('primary','callees','state','outputs','leaves','save-base')]
catalog = {int(b['address'], 16): b for p in sources
           for b in json.loads(p.read_text())['bodies']}
addresses = tuple(catalog)
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

def state(**kw):
    blocks = {STATE: bytearray(0x6000), FIELD: bytearray(16),
              UNIT: bytearray(0xF50*2), REGISTRY: bytearray(24),
              ACTOR: bytearray(0x180), SECONDARY: bytearray(0x180),
              MOVE: bytearray(0x100), ADAPTER: bytearray(0x180),
              RENDER: bytearray(0x740), SPEED: bytearray(0x40),
              0x2089340: bytearray(4), 0x2098E10: bytearray(0x288),
              0x209A2C4: bytearray([0xA5,0xA5,0x5A]),
              0x22C7FE0: bytearray(4), 0x22C8000: bytearray(8),
              0x208E688: bytearray(8), 0x208E6A0: bytearray(4),
              0x2EBF190: bytearray(8), 0x2ADD100: bytearray(8),
              0x22C6F28: bytearray(8), 0x21654C4: bytearray(4)}
    def put(base, off, data): blocks[base][off:off+len(data)] = data
    put(0x2EBF190,0,q(STATE)); put(0x2ADD100,0,q(FIELD))
    put(0x22C6F28,0,q(RENDER)); put(0x208E688,0,q(UNIT))
    put(0x208E6A0,0,d(2)); put(STATE,0x5B04,d(kw.get('mode',0)))
    put(STATE,0x5AD5,bytes([1])); put(FIELD,4,d(1))
    put(FIELD,8,struct.pack('<H',kw.get('field',0)<<15))
    put(0x2089340,0,d(kw.get('battle',0x10)))
    put(0x22C7FE0,0,d(0x100000 if kw.get('leader',True) else 0))
    put(0x2098E10,0,q(1)); put(0x2098E10,8,q(REGISTRY))
    put(0x2098E10,0x10,d(1)); put(0x2098E10,0x20,d(2))
    put(REGISTRY,0,d(2)); put(REGISTRY,8,q(ACTOR))
    put(ACTOR,3,b'\x60'); put(ACTOR,0x16,b'\x01\x00')
    put(ACTOR,0x30,q(UNIT)); put(ACTOR,0xB8,q(MOVE))
    put(ACTOR,0xC0,q(SECONDARY))
    put(SECONDARY,0,d(0)); put(SECONDARY,0x138,q(ADAPTER))
    put(MOVE,0xF0,q(SPEED)); put(MOVE,0xD0,struct.pack('<f',3.5))
    put(SPEED,0x24,struct.pack('<f',3.5))
    put(ADAPTER,0x110,d(0x88)); put(ADAPTER,0xC8,struct.pack('<f',3.5))
    put(UNIT,0,q(8|kw.get('flags',0))); put(UNIT,8,d(0x100000))
    put(UNIT,0x698,q(0 if kw.get('null_bkbi') else STATE+8))
    put(UNIT,0x5C,d(kw.get('event',0x2001)))
    put(UNIT,0x6B7,bytes([kw.get('combo',0)]))
    put(UNIT,0x6B4,bytes([kw.get('phase',0)]))
    put(UNIT,0x714,struct.pack('<H',kw.get('action',0x21E)))
    put(STATE,8+0x3C,d(kw.get('status',0)))
    put(STATE,8+0x64,d(kw.get('status_b',0)))
    put(UNIT,0xF50+0x698,q(STATE+8+0x1C8))
    put(STATE,8+0x1C8+0x3C,d(kw.get('other_status',0)))
    put(RENDER,0x284,d(1)); put(RENDER,0xC8,d(-1))
    put(RENDER,0xCC,struct.pack('<H',kw.get('render_event',0x2001)))
    put(0x22C8000,0,d(kw.get('movement_mask',0)))
    put(0x22C8000,4,bytes([0xA0,kw.get('mask1',0xAC),0x50,0xA0]))
    for a in (0x1DFE0BC,0x1DFE0B8,0x8F8D80,0x915734):
        blocks[a] = bytearray(extract(a,4))
    return [(a,bytes(b)) for a,b in blocks.items()]

out = dict(exe_sha256=sha, unicorn_version=unicorn.__version__, stubs=[],
           source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
           body_sha256={hex(a):hashlib.sha256(b).hexdigest() for a,b in bodies.items()},
           limits=['All globals, registry, actor, units, status and movement/render state are injected.',
                   'Full 0023B040 entry, original callees and native movement writes; no live initialization or scheduling.',
                   'Render record C8=-1 selects original CC return; 004235C0 and nontrivial render-event selection not executed.',
                   'Normal ownership and gameplay reachability of constructed states are not established.'],cases=[])
output=WORK/'cap-policy-result.json'

def bank(c):
    out['cases'].append(c)
    output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok'] and c['code_unchanged'] and not c['invalid'],c['name']
    print(c['name'],len(c['memory']),'events')

def policy(name, mask, **kw):
    writes=state(**kw)
    c=run(name,0x23B040,(0,0,0,0),writes,[(a,len(b)) for a,b in writes])
    c['parameters']=kw; c['expected_mask']=mask
    bank(c)
    actual=bytes.fromhex(c['after']['0x22c8000'])
    old=bytes.fromhex(c['before']['0x22c8000'])
    expected_movement=(int.from_bytes(old[:4],'little')&~2)|((mask&1)<<1)
    expected_mask1=(old[5]&~2)|((mask>>1)&2)
    assert actual[:4]==d(expected_movement) and actual[5]==expected_mask1,name
    assert bytes.fromhex(c['after']['0x209a2c4'])==bytes([0xA5,1-((mask>>1)&1),0x5A]),name
    return c

# Two opposite real output controls before any broader cases.
policy('healthy-positive',0)
policy('immobilize-positive',5,status=0x4000)
if '--feasibility' in sys.argv:
    print('Two nonempty full-entry controls completed.')
    sys.exit(0)

for name, mask, kw in (
    ('stop',7,dict(status=8)),
    ('immobilize-second-layer',5,dict(status_b=0x4000)),
    ('immobilize-event-denial',7,dict(status=0x4000,event=0x2002)),
    ('immobilize-render-event-denial',7,dict(status=0x4000,render_event=0x2002)),
    ('immobilize-seed-denial',7,dict(status=0x4000,battle=0x50)),
    ('combo-one',7,dict(combo=1)),('combo-255',7,dict(combo=255)),
    ('flag46',7,dict(flags=1<<46)),('flag45-control',0,dict(flags=1<<45)),
    ('party-incapacity',7,dict(battle=0x210)),('roster-incapacity',7,dict(battle=0x410)),
    ('incapacity-no-leader',0,dict(battle=0x610,leader=False)),
    ('incapacity-mode2-skip',0,dict(battle=0x610,mode=2,combo=1,flags=1<<46)),
    ('incapacity-field-skip',0,dict(battle=0x610,field=1,combo=1,flags=1<<46)),
    ('seed-mode2-preserved',7,dict(battle=0x50,mode=2)),
    ('action-phase8',0,dict(action=0x21E,phase=8)),
    ('action-phase9',2,dict(action=0x21E,phase=9)),
    ('action-outside-id',0,dict(action=0x21F,phase=9)),
    ('flag24-overrides-action-range',2,dict(action=0xFFFF,phase=0,flags=1<<24)),
    ('mode1-healthy-counterpart',0,dict(mode=1)),
    ('mode1-incapacitated-counterpart',7,dict(mode=1,other_status=1)),
    ('unrelated-output-bits-preserved',0,dict(movement_mask=0x82,mask1=0xAE)),
): policy(name,mask,**kw)

# Every value in each finite bitmap range, immediate outside controls, extremes.
for entry,lo,hi,members,inverted in (
    (0x322600,0x2006,0x203C,{0x2006,0x2037,0x2039,0x203A,0x203B,0x203C},False),
    (0x322920,0x2001,0x2031,{0x2001,0x2009,0x2031},True)):
    for value in [0,0x7FFFFFFF,0x80000000,0xFFFFFFFF,*range(lo-1,hi+2)]:
        c=run('predicate-'+hex(entry)+'-'+hex(value),entry,(value,0,0,0),[],[])
        c['expected_return']=int((value not in members) if inverted else (value in members))
        bank(c); assert int(c['rax'],16)==c['expected_return']
for value in (0,1,2,0xFFFFFFFF,0x100000000):
    c=run('permit-setter-'+hex(value),0x26BD40,(value,0,0,0),[(0x209A2C4,b'\xa5\xa5\x5a')],[(0x209A2C4,3)])
    bank(c); assert bytes.fromhex(c['after']['0x209a2c4'])==bytes([0xA5,int(bool(value&0xFFFFFFFF)),0x5A])

# Deliberately invalid state tests the alleged null-status safe fallback.
writes=state(null_bkbi=True)
c=run('null-bkbi-negative',0x23B040,(0,0,0,0),writes,[(a,len(b)) for a,b in writes])
c['expected_fault']={'rip':'0x23b15e','address':'0x64'}
out['cases'].append(c); output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
assert not c['returned'] and c['invalid'] and c['invalid'][0][0]=='0x23b15e' and c['invalid'][0][2]=='0x64'
assert all(e[1]!='W' for e in c['memory']), 'fault must precede output publication'
print('Expected invalid-state read fault; no output writes. Cases:',len(out['cases']))
