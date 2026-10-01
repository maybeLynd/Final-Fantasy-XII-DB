"""Initial read-only identity/decoding gate; semantic reducer follows primary review."""
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
def check(root=W):
 root=Path(root);raw=json.loads((root/'raw.json').read_bytes())
 for b in raw['bodies']:
  data=(root/'retained'/(b['name']+'.bin')).read_bytes()
  assert len(data)==b['bytes'] and hashlib.sha256(data).hexdigest()==b['sha256']
  assert b''.join(bytes.fromhex(x['bytes']) for x in b['instructions'])==data
 assert len(raw['bodies'])==3
 return {'status':'IDENTITY_ONLY_SEMANTIC_REVIEW_PENDING','limits':raw['limits']}
if __name__=='__main__':print(json.dumps(check(Path(sys.argv[1]) if len(sys.argv)>1 else W),indent=2))
