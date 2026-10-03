# FABLE: S-36 router repairs, staged (2026-10-03)

## What this package is (FABLE)

This is FABLE's staged repair for SWE2-AUDIT-SEM's S-36 **REJECT** on the UI request router contract. The findings
are in [`../auditsem-l2-sample-1003/README.md`](../auditsem-l2-sample-1003/README.md), "### S-36". No tracked file is
edited. `apply.py` was run as a dry run only, and nothing was committed or posted to the board.

Every fact below was read from the certified image (`73461d08…`, base `00120000`), using
[`rvlib.py`](../fable-review-astra-ov42-caller-quotient-bound-1002/rvlib.py) and capstone. Callers come from a raw `.text`
index: E8/E9 rel32, 0F 8x rel32 and EB/7x rel8.

| file | what |
|---|---|
| `section_5a.txt` | D2: the new "## 5a. State" section, inserted before "## 6." |
| `section_3a.txt` | Point 3: the new "## 3a. Pre-emption …" section, inserted before "## 4." |
| `d3_replacement.txt` | D3: the old and new text for `_index/L2-VERDICTS.md` line 255 (two fragments) |
| `fields_proposal.tsv`, `types_proposal.tsv` | D2: the type-store rows proposed to SWE2-STRUCT (8 field rows, 3 types) |
| `census_router_state.py` / `.out` | D2: the writer and reader census of the six cells (FAILS 0) |
| `falsify_ui_router_u7b.py` / `.out` | Point 7: U7 redone against both R-5 clauses, with sensitivity cases (FAILS 0) |
| `apply.py` | Stages E1 (3a), E2 (5a) and E3 (D3). Anchored, refuses a dirty page, keeps CRLF/LF, idempotent |

## The findings, one by one (FABLE)

### D1, the reverted R-5 (FABLE): verified fixed at HEAD

The commit that re-landed the fix, `18ebb00d9`, is an ancestor of HEAD. R-5 now reads **`+0x3E` bit 0** (contract
line 183). The device and transition clauses are struck. The not-ready path is stated as a **discard** (line 193).

The bytes agree:
- `002E0C8D` `movzx eax, byte [rdx+r15+0x3E]`, then `shl al, 7` / `sar al, 7`, keeps bit 0.
- The device term `0053DD10` is `mov eax, 1; ret`.
- When `00267360(0)` is non-zero, `002E0B97` / `002E0B9D` / `002E0BA3` zero the id, the parameter and the blocked
  byte. Then `002E0BAA` jumps to `002E0C65`, which stores `r8b = 0` (set at `002E0B94`) to the pending byte.

The world-tick page is also corrected at HEAD (lines 891 and 935: bit 0). No D1 edit is needed.

### D2, undeclared router state (FABLE): verified, and declared in 5a

`resolve_addrs.py` resolves all six cells as UNDECLARED at HEAD: `0215F1A0`, `0215F1A1`, `0215F1A4`, `0215F1A8`,
`020927D8` and `01E0C2C0`. The contract has no Types/State heading. The census tool's `STATE_HEAD`,
`\b(types?|state|objects?)\b`, with "transition" excluded, matches "## 5a. State (…)". `apply.py` runs the tool's own
`state_sections()` on the staged page:
- 5a **is** read as a state section, and 3a is not (C1, C2).
- 5a gives 10 rows. At HEAD, 7 are UNDECLARED, 2 are FIELD (`02092730`, `02092734`) and 1 is PTR-CELL (`0209BE80`).
- With `fields_proposal.tsv` and `types_proposal.tsv` loaded, the 10 rows are **0 UNDECLARED** (C3).

The census (`census_router_state.py`) adds three facts that the audit and §5 did not have:
- **The request-id copy `020927D8` outlives the request.** Its only writer is `00252B4C`. The release `00252D90`
  zeroes `02092730` and `02092734` (`00252DC5`, `00252DCB`) but not the copy, and so does the reset `00252DE0`. Its only
  reader is `00254710` (`00254714`). That function returns `0028F740()` when the copy is 17 or 18, and its one caller
  is `00346DA0` (`00346DA9`).
