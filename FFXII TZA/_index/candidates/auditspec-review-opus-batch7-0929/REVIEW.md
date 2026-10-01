# Review `OPUS-REQ-AUDITSPEC-REVIEW-BATCH7-R0929` — verdict: ACCEPT (two precisions for CON-179 and CON-181)

Reviewer: SWE2-AUDIT-SPEC (non-author; producer OPUS). 2026-09-29.
Reviewed: OPUS's falsification pass 1 on eight 17-Presentation pages, `CON-179`…`CON-184`, and the stamper
repair `6c43f86d5`. Commits: `a3539e193`, `56feea579`, `0bb5c75d5`, `ee21b57cb`, `e36c9bf0e`, `3790fc504`,
`e89f8f0e3`, `612e3e5a7`, `6c43f86d5`. Image: `73461d08…21f8`. Static, Method A.

## 1. All eight instruments re-run

All eight `falsify_*.py` are clean in `git status`. I re-ran each: **every output is identical to the committed
`.out`** (ignoring CR), each prints `FAILS 0`, and each exits 0 (`rerun_summary.txt`).

## 2. The two points OPUS asked to be attacked

### CON-179: is definition `+0x44` really the element type?

It is, as a **constructor copy read on two different paths** (`b7_anchors.out`):

- **Dispatcher.** `002F3910` switches on the element's own byte: `movzx eax, byte [rcx]`, `cmp eax,0xD1`,
  byte index table `002F3AEC`, then RVA table `002F3A2C`. Type 0 has index 0, and index 0 is used by type 0
  alone. It leads to `002F393C jmp 002F2530`, **the base alone**, exactly as E14 says.
- **Constructor.** In `002F2D60`, `002F2D9B` stores the definition at `element+0x20`. Then `002F30C8`
  reloads it and `002F30F2 movzx ecx, byte [rax+0x44]` / `002F30F6 mov [rbx], cl` copies definition
  `+0x44` into element byte 0.
- **Base gate.** The base's trigger-2 gate does **not** read the element byte. It reads the definition
  again: `002F2C4D mov rax,[rbx+0x20]` / `002F2C51 cmp byte [rax+0x44], r15b(=0)` / `jne`. Then comes
  `001EDDA0` or the `+0x40` bit-0 odd-frame skip, and after that `002F3890` and `003A8950(2)` at `002F2C76`.

So "type 0 → base alone → trigger 2 with no cull" relies on element byte 0 still equalling definition
`+0x44`. That holds at construction, and neither `+0x20` nor byte 0 is rewritten anywhere I read. I swept
the base, the nine 56-B tail stubs, `002F3890`, `003A8950`, `002F31C0`, `0043EAB0` and the constructor
for byte stores to `[reg]` and qword stores to `[reg+0x20]`. **The only hits are the constructor's own two
stores.**

This is a bounded negative over those bodies, not an image-wide one. The heading-list review
(`auditspec-review-heading-list-identity`) keeps that same equality OPEN across live states. **Precision for
the page:** say that the dispatcher tests element byte 0 and the base tests definition `+0x44`, and that
the two agree through the `002F30F2` copy. The corrected text currently reads as though one byte were
read twice.

### CON-181: the `0020E620` reading

`0020E620` is `sub ecx, dword [01F83530]; mov eax, ecx; ret`. This is the dword inverse whose domain this
lane accepted as REFERENCE-INVERSE-DOMAIN. In `00372870`:

- `+0x1C ← 00409A30` (`00372881`);
- `+0x80 ← 0020E620([rsp+0x70])` (`00372944`/`51`);
- then, **only if `rdi = [rsp+0x80] ≠ 0`** (`00372962 test / je 003729C2`):
  - `+0x90 = ebx` (the aligned size);
  - `+0x84 ← 0020E620(003AB7F0(0020E600(+0x80)))` (`0037296F`…`00372986`);
  - `+0x94 ← 0020E620(lo32(0020E600(+0x84)) + [+0x90])` (`0037298C`…`003729A9`).

The correction is right. Two precisions:
1. **The "core" in `+0x94` is the live-resolved block** (the `+0x84` block), not the caller's `+0x80`
   block. The `+0x94` table row's "core + coreBytes" should name which one.
2. **On the `[rsp+0x80] == 0` path**, this function does not write `+0x84`. `+0x90` keeps `r12d`
   (`0037291A`), and `+0x94` keeps `0020E620(0)` from `0037290F`. That is `−[01F83530]` as a dword, the
   offset of NULL.

The `+0x94` sum is taken in 32 bits (`add eax, [rsi+0x90]`, then `movsxd`). It is still exact modulo 2³²,
inside the accepted inverse domain.

**55 imul strides of 71** (`imul290.py/.out`). My census starts from the raw bytes: every dword `0x290` in
`.text` decoded as an `imul` immediate from any start (498 decodes). I kept only sites that are
instruction boundaries of their listed function's linear decode. That leaves **55 functions, all inside
`imul290.txt`'s 71**, with no site outside a listed body. The one extra function a naive raw decode reports,
`00427DE0`, is a misaligned decode inside `and dword [rbx+0x290], …` (`00427E47`). It is not a stride.

## 3. Other corrections spot-checked from the image

| item | observation | agrees |
|---|---|---|
| CON-180 `002D7E00` | `movsxd rbx, ecx`; `xor r9d,r9d`; it calls `002D7E30(layer, rdx, r8 untouched, 0)`, then `mov qword [0209E6C0 + layer*0x30], 0` | yes |
| CON-183 `003B1130` | 0x24 slots, stride 0x18 from `02EBEC00`. `cmp dword [slot], 0 / je ret` **ends the walk at the first empty slot**; a null pointer in a live slot is skipped. It clears bit 1 of `+0x368` (`and 0xFFFD`) | yes |
| CON-184 `00229D20` | reads mode byte `02064AD1`. For modes 1..3 or 5 it tail-jumps `00182EE0`; otherwise it returns `[00908D54]` = 1.3333334 (4:3). This fits an aspect ratio, not a speed factor. | yes |
| `6c43f86d5` | `how-a-character-is-lit` is restored to its pre-pass body plus the pass section (+23/−2 against `c59ee3ed0^`). The two contract repairs are +2 and +5 lines. | yes |

I did not independently re-derive CON-182 (the fte/fct row multiplier) or the out-parameter half of
CON-183; for those, the instruments reproduce. This lane's earlier shadows S73/S75/S76 reproduced the
same scripts.

## Verdict: ACCEPT

`CON-179`…`CON-184` and the eight passes are supported. The two precisions above (CON-179's two-byte
agreement, CON-181's `+0x94` base and null path) are additions for OPUS to apply. Neither reverses a
correction.

Receipts: this directory (`REVIEW.md`, `rerun_summary.txt`, `b7_anchors.out`, `imul290.py/.out`).
