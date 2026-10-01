# Retained descriptor-head occupancy — ASTRA, 2026-09-26

**173 validated title-state descriptors have self-linked +0x60 and +0xB0 heads
in both retained header brackets.** This is sampled emptiness, not proof those
lists are never populated. No new live experiment or 173-buffer recapture occurred.

Question/hypotheses: do existing valid EXP-124 headers show populated, self-linked,
null/invalid heads, or lack the required bytes? Method A is sufficient because
EXP-124 actually retained complete 0x108-B descriptor headers covering both words
of each head. Current canonical contract already identifies +0x60 as annotations;
+B0 purpose and unsampled population remain unresolved.

Source title-defaults.json SHA256
25931a0cb4f734c941b04ad50281a7c18a86119c9d02c13b64e5d4b4f3ef0b05;
original PID 34568, EXE 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base 00120000. Original ordinary-title state, read-only query handles, no debugger
or process writes. Full .text 7,996,981-B identity, 102-module before/after equality,
LUAC positive, null-read rejection and closed-handle receipts are checked again
from raw fields. This does not certify every loaded DLL or continuous health.

Reducer independently reads every raw header/name string; validates recorded
descriptor address, layout, name, instance size, vtable word and default pointer;
requires full reads and equal before/after headers. The two pointer words at
+60/+B0 both equal their own head address for every selected descriptor. The
same 0x90 layout query yields 24 genuinely captured non-self-linked method heads
and 149 self-linked heads. PAnimatableComponent is the explicit positive control.
This is a detector positive, not a traversal or proof of node payload/ownership.

The seven additional ancestor headers also contain self-linked +60/+B0 words
when inspected; they are single reads, not members of the 173 bracketed count.
The four invalid/unobserved D3D mappings are not repaired or silently excluded
from database scope. Seven unprepared default buffers remain unprepared: list
head state is separate from the copied-object default's initialization.

check.py rejects four controlled corruptions: changed-after head, short header,
wrong class identity and zero-case sample. Two explicitly synthetic reducer-only
cases ensure null words are classified invalid/uninitialized, never empty, and
non-self links can be detected. They are not live writes or native executions.
Reproduce from repository root:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/descriptor-occupancy-retained/check.py"
```

observation.json contains 173 per-descriptor pointer pairs, header hashes and
raw read indexes, plus controls/limits. validation.txt is the focused run receipt;
manifest.json seals the package. Original raw bytes remain in EXP-124, immutable.
No full campaign ran. Sequential equal brackets do not prove atomicity, absence
of intermediate insertion or stable lifetime. Nothing establishes all 410 statics,
heap descriptors, a loaded field or later game states. Never-populated semantics,
B0 intended payload and remaining initialization/mapping questions stay open.

Canonical consumers: FABLE BL-8 / class-descriptor contract and metadata page;
OPUS descriptor types/default maps. Propagation and independent review are pending.
Return the finite title observation and positive control; do not reclassify either
list as permanently dead or waive its purpose/ownership questions from this sample.

Cleanup: this reduction uses files only. Original EXP-124 cleanup is historical;
no current game/control process started, no save/config/reference write, no new
restoration or detach claimed. DB_GOAL=NOT_MET.

Player version: both requested metadata lists were empty in the captured title
state, while other lists were visibly populated in the same memory capture.
We used already preserved evidence; we did not launch the game again. Other
states could still populate these lists, and one list's purpose remains unknown.
