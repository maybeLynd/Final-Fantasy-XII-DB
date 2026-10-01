# S-21 runtime: per-invariant stub exposure for EXP-149, and one exposure that changes a result (OPUS, 2026-09-25)

**Row:** S-21 result application. The runtime cell is MIXED, pending the same per-invariant analysis as S-14
(`s14-runtime-per-invariant-exposure.md`). The contract is `07-Combat-Action/CONTRACT-apply-result-to-target.md`,
I1–I8 plus section 5. The executing record is **EXP-149**: the whole applier `003112F0`, with 54 scripted
boundaries at several depths. `s21-runtime-boundaries.md` already lists which of those run elsewhere. This note
scores nothing.

**Which text I1–I8 means here.** The wording is the SECTION-01 overlay, which is owner-merged in the worktree and
waiting for FRONTIER to publish it. The published `HEAD` contract uses different I-statements. Where they differ, the
table names the claim itself, not only its number.

## Method (bounds stated)

1. **Every direct call in the applier** (`003112F0..00311AE7`) is classified two ways:
   - scripted in EXP-149 or real;
   - whether the applier **reads the return value** before overwriting it.

   The scan (`s21_calls.py`, scratch) is linear and follows fall-through only. Hits on `nop dword ptr [rax]` are
   alignment padding, not reads.
2. **Scripted callees whose returns are unused can reach an invariant only through memory.** For these, the
   callee's own stores were read.
3. **Not done.** No analysis below `0030E360`. Its call-graph row in `Tools/work/graph/edges.tsv` lists hundreds of
   unrelated callees, which points to a bad function extent in that graph. No census built on it is reported.

### The applier's direct calls

| call site | callee | EXP-149 | return used by the applier |
|---|---|---|---|
| `00311321`, `0031132C` | `0031B860` (owner resolver) | scripted | yes: target owner `rsi`, source owner `r15` |
| `00311360` | `0030B9B0` (eligibility) | scripted | **yes: non-zero skips the whole apply** (`00311367 → 00311ACA`), unless caller-flags bit 0 |
| `0031137A` | `00385BA0` (metadata) | **scripted, no record runs it** | no, but it **writes memory**; see below |
| `003113A5` | `003A1180` | scripted | yes: `-1` skips `002DF220`; owner `+0xE9A` bit 2 is set either way |
| `003113BA` | `002DF220` | scripted | no |
| `003113DF`, `003113FD` | `0030C650` (level) | real | no |
| `00311457`, `003114A8` | `003008A0` (item write) | real | no |
| `00311475` | `00253770` (steal-slot tail) | scripted, no record | no |
| `0031153A`, `0031159F` | `0030E360` (status) | real | no |
| `003117CB`, `00311807` | `0030E130` (layers) | real | no |
| `00311668`, `003116A4`, `00311739`, `00311775` | indirect numeric setters | real (`00300520`/`530`/`C90`/`CE0`) | no |
| `003116E0` | `00300BC0` | real | no |
| `00311A8D` | `00253690` (gil read) | scripted | yes: new gil = `ret − d[rec+8]`, kept only if non-negative (`cmovns`) |
| `00311A9E` | `00254EE0` (gil write) | scripted | no |
| `00311AC5` | `0030FED0` (outer recompute) | real | tail |

## `00385BA0` changes one observable result

`00385BA0` (`BattleFormula_ApplyResultMetadata`) runs at `0031137A`, before every branch the invariants describe.
Its stores:
- **Battle-state block.** Record `+0x138` (byte) and `+0x13C` (dword), when not −1, go to `q[02EBF190]+0x5B0E` and
  `+0x5B00`.
- **`02EBF188`.** Receives the target's owner.
- **The availability byte.** For record bytes `+0x34`/`+0x33`/`+0x32` non-zero, `and byte [owner->spawn+0x14]` clears
  bits 2/1/0 (`00385BF0`–`00385C6B`). The only preconditions are a resolved owner and a non-null `+0x6A0`.
- **Post-result events.** When record `+0x1C == 1`, it calls `00469EC0` (the post-result events).

It **never writes the record, the source or the target stats**. So no numeric, status, copy-through, timer or
dirty-flag claim can be reached through it.

