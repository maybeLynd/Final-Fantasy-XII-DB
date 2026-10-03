"""Seal only the returned-review correction; never modify old published members."""
import hashlib,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
ROOT=next(p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
F=W/'uq147-reviewed-boundary-correction-frozen-ready';F.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for stem,driver in [('prove-reviewed-local-boundaries-01','prove-reviewed-local-boundaries.py'),('control-reviewed-boundaries-prerequisite-01','control-reviewed-boundaries-prerequisite.py')]:
    s=json.loads((P/(stem+'.status.json')).read_text())
    if not(s.get('terminal') is True and s.get('exit')==0 and s.get('exception') is None and s.get('driver_sha256')==sha(P/driver)):raise ValueError('successful current producer/control required')
r=json.loads((P/'result-reviewed-local-boundaries-01.json').read_text())
if r.get('producer_complete') is not True or len(r['controls'])!=5 or r['driver_sha256']!=sha(P/'prove-reviewed-local-boundaries.py'):raise ValueError('current nonempty result required')
names=['prove-reviewed-local-boundaries.py','control-reviewed-boundaries-prerequisite.py','freeze-reviewed-local-boundaries.py',
 'result-reviewed-local-boundaries-01.json','reviewed-boundaries-failed-prerequisite-01.json','reviewed-boundaries-prerequisite-control-01.json',
 'reviewed-boundaries-refusal-01.stdout','reviewed-boundaries-refusal-01.stderr',
 'source-request-tail-01.json','capture-request-tail.py','source-defeat-boundary-01.json','capture-defeat-boundary.py']
for stem in ['prove-reviewed-local-boundaries-01','control-reviewed-boundaries-prerequisite-01','capture-request-tail-01','capture-defeat-boundary-01']:
    names += [stem+x for x in ['.status.json','.stdout','.stderr']]
sources={name:P/name for name in names}
sources['validate-title-source-annotations.py']=W/'validate-title-source-annotations.py'
sources['retained/reduce-request-tail-boundary.py']=P/'reduce-request-tail-boundary.py'
sources['retained/prove-defeat-recompute-boundary.py']=P/'prove-defeat-recompute-boundary.py'
for slug in ['local-boundaries','mode-query','dismiss-stage']:
    sources['review/'+slug+'.md']=ROOT/('Database/FFXII TZA/_index/candidates/auditspec-review-astra-uq147-'+slug+'-1003/REVIEW.md')
for name,path in sources.items():
    target=F/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
(F/'README.md').write_text('''# UQ147 returned-review correction: caller writes remain

Player version: one notification step skips publishing updates, while the
caller can still set a unit flag and invoke a reset helper. Skipping that block
does not make the entire cleanup write-free. Natural summoner KO/Esper timing
and visible behavior remain open.

Question: what survives before the exact notification(1,0) tail, and does our
lookup checker actually reject a redirected required helper? Method A is
sufficient. Original retained169B request bodies and477B defeat/lookup source
are consumed, not recaptured or executed. Image73461d08…21f8/base120000;
complete sources, byte/role validator, current invocation receipts preserved.
The shared reviewed adapter remains used through the actual byte validator.

SPEC at bff21d191 accepted the original local-boundaries package WITH NARROWING.
The mode-query and Dismiss-order packages were independently ACCEPTED. These
three external reviews and their runs are reviewer corroboration, not new
ASTRA experiments. OPUS c6de67245 already incorporated the exact317E9A/33C9B0
narrowing in CONTRACT-auto-status-rebuild13bh-a. No duplicate OPUS work needed.
FABLE's existing consumption request remains its owner; route the supplement
there, not an edit to its claimed page.

The new actual producer checks all22 caller instructions, its own persistent
write census, the flag/NULL gates, unit pointer/write identity, flag32 constant,
and the exact lookup direct calls236850/236820/236850. The old tail reducer
examined only25AAD0's memory roles, omitting317E60's own conditional OR write.
The old defeat checker reported lookup transfers without checking their
targets. Old published drivers/results stay immutable; this producer is the
replacement for those two missing checks in further qualification.

Result: under valid readable state, normal Win64 ABI/returning helpers and no
interference, the(1,0) tail excludes25AAD0's five publication writes and2F1710.
Before it,317E60 tests byte02089340bit4, resolves a non-NULL unit and tests its
byte0bit3. The admitted arm ORs QWORD flag32 at317E9A and calls33C9B0(unit+80).
Neither effect is excluded. Opaque helper effects, mode preservation, actual
command reachability/acceptance/execution, ownership/lifetime and fullUQ147
remain open. This is a local conditional implementation fact, not gameplay.

Five labelled source-record controls reject missing/write-role, wrong-offset,
wrong-mask, extra-caller-store and redirected-lookup-helper defects. They are
synthetic detector controls, not coherent machine-code mutants. The actual
changed producer CLI also refuses a labelled failed prerequisite with exit1
and no result. Positive producer/control receipts terminal0, nonempty result;
no missing/incomplete/zero-case run credited. No unchanged settled native or
live experiment repeated. This correction's independent review remains
pending; original reviewed scope and new producer validity are separate.

Reproduce in the original recorded absolute argv layout, or copy this folder
to a scratch child of a directory containing the frozen byte validator and
the reviewed adapter path expected by that validator. The driver verifies
the original successful captures before semantic reduction; sources/members
must remain exact. No native execution, process/control/attach/save/config or
reference writes occurred. Own finite shells/children returned terminal.
Whole formerly-runtime rows newly closed here0; no full database completion.
''')
(F/'SETUP-LESSONS.md').write_text('''Read before reuse

Do not infer caller write-freedom from a callee branch exclusion. Census the
caller too, retain its conditional OR/reset gates, and check required helper
identities rather than merely printing their transfer list. Use current
prove-reviewed-local-boundaries.py for these exact two missing checks.
Published original sources/producers/results remain immutable.

Delivery lesson: a45s external subprocess timeout killed an actual supported
finish transaction, with no Saved receipt. Current boardcheck showed the op
had not landed. The fresh successful courier removed that parent timeout,
persisted stdout/stderr immediately, and let team.py's supported internal
lock/retry bounds operate. Never replay the old operation after ambiguity:
inspect current task/history first, then issue a newly prepared operation.
Finite science timeouts still apply to science, not arbitrarily to writers.
Use FRONTIER's opt-in PUBLISH_RECEIPT on the actual existing publisher call;
an attested commit or committed-only receipt does not recover a terminal exit.
''')
(F/'.gitattributes').write_bytes(b'* -text\n')
members=[dict(path=p.relative_to(F).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps(dict(members=members,limits='Integrity only; additive independent scientific acceptance pending'),indent=2)+'\n')
print('FROZEN',len(members),sha(F/'manifest.json'))
