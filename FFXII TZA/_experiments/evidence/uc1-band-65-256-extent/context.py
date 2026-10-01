"""Reuse existing 1-64 B evidence for the only unlisted external target; no resweep."""
import csv,hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest();out=W/'retained/external-target-context.json';assert not out.exists()
p=W.parent/'uc1-band-ruling/observation.json';raw=p.read_bytes();old=json.loads(raw)
observed=next(x for x in old['observations'] if x['candidate']['start_va']=='0071BB70');assert observed['candidate']['bytes']=='32' and not observed['flow']['problems']
p2=Path('Database/FFXII TZA/_index/candidates/uc1-band-1-64-fable-2026-09-25.tsv');b=p2.read_bytes();rows=list(csv.DictReader([l for l in b.decode().splitlines() if l and not l.startswith('#')],delimiter='\t'));r=next(x for x in rows if x['start_va']=='0071BB70');assert r['ruling']=='admit' and r['bytes']=='32'
out.write_text(json.dumps(dict(target='0x71bb70',prior_astra_source=p.as_posix(),prior_astra_sha256=sha(raw),prior_observation=observed,fable_table=p2.as_posix(),fable_table_sha256=sha(b),fable_row=r,scope='Reuse prior source/flow observation and ruling row. Target32B is separately admitted in old band, not an interior listed entry. No current population update, target-native execution or complete caller-function identity proof.'),indent=2)+'\n');print('Reused prior32B target evidence for00708270 external transfers')
