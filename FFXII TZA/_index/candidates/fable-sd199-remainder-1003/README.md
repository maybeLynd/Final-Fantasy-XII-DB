# SD-199 remainder: the compare and the zero entry, settled at the bytes (FABLE, 2026-10-03)

**Asked.** [`fable-sd197-sd199-1003`](../fable-sd197-sd199-1003/README.md) narrowed SD-199 to two questions:

1. What does the "per-vertex compare" at `0039A0C6` (in `00399B80`) and `0039A6C8` (in `0039A150`) test?
2. Does `0039A150` ever write a vertex entry whose first qword is zero? That is the only trigger of the zero-corner
   drop in `00437130` / `00444340` (A-1 / B-1).

**Short answer.**
1. Both compares are the same per-vertex range test. The vertex is projected to integer screen coordinates. The test
   passes only if X and Y lie in 0…0xFFF0 and Z lies in 0xFF…0xFFFFFF. It is not a loop test. The loop test is a
   separate compare.
2. **Yes.** For a vertex that fails the test, `0039A150` stores `$zero`'s low qword. That is 0. A passing vertex's
   qword always has 0xFF as its top byte, so a passing vertex never produces 0. The entries are the corners that
   `00437130` and `00444340` test.

**SD-199 can be closed as ANSWERED.**

| file | what |
|---|---|
| `check_sd199b.py` / `.out` | 133 PASS lines, FAILS 0. Static anchors, two image-wide sweeps, the original bytes of both functions executed under Unicorn (10 edge vertices and 2,000 random ones against a float32 model), 3 controls |

run: check_sd199b.py at 015712a7a, FAILS 0 (about 8 s; no inputs besides the shipping image, sha256 `73461d08…21f8`,
checked by `rvlib.py`)

The register names follow [the register-bank page](../../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md).
GPR[k] is at `022D8F10 + 16k`, so `$zero` = `022D8F10`, v0 = `022D8F30`, t0…t5 = `022D8F90`…`022D8FE0` and
t7 = `022D9000`. Vector rows 1–4 are at `022D91B0`. Both functions are translated PS2 assembly, a VU0 transform
followed by MMI packing. The "clip-flag-style globals `022D8F90`–`022D8FE0`" in the earlier record are GPR t0–t5.

## FABLE: the structure of both transforms

The two functions have the same signature and the same arithmetic. They differ only in what happens when a vertex
fails the test.

**Inputs.**

| register | meaning |
|---|---|
| `rcx` | float4 vertices, stride 16 (only x, y and z are read) |
| `rdx` | the output entries, stride 16 |
| `r8` | a float array that receives Q, stride 4 |
| `r9d` | the vertex count |

The input and output pointers advance through their home slots: `[rsp+0x50]` / `[rsp+0x58]` in `00399B80`, and
`[rsp+0x70]` / `[rsp+0x78]` in `0039A150`.

**Before the loop.** The caller loads the matrix into rows 1–4 (`0039B550`). Both bodies are call-free and each has
one `ret` (S0).

**Each vertex, in order (both functions):**

1. **Transform.** `P = x·row1 + y·row2 + z·row3 + 1.0·row4`, where 1.0 is vf00.w at `[01EF93FC]`. Then
   `Q = 1.0 / P.w` (`divss`: `00399DA3` / `0039A34B`). The scale constant is `[01CEBC84]` = 16.0. The integer
   coordinates are:
   - `X = cvtt(P.x·Q·16)`
   - `Y = cvtt(P.y·Q·16)`
   - `Z = cvtt(P.z·Q)`

   These are the three `cvttss2si`. t0 receives (X, Y, Z, Q bits).
2. **Q store.** Q is stored to `[r8]`, and r8 advances by 4 (`00399EAD` / `0039A4A7`). This store comes before the
   test, so a failing vertex still gets its Q.
3. **Clamp.**
   - t4 holds the low bounds (0, 0, 0xFF, 0); it is built as `$zero | 0xFF`.
   - t2 holds the high bounds (0xFFF0, 0xFFF0, 0xFFFFFF, 0); it is built from `$zero | 0xFFF0` and t3 = 0xFFFFFF.
   - `t1 = PMINW(PMAXW(t0, t4), t2)`. These are the two 4-lane signed loops: `00399EC0`–`00399F0F` and
     `0039A4C0`–`0039A50F`.
4. **The compare value.**
   - `t0 = PCEQW(t0, t1)`: each lane is −1 if the clamp left it unchanged and 0 otherwise. This is the
     `setne` / `dec` sequence at `00399FA0`–`0039A002` and `0039A5A0`–`0039A602`.
   - The four lanes are packed to halfwords.
   - The result is ORed with t5 = 0xFFFF000000000000, which forces the Q lane to "unchanged".
   - Then 1 is added (`inc`: `0039A087` / `0039A68E`).

   The result is 0 exactly when the clamp changed none of X, Y and Z.
5. **The compare** at `0039A0C6` `cmp rcx, rax` and `0039A6C8` `cmp rax, rcx`. The other operand is `$zero`'s low
   qword (`movups xmm4, [022D8F10]` at `00399F1A` / `0039A51A`, then `movq`).
