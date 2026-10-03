# SD197 question pack (FABLE, 2026-10-03)

## The question

SD-197: what are the planar scalars when a kind-0x54 pass slot authors them as a resource or curve track rather than a constant? Decode the three track kinds 004309C0, 00430540 and 004307C0: for each, the record fields it reads (offset, width, signedness), how it turns the time/frame input into a value (keys, interpolation, clamping/looping, units), what it returns and where, and every path including early returns.

## The register row (as registered by FABLE)

```
Registered 2026-10-03 by FABLE (record fable-status-residue-1003, publishing); the question above is the row's scope.
```

## Page context: effect-mesh-records-kind-54.md section 8 (excerpt)

## 8. The vertex-prep consumers (SWE2-DATA, 2026-09-30)

Both consumers take the record's three attribute arrays by their `+0x24` / `+0x28` / `+0x2C` offsets and counts
([`fx54_consumers.py`](../../_index/candidates/dd-data-4-0930/fx54_consumers.py), V1–V3 and control C1, FAILS 0).
One caller chooses between them.

| consumer | `+0x24` vectors (count `+0x16`) | `+0x28` 4-byte (count `+0x18`) | `+0x2C` 8-byte (count `+0x18`) |
|---|---|---|---|
| `00435050`, one record | `memcpy` of 16 bytes per entry (`004351D3`–`004351EC`) | through a per-byte kernel together with the draw-parameter block's `+0x40` colour — the dword at `[01FD4A78]+0x800+0x40`, written by `0026EE00` from the element instance's `+0x240` (`00435197`–`004351B0`; **narrowed per `SD-140` X4**: the operand is the parameter block, not the element) | `memcpy` of 8 bytes per entry (`004351B5`–`004351CE`) |
| `00434CD0`, two records blended by a factor | a normalised lerp (`0043500D`), or a copy of the second record's entries when element `+0x1F1` bit 6 is set (`00434FAF`) | blended per channel (`00434F33`), then the same byte kernel (`00434F47`) — **only when `+0x1F1` bit 4 is clear; when set, the record's own `+0x28` goes straight to the kernel unblended** (`SD-140`) | a float-pair blend (`00434FAA`), or a copy when element `+0x1F1` bit 5 is set (`00434F4C`) |

