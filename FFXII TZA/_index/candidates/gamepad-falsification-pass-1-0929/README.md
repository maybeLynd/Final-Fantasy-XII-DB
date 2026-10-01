# Consumer check: falsification pass 1 on how-a-gamepad-becomes-a-controller-object (OPUS, 2026-09-29)

corrects: 15-Input/how-a-gamepad-becomes-a-controller-object.md (sections 3 and 7: CON-188; section 3 step 5: CON-189)

## What was corrected

- **CON-188.** Steam does not pre-empt XInput. The XInput branch of `00797690` runs whatever the Steam step did;
  Steam suppresses only the DirectInput path.
- **CON-189.** Not every failing DirectInput step abandons the pad:
  - `SetCooperativeLevel` abandons only on `E_NOTIMPL`;
  - `Acquire` is unchecked;
  - no abandon path releases the device.
- **Answered, not corrected:** section 3.2's residue. All controller classes answer 2 (`00290180`). While Steam reports
  a controller, a walk builds a new Steam object for every pad with no stored twin.
- **Added:** the XInput constructor loads `.\xinput1_3.dll` and resolves ordinal 100; the XInput test runs twice per
  device; a failed re-enumeration skips the poll.

## Current consumers

- consumer: `15-Input/README.md` names the kinds "and their precedence" without its shape; it agrees.
- consumer: `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md` describes the kinds' button bytes
  and the Steam account id, not the build order; it agrees. No other page under `15-Input` or
  `20-Platform-Online-Achievements` states the order (grep for Steam with XInput, and for precedence).
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-188`, `CON-189`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_gamepad_objects.py` G5 and G6. G5 fails unless `test bl`
occurs only at `00797826`, after the XInput branch. G6 fails unless `E_NOTIMPL` is the only cooperative-level abandon
and no `Release` call follows `CreateDevice`.

run: verified at f879cc45f (BROKEN 0, exit 0), against the certified image `73461d08…`.
