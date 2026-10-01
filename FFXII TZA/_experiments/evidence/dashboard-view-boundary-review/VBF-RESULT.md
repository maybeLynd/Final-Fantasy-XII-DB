# Capture-to-view failure boundary

Exact eae0ed3c7 capture CLI plus exact `v_vbf`/`M` function slice; disclosed
two-entry synthetic archive header, not shipping payload or new original-game
format evidence. Existing A17 original archive facts remain separate.

Five actual CLI cases flowed into the adapter. Valid names/sizes yielded two
files/300 uncompressed bytes; an altered listing yielded one extra name plus
one changed size, drift two/PARTIAL. Missing and corrupt archives both exited
1, replaced preseeded stale capture, and the adapter returned FAILED with no
measures. Atomic output temporary files were gone. These bounded controls pass.

**REJECT missing-comparison boundary:** valid archive plus nonexistent supplied
listing exits 0; capture omits `vs_listing`; `v_vbf` substitutes an empty dict,
calculates drift zero, displays the numeric zero and its explicit limit
“0 = the old listing still describes the archive exactly”. With empty valid
requirement facts it even returns overall OK. The archive facts are measured;
the absent comparison is not. `vbf-chain/result.json` records actual exits,
stdout/stderr, capture and returned views. Review probe exits1, never PASS.

OPUS owns repair: keep absent/malformed comparison distinguishable from a
completed zero-difference comparison through capture, adapter and presentation.
Render comparison UNMEASURED/FAILED explicitly and preserve archive inventory
where independently valid. Add an actual CLI-to-view missing-listing control,
retaining matching-listing, drift, missing/corrupt-archive positives. No old
listing fallback. Listing parse validity beyond this absence control, full
build/store/server, installed archive identity on a new build, concurrent
archive mutation and original-game resource binding remain untested here.

No peer/canonical changes, game, PC controls, saves/config/reference writes.
Fixtures and raw cases are bounded own work. No unchanged rerun: execute copied
driver from a fresh owned directory for reproduction. This original-driver
test is host engineering verification, not additional FF12 original-code or
live experiment count and not overall migration/database acceptance.
