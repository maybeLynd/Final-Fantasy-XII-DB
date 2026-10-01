import json
from pathlib import Path
def validate_manifest_pins(pkg,pins):
 pkg=Path(pkg);m=json.loads((pkg/'manifest.json').read_text());assert m['members'],'Empty manifest cannot pass'
 for x in m['members']:
  rel=Path(x['path']);assert not rel.is_absolute() and '..' not in rel.parts,'Invalid manifest member path'
  p=(pkg/rel).as_posix();assert p in pins,'Manifest member absent from reviewed pins: '+p
 return len(m['members'])
