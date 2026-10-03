# SWE2-AUDIT-SEM independent L2 sample of the MET verdicts, 2026-10-03

*Requested by the user's package `Database/Tools/work/FABLE/FFXII_INDEPENDENT_CORPUS_AUDIT_FOLLOWUP_2026-10-03.md`
§6 (constraints §11). Lane: SWE2-AUDIT-SEM (Claude stand-in for the offline Devin session). Measured at HEAD
`8fabf1300`, EXE `73461d08…`. A second auditor takes the other §6 families.*

## SWE2-AUDIT-SEM outcome in one paragraph

**The sample does not survive unqualified.** Of six high-blast-radius MET systems:
- none is ACCEPT as written;
- four are **ACCEPT-WITH-NARROWING**: S-02, S-13, S-28, S-43;
- two are **REJECT**:
  - S-36: a reverted correction leaves a wrong invariant at HEAD, and the router state is undeclared;
  - S-49: a contract-named state item is undeclared, the same defect S-46 was held PARTIAL for.

**No byte-level claim re-derived in this audit was wrong.** The failures are in what the verdict cells *say*, and in how the scoring instruments *measure*. Six systemic patterns (see §"Systemic findings") recur across all six systems. Three of them have measurable reach beyond the sample:
- 15 of 52 runtime cells rest on denominator rulings;
- 5 literal-pass harness records exist in 4 packages;
- a stale-preimage batch publish silently reverted a FABLE correction.

**Recommendation: expand the audit before terminal certification** (§10 "risk-based independent L2 sample survives" is NOT satisfied).

## SWE2-AUDIT-SEM method

For each sampled system:
1. Read the registry row (`_index/important-subsystems.tsv`), the verdict row (`_index/L2-VERDICTS.md`, table lines 238–289), the primary pages and every credited contract.
2. Resolve the named state against `_types/types.tsv` and `_types/fields.tsv`.
3. Read the replay or differential harness **code**, not its README, and compare each case with the invariant it is credited for.
4. Re-run harnesses from scratch copies where cheap. Each run reproduced its published md5; the repo was confirmed unchanged afterwards.
5. Re-derive load-bearing claims from the image with `disr.py` (from `Database/Tools/work/FABLE/pub140-scratch`) and with raw sweeps. The sweeps covered rel32 call/jmp/jcc, rip-relative, image-base-relative disp32 and abs64, each with a positive control.

Per-system work was split among read-only helper agents. Every finding used in a verdict below was spot-checked by the coordinating session, and those checks are listed under each system.

Verdicts use the vocabulary of `_index/_inbox/REVIEW-POLICY.md`. Rules applied:
- the types criterion as ruled 2026-09-21 (`L2-VERDICTS.md:2764`ff), including the S-46 precedent "measured-address enumerations count";
- the runtime criterion as ruled 2026-09-25 (`L2-VERDICTS.md:2859`ff);
- `EVIDENCE-POLICY.md` rules 4a and 8.

Helper scripts in this directory (absolute paths inside; read-only):
- `cells.py`: mirrors `goal_gate.check_verdicts` and prints each row's five requirement cells;
- `who.py`: the lane attributed in each cell;
- `denom.py`: runtime cells that reach MET through denominator rulings;
- `survive.py`: whether lines a commit added since a date still exist at HEAD;
- `resolve_addrs.py`: resolves addresses through the census's own resolver.

## SWE2-AUDIT-SEM sample choice

| family | MET candidates | sampled | why this one |
|---|---|---|---|
| core scheduling / lifecycle | S-01, S-02, S-03, S-15, S-27 | **S-02** world tick and field frame | Every field frame runs through its tick, update gate and stop registry, so it has the most consumers |
| actor identity / ownership | S-04, S-13, S-52 | **S-13** actor storage, manager slots, unit pool | The record behind every actor; its registry scope includes the slot pool and actor class |
| party / control | S-20, S-28, S-35 | **S-28** party roster and leader change | Combat, AI, camera and UI all read membership and leader/control ownership |
| save / load / persistence | S-34, S-43 | **S-43** the save image | The whole persisted image; S-34's flag banks are one region of it |
| UI state / request routing | S-36 | **S-36** widget object model + request router | The only MET UI system |
| Phyre / middleware boundary | S-40, S-45, S-49, S-50 | **S-49** Phyre asset and class-descriptor surface | Every one of the 35,984 shipped `.phyre` assets crosses it |

## SWE2-AUDIT-SEM independence disclosure (read before relying on this record)

The task described the verdicts as authored by OPUS and FABLE. **At the level of the deciding cells that is not accurate.** `who.py`, over the 52 MET rows:

| cell | last scored by SWE2-AUDIT-SEM |
|---|---|
| `types` | **50 / 52** |
| `runtime` | **43 / 52** |
| `contract` | 29 / 52 |
| `relationships` | 49 bare `MET` (no basis, no author) |
| `script/data` | 49 bare `MET` (no basis, no author) |

In all six sampled rows, SWE2-AUDIT-SEM wrote the `types` and `runtime` cells. It also wrote the `contract` cell in S-02, S-13, S-28 and S-43.

**This audit is therefore partly a review of this lane's own earlier scoring.** That is one reason it was run adversarially against the image rather than against the cells. The second auditor, or SWE2-AUDIT-SPEC, should independently re-check at least one sampled row, and the expansion this record recommends should not be run by SWE2-AUDIT-SEM alone.

## SWE2-AUDIT-SEM per-system results

Legend: **P** pass · **P/N** pass with note · **F** fail · **F(n)** narrow fail (does not touch the mechanics). Paths are relative to `Database/FFXII TZA/` unless stated otherwise.

