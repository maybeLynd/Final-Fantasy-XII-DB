# Loose files, size tables, and the override path

**Not archive entries.** These ship loose in the install directory, so the archive census cannot see
them. They are declared with `container_format:` — **counted, not scored**, because the population
is a handful of files and inventing a percentage over it would be worse than the plain count.

## `FileSizeTables/*.fst`

**Twelve files, exactly 820,000 bytes each** — 205,000 dwords. First dword `0x39`, then long runs of
`0xFFFFFFFF`; no zero dwords observed. **Ten distinct contents across twelve language files**, so
two pairs are byte-identical.

> **Why this matters beyond completeness:** a file-size table is precisely what a loose-file override
> loader must satisfy. This install runs the External File Loader (present as `dinput8.dll.modbak`),
> which makes the `.fst` path load-bearing for the mod scene and completely undocumented.

~~Questions a sheet must answer: what the 205,000 slots are indexed **by**; whether `0xFFFFFFFF` means
*absent* or *unbounded*; and **whether the retail engine reads these at all**, or only an override
DLL does — which would make the whole family inert in a stock install.~~ **Answered by
[the sheet](file-size-tables-fst.md) (2026-09-11):** the slots are `size[kind][id]` for the 41
resource kinds by 5,000 path-array positions; `0xFFFFFFFF` means *absent* — the read issuer refuses
it; and the retail engine reads the table at every boot (`ResourcePath_Init`) and sizes every
request from it.

## Loose configuration

| file | state |
|---|---|
| `ConfigData/keymap.ini` | not documented |
| `ConfigData/GaussianFilter/GaussianFilterSetting.ini` | not documented |
| `SettingsLoc.xml` | not documented — 16.7 KB, plain readable XML, all languages |

`GameSetting.ini` itself **is** documented, from the reader side only. Its *writer* is a separate
managed .NET program — see
[19-Save-Load-Settings/Game-Settings-Config](../../19-Save-Load-Settings/Game-Settings-Config/).

Write sheets to `_templates/FORMAT.md`. See
[_index/ASSET-FORMATS.md](../../_index/ASSET-FORMATS.md) §6.
