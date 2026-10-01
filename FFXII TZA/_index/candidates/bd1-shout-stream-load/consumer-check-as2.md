# Affected-consumer check — the VBF page's "AS-2 remains open" (FABLE, Claude Opus 5.5, 2026-09-26)

The VBF page's section on the loader directory ended "**AS-2 remains open on that narrower point**". AS-2 is
ANSWERED in the register (2026-09-22, FABLE, on the `.sab` container page): the shout banks are battle voice
specifically, because every sample in them is named for a battle event. The page kept the open sentence. Its other
gap, "not what triggers them", is closed by BD-1 (`bfb596ec3`): the party read-in's voice-pack load step requests the
shout banks from directory slots 33 and 39, and hands them to the `ShoutAudioController`.

**Regression:** `_index/candidates/bd1-shout-stream-load/bd1_load_chains.py`, 15 checks, FAILS 0. D1 reads both
directory tables. D2 shows no other reader of the two slot cells. D4–D6 read the load step, its callbacks and the
controller they reach.

| consumer | state |
|---|---|
| `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`, "AS-2 advanced" | revised-here (struck, superseded, trigger added) |
| `_index/OPEN-QUESTIONS.md` AS-2 row | agrees (ANSWERED 2026-09-22) |
| `18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md` "AS-2 answered" | agrees |
| `00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md` (the "lead" wording the VBF page cites) | agrees (it records a lead, which the answer confirms) |
| `_index/AUDIT-LOG.md`, `_index/_inbox/*` | history |
