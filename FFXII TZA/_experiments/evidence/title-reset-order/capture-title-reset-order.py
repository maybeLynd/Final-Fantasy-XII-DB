"""Method A source for a candidate count writer, not a constructor assumption.

Reuse the reviewed actual capture path and bound complete normal root extents.
No FF12 execution, injected state or refcount/initialization inference.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
out=W/'title-reset-order-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong original image')
p=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,p+6)[0];opt=struct.unpack_from('<H',d,p+20)[0]
sections=[struct.unpack_from('<IIII',d,p+24+opt+40*k+8) for k in range(ns)]
def read(a,n):
    for vs,va,rs,ro in sections:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('whole original range not raw-backed')
rva,size=struct.unpack_from('<II',d,p+24+112+3*8)
if size%12:raise ValueError('partial exception directory')
pd=[tuple(x+0x120000 for x in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
entries=[(0x611F80,0x611FE2,0x1DA8660),(0x5DE290,0x5DE2CF,0x1D9FE28)]
if any(e not in pd for e in entries):raise ValueError('named root extent changed')
spec=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(a,b) for a,b,u in entries];sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text())
spec=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
agreement=S.validate(raw)
raw.update(wrapper_complete=True,pdata_entries=[list(e) for e in entries],exception_directory=dict(rva=hex(rva),bytes=size),
           annotation_prerequisite=agreement,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           limits='Physical complete root source and annotation agreement; normal CFG reduction required. No constructor, natural caller, native service, transitive writes or initialized lifetime claim.')
out.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
print('Named candidate writer and tail roots captured; semantic qualification still required')
