---
contract: run the frame's sixteen gated subsystem updates, in the order the pump emits them
category: 00-Engine-Core-Runtime
scope: family
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md
entries: ["0028E290"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 33 addresses cited - 4 data, 21 entry, 8 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-frame-gate-pass-1    # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the per-frame update gate

One ~~16-bit~~ 32-bit word *(corrected 2026-10-02, OPUS: eight `test dword` sites, e.g. `0028E290+0x16F`; the `uint32` row of §2)* at `01E0C464` decides which subsystems tick, and `0028E290` is the fan-out that reads
it sixteen times. The page this implements establishes the word, the masks and the groups. **What a
reimplementation needs beyond that is the order** — and the order is not the bit order.

## 1. Purpose

To state the frame's gated update sequence as an operation: what is read, in what order the calls are
made, what is not touched, and which of the obvious implementations is wrong.

## 2. Interface

| | |
|---|---|
| entry point | `0028E290`, 745 bytes |
| reached from | `002507C0`, itself from `0022A770` and `0022B7E0` |
| parameters | `ecx` — **`0028E2A0` keeps it and `0028E3B7 test dil, 1` gates a group on its low bit.** See the box below; this row said "none used by the gate logic" until 2026-09-12 |
| returns | nothing |
| the enable word | `01E0C464`, **`uint32`** — ships `FF FF FF FF` and **nothing writes it** (§10). *CORRECTED 2026-09-25 (OPUS): this cell said `uint16`. Eight of the sixteen tests are `test dword ptr` (e.g. `0028E3FF test dword ptr [01E0C464], 0x1000`), which read bytes +2..+3, and MSVC does not emit a dword read of a 2-byte global; §3 proves not-`uint8`, not `uint16`. Fifteen bits are live (0x0010 and 16-31 are never tested). Declared as `FrameUpdateGateEnableWord` 4 bytes.* |

**The gate sits inside a render-path call neighbourhood.** Both parents of `002507C0` —
`0022A770` and `0022B7E0` — also call **Presentation**-layer bodies (`0036F2C0`, `0036F2F0`,
`002E65A0`, `00375500`, `0037D4C0`…), and the gated group-2 body `001EDE80` is additionally invoked
directly by `003E00C0` (interior read 2026-09-17, SWE2-FRONTIER: `0020E600` first at [`003E00D5`](../_index/ADDRESS-INDEX.md), `0036D9E0` next — the master pose evaluator) and `00477480`, bypassing the gate — 20 edges total. The word selects which
subsystems tick; the ticking is done by code that is mostly the draw path.

## 3. Types

The enable word is **not a `uint8`**. Eight sites test it as a byte (`0x0001`–`0x0080`) and eight as a
dword (`0x0100`–`0x8000`); a byte test cannot reach past bit 7, so the high half must be read wider.
**A reimplementation that declares the enable as `uint8_t` silently loses eight of the sixteen groups.**

> ### ⚠ Sixteen test sites, FIFTEEN bits — and the gate does read its argument
>
> **CORRECTED 2026-09-12 (`OPUS-FRAMEGATE-ISOLATED`), by counting the sites and then executing
> them.** The width split above is exactly right: eight byte tests and eight dword tests, confirmed
> instruction by instruction. What the range `0x0001`–`0x0080` implies is not.
>
> **§15 already knew.** Its evidence paragraph records *"fifteen distinct bits with a hole at
> `0x0010`"*, independently derived. So this is not a discovery against the contract — it is the
> same failure as the one this programme found in `CONTRACT-character-transform-publish`: **the
> contract knew and its `Types` section did not say**, and a reimplementer reads `Types` for the
> shape. The correction belongs here, where the wrong impression is formed.
>
> The byte immediates actually present are **`1, 2, 4, 8, 0x20, 2, 0x40, 0x80`**:
>
> - **`0x10` never appears. Bit 4 gates nothing at all.** Driving it alone produces an empty trace,
>   and §13 shows that rather than asserting it.
> - **`0x02` appears TWICE**, at `0028E2B7` and `0028E3AE`, gating two unrelated groups with six
>   other groups between them. Driving bit 1 alone produces both, in that order.
>
> So the sixteen sites cover **fifteen** distinct bits. A reimplementer reading "`0x0001`–`0x0080`"
> as all eight would wire a group to bit 4 that the original leaves dead, and would split bit 1's
> pair apart.
>
> **And §2's "none used by the gate logic" is wrong.** `0028E2A0 mov edi, ecx` keeps the first
> argument across the whole body, and `0028E3B7 test dil, 1` gates the second of bit 1's two groups
> on its low bit. A reimplementation taking no parameter runs that group unconditionally — driven at
> both parities in §13, where the two traces differ by exactly that group.
>
> **The last group is a tail jump.** Bit `0x0800` restores, adjusts the stack and `jmp`s at
> `0028E56A`, so it is the last thing on its own path and nothing can follow it.

## 4. Preconditions · postconditions · invariants

**Preconditions.** None checked. The gate reads a static word and calls; it validates nothing.

**Postcondition.** Every group whose bit is set has been called exactly once, in the order of §6.

**Invariant: a clear bit is a skip, not a degrade.** The subsystem does not run slowly or partially
that frame; it does not run. Nothing accumulates and nothing is caught up next frame.

## 5. State

| | what | evidence |
|---|---|---|
| read | the enable word at `01E0C464`, ~~sixteen bits~~ a dword whose low sixteen bits are tested *(corrected 2026-10-02, OPUS: `0028E290+0x16F` `test dword`)*, every frame | the sixteen test sites, §3 |
| read | the object behind `0209BE80`, re-loaded from its slot after almost every group | `mov rbx, [rip+...]` between groups |
| written | `object+0x10F68` bit 1, and the three pointer fields `+0x10F20`, `+0x10F30`, `+0x10F40` | §12; each is a callee's result stored back |
| allocated / deallocated | none | |

**The gate writes nothing else.** Everything else it does is deciding who else writes.

**Added 2026-09-12** — this contract had no §5 and every later heading sat one number below the
template, so `check_gate26` could not find its runtime section and `parity_status` read the parity
plan where the evidence table should be. *A section number is part of the evidence.*

## 6. State transitions — the frame order, which is NOT the bit order

Read from `0028E290` by pairing each `test` of `01E0C464` with the call **or tail jump** it guards:

| # | mask | test width | call |
|---:|---|---|---|
| 1 | `0x0001` | byte | `00289970` |
| 2 | `0x0002` | byte | `001EDE80` |
| 3 | `0x0004` | byte | `002917E0` |
| 4 | `0x0008` | byte | `003F6BB0` (interior read 2026-09-17, SWE2-FRONTIER: `002713E0` at [`003F6CEA`](../_index/ADDRESS-INDEX.md) and again at `003F6D05`) |
| 5 | `0x0020` | byte | `003F9F40` |
| 6 | `0x0002` | byte | `00291B90` |
| 7 | **`0x1000`** | dword | `00273900` |
| 8 | `0x0040` | byte | `003F80D0` |
| 9 | `0x0080` | byte | `00296860` |
| 10 | **`0x2000`** | dword | `00290CF0` |
| 11 | **`0x4000`** | dword | `00290EB0` |
| 12 | **`0x0100`** | dword | `003F8EC0` |
| 13 | `0x0200` | dword | `003F31B0` |
| 14 | `0x0400` | dword | `003FA790` |
| 15 | `0x8000` | dword | `002C6180` |
| 16 | **`0x0800`** | dword | `0028C870` — **reached by `jmp`, not `call`** |

**The obvious implementation is wrong.** Iterating bits `0..15` and calling each set group runs the
frame in a different order from the original: `0x1000` executes **seventh**, ahead of `0x0040` and
`0x0080`; `0x0100` executes **twelfth**, after `0x2000` and `0x4000`. Any subsystem that reads state
another writes — and in a frame pump that is most of them — sees different inputs.

**Bit `0x0002` runs twice**, at positions 2 and 6, gating two different calls. One bit, two groups, at
two points in the frame; a reimplementation keyed one-bit-to-one-subsystem cannot express it.

**The sixteenth group is a tail jump and is the frame's last act.** `0028E54E` tests `0x0800` and
`0028E56A` does `jmp 0x28C870` after restoring the frame — so the pump *returns through* its final
group. **This row was missing from the first version of this contract**, whose extractor paired each
`test` with the next `call` and therefore could not see a tail-jumped group. That is the same
instrument failure that hid `FUN_003847B0` from a registry sweep earlier the same day; a `call`-only
matcher is wrong twice over in this image.

So there are **sixteen gated groups across fifteen distinct masks**, not fifteen groups — the page's
"fifteen" counts *bits*, and two of the sixteen share `0x0002`.

**Bit `0x0010` is absent** — fifteen distinct bits, every one of the low sixteen except this. Retired,
reserved, or handled elsewhere is **not established**.

## 7. Relationships

The sixteen callees are owned by their own subsystems; this contract owns only the fan-out. The page
identifies the groups.

## 8. Script · resource · event interactions

None. The gate reads no authored data.

## 9. Determinism

Total, given the word. No RNG, no timing, no threading in the fan-out itself.

## 10. Failure paths and edge conditions

**There is no hand on the switch.** The word ships as `FF FF FF FF` and nothing in the image writes
it, takes its address, or encodes it — so in this build all sixteen groups always run and the facility
is inert. **Re-tested 2026-09-11** (`OPUS-GATEWORD-RETEST`) with a raw byte scan of all `.text`,
deliberately tolerant of instruction length and independent of the function graph: 20 candidate sites,
two carrying a `lea` prefix, **both false** — they take the addresses of `01E0C45C` and `01E0C460`, the
neighbouring pointer table, and the scan's tolerance mapped them onto this word.

**The residual limit, unchanged:** a write through an address computed by arithmetic rather than `lea`
would be invisible to any static sweep, here as for every global.

## 11. Observable behaviour

Not established, and it cannot be observed without modifying the word, because in the shipped build it
is never anything but all-ones.

## 12. Reproduction formula

```c
void FramePump(void) {                      /* 0028E290 */   // <- corrected 2026-10-02, OPUS - one argument (word[01E0C2B0], 0028E290+0x10 mov edi, ecx), and the handlers take a pointer, e.g. rcx = [0209BE80] + 0x5380 for 00289970 (0028E290+0x14 to +0x22)
    uint32_t en = *(uint32_t*)0x01E0C464;   /* 4 bytes: eight dword tests; NOT a uint8 -- see section 3 */
    if (en & 0x0001) Group_00289970();
    if (en & 0x0002) Group_001EDE80();
    if (en & 0x0004) Group_002917E0();
    if (en & 0x0008) Group_003F6BB0();
    if (en & 0x0020) Group_003F9F40();
    if (en & 0x0002) Group_00291B90();      /* same bit, second group */   // <- corrected 2026-10-02, OPUS - and only when (arg & 1): 0028E290+0x127 test dil, 1
    if (en & 0x1000) Group_00273900();      /* out of bit order, deliberately */
    if (en & 0x0040) Group_003F80D0();
    if (en & 0x0080) Group_00296860();
    if (en & 0x2000) Group_00290CF0();
    if (en & 0x4000) Group_00290EB0();
    if (en & 0x0100) Group_003F8EC0();
    if (en & 0x0200) Group_003F31B0();
    if (en & 0x0400) Group_003FA790();
    if (en & 0x8000) Group_002C6180();
    if (en & 0x0800) Group_0028C870();  /* a TAIL JUMP in the original */
}
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent, and it is absent for an
unusual reason.** (2026-09-12)

The 745-byte body runs at its real virtual address under Unicorn against an independent
reconstruction, with the enable word mapped at `01E0C464` and the object's slot at `0209BE80`,
because the gate reaches everything through those two globals.

**Instrument:** [`diff_frame_gate.py`](../../../Reconstruction/Tests/Differential/diff_frame_gate.py)
against [`frame_gate.c`](../../../Reconstruction/Game/Core/frame_gate.c).

**Result: 390 commands, 70 compared lines, 0 mismatches** — 20 distinct traces out of 35, **all 23
callees reached at least once**, and 10 empty traces.

**The comparison is the trace, because choosing is what this operation does.** Every callee is
hooked and the call sequence with its arguments is what gets compared; a reconstruction running the
same groups in a different order fails here and would pass any test of a single subsystem.

### The three corrections, each driven rather than argued

1. **Bit 4 gates nothing.** Driven alone, it produces an empty trace — as does the all-off run, which
   is the control that makes the empty trace mean something.
2. **Bit 1 gates two groups.** Driven alone, it produces both, with the six groups between them
   absent, which is what shows they are two sites and not one.
3. **The argument is read.** Bit 1 at `arg0 = 0` and `arg0 = 1` produce traces differing by exactly
   the second group. §2 said no parameter was used.

**The unused argument registers are not compared, and that is deliberate.** The MS x64 ABI leaves
them undefined for a callee that does not take them, and the shipped code leaves whatever was last
there — so the first run of this suite reported eight mismatches that were facts about the
instruction before each call. Each callee's arity is read from its own call site and only that many
arguments are printed, on both sides.

### How far the instrument itself has been tested

**57 mutants: 45 KILLED · 3 EQUIVALENT · 9 SURVIVED · 0 NO_BUILD · 0 TIMEOUT · 0 INVALID.**
Production inputs verified stable, all four hashes checked against the working tree afterwards.

**The nine survivors are one cause, and the cause is a decision made earlier in this same pilot.**
They are the zeros the reconstruction passes for arguments a callee does not take. Since each
callee's arity is read from its own call site and only that many arguments are compared, those
padding values are not observed — deliberately, because the shipped code leaves whatever was last
in the register and comparing them compares the instruction before the call. **The nine are the
visible price of that decision, and the alternative was eight false mismatches on the first run.**
An unused argument's value is not part of this contract, so no case can or should distinguish them.

**Four survivors from the first campaign WERE real, and they were one hole: no case set flags bit
0.** Widening `& 8` to `& 9`, `& 0x100` to `& 0x101`, and bit 12's fold from `& 2` to `& 3` are all
invisible while that bit is always clear — three different tests, one missing input. Cases driving
flags bit 0 alone and beside each test's own bit kill all three, and a fourth case pairing a null
`+0x10F78` with a non-null `+0x10F80` kills the field-offset mutant that could only show when two
adjacent pointer fields disagree. First campaign 41 killed of 57; second, 45.

**The three `EQUIVALENT` rows are the two global addresses and the object size**, which this file
carries as documentation — the gate takes its object and its enable word as parameters and does not
read the globals — and which the tool proves byte-identical.

### Why no live read is queued

Unchanged from the previous revision and worth keeping: the check that would matter needs a
**modified** enable word, not a capture — clear one bit and confirm exactly one group stops. §9 says
nothing in the image writes the word, so there is no state to catch it in. That is a different
situation from "not yet captured", and it is why this contract queues no read.

The check that would matter needs a modified word rather than a capture: clear one bit and confirm
exactly one group stops. Until the word can be written, §11 stays empty by construction — which is a
different situation from the usual "not yet captured", and is why this contract does not queue a
read.

## 14. Unresolved

- ~~What `0x0010` was for~~ — **closed 2026-09-22 (SWE2-CONTRACT): provably dead, intent not
  recoverable — this is `UQ-26`, already signed NO ADMISSIBLE SOURCE (OPUS/FABLE,
  2026-09-16), and this census independently reproduces it.** A per-body rip-relative census
  over all 35,713 `.pdata` bodies finds exactly **sixteen** references to `01E0C464` in the
  whole image — the pump's sixteen `test`s and nothing else: no writer, no `lea`, no second
  reader, and no test anywhere uses mask `0x10`. Bit 4 is therefore set (~~`0xFFFF`~~ `0xFFFFFFFF` at ship *(corrected 2026-10-02, OPUS: the image bytes at `01E0C464` are `FF FF FF FF`)*) and
  never consulted; whether it was a retired group, a reserved slot, or never used cannot be
  recovered from this build — the signed verdict's exact scope. Addendum: there is no
  structural residue either — the byte-mask sequence `1,2,4,8,0x20,…` is not strictly sorted
  (the second `0x0002` sits between `0x20` and `0x40`), so the pump's order is authored
  control-flow order and a deleted `0x0010` group would leave no positional scar.
- ~~Whether the two `0x0002` groups are related, or share a bit by accident of history~~ —
  **closed 2026-09-22 (SWE2-CONTRACT): two independently authored `if`s on one flag, not one
  group split and not a compiler artefact.** Group A (`0028E2B7`) is `001EDE80` — the
  ~~pause/cutscene-name-slot predicate~~ 60 fps half-rate predicate *(corrected 2026-10-02, OPUS: `001EDDC0+0x28` sets `01F82E38` with the 60 fps divisor; `0022A080`/`0022A030` read the frame counters `02064AD8`/`02064AA8`)* (`[01F82E38]==0` or `[01DFE0C0]!=0` → return 1, else
  `0022A080()`+`0022A030()` — verified byte-exact) — whose return gates `003F8B40`. Group B
  (`0028E3AE`) is `00291B90`,`003F6100`,`003F24D0`,`003F24A0`, disjoint subsystems, gated
  *additionally* by `dil&1` — the pump's first argument, `word[01E0C2B0]`, written ~~once~~ at
  ~~`002539E5` with `0xF` (so always true in this build).~~ `00253970+0x75` with `0xF` and at `002547C0+0x0` with its caller's `cx` (`00226280+0x203`, `0036D840+0x2B`), so not fixed in this build *(corrected 2026-10-02, OPUS: the two stores to `01E0C2B0`)*. Three facts make it authored, not
  accidental: the second `0x0002` sits out of mask-sort order at an authored position; group B
  carries its own argument gate, so it is not a continuation of group A; and the sole pump
  caller `002508AB` *itself* calls `001EDE80` at `00250896` to gate `003BBA60` before invoking
  the pump — group A is literally a second invocation of the caller's own predicate. Whether
  bit 1 named a category the authors meant to share or collided by history is not
  distinguishable in an image where the word is never written; the structure says deliberate
  reuse of one flag for two separate tests.
- ~~One `test` site unaccounted for~~ — **CLOSED**: it is `0028E54E`, mask `0x0800`, whose group is
  entered by `jmp 0x28C870` rather than `call`. All sixteen sites are now in §6.

## 15. Evidence

Static, from the shipping image (`73461D08…`). The order, masks and test widths were extracted from
`0028E290` by a disassembler pairing each `test` of `01E0C464` with the transfer it guards — **`call` alone was not enough, and the first version of this table lost row 16 to exactly that** — and the
byte/dword split and the absence of `0x0010` **reproduce the page's independently derived counts** —
eight byte tests, eight dword tests, fifteen distinct bits with a hole at `0x0010`. That agreement is
why the ordering table is offered as more than one reading of one function.

**Claim table added 2026-09-12 (`OPUS-FRAMEGATE-ISOLATED`).** The paragraph above states the method
and is kept; the table enumerates the claims so `diff_frame_gate.py` can map to them.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the enable word is at 01E0C464 and gates sixteen groups | sixteen `test` sites, each paired with the transfer it guards. Executed — each bit driven alone, and the resulting traces partition the twenty-three callees | 1 (isolated original-code) | PROVEN |
| **the function tests TWO objects, and only sixteen of its eighteen tests are the gate** | **found 2026-09-12 (§15a)**: `0028E2EE test byte ptr [rbx+0x10F68], 8` and `0028E4B3 test dword ptr [rbx+0x10F68], 0x100` are on a **different object**. A count that does not exclude them returns nine and nine, not eight and eight | 1 | PROVEN |
| eight sites test it as a byte and eight as a dword | the immediates and operand widths, counted. Executed — bits 8–15 each produce their group, which a `uint8` reading could not | 1 (isolated original-code) | PROVEN |
| bit 4 is never tested and bit 1 is tested twice | the byte immediates are `1, 2, 4, 8, 0x20, 2, 0x40, 0x80`. Executed — bit 4 alone produces an EMPTY trace; bit 1 alone produces two groups with six others between them | 1 (isolated original-code) | PROVEN |
| the first argument gates bit 1's second group | `0028E2A0 mov edi, ecx` and `0028E3B7 test dil, 1`. Executed at both parities; the traces differ by exactly that group | 1 (isolated original-code) | PROVEN |
| the last group is a tail jump | `0028E56A jmp 0x28C870` after the epilogue. Executed — its callee is last in every trace it appears in | 1 (isolated original-code) | PROVEN |
| each group's inner conditions are its own | the null tests and the two flag-bit tests at `+0x10F68`. Executed — every inner pointer driven null and non-null, and both flag bits at both values, independently of the enable bit reaching them | 1 (isolated original-code) | PROVEN |
| any runtime observation | — the check needs a WRITTEN enable word, not a capture; §13 | none | UNKNOWN |
| the sixteen tests are the word's only accessors | per-body rip-relative census over all 35,713 `.pdata` bodies: exactly 16 references to `01E0C464`, every one a `test` inside `0028E290`, none masked `0x10`; no writer, `lea`, or second reader exists — bit 4 is dead image-wide, not just in the pump | 1 | PROVEN |
| the two `0x0002` groups are two authored `if`s, not one group | group A `001EDE80`→`003F8B40` (predicate verified byte-exact: `[01F82E38]`/`[01DFE0C0]` then `0022A080`+`0022A030`); group B `00291B90`/`003F6100`/`003F24D0`/`003F24A0` under `dil&1`; the pump's sole caller `002508AB` itself calls `001EDE80` at `00250896` gating `003BBA60`, and feeds the pump `word[01E0C2B0]` (~~single writer `002539E5`, value `0xF`~~ two writers: `00253970+0x75` stores `0xF`, `002547C0+0x0` stores its caller's `cx` *(corrected 2026-10-02, OPUS: the two stores to `01E0C2B0`)*) | 1 | PROVEN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

**Both counting claims reproduce exactly**, by disassembling `0028E290` whole and classifying every
`test <mem>, imm` by operand width and by bit:

| | |
|---|---|
| tests on the gate | **8 byte + 8 dword = 16**, and **every one resolves to `01E0C464`** — there is no second gate |
| bit 4 | **never tested** |
| bit 1 | **twice** — `0028E2B7` (byte) and `0028E3AE` (byte) |
| every other bit 0–15 | exactly once |

### The refinement, and it exists to protect the claim

The function contains **eighteen** `test <mem>, imm` sites, not sixteen. Two are on a **different
object**: `0028E2EE test byte ptr [rbx + 0x10F68], 8` and `0028E4B3 test dword ptr [rbx + 0x10F68],
0x100`.

**A re-checker with a looser instrument gets nine and nine and reports a refutation.** It would be
wrong, and the reason is one word the claim did not have to say until now — *it*. The new claim above
says which sites are the gate's and which are not, so the next sweep can agree with this one.

> **This is the third census in this sweep whose number depends on a qualifier**: the inventory
> table's *rows carrying NULL* (seven, not four), commit-action's *immediate* sites (40, not 171),
> and now the gate's *own* tests (16, not 18). **A count is a claim about a population**, and the
> population is where these go wrong — never the arithmetic.

**Mechanical:** no body-size drift; banned-evidence sweep clean; `0028E290` resolves at 745 bytes
with 23 callees, and all 20 cited functions resolve.

## 16. Parity plan

Reproduce the **order** first — it is the thing a correct-looking implementation gets wrong, and no
test of a single subsystem detects it. Then the **width** of the enable, then the **twice-run bit**,
then the fact that a clear bit skips rather than degrades.

## 17. Related

- `00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md`

*(Pass 22 adjacency, 2026-09-14, tail rows: `0022A770` calls **achievements** `00316930`,
**party** `00358BB0` and **audio** `0036F460`, and `001EDE80` is called by **movement**
`0025DF00` (4 edges) — the same gate-frame shape the note above describes; the frame's callees
span every layer it ticks.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (12 edges through 5 of this page's functions).** The ActorEntity layer reaches this page at `0025DF00`, `00358BB0`, `002E65A0`, `003F6BB0` and 1 more. `ActorManager_RunFieldRuntimePass` is the worked example, read in full - it is the field-runtime pass over one manager record - `02098E10` at the **`0x288` stride** - which returns at once while the write-in-progress flag is set; **2 of the 11 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (28 edges through 13 of this page's functions).** The UI layer reaches this page at `0028E290`, `002507C0`, `002917E0`, `003F8EC0` and 9 more. `FUN_0028faf0` is the worked example, read in full - it is a 75-byte step over the HUD object at `[0209BE80]`: it sets **bit 8 of `dword[+0x10F68]`** and then works the `+0xA0` and `+0x80` sub-objects; **2 of the 23 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — MECHANICAL (4 edges, a shared callee one remove away).** The `003F26F0` section cites `00203170`/`00202F00`, and the batch-33 `00322C50` mention predates it; the Gameplay layer's `00339630` also calls `00203170`/`00202F00` and `0031B9F0`/`0031C5D0` also call `00322C50`. The crossing is those shared leaves being consulted by both sides — this page owns the update gate, not whatever Gameplay uses the same helpers for. Edge list from `edges.tsv` (batch-52 audit, SWE2-EC7).

**Resource — CLIENT and SERVICE (SWE2-EC7-157, 38 edges).** Batch-122's `002E6EB0` names the shared helpers `0036C1D0`/`0036C1A0`/`002E9920`/`0036B160`/`0036C5D0`/`002ED6F0`/`0036A000`/`0032E620`/`0036C140`/`0036C110`, several of which sit in the resource layer's neighbour set (`00181000`/`00181250` call `0024A1D0`) — shared fan-in, not a shared responsibility.

**Script_VM_Native_Bridge — CLIENT (SWE2-EC7-157, 33 edges).** `002E6EB0`'s callees and their callers reach the bridge layer (`00202F00`/`00203170` called by `00356160`, `00229E40` by `0033FED0`); the gate page's helpers are consulted there, not owned there.

**CombatAction — CLIENT (SWE2-EC7-166, 10 edges).** The `00263C20`/`00322C50`
helpers this page's `002BF0E0` classifier runs are also consulted by the
CombatAction layer - `00322C50` by `002FFCF0`/`003060E0`/`003093xx`,
`00263C20` by `0030AB40` (+6 more of the same shape). Consultation of
shared leaves, not shared ownership of the gate.
**Input — CLIENT (SWE2-EC7 batch-150).** The `003C80C0` entry's `0053DD10` quiet-check reaches into the Input layer (`0035FCA0`/`0035FDD0`/`0046DD50`/`002E09A0` callees) beside the `0022A770` rows already here - the same shared gate consulted there, not an input path this page owns.

**Save_Load_Settings — CLIENT (SWE2-EC7 batch-150).** `003C80C0`'s `003148F0` first-stage check is called by that layer's `00583D60` and calls `002EF2B0` in turn - a shared scheduling leaf, no save-image business of the gate.

**Spawn_Encounter_Lifecycle — CLIENT (SWE2-EC7 batch-150).** `003148F0` is likewise called by that layer's `00233780` - one more caller edge through the same shared check.
- **RNG_Random_Selection — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_NextU32_Thunk` (00379CD0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **Combat — MECHANICAL (1 edge).** 1 inbound (Combat bodies `003206E0` call page-cited `ActorWork_GetBattleUnitRaw` (00263E30)) - shared-helper call surface, not a Combat relationship of this page's subjects.
## Interior citation — frontier hub `002E65A0` (2026-09-18, SWE2-EC7)

`002E65A0` — 346 B, 8 A-measured callers; the drain sweep the update gate brackets. Interior
verified: `002E6900(1)` opens and closes the sweep (`002E65BF`/`002E666E`); between them the
`0215FD88` list is walked to its tail, then each node with `[+0x10]` set and neither
`+0x18` bit 3 nor `+0x19` bit 2 has its handle resolved through `0020E600` at
[`002E662B`](../_index/ADDRESS-INDEX.md), delivered to `0041E490`, and freed by `002E9360` (`002E663D`), the
head pointer `0215FD88` stepping down the `+0x00` link. Afterward `00369C60(6, 1)` and
`00369C60(10, 1)` post, `002E6880`/`002E6700`/`003DD4C0`/`0037B2F0` run in order, and the
indirect notify at `0215FD98` (called with the `021641F0` dword) fires once before the slot is cleared — the
full "flush then signal" sequence the gate's callers expect.

## Name-binding removal, completion and the release drain (OPUS, 2026-10-01)

*Consumed from ASTRA's [`namebinding-deletion`](../_experiments/evidence/namebinding-deletion/README.md) (SWE2-AUDIT-SPEC [review](../_index/candidates/auditspec-review-namebinding-deletion-1001/REVIEW.md), ACCEPT, no narrowing). OPUS re-read `002EAEB0`-`002EAECC`, `002E6D66`-`002E6DEA` and `002E93E1`-`002E93F7` at the bytes. Static and conditional: valid records and lists, normal ABI returns and no interfering writes are premises.*

- **Removal can be mark-only.** `002EAEB0` sets `+0x18` bit `0x04` (`002EAEC4`) and returns, with no other write or call, when `+0x18` bit `0x02` and `+0x19` bit `0x04` are both clear. Otherwise it advances the stamp, unlinks the record and retires it. `+0x19` bit `0x04` bypasses the mark-only arm; its meaning is not inferred.
- **Completion of a marked record.** The completion `002E4D20` unpins first. A record marked by removal (`+0x18` bit `0x04`) gets bit `0x08` and skips registration (`0041E580`). `002EA6E0` returns 0 early under that bit, and the callback then sets bit `0x02` and retires the record. Without the mark, the follow-up allocation may return 1, so the callback does not always set bit `0x02`. A successful follow-up sets it at the `002E60F0` tail.
- **This gate's drain releases them.** `002E6D60` enters the cleanup only when `002E6900(0)` returns 0 (`002E6D66`/`002E6D6B`) - *(corrected 2026-10-01, OPUS, on ASTRA's lane-drain correction, re-read at the bytes: which is every normal return, so that test does not gate on IO completion)* and a selected retired record has a non-zero handle `+0x10` (`002E6DAC`). `+0x18` bit `0x08` (`002E6DB3`) or `+0x19` bit `0x04` (`002E6DB9`) skips the unregister `0041E490` (`002E6DDD`) but not the release `002E9360` (`002E6DEA`). `002E9360` requests the child and secondary releases, calls `00369800` on the handle (`002E93E1`, `002E93F2`), clears the handle after it returns (`002E93F7`) and recycles the record. A record with a zero handle bypasses that call.
- **The stamp stays 16-bit.** `INC dword +0x24` then a clear of `word +0x26` is `(old + 1) & 0xFFFF`, as the name-binding page already records; this corroborates it.

**Open.** The producer of `+0x19` bit `0x04`, any natural overlap with a pending read, `00369800`'s and the allocator's own effects, real delivery timing, list progress, and OV-21/OV-25 as wholes. The `movsxd` completion argument and the low-32-bit list comparisons do not establish 64-bit pointer placement.

## SWE2-EC7-30 update (2026-09-18) — `002713E0` resolve-and-copy shim

`002713E0` (49 B) is the resolve `003F6BB0` calls twice: `003588B0(id)`
looks the id up and a null result returns 0; otherwise `00264510(rec,
out)` copies the resolved record into the caller's out pointer and the
function returns 1 — a found-flag wrapper over the registry resolve.
Interior anchor `00271401` (the `call 00264510` copy-out).

## The group handlers' argument is a named sub-object, not an unnamed `obj` (2026-09-18, OPUS)

§13's reconstruction sketch writes the handlers as `Group_003F9F40()`, `Group_00296860()` and so
on — nullary, because nothing had established what they are passed. **They each take one specific
EMBED child of the `0209BE80` singleton**, and that is a signature fact a reimplementation needs
before it can call any of them.

Established by tainting the singleton through the **136 bodies that load slot `0209BE80`** and
taking every `lea rcx,[singleton+d]` that survives to a call — so the displacement is the child's
offset and the callee's `rcx` is the child itself. The anchor column is the instruction inside
each handler that reads its argument at the offset the
[gate page](Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md) §3 already
records, which is what makes the pairing checkable rather than asserted:

| group | handler | argument | child size | interior anchor |
|---|---|---|---|---|
| `0x0020` | `003F9F40` | `ManagerSub0209BE80_57E0` | `0x26C0` | [`003F9F51`](../_index/ADDRESS-INDEX.md) `test byte ptr [rcx+0x249C], 4` |
| `0x0400` | `003FA790` | `ManagerSub0209BE80_57E0` | `0x26C0` | [`003FA796`](../_index/ADDRESS-INDEX.md) `mov rdx, qword ptr [rcx+0x2490]` |
| — | `003FA4E0` | `ManagerSub0209BE80_57E0` | `0x26C0` | [`003FA50E`](../_index/ADDRESS-INDEX.md) `mov qword ptr [rcx+0x2490], rax` |
| `0x0080` | `00296860` | `ManagerSub0209BE80_7FB0` | `0xFF0` | [`00296881`](../_index/ADDRESS-INDEX.md) `lea rbx, [rcx+0x104]` |
| `0x0800` | `0028C870` | `ManagerSub0209BE80_7EA0` | `0x110` | [`0028C88C`](../_index/ADDRESS-INDEX.md) `test byte ptr [rcx+0x74], 1` |
| `0x0100` | `003F8EC0` | `ManagerSub0209BE80_00A0` | `0x52E0` | already carried |
| `0x0040` | `003F80D0` | `ManagerSub0209BE80_A0D0` | `0x990` | already carried |

**One correction to the sketch beyond the signatures.** §3 describes `003FA4E0` as something
`003FA790` calls over the list at `+0x2490`. It does not only read that head — `003FA50E` **writes
it**, `mov qword ptr [rcx+0x2490], rax`. A reimplementation that treats the `0x0400` group as a
read-only walk over that list will diverge on the first entry it retires.

**`0028C870` is the one reached by `jmp`, and §7 already says so.** Its argument is established
from the caller's `0028E55A lea rcx,[rbx + 0x7EA0]` rather than from a handoff at a call, because
a tail jump passes no argument register the scan inspects. The anchor above is instead its own
first use of `rcx`, and it agrees with §3's reading of `+0x74` as the fade-direction bit.

**What this does not do.** It names arguments and confirms extents; it explains none of those
children's contents, which remain about 99 % unknown and are the largest single block of unknown
bytes in the database. ~~Two of the seven — `_5380` (`0x460`) and `_8FA0` (`0x1130`) — are passed to
no handler at all and still have no owner, so the fifteen groups do not account for the whole
singleton.~~ **WRONG, corrected below: every child has owners, and `_8FA0` has the most of any of
them. The fifteen groups still do not account for the whole singleton, but for a different reason.**

### Correction — "no owner" was an artifact of my own scan's blind spot (2026-09-18, OPUS)

The sentence struck through above was **wrong**, and it was wrong in the one way this scan is
documented to fail. `member_reach_scan.py` records handoffs at **`call`** sites. A tail `jmp`
passes its arguments and never returns, so the scan cannot see it — which is stated in that tool's
docstring and is why `0028C870`'s absence was called correct behaviour two sections above. I wrote
that caveat and then read "no handoff" as "no owner" for two other children.

Following tail jumps as the handoffs they are — a `jmp` passes its arguments exactly like a `call`
— **every child is owned**, and most of them several times over. Measured by
`member_reach_scan.py --slot 0x0209BE80`, which tracks the calling convention rather than matching
instruction shapes. Its seed is every body that loads the slot, and the closure over those reaches
rather more; the per-child owners it reports are:

| child | size | owners, `(t)` = reached by tail jump |
|---|---|---|
| `_00A0` | `0x52E0` | `003F8C70`, `003F8D20` (t), `003F8EA0`, `003F8EC0` |
| `_5380` | `0x460` | `00289970`, `00289A10`, `00289D00`, `00289D70` (t), `00289F50` (t), `0028A080` (t) |
| `_57E0` | `0x26C0` | `00244F00`, `00273A20`, `003F9F40`, `003FA160` (t), `003FA4E0`, `003FA570`, `003FA600`, `003FA6E0` (t), `003FA730` (t), `003FA790` |
| `_7EA0` | `0x110` | `0028C870` (t), `0028C940`, `0028C970`, `0028CA30` (t), `0028CA40` (t) |
| `_7FB0` | `0xFF0` | `00296670`, `002966E0`, `00296860` |
| `_8FA0` | `0x1110` | `002BDAE0`, `002BDB00`, `002BDB60`, `002BDC00` (t), `002BDCA0` (t), `002BDCE0` (t), `002BE020` (t), `002BE050` (t), `002BE090` (t), `002BE1A0` (t), `002BE230` (t), `002BE270` (t) |
| `_A0D0` | `0x990` | `003F80D0`, `003F80E0` (t) |

**`_8FA0`'s size corrected `0x1130` → `0x1110`, 2026-09-21 (OPUS), closing `CON-124`.** The row carried `0x1130` while `_types/types.tsv` carried `0x1110`, and the construction site settles it from the image: `002BE450` is 52 bytes and does `mov edx, 0x1110` at `002BE460` immediately before `call 00245000`, the placement allocator, whose result it hands to the constructor `00246AC0`. **The 0x20 difference was the gap to the next sibling, not part of the object** — which is exactly the error a table of adjacent children invites, because subtracting one base from the next measures the stride and not the extent.

`_8FA0` is not ownerless; it is the **most heavily owned child of the seven**, with a contiguous
`002BDAE0`–`002BE270` family. `0016D6A0` (`_guard_check_icall`) is excluded throughout — that is
the CFG check on an indirect call, not a handler.

**This table is the scan's, not a hand-match's, and the difference cost one wrong row.** A first
pass matched the thunk *shape* textually — slot load, `add rcx, <offset>`, `jmp` — and reported
`_7FB0 -> 002970C0`. That is wrong. `0028E8D0` reads:

```
0028E8DE  mov  rcx, qword ptr [rip -> 0209BE80]
0028E8E5  mov  edx, 6
0028E8EA  add  rcx, 0x7FB0
0028E8F1  call 00296670          <- the owner call, rcx = _7FB0, edx = 6
0028E8FA  jmp  002970C0          <- rcx is DEAD here: volatile, clobbered by the call
```

The tail jump is real and `002970C0` is not this child's handler; `rcx` stopped being `_7FB0` at
`0028E8F1`. Pattern-matching three instruction kinds without modelling the calling convention
finds thunks that are not thunks, which is the same error class as reading an unrolled copy's
displacements as fields — a shape that looks right to a reader who is not tracking what the ABI
says about the registers in between.

**Two more things the thunk scan shows that the call scan could not.**

- **`0028F0C0` hands `singleton+0x5980` — that is `_57E0+0x1A0`, the second widget slot — to
  `00244F00`.** So that slot has a consumer outside the `0x0020` handler as well as the builder
  pair documented above.
- **Two owned regions lie outside every declared *child*, and the store already names both.**
  `+0xAA60` is passed to `00861EC0` (`memset`) by `0028E880`; the store has `zeroedBlockAA60`,
  196 bytes, which is exactly what a memset target should look like. `+0xAB30` has four owners
  (`002767C0`, `0031C200`, `00296490`, `00296960`) and the store has `ptrAB30`, a `void*`.
  `_A0D0` ends at `0xA0D0 + 0x990 = 0xAA60` exactly, so `+0xAA60` begins where the last declared
  child stops. They are **not** `ManagerSub*` children, which is why the child scan missed them —
  they are ordinary declared rows, and the fifteen groups therefore do not cover the singleton
  because it holds more than its seven children, not because any child is ownerless.

#### `ptrAB30` is an 8-byte pointer row on a sub-object at least `0x714` bytes long

The store's own note for that row is careful and was right about what it had: *"the callee that
receives this address, `00273A20`, is NINE BYTES LONG and its whole body is `xor eax,eax;
cmp qword ptr [rcx], rax; setne al; ret` — so what is established here is a QWORD, read as a
pointer and tested for null, not a sub-object of unknown size."* That refusal was correct on one
callee. **There are five**, and the other four reach much further into the same address:

| owner | reaches |
|---|---|
| `002767C0` | `+0x0`, `+0x18` |
| `00296490` | `+0xC0`, and writes `+0x710` — [`002964BA`](../_index/ADDRESS-INDEX.md) `mov dword ptr [rbx+0x710], 1` |
| `00296960` | `+0x180`, `+0x414`, `+0x648`, and tests `+0x710` — [`0029696A`](../_index/ADDRESS-INDEX.md) `cmp dword ptr [rcx+0x710], 0` |
| `0031C200` | nothing off its first argument |

So `singleton+0xAB30` is the base of an object of **at least `0x714` bytes** (`+0x710` read as a
dword), ending no earlier than `0xAB30 + 0x714 = 0xB244`.

**That accounts for an 1,800-byte gap, and it checks against a row nobody had connected to it.**
`unobservedSpanAB38` (1,800 B, `0xAB38`–`0xB23F`) is this object's interior, and `dwordB240` — a
separately declared `uint32` at `0xB240` — is its **`+0x710`**: the very field `00296490` sets to 1
and `00296960` compares against 0. Two store rows written independently turn out to be one
structure, and the arithmetic is what says so.

**This is extent, not meaning.** Nothing here says what the object is for, and the 1,800 bytes stay
unexplained; what changes is that they are the inside of something with five named owners rather
than a hole after a pointer. The store rows are not edited here — `_types/fields.tsv` is parked
behind `OPUS-CONTRA-SWE2-CONTRACT-STEERINGRECORD-NAMES-PUBLISHED-ONLY-IN-PROSE` — so `ptrAB30`
still reads as a bare `void*` until that clears.

> **REFINED 2026-09-28 (OPUS, [`battle_menu_child_base.py`](../_index/candidates/battle-menu-child-base-opus/battle_menu_child_base.py) X): two
> different widgets use this storage.** `00290707` builds a 0x720-byte widget at `singleton + 0xAB30` (`00296940`,
> handler `002985D0`) while `+0x10F68` bit `0x2000` is clear, then sets the bit; `00290CF0` builds the 0x61F0 battle
> menu (`00276650`) in the same storage in the other mode. `00296490`, `00296960` and `002906D0` all run behind bit
> `0x2000`, so the `+0x710` dword (`dwordB240`) is the 0x720 widget's field - `Widget0720At0209BE80_AB30 +0x710` in the
> store. Inside the 0x61F0 battle menu the same bytes are the second record's text-draw state of a
> `BattleMenuChildWidget1620`. The paragraph above stands for the object that owns `+0x710`; the extent argument below
> (0x61F0) stands for the battle-menu variant.

#### `_8FA0`'s traffic is all in its last 256 bytes

Censused from the fourteen thunk owners plus five bodies the closure reaches, **nineteen member
bodies** touch **sixteen offsets** across ~~4,400~~ 4,368 bytes *(corrected 2026-10-02, OPUS: `002BE450+0x10` `mov edx, 0x1110`)* — and every one of them lies in
`+0x1030`–`+0x10FA`, the tail. Fourteen carry a single width; the two that do not are left
undeclared:

- widest traffic at `+0x1080` (17 accesses in 4 functions), `+0x1078` and `+0x1058` (11 each);
  qwords throughout, with `+0x103C`/`+0x103E`/`+0x10F8` as words and `+0x1040` a dword.
- **`+0x10D0` reads as both 8 and 16 bytes**, and `+0x10E0` is a plain `xmmword`
  ([`002BE16F`](../_index/ADDRESS-INDEX.md)) with `+0x10F0` a qword — the shape of a 16-byte vector
  written whole and read in halves. Plausible, so not declared.
- **`+0x10FA` reads as both 1 and 2 bytes** — the flag-word-with-byte-sub-reads signature again.

Two sub-objects are handed on: `+0xAC0` to `002BE300`/`002BEA40`, and `+0x109C` to `002BF3D0`.

**So the first 4,144 bytes of this child are untouched by its own owner family.** That is a
measurement, not a verdict — the same closure said `_5380` and `_8FA0` had no owners at all until
tail jumps were followed, and a region reached some third way would look exactly like this. It
does say where to read next, and it is the opposite end of the object from where one would start.

### All seven children censused: 103 offsets over ~~43,456~~ 43,424 bytes, and they sit in bands *(corrected 2026-10-02, OPUS)*

With the owner table settled, each child was censused from **its own owners** and their closure.
The result is the same shape seven times:

| child | size | members | offsets | they span |
|---|---|---|---|---|
| `_00A0` | 21,216 | 5 | 9 | `+0x0`–`+0xC` and `+0x52A0`–`+0x52C6` — both extremes only |
| `_5380` | 1,120 | 14 | 6 | `+0x0`–`+0x430` |
| `_57E0` | 9,920 | 18 | 32 | `+0x0`–`+0x26AE` |
| `_7EA0` | 272 | 10 | 13 | `+0x0`–`+0x76` |
| `_7FB0` | 4,080 | 18 | 27 | `+0x0`–`+0x104` — the first 6 % holds all of them |
| `_8FA0` | ~~4,400~~ 4,368 *(corrected 2026-10-02, OPUS: `0x1110`, `002BE450+0x10`)* | 16 | 14 | `+0x1030`–`+0x10FA` — the last 6 % holds all of them |
| `_A0D0` | 2,448 | 2 | 2 | `+0x960`, `+0x984` |

*(The `_57E0` section above reports ten offsets; that was from three of its ten owners, before the
owner table was corrected. With all ten it is 32. The two width conflicts named there stand.)*

**These are not field records with most fields undiscovered.** In every case the owners address a
narrow band and never the bulk, and `_7EA0` — the only one small enough for a band to be the whole
object — is the only one densely covered, 13 offsets across 272 bytes. The bulk is not addressed
**from the object base at all**.

The mechanism is visible in the band itself: `_00A0+0x52B8` is read five times and then used as a
base — [`003F8DD4`](../_index/ADDRESS-INDEX.md) `mov r8, qword ptr [rdi+0x52B8]` followed by
`mov rcx,[r8+0x20]` and `mov r8,[r8+0x30]` — so it is a **pointer to another structure**, and the
work happens there. `_5380`'s `+0x420`/`+0x428`/`+0x430` triple and `_57E0`'s `+0x2490` list head
are the same shape. A `memset` target at `_00A0+0x4020` says at least one interior span is a
buffer cleared wholesale rather than a set of fields.

**What this changes about the 99 %.** It is not a measure of how much reading is left in these
types; it is a measure of the wrong question. The interiors are containers and buffers reached
through a handful of pointers, so a displacement census of the child can never explain them however
long it runs — the next move is to follow those pointers and type what they land on, not to look
harder at the child. That is a bounded statement about what the owners do, not proof that no other
code addresses the interiors directly; a route this closure cannot see would look identical, which
is exactly the mistake corrected two sections above.

### The parent's own 25,767 unknown bytes are one span, and it is untouched

Running the same closure against `ManagerSingleton0209BE80`'s **24 declared UNKNOWN spans** — not
its children's — splits them cleanly. Ten spans are touched; fourteen are not, and the sizes are
lopsided:

- **`unobservedSpanB244` is 23,224 bytes — 90 % of this type's unknown bytes, and about 36 % of
  every unknown byte in the database** — and **nothing reaches it**. See below; it is the largest
  single result here.
- `unobservedSpanAB38` (1,800 B) is also untouched, which is consistent rather than surprising:
  it is the `+0xAB30` object's interior, reached *through* that pointer and never by displacement
  from the singleton.
- Nine small spans of 1–12 bytes each are single declared fields that the closure does reach
  (`dwordB240`, `word10F60`, `flag10FA3`, `dword10FA8` and so on) — those are UNKNOWN in the
  *confidence* column, not unreached.

### `unobservedSpan0000` is a 128-byte gap that is not unobserved

The one genuinely mis-declared span is the singleton's own header. `+0x0`–`+0x7F` is carried as
`unobservedSpan0000` and the closure touches ten offsets in it. Nine carry a single width and are
listed here; the tenth, `+0x00`, is held back for the reason given under the table:

| offset | width | sites / fns | first instruction |
|---|---|---|---|
| `+0x08` | 8 | 1 / 1 | [`002483CA`](../_index/ADDRESS-INDEX.md) `mov rbx, qword ptr [rdi+8]` |
| `+0x10` | 8 | 1 / 1 | [`00248308`](../_index/ADDRESS-INDEX.md) |
| `+0x18` | 8 | 3 / 3 | [`002448E0`](../_index/ADDRESS-INDEX.md) |
| `+0x20` | 8 | 1 / 1 | [`00248315`](../_index/ADDRESS-INDEX.md) |
| `+0x28` | 8 | 1 / 1 | [`00248311`](../_index/ADDRESS-INDEX.md) |
| `+0x40` | 4 | 4 / 2 | [`00244865`](../_index/ADDRESS-INDEX.md) `mov dword ptr [rcx+0x40], 0xFFFFFFEF` |
| `+0x50` | 4 | 3 / 1 | [`00248334`](../_index/ADDRESS-INDEX.md) |
| `+0x60` | 8 | 4 / 1 | [`0024833E`](../_index/ADDRESS-INDEX.md) `mov qword ptr [rdi+0x60], 0` |
| `+0x7C` | 4 | 1 / 1 | [`002483BE`](../_index/ADDRESS-INDEX.md) `mov dword ptr [rdi+0x7C], 0xFFFFFFF0` |

**`+0x00` is excluded although it has the most traffic** — seven accesses in five functions, at
widths 2, 4 **and** 8. A zero displacement is also what a scan produces when it has tainted the
wrong base, so of all offsets it is the one least safe to declare from a conflict. `+0x40` and
`+0x7C` being written `0xFFFFFFEF` and `0xFFFFFFF0` looks like a sentinel pair and is not claimed
as one.

That is 60 of the span's 128 bytes declarable from instruction widths — five qwords at
`+0x08`–`+0x28`, plus `+0x40`, `+0x50`, `+0x60` and `+0x7C` — leaving 68 in five gaps, including
the eight bytes at `+0x00` that the conflict puts out of reach. The store edit is **held as
a prepared patch rather than applied**, because `_types/fields.tsv` is being written by
SWE2-CONTRACT and an unstaged edit parked in a shared file is not safe — see the note added to
`publish_paths.sh`.

### 23,224 bytes in the middle of this object are reached by nothing, on four routes

`+0xB244` through `+0x10CFB` is **the largest single block of unknown bytes in the database** —
about **36 % of every unknown byte in the store**, in one contiguous run inside one heap object.
Four independent routes were measured across the 136 bodies that load the slot and the 143-body
closure they reach, and every one is zero:

| route | result |
|---|---|
| direct `[singleton + disp]` | **0** offsets in the span |
| handoff — `lea` into an argument register at a `call` **or a tail `jmp`** | **0** |
| escaping interior pointer — a `singleton+d` value stored to memory | **0**; the only escapes anywhere are at `+0x00000` (`002448FE`, `0028EDA0`), the object pointer itself, so nothing can route back in through a saved interior address |
| indexed `[singleton + reg*scale + disp]` | **0** real ones. The single hit an image-wide scan returns is `0028F2B6 nop word ptr [rax + rax]` — the multi-byte NOP encoding, i.e. padding |

**The object's size is not in doubt, so this is a hole and not a mis-measured end.** `0028F8CA`
loads `ecx = 0x10FD0` and `0028F8CF` calls the tagged allocator wrapper `00271420`, with the result
published to `0209BE80` at `0028F8D4` under the null guard at `0028F8C5`. **And the span is bounded
on both sides by traffic**: below it the `+0xAB30` object runs to `+0xB244`, and the very next
touched offset above it is `+0x10CFC`, followed by the dense HUD block at `+0x10EF0`–`+0x10FC8`.
The hole is in the middle of a live object, not off its end.

~~**The `+0xAB30` object does not extend into it.** That was the obvious reading — the span begins
exactly at `0xAB30 + 0x714` — and it is now measured and **false**: censused as an object in its
own right from its five owners with a deliberately generous `0x6000` bound, its accesses are
`+0x0`, `+0x18`, `+0x414`, `+0x710` and nothing beyond.~~

> **RETRACTED 2026-09-19 (OPUS) — it does extend into it, and it is accessed beyond `+0x710`.**
> `00290CF0` holds the singleton in `rbx` (it reads `[rcx+0x10F68]`, inside the declared
> `0x10FD0`), does `lea rcx, [rbx + 0xab30]` at `00290D96` and passes that interior pointer to
> `00276650` at `00290DC0`. The callee keeps it in `rsi` (`00276685`) and then does
> `mov edx, 0x61f0 ; mov rcx, rsi ; call 00245000` at `002766D8`–`002766E0` — **a 0x61F0-byte
> clear of the handed-out object** — followed immediately by
> `and dword ptr [rsi + 0x61cc], 0xfffffeff` at `002766E5`, **an access at `+0x61CC`**.
>
> `0xAB30 + 0x61F0 = 0x10D20`, so the object spans `+0xAB30`–`+0x10D1F` and the hole at
> `+0xB244` is **inside it**. The `+0x61CC` access is singleton `+0x10CFC`, which the type store
> independently declares as `ManagerSub0209BE80_AB30 +0x61CC flags61CC`, *"RE-BASED from
> +0x10CFC"*.
>
> **Why the census said otherwise, and the lesson is the instrument again:** it bounded the
> object at `0x6000`, and `0x61F0 > 0x6000`. `+0x61CC` fell outside the window by `0x1CC` bytes.
> **A bound that looks generous but falls short of the real extent reports its own truncation as
> an absence** — the same shape as the `movs`-substring filter recorded in `ac8f068f3`.
>
> **This closes the third gap of `ac8f068f3` rather than leaving it open**, and corrects its
> example. That commit named `[rdi + 0x10FC0]` as *"exactly such a hand-out"*; its facts are
> right — `00291750` allocates `0x8030` at `0029176F` and stores it at `00291779` — but a pointer
> to a **separately allocated** block cannot reach a hole **inside** the singleton, so it is not
> an instance of the gap at all. The real interior hand-out is `+0xAB30` itself, and the bulk
> write through it reaches the hole. **`4d05cc7a0`'s bound — "the constructor's memset remains
> the ONLY bulk write reaching the hole" — is wrong by one.**
>
> **What this does NOT overturn:** the read-absence. Every route in the table above looked for
> something that *reads* `+0xB244`, and a `memset` is a write. The hole is still reached by no
> read on those four routes; what has changed is that it is inside a live object and is written
> by that object's own clear, so "the constructor's memset is the only bulk write" and "the
> `+0xAB30` object stops short of it" are both retired.

(The `+0xAB30` object does hold three embedded sub-objects, handed off at `+0xC0` to `00244F00`
— the same builder that takes `_57E0+0x1A0` — at `+0x180` to `002475D0`, and at `+0x648` to
`0029B550`.)

**For reconstruction:** the allocation is a fixed `0x10FD0` and must stay that size, because every
later field's offset depends on it; but no behaviour this project can observe reads those 23,224
bytes. That is the same shape as `BattleUnit +0x298`, twenty-three times larger.

**The limit, stated as it was for `BattleUnit`:** this is four static routes, not a proof of
absence. A reader that computes the address in a form the taint does not model, or one that only
exists at run time, would look exactly like this. What has changed is that the largest unknown
block in the database is now a *specific bounded question* — "does anything read `+0xB244`?" — with
four routes already closed, rather than 23 kB of undifferentiated silence.

**The lesson is about the instrument, not the corpus.** A scan that reports handoffs at calls will
report *nothing* for a subsystem wired with tail-jump thunks, and nothing reads exactly like
absence. The guard is to ask what shape the code uses before concluding from a silence — here
`0028E220` is nineteen bytes and says so plainly.

`member_reach_scan.py` follows tail jumps now, so the gap is closed rather than only documented.
Two things that came out of closing it are worth recording, because both are about how easily this
kind of fix does damage:

- **A self-test control was asserting the bug.** It read *"`_7EA0` is NOT handed — it is a tail
  jmp, correctly unseen"*, so a green run confirmed the blind spot instead of catching it. It now
  asserts that `0028C870` **is** seen. A control written to match current behaviour rather than
  intended behaviour is worse than no control, because it makes the gap look deliberate.
- **The first version of the fix invented a field, in the worst possible place.** Following thunks
  needs `add rcx, <offset>` treated as address arithmetic — and taken generally, that carries the
  taint through a register the compiler has reused as a scratch index. In
  `BattleUnit_RebuildPerceptionCandidateCache`, `00324D9C add rax, 0x375` followed by
  `00324DA2 lea rax,[rdi + rax*4]` is an ELEMENT INDEX, and the naive rule reported an access at
  `unit+0x375` — inside the 1,016-byte span this same tool had been used to establish as unread.
  One line would have manufactured the counter-example to a published finding. The rule now marks
  such a value **argument-only**: it may be reported as a call argument and can never count as a
  field access. Re-measured after the fix, that span is empty again.

### First interior view of `_57E0`, the largest child (2026-09-18, OPUS)

Following the reading order above rather than guessing: seeded from the three handlers now known to
take it (`003F9F40`, `003FA790`, `003FA4E0`) and closed over `this`-in-`rcx` handoffs, which adds
`00229E40`, `00273A20`, `003F9E50` and `003FAAF0` for **seven member bodies**. Across 9,920 bytes
they touch **ten offsets**, every width read from its own instruction:

| offset | width | sites | first instruction |
|---|---|---|---|
| `+0x0000` | 8 | 1 | [`00273A22`](../_index/ADDRESS-INDEX.md) `cmp qword ptr [rcx], rax` |
| `+0x0060` | 8 | 2 | [`003FA11C`](../_index/ADDRESS-INDEX.md) `mov rax, qword ptr [rbx+0x60]` |
| `+0x00C4` | **1 and 4** | 6 | [`003F9E8E`](../_index/ADDRESS-INDEX.md) `mov eax, dword ptr [rbx+0xC4]` |
| `+0x00C8` | 4 | 1 | [`003FA12C`](../_index/ADDRESS-INDEX.md) `mov eax, dword ptr [rbx+0xC8]` |
| `+0x2490` | 8 | 4 | `003FA4E0` `mov r8, qword ptr [rcx+0x2490]` — the list head |
| `+0x2498` | 2 | 2 | [`003FA004`](../_index/ADDRESS-INDEX.md) `movzx eax, word ptr [rbx+0x2498]` |
| `+0x249A` | 2 | 2 | [`003FA010`](../_index/ADDRESS-INDEX.md) `cmp ax, word ptr [rbx+0x249A]` |
| `+0x249C` | **1 and 4** | 8 | [`003F9F51`](../_index/ADDRESS-INDEX.md) `test byte ptr [rcx+0x249C], 4` |
| `+0x24A0` | 2 | 3 | [`003F9F5D`](../_index/ADDRESS-INDEX.md) `inc word ptr [rcx+0x24A0]` |
| `+0x24A2` | 2 | 1 | [`003FA0AD`](../_index/ADDRESS-INDEX.md) `movsx ecx, word ptr [rbx+0x24A2]` |

**Two offsets show two widths and are deliberately left unresolved.** `+0xC4` and `+0x249C` are
each read both as a byte and as a dword. A census cannot tell a coarse store over sub-fields from
a union keyed elsewhere — the `BattleUnit` layout work withheld seventeen displacements for exactly
this signature, and four of them later resolved as 32-bit flag words with byte-granular sub-reads.
That is the likely shape here too, and *likely* is not a width, so neither is declared.

**Two embedded sub-objects, not fields.** `+0xD0` and `+0x1A0` are handed by `lea` to `00245000`
and `00246AC0` — the widget build pair §3 names for the `0x0020` group. They are widget slots
embedded in the child, and their extents are set by those builders rather than by anything here.

**Ten offsets and two sub-objects out of 9,920 bytes leaves this type essentially unknown**, and
the store still says so. What has changed is that it is now approachable: the owners are named,
the control cluster at `+0x2490`–`+0x24A2` is visibly one structure, and the next question is a
specific one — what `00245000`/`00246AC0` make of `+0xD0` and `+0x1A0`.

#### The two slots are built in place and then registered, and that is a lifetime fact

Both are passed in **`rcx`** — they are genuinely `this` for the pair, not some later argument:
`003F9FA4`/`003F9FB0` for `+0xD0`, and `003F9FCC`/`003F9FEC`/`003F9FF8` for `+0x1A0`, which also
goes through the free check `00273A20` first. Identical sequence for both, so they are the same
kind of slot.

- **`00245000` builds in place.** It reaches `+0xB8` into its first argument
  ([`00246700`](../_index/ADDRESS-INDEX.md) `mov dword ptr [rdi+0xB8], 0x3F800000` — `1.0f` — and
  [`0024675C`](../_index/ADDRESS-INDEX.md) `mov dword ptr [rdi+0xB4], 1`), so **the slot is at
  least `0xBC` bytes**. That is a floor from what this function touches, not a size.
- **`00246AC0` registers it, and is fifteen bytes read end to end.** `mov rdx, rcx` — the widget
  becomes **argument two** — `mov rcx, qword ptr [rip -> 0208EA28]` — a manager pointer becomes
  argument one — then `jmp 00246AD0`. So the widget is not the subject of the call it ends in.
- **`00246AD0` (321 B) is the registrar.** It null-guards `rdx`, clears bit 6 of the widget's
  `+0x40`, branches on `[widget+0x10]` and sets bit 1 of `+0x40`. So a widget carries a flags dword
  at `+0x40` and a pointer at `+0x10`, consistent with the `0xBC` floor.

**The array reading is available and is not taken.** The two slots are `0xD0` apart, `0xBC ≤ 0xD0`,
and the sequence is identical — which is exactly what an array of `0xD0`-byte elements looks like.
Against it: **no indexed access into this child exists anywhere in the member set** (zero, measured),
and no third slot is observed at `+0x270`. Two elements and a plausible stride are not an array;
the corpus takes strides from indexed accesses, and there is none here. Recorded as two embedded
slots of unknown extent, `≥ 0xBC` each.

## `_57E0`'s 8,728-byte span is very probably 42 more of a record the store already declares twice — and that is a hypothesis, not a declaration (2026-09-19, OPUS)

*`unobservedSpan0278` is **8,728 bytes, 78 % of `ManagerSub0209BE80_57E0`** and the largest remaining
unknown span in the store after the `+0xB244` hole. This narrows it and deliberately stops short of
declaring it.*

### The store already contains two complete instances, back to back

Read out of `fields.tsv`, the rows immediately before the span are **two byte-identical records**:

| record | offsets | fields | total |
|---|---|---|---|
| **A** | `0x0D0`–`0x19F` | `ptr00D0` (8) · `unobservedSpan00D8` (186) · `count5972` (2) · `unobservedSpan0194` (12) | **208 = `0xD0`** |
| **B** | `0x1A0`–`0x26F` | `ptr01A0` (8) · `unobservedSpan01A8` (186) · `count5A42` (2) · `unobservedSpan0264` (12) | **208 = `0xD0`** |

The field-size sequence is identical, both total exactly `0xD0`, and they abut. **The third record
would begin at `0x270`, and `subAddr0270` — a pointer, like `ptr00D0` and `ptr01A0` — is declared
there.** The span then runs `0x278`–`0x2490`, and `0x2490` is exactly where the next declared row,
`ptr7C70`, begins.

**The arithmetic closes on the boundary:** `(0x2490 − 0xD0) / 0xD0` = **44** records, and
`0xD0 + 44 × 0xD0 = 0x2490` to the byte. Two are declared, the third's first field is named, and the
span holds the remaining **42**.

*(Stated because I got it wrong once on the way: it is 44 records, not 45 — `0xD0 + 45 × 0xD0` is
`0x2560`, past the end of a `0x26C0` object. The off-by-one was caught by printing the comparison
instead of asserting it.)*

### Why no scan has seen inside it, and this part is the general lesson

**Nothing in the closure reaches these bytes, and a displacement-keyed scan structurally cannot.** An
array reached as `base + index × 0xD0` produces no literal `[reg + 0x3XX]` operand for any element
past the first, so every instrument in this kit that keys on displacements is blind to 42 of the 44
records by construction. This corpus has recorded exactly that failure before — `AU-5`, where *"no
literal `[reg+0x64]` write exists — all three go through `[base + index × 4]`, which is why
displacement-keyed scans found nothing."* **A span being "unobserved" is a fact about the
instruments as much as about the engine.**

### What is missing, and why the row is not being changed

**No code has been tied to this object with a `0xD0` stride.** Image-wide, exactly **three** bodies
multiply an index by `0xD0` — `0028D030`, `003F26F0`, `005C4F30`. Both of the first two are real
`0xD0`-stride array walks (`003F26F0` even steps `add rbx, 0xD0` in a loop), but **each indexes its
own `this`, and I could not establish that `this` is `_57E0 + 0xD0`** for either. `0028D030` reaches
`rdi+0x4E0`, `rdi+0xAB0` and `rdi+0xBE0` and runs *two* `0xD0`-stride arrays, at `rdi+0` and
`rdi+0x5D0`, which is a shape the `_57E0` layout does not obviously match.

So the record structure rests on **the store's own two instances and an exact boundary**, and not on
a single indexing site. That is good evidence and it is not proof, so:

- **NOT DECLARED.** The span stays `unobservedSpan0278`. Declaring 42 records here would be
  consuming an unexplained gap to make a layout look complete, which is the one thing this database
  forbids itself — and the gap is 8,728 bytes, so getting it wrong would be the largest single act of
  invention in the store.
- **NOT CLAIMED:** what a record is, what `ptrXXX` points to, what `countXXXX` counts, and whether
  the array is 44 long or merely occupies room for 44.


### All three `0xD0` sites are now ruled out, and that weakens the stride argument

Followed to their callers rather than left as candidates. `0028D030` and `003F26F0` have **one caller
each**, `0028C590` and `0028C620`, and both callers operate on the **same type**: `0028C590` walks a
linked list (`rbx = [rbx + 0xD70]`, looping while non-null) and `0028C620` reads `+0xD48`, `+0xD4A`,
`+0xD4B` and `+0xD50` off the same `this`. So both `0xD0`-stride walkers are methods on a
**list-node type that carries two `0xD0`-stride arrays of its own**, at `node+0` and `node+0x5D0`,
and reaches `+0xBE0`. The third site, `005C4F30`, has **no callers at all**.

**None of them is `_57E0`**, and the consequence runs against my own hypothesis: **`0xD0`-stride
arrays demonstrably exist elsewhere in this engine**, so "the stride is `0xD0`" is a much weaker
coincidence than it looked when three sites were merely unexamined. What survives is **only** the
store's own evidence — two byte-identical 208-byte records, the third's first field, and the span
ending to the byte on a record boundary. That is why the span stays undeclared: the arithmetic is
exact and the corroboration is entirely internal to the store, with no code-side witness at all.


### Swept the whole store: this is the only span of its kind

The hand-reading above generalises to a rule, so it was made one — `check_repeated_records.py` walks
every type's rows looking for **two adjacent groups with an identical field-size sequence**, then
asks whether an unknown span abuts the repeat and whether its length is a whole multiple of the
record. Across **275 types it returns exactly one exact hit: this one.**

**Two false-positive classes had to be removed first, and both are worth knowing.** *(1)* **A uniform
run is not a record.** Six consecutive dwords trivially "repeat" as two three-dword groups, and
`CharacterRenderSystemTail` produced precisely that — `0x4C`/`0x50`/`0x54` are three plain `uint32`s
and the first draft read them as a 12-byte record continuing into a 192-byte span. What makes this
type's repeat evidence is that its sequence is **heterogeneous** — `8/186/2/12` is a signature,
`4/4/4` is not. *(2)* **"Closes exactly" is a weak filter on small spans.** A 192-byte span divides
exactly by 8, 12, 16, 24, 32, 48, 64 and 96, so two competing readings of the same span can both
pass; the tool now prints how many rival record sizes also divide the total, and this span's 10
rivals are a reminder that the exact close is corroboration and **not** the evidence.

**The result is threshold-stable, which the first version was not.** Before uniform runs were
rejected, loosening the thresholds took the exact-hit count from 1 to **35** — the null was an
artifact of where the cutoffs sat. With the rejection in place the same loosening yields three
candidates and still **one** exact hit. So the claim is bounded and it holds: **no other span in the
store continues a heterogeneous record the store has already declared twice.** This is a single case,
not a widespread documentation defect.


### The store had already recorded a reason to doubt, and my section omitted it

**Correcting my own section above, same day.** It argued the case on *"two byte-identical 208-byte
records"* and left out a disconfirming measurement that was already written down in the store, in a
row I wrote the day before. `count5A42`'s own text says: *"A repeat at stride `0xD0` is **VISIBLE BUT
NOT ESTABLISHED**: the flag-to-sub-object distances differ (`0xC` then `0xE`)."*

Re-derived, in `_57E0`-relative terms:

| | guard flag | object it guards | distance |
|---|---|---|---|
| record A | `+0xC4` (`flag58A4`) | `+0xD0` (`ptr00D0`) | **`0xC`** |
| record B | `+0x192` (`count5972`) | `+0x1A0` (`ptr01A0`) | **`0xE`** |

So **the pointers are `0xD0` apart and the guards are `0xCE` apart** — off by two. The two records do
not sit on one lattice.

**The evidence is mixed, and both halves are real.** For: the pointers step exactly `0xD0`; both
records place their count at the same record-relative slot `+0xC2`; the span closes to the byte on the
44th boundary. Against: the guards do not step `0xD0`, and the layouts are therefore not congruent.

**`check_repeated_records.py` cannot see this, and that is a limit worth stating.** It compares
declared field *sizes* — `8/186/2/12` against `8/186/2/12` — so two records whose guards sit at
different relative offsets look identical to it. **A sweep that compares tilings is not comparing
structures**, and the tiling is partly a record of how the documentation grew rather than of how the
object is laid out. The instrument's one exact hit is therefore weaker evidence than its output
suggests, and its docstring's *"a hit is a hypothesis"* is doing more work than I gave it credit for.

**Net effect on `U-7`: it is weaker, not stronger, than the section above claimed.** The stride
argument was already spent when all three `imul`-by-`0xD0` sites were ruled out; this removes part of
the store-internal argument too. What survives is the pointer stride, the shared count slot and the
exact boundary — three coincidences with no code-side witness and one measured inconsistency against
them.


### ANSWERED, NEGATIVELY — and it was answered a day before I asked it

**The array reading is refused, and `ede00af49` refused it on 2026-09-18.** That commit is titled
*"The two slots inside `_57E0` are built in place and then registered, **and the array reading is
refused**"*, and it reads `+0xD0` and `+0x1A0` into `00245000` (builds in place) and `00246AC0`
(registers with the manager at `0208EA28`), concluding *"identical sequence for both, so they are the
same kind of slot."* **A pair of slots, already established.** I proposed a 44-record array over the
same offsets the following day without reading the object's own history.

**The decisive witness, and it is neither stride nor tiling.** `003F9F40` — the function that
established both records — calls the null-predicate `00273A20` **exactly twice**, and the two calls
are coded *separately*:

```
003F9F7D  add  rcx, 0xd0          ; then call 00273A20 at 003F9F84
003F9FC5  lea  rcx, [rbx + 0x1a0] ; then call 00273A20 at 003F9FCC
```

**Two hand-written accesses, not a loop.** Forty-four records would be walked; two slots get two
instructions. There is no third call at `+0x270`, and the sibling bodies `003FA790` and `003FA4E0`
make none at all.

**So `unobservedSpan0278` is not 42 more of anything.** The evidence now runs one way: the array
reading was refused on the object's own reading order, the guards step `0xCE` rather than `0xD0`, all
three `imul`-by-`0xD0` sites in the image belong to a different type, and the only code that touches
the pair handles exactly two. **The 8,728 bytes stay unobserved, which is what they were.**

**What survives of the observation:** `+0xD0` and `+0x1A0` are two slots of one kind, `0xD0` apart,
each null-guarded and each carrying a count at record-relative `+0xC2`. That the pair's spacing equals
a number that divides the following span is a **coincidence of arithmetic**, and this section spent
two rounds treating it as a lead.

**The process failure is the part worth keeping.** The span was attractive precisely because it was
big — 8,728 bytes is the largest remaining prize in the store — and a tidy division made a
hypothesis out of a coincidence. What should have come first is the cheapest question available:
*what has this object already been read for?* The answer was one commit away and said **refused**.

### The open question this leaves

**What indexes `ManagerSub0209BE80_57E0 + 0xD0` with stride `0xD0`?** One such site converts this
from a strong hypothesis into a declared array and retires 8,728 bytes of unknown in a single step —
the largest such step available in the store. The three `imul`-by-`0xD0` bodies are the place to
start, and what they need is a base identification, not more disassembly.

## The 23,224-byte hole survives a route with a different blind spot (2026-09-19, OPUS)

*The hole at `ManagerSingleton0209BE80 +0xB244..+0x10CFB` was established as reached zero times on
**four routes**, and all four are **taint-first**: they start from the singleton and propagate a
tainted base through the bodies that receive it. That is exactly the method `AU-5` records as blind
to indexed access, and it is the method that nearly sold me a 44-record array in `_57E0`. **Four
routes that share a blind spot are one route.** This is a fifth with a different one.*

### Displacement-first, not taint-first

The question is turned around: instead of asking *what does the singleton reach*, ask **what in the
image carries a memory displacement that falls inside the hole at all** — whatever its base, tainted
or not — and then ask whether any of those bodies could be holding the singleton.

Across all 38,161 bodies, **32 carry a memory operand with a non-`rip` base and a displacement in
`0xB244..0x10CFB`**. Of those:

- **0 load the singleton slot `0209BE80`** — against **136** bodies image-wide that do.
- **2 are call-reachable from a loader** (`002B9D30`, `00322C50 BattleEncodedId_IsValidForClass`), and
  reachability at that depth spans 1,455 bodies, so it means very little on its own. Reading their
  actual bases settles it: `002B9D30`'s rip-relative globals are `0209E5F0`, `01F44830`, `02B457D8`
  and others — **`0209BE80` is not among them** — and `00322C50`'s are all `02EBF0xx`, the
  battle-state block. **Neither is a singleton access.**

**So the hole holds on a route that does not depend on taint propagation at all.** An indexed access
this method would see, because it keys on the displacement rather than on the base, and there is
nothing to see.

### Two instrument bugs on the way, both caught by an implausible number

**Neither figure above is the one the first run produced.**

1. **`rip`-relative operands were counted as object fields.** `lea rax, [rip + 0xce0e]` has a
   displacement in the hole range and nothing to do with any object, so the population came out at
   **91** instead of 32 — a third of it noise from `.data` references.
2. **`base == 0` was used to detect `rip`-relative**, which is wrong: Capstone sets the base to
   `RIP`. That filter therefore excluded exactly what it was meant to find, and reported **0 bodies
   loading `0209BE80`** — for a singleton with **136** loaders and a documented binder. A zero that
   large for an object this well known is not a finding, and it was not treated as one.

Both were caught the same way every instrument defect in this session was caught: **a number too
clean to believe, checked against something already known.**

### What this does and does not add

- **Adds:** the hole's unreachedness no longer rests only on methods that share the indexed-access
  blind spot. **NOT CLAIMED:** that the hole is unwritten. Bulk operations reach regions no
  displacement names — `BattleUnit +0x298` was *"unreached on six routes"* and is nonetheless cleared
  by a `0x610`-byte `memset`, published earlier today. **Unread is still not untouched**, and no
  equivalent sweep for bulk writes into this hole has been run.

## The hole is never read and is definitely written: the constructor zeroes all 69,584 bytes (2026-09-19, OPUS)

*The bulk-write sweep this page's previous section said had not been run. It has now, and it changes
what the hole's "unreached" means.*

**`00291750`, the constructor `types.tsv` already names, opens by clearing the entire object:**

```
0029175A  xor  edx, edx            ; value 0
0029175C  mov  r8d, 0x10FD0        ; length 69,584 - the whole allocation
00291762  mov  rdi, rcx            ; keep `this`
00291765  call 00861EC0            ; memset(this, 0, 0x10FD0)
```

`rcx` is untouched between entry and the call, so the destination is `this`, and `0x10FD0` is the
same immediate the allocator takes at `0028F8CA`. **The hole at `+0xB244`–`+0x10CFB` lies wholly
inside it.** What follows in the same body is the child construction this page already documents —
`lea rcx, [rdi + 0x5380]`, `+0x7EA0`, `+0x8FA0` — plus `[rdi + 0x10F90] = 0xFFFFFFFF` and the pointer
store at `[rdi + 0x10FC0]`, which is the last field and ends at `0x10FC8`, eight bytes inside the
allocation.

### So the claim changes shape, and it is worth stating precisely

**Before:** 23,224 bytes reached zero times on five routes — four taint-first, one displacement-first.
**Now:** 23,224 bytes **never read and never individually written, and zero-initialised wholesale
~~exactly once, at construction.~~ by two bulk writes, at construction and in the `0x61F0`-byte clear of the `+0xAB30` child.** *(corrected 2026-10-02, OPUS: `00290CF0+0xA6` hands `+0xAB30` to `00276650`, whose `+0x88`–`+0x90` calls `00245000(obj, 0x61F0)`, and `002465F0+0x36` clears it; the RETRACTED 2026-09-19 note above)*

That is a different and better claim, because it supplies a **lifetime** where there was only an
absence: the bytes have a defined value from the moment the object exists, and nothing observed
changes it. *"Unreached"* was never the same as *"untouched"*, and this is the second time today that
distinction has mattered — `BattleUnit +0x298`, 1,016 bytes *"unreached on six routes"*, turned out to
sit inside a `0x610`-byte `memset` from `BattleUnit_ResetStateForReuse`. **The same mistake was
available here at ten times the size.**

### What was already known, and what was not

The allocation (`0028F8CF`, `0x10FD0`), the constructor's address (`00291750`) and the object's size
are all recorded already — in `types.tsv`'s `ctor` and `allocation_site` columns and in §above. **What
no page or row states is that the constructor's first act is a wholesale clear**, and that is the only
part of this section that is new. A `ctor` column naming an address is not a reading of it, which is
the same gap `BQ-25` punished on the 88 teardown functions: **a named function is not an understood
one.**

**NOT CLAIMED:** that the hole is *only* written by this `memset`. This sweep covers `memset` and
`memcpy` calls reachable within three call levels of a singleton loader — **17 bulk calls, 2 of them
`0x400` bytes or larger**. The negative from the five earlier routes bounds *reads*; this bounds one
class of *writes*.

> **TIGHTENED, same day: the two gaps this paragraph named have now been swept, and both are empty.**
>
> **`rep stos` / string ops.** Across the whole 805-body closure there is **exactly one** true string
> instruction: `00275564 rep stosd` inside `00275550`, a 28-byte generic `zerofill(dst, byteLen)`
> (`sar edx, 2` to convert bytes to dwords, `eax = 0`). It has ten callers, four of them in the
> singleton's own `00291xxx` family, and **none of the eight call sites targets the hole**: seven pass
> a register-held buffer (`rcx, rax` / `rcx, rbx` — separately allocated, not `singleton + disp`) and
> the one that does use a displacement is `[rsi + 0xD54]`, far below `+0xB244`.
>
> **Inline unrolled copies.** Of the 136 bodies that load the singleton slot, **zero** contain a wide-move
> run of eight or more within `0x80` — so no unrolled block copy writes this object directly.
>
> ~~So on the extended sweep the constructor's `memset` remains the **only** bulk write reaching the hole.~~ *(corrected 2026-10-02, OPUS: a second bulk write reaches it, the `0x61F0`-byte clear of `+0xAB30` at `00276650+0x88`–`+0x90`; the RETRACTED 2026-09-19 note above)*
> **The third gap was MIS-SPECIFIED, and correcting it closes most of it.** I wrote that `[rdi + 0x10FC0]`
> was *"exactly such a hand-out"*. It is not a write path into this object at all: `0029176A` allocates
> `0x8030` bytes and `00291779` stores that pointer **into** the singleton, so a write through it lands
> in the separate buffer, not in the hole. The `0x8030` block is a **child allocation**, and the hole is
> `0x5AB8` bytes of the singleton's own storage.
>
> **The gap that actually exists is the singleton's own address escaping**, and it now has a bound.
> Taking the call graph to its **fixpoint** rather than three levels — **2,341 bodies, depth 21**, every
> function transitively reachable from any of the 136 slot loaders — only **3** of the 32 bodies in the
> image carrying a hole displacement fall inside it: `0019AA20`, `002B9D30` and `00322C50`. **None
> references the slot**, and their rip-relative globals are `008C27C8`/`008F3DC0`, `0209E5F0` and the
> `02EBF0xx` battle block respectively — three different objects, none of them this one. So if the
> singleton were handed to anything that writes at a hole offset, that body would be in the 2,341 and
> would carry the displacement. It is not there.
>
> **What genuinely remains is narrower than a subsystem hand-out: an INDIRECT call.** A virtual or
> function-pointer target has no edge in the static graph, so a writer reached only that way sits
> outside all 2,341. That is the residual, and it is the same shape as every other limit in this
> section — a route the instrument cannot follow, named rather than assumed away.
>
> *(The first pass of this sweep reported 1,766 string instructions. `movss` and `cmovs` contain the
> substring `movs`. The count is 1.)*

## 42,192 bytes of the database's UNKNOWN space have a known value (2026-09-19, OPUS)

*The sweep above, run across every type rather than this one. It is placed here because the method
and its largest instance are here; the other rows belong to their own pages and are cross-referenced,
not claimed.*

`check_ctor_clears.py` finds whole-object clears two ways — a `memset(this, 0, N)` inside a recorded
constructor, and a declared type size matching a literal `memset` length anywhere in the image. Every
destination below was **read** before it was counted, and the coverage column is how many of that
type's own gap-named bytes fall inside the cleared extent.

| type | clear | where | gap bytes zeroed | spans |
|---|---|---|--:|--:|
| `ManagerSingleton0209BE80` | `0x10FD0` | `00291765`, ctor's first act | **25,682** | 19 |
| `BattleUnit` | `0xF50` | `002344D2` allocate, `002342CE` release | **1,357** | 31 |
| `ManagerSub0209BE80_5380` | `0x460` | `00893ED1`, allocated then zeroed | **1,087** | 4 |
| `PersistentFlagPayload` | `0x1538` | `002EF2E8`, at `buffer + 0x200` | **778** | 1 |
| `ManagerSub0209BE80_57E0ArrayRecord` | `0x2A0` | `00333048`, `rcx` = the record | **622** | 3 |
| `ImageBackedStateBlock` | `0x4818` | `00253AA7`, after the `0x58` header clear | 277 | 7 |
| `CharacterRenderRecord` | `0x740` | `0041F754`, in `_ResetDefaults` | 253 | 42 |
| `ActorManagerSlot` | `0x288` | `00266EFC`, a static array, slot by slot | 147 | 11 |
| `SpawnRecord` | `0x250` | `0036496A`, a static cleared then published | 24 | 6 |
| `BattleStatsRecord` | `0x1C8` | `0023ACBD`, `rcx` = the record | 13 | 5 |
| `SpawnKeepImage` | `0x20010` | `00233451`, `rcx` = the incoming image | 12 | 1 |
| *(`SavePayload`, three spans)* | `0x56690` | `002EF603` / `002EF663`, the whole image | **11,940** | 3 |

**Total: 42,192 bytes across 133 spans and 12 objects.** `BattleUnit`'s row is the whole of its
unknown space — **all 1,357 bytes in all 31 spans** — and the singleton's 25,682 is most of the
database's single largest unknown region.

### What this is and is not

**It is a lifetime fact.** These bytes hold zero from the moment the object exists, and for
`BattleUnit` from both ends of a slot's life. A reimplementation that allocates without the clear
differs from the engine **in bytes no test will catch**, because nothing reads them — until something
does.

**It is not a semantic fact, and it does not shrink the unknown space.** Not one of these bytes is
better understood than before; `unobservedSpan0298` is still 1,016 bytes of unread `BattleUnit`. What
changed is that *unknown* no longer implies *undefined*.

**And the method's limits are printed with its output.** A size match is a candidate, not a finding:
a size with 73 `memset` sites is a common number rather than a type, and a `lea rcx, [rsp + 0x40]`
destination is a local buffer. Every small-size candidate in the store resolves one of those two
ways, and the tool now says which. **The first version of this note called the match
"high-precision"; that was true only of the six largest rows, and is corrected here.**

### The embedded children are covered too, and the total is 52,076 bytes

**The table above undercounts, because it charged the singleton only its own rows.** Seven types are
*embedded* in this object rather than allocated separately — `_00A0`, `_5380`, `_57E0`, `_7EA0`,
`_7FB0`, `_8FA0`, `_A0D0` — and every one of them ends inside `0x10FD0`, so the constructor's clear
zeroes their unknown bytes as well:

| child | at | gap bytes | spans |
|---|---|--:|--:|
| `ManagerSub0209BE80_8FA0` | `+0x8FA0` | 4,328 | 9 |
| `ManagerSub0209BE80_A0D0` | `+0xA0D0` | 2,435 | 4 |
| `ManagerSub0209BE80_7FB0` | `+0x7FB0` | 2,448 | 1 |
| `ManagerSub0209BE80_5380` | `+0x5380` | 1,087 | 4 |
| `ManagerSub0209BE80_57E0` | `+0x57E0` | 1,086 | 14 |
| `ManagerSub0209BE80_7EA0` | `+0x7EA0` | 153 | 2 |
| `ManagerSub0209BE80_00A0` | `+0xA0` | 56 | 3 |

**11,593 bytes in 37 further spans**, so this object alone accounts for **37,275 bytes in 56 spans**
and the corpus-wide total is **52,076 bytes across 163 spans**, not 42,192. `_5380` is counted once:
its separate `0x460` allocate-then-zero at `00893ED1` is the same type reached a second way, not a
second region.

### `U-7` was answered while this was being written, and the sweep corroborates it

`b2e83fb7a` (SWE2-STRUCT) resolves the span this page spent two rounds on: `+0x270` is **thirteen
`0x2A0` claim-slot records**, not forty-two `0xD0` ones, and `0x270 + 13 × 0x2A0 = 0x2490` lands to
the byte on `ptr7C70` — **the same boundary this page derived, with the right stride.** My negative
answer stands for the question asked; the positive answer is theirs.

**Two independent confirmations fall out of the sweep above.** Their witness is
`00275550(rcx, edx=0x2A0)`, the generic `rep stosd` zerofill — **the same helper the `rep stos` pass
on this page identified as the closure's only string instruction**. And the size-match pass
independently flagged `ManagerSub0209BE80_57E0ArrayRecord` (`0x2A0`) as a whole-record clear at
**`00333048`**, a *different* site from the claim loop. So the record type is cleared at two
independent places, and neither of us started from the other's evidence.

*The `+0xD0`/`+0x1A0` pair remains a different shape — a count word at record-relative `+0xC2`
against the claim record's flag at `+0x272` — which is why the two readings never reconciled.*

### The whole unknown space, split: 93 % of it has a known value

*The sweep turned on the store as a whole rather than one object. This is the reconstruction-readiness
statement the earlier sections were building toward, and it is a different claim from any coverage
figure this database reports.*

Of **56,958 declared-unknown bytes in 377 spans**:

| | bytes | spans |
|---|--:|--:|
| zeroed — the object is cleared wholesale | **52,758** | 167 |
| zeroed — the span sits inside a cleared container (`SaveImageHeader` within the `0x56690` save image) | 338 | 4 |
| **no clear attributed** | **3,862** | 206 |

**So at least 93.2 % of the database's unknown bytes are zero-initialised, and at most 6.8 % are
genuinely undefined at allocation.** *Unknown* and *undefined* have been the same word in this corpus
and they are not the same thing: the first says nobody read the bytes, the second says a
reimplementation is free to put anything there. Only the second is a reconstruction risk.

**The 3,862 is an UPPER bound and the 53,096 a LOWER one.** Containment is hand-maintained here — the
`SaveImageHeader` row is in the second tier only because I happened to publish that clear this
morning and recognised the overlap. Other rows in the residue are plausibly sub-records of cleared
parents (`ManagerSub00A0Entry`, `ManagerSub7FB0Record`, `CharacterRenderSystemTail` all name a parent
that is itself cleared or allocated in one block) and each needs its containment read before it can
move. **No row was moved on a name.**

### What the residue actually is

| type | offset | bytes |
|---|---|--:|
| `CharacterRenderObject` | `+0x118` | 632 |
| `MessageWindowRecord` | `+0x1B0` | 520 |
| ~~`ManagerSub00A0Entry`~~ | ~~`+0x18`~~ | ~~232~~ *re-tiled 2026-09-27 (OPUS): its own initialiser `003F9390` and reset `003F00F0` write most of it; 90 bytes stay unobserved (`_index/candidates/manager-a0-entry-layout/`)* |
| `ManagerSub7FB0Record` | `+0x8` | 232 |
| `CharacterRenderSystemTail` | `+0x70` | 192 |
| `CharacterRenderObject` | `+0x80` | 144 |

**206 spans for 3,862 bytes — a mean of under nineteen bytes each.** The genuinely undefined part of
this database is not a hole; it is dust, and `CharacterRenderObject` owns three of the six largest
pieces. That is a far more actionable target list than *"57 KB unknown"*, and it is the first time the
two questions have been separated.

> **CORRECTED SAME DAY — THE UPPER BOUND WAS TOO HIGH, AND RUNTIME-SIZE CLEARS ARE WHY.**
> `MessageWindowRecord +0x1B0` (520 B) sat in the residue above and does not belong there. Every
> widget is allocated by `00244F50` and constructed by **`002465F0`**, which does `movsxd r8, edx`
> on the **size argument**, `xor edx, edx`, and `call memset` at `00246626` — so the whole record
> is zeroed with a length the caller supplies. **The sweep reads only LITERAL lengths**, which is
> the limitation stated when it was published, and this is what it costs: **783 bytes in 15 spans**
> move from undefined to zeroed. **The residue is at most 3,079 bytes in 191 spans**, not 3,862.
>
> A third pass now reports `memset(this, 0, <register>)` as its own shape, because an allocator
> that takes a size and clears what it hands back is an ordinary idiom rather than an edge case.
> **The direction of this error is the important part:** a literal-only sweep can only ever
> *overstate* the undefined residue, so `3,079` remains an upper bound and `53,879` a lower one.
>
> **AND THE BLIND SPOT IS NARROW, WHICH IS WHY `3,079` IS TIGHT RATHER THAN NOMINAL.** Swept
> image-wide, **exactly seven** functions do `memset(this, 0, <register>)`: `002465F0` (5 callers,
> the widget constructor above), `0061E6B0` (5), `003EFD00` (4), `00124380` (2), `00403F90`,
> `0061E550` and `0061E600` (1 each). **One of the seven touched the residue.** The runtime-size
> idiom is rare in this executable, so the literal restriction cost one family and not a class of
> them — which is a measurement, not a hope.
>
> **`001F4DA0` is not among the seven**, which reconfirms `CharacterRenderObject` by a route
> independent of the `0x668` literal sweep: it is cleared neither by a literal-size `memset` nor by
> a runtime-size one, because it is cleared by neither kind anywhere.
>
> **ALL SEVEN ARE NOW ATTRIBUTED, AND ONLY ONE REACHES A DECLARED TYPE.** Reading each:
> `002465F0` is the widget constructor (above). **`00124380` is not a constructor at all** —
> thirty-three bytes that `memset(rcx, 0, rdx)` and return `(rcx + 0xF) & ~0xF`, a generic
> **aligned-buffer zeroer**; both its callers pass `0x630` and **no type in the store is `0x630`**.
> `003EFD00` takes its length from `r11d`, `[rdi + 0x54]` and `esi` at its three call sites, and
> `0061E550` / `0061E600` / `0061E6B0` / `00403F90` are likewise dynamic. **None of the six is a
> fixed-size object clear**, so no further span moves out of the residue by this route.
>
> **The runtime-size question is therefore closed by exhaustion rather than left open:** seven
> candidates, all read, one attributable, and `≤ 3,079 bytes in 191 spans` stands.
>
> **INLINE UNROLLED ZEROES ARE CLOSED TOO, AND THAT WAS THE OTHER NAMED LIMIT.** A constructor can
> zero an object without calling anything — `xorps xmm0, xmm0` then a run of `movups
> [rcx + N], xmm0` — and no pass above can see it. Swept image-wide for a zeroed XMM register
> stored to four or more `this`-relative offsets: **eight functions**, the largest covering
> `+0x60`–`+0xA60`. **Not one is named as a `ctor` or `allocation_site` by any type in the
> store**, so nothing moves out of the residue by this route either.
>
> **`001F4DA0` is not among the eight.** `CharacterRenderObject` is now confirmed uninitialised by
> **three independent sweeps** — no literal-size `memset` of `0x668` anywhere, not among the seven
> runtime-size clears, not among the eight inline zeroes — on top of its fourteen-byte base
> constructor and its plain `malloc`.
>
> **What remains is one structural limit, not an unexamined one:** a writer reached only through an
> indirect call has no edge in the static graph. Every other route into these bytes has been
> enumerated and read.

**NOT CLAIMED:** that a zeroed byte is understood. Not one byte above is better explained than it was
— `unobservedSpan0298` is still 1,016 bytes of unread `BattleUnit`. The claim is only that a
reimplementation which zeroes these objects will agree with the engine there, and that the 3,862 *(answered: see the CORRECTED SAME DAY note above, at most 3,079 bytes in 191 spans; 2026-10-02, OPUS)* are
where it will not.

## SWE2-EC7-40 update (2026-09-19) - `002E6700`

`002E6700` (381 B) is a per-frame-gate body - `0215FD58`/`0215FD78`, `0036C1D0`/`0036C1A0`/`002ED6F0`/`0032E400`/`0036B160`/`002EAD50`. Interior anchor `002E673F` (a `0036C1D0` call).

## SWE2-EC7-42 update (2026-09-19) - `00290EB0`

`00290EB0` (319 B) is a per-frame-gate body - `00915FE8`/`0209BE80`, `00273A20`/`00245000`/`003F8010`/`003F8030`/`00247570`/`00247930`/`00246AC0`. Interior anchor `00290EEC` (a `00273A20` call).

## SWE2-EC7-43 update (2026-09-19) - `0028F0C0`

`0028F0C0` (291 B) is the per-frame helper that hands `singleton+0x5980` on - `0209BE80`, `00244F00`/`00253770`/`00273A20`. Interior anchor `0028F0E3` (a `00244F00` call).

## SWE2-EC7-43 update (2026-09-19) - `002C6180`

`002C6180` (295 B) is a per-frame-gate body - `01DFE0B4`/`02092730`, `0028F5B0`/`002C6B50`/`002C6BE0`/`002C8D60`/`002C8DF0`. Interior anchor `002C61E3` (a `0028F5B0` call).

## SWE2-EC7-48 update (2026-09-19) - `00291B90`

`00291B90` (208 B) is a body - `00273B40` single call. Interior anchor `00291C3F` (the `00273B40` call).

## SWE2-EC7-52 update (2026-09-19) - `003F26F0`

`003F26F0` (893 B) is the `0xD0`-stride array walk - `add rbx,0xD0` loop, `00203170`/`00202F00`/`00202B70` calls plus `02EBB7A4`. Interior anchor `003F276D` (a `00203170` call).


## SWE2-EC7-52 update (2026-09-19) - `0019AA20`

`0019AA20` (1099 B) is a hole-displacement body - `0080C5A0`/`00861EBA` calls plus `call [rip]` import sites (`008C27C8`/`008C27D0`/`008C29C0`). Interior anchor `0019AAAE` (a `0080C5A0` call).

## SWE2-EC7-53 update (2026-09-19) - `0028C620`

`0028C620` (547 B) is a per-frame-gate body - `003F26F0`/`003F2A70`/`003F2F20` triple plus `00271530`/`00271650`/`002716C0`, `008F8180` rdata. Interior anchor `0028C688` (a `003F2A70` call).


## SWE2-EC7-53 update (2026-09-19) - `002C6BE0`

`002C6BE0` (468 B) is a call-free per-frame ramp - `[rdx+0x1B0]`/`[rdx+0x1B9]`-bit-0 gate, `+0x1BA` accumulates `0x20/[01DFE0B4]` clamped at `0x80` (bit-1 arm decrements). Interior anchor `002C6C2A` (the `+0x1BA` accumulate).


## SWE2-EC7-53 update (2026-09-19) - `00289A10`

`00289A10` (448 B) is a `0x460`-word gate body - `0028A790`/`0028AAA0`/`0028B140`/`0035D3D0`/`0035D460`/`0035D470`. Interior anchor `00289A2A` (a `0035D460` call).


## SWE2-EC7-53 update (2026-09-19) - `0029B550`

`0029B550` (420 B) is the `+0x648` gate body - `00254560`/`00272EE0`. Interior anchor `0029B59D` (a `00272EE0` call).


## SWE2-EC7-53 update (2026-09-19) - `0028D030`

`0028D030` (400 B) is a `0xD0`-index gate body - `00270FF0`/`00271080`/`00271450`/`002714A0`/`00272390`/`003F3010`. Interior anchor `0028D052` (a `003F3010` call).

## SWE2-EC7-54 update (2026-09-19) - `0028A790`

`0028A790` (771 B) is a per-frame-gate body - `00271140`/`00271AB0`/`00272DE0`/`0035D3D0`/`003F0040`/`003F1290`/`00808C40` plus `00915F68` rdata. Interior anchor `0028A7CF` (a `0035D3D0` call).


## SWE2-EC7-54 update (2026-09-19) - `003F2A70`

`003F2A70` (638 B) is a per-frame-gate body - `00202B70`/`00202C70`/`00202C90`/`00202F00`/`00202F70`/`00203170`/`00271290`/`00808C40` plus `008F3138`/`008FCCA0`/`00902438` rdata. Interior anchor `003F2AB1` (a `00203170` call).


## SWE2-EC7-54 update (2026-09-19) - `002BE300`

`002BE300` (334 B) is the `+0xAC0` sub-object body the gate hands on - `0016D6A0`/`00290990`/`002BEA40`/`002BF0E0`/`0035C070`/`003C53E0`. Interior anchor `002BE33B` (a `00290990` call).


## SWE2-EC7-54 update (2026-09-19) - `0028CA40`

`0028CA40` (332 B) is a `0x110`-word `_7EA0` gate body - `00202C90`/`0028DFD0`/`002E7F70`/`003588B0`. Interior anchor `0028CA75` (a `003588B0` call).

## SWE2-EC7-56 update (2026-09-19) - `002C8DF0`

`002C8DF0` (234 B) is a call-free intrusive-list unlink - `+0x17` flag test, `+0x18`/`+0x20` neighbour relinks, `[r8+0x1D70]`/`[r8+0x1D60]` heads, `rax+0..0x38` zeroed. Interior anchor `002C8E37` (the `+0x18` relink).


## SWE2-EC7-56 update (2026-09-19) - `003FA600`

`003FA600` (223 B) is a `0x26C0`-word `_57E0` gate body - `003FBA80` single call plus `0090769C`/`009153EC`. Interior anchor `003FA695` (a `003FBA80` call).


## SWE2-EC7-56 update (2026-09-19) - `002EAD50`

`002EAD50` (206 B) is a per-frame-gate body - `0017F000`/`002ED6F0`/`0032E400`/`0032E620`/`0036A000`. Interior anchor `002EAD65` (a `0036A000` call).

## SWE2-EC7-58 update (2026-09-19) - `002BF3D0`

`002BF3D0` (166 B) is the `+0x109C` sub-object body the update-gate contract names - `002432B0`/`00244F50` plus `01E0CE88`/`0209AC30`. Interior anchor `002BF3F3` (a `00244F50` call).

## SWE2-EC7-59 update (2026-09-19) - `002BDB60`

`002BDB60` (159 B) is an `_8FA0`-family update-gate body - `00244DD0`/`002544B0`. Interior anchor `002BDB77` (a `002544B0` call).


## SWE2-EC7-59 update (2026-09-19) - `002BDC00`

`002BDC00` (159 B) is an `_8FA0`-family update-gate body - `00246AC0`/`00247930`/`002544B0`. Interior anchor `002BDC1E` (a `00247930` call).

## SWE2-EC7-61 update (2026-09-19) - `003F8030`

`003F8030` (151 B) is a per-frame-gate body - `0029CD90`/`002F9860` plus `00D11E30`/`01CEBBA8`. Interior anchor `003F804C` (a `002F9860` call).



## SWE2-EC7-63 update (2026-09-19) - `002C6B50`

`002C6B50` (144 B) is a call-free flag-gated divider - `r8b&1`/`&2` gates, `word[rcx]` count, `0x20 / [01DFE0B4]` div then `r10w`-bounded loop (`002C6BE0` sibling). Interior anchor `002C6B92` (the `div [01DFE0B4]`).



## SWE2-EC7-64 update (2026-09-19) - `002BE1A0`

`002BE1A0` (141 B) is a `_8FA0`-band body - `0016D6A0`/`0028E1D0`/`0028E240`/`00290990`/`002BE0A0`/`002BE300`. Interior anchor `002BE1C9` (a `002BE0A0` call).



## SWE2-EC7-65 update (2026-09-19) - `002C8D60`

`002C8D60` (137 B) is a per-frame-gate body - `002C6F70`/`003588B0`/`003590D0`/`0035D500`/`0035D510`. Interior anchor `002C8D7D` (a `003590D0` call).



## SWE2-EC7-66 update (2026-09-19) - `003FA570`

`003FA570` (131 B) is a `_57E0`-band body - `003F14D0`/`003FB3E0`. Interior anchor `003FA5AE` (a `003FB3E0` call).



## SWE2-EC7-66 update (2026-09-19) - `0028C590`

`0028C590` (130 B) is a same-type caller pair member - `00270FF0`/`00271080`/`00271450`/`002714A0`/`00272390`/`0028D030`. Interior anchor `0028C5AE` (a `00271450` call).


## SWE2-EC7-67 update - `002E6880`

`002E6880` (128 B) is a per-frame-gate body - `002E6EB0` single call plus `0215FD68`/`0215FD80`. Interior anchor `002E68A7` (a `002E6EB0` call).

## SWE2-EC7-69 update (2026-09-19) - `00271290` element-fill loop measured

`00271290` (70 B) is the strided element-fill the gate bodies run: `r8d <= 0`
returns; otherwise it calls `00202C90(dst, src_base + dst)` `r8d` times,
stepping `dst` by `0x10` - `rsi = rdx - rcx` folds the source base into the
second arg so each element is `00202C90(dst_i, src + dst_i)`. The callee is
the 16-byte record copier the gate's sibling bodies name.
Interior anchor `002712B7` (the `00202C90` call).

## SWE2-EC7-70 update (2026-09-19) - `002BE0A0` one-time three-part init measured

`002BE0A0` (107 B) is the init the `_8FA0`-band bodies gate on
`word[+0x10FA] & 1`: already set returns 1, `[0209AC30]+8` absent returns
0; otherwise it runs `002BF3D0` on `+0x109C` (arg 0), `+0x10B0` (arg 1) and
`+0x1088` (arg 8) - the three sub-record initializations - then ORs the
`+0x10FA` flag so the body never re-runs.
Interior anchor `002BE0F8` (the `or word[+0x10FA], 1` commit).

## SWE2-EC7-71 update (2026-09-19) - `00271080` / `00270FF0` draw-list helpers measured

Measured on `the-map-screens-and-their-shared-map-data.md` (PARTIAL - non-bearing); mirrored here on the gate page their callers run under.

`00271080` (58 B) is the tag writer the draw bodies call to head a packet:
`rax = [rcx+0x18]` is the write cursor, `dword[rax+8] = 0x11000000` and
`dword[rax+0xC] = 0x10000000` stamp the two tag fields, and
`([rcx+0x10] - eax - 0x10) >> 4` derives the element count handed to
`0016D6A0`. Interior anchor `002710B0` (the `0016D6A0` call).

`00270FF0` (30 B) is the matching consume: when `[rcx+0x10]` and `[rcx+8]`
differ it advances `[rcx][+8]` by the 16-aligned pending span
`((+0x10 - +0x8) & ~0xF)` and tail-jumps `003A1DB0`; equal cursors return
without touching the buffer. Interior anchor `00271004` (the `[+8]`
advance).

## SWE2-EC7-71 update (2026-09-19) - `00275490` vec3 lerp measured

`00275490` (79 B) is the scalar-lerp the gate bodies share:
`dst[i] = (b[i] - a[i]) * xmm3 + a[i]` for `i = 0..2` (`subss`/`mulss`/
`addss` per channel) and `dst[3] = 1.0f` - a `lerp(a, b, t)` with the
blend factor passed in `xmm3` and unit w written unconditionally.
Interior anchor `00275499` (the first `mulss`).

## SWE2-EC7-73 update (2026-09-19) - `003C53E0` slot clear measured

`003C53E0` (18 B) is the `02B45970` element clear the gate bodies call:
`dword[02B45970 + ecx*4] = 0` - a single indexed slot reset.
Interior anchor `003C53EA` (the indexed zero store).

## SWE2-EC7-76 update (2026-09-19) - `00290990` + `00272DE0` + `00272390` gate helpers measured

`00290990` (83 B) is the `0209BE80` teardown: `[+0x10F00]` non-NULL
gets `0028C4F0`, `+0x10F68` bit 3 cleared, `+0x10EF0` zeroed, and
`0028C940(+0x7EA0)` tails - the release the per-frame gate calls.
Interior anchor `002909B3` (the `+0x10F68` mask).

`00272DE0` (34 B) is the `003588B0`-gated tail: NULL returns
`xmm0 = 0`; otherwise `002E7E90(rax)` - the one-call forwarder.
Interior anchor `00272DFD` (the `jmp 002E7E90` tail).

`00272390` (110 B) is the 16-byte element apply: `r8d` iterations run
`00202C90` on each `+0x10`-strided element starting at `[rcx+0x10]`
with `rdx - base` preserved via `rsi`, then `[rcx+0x10]` advances by
`r8d * 16` - the consume-and-advance the gate bodies share.
Interior anchor `002723C9` (the `00202C90` call).

## SWE2-EC7-86 update (2026-09-20) - `003F3010` dual static-config apply measured

`003F3010` (49 B) is the two-table apply the frame-gate callers
run: `00202C70(rcx+0x50, 02AEDDB0)` loads the first static table
into the record, then a tail `00202C90(rcx+0x90, 02AED5F0)`
applies the second - two `.data` template copies onto `+0x50`
and `+0x90`.
Interior anchor `003F303C` (the `00202C90` tail).

## SWE2-EC7-88 update (2026-09-20) - `003CA1C0` object flag rewrite measured

`003CA1C0` (27 B) is the two-bit rewrite the frame-gate callers
run: when `[02B47758]` is live, `dword[+0xA90]` is cleared of
bit 0 and set with bit 1 - one flag edge on the shared object.
Interior anchor `003CA1D3` (the `or` arm).

## SWE2-EC7-94 update (2026-09-20) - `0035BC40` measured

`0035BC40` (10 B) is the constant-1 trampoline `002507C0`,
`00285290` and `002964D0` call: it sets `ecx = 1` and falls into
`0035BC50`, the shared continuation the gate uses to re-enter the
poll with the enable value pre-set.
Interior anchor `0035BC45` (the tail `jmp 0035BC50`).

## SWE2-EC7-102 update (2026-09-20) - `0028C4F0` measured

`0028C4F0` (101 B) is the `+0xD70`-linked normalize
walk `00290990`, `002909F0`, `00290B10` and
`002917E0` call: each node's `word[+0xD54]` is
tested - a value of 4 skips; a value carrying any
`0xFFFA` bit takes `+0xD4C &= ~8`, `+0xD54 = 3` and
`+0xD30 = 0`; a zero value instead gets
`+0xD54 = 5` - the state rewrite the per-frame
update arms run down the list.
Interior anchor `0028C510` (the `+0xD54` loop
head).

`003FC510` (1005 B) is the emit body the `0x0400` group `003FA790` runs: `word[rcx+0x272]` seeds the count, `edx = 0x140` and `r8d = 0x4000` size the span, `002713E0`/`00275490` do the work across four cookie-checked regions - the bit-0x0400 subsystem's per-frame emit.

Interior anchor `003FC73C` (function `003FC510`).

`002917E0` (930 B) is the emit body the `display UI : battle` fan-out `0028E290` runs: `00275550` x3, `00271650`, `00272F30` x2, `00202C90` x2, `0028C850`, `0028C4F0`, `0028C4B0`, `00273A30`, `0024A5A0`, `00271140`, `0028C620` with the `00181540`/`00181250`/`00181000` text helpers - the battle-UI layer's draw submission.

Interior anchor `002919B0` (function `002917E0`).

`00271650` (99 B) is the tagged record builder `0028C620`, `002917E0`, `003F77F0` and `003F7CC0` call: `[rcx]` gets `(arg << 0xF) | 0x1000000000000002`, `+8` is `0xE`, the `+0x10` sub-record stores `5`, `8`, two zeroes and a `(r9 + r10*2)*2 << 0x25 + [rdx+0x30]` pointer - a call-free packet-shape writer.

Interior anchor `0027166A` (function `00271650`).

`00275550` (28 B) is the dword zero-fill ten emit bodies share (`002917E0` x3 among them): `edx >> 2` counts the dwords and `rep stosd` clears `[rcx]` - the smallest helper on the gate's caller list.

Interior anchor `00275564` (function `00275550`).

`0028D980` (627 B) is the target-line group's render setup `0028C590` runs (the `0x0004` arm's body on the one-word page): `003F3010` x2 on `+0x3C0`/`+0x990`, `00181560`, `00181910(0x53001)`, `001816B0(0x44)`, `00181870(4)` and `00181890(1, ...)` prime the pass, then `+0xD00`/`+0xD78`/`+0xD7C` feed `00181930` on the "targetline_p" literal, `00181740` + `00271450`/`00270FF0`/`00271080`/`002714A0`/`00272390`/`0028DC00` - the target-line list's per-frame emit.

