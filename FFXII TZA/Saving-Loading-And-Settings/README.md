# Saving, loading and settings

Save files, loading, the game options and language selection.

| Page | What you will find |
|---|---|
| [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md) | How the game picks its language: the Language setting in the GameSetting.ini object, its ten-entry code table, the converter that turns a code into the locale id the rest of the game reads, the per-locale data folder and file size table that id selects, the Windows language the setting defaults to on a fresh install, the locale-dependent rules in text and script code, and the DecideButton setting that swaps confirm and cancel. |
| [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md) | What a FFXII_000 save file is from the outside in: the 12-byte SAFH container header, the body that is zlib-compressed and then RC4-encrypted under a key derived from the rotated game title, the 353,936-byte image inside it with its 512-byte header (checksum, gil, play time, slot roster, area, format constants) and payload, the four image buffers the game keeps in memory, the checksum the writer computes, the stamps the loader checks, and what loading an older or edited image does. |
