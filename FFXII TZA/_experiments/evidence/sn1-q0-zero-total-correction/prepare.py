import hashlib,json,re,subprocess,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-source-coordinate-domain');Q=W.parent/'sn1-q0-source-coordinate-domain';R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-Q0-ZERO-TOTAL-CORRECTION');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not R.exists();R.mkdir()
for n in ['check.py','capture.py','README.md','result.json','manifest.json','default-invocation.stdout']:(R/('original60-'+n)).write_bytes((P/n).read_bytes())
assert (Q/'check.py').read_bytes()==(P/'check.py').read_bytes()
(R/'work60-check-preimage.py').write_bytes((Q/'check.py').read_bytes());(R/'work60-capture-preimage.py').write_bytes((Q/'capture.py').read_bytes())
peer=Path('Database/FFXII TZA/_index/candidates/sn1-q0-source-domain')
for n in ['README.md','q0_domain.py','q0_domain.out']:
 if (peer/n).exists():(R/('fable-'+n)).write_bytes((peer/n).read_bytes())
raw60=json.loads((P/'raw.json').read_text());res60=json.loads((P/'result.json').read_text());counts={};total=0
for m in raw60['modules']:
 b=(P/'retained'/(m['name']+'.dbg')).read_bytes();k=0
 for sc in m['scopes']:
  for x in sc['records']:
   data=b[x['file_offset']:x['file_offset']+4];assert data.hex()==x['record_hex']
   if data==b'\0'*4:k+=1
 counts[m['name']]=k;total+=k
assert total==res60['coordinate_counts']['zero-line-convention-unresolved']==sum(x['count'] for x in res60['zero_suffixes'])
prose=int(re.search(r'All(\d+) line0',res60['interpretation']).group(1));assert prose!=total and (prose,total)==(61,59)
raw=dict(question='Why did60 report61 zero suffix records although numeric/raw original data reports59?',method='A immutable original60 byte records/numeric result and actual producer source; no recapture/execution',parent=P.as_posix(),parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),parent_raw_sha256=sha((P/'raw.json').read_bytes()),parent_result_sha256=sha((P/'result.json').read_bytes()),original_checker_sha256=sha((P/'check.py').read_bytes()),by_module=counts,actual_zero_total=total,incorrect_text_total=prose,cause='Hardcoded unchecked interpretation/stdout, while numeric field and physical byte counter are59; control/counter/data did not regress',affected_claims=['60 README/check interpretation/stdout/default stdout and result.interpretation','60 delivery task question/board note/ASTRA handoff prose total61','FABLE flagged discrepancy; OPUS/DATA/SPEC pending payloads must use59'],unaffected=['Original eight input identities/raw bytes and numeric coordinate_counts','six internal EOF+1 records and nine lineCount coordinates','0..3 suffix bound/five scopes with3, no interior all-zero records','61 source-statement anchors and their original code identities','canonical index not reported regressed'],consumer='FABLE/DATA/OPUS/SPEC original60 consumers; original package remains immutable with additive correction',cleanup='PC OFF; no game/save/config/reference/peer writes')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
src=(P/'check.py').read_text()
a="W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()"
z="OUT=Path(__file__).resolve().parent;W=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-source-coordinate-domain');R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()"
assert src.count(a)==1;src=src.replace(a,z).replace('import ast,collections,hashlib,json,struct,sys','import ast,collections,hashlib,json,re,struct,sys')
a="result=dict(method=raw['method']";z="zero_total=all_counts['zero-line-convention-unresolved'];assert zero_total==sum(x['count'] for x in zero_details)\nreported_total=zero_total+(2 if '--fault-stale-total' in sys.argv else 0)\nresult=dict(method=raw['method']"
assert src.count(a)==1;src=src.replace(a,z)
a="interpretation='Two source block2";assert src.count(a)==1;src=src.replace(a,"interpretation=f'Two source block2").replace('All61 line0','All{reported_total} line0')
a="out=W/'result.json'";z="assert int(re.search(r'All(\\d+) line0',result['interpretation']).group(1))==zero_total, 'Prose total must equal original reduced zero total'\nout=OUT/'corrected-result.json'"
assert src.count(a)==1;src=src.replace(a,z)
a="print('PASS60 retained8 inputs/source parser/50 coordinate maps;6 internal EOF+1 records,61 all-zero suffixes; actual raw4B positive/block/line controls, no compiler/native/game execution',flush=True)"
z="print(f'PASS_CORRECTED60 retained8 inputs/source parser/50 coordinate maps;6 internal EOF+1 records,{zero_total} all-zero suffixes; derived prose/numeric/raw count agreement, no compiler/native/game execution',flush=True)"
assert src.count(a)==1;src=src.replace(a,z)
(W/'corrected60-check.py').write_text(src)
shim="\"\"\"Additive62 producer correction; immutable60 original checker retained.\"\"\"\nimport runpy\nfrom pathlib import Path\np=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-zero-total-correction/corrected60-check.py')\nassert p.exists(), 'Correction publication missing; do not fall back to stale unchecked total'\nrunpy.run_path(str(p),run_name='__main__')\n"
(W/'work60-default-check.py').write_text(shim)
print('PREPARED62 original raw/numeric',counts,total,'stale prose',prose,flush=True)
