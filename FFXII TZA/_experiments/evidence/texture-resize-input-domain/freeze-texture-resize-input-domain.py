"""Freeze selected input-domain proof; no duplicate runtime/caller census."""
import hashlib,importlib.util,json,pathlib,shutil
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-resize-input-domain-frozen-ready'
if out.exists():raise ValueError('immutable input-domain packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'texture-resize-input-domain-result-01.json').read_text());c=json.loads((W/'texture-resize-input-domain-controls-01/result.json').read_text())
if not r.get('producer_complete') or r['checker_sha256']!=sha(W/'prove-texture-resize-input-domain.py') or c['status']!='PASS_ACTUAL_SELECTED_COUNT_REFUSALS_INDEPENDENT_PENDING' or len(c['refusals'])!=3 or any(q['exit']==0 or not q['result_absent'] or not q['expected_error_seen'] for q in c['refusals']):raise ValueError('required proof/control failed')
s=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
for q in r['source_pins']:
 if sha(W/q['path'])!=q['sha256']:raise ValueError('source preimage moved')
 S.validate(json.loads((W/q['path']).read_text()))
paths=[q['path'] for q in r['source_pins']]+['capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','inspect-texture-resize-input-callers.py','capture-texture-resize-input-tail.py','prove-texture-resize-input-domain.py','control-texture-resize-input-domain.py','freeze-texture-resize-input-domain.py','texture-resize-input-domain-result-01.json','texture-resize-input-root-closure-incomplete-01.json','texture-resize-input-root-cfg-qualified-02.json','texture-resize-count-domain-method-01.json','texture-resize-domain-caller-preparation-05.json','prepare-texture-counter-references.py']
paths += [p.relative_to(W).as_posix() for p in sorted((W/'texture-resize-input-domain-controls-01').rglob('*')) if p.is_file()]
paths += [p.relative_to(W).as_posix() for pattern in ('texture-resize-input-domain-positive-01.*','texture-resize-input-domain-controls-invocation-01.*','texture-resize-input-callers-feasibility-01.*','texture-resize-input-tail-capture-01.*','texture-resize-domain-caller-preparation-invocation-05.*') for p in sorted(W.glob(pattern))]
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in dict.fromkeys(paths):
 p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,p)
(out/'README.md').write_text("""# Selected texture resize input counts: raw zero excluded, masked-zero residue

Method A STATIC_ONLY; producer checked, independent acceptance and canonical
incorporation pending. Six prepared raw references were validated as original
CALL628100 instructions. Three complete normal roots and one six-fragment root
are byte-qualified and their normal CFGs rederived. The counted201/142/185/276
instructions are source coverage, not tests or game observations.

For these selected normal paths,17E8E0 and17F3B0 supplymax(1,u32 incomingR9D),
1946E0 supplies1, and the three1B7850-root sites supply4. Definition domination,
nonvolatile register preservation/explicit writes and private stack-slot stores
are checked on paths reaching each call. Ordinary ABI, valid object/private
stack and no interference/escaped local alias are premises. Opaque callees do
not become certified memory-safe merely because those premises are stated.

RawnewN0 is excluded through these six sites. The prior higher/helper conditional
rawzero/null-read witness stays mathematically valid, but do not spend runtime
trying to witness it through these bounded normal paths. The stronger universal
maskedcount-positive claim is REFUTED for arbitrary dynamic inputs: the two
unsigned floors pass80000000 unchanged; AND7FFFFFFF yields0. Algebraically the
mask's preimage of0 is{0,80000000}; flooring excludes only0. Fixed1/4 excludes
both. No exhaustive2^32 execution, fixture/native run, natural highbit occurrence,
allocation success or game crash is claimed. Ordinary incomingR9D bounds are
still needed for the two dynamic producers. All other direct/indirect/RVA/virtual
callers and actual initialization/lifetime remain outside selected coverage.

Default reproduction, existing analysis Python, fresh output:

    python <packet>/prove-texture-resize-input-domain.py <fresh.json>

Three actual CLI controls reuse one positive: byte/annotation-consistent CMOVBE
in place of the unsigned floor, missing normal tail, missing tail metadata.
The changed predicate successfully redecodes through the actual shared reviewed
role adapter, then the full original body gate refuses it. Every negative has
nonzero exit, expected error and no final result. Producer controls, independent
review and semantic incorporation remain separate. No external audits count
as our tests.

Learning: the first whole-root check refused at1B7C93. The caller-containing
fragment end was not whole root end; that incomplete result is retained asNOTPASS.
Only missing75-byte tail was added. Existing241-byte prefix and850-byte child
were reused, never recaptured. The prefix was produced by an inline tool command
through the pinned capture-index-path.py; no retrospective wrapper-file execution
identity is invented. Its raw spans/tool pins remain independently inspectable;
actual source/annotation/body identity and all normal edges are checked now.
Six original pdata fragments/parentage, complete bytes and normal branches
resolve the earlier scope gap. Exception/async entry effects are not certified.

Shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000, Capstone5.0.7/shared adapter receipts are retained. Referenceprep05
is a controlled candidate locator only, not complete caller closure; zero raw
hits never proves absence. Earlier selected higher caller70 and lower capacity41/
helper33 have separate evidence/reviews; reuse their eventual acceptance without
rerunning their censuses. This packet proves count arguments under the stated
mask, not full downstream allocation/ownership safety.

OPUS owns count ABI/domain contracts; FABLE owns the narrowed natural-input
question. Next A discriminator: original R9D producers feeding17E8E0/17F3B0,
with request/resource bounds, before any automated real-process observation.
Do not promote max(1,N) to an encoded-count sanitizer or request human gameplay.
No FF12/native/emulated/PC/input/instrument/save/config/reference or peer-process
writes. Known own helpers exited. K14 closed/accepted, menu spent/unapproved,
EXP127 invalid. No wholeOV or fullL1+L2/M0-M5 completion; goal ACTIVE/NOT_MET.
""",encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VERIFIED_INDEPENDENT_PENDING',members=members),indent=2)+'\n');print('Frozen input domain',len(members),sha(out/'manifest.json'))
