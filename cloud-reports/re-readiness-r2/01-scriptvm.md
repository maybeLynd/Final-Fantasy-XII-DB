# Reconstruction readiness, pass 2: `FFXII TZA/01-Script-VM-Native-Bridge/` (`01-scriptvm`)

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Working for | FABLE |
| Pass 1 | [`cloud-reports/re-readiness/01-scriptvm.md`](../re-readiness/01-scriptvm.md) (2026-10-02, snapshot `86b70c69`) |
| This pass | 2026-10-03, snapshot `b23bdddd` (synced from XIIOnline `f9d9053b9`) |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes a page or a register row and gives its current location. No executable, Ghidra or live game was used. |

## How to read the citations

A citation is `ALIAS:line` against the **current** snapshot. Line numbers moved since pass 1: most pages lost their
`level:` front-matter line on 2026-10-02 (so many lines are one lower), and several pages gained sections. The paths
are relative to `FFXII TZA/01-Script-VM-Native-Bridge/`. `REG` is `FFXII TZA/_index/OPEN-QUESTIONS.md`, cited by
row id. Pages in other categories are given as paths from `FFXII TZA/` and were **not** audited for this report.

| alias | page | lines now |
|---|---|---:|
| `README` | `README.md` | 50 |
| `DT` | `scriptvm-native-dispatch-table.md` | 1,186 |
| `WAIT` | `verbs-that-only-wait-and-verbs-that-do-nothing.md` | 397 |
| `NAMES` | `how-a-script-names-a-thing-in-the-world.md` | 610 |
| `C-INT` | `CONTRACT-interpreter-core.md` | 320 |
| `C-NCL` | `CONTRACT-native-command-lifecycle.md` | 289 |
| `C-BR` | `CONTRACT-script-to-native-bridge.md` | 471 |
| `INT` | `Interpreter-Core/worldactor-scriptvm-interpreter.md` | 1,148 |
| `RES` | `Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md` | 192 |
| `REQ` | `Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` | 257 |
| `BIND` | `Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md` | 543 |
| `VARS` | `Interpreter-Core/script-variables-and-their-storage-classes.md` | 635 |
| `ATEL` | `ATEL-Control-Modules/the-ctrl-module-debug-companions.md` | 934 |
| `NCL` | `Native-Command-Lifecycle/native-command-lifecycle.md` | 813 |
| `VD` | `Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md` | 1,533 |
| `C-VD` | `Verb-Dispatch/CONTRACT-verb-dispatch-abi.md` | 686 |
| `POP` | `Verb-Dispatch/the-shape-of-the-verb-population.md` | 498 |
| `REACH` | `Verb-Dispatch/what-each-script-verb-touches.md` | 383 |
| `CC` | `Spawn-Verbs/the-script-to-native-calling-convention.md` | 898 |
| `BP` | `Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md` | 187 |
| `READIN` | `Party-Presentation-Verbs/the-party-read-in-state-machine.md` | 441 |
| `STDM` | `Party-Presentation-Verbs/the-party-standard-motion-verbs.md` | 541 |
| `LOOKS` | `Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md` | 647 |

**Method.** I read pass 1's §2 (gaps S-1 to S-31 and G-1 to G-18) and its §3.1 value contradictions (C-V1 to C-V60).
I diffed the folder and the register between pass 1's snapshot `86b70c69` and this one: 24 files, 640 lines added,
204 removed. Every gap was then re-checked against the current page text, whether or not its lines changed. Pass 1's
68 stale-text items (§3.2, C-S1 to C-S68) are not re-audited here. Where a stale line now contradicts a newer
answer, it is listed as a new DOC gap.

---

## 1. Summary

**Pass-1 gaps: 49** (31 stated by the pages, 18 structural).

| verdict | count | ids |
|---|---:|---|
| CLOSED | **3** | S-3, S-10, G-8 |
| NARROWED | **8** | S-2, S-17, S-27, G-1, G-3, G-7, G-13, G-14 |
| OPEN | **34** | S-1, S-4, S-5, S-6, S-8, S-9, S-11 to S-16, S-18 to S-24, S-26, S-28 to S-31; G-2, G-5, G-6, G-9, G-10, G-11, G-15, G-16, G-17, G-18 |
| WRONG-IN-PASS-1 | **4** | S-25, G-4 (wholly); S-7, G-12 (in part, with a residue still open) |

**OPEN and NARROWED gaps by class** (42): STATIC 29 · RUNTIME 6 · DATA 4 · DOC 3. A gap with a mixed residue is
counted under its main class; §2 gives each one's class.

**New gaps: 9** (STATIC 5 · DOC 3 · DATA 1 · RUNTIME 0).

**Pass-1 value contradictions (C-V1 to C-V60), follow-up:** **41 resolved** on the pages since pass 1, nearly all
by OPUS's dated 2026-10-02 corrections. **19 remain**: 16 unchanged, 2 resolved only in part (C-V44, C-V45) and 1
narrowed (C-V29). See §2.3.

**Rating: NOT YET (unchanged from pass 1).** The machinery that runs a script is now very close to READY. Most of the
decisive pass-1 contradictions (the default opcode arm, arithmetic typing, the family-table initialiser, the
`cmdState+0x08` width, the `+0x15` writers and values, the unknown-tag pop, the `+0x44` byte) are settled on the pages.
What still decides the rating is G-1, the verb bodies: of about 1,886 callback functions, about 140 have gained a
one-sentence body description since pass 1, and most of those sentences name their callees only by call site.
By part: value stack and calling convention **READY** (was MOSTLY); variables **READY** (was MOSTLY); dispatch and
lifecycle **MOSTLY**, with a shorter list; request scheduling **MOSTLY**; interpreter **MOSTLY** (was NOT YET);
verbs **NOT YET**. See §4.

