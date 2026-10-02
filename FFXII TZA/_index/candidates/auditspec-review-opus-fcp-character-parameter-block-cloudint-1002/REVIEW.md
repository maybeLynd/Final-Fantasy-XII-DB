# Audit-spec review: OPUS cloudint interior citations (opus-fcp-character-parameter-block-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-FCP-CHARACTER-PARAMETER-BLOCK-CLOUDINT-1002` · Package: `_index/candidates/opus-fcp-character-parameter-block-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 22 rows applied, 98 anchors, rejected/skipped/missing 0.
- Semantic pass: all 22 rows exact vs the certified image, incl. 00265240 (type-mask 0x60 copy triple from qword+0xB8), 00265270 (02098E20 bit-0 gate + word 02098E58), 00265290 (jmp 002E9A30), 002652A0 (nested +0xF0/+0x38 float for mask 0x60), 002652D0 (r8d<=0x11 selector, 0xE case, rdx+0xC8 table, -1 fallback), 00265380/00265390, 0026B2D0/0026B2E0 (float calc + 003DA860 + maxss 0.1875 clamp + conditional 003DA890), the 002E7DD0/2E7E10/2E7E50 helpers (incl. exact 0x9000808/0x9000202 select), 002E7F10, 002E9630 (0x9001D1E), 002E9660 (0x1002D4F/0x1002143 via 00377C20), 002E9780 (bit 6 of nested byte+0x11), 00342640 (word+0xA switch cases 1/3 + 002EAC90 + tail 0025B470), 0034EFE0/0034F4F0 (0026A1A0 rdx,0/1 chain + tail 002690D0), 0034F570, 0034F590 (jmp 0025A840), 0034F5A0 (three 002650B0 values, -1-padded stack array, 0026B4E0), 003E4700 (1.0 fallbacks), 0051CDE0 (dual-packet builder: copies, byte-assembled qword, +0x3C/+0x5C/+0x20/+0x24 multiplies, conditional 00861F5C, both submits, 0x1D0 stride) and 0051D1D0, 0051DB60..0051DC90 (0x1D0-stride record init incl. word 1 at +6, 1.0 at +0x14, 00861EC0(+0xA0,0,0x100)).
- Limits hold: body statements only.
