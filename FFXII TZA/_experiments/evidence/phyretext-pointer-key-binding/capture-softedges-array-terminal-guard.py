"""Prepared key22/27 discriminator: actual array-member kind/recursion guard.
Correct the private untested null-stub hypothesis by original getter bytes.
No new family disposition, game execution, resource capture or generic platform.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'softedges-array-terminal-guard-source-01'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();B=0x120000
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong reference')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];op=struct.unpack_from('<H',d,p+20)[0];sections=[]
for i in range(n):
 q=p+24+op+40*i;sections.append((d[q:q+8].rstrip(b'\0'),*struct.unpack_from('<IIII',d,q+8)))
def read(a,z):
 for name,vs,va,rs,ro in sections:
  if B+va<=a and a+z<=B+va+rs:return d[ro+a-B-va:ro+a-B-va+z]
 raise ValueError('unbacked exact original read')
slots={}
for a in (0xd49ea0,0xd4bd30):slots[hex(a)]=dict(offset='0x8',bytes=read(a+8,8).hex(),target=hex(struct.unpack('<Q',read(a+8,8))[0]))
if slots['0xd49ea0']['target']!='0x16d680' or slots['0xd4bd30']['target']!='0x16d680':raise ValueError('type-query slot identity changed')
if read(0x16d680,4)!=bytes.fromhex('488bc1c3'):raise ValueError('original self getter differs')
rows=[]
for name,vs,va,rs,ro in sections:
 if name==b'.pdata':
  for q in range(ro,ro+rs-11,12):
   a,b,u=struct.unpack_from('<III',d,q)
   if a+B==0x632a10:rows.append((a+B,b+B,u+B))
if len(rows)!=1 or rows[0][1]-rows[0][0]>512:raise ValueError('bounded constructor identity/extent')
out.mkdir();s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x16d680,0x16d684),rows[0][:2]];sys.argv=[sys.argv[0],str(out/'original-code.json')];C.main()
r=json.loads((out/'original-code.json').read_text());r.update(wrapper_complete=True,constructor_pdata=[list(x) for x in rows],
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Exact self getter and physical array-member constructor source only; native registration/load/mapping not executed.')
(out/'original-code.json').write_text(json.dumps(r,indent=2)+'\n')
(out/'facts.json').write_text(json.dumps(dict(status='PREPARED_NATIVE_GUARD_SOURCE_ONLY',exe_sha256=r['exe_sha256'],slots=slots,
 correction='Private untested16D680 null-stub hypothesis refuted by original488BC1C3: it returns RCX. Published member-boundary packet did not depend on the hypothesis; its registered callback/status/address-width claims remain unchanged.',
 next='Bind constructor argument7 to member+5C: outer-kind3 from5E48C6/5E4951 versus inner-kind2 from5EED9A. Both registered getters return self. Original59EC40 kind2/bit6 guard, not a null getter/link, should stop inner recursion; verify59BED0 terminal member. Mapped child-link at59B93C is a class-reference calculation, not assumed null.',
 limits='No loaded descriptor/pointer, lifetime, resource-success or natural caller observation.'),indent=2)+'\n')
print('Retained exact shared self getter and array-member constructor; failed outer-null-slot hypothesis preserved/refuted')
