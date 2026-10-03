# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-element-types-80-97-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-ELEMENT-TYPES-80-97-EE-1003-91519` · Package: `_index/candidates/opus-the-element-types-80-97-ee-1003/` · Page: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-80-97.md` (commit `51ad88762`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `ALREADY` / `FAILS 0` (exit 0).
- `rows.json`: 5 rows, 25 anchors. **All 5** rows were read against raw capstone output of the whole bodies in the certified
  image (SHA256 73461D08...).
  - **`0039B960` exact.**
    - The squared length is `ucomiss`-compared with 0.0. `jp` leads to the `sqrtf` path (`00861F14`), so a NaN takes
      the second path, and `je` gives k = 0.
    - Otherwise k = 1.0 (`01CEBBA8`) / sqrtf.
    - Three `movss` stores to `[rdx]`, `[rdx+4]`, `[rdx+8]`.
  - **`004504C0` exact.**
    - `002F2D60` returning 0 returns 0.
    - Then `00450CE0(rcx)`, and `0044B960()` with no argument set up, stored to `+0x290`.
    - `w` = word `[[rcx+0x20]+0x25C]`. If `w & 0x180 == 0x100`, `003A6E60(2) << 7` is stored, else
      `((w >> 7) & 3) << 7`, to `+0x294`. Returns 1.
  - **`00452020` exact, clause by clause:**
    - the three `00430B90(&stack, d+o, k)` reads (o = 0xC0, 0x100, 0x80);
    - the bit-0x8 add and the bit-0x4 multiply through the statics `022D92E0`/`022D92F0`. The bit-0x4 test re-reads
      `[rcx+0x20]` (`00452116`);
    - `00398480(+0x110, +0x250, byte [d+0x48])` and P += `[rcx+0x60]`;
    - the `[rcx+0x10]` arm: `0039AF70`, `00398F90(P, P)`, and `00397ED0(+0x40, +0x250)` when `byte [d+0x4A] & 0x1C`
      is 0;
    - the `+0x70` to `+0x80` shift;
    - the 0xC arm: `002F3570`, 64 bytes copied, dwords at M+0xC/+0x1C/+0x2C zeroed (`[rsp+0x7C]`/`[rsp+0x8C]`/`[rsp+0x9C]`),
      then `00397910`;
    - `003970F0` or `0039ADE0` on bit 0x2 of byte `[d+0x4B]`;
    - `+0x280` = P and `+0x28C` = 1.0;
    - `0042FDB0(d+0x180, k)` and `(d+0x1D0, k)` to `+0x240`/`+0x244`, each followed by `0026EE00` unless dword `+0x1F0`
      is 0x80808080;
    - the unsigned `>= 0x20` test and `004314E0(d+0x30, k)` != 100, then the bytes `+0x243`/`+0x247` scaled by
      q/100 through the 0x51EB851F magic (`sar 5` plus the sign bit), which truncates toward zero;
    - `+0x1F4` = `+0x240`;
    - `005002E0(d, P)`: 0 leads to `002F31C0(rcx, [rcx+8])`, otherwise `003A8950(2, rcx)`.
  - **`00452C70` and `00453810` exact, by template.**
    - `tdiff.py` normalises addresses and branch and call targets, then diffs the three bodies instruction by
      instruction. All three have 228 instructions.
      - `00452C70` differs from `00452020` in exactly 2 instructions: the `0042FDB0` operands, `d+0x1D0`/`d+0x220`
        instead of `d+0x180`/`d+0x1D0`.
      - `00453810` differs in exactly 5: the three `00430B90` offsets permuted (0x80, 0xC0, 0x100), and `d+0x1A0`/`d+0x1F0`.
    - A character diff of the three sentences against `00452020`'s finds exactly the same substitutions and nothing
      else. The full read of `00452020` therefore carries over to both.
- Limits hold: body statements only, static evidence. The draft and OPUS's re-read are not independent review; this
  record is.
