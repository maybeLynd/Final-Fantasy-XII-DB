---
system: The extensionless FF12CONFIG boot option block and the unreferenced DebGlobal network list
category: 19-Save-Load-Settings
status: AUDITED
owner_layer: PrimaryOwner:Save_Load_Settings
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 39 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "2 / 2 extensionless archive entries, with a RIP-reference scan of both path literals and a positive control, 2026-09-13"
last_reviewed: 2026-09-13
archive_formats:
  - "(none)"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-ff12config-pass-1 - both files and both literals reproduce, the 15 call sites and their 02B62DAB-first order are exact, and the 'none' list is confirmed over all 38,161 function bodies; NEW: 02B62DB9 is an eleventh block global with four consumers (verb debug_getdebugstatus, two bodies gated on == 1, and the field-0xC substitution) and no writer but the reset, 02B62DC0's readers reach the ret-0 stub, 02B62DBA is dead, and the verb negative is redone as a byte walk over 1,115 shipped scripts with two controls
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# `FF12CONFIG` and `DebGlobal.bin/file1` — the two files without an extension

> **`ps2data/square_ff12/ff12config`** is read at every boot: 16 of its 2,048 bytes are copied into a block of
> option globals, and in the shipped image **none of them changes what the game does** — each one either has no
> reader, feeds a message stub, is overridden before its reader sees it, or sits behind a branch another global
> always takes. **`ps2data/debglobal.bin/file1`** is four IPv4 strings; nothing in the executable refers to it.

**Corpus validation.**

| | |
|---|---|
| extensionless entries | **2 of 2** |
| `ff12config` | 2,048 bytes; nonzero bytes `+0x00 = 1`, `+0x07 = 1`, `+0x08 = 1`, `+0x0A = 236`, `+0x13 = 1` |
| `debglobal.bin/file1` | 148 bytes; 16-byte NUL-padded strings `10.0.5.238`, `10.0.5.255`, `10.0.5.254`, `10.0.16.26`, then zeros |
| RIP references to `"PS2Data/SQUARE_FF12/FF12CONFIG"` | **1** (`00408C88`) |
| RIP references to `"PS2Data\DebGlobal.bin"` | **0** — control: the double 8 bytes before it (`00D22C50`) is found at `0051E03C` |

Census: [`census.py`](../../_experiments/evidence/ps2-config-extensionless/census.py) →
[`census.out.txt`](../../_experiments/evidence/ps2-config-extensionless/census.out.txt).

---

## 1. What the player sees

**Nothing.** The config file is loaded during start-up and its values land in globals, but no reader in the
shipped build acts differently for any value the file holds (§3). The network list
belongs to a development network (private `10.0.x.x` addresses) and is never opened.

## 2. The layout

```struct Ff12Config base=file size=0x17
+0x00  u8        unread00     1 in the shipped file; not copied
+0x01  u8        unread01     not copied by the loader
+0x02  u8        opt02        -> 02B62DA8 (default 3)
+0x03  u8        opt03        -> 02B62DA9
+0x04  u8        opt04        -> 02B62DAA
+0x05  u8        unread05     not copied by the loader
+0x06  u8        opt06        -> 02B62DAC
+0x07  u8        unread07     not copied by the loader
+0x08  u8        opt08        -> 02B62DAE (1 in the shipped file)
+0x09  u8        opt09        -> 02B62DAF (default 1)
+0x0A  u16       fieldId    -> 02B62DB4 (236 in the shipped file)
+0x0C  u8        opt0C        -> 02B62DB0
+0x0D  u8        useHdd       -> 02B62DB1
+0x0E  u8        opt0E        -> 02B62DB2
+0x0F  u8        opt0F        -> 02B62DB3
+0x10  u8        opt10        -> 02B62DB6
+0x11  u8        opt11        -> 02B62DB7
+0x12  u8        opt12        -> 02B62DB8
+0x13  u8[2]     unread13     not copied by the loader
+0x15  u8        opt15        -> 02B62DBB (not reset by 00408BA0)
+0x16  u8        opt16        -> 02B62DBC
```

Bytes `+0x01`, `+0x05`, `+0x07`, `+0x13`, `+0x14` and `+0x17`–`+0x7FF` are not copied. Names above are this
page's, from the readers in §3 where one exists.

**Three globals in the block take no file byte at all**: `02B62DAB` (always 1, §3 step 3),
**`02B62DB9`** — a debug-status flag with four consumers and no writer but the reset (§6) — and
**`02B62DBA`**, which the reset zeroes and nothing else touches. `02B62DC0` takes one only on the
path that never runs.

## 3. The loader contract

**When.** The start-up routine `003692D0` resets the block with `00408BA0` (`00369323`) and later calls the
loader `00408C30` (`0036943F`) unless `008624C0` returns `-0x65` — and `008624C0` always returns 0.

**`00408C30`:**

1. zeroes a `0x800` buffer, opens `"PS2Data/SQUARE_FF12/FF12CONFIG"` with `001D6F20(path, 1)` (`00408C88`), reads
   `0x800` bytes (`001D6FA0`) and closes it (`001D6E80`); if the open fails, nothing is copied;
