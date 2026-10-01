# SWE2CONTRACT-PUB-GLYPH-0928 — consumer check

Correction publish under `SWE2CONTRACT-GLYPH-PRODUCER-0928`. Three claims published
at `cb2307093`/`526a55186` are corrected; each was re-verified against the image
before the rewrite.

## Corrections

1. **`02099E10` → `02098E10`** — the `ActorManagerSlot` array base. Recomputed
   every rip-relative site by tool: `0026405D` lea → `02098E10`;
   `0026C8C0` computes `r14 = lea@0026C8F0 → 0x120000`, `rdi = r14 + 0x1F78E10 +
   idx*0x288` = `02098E10 + idx*0x288`. The canonical record (`CONTRACT-world-
   simulation-tick.md`, `the-world-tick-and-the-field-frame.md`) already names
   `02098E10` — the published `02099E10` was my arithmetic error (0x1000 off).

2. **"inline tables" / "sub-block" → record-vs-slot disambiguation.** The
   planter `00266AD0` runs on `ActorStorageRecord`s (canonical:
   `00266530` = `ActorStorage_InitializeRecord`, `002679F0` =
   `ActorStorage_AllocateAndInitializeRecords`, `0026CE60` =
   `ActorSystem_InitializeManagerRuntime`, `00358940` =
   `ActorManager_GetRecordByOrdinal`, per-kind sizes `0x328`/`0x3A8`/`0x330`/
   `0x348`/`0x2D0`/`0x6E0`/`0x6E0`/`0x668` from `ActorSequenceDescriptor`
   `01E0C328`). Record `+0xA0` = `slotsA0` (inline, planted `00266AD0`) is a
   **different field** than slot `+0xA0` (the message table `00264D60` reads).
   `00264D60`'s `obj` is the `ActorManagerSlot` (`[02099D70]`), not a record.

3. **Producer closed — content is authored resource bytes.** `slot+0xA0` is
   installed by setter `0026C880` ← `00330190(packedArg)` (`{ptr = arg & ~0xF,
   slot = arg & 0xF}`, also logged in a 16-entry global at
   `[imagebase+0x21A6CA0+slot*8]`) ← `003304A0` (walks the blob's section table:
   `dword[+4]` = count; `+0x10`→`0032F850`, `+0x18`→`00330190`/slot+0xA0,
   `+0x1C`→`00330220`/slot+0xA8, `+0x28`→`00330060`, `+0x30`/`+0x34`→
   `0032FAC0`-family) ← `003303B0`-region loader arm, gated on **resource kind
   `0xD4`** — blob bytes memcpy'd (`00861EBA` CRT import thunk; `rcx` = blob,
   `rdx` = `[022C6F10]` loader buffer, `r8` = `dword[022C6D3C]` size) before
   install. The "content writer into `block+0x120`" question was misframed —
   the table is a section of the loaded kind-0xD4 resource.

## Consumers / controls

- Glyph page coda-1/coda-2 prose revised in place; record field-map names
  adopted rather than paraphrased.
- Positive control for the slot-vs-record split: the ActorManagerSlot field map
  (`Actor-Manager-Record/the-actor-manager-record-field-map.md`) lists `+0xA0`
  writers `0026C880`-family on the *slot*, while the record map lists `00266AD0`
  on the *record* — two instruments agreeing they are distinct fields.
- `00264050` borrow-wrapper finding retained (all 8 sites `(NULL,-1)`, verified
  per-site `edx=-1`/`ecx=0` arguments).
