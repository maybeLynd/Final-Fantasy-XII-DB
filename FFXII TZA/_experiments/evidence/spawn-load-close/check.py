from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence')
s=(W/'spawn_load_close_primary.py').read_text();ns={}
exec(compile(s.split('for a in (')[0],'<existing verified shipping PE reader>','exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={};sources=[]
for name in ('primary','helpers','context','controller','request','screen-close','factory','admission'):
 p=W/('spawn-load-close-'+name+'.json');j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for b in j['bodies']:
  a=int(b['address'],16);assert a not in cat;cat[a]=b
 sources.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[b['address'] for b in j['bodies']]))
assert len(cat)==17
reused=[]
for name,addresses in [
 ('spawn-load-continuation/sequence.json',[0x582860,0x2EF640]),
 ('spawn-restore-request/support.json',[0x285E60]),
 ('spawn-restore-request/callers.json',[0x280140]),
 ('spawn-widget-hierarchy/helpers.json',[0x583930]),
 ('spawn-widget-teardown/primary.json',[0x244F00,0x244DD0,0x245020]),
]:
 p=E/name;j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for a in addresses:
  assert a not in cat;cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
 reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[hex(a) for a in addresses]))
assert len(cat)==25
for a,b in cat.items():
 pos=a;data=b''
 for i in b['instructions']:
  assert int(i['address'],16)==pos
  d=bytes.fromhex(i['bytes']);data+=d;pos+=len(d)
 o=ns['off'](a-ns['ib'])
 assert data==ns['raw'][o:o+len(data)] and len(data)==b['bytes'] and sha(data)==b['sha256'],hex(a)
