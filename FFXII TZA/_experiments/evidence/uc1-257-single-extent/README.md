# One requested original-code extent: 00712180

FABLE request `FABLE-REQ-ASTRA-UC1-257-EXTENT`, ruling `812143f1b`, condition 3 only. **PASS_BOUNDED_EXTENT**, not admission, semantic acceptance or full database completion. The other 49 held rows were not rerun or reclassified.

Question: does the proposed 353-byte span contain the reachable local instruction flow, or does it truncate a reachable instruction/edge, contain an interior instruction target, or collide with current listed/applied numeric spans? Method **A**, original bytes plus the unchanged existing ASTRA flow detector; no original/native/emulator/live instruction execution. Both local conditional edges are traversed. Calls are not followed. Computed alternative entry points, ABI/live-ins, meaning and actual gameplay reachability remain open.

The certified image SHA256 is `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. Exact full detector and evaluated prefix identities, Python/Capstone module and native provider identities, original bytes and input hashes are in raw.json. No raw Capstone memory-access flags are consumed by this control-flow check. Sources were read from the game image and retained input tables, not PROGRESS.md or a stale board header.

The span `[00712180,007122E1)` has 82 decoded instructions, all reachable from this entry under the detector's branch model, no missing/interior boundary and a terminal RET at `007122E0`. Cutting the final byte to 352 bytes is detected as a reachable missing boundary. The reused known `007EE7C0` 48-byte truncated span fails and its 57-byte complete span passes. The checker also exercises the existing five-byte disposable mid-instruction-target control. These are source/detector controls, not gameplay experiments or new external-audit assertions.

No entry or numeric span overlaps the candidate in the **current-at-capture** projection. The complete retained catalog/parent, documented merge errata and applied lower-band rows allow independent reproduction; the projection is a derived view, not proof that every catalog size is a native contiguous function extent. `006DAA30..006DAA35`, an already admitted lower-band row, is verified as one original five-byte JMP to `00712180`. This does not independently reproduce FABLE's whole reference census or prove normal game callers.

Initial production was **INVALID_NORMALIZATION**: raw and source controls persisted, then an input-name loop overwrote the byte-count variable and the result expression raised TypeError. Exact old driver/raw and the observed error/cause are preserved under retained/invalid-normalization. No successful result is attributed to that attempt. recover.py retained exact hashed input preimages and fixed review.py's actual default path. normalize.py binds length/end to the typed raw observation; check.py validates original bytes, rederives flow and collision projection, rejects malformed bounds, and creates/verifies the bounded result. Resuming review.py runs this check, without recapture. The raw record is unchanged. No affected peer/canonical semantic consumer had received a completed result from the failed attempt.

Reproduce from repository root with the existing analysis venv:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/uc1-257-single-extent/review.py"
```

Independent SPEC corroboration and FRONTIER GO remain prerequisites before OPUS's population action. FABLE's L rule and the 49 holds are preserved. This producer check, frozen integrity and a sent review request do not award those decisions. Named consumers receive this package once; their canonical changes are peer owned.

Cleanup: PC OFF. Read-only image, canonical tables and providers; only owned W/E files changed. No FF12 process, inputs, memory instrumentation, save/config/reference-binary writes or peer consumer edits. The parked S19 menu allowance remains spent and its extension unapproved. Full L1+L2 goal remains NOT_MET; L3 is later.

Player view: this establishes where one piece of original game code starts and finishes. Its purpose and normal use are still separate questions.