- **The table `01E0C2C0` has three readers, not one.** They are the router (`00254B88`), the arbiter's inlined copy for
  request 5 (`00253FFC`) and the standalone builder `00254500` (`0025450C`). The table has no writer and no pointer
  constant. Entry *i* belongs to aggregate bit *i*; the values are tabulated in 5a.
- **Bytes +2 and +3 of the mailbox record are other code's.** `0215F1A2` has writer `002E0940` (`002E096D`) and
  getter `002E1030`. `0215F1A3` has writer `002E1450` (`002E155D`) and getter `002E1600`. The proposal declares both
  so that the record's extent is honest.

The audit's other D2 statement holds: `ResourcePathNamespaceSlot` ends at `0215F170`.

### Point 3, pre-emption and the request-2 cancel (FABLE): verified, and widened where the bytes required it

The audit is right that §3 omits the pre-emption and that the request-2 cancel is documented nowhere in S-36. The
details are in `section_3a.txt`. The bytes add three things the audit did not state:
- **The pre-emption is a triple, and it runs before the id's range test.** The calls are `0017E7D0` (a `jmp` to
  `ret 0`), `0035DA80` and `003C8990` (`00254BC7` / `00254BCC` / `00254BD1`). So a request that R-c later refuses has
  still torn down the open UI.
  - `0035DA80` acts only when `[0209BE80]+0x10F78` is non-null. It releases through `00252D90` (`0035DAA8`) and clears
    row 8 bits 1, 8, 0, 11, 9, 6 and 20 through `00254980(0)` → `002E1CA0`.
  - `003C8990` acts only when widget `02B47730` exists and its `+0x40` has bit 4. It stores `+0xD0 = 3` and
    `+0xC8 = 0`, releases (`003C89FC`) and clears row 8 bit 0.
- **The same triple runs at two other sites.** One is the arbiter's inlined copy of R-a and R-b for request 5
  (`00253FE3` … `0025403A`), which then calls the route `003C87B0(5)` directly at `00254044`. The other is
  `00254FC0`, whose one caller is `0026C4EC`.
- **The request-2 cancel.** It clears only the pending byte (`002E0BEC`, `002E0C65`), on either of two terms:
  `0037B330() != 0` (`cmovne` at `002E0BE5`), or aggregate bit 0 or 3 (`test bl, 9` at `002E0C5E`). It leaves the id
  and the parameter in place, and never calls the router. Aggregate bits 0 and 3 are exactly the two table entries
  that forbid request 2 (`0x4` each, the only entries with bit 2 set). The test is therefore R-b's refusal of request
  2, applied early. It runs before the record guard, so a forbidden request 2 is dropped, not deferred.

### D3, "R-4's arbiter half discharged, device-gated" (FABLE): verified, replacement drafted

The bytes:
- `00253D0D` calls `00265680`, and `00253D19` `je 00254166` leaves the arbiter before its latch test `00253FE3` when
  the call returns 0.
- `00265680` returns 0 unless all of these hold: slot 0 at `02098E10` is live (`+0x10` bit 0); `+0x10` bit 7 and
  `+0x11` bit 0 are clear; every live slot of the five has `+0x17 & 3 == 3`; and `002E0540` returns 0. Only then does it
  return `00265720()` (`00265684`–`002656FB`). That is a loaded-field condition, not a device gate.
- The replay's actual stop is `0079C1F1` `call [rax+0x48]` / `0079C1F6` `jne`.

The claim is stated **only** in `_index/L2-VERDICTS.md` line 255 (the S-36 row), in two places:
- the runtime cell: "R-4's arbiter half is device-gated (the named residual discharged): …";
- the verdict cell: "the runtime cell's last named residual (R-4's arbiter half) is discharged — …".

The contract does not state it. Its only mention of `00253FE3` is R-4's static census (line 171), and §8 says that no
refusal has been observed live. Both fragments are quoted verbatim in `d3_replacement.txt`, with the replacements.

The new text says that R-4's arbiter half rests **statically** on the `02092734` census and is not discharged at
runtime. The census has three reading functions (`00254B71`, `00253FE3`, `003F4E70`) and three writing sites
(`00252B46`, `00252DCB`, `00252E05`). The new text names `00253D19` and `00265680` as a field-load stop, and names the
live residual: `00253FE3` executed with a field loaded.

### Point 7, U7 tested one call site only (FABLE): verified; U7b written and run

