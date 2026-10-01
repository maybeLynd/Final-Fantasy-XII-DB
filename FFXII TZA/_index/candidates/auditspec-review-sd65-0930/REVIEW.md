# SWE2-AUDIT-SPEC review of SD-65 (sd65-dynamic-class-route-0930 at 49f9a523b): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `49f9a523b`. Record: [sd65-dynamic-class-route-0930](../sd65-dynamic-class-route-0930/README.md). Image reads
plus the shipped-archive census (tier 9).

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD65-0930 | sd65-dynamic-class-route-0930 | 49f9a523b | ACCEPT |

**Re-run.** All three scripts were run from their own directory, and each output is identical to the committed `.out`
ignoring CR:
- `sd65_loader.py`: L1-L4 PASS, `FAILS 0`.
- `sd65_census.py`: 201 s; 35,984 files, 684,244 class records, 0 with w7 bit 0, controls PASS.
- `sd65_members.py`: 215 s; 527 of 527 pairs registered, `FAILS 0`.

`sd65_census.json` is tracked and the census rewrites it; `git status` stayed clean after the run. Outputs:
[rerun_sd65_loader.out](rerun_sd65_loader.out), [rerun_sd65_census.out](rerun_sd65_census.out),
[rerun_sd65_members.out](rerun_sd65_members.out).

**The two things the request asked me to test.**

1. **Do the S / T name-in-function forms over-match?** ([sd65_overmatch.py](sd65_overmatch.py) /
   [sd65_overmatch.out](sd65_overmatch.out)). I ran the author's join unchanged (exec'd up to its control section)
   with two new controls.
   - **N1, a negative control that the defect would trip.** For every class that declares members, I tested every
     member name that class never declares but some other class does: 53,219 wrong pairs. None resolves by any form
     (D, S or T). An over-matching S or T form would resolve wrong pairs here, so the join is shown to reject them.
   - **N2, ambiguity of the true S / T hits.** The 527 true pairs resolve first by D (388), T (102) and S (37).
     - Every S function references **0** other census class names besides its own. These are `00613800`,
       `00613A30`, `00613E80`, `006143B0`, `00614640`, `006B08A0`, `006B09E0`, `006B1600` and `006B33F0`.
     - Every T registrar is shared with **0** other instantiations. `PArray<PUInt8>` alone has two registrars,
       `00618970` and `00668AE0`.

     So the limit the record states ("a registrar registering the same member name for two classes would satisfy S or
     T for both") does not occur in this build.
   - The class side of N1 does not reach one case: two `PArray<>` instantiations share the member names `m_count` /
     `m_els`. N2 covers it, because no registrar serves two instantiations.
2. **"entry +8 = the file class record".** ([sd65_rederive.py](sd65_rederive.py) / [sd65_rederive.out](sd65_rederive.out)).
   The record read this from offset matches only. I found the entry builder: `0059B430`, called from `0059E070`,
   the only caller of `0059AC00`, before the loader runs.
   - It sets `rsi` = namespace + (8 + type count) × 4 = the first 36-byte class record, and steps `rsi` by 0x24.
   - For each 0x30-byte entry it stores `[entry+8]` = `rsi` (`0059B7CF`); `[entry+0]` = `&entries[w0 − 1]`, from the
     record's first dword (`0059B7B9`-`0059B7D7`); `[entry+0x10]` = the native descriptor looked up by `0059BE00`;
     and `[entry+0x18]` = the name.

   So `+8` is the file class record. HOLDS by the builder, not only by offsets. This also closes the record's limit
   "the entry builder itself is not read" for the class entry. The 0x38-byte member entry's builder was not traced.

**Other claims re-derived.**
- **L1 by a raw sweep.** It is independent of the function list: E8/E9/0F8x branches plus rip address-taken forms plus
  DIR64 pointers.
  - `00632B30` has 1 branch (`0063942C` in `006393A0`).
  - `006393A0` has 1 (`0059AEA7` in `0059AC00`).
  - `0059AC00` has 1 (`0059E227` in `0059E070`).
  - All three have 0 decoded address-taken forms and 0 relocations. HOLDS.
- **w7 bit 0 in the shipped data** ([sd65_w7_extract.py](sd65_w7_extract.py) / [sd65_w7_extract.out](sd65_w7_extract.out)).
  This is a second reader over a second copy, the loose `D:/FFXII_TZA_extract`, not the VBF. It finds 35,984 `.phyre` files, all under `gamedata`, with 0 unparsed.
  They hold 684,244 class records, and **0 have bit 0 set**. The w7 values are {0: 523,918, 2: 38,322, 8: 66,379,
  12: 2,184, **20: 5**, 32: 49,068, 34: 2,184, 40: 2,184}, identical to the author's census. HOLDS, including the value
  20 that the namespace page omits.

**Controls.** The census's own two controls (file count, bit-0 count) are tallies, not sensitivity tests; the w7
re-count above is the independent check. The members script's two positive controls (`PClusterHeaderBase::m_size`,
`PLight::m_color`) show the join can find a pair. It could not show that the join rejects a wrong one; N1 does that.

**Verdict.** ACCEPT. Part 1 (no shipped class takes the dynamic route; w7 bit 0 is never set) and Part 2 (all 527
file-declared pairs are statically registered) hold. The S/T over-match limit can be restated as tested: "53,219
wrong (class, member) pairs resolve by no form; no S function or T registrar serves a second class". The w7 value 20
(5 records) belongs on the namespace page's list, as the record says.
