# MapScreenPage type rows: a stale name and fields the UQ-156 / UQ-158 readings establish (FABLE, Claude Opus 5.5, 2026-09-26)

A propagation request for the type store. FABLE does not edit `_types`. The static readings are published on
[the map screens page](../../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) and in the UQ-156 /
UQ-158 rows (`a70596b92`, `16c61d002`, `4914ae1bd`), with controls in this folder and in `../uq158-segment-filter/`.

## 1. A stale semantic name: the `+0x140` nodes are not markers

`MapScreenMarkerNode0B0` (256 × 0xB0 at `MapScreenPage +0x140`) and `markerListHead` (`+0xBBD0`) were named on
2026-09-20 from `00402A40`'s structure. The later readings show what the nodes hold:
- `00402A40` asks the draw-list builder `003BE3A0` for **selector 0**. In `003C1A20` the selector is a point-kind
  filter, so the nodes come from the **field points** (lmap array A). The marker list uses selector 2, every point.
- Each record becomes a node only when `004023D0` does **not** find the same undirected segment already listed. It
  compares the two ids at `+0x80`/`+0x82` and the endpoints `+0x84`/`+0x86`, `+0x8C`/`+0x8E` in either order
  (`004023E0`–`0040246F`). The UQ-158 correction `a70596b92` fixed that branch direction.
- `004043B0` draws each node as a **line** between two areas (through `00274CA0`).

So the `+0x140` array holds **the connections between the location's areas, each once**, and `+0xBBD0` is the head
of that segment list. The **marker list** head is `+0xBBC0`: `002B7460` builds it from the block evaluator's
selector-2 scratch through `00402D20(page + 0xB140, scratch, n)`, and arm 4 hands it to the icon drawer and the
label pass. Proposed: rename the type to reflect area links (for example `MapAreaLinkNode0B0`), rename
`markerListHead` to an area-link list head, and give `+0xBBC0` the marker-list name.

Node fields the readings add:

| offset | proposed | meaning | evidence |
|---|---|---|---|
| `+0x80` | segment record (16 B) | ids `+0x80`/`+0x82`, endpoints `+0x84`/`+0x86` and `+0x8C`/`+0x8E` | `004023D0` compare, `004023E0`–`0040246F` |
| `+0xA8` | flags, bit 0 = pulse | `004043B0` modulates the line by `sinf` when bit 0 is set; no writer in the page procedures or `00402000`–`00405000`, and the node is zero-filled | `004043B0` read, the map page's element-node narrowing |

## 2. `MapScreenPage` fields named by the readings (currently DISCOVERED census rows)

| offset | width | proposed name | meaning (static) | where read |
|---|---|---|---|---|
| `+0xC8` / `+0xCC` | dword ×2 | view base x / y | the view origin's base; arm 4 adds the scaled scroll to it; arm 14 repeats `002B66E0` until the pair stops changing | arm 4 skeleton, arm 14 centring |
| `+0xD4` | dword | zoom percent | divided by 100 for the view scale; arm 10 rescales the marker list by zoom ÷ 100 | arm 4, arm 10 |
| `+0xE0` | dword | input/state flags | bit 0 set: arm 10 does nothing, and after the dispatcher a set bit 0 ends the centring (clears `+0x13A` bit 0); bit 1 likewise | arm 10 (behaviour only; meaning not named) |
| `+0x130` | qword | map data | the construct message's `+0x10`; its `+8` is the sprite atlas, its `+0x10` the map picture texture | arm 1, arm 4, `00404230` |
| `+0x138` | word | map slot | from the construct message (negative → 0); queried through `003C02B0` | arm 1, arms 14/42 |
| `+0x13A` | word | page flags | bit 0 centring in progress (arm 14); bit 2 about to be destroyed (arm 15); bit 3 from the slot's `+0x10` bit 15, disables the dispatcher / zoom / marker step | arms 14, 15, 10 |
| `+0xB140` | 96 B | marker entry storage | the region `00402D20` fills from the selector-2 scratch | UQ-158 `002B7460` |
| `+0xBBC0` | qword | marker list head | built by `002B7460`; drawn by the icon drawer and label pass; rescaled by arm 10 | UQ-158, arm 4, arm 10 |
| `+0xBBC8` | qword | current record | the record arm 4 reads flags `+0x28` and the field word `+0x1C` from, and whose `+0x30` rectangle the RectTween targets; arm 10 on the location map treats it as the current marker. The page uses both words; the type is not claimed. | arms 4, 10, C-13 |
| `+0xBBD0` | qword | area-link list head | see §1 | `00402A40` return stored at `002B82AE` / `002BB71D` |
| `+0xBBD8` / `+0xBBDA` | word ×2 | scroll x / y | scaled by the zoom into the view origin | arm 4 |
| `+0xBBE0` | word | mode | mode 6 changes arms 14 and 10 and the marker build | arms 4, 10, 14, UQ-158 |
| `+0xBBE4` / `+0xBBE5` | byte ×2 | message-37 latch | message 37's bytes `+8` / `+0x10`; message 38 clears them to `0xFFFF` | arms 37, 38 |
| `+0xBBE6` | word | message-40 word | message 40 stores its word `+8` here | arm 40 |
| `+0xBBE8` | dword | message-37 tick | the 60 Hz tick `0208F570` latched by message 37 | arm 37 |
| `+0xBBEC` / `+0xBBEE` | word ×2 | layout size copy | arm 1 copies the 512 × 448 layout size here | arm 1 |

## 3. Widget-level note

The page's `+0x38` is `Widget +0x38`, the node's live draw record ([the widget contract](../../../16-UI/Widget-Object-Model/CONTRACT-widget-object.md)).
Its byte `+0x5C` is a palette-bank index: `00404230` adds four times it into `TEX0`'s palette base (control
`map_picture.py`). That belongs on the draw record's type, if the store declares one.

Everything here is static. None of it is runtime-observed.