---

## 2. Pass-1 gaps

One row per pass-1 gap, in pass 1's order. "Class" applies to what is still missing. Quotes are exact. `…` marks
an elision. A `~~struck~~` passage is struck on the page itself.

### 2.1 Gaps the pages stated themselves (pass-1 S-1 to S-31)

| id | gap (short) | verdict | evidence now | still missing · class · register |
|---|---|---|---|---|
| S-1 | live scheduling, synchronisation, reentrancy, allocation identity | **OPEN** | `RES:140`: "- [ ] **OV-16.** Establish live scheduling, synchronization, reentrancy and allocation-identity requirements where needed."; `RES:4`: "OV-16 stays open (… runtime, carried by FABLE-REQ-ASTRA-RT-REMAINDERS-0929; the universal reentrancy part is superseded under OV-2's limit)"; `C-NCL:221`; `C-INT:244` | The live-scheduling half. The universal reentrancy half is now a declared limit (OV-2 SUPERSEDED). · **RUNTIME** · REG `OV-16` **OPEN** (RT) |
| S-2 | does shipped play exhaust the notification pool; what recovery follows | **NARROWED** | Recovery: REG `OV-10`: "there is no recovery policy because both notification producers ignore the allocation return". New since pass 1, `REQ:224-226`: "the end notification is attempted before the removed slot is relinked and published, so the capacity that matters is the requester's free head at the attempt (section 3)"; `REQ:128`: "**So a self-requested notification on a full pool is lost.**" (a conditional static reading, premises at `REQ:129-133`) | Only whether shipped play reaches a full pool, observed at the attempt (`REQ:140`). · **RUNTIME** · REG `OV-10` **PARTLY ANSWERED**, residue OPEN (RT) |
| S-3 | RC-12 adjudication "pending" | **CLOSED** | `BIND:4`: "the footer slots answered on ORACLE's record with a premise correction (RC-12: the footer is 0-based; FABLE accepted it and corrected its own slot table at a8aed6ca9, auditsem-corrections-fable-0930)"; REG `RC-12`: "*Restated 2026-10-03 on FABLE's adjudication at `a8aed6ca9` …: FABLE accepted ORACLE's 0-based footer and corrected its own slot table*" | Nothing for the value. Two lines on `BIND` still say "pending": see new gap N-1. · REG `RC-12` **ANSWERED** |
| S-4 | which record a spawn entry's function runs on (RC-16 residue) | **OPEN** | `INT:931`: "RC-16's stated limit: which record a spawn entry's function runs on (static, not traced)." | As stated. · **STATIC** · REG `RC-16` **ANSWERED** (FABLE accepted ORACLE's NARROWED; the residue is a stated limit) |
| S-5 | 51 of 436 `00267DB0` call sites undetermined | **OPEN** | `INT:872-873`: "Those 51 are undetermined in the interesting direction (Pointer 2026-10-01 (SWE2-CONTRACT for OPUS): a limit on the helper's name, not an open question about the interpreter …)"; `C-BR:87-89` | The page now frames it as a limit on the helper's name. A port does not need it. · **STATIC** · no row |
| S-6 | MXCSR state, behaviour after an integer divide fault, NaN compares | **OPEN** | `INT:559`: "**Not claimed:** the game's MXCSR, what the process does after a divide error, or which scripts compare NaNs" | All three. The NaN-compare half is a script census. · **RUNTIME** (NaN half: DATA) · no row |
| S-7 | what a `global` variable at a given offset means | **WRONG-IN-PASS-1** (in part) | REG `FZ-27` was already **ANSWERED** 2026-09-12 for the most-shared globals: "`mp_map_set_angle/x/y/z` are the turn/look verbs' scratch target …; `mp_last_weather` caches `getweatherslot()` …; `quest_global_flag[94]` holds per-quest counters and bit flags …"; `VARS:266` points to it ("meanings are FZ-27"). `VARS:327` still: "What a `global` at a given offset means \| **not established** \| — \| UNKNOWN" | Meanings of the other declared offsets (587 in all, `VARS:124`). These are script data, not engine behaviour. · **DATA** · REG `FZ-27` **ANSWERED** (named subset) |
| S-8 | which fields share a persistence group id | **OPEN** | `VARS:180`: "Which fields share which group id is authored in that file and not decoded here" | The census of group ids over the field records. · **DATA** · no row |
| S-9 | does any shipped array have a dimension of 0 or less | **OPEN** | `VARS:88-89`: "whether any shipped array has a dimension of 0 or less is not claimed" | As stated. · **DATA** · no row |
| S-10 | the value-stack `+0x44` byte; the `+0x84` array | **CLOSED** | `VARS:469`: "*(corrected 2026-10-02, OPUS: `PUSHV`'s value is always 6 — the resolver writes `+0x00 = 6` at `00262667` on its only exit — and the one other value source is `PUSHP`, which stores the descriptor's width nibble 0..5 there (`00268118`–`00268150`, `00268185`); one reader, `00263450`, called from `00353D10`)*"; `C-BR:325` "*(answered: …)*"; `+0x84`: `C-BR:116`/`:357` "written 0, never read" (PROVEN) | Nothing. Two lines still print the old "unknown": see N-2. |
| S-11 | does any handler read `begin`'s fifth (stack) argument | **OPEN** | `C-VD:160-161`: "**Whether any of the 1,960 handlers reads it is unmeasured; the ABI is in the image either way**" | The measurement. A port can simply pass the manager. · **STATIC** · no row |
| S-12 | no live observation of the dispatcher or any verb | **OPEN** | `C-VD:387`: "**The live half, still queued and still unperformed:**"; `C-VD:311`: "**Evidence class: isolated original-code. There is still no live evidence.**"; `C-BR:321` | One live capture. · **RUNTIME** · no row |
| S-13 | parity dimensions not constructible offline; drive and interpreter never run | **OPEN** | `C-VD:598`: "**Not constructible offline, and why:**"; `C-VD:635-636`: "**Links 4 and 5 — the 1,228-byte drive and the interpreter — have never been run**" | As stated. · **RUNTIME** · no row |
| S-14 | whether `POPV`'s `rsp+0x50` field is the caller-visible return | **OPEN** | `VD:1423`: "Whether the `rsp+0x50` field is the caller-visible return is not proved here." | As stated. · **STATIC** · no row |
| S-15 | the three empty records `0x0330`, `0x0356`, `0x03B0` | **OPEN** | `WAIT:232`: "UQ-65 is SUPERSEDED as a duplicate of CR-2, closed NO ADMISSIBLE SOURCE"; `WAIT:182-183`: "They are recorded as unverified candidates; no instruction-boundary decode was run on them." | Behaviour is a stated limit (no implementation, no caller: REG `CR-2`). The two candidate script matches still need a decode. · **STATIC** (the decode) · REG `CR-2` bounded; `UQ-65` SUPERSEDED |
| S-16 | `003B6F60`, `003B7D30` unread | **OPEN** | `WAIT:342-343`: "What `00314D40`, `003B6F60`, `003B7D30`, `003B7180` and `00237D60` do — **the result bodies were read, their callees were not.**" `003B7180`'s own callees are now named (`WAIT:373`), not these two. | The bodies of `003B6F60` and `003B7D30`. · **STATIC** · no row |
| S-17 | what the other 71 callers of the skip-mask reader `00267310` do with the mask | **NARROWED** | `NCL:640`: "what each of the other 71 does with the mask is not claimed." New body sentences on `VD` give four of them: `0034C570` (`VD:1437`), `00353D90` (`VD:1439`), `003563D0` (`VD:1507`), `00356990` (`VD:1509`), e.g. `00353D90`: "tests `00267310(byte +0x15 of rdx)` and on both paths pops one value through `00267E10(r9)` and discards it; when the test is non-zero it calls `002E2440(1, 0)` …" | The other 67. · **STATIC** · REG `OV-15` ANSWERED covers the mask itself |
| S-18 | dispatch-table residual: a compensating pair of shifts | **OPEN** | `DT:979-980`: "**The honest residual:** a *compensating pair* of shifts — one skip and one re-add — falling entirely inside a single anchor-free window could not be seen." | As stated. · **STATIC** · `I-6` |
| S-19 | name-binding sub-record `+0x30`, `+0x58`; writer of `+0x3C` | **OPEN** | `NAMES:235`: "UNRESOLVED (allocator zero only); `+0x3C`'s writer is not among the 16 RIP-relative" | As stated. · **STATIC** · no row |
| S-20 | the 997-byte part-slot function's 15 callees | **OPEN** | `NAMES:466`: "Its 15 callees were not read." | As stated. · **STATIC** · no row |
| S-21 | bridge §14 residue: pop asymmetry reason; values below arguments; other wrappers; single-threaded use | **OPEN** | `C-BR:332-336`: "3. The reason for the two pop helpers' unknown-tag/underflow asymmetry remains distinct from the established branch behavior. 4. … Authored reachability and safe caller discipline remain open. 5. All other command wrappers and native services"; `C-BR:211`: "**single-threaded use is assumed by the code and not proven here.**" | As stated. Item 5 is G-1. · **STATIC** · no row |
| S-22 | EF-2 residue: 35 register-sourced `+0x11` stores on untyped bases | **OPEN** | `CC:735-737`: "`EF-2`'s separate residue is **35 register-sourced stores at displacement `0x11` on untyped bases**, and it is not re-examined here." | As stated. · **STATIC** · REG `UQ-54` ANSWERED (producer side), `EF-2` |
| S-23 | `00268D10`'s calls to `00377700` and `00317E60`; WorldAreaField edges from `00394130` | **OPEN** | `CC:746-747`: "`00268D10` calls `00377700` at `00268E11` … This section does not say what that call does."; `CC:749-750`: "are **not** dispositioned here"; `CC:753-754`: "this section makes no claim about the call." | As stated. · **STATIC** · no row |
| S-24 | the 37-verb spawn vocabulary is a floor | **OPEN** | `CC:403`: "**37 is a floor, not a ceiling**" | The indirect callers. · **STATIC** · no row |
| S-25 | `DO-1`: begin and poll handlers recorded, not classified | **WRONG-IN-PASS-1** | REG `DO-1`, before pass 1: "**ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): … the census was done anyway; all 505 handlers are in members/dispatch-secondary-handler-shapes.tsv.**" | Nothing. `POP` was not updated: see N-8. · REG `DO-1` **ANSWERED** |
| S-26 | the verb-reach census reads no handler body; 1,029 blank verbs need handler reads | **OPEN** | `REACH:4`: "the handler bodies are not read (UQ-57, SUPERSEDED as a duplicate of CY-3, itself SUPERSEDED under the class-1 ruling: this census's declared scope)"; `REACH:239-240`: "for the 1,029, reading the handler is the only route." | It is G-1 seen from the census, and the register makes it a declared scope. · **STATIC** · REG `UQ-57`, `CY-3` **SUPERSEDED** |
| S-27 | battle party: roster mutators, lock routine, preamble routine, flag setter unread | **NARROWED** | Flag pair now stated: `BP:56`: "*(answered: `003601B0` / `003601C0` set and clear bit `cl` of `022CB720` …)*". The preamble verbs are now named, `BP:56`: "`setbattlemember`, `setbattlememberone` and `addguestbattlemember`". New bodies `0034CDF0`, `003596B0`, `003596D0`, `00359740`, `00359BA0`, `00359C00` (`BP:173-178`). Still `BP:127-129`: "**Not read:** the roster mutators the begins end in (reconcile, demote, move-out, the two removers); the lock routine `setbattlememberlock` ends in; … the per-actor routine … the three preamble verbs … call first." | The roster mutators, the lock routine and the per-actor preamble routine. · **STATIC** · no row |
| S-28 | party read-in: pointer writes into `02EBF3D0`–`02EBF3FF` not excluded | **OPEN** | `READIN:226`: "Writes through a pointer into `02EBF3D0`–`02EBF3FF` were not excluded." | As stated. · **STATIC** · no row |
| S-29 | party appearance: what the `m[+0x08]` bits 1–2 pair selects; the third and fourth states of the `+0x304` field | **OPEN** | `LOOKS:390`: "**What the flag pair in `m[+0x08]` bits 1-2 selects.** The write is exact; the meaning is not."; `LOOKS:294-296`: "a third and fourth state exist that this verb cannot reach" | As stated. The map-1 half of SP-1 is closed (RC-18, `LOOKS:409`). · **STATIC** · REG `SP-1` "ANSWERED (the band); map-1 residue" |
| S-30 | standard motion: values the shipped scripts pass; whether a shipped script hits the SP-2 window | **OPEN** | `STDM:216-217`: "Which values the shipped scripts pass is a question about the script data, not the executable."; `STDM:213-214`: "the mechanism is proven, the divergence not demonstrated." | Both are script censuses. · **DATA** · REG `SP-2` "ANSWERED (static); live demonstration residue" |
| S-31 | debug companions: escape semantics, unpinned arities, q3's X, `.mld` | **OPEN** | `ATEL:715-716`: "Per-`cmd` escape semantics and the kanji-plane assignments are **not decoded**"; `ATEL:617`: "`18` … arity unpinned"; `ATEL:810`: "*OUT OF EVIDENCE BOUNDARY 2026-09-29 (OPUS) … What X counts is not claimed.*"; `ATEL:891-892`: "What the `.mld` files hold … is not claimed." | Not needed for a port of the shipped game (`ATEL:881-887`). X is now a declared out-of-evidence limit. · **DATA** · REG `SN-1` |

