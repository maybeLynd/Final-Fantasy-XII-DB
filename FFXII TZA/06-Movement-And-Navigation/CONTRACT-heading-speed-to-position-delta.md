---
contract: Turn a heading, a pitch and a speed into a position delta, behind an actor-class gate that refuses in silence
category: 06-Movement-And-Navigation
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 06-Movement-And-Navigation/heading-speed-to-position-delta.md
entries: ["002E4380", "00265020"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants read from the
    shipping bytes — **both class gates taken at their instructions and compared as idioms**, and
    **both refusal paths followed to what they write**, which is the fact §4's third invariant turns
    on. **This records checks performed on that date, not the method of the original derivation**,
    which is on the locomotion page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-heading-delta-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — heading, speed and the position delta

> **Authored 2026-09-22 by FABLE.** S-18's contract column carries one contract over three pages.
> **This takes the locomotion page.**
>
> Written against FRONTIER's adequacy test. **`LD-2` and `LD-3` are why this is not
> operation-scoped:** two functions test the *same field* with *different idioms* and accept
> *different sets*, and both refuse by writing a plausible value instead of a status — a pair of
> facts neither body can state alone.

## 1. Purpose

Convert where an actor is facing and how fast it is going into how far it moves this frame.

## 2. Interface

| | body | note |
|---|---|---|
| **the delta** | `Movement_ComputeDeltaFromHeadingSpeed` (`002E4380`), 601 B | yaw + pitch + speed → a 4-vector |
| **the position** | `Actor_GetWorldPosition` (`00265020`), 61 B | the wider gate, and the one that lies most quietly |

**Two arms this table did not state** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 307, which executed both bodies; bytes re-read.)*:
- **`r8d != 0` is a pass-through.** The output is the caller's vector `r9` with W = 1.0 (`002E43EE`–`002E4409`), and
  the movement context's `+0xF8` becomes `sqrt(|v|²)` through the square-root helper (`002E43B7`–`002E43E6`). No yaw, pitch or speed is
  consulted.
- **Speed 0 short-circuits to `{0, 0, 0, 1}`**, the same output as the refusal (`LD-2`). This one rests on OPUS's
  execution.

## 3. Types

