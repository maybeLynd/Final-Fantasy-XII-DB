# G-5 answered: no authored sequence reaches Magi, and the sync switch's 4.0 is seconds (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

G-5 asks how `Magi::Music` handles exploration↔battle transitions. The earlier narrowing (`g5-music-transitions/`,
M1–M4) showed the following:
- The exploration↔battle change is not a Magi transition. It is a track substitution plus a 2.0 s volume fade.
- Magi's own mode switch is the soundtrack version (command `0x26`, from Config).
- SetMode, Start and End (`0x21` / `0x27` / `0x28`) are posted only by `007EEA00`.

It left two residues: what `007EEA00`'s records are, and what the `0x26` argument `4.0` measures.

**Residue 1: no authored sequence can post Magi commands** (`g5_sequences_and_sync.py` Q1–Q3).
- `007EEA00` is SEAD's command-sequence interpreter. Its opcodes map as follows:
  - `0x100` → `0x1D`
  - `0x101` → SetMode
  - `0x102` → Start
  - `0x103` → End
  - `0x200` → a float ramp
- The interpreter's objects are allocated only by `007EE910`, and `007EE910` is called only by `007B6350`.
  - `007B6350` resolves a sequence by name in a 257-bucket table at `01F41460`.
  - `007B6350` is reached only from the driver drain `007AB5C0`'s arm for command `0x33`.
- Nothing posts `0x33`. There are 34 queue-allocation sites, and every one stores an immediate id; none computes one.
  - The 33 distinct ids include `0x21`, `0x26`, `0x27` and `0x28` (the positive control), but not `0x33`.

**Residue 2: the 4.0 is seconds** (Q4). `Music::SyncTo` (`007CAB80`) uses it in two ways:
- It adds samples / `[this + 0x64C]` to it.
- It scales (4.0 + 0.2) by `[this + 0x64C]` into samples for the sync search.

`+0x64C` is loaded from the music record's `+0x44` (`007C6FB0`). That value is 48,000 in all 116 shipped `.mab` music
records, which are all version 11.

**Not claimed:**
- Which data registers named sequences (`007B67E0`).
- What those sequences contain. None of them can start, so it does not affect the answer.

**Run receipt:** Q1–Q4 PASS, FAILS 0 (2026-09-27).

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` G-5 | ANSWERED; the earlier narrowing kept as *Earlier* | revised-here |
| `18-Audio/sqex-sd-sound-driver-architecture.md` G-5 box | ticked, with the answer | revised-here |
| `how-the-music-changes-when-you-change-area.md` §7 (the game side) | agrees | agrees |
