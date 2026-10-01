"""Additive producer repair; old accepted inputs/results remain byte-immutable."""
import hashlib,importlib.util,json,pathlib,shutil
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'title-tracker-qualification-frozen-ready'
if out.exists():raise ValueError('immutable qualification packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'title-tracker-callback-boundary-result-02.json').read_text());c=json.loads((W/'title-tracker-qualification-controls-02/result.json').read_text())
if r.get('producer_complete') is not True or r['checker_sha256']!=sha(W/'prove-title-tracker-callback-boundary-02.py') or r['prerequisite_execution']['exit']!=0 or c['status']!='PASS_ACTUAL_TITLE_TRACKER_QUALIFICATION_REFUSALS_INDEPENDENT_PENDING' or len(c['refusals'])!=5 or any(q['exit']==0 or not all(q[k] for k in ('result_absent','retained_output_absent','expected_error_seen')) for q in c['refusals']):raise ValueError('required qualification/control failed')
spec=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
for p in r['source_pins']:
    if sha(W/p['path'])!=p['sha256']:raise ValueError('source preimage changed')
    S.validate(json.loads((W/p['path']).read_text()))
old=ROOT/'Database/FFXII TZA/_experiments/evidence/title-tracker-callback-boundary'
for name in ('prove-title-tracker-callback-boundary.py','title-tracker-callback-boundary-result-01.json','title-tracker-cleanup-source-01.json','title-cleanup-callback-queue-source-01.json'):
    if sha(W/name)!=sha(old/name):raise ValueError('historical accepted member changed '+name)
paths=['prove-title-tracker-callback-boundary.py','prove-title-tracker-callback-boundary-02.py','prove-title-tracker-callback-boundary-02-before-metadata-fix.py','prove-title-queue-consumption.py','validate-title-source-annotations.py','control-title-tracker-callback-boundary-02.py','freeze-title-tracker-qualification.py','title-tracker-cleanup-source-01.json','title-cleanup-callback-queue-source-01.json','title-tracker-callback-boundary-result-01.json','title-tracker-callback-boundary-result-02.json','title-tracker-callback-boundary-result-02-retained-producer.json','title-tracker-qualification-initial-metadata-refusal.json']
paths += [p.relative_to(W).as_posix() for p in sorted((W/'title-tracker-qualification-controls-02').rglob('*')) if p.is_file()]
paths += [p.relative_to(W).as_posix() for pattern in ('title-tracker-qualification-positive-02.*','title-tracker-qualification-controls-invocation-02.*') for p in sorted(W.glob(pattern))]
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in paths:
    p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,p)
review=ROOT/'Database/FFXII TZA/_index/candidates/auditspec-review-astra-title-tracker-callback-0930/REVIEW.md'
(out/'review-provenance.json').write_text(json.dumps(dict(commit='2e88eceef18adbf17d31f8bd1fc61ae1f8e96b80',review=review.relative_to(ROOT).as_posix(),review_sha256=sha(review),verdict='Original shipping science independently ACCEPTED; old producer accepts unwitnessed rehashed fast CALL',reviewer_assertions='100 external assertions, NOT our tests',old_packet_commit='7d81d759e4b8d90ab5af058d4b360b78c1f572b1'),indent=2)+'\n')
(out/'README.md').write_text('''# Title tracker: qualify the actual producer after returned review

Method A, STATIC_ONLY. This is a producer correction, not another semantic
experiment. The original packet7d81d759e4b8 and independent review2e88eceef18a
remain authoritative at their bounded scopes. Original inputs, driver and
result are retained unchanged. The review's100 assertions are external work.

Defect: the old checker witnessed selected operations but trusted the retained
normal_cfg and self-rehashed ranges. Changing185AD2 ADD RSP,38;RET (five bytes)
into CALL1858A0 with consistent annotations/span hash passed its gate. Thus its
absence/complete-CFG producer qualification was incomplete. Independent review
of the actual shipping image still supports the original findings. No known
false original semantic capture or canonical index regression follows.

DEFAULT REPRODUCTION (existing analysis Python, fresh output):

    python <packet>/prove-title-tracker-callback-boundary-02.py <fresh.json>

The02 invocation requires the reviewed shared access adapter through the actual
byte/annotation validator, all seven full shipping-body hashes, exact fragment
metadata and decoded unwind chains. It derives the complete normal CFG, compares
the recorded tracker metadata with that derivation, derives both fast returns
and checks no CALL occurs on the write<end branch. Calls remain opaque and the
17ECC0 external tail is explicitly bounded. It then executes the unchanged old
producer with checked exit/result/source pins. No downstream PASS can suppress
that upstream failure. The intermediate original result and invocation receipt
are preserved. Syntactic source completeness is not natural reachability.

Five actual02 CLI controls reuse one completed positive: reviewer's consistent
fast CALL (also successfully redecoded before invoking the checker), forged CFG,
old false store role, failed wrapper and missing source. Every refusal has a
nonzero exit, expected error and no final/intermediate result. They are producer
controls, not FF12/native/emulated experiments or independent acceptance. The
initial02 hand-entered metadata typo was refused before any semantic output; its
driver preimage/refusal is retained, corrected against original metadata. It was
never a passing result. No published source was recaptured or changed.

Scope retained:189120 reads shared global01F7F598 and ignoresRCX;183720 conditionally
queues17ECC0/original argument through185A90. The fast branch stores its advanced
cursor before the16-byte pair and makes no call. Tracker local pointer clears do
not establish native release/cancellation. The vcall18 remains allocator-like
inference with unresolved target. The1FB660 body does not itself unlink+18 nodes;
16D6D0/1AF2B0 effects remain outside this packet. Original/related later queue,
pump/import/cleanup results have separate reviews and consumers.

FABLE's existing ASTRA-RETURN-FABLE-TITLE-TRACKER-CALLBACK-0930 route owns canonical
semantic adoption; do not resubmit its completed census or edit claimed pages.
Use fresh canonical preimages. This new repair needs independent code/control
review, then future producer consumers should invoke02 and retain its checked
receipt. Current canonical semantic wording is a consumer task, not a reason
to alter immutable original evidence. Producer validity, independent semantic
acceptance and canonical consumption stay distinct.

Exact EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000, Capstone5.0.7/shared adapter pins appear in raw and qualified records.
No initialized global/object/index proof, scheduler/frame/thread assertion,
full cancellation/free/lifetime, arbitrary malformed-state or atomicity claim.
No whole OV or goal closure. K14 closed/accepted; parked menu spent/unapproved;
EXP127 INVALID_POST_TRACE unchanged. No game/PC/input/instrument/save/config/
reference writes; bounded child scripts exited, no peer-process termination.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VERIFIED_INDEPENDENT_PENDING',members=members),indent=2)+'\n')
print('Frozen qualification',len(members),sha(out/'manifest.json'))
