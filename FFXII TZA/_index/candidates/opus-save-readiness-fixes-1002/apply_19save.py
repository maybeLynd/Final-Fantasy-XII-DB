"""apply_19save.py [--apply] - 19-Save-Load-Settings readiness map (readiness-19-save.md), section 2.4
contradictions 1-52 and the section 2.5 claims the bytes refute, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the DISFAVOURED side only (the side the image or the shipped data refutes) and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*.
Items 22, 23, 29 and 30 favour no page: the wrong figure is struck on every cited side that states one and the
checked value restated (item 29's second side, the-save-payload-field-map.md "1,725 sites", already states it).
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment instead of a strike (their OLD includes the line end, so NEW
never contains OLD). No front-matter edits; no heading changes.
X1-X4 are the section 2.5 refutations: the no-op 0020E540 (shared by three pages), generation B's header constants,
header +0x40 / +0x44 / +0x57 bit 1, and the 01F82E38 readers.
The structural gaps (section 2.2) are left for later, as briefed.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "19-Save-Load-Settings/"
R = F + "README.md"
WK = F + "where-the-game-keeps-your-files.md"
MS = F + "how-a-manual-save-is-committed.md"
W = F + "the-save-load-screen-widgets.md"
CSP = F + "CONTRACT-save-image-pipeline.md"
CSB = F + "CONTRACT-save-image-buffers.md"
CCT = F + "CONTRACT-save-container-transform.md"
CSR = F + "CONTRACT-storage-read-completion.md"
SI = F + "Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md"
PM = F + "Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md"
VS = F + "Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md"
KS = F + "Save-Image-Layout-And-Pipeline/katano-debug-savedata.md"
CGC = F + "Game-Settings-Config/CONTRACT-game-setting-config.md"
GI = F + "Game-Settings-Config/game-settings-ini-and-runtime-config.md"
SC = F + "Game-Settings-Config/the-settings-command-table.md"
FC = F + "Game-Settings-Config/ff12config-and-debglobal.md"
LL = F + "Language-And-Locale/language-selection-and-locale-ids.md"

NOOP = "`0020E540` is `call 001C18E0` then `jmp 0016D6A0`, and `0016D6A0` is `ret 0`"

EDITS = [
    # C1: a manual save writes the ACTIVE buffer (00581DCA-00581DCF rdi = 002EF640(); 00581F27-00581F2F element
    #     +0x28 = rdi, +0x30 = 0x56690; kind 8 at 00581F51); staging / submission serve the autosave 0057E310 only.
    (CSP, "*live → (capture) staging → (copy, SV-2) submission → (tail-call, SV-6) writer.* Separately and off",
     "~~*live → (capture) staging → (copy, SV-2) submission → (tail-call, SV-6) writer.*~~ *live → (storage queue, "
     "kind 8) file* for a manual save; the staging and submission copies serve only the autosave `0057E310` "
     "*(corrected 2026-10-02, OPUS: checked at `00581DCA`–`00581DCF` `rdi = 002EF640()`, `00581F27`–`00581F2F` element "
     "`+0x28 = rdi`, `+0x30 = 0x56690`, kind 8 at `00581F51`; and " + NOOP + "; "
     "save-image-buffers-header-and-payload.md §5)*. Separately and off"),
    (CSB, "One copy is live while you play, one is the snapshot taken\n"
          "when you save, one is what gets handed to the file write, and one is a backup.",
     "One copy is live while you play~~, one is the snapshot taken~~\n"
     "~~when you save, one is what gets handed to the file write,~~ and is the one a manual save writes; one is the "
     "autosave's snapshot and one what the autosave `0057E310` hands to the storage machine *(corrected 2026-10-02, "
     "OPUS: checked at `00581DCA`–`00581DCF` and `00581F27`–`00581F2F`, the manual save's element `+0x28` is "
     "`002EF640()`, the active buffer)*; and one is a backup."),
    (SI, "player saves\n",
     "player saves   <- corrected 2026-10-02, OPUS: a manual save writes ACTIVE, not STAGING (00581DCA-00581DCF, "
     "00581F27-00581F2F, kind 8 at 00581F51); staging and submission serve the autosave 0057E310 only\n"),

    # C2 + X1 + C41: 002EF690's copy reaches no file - 0020E540 is call 001C18E0 / jmp 0016D6A0 (ret 0), checked at
    #     002EF72C and 0020E540-0020E576; the "handle" is a one-bit selector that selects nothing.
    (SI, "and then clears that flag (`001C1919`..`001C192E`): the manual save's deferred hand-off, driven from "
         "`0017D6E0`.",
     "and then clears that flag (`001C1919`..`001C192E`): ~~the manual save's deferred hand-off~~ a copy that reaches "
     "no file, because its tail is a compiled-out stub *(corrected 2026-10-02, OPUS: checked at `002EF72C` and "
     "`0020E540`–`0020E576` — " + NOOP + "; the manual save writes the active buffer, §5)*, driven from `0017D6E0`."),
    (CSB, "Step 4 is the write submission, and it is the *point* of the operation: the copy does not merely\n"
          "stage the image, it hands it on. A reader who took this section at its word would build a\n"
          "reconstruction that fills a buffer nobody collects.",
     "~~Step 4 is the write submission, and it is the *point* of the operation: the copy does not merely~~\n"
     "~~stage the image, it hands it on. A reader who took this section at its word would build a~~\n"
     "~~reconstruction that fills a buffer nobody collects.~~ Step 4 reaches no file: " + NOOP + ", so the "
     "submission buffer this copy fills is collected by nothing *(corrected 2026-10-02, OPUS: checked at `002EF72C` and "
     "`0020E540`–`0020E576`; only `0057E310` and `00581DA0` reach the storage machine — "
     "save-image-buffers-header-and-payload.md §5)*."),
    (CSP, "| **Downstream** | `0020E540`, the writer |",
     "| **Downstream** | `0020E540`, ~~the writer~~ a compiled-out stub, not a writer *(corrected 2026-10-02, OPUS: "
     + NOOP + ", checked at `0020E540`–`0020E576`)* |"),
    (CSP, "**SV-6 — The submission buffer is handed to the writer by tail-call, with the size passed\nexplicitly.**",
     "**SV-6 — The submission buffer is handed ~~to the writer~~ by tail-call to `0020E540`, with the size passed\n"
     "explicitly.** *(corrected 2026-10-02, OPUS: `0020E540` is no writer — " + NOOP + ", checked at "
     "`0020E540`–`0020E576`; the copy reaches no file, and only `0057E310` and `00581DA0` reach the storage "
     "machine)*"),
    (CSP, "*What the writer\nselects with that bit is the writer's question, not this contract's.*",
     "*~~What the writer~~\n~~selects with that bit is the writer's question, not this contract's.~~* *(answered: it "
     "selects nothing — `0020E540` is a compiled-out stub, as corrected above; 2026-10-02, OPUS)*"),
    (CSB, "What the bit *selects* inside `0020E540` is outside\n   this family and stays open.",
     "~~What the bit *selects* inside `0020E540` is outside~~\n   ~~this family and stays open.~~ *(answered: "
     "nothing — " + NOOP + ", checked at `0020E540`–`0020E576`; 2026-10-02, OPUS)*"),
    (CSB, "           return submitWrite(bit, submit, IMAGE)   /* 0020E540, a TAIL JUMP */\n",
     "           return submitWrite(bit, submit, IMAGE)   /* 0020E540, a TAIL JUMP */   <- corrected 2026-10-02, OPUS: "
     "0020E540 is a stub (call 001C18E0; jmp 0016D6A0 = ret 0); nothing is written\n"),
    (SI, "       -> FUN_0020e540(handle, 0x02211000, 0x56690)      -> to disk\n",
     "       -> FUN_0020e540(handle, 0x02211000, 0x56690)      -> to disk   <- corrected 2026-10-02, OPUS: not to "
     "disk; 0020E540 is call 001C18E0; jmp 0016D6A0 (ret 0), and 'handle' is the one-bit selector of 00236760\n"),
    (SI, "    FUN_0020e540(handle, &DAT_02211000, 0x56690);   // same size\n",
     "    FUN_0020e540(handle, &DAT_02211000, 0x56690);   // same size   <- corrected 2026-10-02, OPUS: 'handle' is "
     "a one-bit selector (00236760), and 0020E540 is a stub (call 001C18E0; jmp 0016D6A0 = ret 0)\n"),
    (CSP, "here:** the handle source. **Not this contract's:**",
     "here:** the ~~handle source~~ selector source `00236760`, a one-bit read, not a handle *(answered: see SV-6 and "
     "CONTRACT-save-image-buffers.md §14 item 2; 2026-10-02, OPUS)*. **Not this contract's:**"),
    (CSP, "through `00236760`, the handle source SV-6 names, or through",
     "through `00236760`, the ~~handle source~~ one-bit selector *(answered: see SV-6; 2026-10-02, OPUS)* SV-6 names, "
     "or through"),

    # C3: queue kind 7 is a write (00582149-00582160 -> 003BB920, 02B40E1C = 2 at 003BB98C), nothing is read back.
    (SI, "     first 8 bytes back into active+0 (op 7, `00581FD9`). So the file carries whatever is live in\n",
     "     first 8 bytes back into active+0 (op 7, `00581FD9`). So the file carries whatever is live in   <- corrected "
     "2026-10-02, OPUS: op 7 is a write, not a read-back - kind 7 -> 003BB920 (00582149-00582160) arms 02B40E1C = 2 at "
     "003BB98C, the write command; state 8 writes {checksum, 1} into the file\n"),

    # C4: 003BB9B0 is the write submission (kind 8's arm 00582180, autosave 0057E490; 02B40E1C = 2).
    (CSR, "`003BB9B0` (174 B) is the element-array install the read\ncompletion runs once (`[02B40E10]` gates it)",
     "`003BB9B0` (174 B) is ~~the element-array install the read~~\n~~completion runs once~~ the write submission — queue "
     "kind 8's arm (`00582180`) and the autosave's call (`0057E490`) *(corrected 2026-10-02, OPUS: it arms `02B40E1C` = "
     "2, the write command; how-a-manual-save-is-committed.md, kind 8 → `003BB9B0`)* (`[02B40E10]` gates it)"),
    (CSR, "`003BAEB0` (803 B) is the `02B40E14` state pump the completion\ninstall arms:",
     "`003BAEB0` (803 B) is the `02B40E14` state pump ~~the completion~~\n~~install arms~~ the write submissions arm, "
     "the write worker *(corrected 2026-10-02, OPUS: `003BB920` and `003BB9B0` arm `02B40E1C` = 2 and run it)*:"),

    # C5: 008625D0 is the seek (008625D0-008625F0 -> 00866A80, absolute / relative / end-relative, bounds-checked).
    (CSR, "`008625D0` (33 B) is the conditional teardown the `003BA7B0` caller\nruns: `ecx == 0` releases "
          "`[02EAF8E8]` through `00866A80`;",
     "`008625D0` (33 B) is ~~the conditional teardown~~ the seek *(corrected 2026-10-02, OPUS: checked at "
     "`008625D0`–`008625F0`; `00866A80` writes the cursor absolute, relative or from the end and bounds-checks it — the "
     "callee/caller note, \"the sibling **seek**\")* the `003BA7B0` caller\nruns: `ecx == 0` ~~releases~~ repositions "
     "`[02EAF8E8]` through `00866A80`;"),

    # C6: the admit gate and the busy bit are +0xDC bit 0 (00582076 test byte [rcx+0xdc], 1; 005820BD or [rbx+0xdc], 1).
    (CSR, "and `+0xDC` bit 1 is clear (`00582076`), dispatches",
     "and `+0xDC` ~~bit 1~~ bit 0 is clear (`00582076`) *(corrected 2026-10-02, OPUS: `00582076` is `test byte ptr "
     "[rcx + 0xdc], 1`; bit 1 is the completion-callback suppressor)*, dispatches"),
    (CSR, "then sets busy bit 1 and returns 1.",
     "then sets busy ~~bit 1~~ bit 0 *(corrected 2026-10-02, OPUS: `005820BD` `or dword ptr [rbx + 0xdc], 1`)* and "
     "returns 1."),

    # C7: every write-mode close emits a SAFH container (0086623F, 'SAFH' at 008663BD, header fwrite at 008663FB).
    (MS, "A save interrupted anywhere between has a data file whose first 8 bytes are zero, or no data file at all.",
     "A save interrupted anywhere between has a data file whose ~~first 8 bytes are zero~~ decoded image's first 8 bytes "
     "are zero (the file itself opens with the `SAFH` container header) *(corrected 2026-10-02, OPUS: every write-mode "
     "close builds the container — `0086623F`, `'SAFH'` at `008663BD`, the 12-byte header `fwrite` at `008663FB`; "
     "CONTRACT-save-container-transform.md)*, or no data file at all."),
    (MS, "1,195 B) writes the whole vector to a file under `GetTempPathW`",
     "1,195 B) ~~writes the whole vector to a file~~ deflates the whole vector (`compress2`, level 9), RC4-encrypts it "
     "behind a 12-byte `SAFH` header and writes that to a file *(corrected 2026-10-02, OPUS: mode 0 takes the container "
     "path at `0086623F`, `'SAFH'` at `008663BD`, `rand` rotation at `008663C5`–`008663ED`, header `fwrite` at "
     "`008663FB`; CONTRACT-save-container-transform.md)* under `GetTempPathW`"),

    # C8: the finaliser returns the PLAIN CRC (00583F97-00583FA1 keep crc in eax; 00808C40 preserves it; 00581EF8).
    (SI, "by V-4 that dword is the complemented CRC-32 of `+0x0008`..`+0xE200`, so",
     "by V-4 that dword is the ~~complemented~~ plain CRC-32 *(corrected 2026-10-02, OPUS: the finaliser stores `~crc` "
     "at dest `+0` but returns `crc` in `eax`, `00583F97`–`00583FA1`; `00808C40` preserves `eax` and `00581EF8` caches "
     "it; katano-debug-savedata.md, the `+0x00` row)* of `+0x0008`..`+0xE200`, so"),
    (SI, "`+0xD8` is the finaliser's return, the complemented CRC)*",
     "`+0xD8` is the finaliser's return, the ~~complemented~~ plain CRC)* *(corrected 2026-10-02, OPUS: "
     "`00583F97`–`00583FA1` keep `crc` in `eax`; the complement is only the finaliser's own `+0` store, which state 8 "
     "overwrites at `00581FA8`–`00581FBA`)*"),

    # C9: the header's last 320 bytes are zero (002EF5F6-002EF603, 002EF656-002EF663 memset the whole image; boot
    #     frame 0022B6E0 takes 002EF650 before any save).
    (CSB, "depends on it — but no code sets them, so what reaches the save file is whatever the buffer already\nheld.",
     "depends on it — but no code sets them~~, so what reaches the save file is whatever the buffer already~~\n"
     "~~held~~ individually, and both clears zero them with the whole image *(corrected 2026-10-02, OPUS: "
     "`002EF5F6`–`002EF603` and `002EF656`–`002EF663` run `memset(02164280, 0, 0x56690)`, and the boot frame `0022B6E0` "
     "takes `002EF650` before any save; the correction at the head of this section)*."),
    (CSB, "**A\nreimplementation that zeroes them is not reproducing the engine, and one that writes anything into\n"
          "them is inventing data the engine never wrote.**",
     "**~~A~~\n~~reimplementation that zeroes them is not reproducing the engine, and~~ A reimplementation must zero them, "
     "and one that writes anything into\nthem is inventing data the engine never wrote.** *(corrected 2026-10-02, OPUS: "
     "zero is the engine's value, as above)*"),
    (SI, "  +0xC0..+0x1FF   untouched by any enumerated route (320 B)\n",
     "  +0xC0..+0x1FF   untouched by any enumerated route (320 B)   <- corrected 2026-10-02, OPUS: zero - both clears "
     "memset the whole image (002EF5F6-002EF603, 002EF656-002EF663), the boot frame 0022B6E0 first\n"),

    # C10: the roster holds seven entries, +0x20..+0x3B (00583E35-00583E3A, 00583EBE-00583EEB, 00583F0D).
    (SI, "one entry per living party page (N <= 9, written by the\n",
     "one entry per living party page (N <= 9, written by the   <- corrected 2026-10-02, OPUS: seven entries, "
     "+0x20..+0x3B (00583EBE-00583EEB fill 0xFF up to 7; an eighth or ninth page lands on +0x3C, rewritten at "
     "00583F0D; CONTRACT-save-image-buffers.md)\n"),

    # C11: 002EF640 is SaveImage_GetActiveRuntimeBuffer (lea rax, [02164280]; ret), not an enumerator.
    (W, "calls `002EF640` — the slot/file enumerator — on `msg->arg`, stores",
     "calls `002EF640` ~~— the slot/file enumerator — on `msg->arg`~~, the 8-byte `SaveImage_GetActiveRuntimeBuffer` "
     "*(corrected 2026-10-02, OPUS: `002EF640` is `lea rax, [02164280]` / `ret`, checked with `0057FEC5`–`0057FECA`; "
     "this page's own correction further down)*, stores"),

    # C12: 0016D6A0 is ret 0 - no notification happens.
    (SC, "`0016D6A0` is the shared post-set notifier tail every handled arm jumps to\n"
         "(generic UI-dirty broadcast, ~2.4k callers",
     "`0016D6A0` is the shared ~~post-set notifier~~ tail every handled arm jumps to\n"
     "(~~generic UI-dirty broadcast,~~ a bare `ret 0` that notifies nothing *(corrected 2026-10-02, OPUS: `0016D6A0` is "
     "`ret 0`; CONTRACT-save-image-buffers.md — a port must not add a notification)*; ~2.4k callers"),

    # C13: ids {0,7,8,0xA,0xB} default to JAPANESE voices (002DDF24-002DDF6E set dword1 bit 10, 1 = Japanese).
    (SC, "ids {0,7,8,0xA,0xB} select the non-Japanese\n  voice default;",
     "ids {0,7,8,0xA,0xB} select the ~~non-Japanese~~\n  ~~voice default~~ Japanese voice default *(corrected "
     "2026-10-02, OPUS: `002DDF24`–`002DDF6E` set bit 10 of dword1, stored 1 = Japanese, for those ids; §2)*;"),
    (SC, "- the Japanese-voice bit clear for ids 0, 7, 8, 10 and 11.",
     "- the Japanese-voice bit ~~clear~~ set for ids 0, 7, 8, 10 and 11 *(corrected 2026-10-02, OPUS: "
     "`002DDF24`–`002DDF6E`, `ebx = 0x400` for those ids, `or` into dword1)*."),

    # C14: the value-name rows are not NULL-terminated (01DFD150 row 0 uses all nine slots).
    (GI, "value names   0x01DFD150    31 x 9 qword char*, NULL-terminated per row\n",
     "value names   0x01DFD150    31 x 9 qword char*, NULL-terminated per row   <- corrected 2026-10-02, OPUS: not "
     "terminated - row 0 (Language) fills all nine slots, read at 01DFD150; CONTRACT-game-setting-config.md\n"),

    # C15: the ini lives in the Steam-id subfolder, with the doubled separator (0079817E-00798234).
    (GI, "`%DOCUMENTS%\\My Games\\FINAL FANTASY XII THE ZODIAC AGE\\GameSetting.ini`.",
     "~~`%DOCUMENTS%\\My Games\\FINAL FANTASY XII THE ZODIAC AGE\\GameSetting.ini`~~ "
     "`%DOCUMENTS%\\My Games\\FINAL FANTASY XII THE ZODIAC AGE\\<Steam id>\\\\GameSetting.ini` *(corrected 2026-10-02, "
     "OPUS: checked at `0079817E`–`00798234` — `L\"%s%s\\\"` with the Steam-id folder from `001F3ED0`, then "
     "`L\"%s\\%s\"` + `L\"GameSetting.ini\"`; CONTRACT-game-setting-config.md, the per-account path)*."),

    # C16: 0017E070's arms read the GameSettingConfig object (0017E070-0017E108, table 0017E1AC).
    (CGC, "and each arm pulls a field off the settings record `[01F7CD80]` — `+0x18` word, `+0xB0` byte, `+0x68` byte, "
          "`+0x12` byte, `+0x14` byte, `+0x6C` byte — normalising each to `eax`.",
     "and each arm ~~pulls a field off the settings record `[01F7CD80]` — `+0x18` word, `+0xB0` byte, `+0x68` byte, "
     "`+0x12` byte, `+0x14` byte, `+0x6C` byte —~~ loads a field of the GameSettingConfig object `[01F82D20]` (`+0xC`, "
     "`+8`, `+0x10`, `+0x14`, `+0x44`, `+0x48`) or calls the display object's `001DDAB0` *(corrected 2026-10-02, OPUS: "
     "checked at `0017E070`–`0017E108`, the 23-case table at `0017E1AC`; the Config screen's per-row reader, after the "
     "call chain above)*, normalising each to `eax`."),

    # C17: 001DE5A0 returns the shadow-map size (setting[7] mod 3 -> 00900F00 = {512},{1024},{2048}).
    (GI, "It also resolves the resolution path: `FUN_001DE5A0` is called twice",
     "~~It also resolves the resolution path:~~ *(corrected 2026-10-02, OPUS: `001DE5A0` is the shadow-map size from "
     "`Shadow`, not the resolution — `setting[7]` mod 3 indexes `00900F00` = {512,512}, {1024,1024}, {2048,2048}, "
     "checked at `001DE5A0`–`001DE5CD`; the SWE2-EC7-32 note)* `FUN_001DE5A0` is called twice"),

    # C18: 001DFD40 is the file writer (001DFD7A _wfopen_s L"wb" at 00901018, 001DFDE2 fwrite, 001DFDEC fclose).
    (GI, "an IAT-driven buffered read over the entry's `+0x450` source — `call",
     "~~an IAT-driven buffered read over the entry's `+0x450` source~~ the settings file writer *(corrected 2026-10-02, "
     "OPUS: `001DFD7A` opens `+0x450` with `_wfopen_s` mode `L\"wb\"` (`00901018`), `001DFDE2` is `fwrite` and "
     "`001DFDEC` `fclose`; CONTRACT-game-setting-config.md, `001DFD40` = write file)* — `call"),

    # C19: 007A3810 copies object +4, Resolution (007A3847-007A3859).
    (GI, "copies `dword[01F82D20+4]` (the locale id) into each",
     "copies `dword[01F82D20+4]` (~~the locale id~~ `Resolution`, setting 1 *(corrected 2026-10-02, OPUS: "
     "`007A3847`–`007A3859` `mov rax, [01F82D20]` / `mov edx, [rax + 4]`; the key table puts `Resolution` at `+0x04`, "
     "the language at `+0x00`)*) into each"),

    # C20: 00184950 returns the present sync interval (mov eax, [01F3DA18]; ret).
    (FC, "The debug-status getter `00184950` (7 B) is read by",
     "The ~~debug-status getter~~ present-sync-interval getter `00184950` (7 B) *(corrected 2026-10-02, OPUS: "
     "`00184950` is `mov eax, [01F3DA18]` / `ret`; the debug status is `02B62DB9`, getter `00408B00`; "
     "game-settings-ini-and-runtime-config.md `DH-7`)* is read by"),

    # C21: IAT 008C2A08 is VCRUNTIME140!strstr.
    (GI, "probes `GetModuleHandle`-family IAT `008C2A08` for `\"g0111\"`",
     "~~probes `GetModuleHandle`-family IAT `008C2A08`~~ matches an asset name with `strstr` (IAT `008C2A08`) "
     "*(corrected 2026-10-02, OPUS: the import directory names `008C2A08` `VCRUNTIME140!strstr`; §17.3, asset names "
     "matched with `strstr`)* for `\"g0111\"`"),

    # C22 (neither side): 001F3EA0 is _waccess(path, 0), then on -1 _wmkdir(path) - it creates the directory
    #     (001F3EA0-001F3EBE; IAT 008C2B20 = _waccess, 008C2B10 = _wmkdir).
    (WK, "00197F22  call 0x001F3EA0                ; obtain the base path into a buffer\n",
     "00197F22  call 0x001F3EA0                ; obtain the base path into a buffer   <- corrected 2026-10-02, OPUS: "
     "001F3EA0 obtains nothing; it is _waccess(path, 0) then, on -1, _wmkdir(path) - it creates the directory when "
     "missing (001F3EA0-001F3EBE; IAT 008C2B20 / 008C2B10); the base path comes from SHGetFolderPathW\n"),
    (WK, "what `001F3EA0` returns as a base path, what the file names are\nbeyond the keymap's first characters, "
         "whether the directory is created or only read, or",
     "~~what `001F3EA0` returns as a base path,~~ what the file names are\nbeyond the keymap's first characters, "
     "~~whether the directory is created or only read,~~ *(answered: `001F3EA0` returns no path; it runs "
     "`_waccess(path, 0)` and, on `-1`, `_wmkdir(path)`, so the directory is created when missing — checked at "
     "`001F3EA0`–`001F3EBE`; 2026-10-02, OPUS)* or"),
    (GI, "tails into `qword [008C2B10]`\n(the failure/handler IAT slot),",
     "tails into `qword [008C2B10]`\n(~~the failure/handler IAT slot~~ `_wmkdir`; `008C2B20` is `_waccess` *(corrected "
     "2026-10-02, OPUS: the import directory names both; `001F3EA0` creates the directory when `_waccess(path, 0)` "
     "fails, checked at `001F3EA0`–`001F3EBE`)*),"),

    # C23 (neither side): the SpawnKeep copy is 0x128 passes of 0x80 = 0x9400 bytes per 0x10000 bank
    #     (00233560 mov r8d, 0x128; serializer 00233448 / 0023345D).
    (CSR, "and it gives the bank a width: **`0x128` bytes** are copied",
     "and it gives the bank a width: ~~**`0x128` bytes**~~ **`0x9400` bytes** (`0x128` passes of `0x80`) *(corrected "
     "2026-10-02, OPUS: `00233560` `mov r8d, 0x128` counts passes; the serializer `00233448` / `0023345D` copies the "
     "same)* are copied"),
    (PM, "| bank 2 of image A (0x10000) | 1 / 2 |",
     "| bank 2 of image A (~~0x10000~~ a `0x10000` slot holding `0x9400` copied bytes and a `0x6C00` zero tail "
     "*(corrected 2026-10-02, OPUS: `00233448`, `0023345D`, `00233560` — `0x128` passes of `0x80`)*) | 1 / 2 |"),
    (PM, "| bank 1 of image A (0x10000) | 1 / 1 |",
     "| bank 1 of image A (~~0x10000~~ a `0x10000` slot holding `0x9400` copied bytes and a `0x6C00` zero tail "
     "*(corrected 2026-10-02, OPUS: `00233448`, `0023345D` — `0x128` passes of `0x80`)*) | 1 / 1 |"),

    # C24: the stash copies five dwords (0058427B-005842B1, 00584325-00584362).
    (CSR, "`rbx+0x1244..0x1254` (six\n  dwords) to",
     "`rbx+0x1244..0x1254` (~~six~~ five *(corrected 2026-10-02, OPUS: `0058427B`–`005842B1` and "
     "`00584325`–`00584362` copy five; the save-image page's header map, `+0x80 5 dwords`)*\n  dwords) to"),

    # C25: kinds 2, 3 and 4 name static.ico (0058383C-0058384E).
    (CSR, "kinds 2/3 → `\"static.ico\"`",
     "~~kinds 2/3~~ kinds 2, 3 and 4 *(corrected 2026-10-02, OPUS: checked at `0058383C`–`0058384E`)* → "
     "`\"static.ico\"`"),

    # C26: +0x3244 is zero after init (00253B1C keeps bit 0, then 00253B47-00253B56 memset(+0x3244, 0, 0x80)).
    (PM, "bit 0 kept, bit 1 cleared at init | 3 / 2 |",
     "~~bit 0 kept, bit 1 cleared at init~~ zero after init *(corrected 2026-10-02, OPUS: `00253B1C` keeps bit 0, but "
     "`00253B47`–`00253B56` then zero `+0x3244` for `0x80` bytes; katano-debug-savedata.md)* | 3 / 2 |"),

    # C27: 00686DE0 and its family are the D3D11 texture path; the save file is written by the storage machine.
    (CSB, "`00686DE0` (3,463 B) is the save-image serializer - 6",
     "`00686DE0` (3,463 B) is ~~the save-image serializer~~ a D3D11 texture-path body, not a save-image serializer "
     "*(corrected 2026-10-02, OPUS: the four buffers' only rip references are the `002EF4A0`–`002EF7C0` bodies, SV-4, "
     "and no `006xxxxx` body calls a buffer getter; the save file is written by the storage machine, `003BAEB0` → "
     "`00862620` / `00866AD0` → `00866200`)* - 6"),
    (CSB, "`00607FA0` — the save-image write family.",
     "`00607FA0` — ~~the save-image write family~~ the D3D11 texture path *(corrected 2026-10-02, OPUS: none of these "
     "bodies references a save buffer; the rows are `Texture2DD3D11Element` records, the section below)*."),
    (CSB, "the save image is captured through the renderer's own graphics-device\nlayer.** The save-image write family "
          "this page names shares its helpers with the renderer:",
     "~~the save image is captured through the renderer's own graphics-device~~\n~~layer.~~** *(corrected 2026-10-02, "
     "OPUS: these bodies are the D3D11 texture path, not a save-image route — the save image is written by the storage "
     "machine)* ~~The save-image write family this page names~~ The texture-path family shares its helpers with the "
     "renderer:"),

    # C28: 001DF340 has 38 call / jmp sites in 15 functions (retool.py callers 001DF340).
    (CGC, "`001DF340` has\n  roughly twenty-five callers across the `0079xxxx` settings-load band.",
     "`001DF340` has\n  ~~roughly twenty-five callers across the `0079xxxx` settings-load band~~ 38 call sites in 15 "
     "functions *(corrected 2026-10-02, OPUS: `retool.py callers 001DF340`; language-selection-and-locale-ids.md "
     "AV-3 counts the same 38)*."),
    (GI, "enumerating all 36 call sites of the generic setter",
     "enumerating all ~~36~~ 38 *(corrected 2026-10-02, OPUS: `retool.py callers 001DF340`, 38 call sites in 15 "
     "functions)* call sites of the generic setter"),

    # C29: the published TSVs hold 1,725 / 350 / 301 (payload) and 199 / 25 / 40 (header).
    (PM, "It reaches 368 functions and\n> 309 offsets, places",
     "It reaches ~~368 functions and~~\n> ~~309 offsets~~ 350 functions and 301 offsets in the published "
     "`save-payload-accesses.tsv` *(corrected 2026-10-02, OPUS: counted in the TSV, 1,725 rows)*, places"),
    (PM, "| payload access rows | 1829 (976 at a seed, 853 through propagation) |",
     "| payload access rows | ~~1829 (976 at a seed, 853 through propagation)~~ 1,725 in the published TSV "
     "*(corrected 2026-10-02, OPUS: counted in `save-payload-accesses.tsv`; the reserved-span check below cites the same 1,725)* |"),
    (PM, "| payload functions / offsets | 368 / 309 |",
     "| payload functions / offsets | ~~368 / 309~~ 350 / 301 *(corrected 2026-10-02, OPUS: distinct functions and "
     "displacements in `save-payload-accesses.tsv`)* |"),
    (PM, "| header access rows / functions / offsets | 204 / 26 / 40 |",
     "| header access rows / functions / offsets | ~~204 / 26 / 40~~ 199 / 25 / 40 *(corrected 2026-10-02, OPUS: "
     "counted in `save-header-accesses.tsv`)* |"),

    # C30 (neither side): retool.py refs 01F82D20 - 158 reads and 1 write in 63 functions; one writer holds.
    (CGC, "all **60** that load `*(0x01F82D20)`, plus",
     "all ~~**60**~~ that load `*(0x01F82D20)` — 63 functions with 158 reads and 1 write by `retool.py refs "
     "01F82D20` *(corrected 2026-10-02, OPUS: no page figure matches the image)* — plus"),
    (CGC, "→ **1 writer, 61 readers** (RIP-relative instrument).",
     "→ **1 writer, ~~61 readers~~** 63 functions referencing it, 158 reads and 1 write *(corrected 2026-10-02, "
     "OPUS: `retool.py refs 01F82D20`)* (RIP-relative instrument)."),
    (CGC, "| readers | **156 references across 61 distinct functions** |",
     "| readers | ~~**156 references across 61 distinct functions**~~ **158 reads in 63 functions** *(corrected "
     "2026-10-02, OPUS: `retool.py refs 01F82D20`, beside the one write)* |"),
    (GI, "finds **157 instructions referencing `0x01F82D20`: 156 reads and\nexactly one write**",
     "finds **~~157~~ 159 instructions referencing `0x01F82D20`: ~~156~~ 158 reads and\nexactly one write** "
     "*(corrected 2026-10-02, OPUS: `retool.py refs 01F82D20`, in 63 functions)*"),
    (LL, "a shared runtime object — around 150 instructions across",
     "a shared runtime object — ~~around 150 instructions~~ 159 instructions (158 reads, 1 write, 63 functions) "
     "*(corrected 2026-10-02, OPUS: `retool.py refs 01F82D20`)* across"),

    # C31: AX-6a answered - the graphics apply runs on a left/right press on a Config row (C-GC, GI "Resolved").
    (CGC, "whose firing time is **UNRESOLVED** (`AX-6a`).",
     "whose firing time is ~~**UNRESOLVED**~~ a left/right press on a Config-screen row *(answered: see \"The trigger "
     "for the whole graphics-apply chain is now established\", after the call chain; 2026-10-02, OPUS)* (`AX-6a`)."),
    (CGC, "5. When the graphics callback fires, hence whether §10's mismatch is observable (`AX-6a`).",
     "5. ~~When the graphics callback fires, hence whether §10's mismatch is observable (`AX-6a`).~~ *(answered: on a "
     "left/right press on a Config row, so §10's mismatch stands until the player moves `Quality`; `AX-6a`, "
     "game-settings-ini-and-runtime-config.md \"Resolved 2026-09-08\"; 2026-10-02, OPUS)*"),
    (CGC, "untested**, and `AX-6a` — when the graphics-apply\ncallback fires — remains the open question that would make "
          "`INTEGRATION` testable at all.",
     "untested**~~, and `AX-6a` — when the graphics-apply~~\n~~callback fires — remains the open question that would "
     "make `INTEGRATION` testable at all.~~ *(answered: `AX-6a` is answered — the apply runs on a left/right press on a "
     "Config row; 2026-10-02, OPUS)*."),
    (GI, "**Whether anything applies a preset at startup is\nnot shown here**",
     "**~~Whether anything applies a preset at startup is~~\n~~not shown here~~** *(answered: nothing does — `AX-6` "
     "answered NO, \"Resolved 2026-09-08\" below; 2026-10-02, OPUS)*"),
    (GI, "**Not established, and not establishable from the call graph:** *when* that runs. The chain terminates",
     "**~~Not established, and not establishable from the call graph:~~** ~~*when* that runs.~~ *(answered: a "
     "left/right press on a Config row — \"Resolved 2026-09-08\" below; `AX-6a` answered; 2026-10-02, OPUS)* The chain "
     "terminates"),

    # C32: AX-2 is 22 of 31 (GI, the Config screen page section 11).
    (CGC, "6. Which of the 31 the options UI exposes versus ini-only (`AX-2`).",
     "6. ~~Which of the 31 the options UI exposes versus ini-only (`AX-2`).~~ *(answered: 22 of 31 — "
     "game-settings-ini-and-runtime-config.md `AX-2` and the Config screen page §11; 2026-10-02, OPUS)*"),
    (GI, "**ANSWERED — 16 of\n      31.** Full split",
     "**ANSWERED — ~~16 of~~\n      ~~31.~~** 22 of 31 *(corrected 2026-10-02, OPUS: the correction this list records "
     "under AX-3, the Config screen page §11)*. Full split"),

    # C33: AX-4 answered (section 9), AX-5 answered (the AX-5 box).
    (GI, "Which index each arm selects is not read\nhere. **AX-4.**",
     "~~Which index each arm selects is not read~~\n~~here.~~ *(answered: see §9, \"AX-4 answered — the whole locale "
     "mapping\"; 2026-10-02, OPUS)* **AX-4.**"),
    (GI, "all set before the defaults copy, all unidentified. **AX-5.**",
     "all set before the defaults copy~~, all unidentified~~ *(answered: see the AX-5 box above — `+0x44C` is the MSAA "
     "availability mask, `+0x658` / `+0x65A` fresh-defaults markers; 2026-10-02, OPUS)*. **AX-5.**"),

    # C34: DH-3, DH-4 and the shipped FrameLimit answered (17.2, 17.3, the fresh-install section).
    (GI, "**What those thirteen do\n> is not read here**",
     "**~~What those thirteen do~~\n> ~~is not read here~~** *(answered: see §17.3, `DH-3` — four accessors and nine "
     "content exceptions; 2026-10-02, OPUS)*"),
    (GI, "**that is a tag, a prior session's claim, not\na reading**; none of the seven has been disassembled here.",
     "**that is a tag, a prior session's claim, not\na reading**~~; none of the seven has been disassembled here~~ "
     "*(answered: see §17.2, `DH-4` — they convert authored presentation timing tables at boot; 2026-10-02, OPUS)*."),
    (GI, "**only when no\n> file exists**, and this document has not examined an installed `GameSetting.ini` or the "
         "launcher.",
     "**only when no\n> file exists**~~, and this document has not examined an installed `GameSetting.ini` or the "
     "launcher~~ *(answered: see \"What a fresh install writes for `FrameLimit` — 30\"; 2026-10-02, OPUS)*."),
    (GI, "| What the thirteen `01F82E38` readers do | **not read** | — |",
     "| What the thirteen `01F82E38` readers do | ~~**not read**~~ read, §17.3 *(answered: `DH-3`; 2026-10-02, OPUS)* "
     "| — |"),
    (GI, "| What `0033F020`'s seven targets do | **not read** | — |",
     "| What `0033F020`'s seven targets do | ~~**not read**~~ read, §17.2 *(answered: `DH-4`; 2026-10-02, OPUS)* | — |"),
    (GI, "| What a shipped `GameSetting.ini` contains | **not examined** | — |",
     "| What a shipped `GameSetting.ini` contains | ~~**not examined**~~ none ships; both writers default `FrameLimit` "
     "to 30 *(answered: \"What a fresh install writes for `FrameLimit`\"; 2026-10-02, OPUS)* | — |"),

    # C35: the language page's own open list (answered under Open questions and section 10).
    (LL, "| `0017E260` | `+0x58` | 9 callers, unidentified |",
     "| `0017E260` | `+0x58` | 9 callers, ~~unidentified~~ `CameraRevise`, index 22 *(answered: see §10 and AV-2; "
     "2026-10-02, OPUS)* |"),
    (LL, "- What occupied ids `0`, `6` and `9`. **AV-1.**",
     "- ~~What occupied ids `0`, `6` and `9`.~~ *(answered: see Open questions, AV-1 closed 2026-09-12; 2026-10-02, "
     "OPUS)* **AV-1.**"),
    (LL, "- What the object at `0x01F82D20` is as a whole — three fields are identified out of an unknown\n"
         "  total. **AU-6.**",
     "- ~~What the object at `0x01F82D20` is as a whole — three fields are identified out of an unknown~~\n"
     "  ~~total.~~ *(answered: see §10 — the GameSetting.ini object, 31 settings at index × 4; 2026-10-02, OPUS)* "
     "**AU-6.**"),
    (LL, "- What `+0x58` holds. **AV-2.**",
     "- ~~What `+0x58` holds.~~ *(answered: `CameraRevise`, §10; 2026-10-02, OPUS)* **AV-2.**"),
    (LL, "- Where the language index is written from — the settings file, a launcher, or a platform query.\n"
         "  The same argument-passing blind spot that hides the `+0x64` writer applies. **AV-3.**",
     "- ~~Where the language index is written from — the settings file, a launcher, or a platform query.~~\n"
     "  ~~The same argument-passing blind spot that hides the `+0x64` writer applies.~~ *(answered: see Open "
     "questions, AV-3 — the OS, then the settings file, then Steam, which wins; 2026-10-02, OPUS)* **AV-3.**"),
    (LL, "or both. No consumer of `0017E270`'s\n  return value is read here. **AV-4.**",
     "or both. ~~No consumer of `0017E270`'s~~\n  ~~return value is read here.~~ *(answered: `0022A0B0` caches it at "
     "`0x01E02814`, §6 and AV-4 under Open questions; 2026-10-02, OPUS)* **AV-4.**"),

    # C36: AU-5 answered - +0x64 is DecideButton, written by 0017E6E0 via 001DF340(cfg, 0x19), command 0x26.
    (LL, "- What writes `+0x64` — still **AU-5**, and still the question that decides whether a player can\n"
         "  change this.",
     "- ~~What writes `+0x64` — still **AU-5**, and still the question that decides whether a player can~~\n"
     "  ~~change this.~~ *(answered: `+0x64` is `DecideButton`, written by `0017E6E0` through `001DF340(cfg, 0x19)`, so "
     "the player can change it — §4's AU-5 note and game-settings-ini-and-runtime-config.md; 2026-10-02, OPUS)*"),
    (LL, "(**AU-5**, still open).",
     "(**AU-5**~~, still open~~ *(answered: `DecideButton`, written by `0017E6E0` through `001DF340(cfg, 0x19)`; "
     "2026-10-02, OPUS)*)."),
    (LL, "Whether a menu\nactually calls it is not shown here; the function's existence and shape are.",
     "~~Whether a menu~~\n~~actually calls it is not shown here;~~ *(answered: settings command `0x26` does — "
     "`0017E6E0` tail-jumps to `0022A4F0`, game-settings-ini-and-runtime-config.md; 2026-10-02, OPUS)* the function's "
     "existence and shape are."),

    # C37: AV-9 closed 2026-09-12.
    (LL, "- What sound ids `2` and `3` are named. **AV-9.**",
     "- ~~What sound ids `2` and `3` are named.~~ *(answered: see Open questions, AV-9 closed 2026-09-12 — the names "
     "are not in the image or the data, the roles are; 2026-10-02, OPUS)* **AV-9.**"),

    # C38: FF12CONFIG is read from the archive (PC-1, 2026-09-27); the gated bodies read (PC-2, 2026-09-14).
    (FC, "`002DDA30` with 1, and whether `001D6F20` reads the archive entry or a loose file) is untouched by it.",
     "`002DDA30` with 1~~, and whether `001D6F20` reads the archive entry or a loose file~~ *(answered: the archive — "
     "see `PC-1`, answered 2026-09-27; 2026-10-02, OPUS)*) is untouched by it."),
    (FC, "whether `001D6F20`\nreads the archive entry or a loose file, and whether",
     "~~whether `001D6F20`~~\n~~reads the archive entry or a loose file,~~ *(answered: the archive, `PC-1` "
     "2026-09-27; 2026-10-02, OPUS)* and whether"),
    (FC, "What `0035FCA0` and `0035FF90` would do if the flag were 1 — **their bodies were not\nread past the gate.**",
     "~~What `0035FCA0` and `0035FF90` would do if the flag were 1 —~~ **~~their bodies were not~~\n~~read past the "
     "gate.~~** *(answered: flag 1 updates both registered input channels — `PC-2`, 2026-09-14; 2026-10-02, OPUS)*"),
    (FC, "unreachable in this build and were not\n      read past their gate. `PC-2`",
     "unreachable in this build ~~and were not~~\n      ~~read past their gate~~ *(answered: read since — the "
     "2026-09-14 note directly below; 2026-10-02, OPUS)*. `PC-2`"),

    # C39: the backup writer has a caller (thunk 00584490 <- 0027F974).
    (CSB, "written by one function nothing calls and read by nothing (`V-6`) |",
     "written by one function ~~nothing calls~~ called through the thunk `00584490` at `0027F974` on load-mode opens "
     "*(answered: see §10 item 3, THE WRITER HAS A CALLER; 2026-10-02, OPUS)* and read by nothing (`V-6`) |"),

    # C40: the backup runs on load-mode opens (0027F8DB-0027F984).
    (CSB, "but the write runs on every save — a reimplementation",
     "but the write runs on ~~every save~~ every load-mode open *(corrected 2026-10-02, OPUS: §10 item 3's correction "
     "of 2026-09-23 — `0027F8DB`–`0027F984`, the arm that opens the controller in load mode)* — a reimplementation"),

    # C42: SV-5 resolved 2026-09-23 (section 14).
    (CSP, "which of the two clears a caller takes is SV-5's open question, and that caller",
     "~~which of the two clears a caller takes is SV-5's open question,~~ *(answered: see §14 — resolved 2026-09-23, "
     "this caller `0022B6E0` takes the compound clear `002EF650`; 2026-10-02, OPUS)* and that caller"),

    # C43: the container round trip was executed (EXP-088, 46/46).
    (CCT, "- **The codec/file round trip**, caller allocation preconditions",
     "- ~~**The codec/file round trip**,~~ *(answered: executed in EXP-088, 46/46 cases — §13's correction of "
     "2026-09-16; 2026-10-02, OPUS)* Caller allocation preconditions"),
    (CCT, "No differential harness exists for this contract — §13 is honest that nothing has been executed.",
     "No differential harness exists for this contract~~ — §13 is honest that nothing has been executed~~ *(answered: "
     "see §13's correction of 2026-09-16 — EXP-088 executed five bodies, 46/46 cases; 2026-10-02, OPUS)*."),

    # C44: 00580CD0 closes the popup and copies the new header record (the same line's first half).
    (W, "**`0xF` → `00580CD0`** destroys the pane, re-enumerates the slots through `SaveImage_GetActiveRuntimeBuffer`, "
        "re-binds",
     "**`0xF` → `00580CD0`** ~~destroys the pane, re-enumerates the slots through `SaveImage_GetActiveRuntimeBuffer`~~ "
     "closes the popup and copies the new `0xA0`-byte header record out of the active image *(answered: as struck in "
     "this line's first half, and `002EF640` is not an enumerator, corrected below; 2026-10-02, OPUS)*, re-binds"),

    # C45: 0x40 is the name buffer's size, the slot is r9b = 0.
    (SI, "       -> slot asset name (index 0x40) -> rec +0xD0; rec +0xF8 = submission, +0x100 = 0x56690\n",
     "       -> slot asset name (index 0x40) -> rec +0xD0; rec +0xF8 = submission, +0x100 = 0x56690   <- corrected "
     "2026-10-02, OPUS: 0x40 is the name buffer's size and the slot is r9b = 0 (the autosave note in section 4)\n"),

    # C46: the battle-state copy is 0x6000 bytes; the group banks are 0x200.
    (PM, "Its first 0x80 bytes are what the capture functions mirror to `+0x2000` |",
     "Its first ~~0x80~~ `0x6000` bytes *(corrected 2026-10-02, OPUS: the capture copies `0x6000`, "
     "`00229B76`–`00229BE2`; this map's `+0x2000` row)* are what the capture functions mirror to `+0x2000` |"),
    (PM, "each preceded by a 128-byte\n  group bank",
     "each preceded by a ~~128-byte~~ 512-byte *(corrected 2026-10-02, OPUS: `0x200` B, this page's bank rows, "
     "corrected 2026-09-11)*\n  group bank"),

    # C47: the component census proves exactly two builders (the table below).
    (WK, "this pair census found two — it does not\nprove there are only two.**",
     "this pair census found two ~~— it does not~~\n~~prove there are only two.~~** *(answered: the component census "
     "below proves exactly two — four references from two functions; 2026-10-02, OPUS)*"),

    # C48: all three generations carry the party-stats array (section 7, SV-1, 2026-09-27).
    (KS, "checksum (§6). What follows the header is still undecoded.",
     "checksum (§6)~~. What follows the header is still undecoded~~ *(answered: see §7 `SV-1`, narrowed 2026-09-27 — "
     "all three generations carry the 40-record party-stats array; 2026-10-02, OPUS)*."),
    (KS, "The\npayload past the header is still undecoded in both, and generation C — zero through `+0x6C`, first\n"
         "non-zero byte at `+0x901` — is undecoded entirely.",
     "~~The~~\n~~payload past the header is still undecoded in both, and generation C — zero through `+0x6C`, first~~\n"
     "~~non-zero byte at `+0x901` — is undecoded entirely.~~ *(answered: see §7 `SV-1` — all three generations carry "
     "the 40-record party-stats array, generation C at image `+0x15FC`; 2026-10-02, OPUS)*"),

    # C49: Subtitles' getter reads other storage only while 0215E6DC is non-zero (CON-194).
    (SC, "**Subtitles** — the only command whose setter and getter touch *different* storage: setter",
     "**Subtitles** — ~~the only command whose setter and getter touch *different* storage~~ the command whose getter "
     "reads other storage only while `0215E6DC` is non-zero *(answered: see the falsification table, C4, CON-194; "
     "2026-10-02, OPUS)*: setter"),

    # C50: README labels against each page's own front matter, and the twelve pages it did not list.
    (R, "  **DOCUMENTED, tier 1.** The save-slot transaction",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The save-slot transaction"),
    (R, "  **PARTIAL, tier 1.** A save is",
     "  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: DOCUMENTED`)*. A save is"),
    (R, "  **DOCUMENTED, tier 1.** The payload region",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The payload region"),
    (R, "  **DOCUMENTED, tier 1.** The two archive entries",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The two archive entries"),
    (R, "  four development-network addresses nothing refers to.\n\n## How to add a system here",
     "  four development-network addresses nothing refers to.\n\n"
     "- [`where-the-game-keeps-your-files.md`](where-the-game-keeps-your-files.md) — the per-user directory and its two "
     "path builders — **AUDITED**\n"
     "- [`the-save-load-screen-widgets.md`](the-save-load-screen-widgets.md) — the slot screen, the write spinner and "
     "the controller's fifteen states — **DOCUMENTED**\n"
     "- [`CONTRACT-save-image-pipeline.md`](CONTRACT-save-image-pipeline.md) — **CONTRACT READY**\n"
     "- [`CONTRACT-save-image-buffers.md`](CONTRACT-save-image-buffers.md) — **BEHAVIORALLY UNDERSTOOD**\n"
     "- [`CONTRACT-save-container-transform.md`](CONTRACT-save-container-transform.md) — "
     "**BEHAVIORALLY UNDERSTOOD**\n"
     "- [`CONTRACT-storage-read-completion.md`](CONTRACT-storage-read-completion.md) — **DIFFERENTIAL TESTED**\n"
     "- [`Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md`]"
     "(Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md) — the two stamps and the load "
     "normaliser — **DOCUMENTED**\n"
     "- [`Save-Image-Layout-And-Pipeline/katano-debug-savedata.md`]"
     "(Save-Image-Layout-And-Pipeline/katano-debug-savedata.md) — the sixteen shipped development saves — "
     "**AUDITED**\n"
     "- [`Game-Settings-Config/CONTRACT-game-setting-config.md`](Game-Settings-Config/CONTRACT-game-setting-config.md) "
     "— **RUNTIME VALIDATED**\n"
     "- [`Game-Settings-Config/game-settings-ini-and-runtime-config.md`]"
     "(Game-Settings-Config/game-settings-ini-and-runtime-config.md) — `GameSetting.ini`, its 31 settings and the "
     "frame-rate switch — **AUDITED**\n"
     "- [`Game-Settings-Config/the-settings-command-table.md`](Game-Settings-Config/the-settings-command-table.md) — "
     "the in-save options record and its command dispatch — **AUDITED**\n"
     "- [`Language-And-Locale/language-selection-and-locale-ids.md`]"
     "(Language-And-Locale/language-selection-and-locale-ids.md) — language ids and the confirm-button convention — "
     "**AUDITED**\n"
     "- *(corrected 2026-10-02, OPUS: twelve pages this list omitted, added with the status each page's own front "
     "matter states)*\n"
     "\n## How to add a system here"),

    # C51: in-body PARTIAL banners against each page's front matter.
    (SI, "**PARTIAL.** The buffer layout, sizes,",
     "~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, every "
     "register row closed 2026-09-30)* The buffer layout, sizes,"),
    (VS, "**PARTIAL.** *(DOCUMENTED since 2026-09-30",
     "~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`)* "
     "*(DOCUMENTED since 2026-09-30"),
    (W, "**Status:** PARTIAL — the seven atlas rows",
     "**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, "
     "GI-13 answered 2026-09-29)* — the seven atlas rows"),
    (W, "**Not attacked**, and still `PARTIAL` for the reasons the page gives: `0057FE80`'s",
     "**Not attacked**~~, and still `PARTIAL` for the reasons the page gives~~ *(answered: the three reasons are "
     "closed — the arms read at dispatch level and the `00583FD0` child confirmed 2026-09-18, the storage-result values "
     "named 2026-09-29, GI-13; the front matter says `DOCUMENTED`; 2026-10-02, OPUS)*: `0057FE80`'s"),

    # C52: the settings contract's readiness is RUNTIME VALIDATED (front matter, EXP-001, section 13).
    (CGC, "`readiness` stays **`CONTRACT READY`**, because promoting the whole\nsubsystem on the strength of its "
          "smallest operation is exactly the overstatement the readiness ladder\nexists to prevent.",
     "~~`readiness` stays **`CONTRACT READY`**, because promoting the whole~~\n~~subsystem on the strength of its "
     "smallest operation is exactly the overstatement the readiness ladder~~\n~~exists to prevent.~~ *(corrected "
     "2026-10-02, OPUS: the front matter says `readiness: RUNTIME VALIDATED   # EXP-001`, on §13's controlled A/B, not "
     "on this one differential-tested operation)*"),
    (CGC, "| any runtime observation | **none exists** | none | UNKNOWN |",
     "| any runtime observation | ~~**none exists**~~ `EXP-001`, a controlled A/B run 2026-09-08 (§13) *(corrected "
     "2026-10-02, OPUS: the front matter says `RUNTIME VALIDATED # EXP-001`)* | ~~none~~ runtime | ~~UNKNOWN~~ "
     "PROVEN |"),

    # X2: generation B carries no header constants - +0x58..+0x6C are zero in the shipped B images (vbf_read_entry).
    (KS, "generations differ in their **first eight bytes only**, tag and version",
     "generations differ in their **first eight bytes ~~only~~** and in `+0x58`–`+0x6C`, which are zero in "
     "generation B where generation A carries its six constants *(corrected 2026-10-02, OPUS: read through "
     "`vbf_read_entry` from `FFXII_TZA.vbf`)*, tag and version"),
    (KS, "differ in their first eight bytes and nothing else that is decoded**: the",
     "differ in their first eight bytes ~~and nothing else that is decoded~~** and in the header constants "
     "`+0x58`–`+0x6C`, all zero in generation B *(corrected 2026-10-02, OPUS: read through `vbf_read_entry`; generation "
     "A carries `20050223` / `00001538` / `05071901` / `00005A70` / `0131F3EA` / `00004818`)*: the"),
    (KS, "generation B's header *is* generation A's from\n      `+0x08` on (§6),",
     "generation B's header ~~*is* generation A's from~~\n      ~~`+0x08` on (§6)~~ follows generation A's map from "
     "`+0x08` on (§6) but carries none of its constants at `+0x58`–`+0x6C` *(corrected 2026-10-02, OPUS: zero in the "
     "shipped generation-B images, read through `vbf_read_entry`)*,"),

    # X3: header +0x44 is the clan rank and +0x40 is written when 0032A8A0(0x400B) != 0 (00583F03-00583F32);
    #     +0x57 bit 1 comes from 00236740() (00583F74-00583F7D).
    (SI, "  +0x44   dword   [0x11]  written as 0\n",
     "  +0x44   dword   [0x11]  written as 0   <- corrected 2026-10-02, OPUS: zeroed, then, when 0032A8A0(0x400B) is "
     "non-zero, the clan rank (u8)00315390() is stored here and 003166F0(0x11) at +0x40 (00583F03-00583F32)\n"),
    (SI, "                         bit 2 from block +4 bit 14 (00583F70)\n",
     "                         bit 2 from block +4 bit 14 (00583F70)   <- corrected 2026-10-02, OPUS: bit 1 is set "
     "too, from 00236740() (00583F74-00583F7D)\n"),

    # X4: not every 01F82E38 read is a cmp - 001EDE70 reads it with mov eax, [01F82E38] (retool.py refs: 13 / 1).
    (GI, "and thirteen reads, every one of them `cmp dword ptr [...], 0`**, in thirteen",
     "and thirteen reads, ~~every one of them `cmp dword ptr [...], 0`~~ not all of them `cmp` — `001EDE70` reads it "
     "with `mov eax, [01F82E38]`** *(corrected 2026-10-02, OPUS: `retool.py refs 01F82E38`, 13 reads and 1 write; the "
     "list below omits `001EDE70`)*, in thirteen"),
    (GI, "001EDBD0  001EDCD6  001EDDA9  001EDE84  001EDEC0      (+ the write at 001EDDE8)\n",
     "001EDBD0  001EDCD6  001EDDA9  001EDE84  001EDEC0      (+ the write at 001EDDE8)   <- corrected 2026-10-02, "
     "OPUS: the read in 001EDE70 (mov eax, [01F82E38]) is missing from this list\n"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
