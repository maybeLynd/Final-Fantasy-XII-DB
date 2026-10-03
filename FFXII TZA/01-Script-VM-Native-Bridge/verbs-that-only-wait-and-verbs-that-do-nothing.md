---
system: The script verbs that only wait, and the ones that do nothing at all
category: 01-Script-VM-Native-Bridge
status: AUDITED
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-wait-and-stub-verbs-pass-1 - the 26 and the 3 reproduce set-for-set and the nine stub rows address for address; CORRECTED: the stubbing is in begin and poll only, and three of the nine still run a result (003447F0 sets the FF12CONFIG useHdd global, an answer stranded on the config page), 0034E3E0 is shared by four verbs not two, 005C5230 is the poll of nine including callgameover which has a real begin, and a 0016D6A0 result marks 'no value to push' in four ordinary verbs
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The script verbs that only wait, and the ones that do nothing at all

> Thirty-eight of the game's script verbs have no code that *does* anything. **Twenty-six of them are
> not broken — they are pure waits.** Nine are PlayStation-era leftovers stubbed out for the PC
> release. Three are simply empty.

## 1. What the player sees

**Almost every cutscene in FFXII is built out of pairs.** Something is started — a character walks, a
camera swings, a movie begins, a music track streams in — and then the script **waits** for it to
finish before the next line runs. That waiting is a verb in its own right, and there are twenty-six
of them: `movesync` waits for a move, `turnsync` for a turn, `movieplaysync` for a movie,
`bgmstreamplaysync` for a music stream.

