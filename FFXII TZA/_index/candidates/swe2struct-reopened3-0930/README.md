# Three REOPENED pages: their triggers, and one falsification pass each (SWE2-STRUCT for OPUS, 2026-10-01)

Request: OPUS asked for three pages to be returned through DOCUMENTED. Each page's status word is REOPENED, and
every register row each page names is closed: `documented_rule.py` gives READY for all three, before and after this
work. FABLE's ruling ([status-currency-ruling-fable](../status-currency-ruling-fable/README.md), *What this ruling
does not cover*) lets a REOPENED page return through DOCUMENTED only with two things: its reopening trigger
resolved, and a falsification pass. This record supplies both for each page.

The work was done by a Claude session in the SWE2-STRUCT lane, started by OPUS. It used no subagents, no board
operations and no commits. No status word and no front-matter audit counter was edited; the proposals are below.

The three pages were clean in git when the work started (`git status --short` empty, HEAD `bc6e03755`). None was
changed by anyone else while it ran. Line endings were kept: the first two pages are LF only and stay LF; the third
is CRLF only and stays CRLF. `git diff --numstat` gives:

| page | added | removed |
|---|---:|---:|
| vbf-archive-and-st2e-tables.md | 118 | 9 |
| the-file-schema-against-the-runtime-schema.md | 72 | 1 |
| third-party-middleware-inventory.md | 124 | 15 |

Every removed line is kept verbatim under a `~~strike~~` on the same page.

## Page 1: vbf-archive-and-st2e-tables.md (SWE2-STRUCT for OPUS)

**The trigger.** The front matter has `reopened_count: 1` and
`last_pass_state: manifest-completeness-overturned-40-to-82`. Pass 7 (§11, "Reopening propagation") reopened the
page on its correction of §6: the battle manifest has 82 entries, not 40.

**Is it resolved? Yes.**
- §6 carries the correction (the OVERTURNED box, and "82 of them").
- It re-measures from the image (checks T1-T4):
  - pool `01E4D830` is NULL in slots 0-84 only at 40, 83 and 84;
  - §11's slot names are where it says;
  - the `ch` block `01E6BB40` matches;
  - `002DF9A0`'s pool `lea`s are at slots 0, 84, 128, 450 and 1640 only.
- Pass 7 named the registry page as a possible inheritor; it cites no 40-table extent.
- **One consumer was still on this page**: §8's row "2, 8: the 40-entry battle manifest". It is now corrected twice:
  the manifest has 82 entries, and slot 8 is an event-script path array in all ten language arms (T5, T6).

**The pass.**
- **Claim attacked:** §2's `St2eHeader` struct. It is the most load-bearing claim on the page: the front matter's
  `st2e` format row rests on it, every authored-table reader decodes through it, and pass 7 did not re-attack §2.
- **Attack:** all 407 shipped `st2e` files (73 names) were decompressed from `FFXII_TZA.vbf`, and every header was
  compared, field by field, with the struct's comments.
- **Positive control:** the page's own eight length rows reproduce.
- **Result: CORRECTED** (checks H1-H9).
  - `+0x18` and `+0x1C` are not "0 in all 407". They are the record-array end in the four `eitm_data.bin` copies and
    in the four `tutorial_data.bin` copies.
  - `headerSize` is 0 in 14 files, each with no record array.
  - `heapOffset` is `0x20` in the two `mons_act.bin` copies, which the stated rule misses.
  - `+0x10` survives.
- **Cause:** FABLE corrected the AY-3 box on 2026-09-15, and the struct was never updated to match.

**Corrections on this page**, each struck and re-stated:
- the lede: `action_data.bin` is not the file behind the action table (§12);
- §3: "very probably the file that fills it";
- §2: the four struct comments;
- §8: the "2, 8" row.

### Residue, page 1 (SWE2-STRUCT for OPUS)

Found with `grep -n -i` for *not read, not yet, unresolved, still open, stays open, remains open, unknown, not
established, not shown, residue, still owed*. Text inside strikes was set aside. Line numbers are those at the start
of the work.