### 2.2 Structural gaps (pass-1 G-1 to G-18)

| id | gap (short) | verdict | evidence now | still missing · class · register |
|---|---|---|---|---|
| G-1 | **the verb bodies** ("**1,886 distinct functions** serve as callbacks", `VD:552`) | **NARROWED** | About 140 function bodies have gained a one-sentence description on this folder's pages since pass 1. The largest blocks are `VD:1427-1440` (interior citations, 8 bodies) and `VD:1442-1533` ("Homed bodies: functions reached only indirectly whose callees this page cites", about 88). There are also 6 on `NCL` (`NCL:803-813`, each tied to its dispatch record, e.g. `00341D00` "is the result callback of command id 0x01D7"), 9 on `BP:166-187`, 20 on `READIN:409-441`, 3 on `LOOKS` (`0x04E7`, `0x003B`, `0x04B4`), and 8 on `CC`. The sentences "state what the body does (access and representation, not purpose)" (`VD:1444`). | Most of the 1,886 bodies are still undescribed. Of those now described, most name their callees only as "the call at `X+0xNN`", and the homed ones do not say which verb reaches them (N-9). The README still does not say which category owns the verb bodies. · **STATIC** · REG `CY-3` SUPERSEDED (declared scope) |
| G-2 | opcode semantics for about half the 100 opcodes | **OPEN** | `INT:260-262`: "*ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: all 100 handlers are read, here or on the cited pages, and [the BF-1 opcode table](../../_index/candidates/bf1-opcode-semantics/README.md) gives each one's effect*" | No page in the folder states the semantics of `0x04 SYSTEM`, `0x05`–`0x09`, `0x10`–`0x14`, `0x17`, `0x18`, `0x1D`–`0x20`, `0x2A`–`0x2C`, `0x2E`–`0x31`, `0x33`, `0x34`, `0x35`, `0x52`–`0x56`, `0x5A`–`0x5C`, `0x62`. The table exists only in a candidate directory, which the page points to. · **DOC** · REG `BF-1` **ANSWERED**, `OV-13` ANSWERED |
| G-3 | arithmetic typing per opcode | **NARROWED** | `INT:114`: "*~~so the bytecode is integer-encoded and the arithmetic is float~~ but the arithmetic is typed by its operands: two int32 add and subtract as integers, anything with a float as float32* *(corrected 2026-10-02, OPUS: `0x12` takes its integer path when both tags are 1, `0025ECBA`–`0025ECD8`; `0x13` `0025EEA0 sub ecx, ebx` against `0025EF6B subss` …)*"; `C-INT:81-83` agrees | Typing is on a page for add and subtract (`0x12`, `0x13`) and for the compare and divide group only. Multiply, the logic, bitwise and shift operators are typed only in the BF-1 candidate. REG `BF-1`: "(int, with float paths for add/sub/mul/div; OPDIV guards zero, OPMOD does not …)". · **DOC** · REG `BF-1` ANSWERED |
| G-4 | `0025B400` (the yield point) body undescribed | **WRONG-IN-PASS-1** | `VARS:537` already stated the body at pass 1's snapshot (checked against `86b70c69`): "`WorldActorScriptVM_ServiceRequestWaitState` — the `wait`-family poll: request slot `[+0xA8] + byte[+0x11] × 40`, if `+0x14 == 4` computes `pending − [+0x58]` elapsed and calls `003DC050`; `0xFF` → keep waiting (return 1), else `003DB2A0` and mark `+0x14 = 1`"; `CC:584` gives its `+0x11` load as `movsx` | Nothing. `INT` itself (`INT:117`, `:251`, `:475`) does not point to `VARS:537`. |
| G-5 | the driver beyond its kind table; kind 2; footer test; the "active-actor global" | **OPEN** | `REQ:155`: "\| 1 / 2 \| Original interpreter \| Opcode/command semantics \|" (kind 2 is still not told apart from kind 1); `C-INT:135`: "it clears its active-actor global afterward" (no address). REG `OV-11`: "in-frame order is the field-pass page sections 4-5" (04 category) | What kind 2 does differently, if anything; the active-actor global's address; the driver's other arms, if they are not on the 04 page (not audited here). · **STATIC** (part DOC) · REG `OV-11` ANSWERED |
| G-6 | interpreter return values: no complete taxonomy | **OPEN** | `C-INT:63`: "This is not a complete error/success taxonomy." | As stated. · **STATIC** · no row |
| G-7 | the mode-1 start arm `00263230`; `0025B580(target)` after a submit | **NARROWED** | `BIND:405-407` (corrected 2026-10-02): `00263230` calls `00226BE0`, "the system-stop registry's request start for channel 6 … *(corrected 2026-10-02, OPUS: it ORs the bit into `01FD46D4` (`00226C7A`), raises `01FD46D0` (`00226C87`) and marks every actor's stop masks …; the call at `002632AD` passes `ecx = 6`)* … the entry-start path ~~consults the input channel state~~ raises a system stop request" | `00263230` as a whole: when the mode-1 arm runs and what else it does (only two of its callees are described, the other being `002EC380`, `BIND:496`). `0025B580` is still undescribed: `BIND:191` names it, and `25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md:585` lists "what `0025B580` does after a submit" as open. · **STATIC** · no row |
| G-8 | what a push writes at `+0x44` and whether anything reads it | **CLOSED** | as S-10: 6 from every push and `PUSHV`, the width nibble 0..5 from `PUSHP`; one reader `00263450` (`VARS:469`; `C-BR:117`) | Nothing for a port. |
| G-9 | per-command scratch shapes | **OPEN** | `C-NCL:220`: "- Other commands' scratch shapes, service effects, polling conditions and resource ownership." | As stated. Some new body sentences show scratch use (e.g. `0034CDF0`'s state dword at `[r8]`, `BP:173`), but no census exists. · **STATIC** · no row |
| G-10 | the partition of the 1,960 commands | **OPEN** | `VD:604`: "**327 verbs are durative, ~~1,573~~ 1,571 are instantaneous** *(corrected 2026-10-02, OPUS: plus `0x0297` and `0x20B5`, which carry a `poll` and can block, CZ-1)*"; `VD:1271-1274`: 1,571 / 250 / 77 / 29; `VD:1350`: "no handler at all \| 4" | 1,571 + 2 + 250 + 77 + 29 + 4 = 1,933, so 27 of the 1,960 are still in no row. No page gives a partition that sums to 1,960. · **STATIC** · no row |
| G-11 | notification ids from `0032F240` for the voice verbs | **OPEN** | `VARS:309-311`: "**every slot's enable byte is `0` and `0032F240` returns `-1` for all five.** The notification is a runtime registration, not authored data" | As stated. · **RUNTIME** · no row |
| G-12 | entity names: `002650B0`'s host object and six pools; the fourteen bind keys; the `.rdata` constant; the list-head map; `0050D810`'s verb id; `0037B4D0` as a bind caller | **WRONG-IN-PASS-1** (in part) | The host object was already answered at pass 1's snapshot, `CC:247-248`: "**`EF-3` ANSWERED 2026-09-11 (FABLE):** `002640C0` returns the current actor-manager slot block, the qword at `02099D70`". The six pools are the variable storage homes (`NAMES:404-410`, matching `VARS:122-129`; class 1 re-derived in the new `VARS` section at `VARS:619-622`). The key opacity is a stated design: `NAMES:344`: "**The key is opaque and must stay that way.**" | Still missing: the `.rdata` constant multiplied with `0x09000707` (`NAMES:244`: "`0x09000707` × a `.rdata` constant → `+0xE4`", no address); the full list-head map in one place; `0050D810`'s verb id (`NAMES:441` gives only "`.data@01F26740`"); what `0037B4D0` does as a bind caller (`NAMES:442`). · **STATIC** · no row |
| G-13 | party read-in: the verb-mode byte `02EBF3FC`; the state-2 and state-22 chains; `0037C2E0`; the `highmodelreplace.bin` lookup; `00233AA0`/`00233CF0` constituents; the shared poll `0034E3E0` | **NARROWED** | The shared poll is now described, `READIN:417`: "`0034E3E0` \| 40 B \| calls `0037CB50` (incoming registers passed through); when it returns non-zero, returns 0, otherwise calls `00314D40(1)` and returns 1". Its end test is `0037CB50` (`BP:179`). The installer is described at `READIN:420` (`0037C980` "stores … 1 at byte `02EBF3FC`") | What `02EBF3FC` changes inside `0037B4D0` (only its writers are stated: `READIN:75`, `:254`, `:420`); the state-2 and state-22 chains are still address lists (`READIN:103`, `:119`); `0037C2E0`; the `highmodelreplace.bin` lookup ("22 records, `(a,b,c)` keys", `READIN:189`). · **STATIC** · no row |
| G-14 | battle party: the `setbattlemember` reconcile; the add routine behind `0034C370`; `00324360` | **NARROWED** | `BP:172`: "`00324360` \| 23 B \| calls `0037CB50()` and returns 1 when its result is non-zero, otherwise 0"; `0037CB50` at `BP:179` | The reconcile and add routines are among the roster mutators that are "Not read" (`BP:127`). · **STATIC** · no row |
| G-15 | standard motion: what a motion id selects; the `00427860` commit | **OPEN** | `STDM:152`: "For `002EB4F0` the blend is not consulted and `00427860` commits instead." | Both. · **STATIC** · no row |
| G-16 | party appearance: `002E8FD0`'s visibility gates via `00428E10`/`00428DE0`/`00429020`; `002367A0` | **OPEN** | `LOOKS:580-582`: "`00428E10`/`00428DE0`/`00429020` write the per-record visibility flags, with `[+0x284]` as the present-check." (the render base is corrected to the pointer at `022C6F28`, `LOOKS:579`); `LOOKS:334`: "`002367A0` \| `BattleUnit_FindByDefinitionSelector` \| 126 B \| id -> unit" | Which flags the three setters write and what each gate tests. · **STATIC** · no row |
| G-17 | spawn native targets (`002366E0`, `002354F0`, `00235360`, `002391C0`, `0023A3B0`, `00239840`, `0023A2E0`) | **OPEN** | `CC:158-165` names them; `CC:303-306` points to the 05 spawn pages. Every one of the seven appears on a 05, 04, 08 or 11 page (for example `05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md` names six of them), not audited here | The verb pages do not carry the effects. Whether the pages they point to describe the effects completely was not checked here. · **DOC** · no row |
| G-18 | `setuptreasure`'s callees and the bind's tail callees | **OPEN** | `NAMES:139-148` (`0026E060`, `0026A320`, `0026AF80`, `0026DAC0`); `NAMES:245-248`, `:261` (`00269E60`, `0026B2E0`, `0026A370`, `00426C90`, `00263A30`) | Not described in this folder. `0026A320`, `0026E060`, `0026B2E0`, `00426C90`, `00263A30` and `0026AF80` appear on 04, 06 and 17 pages (not audited). `0026A370` and `00269E60` appear on no page outside the folder. · **STATIC** (part DOC) · no row |

### 2.3 Pass-1 value contradictions (C-V1 to C-V60): follow-up

Pass 1's §3.1 listed 60 value-changing disagreements. Its rating asked for a local check of nine of them (C-V2,
C-V3, C-V8, C-V12, C-V15, C-V17, C-V20, C-V21, C-V22). **All nine are now resolved on the pages.**

