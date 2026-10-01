# 0x72 field gate to oscillator: bounded source discriminator

Claim at issue: after the type 0x72 constant store `node+0x3F8=1`, normal
type-specific step `0052B5E0` checks that field and, when nonzero, calls
`0052BBD0`. Existing oscillator page names `0052BBD0` as a caller of
`0054B1F0`, the parameter-install routine. What exactly does the intervening
body do, and is the parameter-install edge conditional on further state?

Competing explanations: it directly reaches `0054B1F0` on a supported source
path; it calls it only after additional object/resource gates; or the page's
caller summary elides a different edge. Method A is sufficient for source
control flow. Check existing page and immutable node-reader package, then
capture the single 925-byte original `0052BBD0` body and its immediate direct
edges. Source method cannot prove initialized object validity, that the type
step runs after the setter, heavy nested native effects, scheduling, or
presentation. No FF12 process, native harness, saves or configuration touched.

Positive controls: certified EXE hash; preceding parent call and field read
against published source; catalogue size/complete decode; expected direct
`0054B1F0` edge. Failure/stop: incorrect range identity, incomplete decode,
no expected edge, or unresolved indirect call prevents a stronger inference.
Keep original instruction/raw bytes, tool/provider identity and exact limits.
