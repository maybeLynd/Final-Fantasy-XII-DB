# RNG and Determinism

**Engine category.** ~~The gameplay MT19937 stream and the separate shared procedural render PRNG - two different domains that must never be conflated.~~ At least eight random generators that must never be conflated: the two gameplay generators specified exactly (the shared LCG and the gameplay MT19937), the CRT `rand()`, which also reaches gameplay, and the presentation and engine streams (the graphics-noise MT19937, the presentation bit-feedback PRNG, the stream-5 counter hash, the PPFX xorshift128 and the Bullet solver LCG) *(corrected 2026-10-02, OPUS: rng-streams.md's opening line and §10 — the PPFX xorshift128 `0074BDE0`, checked at `0074BFE0`–`0074C0C4`; the CRT `rand` at IAT `008C3098`, 48 call sites in 30 functions)*.

| | |
|---|---|
| Classification source | PrimaryOwner: RNG |
| Functions | 18 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`rng-streams.md`](rng-streams.md) - the ~~two independent random streams~~ generators, at least eight, and their streams *(corrected 2026-10-02, OPUS: rng-streams.md's opening line and §10)* — **AUDITED**
- [`which-roll-is-on-which-generator.md`](which-roll-is-on-which-generator.md) - which roll is on which generator, and what reseeds each — **AUDITED**
- [`CONTRACT-gameplay-generators.md`](CONTRACT-gameplay-generators.md) - the shared LCG and the gameplay MT19937, draw for draw — **DIFFERENTIAL TESTED** (the algorithm only)
- [`CONTRACT-which-generator-serves-which-roll.md`](CONTRACT-which-generator-serves-which-roll.md) - the routing of consumers to generators — **BEHAVIORALLY UNDERSTOOD**
- *(corrected 2026-10-02, OPUS: three pages this list omitted, added with the status or readiness each page's own front matter states)*

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
