---
system: The focus point of a character - the point on a body that others look at and the camera aims at
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the per-frame body 003E43D0, its four helpers (003E5ED0, 003E5FA0, 003E6070, 0046FAA0), the two chunk
    lookups (004234B0, 00423510) and one getter (003E5810) disassembled whole; the ease table and the smoothing constant read from the image;
    consumers found by a displacement sweep of record +0x670..+0x688 and a raw call sweep of the getter family
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-focus-point-falsification-pass-1
  note: written by FABLE from the uncredited-body breakdown (003E43D0, 814 bytes, was uncited and
    unresolved); pending first review
---

# The focus point of a character

Every character render record keeps one world-space point, recomputed each frame, that stands for *where this
character is* to anything that needs a point rather than a body: the look solver of **another** character turning its
head toward this one, the camera code that reads the viewer matrix, a handful of actor services. It lives at
`+0x660`..`+0x6A8` of the `0x740`-byte record of
[the character render record array](the-character-render-record-array.md). *Focus point* is this page's name for it;
the image has no name for it.

## 1. What the player sees

When a character looks at another it looks at a point the model's author placed, not at the feet. And when the
source of that point changes - the record's resource gains or loses its own frame block - the point **slides** to the
new place, eased, instead of jumping. That slide is this mechanism. *(Which in-game situations change the source was
not established.)*

## 2. Two places the point can be

`003E5ED0` `(record, out)` (201 B) picks a local offset and reports which kind it is:

- **Kind 1 - the resource's own frame chunk.** `004234B0` (96 B) resolves the record's resource at `+0xF0`, looks in it
  for the chunk tagged **`@FRM`** (`0x4D524640`, through `00408F90` / `00408F80`), and returns the sub-block named by the
  offset at `+0x10` of the chunk's `+0x30` header - or null when the resource has no such chunk or the offset is zero. If
  it returns a block, the offset is the vector at the block's `+0x3C`.
- **Kind 0 - the authored point.** Otherwise it is the three floats at `+0xD4` of the model's authored parameter block
  (the block at record `+0x400`, entered through the offset in its word `+2`).

So what selects the kind is **data**: whether the model resource bound to the record carries an `@FRM` block. In kind 1
the height still comes from the authored point unless bit 0 of the record's byte `+0x66D` is up.

`003E5FA0` `(record, kind, out matrix)` (201 B) then supplies the frame the offset is expressed in. For kind 1, when the
authored block is version 3 or later and names a bone - the first of the three ids at `+0x3A`, `+0x3C`, `+0x3E` that is
not `0xFFFF` - it is **that bone's matrix** (`003710E0` on the record's skeleton; identity if the record has none).
Otherwise, and always for kind 0, it is the record's own world matrix at `+0x180`.

## 3. One frame - `003E43D0` (814 B)

*Who runs it (added 2026-09-19; read whole):* `004288E0` (87 B), a system phase that walks the active-record list -
head index at the record system's `+0x48800`, next at each record's word `+4` - and calls this body on every record
whose `+0x290` bit 1 is clear.

1. Offset and kind from `003E5ED0`; matrix from `003E5FA0` - of which only the **translation row is kept**: the three
   rotation rows are overwritten with the record's own (`+0x180`..`+0x1AF`), and unless bit 0 of `+0x66D` is up the
   translation's height is replaced by the record's `+0x1B4`. So a bone moves the point but never tilts the offset. The
   transformed point goes to **`+0x670`**.
2. **The slide.** The byte `+0x66C` holds two four-bit countdowns, the high nibble for kind 1 and the low nibble for
   kind 0. While the current kind's countdown `n` is non-zero the point is pulled back toward where the *other* kind
   last left it - `+0x690` when the kind is 1, `+0x660` when it is 0 - by `t = ease(n / (8 * [01DFE0B4]))`:
   `point = point + (other - point) * t`. Then the current point is saved as this kind's last position and **the other
   kind's countdown is reloaded to 8 x the frame-rate multiplier** - every frame, so it is always full at the moment
   of a switch. This body never counts a nibble down: the byte is also rewritten by the record's animation-presentation-
   phase update, which was not read here. With `n` at 8, `t` is 1 and the point is wholly the old one; as `n` falls the
   point converges on the new one; at 0 nothing is blended.
