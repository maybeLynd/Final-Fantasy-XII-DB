"""Native root retention and resource message16 order, method A only."""
from pathlib import Path
import hashlib,json
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence');ns={}
s=(W/'spawn_widget_retention_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x2445D0')],'<existing PE reader>','exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={int(b['address'],16):b for name in ('primary','helpers','adapters')
     for b in json.loads((W/('spawn-widget-retention-'+name+'.json')).read_text())['bodies']}
assert len(cat)==13
reused=[]
for name,addresses in (
 ('spawn-widget-hierarchy/primary.json',[0x248220]),
 ('spawn-widget-hierarchy/linkage.json',[0x2465F0,0x582790]),
 ('spawn-widget-hierarchy/roots.json',[0x247AE0]),
 ('spawn-widget-teardown/primary.json',[0x245020,0x2482E0]),
 ('spawn-widget-teardown/helpers.json',[0x2473F0]),
 ('spawn-load-continuation/sequence.json',[0x582860]),
):
 p=E/name;j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for a in addresses:cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
 reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[hex(a) for a in addresses]))
assert len(cat)==21
for a,b in cat.items():
 pos=a;data=b''
 for i in b['instructions']:
  assert int(i['address'],16)==pos
  d=bytes.fromhex(i['bytes']);data+=d;pos+=len(d)
 o=ns['off'](a-ns['ib'])
 assert data==ns['raw'][o:o+len(data)] and len(data)==b['bytes'] and sha(data)==b['sha256']
def at(a):return next(i for b in cat.values() for i in b['instructions'] if int(i['address'],16)==a)
anchors={
 0x2445D0:('cmp','dword ptr [rdx], 1'),0x2445D8:('or','dword ptr [rcx + 0x40], 0x23'),
 0x2445E1:('mov','dword ptr [rcx + 0xc0], eax'),0x24460A:('xor','eax, eax'),
 0x2418E0:('and','dword ptr [rcx + 0x40], 0xffffffdf'),0x2418EA:('or','dword ptr [rcx + 0x40], edx'),
 0x2463FF:('mov','rbx, qword ptr [rcx + 0x18]'),0x24640C:('call','rsi'),
 0x246429:('call','0x2463f0'),0x24642E:('mov','rbx, qword ptr [rbx + 0x20]'),
 0x248271:('or','dword ptr [rdx + 0x40], 0x20'),0x2482A0:('call','0x2463f0'),
 0x245072:('test','byte ptr [rdi + 0x40], 0x20'),0x24508C:('call','0x2473f0'),
 0x2474AE:('je','0x2474f6'),0x2474B7:('je','0x2474f6'),
 0x2474C2:('mov','dword ptr [rcx + 0x40], eax'),0x2474D0:('call','rax'),
 0x2474E8:('call','0x247490'),0x2474ED:('mov','rbx, qword ptr [rbx + 0x20]'),
 0x24959B:('cmp','edx, 0xc'),0x2495B0:('mov','qword ptr [rax + 0x18], rdx'),
 0x2495B4:('or','dword ptr [rax], 1'),0x2495B7:('mov','qword ptr [rax + 8], rcx'),
 0x249425:('or','dword ptr [rcx], 2'),0x249438:('jne','0x249482'),
 0x249440:('call','qword ptr [rcx + 0x10]'),0x24945D:('mov','dword ptr [rsp + 0x20], 0x10'),
 0x24947D:('call','rax'),0x24947F:('and','dword ptr [rbx], 0xfffffffe'),
 0x24950C:('inc','word ptr [rcx + 0x1a]'),0x24951D:('jne','0x249567'),
 0x249525:('call','qword ptr [rcx + 0x10]'),0x249562:('call','rax'),
 0x249564:('and','dword ptr [rbx], 0xfffffffe'),
 0x2495D9:('movsxd','rbx, ecx'),0x2495E8:('call','rax'),
 0x2495EA:('mov','rdi, qword ptr [rbx]'),0x2495ED:('inc','word ptr [rdi + 0x1a]'),
 0x249606:('call','qword ptr [rdi + 0x10]'),0x249632:('call','rax'),
 0x249634:('and','dword ptr [rdi], 0xfffffffe'),0x249637:('and','dword ptr [rbx + 0x20], 0xfffffffe'),
 0x24924C:('cmp','eax, 0x30'),0x249286:('mov','dword ptr [rsp + 0x38], ebx'),
 0x24928D:('mov','qword ptr [rbx], rbp'),0x2492F3:('call','0x32e620'),
 0x2492F8:('inc','word ptr [rbp + 0x18]'),0x249332:('call','0x249210'),
 0x24933E:('mov','qword ptr [rax + 0x10], rcx'),0x2493DE:('call','0x249210'),
 0x2493FF:('mov','qword ptr [rbx + 0x10], rcx'),
 0x58279D:('call','0x249580'),0x5827BC:('call','0x393460'),
 0x5827D8:('call','0x3933f0'),0x582850:('jmp','0x249410'),
 0x5829B1:('mov','rcx, rbx'),0x5829B4:('call','0x582790'),0x582A14:('call','0x244960'),
}
for a,want in anchors.items():
 i=at(a);assert (i['mnemonic'],i['operands'])==want,(hex(a),i)
for a,want in ((0x249580,0x2090790),(0x249274,0x2495C0),(0x249337,0x249660),
               (0x2493F4,0x249670),(0x248296,0x2418E0),(0x247D93,0x2445D0)):
 assert int(at(a)['rip_targets'][0]['address'],16)==want
assert not any(i['mnemonic'] in ('call','jmp') for i in cat[0x2445D0]['instructions'])
# Both filtered recursion gates jump past the child recursion; ordinary tree
# callback traversal has no analogous self-state gate. This is static control flow.
assert int(at(0x2474AE)['operands'],16)>0x2474E8 and int(at(0x2474B7)['operands'],16)>0x2474E8
out=dict(exe_sha256=ns['sha'],method='A only; no instructions executed',checks='pass',
 new_complete_bodies=13,reused_complete_bodies=8,anchors=[at(a) for a in anchors],reused=reused,
 bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],
 conclusions='Root message1 sets bits0/1/5; attachment propagates5. Filtered247490 prunes whole subtrees on failed selfgate. Native batch completion invokes16 before freeing its slot; member callback precedes completed count.',
 limits='No live root or load sequence, no native resource materialization/allocator execution, no error-success inference from equal counts. Custom callback ABI differs at2495C0; do not assume RCX=batch there.')
(W/'spawn-widget-retention-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:13 new/8 reused shipping bodies; root flag inheritance, pruned traversal and batch16 call/write order. NoB/live.')
