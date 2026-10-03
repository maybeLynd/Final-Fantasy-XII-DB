# FABLE: S-21, the post-result events - route, poster, ring and message realiser (staged, 2026-10-03)

## What this package is (FABLE)

This is FABLE's staged contract text for SWE2-AUDIT-SPEC's **SCOPE-SHORT on S-21**
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md) item 3, [`item3.md`](../auditspec-l2-expansion-1003/item3.md) "### S-21").
The finding was that the poster `0046AB10` and the `battle_message.bin` realiser `005369C0` are documented on the
post-result-events page and in no contract. No tracked file is edited here. `apply.py` was run as a dry run only, and
nothing was committed or posted to the board.

**Host contract:** [`07-Combat-Action/CONTRACT-apply-result-to-target.md`](../../../07-Combat-Action/CONTRACT-apply-result-to-target.md).
It is S-21's only credited contract, and its §8 "Script · resource · event interactions" gave the events one sentence
("`00385BA0` can dispatch post-result events"). The new section is **§8a**, inserted after §8 and before
`## 9. Determinism`. Its invariants are **I9–I12**, continuing the contract's I1–I8.

**Already stated elsewhere? Checked first, and only in part.**
- A DB-wide grep for `0046AB10` / `005369C0` / `battle_message` finds no contract that states the mechanism.
- [`CONTRACT-auto-status-rebuild.md`](../../../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) §13bc–§13bm records
  EXP-246 and EXP-249–256. Those runs executed the poster's arms as callee validation, with `005369C0` scripted.
- `CONTRACT-status-write.md` (SW-4), `CONTRACT-gambit-walk.md`, `CONTRACT-inventory-class-storage.md` and
  `CONTRACT-defeat-rewards-sequence.md` mention the poster only as a callee or a neighbour.
- §8a points to those records and to the page for the event map and the row texts. It states the contract they leave
  implicit.

| file | what |
|---|---|
| `section.txt` | the drafted §8a with invariants **I9–I12**, failure paths, evidence class, and a `### Crossings into other layers` subsection for the two Save/Load/Settings edges its citations add |
| `neighbour_precheck.py` / `.out` | the pass-22 neighbour pre-check of the staged page (`check_page_neighbours.hits`, staged vs HEAD): **NEW HITS 0**. A preview, not the gate |
| `check_s21.py` / `check_s21.out` | the executed check: V0–V3 and K1–K8, with sensitivity controls S1–S5. **FAILS 0** |
| `rawref.py` | the raw reference index, copied from `fable-l2exp-s17-mech-1003` (the copy with the NOPDATA decode fix) |
| `fdis21.py`, `probe1.py`–`probe3.py` | reading aids: the disassembler, the raw-index survey, return-value and ctx `+0x2C` use per site, and the event id per site. The check re-derives everything it relies on |
| `apply.py` / `apply_dryrun.out` | inserts §8a before `## 9. Determinism`. It is anchored, refuses a dirty page, keeps CRLF/LF, is idempotent and prints **FAILS 0** |

## The facts, with sites (FABLE)

- **One route, keyed by the scratch word (I9).**
  - The route is `0031137A` → `00385BA0` → `00385C85` → `00469EC0`, and each link has exactly one caller.
  - It dispatches only when record byte `+0x1C == 1` (`00385C6F`).
  - The action id is `word [02AEDFD4]` (`00385C75`). The gate never reads the `ecx` the applier passes, because
    `00385BC9` overwrites it first.
  - `02AEDFD4`'s writers are the preview `00385680` and the resolver `00385F60`.
  - The dispatcher's context carries a zero-extended 16-bit action at `+0x28` and zero at `+0x2C` (`00469EF0`).
  - No dispatcher path reads the poster's `rax`.
- **The poster's census (K1).**
  - It has 48 call sites in 18 functions: the dispatcher holds 10, and 17 others hold 38. Chained `.pdata` fragments are
    resolved to their roots.
  - 25 sites load a literal event id, the largest `0x4D`.
  - The six `.rdata` dwords equal to the entries' RVAs are five chained-unwind parent records and one unwind-code
    coincidence.
