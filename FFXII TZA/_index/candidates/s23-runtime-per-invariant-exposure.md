# S-23 runtime: per-invariant stub exposure, and EXP-093's stubbed recompute hides a second HP write (OPUS, 2026-09-25, block 300)

**Row:** S-23, the HP write and the lethal transition. The runtime cell is MIXED with the qualifier "no per-invariant
stub-exposure analysis yet". The binding gap reads "a transition-scoped contract over a system that IS one
transition; nothing live". The contract is `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md`. This note
scores nothing.

## Substitutions per record

| record | real | substituted |
|---|---|---|
| **EXP-060** | the numeric applier segment around `00311608` (caller-side HP presence, numeric and flag translation) | all five HP setter entries are **no-effect stubs**. Its own coverage line: "no HP store or lethal transition is established" |
| **EXP-093** | `00300530` (the HP write), `00300520`, `0031B860`, the gates `0030B9B0` / `0030B8E0`, `00377C20`, RX `003283D0` → `003BBD00` (real queue insert), NB `0028F1F0`, `00316D70`, **`0030E360` status transition with its real subtree**, the kill history `00469BB0`, `0032A150`, the group / death path `00306F00`, event dispatch `003299B0`, `001D50D0`, `0017D470` | `ret` stubs: `005369C0` (fired), `00300FC0` (fired), `00312280` (fired), `00301140` (fired), `003284D0` (fired), **`0030FED0` post-write recompute (fired)**, `0046A800` (fired); `003112F0` / `00300140` / `00307D10` never reached. Import thunks: `memset`, `sqrtf`, `rand` |

## The finding: the stubbed recompute re-stores `+0x48`

- **The call chain (static).** `00300530` stores HP at `00300749`. It then calls `0030E360` (`0030077A` / `003007CF`),
  which EXP-093 runs **real**. `0030E360` calls `0030FED0(rcx = unit, edx = flags)` when flags bit 9 is clear
  (`0030E81D`–`0030E828`); `0030E130` does the same (`0030E31C`–`0030E329`).
- **What `0030FED0` writes.** Its body stores `dword [unit+0x48]` at **`00310508`** (`rbx` = the incoming `rcx`,
  `0030FF0F`):
  1. `cap = +0x24`, or `max(HP, 1)` under status bit 16 (`003104CF`–`003104DB`);
  2. `cap` is doubled on status bit 28 (`003104E0`–`003104E6`);
  3. `+0x48 = HP > cap ? clamp : HP` (`003104E8`–`00310508`).
- **This has been executed.** EXP-148 ran `0030FED0` real (S-21) and records these "final gated updates of
  `d[unit+0x48]` (vs `d[+0x24]`, the `flags & 0x10000` clamp to 1, `bt edx, 0x1C` doubling)".
- **EXP-093 reached it.** EXP-093 logged its `0030FED0` stub as **fired**, so its own lethal / status cases take this
  path.

**Consequence.** The contract's postcondition "**at most one write of current HP, at `00300749`**" and its invariant
"**the store is the only write of `+0x48` on this path**" do not hold whenever the status transition reaches the
recompute. A second `+0x48` store follows, clamping HP to a cap recomputed from current status. The bound `floor <= hp
<= cap` may still hold, but the single-store claim does not. **This is application-stub exposure, and it has
consequences:** EXP-093's stub is exactly what made the single-store claim look executed.

## Per invariant

| contract item | executed by | can a substitution reach it? |
|---|---|---|
| precondition: a stats record in `rcx`; null source / target / zero delta ordinary | EXP-093 | **no** |
| postcondition: **at most one HP write, at `00300749`** | EXP-093 (with `0030FED0` stubbed) | **YES.** The stubbed `0030FED0`, reached through the real `0030E360`, performs a second `+0x48` store in shipped code (above) |
| invariant: `floor <= hp <= cap` after a storing call, bounds recomputed | EXP-093 | the recompute's second store also clamps to a (recomputed) cap, so the bound survives. Its *timing* is after the status transition, not only at `00300749` |
| invariant: **the store is the only write of `+0x48` on this path** | EXP-093 | **YES**, the same exposure |
| the lethal path's further effects | EXP-093: the real group / death, kill history and event dispatch; the stubbed defeat cleanup, rewards, recovery, reaction and kill-ledger sinks | the stubbed sinks' own effects are not executed. Whether `00301140` (recovery) or `00300FC0` (defeat cleanup) write `+0x48` was checked for **direct** stores only, and they have none. Their callees were not read |

## For the scorer

- **The one decisive exposure:** EXP-093's `0030FED0` stub hides a second `+0x48` store. That store is shown by EXP-148's
  own execution of `0030FED0` and by the static chain `00300530` → `0030E360` → `0030FED0`. The contract's single-store
  postcondition and invariant need restating.
- EXP-060 establishes no HP store by its own statement.
- `live_game` is false.
