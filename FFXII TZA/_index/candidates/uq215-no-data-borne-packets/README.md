# UQ-215: no loaded-data VIF command stream reaches the UNPACK decoder (FABLE, Claude Opus 5.5, 2026-09-27)

**What the row still asked.** The formats are read. `0022BFF0` is parametric, and two of its thirteen arms misaddress
their source. FABLE's 2026-09-18 census showed every UNPACK in a code-built packet is `V4_32`. The row stayed PARTIAL on
one clause: "whether data-borne packets use the other twelve formats".

**Answer: none reach the decoder.** Loaded data enters a decoded packet only as payload under a V4_32 header that the
code writes. The one VIF command stream that does come from loaded data, effect type `0x97`'s resource payload, travels
the raw-packet path that the PC drain never submits. So no shipped content exercises the other twelve arms. The
`V2-32` / `V4_5` source defects are latent on every route, not just on code-built packets.

## The routes, static (`uq215_routes.py`, 7 checks, FAILS 0)

1. **One entry into the decoder.** The VIF1 interpreter `001DB550` is reached only as vtable slot 0 of `GiVmax`.
   - `009007E8` is the only qword in `.rdata` / `.data` holding `001DB550`.
   - The ctor `001DB220` is the only instruction that loads `009007E8`.
   - Chunks enter a command only through `001DB340`, whose only callers are the builder `001DB840` and the thunk
     `001DB7D0` that the effect finalisers' `001DB7E0` commands use (R1, R2).
2. **What the VU1 registrars are given.** Every payload handed to `003A34D0`, `003A35E0`, `003A2F70` and `003A33B0` falls
   in one of three classes (R3):

   | payloads | source |
   |---:|---|
   | 101 | exe `.data` templates (rip-relative into `02ADE000`..`02AEE000`) |
   | 2 | stack buffers built by code (the bone-trail commands, program `0053F490`) |
   | 1 | the type-`0x67` record block (see 3) |

   None is a resolved resource pointer. Sensitivity (R3c): the same classifier, applied to type `0x97`'s call
   `0045BE73`, does not class that call's resolved resource pointer (`r8`) as a template, and does class its exe
   template `02AE3460` (`rcx`) as one.
3. **Type `0x67`'s second payload** (R4).
   - **Setup.** The setup `0045FD50` allocates `count × 0x260` records and copies each from the exe template
     `02AEC860`. The startup builder `004E79C0` fills that template: `STCYCL 0x01000404`, then `UNPACK 0x6C22001E`, which
     is V4_32 with NUM 34.
   - **Per frame.** The walk `00460170` copies 0x200 bytes from the element's work buffer into record `+0x10`, inside
     that payload.
   - **The work buffer.** It is a code-owned allocation (`elem+0x338`), which `00532EF0` fills with `memset` and
     `003D8E50`. It is not copied from data.
4. **The effect finalisers** (R5). Where resource bytes do enter an effect packet, the builder writes the UNPACK header
   itself and `memcpy`s the payload under it:
   - `0054C10E` and `0054D9EE` (`or ecx, 0x6C000064`, types `0x73` / `0x74`);
   - `005466E0` (`or eax, 0x6C00`, type `0x6A`).

   All three headers are V4_32.
5. **The one data-borne command stream** (R6). Effect type `0x97` resolves `def + 0x2A0 + 4 × elem[+0x298]`
   (`0045BE30`..`0045BE3E`) and appends that resource payload as a DMA `ref` after an `STCYCL 4/4` descriptor. It does so
   through `003A2E30` (`0045BE73`) or `003A31A0` (`0045BEE0`), the raw-packet appenders. The UQ-204 record
   (`_index/candidates/uq204-element-type-emits/README.md`) establishes that the drain `003A3740` never submits a raw
   packet on PC. So this stream never reaches `001DB550`.

## Limits

- **Static.** Nothing was executed.
- **The template range.** R3 bounds templates to the range the 48 measured packet objects occupy (UQ-46). Every template
  hit lies inside it.
- **The `0x97` payloads are not censused.** Which formats those resource payloads contain would matter only to a port
  that submitted raw packets.
- **What V4_32 rests on.** The 2026-09-18 immediate census and the OR-form headers above. A header computed some other
  way at run time is not excluded by an immediate census. The route census here confirms that the payloads themselves
  are code-owned.

## Files

- `uq215_routes.py`, the control.
- `consumer-check.md`.