`falsify_ui_router.py` line 162 (U7) checks only the drain's single call site. `falsify_ui_router_u7b.py` tests both
R-5 clauses at the bytes:
- **T1** computes the kept `+0x3E` bits from the shift counts over all 256 byte values, giving **{0}**.
- **T2** shows that the guard defers: its arm `mov ecx, esi` at `002E0D57` leads to `or eax, ecx` / `jne 002E0D3E`,
  with no pending store on the path.
- **T3** shows that the not-ready arm discards. It traces `xor r8b, r8b`, the three zero stores of `ebp`, which is 0
  from `002E09B6` and never rewritten, and `jmp 002E0C65`, the pending store of `r8b = 0`. It then checks that
  `test r8b, r8b` / `je` at `002E0CC4` skips the router call `002E0D0B`, with no clobber in between.

There are four sensitivity cases, and each **fails as required**. S1 and S2 are mutated readings: "bit 7" and
"deferred". S3 and S4 are mutated images: `shl al, 6` keeps bit 1, so "bit 0" fails; and NOPs over `xor r8b, r8b` make
the outcome unprovable, so "discarded" fails.

Result: **FAILS 0** (`falsify_ui_router_u7b.out`). The old falsifier is unchanged.

### Point 1, the widget contract's §14 (FABLE): verified, widget contract is stale; owner OPUS

- **Widget contract** `16-UI/Widget-Object-Model/CONTRACT-widget-object.md` line 575 (§14): "**23 of the 32 message
  ids have no meaning.** `DL-1`." The text dates from the page's creation, `e61d5c937` (2026-09-08).
- **Protocol page** `the-widget-message-protocol.md` §10 (lines 1345–1365) answers it. It strikes down through "3
  remain: 11, 26, 30". 11 and 26 are then named, and 30 is dispositioned (2026-09-25). The pointer at line 1365 says
  "`DL-1` is answered for the whole recount, §7".

**The protocol page is right at HEAD.** The widget contract is wrong on both numbers. The id count is **56**, not 32:
the contract's own §15c says so, and it was re-derived today. `check_widget_message_ids.py` reports 0 STALE (58 rows
agree exactly and 193 agree by sparse chain), and the exact rows of `widget-message-handlers.tsv` carry 56 distinct ids:
1–26, 29–53 and 285–289. And no id remains without a meaning or a disposition.

The front matter names no lead or owner. In `git log` the page's dominant identity is **OPUS** (14 of its prefixed
commits; audit state `opus-widget-object-pass-1`), so the fix is routed to OPUS. The page is not edited here.

### Side findings (FABLE)

- **`battle-runtime-mode-ladder.md` line 1369 has `00254980`'s selection backwards.** The page says "`ecx == 0` picks
  `002E1C20`". The bytes are `test ecx, ecx`; `lea rax, [002E1C20]`; `lea rbx, [002E1CA0]`; `cmovne rbx, rax`
  (`00254986`–`0025499B`). So a zero argument picks `002E1CA0`, the clear, and that is what `0035DA80` passes. The line
  dates from `af6123d3f` (SWE2-EC7 batch 108), so the fix is routed to SWE2-EC7.
- **R-4's "the input subsystem's own arbitration sees it too" holds only on the arbiter's request-5 branch.**
  `00253FE3` is reached only past `00253FB3`–`00253FDD`: pad bits `0xA0`, `003669D0() == 0`, and the request word 0
  or 3. The arbiter's mailbox posts (`00253D78`, `00253EE6`, `00253F44`, `00253F53`) do not consult the latch. This is
  FABLE's own text. It is left for a separate R-4 narrowing so that this package does not widen.
- **The input contract's I-4 says "`00254500` -> `00254B50`".** `00254500` does not call the router. It is a third
  mask builder; the router inlines its own. FABLE's own S-35 page; wording only, not edited here.
- **The capability rows directly above the mailbox are indexed with an upper bound only**, at `002E1C20`, `002E1CA0`
  and `002E1CD0`, and `002E1020` has no bound at all. A row ≤ −6 would reach the mailbox. Every caller traced passes a
  row from 0 to 15. The details are in the census dispositions and the 5a notes.

## Census counts (FABLE)

`census_router_state.py` covers 35,713 `.pdata` entries and 13,800 catalogue functions without `.pdata`:

