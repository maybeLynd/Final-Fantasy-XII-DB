# S-24 runtime: per-invariant stub exposure for EXP-100..104 (+ EXP-092) (OPUS, 2026-09-25, block 305)

*Drafted by a delegated OPUS pass and reviewed before publication (block 305): its concrete address claims were spot-checked against the image; see the block-305 inbox entry for which.*

**Row:** S-24, stat derivation and auto-status.
- **Runtime:** MIXED. The cell reads: *"the auto-status family executed under isolated original-code replay: gate
  chain (EXP-100), unit resolvers (101/102), Notify `002FEF30` (103), Sinks … (104); EXP-092's bazaar callees
  belong to S-30's surface … no per-invariant stub-exposure analysis yet"*.
- **Binding gap:** *"types PARTIAL and nothing executed — runtime is ASTRA/ORACLE's gap; the contract no longer
  binds it"*.
- **Contracts** (column 6 of `important-subsystems.tsv`):
  - `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md`. Its §4 has no preconditions; the derived-set
    invariant; the "exactly once per changed bit" postcondition; the "corrected by execution" `+0x78` statement;
    and the §7a after-effects that §4 imports.
  - `08-Combat-Formula/CONTRACT-stat-derivation.md` (D-1..D-7, body `002FEF30`).

Evidence class throughout: isolated original-code replay (Unicorn, `live_game: false`), plus static reading. This
note scores nothing. The probe is `s24-probes/s24_rebuild_callee_reach.py`, with its output in
`s24-probes/s24_rebuild_callee_reach.out.txt`.

## Substitutions per record

