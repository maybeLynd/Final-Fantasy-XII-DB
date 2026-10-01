# Esper order residue: compressed-switch premise refuted from original bytes

The live-labelled request `SWE2STRUCT-REQ-ASTRA-OV58D-ESPER-ORDER-0930` asks
whether order words `0x4049/0x404A` reach the two high-status-index calls on an
Esper's record 38/39. **The normal original handler maps both words elsewhere.**
The proposed high-index route was a switch-interpretation error, not a natural
state question requiring a fight. Producer proof is complete; independent review
and STRUCT/FABLE/OPUS consumption remain required. Whole OV-5/8 stays open.

## Question, hypotheses and method

The prior `ov58d-pointer-flow-0930/CALLER-CONE-0030E360-0930.md` assigns `0x4049`
to `002FDF18` and `0x404A` to `002FDF5A`, then derives byte arguments F8/D9.
Competing hypothesis: the compressed byte-selector stage was omitted, so those
words take a different arm and the two real status arms pass ids 0–31.

Method **A** is the cheapest sufficient discriminator. The original handler reads
the WORD, performs unsigned bounds and an exact two-stage lookup, without an
opaque call before the first switch. Its finite table and local return arm settle
the named route under ordinary valid-code/state/ABI premises. No absence sampling,
forced state, synthetic original-code execution or game session is needed.

Reference: original `FFXII_TZA.exe`, SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base 0x120000.
Capstone 5.0.7, actual reviewed `reg_tracking.py` and byte-annotation validator.
The collector validates the contiguous chained-unwind normal code partition
`002FDDA0..002FE534`; inline lookup data starts at `002FE534`. It does not
disassemble lookup bytes as instructions. Unwind/EH execution is not tested.

## Raw and normalized result

The outer order table at `01EEC6A8/01EEC6B0` does point both words to `002FDDA0`.
That part of the earlier evidence remains correct. The *inner* handler switch is:

1. Read `EDX = zero_extend(word[unit+0x714])` at `002FDDB0`.
2. Bound the first-switch index `message - 0x4046` to 0..0x4B.
3. `002FDE23` reads a **selector byte** from `002FE54C + index`.
4. `002FDE2C` reads the **arm RVA** from `002FE534 + 4*selector`.
5. Add image base 0x120000 and jump at `002FDE37`.

The retained 76 selector bytes address six arm RVAs:

| Messages through this first switch | Selector | Original arm |
|---|---:|---|
| 0x4046–0x4047 | 0 | 002FDE39 |
| **0x4048–0x404F** | **1** | **002FDE7B** |
| 0x4050 | 2 | 002FDE98 |
| **0x4051–0x4070** | **3** | **002FDF18** |
| **0x4071–0x4090** | **4** | **002FDF5A** |
| 0x4091 | 5 | 002FDEC1 |

Thus 0x4049 and 0x404A select byte 1 and go to `002FDE7B`. That arm subtracts
0x48 from DL, stores 1/2 into `byte[unit+0x54]`, sets `byte[unit+0x6B4]=2` and
returns EAX=1 locally. It has no CALL or branch into the status arms. A nonzero
entry phase at +0x6B4 returns earlier, before the switch. These are conditional
source effects, not observed command acceptance or player-visible presentation.

The actual status-arm message domains yield:

- `002FDF1F`: `(0x4051..0x4070 - 0x51) mod 2^32` = 0x4000..0x401F,
  so **R8B = 0..31** at call `002FDF40`.
- `002FDF61`: `(0x4071..0x4090 - 0x71) mod 2^32` = 0x4000..0x401F,
  so **R8B = 0..31** at call `002FDF79`.

The complete handler code contains the same two named `0030E360` call sites.
Its other physical switch target sets do not select these status-arm entries.
EDX remains the loaded message through the first dispatch until each LEA computes
R8D; RDX is changed to the stats pointer afterward. The full 76-member normalized
mapping and positive boundary cases are in `ov58d-order-switch-result-02.json`.
They are finite data/arithmetic proof cases, **not 76 machine-code executions**.

With the existing record premise `rec=state+8+0x1C8*k`, k<=39 and the retained
id byte unchanged at the displayed store sites, max id31 gives:

| Record | Dword site's highest end (exclusive) | Word site's highest end (exclusive) |
|---:|---:|---:|
| 38 | state+0x44F4 | state+0x4534 |
| 39 | state+0x46BC | state+0x46FC |

Both are below region-A start state+0x4748. This refutes the *two-site high-ID
premise*. Generic `0030E360` still accepts an unmasked byte and these controls
do not establish bounds for every other caller or arbitrary corrupted state.

## Controls, failures and reproducibility

The actual capture exercises shared store/LEA/RMW controls. Its first attempt
refused before source output: the chosen final store span ended partway through
the 8-byte instruction at `0030E5AF`. Original bytes establish end `0030E5B7`;
the corrected capture succeeds. Old driver/error/terminal exit are preserved.
No incomplete capture is accepted or stretched into an empty result.

The final prover requires successful terminal capture, exact source/driver
bindings, re-decodes with the reviewed adapter, and directly rechecks *both
code and table bytes* against the pinned shipping image. Its earlier positive
used a checked capture; direct rechecking was added before final sealing. Both
driver/result generations stay immutable and final result02 names final code.

Five labelled synthetic controls run through the actual final CLI: failed
capture, coherent 4049 selector mutation, coherent LEA-offset change, missing
selector table and wrong store role. Each refuses with the expected diagnostic
and no result. These are producer regressions, not native or independent runs.

Reproduce in this directory using the existing project Python:

    python prove-ov58d-order-switch.py . ov58d-order-switch-capture-02.status.json NEW_RESULT.json
    python control-ov58d-order-switch.py NEW_CONTROLS_DIRECTORY

The source capture can be reproduced from the ASTRA preparation directory with
the same original EXE and reviewed helpers, into a fresh output. Fixed source
and receipt names bind this archived generation; never overwrite them. No broad
export, new runtime framework, or failed EXP-127 trace is involved.

## Interpretation, consumers and remaining limits

One previously runtime-labelled **proposition** is answered without gameplay.
No entire runtime/register row is awarded. The prior sender search/caller census
belongs to SWE2-STRUCT and is not an additional test performed here.

STRUCT must correct its caller-cone and residue wording and the switch-decoding
procedure that assigned message offsets directly to arm entries. FABLE must
remove this particular named-reach exception from its T3b state-region-A account
after acceptance. OPUS must use the bounded arguments at these two exact call
sites while preserving generic callee/unproved other-caller limits. Independent
review must examine original dispatch bytes and the byte-selector stage, not
only compare the normalized output with itself.

If another caller or alias remains, name its original address, complete argument
provenance and discriminating state. Natural Esper order production, scheduling,
native transitive effects, save aliasing and actual lifetime/placement are not
established here. None is needed to falsify the queued 4049/404A high-ID route.

Cleanup: finite checked child processes terminate; original image/helper/source
identities are preserved. No game, PC control, native instrumentation, saves,
configuration or peer processes were touched. The menu extension remains
unapproved and its allowance spent; EXP-127 remains INVALID_POST_TRACE.
Full L1+L2 goal ACTIVE/NOT_MET. Take the next independent unresolved proposition
while review/publication waits; do not retry this settled route in a fight.