```
WorldActor
  +0x03   u8     top three bits are the actor class (LD-1)
  +0xB8   ptr    the movement / position block

movement state
  +0xA0   f32    pitch
  +0xA4   f32    yaw
  +0xD0   f32    speed
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**LD-1 — One actor-class gate, and it is a precondition of the whole API rather than a quirk of one
function.** `002E439A`–`002E43A2` reads `byte [actor + 3]`, masks `0xE0` and requires `0x60` —
class 3. The same gate stands in `Movement_SetRequestedSpeed`,
`Actor_SetDesiredMovementHeading`, this body, and **twice** in `Movement_UpdateActorFrame`.

**LD-2 — `Actor_GetWorldPosition` tests the SAME field with a DIFFERENT idiom and accepts a WIDER
set.** `00265025`–`00265038` does `shr r10d, 5` — taking the class as a *value* `0..7` — then
`sub 1` / `je` and `cmp 2` / `jne`, which admits classes **1 and 3**. It also **null-checks the
actor first** (`00265020`), which the movement gate does not.

> *So the field has two readings in the same subsystem: a masked equality that admits one class, and
> a shifted value compared twice that admits two.* **A reimplementation that unifies them is wrong in
> one direction or the other**, and which direction depends on which body it standardises on.

**LD-3 — BOTH refusals are silent and BOTH write a plausible value. Neither returns a status.**
`00265052` writes **zero into all three position outputs** and returns — *a refused position is the
world origin, which is a legal coordinate.* `002E45C9` writes `0x3F800000` — **`1.0f`** — into the
delta's W and returns. **So a caller that ignores the class receives well-formed data rather than an
error**, and the two failure values are exactly the ones that look least like failures.

**LD-4 — The delta is a SPHERICAL decomposition, not a planar one — except under the flat-movement condition**
(the page's §4). There the pitch term is dropped: Y = 0, and X / Z are not scaled by `cos(pitch)`. OPUS executed
both branches *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 307, which executed both bodies; bytes re-read.)*. Otherwise: pitch both supplies the
vertical term and foreshortens the horizontal one:

```
X = sin(yaw) · cos(pitch) · speed
Y = sin(pitch)            · speed
Z = cos(yaw) · cos(pitch) · speed
```

*A port that treats movement as planar and adds Y separately agrees on flat ground and diverges on
every slope, because it loses the `cos(pitch)` factor on X and Z.*

**LD-5 — The output is FULLY INITIALISED even when refused, and the two halves are written in
different places.** `002E438E`/`002E4394` zero X, Y and Z **before the gate is tested** — a qword
and a dword, twelve bytes — and W is written **on the exit path**. *So the refused result is
`{0, 0, 0, 1.0}` and not a partially written vector, which is why `LD-3`'s silence is survivable and
also why it is hard to notice.*

**LD-5a - The pass-through assumes the input vector does not overlap the output** *(2026-09-30, FABLE, Claude Opus 5.5,
on ASTRA `2ada8a5a0`, `heading-passthrough-alias-boundary/`; bytes re-read by FABLE).* `002E438B` saves only the input
**pointer** (`mov r14, r9`). `002E438E`/`002E4394` then clear output bytes 0-11, and only after that does the pass-through
(`r8d != 0`) read the input at `002E43BC`/`002E43C2`/`002E43C7` (+4, +0, +8). If the input is the output, those reads see
the zeros just written, not the caller's vector. A distinct input keeps its three components. The decomposition path
(`r8d == 0`, `002E4419` on) never reads `r9`/`r14`, so aliasing matters only on the pass-through. *Scope: this is the
exact-alias case. General partial overlap is not analysed. The effect of an alias on the `sqrtf` call and the `+0xF8`
store that follow is not claimed.* *Accepted 2026-09-30 (OPUS incorporation): SWE2-AUDIT-SEM re-derived the save, clear
and read order, the shipped call's local output and the interposed body's registers, verdict ACCEPT (`64db6a9ef`,
`_index/candidates/auditsem-review-heading-alias-0930/REVIEW.md`). SWE2-AUDIT-SPEC independently byte-verified the
same three claims and reproduced `callee_nonvol.py`'s output, verdict ACCEPT (`FABLE-REQ-AUDITSPEC-REVIEW-HEADING-ALIAS-0930`,
its 2026-09-29 final-batch review), keeping the direct-level limit and K-14's class-byte question as stated.*

*At the one shipped call site the precondition holds.* `002E50CB` in `Movement_UpdateActorFrame` `002E5030` passes output
`rdx = rsp+0x30` (`002E50C0`), a 16-byte local in `002E5030`'s own frame (the GS cookie is at `rsp+0x40`, `002E5043`).
It passes input `r9 = r14` (`002E50BD`) and mode `r8d = ebp` (`002E50C5`); `r14` and `ebp` hold the caller's entry `r8`
and `edx` (`002E504C`/`002E504F`). The local lies below `002E5030`'s entry stack pointer, so no pointer that is valid
when `002E5030` is entered can address it. A port that keeps separate input and output buffers matches the shipped
call. A port that computes the delta in place must copy the input first.

**LD-6 — Both angles are wrapped into ~~`(−π, π]`~~ `[−π, π]` before use** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 307, which executed both bodies; bytes re-read.)*. The shipped wrap
(`002E4464`–`002E44EF`) adds `±π` by sign, subtracts a truncated multiple of `2π`, then subtracts the `±π` again.
That maps `+π → −π` and `−π → +π`, so both endpoints are reachable. It uses the truncating-`fmod` idiom the
page describes in §4. *Carried, not re-derived here.*

## 5. State

**Read:** the actor class byte, and the movement block's pitch, yaw and speed. ~~**Written:** only the
caller's output vector.~~ **Written:** the caller's output vector, **and the movement block's `+0xF8`** - `sqrtf(|v|²)` on the pass-through (`002E43E6`), and the speed when `+0xF8` is negative on the
decomposition path (`002E445C`). *This body owns nothing.* *(Corrected 2026-09-29, OPUS, falsification pass 1, `CON-167`.)*

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-facing-and-steering.md`](CONTRACT-facing-and-steering.md) — S-18's first |
| **Producers of `+0xA4` / `+0xD0`** | the combat-side movement intent, and the animation-state override |
| **Same gate** | the speed setter, the heading setter and the frame driver (`LD-1`) |

## 7. State transitions

*class gate → wrap both angles → decompose → write the delta.* On refusal: *zero X/Y/Z, write
W = 1.0, return.*
*(Made exact 2026-09-29, pass 1: gate → pass-through when `r8d != 0`; otherwise the `+0xF8` sentinel repair → wrap →
`00424080`, when `[actor+0xC0]` is live, which may change the wrapped yaw and the speed → speed-0 test → decompose.)*

## 8. Script · resource · event interactions

None directly. The angles and speed arrive from the combat-side intent or the animation-state
override.

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- A wrong actor class yields `{0,0,0,1.0}` with no status (`LD-3`, `LD-5`).
- A null actor, or a class other than 1 or 3, yields the world origin from the position getter
  (`LD-2`, `LD-3`).
- The two gates disagree about class 1 by construction (`LD-2`).

## 11. Observable behaviour

An actor of the wrong class simply does not move, and anything that asked where it was is told the
world origin — which is why a mis-classed actor reads as standing at the map's zero point rather
than as an error.

## 12. Reproduction formula

Call the delta with a class byte whose top bits are not `0x60` and assert the output is exactly
`{0,0,0,1.0}` (`LD-3`, `LD-5`). Call the position getter with class 1 and assert it **succeeds**,
then with class 2 and assert `(0,0,0)` (`LD-2`). Call it with a null actor and assert the same
`(0,0,0)` (`LD-2`). Feed a non-zero pitch and assert X and Z are scaled by `cos(pitch)` (`LD-4`).

## 13. Runtime validation

~~**None.** No experiment executes these bodies.~~ **Superseded 2026-09-25:** OPUS's replay executes both bodies
(block 307; `_index/candidates/s18-opus-replay-delta-and-position/`), and that is the source of the four
additions above. S-18's runtime cell is not addressed by this
contract — *and that cell's gap is separately recorded as 92 bodies executed across `EXP-132`–`137`
whose records name no contract, which is a different half of S-18 and is not claimed here.*

