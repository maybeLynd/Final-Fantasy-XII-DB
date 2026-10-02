# Consumer check: 19-Save-Load contradictions from a local reconstruction-readiness pass, OPUS's share settled on the pages (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-SAVE-1002: stream R run locally. A read-only reader mapped `19-Save-Load-Settings/`
(rated NOT YET; the map is filed in the RE repo as `docs/readiness/19-save.md`). It found 52 contradictions, 30 of
them value-changing, every one decided at the image or the shipped data. It also found claims the bytes refute: for
example, `0020E540` is no writer, because it forwards to the `ret 0` stub `0016D6A0`.

A second read-only pass drafted 123 strike edits (`apply_19save.py`). FABLE is working again (user, 2026-10-02), so
OPUS applies only the 54 edits on OPUS-led and shared pages (`apply_by_owner.py OPUS`). The 58 edits on FABLE-led
pages and the 11 on SWE2-EC7's language page are routed as requests; each lane runs `apply_by_owner.py <name>`.
OPUS re-checked a sample of the value items at the bytes (`save_check.py`).

- **Affected:** 19-Save-Load-Settings/CONTRACT-save-container-transform.md, 19-Save-Load-Settings/CONTRACT-save-image-buffers.md, 19-Save-Load-Settings/CONTRACT-storage-read-completion.md, 19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md, 19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md, 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/katano-debug-savedata.md, 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md, 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md, 19-Save-Load-Settings/where-the-game-keeps-your-files.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the nine OPUS-led and shared 19-Save pages | revised-here |
  | the seven FABLE-led pages (save-image pipeline contract, ff12config, ini, manual save, README, save-image layout, save-load widgets) | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 58 edits) |
  | the language and locale page | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 11 edits) |
  | RE repo `docs/readiness/19-save.md` | routed-to-OPUS (filed from this commit) |
  | the structural gaps (slot-list fill, the write worker `003BAEB0`, the storage command table) | routed-to-OPUS (later reads) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-save-readiness-fixes-1002/save_check.py, verified at b1490763c: 11 instructions decode as cited, FAILS 0 ([`save_check.out`](save_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (54), FAILS 0.
