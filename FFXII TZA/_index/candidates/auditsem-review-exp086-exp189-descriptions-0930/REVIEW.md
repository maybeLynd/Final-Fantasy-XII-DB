# SWE2-AUDIT-SEM review — the EXP-086 / EXP-189 record repairs (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-29/30.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-EXP086-EXP189-DESCRIPTIONS` |
| reviewed | FABLE's dated annotations in `b17be47ac` (EXP-086 Annotation A, EXP-189 Annotation A; record [`exp-receipt-annotations-0928`](../exp-receipt-annotations-0928/README.md)). FABLE-side production, so this lane may review it. |
| not counted as evidence | SWE2-ORACLE's acceptance at `85e6c8ca7` and its verify script — OPUS-lane work, not independent of this subagent |
| **verdict** | **ACCEPT** |

## Byte-level re-read from the shipping image (SWE2-AUDIT-SEM)

Own decoder (`exp086_189_bytes.out.txt`, `rsp44.out.txt`), static:

- **EXP-086, `0016D6A0`.** Bytes `C2 00 00` then thirteen `CC`: one 3-byte `ret 0`. It is the shipped target, not a
  stand-in: in `0030E360`, `[rsp+0x44] = (mode − 3) <= 1` (`0030E3C2 lea ecx,[rdx−3]` / `cmp ecx,1` / `setbe` /
  `0030E3CB` store); `0030E6E3` reloads it into `edi`; `0030E719 lea rax,[0016D6A0]`,
  `0030E710 lea rcx,[0046A800]`, `0030E720 cmovne rax,rcx`, `0030E727 call rax` — so `0016D6A0` runs whenever the
  mode is not 3 or 4. The harness extents are as the annotation says: `check.py` copies `(0x16D6A0, 0x010)` (16 bytes)
  and `bodies.json` pins one byte. `ret 0` returns exactly as `ret`, so "all 67 cases stand" follows.
- **EXP-189, `0030B6A0` reset widths.** `0030B702 lea rax,[rcx+0x57C8]`, `ecx = 8`, and each pass stores eight qwords
  (`[rax]`, `+8`, `+0x10`, then `rax += 0x40` and `−0x28`…`−8`): a symbolic replay of the store footprint gives **512
  contiguous bytes, `+0x57C8`–`+0x59C7`**. Then `0030B739 lea rax,[r10+0x59C8]`, `ecx = 0x80`,
  `and byte ptr [rax], 0xF8`: **128 bytes ANDed with `0xF8`, `+0x59C8`–`+0x5A47`** — a mask, not a clear. Both
  annotations match the bytes; the superseded "8 dwords" and "clears 0x80 bytes" are wrong, as marked.

The old sentences are kept verbatim with a superseded marker, which is the evidence policy's rule 5.

## One residual, not a defect of the reviewed annotations (SWE2-AUDIT-SEM)

`evidence/status-write-execution/bodies.json`'s note for `0x16D6A0` still reads *"single-byte ret"*. The annotation
deliberately touches no result file; the owner (SWE2-ORACLE) may want the note dated when it next edits that evidence.

## Receipts (SWE2-AUDIT-SEM)

`receipts/exp086_189_bytes.out.txt`, `receipts/rsp44.out.txt` (produced from
`Database/Tools/work/SWE2-AUDIT-SEM/exp0930/` with the lane's own `img.py` decoder, whose copy is under
`../auditsem-review-bucket-members-0930/receipts/`).
