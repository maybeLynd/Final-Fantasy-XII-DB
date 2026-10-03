# SWE2-AUDIT-SPEC review — fable-the-context-switch-axes-and-the-variant--homing-1003

**Target.** `_index/candidates/fable-the-context-switch-axes-and-the-variant--homing-1003/` (task `FABLE-REQ-AUDITSPEC-FABLE-THE-CONTEXT-SWITCH-AXES-AND-THE-VARIAN`)
**Verdict.** ACCEPT

## What was checked

- **Mechanical checker.** `fable-the-context-switch-axes-and-the-variant--homing-1003/interior_applier.py` re-run verbatim in place: `FAILS 0`, matching the committed `interior_applier.out`.
- **Semantic pass.** All 6 rows / 30 anchors verified instruction-by-instruction against the certified shipping image (SHA256 `73461D08...D89721F8`, canonical VAs incl. image base). Every named address (call targets, globals, RIP-relative loads/stores, float constants) resolved to the claimed value; every stated offset, bound, sign, stride, arg order and branch polarity matched.

## Per-row notes

Six sibling context registrations 001670A0-F67230: each calls 006B8D20 on its 01F2EBxx/ECxx slot, on zero increments (or adds 3 to) counter 02E522E0 and stores the slot count dword; unconditionally stores the 00D80E-Fxx descriptor address into the slot qword and tail-jumps 00808B90 with rcx = the matching 008B58B0-5B30 thunk. All rip-relative targets resolved and confirmed; 00167140 additionally stores byte 0 at 01F2ED04 as documented.

## Limits

Body statements only, per the package README — the sentences describe instruction behaviour, not semantics. Cloud-drafted rows stand on FABLE's re-read; this review independently re-derived every row from the image.
