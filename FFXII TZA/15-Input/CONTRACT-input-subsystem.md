---
contract: Input subsystem — the published frame snapshot, the arbitration point, and the capability gate
category: 15-Input
scope: subsystem
level: L2
readiness: CONTRACT READY   # the ordering and the shared object are STATIC; no live capture of the frame order
confidence: PROVEN
implements:
  - Input-Stack/input-stack-device-channel-and-bindings.md
  - Binding-Profiles/binding-profiles-remapping-and-control-state.md
  - Input-Name-Registry/the-input-name-registry-and-channel-aliases.md
  - Gameplay-Capability-Policy/capability-inhibition-policy.md
entries: [002498B0, 00253C70, 002284F0, 00314020, 0022B8C0, 00254B50, 0017DE10, 002E0FA0, 00313A00]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: read from the authority image in this session (2026-09-21, FABLE) - every call site, store
    site and loop bound below was disassembled from that file, not carried from a page. The
    image-wide reference sweep in section 6 is `Database/Tools/work/FABLE/pub140-scratch/ripband.py`
    over the band `02F97360`..`02F9739C`, run with two hand-read control sites planted in it.
last_reviewed: 2026-09-29
falsification_passes: 0
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-input-subsystem-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the input subsystem (FABLE)

> **This contract exists because S-35's two existing contracts are narrower than S-35.**
> [`CONTRACT-binding-profiles.md`](Binding-Profiles/CONTRACT-binding-profiles.md) is `scope: subsystem`
> over binding profiles; [`CONTRACT-input-name-registry.md`](Input-Name-Registry/CONTRACT-input-name-registry.md)
> is `scope: operation` over one name registration. S-35 is **the input stack, binding profiles *and*
> the capability policy**, and its [L2 verdict](../_index/L2-VERDICTS.md) records the binding gap as
> **COVERAGE, not evidence** — "adding evidence cannot fix this row, only an artifact covering the
> rest of the subsystem can."
>
> The governing test is SWE2-FRONTIER's ruling on `OPUS-REQ-FRONTIER-TWENTY-TWO-SYSTEMS-LACK-A-SUBSYSTEM-SCOPED-CONTRACT`:
> **a narrower contract is adequate exactly when the system's operations have no cross-operation
> invariant or ordering the narrower contract leaves unstated.** This document answers that test for
> S-35 by stating six such invariants, and it deliberately **restates none** of what the two narrower
> contracts already specify — no binding record layout, no keymap format, no name-registry ABI.

## 1. What this contract covers

One thing: **the object the three operations of S-35 share, and the order in which they touch it
within one frame.**

The three operations are separate in the database and were separate in the evidence. When this
session intersected the code addresses cited by the four `15-Input` L1 pages, the capability page
shared **zero** function addresses with the input-stack page and **zero** with the binding-profiles
page. That is not because the mechanisms are disjoint. It is because **the body where they meet is
cited on only one of them**, and the shared datum is named on neither.

## 2. The shared object

**`02F97360` .. `02F9739B` — the published gameplay input snapshot, 0x3C bytes.**

Its field map is already established and is **not** restated here; see
[the Config screen](../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) §6
(`DI-2`, answered 2026-09-14) and
[the input stack](Input-Stack/input-stack-device-channel-and-bindings.md) §2, which give the
history-field-to-slot mapping and the eight mask offsets. What matters here is only the role of four
words of it, because the invariants below are about *who writes them and when*:

| word | contents | who clears it |
|---|---|---|
| `02F97368` | held | the frame-wide clear; `002A3250` writes it by name |
| `02F9736A` | **newly pressed** (an edge word) | the frame-wide clear, and **`00253C70` by name, after acting** |
| `02F9736C` | repeat-filter "fires this frame" | the frame-wide clear only — **no instruction writes it by name** |
| `02F9736E` | released | the frame-wide clear only |

> **"The frame-wide clear" is two bodies and eight stores, not a per-word write.** Both `002498B0`
> (`002498BD`-`002498EE`) and `002284F0` (`00228605`-`00228636`) zero the band with **eight stores
> anchored at `02F97360`, `68`, `70`, `78`, `80`, `88`, `90` and `98`**. A word like `02F9736A` or
> `02F9736C` is therefore cleared *inside* the qword store at `02F97368` and has no store of its own
> — which is why the per-displacement counts in §6 credit the anchor, and why the distinction
> between "cleared by the frame" and "written by name" is the one that matters here.

## 3. The frame ordering

Two fixed points in the main loop, and two more inside the second of them. All four are direct calls
at constant sites; none is a vtable slot, so the order is a property of the image and not of any
object graph.

```
MainLoop_UpdateAndRenderFrame            0022B8C0
  0022B908  call 002498B0   InputGameplay_RebuildFrameSnapshotFromChannelHistory
            |  zeroes 02F97360..02F97398 (eight stores, 002498BD-002498EE)
            |  then ORs the channel history's eight mask fields back in (00249940-002499AC)
  …
  0022BA23  call 00314020   World_UpdateSimulationTick
            |
            |  r13d = 0 (003140D9); r14d = the tick's mode argument (00314042)
            |
            |  mode 1 (battle):  ebx = 3; while (ebx < 5) { 00234590(ebx); …; ebx++ }   00314114-00314135
            |                    then, once:                 002E0D90 -> 00253C50       00314137
            |  mode 0 (field):   ebx = 0; while (ebx < 5) { 00234590(ebx); …; ebx++ }   003141C0-003141EC
            |                    then, once:                 002E0D90 -> 00253C50       003141F2
            |
            |  each 00234590 iteration calls 00313A00 at 00234624  (reconcile capability row 2)
            |  00253C50 calls 00253C70 at 00253C56              (arbitrate)
  …
```

**The reconcile-then-arbitrate order is not incidental.** In both arms the reconciler runs inside a
loop and the arbiter runs **once, after the loop has finished for every slot it iterated**. There is
no path in `00314020` on which the arbiter precedes the reconciler.

> **Two branches in the field arm are folded dead, and the loop is denser than it looks because of
> it.** `esi` is loaded from `r13d` at `003141BA`, and `r13d` was zeroed at `003140D9` and never
> written again, so `003141C5 je` always takes and the per-slot gate `00267310` at `003141C9` is
> **never reached from this body** — every slot 0..4 reaches the orchestrator. The same constant
> makes `003141F0 jne` never take, so the arbiter always runs. Stated because a reader who assumes
> the gate is live would conclude the reconciler is conditional; it is not, here.

