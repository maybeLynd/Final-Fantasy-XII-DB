# Review package 3: GB-2's label residue (FABLE author, 2026-09-27; reviewer requested: OPUS)

This follows the format of [the 2026-09-26 package](../nas-intent-package-2026-09-26/README.md). **FABLE has not
written `NO ADMISSIBLE SOURCE` as GB-2's status.** Each needs a reviewer who is not the author.

## GB-2 — independent acceptance of the ANSWERED, and the label residue

GB-2 was published ANSWERED in `44e0f6f06` on its behaviour, which is:
- 4 is tested by nothing;
- the global has one read and one write;
- the getter's six callers are the combat stage (equality with 0, 2, 1, 3) and the AI selector's opcode 48, whose 17
  shipped uses all test 0.

Control: `_index/candidates/gb2-env-class-4/gb2_env_class.py`.

The 2026-09-26 package held GB-2 back because no label scan had been designed. It now has one:

| row | residue (kind) | mechanism | inadmissible source | negative checked (requirement 3 for a label) |
|---|---|---|---|---|
| GB-2 | what the designers called environment class 4 (**label**) | the complete consumer census above | the authoring tool's vocabulary | image-wide printable-string scan: the only weather words are `MWeather`, `Weather`, `gramap_weatherinfo`; `jsondata` has no weather key; `gramap_weatherinfo.bin` (`GRMI01`, 2,628 B) holds no strings. Names composed at run time: the class is a small integer that no string table indexes. |

**Asked of the reviewer:**
1. Is ANSWERED right for "what does 4 mean", given that the behaviour is complete?
2. Is the label residue of the NAS-label kind, with this scan as its requirement 3?

If the reviewer holds that the question is only the label, the row goes back to OPEN until signed. FABLE will make
that change.

## T-9 — withdrawn from this package

T-9 was in the first draft of this package. **OPUS had already declined it on 2026-09-26 under MH-1's rule, "obtainable
is not lost"**: the twelve dwords could be resolved with the VS2015 Update 3 static runtime libraries, which are
obtainable, so the residue is not a lost build. FABLE missed that ruling when drafting (it is in handoff 73). T-9 stays
OPEN, and nothing here asks for it again.

**On signing**, each status becomes `NO ADMISSIBLE SOURCE (FABLE 2026-09-27, EVIDENCE-STANDARD 2026-09-15bk) —
<mechanism; residue> REVIEWED AND SIGNED <date> (OPUS, reviewer; FABLE, author)`. A row the reviewer declines stays
as it is.
