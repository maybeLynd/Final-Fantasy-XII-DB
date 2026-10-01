import json,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
SID='ASTRA-sol-20260928-access-default'
ID='ASTRA-ACCESS-PRODUCER-DEFAULT'
assert team.board_status(team.BOARD)[0]
b=json.loads(team.BOARD.read_text())
if not any(t['id']==ID for t in b['tasks']):
 t=dict(id=ID,kind='research',priority='P1',target='Remove raw-access default from ASTRA matrix capture',scope='Private matrix capture default, bounded invocation controls and additive exact affected-path inventory; published inputs immutable; no canonical index edits',completion='Actual default capture invokes pinned shared reviewed adapter; store/LEA and RMW profile controls plus bypass detector pass; original records retained, exact affected consumers routed, explicit reviewed publication and independent review pending',dependencies=[],resources=[dict(key='Database/Tools/work/ASTRA/matrix-buffer-alias/capture.py'),dict(key='Database/Tools/work/ASTRA/access-producer-default'),dict(key='Database/FFXII TZA/_experiments/evidence/access-producer-default')])
 b=team.transaction(team.BOARD,'ASTRA',dict(action='add',task=t),SID)
t=next(t for t in b['tasks'] if t['id']==ID)
if t['status']=='READY':
 b=team.transaction(team.BOARD,'ASTRA',dict(action='claim',task=ID,note='Method A: original capture paths and decoded metadata suffice. Repair actual private invocation, retain original19/22 publications, run disposable actual-producer store/LEA/bypass controls; RMW explicitly scoped. No live setup, canonical consumer edits or index regression claim.'),SID)
print('CLAIMED',ID,b['revision'])
