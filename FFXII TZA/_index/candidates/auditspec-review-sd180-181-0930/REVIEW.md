# REVIEW: sd180-181-emitter-walk-0930

- **Package:** `sd180-181-emitter-walk-0930` (OPUS, commit `1dbac71de`)
- **Task:** `OPUS-REQ-AUDITSPEC-SD180-181-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of OPUS author maybeLynd)
- **Verdict: ACCEPT-WITH-NARROWING**

## Controls re-run

`sd180_walk.py` re-executed (`rerun_sd180_walk.out`): W1-W4 + B1 PASS, `FAILS 0`, output
text-identical to the committed `.out` (CRLF only). Package dir clean after re-run. Image sha256
asserted `73461d08…21f8`.

## Independent derivation (own loader `sdx_indep.py` + capstone, `sd180_rederive.out`)

Independent re-derivation (sections A–E of `sd180_rederive.out`, verified byte-exact on the
certified image by this reviewer):

- Dispatch confirmed: `0036326A movzx ecx, byte [rbx+9]` / `and ecx,0x7f` → class 0 → `003632C1`,
  1 → `003632AF`, 2 → `00363293`, else fall-through `0036327D`.
- `00361810` reads the record at `+0x1B, +0x10, +0xB, +0xA, +9, +0x2C, +0x2E` — **not +0x38** (section B).
- W2: `ucomiss xmm6,xmm7; jp; jne` — takes `003638B0`'s result only on exactly-0.0 ordered compare. ✓
- W3: `003638B0`: `js` on `[rcx+0x1A]` sign, `movsx`, `jmp 003639FF` (`mov eax,esi`). ✓
- B1: `003635C0` is a 3-instruction leaf (clears `022CBA90`/`022CBA9A`, stores rcx→`022CBAF0`);
  `022CBAF0` census (section E): 17 rip refs, writers = `00362FA7` (boot), `00363737` (unload
  zero), `003635CE` (the `003635C0` store). No image-base/data/DIR64 refs. ✓

## Narrowings (found on the bytes)

1. **W1 "+0x38 (all classes)" is false for the fall-through arm.** The `class ≥ 3` arm at
   `0036327D` copies the unclamped point `[rsi]`, passes `xmm1 = 0` (xmm7 = xorps'd),
   `xmm2 = xmm8 = 4.1415929`, `xmm0 = xmm9 = -1.0`, and jumps to `003632E0` — **past** the
   `+0x38` load at `003632DB`. Verified directly: `0036327D movaps xmm0,[rsi]` … `00363291 jmp
   003632E0`. The page's own SP1 table lists class 3 as the shipped class ("constant arm — no
   transform call"), so shipped records take this arm. The same "(all classes)" overreach
   appears on the map-ctrl page.
2. **Class 2's arg6 is subtracted, not added.** `00362230`'s result lands in xmm6 (arg6) and is
   `subss`'d at `003619A9` inside `00361810` — "adds 00362230's own float result" should read
   "passes (subtracted downstream)".
3. **W4 omits two driver steps** in `00362850`: initial value `esi = [022CBA80]` (00362870);
   the second walk runs only when `0020E600(…) != 0` (`00362B8F je`); then
   `cmp byte [022CBA91], bl(=0)` / `cmovne esi, [022CBA84]` substitutes a stored value
   (`00362BBE`/`00362BC4`); and `cmp [022CBA80], esi; je` gates the `002DF410(1, 0xB4, value)`
   dispatch to value-changed only (`00362BCB`/`00362BD1`). All verified byte-exact.

## Limits

- Section F of the re-derivation (shipped SP1 record parse) did not reproduce the page's 2,326
  records (found 14,272, classes up to 9) — the `{u16 bound; u16 recordOff[]}` index parse is
  suspect and is **not cited** in this verdict. The narrowing above stands on the dispatch arms
  alone plus the page's own class-3 statement.
- Static only; no runtime trace.

**Verdict: ACCEPT-WITH-NARROWING** — dispatch, compare semantics, return path and `022CBAF0`
writer census all hold; the "+0x38 all classes" claim and the additive description of class 2's
arg6 are narrowed as above; W4's driver sequence is narrowed to include the omitted steps.
