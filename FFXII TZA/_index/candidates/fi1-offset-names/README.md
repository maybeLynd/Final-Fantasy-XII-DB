# FI-1 — the actor storage record's offsets that had no store row, named

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `fi1_offsets.py` (10 checks, FAILS 0).

## The premise, re-measured (N1)

FI-1 asked for "the names of the 41 touched offsets without a store row". The field map
([the-actor-storage-record-field-map.md](../../../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md)
§2.2) now flags **34** offsets "*not in the store*". **Every one of the 34 now has an `ActorStorageRecord` row** in
`_types/fields.tsv`, so the rows exist; what was missing was a meaning. The table below gives one for each: the
store's own, a reference, or a reading made here.

## The `+0xC8`–`+0xEB` band is one array (N2–N4)

**The array.** `+0xC8`–`+0xEB` is **`u16 overrides[18]`**: per-slot ids that override the actor's authored list.
- **Initialisation.** The initialiser fills exactly 18 words with `0xFFFF` (`002668A0` `lea rdi, [rbx + 0xc8]`,
  `002668AB` `mov ecx, 0x12`, `002668B0` `rep stosw`). `0xFFFF` means "no override".
- **Readers take slot k.** When the word is `0xFFFF`, the reader falls back to element k of the count-prefixed s16
  list at the authored entry's `+0x18`, meaning `image + resolve(entry.+0x18)`; if the list is shorter, the answer is
  −1. Examples:
  - the indexed readers `002652D0` (slot bounded to `0x11`) and `00269860` (slot 7 or 14);
  - the fixed-slot reads at `0025C490` / `0025CFA5` (slot 3);
  - the initialiser's own resource requests for slots 15, 9 and 1 (`002668EC`…).
- **Writers.**
  - `0025AF60` writes by slot (`0025AFA1`). It refuses a slot above `0x11` and a value with bit 15 set, and the script
    VM interpreter calls it.
  - `0025AE00` writes at `0025AEC2`, called from `setentrygroupall`'s handler `00340970`.

The 12 flagged offsets `+0xC8`, `+0xCC`, `+0xCE`, `+0xD0`, `+0xD2`, `+0xD4`, `+0xD8`, `+0xDC`, `+0xDE`, `+0xE2`,
`+0xE8` and `+0xEA` are elements 0, 2, 3, 4, 5, 6, 8, 10, 11, 13, 16 and 17 of this array. Element 16 (`+0xE8`) is the
id the EH-5 countdown hands to `ActorResource_SubmitRequestDescriptor`.

**A correction this carries.** The record page's §4 says the initialiser does not touch `+0xC0`–`+0xEC`, and its §17
leaves `+0xC8`–`+0xE8` as the largest gap. The initialiser writes that span with one `rep stosw`. A scalar census
cannot see a string store, which is why it read as untouched.

## Every flagged offset

| offset | meaning | source |
|---|---|---|
| `+0x004` | `hitObjectBindState` | store, SEMANTICALLY IDENTIFIED |
| `+0x00A` | per-record **target-candidate flags** for a battle-command list rebuild. The candidate builder clears it per record and sets `0x10` / `4` / `1` from its predicates (`0046B740` / `0046B7C3` / `0046B7EE` / `0046B7FE`); `002647E0` returns it by packed id, and bit 0 enters the default-target election ([command availability](../../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md)) | N9 |
| `+0x00B` | flag byte: bit 2 = countdown armed and bit 3 = countdown held (EH-5 on [the record page](../../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md)); bit 5 = exempt from stop set 2 ([the stop registry](../../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) row 2); the low bits are the actor passes' mask bits | reference |
| `+0x010` | `outstandingRequestCount` | store |
| `+0x012` | `partySlot` | store |
| `+0x018` | `pairLinkState` | store |
| `+0x020` | a **signed byte handle**. It starts at −1 (`00266670` / `00266698`); `002E3AF0` releases a non-negative one through `0036EC10` and stores −1 | N6 |
| `+0x024` / `+0x026` | `requestAllChannelMask` / `submittedChannelMask` | store |
| `+0x038` | `boundBattleUnitPtr38` | store |
| `+0x0C0` | `secondaryContextPtr` | store |
| `+0x0C8`–`+0x0EA` (12 rows) | `overrides[0..17]` | N2–N4 |
| `+0x0EC` | a dword reset to 0 on every event post (`002EB030` / `002EB430`) and by `002E6BD0`; no reader on the censused routes | N5 |
| `+0x0F4` | the byte an actor contributes to the slot table at `02B59CC0` through `003DF760`: slot 3 from `00268D10` (with `flags1C` bit 13 set), slot 2 from `0025C830`. No writer on the censused routes, and the initialiser's stores do not cover it, so on those routes it publishes the pool's zero | N10 |
| `+0x0F5` | a byte reset to `0xFF` on every event post; no reader on the censused routes. The post also stores the event id at `+0xF0` and forwards it through `002EB0D0` (FT-2's route) | N5 |
| `+0x0F6` / `+0x0F8` | `recordIndexWord` / `fallbackObjectPtrF8` | store |
| `+0x100` | a word the initialiser zeroes; `00263A10` returns it only when `nameIndex` (`+0x102`) is negative. `0025C230`'s dword accesses at `+0x100` belong to the context at `[record + 0xB8]`, not to this record | N8 |
| `+0x102` | `nameIndex` (initialised to −1) | store |
| `+0x108` | a dword the field pass stores as 0 every pass (`0025DF1F`…`0025E134`); no reader on the censused routes | N7 |
| `+0x10C` / `+0x114` | stop set 2's live set / pending clear; `+0x110` is the pending set | stop registry row 2 |
| `+0x118` | the EH-5 countdown; `+0x11A` is its reload value, 60 | EH-5 |

## What this does not claim

- **Readers of the reset-only fields.** "No reader on the censused routes" for `+0xEC`, `+0xF5` and `+0x108` is bounded
  by the field map's routes. An indirect reader would not appear. The claim is only that no censused function reads
  them.
- **What the override slots and the `+0x0A` bits mean to the player.** Which resource kind each of the 18 slots
  selects, and what the `02B59CC0` slot table is for, are not named here.
- **The type store.** Its rows are not edited here. The band's twelve TYPE RESOLVED rows are routed to the store's
  owner for renaming.