2. copies the bytes of §2 into their globals (`00408CBB`–`00408D7E`) — except that `02B62DB4` takes the low word of
   `[01E02804]` instead when that dword is non-negative (`00408D48 cmovns`), and `02B62DAD` = (`[01E02804] >= 0`);
3. always sets `02B62DAB = 1` (`00408D89`);
4. if the process has a second argument equal to `"debug"`, sets `02B62DB4 = 0` (`00408D84`–`00408DC4`);
5. if `[01E02810] >= 0`, builds and opens a second path and sets `02B62DAD = 2`, `02B62DC0` = its low word
   (`00408DCB`–`00408E8E`).

**`01E02804` and `01E02810` are `-1` in the image and have no RIP writer**, so in the shipped build step 2 keeps the
file's `fieldId`, `02B62DAD` is 0, and step 5 never runs.

> **The pointer question `PC-1` raises about these two is now answered as far as static evidence can answer it —
> 2026-09-22 (FABLE).** `PC-1` asks *"whether `01E02804` / `01E02810` are written through a pointer this page's RIP
> scan cannot see"*. **Neither address occurs as a stored 8-byte or 4-byte value anywhere in the image**, so there
> is no pointer to either to be written through; and a sweep of every RIP access into the surrounding
> `01E02700`–`01E02900` shows that window is **scattered unrelated globals, not an indexable block** — the only two
> `lea`s into it take `01E027F0` and `01E027F4`, neither of which anchors an indexed reach to `+0x804` or `+0x810`.
> Their image bytes were re-read through a section-aware offset and are `FFFFFFFF` at both, so the `-1` is an
> initialised datum and not a zero-init artefact.
> **What this does not exclude:** a store to a fully computed address, which no static sweep can rule out. *That
> residual is the reason this is recorded as narrowing the clause rather than striking it* — and the rest of `PC-1`
> (the ten fields' meanings, options-word bits 13 and 14, the value 3, field id 236, which callers enter
> `002DDA30` with 1~~, and whether `001D6F20` reads the archive entry or a loose file~~ *(answered: the archive — see `PC-1`, answered 2026-09-27; 2026-10-02, OPUS)*) is untouched by it.

**What each copied byte reaches** (every RIP reference to `02B62DA8`–`02B62DC1` was listed; the readers are the
one-instruction getters `00408B00`–`00408B90`):

| File byte | Global | Reader | Effect in the shipped build |
|---|---|---|---|
| `+0x02` | `02B62DA8` | getter `00408B10`, at 15 call sites (`ActorResource_ResetManagerLoadState` `0032ED80` ×11, `0032F3D0`, `WorldSimulation_ProcessDeferredModeRequest` `0032FC30`, `ActorResource_BeginManagerResourceSetLoad` `0032FCA0`, `00331880`): skip the `005C5230(5)` path when it is 3 | **never decisive**: at every one of the 15 sites the getter for `02B62DAB` is called first and skips on 1 (e.g. `0032ED9D`–`0032EDA5`), and step 3 makes that always true |
| `+0x04` | `02B62DAA` | `00408B50` in `003694D0` | chooses the argument of a call to `0016D6A0`, which is `ret 0` — **no effect** |
| `+0x06` | `02B62DAC` | `00408B80` in `002DDA30` | when `002DDA30` is entered with 1: value 1 sets, 2 clears bit 13 of the options word `*(0215E6E0)`; 0 leaves it — **shipped 0** |
| `+0x10` | `02B62DB6` | `00408B40` in `002DDA30` | the same for bit 14 — **shipped 0** |
| `+0x0A` | `02B62DB4` | `00408B60` in `003318C0` / `00331920` | the field id requested (`WorldTransition_RequestFieldTransition`) **only when `02B62DAD == 1`**, which only happens when `01E02804` also replaced the value; with `02B62DAD == 0` both request field `0xC` instead (`00331903`) — **the file's 236 never reaches a reader** |
| `+0x0D` | `02B62DB1` | `00408B70`: verb `getusehdd` (`0x0376`); written also by `setusehdd` (`0x0375`) and `hddinstall` / `networkhddinstall` (`0x0372`/`0x0373`, which set 1) | returned to a script; **none of the four verbs is called** in the 1,114 decompiled `us` scripts (control: `mapsoundplay` is found) |
| `+0x03`, `+0x08`, `+0x09`, `+0x0C`, `+0x0E`, `+0x0F`, `+0x11`, `+0x12`, `+0x15`, `+0x16` | `02B62DA9`, `DAE`, `DAF`, `DB0`, `DB2`, `DB3`, `DB7`, `DB8`, `DBB`, `DBC` | **none** — only `00408BA0` and `00408C30` reference them | inert |

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| the whole file | `00408C30` | open failure → nothing copied | at most `0x800` bytes asked for | bytes not in §2 |
| `fieldId` | `00408D48` | — | replaced by `[01E02804]` when non-negative; zeroed by a `debug` argument | yes, in this build (above) |
| `opt02` | `0032EDA7` | — | — | yes (behind `02B62DAB`) |
| the others | as in the table above | — | — | as in the table above |

