# The four-slot drain bullet corrected on FABLE's adapter-family page - consumer check (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). F1 of [FABLE's title packet record](../astra-returns-title-fable-1002/README.md):
the `00186230` bullet on [the return-value adapter family](../../../24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md)
said "run by the per-frame pump" and "calls every entry and empties it". The accepted title-queue-pump packet shows one
flush at most per call of the pump, gated on a zero dword, with pump calls not shown to be frames. The accepted
title-queue-consumption packet shows the loop stops at a snapshot of the write cursor, resets the write cursor of the
bank the index then names, and frees nothing (the body's only call is the indirect entry call).*

affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md`

- consumer: the adapter-family page's `00186230` bullet: revised-here (strike and restate).
- consumer: the title-asset page's FABLE subsection: agrees (it states the same two facts).
- consumer: `ta-texture-animation-lists.md`, the EC7-77 slotted push_back paragraph: agrees.
- regression: run: [`title_astra_check.py`](../astra-returns-title-fable-1002/title_astra_check.py) at 5b8ffef20 (FAILS 0).
