# SWE2-AUDIT-SPEC review of SD-20 (sd20-voice-callback-0930 at fd421c927): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS. Reviewed
commit `fd421c927`, record [sd20-voice-callback-0930](../sd20-voice-callback-0930/README.md). Static, image `73461D08…21F8`,
checked at HEAD `cb5b622f2`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD20-0930 | sd20-voice-callback-0930 | `fd421c927` | ACCEPT |

**Re-run.** `sd20_voice_callback.py` from its own directory: F1-F5 PASS, `FAILS 0`. Output
([rerun_sd20_voice_callback.out](rerun_sd20_voice_callback.out)) is identical to the committed `.out` ignoring CR.
The record directory stayed clean.

**Re-derived independently** ([sd20_rederive.py](sd20_rederive.py) / [.out](sd20_rederive.out) and
[sd20_parents.py](sd20_parents.py) / [.out](sd20_parents.out); `tk.py` raw sweeps, not retool's function-list scan):
- **Factory callers, raw.** A raw E8/E9/`0F 8x` sweep of all of `.text` for `007AEA20` finds exactly three calls:
  `007B91E7` (owner `007B9050`), `007DCF92` (`007DCE20`), `007ED332` (`007EBAD0`). `rawcalls.json` gives the same three.
  No DIR64 relocation points at the factory, so there is no pointer-table use. F4's caller set is complete.
- **5th argument.** The last store to `[rsp + 0x20]` before each call is `007B91E2 mov [rsp+0x20], rax`,
  `007DCF87 mov [rsp+0x20], rax` and `007ED32D mov [rsp+0x20], rdi`. These are the registers F4 traces to `this+0x10`,
  `this+8` and `rbx+8` (or null).
- **Interface installers, raw.** The raw rip-relative sweep for `01CB5218` finds 4 verified references and 0 raw-only
  ones, all `lea rax`: `007B8ED0` (in `007B8E50`), `007B8F76` (`007B8F70`), `007DC886` (`007DC730`) and `007EA35D`
  (`007EA050`). There is no relocation to it. F2 holds.
- **RTTI, read without retool.** Reading `[vt-8]` → COL (signature 1) → `+0x0C` type descriptor → name gives
  `01CB5218` `.?AVICoreSourceVoiceCallback@Core@Driver@Sd@SQEX@@`, `01CB5238` `ExternalSourceVoice`, `01CB7B20`
  `CRI::HCAMixerVoice` and `01CB92A8` `Voice`. That agrees with retool's `rtti_class`. The retool reader's layout
  (`vt-8` COL, `COL+0x14` self-RVA for the image base, `COL+0x0C` TD, name at `TD+0x10`) is the correct MSVC x64 layout.
- **Parents.** Each constructor has exactly one raw caller: `007B8F20`, `007DCA50` and `007EA410` respectively. Each
  of those wrappers is itself referenced from a relocation, i.e. a factory/clone slot. None of the three parents
  (`007A4930`, `007DCD70`, `007B5D20`) calls a constructor or loads a class vtable. So I confirm the record's own limit:
  the caller-to-class tie is by field layout only, and the record says so. `007DCD70` gets its object from `007DC6B0`
  (`007DCDEB`, a guarded static accessor) and tail-jumps (`007DCE07`) into `007DCE20`.

**Controls.** F1-F3 are exact-value asserts on RTTI strings and installer offsets, so they are sensitive to a
misnamed class. F4 compares an exact site list. That catches an extra or missing listed caller but is blind to an
unlisted one; the raw sweep above closes that gap. F5 is an overlap test with low field offsets (`+0x8`, `+0x10`).
Many classes would pass it, so it is not sensitive to a wrong type, and the record labels it "consistency, not
proof". The answer does not lean on it beyond that label.

**Not checked.** Which of the three kinds a shipped sound uses at run time. That is static-only, as stated.
