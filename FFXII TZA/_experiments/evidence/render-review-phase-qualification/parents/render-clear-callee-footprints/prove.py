"""Original composed write-footprint proof for record clear helpers.

STATIC_ONLY. Fixed-width calculations below are not execution of FF12 code.
"""
import hashlib, importlib.util, json, struct, sys
from pathlib import Path
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
ROOT = next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
PIN = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'

def load(name, file):
    s = importlib.util.spec_from_file_location(name, P/file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

for file, pin in [
    ('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),
    ('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),
    ('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
    if sha(P/file) != pin: raise RuntimeError('reviewed dependency changed')
V = load('roles','validate-title-source-annotations.py')
G = load('graph','prove_owner_reload_order.py')

def checked_capture(prefix):
    d = P/prefix
    status = json.loads((d/'capture-01.status.json').read_text())
    if status.get('terminal') is not True or status.get('exit') != 0 or status.get('exception') is not None or status['driver_sha256'] != sha(d/'capture.py') or not (d/'capture-01.stdout').read_bytes() or (d/'capture-01.stderr').read_bytes():
        raise RuntimeError('required capture status failed '+prefix)
    x = json.loads((d/'source-01.json').read_text())
    if x.get('wrapper_complete') is not True or x.get('driver_sha256') != sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256') != sha(d/'capture.py') or x['exe_sha256'] != PIN:
        raise RuntimeError('actual capture incomplete '+prefix)
    return x, V.validate(x)

x, roles = checked_capture('')
lineage=json.loads((P/'lineage.json').read_text());pin='a2bcea12693de55748686a2cef48402c0189666974a8af9a8c0720b2717c73ee'
if lineage['manifest_sha256']!=pin or sha(P/'retained/manifest.json')!=pin:raise RuntimeError('retained manifest changed')
members=json.loads((P/'retained/manifest.json').read_text())['members']
for r in lineage['files']:
 q=P/'retained'/r['path']
 if sha(q)!=r['sha256'] or q.stat().st_size!=r['bytes']:raise RuntimeError('retained input changed')
 if r['path']!='manifest.json' and not any(m['path']==r['path'] and m['sha256']==r['sha256'] for m in members):raise RuntimeError('unbound retained input')
y,parent_roles=checked_capture('retained')
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,offset in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
 raise RuntimeError('unbacked original range')
required=[('0x6c0520','0x6c053a'),('0x46d110','0x46d11c'),('0x202c70','0x202c8f'),('0x3e5d00','0x3e5d2c'),('0x3e37e0','0x3e37eb')]
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=required:raise RuntimeError('required helper source changed')
ix={};gb={};graphs=[]
for source in [x,y]:
 for r in source['ranges']:
  a,b=int(r['start'],16),int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
  local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
  if source is y and a!=0x41f730:continue
  tail={0x46d110:'0x202c70',0x3e37e0:'0x861ec0'}.get(a)
  g=G.graph(local,a,b,tail=tail)
  if g['visited']!=set(local):raise RuntimeError('unaccounted helper/caller CFG')
  gb[a]=g;graphs.append({'entry':hex(a),'instructions':len(local),'tails':[hex(v) for v in g['tails']],'calls':g['calls']})

# No result is emitted until both actual capture paths, their retained binding,
# original bytes, complete CFGs and the composed effects below have passed.
def need(pc, mnemonic, args):
    if (ix[pc]['mnemonic'], ix[pc]['args']) != (mnemonic, args):
        raise RuntimeError('required operation changed '+hex(pc))

ops = '''41f744|xor|edx, edx
41f74b|mov|r8d, 0x740
41f751|mov|rbx, rcx
41f754|call|0x861ec0
41f761|lea|rcx, [rbx + 0x210]
41f768|or|ebp, 0xffffffff
41f76b|movss|dword ptr [rsp + 0x20], xmm6
41f775|xor|esi, esi
41f795|mov|word ptr [rbx], bp
41f95f|call|0x6c0520
41f964|lea|rcx, [rbx + 0x220]
41f96b|movss|dword ptr [rsp + 0x20], xmm6
41f97a|call|0x6c0520
41f97f|lea|rcx, [rbx + 0x180]
41f990|call|0x46d110
41f995|lea|rcx, [rbx + 0x1c0]
41f99c|call|0x46d110
41f9c0|mov|edi, esi
41faf5|mov|edx, edi
41faf7|mov|rcx, rbx
41fafa|call|0x3e5d00
41faff|inc|edi
41fb01|cmp|edi, 0xa
41fb04|jl|0x41faf2
41fb0d|lea|rcx, [rbx + 0x580]
41fb5a|call|0x3e37e0
6c0520|movss|xmm0, dword ptr [rsp + 0x28]
46d110|lea|rdx, [rip + 0x1ab33c9]
46d117|jmp|0x202c70
3e5d08|movsxd|r8, edx
3e37e0|xor|edx, edx
3e37e2|lea|r8d, [rdx + 0x50]
3e37e6|jmp|0x861ec0'''
for line in ops.splitlines():
    pc,m,a=line.split('|');need(int(pc,16),m,a)
if ix[0x46d110]['memory'][0]['rip_target'] != '0x1f204e0':
    raise RuntimeError('matrix source identity changed')
caller = gb[0x41f730]
expected_calls = [(0x41f754,'0x861ec0'),(0x41f95f,'0x6c0520'),
                  (0x41f97a,'0x6c0520'),(0x41f990,'0x46d110'),
                  (0x41f99c,'0x46d110'),(0x41fafa,'0x3e5d00'),
                  (0x41fb5a,'0x3e37e0')]
if caller['calls'] != expected_calls or caller['returns'] != [0x41fbe7]:
    raise RuntimeError('unresolved caller effect boundary')
if [(pc,i['args']) for pc,i in ix.items() if 0x41f730<=pc<0x41fbe8 and i['mnemonic'].startswith('j')] != [(0x41fb04,'0x41faf2')]:
    raise RuntimeError('new caller branch requires analysis')
if any(gb[a]['calls'] for a in gb if a!=0x41f730):
    raise RuntimeError('new helper call requires analysis')

import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def unchanged(regs,lo,hi,allow=()):
    for pc in sorted(q for q in ix if lo<=q<hi and q not in allow):
        i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
        if {i.reg_name(r) for r in wr}&set(regs):
            raise RuntimeError('register carrier changed '+hex(pc))

# regs_access is used only for register carriers. Memory roles always come
# from the reviewed adapter already independently checked by V.validate.
unchanged({'rbx','ebx','bx','bl','bh'},0x41f754,0x41fbdd)
unchanged({'rcx','ecx','cx','cl','ch'},0x41f730,0x41f754)
unchanged({'rdx','edx','dx','dl','dh'},0x41f746,0x41f754)
unchanged({'r8','r8d','r8w','r8b'},0x41f751,0x41f754)
unchanged({'rsi','esi','si','sil'},0x41f777,0x41fbce)
unchanged({'rbp','ebp','bp','bpl'},0x41f76b,0x41fbbb)
for a in [0x6c0520,0x46d110,0x202c70,0x3e5d00,0x3e37e0]:
    end=next(int(r['end_exclusive'],16) for r in x['ranges'] if int(r['start'],16)==a)
    unchanged({'rbx','ebx','bx','bl','bh','rsi','esi','si','sil','rbp','ebp','bp','bpl','rdi','edi','di','dil'},a,end)
bindings=[(0x41f761,0x41f95f,0x210,0x6c0520),
          (0x41f964,0x41f97a,0x220,0x6c0520),
          (0x41f97f,0x41f990,0x180,0x46d110),
          (0x41f995,0x41f99c,0x1c0,0x46d110),
          (0x41fb0d,0x41fb5a,0x580,0x3e37e0)]
for definition,call,offset,target in bindings:
    unchanged({'rcx','ecx','cx','cl','ch'},definition+len(bytes.fromhex(ix[definition]['bytes'])),call)
    if any(ix[pc]['mnemonic']=='call' or ix[pc]['mnemonic'].startswith('j') for pc in ix if definition<pc<call):
        raise RuntimeError('receiver crosses unchecked control/effect boundary')
    if not G.dominates(caller,definition,call):raise RuntimeError('receiver does not dominate call')
unchanged({'rdi','edi','di','dil'},0x41f9c2,0x41fb06,allow=(0x41faff,))
unchanged({'rdx','edx','dx','dl','dh'},0x41faf7,0x41fafa)
unchanged({'rcx','ecx','cx','cl','ch'},0x41fafa,0x41fafa)
for a,b in [(0x41f751,0x41f754),(0x41f754,0x41f795),
            (0x41f768,0x41f795),(0x41f775,0x41f9c0),
            (0x41f9c0,0x41fafa),(0x41faf5,0x41fafa),
            (0x41faf7,0x41fafa),(0x41fafa,0x41fb04),
            (0x41fb04,0x41fb0d),(0x41fb5a,0x41fbe7)]:
    if not G.dominates(caller,a,b):raise RuntimeError('required caller order changed')
if caller['edges'][0x41fb04] != [0x41faf2,0x41fb06]:raise RuntimeError('indexed loop edges changed')
# Induction: EDI=0 before the first iteration; body/leaf preserve it; INC
# produces 1..10; signed JL repeats exactly while <10. All values are positive
# and no 32-bit overflow occurs. Not ten executed native calls.
indices=list(range(10))
for k in indices:
    if (k+1<10)!=(k!=9) or k!=(k&0xffffffff):raise RuntimeError('index induction failed')

def write_spans(instructions,base,index_values=None):
    """Concrete reviewed-role path: include full w/rw width, exclude addr/r."""
    rows=[]
    for i in instructions:
        for m in i['memory']:
            if m['role'] not in ['w','rw']:continue
            if m['base']!=base:raise RuntimeError('unbound write base '+i['pc'])
            if m['size']<=0:raise RuntimeError('invalid write width')
            if m['index'] in [None,'']:
                values=[0]
            elif index_values is not None and m['index'] in index_values:
                values=index_values[m['index']]
                if not values:raise RuntimeError('zero index cases')
            else:raise RuntimeError('unbound write index '+i['pc'])
            for k in values:
                start=m['displacement']+(k*m['scale'] if m['index'] else 0)
                rows.append({'pc':i['pc'],'start':start,'end_exclusive':start+m['size'],'role':m['role']})
    return rows

def protected_hits(spans):
    protected={'id0':(0,2),'active284':(0x284,0x288)}
    return {name:[r for r in spans if r['start']<b and a<r['end_exclusive']]
            for name,(a,b) in protected.items()}

def body(a):return next(r['instructions'] for r in x['ranges'] if int(r['start'],16)==a)
scalar=write_spans(body(0x6c0520),'rcx')
matrix=write_spans(body(0x202c70),'rcx')
indexed=write_spans(body(0x3e5d00),'rcx',{'r8':indices})
if [(r['start'],r['end_exclusive']) for r in scalar] != [(12,16),(0,4),(4,8),(8,12)]:raise RuntimeError('scalar footprint changed')
if [(r['start'],r['end_exclusive']) for r in matrix] != [(0,16),(16,32),(32,48),(48,64)]:raise RuntimeError('matrix footprint changed')
if len(indexed)!=30 or set(q for r in indexed for q in range(r['start'],r['end_exclusive'])) != set(range(0x4c0,0x510)):
    raise RuntimeError('indexed footprint changed')
unchanged({'rcx','ecx','cx','cl','ch'},0x6c0520,0x6c053a)
unchanged({'rcx','ecx','cx','cl','ch'},0x46d110,0x46d11c)
unchanged({'rcx','ecx','cx','cl','ch'},0x3e37e0,0x3e37eb)
unchanged({'rcx','ecx','cx','cl','ch','rdx','edx','dx','dl','dh'},0x202c70,0x202c8f)
unchanged({'rcx','ecx','cx','cl','ch','r8','r8d','r8w','r8b'},0x3e5d0b,0x3e5d2c)
if any(m['role'] in ['w','rw'] for a in [0x46d110,0x3e37e0] for i in body(a) for m in i['memory']):
    raise RuntimeError('unexpected wrapper write')
composed=[]
for definition,call,offset,target in bindings:
    if target==0x3e37e0:
        rows=[{'pc':'0x3e37e6','start':0,'end_exclusive':0x50,'role':'library-fill-contract'}]
    else:rows=scalar if target==0x6c0520 else matrix
    for r in rows:composed.append({**r,'call':hex(call),'start':r['start']+offset,'end_exclusive':r['end_exclusive']+offset})
composed.extend({**r,'call':'0x41fafa'} for r in indexed)
for r in composed:
    if not 0<=r['start']<r['end_exclusive']<=0x740:raise RuntimeError('helper outside record')
if any(protected_hits(composed).values()):raise RuntimeError('helper overlaps protected fields')

caller_body=[i for i in ix.values() if 0x41f730<=int(i['pc'],16)<0x41fbe8]
direct=[];private_stack=[]
for i in caller_body:
    for m in i['memory']:
        if m['role'] not in ['w','rw']:continue
        if m['base']=='rsp' and m['index'] in [None,'']:private_stack.append(i['pc']);continue
        if m['base']!='rbx' or m['index'] not in [None,'']:raise RuntimeError('unbound caller write')
    nonstack={**i,'memory':[m for m in i['memory'] if m['base']!='rsp']}
    direct.extend(write_spans([nonstack],'rbx'))
hits=protected_hits(direct)
if [r['pc'] for r in hits['id0']]!=['0x41f795'] or hits['active284']:
    raise RuntimeError('direct protected-field write census changed')
if any(not 0<=r['start']<r['end_exclusive']<=0x740 for r in direct):raise RuntimeError('direct write outside record')
if any(protected_hits([r for r in direct if int(r['pc'],16)>0x41f795]+composed).values()):
    raise RuntimeError('post-ID effects touch protected field')

result={'producer_complete':True,'method':'A STATIC_ONLY composed original write footprints',
 'driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,
 'source_pins':[{'path':p,'sha256':sha(P/p)} for p in ['source-01.json','retained/source-01.json']],
 'annotation_prerequisites':[roles,parent_roles],'graphs':graphs,
 'new_original_bytes':124,'retained_caller_bytes':0x41fbe8-0x41f730,
 'question':'Can the seven exact caller call sites and all direct post-fill writes establish the clear result at ID0 and active284 without opaque-helper preservation assumptions?',
 'bindings':[{'definition':hex(a),'call':hex(b),'offset':c,'target':hex(d)} for a,b,c,d in bindings],
 'indexed_domain':{'entry_reset':'0x41f9c0','zero_origin':'0x41f775','body':'0x41faf2','call':'0x41fafa','increment':'0x41faff','signed_bound':10,'indices':indices,'method':'Source induction, no execution'},
 'composed_helper_writes':composed,'direct_caller_writes':direct,'direct_protected_hits':hits,
 'private_stack_write_sites':private_stack,
 'established':['6C0520 leaf writes exactly sixteen bytes at RCX, with fifth scalar read at callee RSP+28h. Exact caller RCX binds to record210 and220 without an intervening call/branch/register overwrite. Windows call return-address shift makes caller RSP+20h the fifth scalar source; values not sampled.',
 '46D110 sets RDX=01F204E0 and tails to202C70. Four sequential MOVUPS reads/writes copy64 bytes to each of record180 and1C0. This is copy, not zero-fill; no general overlap safety or live constant binding inferred.',
 '3E5D00 writes WORD/DWORD/WORD totaling eight contiguous bytes at record4C0+8*sign32(EDX). Caller resets EDI from zero ESI, then runs indices0..9, so composed union is4C0..510. Earlier EDI=FFFF is superseded; bound is ten, not sixteen. Floating arithmetic output/exception behavior not established.',
 '3E37E0 supplies EDX=0,R8D=50h and tails to named library fill861EC0. Exact caller RCX is record580, requesting580..5D0 under that contract. No stub or native execution.',
 'All composed helper writes are disjoint from WORD ID0 and DWORD active284. Whole supplied caller direct w/rw spans use full widths; its only post-fill ID write is WORD0=FFFF at41F795, and it has no direct write overlapping284..288.',
 'Given valid private stack/nonaliased readable constants/740h record, normal returns, standard library fill confined to requested span and native ABI nonvolatile preservation, normal return from41F730 leaves ID0=FFFF and active284=0. This replaces the blanket opaque-helper preservation premise for these exact supplied bodies; library effects and validity premises remain explicit.'],
 'affected_claims':['Render-slot identity/publication parent clear premise; OPUS CharacterRenderRecord000/284 initialization','FABLE render allocation/system-clear and rig owner sentinel preconditions'],
 'limits':['No original instructions executed, emulated or forced; no live process/input/screenshot/state observation.',
 'Original local call/body closure only, named861EC0 library semantics/ABI assumed. Native implementation, exceptions, private-frame aliasing, constant accessibility and interference are not independently executed here.',
 'Matrix constant source is original LEA identity, not sampled runtime values or a lifetime guarantee. Sequential copy is not a general overlap-safety proof.',
 'Indexed write address bound is proved for exact caller domain, not arbitrary signed32 index safety or conversion/MXCSR values.',
 'Normal return result is not proof all natural callers initialize or hold a valid row, all writers preserve it, or field reads are atomic. Ownership/reuse, scheduling and lifetime remain open.',
 'Parent source was frozen/publication-ready at retention, not independently accepted. Its immutable lineage remains unchanged after publication.',
 'Independent review/canonical consumption pending; no whole OV row or full L1+L2 goal closure. K14 closed, EXP127 invalid, menu spent/unapproved.'],
 'cleanup':'Offline read-only EXE; only owned disposable evidence writes. No FF12/PC/native instrument/save/config/reference/peer changes.'}
out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
if out.exists():raise RuntimeError('immutable result exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode())
print('PROVED conditional original clear ID/active result and composed helper bounds; STATIC_ONLY')
