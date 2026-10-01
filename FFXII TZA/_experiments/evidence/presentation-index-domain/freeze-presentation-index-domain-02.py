"""Additive second freeze after a correctly refused publication interface."""
import hashlib,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'presentation-index-domain';F=W/'presentation-index-domain-frozen-ready-02';old=W/'presentation-index-domain-frozen-ready'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if sha(old/'manifest.json')!='091371928365d23a91d4f58ef522cd5a67d5fb1649e14077165ec3f9ab9fa09e':raise RuntimeError('original refused freeze changed')
for m in json.loads((old/'manifest.json').read_text())['members']:
 if sha(old/m['path'])!=m['sha256']:raise RuntimeError('old frozen member changed')
for tag,driver in [('capture-01','capture.py'),('proof-01','prove.py'),('control-03','control.py'),('binding-01','bind-publication-source.py')]:
 st=json.loads((P/(tag+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise RuntimeError('failed/incomplete '+tag)
v=json.loads((P/'result-02.json').read_text());binding=json.loads((P/'source-binding-01.json').read_text());controls=json.loads((P/'proof-controls-02/result.json').read_text())
if v.get('producer_complete') is not True or len(v['equal_branch']['cases'])!=256 or len(v['source_pins'])!=2 or binding['semantic_fields_unchanged'] is not True or controls.get('complete') is not True or len(controls['cases'])!=4 or not all(r['passed'] for r in controls['cases']):raise RuntimeError('incomplete proof/binding/control')
if F.exists():raise RuntimeError('immutable new freeze exists')
shutil.copytree(P,F);(F/'.gitattributes').write_text('* -text\n')
shutil.copytree(old/'dependencies',F/'dependencies')
shutil.copyfile(old/'manifest.json',F/'retained/refused-freeze-01-manifest.json')
shutil.copyfile(W/'freeze-presentation-index-domain.py',F/'freeze-presentation-index-domain.py')
shutil.copyfile(Path(__file__),F/'freeze-presentation-index-domain-02.py')
(F/'PUBLICATION-CORRECTION.md').write_text('''# Source-map binding correction

First actual publication was refused before preparation/canonical writes because
result01 used singular annotation/source fields instead of the shared guard's
required source_pins map. Brief @publication lease was released45387; no guard
was bypassed or weakened. Original82-member frozen inputs/results/manifest are
unchanged, retained here by manifest reference. They were never published as an
accepted packet. Scientific proof01/source/counter-control result remain intact.

bind-publication-source.py requires actual terminal proof/driver/source hashes,
preserves every original scientific result field and adds two explicit source
pins in result02. It invokes the actual publisher annotation function: original
missing map refused for exact reason, bound map passed with two re-decoded
sources. source-binding01 plus binding01 CLI receipts preserve that path.
This is publication admission evidence, not another original-code/game test or
independent semantic acceptance. Use result02 for publication; result01 remains
the original producer proof. No scientific case repeated to fix the interface.
''')
members=[{'path':str(p.relative_to(F)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps({'package':'presentation-index-domain','method':'A STATIC_ONLY source/address proof','members':members,'limits':'Original immutable scientific proof + additive actual publication map binding; not independent acceptance/natural reachability.'},indent=2)+'\n')
print(json.dumps({'members':len(members),'manifest_sha256':sha(F/'manifest.json'),'frozen':str(F)}))
