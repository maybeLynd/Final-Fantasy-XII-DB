"""One bounded reconciliation of the 30-item checked ASTRA snapshot.

This is an owner disposition record, not a dashboard or semantic validator.
Existing results are consumed; no tests, game runs or independent acceptance
are credited here. The executor uses supported fresh board transactions.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
snapshot = json.loads((HERE / 'input-snapshot-01.json').read_text(encoding='utf-8'))

# FINISH_SCOPED means only the original bounded delivery criterion is met.
# REBLOCK means dependencies were consumed, but the proposition remains open.
ROWS = {
 'ASTRA-HANDLE-SEMANTIC-CLOSURE': ('FINISH_SCOPED',
  'FABLE 1aa6311 and current slot-pool/definition pages name 2659D0/3220E0, finite 2047 advance period and EXP047/048; the old writer-denial/integration obligation is satisfied.',
  'Natural reuse, lifetime and universal live stability are not established by this integration.', None),
 'ASTRA-HWBP-LOADED-DEADLINE': ('FINISH_SCOPED',
  'SPEC 7e018ec8 independently accepts the retained bounded 195-hit positive and its incomplete-campaign designation. EXP031 separately retains the later post window and unmatched timing. This finishes preservation/review delivery, not the incomplete matched campaign.',
  'PARTIAL_POSITIVE_ORIGINAL_CAMPAIGN_INCOMPLETE remains; no general debugger safety, timing equivalence or handler-semantic promotion.', None),
 'ASTRA-SHAKE-OPTION-BOUNDARY': ('FINISH_SCOPED',
  'SPEC accepts exact original compute-before-copy and override OR(two flags) boundary; FABLE 0080231f1 and OPUS consume it. 28-byte write/32-byte stride is retained.',
  'No authored-state binding, per-frame occupancy, MT draw count or scheduling conclusion.', None),
 'FABLE-REQ-ASTRA-OLD-SAVE-LOAD': ('FINISH_SCOPED',
  'SEM independently accepts retained same-process older-save import; FABLE bbbc4b557 and OPUS section8b consume prefix/bank0 endpoints, 1572 changed load bytes and B=active buffer+4E68C.',
  'Sequential non-atomic sampling; keep-bank endpoint equality is not copy/swap/lifetime proof. Change-save-reload remains a separate open question.', None),
 'OPUS-REQ-ASTRA-S33-LOOT-POOL-ISOLATED-RUN': ('ALREADY_DONE',
  'The original request is already DONE; ORACLE transfer and EXP141 at74e88f699 are its delivery. This is a stale wakeup.',
  'ORACLE executions are not ASTRA tests. Callee stubs and natural placement/exhaustion limits survive.', None),
 'ASTRA-SKELETAL-RESET-LIVE': ('REBLOCK',
  'EXP127 dispatch-ownership review accepts only synthetic/disposable native dispatch controls. It does not qualify FF12 tracing or repair FIP/FXSAVE transparency.',
  'EXP127 remains INVALID_POST_TRACE, crash cause UNKNOWN; paired raw boundaries are provisional observations, not skeletal semantics.',
  'A named instrument hypothesis/change with FIP/FXSAVE preservation and post-detach responsiveness/dialog controls, independently reviewed against the exact intended trace; no unchanged four-breakpoint rerun.'),
 'OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME': ('REBLOCK',
  'The cited FAILED-SESSION filename is absent; the actual primary report is REVIEW-EXP127-SKELETAL-FAILED-SESSION.md. Its ACCEPT-WITH-NARROWING retains raw counts while withholding health and causation.',
  '2113 boundary pairs and sampled RCX values do not establish codec behavior, universal arena/lifetime or healthy execution. K14 is accepted and closed separately.',
  'Consumer identifies an arena/reachability proposition still required after K14 and retained evidence, with valid identity/state and a repaired health-qualified collector if original process observation is truly necessary.'),
 'OPUS-REQ-ASTRA-BJ1-GUARD-SNAPSHOT': ('REBLOCK',
  'SPEC818e85de6 accepts preparation and OPUS9811b61f5 supplies TITLE/FIELD guard predicates. Preparation is not an observation.',
  'No prepared backed-up save/slot/area proof or naturally initialized paired guard capture; missing guard data is INVALID, not zero.',
  'Exact backed-up save identity/slot/area, initialized TITLE and FIELD state proof, scoped read collector and controls; current menu setup allowance remains spent/unapproved. First reconsider static/retained sufficiency.'),
 'FABLE-REQ-ASTRA-MT-CURSOR-ACROSS-A-CAMERA-SHAKE': ('REBLOCK',
  'FRONTIER1889e1463 prepares five slots, Stepping/dgl trigger and a bounded tick discriminator. Shake computation before copy is now accepted.',
  'A save/trigger recipe does not prove zone binding, active drivers, original ticks or per-tick RNG consumption.',
  'Prove exact zone/driver/tick binding and whether static original-code composition suffices; only then a bounded validated collector for the still-required natural scheduling claim, without reopening the parked menu setup.'),
 'FABLE-REQ-ASTRA-EO3-PATH-POINTER': ('REBLOCK',
  'FABLE/OPUS consume requested index versus accepted/carry +24 distinction. SPEC accepts stopped-observer synthetic controls and exact32E846 anchor only.',
  'No live accepted/issued/delivered pointer, initialized allocator state or universal observer transparency; FIP and pending-event-abort boundaries remain open.',
  'Exact .efb backed-up load trigger and observer qualification for FIP/pending-event abort plus post-detach health; first exhaust retained/static identity analysis. Only affected natural pointer state requires fresh C.'),
 'FABLE-REQ-ASTRA-KIND-INDEX-TRACE': ('REBLOCK',
  'FABLEaeb83f16d and OPUS consume alignment/count/+28-size and +5C-width corrections; FRONTIER supplies a bounded .efb transition recipe.',
  'The actual correlated request-kind/index/accepted/issued/delivered tuple census is not captured by those corrections.',
  'Named consumer and a still-needed tuple proposition after retained/static analysis; exact prepared load identity and qualified collector with separable controls. Batch with EO3 only if attribution remains distinct.'),
 'FABLE-REQ-ASTRA-LEADER-STATS-NULL': ('REBLOCK',
  'FABLE agrees that no hits in one session cannot establish a global non-null invariant and supplies its correction procedure.',
  'Zero RAX at23B15E is not observed. A finite no-hit window would not prove impossibility.',
  'A static reachability/invariant discriminator first, or an exact prepared state/control for a decisive NULL hit with stack identity; consumer must confirm the proposed wording correction actually landed.'),
 'FABLE-REQ-ASTRA-LEDGER': ('REBLOCK',
  'EXP010 loaded no-arm control is retained; EXP019 player-KO baseline is not an enemy-kill/death-chain observation.',
  'RT1 ledger armed observations and target->command->executed action->consequence are missing.',
  'Prepared enemy target/command/action/death route, validated observer and paired expected fields; isolate no-kill control. Retained/static/original-code evidence may close bounded fields before any gameplay.'),
 'FABLE-REQ-ASTRA-REAR-HALF-VOICE-PAN-LISTENING-TEST': ('REBLOCK',
  'FABLE36a84e00b consumes original-code spread reading; spread1 collapse and stereo-side ambiguity remain explicit.',
  'Sample pan and interpolator target are not audible side; natural spread/voice/channel state is not established.',
  'Named remaining presentation proposition with exact prepared voice/speaker/spread and audio observation controls; prefer original-code/state proof if the claim is only target arithmetic.'),
 'OPUS-REQ-ASTRA-AUDIO-GATE-LIVE': ('REBLOCK',
  'Default pan40/volume7F correction and issued-arguments versus native voice-acquisition boundary are consumed. FRONTIER identifies rbn_a0380 voice calls.',
  'No controlled selective-gate/actual voice-acquisition observation; an issued sound request is not a playing voice.',
  'OPUS supplies exact selective gate discriminator and native-voice identity/control, prepared backed-up scene state and qualified bounded logging; first determine which claims retained original-code evidence already settles.'),
 'OPUS-REQ-ASTRA-CML1-COLUMN-STABILITY': ('REBLOCK',
  'cc1deea6f and OPUS consume effective16-byte entry stride versus24-byte channel stride, not the old8-byte formula; complete duplicate CAM7 payloads are equal. FRONTIER provides rbn_a0380 entry6 authored9 versus first-match6.',
  'This counterexample fixes observer addressing; it does not refute/establish actual initialized overwrite. Identical pictures cannot identify the selected index.',
  'Exact loaded blob/manager identity and a discriminator for authored versus accepted index, or a static proof of all relevant initialized writer paths; no repeat of the settled stride check.'),
 'OPUS-REQ-ASTRA-MGRMARK-RELOAD': ('REBLOCK',
  'SPEC accepts the physical clear-offset evidence; OPUS independently resolves image-offset displacement to22C6D20 and finds the second clear/5-row SoA reset. Canonical sticky/no-writer premise is withdrawn.',
  '21A6D20 in the instruction is an offset from image base, not the getter absolute22C6D20. Ordinary reload timing/mark consumption remain unobserved; no reset coverage is credited.',
  'Consumer names any reload-timing proposition still required after per-row teardown/whole-block init correction; analyze original reload callers first, then prepare exact area transition/state only if timing remains material.'),
 'OPUS-REQ-ASTRA-PHYRE-HIERARCHY-AT-RUNTIME': ('REBLOCK',
  'EXP124 raw audit is ACCEPT and OPUS startup return DONE; four actual descriptor identities corrected in71b9cfef2. Guard-minus58 resolves member objects, not class descriptors.',
  'Do not recapture173 spans. Sampled values, seven unprepared cases/four excluded mappings survive; corrected four descriptor +78 live values are unobserved.',
  'OPUS identifies a specific still-required parent fact beyond retained173/known constructor stores, using validated class layout/name/size/identity. Static/original-code proof before any read-only startup collector.'),
 'OPUS-REQ-ASTRA-SHAKE-DRIVER-OCCUPANCY-PER-FRAME': ('REBLOCK',
  'FRONTIER narrows the recipe to occupancy only and consumes the option/copy boundary. Sourcebank+F0 is not runtime channel state.',
  'Per-frame occupancy and per-tick visits are different observations; no visit/draw count follows from a static count or flag snapshot.',
  'Exact prepared driver slots/flags/output identity with a validated event/tick-correlated collector and before/during/after control, if original scheduling cannot be proved without the game.'),
 'OPUS-REQ-ASTRA-TWO-PARITY-CLAIMS-ARE-LIVE-ONLY': ('REBLOCK',
  'FABLE125d86d5a/e0d403734 and OPUS consume unchanged-scratch-not-evidence-of-no-call and bazaar payload0x56490 correction. Containment conclusion survives.',
  'Live title call frequency, refresh timing and change-save-reload persistence remain open. L3 parity is later and not the current endpoint.',
  'Consumer splits any remaining required L1/L2 proposition from L3 parity and supplies exact acceptance discriminator; use original caller/store proof before absence sampling or gameplay.'),
 'SWE2STRUCT-REQ-ASTRA-OV58D-ESPER-ORDER-0930': ('REBLOCK',
  'SPEC818e85de6 accepts local branch proof; STRUCT892c71358 and OPUS9d6115d1e consume4049/A selector1 local return, real status4051..4070/4071..4090. FABLE withdraws the causal OV5/8(d) probe.',
  'Literal natural4049/A occurrence and unit identity were not observed; the refuted causal premise needs no unchanged Esper experiment.',
  'Requester adjudicates whether literal word-presence is independently required for L1/L2 after the causal probe withdrawal; if yes, name impact and a prepared natural discriminator. Do not recreate the answered causal test.'),
 'FABLE-REQ-ASTRA-REGFILE-REUSE': ('REBLOCK',
  'SPECf24457dc7 accepts conditional spawn-record binding; FABLE/CONTRACTd0809ac13/c282e703e restate RC16. Old different-actor-in-pool premise is superseded.',
  'Conditional supplied-state binding is not natural reuse or lifetime; no repeat of accepted original-code binding is needed.',
  'Consumer defines the required natural reuse/lifetime residue under corrected RC16, with identity generation, initialized state and transition discriminator; first use static reachability/lifetime proof.'),
 'FABLE-REQ-ASTRA-STATE-ROUNDTRIP': ('REBLOCK',
  'FABLE1dbd2f844 consumes manualop8 active-buffer correction; old-save import does not answer change-save-reload. FRONTIER gives a purchase/save-crystal/reload recipe.',
  'Change-save-reload is UNOBSERVED. Only piggyback on a valid existing compatible session; no standalone menu recovery or allowance reset.',
  'Prepared backed-up Stepping save with exact gil/bazaar/item-neighbour fields and action controls; validate automatic collector first. Only one consolidated ordinary-actions checklist if natural gameplay remains necessary.'),
}

records = []
for item in snapshot['items']:
    n = item['notification']
    if not n['id'].startswith('AUTO-UNBLOCK-'):
        continue
    u = item['underlying']
    disposition, facts, limits, resume = ROWS[u['id']]
    records.append(dict(notification=n['id'], underlying=u['id'], disposition=disposition,
        accepted_or_returned=facts, unresolved=limits, resume_when=resume,
        evidence_refs=[r for d in item['dependency_returns'] for r in d.get('result_refs', [])],
        preimages=dict(notification=n, underlying=u, dependency_returns=item['dependency_returns'])))
assert len(records) == 23 and set(ROWS) == {r['underlying'] for r in records}

for key, facts, limits in [
 ('FABLE-NOTICE-ASTRA-GG1-SHARPER-CAPTURE',
  'Acknowledged cheaper static ordering discriminator: reader277ACD is proc message10/11; field deliveries22AB83/22AC17 bracket world tick22ABD8 with named gates. This is a prepared proposal, not a live order result.',
  'Natural GG1 order remains open; menu allowance spent/unapproved and observer FIP/health qualification remains necessary. No game launched.'),
 ('FABLE-NOTICE-ASTRA-OV42-PACKET-WORDING-AND-NEXT-1002',
  'Acknowledged FABLE185570319 consumption and SPEC wording debt. Subsequent action producer/interpreter/binding/cost-query packets were delivered through existing routes, not new duplicate requests.',
  'Original frozen inputs remain immutable; additive Row113 radix275, conditional prefix/exclusion/ns8 wording still needs explicit ASTRA correction delivery where absent. Render half1f6569546 has no SPEC acceptance and is not consumed. Acknowledgement is not application or acceptance.'),
]:
    n = next(i['notification'] for i in snapshot['items'] if i['notification']['id'] == key)
    records.append(dict(notification=key, underlying=None, disposition='ACKNOWLEDGE', accepted_or_returned=facts,
        unresolved=limits, resume_when=None, evidence_refs=[], preimages=dict(notification=n)))

# Optional tooling has a completion alternative of reasoned refusal. Preserve the
# actual bounded workaround rather than duplicating the fleet maintenance lane.
key = 'FRONTIER-REQ-ASTRA-PUBLISH-PATHFILE-1001'
n = next(i['notification'] for i in snapshot['items'] if i['notification']['id'] == key)
records.append(dict(notification=key, underlying=None, disposition='DECLINE_OPTIONAL',
    accepted_or_returned='Reasoned refusal for this evidence lane: the existing explicit-path split is available, and the latest126-path publish ran at12724 UTF16 units within the24000 guard. No selected empirical capture is blocked by pathfile support.',
    unresolved='This does not implement or reject the technical usefulness of pathfile support for other workers. FRONTIER/technical delivery may retain it as maintenance; ASTRA returns to required L1/L2 evidence.',
    resume_when=None, evidence_refs=['commit:7b4e2b92cc1e33177baf166812827ad16356600c'], preimages=dict(notification=n)))

primary_paths = [
 'Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-SHAKE-OPTION-BOUNDARY.md',
 'Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-MGRMARK-CLEAR.md',
 'Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-EO3-STOPPED-OBSERVER.md',
 'Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-EXP127-INSTRUMENT-OWNERSHIP.md',
 'Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-EXP127-SKELETAL-FAILED-SESSION.md',
 'Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-old-save-start-p.md',
 'Database/FFXII TZA/_experiments/EXP-031-loaded-deadline-control.md',
 'Database/FFXII TZA/_experiments/evidence/EXP-031-loaded-deadline/recovered/observation.json',
 'Database/FFXII TZA/_index/_inbox/SWE2-AUDIT-SPEC.md',
 'Database/FFXII TZA/04-Actor-Entity/battleunit-slot-pool-and-actor-class.md',
 'Database/FFXII TZA/04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md',
 'Database/FFXII TZA/17-Presentation-Rendering/Scripted-Camera/how-a-camera-reaches-the-renderer.md',
 'Database/FFXII TZA/19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md',
 'Database/FFXII TZA/_experiments/evidence/cml1-runtime-discriminator/README.md',
]
primary = [dict(path=p, sha256=hashlib.sha256((ROOT / p).read_bytes()).hexdigest()) for p in primary_paths]
plan = dict(kind='OWNER_QUEUE_RECONCILIATION_NOT_NEW_SEMANTIC_EVIDENCE', snapshot_revision=snapshot['revision'],
    snapshot_epoch=snapshot['recovery_epoch'], snapshot_sha256=hashlib.sha256((HERE/'input-snapshot-01.json').read_bytes()).hexdigest(),
    original_counts=dict(ready=30, active=6, automatic_notices=23, informational_notices=2, substantive_requests=4, optional_tooling=1),
    primary_records=primary, records=records,
    untouched_substantive=[i['notification']['id'] for i in snapshot['items'] if i['notification']['id'] not in {r['notification'] for r in records}],
    limits='No new tests, captures, original-code execution or live observations. Four scoped completed deliveries, one already-DONE request, eighteen still-open original requests, two acknowledgements, one optional refusal. Scientific unknowns are not waived.')
for name in ['dispositions-01.json', 'DISPOSITIONS.md']:
    if (HERE / name).exists():
        raise ValueError('immutable output exists: ' + name)
(HERE/'dispositions-01.json').write_text(json.dumps(plan, indent=2), encoding='utf-8')
lines = ['# ASTRA ready-queue reconciliation, 2026-10-03', '',
 'The checked snapshot had **30 READY and 6 ACTIVE**: 23 automatic wakeups, two information notices, four substantive requests and one optional tooling request. The queue primarily measured unprocessed follow-up. ASTRA let that work lag while pursuing the OV42 research chain.', '',
 'This record consumes returned evidence without claiming new experiments or independent acceptance. Completed administrative notices are not answered game questions. Board lifecycle receipts record the actual resulting counts; these decisions alone are not proof of mutation.', '',
 'Each original BLOCKED request is resumed for owner reconsideration. Only four bounded deliveries finish; eighteen are reblocked on the exact remaining prerequisite. The already-DONE loot request is untouched. Narrow disposition claims grant no peer-file or runtime authority.', '']
for r in records:
    lines += ['## ' + r['notification'], '', '**' + r['disposition'] + '**' + (' — ' + r['underlying'] if r['underlying'] else ''), '',
        r['accepted_or_returned'], '', '**Still open / limits:** ' + r['unresolved'], '']
    if r['resume_when']:
        lines += ['**Resume condition:** ' + r['resume_when'], '']
    if r['evidence_refs']:
        lines += ['**Existing delivery refs:** ' + '; '.join(r['evidence_refs']), '']
lines += ['## Remaining substantive READY', '', *['- '+t for t in plan['untouched_substantive']], '',
 'These four need proposition-based method selection. Historical runtime labels do not compel live FF12. SD194 needs inherited-buffer/reachability analysis; UQ146 needs installed-UCRT call-frame sufficiency analysis; PC1 needs a stronger static writer-route analysis before any bounded absence watch; UQ147 needs scheduling/reachability proof before a prepared natural summon observation.', '',
 'Menu budget spent/unapproved; EXP127 invalid/crash unknown; K14 accepted/closed. Goal ACTIVE/NOT_MET. No game, PC control, instrumentation or reference/save/config changes.']
(HERE/'DISPOSITIONS.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps(dict(records=len(records), scoped_delivery_finishes=4, reblocked=sum(r['disposition']=='REBLOCK' for r in records), remaining_substantive=plan['untouched_substantive']), indent=2))
