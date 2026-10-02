# Save / Load / Settings

**Engine category.** The SaveImage persistent payload, the settings serializer, and load/save lifecycle.

| | |
|---|---|
| Classification source | PrimaryOwner: Save/Load/Settings |
| Functions | 87 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`how-a-manual-save-is-committed.md`](how-a-manual-save-is-committed.md) —
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. The save-slot transaction step by step: header zeroed, three files deleted, the
  image written, the header stamped `{checksum, 1}` - one storage operation at a time, each started by the
  completion of the last.

- [`Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md`](Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md) —
  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: DOCUMENTED`)*. A save is **353,936 bytes** with a **512-byte header**, and the game keeps
  **four copies in memory** spaced `0x566C0` apart. Header carries area id, map group and party
  leader. Opened by U-1.

A full map of the persistent payload is a high-value target - it defines what is actually durable world state.

- [`Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`](Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) —
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. The payload region by region from a typed field scan with global-pointer
  seeds: the achievement block inside the image (`AB-5`), the two SpawnKeep images and their group
  banks, the transition snapshot and its mirror, the transition metadata, the rebased inventory
  descriptors, the header's writers; both access tables beside it.

- [`Game-Settings-Config/ff12config-and-debglobal.md`](Game-Settings-Config/ff12config-and-debglobal.md) —
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. The two archive entries without an extension: `FF12CONFIG`, a PS2 option block the
  PC build still loads at start-up but whose copied bytes no consulted reader acts on, and `DebGlobal.bin/file1`,
  four development-network addresses nothing refers to.

- [`where-the-game-keeps-your-files.md`](where-the-game-keeps-your-files.md) — the per-user directory and its two path builders — **AUDITED**
- [`the-save-load-screen-widgets.md`](the-save-load-screen-widgets.md) — the slot screen, the write spinner and the controller's fifteen states — **DOCUMENTED**
- [`CONTRACT-save-image-pipeline.md`](CONTRACT-save-image-pipeline.md) — **CONTRACT READY**
- [`CONTRACT-save-image-buffers.md`](CONTRACT-save-image-buffers.md) — **BEHAVIORALLY UNDERSTOOD**
- [`CONTRACT-save-container-transform.md`](CONTRACT-save-container-transform.md) — **BEHAVIORALLY UNDERSTOOD**
- [`CONTRACT-storage-read-completion.md`](CONTRACT-storage-read-completion.md) — **DIFFERENTIAL TESTED**
- [`Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md`](Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md) — the two stamps and the load normaliser — **DOCUMENTED**
- [`Save-Image-Layout-And-Pipeline/katano-debug-savedata.md`](Save-Image-Layout-And-Pipeline/katano-debug-savedata.md) — the sixteen shipped development saves — **AUDITED**
- [`Game-Settings-Config/CONTRACT-game-setting-config.md`](Game-Settings-Config/CONTRACT-game-setting-config.md) — **RUNTIME VALIDATED**
- [`Game-Settings-Config/game-settings-ini-and-runtime-config.md`](Game-Settings-Config/game-settings-ini-and-runtime-config.md) — `GameSetting.ini`, its 31 settings and the frame-rate switch — **AUDITED**
- [`Game-Settings-Config/the-settings-command-table.md`](Game-Settings-Config/the-settings-command-table.md) — the in-save options record and its command dispatch — **AUDITED**
- [`Language-And-Locale/language-selection-and-locale-ids.md`](Language-And-Locale/language-selection-and-locale-ids.md) — language ids and the confirm-button convention — **AUDITED**
- *(corrected 2026-10-02, OPUS: twelve pages this list omitted, added with the status each page's own front matter states)*

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
