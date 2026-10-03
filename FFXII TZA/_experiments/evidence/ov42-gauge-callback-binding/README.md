# Original stat-bar callback binding and local effect boundary

Player version: a newly registered bar gets a prescribed update callback. Reusing an already matching bar record changes its associated object but leaves the old callback in place. A bar update can run synchronously before the surrounding cost routine continues. This package proves the local code boundary; it does not establish what a player saw or which callback a naturally initialized record currently holds.

## Question and hypotheses

OV42's cost path attempts `28F1F0` before its post-query veto and own resource store. Does original registration prescribe the callback identity at `view+38` for all selected records, including reused ones? Does the conflicting canonical edge (handlers called by `2973E0`) describe this consumer's own calls?

H1: registration always restores the prescribed callback. H2: new and existing-record paths differ, leaving callback identity conditional on prior state. H3: `2973E0` itself directly/indirectly calls either handler. Existing canonical handler descriptions already state that handlers call `2973E0`; do not count that naming as a new discovery.

## Method and identity

Method A, complete shipping instruction bodies and local dataflow/footprint. No native/emulated execution or game session. Exact reference EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base `120000`, Capstone5.0.7. Raw original metadata, physical bytes, normalized instructions/access roles, actual CLI receipts and tool identities are retained.

The producer verifies complete575-byte registration/initializer bodies `296360`, `297C10`, `3F89C0` and complete247-byte consumer `2973E0`, totaling822 bytes. Both actual capture invocations use the reviewed shared access-role adapter and `capture_prerequisites.check`; complete metadata, successful upstream receipts, complete wrapper and byte correspondence are prerequisites, not optional labels.

## Established local facts

- `296360`'s admitted registration leg prescribes `29B7D0` at `0209C240` and `29B810` at `0209C298`, with its incoming object as context. Its guards and unregister leg remain part of the condition.
- `297C10`'s free-entry leg installs those callbacks at row/row+58. An existing matching record jumps to `297CE2`, updates contexts+48/+A0 and id+B0, and neither calls the initializers nor writes callback+38/+90. H1 is too broad; H2 is supported locally.
- `3F89C0` reads the fifth argument at its currentSP+50 (callerSP+20 after the CALL/prologue adjustments), writes callback QWORD+38, DWORD+40 and context QWORD+48, and calls a nonNULL callback synchronously with event0. Normal ABI/private stack, valid storage and non-overlap/canonical memory-fill premises remain explicit.
- Complete `2973E0` has four direct helper calls (`271960`, `272730`, `2726C0`, `2727C0`) and no indirect or direct handler call. Own nonstack writes affect viewWORD+14, DWORD+50 and RMW WORD+26. H3 is refuted for this local body. Transitive helper callbacks/effects are not excluded.

The already-known `3F8980` event1 dispatcher ABI and canonical handler descriptions connect the synchronous callback boundary conditionally. Prior EXP243 has **zero** `3F8980` hits in its BSS-zero fixture; it is not a detection control for initialized callbacks, and none of its executions are credited to ASTRA here.

## Controls and limits

`prove-01` succeeds on the original inputs. Four synthetic source mutations reject changed handler identity, matched-row reinitialization, callback-field destination and a direct handler call. Three actual producer CLI controls reject incomplete target metadata, incomplete target wrapper and failed target capture, without producing a result. The existing positive is reused, not repeated for counts. Review `result-01.json`, `control-result-01.json`, raw source maps and receipts.

Prepared handler metadata and an unrun handler capture driver are retained as preparation only; their known semantics were consumed from the canonical page instead of duplicated. No natural initialized callback value, lifetime/reuse guarantee, scheduling, resource-binding preservation, transitive helper no-write/no-callback claim or visible presentation is established. The normal-return/local-state premises do not prove natural reachability.

## Canonical consumption

FABLE: qualify the opposite direct-call edge on the residual renderer page and OV42's callback-window premise. Keep transitive uncertainty and actual field-state separate. OPUS: consume conditional callback/context layout and matched-record preservation; do not make constructor callbacks a universal invariant. SPEC: independently inspect original bytes, actual input gates, per-path proof and controls. Producer validity and manifest integrity are not independent acceptance.

Menu setup budget remains spent/unapproved, EXP127 INVALID_POST_TRACE/crash cause UNKNOWN, K14 accepted and closed. No save/config/reference/peer changes; finite owned helpers are terminal. Full L1+L2/M0-M5 goal remains ACTIVE/NOT_MET.
