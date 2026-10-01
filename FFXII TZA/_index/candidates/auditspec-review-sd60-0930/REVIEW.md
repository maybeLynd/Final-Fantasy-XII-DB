# SWE2-AUDIT-SPEC review of SD-60 (sd60-gibegineff-blocks-0930 at 5f7bd30da): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `5f7bd30da` (record) and its prose-only correction `f55dd3c9a` (Limits, on SWE2-AUDIT-SEM `e89b4567b`).
Record: [sd60-gibegineff-blocks-0930](../sd60-gibegineff-blocks-0930/README.md). Static, image `FFXII_TZA.exe`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD60-0930 | sd60-gibegineff-blocks-0930 | 5f7bd30da (+ f55dd3c9a) | ACCEPT-WITH-NARROWING |

**Re-run.** `sd60_gibegineff.py` from its own directory: F1-F6 PASS, `FAILS 0`, byte-identical to the committed
`.out` ignoring CR ([rerun_sd60_gibegineff.out](rerun_sd60_gibegineff.out)). The record directory stayed clean.

**Re-derived independently** ([sd60_rederive.py](sd60_rederive.py) / [.out](sd60_rederive.out),
[sd60_rederive2.py](sd60_rederive2.py) / [.out](sd60_rederive2.out); raw `.text` sweeps through `tk.py`, not the
function list):
- **F3, the depth terms.** The whole of `00678B50` read: m33 (`+0x3C`) compared with 0; equal: xmm0 = f, xmm4 = n·f,
  both divided by (n − f) and stored to `+0x28` / `+0x38`; otherwise xmm0 = the 1.0 at `01CEBBA8` and xmm4 = n, both
  divided by (n − f). So m22 = f/(n−f), m32 = nf/(n−f) (perspective) and 1/(n−f), n/(n−f) (orthographic). HOLDS;
  these are the right-handed D3D projection depth terms as stated.
- **F4, "only 0024FF60 writes the floats".** Rip-relative sweep of `02AEEBA0..02AEEBA7`: 8 references, 4 stores, all
  in `0024FF60` (`0024FFBB`, `0024FFC3`, `0024FFE2`, `0024FFEA`); 0 image-base-relative forms. HOLDS in both
  addressing forms. The readers are `0039D1E0`, `0039D1F0` and `0039CDC0` (a min/max clamp).
- **F1/F5, block 1.** `02AEEB20..5F` has 5 rip references and 0 stores. `0024E180` passes it in `rcx` (the output)
  to `00202D60` (`jmp 00216720`), which reads its input through `rdx`. The other three address-takers
  (`00376470`, `0039CDC0`, `0039CF10`) pass it in `rdx`, as an input. So `0024E180` is its only producer, and
  `0024E180` has one caller, `003828DB` in `003820C0` (raw call index). That `00216720` computes an inverse is
  the author's reading; this review did not re-derive the arithmetic.
- **F6, the device.** Execute passes its second argument (`rdi`) as the device; `[vtable+0x30]` is called with the
  `+0x48` block. The only RTTI names containing `PrimitiveRenderer` are `PrimitiveRenderer` and
  `PrimitiveRendererD3D11`, and the only DIR64 pointer to `006CAF40` is slot `00D86990` (`00D86960` + 0x30).
  `006CAF40` copies 16 dwords to `+0x10..+0x4C` and stores byte 1 at `+0x208F3`. HOLDS.
- **The execute targets.** `01FD3620..01FD3667`: 6 stores, all in `00210520`; readers `0020EA50` and `00210230`
  (`00210230` reads `01FD3664` at `0021026C` and `01FD3660` at `002102C5`), matching the corrected Limits.

**The narrowing (a prose defect, not a checked finding).** F5 says "`002F5550` ... calls `0024FF60` right after
`003B4150` ... `003820C0` does the same before `0024E180`." Read plainly, that makes `003820C0` a second caller of
`0024FF60`. It is not. A raw E8/E9/jcc sweep finds exactly one branch to `0024FF60`, at `002F58BD`. `003820C0` calls
`003B4150` (at `003828CF`) and then `0024E180` (at `003828DB`); it never calls `0024FF60`. So the two floats
have one producer path: the map-ctrl-pack presentation pass.

**Controls.** F1-F6 are instruction-text point checks at fixed addresses. They catch a wrong address or operand, but
they cannot catch a second writer or caller. F4's "only writer" is the one census claim, and it rests on retool's
rip-reference cache. The image-base sweep above closes that gap. No control covers the F5 caller sentence, which is
why it drifted.

**Correction wording for the row owner (SWE2-DATA).** Where SD-60's row or page restates the float source, use:
"The two floats are written only by `0024FF60` (4 stores), which has one caller: `002F5550` at `002F58BD`, right
after `003B4150` sets `02B40470`. `003820C0` calls `003B4150` and then `0024E180` (block 1's producer), not
`0024FF60`." The rest of the answer stands as written.