6. **The packed entry** for a passing vertex:
   - the clamped lanes as halfwords, ORed with the X and Z dwords and with t3 = 0xFF00000000000000;
   - the result is `X | Y<<16 | Z<<32 | 0xFF<<56`;
   - this is stored as the entry's first qword.

   This is the GS XYZF layout: X and Y are 16-bit 12.4 fixed point, Z is 24 bits and F is 0xFF. The layout name is
   my reading of the bit positions; the bit positions themselves are executed (E1, E5).
7. **Loop test, a separate compare.** `movsxd rax, r9d` is compared against `$zero` after `dec r9d`:
   - `00399B80`: `0039A107` `cmp rax, r10`;
   - `0039A150`: `0039A6E1` / `0039A723` `cmp rax, r8`.

   The back edges are `0039A111` and `0039A6EB` / `0039A72D` (S4).

**Neither function writes an entry's second qword** (S1, S2, E1). The only stores through a pointer are the entry
qword(s) and the Q dword. Everything else goes to the register bank or the frame.

**How each function handles a failing vertex:**

| | `00399B80` (bit 3 clear) | `0039A150` (bit 3 set) |
|---|---|---|
| compare | `0039A0C6` `cmp rcx, rax`, `0039A0C9` `jne 0x39a122` | `0039A6C8` `cmp rax, rcx`, `0039A6CB` `je 0x39a6f0` |
| passing vertex | packs and stores at `0039A0F6`, continues | jumps to `0039A6F0`, packs and stores at `0039A712`, continues |
| failing vertex | leaves at once. It returns v0 = `$zero \| 1` = **1** (`0039A122`). The failing entry and all later entries are never written | **falls through to `0039A6CD` `mov qword ptr [r11], rcx` with rcx = `$zero`, so the entry is 0**. It continues with the next vertex |
| all pass | returns `$zero` = **0** (`0039A116`–`0039A11D`) | — |
| return value | 0 or 1 | always v0 = `$zero \| 1` = 1 (`0039A3A9`, `0039A3E1`, `0039A732`); every caller ignores it |

## FABLE: answer 1, what the compare tests

**It tests one vertex: whether its projected integer coordinates fit.**
- X and Y must lie in [0, 0xFFF0], which is [0, 4095.0] in 12.4 fixed point.
- Z must lie in [0xFF, 0xFFFFFF].
- The Q lane is masked out.

**What fails, and what does not:**
- NaN, ±inf and anything outside int32 fail, because `cvttss2si` returns 0x80000000, which the clamp changes. This
  includes w = 0.
- The test is not a frustum test. In E5, 405 vertices with w < 0 passed it, because their projected coordinates
  landed inside the window.
- Truncation runs toward zero, so x·Q·16 in (−1, 0) gives X = 0 and passes (E1, "x = −0.03").

The loop/count test is the separate compare against the decremented `r9d` (point 7 above).

**"One failing vertex rejects the whole element" holds for bit 3 clear.**
- `00399B80` returns 1 at the first failing vertex, wherever it sits (E2, E4). Bit-identical results over 400 random
  single-vertex calls (E6).
- Its callers turn that into a whole-element skip (`check_sd199.py` T1 / T2): the mesh preps return 0 and
  `004355D0` returns before its path ladder; the grid walks jump past both draw calls.

## FABLE: answer 2, `0039A150` writes zero entries

**Every store to an entry's first qword.** `0039A150` has exactly two stores through `r11`. `r11` starts at rdx and
advances by 16 through `[rsp+0x78]` (S2).

| site | arm | value | can it be 0? |
|---|---|---|---|
| `0039A712` | test passes | `[t2] \| [t1] \| [t3]`. t3's only writers are `0039A1EA` (0xFFFFFF, read by the bound build) and `0039A3C3` (0xFF00000000000000, after it) | **No.** The top byte is always 0xFF (S3, E1, E5) |
| `0039A6CD` | test fails | rcx = `$zero`'s low qword, `0039A51A` → `0039A6B1` → `0039A6CD`, straight-line code (S3) | **Always.** `$zero` is 0 (below) |

**`$zero` is 0.**
- **Z1:** an image-wide raw sweep finds **no writer** of `022D8F10`–`022D8F1F`. The sweep covers rip-relative,
  absolute and image-base-relative disp32, confirmed at instruction boundaries.
- **Z2:** all 11 instructions that take its address pass it in `rdx` to `003CCA70`, which stores only through `rcx`.
- **Z3:** the cell lies past `.data`'s raw data (`01F7E400`), so it is zero at load.
- **Sensitivity:** on a patched image with a planted writer at `0039A0F9`, the sweep finds it (C3).
- **Not covered:** stores through a computed pointer whose base is not `022D8F10`. The nearest such family is the
  heap counter array at `022D8E10`, indexed by a block byte (`0036C60C`, `0036D0FE`). It would reach `022D8F10` only
  at index 64, while a separately addressed global sits at index 16 (`022D8E50`).
- **The bodies need it to be 0.** Both loops end on `count == $zero`, so a non-zero `$zero` would not end them at the
  count.