## 4. The arbitration point

`00253C70` `InputGameplay_ArbitrateDigitalInputAndModalState` (1,599 B) is **the only body in the
image that reads both halves of S-35**. It has exactly one caller (`00253C50`, itself reached only
through the 5-byte thunk `002E0D90`), so it runs exactly once per tick.

| it reads | at | which half |
|---|---|---|
| the capability aggregate `002E0FA0` | `00253D2E`, `00253FF2` | capability policy |
| the snapshot's edge word `02F9736A` | through `002501A0`, `00250200` | input stack |
| the snapshot's filtered word `02F97392` | through `00250130`, `00250200` | input stack |
| the snapshot's held word `02F97360` | `0025420A` (`test …, 0x200`) | input stack |
| a live binding query | `002541D4` -> `0017DE10` | binding profiles |
| the field-record permission bit `00377C20` | `00254067` | capability policy's input |

| it writes | at | effect |
|---|---|---|
| `02F9736A` <- 0 | `00253F70`, `00253FE9`, `002540C5`, `0025415F`, `002541BC` | **consumes the press** |
| the UI request router `00254B50` | `002540D2`, `002541C7` | raises the request the press asked for |

> **The clears really are clears.** `edi` is zeroed at `00253D12` and written again in only three
> places in the body — `00254049` (`mov edi, eax`) and `00254189`/`002541F9` (`setne`/`sete dil`) —
> and each of those three reaches an unconditional transfer to the epilogue **within one
> instruction** — `0025404B mov eax, edi` / `0025404D jmp 0x25425F`, `0025418D mov ecx, edi` /
> `0025418F jmp 0x254256`, and `002541FD mov [020927E0], edi` / `00254203 jmp 0x254249`. No path from
> any of them reaches a `mov word ptr [02F9736A], di`. So `di` is 0 at all five stores.

**The binding query at `002541D4` is a live read, not a cached one.** `0017DE10` (67 B) fetches the
application singleton (`00796E20`), takes the device bank from its field `+0xDF8`, gets the input
manager (`00198790`), resolves a slot through `00197710` — **an entry of
[`CONTRACT-binding-profiles`](Binding-Profiles/CONTRACT-binding-profiles.md) §2, "read a slot on
demand"** — and asks `0079E6A0` whether that control code is active on that bank. Binding state is
therefore consulted **at arbitration time**, after the snapshot for this frame was already built.

## 5. The invariants

Each is stated with the observation that would falsify it.

**I-1 — Publication precedes arbitration.**
`002498B0` runs at `0022B908`; `00253C70` runs inside the call at `0022BA23`. Anything reading the
snapshot before `0022B908` in a frame reads the previous frame's snapshot.
*Falsified by:* an arbitration path that does not run under `0022BA23`, or a second publication of
the snapshot between the two sites.

> **CORRECTED 2026-09-21 (FABLE) on `AUDITSEM-CONTRA-FABLE-INPUTSUB-2498B0-CALLERS` — I wrote that
> `002498B0` has "exactly one direct caller" and it has four sites, and the correction strengthens
> the invariant rather than weakening it.** SWE2-AUDIT-SEM's per-function scan over all 38,161
> bodies found **three `call` sites** — `0022A770`, `0022B8C0` (at `0022B908`, as stated) and
> `0022BC20` — and a re-run here adds a **fourth by tail-jump**, `00249C30` at `00249C4D`, which a
> call-only census does not see.
>
> **All four hang off one frame dispatcher, `0022A580`, and its arms are ALTERNATIVES, not a
> sequence.** `0022A685` reads a byte at `02064AD3`, `cmp eax, 6` / `ja` takes the default arm at
> `0022A6D9`, and otherwise `0022A6A3 jmp rcx` enters one of six table arms — **every arm ending
> `jmp 0022A6DE`**, so exactly one runs per dispatch. Seven arms, of which four reach the rebuilder:
> `0022A6A5` (a frame mode whose body is not cited here — it carries an RNG edge this contract does
> not assert) reaching the gated `00249C30`; `0022A6B3` → `0022B8C0`; `0022A6BA` → `0022BC20`;
> and the default `0022A6D9` → `0022A770`.
> **The three frame bodies each publish and then tick** — `0022BC20` runs the same three-step
> prologue as the main loop (`0035FF90`, `0036FDF0`, then `002498B0` at `0022BC50`) and calls
> `00314020` at `0022BCCF`. **So the ordering in §3 is not a property of one frame body; it holds on
> every frame path in the image.**
>
> **And the one site that could have falsified I-1 does not.** `00249C30` is a *conditional
> republication*: it reads `0209273C`, and only when `(v - 2) & 0xFFFFFFFD == 0` — `v == 0` or
> `v == 2` — does it run `0035FF90` and tail-jump into the rebuilder. **It is reached on the
> `0022A6A5` arm, which runs INSTEAD of the frame bodies and not before them** — on that dispatch
> `0022B8C0` does not execute at all, and `0022B908` and `0022BA23` are both inside it. So the
> republication cannot interleave with the window for a stronger reason than adjacency: *the window
> does not exist on the pass that republishes.* **The falsifier was the right one to name; it is not
> triggered.**
>
> *Mechanism corrected 2026-09-21 (FABLE) on `AUDITSEM-NOTE-FABLE-2498B0-ARM-IS-EXCLUSIVE-NOT-PRIOR`
> — the second correction to this clause in an hour, and the same mistake twice running: I read the
> arm call sites in **address order** and called that a sequence, exactly as I had read `002498B0`
> once in a listing and called that a caller count. **Both times the instrument that would have
> settled it was one command away.** The conclusion has survived both corrections; the reasoning
> under it has been wrong twice.*
>
> **What I actually did wrong** is worth stating, because the instrument was available: I read the
> main loop's disassembly, saw `002498B0` once, and wrote an absence claim from it **without running
> the caller scan** — on the same day I twice insisted elsewhere that a zero has to be measured.
> Indirect dispatch into either body is still not excluded — `GG-2`, §8.

