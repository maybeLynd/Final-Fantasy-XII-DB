# Movie containers

| ext | files | size | tree |
|---|---:|---:|---|
| `webm` | 40 | 10,377 MB | `gamedata/d3d11` |
| `mh` | 43 | 172 KB | `ps2data/movie_finish` |

**`webm` is 10.4 GB — the single largest thing the game ships**, and a candidate `standard`
disposition: WebM/Matroska is an open format the game did not author.

> **`standard` is not a free pass, and this is the clearest case of why.** The interesting question
> is not *what is WebM* but **which codecs this build accepts, at what resolutions, and what it does
> with a file it cannot decode** — none of which the spec answers. A `standard` row that stops at
> naming the standard has documented the format and not the game.

**40 `.webm` against 43 `.mh`** is close enough to suggest `mh` is a per-movie sidecar — a header, a
cue table, a subtitle index. The near-match is a lead, not a finding.

## Confirmed by the magic census — 2026-09-03

- **`.webm` is `1A 45 DF A3`** — EBML, so genuinely Matroska/WebM. The `standard` disposition is
  correct, and the note must still say which codecs this build accepts.
- **`.mh` is `.mhe`** — its own four-byte magic, not a text header. A real format with a real
  signature, so the sidecar reading survives contact with the bytes.
- The binary carries `%s%s.webm` and `PS2Data\movie_finish\us\OPN.mh` — **paired trees, one per
  language**, which is what a per-movie sidecar should look like.

Write sheets to `_templates/FORMAT.md`. See [_index/ASSET-FORMATS.md](../../_index/ASSET-FORMATS.md).

## `.mh` — explained 2026-09-12

[`mh-movie-seek-index.md`](mh-movie-seek-index.md): the PS2 movie seek index (`.mhe` header + 12-byte
`{offset, frame, flags}` entries), shipped for 43 movies and **not read** — the movie open takes only the
`.md` name to build the `.webm` path, and the one lookup of the `.mh` path discards it.

