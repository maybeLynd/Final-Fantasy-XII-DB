# Game files and data tables

How game files are found, loaded and read: archives, file tables, the battle and game data tables and the image formats.

| Page | What you will find |
|---|---|
| [Bigfile archive: the VBF container, how its index loads and is checked, and how a read reaches the file](bigfile-archive.md) | The FFXII_TZA.vbf archive the game reads its data from: how it is mounted, the SRYK header, the index of MD5 keys, 32-byte entry records, names and the 64 KiB block-size table, the MD5 check over the index and what it does not cover, the lookup by the MD5 of a path, the pool of reader handles, how a read is planned block by block and inflated with zlib, the shipped counts, and the rules a repacker must follow. |