Each record was read from its `check.py` stub/hook tables and its record text. EXP-100's `World` and `on_call` were
read in full. For EXP-101..104 the constants/stub tables, the record tables and selected cases were read, not every
hook body.

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-100** `evidence/auto-status-gates-exec/check.py` (whole image mapped from the EXE's sections) | rebuild `0030FED0`; `0020E600`; `00322C50` (arm 6); `0031E9A0` / `0031E9F0`; `00323890` / `003241D0`; `00808C40` | **Application stubs** (`STUBS`, `ret` at entry; `on_call` sets `rax`): FIND `0031B860` (returns the planted unit), **APPLY `0030E130`**, CASCADE `0030E360`, **NOTIFY `002FEF30`**, TAIL `0030E060`. **Fixtures:** `[01F83530]` → IMG32 arena; registry slots `02EBF130` / `02EBF0F8` / `02EBF038` → synthetic headers and rows; record, unit and spawn. **No import bridge is reached** (APPLY is stubbed, so memset is not reached) |
| **EXP-101** `evidence/find-owning-unit-exec/check.py` | FIND `0031B860` + `00236850` / `00236820` | **none.** Fixtures: pool globals `0208E688` / `0208E6A0` and units |
| **EXP-102** `evidence/unit-resolver-family-exec/check.py` | 17 resolver-family bodies (incl. `00322C50`, `00309440`, `003588B0`) | **none.** Fixtures: pool, family and registry globals |
| **EXP-103** `evidence/autostatus-notify-exec/check.py` | **stat derivation `002FEF30` (all 2,859 B)** + `002F8E50`, `002F9180`, `0031B860`, `00236850`, `00236820`, `00322C50`, `0031E9A0`, `0031E9F0`, `00309440`, `0020E600` | **Application stubs** (entry-stubbed, `rcx` captured): RESET `003105D0` (call site `002FF9C7`) and SINK `00307D10` (call site `002FFA40`). The harness names `00307D10` "APPLY" (`check.py` line 27); it is not EXP-100/104's APPLY `0030E130`. **Fixtures:** registry slots `02EBF130` / `120` / `148` / `140` / `150` / `0F8` / `040` (+ decoy twins), resolver base, record, unit and pool. The bitmask walks read the **real** `.rdata` tables `00D10290` / `2A0` / `2B0`. **No import bridge**; the zeroing at `002FEFB9`–`002FEFC8` is inline |
| **EXP-104** `evidence/autostatus-sinks-exec/check.py` | the five sink subjects `00307D10`, `0030E060`, `003105D0`, `0030E130`, `0030E360`, plus 29 resolver bodies. "Quiet" real bodies, including **the rebuild `0030FED0` nested under APPLY/CASCADE**. Per the record's table, **`002FEF30` runs real nested** under the rebuild | **Application stubs (ret-0):** `0024FE30`, `00300FC0`, `0017D470`, **`003112F0`**, `0033E1F0`, `003BBD00` (arg capture). **Value stubs** (return from `case["qret"]`): `0030B9B0`, `0030B8E0`, `00387730`, `003876D0`, `00300140`, `00301140`, `00312280`, `003299B0`, `003284D0`, `0046A800`, and **`00384B10`** (an application body whose value comes from `rand`, IAT `008C3098`). **Entry intercept of an application body:** `003A1920`, whose own `subss`/`mulss`/`addss` distance arithmetic is replaced by the harness before it tail-jumps to sqrtf. **Import bridges:** `00861EC0` → IAT `008C2A60` memset, and `00861F14` → IAT `008C2BB8` (`api-ms-win-crt-math!sqrtf`, resolved). **Fixtures:** pool, family, registry and table globals (`02EBF040` / `118` / `130` / `190`, …) |
| **EXP-092** `evidence/bazaar-callees-exec/check.py` | 16 bazaar / inventory bodies | **none** (fixtures only). Read in S-30's note. It runs `00322C50` arms 1 and `0x12` only. S-24's code uses arm 6 (equipment) and arm `0x1D` (APPLY's gate), so it **touches no S-24 invariant**. The cell's "belongs to S-30" is correct |

## Where the stubbed callees sit in the rebuild `0030FED0` (static)

The rebuild's call order, with each call's reach:

| order | site | call | real behaviour that reaches later rebuild reads |
|---|---|---|---|
| 1 | `00310023` | FIND | its return selects the unit whose `+0xE80` is the kind-1 source |
| 2 | `00310378` / `00310396` | **APPLY** per changed bit | **writes the derived set**: `+0x78` via `bts` at `0030E20E`/`0030E212` (action 3) and `btr` at `0030E235`/`0030E239` (action 1). The gate is `00322C50(0x1D, idx)`. Re-entry into `0030FED0` at `0030E329` is skipped: `bt r12d,9` at `0030E31C`, and the rebuild passes flags `\| 0x202` (`0030FEFB`). The apply loop reads the stack masks (`rsp+0x50` / `0x60`), never `+0x78` |
| 3 | `003103AD` | **NOTIFY** `002FEF30(rec,0,0)` | `rsi = rec+0x24` (`002FEFAB`). **It zeroes `rec+0x24..0x47`** (`002FEFB9`–`002FEFC8`) and rebuilds that range: `[rsi]` = `+0x24` (`002FF7E2` / `002FF805`), `[rsi+4]` = `+0x28` (`002FF824`), `+0x13` = `+0x37` (`002FF89F`), `+0x14` / `+0x18` = the status words **`+0x38` / `+0x3C`** (`002FF0D3`/`D9`, `002FF510`/`1E`), and `+0x1C..0x20` = `+0x40..0x44` |
| 4 | `00310409` | CASCADE ×bits of `unit+0xE90`, mode 5, flags `\| 0x202` | writes `+0x38` only, then returns at the presence compare (S-26 note) |
| 5 | `00310433`… | spawn exchange of `rec+0x40..44` ↔ `spawn+0x78..7C` | — |
| 6 | `003104BF`–`00310594` | clamps | read `+0x64 \| +0x3C` (presence), **`+0x24`** (the HP cap), **`+0x28`** (the MP / `+0x06` cap), **`+0x37`**, `+0x6C`, `+0x7C` |
| 7 | `0031059C` | TAIL | last call |

## Probe (counterfactual, measured)

`s24_rebuild_callee_reach.py` reuses EXP-100's `World` read-only; `sys.dont_write_bytecode` is set, so no cache is
written into the evidence directory. It runs the shipped `0030FED0` three ways:
- **STUB:** EXP-100's stub set.
- **APPLY:** `0030E130` real, with its closure real. It adds two import bridges (memset IAT `008C2A60`, rand IAT
  `008C3098`), a logged ret-0 application stub at `003112F0`, and a fixture `[02EBF040]` with count `0x80`.
- **NOTIFY:** `002FEF30` real.

**All 10 runs reached the return sentinel.** Each had final RIP `62000000` = `RETQ`, `rax = 0`, no emulator error
and an empty fault list.

| case (EXP-100 fixture) | config | `+0x78` on return | `+0x24` | `+0x28` | hp `+0x48` | mp `+0x4C` | notes |
|---|---|---|---|---|---|---|---|
| `diff-add-rem` (prior `0x0F`, acc `0x03`) | STUB | `0f…` | | | | | APPLY entered 2×, no `+0x78` write |
| | APPLY | **`03…`** = acc | | | | | `btr` writes at `0030E239` (→ `0x0B`, → `0x03`); `00386A50` ×2 |
| `def-masks` (acc bits 0, 2, 32, 33) | STUB | `00…` | | | | | APPLY 4× |
| | APPLY | **`05000000 03…`** = acc | | | | | `bts` at `0030E212` ×4; `00386AE0` ×4; **`003112F0` not entered** (no `3112F0` count) |
| `clamp-hp` (hp 100, planted cap 50) | STUB | | 50 | | **50** | | |
| | NOTIFY | | **1** | | **1** | | NOTIFY rewrote the cap before the clamp |
| hp 100, planted cap 500 | STUB | | 500 | | **100** | | |
| | NOTIFY | | **1** | | **1** | | |
| `clamp-mp` (mp 100, planted `+0x28` = 32) | STUB | | | 32 | | **32** | |
| | NOTIFY | | | **0** | | **0** | |

The NOTIFY values (cap 1, `+0x28` 0) are what NOTIFY computes from EXP-100's near-empty definition rows; they are
not game values. The probe shows only **that** the operand changes, not what it is in a game.

## Per invariant

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| auto-status **no preconditions** (record unchecked before the loops) | EXP-100 finding 10 (`rcx = 0` survivable on the fixture's zero page) | **no** |
| auto-status **invariant: the derived set is a pure function of its sources**; nothing adds to `+0x78` incrementally | EXP-100 (accumulation observed through the APPLY tokens); EXP-104 nested (`apply-set78`: real FED re-clears the bit the outer APPLY set) | **the accumulation: no** — the equipment, licence and definition-row loops write only the stack. The kind-1 source unit comes from the FIND stub (FIND runs real in EXP-101 and 104). **The `+0x78` value itself is exposed to the APPLY stub in EXP-100**, where no `+0x78` write happens at all. The probe with APPLY real gives `+0x78` = acc |
| auto-status **postcondition: `0030E130` called exactly once per changed bit** | EXP-100 (`diff-add-rem`, `diff-all-rem`: tokens `A<bit>+1/3`) | **no, for the rebuild's own calls.** The loop is driven by stack masks computed before the first call, and real APPLY cannot re-enter the rebuild (bit 9). **Open static path:** on the add path, if builder `00386AE0` leaves `result+0x2C` bit0 set, APPLY calls `003112F0`, which calls `0030FED0` at `00311AC5` with `edx = 0`. That would make nested rebuild calls. It was not reached on EXP-100's fixture (probe: 0 entries), and it is stubbed in EXP-104. The builder's path condition was **not read** |
| auto-status §4 **"Corrected … by execution: `+0x78` does NOT equal the accumulation when this function returns"** | the pilot and EXP-100, both with APPLY scripted | **reached — it is a product of the APPLY stub.** With APPLY real (probe), `+0x78` **equals** the accumulation on return, in both an add and a remove case. EXP-104's `apply-set78` agrees under its own stubs. What stays true is the narrower sentence beside it: the rebuild's own instructions never assign `+0x78`; APPLY's `0030E212` / `0030E239` do |
| auto-status §4/§7a **"current HP, current MP and `+0x06` have each been clamped and written"** | EXP-100 `clamp-*` (relation executed) | **relation: no. Cap operands: yes, NOTIFY.** The clamps read `+0x24` / `+0x28` / `+0x37` and presence `+0x3C`, all of which the real NOTIFY rewrites at `003103AD` before `003104BF`. In EXP-100 they are planted values that the real flow would overwrite (probe: hp 50 → 1, 100 → 1; mp 32 → 0). EXP-100 finding 8 therefore measured the clamp against fixture caps |
| §7a: **spawn exchange** in both directions | EXP-100 `k1-spawn-in` / `k1-spawn-out` | **direction: no. Copied bytes: yes, NOTIFY** — `rec+0x40..44` is NOTIFY's `out[0x1C..0x20]` (rowD for kind ≠ 0), and the rec → spawn direction copies what NOTIFY wrote. Not probed |
| §7a: **mode-5 pass over `unit+0xE90`** | EXP-100 `k1-mask-cascade` (args `mode 5`, flags `\|0x202`) | **no**; the call arguments are body-local. Real CASCADE writes only `+0x38`, which no later rebuild read uses |
| stat derivation **D-1** one kind byte selects the path | EXP-103: `kind0-*`, `kind1-four-rows`; mutant `m-kind-off` `002FEFFE` | **no** — both stubs sit in the tail |
| **D-2** all clamps in `002FF7B1`–`002FF8D6` | EXP-103 `kind0-clamps`, `kind0-cap7fff`; mutants `m-clamp63` `002FF82B`, `m-cap7fff` `002FF7F7` | **no** — RESET and SINK run after the block |
| **D-3** one `cmove` party/foe cap | EXP-103: `kind1-four-rows` stores `out[0]` = `0x2810F9E0` (> 9,999, the 1e9 side); `kind0-noband-cap` | **no.** Whether a kind-0 case pins the 9,999 upper cap was **not read** |
| **D-4** `0x7FFF` second write | EXP-103 `kind0-cap7fff` (`out[0]` = `0x51EB`) | **no** |
| **D-5** statuses count from either layer, three pairs | EXP-103 `kind0-bitmask` plants bits **only in `+0x68`** (`check.py` 1084–1088) | **no substitution. Partial coverage:** the `+0x78`-only arm (`002FF5D1` / `002FF66F` / `002FF70F` taken) is never driven, so the "either layer" half via `+0x78` is unexecuted |
| **D-6** `+0x15` bits 0/1 gate base term and equipment term together | EXP-103 `kind1-flag4c-off`, `kind1-flag70-off` | **no** |
| **D-7** "its tail always runs": clears at `002FFA14` / `002FFA22`, `[unit+4] \|= 0x200000` at `002FFA38`, `call 00307D10` at `002FFA40` | EXP-103 `kind0-reset-runs` (tail taken); `kind0-find-miss-tailskip`, `kind0-rdx-tailskip`, `kind0-nodiff` (tail **not** taken: `u_flags = 0`, no `X` / `A` token) | **no stub reach.** RESET (`002FF9C7`) precedes every D-7 store, which overwrite or mask the same fields afterwards; SINK is the last call. **But the claim is contradicted by the bytes and by EXP-103** — see F-2 |

## Findings and contradictions

- **F-1 — the auto-status contract's "corrected by execution" `+0x78` sentence reflects the APPLY stub.**
  - It was measured with APPLY scripted (pilot and EXP-100).
  - With the shipped APPLY, `+0x78` equals the accumulation on return (probe; EXP-104 `apply-set78`).
  - The failing control ("copies the accumulation back … failed on 19 of 719 lines") compared against a stubbed
    applier.
- **F-2 — D-7 is contradicted.** Everything D-7 lists sits behind one gate at `002FF970`–`002FF98E`:
  1. `test edi,edi / jne 002FFA45`, where `edi = [rsp+0x3C]`, the kind flag also used by the D-3 `cmove`;
  2. `cmp [rsp+0x64], ebp / je` (FIND found a unit with `rdx == 0`);
  3. `test (out[0x18] ^ entry[+0x3C]), 0x8000020 / je`.

  That covers the `002FFA14` / `002FFA22` clears, the `0x200000` set at `002FFA38` and `call 00307D10` at `002FFA40`.
  So on a foe, on a FIND miss, with an explicit out pointer, or with no change in those two status bits, none of it
  runs. EXP-103's three tail-skip cases measure this. §2's "always ends `call 00307D10`" is contradicted the same way.
  The RESET call also carries a fourth gate (`002FF99C`–`002FF9C2`).
- **F-3 — the stat-derivation §13 ("None. No experiment executes `002FEF30`") is stale.** EXP-103 runs it as the
  subject, and EXP-104 runs it nested. The sibling auto-status contract already consumes EXP-103 in its §13b, so
  the two contracts disagree.
- **F-4 — the auto-status §4 says the derived set is "a pure function of its *three* sources".** Its own §5/§7 give a
  kind-dependent source: kind 1 reads `unit+0xE80` instead of the definition row. This is wording, not exposure.
- **F-5 — NOTIFY zeroes and rebuilds the status words `+0x38` / `+0x3C`** (it OR-s in authored and equipment masks)
  on every rebuild. That is outside this row's invariants; it bears on the status-write contract's reading of those
  words (S-26), and is noted only.
- **Binding gap is stale on both halves.** The types cell reads MET (re-scored 2026-09-25). "nothing executed":
  `0030FED0` (EXP-100) and `002FEF30` (EXP-103) run as shipped.
- **EXP-104 naming:** `003A1920` is called an "IAT tail-jump" intercept. It is an **application** body whose
  vector arithmetic is replaced along with the `sqrtf` import it tail-jumps to. It sits on TAIL's RNG path, which is
  outside S-24's invariants.

## For the scorer

- **EXP-100:** 5 application stubs (FIND, APPLY, CASCADE, NOTIFY, TAIL) and fixtures; no import bridge reached.
- **EXP-101 / EXP-102:** zero stubs.
- **EXP-103:** 2 application stubs (RESET, SINK), both after every D-invariant store; no import bridge.
- **EXP-104:** 6 ret-0 and 11 value application stubs, 1 intercepted application body, and 2 import bridges
  (memset, sqrtf).
- **EXP-092:** zero stubs, and not an S-24 record.
- **Stat derivation D-1..D-7: no substitution reaches any claimed value or order.**
  - Coverage gap: D-5's `+0x78`-only arm is not driven.
  - D-7 as worded is contradicted by `002FF970`–`002FF98E` and by EXP-103's tail-skip cases.
- **Auto-status: two application stubs reach claimed values, both measured by the probe.**
  - **APPLY `0030E130`** reaches the §4 "`+0x78` ≠ accumulation" statement: with it real, `+0x78` = accumulation.
  - **NOTIFY `002FEF30`** reaches the §7a clamp operands (`+0x24` / `+0x28` / `+0x37` / `+0x3C`): hp 50 → 1,
    100 → 1; mp 32 → 0.
  - It also reaches the spawn-exchange bytes; that was not probed.
  - The "once per changed bit" postcondition and the derived-set invariant's accumulation are not reached. One open
    static path remains: `00386AE0` → `003112F0` → `0030FED0` at `00311AC5`, not reached on EXP-100's fixture.
- **Not read:** every EXP-104 hook body; `00386AE0`'s path condition for keeping bit0; whether a kind-0 EXP-103 case
  pins the 9,999 cap.
- `live_game` is false for all six records.
