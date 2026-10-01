# S-26 runtime: per-invariant stub exposure for EXP-086 (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-26 status write, two-layer model. Runtime **MIXED** — *"EXP-086 executes status write and its side
effects under isolated original-code replay … no per-invariant stub-exposure analysis yet"*. Binding gap: *"types
PARTIAL and nothing executed — runtime is ASTRA/ORACLE's gap; the contract no longer binds it"*. Contracts (column 6
of `important-subsystems.tsv`): `10-Status-Periodic-Terminal/CONTRACT-status-write.md` (§4 invariants 1–5) and
`10-Status-Periodic-Terminal/CONTRACT-effect-layers.md` (§4 L-1..L-6). Evidence class throughout: isolated
original-code replay (Unicorn, `live_game: false`). This note scores nothing.

**Scope of the record.** EXP-086's front matter names only `CONTRACT-status-write.md`. It does not execute any of
the three bodies `CONTRACT-effect-layers.md` is about (mutate `0030E130`, rebuild `0030FED0`, merge `003847C0`):
`0030E360` has no call to `0030E130` or `003847C0` (disassembled `0030E360`..`0030E88B`, 1,323 B), and `0030FED0`
is one of its fourteen `ret`-stubs. `003848E0`, which EXP-086 runs, is the result-record initialiser, not the merge.

## Substitutions per record