- **The gates, in order (I10).** These are executed with the shipped `us` table.
  1. **The cap** is signed: `0x1FF` is dropped, while `0x1FE` and `-1` pass.
  2. **The `02089340 & 0x3080` veto and the unit's `+4` bit 5 apply only when ctx `+0x08` has an owning unit**
     (`0046AB2F`–`0046AB56`). Unit-less and null targets are admitted with any of bits 7, 12 and 13 set.
  3. **The filter.** The source's verdict decides alone when the source has an actor link: a source verdict of 0 drops
     the post although the target's verdict is 1.
  4. **The window** is unsigned: `(u32)(stamp + 0x1C2·G) > now` (`0046ABF5 ja`). This holds at G = 1 and G = 2.
- **One ring, reset only by area initialisation (I11).**
  - Every admitted post takes a slot. Ten unlimited posts evict a limited stamp (executed).
  - The ring has one reset: the branch-free leaf `004696A0` (41 stores) ← `0033A380` ← `00234463` in `002342F0`.
  - Of the four counter-restart routes (S-17), only the area-initialisation one is followed by that reset in the same
    body.
  - **A stamp from before a counter restart suppresses its `(event, stats)` until the new clock passes it.** Executed:
    stamp 5000, counter 10. The repeat is suppressed through 5449 and admitted at 5450, or at once after `004696A0`.
- **The realiser and the last mile (I12).**
  - The row address is 32-bit and has no bound against the row count. That bound is unneeded today: every posted id
    is at most `0x62`, and every language has at least 100 rows (V3).
  - Slot kinds come from row `+0`/`+1`/`+2`/`+5`. Kinds 3–9 map to ctx `+0x10`/`+0x14`/`+0x18`/`+0x1C`/`+0x20`/`+0x28`/`+0x24`,
    and kinds 0 and 10 or more give 0 (executed, every kind).
  - The id dword's bits 16–31 are stack residue; `00536410` masks them.
  - In the request to `0035B990`:
    - `+0x30` = ctx word `+0x2C`, which selects the stash (`[022CA430] + 0x568`) and suppresses the HUD line;
    - `+0x32` = 1 exactly for events `0x24`/`0x25`, and gates only the strip-and-measure step;
    - `0028E110` is called on every non-stash path.
- **An unbound table faults.** With `[02EBF018] = 0` and a filter that admits, the poster reads address 4 at
  `0046ABB3` (executed).

**Sensitivity controls** (each turns a check to FAIL; all five did):
- S1: `jge`→`jg` at `0046AB29`;
- S2: the row bit test moved to bit 1 at `0046ABB3`;
- S3: the kind bound `8`→`7` at `00536B00`;
- S4: `je`→`jne` at `0035B9CB`;
- S5: the claim "the `0x3080` veto drops every post".

## Side findings that contradict DB text (FABLE)

1. **The veto is described unconditionally in two places.** The page's §2.3 "drop" row and its §4 formula say
   `02089340 & 0x3080` drops the post. `the-steal-roll.md` (L130–L133) says the same. The poster tests the word only after
   `0031B860` finds an owning unit for ctx `+0x08` (`0046AB2F`–`0046AB40`). K6c executes both sides.
2. **`CONTRACT-defeat-rewards-sequence.md` L229** says `0046AB10` "matches `{id word, key qword}` subscribers in a
   runtime-built table at `02EFB560`". Three things are wrong:
   - the address is the ring `02EBB560`;
   - it is a ten-entry recent-post ring, not a subscriber table;
   - the match runs only for rows with `+4` bit 0, and row `0x26` (the post that sentence describes) is not one of
     them. The same contract's L305 describes the ring correctly.
3. **The page's last-mile paragraph (§2.5 "The last mile")** reads as if the HUD post were gated by `00254A10()` and
   word `+0x32`. Only the strip-and-measure step is gated. `0028E110` runs on every path that does not take the stash
   (K8). The page also does not say that `+0x32` is 1 only for events `0x24`/`0x25`.