**A separate group does nothing at all, and they are the game's own history.** FFXII: The Zodiac Age
is a PC release of a PlayStation 2 game that passed through a PlayStation 3 remaster, and a handful
of verbs from those machines survive in the script vocabulary with their bodies removed —
`hddinstall`, `networkhddinstall`, `hddmount` (installing to a console hard disk) and the `atrac3`
family (Sony's audio codec). **A zone script can still call them. On PC they return immediately and
change nothing.**

The important part for anyone editing scripts: **the stubbed verbs do not hang.** They report
"finished" the instant they are asked, so a script that calls `hddinstall` runs straight through it.

## 2. Native mechanism

### Three populations, by callback shape

A family-0 command is three callbacks — `begin`, `poll`, `result` — in one record. Which slots are
filled says what kind of verb it is.

| population | shape | count |
|---|---|---:|
| **pure waits** | `poll` only | **26** |
| **fully empty** | nothing at all | **3** |
| **retail stubs** | slots filled with `ret`-only bodies | **9** |

### The pure waits — `poll` only, and it is the correct shape

A `*sync` verb has **nothing to begin**, because the thing it waits for was started by an *earlier*
verb, and **nothing to return**. It needs only the per-frame question *"is it done yet?"* — which is
exactly the `poll` slot.

**Their polls do real work.** `movesync`'s poll (`00356A90`) tests the actor pointer and calls
`0x00264E10`; `gillwinsync`'s (`0034D4C0`) is the whole idiom in seven instructions:

```asm
0034D4C0  sub  rsp, 0x28
0034D4C4  call 0x2E2520          ; ask the subsystem whether it has finished
0034D4C9  xor  ecx, ecx
0034D4CB  test eax, eax
0034D4CD  sete cl                ; keep waiting <=> the call returned 0
0034D4D0  mov  eax, ecx
0034D4D6  ret
```

**A poll returns non-zero for "still running" and zero for "done"** — established from `wait`'s own
poll in [`Native-Command-Lifecycle/native-command-lifecycle.md`](Native-Command-Lifecycle/native-command-lifecycle.md).

> **This closes `CE-1`**, which asked how a command *"that can only be polled, never begun, and never
> producing a result"* could make sense. **It is not an anomaly — it is what a wait looks like when
> the thing waited on was started by a different verb.**

The twenty-six: `movesync` `turnsync` `stdmotionreadsync` `crossfadesync` `gaugeshowsync`
`resumebehindcamerasync` `summonreadsync` `summontopartyreadsync` `behindcamerafovyrollsync`
`vibsync` `lookatsync` `spattackwindowsync` `actoriopvoicereadsync` `entryreadsync`
`behindtoeventcamerasync` `moviestandbysync` `movieplaysync` `bgmstreamreadsync` `bgmstreamplaysync`
`gillwinsync` `ucmovesync` `atrac3standbysync` `atrac3playsync` `initsync` `musicfadeoutsync`
`unkCall_5a6`.

**Shared polls**, which is a fact about the engine rather than the catalogue: `summonreadsync`
and `summontopartyreadsync` both poll `0034E3E0` — **and so do `partyallread` (`0x3EB`) and
`partyallread2` (`0x46F`), which also share the result `0034D460`, so it is a quartet and not a
pair (§7)**; `atrac3standbysync` and `atrac3playsync` both poll `005C5230` — **the stub**, which
is why they are also in population three.

### The retail stubs — and why they complete instead of hanging

Two bodies do all the stubbing:

```asm
0016D6A0   C2 00 00      ret 0        ; the /OPT:ICF-folded no-op
005C5230   33 C0 C3      xor eax, eax ; ret  -- returns 0
```

**`005C5230` returning 0 means "done"**, so a stubbed verb's poll reports completion on its first
frame. **That is the difference between a removed feature and a hung script.**

| verb | begin | poll | result | what it was |
|---|---|---|---|---|
| `disposesummon` | `0016D6A0` | `005C5230` | `0034FB20` | — |
| `changetonormalparty` | `0016D6A0` | `005C5230` | `00350F30` | — |
| `hddinstall` | `0016D6A0` | `005C5230` | `003447F0` | console HDD install |
| `networkhddinstall` | `0016D6A0` | `005C5230` | `003447F0` | **same result body as `hddinstall`** |
| `hddmount` | `0016D6A0` | `005C5230` | — | console HDD mount |
| `moveblurfadesync` | `0016D6A0` | `00345100` | `0016D6A0` | — |
| `atrac3play` | — | — | `0016D6A0` | Sony ATRAC3 audio |
| `atrac3cancel` | `0016D6A0` | `005C5230` | — | Sony ATRAC3 audio |
| `unkCall_5c7` | — | — | `0016D6A0` | — ~~takes **2** arguments~~ the catalogue declares 2 arguments; the handler (`ret 0`) consumes none *(corrected 2026-10-02, OPUS: `0x05C7` has only the result `0016D6A0`; the CONFLICT note in §7)* |

**`hddinstall` and `networkhddinstall` share a result body**, so whatever remains of them is one
function serving both.

> `0016D6A0` is the linker-folded `ret 0` this database already documents under three other
> identities — the CFG check, an array-element destructor and a retail-stubbed frame-phase marker.
> **This is its fourth role**, and it is the clearest illustration of why the fold cannot carry a
> single name: see [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md) `B-2/a`.

### The three that are empty

`setnorecovertelepostatus` (`0x0330`), `battlemembersync` (`0x0356`) and `restartbattle` (`0x03B0`)
have **no begin, no poll and no result** — the only three family-0 records with every slot null. All
three are `cat_known: False`, so their names come from outside the ff12-script catalogue.

**A call to one of them dispatches into a record of nulls.** ~~What the interpreter does with that is
not established here — `CR-1`.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **CR-1** was answered on 2026-09-07. An all-null record is a silent no-op, guarded in the dispatcher itself; it completes in one call and cannot hang (§5 of this page).*


### `CR-2` bounded — no shipped script calls any of them (FABLE, 2026-09-22)

`CR-2` asks **what `restartbattle` did**. The image side was already known: no `begin`, no `poll`,
no `result`. **The script side is now measured too, and it is empty.**

A native verb call is a three-byte instruction — one of `0x58` `CALL`, `0x59` `CALLACT`, `0x5D`
`CALLPOPA`, `0x5E` `CALLACTPOPA`, followed by the 16-bit call id. **Every such triple in all 10,045
shipped `.ebp` files was counted: 18,798,643 of them.**

| the three empty verbs | call sites |
|---|--:|
| `restartbattle` `0x03B0` | **0** |
| `battlemembersync` `0x0356` | **0** |
| `setnorecovertelepostatus` `0x0330` | 2, and both read as noise — below |

> **Why a zero here is decisive while a small positive is not.** A raw byte scan **over-reports**:
> the same three bytes occur inside data. So a count is an *upper bound* — but **a real call has no
> other encoding**, so nothing can hide from it. **A zero is proof of absence; a 2 is not proof of
> presence.**

**The control is the histogram's own shape.** 91.9 % of the 18.8 M triples carry an id that is in
the shipped verb table, and the commonest are what a script corpus should be made of:

| id | verb | triples |
|---|---|--:|
| `0000` | `wait` | 1,014,941 |
| `00FE` | `setmapidfloor` | 756,594 |
| `00FF` | `setmapidwall` | 685,233 |
| `0090` | `nowmap` | 573,617 |
| `0001` | `setpos` | 160,345 |

**The two `setnorecovertelepostatus` matches are data, not calls.** Both are `5D CALLPOPA`, at
`plan_master/ch/event/bhm_d/bhm_d0101/bhm_d0101.ebp` offset 95,677 and
`plan_master/in/event/rwf_c/rwf_c0102/rwf_c0102.ebp` offset 32,093. **Neither sits in code:** within
±40 bytes they have **1** and **0** other call opcodes, where real script is dense with them, and
both carry the same four-byte run `00 00 10 13` a few bytes earlier — one data pattern occurring
twice, not two calls. *They are recorded as unverified candidates; no instruction-boundary decode
was run on them.*

> **So `CR-2` is bounded, not answered, and the distinction is the honest part.** What the verb
> *did* is **not** recovered and cannot be from this build: it has **no implementation and no
> caller**, so there is no behaviour to read and no context to infer one from. **The row's own two
> alternatives — a cut feature or a debug facility — are still not discriminated**, because nothing
> distinguishes them once both the code and the call sites are absent. What changes is that the
> evidence base is now known to be *empty* rather than *unexamined*.

> **Scope.** The shipped `.ebp` corpus under `ps2data`, 10,045 files, read statically. A verb
> invoked by something other than a compiled script instruction — a debug console, a tool, a
> host-side harness — would not appear here. **NATIVE/STATIC.**

## 3. Key addresses

| address | role |
|---|---|
| `0016D6A0` | folded `ret 0`, used as `begin` and `result` for stubs |
| `005C5230` | `xor eax, eax; ret` — the stub `poll`, reports "done" immediately |
| `00356A90` | `movesync` poll — a real wait predicate |
| `0034D4C0` | `gillwinsync` poll — the seven-instruction wait idiom |
| `0034E3E0` | poll shared by `summonreadsync` and `summontopartyreadsync` *(corrected 2026-10-02, OPUS: and by `partyallread` `0x3EB` and `partyallread2` `0x46F` — four records under the five command tables read under the accessor frame - begin `tbl + 8 + 0x20n` (`003DC28E`), poll `+ 0x10` (`003DC25E`), result `tbl + 0x20(n + 1)` (`003DC2BA`))* |
| `003447F0` | result shared by `hddinstall` and `networkhddinstall` |

## 4. Modding notes

- **A `*sync` verb is a wait, not an action.** Calling one without the verb that starts the thing
  waits on a condition nothing will satisfy — or returns immediately, depending on the subsystem's
  idle state. Pair them.
- **The stubbed verbs are safe to leave in a script.** They complete on the first poll. **They are
  not all safe to remove** — the stubbing is in `begin` and `poll`, and three of the nine still have
  a `result` body that does real work, which runs *immediately* because the poll reports done on
  frame one (§7). `hddinstall` / `networkhddinstall` set the `useHdd` config global; `disposesummon`
  and `changetonormalparty` each make two calls.
- **`hddinstall`, `networkhddinstall`, `hddmount`, `atrac3play`, `atrac3cancel` are PlayStation
  heritage.** If a script you are reading calls them, it descends from PS2 or PS3 authoring rather
  than being written for this release.
- **Restoring a stub means writing a body, not flipping a flag.** The slots point at shared no-ops;
  there is no disabled implementation to re-enable.

## 5. What is not known

- [x] ~~What the interpreter does with an all-null record — the three empty verbs.~~ **`CR-1`
  ANSWERED 2026-09-07: a silent no-op.** `begin` null is skipped, `poll` null substitutes a zeroed
  local so the command reads as *finished*, and `result` null takes `00262360`, which pushes tag 1 /
  kind 6 / value 0 onto the 63-entry result list and resets the phase. **It completes in one call and
  cannot hang.** Most of this was **already established** in
  [`Native-Command-Lifecycle/native-command-lifecycle.md`](Native-Command-Lifecycle/native-command-lifecycle.md)
  §2 when this question was filed; its new §14 adds the `00262360` branch and composes the three.
- [x] **UQ-65.** **What `restartbattle` did.** *(Marker normalised 2026-09-30 (FABLE, [record](../_index/candidates/qid-marker-truth-fable-0930/README.md)): UQ-65 is SUPERSEDED as a duplicate of CR-2, closed NO ADMISSIBLE SOURCE.)* A named verb with no implementation at all, in a game with no
  battle-restart feature the player can reach. `CR-2`.
  **BOUNDED 2026-09-22 (FABLE): no shipped script calls it either** — 0 of 18,798,643 native-call
  triples across all 10,045 `.ebp` files. The section above states why the zero is decisive and why
  the question is still not answered.
- [x] **CR-3.** **Why `atrac3standbysync` and `atrac3playsync` are polls-only pointing at the stub** while
  `atrac3play` and `atrac3cancel` are stubs in the other population — the family is split across two
  shapes. `CR-3`. *(DISSOLVED in the register 2026-09-26, FABLE, Claude Opus 5.5: the dispatch records register all
  ~~five ATRAC3 verbs the same way, with a result callback only, and exactly one of them is the folded `ret 0`. There~~
  ~~is no two-shape split to explain. Why that one verb is stubbed is intent, which no shipped artefact carries.~~)* *(corrected 2026-10-02, OPUS: the two-shape split is in the bytes: `0x04AB` and `0x04AD` carry only the poll `005C5230`, `0x04AE` begin `0016D6A0` + poll `005C5230`, `0x04AA` and `0x04AC` a result only, under the five command tables read under the accessor frame - begin `tbl + 8 + 0x20n` (`003DC28E`), poll `+ 0x10` (`003DC25E`), result `tbl + 0x20(n + 1)` (`003DC2BA`))*
- [x] ~~No `result` body of any stubbed verb has been read; only that its `begin`/`poll` are
  no-ops.~~ **Read 2026-09-13 (OPUS): all four, and none is a no-op.** `003447F0`
  (`hddinstall`, `networkhddinstall`) is `mov ecx, 1; jmp 00408EC0` — it sets the `FF12CONFIG`
  option global `02B62DB1`, the one the verb `getusehdd` (`0x0376`) returns
  ([the config page](../19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md)
  had already recorded this writer). `0034FB20` (`disposesummon`) calls `00314D40(1)` and tail-jumps
  `003B6F60`; `00350F30` (`changetonormalparty`) calls `003B7D30()` and tail-jumps `003B7180`.
  **So a "stub" here means a stubbed `begin` and `poll`, not a stubbed verb.** §7.

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| 26 poll-only, 3 fully-null, 9 stub-shaped | the family-0 record table read from the image, cross-referenced with the verb catalogue | 1 |
| `005C5230` is `xor eax, eax; ret` | disassembled | 1 |
| `0016D6A0` is `ret 0` | disassembled | 1 |
| A poll returns 0 for "done" | `wait`'s poll, documented in the lifecycle document | 1 |
| `movesync` / `gillwinsync` polls do real work | disassembled | 1 |
| Shared poll and result bodies | identical addresses in the record table | 1 |
| **The PS2/PS3 attribution** | **the verb names and the codec/HDD vocabulary — a reading of names, not of code** | 8 |


## 7. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run on the addresses this pass introduces; `CR-3` is this page's own and
four ANSWERED rows were read — `DA-4` already records `005C5230` as a folded stub in two `PCallerScript`
vtable slots. Static only: the shipped image and the family-0 record table. Nothing executed.)*

