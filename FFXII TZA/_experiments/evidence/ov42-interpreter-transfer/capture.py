"""Use the unchanged reviewed adapter capture, with bounded code/data separation."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('shared_capture',P/'capture-index-path.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
# This nested packet resolves the reviewed dependency by ancestor, not a copied
# helper's old fixed depth. The original helper/adapter bytes are unchanged.
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
C.RANGES=[(0x267e10,0x267e5e),(0x267fc0,0x2680e8),(0x2650b0,0x26517e)]
C.main()
im=C.EXE.read_bytes();pe=struct.unpack_from('<I',im,60)[0];op=struct.unpack_from('<H',im,pe+20)[0]
sec=[struct.unpack_from('<IIII',im,pe+24+op+k*40+8) for k in range(struct.unpack_from('<H',im,pe+6)[0])]
def data(a,n):
 for vs,v,rs,r in sec:
  if C.BASE+v<=a and a+n<=C.BASE+v+rs:return im[r+a-C.BASE-v:r+a-C.BASE-v+n]
 raise RuntimeError('unbacked original table')
out=Path(sys.argv[1]);z=json.loads(out.read_text())
z.update(invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 tables=[dict(start=hex(a),bytes=data(a,24).hex(),sha256=hashlib.sha256(data(a,24)).hexdigest(),
              targets=[hex(C.BASE+x) for x in struct.unpack('<6I',data(a,24))]) for a in [0x2680e8,0x265180]],
 limits='STATIC_ONLY code bodies580B and two dispatch tables48B; tables/padding never decoded as instructions. Valid resolved records/stack and normal ABI/returns are premises, not captured initialized state.')
out.write_text(json.dumps(z,indent=2)+'\n')
