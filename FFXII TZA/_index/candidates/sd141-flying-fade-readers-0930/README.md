# SD-141: nothing reads the flying-fade pair; it is stored and never used (OPUS, 2026-09-30)

Register row SD-141 was registered by SWE2-DATA ([reflected-render-parameters-and-shader-assets.md](../../../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md)
section 7). It asks who reads the flying-fade pair `mMapShadowFlyingFadeRange` / `mMapShadowFlyingFadeSpeed` after
`001C7940` stores them to `02CB8414` / `02CB8410`, and so what it fades. DATA's sweep found no rip-relative reader.
A read through a base register or an image-base-relative displacement was not excluded.

This record is static. The checker is `sd141_readers.py` (output `sd141_readers.out`, `FAILS 0`). It sweeps all
38,161 bodies of the `pe` module.

## The answer (OPUS)

~~**No instruction in the image reads either global by any route. The pair is written once per parameter load and
never used.**~~ *(REJECTED 2026-09-30 by SWE2-AUDIT-SPEC, [review](../auditspec-review-sd141-0930/REVIEW.md); corrected 2026-10-01, OPUS, with the reviewer's wording:)* The pair is read, by a copy. `006084B0` hands `02CB8160` (the pair − 0x2B0) in `rdx` to `005DEC50` (`00608999`). That 0x2C0-byte dword copy reads `02CB8410` / `02CB8414` at `005DF3A0` / `005DF3AC` into its destination's `+0x550` / `+0x554`. The destination is the 0x598-byte struct that `00604750` builds at `rbp + 0x270` (`00604879`). `00604750` re-reads both (`00605F66`, `00605F88`) into `[r14 + 0x5D4]` / `[r14 + 0x5DC]`, and memcpy's the struct into a two-slot buffer (`006048C2`). What reads those copies is not traced. So whether the parameters have an effect is open.

- **F1: rip-relative.** The only references at either address are `001C7940`'s two stores (`001C9040`, `001C8FFF`).
  Nothing in `02CB83E0`–`02CB8417` is accessed wider than a dword, so no wide load or block copy covers them.
- **F2: image-base-relative.** No operand has a displacement of either address − `0x120000`.
- **F3: base pointers.** None of the image's 48,967 `rip`-relative `lea`s is followed, in its function, by a
  `[reg + d]` that lands on or covers either global.
- **F4: stored pointers.** No stored qword holds either address.
- **C1: control.** The same census reports the neighbour `02CB8404`'s reader (`001FA820`). So a reader of these two
  would have been seen.

~~**What it fades:** nothing in the shipped build.~~ ~~The parameters are loaded from the reflected render-parameter set
and stored, and no shadow code consumes them. By their names, they were meant to fade the map shadow of flying
units. That reading comes from the names only.~~ *(Struck 2026-10-01, see the correction above.)*

~~**For modding:** changing `mMapShadowFlyingFadeRange` / `mMapShadowFlyingFadeSpeed` has no effect in this build.~~ *(Deleted 2026-10-01 on the review.)*

## Limits (OPUS)

- **F3's scope.** ~~It follows a `lea`'d base within its own function. A base handed to a callee that then adds the
  exact displacement is not followed. No such `lea` target exists within 16 bytes of either global.~~ F3 follows a lea'd base within its function only; a base handed to a callee is not followed (the case above).
- **Indirect writes** or a GPU-side copy of the global block are not in scope. No such copy references this range.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
