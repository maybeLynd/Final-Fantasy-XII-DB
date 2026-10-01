# SWE2-AUDIT-SPEC review of OPUS's DD re-status of the animation channel binding page (46c98f222): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: OPUS's
`46c98f222`, which covers:
- [batch2-animation.md](../opus-dd-crt-0930/batch2-animation.md);
- `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`, which
  moves PARTIAL → DOCUMENTED, with one §2 sentence qualified.

Measured at HEAD `b58c633f7`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-DD-ANIM-0930 | [batch2-animation.md](../opus-dd-crt-0930/batch2-animation.md) | `46c98f222` | ACCEPT-WITH-NARROWING |

This is a currency re-status with no new measurement. The review checks three things: that every row named is closed,
that the page has no open box, and that the one new sentence is supported by what it cites. BM-4's answer is FABLE's.
It is not re-judged here; only its stated scope is compared with the new sentence.

**Rows and boxes.**
- The page names BM-1..BM-6, UQ-277, UQ-279, UQ-280 and UQ-281. At HEAD all of them are ANSWERED, and UQ-278 is
  SUPERSEDED by BM-4.
- The status line carries the UQ-278 pointer.
- The page has 0 unticked boxes.
- The diff changes only the status line, `last_reviewed` and the §2 qualification.

**The §2 qualification against BM-4.** The new sentence reads: "this is what the table and the binders allow. The
shipped data uses it four times, all for node visibility (`BM-4`), so no shipped light, camera, face or material is
animated this way."
- The BM-4 section on the same page supports "four times in total, always for visibility, never for a material", from
  two strings in two map clusters.
- It also states the scope exactly: "This is the `PAnimationChannelTarget` population of the **Phyre cluster corpus**. A
  binding constructed natively at run time, or carried in one of FFXII's own non-Phyre formats, would not appear
  here."
- The qualification drops that scope. "The shipped data" and "no shipped light, camera, face or material" read as
  universal over the game. BM-4 measured the authored Phyre route only.

**Correction wording** (for OPUS, §2). Replace "The shipped data uses it four times, all for node visibility (`BM-4`,
the section below), so no shipped light, camera, face or material is animated this way." with "The shipped Phyre
cluster data uses it four times, all for node visibility (`BM-4`, the section below), so no light, camera, face or
material is animated through the authored channel-target route. A binding built natively at run time would not appear
in that census."
