from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence')
s=(W/'spawn_load_success_helpers.py').read_text();ns={}
exec(compile(s.split('for a in (')[0],'<existing shipping PE reader>','exec'),ns)
sha=lambda d:hashlib.sha256(d).hexdigest()
cat={};sources=[];reused=[]
for name in ('primary','helpers','callbacks','restore-callback','boundaries','selection'):
 p=W/('spawn-load-success-'+name+'.json');j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for b in j['bodies']:
  a=int(b['address'],16);assert a not in cat;cat[a]=b
 sources.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes())))
assert len(cat)==18
for name,addrs in [
 ('spawn-load-continuation/sequence.json',[0x582860,0x2EF640]),
 ('spawn-load-close/primary.json',[0x583040]),
 ('spawn-restore-request/support.json',[0x285E60]),
 ('spawn-widget-teardown/primary.json',[0x244F00,0x244DD0,0x245020]),
]:
 p=E/name;j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for a in addrs:
  assert a not in cat;cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
 reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[hex(a) for a in addrs]))
assert len(cat)==25
for a,b in cat.items():
 o=ns['off'](a-ns['ib']);d=ns['raw'][o:o+b['bytes']]
 assert sha(d)==b['sha256'] and b''.join(bytes.fromhex(i['bytes']) for i in b['instructions'])==d
 fresh=list(ns['md'].disasm(d,a));assert sum(i.size for i in fresh)==len(d) and len(fresh)==len(b['instructions'])
 for i,j in zip(fresh,b['instructions']):
  assert (hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)==(j['address'],j['bytes'],j['mnemonic'],j['operands'])