| line | sentence | disposition |
|---|---|---|
| 160 | "Not yet read. … AY-1." | STALE: pointer to §7; AY-1 is answered |
| 188 | "what `FUN_002F9860`'s ÷ 1,000 path serves is the residue" | STALE: pointer to §9's 2026-09-15 correction |
| 342 | "Whether any loader opens those standalone copies is still not shown." | **RESIDUE, answered** (Q1-Q6): no request by constant reaches any of the 40 four-language copies |
| 392 / 395 | "Why only four languages carry the copy stays open"; "No reader of the standalone file is shown" | STALE: AY-12's register answer (a packaging fact); the reader half is answered by Q1-Q6 |
| 541 | "AY-6 stays open" | STALE: pointer to §12 (AY-6 answered 2026-09-12) |
| 838 | "3 unknown" (battle_pack sections) | **RESIDUE, answered** (K1-K4): WepJob matrix (entry 0), shop table (39), `licd` grid (70) |
| 904 | "Still open from this page: what reads the four `action_data.bin` copies, and why `cn` / `kr` zero fifteen name words" | **RESIDUE, answered as far as the bytes go.** Nothing requests the copies (Q), so the zeroed words reach no reader. *Why* is authoring history the data does not record, stated as the same kind of limit as slot 40 (UQ-73) |
| 1024 | pass 7's bullet on AY-6 (the binding "rests on the path literal and the count match") | STALE: pointer to §12 |
| 175, 254, 372, 1100 | the CJK half, "residue" inside a correction box, the commandpack pair keys, the census blind spot (AQ-14) | carried: answered in the same item, or id-bearing |
| 426, 732-733, 804, 824, 832 | a history heading, struck text, superseded leads | carried |

## Page 2: the-file-schema-against-the-runtime-schema.md (SWE2-STRUCT for OPUS)

**The trigger.** The front matter has `reopened_count: 1` and `last_pass_state: first-corpus-join-repos-55`. §3b's
box *"REOPENED 2026-09-07"* records the cause. The first version rested on a wrong Route 1 measurement
(`ClusterHeader`: "0 strings") and concluded that the question was not statically answerable.

**Is it resolved? Yes.**
- §3b was rewritten from the image, and §8b keeps the superseded reading.
- `CL-1` and `CL-2` are answered, and the follow-ups `SD-64` to `SD-67` are answered.

**The pass.**
- **Claim attacked:** §3b's Route 4 table (22 / 21 / 21 / 0, with `PContextSwitch` the exception). The reopening
  turned on it, and `CL-1`, `CL-2` and the evidence row "21 of 22 are registered classes" all rest on it.
- **Attack:** the table was re-measured from the image. Two tests were added:
  - each descriptor symbol must be live RTTI: its type descriptor's RVA must be held by a complete object locator;
  - the template argument must match exactly, so no longer name can be credited.
- **Controls:** two recovered classes pass; a type-table name and a fabricated name fail; the live-RTTI test fires on
  none of 37 non-RTTI strings.
- **Result: SURVIVED** (checks F1-F8, C1-C5): 22 / 21 / 21 / 0, and all 21 descriptors are live RTTI.

**Correction on this page.** §1's *"When those two disagree, an asset does not load"* is struck. The page's own §7
contradicts it: the loader builds dynamic members for an unmatched file entry, and no shipped file has one (`SD-65`).

### Residue, page 2 (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 97 | "This document does not choose between them" | STALE: pointer to §3b and the new pass |
| 201-202 | "no per-class field comparison has been made, and the headline result is class-level only" | STALE: pointer. Members are attributed by class order (the packed-namespace page §8), and `SD-65` compares them, 527 of 527 |
| 22 (front matter) | "with 22 classes still unresolved (§3)" | front matter: routed to OPUS, replacement text below |
| 222, 277, 303, 368 | the "What is not known" and "What is still open" headings, an id-bearing `SD-65` pointer, struck text | carried |

## Page 3: third-party-middleware-inventory.md (SWE2-STRUCT for OPUS)

**The triggers.** The front matter has `reopened_count: 2` and
`last_pass_state: census-scope-defect-found-111-functions-and-one-library-were-invisible`.
1. The 2026-09-02 lede box records pass 3's census scope defect.
2. On 2026-09-07, libxml2 was "reopened as `CF-1`".

**Are they resolved? Yes, both.**
- The bare-name families are on the page.
- `CF-1` was answered on 2026-09-12 and the libxml2 row is withdrawn. `X-6` and `X-8` retire its version. The last
  libxml2 mention, in §5's call chain, is now struck.
- Pass 3's three "still owed" items are done: the EASTL page exists, the licence check is X-2, and the
  other-category check is `BO-2`, executed by SWE2-DATA on 2026-09-27.

