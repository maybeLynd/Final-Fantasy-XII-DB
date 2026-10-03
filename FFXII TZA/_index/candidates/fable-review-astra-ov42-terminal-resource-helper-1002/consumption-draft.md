# Consumption draft: ov42-terminal-resource-helper (FABLE, 2026-10-02)

*Paths in this draft are plain backticked text. When FABLE applies the edits, it turns the packet and record paths in
the proposed page text into page-relative links in the page's usual style.*

This draft is for FABLE to apply. Nothing in it has been applied yet. Its scope is the accepted source claims of
`_index/candidates/fable-review-astra-ov42-terminal-resource-helper-1002/REVIEW.md`, with that review's six
narrowings, at the stated limits. The packet's producer-prerequisite repair and binding qualification are not
consumed here; they go to SPEC (below).

**Drafted against:** the availability page at `1c4c5820f`, its last commit, *plus* the companion draft
`_index/candidates/fable-review-astra-ov42-caller-row-preconditions-1002/consumption-draft.md` applied (its edit 4
appends the terminal-phase subsection). The repository HEAD was `c7e2bb2a1` when the draft was written, and the page
had no working-tree changes. The page has CRLF line endings.

- Apply the companion draft first. This draft's subsection refers back to it as "the terminal-phase subsection
  above".
- If the companion draft is not applied, this subsection still appends at the page end. In that case, replace "the
  terminal-phase subsection above" with "the record's caller review" in its first bullet.
- If `git log -1 --format=%h -- <page>` prints neither `1c4c5820f` nor the commit that applied the companion draft,
  re-read the page before applying.

## What the request asks

The request asks FABLE to:

- distinguish the low-16 cost inputs from the later, freshly recomputed full-32 counter input;
- keep the binding and bounded-quotient premises, the normalized mode 17 and the whole-helper NULL precondition;
- record the narrower frontier of transitive cost, stat and counter callees.

