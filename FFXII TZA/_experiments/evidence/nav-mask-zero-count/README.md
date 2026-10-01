# BMASK: piecewise clamp and positive-dimension precondition

Question: does the navigation corridor family's BMASK003912E0 enforce
`[0,count-1]` for every header/count, and is the current producer sufficient to
prove its negative-index behavior? Consumers: OPUS/FABLE corridor contract10.2,
OPUS conv_checkX3. This is a separate original helper/domain question; no previous
PQUERY upper-edge, finite conversion or authored13x13 calculation was repeated.

**A original292B static evidence.** Shipping SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
PE function003912E0..00391403. Full raw bytes/decode/reader/PE extent identity,
canonical consumer/producer preimages and actual Python control receipts included.
`check.py` binds all four paths, their operands, branch targets and loop/index use.
There were **zero original FF12/emulator/native/live executions**.

The hypothesis “a negative input is first zeroed, then clamped to count-1” is
**refuted**. Each negative path zeroes its register then **jumps past** the upper
clamp. The exact conditional rule, in the stated non-overflow count domain, is
`f(i,count) = i<0 ? 0 : min_signed(i,count-1)`.
For positive counts this agrees with an ordinary range clamp. With count0,
negative inputs (including INTMIN) still become0; nonnegative inputs become-1.
Thus the existing “negative becomes0” statement is retained, while a universal
`[0,count-1]` guarantee needs **positive dimensions**. Do not silently replace
the original piecewise operation with either min(max(i,0),count-1) or
max(min(i,count-1),0) over empty/invalid dimensions.

There is no dimension-zero branch before the rectangle loops. Under stable
globals, normal return from the earlier memset, valid bound memory and count0 on
both axes, all-zero endpoints clamp to-1 and enter the first loop iteration;
the signed32 index `col+row*cols` becomes-1, sign-extended before the validity-byte
read at00391394. All-negative endpoints become0 and read validitybase+0 despite
zero dimensions. Negative starts and zero ends produce an inverted range and
skip the loop. The positive1x1 control reads index0. These are **conditional
source calculations**, not native reads/faults or proof ordinary game state has
empty dimensions. The later record OR/output depends on that validity byte and
additional bound globals; it is not promoted from the first read.

Producer defect: the actual unchanged conv_check invocation still reports X3PASS,
FAILS0 on a disposable file-read supply where the original negative-path JMP
00391320 is replaced by NOPs. That mutation destroys “negative always0” at count0,
but its X3 checks the TEST/zero/upper CMOV without binding the bypass. The shipping
image and peer files were never changed. The baseline also passes. Our exact
source obligation rejects the corresponding292B mutation. Required owner fix:
bind the JNS/JMP destinations for all four piecewise paths and state the positive
dimension interval precondition. Preserve prior records and the current tested
producer version; correction of result prose alone is insufficient.

Limits: count-minus-one arithmetic here is for count0 and ordinary positive signed
dimensions; all malformed count-bit patterns/overflow are unproved. Normal native
memset behavior, actual dimension-zero occurrence, initialization/builder,
allocation/lifetime, atomicity, input conversion, fault behavior and live scene
safety stay open. Source tool identity and two Python producer controls do not
constitute independent project acceptance. Owners/reviewer incorporation pending.

Cleanup: disposable input supplies restored and children exited; exact reference
hash unchanged, no game/PC/process/save/config/peer writes. Published earlier
inputs/results immutable. PC OFF; whole L1+L2 goal NOT_MET.
