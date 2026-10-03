"""Use the documented CLI for this NEW immutable request only.

Two outside-the-lock revision reads raced unrelated peer writes. An additive
request has no mutable target preimage: team.py loads the CURRENT board under
its journal-checked lock and refuses a duplicate ID. No existing task/claim is
changed here, no board copy restored, and no guard implementation is bypassed.
Ownership-mutating audit operations remain parked for FRONTIER, not retried.
"""
import hashlib,json,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent
ROOT=next(p for p in H.parents if(p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T=ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
output=H/'write-denial-additive-current-receipt-01.json'
opfile=H/'write-denial-additive-current-op-01.json'
if output.exists() or opfile.exists():raise ValueError('once-only route; reconcile existing result')
op=json.loads((H/'write-denial-op-02.json').read_text())['operation']
if op['action']!='add' or op['task']['id']!='ASTRA-REQ-FRONTIER-ATOMIC-BOARD-WRITE-DENIAL-1003':raise ValueError('new additive request only')
opfile.write_text(json.dumps(op,indent=2))
cmd=[sys.executable,'-B',str(T),'apply','--agent','ASTRA','--session','SOL-ASTRA-write-denial-additive-1003','--file',str(opfile)]
r=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
receipt=dict(argv=cmd,exit=r.returncode,stdout=r.stdout,stderr=r.stderr,operation_sha256=hashlib.sha256(opfile.read_bytes()).hexdigest(),driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),limits='New additive unique-ID request through documented current-board CLI; not a retry of ownership-mutating audit, not an existing-row preimage waiver.')
if r.returncode==0 and re.search(r'Saved revision \d+',r.stdout):
    b=json.loads((ROOT/'Database/FFXII TZA/_index/_inbox/TEAM.json').read_text(encoding='utf-8'))
    matches=[t for t in b['tasks'] if t['id']==op['task']['id']]
    if len(matches)==1 and matches[0]['question']==op['task']['question'] and matches[0]['requester']=='ASTRA':receipt['status']='ROUTED_ONCE_VERIFIED_CURRENT'
    else:receipt['status']='CURRENT_RESULT_MISSING_OR_DIFFERENT'
else:receipt['status']='ROUTE_FAILED_NO_RETRY'
output.write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))
if receipt['status']!='ROUTED_ONCE_VERIFIED_CURRENT':raise SystemExit(1)
