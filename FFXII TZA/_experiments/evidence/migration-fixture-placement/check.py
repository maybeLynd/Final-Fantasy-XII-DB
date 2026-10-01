import argparse,base64,hashlib,json
from pathlib import Path
def sha(b):return hashlib.sha256(b).hexdigest()
def reduce(w):
 old=json.loads((w/'run-01/raw.json').read_text());new=json.loads((w/'reader-02/raw.json').read_text())
 assert old['finished'] is False and old['fatal']['type']=='TypeError'
 assert old['driver_sha256']==sha((w/'run-01/driver.py').read_bytes())
 assert old['producer_sha256']==sha((w/'freeze-after.py').read_bytes())
 assert len(old['fixture_members'])==10 and len(old['cases'])==4
 expected={'actual-default':1,'same-source-preflight':1,'clean-source':0,'missing-source':1}
 assert {c['name'] for c in old['cases']}==set(expected)
 for c in old['cases']:
  assert c==json.loads((w/'run-01'/(c['name']+'-receipt.json')).read_text())
  assert c['returncode']==expected[c['name']] and c['terminal'] and c['expected_marker'] in c['stdout']+c['stderr']
 source=(w/'freeze-after.py').read_text()
 assert source.index('fixture_preflight(W)')<source.index("assert not P.exists()")<source.index('shutil.copytree(')
 assert new['finished'] is True and 'fatal' not in new and new['prior_overall_status']=='INVALID_TYPEERROR_RETAINED'
 assert new['prior_raw_sha256']==sha((w/'run-01/raw.json').read_bytes())
 assert new['driver_sha256']==sha((w/'reader-correction.py').read_bytes())
 assert new['source_sha256']==sha((w/'run-01/reader-source.py').read_bytes())
 assert new['observation']['file']=='04-Actor-Entity/control.md' and new['observation']['ids']==['W-999'] and not new['observation']['ticked']
 assert new['all_published_members_unchanged'] is True
 capsule=json.loads((w/'reader-root-inputs.json').read_text());assert len(capsule['members'])==6
 assert {x['path'] for x in capsule['members']}=={'04-Actor-Entity/control.md',*[f'archived-fixture/{p}' for p in ('04-Actor-Entity/answered.md','04-Actor-Entity/dispositioned.md','04-Actor-Entity/partial.md','_index/OPEN-QUESTIONS.md','_index/candidates/register-triage/batch-K-scope-rulings.md')]}
 for m in capsule['members']:
  b=base64.b64decode(m['base64'],validate=True);assert len(b)==m['bytes'] and sha(b)==m['sha256']
 return {'status':'SCOPED_PRODUCER_GUARD_AND_READER_CORRECTION','original_run':'INVALID_TYPEERROR_RETAINED',
         'retained_terminal_producer_controls':4,'fresh_corrected_reader_observations':1,
         'published_old_inputs':'PRESERVED','other_walkers':'NOT_CERTIFIED','independent_acceptance':'PENDING','full_L1_L2':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path);a=ap.parse_args();w=Path(__file__).resolve().parent
 r=reduce(w)
 if a.out:a.out.write_text(json.dumps(r,indent=2)+'\n')
 print('SCOPED_PRODUCER_GUARD_AND_READER_CORRECTION',json.dumps(r,sort_keys=True))