4. **`CONTRACT-status-write.md` SW-4** ("what `0046AB10` does with codes `0x12` and `0x11` beyond posting the event") is
   answerable from K4b.
   - The poster has no branch on the event id except the row reads and the ring key.
   - Rows `0x11` and `0x12` have `+4` bit 0 clear, so they are never rate-limited.
   - So the poster does nothing code-specific with them.

## What is not settled (FABLE)

- **Whether every counter restart is followed by an area initialisation before the next post** is not traced. I11's
  stale-stamp suppression is therefore shown possible, not shown to occur in play.
- **The other 17 posters' context `+0x2C`** is not traced. That word selects the stash.
  - `0046AA70` stores `edx` there (`0046AABC`) before its gil post.
  - Which posts reach `[022CA430] + 0x568` instead of the HUD is open.
- **Hooks stand in for:**
  - `0031B860` and `002FA3B0` in K6;
  - all ten of `005369C0`'s callees in K7 (`00536410`'s text, the names and the letters are not produced);
  - the format engines and `0028E110` in K8.
- **The poster's `rax` in the other 17 posters.** 24 of their 38 sites end in a `ret` before any `rax` access (probe2),
  so they pass it on as their own return value. Whether any caller of those reads it is not traced.
- **Nothing is live.** The page's `FL-2` live read stays with ASTRA-QUEUE AQ-16.

## How to apply (FABLE)

`python apply.py` is the dry run, and `python apply.py --apply` writes. Applying needs the contract clean
(`git diff HEAD`). The last dry run, at HEAD `890844135`, printed **FAILS 0** (`apply_dryrun.out`).

## Consumer check (FABLE)

affected: Database/FFXII TZA/07-Combat-Action/CONTRACT-apply-result-to-target.md

- consumer: `07-Combat-Action/CONTRACT-apply-result-to-target.md` — **revised-here**. `apply.py` inserts §8a. §8's
  sentence stays true, and §8a states what it summarised. I1–I8 are unchanged. I8's availability clear by `00385BA0` is
  the same body I9 enters.
- consumer: `07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md` — **agrees** on
  the event map, the row layout, the 48/18 census, the ring geometry and the window. The unconditional veto wording
  (§2.3, §4) and the last-mile gating wording (§2.5) are **routed-to-FABLE** as a page correction (side findings 1 and 3).
  The page is not edited here.
- consumer: `08-Combat-Formula/Steal/the-steal-roll.md` — the same unconditional veto sentence (L130–L133) is
  **routed-to-FABLE** (side finding 1).
- consumer: `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md` §13bc–§13bm — **agrees**. EXP-252's
  correction (the veto exit returns the owner row) is I10's "the exits do not set `rax`". EXP-249's window predicate is
  I10.4.
- consumer: `13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md` — L229 is **routed-to-OPUS** (side
  finding 2).
- consumer: `10-Status-Periodic-Terminal/CONTRACT-status-write.md` — SW-4 is **routed-to-OPUS** (side finding 4).
- consumer: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` — **agrees** (bits 7, 12 and 13
  and their setters). §8a adds that the poster consults them only for a target with a unit.
- consumer: `08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md` — **agrees** (`02AEDFD4` is written by the
  preview and the resolver and is never reset).
- consumer: `_index/candidates/fable-l2exp-s17-mech-1003` (staged §10a of the S-17 contract) — **agrees**. I11 is a
  second consequence of the same counter restart: the event ring keeps its stamps unless the restart came through area
  initialisation.
- consumer: `_index/L2-VERDICTS.md` (S-21 row, contract and script/data cells) — **routed-to-OPUS**. With §8a applied,
  the SCOPE-SHORT item (the poster, the realiser and the table read "in no contract") is stated. The script/data cell's
  `battle_message.bin` row read (`005369C0`, row `+0/+1/+2/+3/+4/+5`) is now contracted. Both cells are OPUS's to
  re-score.

run: check_s21.py at 890844135 (V0–V3 and K1–K8 PASS, S1–S5 sensitivity controls PASS, FAILS 0; Unicorn 2.1.4, image 73461d08…, us battle_message.bin 6,668 B; neighbour pre-check NEW HITS 0; apply.py dry run FAILS 0, contract +181 lines, LF kept). This publish touches only the host contract; every other consumer above agrees or is routed.