**I-2 — Reconciliation precedes arbitration, and the aggregate the arbiter reads is the *last*
slot's.**
`00313A00` runs once per iteration of the `00234590` loop; the arbiter runs after the loop exits. The
aggregate at `00253D2E` therefore reflects capability row 2 **as left by slot 4**, not by the party
leader and not by any per-slot value.
*Falsified by:* any path in `00314020` reaching `002E0D90` before the loop, or a row-2 write between
the loop's exit and `00253C70`.

**I-3 — `02F9736A` is a destructive read with a single consumer.**
Image-wide, **51 functions read `02F9736A` and exactly one writes it by name: the arbiter** — ~~the
only other way it changes is the frame-wide clear that opens each rebuild (§6, §6a).~~ **three wide stores also
clear it** *(corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS's note; `002A329B`, `00228605`–`00228636` and `002498BD`–`002498EE` re-read)*:
- the frame-wide clear that opens each rebuild (`002498B0`, §6, §6a);
- the I-5 swallow, the same eight-store wipe of `02F97360`–`02F97398` in the message-2 arm of `002284F0` (§8, GG-3);
- the window-open wipe, one qword store of 0 at `02F97368` (`002A329B` in `002A3250`), which takes `+2` with it.

None of the three sets a bit, so all of them only lose presses. A press is still acted on at most once. A press is
therefore acted on at most once, and every other consumer of that word in the same frame sees it only
if it runs **before** the arbiter. This is the mechanism behind the already-recorded behaviour that
[Config-screen](../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) rows step
once per press while the Brightness row — which reads `02F9736C`, a word **no instruction writes by
name** — keeps stepping while the stick is held.
*Falsified by:* a second by-name writer of `02F9736A` anywhere in the image, or a register-based one
that §6a's bound does not exclude.

**I-4 — Capability inhibition is applied at arbitration and routing, never at publication.**
`002498B0` builds the snapshot unconditionally; it never calls `002E0FA0`. Inhibition happens only
downstream, at `00253C70` and at `00254500` -> `00254B50`. **"No input" and "inhibited input" are
therefore distinguishable states**, and every consumer that reads the snapshot without consulting the
policy sees the press regardless of whether the game will act on it.
*Falsified by:* a policy read inside `002498B0` or inside the poll/builder chain.

**I-5 — A modal window may erase the whole published snapshot mid-frame, and the button that does it
is the configured Cancel.**
`002284F0` (439 B) is a message handler — it switches on `[rdx]`, has **no direct caller**, and its
default arm tail-jumps to `005C5230`. On message id 2, if the channel-0 held mask equals the word at
`01E0C2A4`, it performs **the same eight-store zeroing of `02F97360`..`02F97398`** that the rebuilder
performs (`00228605`-`00228636`), and continues. That is a hard "swallow every input this frame"
gate, applied to shared state, reached only through a ~~vtable~~ widget's handler slot. *(Refined 2026-09-25, FABLE,
Claude Opus 5.5, with GG-3's answer.)* The slot is `obj+0` of the singleton `01FD4948`, and the caller is the
generation walker `00248030`, which sends message 2 only while the widget's bit 18 is clear (§8, GG-3). The arm
also has a precondition that the sentence above omits: `[[0209AC30] + 0x308] != 0` (`002285D1`–`002285E0`). The
compared value is `0035EF10(0, 0)` (`002285EF`–`002285FD`).

> **`01E0C2A4` is not a fixed button.** It is the DecideButton setting's *other* face button — the
> pair is `01E0C2A0` = confirm and `01E0C2A4` = cancel, and the two swap with the setting
> (`Circle` -> `2000`/`4000`, `Cross` -> `4000`/`2000`); see
> [the UI request router](../16-UI/Request-Router/ui-request-router.md) §4, which derived the pair.
> So the swallow is **"cancel is held"**, and the same pair is what the arbiter itself tests at
> `00253D4F`, `002540DC` and `00254194` — **the input subsystem's own button tests are
> setting-relative, which is a binding-profile fact reaching into arbitration**, and the fourth place
> the three operations touch.

*Falsified by:* showing the arm is unreachable, or that the `01E0C2A0`/`01E0C2A4` pair is not the
configured confirm/cancel masks.

**I-6 — The aggregate is a reduction, so no single owner can clear a capability.**
`002E0FA0` OR-reduces 16 u32 rows and clears only effective bit 19, conditionally
([the capability page](Gameplay-Capability-Policy/capability-inhibition-policy.md), "Re-verification
2026-09-02 (AH-10)", has the 64-byte derivation over `0215F1C0`-`0215F1FF`). **Any one row can inhibit; no row can permit.** A reimplementation that lets a
subsystem "release" a capability by writing its own row to 0 will still be inhibited by any other row
holding the bit.
*Falsified by:* an AND or a priority order in `002E0FA0`.

## 6. The measured population of the shared object

Image-wide rip-relative sweep of `02F97360`..`02F9739C`, read/write split, **221 references from 74
functions**. The rows that carry the invariants:

Counts are **per displacement**, so a word cleared inside a qword store is credited to that store's
anchor, not to itself (§2).

| word | readers | writers **at that displacement** |
|---|---:|---|
| `02F97360` held (ch.0 word 0) | 3 | `002498B0`, `002284F0` — the two frame-wide clears |
| `02F97368` held | 22 | `002498B0`, `002284F0`, `002A3250` — the window-open reconfigure, unconditional at entry (§8, GG-4) |
| **`02F9736A` newly pressed** | **51** | **`00253C70` — and nothing else at this displacement**; cleared inside the qword stores of `002498B0`, `002284F0` and `002A3250` (I-3, corrected 2026-09-25) |
| `02F9736C` repeat | 27 | **none** |
| `02F9736E` released | 2 | **none** |
| `02F97392` | 12 | `002498B0` |

**The arbiter is the only body that writes `02F9736A` by name.** The rebuilder reaches the word twice
— once inside the qword clear at `02F97368`, once through `rbx`, which it loads with
`lea rbx, [02F97372]` at `0024990A` and then stores the history masks relative to. That second form
is invisible to a rip-relative sweep, so the sweep's blindness had to be **bounded rather than
assumed away**.

### 6a. The sweep is rip-relative, and its blind spot is closed rather than assumed

A second instrument, `leaband.py`, asks the two questions a rip-relative sweep cannot answer — **who
takes the address of a cell in the band, and is a pointer into it stored anywhere in the image?**

- **Three functions take a `lea` into the band, all three in the rebuilder's own family:**
  `002498B0` itself (`rbx = 02F97372`, the control this instrument had to find), and the two
  five-instruction indexed readers `00249860` and `00249880`, which return
  `byte[02F97370 + 20·index]` and `byte[02F97371 + 20·index]`. Both are reads, both are called from
  the single body `001EC060`, and for a non-negative index neither can reach `02F97368`..`02F9736E`.
- **Zero absolute qword pointers into the band exist anywhere in the image** (every 8-aligned qword
  scanned).

So no body outside those three can reach the snapshot except rip-relatively, and the §6 population
is complete for the four transition words up to two enumerated readers. **That is what makes I-3 a
statement about the image and not about one instrument's reach.**

> **Instrument note.** The sweep classifies a reference as a write only when the mnemonic writes and
> the **first** operand contains `rip`; capstone renders a memory destination with its size prefix
> (`mov word ptr [rip + 0x…], di`), so a `startswith("[")` test would have reported **zero writers**
> for every row. Two hand-read sites were planted in the input as controls — `002498BD` (rebuilder
> store) and `00253F70` (arbiter store) — and both came back classified `W`.

## 7. What a reimplementation must not do

1. **Do not arbitrate before reconciling.** The refusals will be one tick stale, which is visible
   exactly at the transitions the policy exists to cover (a menu opening on the frame an action
   commits).
2. **Do not treat `02F9736A` as level state.** It is cleared by its consumer. Polling it from a
   second consumer after arbitration yields 0 forever.
3. **Do not apply inhibition when building the snapshot.** I-4. Suppressing at publication collapses
   "not pressed" into "pressed but refused", and the consumers that distinguish them are the ones
   that drive UI feedback.
4. **Do not cache the binding lookup into the snapshot.** I-4's counterpart: `0017DE10` re-resolves
   the bank from the application singleton at arbitration time.
5. **Do not give each subsystem its own capability flag.** I-6 — the reduction is the contract.

## 8. What this contract does NOT establish

Registered as `GG-1` .. `GG-4` in [OPEN-QUESTIONS](../_index/OPEN-QUESTIONS.md), in the commit that
publishes this contract.

- **`GG-1` — where the snapshot's 51 readers sit relative to the arbiter in the frame.** They are
  reached through vtables and jump tables, not direct calls, so the direct-call order in §3 does not
  place them. I-3 states the *consequence* of the ordering, not the ordering for each reader. Placing
  them needs either an indirect-dispatch resolution pass or a live capture — **routed to ASTRA**.
  ***Narrowed 2026-09-28 (FABLE, on `FABLE-REQ-CONTRACT-GG1-STATIC-ORDER`; verified and transcribed
  by SWE2-CONTRACT):*** **one reader is now statically ordered per frame kind** — the battle
  command menu's read of `02F9736A` at `00277ACD`, in the widget proc's focus-input arm (messages
  10/11, all sent through `002481C0`). In the full-menu and capture frames (`0022B8C0`/`0022BC20`)
  the static order is snapshot rebuild < world tick (reaches the arbiter) < UI pass — **focus input
  always arrives after the arbiter**. In the field frame (`0022A770`): rebuild < pause step (after
  which the frame can end without a tick) < `002507C0(1)` at `0022AB83` < world tick at `0022ABD8`
  < `002507C0(1)` at `0022AC17` — **a delivery can precede the arbiter** whenever the `0022AB83`
  gates pass: bit 3 of `022C7F92` *and* an **ordered float equality** `ucomiss xmm0, xmm7` on the
  `02064AC0` accumulator (`0022AB79`, then `jp`+`jne` both skip to `0022AB90` — send iff PF=0 and
  ZF=1). It is not a bit test: +0.0 and −0.0 both pass, a NaN fails the `jp`, and with MXCSR.DAZ
  set a nonzero subnormal compares equal to zero; the game's MXCSR and the accumulator's live
  values are unobserved (qualified 2026-09-28 on `ASTRA-RETURN-CONTRACT-FIELD-FOCUS-FLOAT-GATE` /
  `FABLE-REQ-CONTRACT-GG1-GATE-DOMAIN`; `check.py` PASS_STATIC_GATE). The post-arbiter send needs
  bit 3 alone. Still open: the other 50 readers, whether the proc is also reached through the
  arbiter's own callees, and the gates' live values. Record:
  [`_index/candidates/gg1-static-order/`](../_index/candidates/gg1-static-order/README.md)
  (`gg1_order.py` O1–O6 + control, FAILS 0).
- **`GG-2` — whether `002498B0` is ever entered indirectly.** Its direct sites are now **measured**:
  three `call`s and one tail-`jmp`, all under the dispatcher `0022A580` (I-1's note). What remains is
  the indirect half — a `0` from the direct-call graph is not an absence claim
  ([ABSENCE-CLAIM-GATE](../_index/ABSENCE-CLAIM-GATE.md)). *Narrowed 2026-09-21 (FABLE) on
  SWE2-AUDIT-SEM's contradiction.*
  ***ANSWERED 2026-09-24 (SWE2-CONTRACT): never — the four enumerated routes are exhaustive.***
  Whole-image sweep over every section: **no stored pointer** to `002498B0` (qword or dword,
  `.text`/`.rdata`/`.data`/`_RDATA` and every other section — it sits in no vtable, jump table,
  or callback cell); **no `lea` materialisation** anywhere, so no runtime cell can be populated
  with it either; **no `FF /2`/`FF /4` rip-indirect site** references a cell holding it; **no
  `0F 8x` conditional jump** targets it. The complete route set is exactly the four I-1's note
  lists — `call` at `0022A7F6` (`0022A770`), `0022B908` (`0022B8C0`), `0022BC50` (`0022BC20`),
  tail-`jmp` at `00249C4D` (`00249C30`, verified: `E9` rel32) — all mutually exclusive per frame
  under `0022A580`'s mode dispatch. I-1's "single publication point per frame" is therefore an
  exhaustive static fact, not a direct-graph zero.
- **`GG-3` — the owning class of `002284F0` and what sends it message id 2.** The arm and its effect
  were read; the sender was not.
  ***ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5, as this contract's owning editor), from two sources.***
  **The owner is SWE2-CONTRACT's finding of 2026-09-24, re-checked here.** `002284F0` has no class of its own. It
  is the `obj+0` handler of the lazily created singleton widget `01FD4948`. Its address is taken once, at
  `002284C0` inside the accessor `00228490`, which builds the `0xD0`-byte widget through the factory `00244F50`
  when `[01FD4948]` is zero. `00228490`'s only caller is `002283AE` inside `00228380`, which the arbiter reaches
  at `00253CC3`. The widget is the pause menu's cancel-to-close guard ([the widget protocol page](../16-UI/Widget-Object-Model/the-widget-message-protocol.md) §2a, `58a87a9d8`).
  **The sender, from original-code replay, bounded ([the widget protocol page](../16-UI/Widget-Object-Model/the-widget-message-protocol.md) §2a, `7859420a5`).** Message 2 comes from the
  framework's generation walker `00248030`, which has 13 raw call sites: `0022865C` in `002284F0` itself and
  twelve in `00250540`–`002508E0`. For each stale node (bit 17 differs from the parity global `0208ED5C`):
  - It calls `[node]` with `rdx = 00915108` = `{2, 0, 0}` **only when widget-flags bit 18 is CLEAR**. The
    `bt ecx, 0x12` / `jb` at `002480E1`–`002480E5` tests the flags word just stored to `+0x40`, and skips the
    call when the bit is **set**.
  - It then rewrites bit **17** from the parity: the `and` at `00248101` with mask `0xFFFDFFFF`, then the
    re-stamp at `00248108`–`00248110`. After a call, the parity is re-read from `0208ED5C` at `002480FB`; a
    suppressed node skips that reload.
  - It never writes bit 18.
  - It still walks a suppressed node's children, and they receive message 2.

  The replay ran the unmodified 339-byte body under observation-stub handlers. The `jb → jae` mutant and a nopped
  reload both fail its case assertions.
  **Scope.** What is established is the walker's polarity, its record, its bit rewrites and its subtree
  behaviour, on planted trees with observer callbacks. The route to the singleton is static: message 1 attaches it
  as the last child of the root `[0208EA48]`, and `00250540` walks that root in both arms, paused or not.
  **Not established:** the real handler's behaviour inside a live widget tree, and which frames reach the walk in
  play.
  *History: a pending draft of this answer (SWE2-CONTRACT, 2026-09-24, never published) said that bit 18 gates the
  call, that the `and` clears bit 18, and that the record is `00915058`. That record is `{15, 0, 0}`, the destroy
  notice. The replay above supersedes the draft; the owner half of the draft is kept, with credit.*
- **`GG-4` — the third writer of the held word, `002A3250`.** Found by the §6 sweep, not read.
  ***Read 2026-09-23 (SWE2-CONTRACT): a level clear, not an edge consume — the held word is dropped
  when the message-window opener takes its `+0x40 == 0xFF` arm.*** `002A3250` stores `qword [02F97368] = 0`
  unconditionally at `002A329B`, at the head of the body before any branch — the same one-store wipe
  the rebuilder performs, and by the §6 mechanism it takes `02F9736A`/`6C`/`6E` with it. Its chain:
  it is reached only through `002A35B0`, a setter thunk that installs `[win+0x1A8]` (the caller's
  `r9`, defaulted via `0039C480`) and tail-jumps in; `002A35B0` is called at `002E1933` inside
  `002E16B0`, the **message-window opener** (the body whose first act is
  `PersistentFlag_SetBank2048(actor word +0x102, 1)` — marking the NPC's name as known), on the arm
  where the slot record's prior-state byte `+0x40` is `0xFF`. The rest of `002A3250` is window-state
  bookkeeping: it advances the round-robin cursor `win+0x3C2` over the 40-byte records at
  `0209C700`, resets globals `0209C980`/`0209C988`, copies the `win+0xD0` embedded state, runs a
  `0017F880`-backed accumulation loop into `+0x24`, and marks `win+0xB0 = 7`, `win+0x88 = 1`. So
  the three held-word writers are now all classified: the frame rebuilder, the message-2 modal
  swallow (`002284F0`), and the window-open reconfigure — all level clears; the arbiter's post-act
  zero of `02F9736A` remains the only *edge* consume.
- **Anything live.** No frame order here has been observed in a running process. Readiness is
  `CONTRACT READY`, not `RECONSTRUCTION READY`.

## 9. Evidence

**Class: NATIVE/STATIC throughout.** Every address, call site, store site and loop bound above was
disassembled from the authority image `73461d08…d89721f8` in this session. Three items are carried
from existing pages and are marked as such where used: the snapshot's field map (Config screen §6,
`DI-2`), the policy table's 64-byte shape (capability page, AH-10 re-verification), and the "read a slot on demand"
entry (`CONTRACT-binding-profiles` §2). Nothing in §5 rests on a carried claim.

Instruments. The two the population statements rest on are committed beside this contract, because
a citation into an untracked scratch directory is not a citation:
`_index/candidates/fable_ripband.py` (§6, two planted controls) and
`_index/candidates/fable_leaband.py` (§6a, control: it must find the rebuilder's own `lea rbx`).
The four navigational ones stay in `Database/Tools/work/FABLE/pub140-scratch/` and produce no figure
quoted here: `disr.py` (resolving disassembler), `closure.py` (transitive direct-call closure,
control: the root's hand-read callee `00254B50` must appear), `paths.py` (shortest call path) and
`callers.py` (image-wide direct callers).

## 11. Cross-subsystem neighbours — disposition (FABLE, 2026-09-21)

This contract cites six **hub** bodies, and a hub's neighbour set is the game. The contract's claims
are about **three call sites inside them and their order**, not about anything else they reach, so
each hub's other neighbours are dispositioned here by the route that produces them rather than one
by one.

**Group A — the frame drivers and the field predicate.** `MainLoop_UpdateAndRenderFrame`
(`0022B8C0`), `World_UpdateSimulationTick` (`00314020`), `BattleSystem_RunFieldFrameOrchestrator`
(`00234590`) and `FieldData_GetActiveFieldRecordBit15` (`00377C20`) are cited **only** for the call
sites listed in §3 and §4. Their remaining callees and callers are the per-frame work of
**CombatAI**, **CombatAction**, **CombatFormula**, **Movement**, **Spawn_Encounter_Lifecycle**,
**Status_Periodic_Terminal**, **Rewards_Progression_Economy** and **ActorEntity** — everything a
world tick advances and everything that asks the field record for an action permission. None of it
is a claim of this contract, and none of it is evidence for one; the ordering in §3 is read from the
instruction stream of `00314020` alone and does not depend on what the loop body does.

**Group B — the two image-wide getters.** `005C5230` is a folded constant stub (it returns 0) and
`00796E20` is the application singleton getter. Between them they account for the **Presentation**,
**Resource**, **Developer**, **PlatformOnlineAchievements**, **SaveLoad** and **Save_Load_Settings**
appearances. A caller of either is a caller of the whole program's plumbing; neither edge carries
input semantics, and this contract cites `005C5230` only to say that `002284F0`'s default arm
returns 0 through it, and `00796E20` only as the source of the device bank in `0017DE10`.

**Group C — three real edges, named because they are real.**

- **Audio.** `00229AF0` is a direct consumer of the capability aggregate `002E0FA0` — it reads the
  policy, like the arbiter does. `PROPOSED-repos2d-13` in
  [OPEN-QUESTIONS](../_index/OPEN-QUESTIONS.md) already records it as one of the two direct
  consumers of row 1 bit 21. It is a *sibling* consumer of the policy, not part of the input path,
  and invariant I-6 applies to it exactly as it applies to the arbiter.
- **Story_Event_Quest_Hunt.** The arbiter calls `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate`
  (`0032A8A0`) twice, at `00253F21` and `002540AF`, so a persistent story flag participates in
  arbitration. Which flag, and what it gates, is not read here and is not claimed.
- **ActorEntity.** The arbiter calls `0025B4C0` at `00254115` in the leader/focus chain. Also not
  read here.

Groups A and B are dispositioned as **not neighbours of this contract's subject**. Group C names
three edges of the arbiter that are real and that this contract does not follow; none of them
weakens an invariant in §5, because each invariant is stated over stores and call sites that were
read directly.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

*§11's heading is numbered, so the crossings gate does not read it. This section restates §11's dispositions
for the two layers GG-3's answer touches.*

**CoreRuntimeScheduling — MECHANICAL.** The frame drivers and the mode dispatch of §11 group A reach that
layer's scheduling and helper bodies. This contract claims only the call order, read from the instruction
stream, and nothing about those bodies' behaviour.

**UI — SERVICE, and GG-3 depends on it.** The I-5 swallow lives in a UI widget. The singleton, its factory, the
generation walker `00248030` and the root walks in `00250540` are the UI framework's. The arbiter also reaches
the UI request router. This contract relies on two facts from that layer: the walker's polarity (GG-3) and the
router's policy test. Everything else those bodies do is the UI contracts' business.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE, OUT-OF-SCOPE (11 edges).** The world tick `00314020` calls `0025BFB0`, `ActorManager_RunFieldRuntimePass` (`0025D9E0`), `00263660`, `00268650` and `003DB1F0`; the orchestrator `00234590` calls `BattleUnit_BuildFilteredFourSlotUnitBuffer` (`0030A880`) and `BattleUnit_FindByCombatantId` (`0031B770`); `0025C830` and `BattleGroup_RefreshFourActorDefinitions` (`003266C0`) call the field predicate `00377C20`; and the arbiter `00253C70` calls `0025B4C0`, which resolves a packed actor handle through `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`) and returns bit 1 of the entry's byte `+0xC` when the entry's type bits (byte `+3` shifted right by 5) are 1 or 3, else 0. The frame drivers run the actor layer's per-frame passes and the arbiter asks one yes/no question of an actor entry in its leader/focus chain; this contract claims the call order and the arbiter's reads, and none of those bodies' behaviour.

**Audio — SERVICE, OUT-OF-SCOPE (5 edges).** `00229AF0` (the sibling consumer of §11) calls `002DF370`; `002E0FA0` is called by `00229AF0`; the field frame `0022A770` calls `0036F460`; the world tick `00314020` calls `002DEBA0` and `00362850`. `00229AF0` reads the aggregate and, when bit 21 is clear, tail-calls `002DF370`, which ORs or clears bits in an audio mask word; `0036F460` advances a wrapped float clock (subtract-one loop, scaled by 30) and `002DEBA0` returns one audio float - so the edges are audio bookkeeping scheduled by the frame and one audio body reading the same capability policy this contract describes, with no audio state in the input path.

**CombatAI — SERVICE, CLIENT, OUT-OF-SCOPE (5 edges).** The orchestrator `00234590` calls `BattlePerception_AdvanceCandidateCacheGeneration` (`00325060`) and `BattlePerception_ResetSpatialVisibilityCacheFrameState` (`0032A650`); `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`), `AiOrder_EvaluateTargetSelector` (`00301AD0`) and `BattleUnit_SelectAndCommitNextAction` (`00305AB0`) call the field predicate `00377C20`. The orchestrator resets the AI perception caches each slot pass, and the AI's target and action selection asks the field record whether disabling statuses are waived here - both are real, and neither is part of the snapshot, the reconcile or the arbitration this contract orders.

**CombatAction — SERVICE, CLIENT, OUT-OF-SCOPE (22 edges).** The orchestrator `00234590` calls `003065D0`, `00306BB0` (a 20-byte test that a battle-state word minus 5 is 0 or 1) and `0030CBE0`; `00319090` calls `0025B4C0`; `00313DB0` calls the reconciler `00313A00`; and 17 action bodies call the field predicate `00377C20`, among them `BattleAction_CheckActionAvailabilityReason` (`002FFCF0`), `BattleAction_IsTargetEligibleForCurrentAction` (`002FFA60`), `Battle_ProcessActionTarget` (`00307300`), `Battle_BuildActionTargetSet` (`0030D160`), `BattleUnit_CommitAction` (`0030F760`), `BattleUnit_IssueCommand` (`00311CF0`) and 11 more. The field predicate is the per-area "statuses do not stop you acting" bit, so the action layer's availability, targeting and commit paths consult it; that consumer set is the bit's business, and this contract uses `00377C20` only for the arbiter's own read at `00254067`.

**CombatFormula — CLIENT, OUT-OF-SCOPE (1 edge).** `BattleStats_ModifyHPAndProcessLethalState` (`00300530`) calls the field predicate `00377C20`. The HP-change path reads the same per-area action-permission bit as the arbiter; it is a separate consumer of that bit and plays no part in input arbitration.

**Developer — CLIENT, MECHANICAL (1 edge).** `001C2F50` (a developer auto-test body in the census) calls `00796E20`, the 8-byte getter that returns the application singleton. Every subsystem fetches the application object through that getter; this contract cites it only as the source of the device bank in `0017DE10`, so the edge is shared plumbing.

**Gameplay — CLIENT, OUT-OF-SCOPE (4 edges).** `BattleUnit_UpdateEngagementStateFlag` (`00307D10`), `BattleUnit_CollectMappedFourSlotUnitsByFlags` (`0030A8A0`), `BattleUnit_HasRelationshipClass2PlusInSlotMask` (`0030C210`) and `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) call the field predicate `00377C20`. These battle-unit helpers fold the per-area permission bit into engagement, slot collection and the battle-mode number; they are further consumers of the bit, not of the input snapshot.

**Items_Equipment_Shops_License — CLIENT, OUT-OF-SCOPE (2 edges).** `Inventory_QueryOwnedCountIncludingReservedActionItems` (`00309FB0`) and `Equipment_UnequipEncodedItemFromActiveRoster` (`0030FD10`) call the field predicate `00377C20`. Item counting and unequip read the same per-area bit the arbiter reads; nothing in the input path depends on them.

**Movement — SERVICE, CLIENT, OUT-OF-SCOPE (19 edges).** The frame bodies `0022B8C0` and `0022BC20` call `00263560` (and `0022B8C0` also `0037CF00`); the orchestrator `00234590` calls `PartyFollow_ApplyGoal` (`003246C0`), `PartyFollow_SolveFormationWrapper` (`0033B6D0`), `Navigation_HasDataset` (`00383C80`) and `00392740`; the world tick `00314020` calls `00234520`, `003DAA20`, `003DAA40` (the movement-body pool's tick reset), `003DAC70` and `0046AFA0`; `Movement_UpdateSteeringTowardTarget` (`002E45E0`) and `002E5750` call the per-slot byte reader `00267310`; and `0025B470`, `0026C3E0`, `002E28E0`, `00310920` and `00313670` call the field predicate `00377C20`. The frame and the tick schedule the locomotion, follow and navigation passes, and movement bodies read a per-slot byte and the field bit; the contract's §3 order is read from the tick's instruction stream and does not depend on any of that work.

**Party — SERVICE, CLIENT, OUT-OF-SCOPE (8 edges).** The three frame bodies `0022A770`, `0022B8C0` and `0022BC20` call `PartyFocus_CommitPendingPackedActorHandle_Thunk` (`00358BB0`); the orchestrator `00234590` calls `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`) and `BattleUnit_GetPartyLeader` (`003272A0`); the tick `00314020` calls `PartyControl_UpdateControlledActorLocomotion` (`00358C60`) and `PartyFocus_UpdatePrimarySecondaryActorProcessing` (`00358EE0`); `00304180` calls `00377C20`. Each frame commits the pending focus handle and the tick runs the controlled actor's update; that is the party layer's per-frame work, scheduled by the same drivers this contract orders, and it touches neither the snapshot nor the capability rows.

**PlatformOnlineAchievements — SERVICE, CLIENT, MECHANICAL (2 edges).** The field frame `0022A770` calls `00316930`, and `008655A0` calls the application-singleton getter `00796E20`. The frame feeds the achievement plumbing once per pass and the platform body fetches the application object like every other subsystem; neither edge carries input semantics.

**Presentation — SERVICE, CLIENT, OUT-OF-SCOPE (52 edges).** The three frame bodies call the render side of the frame - `MainLoop_Draw` (`0022B0B0`), `RenderSystem_RunCharacterUpdatePipeline` (`003323D0`), `EffectSystem_ProcessQueuedGraphicsEffectsForPass` (`00375500`), `GraphicsSync_ClearSharedCommandStateBits` (`0036F2C0`), `GraphicsSync_WaitBackendState100ClearAndResetSharedState` (`0036F2F0`), `VFXSystem_RenderSpecialPassWithGraphicsFence` (`002590F0`), `002512B0` and others, 31 edges in all; seven rendering bodies such as `00187950`, `001CD0E0` and `001D1660` call the singleton getter `00796E20`; `002BAF80` and `002B7B80`, two UI input-consumer state machines filed to presentation, call the snapshot testers `00250130` and `00250200`; `00400E80` and `00401620` call the capability aggregate `002E0FA0`; `002AAE40` and `002B0280` call the 21-byte adapter `0017F880`; the tick calls `CameraSystem_GetActiveMask` (`00259AF0`) and `003E7650`; and `PartyCombat_UpdateStanceState` (`00307E70`), `BattleUnit_ComputePresentationSuppressionMask` (`003125E0`), `BattleUnit_BroadcastPartyCombatTargetRelation` (`00313B30`), `AddMotion_ApplyBonePose` (`003714A0`) and `003DD4C0` read the field predicate or the per-slot byte reader. The frame draws after it ticks, and some presentation bodies are themselves consumers of the snapshot and the policy, of the kind whose frame position GG-1 says this contract does not place - so the edges are the render frame's schedule and further consumers, not part of the ordering proved in §3.

**Resource — SERVICE, CLIENT, MECHANICAL (4 edges).** The three frame bodies call `00324510`, the 417-byte message-buffer state machine that all three frame bodies drive (it arms a buffer pair and publishes a handler as it steps its states), and `001A7A50` calls the singleton getter `00796E20`. Stepping that state machine is a fixed step of every frame body and shares no state with the snapshot or the arbiter.

**Rewards_Progression_Economy — SERVICE, CLIENT, OUT-OF-SCOPE (2 edges).** The orchestrator `00234590` calls `Loot_UpdateWorldPickupLifetimeAndDespawn` (`00319600`), and `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) calls the field predicate `00377C20`. The slot pass ages world pickups and the defeat-reward path reads the per-area bit; both are unrelated to input.

**Save_Load_Settings — SERVICE, CLIENT, OUT-OF-SCOPE (2 edges).** `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`, the story-flag query the arbiter calls twice) calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) and is called by `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`). The persistent flags live in the save image, so the flag query reads its base and the save finaliser evaluates the same query; the arbiter depends only on the query's answer, not on the save path.

**Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (65 edges).** 56 script-verb bodies, among them `0033F330`, `00342770`, `00347B00`, `00357040` and `003581B0`, call `00267310`, the 22-byte reader that returns one byte of a slot's `0x288`-byte record; four verbs (`0033F950`, `00348DF0`, `0034ADA0`, `0050EAB0`) call the message-window opener `002E16B0`; `0034E0B0` calls the flag query `0032A8A0`; and `00344740`, `00352FA0`, `003537D0` and `00355680` call the field predicate `00377C20`. Script verbs read a party slot's byte, open message windows and test story flags and the per-area bit; the contract cites `00267310` only as the tick's dead per-slot gate and `002E16B0` only as the route to the window-open wipe of GG-4, so none of those verbs is a claim here.

**Spawn_Encounter_Lifecycle — SERVICE, OUT-OF-SCOPE (1 edge).** The orchestrator `00234590` calls `SpawnGroup_DispatchPendingCompletionSignals` (`00307030`). Each slot pass delivers pending spawn-group completion signals; that is lifecycle work inside the loop whose only relevance here is that `00313A00` runs in the same loop.

**Status_Periodic_Terminal — SERVICE, CLIENT, OUT-OF-SCOPE (4 edges).** The orchestrator `00234590` calls `BattleUnit_ResetActionControlForStatusTransition` (`00300140`); `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`), `BattleStats_RemoveStatusesFromMaskAndRecompute` (`0030F690`) and `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) call the field predicate `00377C20`. The status layer reads the per-area bit because the bit is exactly its waiver of disabling statuses; the arbiter reads the same bit for its own test, and nothing flows between the two.

**Story_Event_Quest_Hunt — SERVICE, DEPENDENCY (3 edges).** The arbiter `00253C70` calls `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`), which calls `PersistentFlag_QueryAuthoredThresholdSchedule` (`00377970`); the message-window opener `002E16B0` calls `PersistentFlag_SetBank2048` (`0032ABF0`) as its first act. Arbitration depends on a persistent story flag (§11 group C; which flag is not read here), and the window opener marks an NPC's name as known before it takes the arm that wipes the held word.

**WorldAreaField and World — SERVICE, CLIENT, DEPENDENCY (16 edges).** The frame bodies `0022A770`, `0022B8C0` and `0022BC20` call the world tick `00314020`; the tick calls the orchestrator `00234590`, `WorldSimulation_ProcessDeferredModeRequest` (`0032FC30`) and, filed to World, `002623A0`, which publishes the actor-manager slot block; the orchestrator calls the 5-byte `00313F60` and is called by the tick; the arbiter `00253C70` calls `FieldData_GetVariable0` (`00265270`), `00313F60` and the field predicate `00377C20`; the reconciler `00313A00` calls `00377C20` and is called by `00234590`; `00377C20` calls `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) and is called by `BattleSystem_InitializeAreaState` (`002342F0`); and `00267310` is called by `00314020`. This layer owns the tick and the field record, so §3's order and the arbiter's permission read depend on it directly: the order is read from `00314020`'s instruction stream, and the permission is the active field record's bit 15.

