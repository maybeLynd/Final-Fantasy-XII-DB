# REVIEW — FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930

*Provenance: written by the concurrent SWE2-AUDIT-SEM session (OPUS-run Claude) that has since ended; its board finish cited `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-takebacks2.md` (gitignored) for the ACCEPT recorded on FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930 at 06:36Z; for t3b it is superseded by the scoped REJECT in auditsem-review-takebacks2-0930 (contradiction AUDITSEM-CONTRA-FABLE-T3B-REGION-A-WRITERS-0930). Published here by the remaining session of the same identity, text unchanged except that each `##` heading now names SWE2-AUDIT-SEM.*

Reviewer: SWE2-AUDIT-SEM (independent). Commit `8bdf31fcb`. Reviewed 2026-09-30.

## VERDICT: ACCEPT (SWE2-AUDIT-SEM)

All five items re-run non-author and attacked with my own disassembly/census.

### 1. rc9_channels.py — FAILS 0; MANUAL reads independently verified (SWE2-AUDIT-SEM)

Sampled 7 of the 13 MANUAL reads covering every resolution class, byte-verified against the image:
- `006865DB`/`006867C7` (bound loop): `mov ebp,r13d` init, `inc ebp` at `00686366`, `cmp ebp,2; jb` bound at
  `0068636C`, `mov ebp,1` arm at `006863FF` — channel = ebp ∈ 0..2 ✓
- `006391F2` (pinned by cmp): `cmp eax,1/je` skip, `cmp eax,2/jne` skip → `lea ecx,[rax-1]` = 1 ✓
- `0062A22A`, `00677D3E` (copied register): `rbp=rax; test rax,rax; jne` → rbp=0 on the fall-through site ✓
- `005CCF6C/8B/99`, `0079C42B`, `00194796`, `001D4636` (constant before jump): `mov ecx,2`/`esi,1`/`ebp,2`
  verified at the named addresses, jump chains carry it to each site with no intervening write ✓

No site passes channel 4 — conclusion stands.

### 2. rc8_inverse.py — h1 and h3 outputs byte-identical to committed; attack found no missed writer (SWE2-AUDIT-SEM)

My own rip-relative census of `01F82EA8` found **8 refs in 4 functions**, not the two get-or-creates the README
prose names: `001F0810`, `001F0850`, plus the un-named `001F1590` and `001F1600` (both: load cell → null → alloc
0xB08 → `call 001EF2D0` → store cell). This is a prose completeness nuance, NOT a coverage hole — the census is
loader-based and all four functions are in H (the "4 cell loaders"), so both extra sites' only constructor path
(`001EF2D0`) is already in H+1. No writer escapes.

The three non-ctor W∩H3 members were independently disqualified:
- `001D0390` writes one `rdi` object out to `+0xAE4`/`+0xB04`/`+0xB44`+ — larger than the 0xB08 shadow ✓
- `001EB190`'s caller `001EBA40` allocates `ecx=0x2E0` before calling it — different singleton ✓
- `0018CD90` is a ctor pattern (`rbx=rcx`, base-init call, byte-field stores) on per-caller allocations ✓

### 3. RC-7 chain — `rsp+0x5C` IS SampleDesc.Count (SWE2-AUDIT-SEM)

`0061FDA0`: desc built at `rsp+0x48` (Width `+0x48`, Height `+0x4C`, MipLevels `+0x50` — verified the stores).
`+0x48+0x14 = +0x5C` = D3D11_TEXTURE2D_DESC.SampleDesc.Count; `+0x60` = Quality (zeroed `0061FE6B`). The MSAA byte
`[rcx+9]` read at `0061FEC1` → `mov [rsp+0x5C],eax` at `0061FECC`; remaps `7→{Count 4, Quality 0x10}`
(`0061FED5`/`0061FEDD`) and `9→{8,0x10}` (`0061FEEC`/`0061FEF4`) byte-verified; `call [rax+0x28]` at `006200E5`
= CreateTexture2D ✓.

### 4. rc10_gates.py — 245 sites / 136 functions control matches; 17 candidates classified correctly (SWE2-AUDIT-SEM)

9 warn-once latches + 4 functional + 1 screen-mode + 3 linear-window artefacts = 17. Spot-verified:
`00601E24` warn-once (`cmp byte[02CE9D9D],0/jne` skip; `mov byte[02CE9D9D],1` immediately before the call);
`007977E7` functional (`cmp eax,4/jae` on the `02EA9500`-loaded count); `007994D8` window artefact
(`cmp byte[02EA523E],0` at `007994B4` jumps AWAY via `je 0x79973e`/`jmp 0x799765` — the site is gated only by the
local `cmp di,r13w`). No verbosity gate exists ✓.

### 5. t3b_regionA.py / t4_desc_inserters.py — reruns byte-identical to committed .out files (SWE2-AUDIT-SEM)

T3B: `FAILS 0`; PASS S1 (kind-9 enqueuer only `0058111E`), S2/S4 controls positive, region A reachable only via the
`002370D3` memset covering the span. T4: all three positive controls found (`0062EFD0` inline pair, `00635980`
rip-formed pair, helper `006B67D0` with all 70 call sites resolving to absolute heads); zero inline inserts at
D ∈ {+0x60,+0x68,+0xB0,+0xB8}; zero static heads at those offsets on descriptor-typed objects; 315 static
descriptors loaded.

## Board (SWE2-AUDIT-SEM)

`FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930` → ACCEPT.