### S-02 world tick and field frame: **ACCEPT-WITH-NARROWING** (SWE2-AUDIT-SEM)

| # | | evidence |
|---|---|---|
| 1 | P/N | The page `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` §2.1–2.4 (lines 46–311) gives the full sequence, arg2, and return `eax=(mode==0)`, which is consumed at `0022ABDD`.<br>Problems in `CONTRACT-world-simulation-tick.md`:<br>- §2 omits arg2 (`r12d`→`002F1770`) and the return value.<br>- Line 74 says "eighty-nine bytes"; the real span is `003140CF−00314078 = 0x57 = 87`.<br>- Lines 2 and 67 say "consulted five times". There are six `r14d` tests at four decision sites, plus two hand-offs (`00314275`→`00358EE0`, `003142BE`→`002F1770`).<br>`System-Stop-Registry/CONTRACT-system-stop-registry.md` lines 35 and 148 still call the tick "uncontracted".<br>**The page itself still states the S-36 drain guard as "`+0x3E` bit 7" (lines 891, 932).** FABLE's dependent correction `30b2fd926` was reverted by `95b1f3a4c`; see systemic finding 1. |
| 2 | P/N | Every §3/§5 address resolves to FIELD.<br>`_types/fields.tsv:6347` (`SystemStopRecord+0x10`, "-1 at init") holds only for the two combined records written at `00226B6D`. The 56 bank records stay 0 (loop `00226B80`–`00226B93`), yet the contract calls this field the fade length.<br>`fields.tsv:6348` `byte14` omits its writer `002276B0 mov [r8+0x14],r9b`.<br>The manager request mask `02099ABC` (WT-2 state) resolves only to a GAP-SPAN (`ActorRecordPool +0x284`, no field row). It is named only in §14 prose, so it is outside the ruled denominator. |
| 3 | P/N | §4/§7/§10 are present in all three contracts.<br>`CONTRACT-per-frame-update-gate.md` lines 4–6 read `scope: family`, `level: L1`, BEHAVIORALLY UNDERSTOOD.<br>The 23-step orchestrator order (page §2.3) and the per-unit frame `00233F70` are page-only, and the tick contract excludes them (§16a). The registry claims "the per-frame order on the battle layer". |
| 4 | F(n) | The runtime cell says WT-1..5 are executed "stub-free". **WT-4's staged consume is not executed**, as the harness's own WT-4 note and README "Not covered" say. It rests on EXP-191 with `0017D280`/`0032FC30` intercepted, plus the static store `003140BF`.<br>The cell credits SS-2 as "AND-combine". The contract's SS-2 is the exemption polarity, which its §15 attributes statically.<br>The update-gate invariants are not named in the cell at all; their only execution is `diff_frame_gate.py`, with every callee hooked. |
| 5 | P/N | The cell says "N/A stated (the tick consumes no authored data)". **That is false for the system:**<br>- script verbs raise stop ids (`talkfadeout`, `settimestopmagic`, `maskopen`, `ucon`, `skipexec`; registry page §6, lines 235–262);<br>- options bit 3 selects id 0's raiser (SM-5);<br>- `skipexec`/`skipend` set the `+0x201` opt-in (`fields.tsv:100`).<br>The links exist, so the column passes as linked, not as N/A. |
| 6 | P | EX-1..9 and SM-1..5 are answered. The nine zeroed singleton cells, the actor-free world and the sound-singleton boundary (15 of 28 ids) are disclosed in the READMEs. |
| 7 | F(n) | `_index/candidates/s02-opus-replay-world-tick-stub-free/check.py:112` reads `record("WT5_loop_bounds_observed", True, …)`, **a literal pass**. The counts in `run_output.txt` match, but nothing asserts them.<br>WT-1 checks four sites hit once, not "five" sites or the per-mode call sets.<br>The case `stop-apply-stub-free` `SS2_combine_is_AND…` tests the AND, not the polarity.<br>`stop-reach-executed/check.py:86` is also a literal `True` (uncredited). |

**Spot-checks re-derived:**
- `022C2548` has exactly 3 accesses (`00314047` / `0031435D` / `00314960`) and a single `ret` at `0031436C`. Its callers are `0022ABD8`, `0022BA23` and `0022BCCF`.
- `01EED064`: 4 writes / 12 reads. `01EED060`: 2 reads / 3 writes.
- The gate word `01E0C464` has 16 tests, all in `0028E290`, and no writer.
- Bit 41: `00226307 or r8,r10`. SS-2 polarity: `00226334 bt rdi,0x19; cmovae`.
- The coordinating session independently read the prologue `00314047`→`00314078 call 0025BFB0`→`0031407D`/`0031408B`.
- Harness md5s reproduced: world-tick `8418dbd2`, stop-apply `8af1fb63`, stop-reach `927ce0d6`. `wt6.py` reproduces `d442c6e8` only after substituting `ctl_remove_cache` for `ctl_flush_tb` (systemic finding 6).

**Narrowed wording:**
- **Runtime:** "MET — WT-1/2/3/5/6 executed stub-free. WT-4 is stub-free on the unstaged path and the first-writer-wins latch; its staged consume rests on EXP-191 (`0017D280`/`0032FC30` intercepted) plus the static store `003140BF`. SS-1/3/4/5/6 are stub-free. SS-2's polarity rests statically on registry page §§3–5. SS-7 is stub-free for 28/28 ids. The update-gate invariants rest on `diff_frame_gate.py` (isolated, callees hooked)."
- **Script/data:** "MET — linked, not N/A (stop-raising verbs, options bit 3, the `skipexec`/`skipend` opt-in)."
- **Scope:** "S-02 L2 covers the tick spine, the gate fan-out and the stop registry. The 23-step orchestrator order and the per-unit frame are page statements, not contract invariants. The gate contract is L1."

