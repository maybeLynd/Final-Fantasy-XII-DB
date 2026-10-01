# Affected-consumer check — contract sentences still calling answered questions open (FABLE, Claude Opus 5.5, 2026-09-26)

Two contract sentences kept "open" / "not established" after their register rows were answered. This is the same
drift class as NS-4 (`43e75987d`): the answer lives elsewhere and the consumer was never updated.

- **`UQ-136`.** `CONTRACT-level-advance-and-growth.md` says the middle forwarding call "remains open on the page". The
  register answered it on 2026-09-25: `1` is a target count and `0x71` the `c_all.efx` effect group spawned on the
  unit.
- **`DD-1`.** `CONTRACT-binding-profiles.md` says the `0x70` → runtime conversion is "still not established for bank
  A". The same contract's §7a answers it: `00195DF0` writes records 2–4 of bank A (`01DF1738` = `01DF1480` +
  2 × `0x15C`), and its register row has read ANSWERED since 2026-09-08.

**Regression:** `_index/candidates/contract-open-drift/contract_drift.py`. It is a scan for contract lines that call an
id open while its register row reads ANSWERED. The first run found these two; the other three hits are a table cell
and two sentences that record a closure, and are left as they are. After the fix, a re-run no longer reports UQ-136 or
DD-1.

| consumer | state |
|---|---|
| `13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md` presentation paragraph | revised-here (struck; points at the answer) |
| `15-Input/Binding-Profiles/CONTRACT-binding-profiles.md` §2 shape box | revised-here (struck; points at §7a) |
| `_index/OPEN-QUESTIONS.md` UQ-136, DD-1 rows | agrees (already ANSWERED) |
| `15-Input/Binding-Profiles/CONTRACT-binding-profiles.md` §7a and the table row `~~DD-1~~ ANSWERED` | agrees (the source of the answer) |
