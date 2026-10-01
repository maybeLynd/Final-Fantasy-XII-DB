import json,os,subprocess,sys,time
from pathlib import Path
from verify import git,normalized,verify
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
w=Path(__file__).resolve().parent;sid='ASTRA-sol-20260928-sn1-variable-binding';task='ASTRA-PUBLISH-SN1-VARIABLE-BINDING'
pins=json.loads((w/'reviewed.json').read_text());inbox='Database/FFXII TZA/_index/_inbox/ASTRA.md'
assert not (w/'commit.txt').exists()
ok,detail=team.board_status(team.BOARD);assert ok,detail
assert json.loads(team.BOARD.read_text())['recovery_epoch']==json.loads((w/'reviewed-epoch.json').read_text())['epoch']
for p,h in pins.items():assert git('hash-object','--',p)==h,p
assert normalized(Path(inbox).read_text())==(w/'reviewed-inbox-preimage.txt').read_text()
need=[{'key':'@publication'},{'key':'file:database/ffxii tza/_index/_inbox/astra.md'}]
board=json.loads(team.BOARD.read_text())
queued=next((t for t in board['tasks'] if t['id']==task),None)
if queued is None:
 print('DEFERRED before claim; supported publication row has not been added yet:',task,flush=True);sys.exit(0)
assert queued['status']=='READY', 'Publication task is not READY; inspect actual claim/commit before retry'
holders=[t['id'] for t in board['tasks'] if t['status']=='ACTIVE' and t['id']!=task and any(team.overlap(a,b) for a in need for b in team.hold_set(t))]
if holders:
 print('DEFERRED before claim; current holders:',','.join(holders),flush=True);sys.exit(0)
# A read is only a preflight; supported claim below still resolves any race.
deadline=time.monotonic()+300
while True:
 try:
  team.transaction(team.BOARD,'ASTRA',{'action':'claim','task':task,'resources':[{'key':'@publication'},{'key':'file:database/ffxii tza/_index/_inbox/astra.md'}],'note':'Explicit reviewed own evidence/body. Own inbox is briefly reserved with publication only after prior original arithmetic carrier releases it. Postcommit verify logged identity, exact blobs/body/manifest; optional unchanged supported TEAM only if parent same with own ACTIVE publication. No broad tool modification.'},sid);break
 except ValueError as e:
  if not str(e).startswith('resource(s) held by:'):raise
  print('DEFERRED supported claim race:',str(e),flush=True);sys.exit(0)
try:
 for p,h in pins.items():assert git('hash-object','--',p)==h,p
 assert normalized(Path(inbox).read_text())==(w/'reviewed-inbox-preimage.txt').read_text()
 # Install the explicitly reviewed checkpoint only after reserving its file.
 # The caller prepares both exact preimage and next body; no unreviewed edit.
 Path(inbox).write_bytes((w/'reviewed-inbox-next.txt').read_bytes())
 assert normalized(Path(inbox).read_text())==(w/'reviewed-inbox-body.txt').read_text()
 env=os.environ.copy();env.pop('PUBLISH_EXPECT',None);env.update(TEAM_AGENT='ASTRA',TEAM_SESSION=sid)
 env['PATH']=str(Path('Collaboration/Tools/analysis/venv/Scripts').resolve())+os.pathsep+'C:/Program Files/Git/usr/bin'+os.pathsep+'C:/Program Files/Git/bin'+os.pathsep+env['PATH']
 paths=[*pins,inbox,'Database/FFXII TZA/_index/_inbox/TEAM.json']
 r=subprocess.run(['C:/Program Files/Git/bin/bash.exe','Database/Tools/analysis-kit/gfz-scripts/publish_paths.sh',str(w/'message.txt'),*paths],env=env,capture_output=True,text=True)
 (w/'publish-output.txt').write_text(r.stdout+'\n'+r.stderr);assert r.returncode==0,(r.returncode,r.stderr[-2000:])
 receipt=verify(w,task,'Database/FFXII TZA/_experiments/evidence/sn1-variable-name-binding');c=receipt['commit']
 (w/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');(w/'commit.txt').write_text(c+'\n')
 team.transaction(team.BOARD,'ASTRA',{'action':'finish','task':task,'note':'Logged actual commit/exact owned blobs/body/manifest and supported TEAM verified; publication released.','result_refs':[c]},sid)
 print('COMMITTED',c,flush=True)
except BaseException:
 team.transaction(team.BOARD,'ASTRA',{'action':'release','task':task,'note':'Publication stopped; inspect logged commit before any retry. Diagnostics retained, no reset/peer changes.'},sid);raise
