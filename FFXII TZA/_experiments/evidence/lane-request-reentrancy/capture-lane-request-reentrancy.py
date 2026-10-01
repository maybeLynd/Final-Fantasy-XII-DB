"""Exact code and guarded nine-target original dispatch data, not table-as-code."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('reentry_capture','capture-index-path.py');S=module('reentry_annotations','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1]);table=out.with_name('lane-request-pump-dispatch-table-01.json')
if out.exists() or table.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x32e620,0x32e774),(0x32e870,0x32e98d),(0x32e070,0x32e149),(0x32e330,0x32e36b)]
C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=S.validate(v),limits='Complete request/adopter code, conditional pump prefix only and done-helper external tail. No complete pump/cancellation/schedule or natural stale-state proof')
out.write_text(json.dumps(v,indent=2)+'\n')
b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();sha=hashlib.sha256(b).hexdigest()
if sha!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('reference identity moved')
e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
secs=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
a,z=0x32e2d0,0x32e2e8
raw=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in secs if 0x120000+va<=a and z<=0x120000+va+rs)
d=dict(method='A ORIGINAL_DATA',exe_sha256=sha,imagebase='0x120000',start=hex(a),end_exclusive=hex(z),bytes=raw.hex(),sha256=hashlib.sha256(raw).hexdigest(),entries=[dict(state=k,rva=hex(x),target=hex(0x120000+x)) for k,x in enumerate(struct.unpack('<6I',raw))],derivation='Pump BYTEstate-1, CMP5/JA guard supplies6entries. Prefix only, conditional state1 zero-length completion path; not full pump CFG proof',invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
with table.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
print('Request/adopter625B, pump prefix217B/done59B and separate24B table; oldcallback window only')
