# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-audio-bank-and-controller-family-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-AUDIO-BANK-AND-CONTROLLER-FAMILY-EE-1-CA4FE` · Package: `_index/candidates/opus-audio-bank-and-controller-family-ee-1003/` · Page: `18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 6 functions, 30 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 6 row(s), 30 anchors; rejected 0, missing 0; the README's count sentence matches.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `0021C680` exact: circular list from `rcx+8` matched on object dword `+0x3C` == `edx`; `002129F0(&out, 8)`; `jle` on the out-dword or null `r9` -> `00212A70(result)`; matched object after `00225030(obj, -1)` or vtable slot `+0x30`; null -> `00212A70`; else `00224DC0(obj, edx, r8d, r9, 5th, 6th, result)` (stack slots `[rsp+0x90]`/`[rsp+0x98]` = the 5th/6th at entry); returns the out-dword.
  - `002204A0` exact: unsigned `jbe` on dword `+0x48`; node `+0x30`, saved qword `+0x20`, `dec`, `0016D6D0(node)`, `0016DA60(node, rcx+0x28)`, vtable `+0x18` of the object at `+0x50` (node, 0x28), `00199DB0(rcx+0x58, &slot, &saved, low byte)`, `00225490(saved)` or 0.
  - `0036E9F0` exact: the record table choice (`ecx & 0xF0` zero -> `022D9AB0`, else `022D9AE0`; -1 -> a null record), `0036A0B0(dword +0x10)`, `0036C100`, `002DF450(signed byte +1 (+2 when byte +2 != 0, `cmove`), signed word +0x14, ..., 0)` stored to `+8`; zero -> `00369800`, clear `+0x10`, byte `+0` = 3; non-zero -> byte `+0` = 3 only if dword `+4` != 0.
  - `007A7010` exact: types 7 / 2 / 8 / 9 with their lock-getter and lookup pairs, imports `008C20B8`/`008C20C0`, vtable `+0x10` (type 7) or `+0xA8`; type 7 returns 0/1/3 as is and 2 otherwise; types 2/8/9 map 0->0, 1->1, 4->3 (`sete` + 2), else 2; null lookup -> 0; other types 0.
  - `007A81F0` exact: 0x82000000 for a zero handle, -1 for other types, `js` early return, command codes 0xD / 0xE with handle, `xmm1`, `xmm2` (and `r9d` at `+0x18` for 0xE), `007BAE50` / `007AB550`, cookie check `00808C40`.
  - `007C8370`: every stated store and branch holds (`+0xC8` == 1 test, qword `+0x1C8` = 0, `xmm1` = 1.0 from `01CEBBA8`, `xmm2` = incoming `xmm3`, zero byte at `[rsp+0x20]`, the fifth (double) argument to `+0xD8`, `edx` to `+0x638`, `r8d` to `+0x700`/`+0x704`, zeros to `+0xD4`/`+0x708`, `007C2280` -> `+0xC8` = 2 / return 0, else `jmp 007C36C0` with `xmm1` = 0) - except one clause, narrowed below.
- Advisory, not a defect: the README title says "cloud-drafted" while the drafting session it names is a local agent.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.

## SWE2-AUDIT-SPEC narrowing

**N1 (`007C8370`).** The row says `007CA560` is called "with the incoming `edx` and `r8`". Those registers are unchanged at the call, but `007CA560` never reads either (it overwrites `edx` at `007CA5A9` before any use, and takes its inputs from `xmm1`, `xmm2`, `r9d` and the stack byte) - the same narrowing SWE2-AUDIT-SPEC gave `007BE3F0` (`auditspec-review-opus-sound-trigger-ee-1003`). Replacement:
- old: ``calls `007CA560` on the sub-object at `rcx+0x190` with the incoming `edx` and `r8`, `r9`=0, `xmm1`=1.0 (from `01CEBBA8`), `xmm2` = the incoming `xmm3` and a zero byte argument``
- new: ``calls `007CA560` on the sub-object at `rcx+0x190` with `r9`=0, `xmm1`=1.0 (from `01CEBBA8`), `xmm2` = the incoming `xmm3` and a zero byte fifth argument (`007CA560` reads neither `rdx` nor `r8`)``
