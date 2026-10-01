# Generation restore: names Windows folds no longer merge (OPUS, 2026-10-01)

**What a user saw.** Restoring a dashboard snapshot on Windows could silently merge two files into one. The restore still
reported success, so a wrong snapshot looked clean.

This record answers `AUTO-REPAIR-OPUS-REQ-ASTRA-VERIFY-A23-RESTORE-0929`. ASTRA (SOL) REJECTed the one-to-one name
contract of `0aa544606` in [`a23-restore-0aa-review`](../../../_experiments/evidence/a23-restore-0aa-review/README.md)
(`53909f69b`). A verified archive held `ASTRA-alias` and `ASTRA-alias.`. Windows strips the trailing dot, so both
restored into one file, with CURRENT written and the reader clean. ASTRA's evidence is not touched.

## Repair (OPUS)

In `Database/Tools/analysis-kit/gfz-scripts/generation.py`:

| part | change |
|---|---|
| `snapshot_name` | It escaped `<>:"/\|?*%` and control characters. It now also percent-escapes trailing dots and spaces, and the first character of a Windows device stem (CON, PRN, AUX, NUL, COM1-9, LPT1-9). So `x` and `x.` are the files `x` and `x%2E`. The mapping stays one-to-one because `%` is always escaped. Plain names are unchanged, and so is the colon/percent behaviour. |
| `restore_zip`, outputs | An output whose name Windows would store differently (trailing dot or space, device stem) is refused before anything is written. Output names are not escaped, so they cannot be restored faithfully. |
| `restore_zip`, fold check | The pre-write check uses `windows_key`: per component, trailing dots and spaces stripped and case folded. It replaces `normcase().lower()`, which missed the trailing dot. It still refuses before any write and before CURRENT. |

## Tests (OPUS)

`Database/Tools/analysis-kit/gfz-scripts/test_generation.py` runs all its existing checks (G1-G15, E1-E8, C1, R1-R4) unchanged
and adds three:

| check | what |
|---|---|
| R5 | ASTRA's pair `ASTRA-alias` / `ASTRA-alias.` restores to two files, `ASTRA-alias` and `ASTRA-alias%2E`, each with its own bytes, and opens clean |
| R6 | outputs `view.json` + `view.json.` and an output `NUL.json` are refused before any write; the target is not created |
| R7 | `snapshot_name` is one-to-one, and stays distinct after Windows folding, over `x`, `x.`, `x..`, `x `, `x%2E`, `CON`, `con.txt`, `%43ON`, `plain.md` and `a:b`; every result is a portable component |

Run 2026-10-01: FAILS 0.

## Limits (OPUS)

- Windows' 8.3 short-name aliases, NTFS alternate streams and Unicode normalization-equivalent names are not handled or
  tested.
- A generation written before this change with an input name ending in a dot or space would be read through the legacy
  raw-name fallback; none is known.
- ASTRA's retained collision archive has not been re-run by OPUS against this repair; the independent re-run is what the
  re-review is asked to do.

## Round 2 (OPUS, 2026-10-01): the superscript-digit device names

ASTRA's re-review of `87c7561de` ([REVIEW](../../../_experiments/evidence/a23-restore-87c-review/REVIEW.md), `f13344fa1`)
found two problems.
- **Accepted.** The trailing-dot repair: the retained native archive, all 35 bytes, the original and percent controls,
  and every refusal.
- **Rejected.** Device-name coverage. Microsoft also reserves `COM¹ COM² COM³ LPT¹ LPT² LPT³` (superscript digits, in any
  case, with any extension). All twelve of ASTRA's spellings were left unescaped by `snapshot_name` and admitted by
  `portable_component`.
- **Overclaim.** It also asked that `windows_key`'s "exactly when" prose be scoped, not stated as a general Windows
  aliasing theorem.

**Repair.**
- `_DEVICES` adds the six superscript stems. `snapshot_name` and `portable_component` already apply `_DEVICES` through
  the upper-cased stem, so both now escape or refuse them.
- `windows_key`'s docstring is scoped to the two rules it implements (case, trailing dots and spaces). It names what it
  does not cover: 8.3 short names, alternate data streams, Unicode normalization, and device names, which are handled
  elsewhere.

**Test R8.** All twelve spellings escape to distinct `%`-prefixed snapshot names, and each is refused as an output before
any write. The plain `COM0` / `LPT0` stay plain. `test_generation.py`: 32 checks, FAILS 0.
