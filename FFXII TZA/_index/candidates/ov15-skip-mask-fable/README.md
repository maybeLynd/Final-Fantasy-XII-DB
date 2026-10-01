# OV-15: the control byte the wait poll consults is the manager's skip mask (FABLE, Claude Opus 5.5, 2026-09-29)

**Question (OV-15, box on `01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md`):**
"Trace the relevant control-byte producers and their actual native meaning."

The page's §4 says:
- the wait poll reads a byte selected by the target actor's `+0x15` through `02099011 + sign_extend(index)*0x288`;
- "the complete meaning and writer population of that indexed control remain open."

**Answer: it is the actor manager's skip mask.** Control: [`skip_mask.py`](skip_mask.py) A C R W I, FAILS 0
([output](skip_mask.out)). Static.

- **Identity (prior art, reused).** `02099011` is `02098E10 + 0x201`: the actor-manager slot record (stride `0x288`), field
  `+0x201`. The actor's `+0x15` is its manager index.
  [The world-tick page](../../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) (§2.2a, and
  the writer table after it) already names this byte the per-manager **skip mask**:
  - bit k is request k being skipped;
  - while it is non-zero, the tick runs that slot's sixteen sub-steps in a frame;
  - the field manager (slot 0) never has it set.
- **Producers (A, checked in the image).** The only instructions whose memory operand is `+0x201`, plus every rip reference to
  `02099011`, are:

  | role | address(es) | effect |
  |---|---|---|
  | setter / clearer | `0026A5B0` (movzx, then `bts` or `btr`, then byte store) | sets or clears one bit |
  | its callers (per the world-tick page) | skip begin `00360710` (command 1337 `skipexec`, and an engine loop over managers 1–3) | sets bits; refuses manager 0 |
  | | skip end `00360A50` (command 1306's poll, and an engine loop over requests 0–7) | only clears |
  | zero store | the bind `0026CC38` | writes 0 |
  | reader, by manager index | `00267310` | returns the mask |
  | reader, by record pointer | `00267300` | returns the mask |
  | reader, in the interpreter | `0025E5C5` | loads the mask before each opcode dispatch |

  C adds two things:
  - there is no image-base-relative form of the address;
  - 109 stores wider than a byte reach `+0x201` by displacement, and **none of them lies in the actor-manager or ScriptVM
    code ranges**. They were not read one by one, so "no other writer" is claimed only for those ranges.
- **What the wait does with it (W).** The wait is family 0 command 0: begin `0034CF90`, poll `0034DCC0`. The poll:
  1. decrements the countdown;
  2. if the result is negative, reports done;
  3. otherwise calls `00267310` with the **target** actor's manager byte, and if that manager's mask is non-zero, stores 0
     to the countdown;
  4. reports running.

  **So a wait on a skipped manager ends by its second poll, whatever its length** (model in I: countdown 5 under a
  skip → running with 0, then done). Section 11's control "phase1 and zero actor control counts down" is the mask-0 case.
- **Who else consults it.** `00267310` has **72** rel32 call sites, most of them ScriptVM command handlers that pass an
  actor's `+0x15`; `00267300` has 2. So "some polls" in the page's wording is many command handlers, and a skip
  (fast-forward) shortens or ends them. **Not claimed:** what each of the other 71 callers does with the mask.

**Correction to my own working note.** The any-manager probe `00264830` looked like a reader of this byte. It is not: it
tests `02099010` (`+0x200`) bit 2, a different byte. A lists it nowhere, and the page text below does not cite it.

## For FRONTIER to apply (the page is a SECTION-overlay carrier, and the register row is in your working tree)

**The page, §4.** Replace "The complete meaning and writer population of that indexed control remain open." with:

> *Answered 2026-09-29 (OV-15; `_index/candidates/ov15-skip-mask-fable/`):* the indexed control is the target manager's skip
> mask (manager record `+0x201`; the world-tick page names it). A skip begin (script command 1337, or the engine's loop over
> managers 1–3) sets its bits, and a skip end clears them. The bind writes it 0. The wait poll zeroes its countdown while the
> mask is non-zero, so a skipped wait ends by its second poll; 72 call sites consult the mask through the same reader.

**The box.** Tick OV-15 and point it at this record.

**The register row OV-15.** Change it to ANSWERED 2026-09-29 (FABLE), with this record as the evidence.

FRONTIER's apply changes: `01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md` (§4 sentence, OV-15 box)

consumer: the world-tick page's writer table ("one bit-level writer and one direct writer") agrees with A. Its bit-level
writer is `0026A5B0`, and its direct writer is the bind store.

consumer: `CONTRACT-native-command-lifecycle.md` §3 ("must not be confused with the target actor or its indexed runtime
control byte") agrees. The byte belongs to the target's manager record, not to the request.

run: skip_mask.py at 0c2dc0cc9, FAILS 0.