Interior anchor `0028D9A8` (function `0028D980`).

`003FC170` (626 B) is the 0x0400-group body `003FA790` runs: xmm-spill cookie frame, the `rcx+0x80` record pairs `01EF93F8`/`01EF93F0`/`01EF93FC`/`01CEBC50` constants with the `00D11E6C` table and `0208F570` bound, then `00202B10`/`00202B70`/`00202C90`/`00202DE0`/`00203080`/`00270720`/`00270A10`/`00270CF0`/`00808C40`/`00861F0E` emit each entry - the group's per-entry transform emit.

Interior anchor `003FC2D6` (function `003FC170`).

`00270A10` (295 B) is the yaw helper the 0x0400-group emit `003FC170` (and `003F6BB0`/`003F7760`) call: |x|/|z| -> `maxss` feeds `00861F02` twice for the two octant cases, the second result negated and wrapped by `00915620`/`01CEBC78`/`01CEBC50` into [0, 2pi) - the vector's heading.

Interior anchor `00270A68` (function `00270A10`).

`00270CF0` (597 B) is the lerp `003FC170`/`003F7760` call: `xmm13 == 0` copies `rdx` through `00202C90`, `xmm13 >= 1.0` copies `r8` the same way, otherwise the component-wise `mulss`/`addss` dot-blend runs - the group's parameter blend.