### S-13 actor storage, manager slots, unit pool: **ACCEPT-WITH-NARROWING** (SWE2-AUDIT-SEM)

| # | | evidence |
|---|---|---|
| 1 | P/N | The pages give:<br>- BattleUnit slot allocation `00234480` (first-free, 32 slots, silent fail);<br>- handles;<br>- pool release `002628B0`@`00262D9F`;<br>- lookup `00358940`.<br>The page omits the gate that lets only manager slot 0 bind: `00265A70 cmp dword [rbp+0x28], r12d / jne` with `r12d=0` (`00265A30`). That gate is recorded only in `_index/candidates/gr17-reward-table-lifetime-0930/README.md` S5. |
| 2 | P/N | All contract-named state is declared: `ActorStorageRecord`, `ActorRecordPool`, `ActorSequenceDescriptor`@`01E0C328`, `ActorManagerSlot`, `BattleUnit` 0xF50, `BattleUnitSlotCount`@`0208E6A0`.<br>**`_types/fields.tsv:479` still gives `BattleUnit+0x057` as "actorClassByte … class-derived".** The page's M-4 (closed 2026-09-12) says it is the entry-group byte; `00263D30` is `movzx eax, word [rcx+0xF6]; ret`. The correction has not reached the type store (rule 4a). |
| 3 | **F** for the registry scope; P for pool construction | The credited contracts cover construction only:<br>- `CONTRACT-actor-storage-record-initialisation.md` AR-1..5;<br>- `CONTRACT-actor-record-pool-and-region-map.md`, which is `scope: family`, `level: L1`, BEHAVIORALLY UNDERSTOOD (lines 4–6, re-read);<br>- S-52's `CONTRACT-manager-slot-entry-tables.md` (L1).<br>**A grep of every `CONTRACT-*.md` finds `00234480`, `00265A20` and `00262D9F` in none** (re-run by the coordinating session).<br>Slot allocate/bind/release, manager bind/unload (`0026C8C0`/`002628B0`) and lookup share cross-operation invariants that no contract states: the 32-count guard `00265A8F`, the manager-0 gate against the release walk (`0025B212`–`0025B21D`), and the owning pointer `mgr+0x08`.<br>Under the table's own adequacy rule, the contract cell is SCOPE-SHORT for the registry text. |
| 4 | P/N | The replay is stub-free with an enforced allowed-set (`world.py:243-244`). `result.json` (`f11ac855`) and `residuals_result.json` (`aa917ce4`) reproduced.<br>**Both contracts' §13 still deny this execution:** storage-init says "None by this contract", and the pool contract (line 427) says "NEITHER". |
| 5 | P/N | Descriptor = bound definition payload (`0026C8C0` ← `0032F850`).<br>Pool-contract line 519 still lists "more than eight groups" as uncensused. The ScriptVM binding page answers it from 1,114 images (`{u16 8; u16 count[8]}`), but the answer was never carried into the contract. |
| 6 | P for construction; F for the registry scope | The slot lifecycle, manager bind/unload and identity handles are not excluded anywhere; they are simply uncontracted. |
| 7 | P/N with defects | `check.py:205` checks only "pointer is 0 or inside the record"; the recorded detail does match the per-arm table. `check.py:216` tests only the first gap byte; a full-span re-run is still clean.<br>**Fixture:** `check.py:13`/`:171` plants `ActorManagerSlot+0x28 = 1`, labelled "the flag", but `+0x28` is `slotIndex`. So the slot-0 arm `0026664C`/`0026664F` never ran in any variant. Re-running with index 0 still gives 11/11, but the records differ (`+0x0D` 0x82 vs 0x02). |

**Spot-checks re-derived:**
- `00267A79 call [r15+0x88]` → `00267A8B memset` → `00267B79 call 00266530` (AR-1).
- `002668E7 cmp eax,0xa / jb`.
- `0026C8FA cmovne r12,r8`.
- `0032F95A lea r8` resolves to `00267930`.
- Sole callers confirmed by a raw rel32 scan.

**Narrowed wording:** "S-13 L2 MET covers actor record pool construction: per-area pool allocation and zeroing, the carve and `+0x03` stamp, the region map, and per-record initialisation (`002679F0` / `00266AD0` / `00266530`), under CONTRACT-actor-storage-record-initialisation AR-1..AR-5 and CONTRACT-actor-record-pool-and-region-map §§3–7. It does not cover the manager-slot bind/unload lifecycle (`0026C8C0`, `002628B0`/`00262D9F`), BattleUnit slot allocation/binding/release (`00234480`, `00265A20`, `0025B070`→`00234200`), record lookup (`00358940`) or actor identity handles (`003589B0` / `002659D0` / `003588B0`). No S-13 contract states those as invariants."

If the producers keep the full registry scope instead, the contract cell is SCOPE-SHORT and the row is NOT MET. If that is disputed, ESCALATE-OPUS (contract scope).

### S-28 party roster and leader change: **ACCEPT-WITH-NARROWING** (SWE2-AUDIT-SEM)

