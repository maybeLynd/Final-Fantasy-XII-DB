"""Specific callback teardown and named shipping import, Method A only.

No pefile dependency. Original descriptor/thunk/leaf bytes are read, not executed.
Natural heap/object validity, loaded CRT module and callee effects are separate.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'title-cleanup-import-boundary-source-02.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];opt=p+24
if d[p:p+4]!=b'PE\0\0' or struct.unpack_from('<H',d,opt)[0]!=0x20b:raise ValueError('wrong PE type')
base=struct.unpack_from('<Q',d,opt+24)[0]
if base!=0x120000:raise ValueError('wrong image base')
ns=struct.unpack_from('<H',d,p+6)[0];osize=struct.unpack_from('<H',d,p+20)[0];ss=[];rows=[]
for k in range(ns):
 q=opt+osize+40*k;vs,va,rs,ro=struct.unpack_from('<IIII',d,q+8);ss.append((vs,va,rs,ro))
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  for j in range(ro,ro+rs-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+base==0x5de250:rows.append([a+base,b+base,u+base])
if rows!=[[0x5de250,0x5de282,0x1d9ff38]]:raise ValueError('teardown boundary changed')
def read(rva,n):
 for vs,va,rs,ro in ss:
  if va<=rva and rva+n<=va+rs:return d[ro+rva-va:ro+rva-va+n]
 raise ValueError('not backed original RVA')
def cstr(rva):
 z=bytearray()
 for k in range(256):
  b=read(rva+k,1)
  if b==b'\0':return z.decode('ascii')
  z.extend(b)
 raise ValueError('unterminated bounded import name')
leaf=read(0x19c590-base,7)
if leaf!=bytes.fromhex('48ff25b1657200'):raise ValueError('import tail bytes changed')
target=0x19c590+7+struct.unpack_from('<i',leaf,3)[0]
rva,size=struct.unpack_from('<II',d,opt+112+8);entries=[];terminated=False
for k in range(size//20):
 blob=read(rva+20*k,20);ilt,time,chain,name,iat=struct.unpack('<IIIII',blob)
 if blob==b'\0'*20:terminated=True;break
 if not ilt:raise ValueError('no original lookup table')
 delta=target-base-iat
 if delta<0 or delta%8:continue
 idx=delta//8
 for j in range(idx+1):
  thunk=struct.unpack('<Q',read(ilt+8*j,8))[0]
  if thunk==0:break
 else:
  if thunk>>63:raise ValueError('unnamed ordinal import')
  entries.append(dict(dll=cstr(name),name=cstr(thunk+2),hint=struct.unpack('<H',read(thunk,2))[0],descriptor_rva=hex(rva+20*k),lookup_table_rva=hex(ilt),slot=idx,iat=hex(target),descriptor_bytes=blob.hex(),lookup_bytes=read(ilt+8*idx,8).hex(),name_bytes=read(thunk,2+len(cstr(thunk+2))+1).hex()))
if not terminated or len(entries)!=1 or (entries[0]['dll'],entries[0]['name'],entries[0]['iat'])!=('api-ms-win-crt-heap-l1-1-0.dll','free','0x8c2b48'):raise ValueError('incomplete/ambiguous/wrong original import')
s=importlib.util.spec_from_file_location('capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[rows[0][:2],(0x19c590,0x19c597)];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=rows,import_boundary=entries[0],invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Original local source and import metadata only. No loaded CRT/IAT/module identity, heap validity/safety, full resource teardown, actual initialized object or natural callback execution.')
out.write_text(json.dumps(r,indent=2)+'\n');print('Original teardown/import boundary captured; transitive effects remain distinct')
