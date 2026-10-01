# S-45 runtime: per-invariant stub exposure for EXP-089 (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-45 Steam and achievements. Runtime **MIXED**, qualifier *"isolated original-code execution under
disclosed stubs — no per-invariant stub-exposure analysis yet"*. Binding gap: *"~~the counter is contracted;
Steam integration is not~~ — Steam integration contracted at `699c743c8` and verified (see contract cell)"*.
Contracts: column 6 of `important-subsystems.tsv` lists **only**
`20-Platform-Online-Achievements/CONTRACT-achievement-counters.md`. The row's contract cell also relies on
`20-Platform-Online-Achievements/CONTRACT-steam-integration-subsystem.md` (exists; `git log -1 699c743c8` =
*"FABLE: CONTRACT-steam-integration-subsystem - S-45's Steam integration…"*; §7 invariants I-1..I-6). Both are
analysed below. This note scores nothing.

The one record is **EXP-089** (`evidence/achievement-evaluate-award/check.py`, 54 cases + 9 mutants, `result.json`
keys counted). Its own text says *"Isolated original-code evidence under Unicorn; no NATIVE-REPLAY or live
claims"*; the cell calls it "isolated original-code replay". No live record exists for either contract.

## Substitutions per record

| record | runs as shipped (`bodies.json` `real_bodies_executed`, 29) | substituted |
|---|---|---|
| **EXP-089** | the whole counter family `00316A50` update, `00316BF0` store, `003166F0` read, `00316760` lookup, `00315E90` evaluate, `003165C0` fire helper; `002536A0`/`002536D0`/`00254E80`/`00320D50` (save base, playtime), `00282DD0`/`00282FA0` (inventory), `00309EC0`→`002FD970` (family resolver, via the shipped `jmp [entry+0x50]`), `00315420`/`003160C0`/`003161A0` (mode 7/5/6), `00264790`/`00265270`/`003148F0`/`002EF2B0`/`002EF640`/`003779F0`/`003C4AD0`/`00255060`/`00255120`, and the Steam-side award path **`008632B0` → `0020CE00` → `0020CE60`**. Shipped tables used real: descriptors `00D10460`, award codes `00D10550`, jump table `00316098`, family table `01EEBCC0` counts `+0x3C` / fnptrs `+0x50` | see table below |

| substitution | where | class | effect |
|---|---|---|---|
| IAT slot **`008C3190`** | `0020CE60` at `0020CEA2` and `0020CEBC` (`call qword [rip+…]`, `rcx = lea 01DFE0D0`) | **import bridge** — resolved from the PE import directory: `steam_api64.dll!SteamInternal_ContextInit`. (The harness and record call it a "name→object getter" and trace `wstr(rcx)`; `rcx` is the context `01DFE0D0`, not a name.) The real import would also run the application init callback `001F3E10` stored at `[01DFE0D0]` (zero-fills the context, then calls IAT `008C31A0`) on first use; that callback is skipped with it | returns planted `OBJA` whose `+0x28` → `OBJB` (the user-stats interface pointer) |
| `OBJB` vtable **`+0x38`**, **`+0x50`** | `0020CEB2 call [rax+0x38]`, `0020CED2 jmp [rax+0x50]` | **import-side** (methods of an object handed back by the Steam import, not application code in the image); logging stubs returning 1 | Steam-side effect of SetAchievement / StoreStats (slot meanings per the Steam contract §5; MEANING NOT CLAIMED by execution) |
| every other IAT slot | — | trap page: any call stops emulation and records a fault. All 54 cases report `faults: []`, `trapped: []` | none reached |
| family-3 entry `+8` pointer | `01EEBCC0 + 3*0x58 + 8` → fixture u16 bitset | **fixture** (zero on disk, runtime-initialised; record F6) | feeds `002FD970`'s bit test → the **mode-2 evaluate arm's** all-present decision only |
| `[01F83450]` manager | planted `POBJ` with `+0x08` → `AWTBL` (stride `0x198`), `+0x18` = case's `pobj_flag` (default 0); `0` in `award-null-pobj` | **fixture** in scope by the Steam contract's own §2 layout (the real manager is made by `0020CD30`, not run) | selects `0020CE60`'s arms |
| save image `[020927C0]` and other globals (playtime, frame, inventory, u16 table, chain root `[022C2550]`, gate/ptr cells) | planted | fixture; the save block `+0x3844` is the counter contract's own `AchievementState` | inputs |
| descriptor byte patches (`eval-mode1/4-dead-patched`, `eval-mode8-reject`, `upd-mode8-skip`) | `00D10460 + id*8 + 2` | disclosed image patch (fixture) | mode selection in those cases only |

No application function in the image is stubbed.