Read from `_experiments/evidence/status-write-execution/check.py` (`REAL`, `STUBS`, `build_world`) and
`bodies.json` (`real_bodies_executed`, `stubbed_callees`, `globals_planted`). Only the listed pages are mapped, so any
call from a real body to an unlisted function would fault as an unmapped fetch. The 67 passing cases' only faults
are the designed data reads at VA 8, 9 and `0xC` (F2/F3) and the dispatch-bound mutant's fetch fault. (This is
inferred from the harness design; `result.json` was not re-run.)

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-086** (`evidence/status-write-execution/check.py`) | `0030E360` whole (mapped `0x30E360`+`0x5A0`, covering the body to `0030E88B` and the in-image jump/case tables at `0030E88C`/`0030E8A4`/`0030E8C4`), incl. its **recursive cascade self-call**; `0020E600` codec resolver; builders `00386A50`/`00386A70`; `003848E0` initialiser; defaults `003876D0`/`00387730`; `0016D6A0` (the image's own `ret 0` extra-effect target); `00808C40` `__security_check_cookie`; the memset thunk `00861EC0` | **Application stubs (14, `ret` at entry, rax set per case, args logged):** `0031B860` unit lookup; `0030B9B0` / `0030B8E0` eligibility gates; `00377C20` field bit15 predicate; `003112F0` applier; `00300FC0` defeat cleanup; `00312280` rewards; `00301140` recover; `003299B0` event dispatch; `00300140` / `00307D10` case-4 actions; `003284D0` reaction; `0030FED0` recompute; `0046A800` add-direction extra effect. **Import bridge:** IAT slot `008C2A60` (`VCRUNTIME140.dll!memset`, per the contract §13) → fixture `rep stosb`. **Fixtures:** `__security_cookie` `01F44830` = `0x0000DEADBEEF`; registry slot `02EBF118` → fixture header whose rows are the shipped `status_data.bin` (32×0x28) verbatim; codec base `01F83530` = 0; beat scale `01DFE0B4` = 4; `.rdata` page `008F3000` copied verbatim; target/source `BattleStatsRecord`s, one `BattleUnit` and its inner object planted per case |

## What each stub can write (static, read from the shipped image)

This bounds "reach" through a stub's *skipped behaviour*.

| stub | where its real body writes | call position relative to the invariants' reads/writes |
|---|---|---|
| `0031B860` | nowhere: callees `00236850` (7 B) and `00236820` (index `0208E6A0`, base `0208E688`, stride `0xF50`) are pure reads; its only store is the rbx home slot | `0030E39A`, `0030E3A7`, **before** the first presence read. Its return goes to `rbx` / `[rsp+0x68]` (units), never to `rsi` (the record) |
| `0030B9B0`, `0030B8E0` | own stack locals (`0030B770` stores to an aligned `rbp` frame local; `0030B7F0` to `[rsp+0x30/0x32]`), **plus a lazy singleton**: `0030B7F0` → `0017D470` → `001D50D0`, which on first use calls `00210EC0` → `malloc` (`0085E730`) for `0x10E8` bytes, constructs it with `001CCB20` and stores it at `01F81428` | `0030E42C` / `0030E44B`: after the first presence read (`0030E404`–`0030E41C`), before the mode arms. A nonzero return leaves via `0030E82D` with nothing written |
| `00377C20` | no stores (→ `003148F0` → `002EF2B0` → `002EF640`, getters) | `0030E4B6`; a zero return leaves via `0030E82D` |
| `00300FC0` | not read in full; its static closure (1,041 functions) does **not** reach `0030E360` or `0030E130` | `0030E497`, party-type early path, then `jmp 0030E82D`: **before** any mask write. Also at `0030E877` (KO / Vanished adds), after the cascade |
| `00312280` | not read; its closure **does** reach `0030E360`, only via `0030C650` → `0030FED0` | `0030E884`, after the cascade |
| `0030FED0` | calls `0030E360` at `00310409` with **mode 5** (`[rsp+0x30]=5`), flags = caller's flags **\| `0x202`** (`0030FEFB`), for each bit of `unit+0xE90`; calls `0030E130` (writes `+0x68`/`+0x78`, not `+0x38`/`+0x3C`/`+0x64`); no direct store to `+0x38`/`+0x3C`/`+0x64` in its own body. **Its callee `002FEF30` does write them:** it zeroes `rec+0x24..+0x47` at `002FEFB9`–`002FEFC8` when its output pointer is null (`002FEFAB lea rsi,[rdi+0x24]`), a span that includes `+0x38` and presence word `+0x3C`, then rebuilds it. This was found by the S-24 draft (`s24-runtime-per-invariant-exposure.md`), and the zeroing stores were confirmed here; the rebuild values were not read | `0030E828`, the **last call** before the epilogue; skipped when flags bit 9 is set, so never inside a cascade call. The `+0x3C` rewrite therefore lands after every I1–I4 read of the same call. It feeds the **next** call's presence, which no I1–I4 claim spans |
| `003112F0` | not read | `0030E638`; unreachable in the shipped build — the builders clear `result+0x2C` bit0 (`00386A66`, `00386AC3`) that the gate at `0030E610` tests (EXP-086 F1) |
| `00301140`, `003299B0`, `00300140`, `00307D10`, `003284D0`, `0046A800` | not read in full; none of their static closures reaches `0030E360` or `0030E130` (direct-edge closure over `Tools/work/graph/edges.tsv`) | all after the presence compare at `0030E5C7`; reaction/extra/terminal-dispatch sites `0030E6FF`, `0030E727`, `0030E75B`–`0030E86D` |

## Per invariant

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| status-write **I1** presence = `(+0x3C \| +0x64) & bit`; `+0x38` not part of it (`0030E404`–`0030E41C`, re-read `0030E5B7`–`0030E5C4`) | EXP-086: all six modes, incl. modes 2/5 writing `+0x38` and returning at the presence compare; mutant `0030E5BC` (`or …[+0x64]` → `[+0x38]`) detected | **no.** Both reads are of `rsi`, the record; no stub receives `rsi` before them, and only `0031B860` and the two gates run between the two reads — none writes the record (table above). The unit lookup's return feeds `rbx`, not the presence words |
| status-write **I2** no side effect fires unless presence changed (`0030E5B7`–`0030E5CB`) | EXP-086: `+0x38`-only writes and already-present-in-other-word cases fire no stub after the compare | **no, for the compare.** It is body-local and precedes every post-write stub; the stubs' returns can only *suppress* later side effects (gates refuse before the write; a null unit skips reaction and terminal dispatch), never make one fire. **But see finding F-1:** the party-type early path fires `00300FC0` with no mask write, and EXP-086 executed it |
| status-write **I3** every mode refuses when the bit is already in the requested state | EXP-086: per-mode already-in-state refusals; mutant `0030E4F4` (`not eax` → `xchg`) detected | **no.** Each arm's `test` and its store are adjacent (`0030E4E7`–`0030E4F8`, …, `0030E557`–`0030E564`) with no call between. The gate / predicate stubs run earlier and only choose whether the arms are reached at all |
| status-write **I4** the cascade cannot recurse indefinitely: each cascade call is `mode 0` and refused when absent | EXP-086: KO mask → 25 inner calls, Stone → 12; mutant `0030E6B1` (`bts eax,9` → `8`) detected | **no, in the replay** — the call's args (`[rsp+0x30]=0` mode, `bts … 9` flags at `0030E6AE`, `0030E6C7`) are body-local and the self-call is real. **Stubs are re-entry points the replay cannot see**, bounded statically: of the fourteen, only `0030FED0` and `00312280` (through `0030C650` → `0030FED0`) reach `0030E360`, and `0030FED0` re-enters with mode 5 and flags `\|0x202`. A mode-5 call writes only `+0x38`, so by I1 it returns at the presence compare before the cascade, and bit 9 stops any further recompute. The bound therefore also holds on the static reading of the stubbed paths. Not executed |
| status-write **I5** the operation never allocates; the result record is a stack block | EXP-086: the record is `[rsp+0x80]`, `memset` over `0x148` at `0030E5E1`, and the real bodies called nothing outside the mapped set | **body-level: no** — the only substitution on the result block is the memset **import bridge** (value-identical semantics). **Transitive reading: exposed.** The stubbed gates' real chain lazily allocates (`001D50EE` → `00210EC0` → `malloc` `0085E730`, `0x10E8` B, guarded by `01F81428 == 0`); the other stubs' allocation behaviour is **not read**. Which reading I5 means is not stated in the contract |
| effect-layers **L-1** rebuild touches `+0x78` only | **not by EXP-086** (`0030FED0` is a stub) | coverage, not exposure |
| effect-layers **L-2** mutate `0030E130` is the only writer of both layers | **not by EXP-086** (never called by `0030E360`) | coverage, not exposure |
| effect-layers **L-3** merge `003847C0` is whole-range and lossy | **no record in `_experiments/` names `003847C0`** (grep of records, `check.py` and `bodies.json`) | coverage, not exposure |
| effect-layers **L-4** the observable alias | not executed (follows L-3) | coverage, not exposure |
| effect-layers **L-5** id 15 revoked after the merge (`0038488C`–`003848B8`) | not executed | coverage, not exposure |
| effect-layers **L-6** derived layer reconciled, not accumulated | not executed by EXP-086; the contract itself says it is "not re-measured" | coverage, not exposure |

## Findings and contradictions

- **F-1 — I2's wording vs §10 row 3, and EXP-086 ran the counter-case.** I2 says no side effect fires unless
  presence changed. §10 row 3 and EXP-086 ("Party-type early path") both show `00300FC0 defeat_cleanup(unit, 0)`
  firing at `0030E497` and returning at `0030E49C` **before any mask write**, so presence cannot have changed.
  Either I2 is scoped to the post-write pipeline (`0030E5B7` onward) and should say so, or it is contradicted by its
  own contract. This is a wording question, not a stub exposure.
- **F-2 — the contract's §13 says "Only `memset` is scripted … Everything else runs".** That is true of the
  differential pilot `diff_status_write.py`'s five bodies. It is **not** true of EXP-086, listed in the same table,
  which `ret`-stubs fourteen application callees. The sentence sits under both rows.
- **F-3 — the effect-layers contract's §13 ("None. No experiment executes these three bodies") is partly stale
  outside this row's cell.** `0030E130` and `0030FED0` run as shipped in EXP-100, EXP-104, EXP-148 and EXP-160
  (contracts `CONTRACT-auto-status-rebuild.md` and `CONTRACT-apply-result-to-target.md`). Those records are not
  named in S-26's runtime cell; their stubs and whether they measure L-1/L-2/L-6 were **not read** here. The merge
  `003847C0` is executed nowhere.
- **Binding gap is stale against the row's own cells.** "types PARTIAL" — the types cell reads MET (re-scored
  2026-09-25). "nothing executed" — the runtime cell names EXP-086, which executes `0030E360`. It stays true only
  for `CONTRACT-effect-layers.md`'s three bodies within this row's records.
