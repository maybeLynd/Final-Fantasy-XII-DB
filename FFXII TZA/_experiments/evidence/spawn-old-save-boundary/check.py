from pathlib import Path
import hashlib,json
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence');ns={}
exec((W/'spawn_old_save_boundary_primary.py').read_text().split('for a in (')[0],ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={};sources=[]
for n in ('primary','helpers','mirror','capture'):
 p=W/('spawn-old-save-boundary-'+n+'.json');j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 sources.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes())))
 for b in j['bodies']:
  a=int(b['address'],16);assert a not in cat;cat[a]=b
assert len(cat)==8
reused=[]
for name,aa in [('spawn-load-close/primary.json',[0x233C10]),('spawn-load-continuation/sequence.json',[0x2EF640]),('spawn-restore-request/support.json',[0x285E60])]:
 p=E/name;j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for a in aa:cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
 reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[hex(a) for a in aa]))
assert len(cat)==11
for a,b in cat.items():
 o=ns['off'](a-ns['ib']);raw=ns['raw'][o:o+b['bytes']];assert sha(raw)==b['sha256'] and len(raw)==b['bytes']
 fresh=list(ns['md'].disasm(raw,a));assert sum(i.size for i in fresh)==len(raw)
 assert [(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str) for i in fresh]==[(i['address'],i['bytes'],i['mnemonic'],i['operands']) for i in b['instructions']]
 starts={i.address for i in fresh}
 for i in fresh:
  if i.mnemonic.startswith('j') and i.op_str.startswith('0x'):
   target=int(i.op_str,16)
   if a<=target<a+len(raw):assert target in starts
ins={int(i['address'],16):i for b in cat.values() for i in b['instructions']}
anchors={
 0x233C14:('call','0x235af0'),0x233C23:('jne','0x233c4d'),0x233C2A:('add','rax, 0x4e68c'),0x233C3F:('call','0x237df0'),0x233C48:('jmp','0x237df0'),0x233C4D:('cmp','dword ptr [rax], 0x5071901'),0x233C53:('je','0x233c5e'),0x233C59:('jmp','0x237df0'),
 0x235B00:('lea','rdx, [rax + 0x2200]'),0x235B0A:('je','0x235dac'),0x235B19:('mov','ecx, dword ptr [r8]'),0x235B1E:('jne','0x235b4e'),0x235B20:('mov','ecx, dword ptr [r8 + 4]'),0x235B27:('jne','0x235b4e'),0x235B29:('movzx','eax, byte ptr [r8 + 0x5b42]'),0x235B37:('jne','0x235b4e'),0x235B39:('movzx','eax, word ptr [r8 + 0x5b12]'),0x235B48:('je','0x235dac'),0x235B76:('call','0x2ef4a0'),
 0x2EF4A7:('mov','edx, 0xc0'),0x2EF500:('sub','rdx, 1'),0x2EF504:('jne','0x2ef4b3'),
 0x235B83:('mov','edx, 0x7370'),0x235BAF:('mov','dword ptr [rdx + rax], 0'),0x235BCC:('movups','xmmword ptr [rcx + 0x5b10], xmm0'),
 0x235BF8:('mov','dword ptr [rcx + 0x5b40], eax'),0x235BAA:('mov','ebp, 2'),0x235CBD:('jbe','0x235d07'),0x235CD8:('je','0x235d07'),0x235CDE:('je','0x235d07'),0x235D07:('movzx','ecx, byte ptr [r15 + 0xc2]'),0x235D0F:('mov','byte ptr [rbx + 0x32], cl'),0x235D20:('mov','dword ptr [rdx], 0xffffffff'),0x235D3C:('add','rsi, 0x34'),0x235D44:('jne','0x235c00'),0x235D57:('add','rdx, 4'),0x235D5B:('add','rcx, 0x9c'),0x235D67:('add','r12, 0x1c8'),0x235D7A:('cmp','r14d, 0x28'),
 0x237DF6:('call','0x23af50'),0x23AF56:('call','0x2370c0'),0x2370CD:('mov','r8d, 0x7410'),0x2370D3:('call','0x861ec0'),0x2370DF:('mov','dword ptr [rax], 0x5071901'),
 0x58450E:('je','0x584574'),0x584510:('call','0x234ed0'),0x58451C:('mov','ecx, 0xc0'),0x58456E:('sub','rcx, 1'),0x584572:('jne','0x584521'),
 0x229B71:('call','0x234ed0'),0x229B7B:('mov','r8d, 0xc0'),0x229B81:('lea','rdx, [rax + 0x4e68c]'),0x229B88:('add','rax, 0x2200'),0x229BDE:('sub','r8, 1'),0x229BE2:('jne','0x229b91'),0x229BEB:('mov','ecx, 0x100'),0x229C41:('jne','0x229bf0'),
}
for a,v in anchors.items():assert (ins[a]['mnemonic'],ins[a]['operands'])==v,(hex(a),ins[a])
assert ins[0x2EF4A0]['rip_targets'][0]['address']=='0x21b290c'
assert ins[0x2EF4AC]['rip_targets'][0]['address']=='0x2166480'
assert ins[0x2EF640]['rip_targets'][0]['address']=='0x2164280'
assert ins[0x861EC0]['rip_targets'][0]['import_name']=='VCRUNTIME140.dll!memset'
assert 0x21B290C-0x2164280==0x4E68C and 0x2166480-0x2164280==0x2200
assert 0xC0*0x80==0x6000 and 0x100*0x80==0x8000
assert 0x4E690-0x4E68C==4 and 0x2200+0x6000==0x8200<0x4E690
assert 0x5B10+40*0x9C==0x7370 and 0x7370+40*4==0x7410
out=dict(status='PASS',method='A exact original bytes, control-flow/extent interpretation; no B/live or save decoding',exe_sha256=ns['sha'],bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],collected_sources=sources,reused=reused,anchors=[ins[a] for a in anchors],
 intervals=dict(compatibility_source_image=[0x2200,0x8200],current_block_image=[0x4E68C,0x55A9C],copy_length=0x6000,old_read_end=0x4E690,stamp_overlap_bytes=4,gambit_records=[0x5B10,0x7370],counters=[0x7370,0x7410]),
 rejected_interpretations=['No conversion before stamp check','A copy body of128 bytes means total128 bytes despiteC0 iterations','Old short read alone proves final block equals pre-load block','Four-byte stamp overlap alone guarantees reset, ignoring235AF0 prelude'],
 limits='233C10 runs235AF0 before null/magic decisions. Compatibility branch requires nonnull bound state and unequal comparison, valid authored tables/callee returns; native prelude234ED0 and helpers not fully interpreted. Individual file final stamp and gameplay effects require receipts/live proof. The rebuild does not imply every padding byte is freshly initialized.')
(W/'spawn-old-save-boundary-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:11 original spans, local targets, copy and guard order,6000/8000 copy lengths and4-byte stamp overlap. No execution cases.')
