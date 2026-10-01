"""Freeze selected upstream normal argument proof; earlier packets immutable."""
import hashlib,importlib.util,json,pathlib,shutil
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-resize-upstream-safe-counts-frozen-ready'
if out.exists():raise ValueError('immutable upstream packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'texture-resize-upstream-safe-counts-result-01.json').read_text());c=json.loads((W/'texture-resize-upstream-safe-controls-01/result.json').read_text())
if r.get('producer_complete') is not True or r['checker_sha256']!=sha(W/'prove-texture-resize-upstream-safe-counts.py') or c['status']!='PASS_ACTUAL_UPSTREAM_COUNT_REFUSALS_INDEPENDENT_PENDING' or c['checker_sha256']!=r['checker_sha256'] or len(c['refusals'])!=4 or any(q['exit']==0 or not q['result_absent'] or not q['expected_error_seen'] for q in c['refusals']):raise ValueError('required upstream proof/control failed')
s=importlib.util.spec_from_file_location('freeze_annotation',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
paths=[]
for q in r['source_pins']:
 if sha(W/q['path'])!=q['sha256']:raise ValueError('upstream source moved')
 S.validate(json.loads((W/q['path']).read_text()));paths.append(q['path'])
for q in r['required_result_pins']:
 if sha(W/q['path'])!=q['sha256'] or sha(W/q['checker_path'])!=q['checker_sha256']:raise ValueError('lower prerequisite moved')
 paths += [q['path'],q['checker_path']]
 for p in q['source_pins']:
  if sha(W/p['path'])!=p['sha256']:raise ValueError('lower source moved')
  S.validate(json.loads((W/p['path']).read_text()));paths.append(p['path'])
for q in r['required_invocation_receipts']:
 if sha(W/q['path'])!=q['sha256'] or json.loads((W/q['path']).read_text()).get('exit')!=0:raise ValueError('lower invocation failed or moved')
 paths.append(q['path'])
paths += ['capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','inspect-texture-resize-dynamic-producers.py','inspect-texture-resize-forwarded-input-caller.py','capture-texture-resize-palette-root-edges.py','prove-texture-resize-upstream-safe-counts.py','control-texture-resize-upstream-safe-counts.py','freeze-texture-resize-upstream-safe-counts.py','texture-resize-upstream-method-01.json','texture-resize-upstream-safe-counts-result-01.json','texture-resize-dynamic-producer-preparation-06.json','texture-resize-forwarded-input-preparation-07.json','prepare-texture-counter-references.py']
paths += [p.relative_to(W).as_posix() for p in sorted((W/'texture-resize-upstream-safe-controls-01').rglob('*')) if p.is_file()]
paths += [p.relative_to(W).as_posix() for pattern in ('texture-resize-upstream-safe-positive-01.*','texture-resize-upstream-safe-controls-invocation-01.*','texture-resize-palette-root-edges-capture-01.*','texture-resize-dynamic-producers-capture-01.*','texture-resize-forwarded-input-caller-capture-01.*') for p in sorted(W.glob(pattern))]
for name in paths:
 if not (W/name).is_file():raise ValueError('missing packet member '+name)
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in dict.fromkeys(paths):
 p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,p)
(out/'README.md').write_text("""# Selected upstream texture counts exclude raw and masked zero

Method A STATIC_ONLY. Producer checked; independent acceptance and canonical
incorporation pending. No FF12/native/harness/emulated execution. The exact
shipping EXE SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000 and Capstone/shared reviewed role adapter are retained in the sources.

Seven selected original callers of17E8E0/17F3B0 and the selected caller of the
183780 forwarding leaf constrain incoming counts to1,4 or32. Complete normal
CFGs, definition domination, actual register-write checks and no intervening
volatile call/clobber establish this property under ordinary normal-entry ABI,
valid private stack/object and no-interference premises. Two palette roots
stage1 viaR8D->R9D. Four other selected wrappers stage1/4. The leaf183780 does
not changeR9 before calling17E8E0; selected1BABB2 setsECX0 then LEA R9D[RCX+20]
and passes32. Earlier1BAB52's resource+F8 load is overwritten. Palette pixel
counts16/256 are EDX arguments and must not be mistaken for element countR9D.

The already-produced lower six-site receipt is required with exact result,
checker, original source and actual successful invocation status. This packet
requalifies its sources; it does not rerun or claim independent acceptance of
that census. Those two unsigned max(1,u32) floors leave1/4/32 unchanged; masking
with7FFFFFFF remains nonzero. The artificial arbitrary80000000 counterexample
remains valid outside these selected paths. There is no universal<=32 count,
complete direct/indirect/virtual/registry caller closure, naturally initialized
resource, allocator success, exception handling, lifetime or scheduling proof.
Do not repeat gameplay samples of these constants. Investigate another caller/
binding or a violated premise only for a named broader unresolved proposition.

Eight complete normal roots cover110/110/7/6/7/152/8/373 instructions. These
are source coverage counts, not executions or experiments. Both palette roots
share an unwind address but have distinct parent triples. Original543B children
are reused; only234B missing edges were captured. Reference preparations06/07
are controlled candidate locators, not universal negative-call evidence.

Default reproduction with the existing analysis Python and a fresh result:

    python <packet>/prove-texture-resize-upstream-safe-counts.py <fresh.json>

Four actual CLI refusals reuse the one positive: a byte/annotation-consistent
LEA changing32 to33, missing palette edge, failed lower result and failed lower
invocation exit. Each has nonzero exit, expected reason and no final result.
The changed LEA redecodes through the reviewed adapter before the original body
gate refuses it. Producer controls, external review and canonical consumption
are distinct; no external review executions count as ASTRA tests.

OPUS owns count-domain/ABI contract incorporation; FABLE owns the narrowed
natural zero-count/lifetime question. Independent review must preserve selected
coverage and the lower pending dependency. No wholeOV row newly closed, prior
obsolete runtime request retired1 cumulative. No wholeL1+L2/M0-M5 completion.
Goal ACTIVE/NOT_MET. K14 closed/accepted, menu budget spent/unapproved,
EXP127 invalid. All foreground helpers exit; no PC/game/input/instrument/save/
config/reference/peer-process writes or termination. Existing originals and
published packages are unchanged; this is an additive downstream proof.
""",encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VERIFIED_INDEPENDENT_PENDING',members=members),indent=2)+'\n');print('Frozen upstream count proof',len(members),sha(out/'manifest.json'))
