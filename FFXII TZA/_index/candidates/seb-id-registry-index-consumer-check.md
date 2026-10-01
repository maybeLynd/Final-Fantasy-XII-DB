# Affected-consumer check — a sound id's `id >> 9` is the SE-block registry index, not the `.seb` block number (OPUS, 2026-09-26)

**The correction.** [`seb-se-block-index.md`](../../18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md) §3.4
(OPUS, 2026-09-15) derived `id = (block << 9) + slot` from `003A1180`. It then read the block field as the `.seb`
block **number**: *"Given a block number, this index resolves a slot to real audio at
`sead_data_win/se<n>/se<n>.win.sab`"*.

The field is the **SE-block registry index** (0..63), raised by FABLE as
`FABLE-CONTRA-OPUS-SEB-ID-BLOCK-FIELD-IS-THE-REGISTRY-INDEX`:
- **Registry entry.** Entry `k` of the `0x18`-stride registry at `02AEEDC0` carries `word +8 = k`, which the validation
  in `003A1180` enforces.
- **Loader.** The loader masks that word `& 0x3F` (`002DEF00`) and installs the bank with the index at `+0x3C`
  (`00223C83`). The file's own block number `n` goes to `+0x38` (`00223C9C`).
- **Lookup.** The group player `0021B5B0` matches `id >> 9` against `+0x3C`.

§3.4 is restated in place, with the wrong sentence struck.

**Regression:** [`seb-id-registry-index-check/check.py`](seb-id-registry-index-check/), STATIC, ALL PASS (4/4). Its
`result.json` md5 is `e66d6663…`, identical over two runs. Every instruction is decoded at its address from the
shipping image:
- **C1:** the id is the registry entry's `word +8` shifted by 9, after the self-index validation.
- **C2:** the loader masks that word to the index and forwards `n` separately, through
  `001DBD20` → `00210B60` → `0021B430` → `00223AD0`.
- **C3:** bank `+0x3C` is the index and `+0x38` is `n`.
- **C4:** the lookup compares `id >> 9` with `+0x3C`, never `+0x38`.

A reimplementation that keys the lookup on the file's block number fails C4.

**Not settled here:** whether, for the one handle that is live in shipped play (`02AEF3FC`; FABLE's UQ-149 answer: always
`se000.seb`), the registry index happens to equal `n`. That depends on which record `003A0C90` claims at boot. It was not
measured, and nothing below relies on it.

| consumer | state |
|---|---|
| `18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md` §3.4, "Given a block number, this index resolves…" | revised-here (struck; restated through the registry slot's bank `+0x38`) |
| same page §3.4, `id = (block << 9) + slot` and the arithmetic | agrees (the arithmetic is exact; the restatement box names "block" as the registry index) |
| same page §3.4 ⚠ box, "positions 128–511 of every block's id range are not addressable" | agrees (a statement about the id stride against the 128-slot index; true per registry slot) |
| same page §3.2 "Registration — `003A1650`", `002DEF00(slot & 0x3F, blob)` | agrees (already names the masked registry slot) |
| `00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md` §7 UQ-31, "the loaded sound group numbered `id >> 9`" / "an object whose `+0x3C` equals the group number" | agrees (FABLE's reading: the group number is `+0x3C`) |
| `13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md` UQ-135, `(bankWord << 9) + ecx`, "slot 7 of whichever bank is live" | agrees (the bank word is the registry entry's `word +8`; nothing there reads it as `n`) |
| `15-Input/Modal-Toggles/r2-force-fight-toggle.md` UQ-149, `bankSlot * 512 + index` | agrees (names the runtime bank slot) |
| `18-Audio/Audio-Boundary/CONTRACT-sound-request.md`, the resolvers `003A1070` / `003A1100` / `003A1180` / `003A11F0` | agrees (handles, liveness and arithmetic; no block-number reading) |
| `07-Combat-Action/applying-a-result-to-a-target.md` row 2, sound `0x34` through `003A1180` / `002DF220` | agrees (a bank-local slot through the resolver) |
