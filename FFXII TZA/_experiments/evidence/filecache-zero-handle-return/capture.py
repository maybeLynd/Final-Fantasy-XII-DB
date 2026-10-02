"""Small original failure path + native malloc boundary + PE declaration."""
import importlib.util,hashlib,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('capture',P/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());C.EXE=C.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=C.ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
C.RANGES=[(0x20c300,0x20c438),(0x210ec0,0x210ecb),(0x85e730,0x85e737)]
sys.argv=[sys.argv[0],str(P/'source-01.json')];C.main()
raw=C.EXE.read_bytes();pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,off in secs:
  if C.BASE+rva<=a and a+n<=C.BASE+rva+size:return raw[off+a-C.BASE-rva:off+a-C.BASE-rva+n]
 raise RuntimeError('unbacked import declaration')
def name(a):
 b=read(a,96)
 if b'\0' not in b:raise RuntimeError('unbounded import name')
 return b.split(b'\0',1)[0].decode('ascii')
dirva=C.BASE+struct.unpack_from('<I',raw,pe+24+0x78)[0];matches=[]
for k in range(256):
 oft,ts,chain,nrva,ft=struct.unpack('<IIIII',read(dirva+20*k,20))
 if nrva==0:break
 for j in range(4096):
  item=struct.unpack('<Q',read(C.BASE+(oft or ft)+8*j,8))[0]
  if not item:break
  if C.BASE+ft+8*j==0x8c2b40:
   if item>>63:raise RuntimeError('unexpected ordinal allocation import')
   matches.append({'dll':name(C.BASE+nrva),'name':name(C.BASE+item+2),'iat_va':'0x8c2b40','hint_name_va':hex(C.BASE+item),'iat_file_bytes':read(0x8c2b40,8).hex(),'lookup_file_bytes':read(C.BASE+(oft or ft)+8*j,8).hex()})
 else:raise RuntimeError('unbounded import descriptor')
else:raise RuntimeError('unbounded import directory')
if len(matches)!=1 or matches[0]['name']!='malloc':raise RuntimeError('missing/ambiguous expected allocation import')
p=P/'source-01.json';x=json.loads(p.read_text());x['import_declaration']=matches[0];x['import_limits']='Shipping PE declaration only, not actual loaded DLL/target or observed allocation failure';x['wrapper_complete']=True;x['invocation_driver_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