**`DebGlobal.bin/file1`.** The literal `"PS2Data\DebGlobal.bin"` sits in `.rdata` at `00D22C58` between referenced
floating-point constants, and the displacement scan finds no instruction addressing it (the census's positive
control finds the constant beside it). The archive entry is a file named `file1` inside a `debglobal.bin`
directory; the ASCII string `file1` does not occur in the image either.

**The write path.** None — the file is never written.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `00408C30` | `FF12CONFIG` loader | ✅ full body |
| `00408BA0` | block reset (defaults) | ✅ full body |
| `00408B00`–`00408B90` | one-byte / one-word getters | ✅ all ten |
| `00408EC0` | `02B62DB1` setter (`setusehdd`, `hddinstall`) | ✅ full body |
| `003318C0` / `00331920` | boot field request by `02B62DAD` | ✅ full bodies |
| `002DDA30` | options apply (bits 13 and 14 forced by `02B62DAC` / `02B62DB6`) | ◐ the two forcing blocks |
| `0032ED80`, `0032F3D0`, `0032FC30`, `0032FCA0`, `00331880` | the 15 `02B62DAB`-then-`02B62DA8` tests | ◐ each test |
| `008624C0` | returns 0 | ✅ full body |
| `0016D6A0` | `ret 0` | ✅ |
| `0050DFC0` | verb `debug_getdebugstatus` (`0x20A6`) — returns `02B62DB9` | ✅ full body |
| `00314440` | field-transition request — substitutes field `0xC` when `02B62DB9` is 0 | ◐ the gate |
| `0035FCA0` / `0035FF90` | bodies gated on `02B62DB9 == 1`; unreachable unless the byte is written from outside the image or through a runtime-computed pointer — see the adjudication in §6 | ◐ the gate only |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `00D121D8` | config path | `.rdata` | `PS2Data/SQUARE_FF12/FF12CONFIG` |
| `00D22C58` | DebGlobal path | `.rdata` | `PS2Data\DebGlobal.bin` — unreferenced |
| `02B62DA8`–`02B62DC1` | the option block | `.data` BSS | §2 and §3 |
| `01E02804` / `01E02810` | override dwords | `.data` | `-1`, no RIP writer |

### The `003692D0` exclusive subtree — all 11 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the start-up routine **11 frontier functions** — what the
boot path resets and signals around the `00408BA0` block reset and the `00408C30` load.
Interior cites are one instruction inside each declared extent (`interior_cite.py scan`; no
boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| apply arms | `00369650` (123 B), `003691E0` (221 B) | `00369650` runs `005C5230` ×2, `00369510`, then `003691E0` (`01EF9360`/`01F44830` touched); `003691E0` is the underlying apply — `005C5230` ×2 between folded-empty message stubs | `00369661` / `003691ED` |
| Phyre-side call chain | `002DE360` (188 B), `001DC040` (76 B), `002110C0` (114 B) | `002DE360` — the Audio-filed helper the crossings name — runs `001DC040` + `003E9B10` and writes the `0215E710`–`0215E72C` block plus `0215EF44`; `001DC040` forwards through `00210B30` to `002110C0`, a four-call `007Axxxx` Phyre sequence | `002DE36A` / `001DC04F` / `002110CA` |
| state clears | `0035F260` (447 B), `0046E000` (39 B) | `0035F260` ~~sweeps the `022CBxxx` flag cells and `022CAE91` with two `memset` calls~~ *(corrected 2026-09-30, FABLE, on SWE2-DATA's [record](../../_index/candidates/dd-leftovers-0930/README.md))* clears `022CB3C0` + ch x `0x100` (`0035F29A`) and the channel record `022CAE90` + ch x `0x294` (`0035F2E3`) with two `memset` calls, then initialises the record through `rdi` = `022CAE91` (record + 1); `0046E000` writes `0xFFFFFFFF` into the `02CA6074`/`02CA6114` sentinel pair | `0035F26F` / `0046E00E` |
| signal + stub | `00474680` (50 B), `004746C0` (42 B), `008628E0` (10 B) | `00474680` snapshots the first 8 bytes of the `memset` import thunk `00861EC0` into `02CA6C88`/`02CA6C8C` — a code-bytes baseline between two stub calls; `004746C0` is four `0016D6A0` calls (ecx 0/2/0/2) — a mode signal that compiles to nothing in this build; `008628E0` zeroes its out-param and returns 0 | `0047468B` / `004746CB` / `008628E9` |
| slot touch | `003E9B10` (111 B) | `002DEBB0` over the `02B5D0B8`/`02B5E0B0` records — the slot side of `002DE360`'s pass | `003E9B1B` |

The subtree is a boot-time environment reset: config apply arms, a Phyre call chain, flag and
sentinel clears, and one curious thunk-bytes snapshot — `003692D0` does more around the config
load than load it.

## 5. Corpus survey

One file each. `ff12config`'s five nonzero bytes are listed above; of the copied fields, `opt02` (0 against a default of
3), `opt08` (1) and `opt09` (0 against a default of 1) and `fieldId` (236) differ from the reset values, and none of those
reaches a consulted reader.

## 6. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run on the page's addresses and again on the ones this pass
introduced, per EVIDENCE-STANDARD amendment 2026-09-13c. No register row answers any of it. The
archive was read, never written; nothing was executed.)*

