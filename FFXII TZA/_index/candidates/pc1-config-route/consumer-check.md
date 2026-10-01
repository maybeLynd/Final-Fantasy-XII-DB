# Affected-consumer check: PC-1's route clause answered - FF12CONFIG is read from the archive; three "loose-file" labels corrected (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md (the PC-1 box and the file-helper crossing note), 02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md (the Presentation/Audio crossing note), 02-Resource-And-Asset-Pipeline/the-resource-request-queue.md (the crossing list), 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md (status and §8), 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md (§7 CreateFileA line)
run: pc1_route.py at 061f2188c (worktree = that HEAD plus this package), 7 checks FAILS 0. R3 and R6 measure the "loose-file" labels (no handle source, no CreateFile but the minidump writers); R4 measures route 1's identity; R5 the one archive.

| consumer | what it said | state |
|---|---|---|
| `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md`, PC-1 box | "whether the loader's stream reads the archive entry or a loose file" open | revised-here: answered beneath (the archive, or the cache's copy); box stays open for the other clauses |
| same page, the Presentation/Audio crossing note (FABLE, pass 22) | `001D6E80` / `001D6F20` / `001D6FA0` "are the engine's generic loose-file helpers" | revised-here: "loose-file" struck, "file-stream" with the correction |
| `02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md`, crossing note (FABLE, pass 22) | "The loose-file open `001D6F20`" | revised-here: "loose-file" struck with the correction |
| `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md`, crossing list (FABLE, pass 22) | "The loose-file open `001D6F20`" | revised-here: "loose-file" struck with the correction |
| same page, §8 read layer | `002DF780` chooses "the loose-file open (`001D6FB0`)" or "the archive read (`001D6D90`)" | not revised: `001D6FB0` / `001D6D90` are the asynchronous queue-item pair, not this resolver; which source their worker uses is not read here (filed as a lead) |
| `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`, status and §8 | "which route serves loose files" and "what route 1's manager is" open; the filter "a dot four or five characters from the end" | revised-here: both answered; the filter description qualified (nine tests; the page's prediction holds) |
| `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md`, §7 | "What `FUN_005CCAB0` and `FUN_0079B1E0` open with `CreateFileA`" | revised-here: answered (minidump files) |
| `02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md`, `00597930` / `0059A9B0` update | the three-source record and the commit-and-release | agrees; this package uses them |
| `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md`, `001D6B20` / `0019AEE0` notes | manifest flag accessor; five-slot resolver | agrees on the calls; `01F83440` is written only by the cache sizer `0020C610` (always 1), so "manifest flag byte" is the cache-enable byte - not revised here, noted |
| _index/OPEN-QUESTIONS.md PC-1 | PARTIAL, route clause open | revised-here: route clause answered, row stays PARTIAL |

Regenerated with it: nothing.
