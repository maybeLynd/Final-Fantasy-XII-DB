# Affected-consumer check: FH-1, the ActorManagerSlot's section pointers and their lifetime (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (control: `_index/candidates/fh1-slot-sections/fh1_slot_sections.py`, 5 checks, FAILS 0):
- **Eight setter stubs.** Each stores one EBP section's base at a slot field, called from that section's handler:
  - section 2 → `+0xA0`, section 3 → `+0xA8`, section 6 → `+0xB0`;
  - section 8 → `+0xD8`, section 9 → `+0xE0`, section 10 → `+0xF0`, section 11 → `+0xF8`, section 12 → `+0x100`.
- **Lifetime.**
  - The bind zeroes `+0xA0`–`+0xB8`, `+0xE0` and `+0xF8`.
  - The teardown `0032ED80` clears sections 8–12 through their setters with 0.
  - For sections 2, 3 and 6 the teardown clears only the global mirror, so the slot field keeps the old pointer until
    the next bind.
  - Whether any reader runs in that window is not claimed.
- **Readers of `+0xB0`.** The gauge-label verbs `0x1BC`–`0x1BE` read it.

**What this corrects.** Store rows `writeOnlyQwordE0`, `writeOnlyQwordF8` and `boundObjectPtrB0` are renamed:
- The first two were write-only only on the slot. Their data is read through the global mirrors.
- `boundObjectPtrB0`'s "evidence exhausted for meaning" measured the access instructions only, not the setter.

The previous meaning cells are kept inside the new ones. The page's three table rows now name the section.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` FH-1 | OPEN, narrowed, residue listed | revised-here |
| `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md` FH-1 box and table rows `+0xB0`/`+0xE0`/`+0xF8` | narrowing appended; rows name the section | revised-here |
| `_types/fields.tsv` ActorManagerSlot `+0xA0`/`+0xA8`/`+0xB0`/`+0xE0`/`+0xF8` | meaning + lifetime; three renamed | revised-here |
| `25-EBP-Script-Container/Container/ebp2-container.md` handler table | the source of the handler→setter pairs; no change | agrees |

Corrects: _types/fields.tsv
Corrects: 04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md

Run receipt: `fh1_slot_sections.py` executed at 38db3fc4c (FAILS 0, 5 PASS lines).