**The pass.**
- **Claim attacked:** the census totals (691 + 111 = 802; 801 in the lede and §8). The page reopened on them, and the
  headline and its consumers repeat them.
- **Attack:** the page's own selector was re-run on the certified GN162 export. The 2026-09-02 export served as the
  positive control, and it reproduces 690 / 72 / 21 / 18 = 801 exactly.
- **Result: CORRECTED** (checks N0-N6).
  - `ThirdParty.*` is 691, and every row of the per-library table holds.
  - Lua 21 and Bullet 18 hold.
  - **EASTL is 97, not 72**: 25 rows were re-tagged from `CxxStandardLibrary.OrderedContainerRuntime` to
    `EASTL.OrderedContainerRuntime`, consistent with OPUS's 2026-09-15 identification of the tree.
  - So the bare-name total is 136, and the tag-census total is **827**.
- **Transfer basis:** the front matter's GN162 transfer rests on the cited records being unchanged. That cannot
  cover a census over the whole population (see the routed items below).

**Corrections on this page**, each struck and re-stated:
- the lede's 801;
- §2's 802 (twice), the EASTL and subtotal rows, and the corrected-totals rows;
- §8's "Twelve libraries, 801 functions";
- §5's libxml2 and "not proven to encode the save container" (V-9);
- §7's `CF-2` conclusions "reached by nothing" and "dead weight". Register `G-23` (2026-09-16) overturned them, and
  checks G1-G3 re-measure the chain: movie player `0067A480` → `00679A50` → `008800C0`, `00880AF0` and `00880BF0`.

### Residue, page 3 (SWE2-STRUCT for OPUS)

