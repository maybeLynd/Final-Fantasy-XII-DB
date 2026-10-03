# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-spawn-placement-and-retirement-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-SPAWN-PLACEMENT-AND-RETIREMENT-10` · Package: `_index/candidates/fable-home-spawn-placement-and-retirement-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`

## SWE2-AUDIT-SPEC verdict: REJECT

All three sentences are exact, including the 432-byte `004068B0`, but all three rows are mis-homed.

- The callers `004061F0` and `00406770` are cited on this page only as the callers of `004058E0`. FABLE withdrew that function from the page on 2026-09-30 ("not a spawn function … the placement on this page … does not hold; returned to SWE2-FRONTIER's residual placement", line 3546). A stale pass-22 line at 3781 still calls it a spawn-record step.
- In the bytes, `004061F0` is the procedure of a 0x198-byte UI widget, and `00406770` is reached from the numeric-display widget walk `00406DD0`.
- The homed bodies write the counter-widget fields (`+0xE4`, `+0x114`–`+0x128`, `+0x174`–`+0x17C`, kind byte `+0xC0`). The UI pages document those fields.

So 3 of 3 rows fail host fit.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 3785, and the rows at lines 3791–3793 match `rows.json` byte for byte.
- **rows.json.** 3 rows, 15 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`004068B0` (0x1B0 B): exact, clause by clause.**
  - `cmp edx, [rcx+0x174]` / `je 00406A28`. That path stores `edi` at `+0x174` with `esi` = 0, so there is no call.
  - When `[+0x118]` is non-zero, the body zeroes it, stores `edx` at `+0xE4` and switches on byte `+0xC0`:
    - 0 → +0x72 `call 00407450`;
    - 1 → +0x68 `call 00407720`;
    - 3 → +0x5E `call 00225580` with `[+0xD0]`, and `edx - [+0xE0]` only when greater (`jle`, signed).
  - `and [+0x130], ~0x20`. Then:
    - Bit `0x40` set: 0x28 when byte `+0x136` is 0, else 8 with byte `[+0x13C + byte +0x137]` = 0xA.
    - Bit `0x80` set (`test al, al` / `jns`): 1 when byte `+0x136` is 0, else 8 with byte `[+0x13B + byte +0x137]` = 1 (`dec eax` / `cdqe`). Bit `0x20` is set in both cases.
    - Otherwise, when `edi < old +0x174` (`jge`, signed): `idiv` of 0x28 by the difference, `cmovle` 1, added to `[+0x17C]`. While the sum is below 0xFA0 (`jl` back to `mov [+0x178], cx` with `cx` = 0x28) it sets 0x28. Else it sets 1 and zeroes `+0x17C`.
    - When not below: it sets 1, and bit `0x20` follows `edi > [+0xE4]` (`jg`).
  - Finally `+0x174` = `edi`, then +0x19B `call 00225580` with `[+0xD0]` and `[+0xE4] - [+0xE0]` when greater.
- **`00407240` (0x4C B): exact.** Null `rcx` returns. Otherwise `+0x120` = `edx - [+0xE4]`; `+0x11C` and `+0x124` = `[+0xE4]`; `+0x114` and `+0x128` = 0; `+0x118` = `movsx` word `+0x108`, or 1 via `cmove`.
- **`00408140` (0x4C B): exact.** `+0x118` = 0 and `+0xE4` = `edx`. Then 0 → +0x46 `jmp 00407450`; 1 → +0x41 `jmp 00407720`; 3 → +0x3C `jmp 00225580` with `[+0xD0]` and `edx - [+0xE0]` when greater (signed); any other value → `ret`.
- **entered_from.** The raw byte scan confirms the sites. `004068B0` is called from `00406481` (= `004061F0` + 0x291) and also from `004064B1` (+0x2C1). `00407240` is called from `00406552` (= +0x362). `00408140` is called from `00406831` (= `00406770` + 0xC1).
- **Who the callers are.**
  - `004061F0` has no direct call or jump anywhere in the image. It is referenced once, by `00405412 lea rdx, [004061F0]` in `00405310`, which passes it with size 0x198 to the widget factory `00244F50` (`0040540D mov ecx, 0x198` / `00405419 call 00244F50`). So it is a widget procedure, entered through a pointer.
  - `00406770` has one caller, `00406E4B` = `00406DD0` + 0x7B. `numeric-formatting-and-character-mapping.md` homes `00406DD0` at line 2037: it walks the `[02B62D88]` widget's entries and calls `00406DD0` + 0x7B for each.
  - The callees `00407450` and `00407720` are UI bodies. `00407720` is "the elapsed-time formatter" (`the-config-screen-and-what-a-setting-change-runs.md` line 825), and `00407450` is the arm that `00407150` runs when byte `+0xC0` is clear. The config-screen row for `00407150` (line 1025) describes the same object fields: byte `+0xC0`, `+0x114`/`+0x118`/`+0x11C`/`+0x124`/`+0x128`/`+0xE4`.
- **Host fit (the defect).**
  - This page cites `004061F0` only at line 3546 and at the stale line 3781. It cites `00406770` only at line 3546.
  - Line 3546 is the struck residual-placement row of `004058E0`. It ends "Signature as first recorded (callers `004061F0`/`00406770`)", after FABLE's correction that nothing in it "addresses a spawn or keep record, a battle unit or a spawn global".
  - Nothing in the three bodies touches spawn state.
- **Advisory, separate from this package.** Line 3781 (SWE2-EC7 pass 22) still says "`004058E0` (827 B) is the spawn-record field apply `004061F0` runs … the placement-parameter stage of the retirement/respawn record update". That contradicts FABLE's 2026-09-30 correction on the same page and should be struck by its owner.
- **Advisory (tool).** The applier's caller test only asks whether the address string occurs on the page. A struck row's "callers" note satisfied it.

## SWE2-AUDIT-SPEC repair

1. Remove the section from `spawn-placement-and-retirement.md`: the heading at line 3785, its intro and the three rows.
2. Home the callers first, since neither is cited on a UI page. Put them on `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`:
   - `00406770`, entered from `00406DD0` + 0x7B (that page homes `00406DD0`);
   - `004061F0`, as the 0x198-byte widget procedure that `00405310` + 0x102 passes to `00244F50`. `00405310` is cited on `the-widget-message-protocol.md`; cite it on the numeric page too, or home the procedure there.
3. Then re-home the three rows with their callers, text unchanged. The applier will pass once each caller is cited on the new host.
4. Regenerate `homing_applier.out` and correct the README.

Limits: static evidence only. A cloud draft plus FABLE's re-read is not independent review; this record is.
