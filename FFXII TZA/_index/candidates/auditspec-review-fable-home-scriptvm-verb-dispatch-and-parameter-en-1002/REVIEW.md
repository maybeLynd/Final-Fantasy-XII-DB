# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-scriptvm-verb-dispatch-and-parameter-en-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-SCRIPTVM-VERB-DISPATCH-AND-PARAME` · Package: `_index/candidates/fable-home-scriptvm-verb-dispatch-and-parameter-en-1002/` · Page: `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 2 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 2 anchors; mechanically rejected 0, skipped 0, missing 8 (README).
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image. The entered_from site was disassembled and confirmed as a direct call to the body. Host fit was checked against every citation of the caller on the page outside the homed section, and the body's address was grepped across the database at the package's commit parent (`5bc7a655a^`).
- `00379D40` (18 B): `sub rsp, 0x28` / `call 00379D60` (`00379D44`) / `add rsp, 0x28` / `jmp 0036FD60` (`00379D4D`). The sentence is exact. `0022A0B0` + 0x2F8 = `0022A3A8 call 0x379d40`, confirmed.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00379D40` (entered from `0022A0B0`): the row's premise is false, and its host is wrong.**
  - *Already cited.* The README says "No page cited these 1 functions". At the package's parent commit, `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` already has the section **"The `00379D40` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)"** (added in `04dc361cf`, 2026-09-17). That section reads the same two steps, `call 00379D60` (`00379D44`) and the tail `jmp 0036FD60` (`00379D4D`), and binds both callees. `_index/ADDRESS-INDEX.md` maps `00379D40` to that page. The homed row repeats an existing binding.
  - *Host fit.* This page cites `0022A0B0` in six lines outside the homed section, and none of them treats it as one of the page's functions. L1329 names it as "the boot fixer" in the `CZ-1` answer about who sets byte `02ADD932` (through the page-cited `0037B390`). L1364 and L1370 are cross-layer SERVICE paragraphs (Input and Presentation; RNG). L1386, L1389 and L1392 are generated neighbour edges, and L1386 lists `0022A0B0` among the **CoreRuntimeScheduling bodies**. The body's work (the `02ADD170` 16 x 0x70 list init in `00379D60`, and the `02AD9E00` flag clear in `0036FD60`) is resource-queue state, which this page does not discuss. The section heading, *"called from this page's functions"*, is false for this row.
  - **Repair:** remove the `00379D40` row from this package, and from the section already on the page (the applier prints `ALREADY`). Do not re-home it: `the-resource-request-queue.md` already binds it, and its statement agrees with the row. If the package ends up with no rows, withdraw the section.