The `+0x24` blend (`00432030`) sums the squares of the three blended components, takes `sqrtf`, divides one by the
length (a zero length keeps a constant) and scales the components before storing each 16-byte entry. Renormalising after
interpolation is what a unit normal needs, and it matches the census (every shipped `+0x24` entry is unit length with
`w = 0`). The `+0x28` bytes are not used raw: they pass through the byte kernel with the draw-parameter block's `+0x40`
colour (one dword — `[01FD4A78]+0x800+0x40`, filled by `0026EE00` from the element instance's `+0x240`), which
is consistent with a colour modulated by the element, but ~~the kernel was not decoded~~ *it is now
(`SD-140`, below)*. The `+0x2C` pairs are copied or
blended as floats, which is consistent with UVs. ~~Neither label is consumer-verified, and the emit paths were not traced.~~

- [x] **What the byte kernel does to the `+0x28` entries with the ~~element's~~ draw-parameter block's `+0x40` colour,
  and how the emit paths pack `+0x28` / `+0x2C` into the emitted vertex.** This decides whether they are colours and texture coordinates. **SD-140**
  (SWE2-DATA, 2026-09-30). *(**Answered 2026-09-30, SWE2-ORACLE** — execution-proven against shipped code over seeded
  trials; record [`sd140-vertex-prep-kernel-0930`](../../_index/candidates/sd140-vertex-prep-kernel-0930/README.md),
  `sd140_kernel.py` 23 checks FAILS 0.) `+0x28` is a **per-corner RGBA8 vertex colour** on the GS `0x80` = 1.0 scale
  (`0x80808080` is the exact identity, 47 % of shipped entries) and `+0x2C` a **per-corner float texture coordinate**;
  `c18 = 3·tri + 4·quad` in all 2,252 census records. The kernel `00432300` is the PS2 colour modulate
  `min(255, e·c >> 7)` against the draw-parameter block's `+0x40` colour (only its first dword is read). The two-mesh
  path `00434CD0` rounds a `cur·(1−w) + next·w` blend through `00433830` when `+0x1F1` bit 4 is clear, else calls the
  kernel unblended. Per pass, all three draw paths re-colour — flat broadcast when `param+0x1A8+p` is set, else
  per-corner modulate by `param+0x138+4p`, with `00432CC0` writing `alpha = trunc(alpha·L[n].w) mod 256` from the lit
  per-normal table — and the builders emit the colour as `float(byte)` lanes 0..255 and the UV pair as GS STQ divided
  back by the corner's `Q`. The pass operators and the clipper `00521450` are now read and execution-proven
  (`kind54-pass-operators-fable-1002`, below).*

The pass operators are read and execution-proven (FABLE, 2026-10-02,
kind54-pass-operators-fable-1002 (`../../_index/candidates/kind54-pass-operators-fable-1002/`)). Each one
writes the per-pass UV copy, never the prepared one.

- Pass byte `+0x1B0` can replace the UV with the first two floats of the lit per-normal table at each corner's normal
  index (`00396F20`). For value 2 it also adds a screen-position term `((X/16)/512 − 3.5, (Y/16)/512 − 3.5625)`
  (`00394B70`).
- Byte `+0x1AC` then swaps the pair (`0043E7B0`), applies `offset + uv·scale` from `param + 0x150 + 16p` (`00434630`),
  or does both (`00434760`).
- `param + 0x1F2` bits 0 and 1 scale the pair about 0.5 (`0043E840`). The scale is the pass pair (which is then reset
  to 0.5) or `param + 0x1EC`.

The clipper `00521450` clips each triangle in homogeneous space against `|x|, |y|, |z| ≤ |w|`, using six planes
(Sutherland–Hodgman). It interpolates position, colour, UV and clip position linearly and returns the polygon's vertex
count. A count of 0 drops the triangle; any other count is re-projected and emitted as an n-gon.

The lit per-normal table is answered (OPUS, 2026-10-02, executed: record
[`opus-k54-lighting-1002`](../../_index/candidates/opus-k54-lighting-1002/README.md), `k54_light.py` 22 checks
FAILS 0). Each of the five routines forms `m = M n` from the caller's three matrix columns (`022D91B0` / `022D91C0` /
`022D91D0`). Pass byte `+0x1B0` then picks a reflection sphere map (1: `00395CF0` about y, `00395780` about z), a
planar normal projection `(−s·m.x, s·m.y, 0)` with `s` at `param + 0x1D8 + 4k` (2: `003962F0`), or a normal sphere
map (3 and 4: `00396A30` about y, `00396560` about z), with `+0x1B4` choosing the y or z axis. Lane 3 is `(M n).w` for
modes 1 and 2 and the carried `022D9310.w` for modes 3 and 4, and a zero vector lands on the centre 0.5. The entry's
lanes 0-1 become the UV through `00396F20`, and its lane 3 feeds the alpha kernel `00432CC0`. So the regenerated UVs
are sphere-map coordinates (modes 1, 3, 4) or a planar normal projection (mode 2).
~~*Not established (the record's Limits): which modes and matrices shipped effects use and what the matrices hold at
draw time (a population and runtime question); the selectors of the four other draw paths (`00437130`, `00438860`,
`004434D0`, `00444340`), which call the same five routines; and whether the planar index k equals the pass index.*~~
*(Answered 2026-10-03, FABLE, except the matrices' contents. Record
`../../_index/candidates/fable-k54-residue-1003/README.md`: `k54_residue.py` 100 checks FAILS 0, static and executed;
`census_k54_modes.py` FAILS 0, authored data.)*

- **The per-pass selector is one switch in all five draw paths.**
  - Each path reads the mode byte `param + 0x1B0 + p` (`00437486`, `00438C70`, `00443865`, `00444711`) and the axis
    byte `param + 0x1B4 + p`.
  - Each reaches the same routine per mode and axis as above. Mode 0, and every mode from 5 to 255, builds no table.
  - The planar call sits on the mode-2 arm only.
- **Which path draws a kind-`0x54` mesh** is chosen per element, by the parameter block's byte `+0x1F1`.
  - The dispatcher has one caller, `00449AB0`+0x6AB. It runs `00438860` when `+0x1F1` is `0x80` or above, else
    `00437130` when bit 3 is set, else its inline path.
  - `00449AB0` builds `+0x1F1` from definition byte `+0x590` (executed over all 256 values):
    - bit 7 is `+0x590` bit 5;
    - bit 3 is bit 0 or bit 5;
    - bits 4-6, the two-mesh switches of §8, are bits 1-3.
  - Over every EFX stream, the 5,204 type-`0x05` elements split 1,800 / 522 / 2,882 (`00437130` / `00438860` /
    inline).
- **`004434D0` and `00444340` draw no kind-`0x54` record.**
  - Their only callers are the type-`0x04`, `0x06` and `0x07` walks of `the-element-types-00-0a.md`. The calls are at
    `00445AF8` / `00445AFF`, `004477D9` / `004477E0` and `004487A1` / `004487A8`; there is no other branch reference and
    no stored pointer.
  - Each walk draws the procedural ring, column or dome grid it builds itself.
  - Definition bit 0 of `+0x672` (type `0x04`) or of `+0x6D2` (`0x06` / `0x07`) picks `00444340`; clear, it picks
    `004434D0`. The same bit becomes `+0x1F1` bit 3.
  - Shipped elements, `004434D0` / `00444340`: type `0x04` 169 / 4, type `0x06` 3 / 22. Type `0x07` is not authored.
- **The planar index k equals the pass index p.**
  - In all five paths the planar call's pointer is `param + 0x1D8 + 4p`, with the same p that indexes `+0x1B0` (call
    sites `004375BE`, `00438D98`, `004439AE`, `00444864` and the inline path's).
  - This is proven inductively over each pass loop: every counter starts at 0 and gains 1 on every back edge.
  - The walks write `+0x1D8 + 4p` with that same p. The value comes from the float track 0x10 bytes before the pass's
    slot, evaluated at `00449AB0`+0x543. So a mode-2 pass scales by the scalar authored for its own slot.
- **The pass bytes are authored.** Each walk goes through the definition's four `0xF0`-byte pass slots (type `0x05`:
  definition `+0x250`).
  - For the p-th kept slot it copies slot byte `+7` to `+0x1B0 + p` and slot byte `+0xB` bit 0 to `+0x1B4 + p`
    (`00449D08`).
  - It skips a slot whose byte `+0` is 0 or whose texture lookup fails, and later slots move down (executed, 2,592 slot
    patterns per walk).
  - The element setups, `00538DB0` among them, leave those bytes as loaded.
