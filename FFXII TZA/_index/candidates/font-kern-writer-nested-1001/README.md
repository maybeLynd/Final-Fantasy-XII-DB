# font-kern-writer-nested-1001 — the .ker pair writer is nested, keyed transposed (SWE2-DATA, 2026-10-01)

Resolves board task `OPUS-CON-FONT-KERN-WRITER-NESTED-0930` (a P1 contradiction). OPUS, on SWE2-ORACLE
`08f4c0821` (`sd81-eastl-callers-0930` K1/K2), refuted the published claim on
`16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md` that the `.ker` writer `001FDC10`
stores a flat `map<first, adjust>` and dead-drops `r8d` (record `+4`).

This record re-reads all four bodies against the certified image and confirms the refutation, adding the
key-order finding the contradiction asked for ("the key-order decision").

**Static.** No execution, no live evidence. Checker `kern_nested_check.py` (`FAILS 0`, 18 checks) reads the
certified image (A0: SHA-256 `73461d08…21f8`) through `retool.py` and asserts every instruction pattern
below. Output: `kern_nested_check.out`.

## The corrected reading

The loader `001B5230` reads `{first, second, adjust}` records and calls
`001FDC10(font, first=edx=rec+0, second=r8d=rec+4, adjust=r9d=rec+8)` (L1).

**The writer `001FDC10` builds the nested map — keyed transposed (W1–W4):**

- It spills `r8d` (`second`, record `+4`) to its home slot `[rsp+0x18]` at `001FDC15`, then passes that
  slot's address (`lea rdx,[rsp+0x60]` after the frame shift) as the key to `001FC420(font+0x70)` — a
  find-or-insert on the font's `+0x70` EASTL map (I20, `0x60`-byte nodes). `second` is **the outer key**,
  not dead-dropped.
- `001FC420` returns `lea rax,[rbx+0x28]` (`001FC55C`) — the outer node's value, which is itself an EASTL
  map (`"EASTL map"` tag at `001FC487`; `sd81-eastl-callers-0930` K2).
- `001FDC10` then walks that inner map comparing `node+0x20` against `ebx` (`edx` = `first`, record `+0`),
  and on a hit stores `edi` (`adjust`) at `node+0x24` (`001FDC66`); on a miss it inserts through `001FC9F0`
  (I19, `0x28`-byte nodes) and stores adjust at the fresh node's `+0x24` (`001FDCAF`).

So the writer populates `ker[second][first] = adjust` — **`map<leftCp, map<rightCp, i32>>`** — exactly the
nested shape the reader walks, but with the two record fields in the opposite slots.

**The reader `001FDDD0(font, prev=edx, cur=r8d)` queries the transposed order (R1):**

- Outer tree: sentinel `font+0x78`, root `[font+0x88]`, keyed on `r8d` — the **current** glyph's kern cp
  (the kern arm at `002AC52F` passes `ecx=[rbx+0x20]`, the current glyph, through `0017F8E0`→`001E9780`,
  which forwards it to `r8d` and supplies `edx=[ [rcx+0x28] + 0x20 ]`, the previous glyph's stored kern cp —
  R2).
- On an outer hit the inner tree sits inside the outer node: sentinel `node+0x30`, root `[node+0x40]`
  (the embedded map at `node+0x28` — the same +0x28 the writer's `001FC420` returns). Inner key vs `r10d`
  (`edx` = **prev**); the kern value comes back from inner `node+0x24`.

So the reader asks `ker[cur(right)][prev(left)]` for a tree the writer filled as `ker[left][right]`.
A lookup `(cur, prev)` can only return a stored adjust when some authored record has `first == prev` and
`second == cur` — i.e. it returns **the reversed pair's adjustment**, and only for glyph pairs authored in
both orders. The published bottom line (the authored `.ker` pair adjustments do not reach the rendered
advance) survives, but the mechanism is key-order transposition, not a flat map with `second` dropped.

## Corrections applied to the page

- §1 player-facing paragraph: "structurally inert … flat `map<rightCp, adjust>`" → the nested map is built,
  keyed transposed; authored pairs unreachable except reversed-pair coincidences.
- §2 `KerPair +0x04` note: "loaded, then dead-dropped by the shipped store" → the outer-map key.
- §3 `.ker` paragraph and the "read side expects a nested map the writer never builds" paragraph rewritten:
  the writer builds `map<second, map<first, adjust>>`; the reader queries `map<cur, map<prev, ·>>`.
  The 0x28-node claim is kept where true — it describes the INNER nodes (I19), not the outer (I20, 0x60).

## Consumers

See `consumer-check.md`. Register rows citing the inert-kern claim: none — `OPEN-QUESTIONS.md` has no
`001FDC10`/ker-pair row (checked 2026-10-01).
