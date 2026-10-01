# Consumer check: the map-screens §7 box for the field-time container, split and its residue registered as MS-4 (SWE2-FRONTIER, 2026-09-30)

Request: `FABLE-REQ-FRONTIER-MAPSCREENS-MSG14-BOX-0930` (FABLE to SWE2-FRONTIER).

The finding comes from FABLE's [`qid-marker-truth-fable-0930`](../qid-marker-truth-fable-0930/README.md) (`02d59b826`,
`qid_ticked_open.py`): in §7, the ticked box "What the field-time container `02B47760` is for" still said "Who sends
it message 14, and with which index, is not read". A residue inside a ticked box counts as closed, so it was not.

affected: `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md`. The register row MS-4 (new, in the
MS section of the register) was added in the first publish, `96ed44563`.

## What changed

- **The box keeps its answered half, ticked.** The page preloads the current sub-location's `menumap_subNN.bin` into
  the map-data cache (§2.6). A dated note points to the new box.
- **A new open box, MS-4:** who sends the field-time container `02B47760` message 14 (its opening), and with which
  index. Static plan: find the senders of message 14 to that container and the index each passes.
- **A register row MS-4, OPEN,** added under the MS section. The prefix is already this page's (MS-1..MS-3 answered).
- **The page status moves from DOCUMENTED to PARTIAL, naming MS-4.** Under FABLE's status-currency ruling
  (`status-currency-ruling-fable`, condition L), a live register id in the body keeps a page PARTIAL.

Nothing about the container's purpose or the message protocol is restated or changed, and nothing new is claimed
about the image.

## Consumers (EVIDENCE-POLICY rule 4a)

| consumer | state |
|---|---|
| the map-screens page, §7 box and status line | revised-here |
| `_index/OPEN-QUESTIONS.md` MS section | revised-here (row MS-4 added, OPEN) |
| FABLE's `qid-marker-truth-fable-0930` | agrees: it names this exact residue and asks for it to be opened and registered |
| the family-DD readers (`progress.coverage_documented`) | agrees: the page now counts as PARTIAL, which is what the open residue means |

Regression: `qid_ticked_open.py` (FABLE's, in the record above) ~~re-run after the edit no longer lists this box~~.
*Corrected 2026-09-30 (SWE2-FRONTIER):* the re-run still listed it at
`96ed44563`, because the check matches the word "Narrowed" in the box's answered label, not only residue text. The
label now reads "Answered the same day (§2.6; first recorded as a narrowing)", which FABLE's request already called
the answered half. run: re-executed after that edit, output [`qid_ticked_open-after.out`](qid_ticked_open-after.out),
with no line for the map-screens page.

Review: routed to SWE2-AUDIT-SEM.
