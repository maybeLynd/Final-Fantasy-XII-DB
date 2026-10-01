"""One-time, prefix-only repair of EXP-037..074; never execute historical probes."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path('Database/FFXII TZA')
EDIR = ROOT / '_experiments'
OUT = EDIR / 'evidence/experiment-metadata-recovery'
sha = lambda data: hashlib.sha256(data).hexdigest()
sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import team
board = json.loads(team.BOARD.read_text(encoding='utf-8'))
assert any(t['id'] == 'ASTRA-EXPERIMENT-METADATA-RECOVERY' and t['agent'] == 'ASTRA' and t['status'] == 'ACTIVE' for t in board['tasks'])

# Reviewed against actual contract interfaces/relationships, not category names.
C = {
 'commit': '../07-Combat-Action/CONTRACT-commit-action.md',
 'target': '../07-Combat-Action/CONTRACT-battle-target-buffer.md',
 'config': '../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md',
 'field': '../04-Actor-Entity/CONTRACT-field-runtime-pass.md',
 'rng': '../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md',
 'save': '../19-Save-Load-Settings/CONTRACT-save-image-buffers.md',
 'hp': '../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md',
 'inventory': '../12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md',
 'widget': '../16-UI/Widget-Object-Model/CONTRACT-widget-object.md',
}
linked = {
 40: ('commit', 'Optional cancellation dependency 003105D0 gates and selected local stores only; 0030F760 commit and omitted cancellation callees are not executed.'),
 41: ('config', 'Assessment of retained EXP-001 address expressions and tool documentation; no new config observation or repair of historical E8 failures.'),
 43: ('target', 'Complete original append 00316CD0; synthetic buffer boundaries, no actor dereference or consumer execution.'),
 46: ('target', 'Original reset 00316CF0 and import thunk; memset is a controlled fill, not execution of the native DLL.'),
 47: ('commit', 'Attacker-mask lifetime constraint from reset wrappers 00322050/00322080; does not execute commit, native renewal delegate or live reuse.'),
 48: ('field', 'Resolver dependency 003588B0 under discriminator advance and finite wrap; no field pass, native registry construction or scheduling.'),
 49: ('field', 'Resolver dependency 003588B0 inside renewal and focus selection; stops before native refresh and never executes the field pass.'),
 56: ('rng', 'MT seed caller 00584210 arithmetic and tail argument at 00379CF0, explicitly described in contract section 7; MT seeder and native normalization dependencies omitted.'),
 57: ('save', 'Original active-buffer getter 002EF640 and distinct active/staging identities in a checksum segment; no whole-image clear, copy, submission or full finalizer execution.'),
 60: ('hp', 'Caller-side HP presence, numeric and register-flag translation at 00311608; HP callees are no-effect stubs, so no HP store or lethal transition is established.'),
 64: ('inventory', 'Caller-side five-argument inventory request at 003008A0 after local reservation; inventory is a no-effect stub, so native class storage and item deduction are untested.'),
 68: ('widget', 'Caller-side 00244F50 size, proc and descriptor/payload snapshots; factory is a recording stub, so allocation, copying, ownership and widget procedures are untested.'),
 69: ('widget', 'Same factory caller boundary composed with original router and setter feedback; native factory and widget effects remain stubbed, with no live UI timing.'),
}
none = {
 37: 'Observer preparation with mocked process memory and time; no game-behavior contract observation.',
 38: 'Stack-capture preparation with mocked APIs; no FF12 handler or native fixture execution in this record.',
 39: 'Disposable generated native fixture validates instrumentation; it executes no shipping FF12 instructions.',
 42: 'Observer source-pin refresh and mocked controls; no new game-behavior observation.',
 44: 'Runtime-checker verdict reproduction and repair under fake process boundaries; not a game operation.',
 45: 'Observer dependency qualification under fake memory and time; no native game observation.',
 50: 'Focus fallback selection 00326500 is outside the existing party-slot assignment contract; its native queries and dispatcher are omitted.',
 51: 'Deferred focus commit 00358BC0 is outside the existing party-slot assignment contract; controlled teardown changes do not prove native reentrancy.',
 52: 'No existing contract specifies linked-list loot selection 00319850; experience and licence award is a different operation.',
 53: 'No existing contract specifies overlap pickup search 002FB150; geometry and selection evidence remain on the loot page.',
 54: 'No existing contract specifies this periodic loot eligibility and grant/removal dispatch segment; actual grant and removal are omitted.',
 55: 'No existing contract specifies loot-node collection and retirement 00319920/003197B0; the inventory grant and presentation effects are stubbed.',
 58: 'No existing contract specifies runtime-format header predicate 00255260; save-image-buffers covers whole-buffer clear, getter and copy, not header acceptance.',
 59: 'Numeric scratch copy-out is outside the preparation-step family contract for calculator slots 60-79; no preparation member executes.',
 61: 'No existing contract specifies MP and secondary-resource writers; the HP writer contract is a different operation.',
 62: 'No existing contract specifies this numeric copy-out to MP composition; HP effects and preparation members are not executed.',
 63: 'No existing contract specifies action MP cost 00309110 and its modifier chain; commit-action is commitment, not cost computation.',
 65: 'No existing contract specifies execution-resource consumption 00305640; commit-action and inventory class storage do not specify this caller.',
 66: 'No existing contract specifies this cost-to-consume-to-MP composition; the HP and inventory storage operations are not executed.',
 67: 'No existing contract specifies UI router dispatch 00254B50; the widget-object contract specifies a different allocation and message boundary.',
 70: 'Gameplay-generators explicitly covers LCG and gameplay MT only; this procedural generator and shared scratch are a separate family.',
 71: 'Procedural initialization and draws are outside the LCG/MT gameplay-generators contract; native startup dependencies are omitted.',
 72: 'Facing-and-steering lists different entry points; writer 002E5E10 is not an executed substitute for its 0026B5A0/0026C090 or unread 002E5FB0 paths.',
 73: 'Reapply 002E5F90 and helper 0033CB70 are different from the facing-and-steering contract entry set; equivalence to those entries is not established.',
 74: 'Conversion-boundary controls run 002E5F90/002E5E10/0033CB70, not the facing-and-steering contract entry set; a category match is insufficient.',
}
scope = {
 37: 'Mocked observer and component controls; prepared game observer not used live.',
 38: 'Mocked stack receipt and capture integration controls; no native target used.',
 39: 'Disposable generated native target, cold and positive stack controls, detach and heartbeat receipts; no FF12 code.',
 40: 'Original entry gates and two separately entered local blocks; no stubs, but intervening native calls are omitted.',
 41: 'Retained capture and address-expression assessment plus unchanged implementation AST; no new memory reads from a process.',
 42: 'Dependency hash refresh and mocked observer controls; no game process.',
 43: 'Complete original append, synthetic buffer, no stubs; negative counts are deliberate invalid-state controls.',
 44: 'Old and repaired checker executed with fake process boundaries; historical printed rows reassessed without new captures.',
 45: 'Repaired dependency pin qualified with mocked memory and time; no native process calls.',
 46: 'Complete original reset and import thunk with controlled memset fill; fill writes are separately labeled.',
 47: 'Original reset wrappers to delegate entry, then separate controlled-return cases; native delegate effects omitted.',
 48: 'Six original bodies composed with a stable synthetic registry, including finite wrap; no stubs.',
 49: 'Ten original bodies with synthetic registry and pool; stop before native refresh, with expected null-input fault separate.',
 50: 'Original selection body and encoder with controlled query returns; stop before native tail dispatcher.',
 51: 'Original deferred commit with recording stubs and labeled pending/kind interventions; new-actor tail callee omitted.',
 52: 'Three original bodies with synthetic list, presence and threshold; cookie checker is controlled.',
 53: 'Six original bodies with synthetic geometry and presence; sqrtf surrogate and cookie checker are controlled.',
 54: 'Original caller segment with injected frame and unit plus original focus predicate/getter; overlap/preparation controlled, grant/removal omitted.',
 55: 'Three original bodies with synthetic linked lists; inventory and presentation are no-effect stubs, including repeat-call control.',
 56: 'Complete original normalization body to seed tail boundary; getters, clock and native dependencies controlled, flag intervention labeled.',
 57: 'Original CRC helper and active getter without stubs; finalizer segment entered with injected destination and frame, earlier effects omitted.',
 58: 'Complete original eight-byte header predicate, synthetic inputs, no stubs; no whole-load acceptance claim.',
 59: 'Original numeric copy-out segment with injected result pointer and fallback; no stubs, earlier resolver and later result work omitted.',
 60: 'Original numeric applier segment with injected parent-frame roles and five no-effect setter stubs; no native resource writes.',
 61: 'Five original MP and reconciliation bodies; ownership, eligibility, reaction, number and accumulator boundaries controlled.',
 62: 'Same-state original copy-out, dispatch and MP composition with an explicit injected frame bridge; ownership and eligibility controlled, HP absent.',
 63: 'Four complete original cost bodies without stubs, synthetic tables and original float constants; setup failures and invalid-input faults preserved.',
 64: 'Complete original preparation and pointer resolver; inventory and gil dependencies controlled, invalid header and stride faults separate.',
 65: 'Complete original consumer and pointer resolver with eight stubs and two labeled callback interventions; native resource stores omitted.',
 66: 'Ten complete original bodies from consumer entry through cost and MP writes, no phase bridge; ownership, eligibility and gil controlled.',
 67: 'Complete original router and shipping dispatch tables with recording callbacks; route arguments established, native UI acceptance omitted.',
 68: 'Complete original generic handler with recording factory/finalization/cookie stubs and a labeled packet/busy intervention.',
 69: 'Original router, generic handler and setter composed across two calls on unchanged intermediate memory; factory and other dependencies controlled.',
 70: 'Two complete original procedural RNG helpers, synthetic state and controlled MXCSR, no stubs; failed fixtures and rounding corrections preserved.',
 71: 'Original initializer then original draw on the same memory; preparation and tail stubs plus labeled early/tail interventions.',
 72: 'Complete original facing writer with three recording callback stubs and controlled MXCSR; no native transforms or live movement.',
 73: 'Original reapply and writer twice on the same state with three callback stubs; separate original angle helper has no stubs.',
 74: 'Ten new paired conversion-boundary inputs through original reapply/writer and separate helper; writer callbacks controlled, older runs not replayed.',
}
assert set(scope) == set(range(37, 75)) == set(linked) | set(none)
assert not set(linked) & set(none)
tools = {37:'test_observe.py',38:'test_capture.py',39:'run_control.py',42:'test_observe.py',45:'qualify.py'}
prepared = {37,38,42,45}
OUT.mkdir(exist_ok=False)
rows=[]
for n in range(37,75):
 p, = EDIR.glob(f'EXP-{n:03}-*.md')
 raw=p.read_bytes(); assert raw.startswith(f'# EXP-{n:03}:'.encode())
 title=raw.decode('utf-8').splitlines()[0].split(': ',1)[1]
 d=EDIR/'evidence'/p.stem
 manifest=json.loads((d/'manifest.json').read_text())
 for name,spec in manifest['files'].items():
  data=(d/name).read_bytes(); assert sha(data)==spec['sha256'] and len(data)==spec['bytes'],(n,name)
 method='B - isolated original-code execution'
 evidence_class='isolated original-code'
 status='COMPLETE - bounded isolated original-code evidence'
 if n in prepared:
  method='A - offline instrument preparation';evidence_class='offline preparation';status='PREPARED - offline controls only'
 elif n==39:
  method='Native instrument control - generated disposable fixture';evidence_class='native instrument control';status='COMPLETE - instrument control only'
 elif n==41:
  method='A - retained-evidence assessment';evidence_class='retained-evidence assessment';status='COMPLETE - bounded offline assessment'
 elif n==44:
  method='A - offline tool reproduction';evidence_class='offline tool reproduction';status='REPRODUCED - checker verdict defect and repair'
 if n in linked:
  key,coverage=linked[n];contract=C[key]
 else:contract='none - '+none[n];coverage='No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.'
 fm=dict(experiment=f'EXP-{n:03}',title=title,status=status,contract=contract,
         evidence_class=evidence_class,method=method,live_game='false',execution_scope=scope[n],contract_coverage=coverage,
         tool=f'evidence/{p.stem}/{tools.get(n,"check.py")}',date_designed='2026-09-12' if n==74 else '2026-09-11')
 if n not in prepared:fm['date_run']='2026-09-12' if n==74 else '2026-09-11'
 fm['metadata_recovered']='2026-09-12'
 assert (EDIR/fm['tool']).is_file()
 # Flat YAML is deliberate: both existing consumers parse flat scalar fields only.
 prefix=('---\n'+''.join(f'{k}: {v}\n' for k,v in fm.items())+'---\n\n').encode('utf-8')
 assert all('\n' not in v and ': ' not in v and ' #' not in v for k,v in fm.items()),fm
 p.write_bytes(prefix+raw)
 rows.append(dict(record=p.name,original_body_bytes=len(raw),original_body_sha256=sha(raw),prefix_bytes=len(prefix),metadata=fm,
                  historical_manifest=f'evidence/{p.stem}/manifest.json',historical_manifest_sha256=sha((d/'manifest.json').read_bytes()),historical_files=len(manifest['files'])))
contracts={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in sorted(ROOT.rglob('CONTRACT-*.md'))}
payload=dict(scope='Metadata recovery only; no historical experiment rerun or semantic revalidation campaign.',
             contract_inventory_sha256=contracts,records=rows)
(OUT/'recovery.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('Prefixed',len(rows),'records; original bodies unchanged; linked',len(linked),'with bounded contract coverage.')
