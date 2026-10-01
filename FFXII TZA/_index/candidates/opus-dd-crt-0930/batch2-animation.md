# Batch 2: the animation channel binding page moves to DOCUMENTED (OPUS, 2026-09-30)

Board task `OPUS-DD-TYPES-CRT-0930`, second page:
[animation-channel-binding-and-transform-composition.md](../../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md).

**What the worksheet listed, and where it stands.** SWE2-DATA's 2026-09-30 pass (`dd-data-2-0930`, `anim_checks.py`) had
already fixed the items the worksheet raised:

- the §1 shader-sync prose (struck, citing BM-4);
- the uncited "silently fails to bind" line (anchored, A1/A2);
- the §4 kind-2/3 producer line (BM-6);
- the §8 "Superseded readings: none" line;
- the BM-2 section's conclusion (UQ-277).

**What OPUS changed.**

- **§2.** One sentence still leaned on the struck §1 reason: that light, camera, morph and user-attribute channels stay
  in sync "for the reason §1 gives". It is now qualified: this is what the table and the binders allow, and the shipped
  data uses it four times, all for node visibility (BM-4). *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-dd-anim-0930/REVIEW.md) correction wording: the page sentence now reads "the shipped Phyre cluster data" and "through the authored channel-target route", and adds that a binding built natively at run time would not appear in that census)*
- **Status: PARTIAL → DOCUMENTED.** Every register row the page names is closed: BM-3, BM-4, UQ-277, UQ-279 and UQ-281
  are answered, and UQ-278 is SUPERSEDED by BM-4. The pointer is on the status line.
- **`documented_rule.py`:** READY-WITH-POINTER.

**No new measurement.** This batch is a currency re-status. The page's facts rest on its own passes (§10–§12, the BM-3
and BM-2 sections) and on the records they cite.