Interior anchor `00270D51` (function `00270CF0`).

`002E6EB0` (450 B) is the bitfield evaluator `002E6880` calls: `rol edi` walks set bits of `dword[rbx+0x28]`, each bit indexes `word[rbx+0x22] * 0x40` into the `0215FDA0` table for a `dword[+0x5C]` compare, and `0036C1D0`/`0036C1A0`/`002E9920`/`0036B160`/`0036C5D0`/`002ED6F0`/`0036A000`/`0032E620`/`0036C140`/`0036C110` run the per-bit arms - the gate's flagged-field pass.

Interior anchor `002E6F3B` (function `002E6EB0`).

`002E9920` (154 B) is the clamped forwarder `002E6EB0`/`002EB9D0` call: `002ED6F0` fills `[rsp+0x40]`/`[rsp+0x48]`, the count chooses `ecx+1` or `ecx+0x43` by `cmove`, `eax >= 1` and `edi & 0xFF0000 == 0x6D0000` gate, `ebx` clamps into `1..0x10`, and `ebx + ecx` tail-jumps `0032E400` - the gate's bounded index step.

Interior anchor `002E9938` (function `002E9920`).

`002E6900` (378 B) ~~is the list append `002E65A0`/`002E6D60` call: walks `0215FD90`'s `+8` links to the tail (or `rbx` when the head is empty), then `0020E600` resolves, `0041E490`/`00369800`/`002E9470` build the node and `002E6A80` links it - the per-frame gate's tail insert.~~ *(corrected 2026-10-01, OPUS, on ASTRA's lane-drain correction, re-read at the bytes: it is the lane DRAIN `002E65A0`/`002E6D60` call. From the tail of `0215FD90`'s list it walks back through `[node]`; for each of the 32 lanes set in both `+0x14` and `+0x1C` with a non-zero handle at `+0x50 + 4*lane` it resolves the handle (`0020E600`, `002E6982`), unregisters it (`0041E490`, `002E698C`), frees it (`00369800`, `002E6994`) and clears the lane and its bits; it unlinks the node and, when `+0x18` and `+0x14` are both 0, retires it through `002E9470` (`002E69E8`); it repeats while its argument is non-zero, then runs `002E6A80` on nodes whose word `+0x22` is negative. Every normal return is 0 (`002E6A70`) - not an IO-completion status)*.

