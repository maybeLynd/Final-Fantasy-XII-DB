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
| `004355D0` inline | `00435760` | SP0-0x1a8, SP0-0x1b8, rcx, rdi | `param + p + 0x1B0` | `param + 4p + 0x1D8` at `00435AF1` |
| `00437130` | `00437200` | SP0-0x190, SP0-0x1a8, rdi, rdx | `param + p + 0x1B0` | `param + 4p + 0x1D8` at `004375BE` |
| `00438860` | `004389F0` | SP0-0x10f8, SP0-0x1118, rax, rdx | `param + p + 0x1B0` | `param + 4p + 0x1D8` at `00438D98` |
| `004434D0` | `00443570` | SP0-0x1d0, SP0-0x1e8, r13, rbx | `param + p + 0x1B0` | `param + 4p + 0x1D8` at `004439AE` |
| `00444340` | `004443F0` | SP0-0x1e0, SP0-0x1f8, r15, rsi | `param + p + 0x1B0` | `param + 4p + 0x1D8` at `00444864` |

The axis reads are `param + p + 0x1B4` at all ten sites. So k = p in all five paths.

The register names the request used fit this table:
- In `00437130`, k is r15 (from `movsxd r15, edx` or `[rsp+0x70]`) and the mode index is rdi.
- In `004434D0`, k is `movsxd rax, ebx` and the mode index is r13.
- In `00444340`, k is esi and the mode index is r15.

In each path, both registers are on the proven list.

**The writer side has the same p.** All four walks store `+0x1D8 + 4p` with the same compacted p as `+0x1B0 + p`
(C2, executed). So a mode-2 pass scales by the scalar authored for its own slot.

**Controls.** Each patched copy makes its check fail:

| patch | check that fails |
|---|---|
| `inc ecx` at `00436C91` -> `dec ecx` | the planar check |
| `inc rdi` at `004387F0` -> `dec rdi` | the mode and axis checks |
| `add rax, 0x76` at `004439A6` -> `0x77` | the planar check |

## (C) Where the pass bytes come from, and what ships

**Writers.** The four walks above fill the block `[01FD4A78] + 0x800`, then call their draw paths. Within one walk:
1. The walk visits the definition's four 0xF0-byte pass slots: type 0x05 at definition `+0x250`, type 0x04 at `+0x350`,
   types 0x06 and 0x07 at `+0x3B0`.
2. It skips a slot whose byte `+0` is 0 or whose texture lookup `00431830` fails. Later slots move down.
3. For the p-th kept slot, it writes:
   - slot byte `+7` to `+0x1B0 + p`;
   - slot byte `+0xB` bit 0 to `+0x1B4 + p`;
   - slot byte `+0xA` bit 3 to `+0x1AC + p` (bit 1 is set for texture mode 3);
   - the float track 0x10 bytes before the slot, evaluated by `004309C0`, to `+0x1D8 + 4p`.
4. It writes the kept count to `+0x1F0`.

This was executed in all four walks (C2, Unicorn over the certified image). Each walk ran 2,592 times: slot byte `+0` in
0..5 for each of the four slots, with the texture lookup present and absent. Every callee was stubbed with a disclosed
return value; the draw callee captured the block. Two side findings:
- `00447020` and `00447ED0` call their draw path even with no kept slot: 626 of their runs did, with `+0x1F0` = 0.
  `004453D0` and `00449AB0` test the count first.
- The element setups (`00538DB0` for 0x05, `00538C80` for 0x04, `00538EB0` for 0x06/0x07) leave slot bytes `+0`, `+7`
  and `+0xB` as loaded. This was executed on 48 random definitions each (C3): 0 of 576 bytes differ, while each setup
  rewrote 27,080 to 29,355 other bytes.

Among the 14 functions holding a rip-relative reference to `01FD4A78`, the only byte stores at displacement 0x1B0 are
the four slot copies: `00449D08`, `004458FB`, `004475E9`, `004485BB` (C1).

Controls, each failing its check:
- `[r13 + 7]` -> `[r13 + 8]` at `00449D03`;
- `inc r15` -> nops at `00445A54`;
- the setup's `+0xA9` store moved to `+0xA7` at `00431800`.

**So the pass modes are authored data:** the definition's slot byte `+7`, with the axis in slot byte `+0xB` bit 0.

The census walks every EFX stream the way `members/type_census.py` does:
- the 3,288 `.efx` files;
- the blobs inside the 410 `.efb` files;
- the 531 streams embedded in `.cm` / `.mpk` files.

