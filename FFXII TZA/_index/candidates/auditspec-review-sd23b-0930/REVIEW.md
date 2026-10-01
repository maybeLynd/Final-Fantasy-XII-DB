# REVIEW: sd23-state7-dynamicsound-0930

- **Package:** `sd23-state7-dynamicsound-0930` (OPUS, commit `9af526c00`)
- **Task:** `OPUS-REQ-AUDITSPEC-SD23B-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of OPUS author maybeLynd)
- **Verdict: ACCEPT**

## Controls re-run

`sd23b_check.py` re-executed: `rerun_sd23b_check.out` text-identical to committed `.out`
(CRLF only), S1–S3 + D1 PASS, `FAILS 0`. Package dir clean.

## Independent verification (certified image `73461d08…21f8`)

- **S1 — state 0/1/7 skipped.** `007BF0A8 mov eax,[rcx+0x54]`; `007BF0B7 cmp eax,1; jbe
  007BF99F` (0/1 → tail); `007BF0C0 cmp eax,7; je 007BF99F` — byte-exact.
- **S2 — gate polarity read on the bytes:** after the dead-child sweep (`007BF113 call
  007B5070`, `dec [rbx+0x4C]`): `lea eax,[rcx-2]; cmp eax,2; jbe` skips states 2–4;
  `cmp [rbx+0x4C],r15d; jg` requires zero children left; `cmp ecx,6; je 007BF18D` sends
  state 6 to 7 unconditionally; otherwise `call [rax+0x138]` (slot 39) → `test al,al; je` —
  only on true does `007BF18D mov [rbx+0x54],7` run. Exactly as claimed.
- **S3 — image-wide state-7 writer census (independent):** raw resync sweep for
  `mov dword [reg+0x54], 7` over all of .text found **exactly 3 sites** — `007BD13F`,
  `007BD16D` (start step `007BD120`, completion/failure arms) and `007BF18D` (the tick).
  All three controls named by the record are the complete set.
- **D1 — RTTI walk (independent via retool's COL reader):** qword site of `007F1670` =
  `01CB9A40` = **slot 10** of the vtable at `01CB9F0`; COL→TypeDescriptor reads
  `SQEX::Sd::Lay::DynamicSound`. Slot 38 = `007C5A40` = `movss xmm0,[rcx+0xE8]` (float
  field); slot 39 = `007E5800` = `mov al,1`. Callers of `007F0820`: zero E8 sites, exactly
  one E9 tail-jump at `007F175A` inside `007F1670` — the single claimed reacher. The 5
  qword refs to `007F0820` are all vtable slots (inherited slot in subclass tables), not
  call sites.

## Limits

- "Slot 39 = finishes when its last child ends" is supported by the verified structure
  (vcall gate for non-6 states; CycleSound named as the false case by the record's own
  scope). Static only; no runtime audio-run confirmation.

**Verdict: ACCEPT** — all four controls reproduce and every anchor independently
byte-verified on the certified image.
