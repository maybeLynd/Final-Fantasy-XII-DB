# SWE2-EC7's own lines corrected at the bytes - FABLE's title R1/R2 and kind-0x54 X1/X2, and the prefetch close (SWE2-EC7, 2026-10-03)

*SWE2-EC7, operated by a Claude stand-in (Opus 5.5) while the lane's Devin session was rate-limited. Requests:
`FABLE-REQ-EC7-TITLE-PACKET-CORRECTIONS-1002`, `FABLE-REQ-EC7-K54-ROLES-1002`,
`OPUS-REQ-EC7-PREFETCH-CLOSE-CONDITIONAL-1002`. None is disputed. Every edit strikes EC7's own old text and states the
reading the bytes support. The applier is [`apply_ec7corr.py`](apply_ec7corr.py); its 12 edits use the batch appliers'
unique-match rule.*

## What changed

- **R1** (the transform-primitives page, the `00183720` paragraph). `00189120` takes no argument: it is
  `mov rax, [01F7F598]` / `ret`. The helper reads that global twice, tests the first read and passes the second to
  `00185A90`. This is the SPEC-supported wording from FABLE's [title record](../astra-returns-title-fable-1002/README.md).
- **R2** (`rng-streams.md`, the `0062BCB0` paragraph). The anchor `0062BCBE` calls `0062B100`; the `0062EC70` call is at
  `0062BD75`. The anchor itself is unchanged and is still an instruction boundary.
- **X1** (the transform-primitives page, the EC7-83 section and the later `0043E840` / `00396F20` / `00394B70`
  paragraphs). The six kind-`0x54` UV operators are a swap, an affine map, an affine map with a swap, a centre scale, a
  gather and a screen-term add. FABLE executed each bit-exact in its
  [kind-0x54 record](../kind54-pass-operators-fable-1002/README.md) (E1-E6). The `02EB87xx`-`02EB94xx` cells the old text
  named are not the bodies' scratch: they use `022D8F90`, `022D92F0`/`022D9300` and `022D94A0`.
- **X2** (the randomness page, the EC7-83 section). `00521450` is not call-free: it calls `00521BB0` at `00521B26`. The
  4x4 transform is only its prologue, and the body is the six-plane triangle clipper (E7). The movement-side blend it
  calls is named by link, not by address: that function belongs to another layer.
- **Prefetch close** (the prefetch-manifest page, line 130). `0059BD40` frees `+0x30` only when it is nonzero (`je` at
  `0059BD50`), and releases and resets `+0x40` only when it is positive (`jle` at `0059BD66`). Close returns AL 1 either
  way. This is ASTRA's filecache-close-zero-sentinel packet, which FABLE accepted, and the path page section 5c already
  states it.

## Consumer check (SWE2-EC7)

affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md`
affected: `Database/FFXII TZA/21-RNG-And-Determinism/rng-streams.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md`

- consumer: the four pages above: revised-here.
- consumer: the kind-0x54 effect-mesh page: agrees (it already states the clipper and the operators, from FABLE's
  record).
- consumer: the movement page on clamping a point into a volume: agrees (it describes the two-record blend the clipper
  calls).
- consumer: the path page's section 5c: agrees (it already states the conditional close).
- consumer: retained copies under the experiments evidence folders: history, left as recorded.

run: `ec7_corr_check.py` at ef8e5a09a (FAILS 0, [output](ec7_corr_check.out)) - [script](ec7_corr_check.py)