instructions={int(i['address'],16):i for b in cat.values() for i in b['instructions']}
def at(a):return instructions[a]
anchors={
 0x27F55A:('cmp','qword ptr [rax + 0x100], 0'),0x27F562:('jne','0x27f5bc'),
 0x27F5AB:('mov','ecx, 0xf0'),0x27F5B7:('call','0x244f50'),
 0x27F738:('mov','qword ptr [rax + 0x100], rbx'),0x27F741:('and','eax, 0x7fff'),
 0x27F746:('mov','dword ptr [rbx + 0xd0], eax'),0x27F74F:('mov','dword ptr [rbx + 0xd4], eax'),
 0x27F85B:('cmp','ecx, 0x13'),0x27F85E:('je','0x27f8b4'),
 0x27F8BA:('add','eax, -2'),0x27F8BD:('cmp','eax, 0x14'),0x27F8C0:('ja','0x27fa31'),
 0x27F8CF:('mov','ecx, dword ptr [rdx + rax*4 + 0x15fad0]'),
 0x27F8DB:('cmp','dword ptr [rbx + 0xd4], 0'),0x27F8E2:('jne','0x27f974'),
 0x27F8E8:('call','0x3c60f0'),0x27F8F4:('jne','0x27f974'),
 0x27F953:('call','0x5844a0'),0x27F96D:('call','0x20e5c0'),0x27F974:('call','0x584490'),
 0x27F979:('mov','ecx, dword ptr [rbx + 0xd4]'),0x27F97F:('mov','edx, 1'),0x27F984:('call','0x583930'),
 0x583958:('test','edx, edx'),0x583966:('setne','r8b'),0x58396A:('mov','qword ptr [rsp + 0x30], r8'),
 0x5828E5:('cmp','qword ptr [rsi + 0x10], 1'),0x5828F1:('cmove','eax, ecx'),0x5828FE:('mov','dword ptr [rbx + 0xc4], eax'),
 0x582CB3:('or','dword ptr [rbx + 0xc4], 0x10'),0x582CD0:('call','0x285e60'),0x582CE6:('call','0x285e60'),
 0x285E6B:('or','dword ptr [rax + 0x400], 0x200'),0x285E7C:('or','dword ptr [rax + 0x400], 0x400'),
 0x582E81:('test','byte ptr [rbx + 0xc4], 0x10'),0x582E88:('je','0x582ebf'),
 0x582E8A:('cmp','byte ptr [rbx + 0x598], 0'),0x582E91:('jne','0x582eac'),
 0x582E93:('call','0x1831a0'),0x582EA2:('call','0x5843e0'),0x582EA7:('call','0x182d40'),
 0x582EBA:('call','0x584210'),0x582EC2:('call','0x582fc0'),
 0x582EF9:('test','byte ptr [rbx + 0xc4], 8'),0x582F07:('je','0x582f13'),
 0x582F09:('mov','ecx, 0xfffffffe'),0x582F0E:('call','0x2814e0'),
 0x2814FB:('cmp','ebx, -2'),0x2814FE:('je','0x28153c'),0x281543:('mov','rcx, qword ptr [rax + 0x100]'),
 0x28154D:('je','0x2818e9'),0x281558:('jmp','0x244f00'),
 0x281500:('cmp','ebx, -1'),0x281537:('jmp','0x27f2e0'),
 0x244F0A:('or','dword ptr [rcx + 0x40], 0x40'),0x244F19:('jne','0x244f25'),
 0x244F20:('jmp','0x244dd0'),0x244F34:('call','rax'),0x244F39:('call','0x245020'),
 0x244E41:('jne','0x244ef7'),0x244EF5:('call','rax'),
 0x27F616:('cmp','ecx, 0xd'),0x27F61F:('test','byte ptr [rbx + 0x40], 0x40'),
 0x27F623:('je','0x27faa9'),0x27F637:('call','0x295ce0'),0x27F63C:('call','0x27f2e0'),
 0x27F84F:('mov','qword ptr [rax + 0x100], rsi'),
 0x27F2F2:('test','dword ptr [rax + 0x400], 0x800'),0x27F301:('cmovne','ebx, eax'),
 0x27F306:('call','0x2c98c0'),0x27F30B:('call','0x250f30'),0x27F312:('call','0x2cc960'),
 0x27F324:('bt','eax, 9'),0x27F328:('jae','0x27f33b'),0x27F32A:('bt','eax, 0xa'),
 0x27F32E:('setb','al'),0x27F331:('inc','al'),0x27F333:('mov','byte ptr [rcx + 0x400], al'),
 0x27F33B:('mov','byte ptr [rcx + 0x400], 2'),0x27F349:('and','dword ptr [rax + 0x400], 0xfffff7ff'),
 0x280446:('add','rax, 0x3f8'),0x28044C:('mov','qword ptr [rbx + 0xc0], rax'),
 0x2802BB:('movzx','eax, byte ptr [rcx + 8]'),0x2802BF:('sub','eax, 1'),0x2802C8:('cmp','eax, 1'),
 0x2802CB:('jne','0x2803d0'),0x280335:('call','0x245020'),0x28033A:('mov','rax, qword ptr [rbx + 0xc0]'),
 0x2801E4:('bt','eax, 9'),0x2801E8:('jae','0x280248'),0x2801FF:('call','0x268320'),0x28021F:('call','0x267c90'),
 0x233C23:('jne','0x233c4d'),0x233C25:('call','0x2ef640'),0x233C2A:('add','rax, 0x4e68c'),
 0x233C3A:('call','0x30b6a0'),0x233C3F:('call','0x237df0'),0x233C48:('jmp','0x237df0'),
 0x233C4D:('cmp','dword ptr [rax], 0x5071901'),0x233C53:('je','0x233c5e'),0x233C59:('jmp','0x237df0'),
 0x233C6E:('or','dword ptr [rax + 4], 0x1000'),0x233CA6:('and','dword ptr [rax + 4], 0xffffefff'),
 0x2CFD14:('xor','r8d, r8d'),0x2CFD17:('lea','edx, [r8 + 4]'),0x2CFD1B:('lea','ecx, [rdx + 2]'),
 0x2CFD1E:('call','0x2527b0'),0x2CFD27:('jmp','0x28e880'),
 0x5830E7:('sub','eax, 2'),0x5830EA:('test','eax, 0xfffffffd'),0x5830EF:('cmove','ebx, r14d'),
 0x5830F5:('cmp','edi, 0xc8'),0x5830FB:('jl','0x5830c6'),
 0x58311D:('call','0x244f00'),0x583156:('je','0x58321a'),
 0x583211:('mov','byte ptr [rsi + 0xc0], 4'),0x58321F:('call','0x583990'),
 0x58322A:('call','0x57ec60'),0x58322F:('mov','byte ptr [rsi + 0xc0], 3'),
 0x247583:('mov','qword ptr [rcx + 0x48], rax'),0x1E0F24:('call','0x198790'),0x1E0F30:('jmp','0x1986d0'),
 0x2527B7:('sub','ecx, 6'),0x2527BA:('je','0x252810'),0x252820:('mov','eax, 0x1f'),
 0x252827:('cmovg','edx, eax'),0x25282D:('mov','word ptr [r9 + rax*2 + 0x30], r8w'),
 0x28E88A:('je','0x28e8a0'),0x28E88C:('add','rcx, 0xaa60'),0x28E895:('mov','r8d, 0xc4'),
 0x28E89B:('jmp','0x861ec0'),0x57ECD7:('mov','qword ptr [rax + 0xc8], r9'),
 0x57ECFC:('mov','dword ptr [rsp + 0x30], eax'),0x57ED00:('call','0x582540'),
 0x2281DE:('and','dword ptr [rbx + 0x40], 0xffffffdf'),0x228251:('call','0x245020'),
 0x228258:('mov','dword ptr [rbx + 0xcc], 0'),0x285EB0:('and','ecx, 0x2000'),
 0x285EC7:('or','dword ptr [rax + 0x400], 0x100'),0x285ED8:('mov','dword ptr [rax + 0x3fc], ecx'),
}
for a,want in anchors.items():assert (at(a)['mnemonic'],at(a)['operands'])==want,(hex(a),at(a))
rips={0x27F5B0:0x27F5D0,0x27F731:0x209AC30,0x27F8C6:0x120000,0x58395A:0x582860,
 0x582899:0x120000,0x582E98:0x209AC10,0x28153C:0x209AC30,
 0x244F2D:0x915058,0x244EEB:0x1E0C0F8,0x27F317:0x209AC30,0x27F342:0x209AC30,
 0x28043F:0x209AC30,0x233C33:0x2EBF190}
