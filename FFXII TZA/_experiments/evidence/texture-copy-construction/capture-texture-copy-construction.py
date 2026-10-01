"""Method A discriminating copy/reset/bounds question, before any runtime setup.

Claim: does61D100 clamp/reset copied counters or preserve old records and zero
only the new tail? AcceptedOPUS613770 layout is reused. Distinguish original
R9D copy count from new EDX capacity and trace initialization/order. Full root
and two branch-closed leaves, exact EXE/shared roles, no calls performed.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'texture-copy-construction-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong original image')
p=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,p+6)[0];opt=struct.unpack_from('<H',d,p+20)[0]
secs=[struct.unpack_from('<IIII',d,p+24+opt+40*k+8) for k in range(ns)]
def read(a,n):
    for vs,va,rs,ro in secs:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('whole range not raw-backed')
rva,size=struct.unpack_from('<II',d,p+24+112+3*8)
if size%12:raise ValueError('incomplete exception directory')
pd=[tuple(t+0x120000 for t in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
root=(0x61D100,0x61D179,0x1D7945C);leaves=[(0x613770,0x6137F5,11),(0x61C250,0x61C2AD,3)]
if root not in pd or any(any(a<=k<b for a,b,u in pd) for k,z,n in leaves):raise ValueError('root/leaf metadata changed')
if any(read(z,n)!=b'\xcc'*n for k,z,n in leaves):raise ValueError('helper padding changed')
spec=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[root[:2]]+[(a,b) for a,b,n in leaves];sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text());spec=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
raw.update(wrapper_complete=True,pdata_entries=[list(root)],leaves=[dict(start=hex(a),end_exclusive=hex(b),padding=read(b,n).hex()) for a,b,n in leaves],annotation_prerequisite=S.validate(raw),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Original normal source only. Allocator effects/success, fullcaller/shrinkreachability, ownership and complete counter-writer closure remain unproved. No native/live execution.')
out.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
print([(q['start'],q['end_exclusive'],q['sha256']) for q in raw['ranges']])
