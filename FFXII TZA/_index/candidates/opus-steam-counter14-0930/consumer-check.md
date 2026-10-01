# Consumer check: the Steam page's shop-driver counter feed corrected (OPUS, 2026-09-30)

SWE2-STRUCT's DD batch 11 ([`swe2struct-ddres-b11-0930`](../swe2struct-ddres-b11-0930/README.md), checks S1-S2) read the
shop transaction driver `0056D370`'s counter call. The `0x2C0` bazaar-mode test guards only the `0030B630` unlock call,
so counter 19 is passed on every purchase, and the sale arm passes counter 14 (*Privateer*) with the quantity sold when
`+0xE4 & 0x3FC0 == 0x1C0`. OPUS corrects its own page.

- **Corrects:** in steam-integration-and-achievement-catalogue.md, the counter-17 census's "gated on `[+0xE4] & 0x3FC0 == 0x2C0`" (struck, with a dated note), and the §9 feeder list, which named only 19 for `0056D370` (a dated note adds 14).
- **Affected:** 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the Steam page's two sentences | revised-here |
  | the bazaar recipe page's PlatformOnlineAchievements crossing (it named only counter 19) | revised in the OPUS batch-5 publish (dated note) |
  | members/achievement-descriptors.tsv and menuhandbook-achievement-records.tsv (counter 14's descriptor, *Privateer*, mode 0, threshold 1000) | agree (descriptor data; no feeder column) |
  | the counter contract page | agrees (it names no feeder of counter 14 or 19) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2struct-ddres-b11-0930/b11_struct.py (S1-S2 pin the sale and purchase arms; FAILS 0).
- run: b11_struct.py at d200a4ac2 (FAILS 0, re-run by OPUS on the worktree)
