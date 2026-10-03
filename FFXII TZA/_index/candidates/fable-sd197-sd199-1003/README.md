# SD-197 and SD-199: the cloud drafts checked against the image (FABLE, 2026-10-03)

**Asked.** Two cloud sessions drafted answers to the registered rows SD-197 (the planar-scalar tracks `004309C0`,
`00430540`, `004307C0`) and SD-199 (what `+0x1F1` bit 3 changes in the drawing beyond picking the path). The drafts
are not evidence. This record re-derives every load-bearing claim from the shipping image and states which claims
passed, which failed and which could not be checked.

The image is `Database/Tools/work/exe/FFXII_TZA.exe`, sha256 `73461d08…21f8`, checked by `rvlib.py`. That file is
imported unchanged from `fable-review-astra-ov42-caller-quotient-bound-1002`. Addresses are VAs with the image base
included.

| file | what |
|---|---|
| `check_sd197.py` / `.out` | 214 PASS lines, FAILS 0. Static anchors; the original bytes executed under Unicorn against a float32 reference model; 5 controls; the shipped data |
| `sd197_planar_tracks.tsv` | one row for each of the 152 type-`0x05` mode-2 pass slots: track kinds, selectors, combine mode, periods, keys, and the executed min/max over time |
| `check_sd199.py` / `.out` | 152 PASS lines, FAILS 0. Static anchors, CFG reachability, whole-body censuses, one Unicorn run of the builder `0039B860`, the shipped population, 5 controls |
| `draft_sd197.txt`, `draft_sd199.txt` | the cloud drafts, copied unchanged under an UNVERIFIED label |

run: check_sd197.py at 51dc0cb0b, FAILS 0 (about 45 s; reads `D:/FFXII_TZA_extract` through `members/type_census.py`)
run: check_sd199.py at 51dc0cb0b, FAILS 0 (about 10 s; section P reads `../fable-k54-residue-1003/k54_modes.tsv`, which is still untracked)

Stubs: the only non-original code that runs is `00861F14`, the `sqrtf` import thunk, replaced by a correctly rounded
float32 sqrt. `00808C40`, the stack-cookie check, is replaced by `ret`. In section E of `check_sd197.py`, `003D8E50`
is replaced by a deterministic recorder so that each combine formula can be checked exactly; E8 then runs the real
`003D8E50`.

---

## SD-197: the planar scalar's track

### The verified answer (everything below PASSED)

**The three addresses are not three track kinds.** They are three layers of one evaluator for one 16-byte record.
For pass p, the walk evaluates the record that sits 0x10 bytes before the pass slot (`00449FEC lea rcx, [rsi + 0x90]`).
The time argument is the element instance's dword `+0x44` (`00449FE8`). The result is stored to `param + 0x1D8 + 4p`
(`0044A017`).

**The record.** Nothing at `+0x10` or above is read. To show this, every run placed the record's last byte at the
end of a mapped page and none of them faulted (E3). Control C5 maps only 14 bytes and the run does fault.

| offset | width | meaning | read at |
|---|---|---|---|
| `+0x0` / `+0x4` | dword | channel 0 / channel 1 key handle, resolved by `0020E600` | `004309E6`, `00430A1F`, `0043056C`, `00430579` |
| `+0x8 + 2c` | u16 | channel c's loop period (0 means no loop) | `0043058E` |
| `+0xC + c` | u8 | channel c's key count | `004309CA`, `004309FF`, `004305C9`, `0043074A` |
| `+0xE` | u16 | bits 0-1 / 2-3: channel 0 / 1 interpolation selector; bits 4-7: combine mode m | `00430573`, `00430581`, `004307DE`, `0043080F` |

Bits 8-15 of `+0xE` are never read. Flipping them on 800 records changed nothing (E2).

**`0020E600`** is `mov eax, ecx` / `add rax, [01F83530]` / `ret`. It returns the handle zero-extended plus the base
qword (S6). E5 executes it: with base `1_00000000`, handle `80000010` returns `1_80000010`.

**`004309C0`, one channel at a time.**
- A count of 0 gives 0.0.
- A count of 1 gives the float at `+4` of the resolved handle, whatever the time (E6).
- A count of 2 or more calls `00430540`.
- If channel 1's count is 0, the function returns channel 0's value at `00430A19` and the combiner is never called.
- Otherwise it tail-jumps to `004307C0(record, a, b)` at `00430A56`.

