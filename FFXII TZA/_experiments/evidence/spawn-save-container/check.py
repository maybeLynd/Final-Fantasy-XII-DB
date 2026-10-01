from pathlib import Path
import hashlib,json
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence')
ns={};exec((W/'spawn_save_container_primary.py').read_text().split('for a in (')[0],ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={};sources=[]
for n in ('primary','decode','zlib','inflate-init'):
 p=W/('spawn-save-container-'+n+'.json');j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 sources.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes())))
 for b in j['bodies']:
  a=int(b['address'],16);assert a not in cat;cat[a]=b
assert len(cat)==10
p=E/'spawn-storage-completion/file.json';j=json.loads(p.read_text());reused=[]
for a in (0x866200,0x8666B0):
 cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a);reused.append(hex(a))
for a,b in cat.items():
 o=ns['off'](a-ns['ib']);raw=ns['raw'][o:o+b['bytes']]
 assert len(raw)==b['bytes'] and sha(raw)==b['sha256']
 fresh=list(ns['md'].disasm(raw,a));assert sum(i.size for i in fresh)==len(raw) and len(fresh)==len(b['instructions'])
 for i,v in zip(fresh,b['instructions']):assert (hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)==(v['address'],v['bytes'],v['mnemonic'],v['operands'])
 # Conditional branches inside these contiguous bodies must land on instruction boundaries.
 starts={i.address for i in fresh}
 for i in fresh:
  if i.mnemonic.startswith('j') and i.op_str.startswith('0x'):
   t=int(i.op_str,16)
   if a<=t<a+len(raw):assert t in starts
ins={int(i['address'],16):i for b in cat.values() for i in b['instructions']}
anchors={
 0x865DDB:None,
 0x865DD9:('call','0x865840'),0x865DE3:('je','0x865e10'),0x865DFB:('call','0x80c5a0'),0x865E02:('je','0x865e08'),0x865E0E:('mov','dword ptr [rsi], eax'),
 0x865932:('sub','ebx, edi'),0x865942:('add','rdx, rdi'),0x86594C:('jle','0x865961'),0x865961:('mov','byte ptr [rbp - 0x12], 0'),
 0x865BD2:('sub','ebx, edi'),0x865BE2:('add','rdx, rdi'),0x865BEC:('jle','0x865c01'),0x865C01:('mov','byte ptr [rbp - 0x12], 0'),
 0x8658F7:('mov','edx, 0x8003'),0x86599F:('mov','r9d, 0x800000'),0x8659A5:('mov','edx, 0x6801'),
 0x865B97:('mov','edx, 0x8003'),0x865C3F:('mov','r9d, 0x800000'),0x865C45:('mov','edx, 0x6801'),
 0x8659C2:('mov','r15d, 0x3e8'),0x8659FE:('cmovb','edi, ecx'),0x865A03:('je','0x865a33'),0x865A27:('je','0x865a3f'),
 0x865C66:('mov','ecx, 0x3e8'),0x865CA5:('cmovb','edi, ecx'),0x865CAA:('je','0x865ce5'),0x865CD2:('je','0x865cf1'),
 0x8663D0:('and','eax, 0x8000001f'),0x866464:('mov','dword ptr [rsp + 0x20], 9'),0x86646C:('call','0x87af40'),0x866478:('je','0x866481'),0x866493:('call','0x865ae0'),
 0x8667BC:('jbe','0x8668cf'),0x8667ED:('ja','0x866802'),0x866805:('cmp','eax, 0x1f'),0x866808:('ja','0x8669d8'),
 0x866817:('cmp','edx, 0x100000'),0x86681D:('ja','0x8669d8'),0x86685D:('call','0x865d90'),0x86686D:('jne','0x8668c2'),0x866871:('jle','0x8668c2'),
 0x80C5AE:('call','0x80c5c0'),0x80C622:('call','0x80e040'),0x80C67F:('call','0x80c750'),0x80C6A3:('sub','dword ptr [r12], ecx'),0x80C6CB:('call','0x80df00'),
 0x80E046:('mov','edx, 0xf'),0x80E04B:('jmp','0x80df50'),0x87AF91:('call','0x87c9f0'),0x87AFE7:('call','0x87bd60'),0x87B008:('call','0x87c6c0'),
 0x87C9F9:('mov','r9d, 0xf'),0x87CA04:('mov','dword ptr [rsp + 0x28], 0'),0x87CA0C:('mov','dword ptr [rsp + 0x20], 8'),0x87CA18:('call','0x87c760'),
 0x87C78E:('cmp','byte ptr [rax], 0x31'),0x87C797:('cmp','dword ptr [rsp + 0x88], 0x58'),0x87C83D:('cmp','ebp, 9'),
}
anchors={a:v for a,v in anchors.items() if v is not None}
for a,v in anchors.items():assert (ins[a]['mnemonic'],ins[a]['operands'])==v,(hex(a),ins.get(a))
expected_imports={0x8658AF:'CryptAcquireContextW',0x8658D6:'CryptAcquireContextW',0x8658FC:'CryptCreateHash',0x865985:'CryptHashData',0x8659AF:'CryptDeriveKey',0x865A1F:'CryptDecrypt',0x865CCA:'CryptEncrypt',0x8663C5:'rand',0x861EBA:'memcpy'}
for a,sym in expected_imports.items():assert any((r.get('import_name') or '').endswith('!'+sym) for r in ins[a]['rip_targets'])
literals=json.loads((W/'spawn-save-container-literals.json').read_text())
for v in literals['constants']:
 a=int(v['address'],16);o=ns['off'](a-ns['ib']);b=bytes.fromhex(v['raw_hex'])
 assert ns['raw'][o:o+len(b)]==b and sha(b)==v['sha256'] and len(b)==v['bytes']
 assert b.decode(v['encoding'])==v['text']+'\0'
base=bytes.fromhex(literals['constants'][0]['raw_hex'])[:-1];assert len(base)==32 and 0 not in base
# Source-derived arithmetic illustrations, NOT an original-code execution or roundtrip.
rotations=[]
for k in range(32):
 rotated=base[k:]+base[:k];hashed=rotated[:31]
 assert len(rotated)==32 and len(hashed)==31 and hashed!=rotated
 rotations.append(dict(selector=k,hashed_ascii=hashed.decode(),hashed_bytes=31))
assert rotations[0]['hashed_ascii']=='FINAL FANTASY XII THE ZODIAC AG'
assert rotations[31]['hashed_ascii']=='EFINAL FANTASY XII THE ZODIAC A'
out=dict(status='PASS',method='A exact shipping bytes and source interpretation; no B/live execution',exe_sha256=ns['sha'],capstone_version=ns['capstone'].__version__,collected_bodies=10,reused=dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=reused),sources=sources,
 bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],anchors=[ins[a] for a in anchors],import_anchors={hex(a):sym for a,sym in expected_imports.items()},literals=literals['constants'],source_derived_rotation_examples=rotations,
 limits='No provider/file/allocator execution, no decoded save or native roundtrip. Core zlib effects use existing library disposition and identified call boundary. Local consumer/native/live closure awaits peers. Two literal-length extraction failures remain rejected.')
(W/'spawn-save-container-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:12 original byte spans/fresh decodes and local branch targets; compression/transform/gate anchors and4 exact literals. Method A only.')