Interior anchor `002E6982` (function `002E6900`).

`002E7F70` (86 B) is the record validator `0028CA40`/`0028DFD0`/`003D9E20` call: `rcx` null, `[rcx + 0xC0]` null, or `dword[*]==0xFFFFFFFF` returns 0; otherwise `word[*] x 0x740` indexes `022C6F28` and a live `dword[rec + 0x284]` calls `003E5510` before returning 1 - the gate's poke-if-live probe.

Interior anchor `002E7FB0` (function `002E7F70`).

`00270720` (340 B) is the row extract `003F74F0`/`003F7610`/`003FC170` call: after `00203170`, `1.0 - 2*(x^2 + y^2)`, `2*(z*y - w*x)`, ... writes the quaternion's first matrix column through `[rdi]` - the gate's orientation unpack.

Interior anchor `00270730` (function `00270720`).

`003F7610` (334 B) is the pose composer `003F6BB0` gates: stack-builds a matrix (`00203170` init, `00270720` compose on `rbx+0x10`/`rbx+0x2A0`, `00202F70`/`00202D70`/`002030E0` ops), resolves a `003588B0` scale lookup (`002645D0` float or 1.0f), then `003F74F0` applies the scaled pair to `rbx+0x100`.

Interior anchor `003F7685` (function `003F7610`).

