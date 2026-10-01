# ASTRA — first EO3 live request: bounded run specification

Existing task: FABLE-REQ-ASTRA-EO3-PATH-POINTER. Consumers: FABLE, resource-request
queue EO-3 semantics; OPUS, ResourceRequestSlot +0x24 and request phase/ABI.
Phase remains DATABASE L1+L2. This document prepares the existing experiment;
it is neither a new authorization request nor evidence that the run occurred.

## ASTRA — Question and method

Does one ordinary primary map-file request in the designated game carry its
allocated path pointer P through the narrow request field and recover exactly P
at the issuer? Alternatives: P is representable by sign extension of its low32;
P loses identity through that representation; or the candidate route does not
reach the selected primary caller in this state. Failure to observe the selected
caller does not distinguish the first two alternatives.

Method C is required for actual allocation and caller/state selection. Existing
shipping-code evidence already establishes the narrow/sign-extend mechanism.
Do not repeat an isolated fixture to assert actual heap placement. The former
EXP127 four-site hot trace is not reused. Current control sources preserve its
failure lessons without asserting its crash cause or full state transparency.

## ASTRA — Exact identity and starting state

- Designated executable: `D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE
  ZODIAC AGE/x64/FFXII_TZA.exe`, SHA256
  `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
  Compare the current image/module layout and relevant shipping instruction
  spans with the pinned reference. Log actual PID, creation time, image path,
  module bases/hashes and all deployed tool/source hashes. Do not operate on a
  historical PID, a mod client, an unexpected existing game, or an unqualified
  image. The existing native child nonce is not evidence of game ownership.
- Use a fresh backup of the current complete save/config directory, verified
  before any changes. Preserve the original independently; the live directory
  is the disposable working copy. Re-observe Steam Cloud OFF and launch options,
  rather than reusing the historical UI receipt as current state. Cloud stays
  off until the new experiment's originals are verified restored.
- Prepared modern save: `76561198045890736/FFXII_000`, 5331 bytes, SHA256
  `859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825`,
  SAFH56690, visible Stepping in Dalmasca Estersand. Use the retained copy only
  inside the new disposable working set. Never restore an old backup over
  current user files. Select by actual save/menu identity, not row number alone.
- Historical EXP026 before-state: Vaan HP103, position approximately
  (65.042313,44.434589,267.024933). One Right camera pulse of one second, then W
  for one second, reached visible Rabanastre Eastgate with HP103. After position
  was (248,-10,72). These are retained route controls, not fresh observations or
  a guarantee of identical camera/input timing on another launch.

## ASTRA — Observation boundaries and controls

Use only the three selected hardware execute sites after current image-base and
instruction verification. These addresses are the pinned image's virtual
addresses, not assumed rebasing offsets.

| Phase | Required observation |
|---|---|
| Producer 0032E84D, before CALL 0032E870 | Full RDI=P; RDX=zero_extend(low32(P)); ECX=FF; `[RSP+38]=00377F87`; at most128 bytes from **RDI**, through NUL. |
| Builder 0032E983, before epilogue | R10 slot; full0x80 slot bytes; RAX=requestId; `[RSP+38]=0032E852`; same-thread frame relationship `builderRSP+40=producerRSP`. |
| Issuer 0032E111, before call | RBX same slot and same requestId; nonzero count; full slot bytes; RCX=Q=sign_extend(slot low32). |

The primary caller control is CALL00377F82 through thunk0032E7B0; the tail thunk
preserves return00377F87. The copied path must independently name the selected
`ps2data/efb/*.efb` resource. Record the actual name; the earlier actor capture
does not establish that name. The queue's phrase "path at producer RCX" is wrong
at this chosen phase: **RCX is FF**, and RDI is the path pointer. RDI also survives
MOV EDX,EDI, so an extra0032E846 stop is unnecessary. A visible map load alone
does not prove this primary call; alternate/gated routes must remain possible.

Reentry while the builder pumps is possible. Correlate thread/frame/return and
then slot+requestId; never join the next same-thread hit by order alone. Reject
unresolved reuse. The copied path and phase constants are positive controls;
the no-zone baseline is a baseline only, not proof that the detector can see a
missing event. Menu MRP/exfont requests are different callers and cannot replace
the primary map control. They may be retained as unselected observations.

Before the zone pulse, verify visible field/HP and input baseline. Reuse the
documented Right/W actions and supported controller; preserve the separate
registration observations. Input sent, input registered, movement accepted,
movement/zone transition, and request observations are separate claims. While
armed, keep control brief and stop sending input immediately after the pulse.
Do not leave PC control active during reduction/review.

## ASTRA — Bounds, failure handling and acceptance

One selected correlated request first; at most10 seconds armed, eight producer
hits, 32KiB semantic context/read payload and128 bytes per selected path. Raw API
journals are additional provenance, not secretly included in the semantic byte
budget. Attachment and cleanup have their separate bounded deadlines. The connected
runner starts Recorder after reference qualification and just before attachment;
this conservatively includes attachment latency and never extends the ten-second
armed window. Manual setup does not consume that clock. Use run_eo3.py with the
existing capture_scoped_v2; wait for its post-arming/continuation armed.json before
the input trigger. A clean partial/zero-event timeout is INCOMPLETE.
`Recorder.finish()` is still mandatory for any complete-chain claim.

If P differs from sign_extend(low32(P)) at the producer, hold before enqueue and
invoke the independently reviewed owned-abort path. Retain P and staged RDX as
raw stopped observations. A projected Q is not an observed issuer Q. A low32
value with bit31 set can lose identity only on the later sign extension; do not
mislabel that as an already-observed discarded upper half. Abort is not a
healthy completed-chain result and must not close the issuer/crash claim.

Stop for unknown identity, missing/partial reads, path/control mismatch, stale
event/context, ambiguous reuse, budget expiry, fatal dialog, or loss of response.
Do not retry the same failed configuration unchanged. On user stop/takeover,
halt automation and do not restart it automatically. Existing ordinary live
authorization remains active unless such a stop occurs.

Normal acceptance requires a complete identity-matched chain, successful
debug-register clear/readback and detach, followed by a real visible input
response and absence of fatal dialogs. Record before/after field presentation
and internal state separately. CPU activity or API success cannot substitute.
No instruction-after-call, file-read success, whole-state transparency,
scheduling guarantee or historical crash linkage is established by these sites.

After termination/exit, verify process and instrumentation absence. Preserve
every changed disposable file before restoring this session's verified backup.
Zoning is known to change autosave as well as settings: the old same-process
cleanup script permits only a config delta and cannot be reused unchanged.
Use the retained EXP026 two-file change guard as a starting pattern, review the
actual change set, restore exact fresh originals, and recheck full census,
unchanged backup and reference hash before releasing @runtime.

## ASTRA — Remaining operating work and evidence return

Independent stopped-observer review is queued. The connected runner now has a
designated-process pre-attach guard, conservative bounded clock, post-arming
notification and the retained abort integration. RUNNER-CONNECTION.md records
the synthetic connection controls and repaired cleanup-stop counterexample. Its
native CLI qualification/use and current save/Cloud/health/restoration receipts
remain unperformed; native-child controls alone do not fill those obligations.
Do not spend a live session discovering them. The experiment's actual allocation,
primary caller and issuer observations remain OPEN.

Return raw API/context/memory records, source/binary identity, UI/input/health
and cleanup receipts, the exact reducer and normalized P/L/Q with correlation,
plus separate established/refuted/unresolved claims and limitations. Route
canonical updates to FABLE/OPUS; acceptance stays pending until consumers agree.