| # | | evidence |
|---|---|---|
| 1 | P/N | Request, commit, teardown and lookup are documented byte-level in `11-Party/active-party-reserve-and-the-moment-the-leader-changes.md` §4 (lines 174–258), §8b and §9.<br>The **trigger and selection policy** are elsewhere:<br>- the trigger is UI request 3 (`16-UI/Request-Router/ui-request-router.md:77`; `0035BAA0` → `00327850` at `0035BAB8` → `jmp 00326500`);<br>- the policy (modes 0/1 use `+0x5AA4`, mode 2 `0x1A`, mode 3 `00377C70`, then a fallback chain) is only in `Battle-State-Block/the-battle-state-block-field-map.md` §2.7 (lines 177–205).<br>Implementable only by joining three documents. |
| 2 | P/N | All declared: `PartyFocusHandles` 0xC @`022C7FE0`, `PartyRosterSlots`, `BattleSystemState` 0x7410 (slot maps `+0x5A48..+0x5A90`, `+0x5AA4`, `+0x5AC8` re-read in `fields.tsv` by the coordinating session), and the `BattleUnit` / `ActorStorageRecord` fields.<br>`PartyFocusRequestKind`'s evidence says "5 refs in 3 functions"; a linear sweep finds 7. |
| 3 | F(n) | **BS-2 omits a precondition.** `00233C14 call 00235AF0` runs before the null test (re-read by the coordinating session: `00233C14 call 0x235af0` / `00233C20 test rax,rax`). `00235AF0` compares the bound block with the save copy at active+0x2200 and rebuilds on mismatch. `Battle-State-Block/CONTRACT-battle-state-block.md` contains `00235AF0` **zero** times.<br>The leader-selection policy (`00327850` → `00326500`) is in none of the four S-28 contracts.<br>OPUS's 2026-10-02 corrections changed `CONTRACT-the-five-parallel-slot-maps.md` materially after the 09-26 runtime MET (`dae5bb6d9`):<br>- `+0x5AA4` meaning;<br>- table `01EC9260` → `01EED260`;<br>- the refresher writes maps 1–4;<br>- the class-3 call count 19 → 24. |
| 4 | F(n) | The runtime cell (09-26) claims every named invariant is covered. But:<br>- CON-169 (09-29) added SM-5 mode arms 1–5, and `check.py` never sets the mode;<br>- SM-7's pool-full path is read, not executed;<br>- part of PF-3 and PF-6's kind-2 source are static census results that the cell does not label;<br>- three contracts' §13 deny the replays the cell relies on (focus §13 line 233, slot-maps §13 line 223, BS §13). |
| 5 | P | Verbs 0x205 (13 shipped uses), `debug_setpc` 0x2021, 0x35C and 0x2B9 (38 uses); the authored table `01EED260`; save placement BS-1 (`00233C25`–`00233C2A`). |
| 6 | P/N | GR-10/11, O-1..6 and FO-6 are answered. Not bounded: the player trigger, the uncontracted selection policy, and the unbounded indexed word array at `022C7F90`. Its setters (`00358580`, `003585B0`, …) use a signed, unbounded index that reaches `022C7FE0` at index 0x14. That affects PF-1's method claim; the debug bridges `0050DC30`/`0050DD60`/`0050DDC0` have 0 uses in 1,114 shipped scripts. |
| 7 | F(n) | The harnesses assert whatever they observe. Three PASS cases (`writer_keeps_its_own_side_only`, `SM7_removal_refreshes_all_five`, `BS1_BS2_binder_arms`) record contradictions of the contract as passes. `check_focus` (PF-5) checks only call order, not the third-handle teardown in contract §12. |

**Spot-checks re-derived** (by the helper; the binder by the coordinating session too):
- Reset `002370C0` does a 0x7410 memset, writes magic `0x5071901` and fills only map 0. `002370E5 call 003047F0` is not in BS-3.
- The refresher `003266C0` copies 0→1, 0→3 and 1→2,4.
- The binder's double reset is at `00233C3F`/`00233C48`, and the magic test at `00233C4D`.
- PF-1's 18 sites hold for shipped content.

**Narrowed wording:**
- **Runtime:** "SM-1..4, SM-5 (mode-0 path only), SM-6, SM-7 (pool-available path), SM-8; PF-3 (the deferral), PF-4, PF-5 (order), PF-6 (thunk choice and the summon call), PF-7, PF-8; BS-1, BS-2 (arms as executed, including the `00235AF0` reference compare), BS-3 and BS-5 are executed stub-free. Static: PF-1, PF-2, BS-4, PF-3's collapsing-caller census, PF-6's verb-source census, SM-5 mode arms 1–5 (CON-169), and SM-7's pool-full path."
- **Contract:** "The four pages carry implementing contracts. The leader-selection policy (`00327850` → `00326500`, field map §2.7, EXP-049/050) and the player trigger (UI request 3, `0035BAA0`) are documented but not contracted in S-28."

Repairs: the BS-2 `00235AF0` precondition (ESCALATE-OPUS if refused), the three §13 sections, PF-1's `022C7F90` caveat, and the count 5→7.

### S-43 the save image: **ACCEPT-WITH-NARROWING** (SWE2-AUDIT-SEM)

