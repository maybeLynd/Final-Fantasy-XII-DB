# CharacterLightingTuningBank +0x90: two floats, not one "mixed" 8-byte span (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SEM.

**Before.** The row `mixed090 u8[8]` read "one field or two NOT resolved by width". The only reason was a single qword store,
`mov qword ptr [02CB8130], 0` at `001D194F`.

**What the image says** ([`bank090_split.py`](bank090_split.py)).
- **W:** a whole-image census of rip-relative operands into `02CB8130..02CB8137` finds 13 accesses. Twelve are 4-byte
  `movss`, six at +0x90 and six at +0x94, beside the one qword. The qword is followed at once by
  `mov dword ptr [+0x98], 0` (**W2**), so it zero-initialises consecutive float cells; it is not an 8-byte field.
- **U:** the bank's only other mover, `006084B0`, copies it in aligned 16-byte units, which never divide +0x90 from +0x94.
- **K:** the console catalogue (`console-command-names.md`) maps these cells in order beside the store's existing
  `cubeMapIntensity`:

| id | label | address | offset |
|---|---|---|---|
| 108 | `Diffuse intensity:` | `02CB8130` | +0x90 |
| 109 | `Specular intensity:` | `02CB8134` | +0x94 |
| 110 | `Cube map intensity:` | `02CB8138` | +0x98 |

**After.** `+0x90 diffuseIntensity float` and `+0x94 specularIntensity float`, both SEMANTICALLY IDENTIFIED like their
neighbours. The old row is kept verbatim in the WAS history, including FABLE's 2026-09-18 note that +0x90 is a float
that id 28 does not own. No page names `mixed090`.

**Run receipt.** Run verified at 2e4e282a2: `bank090_split.py` S FAILED before the patch and FAILS 0 after it; `types_index.py --validate` 0 errors.