`002BF0E0` (325 B) is the mode-resolution classifier `002BE300` calls: `ecx-1` selects mode 1/2/6 specials vs the general path - `00273710`/`00273880` gates, `003588B0`+`00263C20` score classify (result <=2, ==3, ==4, ==7 pick different `(r8d, edi)` pairs), tails `00290990`/`003C53E0`/`003C5400`/`0016D6A0`.

Interior anchor `002BF115` (function `002BF0E0`).

`003F77F0` (318 B) is the gated apply `003F6BB0`/`003F7CC0` call: requires `dword[rbp+0x2D0]`/`+0x2D4` nonzero, `002732E0`'s record live, `word[rbx+0x5C] != 0xFFFF`, and `002739D0` true; then `0030BEF0(+0x2D0, +0x2D4, word[+0x5C])` returns >0 -> `ebx`=4 else 1, `0028F6F0` + `00271650` on `rbp+0x1F0` apply, `dword[+0x32C]`=0 and `+0x330`=1|4 - the per-frame gate's gated state commit.

Interior anchor `003F786C` (function `003F77F0`).

`00272B40` (306 B) is the per-id consult `0035BC50` calls: `dword[rcx]` ids at `[rcx+8]` (a negative `dword[+4]` first resolves through `0035BAD0`) each pass `002E9D10` into `rsp+0x20`, then `00249110(rsp+0x30, 02AEDDB0, rsp+0x20, 1)` evaluates the entry against the flag table and the `(id, result)` pair collects on the stack - the flag-evaluator pass the gate's shared continuation runs.

