import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(w):
 r=w/'run-01';i=json.loads((r/'identity.json').read_bytes());outer=json.loads((w/'capture-terminal.json').read_bytes())
 assert outer['returncode']==0 and outer['terminal'] and not outer['stderr']
 assert sha(w/'capture.py')==outer['driver_sha256']==i['driver_sha256']
 for s in i['source']:assert sha(r/s['copy'])==s['sha256']
 assert sha(r/'retained-empty-seed.json')==i['seed_sha256']
 assert not (r/'failure.txt').exists()
 receipts={n:json.loads((r/(n+'-terminal.json')).read_bytes()) for n in ['first','second','boardcheck-first','boardcheck-second']}
 for n,p in receipts.items():assert p['returncode']==0 and p['terminal'] and not p['stderr'],n
 assert receipts['first']['argv']==receipts['second']['argv'] and '--apply' in receipts['first']['argv']
 for n in ['boardcheck-first','boardcheck-second']:assert receipts[n]['stdout'].splitlines()==['board ok: ok']
 first=json.loads(receipts['first']['stdout']);second=json.loads(receipts['second']['stdout'])
 assert len(first)==2 and {x['transition'] for x in first}=={'REPAIR','INCORPORATE'} and all(x['status']=='created' for x in first)
 assert len(second)==2 and all(x['transition']=='DONE-ALREADY' and x['status']=='-' for x in second)
 before=json.loads((r/'before-board.json').read_bytes());after=json.loads((r/'after-first-board.json').read_bytes())
 assert before['revision']==6 and after['revision']==8 and len(before['tasks'])==2 and len(after['tasks'])==4
 assert before['tasks']==after['tasks'][:2] and before['history']==after['history'][:6]
 assert len(after['history'])==8
 wanted={'AUTO-INCORP-FIXTURE-REVIEW-ACCEPT':'SWE2-DATA','AUTO-REPAIR-FIXTURE-REVIEW-REJECT':'OPUS'}
 actual=after['tasks'][2:];assert {t['id'] for t in actual}==set(wanted)
 for t in actual:
  assert t['status']=='READY' and t['agent'] is None and t['assigned_to']==wanted[t['id']] and t['requester']=='SWE2-FRONTIER'
  assert t['reviews'] if 'reviews' in t else True
 for h,t in zip(after['history'][6:],actual,strict=True):
  assert h['agent']=='SWE2-FRONTIER' and h['session']=='FIXTURE-ASTRA-TRANSITION-WRITE'
  assert h['operation']['action']=='add' and h['operation']['task']['id']==t['id']
 journal=[json.loads(s) for s in (r/'after-first-journal.jsonl').read_text().splitlines() if s]
 assert [s['kind'] for s in journal]==['genesis','intent','commit','intent','commit']
 assert [s['rev'] for s in journal]==[6,7,7,8,8]
 assert journal[-1]['board_sha']==hashlib.sha256((r/'after-first-board.json').read_text().encode()).hexdigest()
 for intent,h in zip([s for s in journal if s['kind']=='intent'],after['history'][6:],strict=True):
  assert intent['op_sha']==hashlib.sha256(json.dumps(h['operation'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 assert (r/'after-first-board.json').read_bytes()==(r/'after-second-board.json').read_bytes()
 assert (r/'after-first-journal.jsonl').read_bytes()==(r/'after-second-journal.jsonl').read_bytes()
 summary=json.loads((r/'summary.json').read_bytes())
 assert summary['private_lock_absent'] and summary['unchanged_sources'] and summary['parent_children_terminal']
 return {'verdict':'ACCEPT scoped real transition/writer integration and repeated dispatch','first':'two exact derived requests committed through original writer','second':'same board/journal bytes, no new request','source':[s['commit'] for s in i['source']],'limits':'Synthetic review declarations, not actual project reviewers/pilot. Child exit/Saved conditions inferred from exact original caller status, not separately captured child stdout. No races/fairness/cancellation/quota/controller/native host or whole A14/A16 acceptance.'}
if __name__=='__main__':print(json.dumps(check(Path(__file__).resolve().parent),indent=2))
