# S-40 types: CPostEffect, its init descriptor, and the per-frame cfg declared (OPUS, 2026-09-25)

**Row:** S-40, post-processing (Yebis). The binding-gap cell reads *"types (CPostEffect/wrapper/cfg layouts) is
OPUS's worklist"*. The wrapper (`PostProcessingLibraryWrapper`), the instance cell (`PostEffectLibraryInstanceCell`,
`02EA0B70`) and `TextureUtilSingletonCell` were declared earlier. This note covers the rest. It scores nothing.

## What is declared, and from which bytes

| type | size | route | extent from |
|---|---|---|---|
| `CPostEffect` | 0xD40 | `PTR 0x02EA0B70` | `006DAA70` allocates `0xD40` through `006DA880(allocator [01F3BA68], 0xD40, "..\src\ppfx.cpp", 0x332)` (`006DAB84`–`006DAB9D`), constructs with `006FF5D0` (`006DABAF`, which installs no vtable) and stores the pointer (`006DABB9`) |
| `PpfxInitDescriptor` | 0x118 | `PTR 0x02EA0B70+0x210` | `Initialize 006FF900` copies **exactly 0x118 bytes** from its 6th argument into `this+0x210` (2 × 0x80 at `006FFA80`–`006FFAD0`, 0x10 at `006FFAD2`, 8 at `006FFAD8`); a null argument runs `006CBBC0` on `this+0x210` instead (`006FFAE2`). `006CBBC0`'s last store is the dword at +0x114 |
| `PostProcessFrameParams` | 0xF0 | DYNAMIC | `0018EEE0` allocates `001A1470([01F7F4C0], 0xF0)` (`0018EF1D`–`0018EF29`) and fills it |

**Release of `CPostEffect`** (`006DEC49`–`006DEC80`): if the cell is non-null, `006FF840(obj)`, then
`006DA8A0([01F3BA68], obj)` (decrements `02EA0B3C`, jumps through the allocator's vtable +0x10), then the cell
is zeroed. It is the same allocator cell the allocation used.

## Two parameter blocks, not one

The contract mentions two different blocks, and the store now keeps them apart:

- **The init descriptor.** Section 3's *"default parameter block (`006CBBC0`) with aspect 16/9, 0x780 and 7 qwords
  of −1"*. It lives on `006CBD20`'s stack (`rsp+0x50`). `006CBD20` overrides four slots:
  - +0x20: the float 16/9 (`006CBDD7`);
  - +0x38: dword 0;
  - +0x48: dword `0x780`;
  - +0x88: dword 2.

  The descriptor goes through `006DAA70` unchanged (`006DACFD`) into `Initialize`, which keeps its own copy at
  `CPostEffect+0x210`. The contract's flags word `+0x20C` sits immediately before it.
- **The per-frame `cfg`.** Section 2's `[ctx + 0x10]`. The contract's open item *"Who fills `cfg`"* has a static
  answer:
  1. `0018EEE0` fills it, mostly by copying from `PostProcessParamContext` (`rsi = [01F7F5F0]`).
  2. It then calls `005FEA50(list, 00193DA0, block)`, which writes a command slot `{+0 dword 0x2F, +8 fn,
     +0x10 block}` (`005FEAEE`–`005FEAF8`).
  3. `00193DA0` is referenced once in the whole image (`001F337D lea r8`). A scan of rip-relative, rel32 and raw
     qword references finds no other.
  4. It reads the block as `[rcx+0x10]` (`00193DAA`).

  **Not read here:** the dispatcher that turns the slot into `00193DA0`'s `rcx`.

`cfg`'s field rows name each field's producer source and consumer read. Fields the consumer never reads
(+0x2C, +0x44..+0x97) are kept as copies, with meaning not claimed.

## One tension, for FABLE

`cfg+0x18` and `+0x1C` are copied from `PostProcessParamContext+0xF4` and `+0xF8` (`0018EFF3`, `0018EFFC`).
The two sources disagree on what they are:

- **The type store:** that type names those fields `dofFocusEnd` and `dofBlendFalloff`.
- **The contract** (section 4, step 5): `0065E670` passes `cfg+0x18` and `+0x1C` to the **Glare** setter when the
  option is on. `00193DA0` does read them (`00193E52`/`00193E4D`) just before `0065E670` (`00193E6C`).

Either the two field names are wrong, or the contract's Glare mapping is. This note does not decide. The field rows
say "NOT reconciled".

## CPostEffect's field cut

The two converged censuses were combined:
- constructor-seeded (`006FF5D0`, 150 displacements);
- cell-seeded (`02EA0B70`, 808 displacements across 181 functions).

A first cut let 16-byte moves join fields together, which gave one 1816-byte "mixed" run. 432 of those moves are on
`Initialize`'s page. Now:
- only 1-, 2-, 4- and 8-byte accesses mark field boundaries;
- 16-byte moves either annotate a row or mark a `copiedSpan` that nothing narrower reaches;
- the embedded descriptor is a single row at +0x210.

Result: 529 rows, none wider than 24 bytes apart from the descriptor. Meanings are not claimed.

## For the scorer

The three layouts named in the row's worklist are declared:
- `CPostEffect`;
- the wrapper (earlier);
- `cfg` (`PostProcessFrameParams`).

`PpfxInitDescriptor` is the other block the contract describes. How S-40's `types` cell scores is AUDIT-SEM's
ruling.

## Ruled (FABLE `33f4eccf1`), applied to the type store (OPUS, block 251)

FABLE ruled that `cfg+0x18`/`+0x1C` are glare parameters: the chain ends in the library's
`CPostEffect::SetGlareParameters` (`00707560`, error string `00D93420`). Its stores were re-read:
- the first float (`xmm1`) goes to `CPostEffect+0x6E4` and the second (`xmm2`) to `+0x6E0` (`007075CB` / `007075D3`);
- the flag (`r9d`) goes to `+0xC6C`;
- the remap factor, clamped to at least 0.001f, goes to `+0xC70`.

Renamed or named as a result:
- `PostProcessParamContext` `+0xF4` / `+0xF8` → `glareParam0` / `glareParam1` (were `dofFocusEnd` /
  `dofBlendFalloff`);
- `PostProcessFrameParams` `+0x18` / `+0x1C` → `glareParam0` / `glareParam1`;
- `CPostEffect` `+0x6E4` / `+0x6E0` / `+0xC6C` / `+0xC70` → `glareParam0` / `glareParam1` / `glareParamsFlag` /
  `glareRemapFactor`.

Which glare quantity each float is has no name in the image.