### Every published figure reproduces

Both files re-read from the archive and both literals re-scanned:

| claim | measured |
|---|---|
| extensionless archive entries | **2 of 2** — `ps2data/square_ff12/ff12config`, `ps2data/debglobal.bin/file1` |
| `ff12config` 2,048 B, non-zero at `+0x00`, `+0x07`, `+0x08`, `+0x0A`, `+0x13` | **2,048 B, exactly five non-zero bytes**, values 1 / 1 / 1 / 236 / 1 |
| `debglobal.bin/file1` 148 B, four 16-byte NUL-padded strings then zeros | **148 B**, `10.0.5.238` / `10.0.5.255` / `10.0.5.254` / `10.0.16.26`, **all zero from `+0x40`** |
| RIP references to the config literal | **1**, `00408C88` in `00408C30` |
| RIP references to `"PS2Data\DebGlobal.bin"` | **0** — control: the double at `00D22C50` is reached by `mulsd` at `0051E03C` |
| `file1` as ASCII in the image | **0** |
| `008624C0` returns 0 | `call 00862A40` then **`xor eax, eax; ret`** — unconditional, whatever the call does |
| the reset's defaults | `02B62DA8` = **3**, `02B62DAB` = **1**, `02B62DAF` = **1**, the rest 0 |
| `01E02804` / `01E02810` are `-1` with no RIP writer | both `FFFFFFFF`; **1 and 3 references, every one a read inside `00408C30`** |
| the `02B62DAB`-then-`02B62DA8` order at 15 sites, 11 of them in `0032ED80` | **15 call sites, `02B62DAB` first at every one**, 11 in `0032ED80` |

The reader census was re-run independently — every rip-relative operand in all **38,161** function
bodies — and the §3 table's "none" list is exact: `02B62DA9`, `DAE`, `DAF`, `DB0`, `DB2`, `DB3`,
`DB7`, `DB8`, `DBB`, `DBC` are touched by the reset and the loader and by nothing else.

### ✔ New: the block has an eleventh global the page never lists, and a script verb reads it

`02B62DB9` has a getter (`00408B00`), a reset to 0, **no file byte, and no other writer over five
decoded write routes with controls** (adjudication below). It has **four consumers**:

| site | what it does with the value |
|---|---|
| `0050DFC0` | the script verb **`debug_getdebugstatus`** (`0x20A6`) — returns it to the script |
| `0035FCA0` | `cmp eax, 1 / jne` at `0035FCA9` — **the whole body is skipped** unless it is 1 |
| `0035FF90` | `cmp eax, 1 / jne` at `0035FF9B` — the same |
| `00314440` | the field-transition request: when the getter returns 0 **and** the requested field id is 0, the id becomes **`0xC`** (`00314463`–`0031446E`) |

So a debug flag that nothing can set gates two native bodies off, returns 0 to any script that asks,
and supplies the same `0xC` fallback that `00331903` supplies. **It belongs in the block's account:
the file cannot reach it, which is why §3's file-byte table does not have it, but it is the eleventh
member and it is the one with the most readers.**

> The spawn page already writes *"field0 with field12 when `00408B00()` is zero"*. This pass says
> **when is always**: the getter reads `02B62DB9`, and the census finds one writer for it — the reset,
> writing 0. Routed to that page's owner rather than edited here (`OPUS-SPAWN-408B00-ALWAYS-ZERO`).