allins={int(i['address'],16):i for b in cat.values() for i in b['instructions']}
anchors={
 0x247523:('mov','dword ptr [rsp + 0x20], 0xc'),0x24752B:('mov','qword ptr [rsp + 0x28], rdx'),
 0x247530:('mov','qword ptr [rsp + 0x30], r8'),0x247547:('call','rax'),0x24755B:('xor','eax, eax'),
 0x57F3DC:('cmp','qword ptr [rdx + 8], 0x1d'),0x57F3EB:('cmp','dword ptr [rdx], 0xd'),
 0x57F48E:('mov','edx, 0x1d'),0x57F493:('call','0x247510'),0x57F49B:('call','0x244f00'),
 0x57F4A0:('mov','ecx, dword ptr [rdi + 0xe8]'),0x57F4BF:('mov','byte ptr [rdi + 0xcc], 5'),
 0x57F6CB:('cmp','dword ptr [rdx + 8], 1'),0x57F6D2:('ja','0x57f774'),
 0x57F759:('mov','qword ptr [rsp + 0x68], r8'),0x57F75E:('mov','dword ptr [rsp + 0x70], 0xa0'),
 0x57F636:('mov','ebx, r8d'),0x57F639:('cmp','ecx, 0xa'),0x57F661:('mov','dword ptr [rbx + 0xe8], edx'),
 0x57F66E:('call','0x57f280'),0x57F677:('mov','byte ptr [rbx + 0xcc], 3'),0x57F695:('mov','byte ptr [rbx + 0xcc], 4'),
 0x57F2B3:('mov','rax, qword ptr [rdi + 0xd8]'),0x57F2BA:('shl','rcx, 5'),0x57F2BE:('cmp','dword ptr [rcx + rax + 4], 0'),
 0x57F29D:('jge','0x57f2d5'),0x57F2D5:('jne','0x57f2ed'),
 0x57F30B:('mov','dword ptr [rsp + 0x20], 6'),0x57F338:('mov','dword ptr [rsp + 0x6c], 4'),
 0x57FE92:('cmp','eax, 0x11'),0x57FE95:('ja','0x5807ac'),0x57FEAF:('jmp','rax'),
 0x580433:('mov','rax, qword ptr [rdx + 0x10]'),0x580437:('movzx','edi, byte ptr [rax + rcx + 0xef]'),
 0x5804A8:('cmp','eax, 3'),0x5804BC:('cmp','eax, 0xd'),0x5804D0:('cmp','eax, 0xf'),
 0x58050C:('movzx','edi, byte ptr [rax + rcx + 0xef]'),0x58052A:('mov','byte ptr [rcx + 0x598], dil'),
 0x58053A:('mov','byte ptr [rbx + 0xeb], dil'),0x58063B:('ja','0x580750'),0x58064F:('jmp','rcx'),
 0x5806CC:('or','dword ptr [rbx + 0xe0], 0x10'),0x5806D6:('call','0x244f00'),
 0x58078B:('mov','edx, 0x12'),0x580797:('mov','r8d, 4'),0x58079D:('call','0x247510'),
 0x580847:('mov','ebx, r8d'),0x58084C:('test','byte ptr [rbx + 0xe0], 0x10'),0x580853:('jne','0x580907'),
 0x58085E:('cmp','ecx, 9'),0x580861:('jne','0x5809d3'),0x5808AD:('test','ebp, ebp'),0x5808AF:('je','0x5808c1'),
 0x5808B1:('cmp','ebp, 8'),0x5808B4:('jne','0x5808bb'),0x5808C8:('test','esi, esi'),0x5808CA:('jne','0x58090e'),
 0x5808CC:('test','r14d, r14d'),0x5808CF:('jne','0x58090e'),0x5808DD:('mov','edx, 0x10'),
 0x5808E2:('lea','r8d, [rdx - 0xc]'),0x5808E6:('call','0x247510'),0x5808EE:('mov','dl, 9'),0x5808F3:('call','0x580eb0'),
 0x580921:('call','0x583c00'),0x5809B0:('mov','r8d, 0xa'),0x5809B6:('mov','dl, 0xe'),
 0x5809C6:('mov','r8d, 6'),0x5809CC:('mov','dl, 0xd'),0x5809D3:('cmp','ecx, 0xc'),
 0x580A1F:('and','dword ptr [rbx + 0xe0], 0xfffffffe'),0x580A26:('or','dword ptr [rbx + 0xe0], 8'),0x580A35:('mov','dl, 0xc'),
 0x580EE2:('cmp','byte ptr [rcx + 0xe9], dl'),0x580EE8:('je','0x58124d'),
 0x58109E:('lea','rax, [rip - 0x865]'),0x5810B4:('mov','dword ptr [rbp - 0x39], ebx'),
 0x5810EA:('mov','dword ptr [rbp - 0x49], 9'),0x581113:('mov','qword ptr [rbp - 1], rsi'),
 0x581117:('mov','dword ptr [rbp + 7], 0x56690'),0x58111E:('call','0x582540'),
 0x581141:('mov','dil, 0x17'),0x581232:('call','0x583990'),0x581246:('mov','byte ptr [rbx + 0xe9], r15b'),
 0x582CB3:('or','dword ptr [rbx + 0xc4], 0x10'),0x582CD0:('call','0x285e60'),0x582CE6:('call','0x285e60'),
 0x582CF2:('cmp','qword ptr [rdx + 0x10], 4'),0x582D04:('call','0x581310'),0x582D19:('call','0x244f00'),
 0x582C41:('mov','qword ptr [rbx + 0xd8], rdi'),0x582C77:('call','0x244f00'),
 0x582E8A:('cmp','byte ptr [rbx + 0x598], 0'),0x582E91:('jne','0x582eac'),0x582EA2:('call','0x5843e0'),0x582EBA:('call','0x584210'),
 0x5831CC:('mov','byte ptr [rsp + 0x40], al'),0x5831FC:('mov','qword ptr [rsp + 0x30], rsi'),0x58320A:('mov','qword ptr [rsi + 0xd8], rax'),
 0x583C1E:('mov','edx, 0x1c4'),0x583C23:('mov','rcx, qword ptr [rcx + 0x588]'),
 0x583C30:('lea','rax, [rax + 0x80]'),0x583C7D:('sub','rdx, 1'),0x583C81:('jne','0x583c30'),0x583C9D:('movups','xmmword ptr [rax + 0x30], xmm1'),
}
for a,v in anchors.items():assert (allins[a]['mnemonic'],allins[a]['operands'])==v,(hex(a),allins[a])
tables=json.loads((W/'spawn-load-success-state-tables.json').read_text())['tables']
selection=cat[0x57FE80]['extent_proof'];tables+=selection['tables']
pd=next(s for s in ns['sections'] if s['name']=='.pdata')
pdbytes=ns['raw'][pd['disk_offset']:pd['disk_offset']+pd['raw_bytes']]
for r in selection['records']:
 d=bytes.fromhex(r['unwind_raw']);o=ns['off'](int(r['unwind'],16)-ns['ib'])
 assert ns['raw'][o:o+len(d)]==d
 triple=bytes.fromhex(r['runtime_function_raw'])
 assert any(pdbytes[k:k+12]==triple for k in range(0,len(pdbytes)-11,12))
