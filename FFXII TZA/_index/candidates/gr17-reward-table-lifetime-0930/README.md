# GR-17: the reward tables are freed only in the same call that zero-fills every battle unit that could point into them; the one data-gated chain is closed by the effect data (SWE2-ORACLE for OPUS, 2026-09-30)

Register row GR-17 asks whether the tables that a battle unit's cached reward-row pointers `+0xE70` / `+0xE78` point
into (the `.ard` buffer bound at registry slots `02EBF148` / `02EBF140`) can be rebound or released while that unit can
still be defeated. OPUS's working notes (`Tools/work/OPUS/gr17_notes.md`) established the rebind side: the only free
is in `003EA820`, reached only through the mode-0 deferred request `0032FC30` (the tick at `003140BA`, and the debug
loader). This record settles the unit side. The method is static, from the certified image. The checker is
`gr17_lifetime_check.py` (output `gr17_lifetime_check.out`, **`FAILS 0`**). It uses only the kit's `retool.py`
(extents, disassembly, and the cached direct call/jmp and rip-reference scan).

## The answer

**Along direct control flow there is no window.** One chain depended on effect data (point 5); the shipped data
closes it ([`gr17-effect-residue-0930`](../gr17-effect-residue-0930/README.md)).

1. **Only manager-0 actors own battle units.** Units are allocated in one place (`00234480`), called only by
   `00265A20` from the manager init. It allocates only when the manager's index `[mgr+0x28]` is 0. Managers 1–4
   (the three event managers and slot 4) never own a battle unit. So guests, traps or escorts in manager 4 cannot hold
   `+0xE70`. Stage's 1/2/3-only unload request does not matter to GR-17.
2. **Every free is followed, in the same call, by manager 0's unload.** `0032FC30` mode 0 calls the rebind
   `003EA6E0` → `003EA820`, which frees at `003EA888` / `003EA992`. It then always calls `0032FCA0`, which always
   calls `002628B0(0)`. On the requeue path, the drain at `00314078` has already unloaded manager 0 before the free.
3. **The unload zero-fills every unit.** It reaches `0025B070` → `00234200` for every actor under the same
   predicate the allocator used. `00234200` memsets the whole `0xF50` unit (`002342CE`), so `+0x698`, `+0xE70` and
   `+0xE78` all become 0.
4. **The readers find their unit only by `+0x698`.** The four readers are reached only through `0030E360` → `00312280`,
   on the status-0/1/31 set arms. `0030E360` finds the defeated unit with `0031B860`, which takes the first pool unit
   whose `+0x698` equals the status holder. A zero-filled unit can never match, and no liveness flag is consulted.
5. **The one chain left.** Between the free and each unit's memset, exactly one direct-call route reaches
   `00312280`. The release itself calls `00300140(unit, 1)` → `003105D0` → `00310780` → `00319420`. That stops the
   unit's effect handle (`+0x6B0+0xC4`) with sequence 1. Sequence 1 goes through `0024FE30` → `003B1260` →
   `0024FE70` → `00333280` to the sequence starter `0046EFD0` (the handle is kind 5; `002FD0C0` serves kind 1 -
   corrected before publication, see the residue record). The starter runs the sequence's opening tracks
   synchronously. A track with kind byte `+1 == 2` and flag `+5` bit 0 is launched through `003B8670` → `002EB740` →
   `00319F50`, an event on a battle unit that can be a hit (opcodes 3 / 34, and 17 / 40 through further effects), and from there the chain continues to HP/KO → `0030E360` → `00312280`.
   If such a hit KOs an enemy unit that has not been released yet, the readers would load `+0xE70` / `+0xE78` from
   the freed buffer. That unit would be one later in manager 0's actor order, or the unit being released.
   **Closed by the data** ([`gr17-effect-residue-0930`](../gr17-effect-residue-0930/README.md)): the only
   effects that can sit in `+0x774` are the fourteen kind-5 `c_all.efx` ids 104-111 / 142-147 stored by `00329F80`,
   and that file uses none of the opcodes that reach `00312280` (a kind-2 track is not itself a hit).
