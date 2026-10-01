# Conditional renderer initializer command routing

ASTRA/SOL, 2026-10-01. Method A; producer checked, independent review pending.
Exact shipping EXE73461d08...21f8. No native/emulated/game execution.

The exact selected question is **which local target and arguments** the
post-index initialization command uses when the renderer getter is null
versus nonnull. This narrows the initial "merely stage or execute" question:
an indirect method call is not proof of command execution or its effects.

Retained original186CD0 writes CB8zero then calls1F16C0 with loaded values
`RCX=[renderer+B10]`, `RDX=[renderer+B58]`. Under a valid normally returning
arena allocation,1F16C0 constructs a24B902F28 command with those values at
8/10, stages it at01F82EB0+8 and calls1FB840. That helper promotes8->0 and
tails the command's physical slot0. It is original16D6A0, **3-byte RET0**
(`c20000`), with no conditional gate or command-body effect under that
unmodified identity. It is shipping code, not a substitute stub. No
meaningful return-value contract is invented.

1F16C0 then tails1FB830, which passes node0 command inRDX and CURRENT
`[01F7F4D0]` target inRCX to1A1850. The submission reads the renderer global
01F7F598 through189120. It receives no renderer object argument from the
initializer. Its two local branches differ:

- First getter null: the original incoming target is retained inRBX.
  RCX becomes **qword `[target+8]`**, RDX becomes the retained command,
  R8D becomes40h.1A190E calls that receiver's vtable slot0.
- First getter nonnull: it allocates28h and calls1F4950(command,R8D0), then
  calls the returned wrapper's vtable slot8 withRDX loaded from the
  **second independently read** renderer's+8. Valid backed construction
  and a nonnull second read are premises, not outcomes proven here.

Neither branch by itself certifies actual command execution, a GPU effect,
accepted submission, safe allocation, native target identity or lifetime.
Two getter reads are not one atomic snapshot. Existing BG9/BG11/callback
frame evidence and reviews remain separate; none of their censuses was
repeated or counted as a new test here.

189000 publishes the renderer after184F20 normally returns. Therefore,
**if no intervening opaque/interfering publication supplies the global**
before this post-index submission, it selects the null-renderer branch.
Publication order alone does not prove that natural state universally;
earlier opaque calls, all writers, alias effects and scheduling remain
open. The original initialized process and final CB8/bank preservation
are not established by this selected call boundary.

Five new original spans384B and physical16B table are captured. Three exact
pdata normal roots and two terminating leaves are bound;1A1850's unwind
handler behavior is outside this normal-path proof. Retained getter and
initializer source were reused, not recaptured. Shared reviewed roles are
used by the actual capture and source re-decoder.

First capture01 refused **before any source output**: an unverified
one-byte RET encoding guess was wrong. The original leaf is3B RET0. Old
driver/exit/stderr remain, capture02 uses the verified full leaf. This
correction changes encoding/extent, not a fabricated native gate.
The semantic reducer requires successful capture exit and exact
source/driver hashes. Its positive and four actual synthetic CLI refusals
(upstream fail, reversed null branch, missing retained getter, changed
physical prepare slot) are retained. They are producer controls, not
native runs or independent acceptance.

Reproduce semantic reduction with retained source and a fresh result:
`python prove-renderer-init-command-routing.py SOURCE_DIRECTORY CAPTURE_STATUS FRESH_RESULT`.
Use a fresh output directory for the control CLI. Capture reruns use the
existing repository working depth and pinned reference/dependencies;
never overwrite recorded files. Missing evidence is not valid empty output.

Required consumers after independent acceptance: FABLE's original renderer
initialization/command lifecycle, OPUS's selected argument/prepare/submission
contracts. Preserve loaded values versus objects, current global reads,
conditional prepublication null route and opaque native effects. Producer
validity, independent review and canonical incorporation remain distinct.

Full L1+L2/M0-M5 goal ACTIVE/NOT_MET. No wholeRT/OV row retired. No game/PC,
native/emulated run, instruments, save/config/reference or peer mutation.
Menu extension remains spent/unapproved; EXP127 remains invalid. Own
bounded scripts terminal. Continue the next exact unblocked obligation.