### The three populations re-derived, and two of them are exact

Re-counted from the record table without reading the prose: family 0 has **1,496** rows and **not one
of them uses a fourth slot** — `slot2` is empty in 1,496 of 1,496, so "three callbacks" is a
measurement, not a convention.

| population | page | measured |
|---|---:|---:|
| `poll` only | 26 | **26** — and the named twenty-six are **exactly** that set, both differences empty |
| every slot null | 3 | **3** — `0x0330`, `0x0356`, `0x03B0`, all `cat_known False` |
| stub-shaped | 9 | the nine rows reproduce **address for address** |

`0016D6A0` is `C2 00 00` and `005C5230` is `33 C0 C3`, from the bytes. `003447F0` is the result of
`hddinstall` and `networkhddinstall` and **of nothing else**.

### ✖ Corrected: the stubbed verbs are not inert — three of the nine still run a result

§5's last item says no stub `result` body has been read. All four have now been read, and **none is a
no-op**:

| verb(s) | `result` | what it does |
|---|---|---|
| `hddinstall`, `networkhddinstall` | `003447F0` | `mov ecx, 1; jmp 00408EC0` — **sets the `FF12CONFIG` option global `02B62DB1`**, the one `getusehdd` (`0x0376`) returns |
| `disposesummon` | `0034FB20` | `00314D40(1)`, then tail-jumps `003B6F60` |
| `changetonormalparty` | `00350F30` | `003B7D30()`, then tail-jumps `003B7180` |

