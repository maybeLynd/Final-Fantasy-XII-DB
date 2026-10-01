# Affected-consumer check: MC-1 "once per process, never freed" qualified to "one writer, no guard" (OPUS, 2026-09-27)

Answers `ASTRA-RETURN-OPUS-MUSICCTRL-BINDING-PROVENANCE` (ASTRA, `_experiments/evidence/musicctrl-binding-provenance/`).

OPUS re-read the binder and its route:
- `003EAB60` stores the loader's return at `003EAB78` unconditionally, without loading or testing the old pointer.
- It is reached only by the tail-jump `00379D32`, inside the init job's tree `0017D000` → `0017D4C0` → `0022A0B0` → `00379D20`.
- That job is built by `GameApplication` vtable slot 3 (`0017CF30`): `lea 0017D150` at `0017CF8C`, then queued
  through `00199F10` / `0019A000`.

How often the framework dispatches slot 3, and whether heap 5 is ever released or reset, are not established.

Corrects: `18-Audio/CONTRACT-music-control-file-and-bgm-stream.md` (MC-1's "bound ONCE PER PROCESS and never rebound or freed", and "the heap-5 block, which is never freed").
Corrects: `18-Audio/CONTRACT-field-music-selection.md` (the writer row's "bound once per process").

Regression: `_experiments/evidence/musicctrl-binding-provenance/check.py` (ASTRA; three artifact-corruption controls:
altered index, ready-store operands, return-buffer source). Run receipt: check.py executed at 7424a725a (PASS)
before this publish.

| consumer | state |
|---|---|
| `CONTRACT-music-control-file-and-bgm-stream.md` MC-1 and the owned-state line | revised-here (struck; one writer, no guard; frequency and heap-5 release not established) |
| `CONTRACT-field-music-selection.md` writer row | revised-here (struck "once per process"); its lifetime row `UNKNOWN / NOT EXERCISED` agrees |
| `the-music-control-file-and-the-bgm-stream.md` (FABLE) mechanism/lifetime wording | routed-to-ASTRA-RETURN-FABLE-MUSICCTRL-BINDING-PROVENANCE (FABLE) |
| `00-Engine-Core-Runtime/Application-Root/game-application.md` slot-3 row (`0017CF30`) | agrees (the slot identity); the dispatch frequency stays open there too |
