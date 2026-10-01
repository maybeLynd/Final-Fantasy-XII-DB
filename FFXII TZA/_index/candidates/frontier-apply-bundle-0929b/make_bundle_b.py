"""make_bundle_b.py - build frontier-apply-bundle-0929b from HEAD (FABLE, Claude Opus 5.5, 2026-09-29).
Edits the five carrier boxes IN MEMORY from `git show HEAD:<page>` and writes a unified diff; the worktree pages are never
touched (peers may hold uncommitted hunks). Refuses unless each old box text is found exactly once."""
import difflib, os, subprocess, sys
ROOT = "C:/Users/Kristian/source/repos/XIIOnline"
DB = "Database/FFXII TZA/"
OUT = ROOT + "/" + DB + "_index/candidates/frontier-apply-bundle-0929b/"
R2 = "../_index/candidates/"          # from 02-Resource-And-Asset-Pipeline/
R1 = "../../_index/candidates/"       # from 01-Script-VM-Native-Bridge/Interpreter-Core/
S = "(FABLE, Claude Opus 5.5)"
EDITS = {
 "02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md": [(
  "- [ ] **OV-25.** Complete the indexed owner's producer/error-recovery and nonempty registration policy, and\n"
  "  identify OTHER external-owner families. SECTION-08 establishes this owner's deferred deletion,\n"
  "  tagged-reference matching and same-key reuse; those are no longer unspecified for this family.",
  "- [x] ~~**OV-25.** Complete the indexed owner's producer/error-recovery and nonempty registration policy, and\n"
  "  identify OTHER external-owner families. SECTION-08 establishes this owner's deferred deletion,\n"
  "  tagged-reference matching and same-key reuse; those are no longer unspecified for this family.~~ *ANSWERED 2026-09-29 "
  + S + ": registration of a loaded source has one door (`00409FE0` <- only the thunk `0041E580` <- four completion "
  "callbacks), so there are exactly four owner families: this indexed owner, the motion cache `02B57F70` (refcounted; its "
  "sweeps release only loaded slots), the script name-binding record, and the per-lane sub-record `02161DA0` (a lane is freed "
  "only when requested and loaded). Error recovery: the OV-42 record; nonempty registration: OV-39/40/41. Still open, kept "
  "here: the name-binding record's deletion policy and a stale-node lane requested in flight; [`ov25-queue-clients-fable/`]("
  + R2 + "ov25-queue-clients-fable/README.md). Register OV-25.*")],
 "02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md": [(
  "- [ ] **OV-39.** Producer guarantees for names, file-size metadata, offset tables and optional configuration.",
  "- [x] ~~**OV-39.** Producer guarantees for names, file-size metadata, offset tables and optional configuration.~~ *ANSWERED "
  "2026-09-29 " + S + ": names and offset tables are guaranteed by census (every `@FRP` name NUL-terminated; all 320,736 "
  "entries in bounds, OV-26); the two `@FEF`-specific inputs have no shipped producer - the configuration table `02B64380` is "
  "never populated, and `@FEF` appears only in 144 PS2-era `obj_finish` `.cm` files whose end-of-extent dword never locates "
  "their EFX data; [`ov39-fef-producers-fable/`](" + R2 + "ov39-fef-producers-fable/README.md). Register OV-39.*"), (
  "- [ ] **OV-40.** Caller policy for re-registration of fresh versus already-relocated borrowed bytes.",
  "- [x] ~~**OV-40.** Caller policy for re-registration of fresh versus already-relocated borrowed bytes.~~ *ANSWERED 2026-09-29 "
  + S + " for this path: `00409FE0` is reached only from the four owner-family completions, and each submit reads into the "
  "block its completion registers, so after a successful read only fresh bytes are rebased. Still open, kept here: what a "
  "byte-count -1 failure callback registers (no completion reads ok), and the five other `003EDAD0` drivers (OV-41's ground); "
  "[`ov40-reregistration-fable/`](" + R2 + "ov40-reregistration-fable/README.md). Register OV-40.*"), (
  "- [ ] **OV-41.** Other specialized subtypes, child construction and nonempty rendering consumers.",
  "- [x] ~~**OV-41.** Other specialized subtypes, child construction and nonempty rendering consumers.~~ *ANSWERED 2026-09-29 "
  + S + ": child construction is three registrars of one shape (`0x700` -> `003A7E80`, `0x800` -> `003A9730`, `0xA00` -> "
  "`003A9A70`, each called once from the walker `003EDAD0`), each followed by a bounded subtype setup switch; the subtypes are "
  "a closed set (4 + 9 + 65 element types, 56 element routines - the dispatch page's own census); each setup rebases or links "
  "encoded dwords at fixed offsets (`subtypes.tsv` maps 48 of 68 routines); the rendering consumers are the per-type "
  "step/update/walk/release methods and UQ-204's emits table. Still open, kept here: the 20 array-bearing setup routines' "
  "loops and what the linked `*02EBEF70` nodes are; [`ov41-efx-children-fable/`](" + R2 + "ov41-efx-children-fable/README.md). "
  "Register OV-41.*"), (
  "- [ ] **OV-42.** Held-state1 submission and outer service-error/callback-reuse recovery.",
  "- [x] ~~**OV-42.** Held-state1 submission and outer service-error/callback-reuse recovery.~~ *ANSWERED 2026-09-29 " + S +
  ": a held state1 owner is never submitted (OV-34); the owner protocol has no recovery for a rejected submission (the "
  "requester's -1 is ignored, state 3 is written, no queue entry means no callback, and a delete parks it at 5); a failed "
  "read calls back only when its byte count is -1. A higher-level arena release is not excluded, so no game leak is "
  "claimed; [`ov42-submit-recovery-fable/`](" + R2 + "ov42-submit-recovery-fable/README.md). Register OV-42.*"), (
  "- [ ] **OV-43.** Whole-session scheduling/reentrancy and actual Windows overlapping-copy behavior.",
  "- [x] ~~**OV-43.** Whole-session scheduling/reentrancy and actual Windows overlapping-copy behavior.~~ *ANSWERED 2026-09-29 "
  + S + " for the copy half: the game imports `memcpy` from `VCRUNTIME140.dll` and ships none, so it loads System32's "
  "(14.51.36247.0); over 31,784 overlapping cases that `memcpy` never differs from an overlap-safe copy. The scheduling "
  "universality half stays superseded under OV-2 (register row); [`ov46-overlap-copy-fable/`](" + R2 +
  "ov46-overlap-copy-fable/README.md). Register OV-43.*")],
 "02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md": [(
  "- [ ] **OV-45.** Establish external owner replacement/reload and all actual pin/unpin caller obligations.",
  "- [x] ~~**OV-45.** Establish external owner replacement/reload and all actual pin/unpin caller obligations.~~ *ANSWERED "
  "2026-09-29 " + S + " for replacement/reload: a manager reload runs the group deleter at unload and the group initialiser at "
  "bind; only the BGM stream head-inserts, so every older owner read completes, and frees its state-5 owner, before the new "
  "payload binds. The all-callers part is superseded under OV-2's limit (register row); [`ov45-owner-reload-fable/`]("
  + R2 + "ov45-owner-reload-fable/README.md). Register OV-45.*"), (
  "- [ ] **OV-46.** Verify overlapping-copy results against the exact deployed Windows CRT dependency, not a host approximation.",
  "- [x] ~~**OV-46.** Verify overlapping-copy results against the exact deployed Windows CRT dependency, not a host "
  "approximation.~~ *ANSWERED 2026-09-29 " + S + ": measured on the exact dependency the game loads (System32 "
  "`vcruntime140.dll` 14.51.36247.0, sha256 `d1f4225d...`; the install ships none): its `memcpy` is overlap-safe in all "
  "31,784 overlapping cases, both directions, so the overlapping move above produces the `memmove` result; another "
  "machine's redistributable is another dependency; [`ov46-overlap-copy-fable/`](" + R2 +
  "ov46-overlap-copy-fable/README.md). Register OV-46.*")],
 "01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md": [(
  "- [ ] **OV-11.** Outer-frame ordering, reentrancy, live actor allocation/reuse, and remaining native wait services.",
  "- [x] ~~**OV-11.** Outer-frame ordering, reentrancy, live actor allocation/reuse, and remaining native wait services.~~ "
  "*ANSWERED 2026-09-29 " + S + ": the native wait services are a closed set - `0025DF00`'s bounded eight-entry kind table, "
  "one predicate per service arm; actor reuse is this section's own 2026-09-26 answer; in-frame order is the field-pass page "
  "sections 4-5; reentrancy stays superseded under OV-2; [`ov11-wait-services-fable/`](" + R1 +
  "ov11-wait-services-fable/README.md). Register OV-11.*")],
}
os.makedirs(OUT, exist_ok=True)
patch = []
for page, edits in EDITS.items():
    old = subprocess.run(["git", "show", "HEAD:" + DB + page], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
    assert old, page
    new = old
    for o, n in edits:
        if new.count(o) != 1: sys.exit("REFUSE %s: box found %d times" % (page, new.count(o)))
        new = new.replace(o, n)
    p = DB + page
    patch += difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + p, "b/" + p, n=2)
open(OUT + "carrier-boxes.patch", "w", encoding="utf-8", newline="\n").write("".join(patch))
print("wrote", OUT + "carrier-boxes.patch", len(patch), "lines")
