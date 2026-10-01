from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence')
s=(W/'spawn_storage_completion_primary.py').read_text();ns={}
exec(compile(s.split('for a in (')[0],'<existing shipping PE reader>','exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={};sources=[];reused=[]
for name in ('primary','dispatch','worker','io','adapters','file'):
 p=W/('spawn-storage-completion-'+name+'.json');j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for b in j['bodies']:
  a=int(b['address'],16);assert a not in cat;cat[a]=b
 sources.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes())))
assert len(cat)==22
for name,addrs in [('spawn-load-success/callbacks.json',[0x580EB0]),('spawn-load-success/restore-callback.json',[0x580840]),('spawn-load-success/boundaries.json',[0x583C00]),('spawn-load-continuation/sequence.json',[0x582860,0x2EF640])]:
 p=E/name;j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for a in addrs:assert a not in cat;cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
 reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[hex(a) for a in addrs]))
assert len(cat)==27
for a,b in cat.items():
 o=ns['off'](a-ns['ib']);d=ns['raw'][o:o+b['bytes']]
 assert len(d)==b['bytes'] and sha(d)==b['sha256']
 fresh=list(ns['md'].disasm(d,a));assert sum(i.size for i in fresh)==len(d) and len(fresh)==len(b['instructions'])
 for i,j in zip(fresh,b['instructions']):assert (hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)==(j['address'],j['bytes'],j['mnemonic'],j['operands'])