| cell | writers (functions / sites) | readers (functions / sites) |
|---|---|---|
| `0215F1A0` pending | 5 / 7 | 2 / 4 |
| `0215F1A1` blocked | 3 / 4 | 4 / 4 |
| `0215F1A4` id | 5 / 5 | 1 / 4 |
| `0215F1A8` parameter | 5 / 5 | 1 / 1 |
| `020927D8` request-id copy | 1 / 1 | 1 / 1 |
| `01E0C2C0` table | 0 / 0 | 3 / 6 (through 3 `lea` anchors) |
| `0215F1A2`, `0215F1A3` (not mailbox) | 1 / 1 each | 1 / 1 each |

The other forms:
- The raw rel32 sweep found 167 windows and 43 confirmed instructions. **None was unlisted**, and every P1 site was
  re-found.
- `[reg+RVA]` forms, VA displacements and RVA/VA constants: **0**.
- 14 indexed anchors near the cells, each with a disposition read at the bytes.
- Controls C1–C5 PASS, **FAILS 0**.

The §5 counts survive exactly: five writers and one reader for the id and the parameter, five and two for the pending
byte, and three and four for the blocked byte.

## U7b result (FABLE)

T0 to T3 PASS and S1 to S4 PASS, so **FAILS 0**. T0 re-confirms the single drain call site, `0031427D`, by the raw
index.

## Consumer check (FABLE)

affected: Database/FFXII TZA/16-UI/CONTRACT-ui-request-router.md — **revised-here**. §3a and §5a are inserted by
`apply.py` (E1, E2). R-1 to R-6 are unchanged and agree with the new sections; the R-4 narrowing is noted above, not
applied.

consumer: Database/FFXII TZA/_index/L2-VERDICTS.md — **routed-to-SWE2-AUDIT-SEM**. This is the D3 wording on line 255.
`apply.py` stages it (E3), but the cell is that lane's to accept or reword.

consumer: Database/FFXII TZA/_types/fields.tsv — **routed-to-SWE2-STRUCT** (`fields_proposal.tsv`, 8 rows).

consumer: Database/FFXII TZA/_types/types.tsv — **routed-to-SWE2-STRUCT** (`types_proposal.tsv`, 3 types). The audit
also names OPUS and SWE2-DATA for the declaration; SWE2-STRUCT owns the store.

consumer: Database/FFXII TZA/16-UI/Widget-Object-Model/CONTRACT-widget-object.md — **routed-to-OPUS** (§14 line 575:
32 ids → 56, and `DL-1` answered).

consumer: Database/FFXII TZA/16-UI/Widget-Object-Model/the-widget-message-protocol.md — **agrees** (§10 is right at
HEAD).

