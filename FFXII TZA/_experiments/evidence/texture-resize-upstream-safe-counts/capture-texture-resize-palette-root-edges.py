"""Complete the two retained palette roots by capturing only missing edges.
Counts are source-domain evidence, not actual gameplay or a whole caller census.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'texture-resize-palette-root-edges-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong image')
p=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,p+6)[0];opt=struct.unpack_from('<H',d,p+20)[0];secs=[struct.unpack_from('<IIII',d,p+24+opt+40*k+8) for k in range(ns)]
def read(a,n):
 for vs,va,rs,ro in secs:
  if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
 raise ValueError('whole range unbacked')
rva,size=struct.unpack_from('<II',d,p+24+112+3*8);pd=[tuple(x+0x120000 for x in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
groups=[[(0x180e70,0x180ec4,0x1d539d0),(0x180ec4,0x180fd0,0x1d539a8),(0x180fd0,0x180ff1,0x1d539c0)],[(0x181000,0x181054,0x1d539d0),(0x181054,0x181167,0x1d539ec),(0x181167,0x181188,0x1d53a04)]]
metadata=[]
for entries in groups:
 unwind=[]
 for a,b,u in entries:
  if (a,b,u) not in pd:raise ValueError('original palette root fragment missing')
  h=read(u,4);at=(4+2*h[2]+3)&~3;flags=h[0]>>3
  chain=[v+0x120000 for v in struct.unpack('<III',read(u+at,12))] if flags&4 else None
  if chain is not None and chain!=list(entries[0]):raise ValueError('palette fragment parent changed')
  handler=struct.unpack('<I',read(u+at,4))[0]+0x120000 if flags&3 else None
  unwind.append(dict(address=hex(u),header=h.hex(),flags=flags,chain=chain,handler=hex(handler) if handler else None,raw=read(u,at+(12 if flags&4 else 4 if flags&3 else 0)).hex()))
 metadata.append(dict(entries=[list(e) for e in entries],unwind=unwind))
s=importlib.util.spec_from_file_location('actual_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x180e70,0x180ec4),(0x180fd0,0x180ff1),(0x181000,0x181054),(0x181167,0x181188)];sys.argv=[sys.argv[0],str(out)];C.main()
z=json.loads(out.read_text());s=importlib.util.spec_from_file_location('actual_annotation',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
z.update(wrapper_complete=True,palette_roots=metadata,annotation_prerequisite=S.validate(z),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Only234B missing prefix/tail edges captured; retained543B children reused. Original normal CFG/count proof pending, no exception-handler semantics or actual initialization/caller census.')
out.write_text(json.dumps(z,indent=2)+'\n');print('Captured only missing palette edges',[(q['start'],q['end_exclusive'],q['sha256']) for q in z['ranges']])
