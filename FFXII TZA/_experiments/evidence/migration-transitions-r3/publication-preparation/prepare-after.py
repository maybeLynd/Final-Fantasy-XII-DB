import json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/migration-transitions-r3');p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'delta-baseline-selection/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
ID='ASTRA-PUBLISH-TRANSITIONS-R3';SID='ASTRA-sol-20260929-transitions-r3'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-delta-baseline-selection',SID).replace('ASTRA-PUBLISH-DELTA-BASELINE-SELECTION',ID).replace('evidence/delta-baseline-selection','evidence/migration-transitions-r3');(p/'publish.py').write_text(s)
paths=[f.as_posix() for f in sorted(P.rglob('*')) if f.is_file()];q=subprocess.run(['git','hash-object','--stdin-paths'],input='\n'.join(paths)+'\n',capture_output=True,text=True);assert q.returncode==0 and not q.stderr and len(q.stdout.splitlines())==len(paths)
pins=dict(zip(paths,q.stdout.splitlines()));assert len(pins)==len(json.loads((P/'manifest.json').read_text())['members'])+1 and len(pins)>1;(p/'reviewed.json').write_text(json.dumps(pins,indent=2)+'\n')
cmd=[sys.executable,'-B',str(W.parent/'migration-generation-independent/prepare-publication.py'),'--preflight-only','--preflight-pins',str(p/'reviewed.json')];q=subprocess.run(cmd,capture_output=True,text=True,timeout=15);(p/'path-preflight-before-assertion.json').write_text(json.dumps(dict(args=cmd,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True),indent=2)+'\n');assert q.returncode==0 and q.stdout.strip()=='PUBLICATION_PATH_ADMISSIBILITY_ONLY_NO_WRITES' and not q.stderr
(p/'path-preflight.json').write_text(json.dumps(dict(args=cmd,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True),indent=2)+'\n');(p/'message.txt').write_text('ASTRA: accept repaired exact fields and caller status at scoped source boundary\n')
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
sys.path.insert(0,str(p));from verify import normalized
ok,d=team.board_status(team.BOARD);assert ok,d;b=json.loads(team.BOARD.read_text());c=(old/'commit.txt').read_text().strip();assert json.loads((old/'verification.json').read_text())['commit']==c
header='''## SOL in ASTRA — ACTIVE; returned transition repairs supported at bounded scope

The full L1+L2 goal remains ACTIVE until actual governing requirements, independent
reviews and terminal sequence are satisfied. No ordinary checkpoint, package, green
validator, all-MET table or empty queue stops/completes it. Honor genuine user stops/
takeover and real host/usage limits. Deployed M0–M5 and full L1L2 remain NOT_MET; L3 later,
no reconstruction phase. Use fresh supported boardcheck/CURRENT and actual publications
on every resume; historical headers/export headlines are not current ownership proof.

OPUS-REQ-ASTRA-VERIFY-TRANSITIONS-R3: exact original d27e9aff8 repaired source passes
independent original117f85 regressions and f112/821c discriminators. Full40 forwarded
unchanged; commitLF/CRLF MALFORMED/no op, verdictLF VERDICT-MISSING/no op. Thirteen exact
oldinputs retain original results. Actual original apply caller with labelled child-entry
substitution: zero wholeSavedline -> created/parent0; nonzero Savedline/error-only and
zero no-valid-marker -> FAILED/parent1. Nonzero taskalreadyexists requires exact derived
id on reread privateboard: absent or unrelated added id fails; derived-id present exists/
parent0. Original parent unchanged, original imported team definitions retained; child
guard exits before real writer body. Private added-id uses original pure team.apply then
serializes disposable fixture, an explicit intervention, not journal/race evidence.
Actual argv/op/child+parent status/result/exception, temp-op removal and before/after
fixture/source identities retained; all synchronous children terminal. Read-only checker
and focused missing-field/hidden-writer-exit receipts refuse. Own original74 immutable members plus additive cache/preparation correction
migration-transitions-r3. Exactnext verify publication/allmemberSHA/blobs/body/epoch/
release; finish scoped source review, OPUS consumption and own SPEC evidence review once.
Then refresh checked queue for returned repairs/independent research; do not idle waiting
for acceptance or repeat these settled controls unchanged.

No full supported writer campaign, real races/idempotence/fault/failed-prefix recovery,
apply-budget/controller/deployment or old timed-out descendant cleanup acceptance. A
substituted child cannot prove omitted writer effects. Old counterexamples remain valid
at their original source scope; required own nonauthor evidence review is separate from
ASTRA independent review of OPUS producer code. Canonical incorporation is still required.

Baseline BASELINE_COMMIT committed/verified/released: original prior_generation/newer
verified missingprogress vs prior_progress/olderwithprogress disagree. Alignedlatest and
emptyhistory controls supported. OriginalStore/actualverification checked, synthetic
40/100 composition only, not full_build/currentnormal/deployed/browser proof. TwoINVALID
guessed-verifier-text preparations retained; exactdefault receipt-before-assertion fixed,
emptyobservation and existingalignedgeneration reused. Original73sciencebytes unchanged,
additive normalized-source identity qualification: rawdriver bytes separatelybound;
metadata/write-once producer-after change NOT_EXECUTED. Final78members; OPUS cause/rule
adjudication and SPEC review routed once, day-boundary versus immediate-prior wording
preserved. This is a narrow input-boundary contradiction, not general reporter repair.

Activity8380c611 scoped repairedattribution ACCEPT exact0bec on original00fd inputs;
OPUS consumer and SPEC ownreview queued once. Foreignrecipient not credited, trueOPUSnote
recent/working, oldclaim/busy/free controls correct. No actualhost/deployedmodule/delta/
renderedtimer/reload/browser award. Writer821c25f8 and linef112e86b findings drove OPUS
d27 source repair; currentR3 is exact re-review, not erased history/wholeM2 acceptance.
Serverc466fc47 selected-view HTTP/producer correction delivered; Poisondf93a1eb Q6 scoped
ACCEPT delivered; MyProgresse66925f2 and archive70a134f6 scopedACCEPT, requiredownreviews
and named consumers pending as board records. Synthetic terminal30 is not30 actual audits.
Fixture7393cec notice/review and A03/cacheced001204 preserved. Reconcile exact tasks before
any reroute; a sent review/frozen package/producer checks are not independent acceptance.

PC/browser/game controls OFF; no production server restart or save/config/reference
changes. No own persistent test server/instrument/child remains after completed captures.
Live authorization is active but the parked menu TWO attempts/TEN minutes remains spent;
extra6min350ms extension UNAPPROVED persists across sessions/tasks/epochs. No retry or
unchanged permission ask. Live-only gaps remain explicit and block only affected claims.
Method A/B/C chosen by sufficiency, not counts/ratios. Input sent/registered/accepted/
executed/consequence remain distinct; no screenshot or memory sample proves the other.

Publication: use team.hold_set/overlap including original resources. Before-claim DEFER
or race is not a commit; preserve attempts and work independently, retry only after
checked release. Verify actual logged commits/exact paths/body/epoch/allmember hashes,
brief supported reservations. No lock reap, claim theft by age, reset/clean/old-op replay
or rival reporter/platform. Claims and generated CURRENT reflect the actual checked board.

---

'''.replace('BASELINE_COMMIT',c)
inbox=Path('Database/FFXII TZA/_index/_inbox/ASTRA.md');text=inbox.read_text();(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text);(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
assert not any(t['id']==ID for t in b['tasks']);b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':ID,'kind':'research','priority':'P1','target':'Publish independent returned transition repairs R3','scope':'Own original74 immutable members plus scoped cache/preparation correction and brief ASTRA header; supported TEAM only','completion':'Actual committed blobs/body/epoch/all finalmemberSHA verified, publication released; scoped consumer/own independent review routed separately','dependencies':[],'resources':[{'key':'@publication'}]}},SID)
print('PREPARED_TRANSITIONS_R3_PUBLICATION',len(pins),b['revision'],flush=True)
