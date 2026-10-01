# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-LIFETIME-PASSES-0929 · SWE2-AUDIT-SEM 2026-09-29

Passes: `50f1e9e67` (external-source owner, E0–E6), `9161b92ea` (resource owner, O0–O4).
Regressions re-run non-author: `falsify_external_owner.py` + `falsify_resource_owner.py` — FAILS 0 each.
Certified image `73461D08…21F8`.

## Attack E4 — is every owner below 4 GiB? (the mov edi,ecx question)

Byte-verified: `003DD85A mov edi,ecx` → `mov ecx,[rdi]` — the owner is
zero-extended from a dword and dereferenced. The whole pipeline is 32-bit by
design: `003DDA20` stores `mov dword[rax+rcx+8],r8d`; `003DDA70` writes the
descriptor owner dword `rsp+0x38 = ebx` and `rsp+0x40 = 003DD850` (lea).
Provenance census: `003DDA20`'s sole caller `003492C5` passes `xor r8d,r8d`
(NULL); `003DDA70`'s sole caller `003DD644` passes `rcx = rbx` = a record
pointer in the static table `0x26581A0` (`imul rbx,rax,0x1c; add rbx,rdx`,
`lea rdx,[rip+0x277acbc]`). Every owner reaching `003DD850` is therefore an
image-section address (< 4 GiB) or NULL — the dword round-trip is lossless.
The pass's low-32 claim is accurate and sound on the certified image.

## Attack O3 — is 0051FCF0 the removal, and does the sweep restart at 0051FE30?

`0051FCF0` byte-verified as the per-slot release: `rsi = movsxd(edx)*0x10 +
bank[rdi+0x38]`, bucket `rbp>>[rdi+0x4C]` → `[rdi+0x10]` (`shl 5`, 32-byte
buckets), `dec dword[rax+0x14]` refcount, conditional `call 0051F880` on
zero-count, next-id read at `dword[rsi+4]` returned in eax. `0051FE30` is the
find: `edi = [rcx+0x40]`, same bank/bucket resolution.

Sweep `00409CA0` verified end-to-end: `00409CD3 call 0051FE30` (find-first),
`cmp ax,-1; je out`, loop head `00409CE5` → render sweep `002ED570` /
`003B37E0` / `00409730` → `00409D18 call 0051FCF0` (removal) →
`00409D36 call 0051FE30` (restart) → `jne 00409CE5`. `00409D60` is a second
sweep with the same pair. The restart claim is exact.

## Verdict

**ACCEPT** both passes — E4's 32-bit owner is lossless (static-table or NULL
provenance only) and O3's removal+restart chain is byte-exact.