ins={int(i['address'],16):i for b in cat.values() for i in b['instructions']}
anchors={
 0x58255B:('cmp','al, 8'),0x58255D:('je','0x5826c1'),0x58256C:('imul','rcx, rax, 0x58'),0x5825C1:('mov','dword ptr [rcx + rbx + 0xdc], r9d'),
 0x5825C9:('cmp','dword ptr [rdx], 8'),0x5825DF:('cmp','ecx, 0x10'),0x5825E2:('jbe','0x5825eb'),0x5825E4:('mov','byte ptr [rbx + 0x39b], r9b'),
 0x58267F:('mov','qword ptr [rcx + rbx + 0x120], rdx'),0x582692:('inc','byte ptr [rbx + 0x398]'),0x5826A4:('call','0x582040'),0x5826B5:('jmp','0x582240'),
 0x582076:('test','byte ptr [rcx + 0xdc], 1'),0x58209C:('jmp','rcx'),0x5820A5:('mov','qword ptr [rbx + 0xc0], rax'),0x5820B2:('mov','dword ptr [rbx + 0xc8], eax'),
 0x58218A:('mov','r9d, dword ptr [rbx + 0x128]'),0x582198:('mov','r8, qword ptr [rbx + 0x120]'),0x58219F:('xor','edx, edx'),0x5821A1:('call','0x3bb440'),0x5821A6:('jmp','0x5820bd'),
 0x58226C:('shr','r8d, 1'),0x58226F:('not','r8d'),0x582278:('mov','byte ptr [rcx + 0x398], al'),0x5822E6:('mov','dword ptr [rcx + rbx + 0xd8], ebp'),
 0x5822F0:('je','0x582395'),0x582307:('call','0x3bb420'),0x58230E:('call','0x17e470'),0x58237F:('mov','r8d, dword ptr [rbx + 0xc8]'),0x582386:('movzx','edx, dil'),0x58238A:('movzx','ecx, sil'),0x58238E:('call','rax'),
 0x582450:('call','0x3bb430'),0x582457:('jne','0x582531'),0x582460:('call','0x582240'),0x582475:('call','0x582040'),0x582485:('call','0x582240'),
 0x3BB447:('mov','r10d, edx'),0x3BB44A:('je','0x3bb44f'),0x3BB44C:('xor','eax, eax'),0x3BB44F:('test','r9d, r9d'),0x3BB452:('je','0x3bb44c'),
 0x3BB477:('mov','qword ptr [rip + 0x2785a72], r8'),0x3BB49C:('mov','qword ptr [rip + 0x278596d], 1'),
 0x3BB7B2:('call','0x862600'),0x3BB810:('call','0x3ba7b0'),0x3BB900:('xor','eax, eax'),
 0x3BA7BF:('ja','0x3ba93d'),0x3BA7D7:('jmp','rdx'),0x3BA801:('call','0x8620d0'),0x3BA831:('call','0x8624d0'),
 0x3BA85B:('jle','0x3ba874'),0x3BA860:('call','0x8625d0'),0x3BA882:('call','0x862590'),0x3BA8C2:('test','ecx, ecx'),0x3BA8C4:('js','0x3ba8e0'),0x3BA8CC:('call','0x8620e0'),
 0x3BA90C:('test','ecx, ecx'),0x3BA90E:('je','0x3ba928'),0x3BA930:('mov','qword ptr [rip + 0x27864dd], rax'),0x3BA937:('mov','dword ptr [rip + 0x27864d3], eax'),
 0x862605:('mov','dword ptr [rdx], 0'),0x862616:('mov','dword ptr [r8], eax'),0x862619:('mov','eax, 1'),
 0x862543:('call','0x8666b0'),0x86254F:('test','rax, rax'),0x862552:('jne','0x86255d'),0x86255F:('mov','dword ptr [rip + 0x264d37b], ebx'),
 0x8625A4:('call','0x866a00'),0x8625A9:('imul','eax, ebx'),0x8625AC:('mov','dword ptr [rip + 0x264d32e], eax'),
 0x8625DF:('call','0x866a80'),0x8625E4:('xor','eax, eax'),0x8625E6:('mov','dword ptr [rip + 0x264d2f4], eax'),
 0x8620F4:('call','0x866200'),0x8620F9:('neg','eax'),0x862106:('sbb','ecx, ecx'),0x862108:('and','ecx, 0xfffffffd'),
 0x866724:('mov','dword ptr [rax], edi'),0x866726:('mov','dword ptr [rax + 4], ebp'),0x8667B8:('cmp','rbp, 4'),0x8667E9:('cmp','rbp, 0xc'),
 0x866805:('cmp','eax, 0x1f'),0x866808:('ja','0x8669d8'),0x866817:('cmp','edx, 0x100000'),0x86685D:('call','0x865d90'),0x866869:('cmp','dword ptr [rsp + 0x60], ecx'),0x8669E0:('mov','rax, r14'),
 0x86623F:('cmp','dword ptr [rcx + 4], ebx'),0x866242:('jne','0x866663'),0x866666:('call','0x19c570'),0x866672:('mov','eax, esi'),
 0x866A42:('cmp','ecx, eax'),0x866A44:('jae','0x866a5c'),0x866A4D:('mov','byte ptr [r10 + rdi], dl'),0x866A54:('inc','dword ptr [r9]'),0x866A61:('cmp','r11d, r8d'),0x866A64:('sete','bl'),
 0x866AB3:('cmp','r9d, eax'),0x866AB6:('jae','0x866abe'),0x866AB8:('mov','dword ptr [rcx], r9d'),
 0x583CCE:('mov','edx, 0x1c4'),0x583CD3:('mov','rcx, qword ptr [rcx + 0x588]'),0x583D31:('jne','0x583ce0'),0x583D4D:('movups','xmmword ptr [rcx + 0x30], xmm1'),
}
for a,v in anchors.items():assert (ins[a]['mnemonic'],ins[a]['operands'])==v,(hex(a),ins[a])
tables=json.loads((W/'spawn-storage-completion-tables.json').read_text())['tables']
for t in tables:
 a=int(t['address'],16);d=bytes.fromhex(t['raw_hex']);o=ns['off'](a-ns['ib'])
 assert ns['raw'][o:o+len(d)]==d and sha(d)==t['sha256'] and len(d)==4*t['count']
 assert [int(r['address'],16) for r in t['targets']]==[x+ns['ib'] for x in struct.unpack('<'+'I'*t['count'],d)]
 assert all(int(r['address'],16) in ins for r in t['targets'])