Interior anchor `00272BD7` (function `00272B40`).

`0028CD80` (271 B) is the flag-directed tick `0028C870`'s `0x0800` group runs: `word[rcx+0x28]` bit 0 gates the update - bit 1 clear runs `00273780([+0x24])` and stores `(result == 0) x 2` into bit 1; bit 2 clear runs `00273750([+0x24])` and folds `(ax & 1) << 2` into bit 2; `003588B0` then hands a live record to `002E7F70(rbx+0x10)`; the `0x20 / dword[01DFE0B4]` step drains `byte[+0x2A]` toward 0 while bit 1 holds (clearing bit 0 at the floor) or fills it capped at `0x80`, `float[+0x20]` ramps `+0.125f` toward `1.0f`, and `dword[+0x2C] += 0x10` caps at `0x100` - the per-frame counter the group's update advances.

Interior anchor `0028CDEF` (function `0028CD80`).

`002E9360` (267 B) is the per-frame object retire `002E65A0` runs on its list node: a nonnegative `word[rcx+0x1E]` resolves the `x 0x120` (`x9 << 5`) record in `02161DA0`, and when `dword[record+0x5C]` still equals `[rcx+0x24]` it takes 32 rounds of `002EAFA0(record, i)`; three `003A0F80` decrements walk `[rcx+0x30..0x38]`, `[rcx+0x10]` frees through `00369800` when nonzero and is zeroed, `[rcx+0x14]` goes to `0017F040`, then the node unlinks from the `0215FD60`/`0215FD88` doubly-linked list, re-links at the head under a bumped `+0x24` generation with `+0x18`/`+0x26`/`+0x14` cleared - the detach-and-recycle the gate's object pool performs.

