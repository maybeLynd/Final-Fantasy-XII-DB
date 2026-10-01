# MapScreenContainer +0xC0: a child widget's header, collapsed; Widget gains +0x68..+0x78 (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SEM.

**What was wrong.**
- `MapScreenContainer` carried 30 rows over +0xC0..+0x17F. Three of them were "mixed ... NOT resolved"
  (`mixed0100`, `mixed0104`, `mixed0161`).
- Offset for offset, the 30 rows restated the shared Widget header of a **child widget built in place at +0xC0**.
- Four of them (+0x128..+0x138) were the only record of Widget +0x68..+0x78. The Widget type had no rows there.

**What the image says** ([`child_widget.py`](child_widget.py)).
- **C:** `002B79BD` builds a 0xD0-byte widget at +0xC0 (`mov edx, 0xd0` / `lea rcx, [rbx+0xc0]` / `call 00245000`).
  Four sites null-test it through the widget predicate `00273A20`. 0xC0 + 0xD0 = 0x190, where the next row starts.
- **H:** the header initialiser `002465F0` stores at +0x40 / +0x44 / +0x9C / +0xA0 / +0xA1. Those are the census's
  +0x100 / +0x104 / +0x15C / +0x160 / +0x161, which were the three "mixed" rows.
- **G:** the generic widget body `00244DD0` shows:

| offset | field | evidence |
|---|---|---|
| +0x68 | `timedRecord68` void* | the class table's record (`[+0x48] + 0x14`) or a static record, dereferenced as a word at +2 |
| +0x70 | `timedFrames70` uint32 | ms × 60 / 1000, ~~the same 60 Hz conversion as `transitionDurationFrames`~~ unsigned and bounded; `+0x90`'s conversion is signed low-32 and agrees only on non-negative, non-overflowing inputs (qualified 2026-09-28, ASTRA `widget-transition-duration-domain`) |
| +0x74 | `timedStartFrame74` uint32 | the global frame clock `0208F570`, like `transitionStartFrame` |
| +0x78 | `timedInit78` uint32 | initialised to `0x3F800000`; no typed access, so width only |

**The changes** (FABLE's rule 0).
- **MapScreenContainer:** the 30 rows become one region row, `childWidgetHeader0C0`, type `Widget`, width 192. This
  follows the store's `widgetBase0000` convention.
  - The absorbed rows are listed verbatim in its evidence.
  - The child's 0x10 content bytes, +0x180..+0x18F (`byte0180`, `unobservedSpan0181`), keep their rows.
- **Widget:** the four rows are added, and the migrated MapScreenContainer evidence is carried verbatim.
- **Meaning:** what the second timed block does is not claimed.

**Run receipt.** Run verified at 996166340:
- `child_widget.py` C / H / G / S FAILS 0 (S failed before the patch);
- `types_index.py --validate` 0 errors;
- `check_census_widths.py` 0 disagreements;
- `check_type_refs.py` 0 dangling;
- `enum_check.py` FAILS 0;
- no finding from `check_embed_overlap`, `check_embed_parent_fields`, `check_ctype_widths`, `check_interior_offsets` or
  `check_alignment` names either type.

## Polarity regression P (OPUS, 2026-09-28)

ASTRA's `widget-deferred-dispatch-domain` (`ASTRA-RETURN-OPUS-WIDGET-DEFERRED-DISPATCH-DOMAIN`) showed that G binds
instructions but not branch polarity: a copy with the branch reversed still passed G.
- **P** binds the one polarity the rows state. On `00244DD0`'s mode-2 rebase arm, +0x70 is zeroed only when
  `[+0x40]` bit 16 is **set** (`00244E62 bt` / `00244E66 jae` over the store).
- P rejects a `jae` -> `jb` copy built in memory.
- The Widget +0x70 and +0x7C rows now record the polarity and the mode domain: nibble 0 and 3 schedule, 2 rebases, and
  every other value returns early.

The contract and layout-page wording is FABLE's.


## Generator repair and T (OPUS, 2026-09-28)

This is the same defect ASTRA found in the +0xB8 rate generator (ASTRA-REQ-OPUS-RATE-GENERATOR-POSTCONDITION). Three ASTRA-return amendments changed the Widget +0x70 row in the store:

- 7f0992cf6 struck "the same conversion as +0x90";
- fff2f6b46 added the selection;
- 8c37324ed added the polarity.

This generator was not changed. So `--patch` from the legacy spans rewrote the struck claim and dropped the three qualifications, and S did not notice: S checks only that the rows exist.

- **Template:** it now carries the accepted +0x70 meaning (`M70`) and evidence tail (`E_TAIL`), inserted from the store row verbatim.
- **T** binds the template to the store: name, ctype, meaning, evidence head and tail for all four Widget rows. A mutant with the old +0x70 text fails T on the current store.
- **`generator_replay.py --legacy <store before 22102235b>`** runs the real producer, with only `FIELDS` redirected to a temporary copy. The regenerated Widget +0x68..+0x78 rows and the MapScreenContainer +0xC0 region row equal the store byte for byte, and the check exits 0 (`generator_replay.out`).
- **The pre-repair producer** (`--src`, HEAD before this change) regenerates a different +0x70 row while its own check still exits 0 (`generator_replay_prerepair.out`). That is the silent loss T now rejects.
