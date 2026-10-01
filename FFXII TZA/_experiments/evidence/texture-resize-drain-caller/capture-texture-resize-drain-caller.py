"""Exact remaining discriminator: does628100 call the original drain before resize?

Reuse previous raw-reference candidates and qualified helper, Method A.
Bind all three chained-unwind fragments, not only the first fragment. No
normal resize/allocator/lifetime observation is asserted by this capture.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'texture-resize-drain-caller-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong original image')
p=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,p+6)[0];opt=struct.unpack_from('<H',d,p+20)[0]
secs=[struct.unpack_from('<IIII',d,p+24+opt+40*k+8) for k in range(ns)]
def read(a,n):
    for vs,va,rs,ro in secs:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('whole source not backed')
rva,size=struct.unpack_from('<II',d,p+24+112+3*8)
if size%12:raise ValueError('incomplete exception directory')
pd=[tuple(t+0x120000 for t in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
entries=[(0x628100,0x628124,0x1DE0C5C),(0x628124,0x62818E,0x1DA85B8),(0x62818E,0x628199,0x1DA85CC)]
if any(e not in pd for e in entries) or read(0x628199,1)!=b'\xcc':raise ValueError('normal fragments/extent changed')
unwind=[]
for a,b,u in entries:
    h=read(u,4);flags=h[0]>>3;extra=(4+2*h[2]+3)&~3;chain=None
    if flags&4:chain=[v+0x120000 for v in struct.unpack('<III',read(u+extra,12))]
    unwind.append(dict(address=hex(u),header=h.hex(),flags=flags,chain=chain,raw=read(u,extra+(12 if flags&4 else 0)).hex()))
if any(q['chain']!=list(entries[0]) for q in unwind[1:]):raise ValueError('chained normal tail does not bind selected root')
spec=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(0x628100,0x628199)];sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text());spec=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
raw.update(wrapper_complete=True,pdata_entries=[list(e) for e in entries],unwind=unwind,padding='cc',annotation_prerequisite=S.validate(raw),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Full selected original normal caller only; reduction/independent acceptance pending. Direct reference candidates do not establish all callers or natural initialized state/lifetime.')
out.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8');print('Complete chained caller source',raw['ranges'][0]['sha256'])