> #### Adjudicated 2026-09-13 (OPUS, `ASTRA-CONTRA-OPUS-CONFIG-GATE-INVARIANT`): the method was wrong, the claim survives, and the part that actually secures it is not the census
>
> **ASTRA is right about the instrument.** The *"no other writer anywhere in the image"* above rested
> on a census of exact RIP **destinations**, and that census is structurally unable to see a write
> through a register, a **covering** store of greater width at a lower address, or a block fill.
> ASTRA asserts no alternate writer — the objection is to the inference, and it is correct.
>
> **Re-run by decoding all 38,161 bodies, over five routes, each with its own positive control:**
>
> | route | result | positive control |
> |---|---|---|
> | R1 direct RIP store to the byte | **1** — the reset `00408BBC` | that store is found, so the decoder sees this shape |
> | R2 **covering** wider store spanning the byte | **0** | the decoder finds **16** wider-than-byte stores into `[02B62D80, 02B62DE0)` — including `mov word ptr […], ax` at `00408BA9` covering `02B62DB4`–`B5` — so R2 is a live detector, not a silent one |
> | R3 `lea` into the block then a store through the register | **0** | two `lea`s into the block exist (`0040507F`, `004050A7`, both → `02B62D90`) and are tracked |
> | R4 `rep stos` / 3-argument fill spanning the byte | **0** | the same decoder finds bounded fills elsewhere in the image |
> | R5 a pointer into the block held in initialised data | **0 of 114,962 DIR64 relocations** | the stored pointer to `006709D0` is found in 1 slot |
>
> **So the claim holds — but ASTRA's second question, initialisation ordering, was the real gap, and
> the census could never have answered it.** It is answered by the image layout instead:
>
> > **`02B62DB9` lies beyond `.data`'s raw size** (`.data` `01DF0000`, virtual `0x11A7530`, raw
> > `0x18E400`). It is **zero-filled by the loader**, so the byte is `0` before a single instruction
> > of this image runs. **The reset is redundant for the value, not load-bearing for it.**
>
> That is what makes *"when is always"* safe, and it is a different fact from *"only one writer."*
> A sole writer that wrote `1` would still leave the claim false; a zero-initialised global with no
> writer that can set it is what closes it.
>
> **One precision fix while checking.** The reset does not store an immediate: `00408BBC` is
> `mov byte ptr [rip+0x275A1F7], al`. `al` is provably `0` — `00408BA0` opens with `xor eax, eax`
> and nothing between it and the store writes `eax` — so *"a reset to 0"* is **correct**, but it was
> asserted from the destination rather than read from the source.
>
> **What stays open, stated as a dependence rather than a hedge.** *"Unreachable in this build"* for
> `0035FCA0` and `0035FF90` now means: unreachable unless the byte is written by a route **no static
> census covers** — a store through a pointer computed at runtime with no `lea` — **or from outside
> the image entirely.** The second is not academic for this particular global: a flag named
> *debug status*, readable by a script verb and settable by nothing the executable contains, is
> exactly the shape of a value a debugger, trainer or host tool is meant to poke. The bodies stay
> unread; the reason is now the measured one.

### ✔ New: two more entries the §3 table does not carry

* **`02B62DC0` has readers.** `00408B20` is called at `003318EA` and `00331953` — the `02B62DAD == 2`
  arm of both boot-field functions. That arm **tail-calls `0016D6A0`, the `ret 0` stub**, so even if
  step 5 ran the value would go nowhere. The same stub that makes `opt04` inert makes this inert.
* **`02B62DBA` is dead outright.** The reset zeroes it (`00408BC2`); no getter, no loader byte, no
  other reference in 38,161 bodies.

### ✔ Strengthened: the verb negative, over the shipped bytes

§3 says none of the four HDD verbs is called, from **1,114 decompiled** scripts. Re-done as a byte
walk over the archive's **1,115** `us` `.ebp`, looking for the four call opcodes (`0x58`, `0x59`,
`0x5D`, `0x5E`) followed by the verb id — no decompiler in the path:

| verb | id | sites |
|---|---|---|
| `hddinstall` / `networkhddinstall` / `setusehdd` / `getusehdd` | `0372` / `0373` / `0375` / `0376` | **0** |
| `debug_getdebugstatus` | `20A6` | **0** |
| **control** `mapsoundplay` | `02BA` | **3,838 sites in 351 files** |
| **control** `0x302B`, whose sites `FZ-5` recorded independently | `302B` | **6 sites in 2 files** — `evt_t0505.ebp` at `0x8144`, `0x8159`, `0x816E`, `0x8399`, `0x85B0` and `naf_b04.ebp` at `0x1CF4`, **the register's offsets exactly** |

### An instrument near-miss, caught by this page's own control

My first reference scan looked only for `lea rN, [rip+disp32]`. It found the config literal's one
reference and reported **0 for the control** at `00D22C50` — which would have read as "the control
failed, distrust the 0 for DebGlobal". The control is a **double**: it is reached by `mulsd`, not by
`lea`, so the instrument could not have found it. Re-run over every rip-relative operand in every
function body, the control reproduces at `0051E03C` and the DebGlobal literal still has none.
**The page's choice of control is what caught the bad instrument**, which is the argument for
choosing one that is not the same shape as the thing under test.

**Not claimed.** Anything in `PC-1`: what the development build used the options for, what bits 13
and 14 mean, what `fieldId` 236 names, which callers enter `002DDA30` with 1, ~~whether `001D6F20`~~
~~reads the archive entry or a loose file,~~ *(answered: the archive, `PC-1` 2026-09-27; 2026-10-02, OPUS)* and whether the two override dwords are written through a
handed pointer. ~~What `0035FCA0` and `0035FF90` would do if the flag were 1 —~~ **~~their bodies were not~~
~~read past the gate.~~** *(answered: flag 1 updates both registered input channels — `PC-2`, 2026-09-14; 2026-10-02, OPUS)* What sets `02B62DB9` in a build where it is settable. Nothing was executed.

## 7. What this document does not claim