And because the stub poll reports **done on the first frame**, the result runs **immediately**. So
"stub" here names a stubbed `begin` and `poll`, not a stubbed verb, and §4's *"safe to remove, since
nothing they do is observable"* is **wrong for these three**. The page's own table shows the non-stub
result addresses; the modding note was written past them.

> The `003447F0` half was **already on record**:
> [the `FF12CONFIG` page](../19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md)
> lists `02B62DB1` as *"written also by `setusehdd` and `hddinstall` / `networkhddinstall`, which set
> 1"*. An answer stranded one directory away from the question.
>
> **It is still not observable to a player**: nothing native reads `02B62DB1` except the getter behind
> `getusehdd`, and a byte walk of the 1,115 shipped `us` scripts finds **0 call sites** for any of
> `0372`, `0373`, `0375`, `0376` (controls: `mapsoundplay` 3,838 sites, `0x302B` 6 — measured
> 2026-09-13). **Observable to a script that asks, unreachable in the shipped ones.**

### ✖ Corrected: `0034E3E0` is a quartet's poll, not a pair's

`summonreadsync` and `summontopartyreadsync` are joined by **`partyallread` (`0x3EB`)** and
**`partyallread2` (`0x46F`)**, which also share the result `0034D460`. The second two are *not*
poll-only — they carry a real `begin` — so one wait predicate serves both a poll-only pair and a
begin/poll/result pair. That is a sharper fact than "two pairs share one poll", and it is the one that
tells a reader the predicate is about *the party being read*, not about the verb.