**Resolved (41).** In each case the stale side is now struck or annotated with a dated correction, nearly all
"*(corrected 2026-10-02, OPUS: …)*":
- C-V1 (`INT:150-154`);
- C-V2 (`INT:114`);
- C-V3 (`REQ:246`, row A1: "`sx(byte[actor+0x11])·0x28`");
- C-V4 (`BIND:431`, `:440`, `:447`: 210 B, `00358A00` ends at `00358A14`, 545 B);
- C-V5 for the value (`BIND:79`, `BIND:4`; the stale text is N-1);
- C-V7 (`BIND:405-407`);
- C-V8 and C-V9 (`DT:642-646`, `:762-776`, `:830-836`, `:855-860`);
- C-V10 (`DT:752-753`);
- C-V12 (`VARS:469`, `C-BR:117`);
- C-V13 (`VD:208`);
- C-V14 (`VD:242`, `C-VD:147`);
- C-V15 (`C-VD:175`: "(u32)");
- C-V16 (`VD:726`, `:1058`, `:1242`);
- C-V17 (`VD:677-679`);
- C-V18 (`VD:229-230`, `:604`);
- C-V19 (`CC:29-30`, `C-BR:205-206`);
- C-V20 and C-V21 (`C-BR:266-268`, `:358`, `CC:216`, `CC:442-450`: both `0026230B` and `00261B97` write `1`);
- C-V22 (`C-BR:396-398`);
- C-V23 (`VARS:254`);
- C-V24 to C-V26 (`WAIT:239-241`, `:126`, `:373`, `:383`);
- C-V28 (`NAMES:242`);
- C-V32 and C-V33 (`READIN:352-354`, `:62`);
- C-V35 (`LOOKS:579`, `:636`, `READIN:160`: the base pointer is *held* at `022C6F28`);
- C-V37 (`STDM:485`);
- C-V38 (`BP:56`);
- C-V39 (`READIN:74`);
- C-V40 (`STDM:491-494`);
- C-V42 (`C-NCL:282`: "built, once");
- C-V43 (`NCL:777`);
- C-V46 to C-V49 (`README:22-23`, `VD:36-38`, `:592`, `:1160-1162`, `:1221`, `:672`);
- C-V51 and C-V52 (`DT:389`, `DT:198`, `C-BR:205`);
- C-V55 (`VARS:152`).