- [x] **PC-1.** *(OUT OF EVIDENCE BOUNDARY for the residue 2026-09-28, applied by FABLE (Claude Opus 5.5) on
      OPUS's non-author signature. The residue is what the development build used the ten unread fields for, what
      `opt02`'s value 3 meant, and whether that build numbered fields as the shipped name table does. The consumer was
      compiled out of retail, so only the unshipped source and `FF12X64.pdb` carry it. Closed for the gate, unanswered
      in fact. The other parts of this item are answered on the register row PC-1.
      [Signature](../../_index/candidates/pc1-oeb-signature-opus/README.md).)*
      What the development build used these options for — the meaning of the ten fields with no reader, of
      options-word bits 13 and 14, of the value 3 in `opt02`, and of `fieldId` 236 as a field id; which callers
      enter `002DDA30` with 1; whether the loader's stream (`001D6F20`) reads the archive entry or a loose file;
      and whether `01E02804` / `01E02810` are written through a pointer this page's RIP scan cannot see. `PC-1`.
      *Narrowed 2026-09-27 (FABLE, Claude Opus 5.5): no pointer route exists in the image. Beyond the RIP scan, no
      image-base-relative form reaches `[01E02800, 01E02820)`, no data word holds either address as a VA or RVA, and the
      only addresses formed nearby are two separate debug-variable dwords, `0x14` and `0x10` bytes below (controls for
      each detector). Static only; ASTRA's live write watch stays the confirming instrument.
      [Record](../../_index/candidates/pc1-pointer-store/README.md).*
      *Narrowed 2026-09-26 (FABLE, Claude Opus 5.5).* Control: [`pc1_ff12config.py`](../../_index/candidates/pc1-ff12config/pc1_ff12config.py) (4 checks, FAILS 0). Read by a delegated read-only pass;
      re-checked here.
      - **Bits 13 and 14 are named.** They are Vibration (command 9) and Screen Shake (command 10) on
        [the settings command table](the-settings-command-table.md). `opt06` and `opt10` force them on (1) or off (2)
        through two plain byte getters of this file's copy; the shipped file has 0 in both, so neither is forced.
      - **Who enters `002DDA30` with 1:** the options defaults installer's tail call, every time. The other entry, a
        thunk, passes 0.
      - **`fieldId` 236 is "Throne Road"** in the shipped field-name table (`planmapname.bin`). Whether the
        development build numbered fields the same way is not established.
      - **Still open:** the ten reader-less bytes and the value 3 in `opt02`, which no shipped code gives a meaning;
        whether the loader's stream reads the archive entry or a loose file; and the pointer-store question.
      - **Archive or loose file - answered 2026-09-27 (FABLE, Claude Opus 5.5), static: the archive.** `001D6F20` hands the path to the stream resolver `0059EE90` with selector 1. The resolver fills only two sources: route 1, the RAM file cache (`01F83440`, budget from `GlobalMemoryStatusEx` at `0020C610`), which route 2's own hits fill through `0059A9B0`, and route 2, the package lookup, whose five slots are mounted only by `0019B070` from one call site with `../FFXII_TZA.vbf`. The only `CreateFile*` import is `CreateFileA`, used by two minidump writers. So `FF12CONFIG` is the archive entry or the cache's copy of it. [Record and control](../../_index/candidates/pc1-config-route/README.md) (7 checks, FAILS 0). **Still open:** the ten reader-less bytes, the value 3 in `opt02`, and the pointer-store question.
- [x] **PC-2.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)* What `0035FCA0` and `0035FF90` do when `02B62DB9` is 1, and what could set it — the flag
      has no writer but the reset, so both bodies are unreachable in this build ~~and were not~~
      ~~read past their gate~~ *(answered: read since — the 2026-09-14 note directly below; 2026-10-02, OPUS)*. `PC-2`, opened 2026-09-13.
      *Partly answered 2026-09-14 (FABLE); the register row is PARTIAL (PC-2, first half): **flag = 1 updates both
      registered input channels; flag = 0 updates channel 0 only.*** The registered-channel block runs from `022CAE90` to `022CB3B8`,
      which is `0x528` bytes, i.e. **two** `0x294`-byte channels. With the flag at 0 (every run of this build),
      `InputControl_UpdateRegisteredChannels` `0035FCA0` tail-calls `InputControl_UpdateChannelByIndex(0)` (`0035FDBF`, into
      `0035FDD0`), and `0035FF90` recomputes the read index of channel 0 alone (`00360019`–`00360065`). With the flag at 1,
      `0035FCA0` walks both channels (`0035FCB2`–`0035FDA0`). Each step advances the 4-bit history index, polls availability and
      carries history forward (`0035ED50`), or builds new history (`InputControl_PollAndBuildChannelHistory` `0035F420`), then calls
      `InputControl_AdvanceChannelTimingState` (`0035F690`). `0035FF90` recomputes both channels' read indices against the
      bound `00184950()` (`01F3DA18`, 2 in the image) (`0035FFA0`–`00360007`). **So "debug status" enables the second input
      channel**, and GFZ's name for the getter, `InputControl_GetRegisteredChannelUpdateMode`, fits the code. What the second
      channel carries in play (a second pad, or a debug device) is not read. The second half, what could set the byte, stays
      as recorded above: nothing in the image.

