---
title: "Prefetch and asset-header manifests: the text lists that preload files into the file cache, and the .ah lists that name the parts of a model, map or font"
kind: "format"
category: "Game files and data tables"
summary: "The plain-text manifests the game reads by whitespace-separated tokens: the prefetch lists (common.txt at start-up, one per map on map entry, one per event, eventList.csv's event schedule, the add-on folder) and the background thread that opens their names into the RAM file cache under protected stamps; and the .ah asset-header lists that name, in order, the .phyre files of every model, map, font and procedural texture set and load each of them. Includes the shipped counts and the rules both formats impose."
addresses: ["001DA0F0", "008F4438", "0018A330", "001DA610", "001DA290", "001D9FD0", "001D9A40", "001D9EC0", "001D9DA0", "001DA9E0", "001DA090", "0020C1A0", "001DAAC0", "001DADC0", "009005E8", "0019EB60", "0019E7B0", "0019EF20", "001A0BB0", "001A07B0", "001A0F80", "001A7A50", "001B44A0", "001BB2B0", "001BE730", "0020C300"]
---

# Prefetch and asset-header manifests: the text lists that preload files into the file cache, and the .ah lists that name the parts of a model, map or font

## What the player sees

Shorter loading. At start-up, on entering a map and before an event, a background worker reads the
next scene's files into the RAM file cache while the game is idle, so they are in memory when the scene
asks for them. Separately, every character, weapon, monster, map and font in the remastered art is
assembled from a `.ah` list of its parts; a part the list does not name is never loaded.

## Where it comes from

Both are plain text in the archive. Prefetch manifests live under `prefetchdata/<language>/`
(`common.txt`, `eventlist.csv`, `maps/<map>.txt`, `events/<n>.txt`) and `prefetchdata/add-on/`. The
`.ah` lists sit beside their assets under `gamedata/d3d11/artdata/` as `<asset>_d3d11.ah`, with a
`_d3d11_srm.ah` list beside many of them.

## Layouts

A prefetch manifest is whitespace-separated tokens, each a file name. A token beginning `##` is a
comment and is dropped; the shipped header `##Total_data_Size:_361_MB` is written with underscores so
that it stays one token. `eventlist.csv` is records of four comma-separated integers, with `##`
lines likewise skipped.

A `.ah` list is whitespace-separated tokens, each a path such as
`/GameData/D3D11/ArtData/chr/...phyre`, in load order, with no comment convention, header, count or
version.

## Shipped data

| Fact | Value |
|---|---|
| prefetch entries | 9,351 files, 283,340,853 bytes |
| languages | `us` 1,040, `fr` 1,040, `it` 1,040, `es` 1,040, `de` 1,042, `jp` 1,039, `kr` 1,036, `cn` 1,036, `ch` 1,036 |
| per language (US) | `common.txt` 1, `eventlist.csv` 1, `maps/` 709, `events/` 329 |
| outside the language folders | `prefetchdata/add-on/events/250.txt`, `prefetchdata/ff12mapjump_custom_nocrystal.csv` |
| prefetch `.txt` files | 579 begin with a `##Total_data_Size:_…` token, none with a spaced header; 3,506,346 name tokens in all |
| `.ah` files | 2,564, 12,235,216 bytes, all CRLF; 2,559 begin `/Gam`, 5 (the font lists) `font` |
| `.ah` tokens | 142,481, of which 62 (in the five font lists) are not paths |
| `.ah` groups | `chr/weapon` 308, `chr/monster` 258, `chr_shadow/monster` 249, `chr/npc` 172, `chr_shadow/npc` 171, `chr/high` 134, `chr_shadow/high` 130, `chr/gadget` 103; 457 `_srm` lists |

## Loader behaviour

### Prefetch manifests

- **Parsing.** `001DA0F0` scans tokens with `"%s"` (`008F4438`, through `0018A330`) until a scan fails,
  frees any token whose first two bytes are `##`, and appends the rest to a list. Nothing reads the
  size header.
