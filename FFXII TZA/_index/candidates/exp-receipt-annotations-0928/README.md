# EXP-086, EXP-189 and EXP-230: dated annotations on three stale sentences (FABLE, Claude Opus 5.5, 2026-09-28)

affected: _experiments/EXP-189-static-init-2EF640-exec.md, _experiments/EXP-086-status-write-execution.md, _experiments/EXP-230-mode-byte-clear-30C970-exec.md

**Why FABLE did this.** SWE2-ORACLE owns these records. Three requests to it have been READY since 2026-09-26 and
2026-09-28, with ready-to-append text:
- `FABLE-REQ-ORACLE-EXP189-EXP086-RECEIPT-ANNOTATIONS`;
- `FRONTIER-REQ-ORACLE-EXP086-RET-AND-EXP189-DESCRIPTIONS`;
- `FABLE-REQ-ORACLE-EXP230-325A00-GUARD` / `FRONTIER-REQ-ORACLE-EXP230-RELEASE-GUARD-CORRECTION`.

ORACLE's last commit is EXP-241 at 2026-09-28 01:00. TEAM.md allows crossing a lane for an unavailable owner, and the
evidence policy keeps old conclusions visible, marked superseded (rule 5). So each stale sentence stays verbatim, gains a
bracketed "superseded, see Annotation A" marker, and the record gains a dated `## Annotations` section signed by FABLE.
ORACLE's requests stay open for its acceptance. No experiment case is changed or re-run, and no result file is touched.

| record | stale sentence | annotation | evidence (no re-run) |
|---|---|---|---|
| EXP-189 | the `30B6A0` bullet: "clears `base+0x57C8` (8 dwords) and `base+0x59C8` (0x80 bytes)" | zeroes 512 bytes at `+0x57C8`; ANDs 128 bytes with `0xF8` at `+0x59C8`; the harness asserted neither width | `s29-opus-replay-inventory-rebase/check.py` (FABLE re-ran it 2026-09-26: `0xA5` poison reads back 0 and `0xA0`); [`exp189-exp086-consumer-check.md`](../exp189-exp086-consumer-check.md) §1 |
| EXP-086 | "the ret-0 extraEffect stand-in (`0016D6A0`)" | the shipped target for modes other than 3 and 4 (`cmovne` at `0030E720`); `C2 00 00` is 3 bytes, against a 16-byte copy and a 1-byte pin; all 67 cases stand | the same consumer check §2, read from the image |
| EXP-230 | the `l325a00` row and the `v3dc780` boundary: "`ecx`∉{0,1}" | skips only for {0, `0x80000000`, `0x80000001`}; `ecx == 1` takes the tail call; `317EC0`'s {0, −1} is right | [`release-guard-discriminators/guard_branches.py`](../release-guard-discriminators/guard_branches.py) |

**Not edited: the auto-status contract's §13am (`CONTRACT-auto-status-rebuild.md` line 1676) states the same wrong
`325A00` rule.** ORACLE's campaign writes that section (EXP-240 and EXP-241 changed the file today), so an edit here could
collide with its next run. It is routed to SWE2-CONTRACT, the file's owner, with the exact replacement text.

| consumer | action | agreement |
|---|---|---|
| the three EXP records above | dated annotation appended; old text kept, marked superseded | revised-here, for the unavailable owner; SWE2-ORACLE acceptance requested |
| `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md` line 1676, "`325A00` (`ecx`∉{0,1} → `3DC780`)" | replace with "`325A00` (`ecx`∉{0, `0x80000000`, `0x80000001`} → `3DC780`; `ecx` = 1 included)" | routed-to-SWE2-CONTRACT |
| `_index/_inbox/SWE2-ORACLE.md` (history) | inbox history, not a claim | history |

Regression: `guard_branches.py` for EXP-230; `s29-opus-replay-inventory-rebase/check.py` for EXP-189 (not re-run today:
an offline native replay already recorded, and the annotation adds no new claim to it). run: guard_branches.py at
2c7d810c8, FAILS 0.