- **What ships.** All EFX streams, all locales; 9,846 active pass slots, none of mode 5 or above:

| element type | active slots | mode 0 | mode 1 (axis y / z) | mode 2 | mode 3 (y / z) | mode 4 (y / z) |
|---|---:|---:|---:|---:|---:|---:|
| `0x05` kind-`0x54` mesh | 9,622 | 9,294 | 54 (28 / 26) | 152 | 21 (7 / 14) | 101 (44 / 57) |
| `0x04` ring band | 173 | 157 | 0 | 16 | 0 | 0 |
| `0x06` column | 51 | 47 | 3 (3 / 0) | 0 | 1 (1 / 0) | 0 |

  - **Mesh paths.** `00437130` meets mode 2 only (8 slots). Mode 1 runs on `00438860` 24 times and inline 30, mode 3 on
    17 and 4, mode 4 on 36 and 65.
  - **Grid paths.** `004434D0` meets modes 2 (16) and 3 (1); `00444340` meets mode 1 only (3).
  - **The constant planar scalar.** 21 of the 152 type-`0x05` mode-2 slots author it as the constant 0.0.

*Not established:*
- *what the matrices hold at draw time (a runtime question). Modes 1 and 3 read one matrix global and modes 2 and 4
  another, in 79 and 269 shipped slots;*