- **Start-up.** The prefetch worker `001DADC0` (started by `001DAAC0`, the only user of the name
  `FileCachePrefetchManager`) first calls `001DA610`: with the RAM cache on, it reads
  `/PrefetchData/<language>/common.txt`, parses it, and opens every name with selector 5, closing the
  stream at once. It then reads `eventList.csv` (`001D9A40`), keeping records whose four fields all
  convert.
- **Map entry.** `001DA290` (when the cache is on, the byte `01F83441` is 0, and the map number changed
  and is not negative) builds `/PrefetchData/<language>/Maps/<map>.txt` and files it as a whole-text
  request; its completion `001D9FD0` parses the tokens into the map list.
- **Events.** `001D9EC0` compares each `eventList.csv` record's first word with the manager's word
  `+0xE8`, and for a match, or for the next record above it, loads `/PrefetchData/<language>/Events/<n>.txt`
  and `/PrefetchData/add-on/Events/<n>.txt` into the event list (`001D9DA0` → `001DA9E0`).
- **Map jumps.** `001DA090(map)` records the new and previous map numbers and writes them into the
  cache's protected words (`0020C1A0`: `+0x80` = new, `+0x84` = previous).

The worker then loops while running: it stops when `01F83441` is set; it sleeps 100 ms while requests
are pending or too little time has passed since the last activity, or when both lists are empty;
otherwise it sleeps 10 ms and opens one name, first from the event list (selector 3) and, when that is
empty, from the map list (selector 4), closing the stream at once.

Opening a name is what loads it. In the resolver a name that passes the cache's name filter is read
whole into the RAM cache when it misses, and the hit or new entry is stamped by its selector
(`0020C300`): selector 5 makes it kind 5, which eviction never frees; selector 3 stamps its group word;
selector 4 stamps the current map number, which eviction protects while that map or the previous one
is current. A name the filter rejects (three- or four-letter extensions) is opened and closed and not
cached. The manifests are advisory: a file no manifest names still opens normally.

### Asset-header lists

`0019EB60(manager, path)` files a `.ah` as a whole-text request whose completion `0019EF20` jumps to
the parser `0019E7B0`. The parser:

1. scans tokens with `"%s"` into a 256-byte stack buffer, without a bound, and steps the text by the token's length plus 2 from
   the scan start, so lines must end in CRLF with no leading whitespace;
2. makes an entry per token, with its position in the list as a `u16` at `+0`, a done byte at `+2` and
   the name from `+3`; there is no `##` filter, so every token is taken as a path;
3. frees the text and, from the last entry to the first, files a load request (kind 1) for each name,
   prefixed with `.` when it does not start with one, whose result goes to the entry's `+0x108`.

The lists are built from these patterns: map `.\GameData\%s\ArtData\map\%s\%s_%s.ah` and its `_srm`
form (`001A7A50`); character `./GameData/%s/ArtData/chr/%s_%s.ah` and the flat and grouped `chr_shadow`
forms (`001BB2B0`); procedural textures `./GameData/%s/ArtData/map/proceduralTexture/proceduralTexture_%s.ah`
(`001BE730`); and five literal font lists `./GameData/D3D11/ArtData/font/<jp|us|ch|cn|kr>/fontlist.ah`
(`001B44A0`). The varying `%s` is always `D3D11`.

## Modding notes

- A prefetch name only speeds up loading; leaving a file out of every manifest still loads it, just
  later.
- Comment a prefetch manifest with `##`; a `.ah` has no comments, and a `#` line in it is requested as a
  file.
- In a `.ah`, end every line with CRLF, start none with whitespace, and keep paths to 255
  characters or fewer.
- A part not named in its `.ah` is never loaded for that model.

## Related

- [File path resolution](file-path-resolution.md): the RAM cache, its name filter and the selector stamps.
- [Texture animation lists](texture-animation-lists-ta.md): the other list format read the same way.
- [Fonts](../Menus-And-HUD/fonts.md): the font list selection by language.
