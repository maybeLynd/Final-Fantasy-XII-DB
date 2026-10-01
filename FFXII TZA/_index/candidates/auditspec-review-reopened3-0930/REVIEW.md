# SWE2-AUDIT-SPEC review - REOPENED batch 3: three falsification passes

Task: `OPUS-REQ-AUDITSPEC-REOPENED3-0930`. Package: `_index/candidates/swe2struct-reopened3-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `p1_vbf_st2e.py`: CHECKS 34 FAILS 0 (st2e header struct over 407 shipped files - the CORRECTED pass, corrections applied).
- `p2_route4.py`: CHECKS 14 FAILS 0 (Route 4 SURVIVED; live-RTTI bound preserved).
- `p3_inventory.py`: CHECKS 10 FAILS 0 (incl. `00679A50` single-caller `0067A480` and the libvorbis reach inside 008800C0..008958B0 two hops below the movie player).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
