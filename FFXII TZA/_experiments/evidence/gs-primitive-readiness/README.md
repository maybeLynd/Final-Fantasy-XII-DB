# GS primitive readiness: lists, strips and ADC

The renderer page's unread list-versus-strip gate is a **saturated phase counter,
an equality test, an ADC bit and a carry/reset rule**. Original integer components
were executed; vertex conversion, index generation and drawing were explicitly
omitted. No full packet or visible output is certified.

`source.json` retains original bytes/disassembly, tool/reference identities,
controlled boundaries and consumer preimage. `raw-results.json` retains each
original executed PC/register/access/counter transition, including dirty-state
initialization and the first three triangle-list control candidates. They were
retained and extended, not repeated to inflate results. `check.py` independently
reduces these producer artifacts without rerunning the emulator; independent
semantic review is still required.

## Mechanism and observed controller patterns

Actual PRIM setter0020FE70 calls0020FBA0 and **then resets phase and vertex count**.
The leaf alone is not that initializer. XYZ2 prefix0020F6B5 increments phase
at01F83574 and uses signedCMOVG to saturate at required01F83570. After the omitted
vertex writer,002102E8 tests bit47 of inputqword+8; if clear, it compares phase
and required, returning AL1 only on equality. Caller0020F70D testsAL, and true
resets phase to carry01F8356C before index dispatch.

| existing primitive mode/name | required | carry | first six candidate AL results |
|---|---:|---:|---|
| 0 point | 1 | 0 | 111111 |
| 1 line list | 2 | 0 | 010101 |
| 2 line strip | 2 | 1 | 011111 |
| 3 triangle list | 3 | 0 | 001001 |
| 4 triangle strip | 3 | 2 | 001111 |
| 5 triangle fan | 3 | 2 | 001111 |
| 6 sprite | 2 | 0 | 010101 |

Fan also sets its separate fan flag; it does not become a strip because the
readiness pattern matches. Sprite's later index generation likewise differs
from line-list geometry. These names come from the current page's index arms.
With triangle-list ADC inputs001000, AL is000100: the suppressed third candidate
leaves saturated phase3, the fourth can pass, then carry0 resets it.

## Evidence limits

First observer labelled primitive byte01F83560 instead of01F83562. The initial
checker rejected the package before acceptance. First driver/source/raw/check
and exact failure are preserved in`historical-observer-failure/`; no live/accepted
result depends on them. Corrected observer derives all seven addresses from original
RIP operands and checks producer20FE7B against reader20FBA0 before execution. Only
affected bounded groups were rerun. Historical raw labels remain invalid; they are
not silently rewritten or counted as another accepted experiment.

Executed full PRIM setter/leaf; phase prefix stops **before** capacity/geometry;
gate enters **after** the writer call with a controlled matching frame;
consumer stops **before** index dispatch or shared continuation. No native-effect
stub is used, but the omitted boundaries are just as material. Counters are held
unchanged across that omitted writer boundary. Actual vertex-count increment,
coordinates, matrix work, exceptions, aliasing, generated indices, submissions
and game scheduling are not proved. The guest vertex count remains0 deliberately;
candidate steps are not claims of complete vertex execution.

For tested valid small counts, original phase/control transitions distinguish
lists from strips and ADC behavior. No universal overflow rule, unsupported mode7
behavior, natural frequency or complete GS parity is inferred. Caller AL widths
and signed comparison must remain explicit. FABLE/OPUS incorporation and independent
SPEC review are pending; no contract/type/family exclusion is invented.

Player version: separate lines and triangles reset progress after each completed
shape. Connected strips keep one or two points' worth of progress. The tested
control bit can suppress a ready result without resetting progress. This explains
the original decision code; it does not establish a picture or complete draw.

PC off/disposable guest only. No FF12/native attach/input/instrument/save/config
or reference writes; no fresh live restoration receipt. Whole L1+L2 database goal
and required final reviews remain NOT_MET, with L3 later.