## 8. Related

- [Game settings INI and runtime config](game-settings-ini-and-runtime-config.md) — the PC build's real settings.
- [The time-stop and system-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) — the saved options word `*(0215E6E0)`.
- [Section 008](../../25-EBP-Script-Container/Sections/section-008.md) — another consumer of `02B62DAB` / `02B62DA8` (`0032F3D0`).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Presentation and Audio — CLIENT of the FF12CONFIG file helpers.** The file close `001D6E80`, open `001D6F20` and
  read `001D6FA0` are also used by `AddMotion_LoadSkeletonMapping`, `AddMotion_LoadResources` and
  `AddMotion_LoadHighModelReplace`, and by a 451-byte Audio-filed body. **They are the engine's generic ~~loose-file~~ file-stream
  helpers, not config-only.** *(corrected 2026-09-27, FABLE, Claude Opus 5.5: a stream open that the resolver serves from the RAM file cache or the `FFXII_TZA.vbf` archive, never a loose file - [record](../../_index/candidates/pc1-config-route/README.md))* The ~~debug-status getter~~ present-sync-interval getter `00184950` (7 B) *(corrected 2026-10-02, OPUS: `00184950` is `mov eax, [01F3DA18]` / `ret`; the debug status is `02B62DB9`, getter `00408B00`; game-settings-ini-and-runtime-config.md `DH-7`)* is read by an 881-byte Presentation body and by
  two Audio-filed bodies (120 B and 306 B).
- **Audio — SERVICE.** `002DDA30` calls a 34-byte Audio-filed helper, and the start-up routine `003692D0` calls a
  188-byte one.
- **CombatAction — CLIENT.**
  - `WorldTransition_RequestFieldTransition` (`00314440`) is called by `BattleUnit_HandleActorTimelineEvent`, so a
    battle timeline event can request a field transition through the field-`0xC` gate.
  - `WorldSimulation_ProcessDeferredModeRequest` (`0032FC30`) is called by
    `BattleAction_InitializeGlobalSpecialSequenceMode`.
- **PlatformOnlineAchievements — SERVICE.** The folder check `008624C0` calls `00862A40`, a 399-byte folder builder.
  That builder uses `SHGetFolderPathW` / `CreateDirectoryW` and the Steam-id string helper, which is the same
  `My Games\…\<SteamID64>\` construction as the start-up's
  ([the Phyre application page](../../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md)
  §7a). The 159-byte helper it calls is that Steam-id string helper. A 21-byte body also calls the builder, and
  `00408C30` calls a 21-byte Achievements-filed helper. **`008624C0` always returns 0**, so the loader always runs,
  whatever the folder builder does.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.**
  - The debug-status getter is read by three core bodies (83, 250 and 465 bytes).
  - A cited per-frame body is called by `MainLoop_UpdateAndRenderFrame` and four core frame bodies.
  - Two cited start-up bodies are called from the start-up subtree's root, and one from a boot-mode body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (19 edges through 4 of this page's functions).** The ActorEntity layer reaches this page at `0032ED80`, `0032FCA0`, `0032FC30`, `00408B10`. `ActorManager_RunFieldRuntimePass` is the worked example, read in full - it is the field-runtime pass over one manager record - `02098E10` at the **`0x288` stride** - which returns at once while the write-in-progress flag is set; **5 of the 16 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — CLIENT (32 edges through 7 of this page's functions).** The Resource layer reaches this page at `001D6F20`, `001D6E80`, `001D6FA0`, `0032FCA0` and 3 more. `FUN_0024f240` is the worked example, read in full - it is a 384-byte reader in an `0x88`-byte frame with a stack cookie: it opens a file and does nothing at all when that fails; **1 of the 19 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — SERVICE.** `00314440` on this page calls `FUN_00254ac0`, owned by that layer. What it reaches is a 117-byte sequence behind two gates - `[02092744]` zero and `([01E0C320] & 0xC0) != 0xC0` - after which eight calls run in fixed order; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## The `00408C30` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00408C30` (2,656 B) — the FF12CONFIG load pass. `0017D240` snapshots the
12-byte state pair (`00408C6A`), `00861EC0` initialises (`00408C80`),
then `"PS2Data/SQUARE_FF12/FF12CONFIG"` is opened and read through the
`001D6F20`/`001D6FA0`/`001D6E80` trio (`00408C88`–`00408CB6`). The
default-state fill writes `al` into `02B62DA8`–`02B62DBC`, sets
`02B62DAB = 1`, and stores the `si` word at `02B62DB4`
(`00408CCB`–`00408D89`). The `"debug"` key is looked up (`00408D97`),
the `"PS2Data//oldsave//" + "%snew%03d"` new-save path is formatted
through `0017D2E0` (`00408DE6`/`00408DFB`), `00862A20` returns the
`02EAF6E0` singleton (`00408E20`), and `00408ED0` plus two import calls
finish the pass (`00408E53`/`00408E6B`/`00408E7A`).

