"""Only missing root construction bytes; retained title/release code is reused."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('root_shared_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
d=C.EXE.read_bytes()
if hashlib.sha256(d).hexdigest()!=C.SHA:raise ValueError('original image changed')
pe=struct.unpack_from('<I',d,60)[0];opt=struct.unpack_from('<H',d,pe+20)[0]
ss=[struct.unpack_from('<IIII',d,pe+24+opt+40*k+8) for k in range(struct.unpack_from('<H',d,pe+6)[0])]
def read(a,n):
 for vs,va,rs,ro in ss:
  if C.BASE+va<=a and a+n<=C.BASE+va+rs:return d[ro+a-C.BASE-va:ro+a-C.BASE-va+n]
 raise ValueError('unbacked original span')
rva,size=struct.unpack_from('<II',d,pe+24+112+3*8)
if not size or size%12:raise ValueError('invalid exception directory')
pd=[tuple(C.BASE+v for v in struct.unpack('<III',read(C.BASE+rva+12*k,12))) for k in range(size//12)]
root=(0x247ae0,0x248024,0x1d699ec);leaf=(0x2445d0,0x24460d)
if root not in pd or any(a<=leaf[0]<z for a,z,u in pd) or read(leaf[1],3)!=b'\xcc'*3:raise ValueError('root/leaf extent identity changed')
# Derive the displacement from the named destination; handwritten displacement
# in attempt01 refused before export. Keep that failed driver/receipt.
if read(0x247d93,7)!=b'\x4c\x8d\x05'+struct.pack('<i',0x2445d0-0x247d9a):raise ValueError('original root handler binding changed')
C.RANGES=[root[:2],leaf];C.main()
r=json.loads(out.read_text());s=importlib.util.spec_from_file_location('root_actual_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
r.update(wrapper_complete=True,pdata_entries=[list(root)],leaf=dict(start=hex(leaf[0]),end_exclusive=hex(leaf[1]),padding='cccccc'),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=S.validate(r),limits='Static root construction/binding only; no actual initialized root pointer, scheduling or opaque effects')
out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print('Missing root code qualified; actual title/release retained, no game run')
