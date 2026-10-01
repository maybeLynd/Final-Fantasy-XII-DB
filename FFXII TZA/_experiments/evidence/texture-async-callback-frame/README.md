# Queued bank reaches a transient callback frame

Method A RETAINED STATIC_ONLY. Producer checked; independent/canonical acceptance
pending. Reuses FABLE's published BG11 answer7e4af33d5 and ASTRA's retained source
confirmation, rather than recapturing or repeating that closed question. Original
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. New composition with bank-dispatch e2506a55e2e59cbe2a111eed7a79ea57888f5338
supplies the local ABI connection that packet correctly left unproved.

Original60A410's opcode2F arm at60A899 reads raw command callback+8 and data+10.
It builds a24B stack frame: field0=executorR14, field8=&stackSlot[rsp+50],
field10=QWORD command+10. At60A8D6 it invokes the callback with RCX=&frame,
NOT the raw128B command. Optional60B750 flush before construction remains an
opaque normally returning/native-ABI boundary; no native effects inferred.

For185A50->5FEA50->186610, command+10 contains the pre-submission DWORD bank
zero-extended throughR8D.186610 reads DWORD frame+10 intoEDX and freshly loads
global context1F7F5B8 intoRCX before tailing62EBC0. It therefore selects the
queued bank, not current bank-global1F7F590 at callback time. Context is current,
bank is captured. This is conditional original-code dataflow, not actual live
scheduling, pointer identity/stability/lifetime or thread/event observation.

Normal callback return resumes at60A8D9, jumps to128B source/biased-cursor
advance and compares the end before next dispatch. This local order does not
prove synchronous completion with the submitting caller, frame frequency,
initialized producer/consumer storage or a safe context change. A transient
stack frame is not a persistent portable object. Counter38 writers/drain,
natural pending work, all-bank cancellation and native graphics effects remain
OPEN. We do not close a wholeOV row or recount the already-retired BG11 request.

Reproduce using existing analysis Python and fresh output:

    python <packet>/prove-texture-async-callback-frame.py <fresh.json>

The checker verifies exact retained shipping ranges and actual reviewed access
roles/byte decoding, original two-level dispatch table bytes and concrete frame/
callback operations. It qualifies the actual bank producer's exit/result/source
preimages. The retained BG11 capture is focused source, not the newer wrapper
schema. First positive01 refused that schema mismatch before any result; original
driver and failed invocation retained. The fix qualifies the actual focused
bytes/roles/identity and preserves the narrower branch scope; it does not alter
raw input or declare the full interpreter/exception paths certified. It also
uses the existing validator's real ROOT interface. Positive02 is valid.

Four actual producer CLI refusals reuse positive02: consistently moved frame
data load, consistently narrowed bank read, missing frame store and failed bank
producer exit. All require nonzero exit, expected error and absent result.
Default freezer requires actual successful producer/control invocation receipts
and current immutable driver/input/result hashes. Empty stderr is normal; absent
positive stdout is not. Producer controls are not independent acceptance.

Return this additive ABI result through the existing bank-dispatch SPEC/OPUS/
FABLE tasks, not duplicate their census or edit their claimed consumers. OPUS
needs separate128B command/24B callback-frame types and bank/context read times;
FABLE needs the captured-bank/current-context traversal/scheduling premises.
Next: selected original submit/flush/drain caller ordering or element38 writer
closure if still needed/unowned, before considering real-process scheduling.

Player version: a queued texture update remembers which work bank it belongs
to, even after the game advances its current bank. The callback fetches its
scheduler context later, so context lifetime is still an unresolved requirement.

Cleanup: finite offline reducer and disposable control files; no new capture,
native/emulated/live execution or PC/game/input/instrument/save/config/reference/
unrelated-process mutation. Menu spent/unapproved, EXP127 invalid, K14 accepted;
fullL1+L2 goal ACTIVE/NOT_MET. Publication/review waits block only their consumers.