## Per invariant — achievement counters (§4, plus the §2 ordering box)

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| **AC-bound** "id bounded at 30 before anything else, in all three entry points" | update `00316A50` (`upd-id-bound`: id 30 rejected, trace `[update]`); evaluate `00315E90` (`eval-id31-bound`, `eval-id30-alias`, mutant `00315E92`). **The read `003166F0`'s bound and the store `00316BF0`'s bound are not driven by EXP-089** (every lookup case uses ids 0/5/6/8/18; the store is reached only behind update's bound) | **no** — the bound tests are the first instructions of the real bodies; no substitution precedes them |
| **AC-nowrap** counter saturates at the signed max of its width, tested before the add; other kinds add unclamped | `upd-sat-word` (id 0, kind 2: `0x7FFFFFF0` → `0x7FFF`), `upd-neg-clamp`, mutant `00316B97`. **Kind 4 (`0x7FFFFFFF`, `00316BA9`) is not driven**: no UPDATE case uses a kind-4 id (shipped kind-4 ids are 6, 7, 11, 17; update cases use ids 0, 13, 18, 19). **The unclamped fall-through (`00316BBB`) is not driven** | **no** — `00316A50`/`00316BF0`/`003166F0`/`002536A0` all real; the only substitutions sit after the store (award tail) or inside the mode-2 evaluate arm |
| **AC-order** (§2 box) evaluate sees the pre-update counter; award lands one update late | `upd-order-first`, `upd-order-real` (trace `eval` before `store`) | **no** — the ordering is two real call sites (`00316BC1`, `00316BCC`); the substituted import/vtable run inside `0020CE60`, after the award decision |

## Per invariant — Steam integration (§7)

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| **I-1** Init fails → `[01F83450]` null → every by-index award returns at the null check | **consequence half** executed: `award-null-pobj` (planted null) — trace ends `awardtail, pobjget`, i.e. `008632B0` returns at `008632C0 je` after one `0020CE00`. The Init/creation half (`007980A0`, `0020CD30`) and the one-writer claim are **not executed** (static) | **no** — the null test precedes any substituted call |
| **I-2** no send before `+0x18`; 1101 then overwrites the local flags | **first half** executed: 14 award-reaching cases with planted `+0x18 = 0` set the entry flag and make **no** `SteamInternal_ContextInit` / vtable call (traces in `result.json`); `award-obj-flag` (`+0x18 = 1`) makes `nameobj → vt_238 → nameobj → vt_250`. The absence in the 14 cases is visible in the traces but asserted by no check. **Second half (1101 `0020C940` overwrite) not executed** | **no** — `cmp byte [rcx+0x18],0` / `je` at `0020CE8C`/`0020CE99` precedes both substituted calls; the substitutions cannot change whether a send happens. The flag's value is a fixture (the real writer `0020C940` is not run) |
| **I-3** already-achieved entry (`+0x190`) → no Steam call | **not executed** — no case pre-sets any entry's `+0x190` (`AWTBL` is zero heap; the harness only reads it back). `eval-awarded-early` is a different gate (the save bitset at `saveBase+0x3844`, `00315EDF`), not `0020CE72` | coverage, not exposure |
| **I-4** entry 0 awarded only by the receipt handlers | not executed (`0020C940`, `0020C8C0`, `0020CE10` not run) | coverage |
| **I-5** `SteamAPI_RunCallbacks` only in the window pump `007A3110` | not executed (static census) | coverage |
| **I-6** RestartAppIfNecessary true → `exit(1)` | not executed (`007980A0` not run) | coverage |

## Contradictions found

1. **Counter contract §4 vs its own box and EXP-089.** §4 still says the id is *"bounded at 30 before anything
   else happens, in all three entry points"* and cites *"`cmp esi, 0x1e` / `jae` at `00315EB0`"* for evaluate.
   Disassembled: `00315E90 cmp cl,0x1f` / `00315E93 jae` is evaluate's entry bound; the `00315EB0` `jae` goes to
   `00315EE5` (the mode dispatch) and skips only the awarded-bit test. EXP-089 `eval-id30-alias` executes id 30
   through the dispatch. The contract's later box (*"THE TWO BOUNDS ARE DIFFERENT…"*, ~line 146) records this,
   but the §4 sentence was not amended.
2. **EXP-089 record vs its harness.** The record lists *"kind4 at `0x7FFFFFFF`"* among the executed update
   rules; `check.py` has no kind-4 update case (see AC-nowrap). The kind-4 cap was driven by the contract's
   §13 differential (`diff_achievement_counters.py`), which is not an EXP record and is not named in the
   runtime cell.
3. **Contract set.** `important-subsystems.tsv` column 6 for S-45 lists only the counter contract, while the
   row's contract/types cells score on the Steam contract (`699c743c8`) too.
4. **Binding gap is stale as a gap statement.** It strikes the old gap and restates the contract verification;
   it names no remaining gap, while the row is NOT MET on runtime.

## For the scorer

- **Exposure: import-class only.** EXP-089's substitutions are the `steam_api64.dll!SteamInternal_ContextInit`
  import (`008C3190`) and the two methods of the object it returns (`+0x38`, `+0x50`); both sit after
  `0020CE60`'s `+0x190` write and `+0x18` test. No application function is stubbed. The fam3 `+8` fixture
  reaches only the mode-2 evaluate arm's decision, which no §4 invariant of either contract covers.
- **Counter contract:** all three claims executed with no substitution in reach; **coverage holes**: the
  read/store id bounds and the kind-4 / unclamped-kind saturation arms are not driven by EXP-089.
- **Steam contract:** I-1 (null-manager consequence) and I-2 (first half) executed with no substitution in
  reach, on a planted manager; **I-3, I-4, I-5, I-6 and I-2's receipt half are not executed**; start-up
  (`007980A0`), the pump (`007A3110`) and the receipt handlers are not in any record.
- No live evidence on this row.
- Not read: the contract's §13 differential harness (`diff_achievement_counters.py`) — it is not a runtime-cell
  record; `001F3E10` beyond its first 0x80 bytes; IAT `008C31A0`'s name.
