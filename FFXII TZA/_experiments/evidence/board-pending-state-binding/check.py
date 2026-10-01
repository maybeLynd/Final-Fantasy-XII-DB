"""Read-only reduction of actual original CLI observations; no writer rerun."""
import copy,hashlib,json
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()

def reduce(raw,run):
 assert raw['state']=='OBSERVED' and 'exception' not in raw
 assert sha((run/'team.py').read_bytes())==raw['identity']['source_sha256']
 assert sha((run/'capture.py').read_bytes())==raw['identity']['driver_sha256']
 parent=(run/'parent/board.json').read_bytes();journal=(run/'parent/journal.jsonl').read_bytes()
 prefix=b''.join(journal.splitlines(keepends=True)[:-1])
 recs=[json.loads(x) for x in journal.decode().splitlines()]
 assert [r['kind'] for r in recs]==['genesis','intent','commit'] and recs[-1]['board_sha']==sha(parent)
 cases={c['name']:c for c in raw['cases']}
 assert len(cases)==len(raw['cases'])==3 and set(cases)=={'healthy-prefix','changed-checkpoint','different-last-operation'}
 for name,c in cases.items():
  d=run/name;b=(d/'before-board.json').read_bytes();jb=(d/'before-journal.jsonl').read_bytes()
  after=(d/'after-board.json').read_bytes();ja=(d/'after-journal.jsonl').read_bytes()
  assert c['schema_valid_before'] is True and sha(b)==c['before_board_sha256'] and sha(jb)==c['before_journal_sha256']
  assert jb==prefix and sha(after)==c['after_board_sha256'] and sha(ja)==c['after_journal_sha256']
  assert c['matches_observed_parent_commit']==(sha(b)==recs[-1]['board_sha'])
  expected=json.loads(parent)
  if name=='changed-checkpoint':expected['checkpoints'][0]['note']='different retained checkpoint value'
  elif name=='different-last-operation':expected['history'][-1]['operation']['note']='different last operation value'
  assert json.loads(b)==expected
  w=c['writer'];assert w['terminal'] is True and w['timed_out'] is False and w['elapsed_seconds']<6
  assert w['argv'][0]==raw['identity']['python_executable'] and w['argv'][1:3]==['-B',raw['identity']['source_path']]
  assert w['argv'][w['argv'].index('--expect-revision')+1]=='1'
  assert w['argv'][w['argv'].index('--session')+1]==name
  assert json.loads((d/'operation.json').read_bytes())=={'action':'note','note':'fresh follow-on after '+name}
  assert c['private_lock_absent'] is True
  if name=='different-last-operation':
   assert w['returncode']==1 and not w['stdout'] and 'different last op' in w['stderr']
   assert b==after and jb==ja and c['health'] is None
  else:
   assert w['returncode']==0 and w['stdout'].splitlines()==['Saved revision 2'] and not w['stderr']
   h=c['health'];assert h['returncode']==0 and h['stdout'].splitlines()==['board ok: ok'] and not h['stderr']
   assert h['terminal'] is True and h['timed_out'] is False
   board=json.loads(after);jr=[json.loads(x) for x in ja.decode().splitlines()]
   assert board['revision']==2 and len(board['history'])==2
   assert board['checkpoints'][0]==expected['checkpoints'][0]
   assert board['checkpoints'][1]['note']=='fresh follow-on after '+name
   assert jr[:2]==recs[:2] and [x['kind'] for x in jr]==['genesis','intent','commit','intent','commit']
   assert jr[2]['healed'] is True and jr[2]['rev']==1 and jr[2]['board_sha']==sha(b)
   assert jr[-1]['rev']==2 and jr[-1]['board_sha']==sha(after)
 assert all(raw['cleanup'][k] is True for k in ['owned_processes_terminal','source_unchanged','all_private_locks_absent','original_parent_bytes_unchanged','production_board_not_a_fixture'])
 return {'established':'Original pending heal promotes changed full state when revision/last operation match; different-last-operation control refuses',
 'healthy_prefix':'accepted and healed','changed_checkpoint_same_last_op':'accepted, changed value persists, new healed hash binds it',
 'different_last_operation':'refused, exact board/journal unchanged',
 'full_A13':'NOT_ACCEPTED','limits':'Constructed copied prefix/state interventions; no genuine interruption, actual production divergence, recovery/deployment or game behavior proof.'}

if __name__=='__main__':
 run=Path(__file__).resolve().parent/'run-01';raw=json.loads((run/'raw.json').read_bytes());result=reduce(raw,run)
 controls=[]
 for name in ['missing-negative-control','hidden-failed-exit']:
  bad=copy.deepcopy(raw)
  if name=='missing-negative-control':bad['cases']=bad['cases'][:-1]
  else:bad['cases'][-1]['writer']['returncode']=0
  try:reduce(bad,run)
  except AssertionError:controls.append({'name':name,'refused':True})
  else:raise AssertionError('Malformed receipt admitted')
 print(json.dumps({'result':result,'receipt_controls':controls},indent=2))