**The availability byte is the exception.** The applier's own steal loop (`00311420`–`0031148B`) clears bit *i*
(`btr` at `0031146C`) only when all three hold:
- the owner's stats kind is 1 (`00311417`);
- record byte `+0x32+i` is non-zero;
- the steal id `w[q[owner+0xE60]+0x32+2i]` is not `0xFFFF`.

The loop never *tests* the bit. `00385BA0` clears the same bit *i* **with no id test and no kind test**.

- **In a real run**, a slot whose record byte is set and whose steal id is `0xFFFF` **loses its availability bit**
  through the metadata step, although the applier does not steal from it.
- **With `00385BA0` scripted** (EXP-149), the bit survives.
- **EXP-149's `ap-steal` case** (`b32 = 1, b33 = 0, b34 = 1`; `stealtab = [0x3001, 0xFFFF, 0x4002]`; expects
  `b14 = 0x02`) gives the same answer both ways, because the empty slot's record byte is 0. The divergent case is
  not exercised.

The existing wording falls short in three places:
- **The published contract's I8** (`HEAD`) reads *"three consumable slots at `+0x32` (one bit each, cleared on
  use)"*. That is incomplete: an unused, empty slot is cleared too.
- **The SECTION-01 overlay's I8**, still unpublished in the worktree, reads *"availability clears at
  `unit->spawn + 0x14`"*. It describes only the applier's conditional clear.
- **The post-result page** says the bits are *"cleared twice"*. That treats the two clears as having the same
  condition, and they do not.

A contract wording for I8 is kept as a patch until FRONTIER publishes the contract's pending owner-merge:
`Tools/work/OPUS/pending_s21_i8_availability.patch`. The page wording is routed to FABLE.

## Per invariant

| inv. | can a scripted callee reach the claim? | owner reading |
|---|---|---|
| **all** | `0030B9B0` decides whether the apply runs at all (caller bit 0 bypasses it) | **selection exposed** (EXP-093 runs `0030B9B0`); every invariant describes the proceeding path |
| **I1** (two operations on 32 statuses; `+0x54` mode 3, `+0x58` mode 0) | the dispatch and arguments are the applier's own; the six-mode mapping is inside `0030E360`, which runs real | **dispatch not reachable**; the mapping is E360's body, and its callee gates apply as the contract says (not analysed below E360, see Method) |
| **I2** (parameter forwarding and copy-through) | the copies (`003115B6`–`00311606`) are applier stores after the real E360 calls; no scripted callee writes the target stats | **not reachable** |
| **I3** (the dirty flag follows branch dispatch; the tail condition) | set without testing any return; the tail test is body-local | **not reachable** |
| **I4** (branches that do not set the flag) | body-local control flow | **not reachable** |
| **I5**, **I6**, **I7** (presence bits, absolute/delta selection, flag translation) | arithmetic on `d[rec+0x2C]`, which no scripted callee writes (`00385BA0` only reads the record) | **not reachable** |
| **I8** (foe paths; steal and effect bytes) | the owner comes from scripted `0031B860` (a value; EXP-090/093/153/… run it). The effect bytes `+0x78..+0x7B` are applier stores. **Steal availability is also cleared by scripted, never-executed `00385BA0`, under a wider condition.** | **exposed, with a concrete divergence** (above) |
| **section 5** (owner `+0xE9A` bits 3 and 2, and the tail clear) | bit 3: body-local; bit 2: set whether or not `003A1180` returns −1 | **not reachable** |
| gil (section 3, "zero suppresses gil adjustment") | the zero test is body-local; the **value** is scripted `00253690`'s | **value exposed** (EXP-092 runs `00253690`/`00254EE0`) |

## For the scorer

- Most I1–I8 claims are out of the scripted callees' reach.
- **I8 is the exception, and it matters.** The scripted, never-executed `00385BA0` changes the availability byte
  in a case EXP-149 does not exercise.
- **What would close it:**
  1. EXP-149's harness with `00385BA0` real;
  2. one case with a set record byte on an empty (`0xFFFF`) steal slot.

  Both are ORACLE work in the existing harness. The request is routed. `00385BA0` is 250 bytes. Its only calls are
  `0031B860` (already executed elsewhere) and `00469EC0`, which is skipped when record `+0x1C != 1`.