| # | | evidence |
|---|---|---|
| 1 | P/N | The pages give:<br>- 4 buffers, a `0x56690` image and a `0x200` header (`19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md` §2/§4);<br>- CRC-32 over active `+0x8..+0xE200`, stored at `+0xE200` and `+0` (`00583F81`–`00583FA1`);<br>- the stamp `0x05071901` with reinit (`00233C4D`);<br>- normalise and reseed `00584210`;<br>- the SAFH container.<br>**The real manual-save commit/load path is on no S-43 page or contract:** the slot transaction `00581DA0`; queue kind 8, element `+0x28` = active and `+0x30` = `0x56690` (`00581F27`–`00581F51`); the worker `003BAEB0`; load op 9 at `0058111E`. It is documented only in `how-a-manual-save-is-committed.md`, which no S-row registers. |
| 2 | P for image/payload; F for the storage layer | `SaveImage` (0x56690), its header (43 rows) and its payload (31 rows) are declared.<br>**Undeclared:**<br>- the storage controller `[02CA99B8]` (`resolve_addrs.py`: UNDECLARED);<br>- the `0x210` storage record;<br>- `02B40E10/14/1C`;<br>- the 12-byte SAFH header.<br>Resolving every .data/.bss address in `CONTRACT-storage-read-completion.md` gives 35 UNDECLARED / 11 FIELD / 8 PTR-CELL. |
| 3 | F(n) | `CONTRACT-save-image-pipeline.md` §7 (line 143, corrected 2026-10-02) routes the file leg through queue kind 8, but none of the four contracts lists `00581DA0`, `003BAEB0`, `00584210`, `00583D60` or `003BB220` as an entry.<br>**The verdict row's contract cell (`L2-VERDICTS.md:260`) still cites two claims its contract struck.** Both were re-read by the coordinating session:<br>- "only `002EF650` guarded" is struck at contract lines 182–186. `002EF5F0` ends `002EF60E jmp 0x16d6a0`, and `0016D6A0` is `ret 0`.<br>- "handle-before-copy tail-call to `0020E540`" is struck at lines 117–124 and 139; `0020E540` is a compiled-out stub.<br>Container §10 says bad files are "rejected". EXP-088 executed them, and the raw file is pushed through; that correction exists only in §14. |
| 4 | P/N | `s43-opus-replay-save-image-pipeline` re-run: 5/5, md5 `68b24505`, identical to the published file. EXP-088: 46/46.<br>`_experiments/evidence/save-container-roundtrip/`: 18/18 real files rebuilt bit-exact. No contract or page cites that record. |
| 5 | P | The payload map links each region's owner: script globals, flag banks, the battle-state block, spawn-keep, the stats record. The pipeline crossings name `00379160` (initial flags) and `0023AF50` (inventory table). |
| 6 | P/N | The slot transaction and load controller are neither owned nor bounded. Nothing in them invalidates the buffer/payload claims. |
| 7 | F(n) | `check.py` tests less than the runtime cell credits:<br>- SV-1: the gaps are the script's own constants compared with themselves.<br>- SV-4: "read by nothing image-wide" is proxied by hooks on 5 bodies. The static census holds: rip-relative counts are backup 1 / active 4 (positive control) / staging 2 / submission 3.<br>- SV-5: execution stops at `001DBAC0`, so `002EF2D0`/`00238A80` never run, yet the cell says "executed stub-free".<br>- SV-6: execution stops on entry to `0020E540`.<br>"Every named runtime invariant covered" counts one contract of four.<br>The types cell treats `storage-read-completion`'s 0 census rows as clean. That contract names state outside any Types/State heading. |

**Spot-checks re-derived:**
- SV-3: six `0x56690` immediates (`002EF5FD`, `002EF65D`, `002EF718`, `0057E42F`, `00581117`, `00581F2F`). A raw `.text` dword scan also finds exactly 6.
- SV-2: `002EF577 mov edx,0xacd` loop with the post-`jne` tail.

**Narrowed wording:** "S-43 L2 MET covers the in-memory save image and its container: the four buffers and the `0x56690`/`0x200` layout, the header map, the CRC-32 and its placement, the `0x05071901` stamp guard, load normalise/reseed (`00584210`) and the SAFH container. It does not cover the on-disk commit/load controller (slot transaction `00581DA0`, storage queue kinds 7/8/9, worker `003BAEB0`, load op 9 `0058111E`). That path is documented at page level only, has no contract, and its objects have no declared types."

Repairs: the contract cell's struck text; runtime coverage named for all four contracts (SV-4, SV-5's tail and SV-6 marked static); container §10; and a citation of the roundtrip record.

### S-36 widget object model, message protocol, request router: **REJECT** (SWE2-AUDIT-SEM)

**Named defects:**

**(D1) A reverted correction leaves a wrong invariant at HEAD.** `16-UI/CONTRACT-ui-request-router.md` R-5 at HEAD (line 184) says the drain guard is "`+0x3E` bit 7 … the device must be available" and that a blocked request is *deferred*.

Three facts were re-derived by the coordinating session:
- `002E0C8D movzx eax, byte [rdx+r15+0x3e]` / `shl al,7` / `sar al,7` / `or al,[…+0x38]` keeps **bit 0**.
- The device term `0053DD10` is `mov eax,1; ret`.
- When `00267360(0)` returns non-zero, `002E0B97`/`002E0B9D`/`002E0BA3` zero `0215F1A4`/`0215F1A8`/`0215F1A1`. Then `002E0BAA jmp 002E0C65` stores `r8b=0` into the pending byte `0215F1A0`, so the request is **discarded**, not deferred.

FABLE corrected exactly this in `fa2f75e21` (2026-09-26 03:25, an ancestor of HEAD). The SWE2-CONTRACT batch `95b1f3a4c` ("38 staged packages", 2026-09-26 11:12) overwrote it from a stale preimage. The same batch also reverted FABLE's dependent page fix `30b2fd926` on the world-tick page (lines 891 and 932 still say bit 7).

At HEAD, the contract tells an implementer to re-queue a request the original drops.

**(D2) Router state undeclared, under the contract cell's own credit.** The contract cell reaches "3 of 3 covered" by counting the router contract. The types cell (`L2-VERDICTS.md:255`) scored only `CONTRACT-widget-object.md`.

The router contract's state is undeclared, by `resolve_addrs.py`:
- the mailbox `0215F1A0` u8, `0215F1A1` u8, `0215F1A4` u32 and `0215F1A8` u32;
- the request-id copy `020927D8`;
- the 22-dword table `01E0C2C0`.

`ResourcePathNamespaceSlot`'s array ends at `0215F170`. The census gives this contract 0 rows because it has no Types/State heading. Under the ruled types criterion, the cell is PARTIAL for the contracts the row credits.

