# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-gambit-evaluation-and-enmity-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-GAMBIT-EVALUATION-AND-ENMITY-1003` · Package: `_index/candidates/fable-home-gambit-evaluation-and-enmity-1003/` (committed in `60f3e63b3`, reviewed at HEAD `33eb7192f`; the package is unmodified in the working tree) · Page: `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`

## SWE2-AUDIT-SPEC verdict: REJECT

The package homes nothing. Its one row (`003340C0`) was moved to `rejected` as "held" before the commit, so `rows` is empty. The commit still installed the section on the page: a heading, the italic intro and an empty table header (page line 2059 on). The README and the committed `.out` still describe one staged row. The ask ("1 frontier bodies homed") is not what the package contains.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 0 functions, 0 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing.
  - The committed `homing_applier.out` says `VERIFY 1 functions, 5 anchors` / `DRY`. It is stale: it was produced before the row was held.
  - With zero rows the applier still builds `HEAD` and appends it, so `--apply` installs an empty section. `ALREADY` here only means that heading is present.
- **rows.json.** `rows: []`; `rejected` holds `003340C0` with reason "held 2026-10-03 (FABLE): its entered_from caller 003A7AA0 is itself being re-homed to 17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md by FABLE-PUB-HOST-MOVES-1003".
- **README.** It says "1 staged with 5 anchors. Rejected by the mechanical check: 0". Both are false for the committed rows.json (0 staged; 1 held in `rejected`).
- **Page.** `gambit-evaluation-and-enmity.md` ends with `## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)`, its intro paragraph and `| function | size | entered from | what the body does | interior anchors |` / `|---|...|` with no rows. `003340C0` is not on the page.
- **Advance check of the held row (for its re-home, not credit here).** `003340C0` (0x57 B) was read in full:
  - `cmp edx, 0x1D` / `jge` is a signed guard. The dword is `[rcx + rax*4 + 0x2C]` after `movsxd rax, edx`.
  - The call sites are +0x19 (`003340D9`, `0020E600`), +0x26 (`003340E6`, `0020E600`), +0x2E (`003340EE`, `0046F370`), +0x36 (`003340F6`, `0020E600`), +0x3E (`003340FE`, `003697F0`) and +0x45 (`00334105`, `0020E620` with `xor ecx, ecx`). The `eax` of the last one is stored to `[rbx + 0x2C]`, the same dword.
  - The `je` at `003340E1` skips to the epilogue on a null resolve, and `jge` skips everything. So "when either guard fails it returns without writing" is exact.
  - `003A7AA0` + 0x26 = `003A7AC6`, a direct `call 003340C0`. Its `edx` is `movzx` of byte `[rcx + 2]`, so it is never negative in that caller.
  - The sentence is correct against the bytes. It may be re-homed unchanged with its caller.

## SWE2-AUDIT-SPEC repair

1. Remove the empty section from `gambit-evaluation-and-enmity.md`: the heading `## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)`, its intro paragraph and the empty table header. Or, when the held row is re-homed here after all, fill it then.
2. Correct the README: "0 staged. 1 held (`003340C0`, its caller `003A7AA0` moves to effect-element-type-dispatch.md under FABLE-PUB-HOST-MOVES-1003)". Regenerate `homing_applier.out`.
3. Make `homing_applier.py` refuse to append when `ROWS` is empty: print `NOTHING TO APPLY`, and do not write the heading.
4. Re-home `003340C0` with `003A7AA0` on its new host. The text above may be used as is.

Limits: static evidence only. A cloud draft plus FABLE's re-read is not independent review; this record is.
