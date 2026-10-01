"""Only the missing original primary-loader body. Reuse prior size/index evidence."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('primary_capture','capture-index-path.py');S=module('primary_annotations','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable capture exists')
b=C.EXE.read_bytes()
if hashlib.sha256(b).hexdigest()!=C.SHA:raise ValueError('original image changed')
e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0];secs=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
def read(a,n):
 for vs,va,rs,ro in secs:
  if C.BASE+va<=a and a+n<=C.BASE+va+rs:return b[ro+a-C.BASE-va:ro+a-C.BASE-va+n]
 raise ValueError('unbacked span')
rva,n=struct.unpack_from('<II',b,e+24+112+24);pd=[tuple(C.BASE+x for x in struct.unpack('<III',read(C.BASE+rva+k,12))) for k in range(0,n,12)]
entries=[(0x330310,0x330319,0x1d77fc4),(0x330319,0x33037e,0x1d77fd0),(0x33037e,0x330456,0x1d77ff0),(0x330456,0x330475,0x1d78008),(0x330475,0x330497,0x1d78018)]
if any(t not in pd for t in entries):raise ValueError('original primary extent changed')
chains=[]
for a,z,u in entries:
 h=read(u,4)
 if h[0]>>3==4:
  parent=tuple(C.BASE+x for x in struct.unpack('<III',read(u+((4+2*h[2]+3)&~3),12)))
  if parent not in entries:raise ValueError('primary unwind parent outside exact chain')
  chains.append(dict(entry=[a,z,u],header=h.hex(),parent=list(parent)))
C.RANGES=[(0x330310,0x330497)];C.main();r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=[list(t) for t in entries],chains=chains,annotation_prerequisite=S.validate(r),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Original391B normal primary loader only; opaque callee effects/live initialization/alternate3306E0 not established')
out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('391 original primary-loader bytes/normal pdata fragments; no game')