It reproduces type_census's chunk counts (N1) and the page's path counts (N3). Counts are over all nine locale trees.
A slot is "active" if its byte `+0` is non-zero.

| type (path family) | active slots | mode 0 | mode 1 | mode 2 | mode 3 | mode 4 |
|---|---:|---:|---:|---:|---:|---:|
| `0x05` kind-0x54 mesh (`004355D0` family) | 9,622 in 5,204 elements | 9,294 | 54 | 152 | 21 | 101 |
| `0x04` ring band (`004434D0` / `00444340`) | 173 in 173 | 157 | 0 | 16 | 0 | 0 |
| `0x06` column (same pair) | 51 in 25 | 47 | 3 | 0 | 1 | 0 |
| `0x07` dome | not authored | | | | | |

- **No mode above 4 is authored anywhere.** Modes 1-4 fill 348 of the 9,846 active slots.

Axis byte, 0 (y) / non-zero (z), per mode:

| type | mode 1 | mode 2 | mode 3 | mode 4 |
|---|---|---|---|---|
| `0x05` | 28 / 26 | 113 / 39 (authored but unused) | 7 / 14 | 44 / 57 |
| `0x04` | – | 14 / 2 (unused) | – | – |
| `0x06` | 3 / 0 | – | 1 / 0 | – |

`003962F0` takes no axis, so mode 2's axis bytes have no effect.

Which draw path each lit pass runs on:

| type | mode | draw path (slots) |
|---|---|---|
| `0x05` | 1 | `00438860` 24, inline 30 |
| `0x05` | 2 | `00437130` 8, `00438860` 95, inline 49 |
| `0x05` | 3 | `00438860` 17, inline 4 |
| `0x05` | 4 | `00438860` 36, inline 65 |
| `0x04` | 2 | `004434D0` 16 |
| `0x06` | 1 | `00444340` 3 |
| `0x06` | 3 | `004434D0` 1 |

So in shipped data:
- `00437130` meets only mode 2;
- `004434D0` meets modes 2 and 3;
- `00444340` meets only mode 1.

Distinct assets with a lit pass:
- type 0x05: mode 1: 37, mode 2: 70, mode 3: 9, mode 4: 33;
- type 0x04 mode 2: 14;
- type 0x06: 1 for each of its modes.

Elements with a lit slot, by path:
- type 0x05: `00437130` 3, `00438860` 121, inline 101;
- type 0x04: `004434D0` 16;
- type 0x06: `004434D0` 1, `00444340` 3.

**The planar scalar of the 152 type-0x05 mode-2 slots.** Its track's kind bytes (`+0xC`, `+0xD`) are 0 / 0 in 21 of
them, which makes it the constant 0.0: `004309C0` returns 0.0 when both bytes are 0. Of the rest:
- 102 are 1 / 0 (a resource's float);
- 29 are other track kinds.

The type-0x04 mode-2 slots are 1 / 0 in 12 and 3 / 0 in 4.

## What stays open

- **What the matrices hold at draw time.** `02AEEA20` serves modes 1 and 3, `02AEEBF0` modes 2 and 4, and `02AEEAA0`
  holds mode 1's V. This is a runtime question. The census now says which matrix each shipped pass uses: modes 1 and 3
  in 79 slots, modes 2 and 4 in 269.
- **The planar scalars that are not constant.** Resource and curve tracks: the `004309C0` / `00430540` / `004307C0` kinds
  are not decoded.
- **The runtime pass index.** The census numbers passes as if every texture lookup succeeds. At runtime a failed lookup
  drops the slot, and the passes after it move down (C2).
- **What the alternative paths change.** What `+0x1F1` bit 3 changes in the drawing (`00437130` against inline,
  `00444340` against `004434D0`) is known as a selector only. It is not characterised. The grid paths' matrix
  preparation (no `00397910`; `0039B960` only in modes 1 and 4) is call shape only.
- **Soundness limits.**
  - Section B assumes no write through a non-frame pointer aliases a stack slot it relies on (MSVC frames; escaped frame
    addresses are invalidated at calls).
  - The C1 writer sweep finds displacement-0x1B0 byte stores only, in functions that name `01FD4A78` directly. A write
    through another addressing form, or by a callee handed a block pointer, is not excluded by it. Between the fill and
    the draw, `0026EE00` gets `param + 0x40` and `00431830` gets `param + 0x70 + 16p` and `param + 0x150 + 16p`; its own
    stores reach 16 bytes past each, but its callee `005030F0` was not read.
  - The C2 runs stub every callee.
