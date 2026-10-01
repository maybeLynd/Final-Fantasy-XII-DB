"""Read exact resource/name slots and the one memcpy import from the pinned EXE.
No broad string scan, process access, native execution or import-name guessing.
"""
import hashlib,json,pathlib,struct
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'softedges-resource-source-01/literal-import-facts-01.json'
if out.exists():raise ValueError('immutable output exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();B=0x120000
pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(d).hexdigest()!=pin:raise ValueError('wrong executable')
pe=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,pe+6)[0];op=struct.unpack_from('<H',d,pe+20)[0]
s=[struct.unpack_from('<IIII',d,pe+32+op+40*i) for i in range(n)]
def read(a,z):
 for vs,va,rs,ro in s:
  if B+va<=a and a+z<=B+va+rs:return d[ro+a-B-va:ro+a-B-va+z]
 raise ValueError('unbacked exact read')
def string(a,limit=128):
 b=bytearray()
 for i in range(limit):
  v=read(a+i,1)
  if v==b'\0':return b.decode('ascii'),bytes(b)+v
  b.extend(v)
 raise ValueError('unterminated bounded literal')
slots=[]
for a,expect in [(0x1dfde00,'./GameData/D3D11/ArtData/shaders/PhyreText.fx.phyre'),
                 (0x1dfde08,'./GameData/D3D11/ArtData/font/tuffysdf.fgen.phyre')]:
 b=read(a,8);p=struct.unpack('<Q',b)[0];name,raw=string(p)
 if name!=expect:raise ValueError('resource literal identity')
 slots.append(dict(slot=hex(a),slot_bytes=b.hex(),pointer=hex(p),name=name,cstring_bytes=raw.hex()))
name,raw=string(0x901b18)
if name!='softEdges':raise ValueError('original lookup name')
imports_rva=struct.unpack_from('<I',d,pe+24+112+8)[0]
target=0x8c2a68;matches=[]
for i in range(64):
 raw_desc=read(B+imports_rva+20*i,20);oft,stamp,chain,nm,ft=struct.unpack('<5I',raw_desc)
 if not any((oft,stamp,chain,nm,ft)):break
 if ft and target>=B+ft and (target-B-ft)%8==0:
  index=(target-B-ft)//8
  if index<4096:
   # Walk only this candidate's prefix to ensure the selected slot precedes its
   # terminator. Never try to read every import's name.
   lookup=B+(oft or ft)
   vals=[struct.unpack('<Q',read(lookup+8*j,8))[0] for j in range(index+1)]
   if all(vals) and vals[-1] and not vals[-1]>>63:
    dll,_=string(B+nm);fn,_=string(B+vals[-1]+2)
    matches.append(dict(dll=dll,name=fn,iat_slot=hex(target),import_index=index,
       descriptor_bytes=raw_desc.hex(),name_rva=hex(vals[-1]),hint=read(B+vals[-1],2).hex()))
else:raise ValueError('import descriptor budget/terminator')
if len(matches)!=1 or (matches[0]['dll'].lower(),matches[0]['name'])!=('vcruntime140.dll','memcpy'):
 raise ValueError('exact memcpy import identity')
r=dict(method='A STATIC_ONLY',exe_sha256=pin,driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 resource_slots=slots,lookup=dict(address='0x901b18',name=name,cstring_bytes=raw.hex()),imports=matches,
 limits='File-backed literal/import identity only, not evidence that the resource loads, callbacks execute or native memcpy was called.')
out.write_text(json.dumps(r,indent=2)+'\n')
print('CAPTURED original two resource literals, softEdges lookup literal and exact VCRUNTIME140 memcpy import')
