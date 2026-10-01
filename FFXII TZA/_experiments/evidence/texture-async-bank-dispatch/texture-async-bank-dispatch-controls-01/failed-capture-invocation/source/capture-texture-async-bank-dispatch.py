"""Only four missing selected-bank dispatch boundaries,436B original code."""
import hashlib, importlib.util, json, pathlib, struct, sys

W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'texture-async-bank-dispatch-source-01.json'
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
roots=[(0x185a50,0x185a7d,0x1d52bc8),(0x5fea50,0x5feb21,0x1d52a90),(0x62ebc0,0x62ec07,0x1d8e1e4)]
children=[(0x62ec07,0x62ec40,0x1daa2d0),(0x62ec40,0x62ec67,0x1daa2e4)]
if any(t not in pd for t in roots+children):raise ValueError('original normal dispatch extents changed')
chains=[]
for a,z,u in children:
    header=read(u,4);extra=(4+2*header[2]+3)&~3;raw_parent=read(u+extra,12)
    parent=tuple(v+0x120000 for v in struct.unpack('<III',raw_parent))
    if header[0]>>3!=4 or parent!=roots[2]:raise ValueError('normal consumer parent triple changed')
    chains.append(dict(entry=[a,z,u],header=header.hex(),parent_raw=raw_parent.hex(),parent=list(parent)))
leaf=(0x186610,0x18661f)
if any(a<=leaf[0]<z for a,z,u in pd) or read(leaf[1],1)!=b'\xcc':raise ValueError('original callback leaf boundary changed')
if read(0x185a62,1)!=b'\xe8' or 0x185a67+struct.unpack('<i',read(0x185a63,4))[0]!=0x5fea50:raise ValueError('original dispatch caller changed')
for a,z,u in roots+children:read(a,z-a)
spec=importlib.util.spec_from_file_location('bank_dispatch_shared_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(a,z) for a,z,u in roots+children]+[leaf];sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text());spec=importlib.util.spec_from_file_location('bank_dispatch_actual_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
raw.update(wrapper_complete=True,pdata_entries=[list(t) for t in roots+children],chains=chains,
           leaf=dict(start=hex(leaf[0]),end_exclusive=hex(leaf[1]),padding=read(leaf[1],1).hex()),
           annotation_prerequisite=S.validate(raw),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           limits='Original positive dispatch/callback/consumer boundaries only; full normal CFG, receiver/protocol semantics, opaque callee effects, actual scheduling/initialization and independent acceptance remain separate. No all-writer/caller or game-execution claim.')
out.write_text(json.dumps(raw,indent=2)+'\n')
print('Retained missing original bank dispatch boundaries',[(q['start'],q['end_exclusive'],q['sha256']) for q in raw['ranges']])
