import hashlib,json,re,subprocess
from pathlib import Path
def git(*a):return subprocess.check_output(['git',*a],text=True).strip()
def normalized(s):return re.sub(r'<!-- TEAM-CURRENT:begin.*?<!-- TEAM-CURRENT:end -->','[SUPPORTED GENERATED CURRENT BLOCK]',s,flags=re.S).replace('\r\n','\n')
def verify(w,task,pkg):
 w=Path(w);pins=json.loads((w/'reviewed.json').read_text());log=(w/'publish-output.txt').read_text()
 match=re.search(r'--- committed ---\s*\n([0-9a-f]{7,40})\s',log);assert match,'Missing logged commit identity'
 c=git('rev-parse',match.group(1));assert git('show','-s','--format=%B',c)==(w/'message.txt').read_text().strip()
 assert subprocess.run(['git','merge-base','--is-ancestor',c,'HEAD'],capture_output=True).returncode==0
 inbox='Database/FFXII TZA/_index/_inbox/ASTRA.md';bp='Database/FFXII TZA/_index/_inbox/TEAM.json'
 required={*pins,inbox};allowed=required|{bp};changed=set(git('diff-tree','--no-commit-id','--name-only','-r',c).splitlines())
 # A correction reuses already identical parent blobs. Require every reviewed
 # difference to be committed, still verify ALL pinned current blobs below.
 # This is not initial publication's all-files-new assumption.
 must_change={inbox}
 for p,h in pins.items():
  before=subprocess.run(['git','rev-parse',c+'^:'+p],capture_output=True,text=True)
  if before.returncode!=0 or before.stdout.strip()!=h:must_change.add(p)
 assert must_change<=changed<=allowed,(must_change-changed,changed-allowed)
 for p,h in pins.items():assert git('rev-parse',c+':'+p)==h,p
 assert normalized(subprocess.check_output(['git','show',c+':'+inbox]).decode())==(w/'reviewed-inbox-body.txt').read_text()
 board=json.loads(subprocess.check_output(['git','show',c+':'+bp]));pub=next(t for t in board['tasks'] if t['id']==task)
 expected_epoch=json.loads((w/'reviewed-epoch.json').read_text())['epoch']
 assert pub['agent']=='ASTRA' and pub['status']=='ACTIVE' and board['recovery_epoch']==expected_epoch
 assert '@publication' in {r['key'] for r in pub.get('claimed_resources') or pub['resources']}
 # Supported ownership can sit in the bounded carrier while its separate
 # publication task reserves only @publication. Verify actual whole-file
 # ownership in the committed board; do not demand a duplicate claim.
 inbox_holders=[t['id'] for t in board['tasks'] if t['agent']=='ASTRA' and t['status']=='ACTIVE'
  and any(r['key']=='file:database/ffxii tza/_index/_inbox/astra.md' and 'start' not in r and 'end' not in r
    for r in t.get('claimed_resources') or t['resources'])]
 assert inbox_holders,'committed board lacks explicit active ASTRA inbox ownership'
 unchanged=bp not in changed
 if unchanged:assert git('rev-parse',c+':'+bp)==git('rev-parse',c+'^:'+bp)
 manifest=json.loads(subprocess.check_output(['git','show',c+':'+pkg+'/manifest.json']))
 for m in manifest['members']:
  raw=subprocess.check_output(['git','show',c+':'+pkg+'/'+m['path']]);assert len(raw)==m['bytes'] and hashlib.sha256(raw).hexdigest()==m['sha256']
 return {'commit':c,'head_at_verification':git('rev-parse','HEAD'),'exact_owned_blobs_and_body':True,
  'manifest_members_verified':len(manifest['members']),'board_revision':board['revision'],'inbox_ownership_tasks':inbox_holders,
  'board_unchanged_from_parent':unchanged,'source':'logged committed identity plus exact message/owned paths/blob/body/manifest checks; optional unchanged TEAM requires same supported parent with own ACTIVE publication'}
if __name__=='__main__':
 # The older c3e test directory has no reviewed-epoch.json; it is not a
 # complete fixture for this epoch-aware verifier. Never invent its pin.
 # Use the actual complete19 receipt to exercise separated claim ownership.
 w=Path('Database/Tools/work/ASTRA/matrix-buffer-alias/publication')
 receipt=verify(w,'ASTRA-PUBLISH-MATRIX-BUFFER-ALIAS','Database/FFXII TZA/_experiments/evidence/matrix-buffer-alias')
 assert receipt['commit']=='58bd6303f9d55d5c84e677d3f6f4b8d99b66b60e'
 Path(__file__).with_name('actual-separated-ownership-regression.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print('Verified actual19 commit with explicit committed ownership/epoch/body/pins; no Git write.')