Edit 1 does that on the availability page. OPUS owns the ABI widths, the normalized mode and the null
preconditions, and those are routed with suggested text. SPEC owns the producer repair and the binding
qualification.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | Bearing | Lead | Action |
|---|---|---|---|
| availability page (`Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`) | its reason table (row `0x15`) and resource leg already name `00305640` as "the consume path" that clears `+0xE58`, and `00309110` / `00308FF0` as the functions compared with live MP and the Mist charge count | FABLE 10, OPUS 2, others 1 each | **FABLE**: edit 1 |
| type store `_types/fields.tsv` (`AuthoredTableHeader` `+0x08`, `+0x0C`) | two more inverse (divide) readers; the mode, width and null clauses | OPUS | **route to OPUS** (below) |
| battle-unit field map (`Database/FFXII TZA/04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`) | `+0xE58` / `+0xDC8` reset gates; `+0xE54` read by the gil request | Database 28, FABLE 12, SWE2-EC7 9, OPUS 7 | noted only |
| binding consumers of `ca2dd6483` (FABLE's `fable-review-astra-ov42-action-table-binding-1002`, and any page that consumes it) | must also require `binding-qualified-01.json` | per the board request | **route to SPEC** and the binding review's consumer |

The regressions for edit 1 are these checks in `rv_termres.py`, with controls 1-13:

- the first-quotient, cost-input, mode, stats, gil, NULL, own-write, type-switch, counter-leg, terminal-call,
  preview-store and table checks;
- the emulated 65744, random, mode, stats, gil, own-write, NULL, type-switch, repointing and US-table runs.

## Edit 1 (FABLE page): new subsection at the end of the page

Append it after the page's last line, with one blank line between. With the companion draft applied, that line is
"- Whole OV-42 stays OPEN." of the terminal-phase subsection.

```
### FABLE 2026-10-02: what the terminal cost helper reads, writes and passes on (OV-42)

*From ASTRA's packet `ov42-terminal-resource-helper` (`_experiments/evidence/ov42-terminal-resource-helper/README.md`,
`d66234298`), reviewed by FABLE ACCEPT-WITH-NARROWING (record
`_index/candidates/fable-review-astra-ov42-terminal-resource-helper-1002/REVIEW.md`, 55 checks, 0 FAIL, 13 controls).
Static, plus an emulation of the original helper on synthetic units, rows and descriptors with its nine callees
stubbed. The packet's producer-prerequisite repair is SPEC's to accept; FABLE inspected it and did not re-run it.*

- **The call.** The terminal phase (the terminal-phase subsection above) calls `00305640` with the unit, the latched
  row and R8D = 1. It does so only for an entry word outside D0..F1 whose row has bit 30 of `+0x0C`. The special
  sequence follows only after a second bit-30 test.
- **`00305640` (393 B, one `.pdata` record).** It computes the row's quotient again:
  q = ((low32(row) - low32(base)) mod 2^32) / u16 stride, unsigned 32-bit. The base and the stride come from two
  reads of `02EBF138` around one `0020E600` call, with no null test and no zero test. Then:
  - *Costs.* `FUN_00309110` and `00308FF0`, the functions the resource leg above compares with live MP and with the
    Mist charge count, each get the unit and q's low 16 bits.
  - *Stats.* Two further calls (`00305640` + 0xB4 and + 0xCD) get the unit's record `+0x698`. The first gets EDX =
    minus `FUN_00309110`'s result. The second gets EDX = minus (the record's signed WORD `+0x28` times `00308FF0`'s
    result). Both get R8D = 16 + (low 32 bits of the entry R8 != 0). That is 17 from the terminal call. Of the
    helper's four direct callers, three pass 1 and one passes 0.
  - *Gil.* It calls `00253690`, subtracts the unit's DWORD `+0xE54` in 32 bits, and passes the difference to the gil
    call (`00305640` + 0xEB). When the difference is negative as a signed 32-bit value, it passes 0 instead, and a
    32-bit wrap can flip that sign. `+0xE54` is the value that the preview call just before this one stores.
  - *Its own writes.* It writes only DWORD unit `+0xE58` := 0 and WORD unit `+0xDC8` := `0xFFFF` (the consume path
    of reason row `0x15`). It writes them only when the unit and its record are non-null and record byte `+5` is 0.
    It writes neither `02EBF138` nor the table.
  - *The final call.* With byte `+5` = 0, the row's type byte `+0x1E` picks the final call (`00305640` + 0x165).
    Types 0, 1 and 2 pass small constants. Type 10 first makes one call (`00305640` + 0x11C), then reads the
    descriptor again, calls `0020E600` again, recomputes the full 32-bit q and passes it with ECX = 13. Every other
    type makes no final call.
- **Two widths, one premise.** The cost inputs are q mod 65536, and the type-10 input is the recomputed q (emulated:
  q 65744 gives 208 and 65744). The two reads are independent: repointing `02EBF138` during the type-10 leg changes
  only the second quotient (emulated). Under the equal-binding premise q is the routine's entry word, at most 542,
  so the two agree.
- **On this call site the type-10 leg needs an off-premise row.** In all nine shipped language tables the type-10
  rows are 226..241. All of them lie inside D0..F1, which the terminal phase routes around this helper. In the US
  table, none of the 53 bit-30 rows outside D0..F1 makes any final call (types 5, 7, 9 and 255; emulated). That
  includes 511..534, which have type 7.
- **No NULL safety.** The unit test skips only the reset. A null unit reads address 0x698 after the two cost calls. A
  null record reads 0x28 after the first stats call. A null descriptor reads 0xC. A zero stride divides by zero.
  These are source predictions.

So the helper's own effects are the two conditional unit resets, and it rewrites neither the descriptor nor the
table. The sequence row was latched before this call and is not reloaded, but `00306760` divides it by the
descriptor that it reads afterwards (queue-writer subsection). So a rebinding of the descriptor or the table by any
of the helper's nine callees would change the queue's quotient. Whether one of them does is the open frontier.

**Limits kept.** These limits are ASTRA's and FABLE's.

- The native effects of the cost, stats, gil, type-10 and final callees, and of `0020E600`, are not read. That
  includes any table or arena rebinding, any callback scheduling and any owner change in the window before the
  special sequence.
- Equal binding (base low32 and positive stride), table initialization and binding, and stable unit, record, row and
  descriptor state are premises. So are the Win64 ABI and table addresses below 4 GB.
- The 65744 case and the repointed descriptors are supplied states run through the original bytes, not native runs.
  No natural row, live counter call or natural reach of this call site is shown.
- No canonical cost census is credited here. The cost and gil semantics are the page's existing ones, consumed and
  not re-tested.
- Whole OV-42 stays OPEN.
```

### Citations and the neighbour gate

The new text cites these 8-digit tokens, and every one is already on the page at `1c4c5820f`, so none is new:

- functions: `00305640` (as an entry and as `00305640` + 0xNN call sites), `00308FF0`, `00253690`, `0020E600` and
  `00306760`, plus `FUN_00309110`, written in the same form as the page's resource leg (the page cites it only as
  `FUN_00309110`; if the address gate does not read that form as a citation, nothing new is imported either way);
