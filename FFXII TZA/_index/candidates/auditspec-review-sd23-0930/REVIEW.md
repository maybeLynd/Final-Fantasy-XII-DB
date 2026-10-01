# SWE2-AUDIT-SPEC review of SD-23 (sd23-sound-slots-38-39-0930 at acb04148d): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS. Reviewed
commit `acb04148d`, record [sd23-sound-slots-38-39-0930](../sd23-sound-slots-38-39-0930/README.md). The status is
NARROWED, not answered. Static, checked at HEAD `cb5b622f2`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD23-0930 | sd23-sound-slots-38-39-0930 | `acb04148d` | ACCEPT |

**Re-run.** `sd23_sound_slots.py`: F1-F4 PASS, `FAILS 0`. Output
([rerun_sd23_sound_slots.out](rerun_sd23_sound_slots.out)) is identical to the committed `.out` ignoring CR. The record
directory stayed clean.

**Re-derived independently** ([sd23_rederive.py](sd23_rederive.py) / [.out](sd23_rederive.out), `tk.py`, not retool):
- **Every Sound-family vtable, found from RTTI.** I walked all of `.rdata` for vtables whose `[vt-8]` COL names a
  class ending `Sound@Driver@Sd@SQEX`. There are 19: primary and secondary vtables of `ISound`, `Sound`, `RandomSound`,
  `VariationSound`, `OrderSound`, `CycleSound` and `SwitchSound`. On the six concrete primaries, slot 38 / slot 39 read:
  - `Sound` `01CB5A30`: false / true;
  - `RandomSound` `01CB87A8`: false / true;
  - `VariationSound` `01CB8940`: **true** / true;
  - `OrderSound` `01CB8AD8`: false / true;
  - `CycleSound` `01CB8C70`: false / **false**;
  - `SwitchSound` `01CB8E08`: false / true.

  The stub bodies are `007E57B0` `xor al, al; ret` and `007E5800` `mov al, 1; ret`. F1 and F2 hold. `ISound`'s vtable
  is shorter, and its slot 38 is past its end.
- **Site counts, raw.** A raw byte sweep of all of `.text` looked for `FF /2` `[reg+disp32]` calls (plain and SIB
  forms), each decoded. Inside `007A0000..00800000` it finds exactly 16 `+0x130` sites and 2 `+0x138` sites, the same
  addresses as the record:
  - 12 boolean sites `007B2F08`…`007BED8E`;
  - 4 float sites `007F0DA8` / `007F0DCD` / `007F0DF5` / `007F0E0D`;
  - `+0x138`: `007BF183` and `007F0A23`.

  The linear census of listed functions agrees.
- **Two table rows spot-read.**
  - `007BDBD6`: the call, then `xorps xmm8, xmm8`. On true, `movaps xmm7, xmm8`, so `xmm7` = 0. On false, `xmm7` =
    `[[rsi+0x30]+0xC]`. The record's "use zero in place of a computed value (`xmm7 = 0`)" holds, although the zeroed
    source register is `xmm8`.
  - `007BED8E`: on true, `jne 007BEE26` skips `cmp byte [rec], 0xd` and the `[rec+0x19]` bit tests. That matches the
    record.

**Controls.** F2 asserts per-class true/false from primary vtables named by RTTI, so it is sensitive to a wrong class
or slot. F3 classifies each site by the next use of the result (`test al` versus `comiss`/`subss xmm0`). That is
sensitive to the 12/4 split, but it takes the audio-range site list as given. My raw sweep confirms that list is
complete in range. Outside the range the image has 20 more `+0x130` and 22 more `+0x138` call sites, for classes the
record does not claim. The record's scope is the row's 16/2 audio-range sites, and it stays within it.

**Not checked.** What state 7 of `007BF0A0` means, and the `007F0820` class. Both are stated limits. The delegation
reading is labelled interpretation, which is appropriate for a NARROWED row.
