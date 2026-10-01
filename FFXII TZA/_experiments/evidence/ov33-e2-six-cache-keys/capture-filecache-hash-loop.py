"""Read-only shipping key recurrence, actual shared adapter/annotation path."""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'filecache-hash-loop-source-01.json'
if out.exists():raise ValueError('immutable source exists')
s=importlib.util.spec_from_file_location('hash_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x674a00,0x674a28)];sys.argv=[sys.argv[0],str(out)];C.main()
z=json.loads(out.read_text());s=importlib.util.spec_from_file_location('hash_annotation',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
z.update(wrapper_complete=True,annotation_prerequisite=S.validate(z),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Original40B hash loop only; no normalization CRT effects, actual cache contents/caller reachability or live/native execution.')
out.write_text(json.dumps(z,indent=2)+'\n')
for i in z['ranges'][0]['instructions']:print(i['pc'],i['mnemonic'],i['args'])
print('Hash body SHA',z['ranges'][0]['sha256'])
