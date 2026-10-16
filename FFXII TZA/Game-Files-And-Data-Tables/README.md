# Game files and data tables

How game files are found, loaded and read: archives, file tables, the battle and game data tables and the image formats.

| Page | What you will find |
|---|---|
| [Bigfile archive: the VBF container, how its index loads and is checked, and how a read reaches the file](bigfile-archive.md) | The FFXII_TZA.vbf archive the game reads its data from: how it is mounted, the SRYK header, the index of MD5 keys, 32-byte entry records, names and the 64 KiB block-size table, the MD5 check over the index and what it does not cover, the lookup by the MD5 of a path, the pool of reader handles, how a read is planned block by block and inflated with zlib, the shipped counts, and the rules a repacker must follow. |
| [File path resolution: how a file name becomes bytes through the RAM file cache or the archive, the stream reader, and what lives under .dat and .bin](file-path-resolution.md) | How the game opens a file by name: the PStreamReaderFile stream and its read, seek, open and close slots, the resolver with its selector and log tags, route 1 into the RAM file cache (the upper-case key, the 33-multiplicative hash, the name filter, hits, stamps and views) and route 2 into the archive (the lower-case key and MD5), how an archive hit is copied into the cache, the cache's memory budget, insertion, eviction and view release, and the formats that share the .dat and .bin extensions. |