## 14. Unresolved

- [x] **K-14.** Whether any caller depends on the refused `{0,0,0,1.0}` rather than merely tolerating
      it. **REOPENED, narrowed (2026-09-29, OPUS, `CON-172`, on ASTRA `2ada8a5a0`; register `K-14`).** What stands:
      - `002E4380`'s only call edge is `002E50CB`;
      - the caller's own class-3 gate at `002E5077` dominates it.

      What fell is the premise that closed the rest. The body run between the two gates is
      `Movement_UpdateSteeringTowardTarget`. It is called at `002E50B8` with the same actor, when the movement
      mode byte `[[+0xB8]+0xF0]+0x29` is 1–4.
      - It is **963 B, eight chained unwind fragments**. The 40 bytes read as "a leaf" are its prologue
        fragment, which has no `ret`; the only `ret` is `002E49A2`.
      - It makes **21 calls**.
      - The body itself has no direct `+0x03` operand. Whether any callee can change the actor's class byte
        is not established, so **neither is "the refusal never executes"**.

      Closing this needs the 21 callees' effects on `[actor+3]`, or an execution that shows the class across
      the call.
      *The caller's registers across the interposed body (2026-09-30, FABLE, Claude Opus 5.5; source read, nothing
      executed; `_index/candidates/heading-alias-fable-0930/`).* `002E5030` keeps the input pointer in
      `r14` and the mode in `ebp` across the call at `002E50B8`.
      - The 963 B extent `002E45E0`-`002E49A2` never writes `r14`.
      - It pushes `rbp`/`rsi`/`rdi` (`002E45E7`-`002E45E9`) and pops them at its one `ret` (`002E499F`-`002E49A1`).
      - It saves `rbx` at entry `rsp+0x18` (`002E45E3`) and reloads it from `rsp+0xF0` (`002E498A`), the same cell.
      - Of its 14 distinct direct callees (21 call sites), none writes `r14`, and the one that writes `rbp` pushes
        and pops it (the per-callee list is in the record).

      So the delta receives the caller's entry `r8`/`edx` unless a deeper callee breaks the x64 convention. ~~That was
      not checked transitively.~~ *Narrowed 2026-09-30 (OPUS incorporation, on SWE2-AUDIT-SEM `64db6a9ef`, verdict
      ACCEPT): the call closure of `002E45E0` to depth 4 over direct calls and tail jumps (`.pdata` chain-root extents)
      is 54 functions, and none writes `r12`–`r15`, `rbx`, `rbp`, `rsi` or `rdi` without saving it in the same body
      (control: `003DA6A0`'s saved `rbp` writes are seen). Six indirect calls inside those 54, and depth beyond 4, are
      not followed.* This settles the alias precondition's register half only, not the class question above.
      Regression: `falsify_heading_delta.py` H8 validates the extent through the chain before counting calls.
      *Static slice consumed (2026-09-29, OPUS, on ASTRA `c957be221`, `heading-class-effects-slice/`, Method A:
      source only, nothing executed).*
      *Ratified 2026-09-30: SWE2-AUDIT-SPEC's ratification at `a95c664bf` (`_index/candidates/auditspec-ratify-legacy-verdicts-0929/`, L351) records `verdict:ACCEPT`,
      scoped: the static effect boundaries are valid, and they are not a class closure. Class stability stays OPEN.
      (Added by SWE2-CONTRACT for OPUS.)*
      - The interposed body calls `0026C120` with mode 0 (`002E4964`–`002E4969`). Its class-3 arm stores the new
        steering mode, and when subrecord `+0x65` is set it calls `002EBE50` and `002E8EE0`. It then calls `002E6300`,
        whose conditional tail enters `00265510`.
      - The object-state setters `003E33E0` / `003E3440` read their flags word twice and replace bit 23 / 24. They
        could touch actor byte `+3` only if that word sat at `actor + 1`, an alias neither observed nor excluded.
        *Placement condition made exact (2026-10-01, OPUS, on ASTRA's `heading-flag-class-mask/`, ACCEPT by
        SWE2-AUDIT-SPEC, `_index/candidates/auditspec-review-astra-heading-flag-class-mask-1001/`; both snippets re-read
        by OPUS):* `003E33E0` stores `((dx << 23) ^ d0) & 0x800000 ^ d1 | 2` and `003E3440` stores
        `((edx << 24) ^ d0) & 0x1000000 ^ d1 | 4`, where `d0` and `d1` are the two separate reads of `[rcx]`. Every
        bit outside the replaced bit and the dirty bit is copied from `d1`. A dword covering actor byte `+3` sits at
        `actor + q` with `q` in 0..3, which puts the class bits that `002E6000` tests (`byte [rcx+3] & 0xE0`,
        `002E6022`) at bits `8*(3-q)+5 .. 8*(3-q)+7`. So `003E3440` (bits 24 and 2) can never reach them at any
        placement, aligned or not, and `003E33E0` (bits 23 and 1) reaches one only at `q = 1`, where bit 23 is class
        bit 7. A 4-aligned flag word and a 4-aligned actor exclude `q = 1`. The real placement, alignment, the absence
        of an interfering write between `d1` and the store, and the class's stability across other writers stay OPEN.
        These are algebraic cases, not observed values.
      - The position path goes through the placement solver `00380D30`, not a copy.
      - The render commit is gated by `003EC3D0`'s global `02B3EC90` OR an optional argument, so a zero argument
        does not prune its four tails.
      - *The four commit-dispatch tails, measured (2026-09-29, OPUS, on ASTRA `eab9cdf34`, source only, re-read by
        OPUS).* Each is a two-instruction store of 1 into its node argument, and reads neither `rdx` nor `r8d`:
        - `0045FD00`: `mov dword [rcx + 0x3D8], 1; ret`;
        - `00529D40`: `mov dword [rcx + 0x3D4], 1; ret`;
        - `0052A8A0`: `mov dword [rcx + 0x434], 1; ret`;
        - `0052B5D0`: `mov dword [rcx + 0x3F8], 1; ret`.

        Which object `rcx` is, what the flags mean, who reads them, and their lifetime are not established. The
        offsets are not mapped onto any type by arithmetic.
      - *Their readers, consumed (2026-09-29, OPUS, on ASTRA `9241ba12c` and `ce6fccd87`, source only, both reviewed by
        SWE2-AUDIT-SPEC; every cited instruction re-read by OPUS).* Each flag has a reader in the matching type's own step
        that tests it, clears it, and only then does its work:
        - `0x6B` / `+0x3D4`: step `00529D50` compares it at `0052A063` with `r13d` (zeroed at `00529FEC`); when they
          differ it writes `r13d` back at `0052A06C`, sets `esi = 0x20` (`0052A073`) and calls `00533B20` from the
          extra loop at `0052A08A`.
          *Consumed 2026-09-30 (OPUS, on ASTRA `8969fe745`, `heading-6b-zero-definition/` and
          `heading-native-helper-saved-registers/`, STATIC_ONLY; ACCEPT by SWE2-AUDIT-SPEC at `cd86f404d`,
          `auditspec-review-heading-zero-abi-0930/`, which re-derived both without the producer's adapter):*
          - **The zero dominates both uses.** In `00529D50`'s normal-return graph (917 B, 187 instructions), removing
            `00529FEC xor r13d, r13d` makes both `0052A063` and `0052A06C` unreachable. The body's only other R13 write
            is the epilogue restore `0052A0AA`.
          - **The two crossing calls restore R13, and the loop's RSI and the receiver's RBX, on a normal return.** Both
            `0052A03A` and `0052A05E` call `00533B20` (9,526 B, 1,653 instructions, decoded to its end `00536056`). It
            pushes RBX, RSI, R13, R14, R15, then `sub rsp, 0x3A0`. It has one `ret` (`00536055`), reached only after
            `add rsp, 0x3A0` and the pops in reverse order, and no jump leaves the body. No direct `[rsp+d]` store
            lands in the saved slots.
          - Conditions that remain stated, not proved: a normal return, a coherent RSP, and intact saved stack bytes.
            The stack-cookie check at `00536038` calls `00808C40` before the pops, and its success is not observed.
            Aliasing through native pointers or callees is not excluded (a direct-store check only).
          - The finding is local. It does not show that the field stays zero after nested work, what type `0x6B`
            means, or that the extra loop's 32 calls complete in a live run.
        - `0x71` / `+0x434`: step `0052A8B0` tests it at `0052AD2E` and zeroes it at `0052AD37` before further work.
        - `0x72` / `+0x3F8`: step `0052B5E0` tests it at `0052BB35` and, when non-zero, calls `0052BBD0` at `0052BB45`
          with the node and node `+0x08`. That body clears the flag at `0052BBF7`, before its first call. Later it calls
          `0054B1F0` thirty-two times on node `+0x280` (`0052BF21`-`0052BF4C`, r8d 1, r9d 0).
        - `0x67` / `+0x3D8`: the 56 B step `0045FD10` has no direct operand. It calls `002F2530` and, on a non-zero
          return, `004607C0` with the node. There `00460ACA` compares the flag with `r12d` (zeroed at `00460A5B`); when
          they differ it clears the flag at `00460AD3` and calls `00533B20` thirty-two times on node `+0x280`
          (`00460ADA`-`00460AF3`).

        So the four stores read as **one-shot update requests** to the node's own step. That is a candidate meaning, at
        source level.

        Not established:
        - that 0x6B and 0x71 mean the same as the other two;
        - that `002F2530` ever returns non-zero;
        - the nested effects of `00533B20`, and of `0054B1F0` beyond the per-model oscillator page's
          parameter-install role;
        - register continuity across the intervening calls, except for `0x6B`: there `00533B20`'s own save and restore
          grounds R13, RSI and RBX under the conditions above (2026-09-30). For `0x67`, `004607C0` holds its zero in
          `r12d` (`00460A5B`) across three calls to `00533B20` (`00460A9A`, `00460AB6`, `00460AC5`) before the compare
          at `00460ACA`. `00533B20` does not push R12, and it writes R12 at `005341AF`, `0053450F` and `00534540`
          (the last reloads it from `[rsp+0x390]`). *OPUS 2026-09-30, ~~pending SWE2-AUDIT-SPEC review~~ reviewed ACCEPT by SWE2-AUDIT-SPEC
          (`_index/candidates/heading-r12-restore-0930/`; review `auditspec-review-heading-r12-0930`):* the spill `00533C56 mov [rsp+0x390], r12` dominates both
          writes, and the reload `00534540` lies on every path from them to the single `ret`. No other store covers the
          slot, and RSP moves only at the prologue and epilogue. So R12 comes back on a normal return, under the same
          conditions as the pushed registers. Until that review lands, the `0x67` path's R12 continuity counts as
          assumed;
        - the initialised node identity, the scheduling, and live execution.
      - *The list the flag walk shares with the effect update, consumed (2026-09-29, OPUS, on ASTRA `c9278cb00`,
        `heading-list-identity/`, Method A: source only; ACCEPT by SWE2-AUDIT-SPEC, `auditspec-review-heading-list-identity/`
        at `b28310393`).* The flag walk `003A9490` and the ordinary effect update `003A8390` → `0043EF40` walk **the same
        structural chain**:
        - the root cell `02EBEF88` (`003A949A`, `003A83BD`);
        - instance `+8` (`003A94A3`/`003A94F7`, `003A83C4`/`003A83D6`);
        - the node head at instance `+0x118` (`003A94D0`, `0043EF9B`);
        - the node link `+0x30` (`003A94EE`, `0043EFB0`).

        The node-type byte `[node+0]` is read by both dispatchers, `0043EE70` and `002F3910`. This is an address-and-link
        result. Three precisions come from the review, and a consumer must carry them:
        - **Different visited populations.** The flag walk reaches nodes only for instances with a non-null `+0x108`
          whose definition byte `+0x44` is `0x67`, `0x6B`, `0x71` or `0x72` (`003A94B1`–`003A94CE`). The update reaches its
          node loop only past the `+0x1B0` gate and a non-null `+0x100` (`0043EF63`–`0043EF96`). "Same chain" means the
          same links, not the same visited set.
        - **The flag walk always runs on a selected context.** `003B3CE7` is `003A9490`'s only raw caller. `003B3CA0`
          reaches it only after a successful handle lookup in `02EBD480` and `0024ED80(selected)`, which stores
          `selected + 0x1B8` into `02EBEF88` (`0024EDF1`/`0024EDF8`). It republishes the saved context afterwards
          (`003B3CFD`). The root is a field of whichever context was last published, not a singleton.
          *No local handler (2026-09-30, SWE2-CONTRACT for OPUS; ASTRA `b51b50668`, `effect-context-exception-dispatch/`,
          ACCEPT by FABLE at `936e4ad11`, `fable-review-effect-context-exdispatch-0929/`):* at the three continuations
          (`003B3CE5`, `003B3CEC`, `003B3D02`), the frame's **local** exception metadata names no language handler (a
          chained root with flags 0). So restoring the temporarily published context on an abnormal exit cannot come from
          a local handler of `003B3CA0`. The normal-path publication and restore above stand separately. Whether the
          context is restored elsewhere on an abnormal exit, or whether such an exit occurs in play, is not decided.
        - **`0024ED80` is not the only writer of the root cell.** Eleven rip-relative sites store to `02EBEF88`:
          `0024B385`, `0024B65D`, `0024C4DB`, `0024D0FB`, `0024D60D`, `0024DC4D`, `0024E89D`, `0024EDF8`, `0024EF25`,
          `0024F59C` and `003B860D`. That sweep covers rip-relative forms only.

        The flag walk reads the next link *after* its per-node call (`003A94EE`); the update reads it *before* (`0043EFB0`).
        This matters only to a live same-node question, where a node can be unlinked during the call.

        Not established: that the flag walk and a later update meet the same live instance or node. Also not
        established: node survival, `[instance+0x108]+0x44 == node[0]` in every state, and scheduling. Player
        version: the code that raises a movement-triggered effect request and the code that updates effects walk the same
        kind of effect list, but the game switches which list is current around the request, so the source alone does not
        show one on-screen effect being requested and then updated.
      - *The first position call's fifth argument (same source, `9241ba12c`).* The call to `0026AFE0` at `002E4751`
        passes a fifth dword of 0: `002E4735` is `xor ebx, ebx`, and `002E474D` stores `ebx` at `[rsp + 0x20]`, with
        no call and no `rbx` write in between. `002E4739` can skip the call. The later call at `002E4928` stays
        conditional on native ABI behaviour.
      - **Still OPEN:** ~~those four commit-dispatch tails,~~ ~~the tails' flag readers,~~ ~~the structural list the flag
        walk and the update share~~, the live identity of the instance and node across the context switch, the flags' confirmed meaning
        and lifetime, the other steering and native paths, and the initialisation and aliasing conditions. Class
        stability ~~and the refusal's reachability stay OPEN~~ stays OPEN *(answered for the refusal's reachability: see the ANSWERED 2026-09-30 item below — the refusal does not run there; 2026-10-02, OPUS)*.
      - **ANSWERED 2026-09-30 (OPUS, static; [`k14-closure-stores-0930/`](../_index/candidates/k14-closure-stores-0930/README.md),
        the actor-flow pass `k14_actorflow.py`): nothing `002E45E0` runs writes actor byte `+3` through the actor pointer, so
        the class `002E5077` checked is the class `002E4380` reads at its one call site `002E50CB`. The refusal does not
        run there, and no caller receives `{0,0,0,1.0}`.**
        - **Method:** the pass follows the actor from `002E45E0`'s entry (`rcx`) through registers, the stack, offsets
          and every direct callee under the arguments it receives: 113 bodies in 214 contexts.
        - **Stores through the actor:** 0 cover byte `+3`. The only actor-derived stores are `002E48CA` / `002E48D0`, on
          byte `+0xD`.
        - **Escapes and blind spots:** the actor pointer is never stored to memory, and no indirect call receives it. The
          12 indirect dispatches in the closure are imports: the stack-cookie failure path, `IsProcessorFeaturePresent`
          and `sinf` / `cosf` / `sqrtf` / `atan2f`.
        - **Untracked stores:** the two that could cover byte `+3` of their base write `0022F9B0`'s own frame and
          `[[actor + 0xC0] + 0x138] + 0x30`.
        - **Controls:** a direct seed at `00380D30` is flagged. The seven object-state setters trace to the render-record
          table `022C6F28 + id × 0x740`, not to the actor.

        So the commit tails and the list identity above no longer bear on this box: whatever they write, they do not
        write the actor's class. *Limit:* an object the actor points to is taken to be a different object (`[actor +
        0xB8]`, `[[actor + 0xC0] + 0x138]`, a render record, `020892C0` / `02089280`). A self-referential layout would
        reopen this, and so would another thread. Review: SWE2-AUDIT-SPEC.
      ~~**CLOSED 2026-09-23 (SWE2-CONTRACT): nobody can observe it.** `002E4380` has exactly
      one call edge image-wide — `002E50CB`, inside `Movement_UpdateActorFrame` (`002E5030`,
      pdata fragments `002E5030`–`002E5085` + `002E5085`–`002E515C`; the second fragment has
      **zero inbound edges**, it is fallthrough-only). The call is dominated by the caller's own
      identical gate: `002E5077` tests `byte[rbx+3] & 0xE0 == 0x60` (after the lifecycle/`+0xC0`/
      `+0x14F` checks) and every failure exits before `002E50CB`. The one body executed between
      the two gates, `002E45E0`, is a 40-byte leaf — no `+3` writes, no calls — so the class
      cannot change in between. **The refusal never executes in shipped code; it is callee-side
      defence for a caller that does not exist.** "Depends" never arises because "tolerates"
      never arises.~~
- [x] ~~Why the position getter admits class 1 when nothing that moves an actor does
      (`LD-2`).~~ **CLOSED 2026-09-23 (SWE2-CONTRACT), mechanism level:** class 1 is the
      **placed-object** class (K-2/BV-4) — it carries a `+0xB8` block with a readable position
      but no steering record. `00265020` reads `[actor+0xB8] +0/+4/+8` through the *same* path
      for both admitted classes (`0026503A`–`00265051` is shared) — so the wider gate is not a
      different opinion about the field, it is the correct one for a **read-only** query: a
      placed object has a position, it just cannot be steered. `sub 1/je` + `cmp 2/jne` admits
      exactly {1,3} by construction — class 1 is a deliberate operand, not sloppiness. The two
      gates guard different operations: movement writes/steers (class 3 only, because only class
      3 owns a movement context), position reads (classes 1+3, because both own a position).
      *Residual: which of the getter's ~100 call sites actually hand it a class-1 actor is a
      runtime data-flow question, not statically bounded.*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `LD-1` — the mask and value | `002E439A`–`002E43A2` read at the instructions | 1 |
| `LD-2` — the wider, differently-written gate | `00265020`–`00265038` read in full: the null test, `shr 5`, `sub 1`/`je`, `cmp 2`/`jne` | 1 |
| `LD-3` — both silent refusals | `00265052`–`0026505C` and `002E45C9`–`002E45D8` followed to their stores and returns | 1 |
| `LD-5` — the split initialisation | `002E438E`/`002E4394` shown to precede the gate test at `002E43A2` | 1 |
| `LD-4`, `LD-6` | [the locomotion page](heading-speed-to-position-delta.md) §§2 and 4, falsified 2026-09-02 | 1 |
| the delta's sole call edge is `002E50CB` in `Movement_UpdateActorFrame`, dominated by the caller's own class-3 gate at `002E5077`; the `002E5085` fragment has zero inbound edges (fallthrough-only) ~~and `002E45E0` between the gates is a 40-byte leaf with no `+0x03` writes~~; **`002E45E0` between the gates is 963 B with 21 calls, so the class's stability between them is not established** (`CON-172`; `falsify_heading_delta.py` H8) | image-wide call/jmp/`lea`/disp32 census + both bodies decoded whole, 2026-09-23 | 1 |
| `00265020` serves classes {1,3} through one shared read path (`0026503A`–`00265051`); class 1 is the placed-object class — readable position, no steering record | `00265020`–`0026505C` decoded whole; class semantics per K-2/BV-4 | 1 |
| the flags' readers and the first position call's fifth argument (ASTRA `9241ba12c`, `heading-source-consumers/`; ASTRA `ce6fccd87`, `heading-node-followup/`) | SWE2-AUDIT-SPEC ratified both `verdict:ACCEPT` at `a95c664bf` (`_index/candidates/auditspec-ratify-legacy-verdicts-0929/`): `9241ba12c` ACCEPT scoped, STATIC_ONLY (L361); `ce6fccd87` ACCEPT scoped, STATIC_ONLY, `STATIC_ONLY_CONDITIONAL_SOURCE` (L442). Every cited anchor was byte-verified by the reviewer | 1, static only |
| the static class-effects slice (ASTRA `c957be221`, `heading-class-effects-slice/`) | ratified `verdict:ACCEPT` at `a95c664bf` (L351): `STATIC_EFFECT_BOUNDARIES_VALID_NOT_CLASS_CLOSURE`; class stability stays OPEN | 1, static only |
| H8's extent repair (ASTRA `feb631dd4`, `heading-extent-repair-review/`) | ratified `verdict:ACCEPT` at `a95c664bf` (L349): ACCEPT scoped to the semantic repair of H8's extent validation. The CLI's exit-0-on-BROKEN producer gap is retained, for OPUS | 1, with a retained producer gap |
| H8's CLI and gated-count repair (ASTRA `f2b7210f6`, `heading-status-repair-review/`) | ratified `verdict:ACCEPT` at `a95c664bf` (L350): ACCEPT scoped to the `2366027d9` H8 CLI and gated-count repair | 1 |
| no local language handler at `003B3CA0`'s three continuations (ASTRA `b51b50668`, `effect-context-exception-dispatch/`) | FABLE's ACCEPT at `936e4ad11` (`fable-review-effect-context-exdispatch-0929/`): the frame's local exception metadata ends at a handler-free chained root; outer handlers and whether an abnormal exit occurs are not decided (§14, the `003B3CA0` paragraph) | 1, static; **local** only |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `LD-1` through `LD-6`. **`LD-4` is the one that
decides numerical parity** — dropping `cos(pitch)` from X and Z agrees on flat ground. **`LD-3` is
the one a port improves into a bug**: returning a status from either refusal is better engineering
and changes what every existing caller sees. **`LD-2` is the one a port unifies**, and it must pick
a direction knowingly.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Movement — internal.** The delta, the gate and the movement block are this category's own.
- **ActorEntity — SERVICE, and `LD-1`/`LD-2` are the statements.** The `WorldActor` class byte and
  the `+0xB8` block belong to that layer. **This contract asserts only which bits are read, which
  values each gate accepts, and what each refusal writes** — all visible at the two bodies' own
  instructions — and nothing about what an actor class means.
- **Audio, CombatAction, CombatFormula, Gameplay, Party, Presentation,
  Rewards_Progression_Economy, Spawn_Encounter_Lifecycle and UI — ALL CLIENTS, and all of one
  body.** `Actor_GetWorldPosition` is a hub: bodies across those nine layers call it. **This
  contract asserts nothing whatever about its callers** — `LD-2` and `LD-3` are statements about
  the 61 bytes of the getter itself, which is read in full, and `LD-3`'s point is precisely that
  a caller cannot tell a refusal from a result. *That every one of those layers silently receives
  the world origin on a refusal is the CONSEQUENCE being recorded, not a claim about any of
  them.*
- **Every other layer reached is MECHANICAL**, through these two bodies' own callees — the
  trigonometric helpers among them. *Their addresses are deliberately not cited: `LD-4` is carried
  from the page as a formula and this contract does not re-derive the transcendentals.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Movement" would otherwise be cleared by the word
> alone.*

## 17. Related

- [Heading, speed and the position delta](heading-speed-to-position-delta.md) — the mechanism
- [Contract — facing and steering](CONTRACT-facing-and-steering.md) — S-18's first

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT (8 edges).** `00265020` is also called by bodies filed to ActorEntity: `00236300`, `0037B4D0`, `003B73B0` - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT (1 edge).** `00265020` is also called by bodies filed to audio: `00362850` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (3 edges).** `00265020` is also called by bodies filed to combat action: `002F8060`, `00307300`, `00320E10` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (1 edge).** `00265020` is also called by bodies filed to combat formula: `00384F40` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (2 edges).** `00265020` is also called by bodies filed to Gameplay: `0031ADB0` (CombatAction), `00339630` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (4 edges).** `00265020` is also called by bodies filed to party: `00303CC0`, `00304180`, `00359150`; `002E45E0` reaches bodies filed to party: `003590D0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (7 edges).** `00265020` is also called by bodies filed to presentation: `002B7B80` (UI), `00322360`, `0037AD40` (EffectConstraint) - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (2 edges).** `00265020` is also called by bodies filed to rewards/progression: `002FB150`, `00312280` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (23 edges).** `00265020` is also called by bodies filed to script VM / native bridge: `0033FD60`, `00344AF0`, `00345180` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (3 edges).** `00265020` is also called by bodies filed to spawn/encounter lifecycle: `00234AF0`, `00234DA0`, `002350C0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (1 edge).** `00265020` is also called by bodies filed to UI: `003C5130` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - DEPENDENCY and SERVICE (4 edges, one far end; FABLE 2026-09-29).** All four edges end at `001EDDA0`, the 27-byte half-rate test owned by that layer: it returns 0 only when `[01F82E38]` is non-zero and `[01DFE0C0]` is zero, else 1 (read whole; decoded in [the widget-object contract](../16-UI/Widget-Object-Model/CONTRACT-widget-object.md), HALFRATE). The four callers are the ones §14's notes name.
  - *DEPENDENCY, `002F2530` (1 edge).* The half-rate test is one of the shared base update's zero-return routes ([the effect dispatch page](../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md), UQ-206 gates 1 and 3). A pending hold that clears returns 0 when the test answers 0 (`002F256B`-`002F2572`), and in half-rate an element whose type byte is `0x67` (bit 0 of the set `0x341B`) returns 0 while `trunc(+0x3C)` is odd (`002F258C`-`002F25B0`). So, in half-rate, the step `0045FD10` that §14 pairs with `0x67` / `+0x3D8` can reach `004607C0`, and the flag reader at `00460ACA`, only on frames where `trunc(+0x3C)` is even. This bounds §14's open item "that `002F2530` ever returns non-zero" by frame parity; it does not settle it.
  - *SERVICE, `003A8390`, `0043EF40`, `0054B1F0` (3 edges): cadence only.* `003A8390` advances the frame stamp at `02EBEF88` by 2 at full rate and by `2 / [01DFE0B4]` in half-rate (`003A839E`-`003A83BB`). `0043EF40` returns 1 before its node loop when its `+0x1B0` hold clears in half-rate (`0043EF74`-`0043EF86`), and consults the test again before its tail (`0043F1A8`). `0054B1F0` runs `0040AA20` a second time in half-rate (`0054B342`-`0054B34E`) and gates `0040FEF0` on the test at `0054B353`. None of this changes the delta, the gate or the refusal this contract states.
  - Tier 1: `001EDDA0` and all nine of its call sites in the four bodies read from the shipping image.

## Falsification pass 1 — 2026-09-29 (OPUS): §5's "writes only the output" refuted; the modifier hook added

**Attack.** Every clause of §2-§10 became a check that fails if the shipping image says otherwise. The checks decode every
listed body in `.text`. Script: `Tools/analysis-kit/gfz-scripts/falsify_heading_delta.py`, output
`falsify_heading_delta.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| H0 | §2 sizes; LD-1 one gate, five sites | **survives**: 601 B / 61 B; `and al, 0xe0` then `cmp al, 0x60` once in the speed setter, once in the heading setter, twice in the frame driver, once here |
| H1 | LD-2 | **survives**: null first, then `shr 5 / sub 1 / je / cmp 2 / jne` (classes 1 and 3); a refusal zeros all three outputs |
| H2 | LD-3 / LD-5 | **survives**: X, Y, Z zeroed before the gate; the refusal exit writes W = 1.0 and returns |
| H3 | §5 "Written: only the caller's output vector" | **REFUTED** (below) |
| H4 | §7 the order of operations | **incomplete** (below) |
| H5 | LD-4's flat branch | **survives**: `00267260 != 0 && 00264460 == 0` leaves Y = 0 and X / Z unscaled |
| H6 | LD-6 | **survives**: two truncating wraps, over `2π` with `±π` added and removed |
| H7 | §9 | **survives**: the 14-body closure reaches no generator and no gameplay-LCG reference |
| H8 | §14's first closure and its §15 row: `002E45E0` is a 40-byte leaf | **REFUTED, added later on 2026-09-29** (`CON-172`, ASTRA `2ada8a5a0`): eight chained fragments tile 963 B; 21 calls; one `ret`. The closure is reopened and narrowed. This pass's H0–H7 never tested §14, so their PASS did not cover it |

* **H3: the body writes the movement block.** `+0xF8` of the movement block (`actor+0xB8`) is written on both live paths:
  * the pass-through stores `sqrtf(|v|²)` at `002E43E6`, as §2's 2026-09-25 note says;
  * the decomposition path repairs a negative `+0xF8` to the speed at `002E445C`.

  So §5's "Written: only the caller's output vector. *This body owns nothing.*" is false. It owns nothing, but it writes
  one field it does not own. [The page](heading-speed-to-position-delta.md) documents both writes. `CON-167`.
* **H4: a modifier runs between the wrap and the decomposition.** When `[actor+0xC0]` is non-null and its first dword is
  not `-1`, `Movement_ModifyHeadingSpeedForObjectState` (`00424080`) receives that record's first word and the wrapped yaw
  and the speed **by address** (`002E4510`). The speed-0 test and the decomposition see its results. §7's
  *"gate → wrap → decompose"* is now *"gate → pass-through or: sentinel repair → wrap → modifier → speed-0 test →
  decompose"*. The page documents the modifier (its `00424080` row).

Consumer record: [`_index/candidates/heading-delta-falsification-pass-1-0929/`](../_index/candidates/heading-delta-falsification-pass-1-0929/README.md).
Contradiction: `CON-167`.