- The `bodies.json` span for `0030E360` is given as `0x30E360-0x30E84F`. The body runs to `0030E88B` (the KO /
  Stone / Vanished tail at `0030E850`–`0030E889`). The harness maps `0x5A0` bytes, so the tail **was** executed;
  only the stated span is short.

## For the scorer

- EXP-086 substitutes **14 application stubs**, **1 import bridge** (memset, IAT `008C2A60`) and **fixtures**
  (cookie, registry → shipped `status_data.bin` rows, codec base, beat scale, records, unit).
- **Status-write I1–I4: no substitution reaches the asserted value or ordering.** The stubs' returns choose
  refusal-vs-continue and whether post-write side effects run; they do not write the record words the invariants
  test. Static re-entry through `0030FED0` (and `00312280` → `0030C650` → `0030FED0`) uses mode 5 with flags
  `|0x202`, which returns at the presence compare.
- **Across calls, not within one:** the stubbed recompute's callee `002FEF30` zeroes and rebuilds `+0x24..+0x47`,
  which includes presence word `+0x3C`. It does so after every read in the same call, so it can change the presence
  the **next** status write sees. No I1–I4 claim spans two calls.
- **I5:** body-level not reached (import-class only). A transitive reading is exposed to the stubbed gates' lazy
  `malloc` (`001D50EE`); other stubs' allocations not read.
- **Effect-layers L-1..L-6: none executed by the row's record.** This is coverage, not exposure. `0030E130` /
  `0030FED0` run in four other contracts' records (not read here); `003847C0` runs in none.
- Contradictions: F-1 (I2 vs §10 row 3), F-2 (status-write §13 "only memset is scripted"), F-3 (effect-layers §13),
  and the binding-gap text (both halves stale for the status-write contract).
- `live_game` is false; nothing here is live.