**`00430540`, one keyed channel.**
- The keys are 8-byte entries: `{int32 frame, float32 value}`.
- **Looping.** When the period P is non-zero and the time t > P (signed), t becomes t mod P. A time equal to P is
  not wrapped (E7; control C2 rejects the "t ≥ P wraps" reading).
- **Selector 0: piecewise linear.**
  - An exact key frame returns that key's value.
  - Between two keys it returns `v0 + (v1 − v0)·float(t − f0)/float(f1 − f0)`, with the differences taken in
    integer arithmetic.
  - After the last key it returns the last value.
- **Selector 1 with 2 keys or fewer** takes the same linear path.
- **Selector 1 with 3 keys or more: a uniform quadratic B-spline.**
  - It clamps at both ends.
  - A window of three keys is chosen around the time, using the truncated integer midpoint (`00430633`–`00430690`).
  - In the first and last half-segments it falls back to linear.
  - `0039B6E0` solves x(u) = t for u by the quadratic formula, and returns 2.0 when `x0 − 2x1 + x2 = 0`. On that
    sentinel, `00430540` uses `u = (2t − x0 − x1)/(x2 − x0)`.
  - `0039B630` returns `y = ((1−u)u + ½)·y1 + ½(1−u)²·y0 + ½u²·y2` (lane 1).
  - The curve passes through the midpoints between keys, not through the keys themselves. For example, the shipped
    keys `0:-1, 160:-3.5, 320:-1, 450:-1.5` never go below −2.875.
- **Selectors 2 and 3** return 0.0.
- **Stack residue.** On the linear path, a time before the first key interpolates from the unwritten stack slot
  `[rbp−0x25]`, read both as a frame (int) and as a value (float) (E4: 860 cases).
  - When channel 0 took the curve path in the same call, that slot holds channel 0's result. 32 of the E1 cases hit
    this and match the model.
  - With a zero slot and a first key at frame 0, a negative time gives NaN (E7).
  - The curve path never consumes the residue. This includes lanes 2-3 of its three points, which it leaves
    unwritten (E4b: 2,146 cases).

**`004307C0`, the combiner.** The combiner's mode jump table (in `.text` just past its body) gives, for m = 0..5 (S5, read from the image):

| m | arm | result |
|---|---|---|
| 0 | `004307FD` | a |
| 1 | `00430833` | a + F(b) |
| 2 | `0043084E` | a − F(b) |
| 3 | `0043086C` | F(2b) + a − b |
| 4 | `0043088F` | F(b)·a + a |
| 5 | `004307F2` | a if b − a = 0, else F(b − a) + a |
| 6..15 | `004307FD` | a |

- When b = ±0.0 (and is not NaN), every m returns a, except m = 5: then a non-zero a returns F(−a) + a.
- F is `003D8E50`, the render-local scaled random draw that [the RNG streams page](../../../21-RNG-And-Determinism/rng-streams.md)
  already documents. Run unstubbed (E8) with a = 10 and b = 5:
  - m = 1 gives values in [10, 15);
  - m = 3 gives [5, 15);
  - m = 5 gives (5, 10];
  - with b = 0 there is no draw and the RNG state is unchanged.
- So channel 1 adds a random spread around channel 0. m = 3 is "a ± b", and m = 5 is "a random value between a and b".

**The whole stack is executed and matches bit for bit (E1).** 6,000 seeded random records were run on the original
bytes and compared with the float32 model above: 0 mismatches and 0 faults. The scaler was called with exactly the
model's arguments, in order (E1b). Every decoded path was taken at least once, including 177 hits on the 2.0 sentinel
(E1c).

**The shipped planar scalars.** All EFX streams of the full extract were read: 5,204 type-`0x05` elements and 152
mode-2 pass slots (D0, D2).
- Every authored handle of a used channel was resolved as `stored + low32(record) + bias`. Here bias is the chunk's
  `+0x08` i32, which the loader publishes at `02EBB738`; the setup `003A9A70` adds it, and `00431770` applies it to
  bundle `+0x90`/`+0x94` (S7). Every such handle lands inside its own chunk with room for its keys (D1).
