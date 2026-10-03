# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-equipment-slots-and-the-single-stat-reb-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-EQUIPMENT-SLOTS-AND-THE-SINGLE-ST` · Package: `_index/candidates/fable-home-equipment-slots-and-the-single-stat-reb-1002/` · Page: `12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 3 functions, 12 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 3 rows, 12 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 3 rows** read clause by clause against the full `disr.py` disassembly of the certified image. Every call offset, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call to the body (`0027D889`, `0027D84E`, `0034A304`). Host fit was checked against every citation of the caller on the page outside the homed section.
- `00272400`: dword `+0` (`00272406`); three `movups` cover `+0x08`..`+0x37` and a `movsd` covers `+0x38`..`+0x3F`; then dwords `+0x40` and `+0x44`. The copy loop is guarded by `cmp [r9], 0; jle` (signed, `r9 = rdx+0x40`). It copies qwords from `rdx+0x50+i*8` (through `r8 = rdx - rcx`) to `rcx+0x50+i*8`, re-reading `[r9]` each step (`0027245D`). Bytes `+4`..`+7` and `+0x48`..`+0x4F` are untouched. Exact.
- `0027C220`: the `jl 6` / `jle 0xA` / `jne 0xB` ladder is signed. Arm 6-0xA tests `byte [rcx+rax*8+0x53] & 2` and takes `+0x54`; arm 0xB tests `byte [rcx+rax*8+0x54] & 1` and takes `+0x56`; `movsxd rax, edx`. `js`/`je` on the byte means only a signed-positive byte reaches `call 0027C150` (`+0x44`). `js` on that result, then `jmp 002F9860` (`+0x53`) with `ecx = eax`. Every other path is `xor eax, eax`. Exact.
- `0035A250`: `call 0030BAD0`, `test eax, eax; sete cl`, return `ecx`. Exact.
- Host: `0034A300` is the page's own takeaway/giveback poll (L172 function table; L547-L548), so `0035A250` fits.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00272400` and `0027C220` (both entered from `0027D740`): host-fit defect.** The page cites `0027D740` in two lines outside the homed section, and both place it outside this page:
  - L562: *"Its five callers are all battle-menu bodies (`0027AD70`, `0027C3D0`, `0027CE70` ×2, `0027D740`)"*. These are the callers of the page's `00273270`.
  - L685: *"UI - CLIENT and SERVICE ... `00273270` is also called by bodies filed to UI: `0027AD70`, `0027C3D0`, `0027D740` ... shared machinery across the layer boundary, no shared ownership"*.

  The bodies are a battle-menu record copy (0x50-byte header plus counted 8-byte entries) and a battle-menu entry reader over `rbx+0x4C0`. Neither touches equipment slots or the stat rebuild. The section heading, *"called from this page's functions"*, is false for both rows. The sentences, sites and anchors are exact; only the host is wrong.
  - **Repair:** remove the `00272400` and `0027C220` rows from this package, and from the section already on the page (the applier prints `ALREADY`). Re-home both unchanged on `16-UI/Widget-Object-Model/CONTRACT-widget-object.md`. That page reads `0027D740`'s interior (L633: `0027D747`, `0027D819`) and its other record helpers: `0027BB70` at L1150-1153, the record clone `002727F0` at L1198 and the counted broadcast `002729A0` at L1202.
- The `0035A250` row is exact and stays.
