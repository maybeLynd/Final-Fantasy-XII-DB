# Affected-consumer check — "what `005C5230` returns in play" (FABLE, Claude Opus 5.5, 2026-09-26)

The manager-slot contract kept "what `005C5230` returns in play" as a live-only question, and called side B's use of it
"a behavioural difference". `005C5230` is the three-byte retail stub `33 C0 C3` (`xor eax, eax` / `ret`). So side B's
negative-fifth-argument value is always 0, the same zero side A substitutes. The slots end up identical; the only
difference is a call to a side-effect-free stub, visible in a call trace and nowhere else.

This is propagation, not discovery:
- the register's `DA-4` row names the stub under four other identities;
- the 2026-09 falsification log (`PROGRAM-STATE.md`, "manager slot tables — SURVIVED") says "both sides compute the same
  value; the asymmetry is the call, not the result".

The contract body and the S-52 verdict cell never took it in.

A citation is corrected on the way: side A's `xor ecx, ecx` is at `003DA45A`. The contract's `003DA425` is not an
instruction start (`003DA423` is `test rcx, rcx`).

**Regression, run by FABLE 2026-09-26:** `_index/candidates/mgrslot-stub-005C5230/stub_value.py`, FAILS 0. It checks
the stub's bytes, side B's `test` / `jns` / `call 005C5230` / `mov ecx, eax`, and side A's `xor` / `cmovns`. The known
positive is that it must find the call.

| consumer | state |
|---|---|
| `04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md` symmetry box ("That is a behavioural difference", the `003DA425` citation) | revised-here |
| same contract, "Side B resolves before it validates" and the unbounded-subscript item ("supplied by `005C5230`") | revised-here (always 0); the resolve-before-validate order stands as a trace fact |
| same contract, "What is still owed" item 1 and "What execution would still add" item 1 | revised-here (answered statically; the pilot is not needed) |
| same contract, owed items 2 and 3 (large fifth arguments, `002640C0`'s slot choice) | agrees: still open, not affected |
| `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md` `+0x174` prose | revised-here (the default is always channel 0) |
| `_index/L2-VERDICTS.md` S-52 binding gap "live-only: `005C5230`'s return" | routed-to-FABLE-REQ-AUDITSEM-S52-005C5230-IS-A-STUB (AUDIT-SEM's cell) |
| `Reconstruction/Game/Actor/manager_slot.c` comment "side B has already called 005C5230" | agrees (a trace fact) |
