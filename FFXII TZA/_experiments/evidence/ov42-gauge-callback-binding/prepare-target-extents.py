"""Reuse existing PE/unwind preparation for one callback-consumer discriminator.

The exact source specialization is recorded, not a new general analyzer. Does
2973E0 directly/indirectly call either registered handler, or do the handlers
call this consumer? This extends only that unresolved call-direction boundary.
"""
import hashlib
import json
import sys
from pathlib import Path

P = Path(__file__).resolve().parent
source = (P/'prepare-handler-extents.py').read_bytes()
text = source.decode()
old = "({'lookup-primary-handler-01.json':['0x29b7d0','0x29b7d1'],'lookup-secondary-handler-01.json':['0x29b810','0x29b811']}[n])"
assert text.count(old) == 1
assert text.count("lookups=['lookup-primary-handler-01.json','lookup-secondary-handler-01.json']") == 1
assert text.count('for entry in [0x29b7d0,0x29b810]:') == 1
text = text.replace(old, "['0x2973e0','0x2974d7']")
text = text.replace("lookups=['lookup-primary-handler-01.json','lookup-secondary-handler-01.json']", "lookups=['lookup-target-01.json']")
text = text.replace('for entry in [0x29b7d0,0x29b810]:', 'for entry in [0x2973e0]:')
namespace = dict(__name__='scoped_target_preparation', __file__=str(Path(__file__).resolve()))
exec(compile(text, str(P/'prepare-handler-extents.py'), 'exec'), namespace)
namespace['main']()
out = P/sys.argv[1]
x = json.loads(out.read_text())
x['reused_preparation_sha256'] = hashlib.sha256(source).hexdigest()
x['specialized_source_sha256'] = hashlib.sha256(text.encode()).hexdigest()
out.write_text(json.dumps(x, indent=2)+'\n')
