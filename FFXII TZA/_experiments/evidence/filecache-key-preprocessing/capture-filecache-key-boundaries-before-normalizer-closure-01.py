"""Bounded original cache normalizer/lookup/fill fragments; no process state."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
out = W/'filecache-key-boundaries-source-01.json'
if out.exists():
    raise ValueError('immutable source exists; reconcile')
spec = importlib.util.spec_from_file_location('existing_key_capture', W/'capture-index-path.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
C.RANGES = [(0x20c440,0x20c46b), (0x20be50,0x20bf9e),
            (0x20c1b0,0x20c2f2), (0x59a9b0,0x59aad5)]
sys.argv = [sys.argv[0],str(out)]
C.main()
raw = json.loads(out.read_text())
spec = importlib.util.spec_from_file_location('existing_key_annotation', W/'validate-title-source-annotations.py')
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
raw.update(wrapper_complete=True, annotation_prerequisite=V.validate(raw),
           invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           limits='Declared normal fragments only, no CRT effects, all insertion paths, initialized cache or natural reachability')
out.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
for r in raw['ranges']:
    print('RANGE',r['start'],r['end_exclusive'],r['sha256'])
    for i in r['instructions']:
        print(i['pc'],i['mnemonic'],i['args'])
