# ASTRA — Git verification caught derived-text newline conversion

The first publication is commit `ec31aa985cb2b3a3e073cf2ed115b66f3dfeb124`.
Its exact reviewed Git blob pins passed, but the separate verification of
manifest SHA-256 values **from committed content** failed on `disassembly.txt`.
Windows text writers emitted CRLF; Git's text filter stored LF. The initial
manifest had hashed the working-file bytes. That publication's manifest cannot
be reported as fully verified. The research task was not finished after the
failure, and the next task was not claimed.

The original reference EXE, retained instruction hex, parsed observations and
semantic comparisons are unchanged. This was a packaging-integrity failure in
derived text, not a new original-game result. The first commit preserves the
initial manifest and content for comparison.

Repair: normalize this package's text artifacts to LF, make the capture writer's
newline explicit, reseal the manifest and republish only changed reviewed paths.
Rerun the same focused evidence replay; verify each manifest entry against the
actual committed blob before accepting publication. This changes no repository
Git settings, shared publisher or peer files. No native/live rerun is needed.
