# SWE2-AUDIT-SPEC review of SD-80 / SD-82 (sd80-82-ordered-containers-0930 at 6836e8067): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS, commit
`6836e8067`. The record is unchanged between that commit and HEAD `cb5b622f2`. Static review against the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD80-82-0930 | [sd80-82-ordered-containers-0930](../sd80-82-ordered-containers-0930/README.md) | `6836e8067` | ACCEPT |

**Re-run.** `sd80_82_trees.py`, run from its own directory at HEAD, prints `FAILS 0`. Its output
([rerun_sd80_82_trees.out](rerun_sd80_82_trees.out)) is identical to the committed `sd80_82_trees.out`, ignoring CR.
The record directory was clean before and after the run.

**Re-derived independently** ([sd80_82_indep.py](sd80_82_indep.py), output [sd80_82_indep.out](sd80_82_indep.out)).
This check uses neither `retool` nor the rc22-34 `pe` module.

- **SD-80 S1 (nine identities).** I wrote my own normaliser over `tk.fdis`. It masks rip displacements, turns local
  branches into offsets and lists the outside targets. All nine pairs are instruction-identical. The target lists match
  the record's own-instantiation claim. For example, `0071F4B0` calls `0071F3A0` / `0071F590`; `0079B0D0` calls
  `00799B80` / `00210EB0`; `0071F240` has no outside target.
- **SD-80 S3 / S6.** `00714980` becomes `0071F1E0` with exactly one insertion, `lea rcx, [rdi + 0x20]` plus a call.
  `0079BA10` becomes `0071F590` with `delete 3, replace 1, replace 1, insert 2`, and the insertion is the value
  destructor call. Both match the record's diffs.
- **SD-80 S2 (rotation direction).** My data-flow matcher, described below, run in the MSVC layout (children `+0` /
  `+0x10`), classifies `0071F240` and `00799BD0` as the rotation that takes `y = x->_Right` (`+0x10`), which is
  `_Lrotate`. It classifies `00714B00` and `00799C30` as the mirror, `_Rrotate`. That agrees with the record's
  "direction named" correction of page §3.
- **SD-82, with a second instrument that does not depend on store order.** The matcher tracks registers through the
  core of a rotation:
  1. `y = [x+c]`;
  2. `t = [y+c2]`;
  3. `[x+c] = t`;
  4. `[y+c2] = x`.

  It runs over 49,514 bodies: the 38,161 listed functions plus 11,353 `.pdata` ranges that start at no listed entry.
  This goes past the record's stated limit, "code outside that list is not swept". There is no size cap. The
  EASTL-layout run (children `+0` / `+8`) hits 10 bodies:
  - `0016D780` and `0016D7E0`, the two EASTL rotation functions, one direction each;
  - the four known both-direction bodies `0016D840`, `0016DA60`, `0067F700` and `0067F9D0`, plus two `.pdata`
    fragments interior to the last two (`0067F722`, `0067F9E9`);
  - `00712F60` and `0071E500`, single direction, both testing `_Isnil` `+0x19`. These are MSVC-layout inserts, the same
    two the record's B2 classifies as MSVC.

  No other body inlines an EASTL rotation in either direction. This confirms "no single-direction EASTL rotation
  anywhere" and "none over 20,000 bytes".
- **Sensitivity of my instrument.** The same matcher recovers every known rotation-bearing body in both layouts: the 6
  EASTL bodies and the 4 MSVC rotations plus the MSVC erase and insert bodies. So it would have flagged an inlined
  copy. A first version matched nothing in the EASTL layout because capstone prints small displacements in decimal
  (`+ 8`). The known-positive control exposed that. It is fixed, and the output above is the fixed run.

**Controls (the author's).**
- S1 checks the outside-target lists explicitly, not just the masked shape. So a body wrongly assigned to another
  instantiation would fail. That is sensitive.
- S2–S5 pin exact instruction text at named addresses. They are sensitive to a misreading of those instructions, but
  they only confirm what the prose states.
- B1 is a store-order signature. On its own it could miss a rotation compiled in a different store order, as the
  record states. My data-flow matcher closes that gap for register-carried rotations. A rotation spilled through the
  stack would still escape both.
- A cosmetic defect: the comment above S1 in `sd80_82_trees.py` says "twelve of the fourteen", but the check asserts
  nine, as the README says. No correction is needed.

**Residual limits (not narrowings).** The review is static. A rotation whose pointers pass through memory temporaries
is outside both matchers.
