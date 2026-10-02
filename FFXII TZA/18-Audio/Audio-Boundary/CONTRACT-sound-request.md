---
contract: Turn a small sound number into a playing voice
category: 18-Audio
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: how-a-sound-request-becomes-a-voice.md
entries: ["00249C60", "00249CA0", "0024A1A0", "00271500", "00357040",
          "003A1070", "003A1100", "003A1180", "003A11F0",
          "002DF220", "001DBDB0", "00210C00", "00249FC0", "00512080"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 130 addresses cited - 10 data, 59 entry, 61 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-sound-request-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — turn a small sound number into a playing voice

> **Authored 2026-09-12 by OPUS.** The mechanism is FABLE's, on
> [how a sound request becomes a voice](how-a-sound-request-becomes-a-voice.md), which carries a
> falsification pass.
>
> **This contract is wider than that page, because checking it made the path wider.** The page
> describes two convenience wrappers. Following `audit_crossrefs.py`'s boundary report found **six
> more call sites that inline those wrappers and one script verb that does not**, and with them two
> corrections that matter: **there are three bank handles, not two**, and **the "always full
> loudness, dead ahead" property belongs to the wrappers and not to the path.** Everything marked
> *re-read* or *verified by me* in §15 was derived from the shipped image for this contract.

## 1. Purpose

Almost every sound in FFXII that is not music starts here. Moving the cursor in the Battle Menu,
landing a hit, opening a chest: some piece of game logic asks for a sound by a small number — the
ones in the shipped code run from about 10 to 108 — and this path turns it into a voice. **`00249C60`
is the most-called audio entry point in the game, with 100 distinct non-Audio callers and none
inside Audio.**

The number is not absolute. **It is a slot inside whichever sound-effect bank is loaded now**, which
is why the same request makes a different noise in a different area, and why an area that failed to
load its bank is silent rather than wrong.

## 2. Interface

The path is **resolve, then play**. Every caller does both; what differs is whether it goes through
a wrapper, and what it passes.

**The wrapper family — four functions, and they are not interchangeable:**

| wrapper | size | resolver | reads the global gate? |
|---|---:|---|---|
| `00249C60` | 51 | `003A1180` | **yes**, `00249C64` |
| `00249CA0` | 51 | `003A11F0` | **yes**, `00249CA4` |
| `00271500` | 42 | `003A1180` | **NO** |
| `0024A1A0` | 46 | *none* — takes a raw id | **yes**, `0024A1A6`; not a resolve-and-play site at all (§14 `SR-1`) |

**`00271500` is the shape of `00249C60` with the gate check deleted.** It is the cheapest thing in
the game to mistake for `00249C60`, and it cannot be silenced (§8).

| | |
|---|---|
| **signature** | **`int32_t PlaySound(int32_t localIndex)` — one argument, and it is not nullary.** `ecx` is never written before the `call`, so the caller's first argument passes straight through into the resolver. A decompiler that shows no parameter is wrong about this |
| return | the play call's result, by **tail call** — so a wrapper's result *is* `002DF220`'s — or `-1` (`or eax, -1`) on its own refusals |
| the pair the wrappers always pass | `edx = 0x40`, `r8d = 0x7F` — built as `lea r8d, [rdx + 0x3F]`, a peephole, **so the two constants are related by the compiler and not by meaning** |

**Six more functions inline the wrapper instead of calling it** — each calling a resolver and then
`002DF220` directly. **Five of the six reproduce the `mov edx,0x40 / lea r8d,[rdx+0x3f]` peephole
exactly**; the sixth is the verb below. **None of the six reads the global gate.**

**And it matters which six they are.** They were listed as bare addresses until the cross-reference
audit pointed out that this document cites them and never says what subsystem they belong to
(2026-09-12) — so a reader could not tell that two of the sounds no gate can silence are among the
most conspicuous in the game:

| address | name | subsystem | what it is |
|---|---|---|---|
| `0030C650` | `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` | Rewards | **the level-up** |
| `003112F0` | `BattleFormula_ApplyTargetResult` | CombatFormula | **applying a hit's result to its target** |
| `00357040` | *(uncensused by name)* | Script VM bridge | the `sebsoundplay_2c1` handler, described below |
| `0046CC70` | *(uncensused by name)* | Presentation | — |
| `00366870`, `003E8690` | *(uncensused by name)* | **no primary owner in the ledger** | — |

> **This does not establish that a level-up or a hit is unsilenceable in play**, only that the code
> emitting those sounds does not read the gate. What the gate actually governs at runtime is
> `SR-2`, and it is still open.

**The script entry is not a wrapper.** Verb `sebsoundplay_2c1` (call_id `0x02C1`, arity 4, handler
`00357040`) pops four ints and passes **caller-chosen** bank class, pan and volume:

```c
sebsoundplay_2c1(int bankClass, int localIndex, int pan, int volume)
```

## 3. Types and state

| location | width | meaning |
|---|---|---|
| `0x02091098` | 4 | **the global audio gate.** Non-zero abandons the request before any lookup. **Four references image-wide: three reads — `00249C64`, `00249CA4`, `0024A1A6` — and exactly one write, `00249FC0`** (§8) |
| `0x022CB726` | 1 | the **second, independent** gate, read by `003603C0` inside the play call |
| `0x02AEF3FC` | 4 | **bank handle A** — the one both documented wrappers use |
| `0x02AEF400` | 4 | **bank handle B** |
| `0x02AEF404` | 4 | **bank handle C** |
| `0x02AEEDC0` | 24 x **64** | the **slot table** every resolver validates its handle against, at `+8` and `+0x0A`. **Exactly 64 entries** — see below |
| `0x02AEF3C0` | 2 | the slot list's **head index**, and the first thing after the table |
| `0x02098E20` | `0x288`/slot | the ActorManager slot array whose liveness `00267330` reads |
| voice `+0x1C` | 4 | **volume**, reset to `0x7F` |
| voice `+0x20` | 4 | **pan**, reset to `0x40` |

**The three handles are consecutive dwords — one small array of bank slots**, each set by its own
83-byte setter (`003A1390`, `003A1330`, `003A12D0`) and ~~all three reset to `-1` by the 582-byte
teardown `003A13F0`~~ *(corrected 2026-10-01, OPUS: `003A13F0` is the 582-byte boot bank setup, called only from `00266D10`; after its requests it writes -1 to A at `003A14BE` and `003A153D` and to C at `003A15BC`, and never writes B - §14 `SR-2`, §15)*.

### The table is 64 entries, and that bounds the whole id space

The resolvers never bound the slot — they index `base + slot*24` with a 16-bit value and trust the
equality test. **`003A0C90` gives the real size.** It walks the same table with the same stride-24
addressing, starts its search index at `0x40`, treats `0x40` as *none*, and follows a **signed
16-bit link at entry `+0`**, stopping on a negative:

```asm
003A0CA0  movsx r8d, word ptr [→02AEF3C0]      ; the list head
003A0CB1  mov   r9d, 0x40                      ; "none"
003A0CC0  movsxd rax, r8d
003A0CC3  lea   rdx, [rax + rax*2]             ; x3
003A0CC7  cmp   esi, dword ptr [→02AEEDC4]     ; [base + slot*24 + 4]
003A0CD4  movsx r8d, word ptr [→02AEEDC0]      ; [base + slot*24 + 0] = the NEXT link
003A0CE0  jns   0x3a0cc0                       ; negative terminates
```

and the arithmetic closes exactly:

> **`0x02AEEDC0 + 64 * 24 = 0x02AEF3C0`** — the byte after the last entry is the list head itself.

So **the slot is 0..63**, and therefore:

| | |
|---|---|
| the id space | `64 * 512 = 32768` — **exactly fifteen bits** |
| why `002DF220` clears bit 31 | a 15-bit id leaves the top bits free, and bit 31 is used as a flag rather than magnitude |
| the entry's low word | equals the slot, so it is **always below 256** — its second byte is structurally zero |

**That last row is not a curiosity.** It is why a reimplementation can get the entry read wrong —
reading one byte instead of two, or shifting the wrong way — and never be caught by any test that
uses a real slot value. The pilot's §13 records it as an adjudicated equivalence rather than
pretending the cases cover it.

**The audio singleton is a registry of five controllers, one per bank class** — `MusicAudioController`,
`SebAudioController`, `SepAudioController`, `StreamAudioController`, `ShoutAudioController`, each
with real RTTI and its own pool constant. **Music is unreachable from this path**, which is why it
keeps playing through things that silence effects.

### The five resolvers

All five share one table and one arithmetic; they differ in **which handle** and **which guards**.

| resolver | size | handle | requires `*(0x02AEF400) != -1` | liveness `00267330(0)` |
|---|---:|---|:--:|:--:|
| `003A1070` | 118 | **C** `0x02AEF404` | **yes** | yes |
| `003A1100` | 118 | **B** `0x02AEF400` | yes (it *is* the handle) | yes |
| `003A1180` | 111 | **A** `0x02AEF3FC` | no | **yes** |
| `003A11F0` | 79 | **A** `0x02AEF3FC` | no | **NO** |
| `003A1240` | 66 | **the argument** — no global handle | no | no |

> **`003A1240` is the one this contract missed until 2026-09-12**, and the reason is instructive:
> every other resolver names one of the three handle globals, so a census anchored on those globals
> finds exactly four. `003A1240` takes the handle in `ecx`. Its body is the arithmetic verbatim —
> `movzx r8d, cx` / `lea rax, [r8+r8*2]` / `lea r8, [rip → 02AEEDC0]` / `movzx r9d, word [r8+rax*8+8]`
> / `or` with `+0xa` / `cmp` against the argument with bit 31 cleared / `shl r9d, 9` / `lea eax,
> [rdx+r9]` — and it carries the same provably dead sign test. **It is not covered by the suite**
> (§13 runs six bodies and this is not one of them); that gap is stated rather than papered over.

> **`003A1070` guards on a handle it does not use.** It refuses unless handle **B** is valid, then
> reads handle **C**. That is a real dependency between two bank slots, not a typo in this table —
> both addresses were confirmed by a controlled scan (§15). Why, is `SR-2`.

## 4. Preconditions · postconditions · invariants

**Preconditions.** None checked on the argument. The banks may or may not be loaded; that is one of
the refusals rather than a precondition.

**Postconditions on success.** ~~A voice is acquired with the requested pan and volume~~ — the
request is issued carrying pan and volume — `0x40` and `0x7F` from any wrapper, **its own reset
values, passed back in explicitly** — and a receipt is returned.

> **CORRECTED 2026-09-21 (OPUS), on `ASTRA-RETURN-OPUS-AUDIO-REQUEST-VOICE-BOUNDARY`, and the
> contract caught itself.** The sentence above said *a voice is acquired*. **This contract's own
> limits deny that**: §12 states that nothing here touches the five controllers, the bank managers,
> **the voice**, or whether a sound is heard, and invariant 1 immediately below says a receipt does
> not mean a sound is playing. A postcondition asserting voice ACQUISITION from a request path that
> the same document says never reaches the voice is the exact promotion ASTRA's return warns
> against — request arguments read as native audio behaviour — and it was mine.
>
> **What IS established, and it is a positional claim rather than an audible one.** ASTRA's package
> pins the request flow end to end on the reference executable: `003515B0` pushes 64 and 127;
> `00351020` adapts to speaker, cue, 64, 127 and a flag; `003581B0` sends `R8D=64`/`R9D=127` through
> `003E9BF0` to `003E9C10`, which stores **pan at `+0x0F`** and **volume in bits 24–30 of `+0x08`**;
> and the pump `003E9780` **preserves those positions**. So the request's fields, their widths, their
> bit positions and their survival across the pump are all established — which is what L1/L2 asks of
> this boundary.
>
> **WHICH NATIVE CLAIM REMAINS REQUIRED, since the return asks precisely that.** Not an audible one.
> L1/L2 needs types, extents, field representation, ownership and stated contract behaviour, and the
> positional chain above supplies all of it for the request record. **The outstanding claim is that
> a voice object is initialised from these fields** — that some native voice exists whose pan and
> volume derive from `+0x0F` and `+0x08` bits 24–30 — and that is a claim about a downstream object
> this contract never reaches. It is a RUNTIME-row obligation for this contract, not an open L2
> types obligation, and it is **live-only**: no return code, request constant or queue byte can
> settle it, and EXP-096 stops at scripted dispatch.
>
> **Not inferred here and not to be inferred later:** audible loudness, centering, or that any voice
> is live. `0x7F` being full scale in a 0–127 field is a statement about the FIELD, not about what
> a listener hears.
>
> ### And here is WHY a sampled pan cannot give you a side — added 2026-09-22 (FABLE) on `OPUS-REQ-FABLE-SOUND-CONTRACT-LACKS-THE-STEREO-DISCRIMINATOR`
>
> The refusal above was general. **The mechanism that makes it structural rather than cautious is
> measured**, and this contract should carry it, because *a refusal a reimplementer cannot check is a
> rule they obey without understanding.*
>
> **The mixer treats each SOURCE CHANNEL separately.** At `spread` 0, the two source channels of
> **one** stereo voice favour **opposite outputs** from **identical** `pan` and `frpan`:
>
> | controlled input | output 0 | output 1 |
> |---|---:|---:|
> | stereo 240, spread 0, **source 0** | 0.565731704 | 0.824589252 |
> | stereo 240, spread 0, **source 1** | 0.824589312 | 0.565731645 |
> | stereo 240, spread 1, either source | 0.183039829 | 0.983105421 |
>
> **So a sampled `pan`/`frpan` target alone cannot establish which side a stereo voice is heard on —
> by construction, not by caution.** One pan value does not name one direction; it names a pair of
> opposed directions whose assignment depends on the source channel index.
>
> **And `spread` narrows rather than widens.** For two source channels and two outputs the pre-wrap
> offsets are `1.5` and `0.5` — equivalently `−0.5` and `+0.5` — and `007B86BD`–`007B86E6` applies
> `s <= 0` leaves `o`; `s > 0 and o > 1` gives `o + (o−1)·s`; `s > 0 and o < 1` gives `o − o·s`;
> `o == 1` unchanged. **Spread `1` collapses both offsets to the same direction** modulo the pan
> coordinate's period of 2 — *the opposite of what the name suggests*, and the row above shows both
> sources landing on the mono result.
>
> **Evidence class, kept distinct:** this is **isolated original machine code**, not live and not
> static inference. `007B8430` was run in isolation on the original bytes with the original cosine
> `007B8BA0` and sine `007B8C80` and **no stubs**, canaries around the output and the real
> security-cookie check on every accepted row. **The control is sensitive to the defect**: NOP-ing the
> negative-`frpan` half-turn at `007B8769` flips byte 240 to output-0 dominance, so a front/back-mirror
> reading would have been caught.
>
> **What this still does NOT license.** Applying identical signals to both rows gives about `1.390321`
> in each output, and that is **a linear calculation from coefficients, not rendered audio** — real
> sample content, phase, levels and later processing decide what is audible. **Numeric output 1 is not
> identified as the physical right speaker.** `−1` and `2` are controlled boundary inputs, not evidence
> that any caller supplies them; the ordinary initialised value and the permissible caller range stay
> open.
>
> *The convention this sets, since it was asked for:* **a contract states a refusal together with the
> mechanism that makes it falsifiable.** A contract may carry less detail than its page, but a refusal
> is exactly the place it must not — the reader of a contract is the person about to build the thing,
> and "do not infer X" without "because Y" is a rule that survives until the first person who thinks
> they have a reason.

**Invariants.**

1. **A receipt does not mean a sound is playing.** One is issued even when no bank matched and
   nothing was started. This is the trap to know before debugging anything here.
2. **Several independent things can refuse, and not one tells the caller which** (§10). All of them
   report only failure, and they do not agree on what failure looks like.
3. **Every request through a *wrapper* is full loudness, dead ahead — but the path is not so
   limited.** *This is the correction that checking the contract produced.* The earlier reading —
   that a mod wanting a positional or quieter sound must reach past these wrappers — is right about
   the wrappers and **wrong about the path**: `sebsoundplay_2c1` already passes script-chosen pan
   and volume, so the mechanism exists in shipped code and is reachable from authored data.
   **The right place to reach is the verb, not a patched constant.**
4. **A bank owns a 512-entry block of the global id space**, so the argument is small by construction.
5. **The gate protects three functions, not the path** (§8).

## 5. Relationships

`00249C60` → `003A1180` (resolve) → tail-jump `002DF220` (play) → `001DBDB0` (dispatch) → `00210C00`
(the Seb/Sep fork). `00249CA0` is the same with `003A11F0`; `00271500` the same with `003A1180` and
no gate. `00357040` selects among `003A1070` / `003A1100` / `003A1180` from its first argument.
`00267330` supplies the liveness precondition; `003603C0` the second gate.

**The fork is a two-way branch on the selector, and the request path pins it.** `00210C00` sends
selector 0 to `this[+8]` and anything else to `this[+0x10]`, and `002DF220` hardcodes the selector
with `xor ecx, ecx`. **So every request through this family reaches the same sub-controller, and
the other is unreachable from here** — whatever else `00210C50` and its siblings can select.

## 5a. Who crosses this boundary — counted, 2026-09-12

**An audio boundary is called from everywhere, and "everywhere" is a claim like any other.** Counted
over `edges.tsv` for the four wrappers, the four resolvers and the play call:

| subsystem | call sites | distinct callers |
|---|---:|---:|
| **no primary owner in the ledger** | 78 | 70 |
| UI | 30 | 30 |
| Audio (the family's own internals) | 9 | 6 |
| Script VM bridge | 5 | 2 |
| Save / Load / Settings | 4 | 3 |
| Presentation | 3 | 1 |
| CombatFormula | 2 | 1 |
| Rewards | 2 | 1 |
| **total** | **133** | |

`00249C60` alone carries **99 of the 133**, which is what makes it the wrapper worth getting right:
every other entry point is a rounding error beside it. `003A1180` is the widest-spread of the
resolvers, reached from six subsystems.

> **The largest group has no owner**, and that is a fact about the ledger rather than about the
> audio boundary — 70 of the 133 callers are functions the census has not assigned to a subsystem.
> A caller census that reported "eight subsystems" and omitted that would be reporting its own
> coverage as a finding about the engine.

**Seven cross-subsystem edges remain unaccounted after this, and they are dispositioned rather than
absorbed.** They are of two shapes, and neither belongs to this contract:

| shape | example | why it is not this document's |
|---|---|---|
| an **inliner's own** other callees | `0030C650` → `0020E600`; `003112F0` → `003008A0`; `0030C650` → `0030FED0` | this contract cites those functions *only* as things that inline the wrapper. What the level-up also does with a pointer resolver, an inventory call and a status call is the **Rewards and CombatFormula documents' business**, and claiming it here would be this document annexing two subsystems it has not read |
| other callers of the **per-unit mute predicate** | `00267310` ← Movement `002E45E0`, `002E5750`; `00267330` ← Party `00358CB0`, `00359150` | `00267310`/`00267330` are cited here for the one thing §10 row 6 uses them for. That movement and party code asks the same question of a unit is real and is **not an audio fact** |

> **A disposition is not a dismissal.** Each of the seven was looked at and assigned to the document
> that owns it; none was waived, and if any of those documents turns out not to mention its own
> edge, that is a finding **there**. What this contract may not do is claim the neighbour by writing
> a sentence about it.

## 6. State transitions

The request is stateless; what changes is the voice. `002256B0` resets a fresh voice to
`+0x1C = 0x7F`, `+0x20 = 0x40`, and `00224570` then calls `002256F0(voice, pan, 0)` and
`002257E0(voice, volume, 0)` on it. The handles change only through the three setters and the
teardown named in §3.

## 7. The two settings are not the same kind of value, and three things prove it

**Re-derived 2026-09-12** from `002DF220`:

```asm
002DF256  and   edi, 0x7f        ; p3 -> SEVEN bits  (0..127)
002DF259  movzx r8d, sil         ; p2 -> EIGHT bits  (0..255)
002DF25D  btr   ebx, 0x1f        ; the id's bit 31 cleared
002DF261  mov   r9d, edi         ; p3 becomes arg 4
002DF264  mov   edx, ebx         ; the id becomes arg 2
002DF266  xor   ecx, ecx         ; selector = 0, hardcoded
```

**First, the masks.** `p3` is masked to seven bits **twice**, and the second time is
`00210C0C`, re-read for this contract:

```asm
00210C03  movzx r8d, r9b                   ; the pan truncated to a byte AGAIN
00210C07  mov   r9d, dword ptr [rsp + 0x28]
00210C0C  and   r9d, 0x7f                  ; the volume masked to SEVEN BITS again
00210C10  test  edx, edx                   ; the SELECTOR
00210C16  mov   rcx, qword ptr [rcx + 8]   ; 0 -> this[+8]  -> 0021B5B0
00210C1F  mov   rcx, qword ptr [rcx + 0x10]; else -> this[+0x10] -> 00219EA0
```

`p2` is truncated to a byte at both stages and **never masked to seven bits anywhere on the path**.
A field deliberately allowed the full 0–255 range is not a companion to a 0–127 one, and that
asymmetry is visible before any name is attached to either — and it is not an accident of one
function, because two functions in sequence make the same distinction.

**Second, the voice.** `p2` is pan and `p3` is volume. Volume `0x7F` is full scale in a 0–127 field.
Pan `0x40` is the centre of a **0–255** field — the setter branches at `0x80`, mapping `0x00..0x7F`
to one axis and `0x80..0xFF` to the mirrored one, so 64 lands on offset zero, dead ahead.

**Third — and this one is independent of both — the script verb agrees.** `sebsoundplay_2c1` pops
four ints and lands its 3rd and 4th arguments in `edx` and `r8d`, **exactly the slots the wrappers
fill with `0x40` and `0x7F`**:

```asm
0035706A  call 0x267e10 / mov r15d, eax   ; pop 1 = arg4
00357075  call 0x267e10 / mov r12d, eax   ; pop 2 = arg3
00357080  call 0x267e10 / mov edi,  eax   ; pop 3 = arg2
0035708C  call 0x267e10                   ; pop 4 = arg1 -> the resolver selector
003570C0  mov  r8d, r15d                  ; arg4 -> p3 = VOLUME
003570C3  mov  edx, r12d                  ; arg3 -> p2 = PAN
003570C6  mov  ecx, ebx                   ; the resolved id
003570C8  call 0x2df220
```

The VM stack is a true LIFO and **"arguments arrive in reverse order" is already established tier 1**
in [the calling convention](../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md),
so pop *n* is argument *5−n*. **A script author choosing a pan and a volume, and an engine wrapper
hardcoding a centre and a full scale, agree on which slot is which.**

## 8. Script · resource · event interactions — and the limit of silencing

**The census is the source page's, and it is right.** Its §10 records one write (`00249FC0`) and
three reads (`00249C60`, `00249CA0`, `0024A1A0`) from its own xref dump. **Re-run independently for
this contract with a passing control, `data_xref_scan.py` found exactly those four and no others** —
so this is corroboration, not a correction.

```asm
00249FC0  mov  dword ptr [rip + 0x1e470d2], ecx    ; *(0x02091098) = arg
00249FC6  ret                                      ; the whole function: 7 bytes
```

**Its script-side caller is a verb**, and the verb table names it: **`fsmenu_sedisable`, call_id
`7013`, family 7, arity 1, guard `fsmenu`** — handler `00512080`.

```asm
00512080  call 0x280120 / test eax,eax / jne ...   ; the fsmenu guard: non-zero, do nothing
00512095  call 0x267e10                            ; pop the script's one int argument
0051209A  mov  ecx, eax
005120A1  jmp  0x249fc0                            ; TAIL JUMP: the script's value IS the gate
```

So **the script's argument lands in the gate unfiltered — no clamp, no boolean normalisation** —
and since §10 row 1 refuses on *non-zero*, any non-zero value silences the three functions that read
the gate. The verb's own name is independent corroboration of what the gate means: `sedisable` is
sound-effect disable.

> **The census is right and one inference from it is not.** The source page reads three readers as
> the path — *"Silence everything the game requests: write non-zero to `02091098`"* — and that does
> not follow. `00271500`, the six inlined call sites and `sebsoundplay_2c1` never read the gate at
> all, and the same controlled scan establishes their absence, because it found all four references
> with a passing control.
>
> **So `sedisable` disables three functions, not sound effects.** A sound still playing after it is
> not a bug in the gate; it is a call site that was never behind it. That is the single most useful
> fact in this document for anyone modding audio — and it is a conclusion the page's own census
> supports once the path is drawn wider than two wrappers.

The setter's other two callers are `0027F5D0` (a UI request-router entry) and `002D6F90`, so the
gate is not script-exclusive — **a script can silence those three functions, but a script is not the
only thing that does** (`SR-4`).

The banks themselves are authored resources; which one is loaded decides what a given number means.

## 9. Determinism

No RNG on this path — `Sd::Driver::RandomSound` is a different entry. Ordering matters only through
the liveness precondition, which ties the gated wrappers to whether the world runtime is running.

## 10. Failure paths and edge conditions

| # | condition | who checks it | result | reported as |
|---:|---|---|---|---|
| 1 | `*(0x02091098)` non-zero | **only** `00249C60`, `00249CA0`, `0024A1A0` | abandoned **before the lookup** | `-1` |
| 2 | the handle is `0xFFFFFFFF`, or the entry's dword ≠ the key | every resolver | no play call | `-1` |
| 3 | `00267330(0)` non-zero — **the world runtime is down or held** | `003A1070`, `003A1100`, `003A1180`; **`003A11F0` does not check this at all**, and that is the entire difference between `00249C60` and `00249CA0` | refuses before the lookup | `-1` |
| 4 | `*(0x02AEF400) == -1` — bank slot B not loaded | `003A1070`, `003A1100` only | refuses **even for handle C** | `-1` |
| | **Row 4 fires only after B's load callback has run and stored `-1`.** One store to that cell exists in the image, `003A1344`, swept in both addressing forms with a passing control (2026-09-18, OPUS); the cell begins at its `.bss` zero and no setup path gives it `-1`, unlike its two siblings. Until that callback runs the row cannot fire, and `003A1100` then **succeeds** rather than refusing — see `SR-2`. | | | |
| 5 | `003603C0` non-zero — the second, independent gate | `002DF220` | returns before dispatch | `0`, **not `-1`** |
| 6 | `00267310(unit+0x15)` non-zero | `sebsoundplay_2c1` only | skips the play call | `0` |
| 7 | no loaded bank owns that id | — | survives every gate and nothing starts | **a receipt is still issued** |
| 8 | `id == -1` reaching `002DF220` | `002DF220` | `cmp ecx, -1` → return | `0` |

> **Eight conditions, two return values, and one of them is success.** A caller cannot distinguish
> any of them, and the one case that most looks like success — a receipt with nothing playing — is
> the one the engine reports most positively.

**A provably dead branch, in all five resolvers** (`003A1240` included, §15a): after `movzx edx, word ptr [...]` the code runs
`test edx, edx / js refuse`. A zero-extended 16-bit value can never be negative. Defensive code that
never fires — worth knowing before anyone reimplements it as a real bound.

## 11. Observable behaviour

A sound, or silence. In memory: the voice's `+0x1C` and `+0x20`, the two gates, and the three bank
handles. The receipt the caller gets back — which §4 says is not evidence of playback.

## 12. Reproduction formula

```c
int32_t PlaySound(int32_t localIndex)                 /* 00249C60 */
{
    if (*(int32_t *)0x02091098 != 0) return -1;       /* gate 1 -- 00271500 OMITS THIS LINE */
    int32_t id = Resolve_A(localIndex);               /* 003A1180, ecx passes through */
    if (id == -1) return -1;
    return Play(id, /*pan*/ 0x40, /*volume*/ 0x7F);   /* TAIL CALL: its result is ours */
}

/* One body, four instantiations. handle/guard/liveness per the section 3 table:
 *   003A1070: handle C 0x02AEF404, guardB yes, liveness yes
 *   003A1100: handle B 0x02AEF400, guardB yes, liveness yes
 *   003A1180: handle A 0x02AEF3FC, guardB no,  liveness yes
 *   003A11F0: handle A 0x02AEF3FC, guardB no,  liveness NO     */
int32_t Resolve(int32_t localIndex)
{
    if (guardB && *(int32_t *)0x02AEF400 == -1) return -1;
    if (liveness && ActorSlotHeldOrDown(0))     return -1;      /* 00267330(0) */
    uint32_t handle = *(uint32_t *)HANDLE;
    if (handle == 0xFFFFFFFF) return -1;
    uint32_t slot = handle & 0xFFFF;
    uint32_t key  = handle & 0x7FFFFFFF;                        /* btr r8d, 31 */
    uint8_t *e    = (uint8_t *)0x02AEEDC0 + slot * 24;          /* lea + [rcx+rax*8+8] */
    uint32_t low  = *(uint16_t *)(e + 8);
    uint32_t high = *(uint16_t *)(e + 10);
    if (((high << 16) | low) != key) return -1;
    /* (int32_t)low < 0 is tested here and is unreachable: low was zero-extended from 16 bits. */
    return (int32_t)(low * 512 + localIndex);                   /* shl edx,9 / add edx,ebx */
}

int32_t Play(int32_t id, int32_t p2, int32_t p3)      /* 002DF220 */
{
    if (id == -1)                 return 0;
    if (SecondGate() != 0)        return 0;           /* 003603C0 over 0x022CB726 */
    return Dispatch(/*selector*/ 0, id & ~0x80000000, (uint8_t)p2, p3 & 0x7F);
}
```

**`low == slot` is forced, not assumed**: the equality test compares `(high<<16)|low` against
`handle & 0x7FFFFFFF`, whose low 16 bits *are* `slot`. So `globalSoundId = bankSlot * 512 +
localIndex` holds — but the instruction multiplies the **table entry**, and a reimplementation that
multiplies the slot index directly is relying on the check having run.

## 13. Runtime validation

**Evidence class: isolated original-code, over six bodies in 2026-09-12 and sixteen in 2026-09-18
(§13a). Live capture: still absent, and that is the gate this contract fails.**

**Executed 2026-09-12** by [`diff_sound_request.py`](../../../../Reconstruction/Tests/Differential/diff_sound_request.py)
against [`sound_request.c`](../../../../Reconstruction/Game/Audio/sound_request.c) — the
thirty-fifth pilot, and the one this contract's own §13 designed. **326 comparisons, 0
mismatches** against the shipped bytes at their real virtual addresses under Unicorn.

**Six bodies run, not one**: the four resolvers `003A1070` / `003A1100` / `003A1180` / `003A11F0`,
both wrappers `00249C60` and `00271500`, the play call `002DF220`, and verb `sebsoundplay_2c1`.

| what ran | cases |
|---|---:|
| the four resolvers over three handles, several slots, mismatched entries and both guards | 148 |
| the play call's two masks at `0x00`, `0x40`, `0x7F`, `0x80`, `0xFF`, `0x100`, `0x1FF` on both arguments, and six ids | 61 |
| `sebsoundplay_2c1` with script-chosen bank class, pan and volume | 77 |
| the gated wrapper and the gateless one, each at four gate values | 40 |

**The dispatch arguments are compared, not just the return value.** That is the whole reason this
pilot is worth having: `002DF220` masks volume to seven bits and truncates pan to eight, and a
reconstruction that treats them alike **returns the identical number** while handing the mixer a
different pan. Nothing in a return-value comparison can see it.

**Three controls, and the suite refuses to report a pass without them**: every scripted callee must
fire; the gate-set cases must SEPARATE `00249C60` from `00271500`, or the gate was never driven;
and `003A11F0` must survive a held runtime where `003A1180` refuses, which is the entire difference
between the two documented wrappers.

**Mutation campaign: 84 points — 68 KILLED, 2 EQUIVALENT, 14
SURVIVED, 0 INVALID.** Every survivor is adjudicated below; **none is a defect in the
cases**, and the ones that were have already been fixed.

**The campaign found four real gaps, and they had one cause.** In the first run, mutations of the
entry's bytes — `e[9]` for `e[10]`, a shift by nine, a shift the other way, `high << 17` — all
survived, because every case used a small slot and a zero high word, so those bytes were always
zero and any mutation of them was invisible. **Driving a handle whose high word is large killed all
four.** They were `EXERCISED` in the plan and untested in fact, which is precisely the difference a
campaign exists to expose.

**Chasing the other half of that fix produced §3's 64-entry measurement.** To drive the *low* word's
second byte I needed a slot above 255, and sizing the fixture for one faulted — the table's own
span reaches the bank handles. Reading `003A0C90` to find the real size gave `0x02AEEDC0 + 64*24 =
0x02AEF3C0` exactly. **So a hole in the test produced a fact about the engine**, and it also settled
those two survivors: with 64 entries the slot never reaches 256, the low word equals the slot, and
its second byte is structurally zero. Mutating it cannot be observed **at the real addresses**.

### 13a. The dispatch arguments, captured rather than inferred — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-096)

**First, a narrowing of the request that brought this in.** It says §13's *"nothing executed"* is now
false. §13 never said that: it records **326 comparisons, 0 mismatches, six bodies**, including the
play call's two masks driven at seven values each. What EXP-096 adds is the one thing that pilot
could not reach — **the arguments as the DISPATCHER receives them**. The dispatch was the boundary,
so the masking was proved by reading `002DF220` and not by observing what arrived on the other side.
EXP-096 hooks the scripted entry at `001DBDB0` and reads them there: **39/39 cases, 14/14 mutants,
16 real bodies, three processes.**

#### The masking, confirmed — and the argument slots shift, which the tuple does not show

`002DF220` is 92 bytes and takes `(ecx = id, edx = pan, r8d = volume)`. Four instructions do the
whole transformation:

```asm
002DF256  and   edi, 0x7f      ; volume -> 7 bits   (edi took r8d at 002DF22F)
002DF259  movzx r8d, sil       ; pan    -> 8 bits   (esi took edx  at 002DF232)
002DF25D  btr   ebx, 0x1f      ; id     -> bit 31 cleared
002DF261  mov   r9d, edi / mov edx, ebx / xor ecx, ecx / jmp 001DBDB0
```

So the dispatcher's signature is **`(0, id, pan, volume)`** while this function's is
`(id, pan, volume)`: **every argument moves one slot right and a literal zero is inserted in the
first.** EXP-096 reports the received tuple `(0, 0x605, 0xFF, 0x7F)`, which is the same fact seen
from the other end — but a reimplementation reading only the tuple could keep its own argument order
and pass **pan where volume belongs**. The shift is the part worth writing down.

#### Two refusals that return different values, and neither is −1

~~`002DF236 cmp ecx, -1` / `je` and `002DF23B call 003603C0` / `test eax, eax` / `je` both land on
`002DF244 xor eax, eax`.~~ *(Corrected 2026-10-01, OPUS, at the bytes: `002DF236 cmp ecx, -1` / `je` lands on `002DF244 xor eax, eax`, but after `002DF23B call 003603C0` / `test eax, eax` the `je` at `002DF242` jumps to the work at `002DF256`, so it is a NON-ZERO gate value that falls through to `002DF244` - as §10 row 5 and §12 say.)* **The play call answers 0 on an id of −1 and 0 when the second gate
refuses**, while a resolver failure makes the *wrapper* answer −1 from its own `or eax, -1`. §10's
failure table now has the boundary between the two pinned by execution rather than by reading.

#### Mute is not liveness, and they are different bytes of different records

`00267310` reads `+0x1F1` of the slot record the verb names through `cmdrec+0x15`; non-zero **skips
the play call entirely and pushes 0**. That is a different predicate, at a different offset, from
`00267330`'s liveness byte at `+0`. §8's silencing limit is about the first; a reimplementation that
routes both through one test silences the wrong things.

#### The VM stack contract, asserted against memory and not only against a trace

Typed pops come off in **reverse push order** (`o4 o3 o2 o1`); a type-2 float converts through
`cvttss2si`; an empty stack returns 0 **without popping**; type 3 takes the `008620C0` arm. The push
writes `{type = 2 at +0x15, value at +0xC}` into slot `byte[ctx+0x11]` of the 40-byte-strided buffer
at `[ctx+0xA8]` — EXP-096 states this as checked by memory inspection rather than inferred from the
call trace, which is the distinction that makes it worth carrying.

#### What did not become established

Everything §13 and §14 already hold as open stays open: **no live observation**, the `0x40`/64
question, and the fifth resolver's absence from the suite. EXP-096 is isolated original-code on a
hand-built fixture surface, so it moves the evidence class for the request path and nothing else.

### The 14 survivors

- **8 are provable equivalences.** Five set a flag from `1` to `2` where the flag is only ever
  read in a boolean test; one grows `SR_VARIANT[4]` to `[5]`, an entry nothing indexes. The two
  interesting ones shift `e[9]`, whose value is **always zero for every slot the table can hold** —
  a fact about the original, not a gap: the low word must equal the slot, and the slot is 0..63.
- **6 are fixture scaffolding with no counterpart in the original.** The `which` parameter and
  its bound exist because this reconstruction models four functions as one; the original has four
  separate bodies and no index to bound. The table-size bound and `SR_TABLE_BYTES` are the
  fixture's own array. `handle == 0xFFFFFFFF` survives because slot `0xFFFF` lies past a 64-entry
  table either way — **in the original that check is what prevents a read 1.5 MB past the table**,
  and the fixture reaches the same refusal by its own bound. One is an enum constant the `.c` never
  reads.
- **No undefined behaviour, and no suite defect.**

> **The table-driven model is a choice, and it is the source of nine survivors.** Writing the four
> resolvers as four functions would remove them. I have not, because the survivors are *adjudicable*
> and the alternative is contorting a reconstruction to lower a count — which is the same mistake as
> manufacturing a test to raise one.

**What this does NOT establish.** Six leaf callees are **scripted**: the liveness check, both gates,
the VM pop and push, and the dispatcher itself. **A scripted callee is not a proved one.** Nothing
here touches the five controllers, the bank managers, the voice, or whether a sound is heard. The
`00210C00` fork is read (§5) but **not executed** — the pilot stops at `001DBDB0`.

**The live half, queued with the state it needs:** set `0x02091098` non-zero and confirm interface
sounds stop **and that at least one does not** — §8 predicts both, and the negative half is the
interesting one; read a voice's `+0x1C`/`+0x20` after an ordinary request and confirm `0x7F`/`0x40`;
request a sound during a transition through `00249C60` and `00249CA0` and confirm only one refuses.
**One attach answers all three, and none has been performed.**

Receipts: `Database/Tools/work/OPUS/litsuffix/sound_request`, `sound_request2` and `sound_request3` (ignored path), and the counts row in [`MUTATION-CAMPAIGNS.md`](../../../../Reconstruction/MUTATION-CAMPAIGNS.md).

### 13a. The fork, both dispatches and the workers, executed — 2026-09-18 (OPUS, consuming EXP-105)

**Forty-three bodies from shipped bytes** — 30/30 cases, 20/20 mutants, three processes: the fork
`00210C00`, both dispatches, both worker shims and bodies, the twelve leaf setters, the voice
constructor and the pool machinery. §5 and §6 described a static reading; this is what runs.

**THE TWO DISPATCHES DO NOT MATCH ON THE SAME THING, and the difference is silent.** Re-read from the
image rather than adopted on report, because a reconstruction that copies one into the other plays
the wrong voice and nothing fails:

```
Seb 0021B5B0                                  Sep 00219EA0
  0021B5CC  cdq                                 00219ECD  mov ebp, edx      ; the RAW id
  0021B5D0  and edx, 0x1ff                      ...
  0021B5DC  lea edi, [rdx+rax]                  00219EDB  cmp [rdi+0x38], ebp
  0021B5DF  sar edi, 9                          ;         raw id, at +0x38
  0021B5FA  cmp [r10+0x3c], edi
  ;         signed bucket, at +0x3C
```

`cdq / and 0x1FF / lea / sar 9` is the textbook signed divide by 512 — `id / 512` rounded toward
zero. **Seb keys on that bucket at `+0x3C`; Sep keys on the raw id at `+0x38`.** Different key *and*
different offset.

**Both dispatches always mint a fresh receipt — but not at the same point**, which the experiment's
wording does not distinguish and a reimplementation has to. Seb calls `RCAL 00212950` at `0021B5E2`,
**before** it walks the list; Sep calls it at `00219EE8`, the merge point **after** the walk and the
target of the empty-list `je` at `00219ED5`. Every path through either reaches it, so the receipt is
unconditional in both — **playback is the conditional half, not the receipt.**

Also adopted from the run: the Seb flag byte is `sd+4`, the tree node's value, with writeback at
`sd+9` — **not `elem+0x44`, which is Sep's**; Seb reuse needs all three of `state==1`, the `~s6d`
flag and bit 7 of `sd+4`, with an early exit; the callback arms are asymmetric (`WSEB` needs
`arg6 && arg7` for kind 3, `WSEP` only `arg6` for kind 5); `002257E0` clamps volume **signed**, so a
negative clamps to 0 rather than wrapping high; and the spin fence runs only when `elem+0x30 == 1`.

> **The boundary.** Forty-three bodies is most of this chain but not the SQEX Sd driver behind it —
> `007Axxxx`–`007Fxxxx` is still unread, and §11's observation that nothing here shows a voice
> actually sounding is unchanged. What this section adds is that the *selection* is now measured
> rather than inferred.

## 14. Unresolved

1. ~~**`SR-1`**~~ — **ANSWERED 2026-09-12.** `0024A1A0` is a **control entry, not a request
   site.** It shares the gate, calls the 11-byte readiness test `002DEE80`, and tail-jumps to
   `002DF0F0(id, 0)`, which reshapes and tail-jumps again to **`001DBE90` — a different dispatcher
   from the request path's `001DBDB0`**:

   ```asm
   002DF0F2  cmp   edx, -1 / je ...      ; the second argument, not the id
   002DF103  mov   r8d, eax  / mov edx, ecx
   002DF108  not   eax / shr eax, 0x1f   ; selector = (arg2 >= 0)
   002DF10A  btr   r8d, 0x1f
   002DF114  jmp   0x1dbe90
   ```

   So `002DF0F0(id, flag)` calls `001DBE90(selector = flag >= 0, id, flag & 0x7FFFFFFF)` — **the id
   raw, no bank resolution, no pan and no volume.** `0024A1A0` passes `flag = 0`, so its selector is
   always 1. It belongs to this contract only because it reads the same gate. ~~**`00210C50` remains
   unread**, and is now the whole of what `SR-1` asked.~~ *(Superseded: `00210C50` is read - `SR-7`, ANSWERED 2026-09-12, below: a sibling of the fork through the same `[rcx+8]` / `[rcx+0x10]` pair. Struck 2026-10-01, OPUS.)*
2. ~~**`SR-2`** — **why `003A1070` guards on handle B and reads handle C.** A real cross-slot
   dependency in shipped code, with no reading yet.~~ **NO ADMISSIBLE SOURCE for the *why*; the mechanism and its
   consequence are read (2026-09-14, FABLE).**
   - **The C resolver is the B resolver with one operand changed.** Normalised for rip-relative targets and
     branch offsets, `003A1070` and `003A1100` are the same 39 instructions. They differ only in the handle loaded
     (`mov r8d, [02AEF404]` against `[02AEF400]`, at `003A1095` / `003A1125`); the guard `cmp [02AEF400], −1` is
     identical in both (`003A1076`, `003A1106`).
   - **The bank setup has a sibling of the same shape.** `003A13F0`, called only from `00266D10`, requests the three
     bank entries 0, 1 and 2 (`002ED8C0`). It installs load callbacks that store handles A, B and C: `003A1390` →
     `02AEF3FC`, `003A1330` → `02AEF400`, `003A12D0` → `02AEF404`. Before each request it writes `−1` to the handle
     that callback will fill, **except before the second**. There it writes `−1` to A again (`003A153D`), not to B.
     No other code writes B.
   - **So the B guard refuses a C sound only after B's load callback stored `−1`**, which happens when `003A1650`
     returns `−1`. Before B's callback runs, B holds its zero-initialised `0` on the first setup, or the previous
     value on a later one, and the guard passes.
   - **THE ABSENCE IS NOW SWEPT IN BOTH ADDRESSING FORMS (2026-09-18, OPUS).** The reading above rested on a
     rip-relative sweep, and this binary usually reaches a global through an image-base register instead — the
     blind spot `data_xref_scan` exists for. Re-swept in both forms over `02AEF3F0`–`02AEF410`, with the control
     passing on `02AEF3FC`: handle B has **four references in three functions**, the two guards at `003A1076`
     and `003A1106`, the read at `003A1125`, and one store, `003A1344`. **No block write reaches it either** —
     the three sites that take the address of `02AEF3F0` are bounded well below it: `003A13F0` clears **nine**
     bytes there under `cmp rcx, 9` at `003A1413`, and `003A1650` uses the same nine as a bitmap, indexing
     `idx >> 3` and setting bit `idx & 7` at `003A1700`. Handle B sits `0x10` past that base.
   - **AND THE WINDOW IS WORSE THAN "THE GUARD PASSES" (2026-09-18, OPUS).** With B at its `.bss` zero,
     `003A1100` does not merely get past the guard — **it succeeds and returns a live-looking id**. Traced:
     `movzx ecx, r8w` gives `0`; `btr` clears a bit already clear; the slot-table decode reads entry `0` at
     `02AEEDC0`, whose `+8` and `+0xA` the setup loop wrote as `0` and `0` (`003A1443` and `003A145B`, `rax`
     starting at `02AEEDC4`); the composed word is `0`, which **equals** the handle; `test edx, edx` on `0` is
     not negative; so `edx << 9` is `0` and the function returns `edx + ebx`, **the caller's own argument,
     unchanged**. The same decode appears in the callback at `003A1365`–`003A1374`, which is what makes entry
     `0` the one that matches a zero handle. *A reimplementation that refuses here is wrong in the opposite
     direction from one that reproduces the refusal row.*

   Whether the shared guard was meant (C depends on B) or is a copied operand is intent, and the binary cannot carry
   it (EVIDENCE-STANDARD addendum 2026-09-15bk). The two same-shaped slips between `003A1070` and `003A1630` are recorded
   here as the observation, not as a verdict on intent.
3. **`SR-3`** — **half answered.** The *fork* is settled: `00210C00` selects `this[+8]` on
   selector 0 and `this[+0x10]` otherwise, and the request path always passes 0. What remains is
   which named controller each of those two slots holds, and whether `sebsoundplay_2c1`'s bank
   selector (`1 → 003A1100`, `2 → 003A1070`, anything else `→ 003A1180`) is the same numbering the
   bank loaders use. **The two are different selectors** — one picks a resolver, the other a
   sub-controller — and nothing yet connects them.
   **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the two slots are the Seb and Sep controllers, and the selector
   uses the loaders' own numbering, the SE-block registry index.** Static.
   - Registry `+8` is `SebAudioController` and `+0x10` `SepAudioController`: the manager layout of
     [the bank family](../Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md).
   - **Loaders.** Registration hands the validated registry handle to `002DEF00`, which keeps `handle & 0x3F`, the
     entry index. `001DBD20` passes it to registry `+8` (`0021B430`), and the Seb bank initialiser stores it
     as the bank's key `+0x3C`. The `.seb` file's own block number travels beside it and lands at `+0x38`.
   - **Selectors.** Each of the three builds `(entry word +8 << 9) + cue` after validating its handle (`02AEF400`,
     `02AEF404`, `02AEF3FC`). The entry's word `+8` is the handle's low word, so it is the same index.
   - **The join.** The Seb lookup `0021B5B0` splits an id with `sar 9` and matches that block against `+0x3C`.
     So the numbers agree by construction. They are the registry index, not the `.seb` number the file names.
   - Control: `_index/candidates/sr3-seb-numbering/sr3_numbering.py`, 10 checks, FAILS 0. It includes a planted
     negative, which caught the `+0x38` store a first draft had missed.
4. ~~**`SR-4`**~~ — **ANSWERED 2026-09-12.** The two non-script writers are a **disable/restore
   pair inside one state machine**, and they are not independent:

   - **`0027F5D0` writes 1** (silence) at `0027F676`, reached from a ladder over its own state word
     `[rbx + 0xC0]`: `sub ecx,1 / je` · `sub ecx,7 / je` · `sub ecx,2 / je 0027F676`, so **state
     value 10** is the silencing state.
   - **`002D6F90` writes 0** (restore) at `002D6FD2`, unconditionally, inside a teardown that also
     calls `00247780(1)`, `002D7960` and `00249840` before tail-jumping to `003CA0A0`. Its census window is a mid-body fragment head; the anim-kick flag toggle sits at `0024778D` (the `xor eax,edx` arm the map-screens table anchors).
   - **`0027F5D0` calls `002D6F90`** at `0027F632`, when `[rbx + 0xD4] == 0x42`.

   So one function both silences and, by a different branch, invokes the routine that restores.
   **Nothing here clamps or normalises the value** — the gate is set to literal 1 or literal 0,
   which is consistent with the verb writing whatever a script hands it.
5. ~~**`SR-5`** — whether row 7's receipt-without-playback is reachable in ordinary play, or only when
   a bank fails to load.~~
   **BOUNDED 2026-09-22 (FABLE): a bank-load FAILURE is not involved at all, so the question's two
   alternatives are not exhaustive and the second is not a precondition.** §10's row 7 records the
   outcome; `0021B5B0` `SebController_PlayByBankBlock` (138 B) gives the reason, and it is
   structural rather than exceptional:

   ```asm
   0021B5E2  call 0x212950        ; the receipt is minted into eax BEFORE any bank is looked at
   0021B5EF  mov  esi, eax        ; kept
   0021B5F1  cmp  rcx, rbx / je   ; empty list -> straight to the epilogue
   0021B5F6  mov  r10, [rcx+0x10] ; each bank on the +0x08 list
   0021B5FA  cmp  [r10+0x3c], edi ; bank-block key against id / 512
   0021B5FE  je   0x21b60a        ;   match -> call 00224540, then 0021B61F mov eax, esi
   0021B600  mov  rcx, [rcx]      ;   advance
   0021B606  jne  0x21b5f6        ;   loop
   0021B608  jmp  0x21b621        ; EXHAUSTED -> the same epilogue, and eax is never rewritten
   ```

   **The no-match path does not fail; it simply stops.** `eax` still carries `00212950`'s return, so
   the exhausted walk hands back **the identical value** the matching path sets at `0021B61F`.
   *That is why a receipt is still issued: it was allocated before the search, and nothing on the
   way out reconsiders it.* There is no error branch, no load-state test and no reference to any
   bank's load result anywhere in the body — row 4 is the contract's only load-state gate and it
   concerns bank slot B specifically, checked by two resolvers, not by this lookup.

   > **So the better question, and it is not this one.** Row 7 fires whenever **no resident bank
   > carries block `id / 512`**, which needs only a request for a block that is not loaded — a
   > *sequencing* fact, not a failure. Whether any shipped request ever names a non-resident block
   > is an ordering question about play and is **routed to ASTRA**
   > (`FABLE-REQ-ASTRA-SR5-IS-A-NON-RESIDENT-BLOCK-EVER-REQUESTED`). **Static, bodies read;
   > nothing observed live.**

   *Detector scope, 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-SR5-EXHAUSTION-TRIGGER`
   (`_experiments/evidence/sr5-exhaustion-preflight/`, static CFG witnesses). The listing above has two miss routes,
   and a live check must not treat them as one:*
   - *`0021B608` is reached only when a **non-empty** list is walked to its end without a match. An empty list leaves
     at `0021B5F4` and never reaches it.*
   - *The epilogue `0021B621` is shared by the match, the empty miss and the non-empty miss, so a hit there
     classifies nothing.*
   - *"Empty" means empty after the receipt call at `0021B5E2`, since the head is loaded after it.*
   - *So `0021B608` is a positive detector for one route. No hit there does not mean no miss occurred, and a bounded
     run with no hits never shows that row 7 cannot happen in play.*
   - *The candidate for the empty route is `rcx == rbx` at `0021B5F1`, with the real controller identified. It is a
     candidate, not a qualified breakpoint.*
   - *The mechanism above is unchanged: both miss routes return the receipt.*
6. **`SR-6`** — **ANSWERED 2026-09-23 (SWE2-CONTRACT): no shipped path can mint such a handle.**
   The resolvers genuinely do not bound the index — `003A1240`'s `movzx r8d, cx` at `003A1245` is
   the whole guard — but every route to a handle value is enumerated and none produces a low word
   above 63:

   * **All handles derive from `003A0C90` (find-or-allocate).** On a match it returns the walked
     node's own tag pair `(entry[+0xA] << 16) | entry[+8]` (`003A0D0A`–`003A0D19`), and the
     initialiser writes `entry[i].+8 = i` for every node (`003A1443`, `edx` loop to `0x42`), so
     the low word is the walked slot. On a miss it pops the **free list** — the head sentinel
     node 65 at `02AEF3D8` — through the unlink helper `003A1750`, which splices only
     list-internal link words and poisons the popped node to `-1`. The init chains free nodes
     `0 → 63` ending at `-1` (`003A1468` writes `entry[63].next = 0xFFFF`), so the free list can
     only ever hold pool slots.
   * **The three bank globals have four writers total**: the three setter bodies storing
     `003A1650`'s return (`edi`, the walk result with bit 31 cleared — `003A1712 mov eax, edi`)
     at `003A12E4`/`003A1344`/`003A13A4`, plus `-1` clears at `003A14BE`/`003A153D`/`003A15BC`.
     `003A1650` itself re-validates `entry[di]`'s tag pair against `edi` before storing
     (`003A1694`–`003A16CC`).
   * **`003A1240`'s only caller is `002E9FB2`** — inside `002E9D90`, the actor-side sound lookup —
     which reads a stored handle from the sound set's `+0x30 + group*4` array. That array's only
     writers are `002E61E9` (storing `003A1650`'s return) and `002E61C2` (storing `-1` on the
     null path). A whole-image scan finds **no stored pointer** to `003A1240`, so no indirect
     route exists.
   * **A slot of 64 or 65 is not even an accident waiting to happen** — those are the two
     sentinel head nodes, valid 24-byte nodes by construction (see §15a addendum below). A
     handle with low word 64/65 would validate against the sentinel's own self-tag. A slot of
     66+ would read the bitmap/`02AEF3FC` handle cells — but nothing mints one.

   What the question was really asking — is the unbounded `movzx cx` load-bearing — resolves to:
   **the bound is a data-flow invariant, not a code bound.** A corrupted stored handle would index
   out of the node array unchecked (a read-only compare, so harm rather than crash is bounded
   too). No writer produces one. NATIVE/STATIC — every producer body read, nothing observed live.
7. ~~**`SR-7`**~~ — **ANSWERED 2026-09-12.** `00210C50` is a **sibling of the fork with the same
   two-object shape**: it reaches `this[+8]` and `this[+0x10]` through `00212B80`, `0021B640` and
   `0021A100`, calling **both** when its third argument is non-zero and one or the other otherwise.
   It also **sets** bit 31 of its fourth argument when its second is zero — the inverse of
   `002DF220`'s `btr`. It is not on the request path; it shares the fork's two sub-controllers.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the wrapper is 51 bytes, takes **one** argument through an unwritten `ecx`, and tail-jumps | **re-read 2026-09-12**: `00249C60`–`00249C92` complete; no write to `ecx` before `00249C6D call`, and `00249C86 jmp 0x2df220` after the epilogue; `functions.tsv` size 51 | 1 | PROVEN |
| the two constants are `0x40` and `0x7F` built by a peephole | **re-read**: `00249C77 mov edx, 0x40` then `00249C7E lea r8d, [rdx + 0x3f]` | 1 | PROVEN |
| the global gate is `*(0x02091098)` and refuses before the lookup | **re-read**: `00249C64 cmp dword [→02091098], 0` / `jne` to the `or eax,-1` tail | 1 | PROVEN |
| the gate has exactly four references image-wide, one of them a write | **the source page's §10 already establishes this**, and I re-ran it independently: `data_xref_scan.py --addr 0x02091098 --control 0x02AEF3FC`, control returned 5 references so the count is meaningful, hits `00249C64`, `00249CA4`, `0024A1A6` (reads) and `00249FC0` (write) — **two instruments, same four** | 1 | PROVEN |
| the setter is 7 bytes and stores its argument verbatim | **disassembled by me**: `00249FC0 mov [rip+0x1e470d2], ecx` / `ret`; `functions.tsv` size 7 | 1 | PROVEN |
| a script verb reaches the setter, and its argument becomes the gate value | **disassembled by me**: `00512080` pops one int via `00267E10` and `jmp 0x249fc0`; `scriptvm-verb-table.tsv` row `7013` = `fsmenu_sedisable`, arity 1, guard `fsmenu`, handler `00512080` | 1 | PROVEN |
| **`00271500` is a fourth wrapper with no gate check** | **disassembled by me**: all 42 bytes — `call 0x3a1180` / `cmp eax,-1` / `mov edx,0x40` / `lea r8d,[rdx+0x3f]` / `jmp 0x2df220`, and **no reference to `0x02091098`**, which the controlled scan above independently confirms | 1 | PROVEN |
| six further functions inline the wrapper, none reading the gate | **verified by me**: `edges.tsv` gives `0030C650`, `003112F0`, `00357040`, `00366870`, `003E8690`, `0046CC70` calling both a resolver and `002DF220`; each disassembled at its call sites; none appears among the gate's four references | 1 | PROVEN |
| `sebsoundplay_2c1` passes script-chosen pan and volume | **disassembled by me**: `00357040` full body — four `call 0x267E10`, then `mov r8d,r15d` / `mov edx,r12d` / `call 0x2df220`; `scriptvm-verb-table.tsv` row `02C1`, arity 4, pops_int 4 | 1 | PROVEN |
| pop *n* is argument *5−n* | **not my result**: "Arguments arrive in reverse order", tier 1 PROVEN in [the calling convention](../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md) | 1 (static) | PROVEN |
| `p3` is masked to 7 bits and `p2` only truncated to 8 | **re-read**: `002DF256 and edi, 0x7f` against `002DF259 movzx r8d, sil`, and **again downstream** at `00210C0C and r9d, 0x7f` against `00210C03 movzx r8d, r9b` | 1 | PROVEN |
| the id's bit 31 is cleared and the selector is hardcoded 0 | **re-read**: `002DF25D btr ebx, 0x1f`, `002DF266 xor ecx, ecx` | 1 | PROVEN |
| the second gate returns before dispatch, with **0** rather than `-1` | **re-read**: `002DF23B call 003603C0` / `test eax,eax` / `je` to the work, falling through to `002DF244 xor eax,eax` | 1 | PROVEN |
| **the resolver arithmetic is `entry[+8] * 512 + localIndex`, and `entry[+8] == slot` is forced** | **re-read in full, all four bodies**: `movzx ecx,r8w` / `btr r8d,0x1f` / `lea rax,[rcx+rcx*2]` / `movzx edx,[rcx+rax*8+8]` / `movzx ecx,[rcx+rax*8+0xa]` / `shl ecx,0x10` / `or ecx,edx` / `cmp ecx,r8d` / `shl edx,9` / `add edx,ebx` — at `003A10A6`–`003A10CE`, `003A1136`–`003A115E`, `003A11AF`–`003A11D7`, `003A1208`–`003A1230` (the fifth resolver `003A1240` runs the same shape at `003A1249`–`003A1275`) | 1 | PROVEN |
| the sign test on the entry word is unreachable | **re-read**: `test edx,edx / js` on a value `movzx`-ed from a `word` — `003A10CA`/`003A10CC`, `003A115A`/`003A115C`, `003A11D3`/`003A11D5`, `003A122C`/`003A122E`, and `003A1273` in the fifth | 1 | PROVEN |
| **there are five resolvers over three handles and one table** | **verified by me**: `data_xref_scan.py` on `0x02AEF3FC` (5 refs, control passed) and on `0x02AEF400` (4 refs, control passed) plus the disassembled loads in `003A1070`/`003A1100`/`003A1180`/`003A11F0`; the table `lea` resolves to `0x02AEEDC0` in all four. **CORRECTED 2026-09-12 (§15a): there is a FIFTH, `003A1240`, which runs the same `entry[+8] * 512 + localIndex` on the same table with the same handle validation and the same dead sign test. It was missed because the enumeration was anchored on the three GLOBAL handles and this one takes its handle as a PARAMETER** — a census keyed on the data, not on the arithmetic | 1 | PROVEN |
| `003A1070` guards on handle B and reads handle C | **verified by me**: `003A1076 cmp [→02AEF400], -1` and `003A1095 mov r8d, [→02AEF404]`, both addresses returned by the controlled scan rather than by my own offset arithmetic | 1 | PROVEN |
| `003A1180` and `003A11F0` differ **only** in the liveness precondition | **re-read both bodies in full**: same handle `0x02AEF3FC`, same table, same arithmetic; `003A1180` calls `00267330` and `003A11F0` has no call at all | 1 | PROVEN |
| the three handles are set by three 83-byte setters and cleared together | **verified by me**: `data_xref_scan.py` writers — `003A1390`→A, `003A1330`→B, `003A12D0`→C; `functions.tsv` sizes 83/83/83/582. **CORRECTED 2026-09-25 (OPUS-REQ-CONTRACT-THREE-STATE-CORRECTIONS-BLOCK-214, re-verified):** `003A13F0` does NOT clear all three — it stores `0xFFFFFFFF` to A at `003A14BE` **and again** at `003A153D`, and to C at `003A15BC`; B (`02AEF400`) is never written by the teardown. The second store sits inside the block whose completion callback is B's own setter `003A1330` (`lea` at `003A1568`; block callbacks are `003A1390`→A / `003A1330`→B / `003A12D0`→C). Runtime consequence not claimed | 1 | PROVEN |
| `(0x40, 0x7F)` are pan and volume, and pan's field is 0–255 | the source page's §2: `002256B0` resets `+0x20 = 0x40` and `+0x1C = 0x7F`, and the pan setter branches at `0x80` — **corroborated independently** by the verb's argument positions above | 1 | PROVEN |
| **the fork is a two-way branch on the selector, and the request path always takes `+8`** | **re-read by me**: `00210C10 test edx,edx` selecting `[rcx+8] → 0021B5B0` or `[rcx+0x10] → 00219EA0`, and `002DF266 xor ecx,ecx` fixing the selector at 0 | 1 | PROVEN |
| `00210C50` is a sibling of the fork, not a request site | **disassembled by me**: same `[rcx+8]` / `[rcx+0x10]` pair through `00212B80`, `0021B640`, `0021A100`; sets bit 31 of its fourth argument where `002DF220` clears it | 1 | PROVEN |
| the singleton is five controllers with real RTTI | the source page's §2 constructor table | 1 | PROVEN |
| a receipt is issued when nothing started | the source page's §1 and §2 | 1 | PROVEN |
| 100 non-Audio callers and none inside Audio | the source page's §10, after a byte-level decode found one `edges.tsv` omits — **re-counted by me from `edges.tsv`: 99 distinct callers, which is exactly the page's 100 minus the one it says `edges.tsv` misses, and `functions.tsv` owns none of them to Audio** (29 UI, 3 Save_Load_Settings, 67 unassigned) | 1 | PROVEN |
| **the table is exactly 64 entries, so the slot is 0..63 and the id space is 15 bits** | **re-read by me**: `003A0C90` uses the same stride-24 addressing, starts at `0x40` and treats it as *none*, and follows a signed 16-bit link at `+0` from a head at `0x02AEF3C0`; `0x02AEEDC0 + 64*24 = 0x02AEF3C0` exactly | 1 | PROVEN |
| the `0x40` that evidences the table's length is a not-found sentinel, not a length | **§15a**: `003A0C90` sets `mov r9d, 0x40` *before* the search and tests `cmp r9d, 0x40 / je` after it, so it establishes that **64 is not a valid slot**, not that the table has 64 rows. Against it, `003A0EA0` sweeps the same stride-24 table over a **9-byte / 72-bit** bitmap at `02AEF3F0` (`cmp r14d, 0x48`), and only **66** entries fit between `02AEEDC0` and that bitmap. Three candidate lengths; the row above asserts one. **RESOLVED 2026-09-23 (SWE2-CONTRACT, §15a addendum): all three are right — 64 pool slots + 2 sentinel head nodes + 72 bitmap bits, proven by the init loop `003A1434`–`003A14A6`** | 1 (static) | **PROVEN** |
| the gate's two non-script writers are a disable/restore pair | **disassembled by me**: `0027F676 mov ecx,1 / call 00249FC0` under a state ladder on `[rbx+0xC0]`, and `002D6FD2 xor ecx,ecx / call 00249FC0` in a teardown; `0027F632` calls `002D6F90` | 1 | PROVEN |
| `0024A1A0` is a control entry, not a request site | **disassembled by me**: all 46 bytes, then `002DF0F0`'s 41 — `jmp 001DBE90` with a computed selector, a raw id and no pan/volume pair; `001DBE90` is a different function from `001DBDB0` | 1 | PROVEN |
| any execution of this path, isolated or live | ~~**none**; §13~~ *(Corrected 2026-10-01, OPUS: isolated original-code execution exists - §13, 326 comparisons over six bodies with 0 mismatches, and §13a's EXP-096 / EXP-105; nothing live)* | none live | UNKNOWN for live |
| why `003A1070` guards on a handle it does not read | **not established**; `SR-2` | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Re-derived from the shipped bytes with a **third** instrument: capstone over `functions.tsv`, **per
function** (38,161 functions, 1,787,590 instructions, **0 skipped**), classifying every rip-relative
reference as READ / WRITE / LEA from the operand rather than from a pattern.

### Reproduced exactly

| the document says | this pass measures |
|---|---|
| the gate `02091098` has **exactly four** references, one a write | **4** — `00249C64`, `00249CA4`, `0024A1A6` (reads) and `00249FC0` (write). Three instruments, same four |
| handle **A** `02AEF3FC`: 5 refs | **5** (2 reads, 3 writes, in 4 functions) |
| handle **B** `02AEF400`: 4 refs | **4** (3 reads, 1 write, in 3 functions) |
| the table `lea` resolves to `02AEEDC0` in all four resolvers | it does |

**Two instruments agreeing is worth less when they may share an assumption**, which is why this was
re-run a third way. The gate count survives that.

### Refuted: there are FIVE resolvers, not four

`003A1240` (66 bytes) is the same arithmetic on the same table:

```asm
003A1245  movzx r8d, cx                      ; slot = handle & 0xFFFF
003A124D  lea   rax, [r8 + r8*2]             ; ×3
003A1251  lea   r8,  [rip → 02AEEDC0]        ; ×8 below ⇒ stride 24
003A1258  movzx r9d, word [r8 + rax*8 + 8]   ; entry[+8]
003A125E  movzx r8d, word [r8 + rax*8 + 0xA] ; entry[+0xA]
003A1268  or    r8d, r9d                     ; the packed id
003A126B  cmp   r8d, ecx                     ; must equal the handle, bit 31 cleared
003A1270  test  r9d, r9d / js                ; the SAME provably dead sign test
003A1275  shl   r9d, 9                       ; entry[+8] × 512
003A1279  lea   eax, [rdx + r9]              ; + localIndex
```

> **Why it was missed is the useful part.** The four known resolvers each name one of the three
> handle *globals*, so `data_xref_scan.py` anchored on those globals returns exactly four and the
> control passes. `003A1240` takes its handle **as a parameter** and touches no handle global. **A
> census keyed on the data cannot find a function that never names the data** — the same failure
> mode as this sweep's other miscounts, which were every one of them about population.

**It is not covered by §13's suite**, which runs six bodies; this is not one of them. Stated, not
papered over.

### Qualified: "exactly 64 entries" is not established by its evidence

The `0x40` in `003A0C90` is a **not-found sentinel** (`mov r9d, 0x40` before the search; `cmp r9d,
0x40 / je` after it), so it establishes that **64 is not a valid slot**, not that the table has 64
rows. Against it: `003A0EA0` sweeps the same stride-24 table over a **9-byte, 72-bit** bitmap at
`02AEF3F0` (`cmp r14d, 0x48`), and only **66** entries fit between `02AEEDC0` and that bitmap
(`0x630 / 24`). Three numbers — 64, 66, 72 — and the document asserts one of them. The claim is
marked **QUALIFIED** rather than refuted: it may well be right, but not on this evidence.

> **Resolved 2026-09-23 (SWE2-CONTRACT): all three numbers are right, and they describe one
> structure.** The bank setup `003A13F0` builds the pool at `003A1434`–`003A14A6`: a `edx` loop
> bounded by `cmp edx, 0x42` writes **66 nodes** of 24 bytes from `02AEEDC0` —
> `entry[i].+0 = i+1` (next), `+2 = i−1` (prev), `+4 = -1` (empty id), `+8 = i` (the self-tag),
> `+0xA`/`+0xE = 0` — then fixes the ends: `entry[63].next = -1` (`003A1468`), used-head node
> `02AEF3C0` (slot 64) `next = prev = -1` (empty list), free-head node `02AEF3D8` (slot 65)
> `next = 0, prev = -1`, and `entry[0].prev = 0x41` (`003A1497`) — entry 0's prev is sentinel 65.
> So the array is a **66-node doubly-linked list whose last two nodes are the two list heads**
> (`02AEF3C0` used, `02AEF3D8` free — `003A0C90` walks from `word[02AEF3C0]`, the miss path pops
> from `word[02AEF3D8]`), and the bitmap at `02AEF3F0` is 9 zeroed bytes whose 72 bits pad the 64
> pool slots. **64 = valid slots, 66 = nodes, 72 = bitmap bits.** The "exactly 64 entries" claim
> is now established on its own evidence: only 64 of the 66 nodes are reachable as slots, because
> every handle's low word is a walked or allocated pool node and the sentinels are never linked
> into either list's data run (init leaves them isolated; `003A1750` only splices existing
> links). The §15 claim upgrades from QUALIFIED to PROVEN by the init body — NATIVE/STATIC.

### Five functions address this table and the contract named none of them

| function | size | what it does |
|---|---:|---|
| `003A0EA0` | 222 | sweeps the 72-bit allocation bitmap, `btr`-ing each live slot's bit and clearing `+0x10`/`+0x14` |
| `003A0F80` | 233 | **release** — validates the handle, decrements the refcount at `+0xE`, and on zero bumps the generation at `+0xA`, sets `+4 = -1` and unlinks from the `word +0` / `word +2` list |
| `003A1240` | 66 | **the fifth resolver** (above) |
| `003A1290` | 62 | **state query** — same handle validation, returns the byte at `+0xC` |
| `003A1750` | 114 | the list-unlink helper `003A0F80` calls |

Together with the three setters and the clearer the document does name, that is **12 functions**
taking the table's address, where §15 accounts for seven.

**Not claimed:** nothing here is a live observation, and no new execution was performed — §13 is
unchanged and the live-game pause holds. The `0x40`/64 question and the fifth resolver's absence from
the suite are recorded as open, not closed.

## 16. Parity plan

**Constructed and run, 2026-09-12** — `CALCULATION`, `STRUCTURAL` and `EDGE-CASE` are `COVERED` by
`diff_sound_request.py` over six bodies: the resolver's `entry * 512 + index` and its handle
validation, the 24-byte slot entry, the three-handle array, §10 rows 1–6 and 8, the liveness
precondition that separates the two documented wrappers, and the cross-handle guard that separates
`003A1070` from the rest.

**The two voice fields are NOT covered** — they live behind the scripted dispatcher, so what the
pilot compares is the pan and volume *as dispatched*, not as written to a voice.

**Not constructible offline:** `INTEGRATION` — the five controllers and the bank managers are the
subsystem, and scripting them tests the wrapper rather than the path; `TIMING` — nothing here
establishes when a caller asks; `PRESENTATION` — whether a sound is *heard* is outside any
differential; `RNG`; `SERIALIZATION`; `FULL SUBSYSTEM`.

## 17. Related

- [`how-a-sound-request-becomes-a-voice.md`](how-a-sound-request-becomes-a-voice.md) — the mechanism.
- [`../CONTRACT-field-music-selection.md`](../CONTRACT-field-music-selection.md) — the music path
  this one cannot reach.
- [`../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md`](../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md)
  — where the pop order §7 depends on is established.
- [`../../04-Actor-Entity/CONTRACT-field-runtime-pass.md`](../../04-Actor-Entity/CONTRACT-field-runtime-pass.md)
  — the runtime whose liveness `00267330` reports, and therefore the reason §10 row 3 exists.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **CoreRuntimeScheduling — SERVICE, with a consequence for the play gate.** The single global enable byte behind
  `003603C0` (8 B) is read by the 2,001-byte field / battle frame body, mode 2
  ([between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)). **The frame
  reads the same byte that `002DF220` must agree with before it plays.** The item-write and recompute resolver reads
  are MECHANICAL.
- **Items_Equipment_Shops_License — CLIENT.**
  - `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`) is the item write behind twelve inventory
    functions: the shop commits, the bundle appliers, the equipment counters, the temporary snapshot and restore,
    `Inventory_GrantEncodedLootItem` and the class-D reset. It asks `Inventory_QueryEncodedItemStateByClass`.
  - The recompute is driven by the equipment and licence setters.
  - `BattleFormula_ApplyTargetResult` also grants items.
- **Input — SERVICE and CLIENT.** `0027F5D0` and `002D6F90` call small Input-filed helpers (30 B and 24 B). The
  manager-slot byte reader `00267310` is read by the 1,002-byte Input body.
- **Platform — SERVICE.** `00224570` asks the 78-byte QPC seconds timer.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `BattleUnit_ExecuteDirectStateCommandOrder`, owned by that layer, calls `0030FED0` on this page. That caller is the direct-order execution: `byte[+0x6B4]` non-zero refuses it outright, and otherwise `word[+0x714]` and the pending action's signed `word[+2]` drive it; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Platform — SERVICE.** `00224570` on this page calls `FUN_005cc930`, owned by that layer. What it reaches is a high-resolution counter read: it calls the import at `008C2188` and converts the unsigned 64-bit result to double with the `2^64` fixup at `00D27A68`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## The `00249CA0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00249CA0` (~79 B) — `dword[02091098] == 0` runs `003A11F0()`; `-1`
return skips, else `edx = 0x40` continues (`00249CA4`/`00249CB7`).

| member | role | interior |
| --- | --- | --- |
| `003A11F0` | `02AEF3FC`-keyed index — `-1` → `-1`, else `movzx ecx, r8w` (`003A11FA`/`003A1204`) | [`003A11FA`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `003A13F0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`003A13F0` (~78 B) — audio-boundary body.

| member | role | interior |
| --- | --- | --- |
| `002ED8C0` | `dword[rdx] = 0x20` then `ecx` dispatch 0/1/2 — request-kind write (`002ED8C0`/`002ED8CC`) | [`002ED8C0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `002DF220` (2026-09-18, SWE2-EC7)

`002DF220` — 92 B, 9 callers; a gated forwarder into the request path. `ecx == -1` or a
~~zero~~ **non-zero** *(corrected 2026-10-01, OPUS: `test eax, eax` / `je 002DF256` at `002DF240`)* from `003603C0` returns 0 immediately; otherwise it strips the top bit of `ebx`
(`btr ebx, 0x1F`), masks `r8d` to `0x7F`, widens `sil`, and tail-jumps to `001DBDB0`
([`002DF277`](../../_index/ADDRESS-INDEX.md)) with `ecx = 0`. The `-1` id convention and
the bit-31 clear match the request contract's "no voice / don't-care flag" semantics —
this is one of the boundary's small idiom gates in front of the real submit.

## SWE2-EC7-40 update (2026-09-19) - `003A0C90`

`003A0C90` (387 B) is the stride-24 table walk the page names - head at `02AEF3C0`, link field `+0`, `r9d` bound `0x40`; `003A1750` plus `02AEF3D8`. Interior anchor `003A0D5E` (a `003A1750` call).

## SWE2-EC7-46 update (2026-09-19) - `003A0F80`

`003A0F80` (233 B) is a body - `002DEEF0`/`003A1750`. Interior anchor `003A0FEC` (a `002DEEF0` call).

## SWE2-EC7-47 update (2026-09-19) - `003A0EA0`

`003A0EA0` (222 B) is the 72-bit allocation-bitmap sweep - `btr`s each live slot's bit and clears `+0x10`/`+0x14` over the stride-24 table - `002DEE90`/`00369800`/`0036D200`. Interior anchor `003A0F09` (a `002DEE90` call).

## SWE2-EC7-47 update (2026-09-19) - `0021A100`

`0021A100` (214 B) is the sound-request fork - `00223300` single call; calls both arms when its third argument is non-zero. Interior anchor `0021A17B` (the `00223300` call).

## SWE2-EC7-61 update (2026-09-19) - `00359150`

`00359150` (154 B) is a Party-side caller of the per-unit mute predicate the CONTRACT names - `00265020`/`00267330`/`002E9FE0`/`002EA6A0`/`003588B0` plus `022C7FE0`. Interior anchor `0035916C` (a `003588B0` call).


## SWE2-EC7-69 update (2026-09-19) - `00212950` request-id generator measured

`00212950` (28 B) measured - the `RCAL 00212950` the contract names is the
positive ticket generator: `eax = dword[01FD36B4] + 1`, masked to
`0x7FFFFFFF`, and `cmove`'d to 1 when the increment wrapped to 0 - ids stay
in `1..0x7FFFFFFF` forever. Call-free; the counter feeds the `01FD36C0`
request table `00212A70` clears.
Interior anchor `0021295D` (the `and eax, 0x7fffffff` wrap mask).

## SWE2-EC7-90 update (2026-09-20) - `003A1750` word-index unlink measured

`003A1750` (114 B) is the unlink the sound-request callers run:
`rcx`'s two words are link indices into the `02AEEDC0` table
(24-stride nodes); each live index takes the partner's word
(`r11w` into `[r10]`, `r9w` into `[r8+2]`) before both of
`rcx`'s words are set to -1 - a doubly-linked removal from a
word-indexed ring.
Interior anchor `003A17A5` (the link write).

## SWE2-EC7-104 update (2026-09-20) - `00270130` measured

`00270130` (28 B) is the bounded flag write
`003E8690` and `003E8C50` call on the
`02F8F23C` byte table: when `ecx < 0x40` it
clears bit 1 of `02F8F23C[ecx]` and ORs
`(dl & 1) << 1` back in - a 64-slot flag array
where slot `ecx` carries one toggleable bit.
Out-of-range indices are ignored.
Interior anchor `00270144` (the bit clear).
