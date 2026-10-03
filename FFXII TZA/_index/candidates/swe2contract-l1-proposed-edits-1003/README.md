# OPUS's L1-audit proposals to the contract owner: three applied, one routed for review, one qualified (SWE2-CONTRACT, 2026-10-03)

Request: `OPUS-REQ-CONTRACT-L1-PROPOSED-EDITS-1003`, from OPUS's
[L1-contract audit](../opus-audit-l1-contracts-1003/README.md) (the user's audit follow-up §7, "contract maturity
represented honestly"). Each proposal was checked against the shipping bytes or the contract template before anything
was applied. Written by the Claude stand-in operating SWE2-CONTRACT while the lane's Devin session was rate-limited.
OPUS's census was re-run first and gave the same figures (107 contracts; 78 L2 / 29 L1; level against scope and
against §13 class as OPUS printed).

## Item 1 — relabel `CONTRACT-authored-command-ramp-channels.md` to L2: ROUTED, not applied (SWE2-CONTRACT)

The request itself says "after a non-author review", and the review policy puts a contract-definition change at T2,
which needs the lane's auditor. SWE2-CONTRACT cannot be that reviewer: it wrote this contract's DIFFERENTIAL TESTED
evidence (`diff_ramp_channels.py`, `a27b5cc5`) and its gate repair. OPUS created the contract and ran its only
falsification pass, and FABLE set its scope.

The facts the relabel rests on, checked for the reviewer at HEAD:
- front matter `scope: subsystem` (FABLE, `3981ee43d`), `readiness: DIFFERENTIAL TESTED`, `confidence: PROVEN`;
- it is the only contract on S-48: the registry row lists it alone, and no other `CONTRACT-*.md` names S-48;
- the S-48 verdict row is MET, re-scored by SWE2-AUDIT-SEM on 2026-09-22, who also checked the contract's substance
  against the bytes;
- no gate reads a contract's `level:`: goal_gate and progress do not, and only the knowledge.sqlite mirror stores it.
  So the relabel moves no figure.

It also holds under the goal revision's definition of the key (L2 = reconstruction-grade; see item 4): a
differentially tested subsystem contract on a MET system meets that bar. Routed as
`SWE2CONTRACT-REQ-AUDITSPEC-RAMP-LEVEL-L2-1003` (SWE2-AUDIT-SPEC), with the exact one-line edit.

## Item 2 — `CONTRACT-storage-read-completion.md` §14.1 had no register row: APPLIED, and narrowed (SWE2-CONTRACT)

Registered as **SRC-1** in a new `SRC` section (prefix checked free), and the contract's §14.1 now names it. While
registering it, the question was **narrowed statically**, because the wrapper `00862590` has only two direct callers:
- `003BA990` compares the result with the requested size (`003BABC2` `cmp ebx, [02B40EF8]`; mismatch path `003BABF9`),
  so a short read's `0` is treated as a failure there.
- `003BA7B0` does not test it at either site (`003BA882`, `003BA8AE`). It sets the state word `02B40E14` to 8
  unconditionally, and its one listed caller `003BB790` overwrites `eax` at `003BB815`.
- Open: whether that state-8 continuation notices a partial buffer by another route. An indirect entry to either
  caller is not excluded by a call-graph census.

## Item 3 — `CONTRACT-preparation-step-family.md`'s out-of-range-slot question: APPLIED, answered "no" (SWE2-CONTRACT)

[`recipe_slots.py`](recipe_slots.py) decodes all 109 recipes of the table `01EF96C0` from the image, both
`-1`-terminated lists of each ([`recipe_slots.out`](recipe_slots.out), FAILS 0):
- 563 slot values, smallest 0, largest 201. Every one indexes the 202-entry step table.
- K1 checks the table's own end marker. K2 checks the decoder against weapon-recipes RW-2's recipe 25. K3 is a
  sensitivity case showing the range check flags 202 and -2.
- The table is not rewritten in play. `globals_index.py` finds no rip-relative reference to it, and
  `disp_image_census.py` finds only two `.text` operands at its image-base displacement, both reads: the two
  dispatchers at `003859BD` and `0038635D`.

§4's unchecked index remains, correctly, a modding hazard: an edited list with a slot of 202 or more still calls
through whatever follows the table.

## Item 4 — the template's `level:` line: QUALIFIED, not applied as proposed (SWE2-CONTRACT)

OPUS proposed documenting that the key "records scope, not maturity". **The template's key has a defined meaning.**
It entered the template with the goal revision (`79655c0c9`), whose §1 defines L1 / L2 / L3 as the maturity grades
MODDING-GRADE / RECONSTRUCTION-GRADE / PARITY-CERTIFIED. Writing "records scope" into the template would redefine a
project-level term from inside a template.

What the census does show is that **the values, as populated, do not measure that grade**:
- 101 of 107 contracts follow scope; the six exceptions are the ramp contract and five L2 contracts narrower than
  subsystem;
- all 29 L1 contracts have executed §13 evidence, against 35 of the 78 L2 contracts.

The template now carries a **caution** saying exactly that: do not read `level: L1` as weaker evidence, and read
maturity from readiness, confidence, `audit.passes` and §13 instead. The choice between re-deriving the values
against the definition and redefining the key is routed to FABLE (semantic owner), with OPUS as the proposer, as
`SWE2CONTRACT-REQ-FABLE-CONTRACT-LEVEL-KEY-1003`.

## The promote rows (SWE2-CONTRACT)

The request notes that promote rows 5, 6, 8 and 17 "name their missing work in the README". They do (OPUS's table
above). The work they name belongs to each contract's owner and is not part of this request's edits. Item 1 settles
row 21; row 24 is the S-38 verdict owner's.
