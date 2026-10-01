"""Add only the two original normal continuations; keep the82B first source."""
import hashlib, importlib.util, json, pathlib, struct, sys

W=pathlib.Path(__file__).resolve().parent
ROOT=W.parents[4]
out=W/'texture-async-removal-tail-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong original image')
pe=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,pe+6)[0];opt=struct.unpack_from('<H',d,pe+20)[0]
sections=[struct.unpack_from('<IIII',d,pe+24+opt+40*k+8) for k in range(ns)]


def read(a,n):
    for vs,va,rs,ro in sections:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('whole range lacks raw backing')


rva,size=struct.unpack_from('<II',d,pe+24+112+3*8)
if not size or size%12:raise ValueError('incomplete original exception directory')
pd=[tuple(v+0x120000 for v in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
root=(0x62ec70,0x62ecc2,0x1d8f380)
children=[(0x62ecc2,0x62ed36,0x1daa2a8),(0x62ed36,0x62ed3c,0x1daa2c0)]
if root not in pd or any(t not in pd for t in children):raise ValueError('expected original chained normal extents absent')
chains=[]
for a,z,u in children:
    header=read(u,4);count=header[2];tail=(4+2*count+3)&~3
    raw_parent=read(u+tail,12)
    parent=tuple(v+0x120000 for v in struct.unpack('<III',raw_parent))
    if header[0]>>3!=4 or parent!=root:raise ValueError('original continuation parent triple changed')
    read(a,z-a)
    chains.append(dict(entry=[a,z,u],header=header.hex(),parent_raw=raw_parent.hex(),parent=list(parent)))
spec=importlib.util.spec_from_file_location('removal_tail_shared_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(a,z) for a,z,u in children];sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text());spec=importlib.util.spec_from_file_location('removal_tail_actual_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
raw.update(wrapper_complete=True,pdata_entries=[list(t) for t in children],chains=chains,root_parent=list(root),
           annotation_prerequisite=S.validate(raw),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           limits='Only missing122B normal continuations. Original82B retained/reused; normal CFG/helper effects/independent acceptance remain distinct. No actual game/exception/scheduler observation.')
out.write_text(json.dumps(raw,indent=2)+'\n')
print('Retained two original normal continuations only',[(q['start'],q['end_exclusive'],q['sha256']) for q in raw['ranges']])
