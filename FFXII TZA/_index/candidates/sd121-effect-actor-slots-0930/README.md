# SD-121: the three dword arrays are the script-assigned effect-actor slots (OPUS, 2026-09-30)

Register row SD-121 was registered by SWE2-DATA ([the-largest-unclassified-functions.md](../../../99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md)
section 12). It asks what the three dword arrays at `022D97B0`, `022D98B0` and `022D99B0` hold.

This record is static. The checker is `sd121_slots.py` (output `sd121_slots.out`, `FAILS 0`). It reads the script-VM
verb table [scriptvm-verb-table.tsv](../../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv).

## The answer (OPUS)

**Each array is a 64-slot table of packed actor handles. Scripts fill a slot with the verbs `effectactor` /
`bgeffectactor`, and effect elements read the slot to anchor themselves at that actor.**

- **S1, S2: the arrays and their accessors.**
  - Every rip reference into the three arrays lies in ten small accessors, one get / set / clear trio per array
    plus `0036E080`. Get: slot ≤ 63, else 0. Set: the slot clamped to 0..63. Clear: store 0.
  - The reset `0036E3B0` zeroes all 3 × 64 slots.
- ~~**S3: the writers are four script verbs.**~~ **S3: the non-zero writers are two script verbs; four more paths store 0.** `effectactor` /
  `bgeffectactor` are the only writers of a handle. Zeroes come from `clear_effectactor` / `clear_bgeffectactor`, from
  `0036E080` (called by the area unload `002628B0` at `00262997`, it clears in all three arrays every slot whose handle
  bits 16-19, the actor's `+0x15` nibble, equal the unloaded area index), and from the reset `0036E3B0` (called by
  `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` at `0026CA57`). *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd121-0930/REVIEW.md))*

  | verb (call id) | handler | array |
  |---|---|---|
  | `effectactor` (`0x126`) | `00352270` | sets `022D97B0`, or `022D99B0` (S4) |
  | `bgeffectactor` (`0x570`) | `00352940` | sets `022D98B0` |
  | `clear_effectactor` (`0x56F`) | `00342010` | clears `022D97B0` and `022D99B0` |
  | `clear_bgeffectactor` (`0x571`) | `003423C0` | clears `022D98B0` |

- **S4: what `effectactor` stores.**
  - **The slot** is the verb's argument (`00267E10`).
  - **The value** is the packed handle of the running script's actor (`00263F10` → `003589B0`).
  - **The table.** A script context whose byte `+0x15` is 3 writes `022D99B0`; any other context writes `022D97B0`.
- **S5: the readers are effect elements.** `003A40F0` and `003A4220` read one slot.
  - **Choosing the table:**
    - the mode word at `[02F97348]+0x36A` with bits 12–14 equal to 3 → `022D99B0`;
    - otherwise byte `[02F97348]` equal to 2 → `022D98B0`, the `bg` table;
    - otherwise → `022D97B0`.
  - ~~**Using the handle.** The element resolves it through `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`)
    and copies the actor's position into its own `+0x30` / `+0x34` / `+0x38` (`00265020`).~~
    **Using the handle.** `003A40F0` first maps the handle through `002E9B80` (the actor's `+0xC0` record index). For
    an actor that has one, the element takes the 0x740-byte record `[022C6F28] + i*0x740` and copies no position.
    Only for an actor without one does it resolve the handle through `003588B0` and copy `[actor+0xB8]`'s three dwords
    (`Actor_GetWorldPosition`, `00265020`) into its `+0x30` / `+0x34` / `+0x38`. `003A4220` returns
    `002E9B80(handle)` (an index, or -1) and copies nothing. An empty slot in the `99B0` / `98B0` table falls back to
    `97B0`. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd121-0930/REVIEW.md))*

**For modding:** an effect bound to effect-actor slot *n* ~~follows whichever actor~~ is anchored to (or, for an actor with a battle
record, bound to the record of) whichever actor *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd121-0930/REVIEW.md))* last ran `effectactor n` (or
`bgeffectactor n` in the other table). `clear_effectactor` / `clear_bgeffectactor` detach it.

## Limits (OPUS)

- **The mode word.** What `[02F97348]+0x36A` bits 12–14 = 3 and byte `[02F97348]` = 2 name (which game modes) is not
  read here.
- **The `+0x15` byte.** What a script context with `+0x15 == 3` is, is not read here.
- ~~**`0036E080`.** The slot clearer the world-tick page reads (the first two arrays) is not re-read.~~ `0036E080` is read (see S3). It covers all three arrays, not the first two. The world-tick page's
  "dual-table" line is the source of the old wording. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd121-0930/REVIEW.md))*
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
