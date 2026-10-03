# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-native-command-seam-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-NATIVE-COMMAND-SEAM-1002` · Package: `_index/candidates/fable-home-native-command-seam-1002/` · Page: `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 6 functions, 27 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 6 rows, 27 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 6 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved). Every `sub edx, 1; je` / `cmp edx, 2` chain, comparison polarity and store target was checked. All six entered_from sites are direct calls inside `00355A00`: `00355BC6`, `00355A64`, `00355B59`, `00355BAC`, `00355B1B` and `00355AB6`, each confirmed. Host fit was checked against every citation of the caller on the page outside the homed section, and each body address was grepped across the database at the package's commit parent (`5bc7a655a^`).
- `0026AB60`: `shr edx, 5` of byte `+3`, then `maxss` of 0.01 (`008F30E4` = `0x3C23D70A`) with `xmm1`. 1 → `[[rcx+0xB8]+0x70]`, 3 → `+0xFC`, otherwise `ret`. Exact.
- `0026B480`: for kind 1, `and byte [rcx+0xD], 0xF7`, then `and dl, r8b` (r8b = 1), `shl dl, 3`, `or`. Exact.
- `0026BB00`: 1 → `+0x10`/`+0x14`/`+0x18`. 3 → `subss` of `+8`/`+4`/`+0` from `xmm3`/`xmm2`/`xmm1`, then `jmp 0026BA70` (`+0x26`) with `rcx` intact. Exact.
- `0026BDD0`: kind 1 → `+0x20`/`+0x24`/`+0x28`. Exact.
- `0026BFF0`: the mask `01CEBD80` reads `FFFFFFFFFFFFFF7F` ×2 (`0x7FFFFFFFFFFFFFFF` per lane), so `cvtss2sd`/`andps`/`cvtpd2ps` is a true absolute value. Kind 1: `or byte [rax+0x5D], 2`, stores `+0x30`/`+0x34`, then `comiss [+0x40], x; jbe` (stores only when the stored value is greater), and the same for `+0x44`. Kind 3: `movaps xmm2, xmm4; jmp 0026BF60` (`+0x38`). Exact.
- `003DF790`: `test ecx, ecx; je` → 3, `cmp ecx, 1; je` → 2, else 1. Exact.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **All six rows (entered from `00355A00`): host-fit defect.** `00355A00` is the script verb **`0176` `fieldsign`** (`25-EBP-Script-Container/Sections/section-003-text.md` L215 and L241; `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md` L1016 and L1087). This page never reads it. Outside the homed section it is cited three times, each as a caller of something else:
  - L559, the Party boundary paragraph: "`0026B4A0` names `00351F40`/`00355540`/`00355A00`/`00238BF0` ... the party side consults the seam's helpers, fan-in only".
  - L602, in the `0025D5E0` EC-7 entry's caller list.
  - L656, in the `0026B4A0` EC-7 entry's caller list.

  The six bodies are kind-gated field writes on the actor storage record: `(byte[rcx+3] >> 5)` selects among the `+0xB8` context sub-record fields, the `+0x0D` bit 3, and the byte `+0xF4` mapping in the caller. That record and that verb are read on the record page, not here. The section heading, *"called from this page's functions"*, is false for all six. The sentences, sites and anchors are exact.
- **`0026B480`: the row's premise is false.** At the package's parent commit, `the-record-behind-every-actor.md` already reads it (L1012-L1016): "`0026B480` is twenty-nine bytes and is **gated on kind 1** — `(byte[rcx+3] >> 5) == 1` — after which it clears bit 3 and re-sets it from the argument masked to one (`0026B48F`–`0026B499`)", with `fieldsign` (`00355A00`, `00355A5A`–`00355A64`) as its other caller. The README's "No page cited these 6 functions" does not hold for it. The homed sentence agrees with the existing one.
- **Repair:**
  - Remove all six rows from this package, and from the section already on the page (the applier prints `ALREADY`).
  - Re-home `0026AB60`, `0026BB00`, `0026BDD0`, `0026BFF0` and `003DF790` unchanged on `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md`. That page reads `fieldsign`'s other calls (`00355A71`, `00355A7E`, `00355A8B`) and the record's `+0x03` kind byte and `+0xB8` context pointer (L130, L147).
  - Drop the `0026B480` row: it is already bound there.
