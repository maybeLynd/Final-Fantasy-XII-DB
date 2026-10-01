# Audit-spec section acceptance: SECTION-05

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Task `OPUS-REQ-AUDITSPEC-SECTION05-ACCEPT-1001`
Subject: `291ec5588`; owner review `section05-owner-review.md` (conditional: accept corrections,
disposition nine contract tokens + the page's forty lost addresses).

## Verdict: ACCEPT

## Condition check — all nine tokens restored in the contract at HEAD

`CONTRACT-encoded-id-space-and-class-registry.md`: `002FD530`/`002FD640`/`002FD780`/`002FD880`
(mutation handlers), `0032302E`/`00323036`/`00323039`/`00323041` (validator shared tail),
`EXP-100` — all present.

## Byte-verified anchors (certified image)

**Q05-01** `00309440`: `movzx eax,cx / shr eax,0xC` (nibble), `cmp eax,0xE / ja`, `imul rcx,rax,0x58`,
`lea rax,[rip+…]` → `01EEBCF8`, `mov eax,[rcx+rax]` — the registry row +0x38 read; nibble+5 class
mapping stands ✓
**`+0x54` RMW** `0031CA3C`: `movzx eax,byte[rbp+7] / shr al,1 / xor al,[rbx+0x54] / and al,1 /
xor byte[rbx+0x54],al` — bit-0 read-modify-write exactly as the owner derived; it does refute the
older "read and never written" section, and the page records that ✓

## Scope note

The page's forty overlay-dropped addresses were dispositioned by the page's authors per the
owner's routing; contract-side tokens verified here. Q05-02..06 and Q05-08..12 stand at fixture
scope, not re-derived.