**(D3) The runtime cell's "R-4 arbiter half discharged" is not a demonstrated outcome.**
- Nothing executes `00253FE3`.
- The replay's arbiter exits first at `00253D19`, because `00265680` returns 0. That needs a loaded field; it is not a device gate.
- "Device-gated" is inferred past that earlier stop.

Under the 2026-09-25 ruling, non-reach does not demonstrate an outcome. R-4's arbiter half is a census, so it can rest **statically** if the cell says so.

**The other points** (from the helper; the gate claims re-read in its spot-checks):
- **Point 1, P/N:** widget contract §2/§3/§7/§12 suffices. §14 (line 576) still says "23 of the 32 message ids have no meaning", against the protocol page §10.
- **Point 3, additional:** §3 omits the pre-emption of the open UI by `0035DA80`/`003C8990` (`00254BCC`/`00254BD1`, which release via `00252D90`). The request-2 cancel path (`002E0BC0`, `002E0BE5`, `002E0C5E`) is documented nowhere in S-36.
- **Point 5, P:** router §10 links the script producers (`003462D0`/`003470D0`, verb 0x2A8, dev hook 0x2037), and `menu_message.bin` is on the router page §7b.
- **Point 6, P/N:** concrete widget classes are rightly out of scope. "S-36 MET" must not be read as "the UI is reconstructable".
- **Point 7, F:** the router contract has 0 census rows. `falsify_ui_router.py:162` (U7) tests R-5's single call site only, so it reported "survives" while the guard text was wrong.

**Gate claims that hold:**
- `0079C1F1 call [rax+0x48]` / `0079C1F6 jne`;
- `0079D010`'s sole caller is `0079C260`;
- `[02EA5220]` has one read (`0079F1CF`, not `0079F1D0` as the README says) and no writer, swept with a positive control (`02EA5368`);
- `02092734` has 3 reads / 3 writes;
- the arbiter harness reproduced 6/6, md5 `8a85be46`.

**Repair route:**
1. FABLE re-lands `fa2f75e21` and `30b2fd926`, and adds the pre-emption and cancel path.
2. OPUS / SWE2-DATA declare `0215F1A0..0215F1AB` and `020927D8`, and class `01E0C2C0`.
3. The runtime cell takes the wording "R-4: router half executed (r45 L4/C4); arbiter half (`00253FE3`) static only (census 3R/3W byte-exact); the replay exits first at `00253D19` (manager readiness); live residual named".

After that, ACCEPT-WITH-NARROWING is expected.

### S-49 Phyre asset and class-descriptor surface: **REJECT** (SWE2-AUDIT-SEM)

**Named defect (D1): contract-named state is undeclared, which is the S-46 precedent.**

`22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md` devotes **§7** ("The registration counter is a high-water mark", lines 210–218) and §11 (line 268) to the global `02CF8260`. It is read and written at `006333C7`/`006333D3`.

`resolve_addrs.py` reports `02CF8260` as **UNDECLARED**. So are the descriptor statics `02CAA0A0`, `02CA9DA0` and `02CA9FA0`.

On 2026-09-21 this lane held S-46's types cell PARTIAL for exactly one such u32 (`02089300`, "measured-address enumerations count"). The S-49 types cell, "census zero UNDECLARED", cannot be MET under the same ruling. The repair is one declaration, but the row is not MET until it lands.

**Per point:**

| # | | evidence |
|---|---|---|
| 1 | P/N | Enough for:<br>- header accept/refuse (cluster-header contract §2/§7/§8/§10, 9 failure rows);<br>- namespace read, byte order, BOM and self-size (NS-4);<br>- descriptor layout, reset and teardown.<br>**Not enough for loading assets.** Everything after `0059E19F` (`0059AAE0`, `0059B430`, `00599500`, `0059AC00`, `0059E300`, the fixups in `0059E880`) is call-signature prose (`the-cluster-header-and-what-the-loader-rejects.md` §7, lines 399–425).<br>The header §12 formula carries four inline "corrected 2026-10-02" patches. |
| 2 | **F** | D1 above.<br>**The type store contradicts corrected contracts (rule 4a):** `PhyrePackedNamespaceMemberRecord` still reads:<br>- `fieldOffset` = "byte offset of the field within the class";<br>- `elementSize` = "element size in bytes";<br>- `attributes` = "bit 31 marks a pointer".<br>The coordinating session re-read both. The namespace contract (lines 108–125, corrected 2026-09-26) says `w2` is the *file-side packed* offset in 147 of 154 classes, and that bit 1 marks an object pointer and bit 31 a counted buffer.<br>`PhyreClassDescriptor+0x00C0` is `ctorZeroedQwordC0 u64` (`fields.tsv:5493`). It is the default-instance pointer: `0063DC80 mov [rcx+0xc0],rdx; ret`, re-read.<br>`byteOrderMark`'s meaning contradicts NS-4 (`0059E167 cmp dword [rdi],0x1020304`). |
| 3 | P/N | The failure ladder matches the image (`0059A3E2` = 9, `0059A421` = 6, `0059A524` = 0xD).<br>**Descriptor §8 says flag bit 2 selects a CFG path "instead of `_aligned_free`".** The arm is `00584820 mov edx,0x100` → `0016D6A0` (`ret 0`), re-read, so bit 2 frees nothing. |
| 4 | F(n) | The runtime cell says "11 of 12 … executed-real". Per `_index/candidates/s49-runtime-per-invariant-exposure.md`:<br>- namespace I1/I2 are an archive **census**;<br>- descriptor I1 is **live** (EXP-124, PARTIAL);<br>- descriptor I2 (`005847E0`) **never ran**: `Reconstruction/Tests/Differential/diff_class_descriptor_dtor.py:129` "NOT EXERCISED", and EXP-097 line 134 excludes it.<br>Honest split: 7 executed on original code, 1 live, 2 census, 2 static. MET can stand on the static attribution, but the cell's wording is false for 4 of the 11. The "whole header" for header I1 is honestly disclosed as static. |
| 5 | P | Independent run over `D:/FFXII_TZA_extract`: 35,984 files. Every one has the marker, `m_size` 84, platform `11XD`, physics 0, the BOM, and a self-size that closes. The loader would accept all 35,984.<br>No execution has run `0059A3B0` on a real shipped file; acceptance of shipped files is by composition. |
| 6 | F(soft) | The deserialiser, instance binding and fixups after `0059E19F` are bounded only by "INTEGRATION not constructible offline" (header §16:707, namespace §16:492). No row says they are outside S-49, and no S-row owns them. The 23 % unobserved bytes and the 68 member-less classes are bounded. |
| 7 | F | The types cell rests on a census that sees one mutable S-49 address (`01F2E5A0`). It misses `02CF8260` and offset-named state, and it misreads the BOM value `01020304` as an `.rdata` address. `census_phyre_namespace_vbf.py:94` compares the size formula with the namespace's own word, not the header field the claim names; the claim holds on the corpus run anyway.<br>**Clean:** no literal-pass records in the lighting-slot, EXP-094/097/110 or `ph2` harnesses. `ph2_header_swap_members.py` re-ran 10/0. |

