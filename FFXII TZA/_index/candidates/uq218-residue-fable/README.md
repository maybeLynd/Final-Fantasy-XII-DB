# UQ-218 motion-entry residue, supplied for the owner (FABLE, Claude Opus 5.5, 2026-09-29)

**Task:** FRONTIER-REQ-FABLE-UQ218-SEMANTIC-RESIDUE, on the SN-1 pattern.
- FABLE supplies evidence and proposed page text here.
- SWE2-DATA keeps
  [`fef-and-motion-entries.md`](../../../17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md) and the
  UQ-218 row, and merges these on resume. Neither is edited here: DATA's ACTIVE claim holds both files.

**The residue, from DATA's last narrowing of the row:**
1. the `+0x100` vec4's downstream read;
2. the `@FMW` arm-0 element meanings;
3. the `@FMC` opcode operands;
4. `+0x44` handle consumers;
5. `0041E580` callers;
6. `+0x31A` / `+0x31C` authoring.

**Item 3 is published:**
- all 33 used ids have a read body (2bde27313);
- the selector kinds are read (106541fd0, `uq218-fmc-selector-kinds/criteria.md`);
- the locomotion classifier is read (4f9d556c5, `classifier.md`).

## 6. Where `+0x31A` and `+0x31C` come from

[`authoring.py`](authoring.py) ([output](authoring.out)) runs D, A and V, FAILS 0, static.

- **D: the copy.** The entry initialiser `0041D220` copies descriptor word `+0x20` to entry `+0x31C`, and descriptor word
  `+0x24` to entry `+0x31A`.
- **A: the descriptor.** `0041D220` has one caller, the admission `0051BA80`. It is reached from exactly two sites: the
  first bind in `00424550` and the re-bind in `00424D80`. Both build the descriptor on the stack:
  - `+0x20` is the **render event** being bound;
  - `+0x24` is `movsx byte [render + 0x413]`.
- **V: the variation.** Render `+0x413` is the actor's **standard-motion variation**. Verb `01AA` `stdmotionvariation`
  (`002E8220`) stores `v << 3` into actor-record `+0x14F` bits 3–7 and mirrors `+0x14F >> 3` to render `+0x413`. The unit
  definition refresh is its other writer (`00238E98`, cited from
  [how the engine chooses 3D or flat movement](../../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)).
  The corpus uses 0, 1 and 2.