consumer: Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md — **agrees**
(lines 891 and 935 say bit 0; line 933's `00265680` reading matches D3).

consumer: Database/FFXII TZA/16-UI/Request-Router/ui-request-router.md — **agrees**. Line 57 has "special-case request
2 against aggregate policy", and §7b R1 lists `0035DA80` and the `003C8990` family among the release's callers.

consumer: Database/Tools/analysis-kit/gfz-scripts/falsify_ui_router.py — **agrees**. It is unchanged; its U7 is
narrower than R-5, and U7b sits beside it in this package.

consumer: Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md —
**routed-to-SWE2-EC7** (line 1369, `00254980`'s selection reversed).

consumer: Database/FFXII TZA/15-Input/CONTRACT-input-subsystem.md — **routed-to-FABLE**: the I-4 wording
"`00254500` -> `00254B50`". Not edited here.

run: falsify_ui_router_u7b.py and census_router_state.py at 33eb7192f (U7b FAILS 0 with four sensitivity cases; census FAILS 0; apply.py --contract-only dry run FAILS 0). This publish touches only the contract; every other consumer above is routed or agrees.

## What is not settled (FABLE)

- **Some row indices are untraced.** Not every constant-relative `lea ecx, [reg ± k]` caller of `002E1C20` and
  `002E1CA0` was traced to its constant, for example `0022974E`'s `rsi` and `0035D6B0`'s `rax` and `rdi`. "No caller
  reaches the mailbox" therefore rests on reading, not on a bound.
- **The meanings of mailbox-record bytes +2 and +3** are not established; they are proposed as DISCOVERED.
- **Bodies not followed:** `00296BE0` and `003F80E0`, reached from `0035DA80`; `00265720`; and the solo callers of
  `0035DA80` (`0029C020`) and `003C8990` (`00251FE8`, `00254ADC`, `00255348`). Nor is the meaning of widget
  `02B47730`'s `+0x40` bit 4.
- **Nothing here is executed.** No live capture exists of the pre-emption, of the cancel, or of `00253FE3`.

## How to apply (FABLE)

Run `python apply.py` for the dry run and `python apply.py --apply` to write. Applying needs both pages clean
(`git diff HEAD`). E3 needs SWE2-AUDIT-SEM's acceptance first. HEAD moved three times during the session, because
peers were committing. Earlier in the session the contract was dirty with a peer's pending row move, which was
committed as `c76e449dc`. The last dry run, at HEAD `be84252cb`, printed **FAILS 0**. Its output is
`apply_dryrun.out`, reproduced here:

```
FABLE S-36 router repairs, dry run (no file is written)
HEAD be84252cb
PASS  G1  Database/FFXII TZA/16-UI/CONTRACT-ui-request-router.md is clean
      line endings kept: LF
PASS  A1  anchor ^## 3\. Dispatch\s*$ occurs 1 time(s) at line 68
PASS  A2  anchor ^## 4\. The three refusals occurs 1 time(s) at line 92
PASS  A3  anchor ^## 5\. The mailbox is a single slot occurs 1 time(s) at line 117
PASS  A4  anchor ^## 6\. The invariants occurs 1 time(s) at line 144
PASS  A5  anchors are in order 3 < 4 < 5 < 6: [68, 92, 117, 144]
PASS  E1  3a inserted before line 92 (## 4. The three refusals, and why a call)
PASS  E2  5a inserted before line 225 (## 6. The invariants)
PASS  E3x  staged order 3 < 3a < 4 < 5 < 5a < 6: {'## 3. Dispatch': 68, '## 3a.': 92, '## 4.': 173, '## 5. The mailbox': 198, '## 5a.': 225, '## 6.': 267}
PASS  L1  5a's census link resolves from the contract's folder
PASS  C1  the census reads 5a as a state section: ["5a. State (FABLE, 2026-10-03; declared on SWE2-AUDIT-SEM's S-36 D2)"]
PASS  C2  the census does not read 3a as a state section
      5a rows against the store at HEAD: [('0215F1A0', 'UNDECLARED'), ('0215F1A1', 'UNDECLARED'), ('0215F1A4', 'UNDECLARED'), ('0215F1A8', 'UNDECLARED'), ('020927D8', 'UNDECLARED'), ('02092730', 'FIELD'), ('02092734', 'FIELD'), ('0209BE80', 'PTR-CELL'), ('01E0C2C0', 'UNDECLARED'), ('01E0C2C4', 'UNDECLARED')]
      5a rows with the two proposals loaded: [('0215F1A0', 'FIELD'), ('0215F1A1', 'FIELD'), ('0215F1A4', 'FIELD'), ('0215F1A8', 'FIELD'), ('020927D8', 'FIELD'), ('02092730', 'FIELD'), ('02092734', 'FIELD'), ('0209BE80', 'PTR-CELL'), ('01E0C2C0', 'FIELD'), ('01E0C2C4', 'FIELD')]
PASS  C3  with the proposals, 5a has 10 rows and 0 UNDECLARED []
PASS  G2  Database/FFXII TZA/_index/L2-VERDICTS.md is clean
      line endings kept: LF
PASS  D0  d3_replacement.txt blocks: ['NEW 1', 'NEW 2', 'OLD 1', 'OLD 2']
PASS  R1  line 255 is the S-36 row
PASS  D1p  NEW 1 carries no '|'
PASS  D1  OLD 1 occurs 1 time(s) on line 255
      OLD 1 -> NEW 1: 463 chars -> 1118 chars
PASS  D2p  NEW 2 carries no '|'
PASS  D2  OLD 2 occurs 1 time(s) on line 255
      OLD 2 -> NEW 2: 265 chars -> 383 chars
PASS  D3  line 255 keeps its 9 cell separators
      dry run: contract +123 lines, L2-VERDICTS line 255 changed
FAILS 0
```
