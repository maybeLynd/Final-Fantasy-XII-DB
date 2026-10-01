# SD-62: the two non-type elements of the static array are registry objects, not type records (OPUS, 2026-09-30)

Register row SD-62 was registered by SWE2-DATA (`how-a-class-registers-its-array-members-and-annotations.md` §7). It asks
what `01F2E330` (accessor `006373D0`) and `01F2E780` (accessor `00637440`) are. They are the two elements of the
`0x50`-stride static array that are not `PType` / `PTypeDefault<T>` records. This record is static. The checker is
`sd62_elements.py` (output `sd62_elements.out`, `FAILS 0`). It uses `Tools/analysis-kit/gfz-scripts/retool.py`.
**Status proposed: NARROWED.**

## What they are (OPUS)

- **F1: plain static data.** Neither is built at run time. Each accessor's cold path only registers an exit
  destructor (`008AF490` / `008AFDE0`). Neither starts with a vtable: `+0` is a self pointer, a list head. So they are
  not type records.
- **F2: `01F2E330` is the object every class descriptor is built against.**
  - It holds three self-linked list heads (`+0x00`, `+0x10`, `+0x28`) and zeros, and its destructor walks the list at
    `+0x10`.
  - **384 of the 385** calls to the class-descriptor constructor `00632D80` pass `006373D0()`, this object, as `rdx`.
    `00632D80` stores it at the new descriptor's `+0x70` (`00632DD6`).
  - An object shared by nearly every class is not a per-class parent. It is the root that class descriptors hang
    from. The database's older label for `006373D0` ("TLS context getter") does not fit this use.
- **F3, F4:** ~~`01F2E780` is a record on `PWorld`.~~
  - ~~It holds self-linked list heads (`+0x00`–`+0x3F`), then at `+0x40` the `PWorld` class descriptor `02CF8A80` (its
    constructor `00164100` installs vtable `00D56D10`, RTTI `PClassDescriptorWithoutDefaultConstructor<PWorld>`), and
    at `+0x48` the name `"getInstanceCount"`.~~
  - **Corrected 2026-09-30 (OPUS, adjudicating SWE2-ORACLE's L5/L6 in
    [`sd62-registry-list-links-0930`](../sd62-registry-list-links-0930/README.md), `dedfaf0d7`):**
    - `01F2E780` is a **0x30-byte** object. Its two initialisers write exactly six qwords, `01F2E780`–`01F2E7A8`
      (`00638F73`–`00638F96`, `00636468`–`0063648B`). SWE2-ORACLE reads it as the name-hash tree of class
      descriptors.
    - The `PWorld` descriptor `02CF8A80` and `"getInstanceCount"` sit at `+0x10` / `+0x18` of a **separate record at
      `01F2E7B0`**. It has its own initialiser `00635B80` (`00635BF7`–`00635C05`) and its own exit destructor
      `008AF430` (`008AF43D`–`008AF470`). It is the method record for `PWorld::getInstanceCount`.
    - F3's own byte check already showed the split: slots 6 and 7 self-link to `01F2E7B0`, not `01F2E780`. The bytes
      F3 reads are unchanged; only their attribution was wrong, and the checker's label now says so.
  - Six functions fetch it through `00637440`. One of them, `0059B430`, hashes a name (`and edx, 0x1f` over the string,
    seed `0x7B5`) against what it returns.

## Still open (OPUS)

- **What the list heads chain.** Which descriptors, members or methods each list holds is not traced.
- ~~**What `01F2E780` is exactly.** A static method record (`PWorld::getInstanceCount`) and a name-lookup root are both
  consistent with F3/F4. The registration that fills its lists, and `0059B430`'s full lookup, would decide it.~~
  **Answered by SWE2-ORACLE's `sd62-registry-list-links-0930`, adjudicated 2026-09-30 (OPUS):** it is the name-lookup
  root, the class-descriptor name-hash tree. The method record is the separate `01F2E7B0` (see the F3 correction).
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
