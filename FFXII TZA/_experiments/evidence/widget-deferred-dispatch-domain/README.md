# Deferred widget dispatch: polarity and domain

Player view: the engine has separate paths for starting deferred UI work, changing its deadline, and sending a notification without starting a timer. A database sentence reversed one flag's meaning; another sentence described a conditional notification as universal. No visible UI bug or normal game occurrence was tested.

Question and hypotheses are in [PLAN.md](PLAN.md). **Method A** reuses the previously retained 301 bytes of `00244DD0` from `spawn-widget-teardown`, verifies exact shipping identity, and analyzes branches. `result.json` retains all instructions, conditional calculations, preimages, actual producer invocations and limits. No original-code execution, emulator, native calls, live game, callback stub or PC controls.

At the stable flags snapshot at `00244E17`, after completed prefix calls:

| condition | local source consequence |
|---|---|
| self null at entry | return before the prefix |
| `flags40` bit 0 clear | bypass the mode switch; set the low nibble of `+7C` to 1, OR `0x30`, preserve `+70/+74` on this local arm, then test the handler |
| bit 0 set; mode 0 or 3 | schedule, use prior37's selected-delay conversion, set low nibble 4, OR `0x30`, then test the handler |
| bit 0 set; mode 2 | rebase; **bit 16 set** clears `+70` first, bit 16 clear retains it; `+74 = low32(2*tick - +70 - old74)`; set low nibble 4, OR `0x30`, then test the handler |
| bit 0 set; every other signed low nibble | return before the shared tail and handler test |
| tail reached; handler null | no indirect call |
| tail reached; handler present | reach `call rax` with self and the exact `{15,0,0}` record; native callback effects remain unknown |

The source `BT` at `00244E62` and `JAE 00244E6D` at `00244E66` skip the zero store when bit 16 is **clear**. With tick 100, duration 10 and old start 20, the conditional deadlines are 170 for clear and 180 for set. This refutes the retained Widget contract's bit-clear wording. The layout page's bit-set wording is correct; do not reverse it to match the contract. Its universal `OR 0x34`, getter-input and divide-by-60 descriptions need correction. The earlier37 arithmetic/override is reused, not rerun. The Widget body already documented that selection before37; its table/type refinements are not discovery of the whole behavior.

The low nibble is sign-extended. All sixteen encodings are covered by the source case split: only 0/2/3 enter the active scheduling/rebase tail. Mode 1 is one of thirteen early-return encodings. The bit0-clear arm preempts that split. These are conditional source calculations, not sixteen game tests or evidence that every encoding occurs. Even an early-return nonnull call first writes `+B8` and executes prefix predicates; no whole-function no-effect claim is made.

Two labelled private source mutations reverse bit16 polarity and invert the default return branch. They change the corresponding conditional predictions and are rejected by exact shipping-source bindings. They were not executed as FF12 machine code.

**Producer limit.** The actual retained `child_widget.py` runs in owned Python children on controlled read-only input views. Its unchanged original image guard properly refuses the mutated image. A separate explicitly labelled private copy changes only the hash literal to the **actual mutant SHA**, leaving C/H/G/S obligations unchanged; it still reports G PASS. Thus G establishes its stated width/arithmetic/store facts, not mode2 polarity. Preserve that guard; ask the owner to add the focused branch obligation where polarity is claimed. This is not a canonical index regression or an invalidation of the child-header migration. The focused field view preserves exact current Widget and MapScreenContainer rows, the only types used by S; it is not whole-field-table validation.

**Extent correction and regression.** The first driver stopped before any result because it assumed one `.pdata` row must span all301 bytes. The shipping root row spans123 bytes; four contiguous `UNW_FLAG_CHAININFO` ranges point to that root and complete the301-byte body. Raw unwind records, failed driver and failed receipt are preserved. The corrected check validates all five ranges and rejects a root-only extent. This follows the [Microsoft x64 unwind format](https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64?view=msvc-170); it does not change the old exact retained body.

Reproduce read-only validation with the existing Python environment and `check.py`. `derive.py` preserves original scratch paths for producer children and refuses replay if a result exists. In a fresh private reproduction, use the certified image and current supported ownership; never edit published inputs. No raw Capstone operand access flags are used.

Consumer changes are routed to FABLE (widget contract and layout entry) and OPUS (field/domain and producer obligations), with SPEC independent review. Acceptance is pending, distinct from own controls. Stable widget/state, completed calls and normal ABI are conditions; actual initialization, caller mode constraints, cadence, rendering, callback effects and live scheduling remain open. Saves/config/reference binary were unchanged. PC OFF; menu setup budget stays consumed/unapproved; full L1+L2 goal remains NOT_MET.