### ✔ New: the stub poll has a third use — an instantaneous action

`005C5230` is the `poll` of **nine** family-0 verbs. Eight are the page's. The ninth is
**`callgameover` (`0x04D8`)**, whose `begin` is `0033F640` — `xor ecx, ecx; jmp 00237D60`, real work —
with no `result`. So a stub poll is not only what a removed feature leaves behind: it is also **how a
verb says "I did it, don't wait for me."** `moveblurfadesync` is the mirror case the page already
lists, with stubs at `begin` and `result` and a real poll.

### ✔ New: a `0016D6A0` result does not make a verb a stub

`0016D6A0` appears as the `result` of **seven** family-0 verbs, and **four of them are ordinary
working verbs** with a real `begin`, a real `poll` and arity 1: `setupbattle` (`0x56`),
`motionreadsync` (`0xA3`), `modelreadsync` (`0xC0`), `talktreasure` (`0x2BF`). In the `result` slot
the folded `ret 0` means **"no value to push"**. Reading it as a stub marker would move four working
verbs into population three — which is the trap the `B-2/a` note about the fold's many identities is
there to prevent, now with a fifth role to its name.

### ⚠ The "2 arguments" for `unkCall_5c7` is a conflict, not a fact

The row reads `cat_args 2` and `param_types 0x10,0x10` — but also **`arity 0`** and
**`arity_status CONFLICT`**. §2's table states the 2 flatly. The catalogue says two, the derived arity
says none, and the table itself flags the disagreement.

**Not claimed.** `CR-2` and `CR-3` stand *(answered: CR-3 dissolved 2026-09-26, UQ-65 / CR-2 closed 2026-09-30, §5; `003B7180` read, below; 2026-10-02, OPUS)*. What `00314D40`, `003B6F60`, `003B7D30`, `003B7180` and
`00237D60` do — **the result bodies were read, their callees were not.** Whether the three empty verbs
or any stub verb is called by a shipped script outside the four HDD ids — not walked here. The PS2/PS3
attribution remains a reading of names, as §6 says. Nothing was executed.

## 8. Related

- [`Native-Command-Lifecycle/native-command-lifecycle.md`](Native-Command-Lifecycle/native-command-lifecycle.md)
  — the begin/poll/result contract and the scratch slot.