**Proposed page text** (DATA's residue bullet "Open only: where `+0x31A`/`+0x31C` are authored"):
> `+0x31C` is the render event bound to the entry, which is the motion slot; `+0x31A` is the actor's standard-motion
> variation, which picks the bank of 80 slots (`slot[80 × group + cmdSlot]`). Neither is stored in the `.ca`:
> - the event comes from the render-event selection;
> - the variation comes from the script verb `stdmotionvariation` or the unit definition, through actor `+0x14F` bits 3–7
>   and render `+0x413`.
>
> `0041D220` copies both from the admission descriptor that `0051BA80` builds at its two call sites
> (`uq218-residue-fable` D, A, V).

## 1. What reads the bone scale at `+0x100`

The final-pose composer, `Skeleton_ComposeFinalPose` `00373860`, reads it (residue.py S). It has one caller (`003705BA`), and the
0x290 records are skeleton bones.
- Unless the bone's byte `+0x280` has bit `0x10`, it passes `&bone+0x100` (`lea r9` at `00373B58`) to `00372610`.
- `00372610` scales the pose's rows by that vec4 with four `00202FE0` calls.

**Read but not pinned by a check** (the subagent reading; FABLE saw the matching instructions):
- The bone's `+0x80` gets the **unscaled** pose, and children use `+0x80` as their parent, so **scale is not inherited down
  the hierarchy**. Only the bone's own final matrix, the one copied through the handle at `+0x284`, carries it.
- A second pass, `003703A0`, scales rows 0–2 of each bone's `+0x80` matrix into 0x40-byte records at `renderRecord+0x6C0`
  for `0017F260`, which is unread.
- The branch with bit `0x10` set multiplies `+0x100` by `+0x1E0` component-wise first.

**Proposed page text** (residue bullet "Open only: the `+0x100` vec4's downstream semantic read"):
> The scale at `+0x100` is read by the final-pose composer (`00373860` → `00372610`). It scales the bone's own final matrix and
> is not inherited by child bones, which take the unscaled `+0x80` (`uq218-residue-fable` S).

## 2. `@FMW` arm 0: frame runs and value runs, in the same byte codec

**Correction to the page.** The page says arm 0 is a one-off keyframe table ("`{1: 110, 0: 1}`, the sole arm-0 record is the
`0x644`-byte `w0258.cm` outlier").
- [`arm0_census.py`](arm0_census.py) ([output](arm0_census.out)), re-run by FABLE over the extract's 4,230 `.cm`/`.ca` files,
  finds arm 0 in **727 `.ca` entries** (arm 1: 17,576) and in one `.cm` entry.
- That `.cm` entry is `ps2data/obj_finish/in/treasure/t0006.cm` @ `0xC0C0`, length `0x644`. The page's `w0258.cm` may be the
  VBF index's name for it, which is not checked here.
- The `{1: 110, 0: 1}` split counted `.cm` files only.

**The layout** (the subagent reading of `0041B3A0` / `0041B460` / `0041B920` / `0041BB00`; the codec is pinned by W, the rest is
not pinned):
- The descriptor header is `{u32 frameCount (bit 31 = extended), u32 nA, u32 nB [, u32 nC + nC × 0x1C records]}`.
- A records (8 bytes) are `{u32 streamOff, u16 0, u16 keyCount}`: the frame runs, with `frame += literal` starting from 0.
- B records (16 bytes) are `{u32 streamOff, u16 0, u16 keyCount, f32 bias, f32 scale}`: the value runs, with `v0 = bias +
  lit·scale`, then `v += lit·scale`.
- Both are decoded by arm 1's flag-byte codec: low 6 bits are the run length, `0x80` means s16 literals, `0x40` means repeat.
- The subagent's corpus control (50,768 inline and 19,673 extended channels) found every frame run starting at 0, ending at
  `frameCount − 1` and strictly increasing, with `nA == nB` and every stream inside its entry. FABLE did not re-run that
  control.

**Correction to the page, both arms: the s16 literal is little-endian** (residue.py W). The high byte comes from `p + 2 + 2i` and
the low byte from `p + 1 + 2i`, in the arm-0 reader (`0041B412` / `0041B41F`) and the arm-1 reader (`0041B7C6` / `0041B7D3`). The
page's "`0x80` = s16 big-endian literal" is wrong for both. Any census that decoded the literals big-endian decoded wrong
values, though counts and lengths are unaffected.

## 4 and 5. The effect ticket at `+0x44`, and `0041E580`'s callers

(residue.py E, C; the object is the resource entry, a 0x50-byte bank row.)
- **The four spawn sites are all load-completion callbacks** (C), each registered by `lea`:
  - `002E4D20`: a script name binding finished loading;
  - `002E4E50`: a per-lane sub-record of the binding;
  - `003DC340`: a motion-cache slot (`02B57F70`);
  - `003DD850`: the `motionread` verb's (`0x00A2`) external-source request.

  So the `@FEF` effect is built when a resource with a name is first loaded. None of the four uses the result.
- **The ticket has five readers, not one** (E):
  - `0040A1B3` → `003B3B10` stamps the `chara\hN.efx` number;
  - `00409CFD` and `00409EB8` → `003B37E0` stop and release the effect when the entry is disposed;
  - **`0041F6FB` → `003B3550` builds the character's render object from the ticket**, once per character record;
  - `005049B3` → the `ret 0` stub.

  The ticket is the **external** effect's handle (the `02B64380` blob). The embedded `EFX0010` payload is a different
  pointer (`@FEF + 0x30`), and it still reaches only the stub, so the page's embedded-payload finding stands.
- **Not pinned by a check** (subagent reading):
  - `003B38B0` returns **0, not −1**, when the ticket pool is empty (`003B38F7`), while the release paths test only for −1;
  - a copy of the ticket's low 16 bits in the effect context (`003B3989`) is read by `0024D330` / `0024D262`.

**Proposed page text** (residue bullet "`+0x44` handle consumers and `0041E580`'s four caller bodies"):
> The four spawn sites are load-completion callbacks (name binding, binding lane, motion cache, `motionread`). The ticket at
> entry `+0x44` is read by the stamp `003B3B10`, by the stop/release `003B37E0` on disposal, by `003B3550` (`0041F6FB`), which
> builds the character's render object from it, and by the binder's `ret 0` stub (`uq218-residue-fable` E, C).

## Page and row changes proposed for SWE2-DATA

| page / row locator | change | evidence |
|---|---|---|
| `fef-and-motion-entries.md` @FMW "`0x80` = s16 big-endian literal" | → little-endian (both arms) | W |
| same, "Corpus-verified `{1: 110, 0: 1}`; the sole arm-`0` record is … `w0258.cm` outlier" | → 727 `.ca` + 1 `.cm` arm-0 entries; arm 0 = frame and value runs in the same codec | arm0_census.py; §2 |
| same, residue bullets for `+0x100`, `+0x31A`/`+0x31C`, `+0x44`, `0041E580` | the proposed texts above | S, D A V, E C |
| same, the `+0x44` ticket (the binder passes it to the stub) | add: the ticket, the external effect, has four live readers, including `003B3550` (character render object); the embedded-payload claim is unchanged | E |
| UQ-218 row | the `@FMC` part answered (2bde27313, 106541fd0, 4f9d556c5); the motion-entry residue answered as above; remaining: the yaw's left sign, `0017F260`'s use of `+0x6C0`, the extended descriptor's 0x1C records | this record |

Regression: authoring.py D A V; residue.py E C S W (W rejects big-endian; E rejects "the stub is the only reader"); arm0_census.py
(counts). run: authoring.py, residue.py and arm0_census.py at 25ffc9f4b, FAILS 0 / counts as printed.
