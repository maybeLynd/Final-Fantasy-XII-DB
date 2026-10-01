---
experiment: EXP-080
title: Older-format manual save from fresh title through Load complete into Southgate
status: COMPLETE
contract: none — bounded initialized save/load evidence; L-13 and the full same-session request remain open
tool: evidence/spawn-live-load/observe.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-13
date_run: 2026-09-13
---

# EXP-080 — the older save restores battle state before the load popup is dismissed

**Player version:** the preserved older save loaded Southgate and restored six
level21 character records. Its gambit bank0 records match the compatibility data.
It did not simply retain the title screen's existing battle state.

Method **C** was required for initialized binding and ordinary load. The selected
test file declares decoded length`0x4E690` and matches the existing EXP015 backup.
The exact reference game, PID46768, was observed at fresh title, at **Load complete**
before dismissing it, and in Southgate after dismissal. Two read-only samples per
state passed exact executable/text, module, known-byte, rejected-null and complete
read controls; all read handles closed. No hook, memory write, native call or
debugger attachment was used. An initial sandbox module-list failure remains
INVALID and was excluded; supported read access resolved it with the same tool.

[Raw evidence, normalized observation, source identities and limits](evidence/spawn-live-load/README.md)
record the results. At Load complete the first six stats records had changed
from1,1,1,1,2,1 to all21, the pre-gambit block prefix matched the compatibility
prefix, and all40 bank0 records matched the older per-record sets. Field history
and parity changed only in the later field capture; no call trace attributes
every intervening operation. All-zero keep banks make copying/wiping/retention
indistinguishable in this run. Selector indices were already zero at title.

The **bounded experiment is complete; the broader request is not**. Current-save
positive comparison, same-session current-to-old loading, visible gambit/inventory
menus, nonzero persistence and enemy respawn consequences remain open. Mouse
navigation/confirm worked; the attempted game keyboard bindings produced no
observed response, so keyboard-dependent setup was not expanded blindly.

FF12 exited through its normal dialog. Only LUIDLow in the working settings had
changed; the changed copy was preserved and all26 original save/config hashes
restored. PC control was released when unused and after exit. Existing live
authorization is active; a new user stop or takeover suspends it again.