- the data cell `02EBF138`.

These are **named by call site** (`00305640` + 0xNN) or by role, and not by entry, so that no new caller edges are
imported:

- the stats callees `00300CE0` and `00300BC0`;
- the gil call `00254EE0`;
- the type-10 call `00316440`;
- the final call `00253770`;
- the preview `00303830`, together with its `+0xE54` store at `00303830` + 0x124;
- the other three callers `00307300`, `00313120` and `003191B0`.

No `.text` data address and no non-address 8-digit constant is written.

The neighbour pre-check (`xlayer.py`) was **not** run. Before publishing, FABLE should run `xlayer.py --only
00305640,00309110,00308FF0,00253690,0020E600,00306760` (and the full-page edge diff) on a staged copy. Check
especially the new `00305640` + 0xNN call-site citations, which point into callees the page does not cite.

## Route to OPUS: ABI widths, normalized mode and NULL preconditions

The board request assigns these to OPUS. Placement is OPUS's choice. Suggested text:

```
- 00305640 (FABLE review of ASTRA `ov42-terminal-resource-helper`, 2026-10-02,
  _index/candidates/fable-review-astra-ov42-terminal-resource-helper-1002/REVIEW.md):
  - AuthoredTableHeader inverse readers, fourth and fifth sites: + 0x2E (+0x0C key) / + 0x4B (+0x08 stride) ->
    + 0x50 `div r10d`, and + 0x128 / + 0x13C -> + 0x143 `div ecx`; both unsigned 32-bit, no zero test, two separate
    loads of 02EBF138 around 0020E600 in each.
  - Widths: 00309110 and 00308FF0 get `movzx edx, di` (+ 0x81, + 0x8C), q mod 65536; 00253770 gets the full 32-bit
    recomputed q (+ 0x14A `mov edx, eax`) with ECX 13 on row type 10 only.
  - Mode: R8D = 16 + (low32(entry R8) != 0) to 00300CE0 and 00300BC0 (+ 0xA3 `test r12d, r12d`, + 0xA8 `setne`);
    the raw flag is not forwarded. Raw direct callers: 00304850 + 0x6E8, 00313120 + 0x197 and 003191B0 + 0x107
    pass 1; 00307300 + 0xB9 passes 0.
  - Stats arguments: 00300CE0(record, -(00309110 result), mode); 00300BC0(record, -(sext16(record+0x28) *
    00308FF0 result), mode); record = QWORD unit+0x698, read twice without a null test.
  - Gil: 00254EE0(ECX = (low32(00253690() - unit DWORD +0xE54) signed >= 0) ? that : 0).
  - NULL preconditions: unit (the early test gates only the reset; + 0x99 reads [unit+0x698] unconditionally),
    record (+ 0xC4 reads WORD +0x28), descriptor (+ 0x2E reads +0x0C), stride > 0 (both divides).
  - Own non-stack writes: + 0x73 DWORD unit+0xE58 := 0 and + 0x7A WORD unit+0xDC8 := 0xFFFF, gated by unit, record
    and record byte +5 == 0.
```

## Route to SPEC: the producer repair and the binding qualification

The packet asks SPEC to review its final proof, its controls and the additive `binding-qualified-01.json`. It also
says that existing consumers of the binding packet `ca2dd6483` must require that qualification and inspect the
old-PASS / new-FAIL counterexamples.

FABLE inspected the recorded artifacts and did not re-run them. With extent `complete` false:

- the old helper producer exited 0 with `producer_complete` true, and the current one exited 1;
- the old binding producer exited 0, and the new qualification exited 1;
- the other three helper refusal cases exited 1.

FABLE's own binding review, `_index/candidates/fable-review-astra-ov42-action-table-binding-1002/`, does not yet name
the qualification. Its consumption should add `binding-qualified-01.json` as a precondition before it is applied.

## Noted, outside this package

The battle-unit field map's `+0xE58` and `+0xDC8` rows could record the three gates of `00305640`'s reset: unit,
record, and record byte `+5` = 0. Its `+0xE54` row could record the gil request's 32-bit subtraction. That page is
led by the Database prefix, so this is noted and not proposed.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edit 1)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_termres.py` at HEAD c7e2bb2a1 (55 checks, 55 PASS, 0 FAIL, 13 controls)