- Every key array has strictly ascending frames (D3).
- No slot uses a period (all are 0), and flag bits 8-15 are 0 in all 152.

| what the slot authors | slots | value |
|---|---:|---|
| nothing, kinds (0,0) | 21 | 0.0 |
| one resource float, (1,0) | 102 | a constant: 19 distinct values from −0.4 to 2.4 (1.0 ×27, 0.01 ×17, 0.2 ×11, …) |
| two constants, (1,1) | 10 | m = 5 ×9 (random between a and b) and m = 3 ×1 (a ± b) |
| a keyed curve on channel 0 only | 17 | selector 1 ×15 (14 with 3 to 13 keys, i.e. B-spline; 1 with 2 keys, i.e. linear), selector 0 ×2 (2 keys, linear) |
| keyed curves on both channels | 2 | m = 5: a random value between the two curves |

The keyed slots come from 11 distinct file names (jp and us copies counted once). On the type-`0x05` draw paths they split 00438860 ×19, inline ×8 and
`00437130` ×2 (this count covers the curve and two-constant slots).

The executed range over every time from 0 to the last key, with F at both of its bounds, is −2.875 to 2.4. Each
slot's range is in the TSV.

Every keyed channel's first key is at frame 0. So the stack-residue case cannot be reached for times ≥ 0.

### Draft claims

- **Verified: 34.** These are the record table (offsets, widths, read sites, bits 8-15 unread, at most 16 bytes) and
  every `004309C0` arm and return. In `00430540`: the selector extraction, the key layout, the period rule including
  t = P not wrapped, the linear path and its residue, the curve search, ends, midpoint, five-row window table,
  three-point layout, 2.0 sentinel and lane-1 result. In `004307C0`: the mode bits, the b = 0 branch with ±0.0 and
  NaN, the five arms and their formulas. Also `0020E600`'s body, and the record being the 0x10 bytes before the slot.
- **Failed: 0.**
- **Resolved items the draft left open:**
  - the table mapping above, including its hypothesis that m = 5 enters at `004307F2` (true);
  - what F is (its "uniform in 0..x" hypothesis is right in substance; the exact operation order is on the RNG page);
  - what `0039B6E0` and `0039B630` compute, and that the unwritten lanes are harmless;
  - what `0020E600` returns;
  - the caller's time argument (instance `+0x44`);
  - the shipped selectors, modes, periods and ranges;
  - the residue's reachability in shipped data.
- **Not checked: 2.**
  - The time's unit. Instance `+0x44` is passed unchanged, but what increments it was not read.
  - The body of `00808C40`. It was stubbed; the cookie pattern around it is anchored, and nothing depends on it.

**A correction elsewhere, for FABLE to route.** `how-an-authored-number-gets-its-randomness.md` §6 says `004309C0`'s
"combiner tail `00430540`". The tail is `004307C0` (`00430A56 jmp 0x4307c0`), and `00430540` is the per-channel
curve.

The float twin also differs from the integer twin `004314E0` in three ways:
- its keys are `{int32 frame, float value}`;
- there is no ±0.5 rounding;
- mode 5's equality test is `(b − a) == 0.0` in float.

### Recommendation: ANSWERED

The row asked for the three evaluators to be decoded and the shipped tracks evaluated. Both are done, static and
executed: the stack is executed bit-exact, and all 152 shipped slots are resolved and evaluated.

Two things stay outside the row:
- The time unit (instance `+0x44`).
- The concrete random draws of the 12 slots that use channel 1. They come from the render-local stream and are
  bounded above, not fixed.

---

## SD-199: what `+0x1F1` bit 3 changes

### The verified answer (everything below PASSED)

**The inline path.** It is `00435699`–`00436CFB`.
- It is entered only by `0043568A je 0x435699` (A0c, A0d).
- Everything reachable from its start, stopping at the shared epilogue `00435641`, lies in that range (A0b).
- It leaves only by `00436CFB jmp 0x435641` (A0e).

`00437130` is a whole function, `00437130`–`00438859`, and its `.pdata` tiles it.

**A-1: `00437130` drops a primitive when any of its corners has a zero first qword.** The inline path never does.
- F (`00437130`) has 42 tests in 12 groups: 6 triangle loops × 3 corners and 6 quad loops × 4 (A1a). The inline
  path has none (A1b).
