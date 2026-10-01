"""The only missing3 shipping bytes for the retained caller selector proof."""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('selector_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
s=importlib.util.spec_from_file_location('selector_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x5c5230,0x5c5233)];C.main();r=json.loads(out.read_text())
if [(i['bytes'],i['mnemonic'],i['args']) for i in r['ranges'][0]['instructions']]!=[('33c0','xor','eax, eax'),('c3','ret','')]:raise ValueError('original constant-return leaf changed')
r.update(wrapper_complete=True,annotation_prerequisite=S.validate(r),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Exact reference3B leaf; no additional input/option initialization, effect stub or live reachability inferred')
out.write_text(json.dumps(r,indent=2)+'\n');print('Original3-byte constant-zero leaf; reviewed adapter invocation controls; no game')