for t in tables:
 a=int(t['address'],16);d=bytes.fromhex(t['raw_hex']);o=ns['off'](a-ns['ib'])
 assert ns['raw'][o:o+len(d)]==d and sha(d)==t['sha256'] and len(d)==4*t['count']
 targets=[int(x['address'],16) for x in t['targets']]
 assert targets==[ns['ib']+x for x in struct.unpack('<'+'I'*t['count'],d)]
 assert all(x in allins for x in targets)
maps={int(t['address'],16):{r['input']:int(r['address'],16) for r in t['targets']} for t in tables}
assert maps[0x5807B8][12]==0x580401 and maps[0x5807B8][18]==0x58078B
assert maps[0x580800][9]==0x5806CC and maps[0x581268][8]==0x581052 and maps[0x581268][9]==0x581141
assert maps[0x582FA0][4]==0x582C38
# The second table retains the original R9=image base across this leaf, not arbitrary call-clobber survival.
leaf=cat[0x57ED40]['instructions']
assert not any(i['mnemonic']=='call' or 'r9' in i['operands'] or 'r8' in i['operands'] for i in leaf)
assert int(allins[0x57FE9D]['rip_targets'][0]['address'],16)==ns['ib']
assert int(allins[0x58051B]['rip_targets'][0]['address'],16)==0x2CA99B8
assert 0x5808E6<0x5808F3 and 0x581232<0x581246 and 0x57F493<0x57F49B<0x57F4BF
assert 0x1C4*0x80+4*16==0xE240
rejections=[]
for name in ('extent-correction','unwind-rejection','catalog-mismatch'):
 p=W/('spawn-load-success-'+name+'.json');r=json.loads(p.read_text());assert r['status'].startswith('REJECTED')
 rejections.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),status=r['status']))
assert selection['reachable_instruction_bytes']==2360 and cat[0x57FE80]['catalog_body_bytes']==2105
out=dict(exe_sha256=ns['sha'],method='A only; source and conditional control-flow checks, no original execution',checks='pass',collected_bodies=18,reused_bodies=7,
 sources=sources,reused=reused,bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],anchors=[allins[a] for a in anchors],tables=tables,rejected_attempts=rejections,
 controls=['Original callback operation9/status0 versus8/other nonzero and operation12; E0bit4 refusal before side effects.',
 'Full-width synchronous parent message12/subtype16/argument4 versus storage status message12/subtype29/tag10.',
 'Original slot-index store to parent598 versus zero-only restoration branch; no invented save-slot label.',
 'State9 popup creation precedes state-byte publication; original acknowledgement table closes selector; selector18/argument4 closes parent.',
 'Five original tables have instruction-aligned destinations; corrected selection span2360 plus124 table bytes equals registered2484. Catalog2105 mismatch remains visible.',
 'Prefix recovery copy length E240 from exact loop and tail versus full-image request56690.'],
 limits='No live state, worker I/O, callback scheduling, popup delivery, file validation, full rollback or integrated parity. Low32 callback token requires representable controller address. Historical failed extractions remain rejected; this check does not make them pass.')
(W/'spawn-load-success-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:25 exact shipping bodies/spans; five original tables; callback success/error, slot selector and prefix-recovery controls. No B/live execution.')
