# RC-4 residue closed: nothing in the image can store 1 or 6 into the capture state (ORACLE, 2026-09-30)

## The question

RC-4 (the 282-command console, section 7) asks whether a press on console rows 4 or 5 can start a capture. That
requires a store of 1 or 6 into the render object's capture state `+0xDAC`.

OPUS's record (`../rc4-capture-machine-0930/`, "The derived-pointer census") found no such store by displacement,
derived offset or interprocedural flow. It left four blind classes:
- 66 stores through an object pointer at an unknown offset, 22 of them of an unknown integer;
- 12 self-pointer fields;
- 2 escapes of the object into other objects (`001F1E80` → `+0x18`, `0060CE50` → `+0xA8`);
- 38 virtual calls that receive the object.

The coordinator asked for each class to be closed: bound every index or cursor, model the self-pointer loads, root the
two escapes, and resolve the vtables.

## Method

Five scripts, run in order. All reuse OPUS's `rc4_flow.py` (on `k14_actorflow.py`) unchanged, and extend it by
subclassing. All checks pass.

| script | output | what it does |
|---|---|---|
| [`rc4b_pass1.py`](rc4b_pass1.py) | [`rc4b_pass1.out`](rc4b_pass1.out), [`rc4b_selffields.tsv`](rc4b_selffields.tsv) | OPUS's flow, also recording every exact-offset self-pointer store and vtable store, and every receiver context. The control finds the 5 known stores |
| [`rc4b_pass2.py`](rc4b_pass2.py) | [`rc4b_pass2.out`](rc4b_pass2.out) | the flow with self-pointer loads modelled to a fixpoint, virtual calls resolved through the constructor-stored vtables, the constructors run through the EH vector iterator seeded, and the class-`00902F90` escape rooted |
| [`rc4b_pass3.py`](rc4b_pass3.py) | [`rc4b_pass3.out`](rc4b_pass3.out) | the two escapes into the external object `[A+8]`: the `+0xA8` readers, and the slot-2 call |
| [`rc4b_bounds.py`](rc4b_bounds.py) | [`rc4b_bounds.out`](rc4b_bounds.out) | the hand bound of the 66 unknown-offset stores, each index read from the image |
| [`rc4b_scan.py`](rc4b_scan.py) | [`rc4b_scan.out`](rc4b_scan.out) | a supporting displacement scan, `d = 0xDAC − K`; not needed for the result |

## The object's layout, as the constructors build it

The render object `A` is `new(0xDD8)`, built by `00184F20`:

| where | what | evidence |
|---|---|---|
| `+0x20` | 2 view pairs of `0x338`, via the EH vector iterator `00808FE4` with constructor `00184CE0` | `00184F74` |
| `+0x690` | a third view pair | `00184F8A` |
| each pair | views at `+0` and `+0x190`, vtable `008C5D68` (slot 1 = `00189C20`) | `00184D1F`, `00184DBE` |
| each pair | Phyre sub-objects at `+0x108` and `+0x298`, vtable `00D562A8` stored after the base `00D86B80` | `0062DD19`, `0062DD25` |
| `+0x9C8`, `+0xA50` | two more Phyre sub-objects | `00184F97`, `00184FA4` |
| `+0xC38` | 4 EASTL vector triples of `0x20`, each with its allocator (vtable `00902720`) at `+0x18` | `00184FE1`, `001EDF00` |
| `+0xDAC` | the capture state, 0 from the constructor | `00185020` |

## Result

**RC-4: ANSWERED.** No store reachable from the render object by any route writes `+0xDAC` other than:
- the constructor's 0 (`00185020`);
- the machine's own 3, 4, 0 and 7 (`00187891`, `001878B3`, `001878D5`, `001878E5`).

So nothing writes 1 or 6, and a press on rows 4 or 5 cannot start a capture. Each of OPUS's four classes is closed.

**1. The 66 unknown-offset stores reach at most `A+0xCB0` (`rc4b_bounds.py`, B1-B7).**

| functions | the index or cursor | where the base lies |
|---|---|---|
| `00186CD0` | a loop over `008C5D84`..`008C5DD4` | `A+0`..`A+0x48`, so its stores are at `+0xB90`..`+0xC30` |
| `00185A90` / `001858A0` | vector `A + 0xC38 + 32 * [A+0xCB8]`; the index's only writers are `(i + 1) & 3` (`0018624D`) and the constructor's 0 (`0018715A`) | within `+0xC38`..`+0xCB0` |
| `00188640` | `A + 0xC38 + 32k` with `k < 4` | within `+0xC38`..`+0xCB0` |
| `001897C0` | pair `k = setne al`, which is 0 or 1 (nothing else writes `eax` in between); bases `A + {0x20, 0xF8, 0x1B0, 0x288} + 0x338k` | up to `+0x5F0` |
| `0018A120` | a view's `+8` | up to `A+0x828 + 0xB0` |

- The one other `+0xCB8` store in the image, `006FF816`, belongs to the constructor `006FF5D0` initialising its own
  `this`. Pass 2 shows the flow never enters `006FF5D0` with the object (check N).
