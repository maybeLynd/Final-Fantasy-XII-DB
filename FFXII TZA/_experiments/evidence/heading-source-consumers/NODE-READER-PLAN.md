# Node field-reader feasibility, before a larger capture

Question: do the four type-specific step bodies immediately following the
verified constant-store entries read the corresponding node dwords? A read
would identify a concrete consumer to investigate; absence in these bounded
bodies would only rule out this candidate, not all readers or later scheduling.

Competing explanations: a same-type step directly consumes its flag; a shared
callee consumes it; or the flag is consumed elsewhere. Method A is sufficient
for this first discriminator. Read the four catalogued original ranges from the
certified EXE, classify memory operands with the reviewed access-role adapter,
and require exact bytes/decoded extent. No machine-code or live run.

Targets: 0045FD10/+3D8, 00529D50/+3D4, 0052A8B0/+434,
0052B5E0/+3F8. This is an offset-level feasibility scan, not receiver
provenance. Positive control: each known preceding 11-byte store must decode
as a memory write at the expected offset. If any body is incomplete or a
reader lacks pointer provenance, stop at candidate status and inspect only the
specific dependency. Do not infer an initialized node, a frame delay, or game
presentation. Preserve original module/tool identity and raw instruction rows.
