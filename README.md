# Final Fantasy XII: The Zodiac Age - engine database

A description of how the PC release of *Final Fantasy XII: The Zodiac Age* works, built by reading the
shipping executable: game systems, data formats and the code that reads them.

Pages come in three kinds:

- **System pages** describe a game mechanic: what the player sees, how it works, its layouts,
  operations and state, and modding notes.
- **Format pages** describe a file or data format: where it comes from, its layout, the shipped data
  and how the loader treats each field.
- **Reference pages** list a set of game values, with the same data beside them as a `.tsv` file.

Each page title names the topic and then what the page covers. Each category's README lists its pages
with a one-sentence summary of what you will find on each.

Addresses are virtual addresses in the shipping `FFXII_TZA.exe` (SHA-256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`), image base included.

## Categories

- [World, areas and travel](FFXII%20TZA/World-Areas-And-Travel/README.md) - Areas and zone changes, the per-area map information table, weather, save crystals, teleports, chocobos and airships.
- [Battle actions](FFXII%20TZA/Battle-Actions/README.md) - How an attack, spell, technick or item use is chosen, charged, targeted and carried out.
- [Rewards: EXP, LP, gil and loot](FFXII%20TZA/Rewards-EXP-Gil-And-Loot/README.md) - What a defeated enemy gives: EXP, LP and gil, loot drops and pickups, the kill chain, levelling up and the gil cap.
- [Random numbers](FFXII%20TZA/Random-Numbers/README.md) - Every random number generator in the game, how each is seeded and which rolls use it.
