"""Original manager-count source and region switch table; no live initialization."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
s=importlib.util.spec_from_file_location('reviewed_capture',P/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=[(0x26ce60,0x26d394)]
sys.argv=[sys.argv[0],str(P/'source-setup-01.json')];C.main()
p=P/'source-setup-01.json';x=json.loads(p.read_text());x.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest());p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
raw=C.EXE.read_bytes();pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
a,n=0x266ba4,32
for vs,rva,size,off in secs:
 if C.BASE+rva<=a and a+n<=C.BASE+rva+size:
  b=raw[off+a-C.BASE-rva:off+a-C.BASE-rva+n];break
else:raise ValueError('unbacked original switch table')
out=dict(exe_sha256=C.SHA,driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),address=hex(a),bytes=n,hex=b.hex(),sha256=hashlib.sha256(b).hexdigest())
p=P/'region-switch-01.json'
if p.exists():raise ValueError('immutable switch receipt exists')
p.write_bytes((json.dumps(out,indent=2)+'\n').encode())
print('CAPTURED exact manager source and region-switch identities')
