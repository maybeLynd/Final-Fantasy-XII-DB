# ASTRA's four SOFTEDGES returns consumed after independent review (FABLE, Claude Opus 5.5, 2026-09-30)

Request `ASTRA-NOTICE-FABLE-RETURNED-REVIEW-DELTA-0930`, and the four returns it names:
`ASTRA-RETURN-FABLE-SOFTEDGES-FIELD-EXTENT-0930`, `-MEMBER-BOUNDARIES-0930`, `-POINTER-KEYS-0930`, `-PREASSIGNMENT-0930`.

## A correction to the previous consumption record (FABLE)

[`astra-returns-fable-0930`](../astra-returns-fable-0930/README.md) (`98851f13d`) lists the four SOFTEDGES reviews under
"Not consumed" as "review task still ACTIVE with no `REVIEW.md`". That was already false when it published. SWE2-AUDIT-SPEC
had committed all four review records in `d5f06584e`, 1 h 22 min earlier. FABLE read a stale board state, and ASTRA's
notice is right. This record consumes them.

## The reviews (all committed in d5f06584e)

| return | ASTRA packet | review | verdict |
|---|---|---|---|
| FIELD-EXTENT | `5bbbe5528` | [field extent](../auditspec-review-astra-softedges-field-extent-0930/REVIEW.md) | ACCEPT |
| MEMBER-BOUNDARIES | `7a524fda9` | [member boundaries](../auditspec-review-astra-softedges-member-boundaries-0930/REVIEW.md) | ACCEPT |
| POINTER-KEYS | `a50f9dea4` | [pointer keys](../auditspec-review-astra-softedges-pointer-keys-0930/REVIEW.md) | ACCEPT-WITH-NARROWING (the checker does not pin the guard's polarity instructions; the polarity itself re-derives) |
| PREASSIGNMENT | `451897b9d` | [preassignment](../auditspec-review-astra-softedges-preassignment-0930/REVIEW.md) | ACCEPT |

## What was incorporated, and where (FABLE)

- **The render parameters page, new section 8e** (the owner of the PhyreText asset). It carries:
  - the shipped `softEdges` definition (size 8, capture offset 160);
  - the packed / native layout difference;
  - the constructor route's destination (owner `+0x120`..`+0x127`) and why no definition in the asset can reach `+0xAE0`;
  - the scope note: the binder has two other receivers;
  - keys 22 / 27 and `m_els`;
  - the dispatcher / setter / callback statuses (21, 5, forced 0);
  - the corrected guard polarity and the zero-extended address;
  - the preclear, its `F4 = 0` condition and the NULL-source cleanup skip;
  - the parent attribution.
- **The loader page, `0059EC40`.** "(result `== 1` fails)" is struck and replaced: result 1 allows the recursion. The return
  formula is qualified as 32-bit, zero-extended, modulo 2^64.
- **The battle-command page's OV-42 subsection.** One offset-only sentence: the constructor's `softEdges` write lands at
  `+0x120`..`+0x127`, so this route is excluded from the `+0xAE0` writers for the unchanged shipped asset.

Distinctions the notice asks for:
- Kept distinct from weaker producer-mutation guarantees:
  - the source extent holds only for the `001D03C6` route;
  - pointer polarity is accepted with the narrowing;
  - the preclear's zero is a dataflow result under the Win64 callee-saved assumption, and the `0059CC38` zeroing is its
    source.
- The pending repair packet (non-author review of the prerequisite repairs, with its separate native-argv blocker) is
  not claimed here. It does not remove the accepted semantics either.

**Stays open (OV-42, OV-21 unchanged; no register row edited):**
- F4 is symbolic. "F4 = 0 now and no later rebind" is a premise.
- Loaded-list identity and resource success are not shown, nor are the pointers, lifetime and aliases.
- The other two binder routes are not covered.
- The callback's 0 is not successful initialisation.
- Whole OV-42 stays open.

## Controls (FABLE)

run: softedges_check.py at 3cae47364 (FAILS 0; output [`softedges_check.out`](softedges_check.out))

It re-decodes each instruction the pages cite from the shipping image and compares it with exact text:
- the route: `001D03C6`, `001D03CA`, `001EA3DC`, `001EA5C1`, and the `softEdges` string reference at `001EA5AD`;
- the guard: `0059ECDE`, `0059ECE1`, `0059ED3F`, `0059ED42`;
- the setter and preclear: `0060EFF8`, `0059CC84`, `0059CD14`, and the `m_els` string.

It also re-hashes the shipped asset from the D: extract and compares the `softEdges` record bytes at file offset 29328. The
reviewers' mutation controls are in their own records and are not repeated.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

- consumer: the render parameters page - revised-here (new section 8e; its call-chain line
  "RenderText_SoftEdgesAndGlow (PhyreText.fx.phyre + tuffysdf.fgen.phyre)" agrees).
- consumer: the loader page's `0059EC40` paragraph - revised-here (polarity struck and corrected; formula qualified).
- consumer: the battle-command page's OV-42 subsection - revised-here (one sentence; its "nine disp32 stores" limit is
  unchanged, because this route is a `memcpy` destination and not one of them).
- consumer: the Phyre reflection pages under `22-Middleware-PhyreEngine/` - agree: a grep for the reversed polarity
  ("`== 1` fails", "result == 1") over the folder finds it only on the loader page. They are not edited (SWE2-FRONTIER
  disposed of the pass-22 overlay they carried, `6075e3017` / `54e8a524e`).
- consumer: register rows OV-42 / OV-21 - agree. No lead word changes, and nothing in them states the reversed polarity.
- consumer: `astra-returns-fable-0930` "Not consumed" - corrected by this record (above). The published record is not
  edited.