- Each group's `je` lands past that primitive's emitter calls, on the counter block, so the streams stay aligned
  (A1c).
- The draft's 20 F call sites and its 20 inline call sites are all correct (A1d, A1e).
- The four value-1 loops consume their per-primitive byte before the test (A1g).

**A-2: the inline path rescales the pass pair `param+0x50+8p` by (1/1.15, ×1.15); F never does.**
- The rescale happens at `00435D23`–`00435D53` and `00435D71`–`00435DA2`, with xmm6 = `[00D1247C]` = 1.15f.
- **`0053DD10` is `mov eax, 1` / `ret`** (A2c). So the `cmp eax, 1` / `jne` never skips: the rescale always happens
  when the pass's `+0x130` byte is 4 and `+0x1F2` bit 0 is clear.
- F has no call to `0053DD10` and no reference to 1.15 (A2d).
- The pair is r9 for every builder call (A2f).
- **Executed (A2g):** `0039B860` emits `S = (u + pair.x)·q` and `T = (v + pair.y)·q`. So the pair is an additive
  texture-coordinate offset, and the rescale changes the drawn texture coordinates whenever the pair is non-zero.
- The walk rewrites the pair from the slot's tracks before its one draw call (`00449FA0`–`00449FCC`, `0044A15B`).
  So the in-place rescale does not accumulate across frames.
- `+0x130+p` is slot byte `+0`. Byte 4 takes the same texture-lookup arm as byte 2 (`00449CE9`, `00449D30`).

**Nothing else in the two bodies differs (A3).**
- Callee multisets differ only in `0053DD10` (×2, inline), F's own `00808C40`, and 76 against 77 calls of the pure
  `0020E600`.
- The rip-relative globals are the same set apart from `00D1247C` (inline) and F's cookie `01F44830`.
- The non-stack memory operands have identical (displacement, scale, width) sets.
- Frames are 0x210 (shared) against 0x1F0. Both paths return 1.

**B-1: `00444340` drops a grid quad when any corner has a zero first qword; `004434D0` never does.**
- G1 (`00444340`) has 16 tests in 4 quad groups; G0 (`004434D0`) has none (Bb). The draft's six sites on each side
  are correct (Bc).
- Callee multisets, globals and memory-operand sets are identical (Bd–Bf).
- The four constants are 0.0625, 0.001953125, 3.5625 and 3.5 (Bg). Both frames are 0x208.
- The tested qword begins with the two u16 screen coordinates (X at `+0`, Y at `+2`) that the mode-2 term reads.

**T, which the draft missed: the same bit also picks the vertex transform before every one of these draws.**
- **Mesh preps.** `00435050` (`004350FC`) and `00434CD0` (`00434DF1`) call `0039A150` when bit 3 is set and ignore
  its result. When the bit is clear they call `00399B80`. A non-zero result makes the prep return 0, and `004355D0`
  then returns at `0043563F` before its path ladder, so nothing of the element is drawn (T1).
- **Grid walks.** All three walks (`004453D0`, `00447020`, `00447ED0`) test the same definition bit that picks
  `00444340`, and choose `0039A150` / `00399B80` the same way. A non-zero `00399B80` result jumps past both draw
  calls (T2).
- **The two transforms differ at one compare.** `00399B80` leaves at the first vertex whose per-vertex compare is
  unequal (`0039A0C9`). `0039A150` writes an entry on both outcomes of that compare and continues (`0039A6CD`,
  `0039A712`) (T3).
- **So the bit chooses between two ways of handling a failing vertex:**
  - bit 3 clear: one failing vertex rejects the whole element;
  - bit 3 set: the element is always drawn, and F / G1 drop only the primitives with a zero-flagged corner.
- **An override that runs only with the bit set.** In `00435050` and `00434CD0`, the `0024E410`-gated block that
  overwrites the first vertex entries' packed words (`0043514C`, `00434E25`) sits only on the `0039A150` arm.

**Shipped population (P1).** 57 inline type-`0x05` pass slots have `+0x130` byte 4, so the rescale applies to them.
`00437130` elements author none, so no shipped bit-3 element would show A-2.

**Which differences change drawn output.**

