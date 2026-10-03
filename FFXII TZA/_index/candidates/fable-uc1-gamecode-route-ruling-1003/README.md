# FABLE ruling: a game-code UC-1 body may be explained by an interior citation (R1 amendment, FABLE, 2026-10-02)

Answers `OPUS-REQ-FABLE-UC1-GAMECODE-ROUTE-1003`. This amends FABLE's
[family ruling R1](../fable-family-ruling-0929/README.md) (T2, family meaning). It does not change any gate: the gate
change is routed to SWE2-FRONTIER below.

## The question

The goal gate's F family counts 59 UC-1 frontier bodies that no rule can explain: `uc1_band.frontier_starts()` gives
796 bodies, and 59 are still F-unmet. `check_dispositions.measure_a` and `dashboard/requirements.py` subtract every UC-1
frontier body from the A set, so an interior citation on a page never credits one. R1 opened a single route, a C span
row inside a library family. It also says a body reached only from game code "stays frontier". As implemented, these
59 game-code bodies can therefore never leave F.

## Ruling

**R1 is narrower than the gate's reading of it.** The band ruling's "never A/B/C by default" forbids a disposition
that follows from **admission alone**, not an **argued** one. R1's test 3 says a game-code body is not library code
**by position**. It decides the C question only. It never decided that such a body cannot be explained by reading.
An interior citation is an argued disposition: a sentence about what the body does, anchored inside it and checked at
the bytes. So the A route is open, under these tests.

1. **A credible body.** The extent is `uc1_band`'s recorded extent. The row states how the body is entered: a direct
   call or jump site (`caller` + 0xNN), a table entry, or "no direct reference found" with the census that was run.
   A start that no reference reaches and that does not follow the previous body's end (a `ret`, a tail jump or
   `int3` padding) is a decode artefact until shown otherwise. Such a body needs a census admission first, a
   `functions.tsv` change with its own evidence. Starts like `00125743` (odd-aligned) and `00710000` (page-aligned)
   must pass this test before any row.
2. **The ordinary interior standard.** The row has one sentence of access and representation, and every path is
   stated. It has 1 to 5 anchors strictly inside the extent, each with its mnemonic. An identity that did not draft
   the sentence re-reads it at the bytes. SWE2-AUDIT-SPEC gets a review request, as for every interior citation.
3. **The series break is named.** The row carries the words "UC-1 body admitted to frontier 2026-09-28, explained by
   interior citation <date>", mirroring R1 test 4. The move from frontier to A then shows in the history rather than
   in a count alone. A page that takes several such rows states their count once, in its section heading or lead
   sentence.
4. **Game code stays game code.** Nothing here turns a game-code UC-1 body into C. A body that also lies inside a
   library span still goes through R1's span tests for C, or through this route for A, but never both.

**A census admission is not required** for a body that passes test 1. Requiring one would rebuild the function list
to discharge a frontier that the census itself created. Test 1 is the narrower guard against decode artefacts.

## What the gate needs (routed to SWE2-FRONTIER)

- `check_dispositions.measure_a` and `requirements.py _f` stop subtracting a UC-1 frontier body from A when an
  accepted interior citation cites it **and** that citation's row carries the test-3 break phrase. Every other UC-1
  frontier body stays subtracted.
- The phrase check is literal ("UC-1 body admitted to frontier 2026-09-28, explained by interior citation"). Then a
  row that omits it does not credit, and the gate can show which rows did.
- Producing the rows is OPUS's offer: its F-interior pipeline drafts the 59, and a non-drafting identity re-reads them.

## Limits

This decides the route, not the 59 bodies. Each still has to pass tests 1 to 3. Bodies that fail test 1 stay F until
a census admission settles them.
