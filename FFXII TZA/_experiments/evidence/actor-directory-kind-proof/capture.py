"""Bounded original actor allocator/initializer bytes, reviewed access-role path."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
s=importlib.util.spec_from_file_location('reviewed_capture',P/'capture-index-path.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
C.RANGES=[(0x2679f0,0x267ba4),(0x266530,0x266acf),(0x266bd0,0x266c30),(0x268ea0,0x269057)]
sys.argv=[sys.argv[0],str(P/'source-01.json')];C.main()
q=P/'source-01.json';x=json.loads(q.read_text())
x.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
q.write_bytes((json.dumps(x,indent=2)+'\n').encode())
raw=C.EXE.read_bytes();pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,off in secs:
  if C.BASE+rva<=a and a+n<=C.BASE+rva+size:return raw[off+a-C.BASE-rva:off+a-C.BASE-rva+n]
 raise ValueError('unbacked data span')
spans=[(0x1e0c328,32,'kind size table'),(0x266c30,32,'preset switch destinations')]
out=dict(exe_sha256=C.SHA,driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),spans=[dict(address=hex(a),bytes=n,label=label,hex=read(a,n).hex(),sha256=hashlib.sha256(read(a,n)).hexdigest()) for a,n,label in spans])
dst=P/'native-tables-01.json'
if dst.exists():raise ValueError('immutable table receipt exists')
dst.write_bytes((json.dumps(out,indent=2)+'\n').encode())
print('CAPTURED exact native kind/preset tables; no process observation')
