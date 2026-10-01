# SWE2-AUDIT-SPEC review of SD-169, the draw-surface cells +0x9C / +0xA0 (OPUS, 569685cbb): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `569685cbb`, [README](../sd169-draw-surface-cells-0930/README.md) and `sd169_cells.py`. Measured at HEAD
`b58c633f7`. Package re-runs repeated at `701f1f01a`, identical. Static analysis of the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD169-0930 | sd169-draw-surface-cells-0930 | `569685cbb` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_sd169_cells.out](rerun_sd169_cells.out) is identical to the committed `.out` (CR ignored). G1-G3
PASS, `FAILS 0`. The package dir was clean after the re-run.

**Re-derived independently.** Both scripts use [sdx.py](../auditspec-review-sd141-0930/sdx.py), not retool.py:
[sd169_indep.py](sd169_indep.py) / [.out](sd169_indep.out) and [sd169_qword.py](sd169_qword.py) / [.out](sd169_qword.out).
- **G1 holds.** `0036D280` stores:
  - `+0x9C` = `0x200` (`0036D286`);
  - `022D8EA8` = 0 (`0036D290`, `eax` = 0);
  - `+0xA0` = `0x200` (`0036D2A3`);
  - `022D8EB4` = `0x1C0` (`0036D2AD`).
- **G2 holds, packed field by field** (from `00244224`..`002443A4`).
  - **BITBLTBUF (register `0x50`).** Let `s = [+0x9C] >> 6` (`00244241`). Then
    `(((s << 32) | s | 0x333C0000) << 16) | SBP`, with `SBP = ([022D8EA8] × [022D8EB4] × [+0x9C]) >> 6`
    (`0024425A`). That puts SBP in bits 0-13, SBW = `s` at bit 16, DBP = `0x333C` at bit 32 and DBW = `s` at bit 48,
    with both PSM fields 0.
  - **The GIF tag.** `0x1000000000008007` is NLOOP 7, EOP 1, NREG 1. The register descriptor `0xE` (A+D) is at
    `002442B9`.
  - **The other registers.** `0x51` TRXPOS is `ebx << 16`. `0x52` TRXREG is `[+0x9C] | 0x10 << 32`, i.e. width
    `+0x9C` and height 16. `0x53` TRXDIR = 2. The second TRXPOS / TRXREG pair is `00244343`..`00244378`.
  - **The `0039D0C0` call** (`0024427B`) gets `ecx = 0`, `edx = 0x333C`, `r8d = 0x200`, `r9d = 0x1C0`.
- **G3's conclusion holds, but "one reader" is not exact.** An all-form census of `022D8E70`..`022D8EB3` found five
  operands covering `022D8EB0`:
  - `0036D2A3`, the boot store;
  - `0036D342`, the word read into `r8` for the stub;
  - three QWORD loads of `+0x9C` that also load `+0xA0` in their high half: `00244224` (`rcx`, in `00244200`
    itself), `002443E7` (`r10`, in `002443D0`) and `004FDDC7` (`rsi`, in `004FDDA0`). The package's exact-address
    census does not show them.

  In each of the three, the loaded register is next used only 32-bit: `mov edx, ecx` / `imul eax, ecx`,
  `lea eax, [r10 + r10]` / `sar r10d, 6`, `sub edi, esi` / `lea eax, [rsi - 1]`. It is then overwritten or popped.
  A 32-bit `lea` result does not depend on the source's high half, so no instruction uses `+0xA0` from these loads.
- **The stub.** `0016D6A0` is `c2 00 00` (`ret 0`), with 2,868 raw E8/E9 + jcc callers. In `0036D2F0` nothing reads
  `r8` after the `0036D34E` call before the next call. No lea'd base in `022D8D10`..`022D8EB3` (10 sites) is handed to a callee or
  reaches `022D8EB0`. `0036D3A2` / `0036D7F5` store `022D8E50` (+0x40) into `022D8EA0` (+0x90), but the only operands
  on `022D8EA0` are those two stores, so nothing loads that pointer. No relocation points into the range.

**Controls.**

| instrument | control | result |
|---|---|---|
| exact rip census | K1: `+0x9C`'s readers `00244224` / `0036D31B` | found |
| image-base-relative | K2: SD-121's `0036E414` | found |
| wide coverage | the three qword loads | K1 lists them; V1 flags them COVERS |

The package's G3 compares an exact-address reference list, so it is blind to a wider load that starts at `+0x9C`.

**Citations checked.** G1 and G2's instruction texts decode as stated, including `00244362` and `00244378`. The GS
register numbering is the page's PS2 map, and the packing agrees with it.

**Correction wording** (the producer applies). In G3, replace "It has one writer (the boot `0036D280`) and one
reader, `0036D2F0`." with:

> It has one writer (the boot `0036D280`). Its one use is `0036D2F0`'s word read (`0036D342`), which passes it only to
> the bare `ret` `0016D6A0`. Three qword loads of `+0x9C` also load it as their high half: `00244224` (in
> `00244200`), `002443E7` (in `002443D0`) and `004FDDC7` (in `004FDDA0`). None of them uses that half.

The rest is unchanged.
