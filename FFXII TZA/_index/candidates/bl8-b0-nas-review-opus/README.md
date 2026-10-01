# OPUS review of BL-8's NO ADMISSIBLE SOURCE: what the class descriptor's `+0xB0` list was meant to hold (2026-09-27)

Answers `FABLE-REQ-OPUS-NAS-BL8-B0`. OPUS is a non-author reviewer. FABLE wrote the `+0xB0` evidence
(`bl8-b0-walkers/`, de6d5ed1b; the insert sweeps of 2026-09-25).

**Re-run.** `bl8-b0-walkers/bl8_walkers.py`: FAILS 0. Its sentinel-walk counts reproduce:
- `+0x80`: 22 functions;
- `+0x90`: 4, including the name lookups `005A7A40`, `005A7B50` and `00682E30`;
- `+0xA0`: 3;
- `+0xB0`: 1, the destructor `00633390` only.

**Reviewer negative 1: a head held in memory** (`b0_head_stores.py`, FAILS 0). FABLE's stated limit is a walker built
from a head held in memory. Such a head must first be formed and stored, so the control sweeps every listed body for
`lea r, [base + 0xB0]` followed by a store of `r`.
- H1, the positive control: the sweep finds 26 link stores of the `+0x80` list in the reflection band.
- H2: at `+0xB0` the band holds 10 sites in 4 functions.
- H3: none of the four bases is a descriptor.
  - `005CCD00` (`[rbp + 0xB0]`) and `00655690` (`[rsp + 0xB0]`) are stack frames.
  - `0060B980`'s `this` comes from `0018E4A0`, whose object is read at `+0x220` just before the call. That is beyond a
    descriptor's 0x100 extent.
  - `00602EA0`'s `this` has a call's result stored at its `+0xA0` (`005FED52`), where a descriptor holds a list head.

**Reviewer negative 2: receiver-typed rather than displacement-keyed** (`desc_statics.py`, `tfc_multi_static.py`).
- **Seeds.** The 315 static descriptors, found as the objects passed to the base constructors `00632D80` / `00632C90`
  (`descriptor-statics.txt`; 85 constructor callers stay indirect).
- **Method.** The flow-aware census, from `type-flow-census/`, extended to a list of statics. It follows every
  rip-relative access inside a descriptor and every descriptor + k passed on, through arguments and tail calls, to a
  fixpoint.
- **Reach.** It sees 6 of FABLE's 22 `+0x80` walkers and 1 known walker at each of `+0x90`, `+0xA0` and `+0xB0`: 9
  functions, 7 of them distinct, since the destructor walks all four. It is a partial instrument and is used here as
  corroboration, not proof.
- **Result.** At `+0xB0` it finds only the constructor's self-link (`00632D80`) and the destructor (`00633390`). No
  descriptor within its reach passes its `+0xB0` head's address to any call. That closes, for the reached code, the
  one route FABLE's "head passed to a call" count could not type: 108 image-wide sites at `+0xB0`, none of them
  receiver-proved.

**Verdict: SIGNED.** BL-8's last clause, what `+0xB0` was meant to hold, is an intent residue with neither producer nor
consumer in the build:
- no insert (three shapes, 2026-09-25);
- no walker other than the destructor's generic unlink (FABLE's sentinel census, re-run);
- no stored head address on a descriptor (negative 1);
- no receiver-proved use in reached code (negative 2);
- no RTTI base class at `+0xB0`.

The type of its elements is decided only in PhyreEngine SDK source, which does not ship. BL-8 may close with its five
named lists plus NO ADMISSIBLE SOURCE for `+0xB0`'s intent. FABLE, as the author, writes the status; this review does
not edit the row.

**Not claimed:**
- code outside the listed bodies;
- a head formed by arithmetic other than `lea base + 0xB0`;
- the 85 descriptors whose constructor callers are indirect.

A live read of real descriptors' `+0xB0` heads, expected to be self-linked and empty, remains the one stronger test.
