"""One bounded, read-only export/body capture. Does not load or run the DLL."""
import hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
W=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
assert not (W/'source.json').exists(),'Do not replace captured evidence'
HOST=Path('C:/Windows/System32/ucrtbase.dll');x=HOST.read_bytes()
assert sha(x)=='5c52e3a303baaac0e0af8bd9b96134993da34bc9d834a31ef37e1d2cdc7fe192'
u=lambda o:struct.unpack_from('<I',x,o)[0]
w=lambda o:struct.unpack_from('<H',x,o)[0]
n=u(60);assert x[n:n+4]==b'PE\0\0' and w(n+4)==0x8664
opt=n+24;assert w(opt)==0x20b
sections=[]
for j in range(w(n+6)):
 o=opt+w(n+20)+40*j
 sections.append(dict(name=x[o:o+8].rstrip(b'\0').decode(),rva=u(o+12),virtual_size=u(o+8),raw_size=u(o+16),raw_offset=u(o+20),characteristics=u(o+36)))
def off(r):
 for s in sections:
  if s['rva']<=r<s['rva']+s['raw_size']:return s['raw_offset']+r-s['rva']
 raise ValueError(hex(r))
def z(r):return x[off(r):].split(b'\0',1)[0].decode()
er,es=struct.unpack_from('<II',x,opt+112);e=off(er)
matches=[]
for k in range(u(e+24)):
 nr=u(off(u(e+32))+4*k)
 if z(nr)=='_fdclass':
  ordinal=w(off(u(e+36))+2*k);fr=u(e+28)+ordinal*4;rva=u(off(fr))
  matches.append(dict(name='_fdclass',name_rva=nr,ordinal_index=ordinal,ordinal=ordinal+u(e+16),function_table_rva=fr,function_table_hex=x[off(fr):off(fr)+4].hex(),rva=rva,forwarded=er<=rva<er+es))
assert len(matches)==1 and not matches[0]['forwarded']
ex=matches[0];assert ex['rva']==0x5f410
body=x[off(ex['rva']):off(ex['rva'])+65]
assert x[off(ex['rva'])+65:off(ex['rva'])+80]==b'\xcc'*15
ii=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in Cs(CS_ARCH_X86,CS_MODE_64).disasm(body,ex['rva'])]
assert b''.join(bytes.fromhex(i['bytes']) for i in ii)==body
ref=Path('Database/FFXII TZA/_experiments/evidence/nav-conversion-domain/source.json');s=json.loads(ref.read_text())
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
assert sha(reader.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
spec=importlib.util.spec_from_file_location('retained_image_reader',reader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,secs=m.load_image();imp=s['imports'][0]
for ak,hk in [('descriptor_address','descriptor_hex'),('lookup_address','lookup_hex'),('hint_name_address','hint_name_hex'),('dll_name_address','dll_name_hex')]:
 assert m.img_rd(raw,secs,int(imp[ak],16),len(bytes.fromhex(imp[hk])))==bytes.fromhex(imp[hk])
assert m.img_rd(raw,secs,0x383f10,542)==bytes.fromhex(s['body']['raw_hex'])
ret=W/'retained';ret.mkdir(exist_ok=False);deps=[]
for p,name in [(ref,'nav-source.json'),(Path('Database/FFXII TZA/_experiments/evidence/navgrid-query-exec/gen_bodies.py'),'exp131-gen_bodies.py'),(Path('Database/FFXII TZA/_experiments/evidence/navgrid-query-exec/check.py'),'exp131-check.py')]:
 b=p.read_bytes();assert subprocess.check_output(['git','show','HEAD:'+p.as_posix()])==b,p
 (ret/name).write_bytes(b);deps.append(dict(path=p.as_posix(),retained=name,sha256=sha(b),git_blob=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip()))
assert sha(HOST.read_bytes())==sha(x)
out=dict(method='A STATIC_ONLY identified host CRT body; no DLL execution or game binding',host=dict(path=str(HOST),bytes=len(x),sha256=sha(x),export_directory_rva=er,export_directory_size=es,export=ex,body_rva=hex(ex['rva']),body_size=len(body),body_sha256=sha(body),body_hex=body.hex(),instructions=ii,sections=sections),ff12=dict(exe_sha256=s['exe_sha256'],image_base=s['image_base'],import_witness=imp,ggrid_sha256=s['body']['sha256'],reader_sha256=sha(reader.read_bytes())),dependencies=deps,driver_sha256=sha(Path(__file__).read_bytes()),limits='Host DLL not shipped FF12 binary; actual running-game API-set/module binding unobserved. No native calls, live init, caller state, FP status observation or grid recapture.')
(W/'source.json').write_text(json.dumps(out,indent=2)+'\n')
print('Captured exact 65B host classifier and shipping import witness; STATIC_ONLY.',flush=True)