- *the planar scalars authored as resource or curve tracks;*
- *the runtime pass index, since a failed texture lookup drops a slot;*
- *what `+0x1F1` bit 3 changes in the drawing beyond selecting the path.*
*(Residue replaced 2026-10-03, SWE2-DATA, consuming `OPUS-REQ-DATA-K54-LIGHTING-RESIDUE-1002`.)*



## FABLE's residue record (excerpt)

# The kind-0x54 lighting residue: draw-path selectors, the planar index, shipped pass modes (FABLE, 2026-10-03)

Asked: close or bound the residue that `opus-k54-lighting-1002` left on
`17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md` (the italic *Not established* lines
after "The lit per-normal table is answered", and the status line's "open:" clause):

- (A) the selectors of the draw paths `00437130`, `00438860`, `004434D0`, `00444340`;
- (B) whether the planar index k (the dword `003962F0` reads at `param + 0x1D8 + 4k`) is the pass index p;
- (C) which pass modes (`param + 0x1B0 + p`, values 1..4, axis `+0x1B4 + p`) shipped effects use.

Image: `Database/Tools/work/exe/FFXII_TZA.exe`, sha256 `73461d08…21f8` (checked by `rvlib.py`). Addresses are VAs with
the image base included. Dates are UTC (machine clock 2026-10-02 21:56 CDT = 2026-10-03 02:56 UTC).

| file | what |
|---|---|
| `k54_residue.py` / `.out` | 100 checks, FAILS 0 (static anchors, an affine loop proof, Unicorn runs, 7 patched-copy controls) |
| `k54flow.py` | the affine reaching-definition pass `k54_residue.py` uses (section B) |
| `rvlib.py` | copied unchanged from `fable-review-astra-ov42-caller-quotient-bound-1002` |
| `census_k54_modes.py` / `.out` | the shipped-data census, checks N1-N3, FAILS 0 |
| `k54_modes.tsv` | one row per active pass slot (9,846 rows) |
| `page-draft.md` | the proposed page text (OLD -> NEW) |

Rerun: `python k54_residue.py > k54_residue.out` (about 15 s) and `python census_k54_modes.py > census_k54_modes.out`
(about 40 s; reads `D:/FFXII_TZA_extract` through `members/type_census.py`).

## (A) The selectors

**What picks a kind-0x54 draw path.** The draw dispatcher `004355D0` has one caller, the type-0x05 walk `00449AB0`,
which calls it at `0044A15B`. There is no other `E8`/`E9`/`0F 8x` reference, and no 8-byte VA of the entry is stored
anywhere (C1). After the prep, the dispatcher reads the parameter block's byte `+0x1F1` at `0043566F` (A1):
- `0x80` or above calls `00438860`;
- otherwise bit 3 set calls `00437130`;
- otherwise it runs its own inline path.

`00449AB0` builds `+0x1F1` and `+0x1F2` from definition byte `+0x590`. This was executed over all 256 values (A2):

| `+0x1F1` / `+0x1F2` bits | come from |
|---|---|
| `+0x1F1` bit 7 | `+0x590` bit 5 |
| `+0x1F1` bit 3 | `+0x590` bit 0 OR bit 5 |
| `+0x1F1` bits 4, 5, 6 | `+0x590` bits 1, 2, 3 (the two-mesh blend switches of the page's section 8) |
| `+0x1F1` bits 0-2 | `(+0x4A >> 2) & 7` |
| `+0x1F2` bits 0-1 | `+0x590` bits 6-7 |

So definition `+0x590` bit 5 selects `00438860`, bit 0 selects `00437130`, and anything else selects the inline path.

The census applies that rule to the page's own TSV and reproduces the section-5 figures (514 / 1,791 / 2,859 over 5,164
elements; check N3). Over every EFX stream, the 5,204 type-0x05 elements split as:
- `00437130`: 1,800;
- `00438860`: 522;
- inline: 2,882.

**`004434D0` / `00444340` draw no kind-0x54 record.** Their only callers are three element walks, which pass the
parameter block in `rcx` (raw census, C1):
- type 0x04 `004453D0`: calls at `00445AF8` / `00445AFF`;
- type 0x06 `00447020`: `004477D9` / `004477E0`;
- type 0x07 `00447ED0`: `004487A1` / `004487A8`.

Each walk first builds its own procedural grid (ring band, column, dome; `the-element-types-00-0a.md`) and stages it in
globals. No kind-0x54 handle is involved.

The choice between the two paths is definition bit 0 of `+0x672` (type 0x04) or `+0x6D2` (types 0x06 and 0x07):
- set: `00444340`;
- clear: `004434D0`.

The same bit is copied to `+0x1F1` bit 3, the position that sends a mesh to `00437130` (executed, A2).

Shipped elements, `004434D0` / `00444340`:
- type 0x04: 169 / 4;
- type 0x06: 3 / 22;
- type 0x07: no authored chunk.

**The per-pass selector is the same switch in all five paths (A3).** Every path reads the mode byte at
`param + 0x1B0 + p`:

| path | mode read |
|---|---|
| inline | `004359E5` |
| `00437130` | `00437486` |
| `00438860` | `00438C70` |
| `004434D0` | `00443865` |
| `00444340` | `00444711` |

Each path also tests the axis byte `param + 0x1B4 + p` (two sites each, section B). A CFG walk of every mode 0..6 and
255 against axis 0 / 1 reaches the same routines in all five:

| mode | axis 0 | axis 1 |
|---|---|---|
| 1 | `00395CF0` | `00395780` |
| 2 | `003962F0` | `003962F0` |
| 3, 4 | `00396A30` | `00396560` |
| 0, 5, 6, 255 | none | none |

The planar call sits on the mode-2 arm only.

The matrix globals each arm reads before its lighting call are the same in all five paths:
- modes 1 and 3: `02AEEA20`;
- modes 2 and 4: `02AEEBF0`;
- mode 1 also: `02AEEAA0`, its V vector.

The arms are prepared differently, though. This is call shape only, not read:
- The mesh paths' arms call `00397910` with the parameter block and then `0039B960` three times in every mode.
- The grid paths' arms never call `00397910`, and call `0039B960` only in modes 1 and 4.

## (B) k = p, in every path

`k54flow.py` gives each register and stack slot (keyed by its offset from the entry `rsp`) an affine value
`base + a*P + c`, where P is the pass-loop iteration. It proves the loop inductively:
1. It computes the state at the loop header from the function entry.
2. It hypothesises that every location that is 0 there is P.
3. It runs the body once.
4. It keeps only the locations that every back edge returns as P + 1, and repeats until nothing changes.

Calls clobber the volatile registers, the callee's home area and a 0x100-byte window above any frame address passed out.

For each path:
- exactly one back edge follows a `+0x1F0` read and encloses the mode read;
- its header dominates the mode read, both axis reads and the planar call;
- the proof reaches a fixpoint after 2 iterations.

Results (section B of `.out`):

| path | header | counters equal to p | mode read | planar call: r8 |
|---|---|---|---|---|
| `004355D0` inline | `00435760` | SP0-0x1a8, SP0-0x1b8, rcx, rdi | `param + p + 0x1B0` | `param + 4p

## Listings in this folder

- `004309C0.lst` (155 B, 47 lines)
- `00430540.lst` (634 B, 174 lines)
- `004307C0.lst` (238 B, 67 lines)