**Still open (19).** None has a dated settlement. "Unstruck stale side" means a correction exists elsewhere but this
line was not amended.

| id | what | current text | class |
|---|---|---|---|
| C-V6 | width of actor-entry `+0x06` | `BIND:70` "`u8` party code" against `BIND:76` "the `u16` ff12-script writes as `pcId`" | STATIC |
| C-V11 | does an out-of-range command fail closed | `VD:170-172` and `NCL:232-233` still say "fails closed"; `C-VD:112` "the guard is ONE-SIDED" (signed compare). Favoured side B (2026-09-12); stale side unstruck | DOC |
| C-V27 | width of the entity stamp | `NAMES:285` "a stamp that is sixteen bits wide" against `NAMES:316-317` "The stamp is a full `dword`" and `NAMES:552` "a **dword** load" | STATIC |
| C-V29 | which verbs call the bind `002E28E0` | **narrowed**: three of the six bind-verb callbacks named at `NAMES:454-455` now have bodies (`READIN:429` `00344550`, `:430` `00345A60`, `:432` `003463F0`), and none of the three calls `002E28E0` (they call `002EBC90` and `002E3110`, or a site-relative callee). `NAMES:46` still lists "the whole *bind* family" | STATIC |
| C-V30 | where `requestMask` lives | `NAMES:206` "`+0x28` requestMask" against `NAMES:599` "`[r10+rax*4+0x48]` requestMask" | STATIC |
| C-V31 | size and first field of the read-in record | `READIN:36`, `:59` "12 bytes" against `READIN:141` "size `0x18`" | STATIC |
| C-V34 | `VM_Spawn_ApplySelectedUnit`: `00510160` or `005101B0` | `READIN:79`, `:204` against `READIN:336`, `CC:162` | STATIC |
| C-V36 | the movement-context offset written by `002E5C90` | `LOOKS:395` gives both `[actor+0xB8]` and "the 0x230-byte context at actor `+0x120`" in one sentence | STATIC |
| C-V41 | is a running command polled every frame | `NCL:54-55` "polled every frame", `NCL:182` "once per frame per actor" against `NCL:547` "Invocation count is not automatically live frame count." and `C-NCL:195`. Favoured side B; stale side unstruck | DOC (side B) / RUNTIME (the actual rate) |
| C-V44 | debug companions: corrected narrowings still unstruck | **in part**: the `.sbn` trailer, the `.dbg` header pairs and q0's 1-based line numbers are corrected at `ATEL:805-806`. Still unstruck at `ATEL:806`: "btlctrl index `N` ↔ `global_debug_flag[N+34]`" (against `ATEL:210`) and "T3/T4/T8/q1 land mid-string" (against `ATEL:391`); at `ATEL:807`: "T1 RESOLVED 2026-09-22 (SWE2-DATA): it is the ATEL verb-category directory." (against `ATEL:235`) | DOC (debug only) |
| C-V45 | debug-companion figures | **in part**: the `003306E0` size (`ATEL:917`), the S2 shape (`ATEL:387`) and the `btlctrl` heap start (`ATEL:393`) are corrected. Still `ATEL:264` "143 bytes" against `ATEL:273` "144 bytes", and `ATEL:302-304` "**no variable names at all**" against `ATEL:400` "exactly its `@`-labels and named variables" | DATA (debug only) |
| C-V50 | adapter-family counts | `POP:158` "1,053 of the 1,682 frontier callbacks" against `POP:25` "… \| 1030" | STATIC |
| C-V53 | single-callback and instantaneous counts | `NCL:117`, `:341` "1,155 of 1,496"; `NCL:492` "**1,573 of the 1,960 commands**". These were not carried over from the 2026-10-02 corrections at `C-NCL:133` ("family 0 has 1,288 single-callback records") and `VD:229`, `:604` (1,571) | DOC |
| C-V54 | two different lists both called "the authored catalogue" | `NCL:243-244` "(… 1,960 ids)" against `NCL:276` (1,954 entries, AO-5) | DOC |
| C-V56 | registers read before write | `INT:908` "172 functions in 84 scripts" against the TSV's 96 scripts | DATA |
| C-V57 | `param_types` of the single-int verbs | `CC:343` "**`0x10`** for the single-int verbs" against the verb table | DATA |
| C-V58 | ActorEntity reach count | `REACH:337` "**162** against 142" against `REACH:358` (RC-21: 135–154) | DOC |
| C-V59 | read-in transition sites | `READIN:108`, `:111`, `:112` against `members/party-read-states.tsv` | STATIC |
| C-V60 | battle-party body count | `BP:9` "eleven bodies", and the list that follows names twelve | DOC |