| difference | classification |
|---|---|
| A-2 | **DRAWN** whenever `+0x130` is 4, `+0x1F2` bit 0 is clear and the pair is non-zero |
| T (whole-element reject against per-primitive drop) | **DRAWN** |
| A-1 and B-1 | **DRAWN when they fire.** ~~Whether any entry ever has a zero first qword is not established~~ They fire on every vertex that fails the range test (settled the same day in [`fable-sd199-remainder-1003`](../fable-sd199-remainder-1003/README.md)) |
| registers, stack slots, frame size, own or shared epilogue, the `0020E600` count | BOOKKEEPING |

### Draft claims

- **Verified: 24.**
  - The inline bounds, `00437130`'s extent and the shared epilogue.
  - A-1 in full: the 12 loops, all 40 call sites, the skip landing on the counters, and the byte consumed first.
  - A-2's anchors on both arms; F's bit-1 arm and its do-nothing arm; the pair reaching the builders.
  - The same globals, record fields and constants.
  - The grid's identical inputs and constants; B-1 in full; the tested bytes being the u16 X,Y.
  - Return value 1; frames 0x210 / 0x1F0 / 0x208.
- **Failed: 2.**
  - The conclusion that "every other input, kernel, … is the same" and that "the bit's one cross-cutting drawing
    effect is the zero-corner skip". It is incomplete: the draft compared only the draw bodies, and the bit also
    selects `0039A150` against `00399B80` in both preps and all three grid walks (T).
  - "Apart from A-1 and A-2, they call the same callees". The `0020E600` count differs (76 / 77). This is
    harmless, because the function is pure, but the claim is not literally true.
- **Resolved items the draft left open:**
  - `0053DD10` always returns 1, so A-2 is not provisional;
  - the builders use r9 as an additive texture-coordinate offset;
  - the walk rewrites the pair every call, so there is no accumulation;
  - the population: 57 inline slots, 0 on `00437130`.
- **Not checked: 3.** These are not load-bearing.
  - The per-row stack-slot lists in the draft's alignment tables (rows 1, 4, 6 and 8).
  - The per-section address ranges beyond the anchored ones.
  - The draft's grid register-caching remarks.

### Recommendation: NARROWED

> **Superseded the same day (FABLE, 2026-10-03): SD-199 is ANSWERED.** [`fable-sd199-remainder-1003`](../fable-sd199-remainder-1003/README.md) settles both points below at the bytes and under Unicorn (`check_sd199b.py`, FAILS 0). The arms in the bullet below were swapped: `[022D8FB0] | [022D8FA0] | [022D8FC0]` is the PASSING arm (`0039A712`), and the failing arm (`0039A6CD`) stores the zero register, so A-1 and B-1 fire on every vertex that fails the range test.

What the bit changes is now stated in full at the level of code paths: T, A-1, A-2 and B-1, with A-2 settled as
drawn. What remains open is one question:

- **The per-vertex compare.** What does the compare at `0039A0C6` / `0039A6C8` test? It reads clip-flag-style
  globals in a VU-style emulation (`022D8F90`–`022D8FE0`). And does `0039A150` ever write a vertex entry whose first
  qword is zero? That write is the only trigger of A-1 and B-1. Its failing arm stores
  `[022D8FB0] | [022D8FA0] | [022D8FC0]`, and `022D8FC0` is set to `0xFF00000000000000` in the loop (`0039A3C3`). On a
  first reading, the failing arm therefore writes a non-zero qword. If that holds, A-1 and B-1 would fire only on a
  zero packed vertex, not on a clipped one.
- **How to settle it.** This can be done statically, by reading `0039A150`'s flag arithmetic, or by executing
  `0039A150` / `00399B80` on a staged workbench.

---

## For FABLE to decide

1. **Accept SD-197 as ANSWERED.** The registered question calls the three addresses "track kinds". The answer says
   they are layers of one evaluator, and the register row should say so.
2. **Route the §6 correction** on the authored-number page: the combiner tail is `004307C0`, not `00430540`.
3. **Re-scope SD-199 rather than close it.** Either:
   - keep it OPEN, narrowed to the compare and zero-write question above; or
   - split T's "which vertices fail the compare" out as its own row. It is the shared condition behind the
     whole-element reject (bit clear) and the per-primitive drop (bit set).
4. **Commit `fable-k54-residue-1003/k54_modes.tsv` first.** It is still untracked, and `check_sd199.py` section P
   reads it. Publish this record only after it.