maps={int(t['address'],16):{r['input']:int(r['address'],16) for r in t['targets']} for t in tables}
assert maps[0x58220C][9]==0x58218A
assert {s:maps[0x3BA944][s] for s in (1,2,6,8,9,15)}=={1:0x3BA7F0,2:0x3BA815,6:0x3BA845,8:0x3BA8C2,9:0x3BA90C,15:0x3BA896}
assert int(ins[0x3BA930]['rip_targets'][0]['address'],16)==0x2B40E14
assert int(ins[0x862610]['rip_targets'][0]['address'],16)==0x2EAF8E0
assert 0x582278<0x5822E6<0x58238E
probe=W/'spawn_storage_short_read_probe.py';execution=json.loads((W/'spawn-storage-short-read-execution.json').read_text());feas=json.loads((W/'spawn-storage-short-read-feasibility.json').read_text())
for receipt,n in [(execution,7),(feas,2)]:
 assert receipt['exe_sha256']==ns['sha'] and receipt['probe_sha256']==sha(probe.read_bytes()) and receipt['stubs']=={} and receipt['live_game'] is False
 assert len(receipt['cases'])==n
 for c in receipt['cases']:
  assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok'] and c['code_unchanged'] and not c['invalid'] and c['error'] is None and all(c['checks'].values())
  assert c['visited'] and c['memory'] and c['boundaries'][0]['entry']=='0x862590'
byname={c['name']:c for c in execution['cases']};short=byname['short-prefix-positive'];full=byname['full-read-positive']
assert short['observed']['result']=='0x0' and short['observed']['cursor']==3
assert short['after']['0x30003000']==b'123'.hex()+'c7'*45
assert full['observed']['result']=='0x8' and full['after']['0x30003000']==b'12345678'.hex()+'c7'*40
assert byname['nonzero-fd-refusal']['observed']['result']=='0xfffffffc'
# Direct contradiction controls: the original trace refutes both proposed shortcuts.
assert any(e[1]=='W' and 0x30003000<=int(e[2],16)<0x30003030 for e in short['memory']), 'zero result did not imply zero effects'
assert short['after']['0x30003000'][6:]==short['before']['0x30003000'][6:], 'short read did not clear its unwritten tail'
failure=json.loads((W/'spawn-storage-short-read-import-failure.json').read_text());assert failure['completed_cases']==0
identity=json.loads((W/'spawn-storage-short-read-tool-identity.json').read_text());assert identity['unicorn_version']==execution['unicorn_version'] and identity['loaded_dlls']
out=dict(exe_sha256=ns['sha'],checks='pass',method='A source and conditional composition; B only two original memory-reader functions',collected_bodies=22,reused_bodies=5,sources=sources,reused=reused,
 bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],anchors=[ins[a] for a in anchors],tables=tables,
 B=dict(cases=7,feasibility_cases=2,executed_bodies=execution['bodies'],probe_sha256=execution['probe_sha256'],unicorn_version=execution['unicorn_version'],
 reads=sum(e[1]=='R' for c in execution['cases'] for e in c['memory']),writes=sum(e[1]=='W' for c in execution['cases'] for e in c['memory']),
 counterclaims_rejected=['zero result means no destination writes','short read clears the remaining destination']),
 limits='No native file open/decode/close executed; no live callback/initialized-state proof. Short read becoming parent success is conditional A composition. Import failure remains zero-case NOT RUN. Existing emulator accessed through supported sandbox escalation, no package changes.')
(W/'spawn-storage-completion-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:27 exact A bodies, two original tables;7 B cases plus2 feasibility controls, no stubs; reads/writes',out['B']['reads'],out['B']['writes'])
