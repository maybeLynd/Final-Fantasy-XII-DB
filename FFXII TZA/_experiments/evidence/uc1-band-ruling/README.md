# ASTRA UC-1 ruling — 2026-09-26

**APPLY BY BAND WITH A ROW EXCEPTION; do not apply the proposed 694 unchanged.**
This answers `FRONTIER-REQ-ASTRA-UC1-BAND-RULING`. It is a voter's original-byte
falsification, not independent acceptance of my own production and not a denominator
edit. FRONTIER coordinates application; OPUS owns population/extent adjudication;
FABLE owns the semantic ruling. The existing auditor receipt
`Database/Tools/work/SWE2-AUDIT-SPEC/UC1-BAND-CORROBORATION.md` already corroborates
the earlier rates and 694-row selection. It does not test the new reachable-extent
collision. Only that changed finding and its dependent admission require new review;
the unchanged historical measurements are retained.

## Question and method chosen before work

Are the smallest proposed shipping blocks distinct bodies, predecessor tails,
multiple routines, or mixed code/data? Existing evidence is the Sept13 admission
rule, OPUS's Sept25 table rejection and FABLE's per-row ruling. A decode percentage
cannot distinguish all these hypotheses. Method A, verified shipping instruction
bytes plus a bounded reachable-instruction check, is sufficient to falsify a proposed
extent. No runtime initialization, scheduling or presentation question is involved.
Budget: one focused offline review; no game, instrumentation or original-code execution.
Failure conditions: stale/mismatched row inputs, wrong executable identity, zero-case
controls, or reachable instruction boundaries outside the proposed extent.

The inputs and Capstone version are recorded in `observation.json`. EXE SHA256 is
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Canonical inputs are read directly; no SQLite mirror or unwind metadata is evidence.
The request's 701 uses the generator's `[1,64)` size band; FABLE's 704 includes 64 B.
These are different intervals, not three additional discoveries. Current membership
and extents agree between the admission TSV and FABLE's inclusive 1–64 B TSV.

## New discriminating result: 007EE7C0 is truncated and collides with a listed row

FABLE proposes admitting `007EE7C0`, 48 B, despite `decodes_to_end=no`.
Original bytes show reachable paths for mode 0, mode 1 and the remaining branch.
The mode-2 store starts at `007EE7EF`:

```
007EE7EF 41 89 89 38 01 00 00  mov dword ptr [r9+0x138],ecx
007EE7F6 33 C0                 xor eax,eax
007EE7F8 C3                    ret
```

The proposed half-open extent ends at `007EE7F0`, inside that store. Extending the
original-byte observation to `007EE7F9` (57 B) contains all reachable instructions
and the three return exits. The control accepts 57 B and rejects 48 B.

`functions.tsv` separately lists `007EE7F0`, 9 B. Its entry is inside the same
instruction (after the REX prefix), so these cannot be treated as two independently
proved, disjoint function extents. The image also contains a genuine decoded RIP LEA
at `007EC4F1` in listed `007EBAD0`, targeting `007EE7C0`. This validates an address
reference, **not normal invocation or the lifetime of a stored method pointer**.

The focused direct call/branch scan finds neither start in its decoded supplied
listed/admitted ranges. Its positive control finds all four predecessor branches
to cold tail `0076666F`. That absence does not exclude indirect callers, decode gaps,
unscanned table routes or a deliberate alternate entry at `007EE7F0`.

**Hold this one row for OPUS adjudication:** establish whether the 9-B listed row
is a false entry or an intentional alternate entry, correct/deduplicate the extent
representation accordingly, and revalidate its consumers/dispositions. Do not add
48 B unchanged or automatically delete the listed row on a negative reference scan.

## Other proposed rows and the cold-tail data boundary

The remaining **693** proposed `admit` rows have no reachable missing or interior
instruction boundary under this added check. This is compatible with applying that
qualified small band as unexplained frontier after independent corroboration; it
does not prove their universal semantics, indirect boundaries or runtime reachability.
FABLE's two x87 helpers at `00125743` (16 B) and `00125753` (17 B) each reach their own
return with balanced 8-B stack reservation/restoration. Preserve the split, four
ambiguous rows and five predecessor-tail relationships.

There is a separate limit on the tail at `007C2A29`: the 47-B splitter block contains
`call 00809728` then `int3` (6 B), one alignment NOP at `007C2A2F`, and ten dword RVAs
at `007C2A30..007C2A57`, all targeting its predecessor. Preserve the predecessor
relationship, but **do not call all 47 B executable tail instructions**. OPUS should
represent the code/data distinction when extending the recorded extent. Whether a
particular extent convention includes owned inline data is the owner's decision;
the body count does not increase for this tail.

The two unaligned import candidates `00862028` and `00862034` are exact 6-B RIP
indirect jumps. Their observed instruction shape is preserved; no import resolution
or invocation was tested. Larger bands remain NOT YET under the prior ruling.

## Controls, limits, and downstream obligations

Reproduce from repository root with the existing Python environment:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/uc1-band-ruling/review.py"
```

`validation.txt` records a nonzero 704-row check, seven flow controls (including
explicitly synthetic detector bytes), and four actual cold-tail branch controls.
Raw bytes, decoded instructions and observed reachable offsets are retained in
`observation.json`; `manifest.json` seals this package. A deliberately cut instruction
and a branch into an instruction's second byte are rejected. Complete helper/import
and corrected 57-B candidate controls are accepted. No broad mutation campaign ran.

This check is deliberately narrow: it uses supplied decoded ranges, models calls as
returning, treats external direct branches and indirect jumps as exits, and does not
recover all table dispatch targets. It does not prove that the other 693 are never
fragments. Absence of a decoded direct interior branch cannot support that universal
claim. FABLE's current statement "none ... is a fragment" needs this limitation.

Propagation state: **PENDING OWNER ADJUDICATION / INDEPENDENT CORROBORATION**.
Affected consumers are FABLE's Sept25 band ruling/TSV, OPUS's admitted-row generator
and listed-function extent/disposition consumers, the UC-1 canonical population
decision, and future denominator/coverage accounting. None is silently rewritten by
this package. Actual N must come from deduplicated applied rows, not the numbers here;
keep the held collision, ambiguous rows and larger bands visible with provenance.
Historical figures retain their populations and the application records a series break.

Cleanup: read-only original/reference inputs, no FF12 process or control session
launched, no saves/config touched. No detach or live restoration is claimed.
**DB_GOAL=NOT_MET.** This ruling resolves a preparation question, not database completion.

Player version: one proposed routine was cut in the middle of an instruction and
counted alongside a questionable second entry. Another tail contains both instructions
and a jump table. Keeping these distinctions prevents misleading coverage and tells
the owners exactly what to repair before counting the missing code.
