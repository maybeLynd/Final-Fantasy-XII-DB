"""Method A named Phyre2D constructor/admission/update path, not live state.

Reuse actual reviewed capture/annotation adapters. Bind the one identified
virtual entry through raw RTTI/table identity; adjacent RTTI is not another slot.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'texture-async-count-path-source-01.json'
if out.exists():raise ValueError('immutable source exists')
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong original image')
p=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,p+6)[0];opt=struct.unpack_from('<H',d,p+20)[0]
sec=[struct.unpack_from('<IIII',d,p+24+opt+40*k+8) for k in range(ns)]
def read(a,n):
    for vs,va,rs,ro in sec:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('whole range not backed by original bytes')
rva,size=struct.unpack_from('<II',d,p+24+112+3*8)
if size%12:raise ValueError('incomplete exception directory')
pd=[tuple(x+0x120000 for x in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
entries=[(0x6160B0,0x61613B,0x1DA855C),(0x62C360,0x62C563,0x1DA84D0),(0x62EB90,0x62EBBD,0x1DDF508),(0x622010,0x6221DC,0x1D8F424)]
if any(e not in pd for e in entries) or any(a<=0x621FF0<b for a,b,u in pd):raise ValueError('named root/leaf metadata changed')
if read(0x621FFC,4)!=bytes([0xCC])*4:raise ValueError('tail leaf padding changed')
vt=0xD54348;col=struct.unpack('<Q',read(vt-8,8))[0];td=0x120000+struct.unpack_from('<I',read(col,24),12)[0]
name=read(td+16,192).split(b'\0',1)[0]
if col!=0x1D12448 or td!=0x1F5C5A0 or name!=b'.?AV?$TAsyncUpdate@VPTexture2DD3D11@PRendering@Phyre@@@@' or struct.unpack('<Q',read(vt,8))[0]!=0x621FF0:raise ValueError('actual RTTI/slot0 identity changed')
spec=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(a,b) for a,b,u in entries]+[(0x621FF0,0x621FFC)];sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text())
spec=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
agreement=S.validate(raw)
raw.update(wrapper_complete=True,pdata_entries=[list(e) for e in entries],exception_directory=dict(rva=hex(rva),bytes=size),
           leaf=dict(start='0x621ff0',end_exclusive='0x621ffc',padding='cc'*4,normal_extent_requires_tail_binding=True),
           table=dict(address=hex(vt),COL=hex(col),type_descriptor=hex(td),name=name.decode(),slot0='0x621ff0',raw_from_minus8=read(vt-8,24).hex(),
                      col_bytes=read(col,24).hex(),type_name_bytes=name.hex(),adjacent_at_plus8='0x1d124c8',limits='Identified slot0 only; nextword is adjacent RTTI, not an inferred function slot'),
           annotation_prerequisite=agreement,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           limits='Original physical code/RTTI source only; normal dataflow/CFG and type-layout premises need reduction. No executed queue entry, actual count/lifetime, native service effects, title-object binding or runtime observation.')
out.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8');print('Original2D count/admission/callback sources and one RTTI-bound virtual entry captured; reduction pending')