## 10. Related

- [Input stack — device, channels and bindings](Input-Stack/input-stack-device-channel-and-bindings.md)
- [Binding profiles](Binding-Profiles/binding-profiles-remapping-and-control-state.md) · [its contract](Binding-Profiles/CONTRACT-binding-profiles.md)
- [The input name registry](Input-Name-Registry/the-input-name-registry-and-channel-aliases.md) · [its contract](Input-Name-Registry/CONTRACT-input-name-registry.md)
- [Gameplay capability / inhibition policy](Gameplay-Capability-Policy/capability-inhibition-policy.md)
- [The world tick and the field frame](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
- [The config screen](../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md)

## Falsification pass 1 — 2026-09-29 (OPUS): tested with the contract's own falsifiers

**Attack.** §2's wipes, I-1 to I-6's "Falsified by" clauses and §4's clear proof became checks. Edge censuses are raw
E8/E9 sweeps. Address censuses decode every function to its `.pdata` chain union and are repeated as a linear sweep.
Script: `Tools/analysis-kit/gfz-scripts/falsify_input_subsystem.py`, output `falsify_input_subsystem.out`, image
`73461d08…`, 0 BROKEN, exit 0. §6's population and §8's open items are carried.

| # | Clause attacked | Result |
|---|---|---|
| N0 | §2 | **survives**: both wipes store 0 at the eight anchors (seven qwords and the dword tail at `02F97398`) |
| N1 | I-1 | **survives**: `002498B0`'s edges are exactly the three calls (`0022A770`, `0022B908`, `0022BC50`) and the tail-jump `00249C4D`; `0022BC20` ticks at `0022BCCF`; the dispatcher's `jmp rcx` |
| N2 | I-2 | **survives**: the thunk `002E0D90` is `00253C50`'s one edge, and `00253C50` is the arbiter's one caller; in the tick each arbiter call follows its loop |
| N3 | I-3, §4 | **survives**: the only by-name writer of `02F9736A` is the arbiter, at the five sites, on both instruments. `edi` is written only at the zeroing and at three sites each followed by a jump to the epilogue; the restore at `0025426F` is after the last store. `002A329B` wipes `02F97368`. **51** functions read the word by name, as the page says |
| N4 | I-4 | **survives**: `002E0FA0` is absent from the rebuilder's call closure to depth 3 (14 functions) |
| N5 | I-5 | **survives**: 439 B, no direct caller; the `+0x308` precondition and the `01E0C2A4` compare precede the wipe |
| N6 | I-6 | **survives**: sixteen rows `0215F1C0`–`0215F1FF` as four 16-byte loads, combined only by `por`; one conditional `btr ebx, 0x13` |

No correction.
