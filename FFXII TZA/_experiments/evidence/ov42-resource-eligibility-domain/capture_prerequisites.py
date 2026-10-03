"""Check the actual extent/capture artifacts, not just successful child exits.

Small packet-local prerequisite check for the demonstrated metadata/wrapper gap.
Does not replace the reviewed byte/access annotation validator.
"""
import hashlib,json
from pathlib import Path
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(folder,prepare,capture,extent_tag,capture_tag,metadata,source,entries):
 folder=Path(folder)
 for tag,driver in [(extent_tag,prepare),(capture_tag,capture)]:
  s=json.loads((folder/(tag+'.status.json')).read_text())
  if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s.get('driver_sha256')!=sha(folder/driver):raise ValueError('required successful '+tag)
  if not(folder/(tag+'.stdout')).read_bytes() or(folder/(tag+'.stderr')).read_bytes():raise ValueError('required clean nonempty '+tag)
 e=json.loads((folder/metadata).read_text());c=json.loads((folder/source).read_text())
 if e.get('complete') is not True or e.get('driver_sha256')!=sha(folder/prepare):raise ValueError('required complete current extent artifact')
 if c.get('wrapper_complete') is not True or c.get('invocation_driver_sha256')!=sha(folder/capture):raise ValueError('required complete current capture wrapper')
 if e.get('exe_sha256')!=c.get('exe_sha256'):raise ValueError('extent/capture image mismatch')
 bodies=e.get('bodies');ranges=c.get('ranges')
 if not isinstance(bodies,list) or not bodies or not isinstance(ranges,list) or [b['entry'] for b in bodies]!=entries or len(ranges)!=len(bodies):raise ValueError('required extent/capture population')
 for b,r in zip(bodies,ranges):
  blob=bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))
  if (b['entry'],b['end_exclusive'],b['sha256'])!=(r['start'],r['end_exclusive'],r['sha256']) or len(blob)!=b['bytes'] or blob.hex()!=b['physical_bytes'] or hashlib.sha256(blob).hexdigest()!=b['sha256']:raise ValueError('extent/capture byte identity differs')
 return dict(status='VERIFIED_ACTUAL_CAPTURE_PREREQUISITES',metadata=metadata,metadata_sha256=sha(folder/metadata),source=source,source_sha256=sha(folder/source),checker_sha256=sha(Path(__file__)))
