---
title: "Prefetch and asset-header manifests: the text lists that preload files into the file cache, and the .ah lists that name the parts of a model, map or font"
kind: "format"
category: "Game files and data tables"
summary: "The plain-text manifests the game reads by whitespace-separated tokens: the prefetch lists (common.txt at start-up, one per map on map entry, one per event, eventList.csv's event schedule, the add-on folder) and the background thread that opens their names into the RAM file cache under protected stamps; and the .ah asset-header lists that name, in order, the .phyre files of every model, map, font and procedural texture set and load each of them, with the AssetListManager pools and the pass that resolves asset imports once a list has loaded; the prefetch manager's language folder, lists and event watch; and the menu TexList.txt. Includes the shipped counts and the rules both formats impose."
addresses: "001DA0F0, 008F4438, 0018A330, 001DA610, 001DA290, 001D9FD0, 001D9A40, 001D9EC0, 001D9DA0, 001DA9E0, 001DA090, 0020C1A0, 001DAAC0, 001DADC0, 009005E8, 0019EB60, 0019E7B0, 0019EF20, 001A0BB0, 001A07B0, 001A0F80, 001A7A50, 001B44A0, 001BB2B0, 001BE730, 0020C300, 001DAD60, 001D9400, 001D9930, 001D99C0, 001DA970, 0019EF40, 0019DA30, 0019E740, 0019EE50, 0063DA50, 00677CE0, 001B14E0, 001B07A0, 001B1800, 002E98F0, 0017F000"
---

## What the player sees

Shorter loading. At start-up, on entering a map and before an event, a background worker reads the
next scene's files into the RAM file cache while the game is idle, so they are in memory when the scene
asks for them. Separately, every character, weapon, monster, map and font in the remastered art is
assembled from a `.ah` list of its parts; a part the list does not name is never loaded. The few
menu textures that are not part of a picture, such as the target lines, come from one more list.

## Where it comes from

Both are plain text in the archive. Prefetch manifests live under `prefetchdata/<language>/`
(`common.txt`, `eventlist.csv`, `maps/<map>.txt`, `events/<n>.txt`) and `prefetchdata/add-on/`. The
`.ah` lists sit beside their assets under `gamedata/d3d11/artdata/` as `<asset>_d3d11.ah`, with a
`_d3d11_srm.ah` list beside many of them. The menu texture list is
`gamedata/d3d11/artdata/menu/texlist.txt`.

## Layouts

A prefetch manifest is whitespace-separated tokens, each a file name. A token beginning `##` is a
comment and is dropped; the shipped header `##Total_data_Size:_361_MB` is written with underscores so
that it stays one token. `eventlist.csv` is records of four comma-separated integers, with `##`
lines likewise skipped.

A `.ah` list is whitespace-separated tokens, each a path such as
`/GameData/D3D11/ArtData/chr/...phyre`, in load order, with no comment convention, header, count or
version.

`TexList.txt` is one texture file name per line, relative to `GameData/D3D11/ArtData/menu/`, each line
ending in CRLF.

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
| `texlist.txt` | 301 bytes, 11 CRLF lines, each a `.dds.phyre` name that exists under `gamedata/d3d11/artdata/menu/` (`targetline_p`, its six `_clut_` variants, `chain_item`, `chainflash`, and `w_line01` with its `_clut_1`) |
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

### The prefetch manager

`001DAD60` builds the manager once, `0x1C0` bytes at `01F82CF0`, with `001D9400`. The constructor sets up
the lists and their locks, stores itself as the file cache's owner (`[0020C700()] + 0x18`, so the
cache's group word `+0xE8` is the manager's), and picks the language folder from `0017E270()`: 0 and
10 give `jp`, 2 `fr`, 3 `de`, 4 `it`, 5 `es`, 7 `kr`, 8 `ch`, 11 `cn`, and any other value `us`. The
paths are built by inserting that code and `/PrefetchData/` in front of the file name (`001DAB30`).

- `001D9A40` keeps each `eventList.csv` record as four words in the list `+0xD0` and then sorts the
  list by the first word, ascending (`001D9200`, a merge sort that merges with `001D9150`).
- The map list's completion is the stub `001D9920`, which passes the manager to `001D9FD0`.
- `001D99C0` empties the map list `+0x60` and `001D9930` the event list `+0x118`, freeing each name;
  each sets its list's empty byte (`+0x78`, `+0x130`). `001D9D80` is true when both are set.
- `001DA970`, called on every pass of the worker, reloads the event list when the current event
  number (`00265270`) is positive and differs from `+0xE8`: it stores the number, empties the list under
  its lock `+0xF0` and runs `001D9EC0`.
- The worker takes the map list's first name with `001DAD30` and logs
  `[FileCache] Prefetch On Enter Map End` when that empties the list.

The two busy counters `+0x24` and `+0x28` and the activity time `+0x8C` are what the worker tests
before opening a name. The asynchronous loader raises counter `+0x24` around every load it runs
(`001D9F70`) and lowers it afterwards (`001D9F90`), which also stamps the time.

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