**Spot-checks** (helper, all confirmed):
- `005983E0` = 18 × `call 00632960` onto `02CA9DA0`→`02CA9FA0`, offsets 0x00–0x44;
- `00598C50` = 3 × at 0x48/0x4C/0x50;
- the swap leaf `005CB140` is `mov eax,[rdx]; bswap; mov [rdx],eax; mov al,1; ret`;
- the walk `0063E2E0` follows `+0x78`;
- the `00633390` destructor's sequence.

The stale-preimage scan over all six S-49 files found **no** reverted correction.

**Repair route:**
1. Declare `02CF8260` (u32 class-id counter); declaring the descriptor statics' routes is recommended. ESCALATE-OPUS only if the S-46 precedent is to be overturned.
2. Propagate the 09-26 namespace corrections and the `+0xC0` meaning into `fields.tsv`.
3. Fix descriptor §8's bit-2 arm.
4. Runtime cell: "7 named invariants executed on original code (header I2–I4; namespace I3–I4; descriptor I3–I4); descriptor I1 live (EXP-124); namespace I1/I2 rest on a full-archive data census; header I1's whole-header extent and descriptor I2 (`005847E0`, never driven) rest on static tier-1 reads."
5. Scope: "MET covers header accept/refuse, the namespace read/byte-order/BOM+self-size, and descriptor layout/reset/teardown. It does not cover instance deserialisation, fixups or namespace-to-runtime binding (`0059AAE0`, `0059B430`, `00599500`, `0059AC00`, `0059E300`), which no S-row owns."

## SWE2-AUDIT-SEM systemic findings (recommend expanding the audit before terminal certification)

**1. Stale-preimage batch publishes silently revert peer corrections, and no gate notices.**
- `95b1f3a4c` (SWE2-CONTRACT, 2026-09-26) overwrote FABLE's R-5 correction `fa2f75e21` and its dependent page fix `30b2fd926`. Both are still reverted at HEAD (S-36 D1).
- The same shape occurred on 2026-09-25: ORACLE's `69e9cad19` reverted SWE2-EC7's `d7989ecb` hub fixes across 33 files. EC7 repaired that by hand in `412c9a96c` ("re-land … reverted by peer stale-index sweep").
- A verdict that was correct when scored can thus become wrong at HEAD with no trigger.
- **Expansion check:** for every contract and page behind a MET row, run `survive.py <since> <files>`. It finds commits whose added lines are absent from HEAD and the first commit that dropped them. Then read every hit; rewording also drops lines.
- Over the sample's 38 files the scan's genuine hits are the R-5 pair. The other hits are corrections or re-lands, and ORACLE's EXP-151 lines are pending a read.

**2. MET cells are not re-reviewed when their dependencies change** (EVIDENCE-POLICY rule 8; rule 4a for the reverse direction). In every sampled system, a contract, page or type row changed after the deciding cell, or a correction failed to reach a consumer:
- S-43's cell still quotes two invariants its contract struck (09-23, 09-25, 10-02), and the file-leg model changed on 10-02.
- S-28's slot-map contract was corrected on 10-02, and CON-169 added SM-5 arms on 09-29, all after the 09-26 runtime MET.
- Contract §13 sections deny the very replays the runtime cells rely on (S-13 ×2, S-28 ×3).
- `fields.tsv` lags closed page findings (S-13 `BattleUnit+0x057`; S-02 `SystemStopRecord+0x10`) and corrected contracts (S-49 namespace member record, `+0xC0`).
- Nothing marks a MET acceptance for re-review when a dependency moves.

**3. The types-cell instrument measures less than the ruled criterion.** `Database/Tools/analysis-kit/gfz-scripts/contract_named_state_census.py` resolves only backticked 8-hex .data/.bss/.rdata addresses under Types/State/Objects headings (lines 42, 46, 106, 165–190).
- **What it misses:** heap and offset-named state, on-disk headers, and globals named in other sections such as `02CF8260` in S-49 §7. It misreads value constants in the `.rdata` range as addresses.
- **Effect on the sample:** contracts with no such heading give 0 rows, which reads as "zero UNDECLARED". Examples are `CONTRACT-ui-request-router.md` and `CONTRACT-storage-read-completion.md`.
- **Cells it got wrong:** S-49 (D1) and S-36 (D2) both carried "zero UNDECLARED" types cells over undeclared named state.
- **Where manual checks found coverage complete:** S-02, S-13 and S-28, for example `BattleSystemState+0x5A48..+0x5AC8` and `ManagerSingleton0209BE80+0x10F68`.
- **Outside the sample:** the census run 2026-10-03 prints 4 UNDECLARED rows in contracts behind four MET rows whose types cells claim zero: S-09 `02EBF000`, S-10 `01EF93FC`, S-16 `02089358`, S-31 `0208E680`. **Hand these to the second auditor and the owners.**
- **Expansion check:** for every MET row, resolve *every* backticked data address in each credited contract (`resolve_addrs.py`), not only those under a State heading. Then check offset-named state against `fields.tsv` by hand.

