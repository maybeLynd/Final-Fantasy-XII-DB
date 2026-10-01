"""Shipping generation/reclamation and notification controls; no execution."""
from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence');ns={}
s=(W/'spawn_widget_reclaim_primary.py').read_text();exec(compile(s[:s.index('for a in (0x248030')],'<existing PE reader>','exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={int(b['address'],16):b for b in json.loads((W/'spawn-widget-reclaim-primary.json').read_text())['bodies']}
assert len(cat)==6;reused=[]
for name,addresses in [('spawn-widget-hierarchy/roots.json',[0x250540]),('spawn-widget-teardown/primary.json',[0x245020]),('spawn-widget-hierarchy/linkage.json',[0x2465F0])]:
 p=E/name;j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for a in addresses:cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
 reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[hex(a) for a in addresses]))
assert len(cat)==9
for a,b in cat.items():
 pos=a;data=b''
 for i in b['instructions']:
  assert int(i['address'],16)==pos
  d=bytes.fromhex(i['bytes']);data+=d;pos+=len(d)
 o=ns['off'](a-ns['ib']);assert data==ns['raw'][o:o+len(data)] and len(data)==b['bytes'] and sha(data)==b['sha256']
def at(a):return next(i for b in cat.values() for i in b['instructions'] if int(i['address'],16)==a)
anchors={
 0x248044:('call','0x1edda0'),0x248050:('mov','dword ptr [rbx + 0xb4], r15d'),
 0x248059:('inc','dword ptr [r14 + 0xb4]'),0x24807E:('cmp','eax, edx'),
 0x248080:('je','0x248113'),0x248086:('bt','ecx, 0xa'),0x24808A:('jae','0x2480db'),
 0x24808C:('mov','rdi, qword ptr [rbx + 0x20]'),0x248093:('mov','rsi, qword ptr [rbx + 0x10]'),
 0x248097:('call','0x2482e0'),0x2480DB:('or','ecx, 4'),
 0x2480E1:('bt','ecx, 0x12'),0x2480E5:('jb','0x248101'),0x2480F9:('call','rax'),
 0x248101:('and','dword ptr [rbx + 0x40], 0xfffdffff'),0x24810A:('and','eax, 1'),
 0x248110:('or','dword ptr [rbx + 0x40], eax'),0x248127:('je','0x248142'),
 0x248156:('jne','0x248129'),0x248158:('mov','rbx, qword ptr [rbx + 0x10]'),
 0x2481A0:('xor','dword ptr [rip + 0x1e46bb5], 1'),
 0x2481D6:('je','0x248210'),0x2481DB:('je','0x248210'),0x2481E1:('jb','0x2481fe'),
 0x2481E3:('mov','rax, qword ptr [rax + 0x10]'),0x2481FB:('jmp','rax'),0x24820D:('jmp','rax'),
 0x249660:('mov','rcx, qword ptr [rcx + 8]'),0x249664:('jmp','0x2a00f0'),
 0x249670:('mov','rdx, qword ptr [rcx + 8]'),0x249674:('mov','rcx, qword ptr [rcx + 0x18]'),
 0x249678:('jmp','0x24a1d0'),0x245097:('bts','eax, 0xa'),
 0x250617:('call','0x2481a0'),0x25063A:('call','0x248030'),
 0x250661:('call','0x248190'),0x250666:('call','0x2481c0'),0x25067F:('call','0x244970'),
 0x246659:('cmp','dword ptr [rip + 0x1e48f00], 0'),
 0x246665:('and','eax, 1'),0x246668:('shl','eax, 0x11'),0x24666B:('xor','eax, ecx'),
 0x24666D:('mov','dword ptr [rdi + 0x40], eax'),
}
for a,want in anchors.items():
 i=at(a);assert (i['mnemonic'],i['operands'])==want,(hex(a),i)
rips={0x248060:0x208ED5C,0x2480FB:0x208ED5C,0x248190:0x208F560,
      0x2481A0:0x208ED5C,0x2481A7:0x208F560,0x2481C0:0x208EBC0,
      0x2480EF:0x915108,0x2481F4:0x9150D8,0x248206:0x9150F0}
for a,t in rips.items():assert int(at(a)['rip_targets'][0]['address'],16)==t
c=json.loads((W/'spawn-widget-reclaim-constants.json').read_text());assert c['exe_sha256']==ns['sha']
for r in c['records']:
 a=int(r['address'],16);data=bytes.fromhex(r['raw_hex']);o=ns['off'](a-ns['ib'])
 assert data==ns['raw'][o:o+len(data)]
 assert struct.unpack('<QQQ',data)==({0x915108:2,0x9150D8:10,0x9150F0:11}[a],0,0)
assert len(c['records'])==3
# BT puts the tested bit in CF. JB skips the handler when bit18 is set;
# JAE chooses the non-release branch when bit10 is clear. These are opposite
# branch polarities in the same complete body, not a self-fixture comparison.
assert at(0x2480E5)['mnemonic']=='jb' and int(at(0x2480E5)['operands'],16)>0x2480F9
assert at(0x24808A)['mnemonic']=='jae' and int(at(0x24808A)['operands'],16)>0x248097
assert not any(i['operands']=='0x2482e0' for i in cat[0x2481C0]['instructions'])
out=dict(exe_sha256=ns['sha'],method='A only; no instructions executed',checks='pass',new_complete_bodies=6,reused_complete_bodies=3,
 bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],anchors=[at(a) for a in anchors],
 rip_anchors=[at(a) for a in rips],constants=c['records'],reused=reused,
 conclusions='Generation mismatch gates bit10 release; bit18 SET suppresses message2. After normal notification generation bit17 is replaced with currentglobal lowbit.2481C0 sends focus10/11 and isnot release.',
 review_correction='Draft described constructor phase as flipping its generation seed. Exact246665..66D XORs the same global-derived bit with the already seeded bit, forcing bit17 zero during208F560!=0. This is not logical inversion for global0. Corrected before publication; no execution is implied.',
 limits='No live scheduling, synthetic tree execution, nativecallback effects, actual load message18 chronology or materialization in2A00F0/24A1D0.')
(W/'spawn-widget-reclaim-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:6 new/3 reused shipping bodies, opposite bit10/18 branch controls, phase/order and2/10/11 message bytes. NoB/live.')
