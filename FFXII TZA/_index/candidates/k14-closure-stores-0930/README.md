# K-14: the stores that could reach actor byte +3 between the two class-3 gates (OPUS, 2026-09-30)

Narrowing for `K-14` ([the heading contract](../../../06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md)
section 14). Static evidence only (shipping image `73461d08…`).

## The census

`k14_closure.py` (beside this README) follows direct `rel32` calls and tail jumps from `Movement_UpdateSteeringTowardTarget`
`002E45E0`, which `002E50B8` runs between the two class-3 gates. The closure is **109 bodies**, all with a catalogue
extent. In those bodies it lists every store whose destination `[reg + d]` covers offset 3 of its own base: byte
`+3`, word `+2`, dword or float `+0..+3`, qword and xmm `+0`, plus string stores and calls to the memset/memcpy
adapters. It finds **41 such stores in 27 bodies**, and **12 indirect calls or jumps in 7 bodies**, which are the
closure's blind spot. Output: `k14_closure.tsv`.

## Seven stores resolved: the object-state setters write a slot row, not the actor

ASTRA's static slice (`c957be221`) left one alias open: the setters `003E33E0` / `003E3440` could touch actor byte `+3`
only if their flags word sat at `actor + 1`. All seven setters in the closure (`003E3120`, `003E31E0`, `003E33A0`,
`003E33C0`, `003E33E0`, `003E3440`, `003E36C0`) share one entry shape:
- each has **one** caller, a 12-byte wrapper (`003E6B60`..`003E6C00`) doing `add rcx, 0x580` and then a tail jump;
- each writes `dword [rcx]`, that is **`row + 0x580`**.

Every call to those wrappers inside the closure passes `rcx = idx × 0x740 + *(022C6F28)`, behind a `row + 0x284 ≠ 0`
guard. Examples: `002E8F89`–`002E8FA9`, `002E7AFD`–`002E7B1D`, `002EDB3F`–`002EDB5F`. So the stores land at `+0x580`
of a record in the `0x740`-stride slot table, not at `actor + 0..3`. **The alias ASTRA left open does not occur.**

## What remains

- **34 stores** in the other bodies. They are mostly float stores through out-parameters (`movss [rdx/r8/rbx]`) and
  vector copies. Each needs its base traced to show it is not the actor pointer that `002E45E0` holds in `rsi`.
- The **12 indirect calls** need their targets. `002E45E0` passes the actor directly only to `00264460` and to
  `0026C120` (with `edx = 0`). The other callees receive the steering block (`rdi`), stack locals, or a looked-up
  actor (`003587C0` / `003588B0`), which may be the same actor.

K-14 stays OPEN with this narrower residue. It is a static question; no live session is needed to finish it.

## Where the actor pointer goes: the actor-flow pass (OPUS, 2026-09-30)

`k14_actorflow.py` (beside this README) replaces the per-store base guess of the census above with a pointer flow.
- **Seed:** `002E45E0` is entered with `rcx` = the actor (`002E50B5`) and `rdx` = `[actor + 0xB8]`, the steering
  block (`002E5099`, `002E50B2`).
- **Flow:** it follows the actor through registers, the function's own stack (push/pop, spills, reloads, cursors
  advanced in place), `lea`/`add` offsets and switch tables. Direct callees are analysed under the argument values
  they receive, with a summary back to the caller: the return value, and any actor-derived value stored into the
  caller's stack. Tail jumps count as call plus return. Pointer plus index keeps the pointer's identity with an
  unknown offset, which counts as able to reach `+3`.
- **Store classes:** every store in every body reached is classified by its base: actor-derived (and whether it
  covers byte `+3`), a pointer loaded from memory (named by where it was read), the stack, or untracked.
- **Output:** `k14_actorflow.out` and `k14_actorflow.tsv`.

**Controls**
- **P:** seeded at `00380D30` with `rcx` = actor, the tool reports `00380DA6 mov dword [rbx], eax` as covering `+3`.
- **O:** all 21 stores of the seven object-state setters trace to the render-record table read through
  `022C6F28`, the same finding as the manual section above.
- **Cuts:** 9 contexts were cut for recursion or depth, and none carries the actor.

**Result, 113 bodies, 214 contexts**

| | count |
|---|---:|
| stores through an actor-derived pointer that cover byte `+3` | **0** |
| stores through an actor-derived pointer elsewhere | 1 site pair: `002E48CA` `or byte [rsi + 0xD], 0x10` and `002E48D0` `and byte [rsi + 0xD], 0xEF`, byte `+0xD` |
| stores of the actor pointer into non-stack memory, which a later load could return | **0** |
| indirect calls or jumps that receive the actor | **0** |
| indirect calls or jumps reached | 12, all through import slots, none into engine code |
| stores with an untracked base that could cover `+3` of that base | 2, both explained below |

- **The 12 indirect dispatches:**
  - 7 are the security-cookie failure path in `00809620`/`00809848`: `RtlCaptureContext`, `RtlLookupFunctionEntry`,
    `RtlVirtualUnwind`, `SetUnhandledExceptionFilter`, `UnhandledExceptionFilter`, `GetCurrentProcess` and
    `TerminateProcess`. It ends the process.
  - 1 is `IsProcessorFeaturePresent`.
  - 4 are CRT math thunks (`sinf`, `cosf`, `sqrtf`, `atan2f`).
  - These resolve the census's twelve blind spots: none can write engine memory and return to the gate.
- **The two untracked stores, both in `0022F9B0`:**
  - `0022FAB7 mov qword [rax], rbx`: `rax` is the stack slot `[rsp + 0x30]`. Its writers are `lea rax, [rbp - 0x60]`,
    `lea rdx, [rbp - 0x38]`, `add rax, 8` and `add qword [rsp + 0x30], 0x10`, so this is a cursor into
    `0022F9B0`'s own frame.
  - `0022FDD1 movss [rax], xmm0`: `rax` is the slot `[rsp + 0x48]`, whose only writer is the entry `r8`
    (`0022FA2D`). Its one outside caller (`002327B1` in `00232760`) passes `[[actor + 0xC0] + 0x138] + 0x30`, and
    the recursive call at `0022FE73` passes the same slot again.

So nothing `002E45E0` runs writes actor byte `+3` through the actor pointer. The class `002E5077` checked is the
class `002E4380` reads at its one call site `002E50CB`. The class-3 refusal does not run there, and no caller
receives its `{0,0,0,1.0}`.

**Not claimed**
- That no object the actor points to is the actor itself. The steering block `[actor + 0xB8]`,
  `[[actor + 0xC0] + 0x138]`, the render record `022C6F28 + id × 0x740` and the globals `020892C0`/`02089280` are
  treated as other objects. Stores through them that could cover `+3` of their own base are listed in the `.tsv`
  (class `loaded/other`). A self-referential layout would reopen this.
- Other threads, and anything outside the static call closure (callbacks registered elsewhere, a debugger, a mod).
- Deeper callees breaking the x64 register convention. FABLE checked the direct level (`9ca3df0ac`).
