# Consumer check: CONTRACT-auto-status-rebuild 13an's 0030EDA0 copy range (OPUS, 2026-10-03)

Corrects: `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md` section 13an. It restated EXP-231's `30EDA0`
snapshot copy as `q[obj+0xB88]`->`obj+0x730` (0x480). The bytes copy 0x4F0 bytes to `[obj+0x6B0, obj+0xBA0)`.
The full text is in the [README](README.md).

**Consumers** (every `.md` naming `30EDA0` together with `0x730` or `0x480`), with each one's state:
- `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md` 13an: revised-here.
- `_experiments/EXP-231-detach-siblings-exec.md` L30: agrees. SWE2-ORACLE corrected it in `c03ad4d97`.
- `07-Combat-Action/CONTRACT-commit-action.md` L353: agrees. Corrected 2026-10-01 (OPUS): 0x4F0 to `unit+0x6B0..+0xBA0`.
- `_experiments/EXP-091-commit-callees-exec.md` L60: agrees. The origin is `rcx = unit+0x6B0`.
- `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` L197/L476: agrees. These rows describe a different copy,
  the cancel's `+0x718` -> `+0x730` (`003106B9`-`003106D7`), not `30EDA0`.
- Retained pre-images and evidence quote the old text on purpose and are left as they are:
  `_experiments/evidence/uq147-ko-release-partition/consumer-preimages/*` and
  `_experiments/evidence/suspend-restore-copy-origin/README.md`. So is the `_index/AUDIT-LOG.md` log.

Regression: `Database/FFXII TZA/_index/candidates/opus-ko-13an-copy-1003/check.py`, run on the worktree over HEAD
15ec1ea71cfe, verified at 15ec1ea71cfe: FAILS 0. It covers the `0030EDA7 add rcx,0x6b0` / `mov edx,9` / 7-store tail
bytes, with the old-model control, and the 13an text, with the restored-line control.
