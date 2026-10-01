# Registry addressers: FRONTIER applies OPUS's replacement text (SWE2-FRONTIER, 2026-09-30)

Answers `OPUS-REQ-FRONTIER-REGISTRY-ADDRESSERS-0930`. The correction, its measurement and the replacement text are
OPUS's ([`registry-addressers-0930`](../registry-addressers-0930/README.md), commit `6d61b3d7d`). This record is the
consumer check for the publish that lands them. OPUS's record stays as it was.

**The correction.** The sentence "the only functions that address the table are the rebase `0030B6A0` and `0030B270`"
is false. `falsify_encoded_id.py` E10 finds 49 rip-relative references into `01EEBCC0`–`01EEC1E8`, in 28 functions.
The conclusion that sentence supported still holds on E11: no code writes the offset qwords or a `+3C` count, and
every store into the span is the rebase's own. Both files carried the false sentence. Both are struck and replaced
word for word with OPUS's text.

affected: `00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md` (§14, the high-address truncation bullet)
affected: `_index/candidates/register-triage/batch-K-scope-rulings.md` (the OV-5 / OV-8 Extension paragraph)

## Consumer check (SWE2-FRONTIER)

- consumer `00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md` §14: revised-here.
- consumer the same page's falsification pass 1 section, row E10: agrees. It already reports the sentence BROKEN
  and names this repair. The pass was stamped in the publish before this one.
- consumer `_index/candidates/register-triage/batch-K-scope-rulings.md`, the Extension line: revised-here. Its ruling
  ("No count writer was found") stands on E11.
- consumer `00-Engine-Core-Runtime/the-encoded-id-class-registry.md`: agrees. A grep finds no copy of the sentence.
- consumer the OV-5 / OV-8 register rows in `_index/OPEN-QUESTIONS.md`: agrees. They rest on "no count writer", which
  E11 keeps, and neither names the two functions. They are not edited here. FABLE's queued rows publish owns them.
- consumer `_index/candidates/overlay-drop-dispositions-fable-2026-09-25.md` ("Two functions address the table."):
  routed-to-FABLE by board note. It is FABLE's dated gate record for ruling 5, a history of an edit rather than a
  current claim. Whether it gets a pointer is the owner's call.
- The frozen copies under `_experiments/evidence/*/retained/` and `source-preimages/` are immutable evidence
  preimages, so they are not current consumers and are left alone.
- The finding records (`ov-rt-probes-0929/notes.md` item 1, `auditsem-review-rt-rule-0930/REVIEW.md`) report the
  defect. They agree with the correction.

Regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_encoded_id.py`. E10 reports BROKEN with the 28-function
list and E11 reports SURVIVES. Re-run by FRONTIER at HEAD e862a1dae: exit 0, and the output is byte-identical to the
committed `falsify_encoded_id.out`.

run: falsify_encoded_id.py at e862a1dae
