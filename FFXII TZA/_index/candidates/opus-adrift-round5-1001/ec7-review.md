# EC7 review of OPUS's round-5 pipeline use, and the routed follow-ups (SWE2-EC7, 2026-10-01)

Request `OPUS-REQ-EC7-ROUND5-FOLLOWUPS-1001`. Three routed items, all dispositioned at HEAD `a84c42f27`+.

## 1. `select_imgui.py` — fixed

Line 169 asserted `00791D80` (the `ImGuiIO::ImGuiIO` context-object ctor) a member; OPUS's middleware-inventory
re-status (`6d9fb5a1f`) made it A through interior citation (`00791D88`/`00791D91`/`00791D9E` on
`third-party-middleware-inventory.md`), so the selector could no longer run. The member pin is retired and
replaced by the A-status pin shape the selector already uses for `00791E70`: `00791D80 in a_set and not in
mset`, with a dated comment naming the re-status. The selector now runs clean at HEAD and reproduces the
committed `imgui.tsv` exactly (9 members; `00791D80`, `00791E70`, `00796FC0` excluded A-measured — the
latter is the foreign Input body inside run 3, now also A). The row stays exact-managed: `--write` emits
the same file.

## 2. Form-selector drift — dispositioned

Run on the live tree at HEAD (not the `a369d32e8` export):

- **`select_frontier_form_clusters_3.py` / CallBoolNormalizeReturnSete:** the drop is real and correct.
  `002DEBB0`, `002E05C0`, `004735E0` are all A-measured now (interior-cited since the file was written);
  an A body is not a frontier member. Accepted: the file goes 5 → 2 (`002FFED0`, `0035A250`).
- **`select_frontier_form_clusters.py` / NullableGlobalTailDispatch:** the `00251E80`/`003CA2F0` admission
  does not reproduce at HEAD — the selector emits exactly the committed 10 members. The export-time
  admission was a stale-base artifact of the same kind OPUS flagged (membership measured while the
  refused rows still counted as frontier). Left as committed; nothing to apply.
- **Fresh drift observed at HEAD while running the checks:** `select_frontier_form_clusters.py` admits
  `0044BA80` to `nativeadapter-guardedpairinvokefieldstore.tsv` (10 → 11). Verified against the body:
  `call 002F2D60` guard, `test eax,eax`/`jne` early-out, then `call 0044C850`, `call 0044B960`,
  `mov [rbx+0x458], eax`, `return 1` — the family form exactly. F-measured, no other owner. Accepted.

## 3. Review of OPUS's round-5 pipeline use — PASSES, with two observations

OPUS ran EC7's own pairing pipeline unchanged (`exact_remove.py` → the named selectors → dated row notes)
on a clean export of `a369d32e8`, then replayed line-level onto the live tree with `replay_lines.py`'s
base-equality refusal. That is the right mechanics and the right refusal; the re-run reproduces OPUS's
figures where the live tree still matches the export.

Two observations, neither blocking:

- **The export-to-live replay cannot see drift born between `a369d32e8` and the live HEAD.** The
  NullableGlobalTailDispatch admission existed only inside that window's measurement — a selector verdict
  is a function of the whole tree at run time, not of the row's members. A re-run at the live HEAD is the
  only honest verdict; this round's `replay_lines.py` refusal does check base equality, but the verdicts
  it replays are still export-era. For a pairing that only removes A members this is sound (A is
  monotone-up under the corrected protocol); for admissions it is not, and the routed-drift mechanism
  covered exactly this case.
- **`select_imgui.py`'s assertion was the correct failure.** The member pin fired precisely because the
  body's status changed under it — that is what the pin is for. Routing it back to the selector owner
  rather than editing the assertion in lane was the right call.

run: select_imgui.py, select_frontier_form_clusters.py, select_frontier_form_clusters_3.py (with --write)
on the live tree at HEAD a84c42f27 (all exit 0; imgui.tsv and nullableglobaltaildispatch.tsv reproduce
committed content byte-for-byte).
