"""Freeze conditional primary admission with verified committed upstream evidence."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'bts-primary-admission-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'bts-primary-admission-result-02.json').read_text());c=json.loads((W/'bts-primary-admission-controls-01/result.json').read_text())
for tag,d,key in [('bts-primary-admission-capture-01','capture-bts-primary-admission.py','driver_sha256'),('bts-primary-admission-positive-02','prove-bts-primary-admission.py','checker_sha256'),('bts-primary-admission-controls-run-01','control-bts-primary-admission.py','driver_sha256')]:
 st=json.loads((W/(tag+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get(key)!=sha(W/d) or not(W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-bts-primary-admission.py'):raise ValueError('positive failed/stale')
if c.get('status')!='PASS_ACTUAL_PRIMARY_ADMISSION_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=3 or c.get('checker_sha256')!=r['checker_sha256'] or c['positive_reused']['sha256']!=sha(W/'bts-primary-admission-result-02.json'):raise ValueError('controls incomplete/stale')
if any(x.get('exit')==0 or not x.get('expected_error_seen') or not x.get('result_absent') for x in c['refusals']):raise ValueError('concrete refusal failed')
pins=r['source_pins']+r['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('required input changed')
up=ROOT/'Database/FFXII TZA/_experiments/evidence/bts-index-binding';manifest=up/'manifest.json'
if sha(manifest)!=r['upstream_index_result']['manifest_sha256'] or sha(up/'bts-index-binding-result-03.json')!=r['upstream_index_result']['sha256']:raise ValueError('committed upstream changed')
members=json.loads(manifest.read_text())['members']
if len(members)!=152 or any(sha(up/x['path'])!=x['sha256'] for x in members):raise ValueError('upstream member changed')
paths={x['path'] for x in pins}|{'bts-primary-admission-method-01.json','bts-primary-admission-result-01.json','bts-primary-admission-result-02.json','prove-bts-primary-admission.py','prove-bts-primary-admission-before-canonical-dependency-01.py','control-bts-primary-admission.py','freeze-bts-primary-admission.py'}
paths|={tag+s for tag in ['bts-primary-admission-positive-01','bts-primary-admission-positive-02','bts-primary-admission-controls-run-01'] for s in ['.stdout','.stderr','.status.json']}
paths|={p.relative_to(W).as_posix() for p in (W/'bts-primary-admission-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/bts-primary-admission/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md'];units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('native path budget exceeded')
if any(not(W/p).is_file() for p in paths):raise ValueError('required file missing')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
 p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Missing indexed primary payload is not a successful load

Method A original391-byte330310 normal body and exact retained size/caller bytes.
Producer valid, independent acceptance and canonical incorporation pending.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No native/emulated/live run or duplicated corpus census.

Dependency: bts-index-binding, commitfdc46b6eba1cf92e283290d1737fd55f945157d0,
manifestc57c6b668c5b567014a01c5da45dcbf7899645e4547a6bc310edce0972891abb.
The actual reducer/freezer verify all152 members and the result/input/exit pins;
the earlier evidence is reused rather than recopied or counted as more tests.
Dependency publication is not independent semantic acceptance.

All31 authored test-zone field IDs differ from212. Thus the normal manager0
namespace5/base3*field call does not use330310's special cached-buffer selector
212 exception. With no kind5 runtime size override, unchanged shipping FSTs
return-1 at each primary index. Original32E400 preserves this nonpositive
fallback.330310's signed TEST/JLE skips its primary allocator36A100, pointer
publication, cached memcpy/callback and primary read request32E620.

However,330310 ORs manager flags20000 BEFORE that size gate. This local write
does not prove allocation, accepted read, executed callback or a usable payload.
Its nonpositive suffix can still call5C5230 and staged sibling32EB40(base+2)
for manager0. The suffix does not overwrite the primary payload pointer. Prior
owner state, cleanup, future/pending callbacks and sibling terminal effects are
separate. The conclusion is no new primary admission under these premises,
not no other requests/effects or universal absence of a stale payload.

The alternate3306E0 route is not certified. Canonical32E3F0 is already an8-byte
diagnostic-return stub; it is not proof a filename buffer was filled or that
the alternate path is naturally chosen. Do not recapture that known stub or
turn its label into an initialization/OS-read guarantee.

Reproduce against the existing committed dependency with fresh output:

    python <packet>/prove-bts-primary-admission.py <fresh.json>

The capture verifies five exact normal pdata fragments/parent chains. Actual
shared access-role controls and byte redecoding are retained. The local normal
CFG and the nonpositive suffix are checked; opaque callees retain normal ABI
and valid-state premises. Three actual CLI refusals reuse the positive: failed
capture, coherently changed JLE guard, missing canonical upstream. Incomplete
upstream evidence cannot become PASS. Earlier working-input result01/driver
are history; result02 adds committed all-member dependency and exact FST index
arithmetic. No result from a failed method is used as semantic evidence.

FABLE/OPUS consume this additive GR18 primary admission/attempt-flag distinction.
Independent SPEC review is required. Full GR18/OV/AQ closure, current overrides,
alternate-loader selection, aliases/embedded scripts and natural lifetime remain
open. Next inspect existing option5/size-override initialization/writer evidence
before considering real-process observation. No menu retry is authorized.

Player version: for these test-area IDs, the normal loader can mark that it
tried to load a script even though the missing file size prevents a primary
load. We are separating that flag from evidence that a script actually ran.

Cleanup: finite source/data reads and disposable controls; no PC/game/input/
instrument/save/config/reference or peer-process change. Full L1+L2 goal remains
ACTIVE/NOT_MET; pending reviews affect these claims only.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native units',units,'manifest',sha(out/'manifest.json'))