`001BB2B0` takes a character's name from its PS2 model path: `002E98F0` turns the model id into a kind
and index (`002ED6F0`, adding `0x33` to the index for kind 1), `002DF980` returns that path, and the
text after `PS2Data\obj_finish\in\`, less its last three characters (`.cm`), with `\` turned into
`/`, is the name. Model id −1 uses `global/MaterialSphere`.

`0017F000(id)` asks the object at `01F81240` (`001BC000`, null before it exists) for a model's list
record through `001BB2B0` and returns it. The binding's load `002EAD50` calls it before it files the
model's own file and ignores the result, so binding a character model also queues its `.ah` lists.

### Asset-header list records

The lists live in the `AssetListManager` that `0019EF40` builds once (`0x188` bytes at `01F81158`,
`0019DA30`): a pool of 192 list records of `0x130` bytes at `+0x08` (`0019D5B0`) and a pool of 3,072
entry records of `0x118` bytes at `+0xC8` (`0019D740`), each pool with its own lock. `0019EB60` takes a
list record and the parser takes one entry record per token (`001BA860`) and writes to it without a
test, so the 3,072 entry records bound every list loaded at once.

- The text is read as a kind 4 request whose completion, `0019EF20`, runs on the loading thread, so
  the parse does too.
- The parser files its entry requests at the tail of the queue (`001A0C50`) from the last entry to
  the first, so the entries load in list order ahead of anything already waiting.
- Each entry's request (kind 1) completes in the frame pump through `0019EF00`, which passes the
  manager and the entry to `0019E740`.
- When the entry is the list's last (`u16 +0` equals the count less one), `0019E740` queues a job
  `{0019EE50, list}` on the second `AsyncJobManager` (`01F81100`, through `00199F10` and `0019A000`).
- `0019EE50` runs `0063DA50` and then `0063B010` on each entry's loaded cluster and sets the list's
  done byte `+0x128`. `00796350` runs the same two passes over an array of clusters.
- `0063DA50` walks the cluster chain (`+0x98`), skipping a cluster whose `+0x80` bit `0x1` is set,
  hands every `PAssetReferenceImport` object (descriptor `02D3E780`) to `00677CE0`, and sets that bit.
  `0063B010` runs `0063B040` on each cluster of the chain until one returns non-zero.
- `00677CE0` looks the import's name up among the registered assets (`00676BD0`). A miss logs
  `Failed to find asset %s of type %s, using fallback` and takes the type's fallback (`0063BC00`); a
  hit of another type logs `Found asset %s of wrong type, wanted %s, got %s`. Every pointer chained to
  the import is then set to the asset.

The pools' record vectors are sized with `0019EC40` (list records: grow with `0019E010`, shrink with
`0019EA20`) and `0019ED80` (entry records: grow with `0019E2C0`); `0019DF90` frees the entry vectors of a
range of list records, and `0019DCC0` the list pool.

### The menu texture list

At start-up `001B1630` (through `001B1580`) calls `001B1750` on the menu sprite batcher (`01F811E8`):

1. `001B14E0` opens `GameData/D3D11/ArtData/menu/TexList.txt` (`001D6F20`), reads it whole into a
   zero-terminated block and closes it (`001D6E80`); when it does not open it logs
   `UI TextureList load failed!` and the list stays empty.
2. `001B07A0` splits the text at each LF, up to 1,024 lines, drops the line's last character (the CR),
   and stores `./GameData/D3D11/ArtData/menu/` plus the rest (`"%s%s"`, `008F80F0`) as a string in the
   batcher's vector `+0x00` (`001AB6B0` grows it).
3. For each string, in order, `001B1800` files a kind 1 load at the head of the queue with the
   completion `001B1C10` and the result slot `batcher + 0x108 + 8 × i`; an empty line files nothing.

A line of 128 characters or more before its CR stops the game (`__report_rangecheckfailure`).
`001B1C10` registers each loaded texture under the hash of its lower-cased path in the batcher's tree
`+0x28`.

## Modding notes

- A prefetch name only speeds up loading; leaving a file out of every manifest still loads it, just
  later.
- Comment a prefetch manifest with `##`; a `.ah` has no comments, and a `#` line in it is requested as a
  file.
- In a `.ah`, end every line with CRLF, start none with whitespace, and keep paths to 255
  characters or fewer.
- A part not named in its `.ah` is never loaded for that model.
- In `TexList.txt`, end every line with CRLF (the loader drops each line's last character), keep each
  name under 128 characters, and list at most 1,024 names.

## Related

- [File path resolution](file-path-resolution.md): the RAM cache, its name filter and the selector stamps.
- [Texture animation lists](texture-animation-lists-ta.md): the other list format read the same way.
- [Fonts](../Menus-And-HUD/fonts.md): the font list selection by language.
