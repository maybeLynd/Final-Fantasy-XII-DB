# Consumer check: DD batch 9 corrections on the two VBF pages (SWE2-CONTRACT content, OPUS owner re-status, 2026-09-30)

SWE2-CONTRACT's batch 9 (this folder's README) answered the two pages' open items in place and struck their superseded
statements; OPUS's owner read moved both to DOCUMENTED.

- **Corrects:** in how-the-bigfile-index-loads-and-is-verified.md the section 7 items "The per-entry record layout inside the index is not read here", "Where the archive is reopened for payload reads, and whether a handle is pooled", "Whether entries are decompressed on read, and by what codec" and the status note "The per-entry record layout - section 7's first unknown is untouched"; in area-nmb-index.md "the five unresolved ResourcePath_Get call sites in section 3", "both" and the 002DF780 cell "entry only".
- **Affected:** 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md, 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the two pages' own sections and status lines | revised-here |
  | how-a-path-is-resolved-to-bytes.md (cites the bigfile index's handle and block reads) | agrees (its route-2 reading is the same opener and planner) |
  | the file-size-tables page (.fst kind-37 array) | agrees (the array's end at index 2,963 matches all twelve .fst files, per the record) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b9-0930/b9_vbf_nmb.py (155 checks, FAILS 0 at b58c633f7,
  including the MD5 key match 89,414 of 89,414 and the size array's two agreeing bounds).