Interior anchor `002E93B6` (function `002E9360`).

`002EAFA0` (135 B) is the bit-indexed mark-and-relink `002E9360` runs 32 rounds of and `002E3F00` also calls: `edx = 1 << arg2` tests `dword[+0x2C]`; absent there but present in `+0x34 | +0x28 | +0x24` it is set in `+0x2C`, and when it was also in `+0x24` the node's `[+0x10]` entry unlinks from its doubly-linked list and re-links at the head of `0215FD90` - the per-slot flag-set the retire sweep performs. *(Qualified 2026-10-01, OPUS, on ASTRA's lane-stale-release, ACCEPTED by SWE2-AUDIT-SPEC (`_index/candidates/auditspec-review-astra-lane-stale-release-1001/REVIEW.md`), re-read at the bytes: a lane already set in `+0x2C` returns at `002EAFB2` -> `002EB026` before any write or call, so a stale-owner completion (`002E4E50`'s stale/null-owner arm passes the same sub-record and lane here) neither adds nor removes the node's sweep membership; a lane not yet in `+0x2C` but pending or masked and not loaded (`+0x24` clear) is marked without an enqueue. `002EB890` below only adjusts the lane WORD at sub-record `+0xE0 + 2*lane` - no call, no queue or global write - and sits on the valid-owner branch, so it cannot enqueue either. The node's prior queue membership, other relink producers, the scheduler and callee effects stay OPEN: no leak, safety or eventual-release claim follows.)*

Interior anchor `002EAFD2` (function `002EAFA0`).

`003DC4A0` (261 B) is the 16-slot drain `002E65A0` runs while `dword[02B58170]` is set: each `x 0x14` slot of `02B57F70` whose `byte[+6]` is `4` has its `dword[+0]` id resolved against `[022C6F28]+0x48830` via `0020E600`, released through `0041E490`, freed by `00369800`, and the slot cleared with `02B58170` re-armed to 1; a second pass then runs `003DC5B0` on all 16 slots before `02B58170` clears - the pending-id sweep the per-frame pump performs.

Interior anchor `003DC518` (function `003DC4A0`).

`00273A30` (258 B) is the chunked-block pop `002917E0` runs on the `rdi`/`rsi` pair: `r8d` rounds up to `0x10`, `[rsi+0x10]`/`[rsi]`/`[rsi+0x20]` are walked for a free chunk whose `[rdi+0x18]` capacity covers `rdx + 0x20 + ebx`; on a hit `[rdx+8] = count`, `[rdx]` self-links `rdx+0x20`, `+0x10`/`+0x18` clear and `rdx` stores at `[rdi]`/`[rdi+0x10]`; on a miss `00276000` then `002760A0` grow `rsi`'s list and `00276120` retries - `0` when nothing fits.

Interior anchor `00273AC4` (function `00273A30`).

`003F7BC0` (246 B) is the paired-channel accumulate `003F6BB0` runs: `00203080` gathers `[rcx+0x280]`/`[rcx+0x290]` into a stack pair and `00270550` reduces it into `xmm8`, then `dword[rbx+0x2D0]` and `dword[rbx+0x2D4]` each feed `003588B0` - a non-null result earns `002645D0` and its `xmm0` folds into `xmm7`/`xmm6` - the two-id sum one tick group performs.

Interior anchor `003F7BFB` (function `003F7BC0`).

`003C6000` (236 B) is the state-bit driver `002507C0` runs on `02B45A00`: bit `0` gates the body; under bit `4`, `00254A50` failing or `00377750` succeeding with bit `2` clear runs `003C80C0` and sets bit `2` (else `003C8070`/`00359150`), then `00202C90` binds `02B45810` for `003C5500`/`003C5060`; the tail sweeps `02B45970..02B45978` dword ids through `003588B0`, clearing any that resolve to null - the per-frame mode reconcile.

Interior anchor `003C6013` (function `003C6000`).

`00245000` (31 B) is the `002465F0` wrapper that passes the stack flag `dword[rsp+0x20] = 1` and returns `rbx` - the blocking-mode entry the per-frame gate callers take.

Interior anchor `00245011` (function `00245000`).

`00518D50` (259 B) is the per-element transform publish `003E00C0` runs: it caches the record's `+0x30..+0x58` into `022D91B0`/`022D91C0`/`022D91D0`, then for each of `[rbx+4]` elements resolves the `[rbx+0xC]`-chained index through `0020E600` twice (`[base][0]` -> index `*0x290`), storing the three cached 16-byte rows at `+0x230`/`+0x240`/`+0x250` and a zeroed row at `+0x260` on each element

Interior anchor `00518DA7` (function `00518D50`).

`003C80C0` (230 B) is the late arm `003C6000` installs on `02B476B0`: `003148F0()` feeding `0053DD10()` and `00264790() > 0` gate the pass; on pass it lazily registers `003C5910` through `00244F50` (`0xC8` frame), clears `+0x40` bit `0x8000`, re-tests `002544B0() == 1 || 02B476E0` to set it back and zero `02B476E0`, and tails `00246AC0`; on fail it clears `02B45A00` bits `1|2`, seeds `02B476E4` = `1`, mirrors the same `+0x40`/`0x10000` clear-check-set against `02B476E4`, and tails `00244F00`

Interior anchor `003C8145` (function `003C80C0`).

`002E9470` (226 B) is the node retire `002E6900` runs on `rcx`: the `+0x22` s16 slot's `0x40`-stride `0215FDA0` row takes `+0x1E = -1` when its `+0x24` still matches `[rcx+0x5C]`, `+0x22`/`+0x44` are cleared, the `+0x10` embedded node is unlinked from its doubly-linked list with `0215FD90`/`0215FD68`/`0215FD80` repaired when they named it, then `rcx` itself unlinks and pushes onto the `0215FD70` free head

Interior anchor `002E9501` (function `002E9470`).

`0028CE90` (225 B) is the flag-and-ramp update `0028C870` runs per frame on `rcx`: `+0x14` bit `0` set gates two probe arms - bit `1` clear runs `00273780([+0x18])` and rewrites bit `1` from its truth, then `00273750` writes bit `3` from `eax & 1` and a live `003588B0` record gets `002E7F70`; afterwards `+0x13` ramps by `0x20 / [01DFE0B4]` (currently `1`, so `+0x20`) - bit `1` set decrements (underflow clears bit `0`), clear increments clamped at `0x80` - and `+0x10` accumulates `+0x16`-mirrored ticks clamped at `0x100`

Interior anchor `0028CF0E` (function `0028CE90`).

`00273780` (35 B) is the live-record probe `0028CD80`/`0028CE90` run for the `+0x14` bit-0 arm: `ecx == 0` returns 0 outright; otherwise it returns whether `003588B0()` produced a non-null record

Interior anchor `0027378F` (function `00273780`).

`00273750` (34 B) is the state-range probe beside it: `003588B0()` then `00263C20()` on that record, and returns `1 <= eax <= 2` (the `dec eax; cmp eax,1; setbe` form) - the 'state is 1 or 2' test

Interior anchor `00273754` (function `00273750`).

`003BBA60` (208 B) is the `002508AB`-gated pump `002507C0` invokes: with `01EFE31C` bit 1 set it sweeps 64 `0x50`-stride slots of `02B457D0`, `00505500`-testing each and zeroing the `{+0,+8}` pair on failure; then `01EFE320` is incremented by `0.656f` or decremented by `0.2f` depending on `01EFE31D` bit 1 and clamped to `[0, 1.0]` - the fade accumulator the frame gate wraps

Interior anchor `003BBA9E` (function `003BBA60`).

`002C0F30` (203 B) is the element rebuild `002BE300` runs: it packs `[+0x578]` and `(+0x57E >> 2) & 1` into the out pair, `00245000`s `rdx` with `0x2B8` and the `002C0870` nine-patch callback, `00246AC0`s, stores the product at `+0x570`, and under `+0x57E & 2` sets `[+0x570]+0x280 |= 0x20` with `+0x580`/`+0x57C` copied to `+0x298`/`+0x294` - then clears `+0x57E &= 0xFFFC`, leaving the element refreshed and the request bits consumed

Interior anchor `002C0F7D` (function `002C0F30`).

`003C5060` (192 B) is the position-history push `003C6000` runs when `0035D600` allows: it squares and sums `02B45810`/`02B45818` minus `02B45850`/`02B45858`, `00861F5C`-sqrts the 2D distance and skips when < 3.0f; otherwise the `02B45810` vec4 is written to `02B45860 + 02B45960*16`, count `02B45962` saturates at 16, and the cursor wraps mod 16 - a 16-entry breadcrumb ring

Interior anchor `003C50B9` (function `003C5060`).

`00360C70` (190 B) is the four-slot arm-and-spawn one gated lane runs at registration: it writes `+0 = 0`, `+3 = lane index` into four `0x18`-stride slots at `022CB9F0`, ~~takes registry handle `edi` from `0032E400(6, 9)`, clears `022CBA50`/`022CBA58`/`022CBA60`, and on a live handle enters the `0036C1D0(5, 5)` lock to `0036A190(edi)`-resolve the record and~~ takes `edi` = `0032E400(9, 6)` - `ecx` = 9 selects the group table `[022C51F0 + 9*8]` and `edx` = 6 the dword entry, a size (`MusicTrackState022CB9F0` `+0x60` per `51ad88762`), -1 for group 0xFF - clears `022CBA50`/`022CBA58`/`022CBA60`, and when that value is not negative (`js`) enters the `0036C1D0(5, 5)` lock to obtain a block from `0036A190(edi)` and *(corrected 2026-10-03, SWE2-EC7, record `swe2ec7-corr-00360c70-args-1003`: argument order and the 'handle' reading)* `0032E620`-spawn the lane with handler `00360B40` carried in the stack parameter block

Interior anchor `00360CA1` (function `00360C70`).

`00471230` (189 B) is the per-element offset accumulate `003E00C0` runs inside the publish: `[rdi+4]` chains `0020E600` -> `[rax]` into `003E5AD0(.., 0x104)` whose word result `rbx * 0x290` selects the transform row reached through `[rdi+8]`'s double resolve; the row's `+0x260` vec4 is staged into `022D91D0`, `[rdi+0x20]` into `022D9230`, then each `022D91D0` component is bumped by the `[rdi+0x20]` term (`addss` on the stored value plus `shufps 0x55`/`0xAA` extracts), and the updated vec4 is written back to `row+0x260` - the running per-element translation offset

Interior anchor `0047125D` (function `00471230`).

`00264510` (184 B) is the kind-dispatched vector fetch `002713E0` runs for the gated emit: `[rdx+0xC]` defaults to `1.0f`; a `+3` tag byte masked `0x60` `002E97B0`-resolves the source record and a live `[rax] != -1` tail-jumps `002E9CA0` to fill the out-vector; failing that, `[rdi+3] >> 5` selects the lane - tag 1 copies the `[[rdi+0xB8]+0x20]` twelve-byte vector, tag 3 the `[[rdi+0xB8]]` one, and every other tag zeroes the out-pair

Interior anchor `00264570` (function `00264510`).

`003F24D0` (167 B) is the reaper `0028E290` (FramePump) runs over the `+0x9B0`-linked node list: entries whose `+0x9C0` word reads 0 or 5 are unlinked from their `+0x9B0`/`+0x9B8` neighbours (advancing `rbx` past a dead head), zeroed on all three words, and handed to `0028FA50`; the possibly-advanced head returns

Interior anchor `003F2557` (function `003F24D0`).

`003F31B0` (164 B) is the list-teardown `0028E290` (FramePump) runs: it walks the `+0x70`-next chain calling `003F30D0` per node, and any node whose `+0x50` byte carries bit 1 is unlinked from its `+0x70`/`+0x78` neighbours (head-fix included), zeroed on both links, and handed to the `rbp` callback before the walk resumes

Interior anchor `003F31E7` (function `003F31B0`).

`003F8B40` (162 B) is the per-node refresh `0028E290` (FramePump) runs over the `[rcx]`-rooted `+0x28` chain: each node gets its `[+0x38]` vtable slot called with `edx` 2, then when `+0x26` bit 0 is clear `00272710` clears state and `00271960` recomputes `sx word[+0x14]` into `+0x50`; a set bit 0 fires the slot with `edx` 4, and every node ends with the slot called `edx` 3

Interior anchor `003F8B7E` (function `003F8B40`).

`0028DFD0` (159 B) is the timed-state commit `0028CA40` runs under the pump: `[rcx+0x20]` scales by `0x3FC90FDB` (pi/2), `+0x28` bit 1 clears, `00861F0E` supplies the trig lane and `00275490` builds the scratch from `rdi`/`rdi+0x10`; `ebx` lands at `+0x24`, `00202C90` dispatches, `003588B0([+0x24])` resolves for `002E7F70` when live, and `+0x20` zeroes on exit

Interior anchor `0028E009` (function `0028DFD0`).

`003F30D0` (219 B) is the timed-node refresh `003F31B0` runs: a live `[rcx+0x6C]` id is `002713E0`-checked (a dead one clears `[+0x50]` bit `0` and `[+0x6C]`), `[+0x50]` bit `1` arms once `[+0x4C]` drains to `0`, and `[+0x68]` accumulates `dt * 0.125`-scaled steps (`01DFE0BC` x `0x3E000000`) until the `0x3F7D70A4` wrap resets it to `0`

Interior anchor `003F30E0` (function `003F30D0`).

`00276000` (155 B) is the interval-list insert `00273A30` runs inside FramePump's subtree: it walks `r9 = [r9+0x10]` nodes until one covers `r8 = [r10+0x18] + arg + 0x20` in `[r9]..[r9+8]`, then splices `rax` in - `[rax]=rax+0x20`, `[rax+8]=arg`, `[rax+0x18]=r9`, `[rax+0x10]` takes the old next, the backlink fixes `[rcx+0x18]`, and `[r10+0x10]` records the new node - an ordered free-range allocator insert.

Interior anchor `00276062` (function `00276000`).

`0051A280` (154 B) is the three-row submit `003E00C0` runs: three times it `0020E600`s `dword[rbx+0x38]` into the table and calls `00519880` on `[rax] + idx*0x290 + 0x230` for `idx` = `[rbx+0xC0]`/`+0xC4`/`+0xC8`, passing `rbx`, `rbx+0x40`, `rbx+0x80` as the r8 lane - the triple 0x290-record fan-in the oscillator update consumes.

Interior anchor `0051A2B1` (function `0051A280`).

`003F7050` (154 B) is the kind-4 reaper `0028E290` (FramePump) runs: it walks the doubly-linked chain at `+0x300`/`+0x308` and for each node whose `word[+0x2F0] == 4` unlinks it (next/prev both patched, `rdi` advanced past the removal), clears the links and the kind word, then frees through `0028FA50` - returns the new head in `rdi`.

Interior anchor `003F70CA` (function `003F7050`).

`003E5510` (148 B) is the poke target `002E7F70` calls on a live record (this page's record-validator note): `[rcx+0x400]`'s node supplies the source at `(word[node+2] + node) + 0x120`; a null node or null computed source zeroes the out record `{dword, float, float}`; otherwise the 12-byte `{dword, f, f}` triple is copied into `rbx` and `[rbx+0xC]` gets `1.0f`; `003E5FA0(rcx, &tmp)` then `0046D0C0(rbx, &tmp, rbx)` finish the build - cookie-protected (`00808C40`).

Interior anchor `003E558C` (function `003E5510`).

`003F8140` (272 B) is a four-channel ramp the frame tick drives: `+0x100` progress advances by 1/6 per call (constant `0x3E2AAAAB` at `009159F4`) and clamps at 1.0f; then each of four s16 channel pairs - `+0xF8`/`+0xF0` to `+0xE8`, `+0xFA`/`+0xF2` to `+0xEA`, `+0xFC`/`+0xF4` to `+0xEC`, `+0xFE`/`+0xF6` to `+0xEE` - is written `cur + (target - cur) * progress` via `cvtdq2ps`/`mulss`/`cvttss2si`, the interp the gated tick applies.

Interior anchor `003F81CB` (function `003F8140`).

`002EB890` (147 B) is the sub-record refcount release the binding store's prose names: walk `0215FD58` then `0215FD78` for the `+0x14` id match, follow `word[+0x1E]` into the `0x120`-stride `02161DA0` sub-record (rejecting when `+0x5C` disagrees with the entry's `+0x24` stamp), `dec word[row + r8*2 + 0xE0]`, and when the count lands at or below zero the `+0x38|+0x3C` bit for slot `r8` is consulted and the word re-zeroed only if still live - the decrement half of the `002EB690`/`002EB890` pair the store records.

Interior anchor `002EB8FC` (function `002EB890`).

`002BEED0` (146 B) is the map-teardown reset `002BE050`/`002BE1A0` run: `word[+0x103E]` loses bits 0..1, `+0x1030` zeroes, `00290990`/`0035C070`/`0016D6A0`/`003C53E0` flush their lanes, `002BEA40` runs on the `+0xAC0` sub-object, and `00244F00` frees the `+0x1070`/`+0x1068` children before `+0x1050` clears - the `_8FA0`-band pane teardown the gate's rows list.

Interior anchor `002BEF27` (function `002BEED0`).

`00241BF0` (148 B) is the param-block widget spawn `0027AA70`/`00551E00`/`00551F00` call: it copies the caller's `0x28`-byte record (two `movups` + `movsd`) into a stack frame alongside a `{count, &copy, null, r8d}` request, lazily allocates `0x3D0` via `002497B0` when `rcx` is null, then calls `002465F0` - the widget constructor this page documents - with `edx = 0x3D0`, `r8 = 00241D40`, `r9` the request - a deferred create-message with a pre-seeded body.

Interior anchor `00241C73` (function `00241BF0`).

`002BEA40` (119 B) is the two-slot picker `002BE300`/`002BEED0` run over the `0x2B8`-stride pair on `rcx`: `+0x570` is cleared, then per record `00273A20` probes it - a 0 marks `rsi` as the chosen slot and skips further work, a nonzero with `byte[+0x280] & 1` clear gets released through `00244F00`; returns `rsi` (the first free 0x2B8 record, or the second's base) - the pick-then-release sweep the teardown family shares.

Interior anchor `002BEA80` (function `002BEA40`).

`002E6A80` (141 B) is the 32-bit flag sweeper on the update gate's list node: each set bit shared by the two masks calls `002E6E30` for that lane, the node is then unlinked from its doubly-linked list, and `002E9470` runs when ~~no flags remain~~ *(corrected 2026-10-01, OPUS, on ASTRA's lane-drain correction, re-read at the bytes: the loaded mask `+0x24` and the mask `+0x28` are both 0 (`002E6AED`/`002E6AF0`); the pending mask `+0x34` is not tested)* - the drain-and-detach pass the per-frame gate applies to spent entries.

Interior anchor `002E6AC1` (function `002E6A80`).

`0028E240` (67 B) is the global-gated refresh dispatch both gate arms (`002BE050`, `002BE1A0`) tail into: when manager `0209BE80` is live and bit `0x40` of its `+0x10F68` word is set, `0016D6A0` runs on the `+0x8FA0` child and the body tail-jumps `002BDC00` on that same field; gate closed returns immediately - the frame-gate's conditional broadcast leg.

Interior anchor `0028E262` (function `0028E240`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Forty-one functions this contract named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`pfgate_interior.py`](../_index/candidates/opus-pfgate-interior-1001/pfgate_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017F000` | 55 B | gets the object `001BC000` returns; when it is non-null, calls `001BB2B0(object, id, &out)` and returns `out`; otherwise returns 0 | `0017F021`, `0017F026` |
| `00271530` | 112 B | fills a ten-qword header at `rcx`: `+0` = (signed `edx` << 15) OR `0x1000000000000004`, then the constants `0xE`, `0x53001`, `0x47`, `0x44`, `0x42`, 1, `0x1A`, `0x54` (`0x5C` when `r8d` is 0) and 0; returns `rcx + 0x50` | `00271551`, `0027156C`, `00271593` |
| `002716C0` | 38 B | writes four dwords at `rcx`: 0, `0x13000000`, `0x10000000` and `0x50000000` OR ((`edx` - `rcx` - 0x10) >> 4), the 16-byte count of the span after the header | `002716CB`, `002716D5`, `002716E2` |
| `00272710` | 32 B | adds word `+0x16` to word `+0x14`; at or above `0x400` it clamps to `0x400` and returns 1, else returns 0 | `00272714`, `00272726`, `0027272A` |
| `00272F30` | 48 B | resolves `003588B0`; with no record it returns the float at `01CEBBA8`, else `002645D0(record)` scaled by the float at `00901B34` | `00272F3E`, `00272F4E`, `00272F53` |
| `002760A0` | 120 B | walks the list at `rdx` through `+0x18` for a block with room for `r8d + 0x20` bytes after its used span; carves a node there (`[node] = node + 0x20`, `+8` = size), links it after the block and stores it at `rcx+0x10`; returns the node, or 0 when none fits | `002760B9`, `002760E9`, `0027610D`, `00276115` |
| `00276120` | 110 B | when the head `[rcx]` lies above `[rcx+0x20]` and the gap holds `edx + 0x20` bytes, carves a node at `[rcx+0x20]` and makes it the new head (`[rcx]` and `+0x10`); returns it, else 0 | `0027615D`, `00276183`, `0027618B` |
| `002767C0` | 100 B | asks `002753F0(this, {0x2C, ...})` for key `0x2C`; returns the answer, or the signed word `+0x61B8` when the answer is 0 | `002767FD`, `0027680A` |
| `00289970` | 35 B | runs `0028A550`, then `0028A350`, then tail-calls `0028A620`, all on the same object | `00289981`, `0028998E` |
| `0028C850` | 31 B | counts the nodes of the chain linked through `+0xD70` | `0028C860`, `0028C867` |
| `0028C970` | 120 B | calls `0028D260(this, this, a2, a3, -1)`, then `0028D8A0` for the two 0x20-byte entries at `+0x30` and `+0x50` | `0028C99E`, `0028C9C7`, `0028C9CE` |
| `0028CA30` | 13 B | tail-calls `00861EC0(rcx, 0, 0x80)` | `0028CA32`, `0028CA38` |
| `0028E1D0` | 75 B | with the singleton `*(0209BE80)` present and its `+0x10F68` bit `0x40` clear, calls `002BDB60` on its `+0x8FA0` part, then tail-calls `002BDCA0(part, 1)` | `0028E1E0`, `0028E1F0`, `0028E211` |
| `00290B10` | 90 B | on the singleton `*(0209BE80)`: calls `0028C4F0` on `+0x10F00` when set; when the record at `+0x10EF0` has word `+0xD54` = 3, sets its `+0xD4C` bit 3; then clears `+0x10EF0` | `00290B30`, `00290B4B`, `00290B59` |
| `002964D0` | 101 B | runs `002962D0` and `0035BC40`; when `0035BB60()` is non-zero, makes a `0xB68`-byte object through `00244F50`, sets its `+0x40` bit `0x8000` when `002544B0()` is 1, starts it with `00246AC0` and returns it; else 0 | `002964E3`, `00296502`, `00296519`, `00296523` |
| `00296940` | 20 B | tail-calls `00245000(rcx, 0x720, 002985D0, 0)` | `00296943`, `0029694F` |
| `002BDCA0` | 49 B | when `+0x1080` and `+0x1058` are set, writes bit 0 of word `+0x40B6` of the `+0x1058` object as the inverse of `dx` bit 0 | `002BDCBE`, `002BDCC9` |
| `002BE090` | 16 B | sets `+0x10FA` bit 1 and stores `dx` in word `+0x10F8` | `002BE098` |
| `002BE230` | 51 B | with a child at `+0x1030`: sets its `+0x280` bit `0x20` and its word `+0x294` = `dx`; without one: sets `+0x103E` bit 1 and word `+0x103C` = `dx` | `002BE24B`, `002BE253`, `002BE25B` |
| `002BE270` | 26 B | stores `edx` in the `+0x1030` child's `+0x298`, or in `+0x1040` when there is no child | `002BE27C`, `002BE283` |
| `0031C200` | 73 B | when byte `02089340` bit `0x10` is set, resolves `003588B0` -> `00263E30` -> `+0x698` and returns that record's byte `+4` (unless `0xFF`); otherwise -1 | `0031C224`, `0031C230`, `0031C241` |
| `00377750` | 41 B | returns 1 when `00314AE0()` is 1, 0 when it is 2, otherwise calls `003148F0` and returns 1 | `0037775C`, `00377763`, `00377772` |
| `0037B2F0` | 50 B | when byte `02ADD932` is not 4, copies it to `02ADD930`, calls `0037B3D0`, and copies it to `02ADD931` | `0037B307`, `0037B30D`, `0037B312` |
| `003C5400` | 14 B | stores `edx` in the dword table at `02B45970`, index `ecx` | `003C5403`, `003C540A` |
| `003C8070` | 80 B | on the object `*(02B476B0)`: clears `+0x40` bit `0x10000`, sets it again (and clears dword `02B476E4`) when `002544B0()` is 1 or `02B476E4` is non-zero, then tail-calls `00244F00(object)` | `003C8082`, `003C809C`, `003C80B5` |
| `003F24A0` | 42 B | calls `003F1E90` on every node of the chain linked through `+0x9B0` | `003F24B3`, `003F24B8` |
| `003F6100` | 42 B | calls `003F5CB0` on every node of the chain linked through `+0x868` | `003F6113`, `003F6118` |
| `003F80D0` | 14 B | tail-jumps to `003F7E80` when `+0x984` bit 0 is set, else returns | `003F80D7`, `003F80DD` |
| `003F8EA0` | 31 B | clears qword `+0x52A0`, then tail-calls `00861EC0(rcx + 0x4020, 0, 0x1280)` | `003F8EAD`, `003F8EB4`, `003F8EBA` |
| `002E6E30` | 121 B | for slot `edx`: when the handle at `+0x60 + 4*slot` is non-zero, resolves it against `[022C6F28]+0x48830` (`0020E600`), unregisters it through `0041E490`, frees it through `00369800`, zeroes the slot and clears bit `slot` in `+0x24` and `+0x2C` | `002E6E6F`, `002E6E77`, `002E6E83`, `002E6E93` |
| `002EA6E0` | 157 B | when `+0x18` bit `0x04` is clear and `002ED950(+0x14)` finds an entry, takes a command record from `002F16B0`, copies `edx` dwords from `r8` into `+0x30`, and fills the record (`+4` = `0x30009`, `+0x10` = `002E60F0`, `+0x28` = this); returns 1, else 0 | `002EA6EF`, `002EA70B`, `002EA722`, `002EA73D`, `002EA744` |
| `0036F460` | 110 B | stores its float argument at `02AD9B50` (taking the difference from the previous value), steps the stored value down by a constant while it is at or above a limit, scales the difference by constants and hands it to `004678E0`, then tail-calls `00468520` | `0036F472`, `0036F490`, `0036F4B9`, `0036F4C0` |
| `003F00F0` | 124 B | fills a transform block: the two imported math functions `00861F08` / `00861F0E` of 0.0 go to `+0x60` / `+0x6C` and `+0x64` / negated `+0x68`, `+0xC` = 1.0, `+0x80` and `+0xF0` = 0, `+0xEC` = -1, and two 16-byte constants to `+0x70` and `+0x10` | `003F0101`, `003F012E`, `003F0133`, `003F0152` |
| `003F80E0` | 84 B | zeroes the four dwords at `+0x960`, then copies row `edx` of the 16-byte table at `00D11D80` into them; row 1 is skipped while dword `02092730` is 4 | `003F8103`, `003F8115`, `003F8121` |
| `003FA6E0` | 74 B | when argument 2 has `+0x272` bit 0 and is on this object's `+0x2490` chain (linked through `+0x278`), calls `00202C90(argument 3)` and returns 1; else 0 | `003FA700`, `003FA705`, `003FA71B` |
| `003FA730` | 48 B | the same membership test as `003FA6E0`; returns argument 2's dword `+0x260`, else 0 | `003FA745`, `003FA759` |
| `00356160` | 220 B | takes two floats from `00267DB0` and an id from `00267E10` (all on argument 4), builds a direction through `00203170`, `00202F00`, `00202E90` and `00202B70` with w = 1.0, passes it through `003A1890` and hands it with the id to `003DEA70` | `0035619E`, `003561CD`, `003561FD`, `00356211` |
| `003F7760` | 134 B | forms the vector from `+0x280` to `+0x290` (`00203080`), zeroes its w, passes it through `00202DE0` and `00270A10`, and updates `+0x2A0` from it with a constant through `00270CF0` | `003F778B`, `003F779D`, `003F77CE` |
| `003F7CC0` | 436 B | runs `003F2F20` on this and `+0xF0`; writes the `0x13000000` / `0x10000000` code words at `+0xE0`..`+0xEC` and `+0x1D0`..`+0x1DC`; copies `+0xB0`..`+0xBC` to `+0x2C0`..`+0x2CC`; sets the floats 0.21 at `+0x1A4`, 0.2 at `+0x1AC` and 127.0 at `+0x1B0`, `+0x1B4` and `+0x1B8` (a qword store, so `+0x1BC` = 0); derives `+0x2B0`..`+0x2BC` from the four floats at argument 2; then builds its records with `00271650` / `002716C0` (`+0x1E0`), `003F77F0`, and `00271530` (`+0x230`) / `002716C0` (`+0x220`) | `003F7CE7`, `003F7CEC`, `003F7D46`, `003F7D8E`, `003F7E36`, `003F7E51`, `003F7E6F` |
| `003FAAF0` | 102 B | when `00273A20(this)` is non-zero, stores `edx` in dwords `+0x28`..`+0x34` of parts 0, 1 and 2 (`[this+0x60][k]`) | `003FAB0B`, `003FAB31`, `003FAB37`, `003FAB43` |
| `00505500` | 94 B | in mode `+0x3C` = 2: counts `+0x44` down first (returning 0), then raises word `+0x38` by 6 until `0x80` and by word `+0x3A` after that, returning 1 once it passes `0x100`; in other modes adds `+0x3A` and returns 1 once it passes `0x25` | `0050550D`, `00505523`, `0050553D`, `0050554D` |

`003F5CB0` (1099 B) is one of the gated subsystems' scalar-field updater `003F6100` calls: it reads the object's `+0x820`/`+0x828`/`+0x830` timer triple, accumulates through `003F6370`, compares against 1.0, scales `01DFE0B4` by `0xF` iterations and the `008C5F6C`/`008F30F8`/`009002BC`/`009159F8`/`00901988` constants, clamps via `0028E9F0`, and finishes through `003F62D0` - the parameterized fade/speed curve one gate arm advances each tick.

Interior anchor `003F5F45` (function `003F5CB0`).

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 4)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `95d495604`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../_index/candidates/fable-home-host-moves-b4-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `0035D070` | 12 B | `003C6000` + 0x13 | loads the address `022C8060` into `rcx` and tail-jumps (site `0035D070` + 0x7) with the other incoming registers unchanged; it has no other work | Interior anchor `0035D077` | [CONTRACT-boot-fixups](../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-per-frame-update-gate-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0028E070` | 77 B | returns at once when qword `0209BE80` is null; otherwise ORs 0x40 into its dword `+0x10f68`, calls `002BDB60(qword 0209BE80 + 0x8fa0)`, reloads the qword and, when it is still non-null, tail-jumps to `002BDCA0(qword 0209BE80 + 0x8fa0, 0)`, else returns | Interior anchor `0028E07E`; Interior anchor `0028E080`; Interior anchor `0028E095`; Interior anchor `0028E0A4`; Interior anchor `0028E0B3` |
| `0028E0C0` | 80 B | returns at once when qword `0209BE80` is null; otherwise ANDs its dword `+0x10f68` with `0xffffffbf` (clearing bit 0x40), calls `002BDC00(qword 0209BE80 + 0x8fa0)`, reloads the qword and, when it is still non-null, tail-jumps to `002BDCA0(qword 0209BE80 + 0x8fa0, 1)`, else returns | Interior anchor `0028E0CE`; Interior anchor `0028E0D0`; Interior anchor `0028E0E5`; Interior anchor `0028E0F4`; Interior anchor `0028E106` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-contract-per-frame-update-gate-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001BC010` | 371 B | `0017F040` + 0x21 | finds the node whose dword `+0x20` equals `edx` (lower-bound walk from qword `rcx+0xc8`, header `rcx+0xb8`, following qword `+8` when the node's key is not below `edx` and qword `+0` otherwise, signed); when found it decrements dword `+0x48` of the node's qword `+0x28` and, when that reaches 0, calls slot `+0x10` of the vtable of the object at `rcx+0x1b8` with (`rcx+0x1b8`, `0x18`, 0), writes dwords `edx` and 4 at the returned block's `+0x10`/`+0x14` and links the block in last on the list headed at `rcx+0x1a8` (block `+0` = `rcx+0x1a8`, block `+8` = qword `rcx+0x1b0`, then that node's qword `+0` and qword `rcx+0x1b0` = the block); when `edx` is not negative it then does the same for the key `-2 - edx` | Interior anchor `001BC044`; Interior anchor `001BC074`; Interior anchor `001BC0A1`; Interior anchor `001BC0C7`; Interior anchor `001BC0EE` |
| `003F65C0` | 196 B | `003F62D0` + 0x1A | stores dword `0x10000000` at `rcx+0`, `+4` and `+8` and ((`edx`+5) << 0x10) OR `0x6c008000` at `+0xc`; qwords `0x1000000000000002`, `0xe`, `0x5b`, 0, `0x5c`, 0 at `+0x10` through `+0x38`, (`edx`*4+2, 32-bit) OR `0x3000000000008000` at `+0x40` and `0x412` at `+0x48`; the dword bit pattern `0x42fe0000` at `+0x50`, `+0x54` and `+0x58` and `edx` at `+0x5c`; then dwords `0x10000000`, `0x17000000`, `0x10000000`, `0x10000000` at `rcx` + (`edx`+6)*0x10, and returns (`edx`+7)*0x10 | Interior anchor `003F660C`; Interior anchor `003F6619`; Interior anchor `003F6651`; Interior anchor `003F6668`; Interior anchor `003F6680` |
| `003F6A10` | 288 B | `003F62D0` + 0x88 | with `n` = dword `rcx+0x5c` and `d` the fifth (stack) argument (float), takes `s0` = trunc((1.0 (`01CEBBA8`) - `xmm1`) * `n`), `s1` = trunc(`n` * `xmm2`), `s2` = trunc(`n` * `d`) and `v` = `xmm3` * 100.0 (`008F3134`) * `d`, and stores `xmm3` * 127.0 (`00906A44`) at floats `+0x50`, `+0x54` and `+0x58`; for each `i` below `n` it writes the float at `rcx` + `i`*0x10 + `0x6c`: 0 when `i` <= `s0`, else `v` when `i` <= `s1`, else `v` * (`D` - (`i` - `s1`)) / `D` with `D` = `s2` - `s1` when `i` <= `s2`, else 0 (all compares unsigned); then zeroes the dword at `rcx` + (`n`-1)*0x10 + `0x6c`, calls `003F6A10` + 0x109(the sixth (stack) argument, `rcx` + (`s0`+6)*0x10) and stores the bit pattern `0x3f800000` at dword `+0xc` of the sixth argument | Interior anchor `003F6A71`; Interior anchor `003F6AA6`; Interior anchor `003F6AD5`; Interior anchor `003F6B19`; Interior anchor `003F6B1E` |