- [`scriptvm-native-dispatch-table.md`](scriptvm-native-dispatch-table.md) — the record table these
  shapes were read from.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**World — CLIENT.** The 7-byte getter `00314D40` is also read by the 1,185-byte area initialiser. A verb that
only waits on it reads state that area set-up also reads.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — SERVICE.** `0033F640` on this page calls `FUN_00237d60`, owned by that layer. What it reaches is a 31-byte guard: when the query answers zero it asks for slot `0xB` and returns 1 either way; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction, Gameplay, Input, Movement, Presentation — MECHANICAL (SWE2-EC7-67).** `003B7180`'s measured callees `00263750`, `003589B0` and `0026DC60` are shared helpers those layers also call — `00307300`/`003082F0`/`00319F50`/`00325260`/`0031ADB0`/`00226BE0`/`0034A940`/`0037CF00`/`0037D000`/`002E5610`/`003A4290`/`003A56F0`/`00465120`/`00465690`. Those bodies are clients of the helpers, not consumers of this verb family; neither reads the wait-list. Read from the shipping bytes 2026-09-19 (SWE2-EC7).

**ActorEntity, Party — MECHANICAL (SWE2-EC7, batch 159).** `0030AA00`'s slot machinery is the same shared family: `00263750` is also read by Party bodies `003261D0`/`00326500`/`003272F0`/`003273D0` and by ActorEntity bodies `003266C0`/`0035A8D0`, and `0026DC60` by `00300E40` — clients of the same accessors, not consumers of the wait bitmask. Read from the shipping bytes 2026-09-27 (SWE2-EC7).

**CombatAI, CombatFormula, Items_Equipment_Shops_License, Rewards_Progression_Economy, Status_Periodic_Terminal — MECHANICAL (SWE2-EC7, batch 159).** `00377C20`, the flag-approval test `0030AA00` runs on a `0x80000003`-marked `[+0x698]` block, is also consulted by `003014C0`/`00301AD0`/`00305AB0` (CombatAI), `00300530` (CombatFormula), `00309FB0`/`0030FD10` (Items_Equipment_Shops_License), `00312280` (Rewards_Progression_Economy) and `0030E360`/`0030F690` (Status_Periodic_Terminal); `0026DC60` is also read by `00301140` on the last. All consult the shared predicate — none consume the four-bit mask. Read from the shipping bytes 2026-09-27 (SWE2-EC7).

## SWE2-EC7-67 update - `003B7180`

`003B7180` (129 B) is ~~a wait/do-nothing verb body~~ the shared tail of two result callbacks, `0x0209` `changetonormalparty`'s `00350F30` and `0x02A4`'s `0034D330` *(corrected 2026-10-02, OPUS: `00350F3D` and `0034D33D` jump to it; it is in no dispatch record; for each ready slot it calls `0036E750(.., 9)` and `0026DC60(actor, 1)`, `003B71D9`, `003B71E6`)* - `0030AA00`/`00263750`/`003589B0`/`0036E750`/`0026DC60`. Interior anchor `003B718D` (a `0030AA00` call).

## SWE2-EC7-70 update (2026-09-19) - `003E5710` triple-scale compose measured

`003E5710` (94 B) is the element-wise scale compose the verb bodies write
through: `rdx[0..2] = [rcx+0x260..+0x268] * [rcx+0x160..+0x168] *
[rcx+0x26C]` and `rdx[3] = 1.0f` - a per-channel colour/scale triple
product with a fixed unit w.
Interior anchor `003E5728` (the first `movss [rdx]` store).

`0030AA00` (179 B) is the four-slot readiness poll `003B7180` runs ~~for the wait verbs~~ for those two result callbacks *(corrected 2026-10-02, OPUS: `003B718D` is its only call site)*: slots `0..3` probe `02EBF190 + 0x5A48 + i*2` for a `0xFFFF` vacancy, `0031B8C0(i)` resolves the slot record, and a live `[+0x698]` block sets bit `i` when `+0x64 | +0x3C` stays clear of `0x80000003` - or when `00377C20` still approves the flagged record; a passed `r14` additionally receives `00320890([02EBF190 + 0x5AD5])`, and the four-bit mask is the result

Interior anchor `0030AA39` (function `0030AA00`).
