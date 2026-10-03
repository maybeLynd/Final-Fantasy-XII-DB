"""Freeze the new order claim over retained inputs, never recapture them."""
import hashlib,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
ROOT=next(p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
E=ROOT/'Database/FFXII TZA/_experiments/evidence';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-dismiss-stage-retained-01.status.json').read_text());r=json.loads((P/'result-dismiss-stage-retained-01.json').read_text())
if s['terminal'] is not True or s['exit']!=0 or s['exception'] is not None or s['driver_sha256']!='f3929d1a1ffca77e23fcb8f41482e31e2de3aabd8b169fc5790e2e6fbb3a1097' or r.get('producer_complete') is not True or len(r['controls'])!=4:raise ValueError('Proof incomplete')
out=W/'uq147-dismiss-stage-frozen-ready'
if out.exists():raise ValueError('Immutable fresh package required')
out.mkdir();pins=[]
for dep in r['canonical_dependencies']:
 src=E/dep['slug']/dep['path']
 if sha(src)!=dep['sha256']:raise ValueError('Canonical dependency moved')
 name='retained/'+dep['slug']+'/'+dep['path'];dst=out/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 if dep['path'] in ['source-02.json','source-01.json','retained-prefix-01.json']:pins.append(dict(path=name,sha256=dep['sha256']))
for slug in ['ov42-sequence-queue-source','ov42-kind-row-coherence']:
 for name in ['manifest.json','extent-01.json','extent-01.status.json','capture-02.status.json','data-01.status.json']:
  dst=out/'retained'/slug/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(E/slug/name,dst)
for name in ['prove-dismiss-stage-retained.py','result-dismiss-stage-retained-01.json','DISMISS-STAGE-QUESTION.md','NEXT-DISCRIMINATOR.md','NEXT-DISCRIMINATOR.checkpoint93.preimage.md','capture-dismiss-stage-boundary.py']:
 shutil.copyfile(P/name,out/name)
for tag in ['prove-dismiss-stage-retained-01','capture-dismiss-stage-01','prepare-dismiss-stage-capture-01','lookup-special-presentation-01','lookup-special-init-01']:
 for ext in ['.status.json','.stdout','.stderr']:shutil.copyfile(P/(tag+ext),out/(tag+ext))
for tag in ['lookup-special-presentation-01','lookup-special-init-01']:shutil.copyfile(P/(tag+'.json'),out/(tag+'.json'))
shutil.copyfile(W/'prepare-uq147-dismiss-stage-capture.py',out/'prepare-uq147-dismiss-stage-capture.py');shutil.copyfile(Path(__file__),out/Path(__file__).name)
(out/'publication-source-map.json').write_text(json.dumps(dict(producer_complete=True,source_pins=pins,semantic_result_sha256=sha(out/'result-dismiss-stage-retained-01.json'),limits='Publication adapter binds the actual reused code sources, not a new semantic run or code capture'),indent=2))
(out/'README.md').write_text('''# Dismiss mode-bit clear and local state5 publication

Question: is the Dismiss clear here a later special-sequence finishing-state effect? MethodA reuses complete original code and embedded tables from committed ov42-sequence-queue-source0c421573 and ov42-kind-row-coherenced8328725/independent74b96c7cd. Original EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8/base120000. No new original-byte capture, machine-code execution or live FF12. Old producer/reviewer tests are not rerun or credited as ours.

Under the classifier's full unsigned quotient275, selector byte127 selects jump entry5/306CB0, publishing kind2. Separately,306760 reading kind2 selects relative entry1/306A3D. Matching earlier/later kind, current row and owner is a premise, not a proved natural invariant. Kind1 selects306931 and sets the mode bit, a distinct positive control.

The kind2 arm optionally calls35DAE0, then306D90. It re-reads battle state: bit0set leads to AND~1/directDWORDstore at306A81 and35C620; bit0clear skips that store. Both go to the common rosterflag traversal,332130(3), and this routine's own direct022C2160=5 at306ADF. Thus this conditional direct mode clear precedes that directstate5 write. No finishing-state6/7 guard surrounds this clear. The mode-ladder phrase "when the sequence ends" needs qualification against the original local ordering. Whether the player sees dismissal before/after any visible event remains unobserved.

Opaque helpers can change state. No lasting modeclear, first-ever state5, native helper effects, natural summonerKO/EsperDismiss coexistence, initialized bindings, resource success, atomicity, ownership/lifetime, scheduling, presentation or wholeUQ147 is established. NormalABI/private valid stack/readable objects/returning calls/bounded valid roster traversal/noninterference premises stay explicit. Slot state5 is an internal write, not a screenshot.

Current provef3929d1a/actualterminal0/result01 and four specifically diagnosed source/table-record controls retained. Mutations are labelled static records, not EXE edits/native runs. Actual current shared reviewed role/byte validator7c4ea9f6 is invoked over all three retained code sources; original code/data/table agreement checked against current authorized EXE. Publication map only binds these actual reused inputs to the raw result.

Preparation mistake preserved: capture01 refused BEFORE OUTPUT because a covering retained map exists. Do not repeat/bypass that guard. The lookup result must be inspected, not merely its successful exit. Classifier suffix also already existed in an older package: the mixed-pdata physical bodies contain code, padding and tables and must not be decoded as all code. No capture failure earns scientific credit. The corrected method reuses both full bodies/tables; frozen failed driver/status/raw receipts remain history.

Checkpoint93's proposed +34 native mapping was wrong. It is the text name word, not native dispatch. Original plan preserved plus corrected next step; no capture/test/consumer used the wrong join. Accepted summon-kind-row-carrierc40b2434/49d0564f2 already qualifies304850's current-row carrier; do not repeat it. The new claim concerns local Dismiss ordering only.

Reproduction: run prove-dismiss-stage-retained.py from a repo containing its exact declared canonical dependencies, with a fresh absolute output or package-relative name. Source files/table data/statuses remain pinned in the producer; immutable copies here preserve them, not a competing source. Shared current validator lives in the ASTRA work layout. Frozen driver/input/result receipts are not an ORACLE pre-execution seal. Independent SPEC review and FABLE mode-ladder/UQ147, OPUS mode/command consumption are pending.

No game/PC/input/instrument/save/config/reference or peer-process change; finite own helpers terminate, no detach/restoration required. Zero whole formerly-runtime rows newly closed. FullL1L2+required independently accepted deployedM0M5 ACTIVE/NOT_MET; menu spent/unapprovedextension,EXP127invalid,K14closed persist.
''')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(schema_version=1,status='FROZEN_PRODUCER_VALID_NOT_INDEPENDENTLY_ACCEPTED',method='A retained original code/data and conditional ordering',members=members),indent=2)+'\n')
print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))
