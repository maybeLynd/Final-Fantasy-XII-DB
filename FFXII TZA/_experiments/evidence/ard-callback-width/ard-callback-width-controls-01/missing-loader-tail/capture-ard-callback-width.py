"""Missing ARD loader/binder/tag bodies only; no allocator samples rerun."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ard_shared_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable capture exists')
d=C.EXE.read_bytes()
if hashlib.sha256(d).hexdigest()!=C.SHA:raise ValueError('original image changed')
pe=struct.unpack_from('<I',d,60)[0];opt=struct.unpack_from('<H',d,pe+20)[0];secs=[struct.unpack_from('<IIII',d,pe+24+opt+k*40+8) for k in range(struct.unpack_from('<H',d,pe+6)[0])]
def read(a,n):
 for vs,va,rs,ro in secs:
  if C.BASE+va<=a and a+n<=C.BASE+va+rs:return d[ro+a-C.BASE-va:ro+a-C.BASE-va+n]
 raise ValueError('unbacked original span')
rva,size=struct.unpack_from('<II',d,pe+24+112+3*8)
if not size or size%12:raise ValueError('missing exception directory')
pd=[tuple(C.BASE+v for v in struct.unpack('<III',read(C.BASE+rva+k*12,12))) for k in range(size//12)]
roots=[(0x3ea820,0x3ea87e,0x1d823b4),(0x3ea710,0x3ea81b,0x1d7945c),(0x36c660,0x36c6b2,0x1d6b7c8)]
children=[(0x3ea87e,0x3ea947,0x1d823c4),(0x3ea947,0x3ea9fc,0x1d823d8)]
if any(t not in pd for t in roots+children):raise ValueError('normal ARD extent changed')
chains=[]
for a,z,u in children:
 h=read(u,4);parent=tuple(C.BASE+v for v in struct.unpack('<III',read(u+((4+2*h[2]+3)&~3),12)))
 if h[0]>>3!=4 or parent!=roots[0]:raise ValueError('normal ARD parent triple changed')
 chains.append(dict(entry=[a,z,u],header=h.hex(),parent=list(parent)))
C.RANGES=[t[:2] for t in roots+children];C.main();r=json.loads(out.read_text())
spec=importlib.util.spec_from_file_location('ard_actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
r.update(wrapper_complete=True,pdata_entries=[list(t) for t in roots+children],chains=chains,annotation_prerequisite=S.validate(r),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Complete normal loader fragments/binder/tag bytes only; no allocator/module/native effects, initialized process or all-callers claim')
out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('825 original ARD bytes/normal chains qualified; no allocator/live samples')
