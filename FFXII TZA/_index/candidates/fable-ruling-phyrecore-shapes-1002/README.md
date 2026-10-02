# FABLE ruling: PhyreCore's identity predicate, and no 3-body micro-families (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `SWE2-EC7-REQ-FABLE-SHAPES-PHYRECORE-0930`. The evidence is EC7's:
[`ec7-phyre-uniform-0930`](../ec7-phyre-uniform-0930/README.md) section 2 and
[`ec7-shape-proposals-0930`](../ec7-shape-proposals-0930/README.md) section 2. This ruling adds no measurement.*

## 1. PhyreCore

EC7's sample shows the uniform closure rule cannot be applied to PhyreCore as it stands. Without the A-measured and
declared exclusions, the closure runs from core into game code: +988 bodies, 148 of them carrying an FFXII census tag.
The exclusions were acting as a firewall, but that firewall was accounting state, and module identity never depends on
accounting state (FABLE's closure-cascade ruling, 2026-09-30). **So PhyreCore needs an identity predicate of its own.**
Until a selector implementing it passes the guards below, EC7's current state stands: the old exclusion, 426 members,
and the row says why.

**The predicate.** A body joins PhyreCore by closure only if all three of these hold:
1. **Geography.** It lies inside a contiguous run of the image whose bounding bodies, on both sides, are already
   PhyreCore members by the seed (RTTI or class descriptor). A body in a gap that also holds game-tagged bodies is
   outside.
2. **Identity link.** It has at least one of: a Phyre RTTI or class-descriptor slot; a Phyre census tag; or callers that
   are all PhyreCore members or Phyre class descriptors (exclusive reach).
3. **No game tag.** No census tag names an FFXII domain. Such a body is neither admitted nor walked through: the
   closure stops at it. That replaces the old firewall with an identity fact.

A body measured A or declared in another family is left out of the output and printed, as the other selectors already
do. It is not used as a traversal stop, because traversal stops are what condition 3 provides.

**Guards the selector must pass before its row changes:**
- **Positive.** All 426 current members are re-admitted by the predicate alone.
- **Negative.** EC7's sampled game bodies stay out: the movement body tagged `FFXII.MovementNavigationSteering`, the
  body called from battle-menu code, and the three large Presentation bodies named in EC7's section 2.
- **Population.** Zero FFXII-tagged bodies in the admitted set. A seeded sample read of at least 25 admitted bodies
  shows no game code.

If a module has no usable contiguous run, condition 1 cannot be met, and its members stay seed-only. That is a
smaller family, not a wider rule.

## 2. The two 3-body skeletons

**No micro-families.** A form family needs many bodies sharing a skeleton, with a shared-target control. Three bodies
per skeleton is a coincidence of size, and admitting them would be a shape-based bulk disposition. Route both triples as
EC7 ranks them:
- first, individual explanation (A) on the page of the caller or target that gives them their meaning;
- second, caller-side closure into the owning family, by that family's own predicate.

If the three bodies of a triple share one target and their callers are one object, one interior citation on that
object's page explains all three, and that is the cheapest route.
