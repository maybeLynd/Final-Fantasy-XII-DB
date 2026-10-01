"""Offline instruction correction and bounded historical-evidence assessment."""
import ast
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[3]/'Tools/analysis-kit/gfz-scripts/runtime_probe.py'
def sha(raw):return hashlib.sha256(raw).hexdigest()
before=(HERE/'runtime-probe-before.py').read_bytes();after=SOURCE.read_bytes()
a=ast.parse(before);b=ast.parse(after)
assert isinstance(a.body[0].value,ast.Constant) and isinstance(b.body[0].value,ast.Constant)
a.body=a.body[1:];b.body=b.body[1:]
assert ast.dump(a)==ast.dump(b),'implementation changed'
assert b'--type GameSettingConfig --at 0x01F82D20' not in after
assert b'--deref 0x01F82D20 --type GameSettingConfig' in after
tsv=HERE.parents[1]/'EXP-001-gamesetting-frametimebase.tsv'
original=subprocess.check_output(['git','show','e1fc2df:'+tsv.relative_to(Path.cwd()).as_posix()])
# Git may normalize CRLF; compare records, retaining hashes for both byte streams.
rows=list(csv.DictReader(io.StringIO(tsv.read_text()),delimiter='\t'))
assert rows==list(csv.DictReader(io.StringIO(original.decode()),delimiter='\t'))
indirect={x['id']:x['address'] for x in rows if x['address'].startswith('[0x01F82D20]')}
assert set(indirect)=={'E1','E6','E7','E8','E9','E10','E11','E12'}
historical=[]
for path in sorted(HERE.parent.glob('EXP-001-gamesetting-frametimebase-*.json')):
    data=json.loads(path.read_text())
    observations=data.get('passes',[data['observation']])
    saved=[]
    for observation in observations:
        assert observation['argv']==['runtime_probe.py','--check','EXP-001-gamesetting-frametimebase.tsv']
        lines=observation['stdout'].splitlines()
        saved.append(dict(argv=observation['argv'],returncode=observation['returncode'],
            indirect_rows=[line for line in lines if line.split() and line.split()[0] in indirect],
            error=observation['stderr']))
    historical.append(dict(path=path.name,sha256=sha(path.read_bytes()),observations=saved))
assert len(historical)==4
pin=HERE.parent/'EXP-037-command-observer/dependencies.json'
pinned=json.loads(pin.read_text())['../../../../Tools/analysis-kit/gfz-scripts/runtime_probe.py']
assert pinned==sha(before) and pinned!=sha(after)
result=dict(status='PASS',scope='documentation-only correction and bounded retained-evidence assessment',
            before_sha256=sha(before),after_sha256=sha(after),implementation_ast_unchanged=True,
            tsv_sha256=sha(tsv.read_bytes()),original_tsv_sha256=sha(original),indirect_rows=indirect,
            historical=historical,exp037_pinned_sha256=pinned,exp037_requires_new_qualification=True)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'runtime-probe-after.py').write_bytes(after)
(HERE/'manifest.json').write_text(json.dumps({'files':{p.name:dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
    for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='manifest.json'}},indent=2)+'\n')
print('PASS: implementation unchanged; four historical captures used --check; eight config rows dereference; EXP037 old pin rejects new source')