3. `ease` is `0046FAA0` (60 B): a 60-entry table at `01F20C80` (count at `01F2053C`), indexed by `t * 59` clamped,
   running from 0.0097 to 1.0. *(Qualified 2026-09-29, OPUS, on SWE2-AUDIT-SPEC's [batch-6 review](../../_index/candidates/auditspec-review-opus-batch6-0929/REVIEW.md) section 3: the count is 60 in the image, the `FrameLimit=30` state. Under `FrameLimit=60`, `001EDDC0` calls `0033F020`, whose first callee `0046FBF0` doubles `01F20538` and `01F2053C` (`add eax, eax`, `0046FC29`..`0046FC3F`) and has `0033E5E0` rewrite `01F20AA0` and `01F20C80` in place to 120 entries; each has exactly 120 floats of room. The index is `t * (count - 1)`, so `t * 59` or `t * 119`.)*
4. **A second, smoothed vector.** `003E6070` `(record, out)` (211 B) fetches another local vector: `+0x60` of the same
   `@FRM` block if there is one; else from the `@FRM` chunk of the bound resource behind `+0x69C` (replaced by the one
   behind `+0x430` when the record's `+0xCC` low twelve bits equal `0x36`) - `00423510` (85 B) is the same chunk lookup on
   a resource passed in, taking the sub-block from the header's `+0xC` instead of `+0x10`; else the authored floats at `+0xEC`;
   else zero. `003E43D0` low-pass filters `+0x680` toward it: `v += (new - v) * sqrt(0.12)`, about 0.35 a frame -
   or, when bit 1 of `+0x66D` is up, snaps to it once and clears the bit. The dword `+0x6A8` receives `003E6070`'s
   return value, which is 0 on every path.

## 4. Reading it

`003E5810` `(record, out)` (160 B) is the getter read here: `out = M * (+0x680) + (+0x670)`, where `M` is `003E5FA0`'s
matrix for the kind stored at `+0x6A8` (so, the record's own matrix) and the smoothed vector is transformed as a
direction. Three sibling getters sit beside it and were not read.

**Who asks.** A raw call sweep of the four getters finds `RelationLook_SolveAnglesAndMatrices` - the solver of
[the look controller](the-staged-look-command.md) - the two bodies that read the viewer matrix at `02AEDF00`, four
actor-service functions and two UI bodies. That set of consumers is why this page calls it the focus point.

## 5. Behaviour a reimplementation must keep

1. The point is recomputed every frame from a bone or from the root; nothing caches it across frames except the two
   last-position triples used for the slide.
2. A change of kind never jumps: it starts at the last point of the other kind and converges, eased, as the
   countdown (started at eight, scaled) falls.
3. The second vector is smoothed at about 0.35 a frame and can be snapped once by bit 1 of `+0x66D`.

## 6. What is not known

- Which shipped resources carry an `@FRM` chunk - that census would say which characters are kind 1 - and what the
  rest of the block holds.
- Where the countdown nibbles of `+0x66C` are decremented.
- What the second vector is in the game's vocabulary.
- The three sibling getters, and what each consumer does with the point.
- Static evidence throughout.

## 7. Where each behaviour is in the bytes

| body | what is there | at |
|---|---|---|
| `003E43D0` (814 B) | offset, kind, matrix, optional height, transform into `+0x670` | `003E43FE`, `003E440F`, `003E4414`, `003E4441`, `003E445A` |
| | kind 1: countdown from the high nibble, ease, blend toward `+0x690` | `003E446F`, `003E449D`, `003E44AD`..`003E44FD` |
| | kind 1: save to `+0x660`, reload the low nibble with 8 x multiplier | `003E4505`, `003E4514`, `003E4535` |
| | kind 0: low nibble, ease, blend toward `+0x660` | `003E4546`, `003E4571`, `003E4581`..`003E45D1` |
| | kind 0: save to `+0x690`, reload the high nibble | `003E45D9`, `003E45F1`, `003E460F` |
| | second vector, snap bit, `sqrt`, the three filtered components | `003E461D`, `003E462F`, `003E4650`, `003E4684`, `003E46B0`, `003E46D4` |
| `003E5ED0` (201 B) | `@FRM` block test; authored block fallback at `+0xD4` | `003E5EEE`, `003E5F10`, `003E5F1C` |
| | height rule; kind returned | `003E5F5C`, `003E5F6B` |
| `003E5FA0` (201 B) | version test, the three bone ids, bone matrix, identity, root matrix | `003E5FCD`, `003E5FD2`, `003E6031`, `003E603B`, `003E604C` |
| `003E6070` (211 B) | the block's `+0x60`; the two bound resources and the `0x36` test; authored `+0xEC` | `003E608F`, `003E60A6`, `003E60FB`, `003E60C8` |
| `003E5810` (160 B) | matrix for the stored kind, transform of `+0x680`, add `+0x670` | `003E5831`, `003E585F`, `003E5864` |

## 8. Related

- [The staged look command](the-staged-look-command.md) - the look solver is this point's first consumer.
- [How a character fades - the ten channels](how-a-character-fades-the-ten-channels.md) - neighbouring bytes of the
  same record.

## SWE2-EC7-83 update (2026-09-20) - `004234B0` + `0046FAA0` measured

`004234B0` (96 B) is the FRM-section fetch the focus-point callers
run: `[rcx+0xF0]` resolves through `0020E600` then `003AB7F0`, and on
a live block `00408F90(rax, 0x4D524640)` finds the `FRM@`-tagged
entry (`-1` early-out); `00408F80(rbx, idx)` returns the record and
`[rec+0x30]+0x10` folded into `ecx` is the result - 0 on every dead
path.
Interior anchor `004234DC` (the `00408F90` tag find).

`0046FAA0` (60 B) is the second scalar-to-table sampler sibling of
`0046FBB0`: ~~`cvtsi2ss(word[01EFAB4C]-1) * xmm0` truncates, clamps
`[0, count-1]`, and returns `float[01EFAC80 + i*4]`~~ **`cvtsi2ss(dword[01F2053C]-1) * xmm0` truncates, clamps
`[0, count-1]`, and returns `float[01F20C80 + i*4]`, the 60-entry table of section 3 (corrected 2026-09-29, OPUS
falsification pass 1, `CON-178`: the count is a dword, and `01EFAB4C` / `01EFAC80` are neither sampler's; the sibling
`0046FBB0` reads `01F20538` / `01F20AA0`)** - a unit-float
to one of the tabled weights, call-free.
Interior anchor `0046FAD6` (the table `movss`).

## Falsification pass 1 — 2026-09-29 (OPUS): the mechanism survives; the appended note's table addresses do not

**Attack.** Sections 2, 3 and 7 became checks at their instructions, including the appended SWE2-EC7-83 note. Script:
`Tools/analysis-kit/gfz-scripts/falsify_focus_point.py`, output `falsify_focus_point.out`, image `73461d08…`, 0 BROKEN,
exit 0. Section 6's open items are untouched.

| # | Clause attacked | Result |
|---|---|---|
| K1 | the EC7-83 note: `word[01EFAB4C]`, `float[01EFAC80]` | **refuted** (`CON-178`): `0046FAA0` loads a dword count from `01F2053C` (60) and indexes `01F20C80` (0.0097 .. 1.0), as section 3 says; neither sampler reads the note's addresses |
| F0 | section 7 sizes | **survives**: all nine |
| F1 | section 2 | **survives**: `[rcx + 0xF0]` resolved, tag `0x4D524640` (`@FRM`), then `rec + 0x30` and its `+0x10`; the twin reads `+0xC` |
| F2 | section 2 | **survives**: the version-3 test, the three bone ids, the bone-matrix call |
| F3 | section 3 | **survives**: the point stored through `rdi = rcx + 0x670`; `+0x66C`, `+0x6A8`; the `8 × [01DFE0B4]` reload |
| F4 | section 3 | **survives**: `003E6070` returns 0 |
| F5 | section 3 | **survives**: the `+0x290` gate precedes the per-record call |

Corrected in place: the EC7-83 note. The consumer record is `_index/candidates/focus-point-falsification-pass-1-0929/`.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Resource — SERVICE and MECHANICAL (16 edges).** The two frame-chunk lookups `004234B0` and `00423510` call the Resource-filed pair `00408F90` (an 8-byte tail into the tagged-chunk finder `00408FA0`, used with the `@FRM` tag) and `00408F80` (a 10-byte tail into the chunk-record getter `004090D0`); and the handle resolver `003AB7F0`, which `004234B0` runs on the record's resource at `+0xF0` (an aligned pointer passes through, a tagged one is resolved to a live block or 0), is called by ten resource bodies: `ResourceTable_ResolveEntryByIndex` (`002ED570`), `ResourceEntry_GetResolvedBasePointer` (`00409600`), `ResourceEntry_FindSectionIndexAndOffset` (`00409780`), `00409A60`, `00409FE0`, `0040A210`, `0051FBB0`, `0051FCF0`, `0051FE30` and `0051FF30`. Kind 1 of the focus point reads its frame chunk out of the character's resource through the resource layer's own chunk finder and handle resolver; the resource layer owns the file layout, this page only the chunk's meaning.

**CoreRuntimeScheduling — CLIENT, OUT-OF-SCOPE (2 edges).** The boot frame-base selector `0022BDF0` (it computes `FrameLimit == 1` and tail-calls on) reaches the frame-base writer `001EDDC0`, and `001EDDC0` calls `0033F020`, the entry of the ease-table rescale that item 3's 2026-09-29 qualification describes. The engine's boot-time frame-limit setup is what resizes the ease table under `FrameLimit=60`; the focus point only reads that table, so the crossing is the table's size, not any scheduling this page owns.

**Movement — OUT-OF-SCOPE (1 edge).** `001EDDC0` also calls the Movement-owned `00337A00`, which reads the same frame multiplier and stores two locomotion globals from it, an integer 240 × multiplier and a float 2 / (30 × multiplier). It is a sibling of the ease-table rescale in the same frame-limit setup and plays no part in computing the focus point.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-focus-point-of-a-character-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0040A210` | 28 B | stores a 99-byte helper's result for qword `+0x30` of `rcx` at qword `+0x38` of `rcx` | `0040A219`, `0040A21D`, `0040A222` |
| `00423510` | 85 B | returns 0 when a 99-byte helper (`rdx`) returns null, when an 8-byte helper (that pointer, `0x4D524640`, 0) returns -1, when the sign-extended result of a 10-byte helper (that pointer, that index) plus `0x30` is zero, or when dword `+0xC` at that sum is zero; otherwise returns that dword plus the low 32 bits of the sum | `00423519`, `00423531`, `00423540`, `0042354E`, `00423555` |
| `004288E0` | 87 B | starting from the index in dword `+0x48800` of qword `022C6F28` and stopping at -1, walks `0x740`-byte records at that base, calling `003E43D0(record)` (and re-reading qword `022C6F28`) for each record whose byte `+0x290` has bit `0x2` clear, and takes the next index from the record's sign-extended word `+0x4` | `004288EB`, `00428903`, `0042890E`, `00428917`, `00428923` |
