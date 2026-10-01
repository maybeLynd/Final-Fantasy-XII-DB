# S-49: header I1's fixture exposure, bounded statically against the engine's own registrations (OPUS, 2026-09-25, block 290)

**The exposure.** `candidates/s49-runtime-per-invariant-exposure.md` (block 245) found one named exposure in S-49's
runtime evidence. EXP-094 executes header I1 ("a big-endian file is accepted by flipping the whole header and
re-testing the same constant") through two fixture pieces:
- a **fixture member graph**: five nodes spliced into `desc+0x80`;
- **fixture member-type swap leaves**.

That note also said a static reading of the real members' types would bound the exposure. This is that reading.
**Evidence class: STATIC** (disassembly of the shipped image). No execution is claimed.

## What the engine really registers

| step | site | reading |
|---|---|---|
| registrars | `0059D550` (`PClusterHeader`) calls `005983E0`, `00598C50`, `00598DF0` | `PClusterHeader` itself registers **no** member (0 calls to `00632960` in `0059D550` / `00584D10`); `00598DF0` registers onto `02CA9EA0` (`PInstanceListHeader`: `m_classID`, `m_count` …), a different class |
| `PClusterHeaderBase` | `005983E0`: 18 × `00632960(member, desc 02CA9FA0, type, name, offset, attr 8)` | offsets `0x00`–`0x44`, every 4 bytes |
| `PClusterHeaderD3D11` | `00598C50`: 3 × `00632960(…, desc 02CA9DA0, …)` | offsets `0x48`, `0x4C`, `0x50` |
| member type | every one of the 21 calls takes the type from `00630180` | `00630180` returns `&01F2E5A0` (`006301A7`), the `PTypeDefault<unsigned int>` singleton (`PTypeDefaultUInt`, vtable `00D311B0`, stored by `00631683`) |
| **the swap** | vtable `00D311B0` slot `+0` = **`005CB140`** | `8B 02 0F C8 89 02 B0 01 C3`: `*(u32*)rdx = bswap(*(u32*)rdx); return 1`. 9 bytes, call-free |
| member node | `00632960` installs node vtable `00D580B0` (`006329AF`) | slot `+8` (getType) = `005C5230` = `xor eax,eax; ret` → declType null; `0063CE80` then takes the typed-object swap arm |
| the walk | `0063E2E0`: forward over `desc+0x80`, then `rdi = [rdi+0x78]` until null (`0063E351` / `0063E3B4`) | **the whole parent chain**: `02CAA0A0` → `02CA9DA0` → `02CA9FA0` → root (`phyre-class-parent-chain.tsv`) |

**So the real flip swaps all 21 header dwords, `0x00`–`0x53`, each with `005CB140`.** The flipped fields are exactly the
84 bytes the loader reads.

## Against EXP-094's fixture

| piece | fixture | real | same? |
|---|---|---|---|
| swap body | `SWAP_FN`: a log of `(rdx, r8)`, then `8B 02 0F C8 89 02 B0 01 C3` | `005CB140` = `8B 02 0F C8 89 02 B0 01 C3` | **byte-identical after the log** |
| node getType | `GETTYPE_FN` = `31 C0 C3` | `005C5230` = `33 C0 C3` | the same `xor eax,eax; ret` (a different encoding) |
| members swapped | `MEMBERS5`: `+0x00`, `+0x04`, `+0x08`, `+0x0C`, `+0x44` | 21 members, `+0x00`..`+0x50` | fixture ⊂ real |
| where planted | own list `02CAA0A0` (+ `02CA9DA0` in the parent-chain case) | `02CA9DA0` (3) and `02CA9FA0` (18) | the same walk visits both |

**What the loader reads after the flip** (`0059A3B0`, read 2026-09-25):
- the marker re-test at `0059A419` (`+0x00`);
- platform `+0x0C` at `0059A452`, physics `+0x44` at `0059A461`, namespace size `+0x08` at `0059A476` and size
  `+0x04` at `0059A4DC`;
- then a **second** `0063E2E0` walk over the same buffer at `0059A501` (its descriptor and direction arguments are
  not read here);
- then a copy of all `0x54` bytes out (`0059A536`..`0059A55C`).

**Bound.** The swaps are independent in-place 4-byte operations. The fixture's five members are a subset of the real
21, and they are **exactly the five fields the loader reads individually**. So:
- the **accept / reject decision** and the five scalar values of every EXP-094 BE case are what the shipped
  registrations produce;
- **the copied-out header is not.** The real walk also flips the other 16 dwords. The fixture leaves them in file
  order, so EXP-094's output header differs from the shipped behaviour in those 16 dwords, and no EXP-094 check
  inspects them. The contract's word "whole" is established by this static reading, not by EXP-094.

**What this does not cover:**
- the deferred finalize machinery `00160210` leaves pending (the order in which real nodes are linked); in-place
  independent swaps make the order immaterial;
- a live load.

Whether this static bound discharges S-49's runtime cell is **SWE2-AUDIT-SEM's call**.