| member | role | interior |
| --- | --- | --- |
| `0017D240` (19 B) | state-pair getter — `[rcx] = qword[01F7F480]`, `[rdx] = dword[01F7F488]` (`0017D240`/`0017D24A`) | [`0017D240`](../../_index/ADDRESS-INDEX.md) |
| `00862A20` (21 B) | singleton accessor — `call 00862A40` then returns `&02EAF6E0` (`00862A24`/`00862A29`) | [`00862A29`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00861EC0`, `001D6F20`, `001D6FA0`,
`001D6E80`, `0017D2E0`, `00408ED0`, `00862A40`, and the two `008C2E00`/
`008C2F00` imports.

## The `0035FCA0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0035FCA0` (`InputControl_UpdateRegisteredChannels`, ~253 B) —
`00408B00()` must return 1 to enter the `022CAE90` bank walk
(`0035FCA4`/`0035FCB7`).

| member | role | interior |
| --- | --- | --- |
| `0035FDD0` | `ecx` `x 0x294` into `022CAE90` — 660-byte channel records (`0035FDD6`/`0035FDE0`) | [`0035FDD6`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00408B00`.


## Interior citation — frontier hub `001D6E80` (2026-09-18, SWE2-EC7)

`001D6E80` — 51 B, 6 A-measured callers; the `0x30`-record teardown paired with `001D6F20`'s
factory (measured on the application-root page). Interior verified: null-guarded, it runs
`0059BD80` ([`001D6E8E`](../../_index/ADDRESS-INDEX.md)) then `0016D6A0` and `free`/`00809950`
with `edx = 0x30` (`001D6E96`–`001D6EA3`), and returns 1 unconditionally. The constant return is
the standard `scalar deleting destructor` shape — the bool is the `free-after` flag.


## Interior citation — frontier hub `002DEBB0` (2026-09-18, SWE2-EC7)

`002DEBB0` — 23 B, 26 callers; the `002DDE20` zero-check behind the slot touches above.
Interior verified: `call 002DDE20` at [`002DEBB4`](../../_index/ADDRESS-INDEX.md), then
`test eax, eax; sete` — the predicate is "the `0215E6E0` object is absent or its `[+4]` bit 0x400 is clear",
inverted for the caller.

## SWE2-EC7-42 update (2026-09-19) - `00369510`

`00369510` (317 B) is a call-free dual-source string copier - selects a `01EF9338`/`01EF9340` or `01EF9348`/`01EF9350` pointer pair on `r8d`, optional `01EF9358` `cmovne`, then a `movzx [r10]`/`mov [rcx+r10]` NUL-terminated byte-copy loop. Interior anchor `00369560` (the copy loop).


## SWE2-EC7-66 update (2026-09-19) - `0035ED50`

`0035ED50` (131 B) is a call-free history-carry index compute - `-(x&~0xF)` + `r8d`, `rax*9` x4 stride into `r9`, `r10-1` bounds, `eax=-1` fallback. Interior anchor `0035ED66` (the `shr eax,4`/`neg`/`shl 4` form).


## SWE2-EC7-94 update (2026-09-20) - `0035F420` measured

`0035F420` (360 B) is the authored-record builder the two
`0035Fxxx` settings entries call: `00862660`/`00862670`/`00862680`
install three rip-relative handler tables, the argument byte at
`[rbx]` is normalized mod 16 (`ecx - ((ecx>>4)<<4)` via negated
shift), and a 16-iteration loop at `0035F4D0` fills a `9*4`-indexed
row at `+0x11` - bit `r8d` of the two-byte id (`r9d<<8 | table byte`)
either `bts`-sets bit `ecx` in `word[+2]` and writes a
`0035Fxxx`-indexed byte, or leaves 0x80 (0 once the bit counter
passes 3). `0035FAC0`, `0035F760`, `0016D6A0` and `0035F590` then
finish the record and `sil` lands in the `+0x44` byte at the same
`9*4` index.
Interior anchor `0035F4E2` (the table-indexed byte fetch inside the
fill loop).

## SWE2-EC7-113 update (2026-09-21) - `00862670` measured

`00862670` (8 B) is the
register-shuffle tail jump
`0035F420` runs: `rcx`
takes `rdx` and control
passes straight to
`001E09B0` - a second-
argument promotion and
nothing else.
Interior anchor `00862673`
(the `jmp`).

`00862660` (7 B) is the
`0035F420`-called
`-1`-store: `dword[rdx] =
0xFFFFFFFF` and return -
the smallest writer in the
family.
Interior anchor `00862666`
(the `ret`).

`0035F760` (856 B) is the channel-history builder `0035F420` calls once: a single `0035FBD0` call performs the history step - the `InputControl_PollAndBuildChannelHistory` path's inner stage.

Interior anchor `0035FA6B` (function `0035F760`).

`0035FBD0` (194 B) is the history stage `0035F760` and `0035FAC0` call: `r14 = movsxd r9d` bounds the loop, `word[r8 + r14*2 + 4]` is the indexed source, `edi = 0x10` strides the destination - the channel-history's word-array copy, call-free.

Interior anchor `0035FBF9` (function `0035FBD0`).