---

## 3. New gaps

Gaps found on this pass that pass 1 did not list. Most come from text added since 2026-10-02.

| id | gap | class | evidence | register row |
|---|---|---|---|---|
| N-1 | **Two lines on `BIND` still say the RC-12 adjudication is pending**, and one still says the wait resolver tests `mapjump`, against the page's own status line and the register | DOC | `BIND:236` (added 2026-10-02): "*(answered on ORACLE's record: RC-12, 2026-09-30, section 7 — FABLE's adjudication of the numbering is still pending; 2026-10-02, OPUS)*"; `BIND:299`: "**FABLE adjudication pending**"; `BIND:298`: "wait resolver's `mapjump` test is §2.6"; against `BIND:4` and REG `RC-12` ("Restated 2026-10-03 on FABLE's adjudication at `a8aed6ca9`") and `BIND:79` ("word `+0x18` is `special[11]`, the actor's `parameter` function") | `RC-12` ANSWERED |
| N-2 | **The value-stack `+0x44` and `+0x84` meanings are still printed as unknown** on two pages, against the 2026-10-02 answers | DOC | `C-BR:356`: "\| `+0x44` source-kind \| direct pushes store6; … complete enum remains unresolved \| existing scoped evidence \| NOT universally resolved \|"; `CC:217`: "both pushes store **`6`** — meaning unknown"; `CC:218`: "both pushes store **`0`** — meaning unknown"; against `C-BR:117`, `C-BR:325`, `VARS:469` (two-valued; one reader `00263450`) and `C-BR:116`/`:357` (`+0x84` "written 0, never read") | none |
| N-3 | **The flags helper the removal crosses for entry flags 2 and above is unread, and its pointer leads nowhere.** `REQ` says its address is on "the binding-and-channels page", but `BIND` names no helper for `+0x12`: it states only bit 0, "always 1 here" | STATIC (and DOC for the pointer) | `REQ:102-103`: "The removal past the attempt is opaque for entry flags 2 and above (a flags helper whose effects are not read; its address is on the binding-and-channels page)."; `REQ:130-131`: "(2 and above also cross a flags helper whose effects are not established)"; `BIND:161`: "\| `+8` flag \| `+0x12` bit 0 \| always 1 here (`002689C0`) \|" | none |
| N-4 | **Whether any authored scene cancels a mode-3 (`REQEW`) entry** through the `freqcancel` verbs, which would make the new end-notification-without-RET path reachable | DATA | `REQ:104`: "**Still open:** whether an authored scene cancels a mode-3 entry; natural interleaving; same-key re-entry; the scheduler's own effects."; REG `OV-16` counts the verbs: "the shipped scripts call `freqcancel` / `freqcancel2` 84 times, 77 of them `freqcancel(0)`" | `OV-16` OPEN (its static half covers the verbs, not the mode-3 pairing) |
| N-5 | **The request scheduler `003DB6E0`'s own effects after a cancel**, including the stated NULL-actor read | STATIC | `REQ:100-101`: "After a NULL actor both verbs still tail-jump to the request scheduler `003DB6E0`, which reads `[rcx + 0x63]` without testing rcx."; `REQ:104`: "the scheduler's own effects" | none |
| N-6 | **The insertion helpers' success and effects on a non-`0xFF` free head** (the notification allocation path) | STATIC | `REQ:140-141`: "**Still open:** … the insertion helpers' success and effects on a non-`0xFF` free head." | `OV-10` (adjacent) |
| N-7 | **The `029A` → `029B` out-reference flow's open items**: the initial queue order, native writers of the destination cells, the image buffer's allocation and lifetime, and what action word 0 means | STATIC (queue order, writers); DATA (action word 0) | `CC:878-882`: "**OPEN, as SWE2-DATA states them:** the initial queue order (`022C2178` at init); native writers of these cells outside the bytecode; allocation, non-aliasing and lifetime of the image buffer against the queue globals; the meaning of action word 0."; `VARS:634-635`: "It does not establish the context base's value, the image's allocation or lifetime, or native writers of the cells outside the bytecode." | no row names `022C2178`; `OV-42` PARTLY ANSWERED is the nearest |
| N-8 | **`POP` still says `DO-1` is open and growing**, although the register answered it before pass 1 | DOC | `POP:473`: "`DO-1` stays open and gets larger."; `POP:271`: "unclassified** — `DO-1`."; against REG `DO-1`: "**ANSWERED 2026-09-26 … all 505 handlers are in members/dispatch-secondary-handler-shapes.tsv.**" | `DO-1` ANSWERED |
| N-9 | **The new homed handler bodies do not say which verb reaches them, and name most callees only by call site.** A re-implementer cannot attach them to a verb id, and the callee is not described. By contrast, the `NCL` rows give the dispatch record | STATIC | `VD:1444`: "*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers.*"; e.g. `VD:1453` `00511200`: "makes the call at `00511200+0x3F` with (c, b, a)"; `VD:1477` `0034A920`: "loops forever calling `00267F90(r9, 2)`; it has no exit path" (reaching record not given); the same form at `READIN:422-441` and `BP:181-187`. The `NCL` form, for contrast: `NCL:808` "reached through the result field (`+0x20`) of record 0x1D7 … so it is the result callback of command id 0x01D7" | `CY-3` SUPERSEDED (scope) |