6. **Party-path re-installs (question 4) are not a GR-17 window.** The party arm of `0023A570` does not write
   `+0xE70` / `+0xE78`, so an earlier `.ard` install's values survive a re-install. But allocation zero-fills the
   unit, and no allocation outlives a manager-0 unload (points 2–3). Such a value therefore points into the live
   buffer, never a freed one.

**In player terms:** when you leave an area, the game discards each enemy's battle record in the same step that
discards the area's reward tables, so a defeated enemy cannot pay out EXP, LP or gil from a discarded table. The one
theoretical exception is an effect that lands a killing hit at the instant it is stopped during the area change, and
whether any such effect exists is set by the game's effect data, not its code.

| step | what it shows (addresses) |
|---|---|
| **S1** | The readers `002F8BB0` / `002F90C0` / `00317090` are called only by `00312280`. `00312280` is called only by `0030E360` @`0030E884`. None of the four is named by a rip reference or by any qword in the image. |
| **S2** | Every reader loads `+0xE70` / `+0xE78` from its entry `rdx` (`00317090`: `rcx`). `00312280` passes its own `rdx` (`r14`; `003123C7`, `003124B9`, `003125B9`). `0030E360` passes `rbx` = `0031B860(holder)` (`0030E3A7`–`0030E3B6`). The only other `rbx` writes are the spill reload `0030E6D9` and the epilogue. |
| **S3** | `0031B860` walks `00236820(i)` for `i < 00236850()`. Its only data test is `cmp [rax+0x698], rdi`. |
| **S4** | The jump table at `00120000+0x1EE8C4` / `+0x1EE8A4` sends status ids 0, 1 and 31 to `0030E80A` / `0030E850` / `0030E85E` → `0030E875`. The call is taken only when `edi = [rsp+0x44] = (mode − 3 ≤ 1)`. |
| **S5** | `00234480` is the sole allocator. It is called only by `00265A20` @`00265A9F`, and `00265A20` only by `0026CE60` @`0026CECE`. Allocation memsets `0xF50` (`002344D2`), sets bit 0 and links `actor+0x30` (`002134A0`). The gate is `[rbp+0x28] == 0` (`00265A70`) and `actor+0x14 ≥ 0x80`. `[mgr+0x28]` is the index `0026C8C0` stores at `0026C957` into `02098E10 + idx·0x288`. The only other caller of `002134A0` (`001E8580`) builds a 0x98-byte object, not an actor. |
| **S6** | `00234200` is called only by `0025B070` @`0025B225`, under `+0x14 ≥ 0x80 && +0x30 ≠ 0` (`0025B212`–`0025B21D`). It memsets `0xF50` at `002342CE` for every pool unit. `0025B070` is called only by `002628B0` @`00262D34`, which skips it only for manager 4 (`00262D2C`) or when the loaded bit is clear (`0026292C`). `002628B0` is called only by `0025BFB0` and `0032FCA0`. |
| **S7** | `02B5E0C0` is freed only at `003EA888` / `003EA992`. `003EA6B0` zeroes it without freeing. `003EA820` is reached only via `003EA6E0` (tail jump `003EA700`), and `003EA6E0` is called only by `0032FC30` @`0032FC4B`. Every branch up to `0032FC7B` rejoins before `call 0032FCA0`, and every branch in `0032FCA0` rejoins before `call 002628B0` @`0032FCF6` (`ecx` = the mode, 0). |
| **S8** | Manager bit 0 is set only by the init (`0026D305`, after the allocation at `0026CECE`). It is cleared by the unload (`00262DA8`, after the release) and by the setup `0026C8C0`. `0026C8C0`'s only routes are the load callbacks `0032FCA0` issues at `00330029` / `00330030`, after its own unload call. |
| **S9** | The window from the free to each unit's memset has 174 direct call/tail sites and no indirect call. Its bodies are `003EA820` after the free, `0032FC30` after `003EA6E0`, `0032FCA0` to `0032FCF6`, `002628B0` to `00262D34`, `0025B070`, and `00234200` to `002342CE`. Only `0025B225` → `00234200` and `0023423F` → `00300140` have a direct-call closure that reaches `00312280`. |
| **S10** | Every direct route from `00300140` to `00312280` uses the edge `00310780` @`0031082C` → `00319420` and the node `0046EFD0`. Removing either cuts them all. The gate is data: `0046F092` `test [rax+5],1` and `0046F098` `cmp [rax+1],2` before `call 003B8670` @`0046F0AF`. |
| **S11** | `0023A570` stores `+0xE70` / `+0xE78` only at `0023A9A5` / `0023A9F4`. The party arm `0023AA49`–`0023ABCA` does not touch them. Both `.ard` exits jump to the common tail `0023ABCA`, which sets `+0x698` at `0023ABFA`. |
| **C1** | Controls: the closure finds `0030E360` → `00312280`. The S9 scan is not vacuous (it flags `00234200`). The window callees `00319140` / `002EB780` do not reach. |

