"""Seal an additive producer correction; retained inputs are copies, not recaptures."""
import hashlib, json, shutil
from pathlib import Path
W=Path(__file__).resolve().parent
ROOT=next(p for p in W.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
P=W/'gauge-transfer-check-repair';F=W/'gauge-transfer-check-repair-frozen-ready'
OLD=ROOT/'Database/FFXII TZA/_experiments/evidence/ov42-gauge-callback-binding'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((P/'result-v2-01.json').read_text())
s=json.loads((P/'prove-v2-01.status.json').read_text())
pin='09f4779ae272e157017938e6b024696fda99add25d6fedc2b2a49c94a098b121'
if not(s['terminal'] is True and s['exit']==0 and s['exception'] is None and s['driver_sha256']==pin==sha(P/'prove-transfers-v2.py')==r['driver_sha256'] and r['producer_complete'] is True):raise ValueError('actual current successful producer required')
old=json.loads((OLD/'result-01.json').read_text())
if not all(r['facts'][k]==v for k,v in old['facts'].items()):raise ValueError('prior scientific facts changed')
ids=['secondary-handler-memory-identity','callback-store-memory-offset','consumer-tail-to-handler','consumer-indirect-jump','matched-tail-to-initializer']
if [c['id'] for c in r['source_controls']]!=ids or not all(c['refused'] for c in r['source_controls']):raise ValueError('missing nonempty discriminating controls')
if (P/'prove-v2-01.stderr').read_bytes():raise ValueError('unexpected producer stderr')
(P/'README.md').write_text('''# Callback transfer checker: additive correction

Independent review [95d495604](../../../_index/candidates/auditspec-review-astra-ov42-gauge-binding-1003/REVIEW.md) accepted the [original bounded shipping facts](../ov42-gauge-callback-binding/README.md), while demonstrating three jump mutations missed by its producer. Shipping facts stand on that independent transfer census, not on the old call-only check. The original package, driver, results and manifest remain unchanged.

Player view: this sharpens the evidence about which functions update the stat bars. It adds no observation of when a running game updates them.

Question: does the real successor invocation reject jump-form transfers and memory-only semantic changes while retaining all established facts? Method A, using the same retained 822 shipping bytes. No new capture, native/emulated execution, live game, input or save changes.

The successor enumerates calls and unconditional/conditional branches. The consumer admits exactly four prescribed calls and branches only to instruction boundaries inside its complete body. Register/memory transfers, external branches, missing calls and unexpected calls fail. The matched tail admits no calls or branches. Return/fall-through claims retain the predecessor's exact byte/body bounds; this is not a general ISA verifier or a proof of transitive effects.

`prove-transfers-v2.py result-fresh.json` is the actual command under the analysis venv. It requires the canonical original 65-member package at its repository-relative path, its exact manifest, all unchanged members, the pinned reference image, successful original capture/extent receipts and the reviewed access-role validator. Missing prerequisites fail; the packet alone is not a stand-alone image fixture. Original captures copied here are byte-identical dependency witnesses, not additional capture credit.

The terminal producer accepts the unchanged shipping facts. Five labelled synthetic source-record controls reject: secondary callback identity changed only in the memory operand; callback-store displacement changed only in the memory operand; consumer jump to a handler; consumer indirect jump; matched-tail jump to the initializer. Each requires the specific semantic/transfer diagnostic, so a text-pin failure cannot impersonate that detector. Reviewer's old tests remain external corroboration, not our runs.

Raw command/status/stdout/stderr, exact predecessor source, successor, generator, two unchanged source maps and deterministic result are preserved. `result-v2-01.json` records 14 consumer transfers and an empty matched-tail transfer set. All prior facts compare equal. The manifest establishes integrity, not independent acceptance or an ORACLE execution seal; the developer run precedes publication.

Natural initialization, callback-field writers/reuse, lifetime, scheduling, resource binding, presentation and transitive helper effects remain OPEN. This producer repair requires non-author review. FABLE/OPUS's existing incorporation tasks retain the already accepted original facts and these limits; no duplicate scientific experiment or consumer edit is required.
''')
(P/'KNOWN-PRECONDITIONS.md').write_text('Read review95d495604 and the immutable predecessor before changes. Call-only absence checks miss direct tail transfers and indirect jumps; include all call/jump/conditional transfers and validate internal targets against instruction boundaries. Semantic controls must mutate the field the semantic detector reads while preserving the independent text pins. The current input schema is ranges[].instructions[] with pc/args/memory. This successor deliberately requires the original canonical65 members, pinned image and current successful capture/extent/access-role prerequisites; copying only the driver cannot prove anything. Never rerun completed captures or treat control-record mutations as original instruction execution. No natural initialization/timing inference.\n')
F.mkdir()
for name in ['producer-v1.preimage.py','prove-transfers-v2.py','QUESTION.md','README.md','KNOWN-PRECONDITIONS.md','result-v2-01.json','prove-v2-01.status.json','prove-v2-01.stdout','prove-v2-01.stderr']:
    shutil.copyfile(P/name,F/name)
for name in ['source-01.json','target-source-01.json']:
    shutil.copyfile(OLD/name,F/name)
for p in [Path(__file__),W/'prepare-gauge-transfer-repair.py']:
    shutil.copyfile(p,F/p.name)
(F/'.gitattributes').write_bytes(b'* -text\n')
members=[dict(path=p.relative_to(F).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(F.iterdir()) if p.is_file()]
manifest=dict(members=members,method='A retained original-source analysis and synthetic producer controls',dependency=dict(commit='64cb2c0c330931d7511a930c722b17a86afa6cfc',manifest=r['input_manifest_sha256'],independent_review='95d495604a3994a0fe0078e4b0620a168c9137b7'),limits='Additive producer sensitivity repair; original facts unchanged; independent successor review pending; no native/live/reachability/lifetime closure or committed-before-execution seal')
(F/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('FROZEN',len(members),sha(F/'manifest.json'))