- The largest reach is `A+0xCB0`, below `+0xDAC`. The page's worry about 22 unknown-integer stores is answered by
  where they land, whatever their values.

**2. Self-pointer fields: modelled; no new writer.** Pass 1's 10 exact-offset self stores and the 4 indexed ones from
`001897C0` (`A+0xD8/+0x268/+0x410/+0x5A0`) seed the map. A load from one of these fields returns the stored pointer.
Pass 2 then finds 4 more fields (`A+0x4D8/+0x668/+0x810/+0x9A0`, the Phyre `+0x78` links) and reaches a fixpoint at
14 fields after two iterations. The flow then covers the same 71 store sites as OPUS's run: **0 new**.

**3. Virtual calls: resolved.**
- **Resolved in the flow:** 21 call sites, where the vtable is loaded from `A+K` exactly:
  - views → `00189C20`;
  - Phyre `[+0x50]` → `0062E1C0`;
  - allocators → `001EDF80`/`001EDFE0`.
- **Seeded instead, 16 sites whose receiver has an index-held offset:**
  - `001897C0`'s ten view calls, and `001858A0`/`00188640`'s four allocator calls. The same targets are seeded on
    every concrete receiver: all 6 views, all 8 Phyre sub-objects with both vtables and all code slots, and all 4
    allocators.
  - the EH iterator's `call rsi` (`00808FE4`), 1 site: its constructors and destructors (`00184CE0`, `00184CB0`,
    `001850B0`, `00185070`) are seeded on every element.
  - `001F0AD0`, 1 site: see 4 below.
- **Imports, 5 sites (6 entries):** `_aligned_free`, `_purecall`, `sinf`, `sqrtf`, `tanf`. None stores into its argument; the
  maths calls take their inputs in `xmm` registers.
- In every case: **0 new** writers.

**4. The escapes: rooted; no new writer.**
- **`001F1E80` stores A at `[obj + 0x18]`** of an object whose vtable is `00902F90`. Its 9 code slots are seeded with
  a token B, where a load from `B+0x18` returns A: **0 new**.
- **`0060CE50` stores view + 8 at `[ext + 0xA8]`**, where `ext = [A+8]`, the application object's `+0xE8`
  (`0017D04F` → `00189000`). The five module functions that load `[reg + 0xA8]` (`00602EA0`, `00609D80`,
  `0060B980`, `0060F830`, `00610350`) are seeded with a token whose `+0xA8` returns the six view + 8 pointers, and so
  is `0060CE50` itself: **0 new**, and no unresolved indirect call inside them.
- **`001F0AD0` calls `[[ext] + 0x10]` with `r8` = a view pair.** `ext` is constructed by `005DDBA0` (vtable
  `00D498F0`) from `00793250` (`0079334F`), the base constructor `0017CC70` calls. Slot 2 is `00600D20`, seeded with
  `r8` = each pair: **0 new**.

## Assumption 1 checked (OPUS, 2026-09-30)

What the object at `[A+8]` is, read from the RTTI and the constructors:
- `[A+8]` is `app+0xE8`, an embedded member. The application object's constructor `00792350` builds it with
  `005DC2F0` (`0079241E`). That constructor stores vtable `00D49930`, RTTI `Phyre::PRendering::PRenderer`
  (`005DC375`/`005DC37C`).
- The destructor path `00793250` resets it with `005DDBA0` (`0079334F`), which stores the base vtable `00D498F0`,
  `PRendererBase`.
- Both vtables have slot 2 = `00600D20`, the function this record seeded. So under either class the slot-2 call
  reaches `00600D20`.
- The only other class derived from `PRendererBase` is `PRendererForJobs` (vtable `00D49910`, slot 2 `00600E30`). Its
  vtable is stored only in `0060E9C0` (`0060EA89`/`0060EAFE`), into the elements of a heap array (`[rsi+8]`), never into
  `app+0xE8`.
- Method: every `lea` of the three vtables image-wide, and a `.rdata` census of complete-object locators whose class
  hierarchy names `PRendererBase`.

Assumption 2 (readers of `ext+0xA8` outside `0060xxxx`-`0061xxxx`) stays as stated. `PRenderer`'s three slots are
`005E2BC0` (the destructor, outside the module), `006104E0` and `00600D20`. A whole-image value flow from every holder
of `ext` was not run.

## Not claimed

- **Two assumptions in root 4:**
  - that `[A+8]` keeps vtable `00D498F0`; no later vtable store to that member was searched for;
  - that the readers of `ext+0xA8` all lie in the `00600000`-`00620000` module.
  Either would be a static follow-up.
- **The flow's own depth limit.** `MAXDEPTH` is 12. Pass 1 reports 916 cuts, none carrying the object.
- **External writes** (a debugger or a mod), as OPUS already noted.
- **`rc4b_scan.py`** lists the stores anywhere with displacement `0xDAC − K` for the escaping offsets `K`, as a raw
  cross-check. Its hits include byte-level misdecodes, and none is used above. The result rests on the flow runs and
  the bounds.