## Contradicted or corrected statements

- **The notes' "+0xE70 / +0xE78 ... never cleared"** and the field map's writer count for them
  (`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`, the `+0xE70` / `+0xE78` rows, "0 writers → 1") count
  only field-addressed stores. The record-wide memsets at `002344D2` (allocate) and `002342CE` (release) also zero both
  fields, and those memsets are what closes GR-17.
- **The notes' premise "units of manager 0 or 4 … Stage (1,2,3 only) leaves them alive across the rebind"** is
  wrong in both halves. Manager 4 never owns units. Manager 0 is not unloaded by Stage's request; `0032FCA0` unloads
  it right after the rebind, inside the same `0032FC30` call. The drain ordering at `00314078` vs `003140BA` only
  matters on the requeue path, and there it puts the release before the free.

## Limits

- **Direct edges only.** Conditional tail jumps (jcc) were also checked: none leaves a framed function, and the jcc
  edges from frameless leaves add only the address-taken leaves `002E7090` / `002E70C0` (a review finding,
  `auditspec-review-gr17-0930/gr17_jccfix.out`) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr17-0930/REVIEW.md) optional sentence)*. Reachability follows `call` / `jmp` to immediates. The window's own bodies contain no
  indirect call. But the direct closure of the window's callees is 7,357 functions, with 1,197 indirect call/jmp
  sites in 490 of them, and those sites are not followed. ~~135 of the 383 functions that can reach `00312280` are
  address-taken~~ 135 of the 382 functions that can reach `00312280` (383 counting `00312280` itself, which is not
  address-taken) are address-taken *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr17-0930/REVIEW.md) correction wording)*, mostly script-opcode tables (`01EED8C0`–`01EF91E0`) and debug-menu tables (`01F26CD0`–`01F29EE8`).
  An indirect dispatch into one of them during teardown would be a second route that this record cannot see.
- **The release predicate.** Release requires `actor+0x14` bit 7 and `actor+0x30 ≠ 0` at unload time. Bit 7 is set
  only by `00266BD0` (in the constructor `00266530`, which also clears it first). No `and` writer of `[X+0x14]`
  clears bit 7 afterwards, and the `00358940`-sourced writers (`00265B13`, `0026B929`) keep it. About 35
  `mov byte [X+0x14]` sites elsewhere were not typed to a non-actor base, and neither were the image's `qword [X+0x30]`
  stores. If one of them hit a live manager-0 actor, that unit would leak past the unload with `+0x698` still set.
- **The manager index.** `[mgr+0x28]` is taken as the index from its store at `0026C957`. Register-based stores to
  `+0x28` outside the manager code range were not censused.
- **Threading.** The argument assumes `0030E360` runs on the simulation thread that runs `0032FC30`. The async bind
  completion `003EA710` writes the new buffer and slots; it does not read units.
- **Out of scope, noted.** A manager-0 install that ran before the async bind completed would find `02EBF148` null.
  It would cache 0, not a stale pointer (`0023A9A3`), which is a null-read question and not GR-17. That ordering was
  not examined.