for a,t in rips.items():assert int(at(a)['rip_targets'][0]['address'],16)==t
table=json.loads((W/'spawn-load-close-tables.json').read_text());assert table['exe_sha256']==ns['sha']
o=ns['off'](0x27FAD0-ns['ib']);data=ns['raw'][o:o+84]
assert data.hex()==table['raw_hex'] and sha(data)==table['sha256']
targets=[ns['ib']+v for v in struct.unpack('<21I',data)]
assert len(table['rows'])==21 and all(int(r['target'],16)==targets[i] and r['request']==i+2 for i,r in enumerate(table['rows']))
assert targets[4]==0x27F8DB and targets[0]==0x27F9C1 and targets[19]==0x27FA31
assert [i+2 for i,t in enumerate(targets) if t==0x27F8DB]==[6]
constants=[]
for a,n in [(0x582F54,76),(0x915058,24),(0x1E0C0F8,24)]:
 o=ns['off'](a-ns['ib']);d=ns['raw'][o:o+n]
 constants.append(dict(address=hex(a),bytes=n,raw_hex=d.hex(),sha256=sha(d)))
 if a==0x582F54:
  ts=[ns['ib']+v for v in struct.unpack('<19I',d)]
  assert ts[0]==0x5828AC and ts[11]==0x582B2C and ts[17]==0x582E81
 else:assert struct.unpack('<QQQ',d)==(15,0,0)
# Positive/alternate-path controls are actual branches and table rows. No
# reconstructed model, synthetic state or original instructions are executed.
assert 0x582EA2<0x582EBA<0x582F0E
assert int(at(0x582E88)['operands'],16)>0x582EBA
assert int(at(0x582E91)['operands'],16)>0x582EA2
assert int(at(0x582F07)['operands'],16)>0x582F0E
assert at(0x27F328)['mnemonic']=='jae' and at(0x27F32E)['mnemonic']=='setb'
correction=dict(kind='Rejected search invocation, not an evidence result',
 invalid_command='Repeated --addr flags with argparse nargs=* retained only the last address 00247570.',
 original_output=(W/'spawn-load-close-existing.txt').read_text(),
 corrective_command='Single --addr followed by all nine addresses.',
 corrected_output=(W/'spawn-load-close-existing-corrected.txt').read_text(),
 consequence='The initial no-existing-coverage headline is invalid for this package; existing router and save-map findings are explicitly reused.')
assert '27F5D0' in correction['corrected_output'] and 'version-stamps' in correction['corrected_output']
(W/'spawn-load-close-search-correction.json').write_text(json.dumps(correction,indent=2)+'\n',encoding='utf-8',newline='\n')
out=dict(exe_sha256=ns['sha'],method='A only; no original instructions executed',checks='pass',
 collected_complete_bodies=17,reused_complete_bodies=8,sources=sources,reused=reused,
 bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],
 anchors=[at(a) for a in anchors],rip_anchors=[at(a) for a in rips],constants=constants,request_table=table,
 conclusion='Request6 can build a load controller with C4 bit3. Its admitted18 restoration/normalization precedes 2814E0(-2), which requests closure of context+100; admitted15 invokes27F2E0. With the same context and preserved bits9/10, the latter writes state2 consumed by280140. Close alone does not prove restore.',
 limits='Conditional original-code call order only. Native callbacks, reentrancy/context replacement, actual successful I/O and initialized normal gameplay remain unproved. No complete context-writer census; other producers can write state2. L12/L13 and peer consumer review remain open.')
(W/'spawn-load-close-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:17 collected/8 reused whole shipping bodies; request6 and alternate table controls, restore/close gates, message15 bytes and context-state linkage. Method A only.')
