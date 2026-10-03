# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-game-application-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-GAME-APPLICATION-HOMING-1003` · Package: `_index/candidates/fable-game-application-homing-1003/` · Page: `00-Engine-Core-Runtime/Application-Root/game-application.md` (commit eea05327e; reviewed at HEAD f8b2904c0, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 177 functions, 844 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 177 rows and 844 anchors, `mode: homing`. Rejected 0, missing 0. Skipped 1 (`0019E010`, a 685-byte four-path body the session declined). Corrections 4 (`00798EB0`, `001D9FD0`, `00673030`, `0017F610`); the corrected texts are the ones on the page. All 177 rows are on the page at lines 2497–2673 (heading at line 2491), byte for byte.
- Semantic pass: **15 rows**, spread evenly through the list (row indexes 0, 13, 25, 38, 50, 63, 75, 88, 101, 113, 126, 138, 151, 163 and 176), were read clause by clause against `disw.py` output of the certified image (SHA256 73461D08...). Rip targets were recomputed by hand.
  - **`006AF910`: exact.**
    - The unlink writes `[[n]+8] = [n+8]` and `[[n+8]] = [n]`, then self-points both qwords (`006AF934`/`006AF937`).
    - The `not al` / `test al, 1` gate means bit 0 is clear before `00584730` runs.
    - Then `006AAA50(rdx)` at +0x45, and `mov al, 1`.
  - **`006D7EA0`: exact.**
    - `edx = 0` returns before the frame. The cookie comes from `01F44830` (`006D7EBC`) and is checked by `00808C40` (`006D8184`), on which every arm converges.
    - Weights are collected when `ucomiss` gives `jp` or `jne` (non-zero or NaN), paired with `[r8]` / `+8` / `+0x10`. c = `edx*3`.
    - The arm is selected on the count: 0 → `00861EC0` (memset); 1 → `00861EBA` (memcpy) when the weight equals 1.0 at `01CEBBA8`, else scaling, with nothing written when c = 0 (`006D80D3`); 2 and 3 → weighted sums.
    - The 4-source arm (`006D7F8D`) is unreachable, since at most 3 weights are collected.
  - **`00799C90`: exact.**
    - c = `btr` bit 31. old = qword / address / null on `jbe 1`.
    - `0017D260((c+1)<<6, 4)`; null returns `0xd` (`lea eax, [rsi+0xd]` with `rsi = 0`).
    - c elements are copied, then element c from `rdx`.
    - The free has four conditions, including bit 31 of `[rcx]` clear (`00799D7F`–`00799D89`).
    - `[rcx] = c + 1` (`00799DA0`).
  - **`001615C0`: exact.** `02CB7480` (call at +0xB), `00D3BC30` → `02CB7480`, `005FE350` → `02CB7580`, `02CB757C` = `(x & ~2) | 0xC`, then the tail jump to `00808B90(008AB0B0)`. All values were recomputed from the rip displacements.
  - **`001688F0`: exact.** `02EA0850`, `006DA380` → `02EA0950`, `00D8DFA8` → `02EA0850`, `02EA094C` = `((x & ~2) | 0xC) & ~8`, and `00808B90(008B78B0)`.
  - **`0019A450`: exact.** Three unrolled slots, each doing `00210EB0([b+8])` and zeroing only when non-null, then `00809950(b, 0x18)`. The slots of `rcx` are never written.
  - **`001A6CC0`: exact.**
    - Node walk 1 stops at `rcx+0x4f0`, with `[[obj]+8](obj, 0)` and next = `0016D6D0(node)`.
    - Chain 2 starts at `[rcx+0x500]` (`rdi+0x18` with `rdi = rcx+0x4e8`) and calls `001AF2B0(rcx+0x4e8, [node])` and `[[rcx+0x518]+0x18](rcx+0x518, node, 0x30)`.
    - The final stores go to `+0x4f0`, `+0x4f8`, `+0x500`, byte `+0x508` and dword `+0x510`.
  - **`001C0EB0` (`SaveloadManager_ScalarDeletingDestructor`): exact.** The vtable `008F9B80`, the guarded release with `AND ~0xF`, `test dil, 1`, then `00809950(rcx, 0xa78)` and `rax = rcx`.
  - **`001E74F0`: exact.** The byte `+0xb8` gate goes to `005CD6D0(rcx+0x90)`. Then `001E7560` at +0x2C (`rcx+0x58`) and at +0x36 (`rcx+0x20`), then the slot-`+0x18` release.
  - **`00240A00`: exact.**
    - `[0208E6C0]` and its `[+0]` are both null-checked.
    - The record is `0xd` at `rsp+0x20` plus 16 bytes from `00914D50` at `rsp+0x28`. The image holds dwords `0x2ca6, 0, 5, 0` there.
    - The cookie check runs on every path.
  - **`003DE480`: exact.** Byte `02B58C20 = cl`, then `0016D6A0(02B58C20)`, then qword `02B58C20` = 0, byte `02B58C27` = 0x80, and qwords `02B58C28` and `02B58C30` = 0.
  - **`005AA280`: exact.** `00809054(p, 0x138, [p-8], 005AA2F0)` (`r9 = 005AA2A2 + 0x4E`), then `00584730(p-8)`.
  - **`005F0470`: exact.**
    - Per 0x30-byte element it releases `[+0x18]`, `[+0x10]`, `[+8]` and `[+0]` (`rbx` = elem+0x10, at offsets +8, +0, −8, −0x10), each gated on non-null and bit 0 clear.
    - Then `00584730(rcx)`, which also runs on `edx = 0`.
  - **`00627CF0`: exact.**
    - `cmp edx, [rcx]` takes the whole dword.
    - `cmovb` gives the unsigned smaller of `edx` and n for +0x48 (`0061D030`).
    - 13 is returned only when the result is null and `edx` is non-zero. The free conditions match `00799C90`. `[rcx] = edx`.
  - **`00693C40`: exact.** `ecx = 0` returns 0. Then `0017D260(ecx*0x30, 8)`; null returns 0. Otherwise `ecx` × 3 `movups` pairs, returning the block.
- Advisory (not a defect): 162 of the 177 rows were not read in this pass. The request asked for at least 15. The four corrections FABLE recorded show the same kind of detail that the 15 sampled rows got right.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