**4. Runtime cells over-credit execution, and 15 of 52 reach MET through denominator rulings.** Patterns seen in the sample:
- "executed stub-free" where the harness stops at a boundary partway through the sequence (S-43 SV-5/SV-6; S-02 WT-4);
- image-wide facts proxied by hooks on a few bodies (S-43 SV-4);
- non-reach counted as discharge (S-36 R-4);
- census, live-only and never-driven invariants counted as "executed-real" in an exposure analysis (S-49);
- "every named invariant" counted against one contract of several (S-43);
- an invariant credited to a case that tests a different clause (S-02 SS-2).

`denom.py` finds **15 MET runtime cells** whose MET depends on a denominator ruling ("static-structure", "out of the runtime denominator", "device-gated", "unreachable from every disclosed substitution"): S-05, S-06, S-11, S-13, S-22, S-26, S-28, S-30, S-36, S-37, S-40, S-42, S-43, S-46, S-49. Most rulings were made by SWE2-AUDIT-SEM, so this needs an independent pass.

**5. A harness PASS often means "observation recorded", not "contract held".**
- **Literal passes:** `record("…", True` appears 5 times in 4 replay packages: `s02-opus-replay-world-tick-stub-free/check.py:112`, `s02-opus-replay-stop-reach-executed/check.py:86`, `s06-opus-replay-console-arms/check.py:248` and `:263`, and `s22-opus-replay-recipe-resolver/check.py:242`. S-22's runtime cell credits the RW-2 early exit ("recipes 14/37 stop early"), and the same package records `loop_early_exit_observed` without asserting it. Whether the credit rests on that record needs an expansion check.
- **Contradictions recorded as passes:** three S-28 PASS cases record contradictions of the contract.
- **Mislabelled fixture field:** S-13's fixture plants a mislabelled field, so a real arm never runs while 11/11 pass.
- **One clause tested:** S-36's falsifier tested one clause of R-5.

**6. Contract cells count pages, not mechanisms or maturity.**
- **L1 contracts on L2 MET rows:** S-02's update-gate contract, two of S-13's three contracts, and three of S-43's four are `level: L1`. This bears on package §7.
- **Mechanisms with no contract:** the S-13 slot lifecycle, the S-28 leader-selection policy, the S-43 manual-save commit path, and the S-49 deserialiser. Each is documented on a page but in no contract. The table's adequacy rule was not applied to operations that only pages describe.
- **The gate reads one token.** `goal_gate.py` `check_verdicts` (lines 128–174) reads only the L2 cell's leading `MET`. `cells.py` found all 52 rows internally consistent on 2026-10-03, but 49 `relationships` and 49 `script/data` cells are bare `MET` with no recorded basis. `L2-VERDICTS.md:880-884` itself says those columns "need a page read per system and are unassessed". S-02's script/data "N/A" was false.

**Tooling (not a scoring defect, but it affects reproduction).**
- The prescribed venv's unicorn (2.1.0) fails `uc.ctl_flush_tb()` in the shared replay `world.py` (e.g. S-13 `check.py:151`; S-02 `wt6.py`), and the venv lacks `pefile` for some helpers. Replays reproduce under `C:\Python314` with unicorn 2.1.4, or with `ctl_remove_cache` substituted. Pin the version.
- `s29-opus-replay-inventory-rebase/world.py:29` loads the EXE with no hash pin. It hashes to `73461d08` today.

## SWE2-AUDIT-SEM limits

- **Independence.** This is partly self-review; see the disclosure. All six verdicts should be cross-checked by a lane other than SWE2-AUDIT-SEM before they gate certification.
- **No live work.** Nothing here was observed in the running game.
- **Harnesses not re-run:**
  - S-02: EXP-191, `diff_frame_gate.py`, the 26a5f0 `check_patched.py`.
  - S-28: harness md5s not reproduced.
  - S-43: EXP-056/057/058; CryptoAPI fidelity taken from the 18-file roundtrip record.
  - S-49: EXP-094/097 and the diff pilots, which write into the repo.
- **Not derived:**
  - S-02: 14 of the 16 gate groups beyond the spot-checks; the 23 orchestrator steps.
  - S-13: S-52's own contract; the second header table.
  - S-28: the origins of `edx`/`ebx` at `0024CDFD`, `002F1B66`, `003AAACB` and `003AB5C4`.
  - S-36: whether r45 runs the pre-emption calls for real.
  - S-49: `0063CE80`'s typed swap arm; PCD-4.
- **Heuristic scans.**
  - `survive.py` and `denom.py` produce worklists, not verdicts.
  - Sweeps cover executable sections and the listed addressing modes. Writes through computed addresses remain invisible.
- **Working tree.** The S-49 class-descriptor page carried large uncommitted peer edits during this audit. All S-49 statements are against committed HEAD content or the image.
- **Process.** Per-system work was done by read-only helper agents under this lane. Every verdict-bearing finding was spot-checked by the coordinating session as listed. This record edits no page under review; repairs are the producers'.