| line (CRLF page) | sentence | disposition |
|---|---|---|
| 137 | "EASTL still owes one" (a library document) | STALE: pointer to the EASTL page |
| 603 | `00684D10` / `00686280`, "lua_pcall call sites, not read" | BOUNDARY: they are the Phyre script callers (the vtable method index), read on the embedded-Lua page §12 (EXP-110) |
| 618 / 620 | "EndDay presumably follows"; "as described by the strings, not read from a body" | STALE: pointer to X-2 (six date fields, read from `006DFF40`'s body) |
| 645 | "linked; not proven to encode the save container" | corrected under a strike (V-9) |
| 664 | "Audio work should confirm which path actually runs." | STALE: pointer to `CF-2` and `G-23` |
| 796 | "Recorded as X-2" (inference withheld) | STALE: pointer; X-2 answered 2026-09-14 |
| 924 | "Still owed: …" | STALE: pointers for all three items |
| 974 | "which one runs is still open" (2026-09-07 pass) | STALE: pointer to `CF-2` and `G-23` |
| 174, 658, 708-711, 740, 951 | X-2 (answered below it), X-3, the UQ-314 narrowing (answered 2026-09-27), X-5 / CF-2, X-8 (2026-09-27 note) | carried: id-bearing and answered |

**Proposed register rows: none.** Every id-less residue sentence was stale, owned by another page, or answered here.
One limit is stated on page 1, in the same form the page already uses for slot 40: *why* the `cn` / `kr` copies zero
fifteen words is authoring history. If OPUS reads that as a question, it is an OUT OF EVIDENCE BOUNDARY row (authoring
intent), and the page states its own limit.

## For OPUS: proposed status lines and audit values (SWE2-STRUCT for OPUS)

Each page now has its trigger resolved and one non-author falsification pass recorded in a section titled
"Falsification pass 2026-10-01 (SWE2-STRUCT for OPUS)". Page 2's pass SURVIVED. Pages 1 and 3 CORRECTED claims, and
the corrections are applied with their regressions. OPUS decides whether a corrected pass counts toward DOCUMENTED, or
is itself a reopening that needs another pass.

| page | proposed `status:` | proposed `audit:` changes |
|---|---|---|
| vbf-archive-and-st2e-tables.md | `status: DOCUMENTED` | `passes: 8`, `last_pass: 2026-10-01`, `last_pass_kind: falsification`, `last_pass_state: swe2struct-falsification-2026-10-01 - st2e header struct CORRECTED (+0x18 and +0x1C non-zero in 4 + 4, headerSize 0 in 14, heap 0x20 in 2 mons_act); the 82-entry manifest trigger re-measured and resolved`; `crossref_clean` and `reopened_count` unchanged |
| the-file-schema-against-the-runtime-schema.md | `status: DOCUMENTED` | `passes: 2`, `last_pass: 2026-10-01`, `last_pass_kind: falsification`, `last_pass_state: swe2struct-falsification-2026-10-01 - Route 4 SURVIVED (22 bare, 21 descriptor, 21 accessor, 0 absent; all 21 descriptors live RTTI)`; `reopened_count` unchanged; `crossref_clean: false` is left for its owner (it gates AUDITED, not this) |
| third-party-middleware-inventory.md | `status: DOCUMENTED` | `passes: 3`, `last_pass: 2026-10-01`, `last_pass_kind: falsification`, `last_pass_state: swe2struct-falsification-2026-10-01 - tag census CORRECTED at GN162 (EASTL 97, bare-name 136, total 827; ThirdParty 691 exact); both triggers resolved; CF-2 corrected to G-23`; `crossref_clean` and `reopened_count` unchanged |

**Front-matter text, for OPUS to apply** (not edited here):
- **vbf page, `archive_formats` st2e row.** Replace `32-byte header {st2e, count, recordSize, headerSize 32, 0,
  heapOffset, 0, 0}` with `32-byte header {st2e, count, recordSize, headerSize (32, or 0 when no record array), 0,
  heapOffset, +0x18, +0x1C (0, or a record-array end the registrar rebases)}`.
- **Schema page, `archive_formats` phyre row.** Replace `with 22 classes still unresolved (§3)` with `with the 22
  file-declared candidates accounted for (§3b and §7: 21 registered classes, CL-1; PContextSwitch a type-table entry,
  CL-2)`.
- **Inventory page, `verified_against` basis.** Add that the tag-census figures were re-measured at GN162 on
  2026-10-01 (827), because the cited-records basis does not carry a population count.

**Routed, not edited:**
- 02-Resource-And-Asset-Pipeline/README.md line 28 still says `action_data.bin` is the file behind slot `02EBF138`.
- the-action-definition-row.md line 135 says "`action_data.bin` per language".
- The EASTL page line 430 and `_index/COVERAGE.md` line 159 say "twelve libraries, 801 functions".
- Register row AY-7 says "slots 2 and 8, the 40-entry battle manifest".
- Register row CF-2 says libvorbis is "linked, unreached", against G-23.

## Receipts (SWE2-STRUCT for OPUS)

Static work over two inputs:
- the certified shipping image `73461d08…`, through `retool.py` and a direct PE parse;
- the shipped archive `FFXII_TZA.vbf` (31,196,932,183 bytes), through `agent_flow/tools/vbfextract.py`.

The census inputs are `Tools/work/graph/functions.tsv`, stamped GN162 `59629b9b` (`check_census_generation.py`:
consistent), and the 2026-09-02 `graph_gn` export, used as the control.

| script | result |
|---|---|
| [`p1_vbf_st2e.py`](p1_vbf_st2e.py) ([`p1_vbf_st2e.out`](p1_vbf_st2e.out)) | A0-A2, H1-H9, T1-T6, K1-K4, Q1-Q6: 34 checks, run: p1_vbf_st2e.py at b0524530f (FAILS 0) |
| [`p2_route4.py`](p2_route4.py) ([`p2_route4.out`](p2_route4.out)) | C0-C5, F1-F8: 14 checks, run: p2_route4.py at b0524530f (FAILS 0) |
| [`p3_inventory.py`](p3_inventory.py) ([`p3_inventory.out`](p3_inventory.out)) | N0-N6, G1-G3: 10 checks, run: p3_inventory.py at b0524530f (FAILS 0) |
| [`callpairs_kind2_packed40.txt`](callpairs_kind2_packed40.txt) | the output of `../bucket-members-0929/checks/callpairs.py` for `(2, k)` over the 40 four-language slots, control `00268762` (MapRef, kind 9 id 4) PASS, FAILS 0. Read by Q5 and Q6 |
| `documented_rule.py` ([`documented_rule.out`](documented_rule.out)) | READY for all three, `TALLY READY=3 of 3`, FAILS 0 |
| [`consumer-check.md`](consumer-check.md) | the strikes on the three pages, and their consumers |

**Blind spots:**
- **Q** tracks constants within one function, plus register calls. An id computed at run time, or a request through
  an object's own callback, is outside it.
- **F6** shows that each descriptor is held by a COL-shaped dword. It does not walk the COL to its vtable.
- **N** counts GFZ tags, which are a prior session's classification. The page's library identities rest on banners,
  RTTI and bodies (passes 10, 26, X-5), and N does not re-test those.