**Input condition for a zero entry.** With bit 3 set, the entry of vertex k is 0 **exactly when vertex k fails the
range test**. Executed:
- 6 of the 10 edge vertices: x < 0, X = 0xFFF1, Z = 0xFE, Z = 2^24, NaN, Y over (E1);
- 1,218 of 2,000 random vertices, bit-exact against the model (E5).

The inputs were vertices `(x, y, z, 1.0)`, rows 1–4 written directly (identity rows for E1–E4, a perspective-like
matrix with seeded noise for E5/E6), `$zero` at its load value, and count = number of vertices.

**Sensitivity.**
- On a patched image whose failing arm stores the compare value (`rax`) instead, E1 fails (C1).
- A model with the wrong bounds (X/Y max 0xFFFF, Z min 0) disagrees with the executed bytes (C2).

**The buffer is the one the drawers test (B1–B3).**
- **Mesh:**
  - Both preps call `0039A150` with rdx = `[02AEED50] + 32·word[+0x16]`: `0043511F` in `00435050`, and
    `00434E01` / `00434E04` (in place) in `00434CD0`.
  - `00437130` builds `r14 = [02AEED50] + 16·w + 16·w` (`00437160`–`00437191`) and loads corner idx from
    `[r14 + 16·idx]` (`00437862`) into `[rbp+0x60]`, the qword tested at `0043789C`.
  - `004355D0` hands the same element (`rsi`) to the prep and to `00437130`, and no path between them writes rsi.
- **Grid:**
  - Each walk transforms in place on rcx = rdx = `[02AEED58]`: `0044578A`, `00447463` and `00448426`.
  - `00444340` reads its corners from `[02AEED58]` (`00444366` → `00444B90`) and tests them at `00444BD5`.
- **Pointer writers:**
  - `02AEED50`'s only writer is `0039CD6B`.
  - `02AEED58`'s writers are the prep (`00434D62`) and the walks before their transform (`004454FD`, `004471BF`,
    `00448073`). None is in either drawer.

**One exception on the mesh side.** When `0024E410` (the tagged-record window probe) returns non-zero, the
bit-3-only block after `0039A150` overwrites the X/Y words of the first entries:
- 4 entries in `00435050` (`0043514C`);
- 6 entries in `00434CD0` (`00434E25`).

Those entries are then non-zero even when their vertex failed the test, so their corners are not dropped.

## FABLE: what this closes in SD-199

**With A-1 / B-1 now tied to a vertex condition, what bit 3 changes in the drawing is fully stated:**
- **T + A-1 / B-1, one condition behind both.** A vertex fails when its projected X or Y falls outside
  [0, 0xFFF0] (12.4 fixed point) or its Z outside [0xFF, 0xFFFFFF]. This includes NaN and overflow.
  - **Bit clear:** one failing vertex suppresses the whole element (`00399B80` returns 1).
  - **Bit set:** a failing vertex becomes a zero entry, and `00437130` / `00444340` drop only the primitives that
    use it as a corner. Every other primitive is drawn.
- **A-2:** the inline path's 1/1.15 and ×1.15 rescale of the pass pair. This was already settled as drawn.
- **The `0024E410` override:** it runs only on the bit-3 arm and can keep the first 4 or 6 corners from being
  dropped.

**Recommendation: ANSWERED.** Static and executed (the original bytes under Unicorn); nothing was run against the
game.

**Outside the row (not open questions of SD-199):**
- **Runtime frequency.** How often shipped effects actually put a vertex outside the window or depth range. That is a
  live-data question.
- **The second qword.** Entries carry a second qword that the transform never writes. What `00437130` does with it
  is not read here.
- **The bit-7 path.** `00438860` takes precedence over bit 3 at `00435677`, and it is not part of this row. A linear
  decode of its 20,603 bytes (not part of the check) finds 18 calls to `0039A150` and none to `00399B80`, so that
  path always uses the zero-entry transform.

## FABLE: corrections to route

1. **[`fable-sd197-sd199-1003`](../fable-sd197-sd199-1003/README.md)** has two errors:
   - Its "Recommendation" section, and `page_section.txt`'s "still open" bullet, say the failing arm stores
     `[022D8FB0] | [022D8FA0] | [022D8FC0]` and is "non-zero on a first reading". **That is the passing arm**
     (`0039A6F0`, reached by `je`). The failing arm is the fall-through at `0039A6CD`, which stores `$zero`.
   - Its classification table says A-1 / B-1 are "DRAWN when they fire" and that "whether any entry ever has a zero
     first qword is not established". **They fire on every vertex that fails the range test.**
2. **[the-two-transform-primitives.md](../../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)**
   (around the `00434CD0` paragraph) has two errors to route to its owner:
   - It calls `0039A150` / `00399B80` "the scalar-blend members of this family". **They are the
     perspective-project, range-test and XYZF-pack transforms.**
   - It says "`00399B80` may return 0 early". **It returns 1 on a failing vertex; the prep then returns 0.**
3. **The kind-`0x54` page's SD-199 bullets** (`page_section.txt`) should replace "still open" with answers 1 and 2
   above.

No tracked file was edited for this record.
