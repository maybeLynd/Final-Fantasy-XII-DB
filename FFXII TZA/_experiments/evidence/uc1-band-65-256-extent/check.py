"""Read-only reproduction of bounded extent receipt; no independent acceptance."""
import collections,csv,hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();r=json.loads((W/'result.json').read_text())
assert r['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and r['driver_sha256']==sha((W/'review.py').read_bytes())
source=(R/'old-flow.py').read_text();prefix=source[:source.index('adm = table(ADM)')];assert sha(prefix.encode())==r['reference']['flow_prefix_sha256'] and sha((R/'old-flow.py').read_bytes())==r['reference']['full_flow_source_sha256']
# Keep the original source location so its existing ROOT computation and reader path
# stay exactly the same. Only code before the old population sweep is evaluated.
original=next(x for x in r['inputs'] if x['name']=='old-flow.py');root=next(p for p in W.parents if (p/'Database').is_dir() and (p/'Collaboration').is_dir());ns={'__file__':str(root/original['path'])};exec(compile(prefix,'retained-old-flow-prefix','exec'),ns);assert sha(ns['raw'])==r['reference']['exe_sha256']
def table(p):return list(csv.DictReader([l for l in p.read_text(encoding='utf-8-sig').splitlines() if l and not l.startswith('#')],delimiter='\t'))
band=table(R/'band.tsv');selected=[x for x in band if x['outcome']=='clean'];assert len(band)==120 and len(selected)==100
membership={x['start_va']:x for x in table(R/'admission-membership.tsv')};assert len(membership)==120
listed={int(x['entry'],16):int(x['bytes']) for x in table(R/'listed-span-projection.tsv')};assert listed and len(listed)==r['population']['listed_spans']==34270
obs=r['observations'];assert len(obs)==100 and {x['candidate']['start_va'] for x in obs}=={x['start_va'] for x in selected}
for x in obs:
 c=x['candidate'];a,n=int(c['start_va'],16),int(c['bytes']);assert c in selected and membership[c['start_va']]['bytes']==c['bytes'] and membership[c['start_va']]['prev_entry']==c['prev_entry']
 data=bytes.fromhex(x['raw_hex']);assert len(data)==n and sha(data)==x['sha256'] and data==ns['bytes_at'](a,n)
 f=ns['flow'](a,n,data);assert f==x['flow'] and f['full_linear'] and not f['problems']
 seen=[i for i in f['instructions'] if i[4]];assert seen and len(seen)==x['reachable_instruction_count']
 end=max(int(i[0],16)+len(bytes.fromhex(i[1])) for i in seen);assert hex(end)==x['max_reachable_end'] and data[end-a:].hex()==x['unreachable_trailing_bytes']==''
 assert not [v for v in listed if a<=v<a+n] and not x['listed_entries']
 assert not [v for v,z in listed.items() if v<a+n and a<v+z] and not x['catalog_numeric_span_overlaps']
 assert x['verdict']=='PASS_BOUNDED_EXTENT' and x['bounded_extension'] is None
 ex=[e for e in f['exits'] if e[1] in ('external/direct','indirect')];assert len(ex)==len(x['external_edges'])
 for (site,kind),e in zip(ex,x['external_edges']):
  assert e['site']==site
  if kind=='external/direct':
   ins=next(i for i in f['instructions'] if i[0]==site);assert hex(int(ins[3],16))==e['target'] and e['listed_entry_exact']==(int(e['target'],16) in listed)
assert dict(collections.Counter(x['verdict'] for x in obs))==r['summary']['verdict_counts']=={'PASS_BOUNDED_EXTENT':100}
assert r['summary']['rows_with_external_edges']==['002E4C90','002E5B00','00708270'] and r['summary']['rows_with_tail_bytes']==r['summary']['rows_with_numeric_catalog_overlap']==[]
for name,c in r['controls'].items():
 data=bytes.fromhex(c['raw_hex']);a=int(c['start'],16);assert data==ns['bytes_at'](a,c['bytes']) and ns['flow'](a,c['bytes'],data)==c['flow']
assert r['controls']['known-truncated-store48']['flow']['problems'] and not r['controls']['known-complete-store57']['flow']['problems']
failure=json.loads((R/'initial-failure.json').read_text());assert failure['observed_filtered_entries']==34270 and failure['driver_sha256']==sha((R/'initial-failed-review.py').read_bytes()) and failure['result']=='INVALID_PREFLIGHT, no semantic results'
ctx=json.loads((R/'external-target-context.json').read_text());old=ctx['prior_observation'];assert ctx['target']=='0x71bb70' and ctx['fable_row']['ruling']=='admit' and old['candidate']['bytes']=='32';data=bytes.fromhex(old['raw_hex']);assert len(data)==32 and data==ns['bytes_at'](0x71BB70,32) and not old['flow']['problems']
for inp in r['inputs']:
 path=R/inp['name']
 if path.exists():assert sha(path.read_bytes())==inp['sha256']
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  d=(W/x['path']).read_bytes();assert len(d)==x['bytes'] and sha(d)==x['sha256']
print('PASS_BOUNDED_UC1_65_256 100 exact selected spans; no reachable truncation/interior boundary or listed-span collision. Three direct-exit rows retained, not completefunction/population proof. Truncated-store detection control passes.')
