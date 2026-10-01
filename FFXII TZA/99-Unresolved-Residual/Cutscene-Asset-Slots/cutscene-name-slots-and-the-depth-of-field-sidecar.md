---
system: Cutscene name slots and the depth-of-field sidecar
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Resource.CutsceneConfiguration
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0020AC30, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  residual_sha256: c5d4b7f7fb1ffbf0c3f54c671bb0af02b0513901af634c5ca755333ce3d338ff
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
---

# Cutscene name slots and the depth-of-field sidecar

> `0020AC30` records which cutscene asset is loaded in each of five slots, and decides from the
> **name itself** whether that scene gets a JSON file of camera focus settings. It was listed as one
> of two residual functions with no incoming reference of any kind. **It is live**, and finding its
> caller exposed a hole in the census that reported it dark.

---

## 1. What the player sees

**Cutscenes that are focused differently from the rest of the game.**

In *The Zodiac Age*, some scenes are shot with a shallow depth of field — the character being spoken
to is sharp while the background falls softly out of focus, the way a film camera behaves. Most of
the game is not rendered that way; the field and battle cameras keep everything crisp. Which scenes
get the cinematic treatment is not decided by the camera at run time. **It is decided by the
scene's name.**

When the engine loads a cutscene it writes the asset's name into one of five slots. If that name
carries a particular prefix, the engine goes looking for a companion settings file — a small JSON
document under `JsonData/CutScenes/` holding two numbers: the focus distance and the aperture. Those
are photographic terms and they do what they say. The focus distance is how far from the camera the
sharp plane sits; the aperture controls how quickly things blur as they move away from it.

If the name does not carry that prefix, no file is looked for, and the scene renders with the
ordinary camera.

So the player-visible rule is: **a cutscene is cinematically focused because someone named its asset
so that it would be**, and the depth of field they see is two numbers in a text file sitting beside
the scene data.

The other thing this function does is quieter but constant: it **refuses to redo work**. If the name
being written to a slot is the same one already there, it stops immediately. Reloading the same
scene does not re-read its settings.

---

## 2. Native mechanism

### It is reached through a thunk

```
ActorResource_BeginManagerResourceSetLoad   0032FCA0
   -> thunk_FUN_0020ac30                    001EC660   5 bytes, one JMP
      -> 0020AC30                           the slot setter
```

**That five-byte jump is why this function looked dark.** A call-graph census stops at a thunk, so
`0020AC30` shows zero incoming edges while a byte-level scan finds the jump immediately. See §8.

### The slot

The first argument is a slot index, bounded before anything else happens:

```c
if (param_1 < 5) { ... }        // five slots, checked, not masked
```

For the duration of the call the index is published to a global at `01DFE40C` and restored to
`0xFFFFFFFF` on exit — a "which slot is being loaded right now" marker. It is set before any work
and cleared on every exit path, including the early ones.

> **Corrected 2026-09-03.** This said *"**24** other functions read"* it. **23 functions reference
> it, and seven of them WRITE it** — `001EC520`, `001EC540`, `001EC620`, `001EC680`, `0020A760`,
> `0020AC30`, `0020AF10`. The reader/writer split matters more than the count: *"24 readers"* reads
> as a marker one place sets and many consult, and **a global written from seven sites across the
> image is a different object.** §7's question about what it represents should be read with that in
> front of it. *(The original figure came from a displacement scan known at the time to over-match;
> the corrected one is length-aware and controlled — see §14.)*

### The change guard

The new name is built into a local string, then compared against the one already in the slot —
length first, then `memcmp`:

```c
record  = 0x01F832F0 + slot * 0x20;          // 32-byte slot records
stored  = *(char **)record;                  // begin
storedN = *(int *)(record + 8) - (int)stored;// end - begin

if (storedN == newLength && memcmp(stored, newBegin, storedN) == 0)
        -> nothing happens at all
```

**Everything below this point is skipped when the name is unchanged**, which is what makes
re-entering the same scene cheap.

### The classification

On a genuine change the old entry is released if its per-slot flag is set, the new string is
assigned into the record, and then the name is searched for three literal substrings. All three
searches are `std::search`-shaped calls to `001C34D0` taking a `(first, last)` pair for both the
name and the needle:

```c
if (length > 3) {
    if (search(name, "sum_") == end || firstIndex == -1) {
        // NAME DOES NOT CONTAIN "sum_"
        if (search(name, "spc_") != end && firstIndex != -1)
                flagB = 1;                            // 01F832E9
    } else {
        // NAME CONTAINS "sum_"
        tmp = concat(name, ".json");
        FUN_001c5750(tmp);                            // -> JsonData/CutScenes/<name>.json
        release(tmp);
        if (search(name, "0001") != end && firstIndex != -1)
                flagA = 1;                            // 01F832E8
    }
}
```

The two flags are cleared at entry, so they describe **the most recent slot write**, not accumulated
state. Each is read by exactly one other function — `0020AA40` reads flag A, `0020AA30` reads flag
B — both tiny accessors, which is how the rest of the engine queries the result.

### The sidecar

`001C5750` is where the name becomes a file. It is the only direct callee that references both the
directory and the parameter names:

```
001C5750  ->  "JsonData/CutScenes/"      the directory
          ->  "mDofFocusDistance"        a key in the document
          ->  "mDofApertureFnumber"      a key in the document
```

`mDof…` is a member-name convention — an `m`-prefixed field. **Aperture f-number and focus distance
are the two parameters a depth-of-field effect needs**, which is what §1 describes in plain terms.

A wider family of about fifteen functions in `001C…` and `001EC…` references the same three strings,
so this is a subsystem rather than one path; only the part reachable from `0020AC30` was read here.

### What the names look like

The prefixes are not invented for the test — the executable carries a table of authored cutscene
identifiers in FFXII's own convention, and the `sum_` family is ~~eight~~ **seven** of them (recounted 2026-09-15):

```
mrm_g0100   bds_f0100   n1150       sum_j0001   sum_a0001   s0002
sum_f0001   sum_i0001   n1120_32    n1129       m1072_10    g0111
spc_z0000   hc1006      sum_m0001   sum_l0001   sum_h0001   hne_e0100
wdl_b0101   m1009       m1266       m1222       m1223       m1151
```

~~Eight~~ **Seven** `sum_` entries (`j`, `a`, `f`, `i`, `m`, `l`, `h`), each `sum_` + one letter + `0001`; one `spc_z0000`. **What the prefixes denote
is not established here** — the names are authored data and the bridge that would settle it lives in
the VBF archives, not the executable. §7 records it.

---

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0020AC30` | `CutsceneSlot_SetNameAndClassify` | 572 B | **residual when surveyed, classified at GN162 as `Resource.CutsceneAssetSlot.NameClassifyingSetter`.** The subject: slot write, change guard, three substring tests |
| `001EC660` | `thunk_FUN_0020ac30` | 5 B | The `JMP` that hides it from a graph census |
| `0032FCA0` | `ActorResource_BeginManagerResourceSetLoad` | — | The named caller, reached through the thunk |
| `001C5750` | `CutsceneDof_LoadSidecar` | 467 B | Composes `JsonData/CutScenes/<name>.json`, reads the two DoF keys |
| `0020A800` | — | 554 B | Predicate on the source object; gates the whole body |
| `0020AA50` | — | 476 B | Builds the name string from the source object |
| `0020A760` | — | 146 B | Releases a slot's previous entry |
| `001C34D0` | — | 186 B | `search(first1, last1, first2, last2)` — the substring test |
| `001B31E0` | — | 163 B | String concatenation, used for `name + ".json"` |
| `001A5760` | — | 154 B | String assignment into the slot record |
| `0020AA40` | — | 8 B | Reads flag A |
| `0020AA30` | — | 8 B | Reads flag B |
| `001EC5E0` | — | 17 B | Zero-extends flag A for its 3 consumers |
| `001EC5C0` | — | 17 B | Zero-extends flag B for its 4 consumers |
| `0025DF00` | `WorldActor_UpdateRuntimeAndScriptExecutionState` | 1228 B | The consumer read in §10: gates the script stop marker |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01F832F0` | slot records | `.data` | 5 × 32-byte string records, indexed by slot |
| `01F832B0` | per-slot flags | `.data` | 5 × 4-byte; non-zero means the slot holds a releasable entry. 14 referencing functions |
| `01F832E8` | flag A | `.data` | set when a `sum_` name also contains `0001`; read by `0020AA40` |
| `01F832E9` | flag B | `.data` | set when a non-`sum_` name contains `spc_`; read by `0020AA30` |
| `01DFE40C` | current-slot marker | `.data` | slot index during the call, `0xFFFFFFFF` otherwise. **23 referencing functions — 16 read, 7 write** (corrected, §14) |
| `00905988` | — | `.rdata` | `"sum_"` |
| `00905998` | — | `.rdata` | `"spc_"` |
| `00905990` | — | `.rdata` | `"0001"` |
| `008FB2B4` | — | `.rdata` | `".json"` |
| `008F9E70` | — | `.rdata` | `"JsonData/CutScenes/"` |
| `008FA470` | — | `.rdata` | `"mDofFocusDistance"` |
| `008FA488` | — | `.rdata` | `"mDofApertureFnumber"` |
| `00902540` | cutscene id table | `.rdata` | authored identifiers, `mrm_g0100` … `m1267` |

Addresses are Ghidra image base `0x00120000`.

---

## 4. Data structures and formulas

```
SlotRecord   at 0x01F832F0 + slot * 0x20        slot in 0..4
  +0x00  ptr   begin        pointer to the name bytes
  +0x08  ptr   end          one past the last byte
  +0x10  ptr   capacity
  +0x18  ptr   allocator    a vtable; +0x18 in it is the deallocate slot

PerSlotFlag  at 0x01F832B0 + slot * 4
  u32   non-zero  ->  the slot owns an entry that must be released before overwrite
```

**The bounds check and the marker:**

```c
if (slot >= 5) return;                 // checked, so no slot 5..255 aliasing
DAT_01DFE40C = slot;                   // published for the duration
...
DAT_01DFE40C = 0xFFFFFFFF;             // cleared on EVERY exit path
```

**The change guard, exactly:**

```c
storedLen = *(int *)(0x01F832F8 + slot*0x20) - (int)*(char **)(0x01F832F0 + slot*0x20);
newLen    = (int)end - (int)begin;
if (storedLen == newLen && memcmp(stored, begin, storedLen) == 0)
        -> skip everything
```

**The three substring tests.** `001C34D0` returns the position of the needle or `last`; the caller
also rejects a result whose offset from `begin` is `-1`:

```c
found(needle) :=  (search(begin, end, needle, needleEnd) != end)
               && ((int)result - (int)begin != -1)

length > 3  is required before any test runs      // all three needles are 4 bytes

  found("sum_")  ->  load "<name>.json";  if found("0001") then flagA = 1
  else if found("spc_")                        then flagB = 1
```

Note the asymmetry, which is in the code and not a simplification: **`0001` is only tested when the
name contains `sum_`, and `spc_` is only tested when it does not.** A name containing both `sum_`
and `spc_` sets flag A's branch and never reaches the `spc_` test.

---

## 5. Call chain

```
resource set load
  -> ActorResource_BeginManagerResourceSetLoad   0032FCA0
     -> thunk_FUN_0020ac30                       001EC660        [THUNK - graph censuses stop here]
        -> 0020AC30                              THIS SYSTEM
           -> 0020A800    gate on the source object
           -> 0020AA50    build the name
           -> 0020A760    release the previous entry            the release side of the line below
           -> 001A5760    assign into the slot record           [MEMORY OWNERSHIP, not a subsystem transition]
           -> 001A5760    assign into the slot record
           -> 001C34D0    substring test  x3
           -> 001B31E0    name + ".json"
           -> 001C5750    -> JsonData/CutScenes/<name>.json, mDofFocusDistance, mDofApertureFnumber
```

**Upstream:** one caller, through one thunk. The thunk is the *trigger*; the **owner transition** is
`001A5760`, where the slot record takes ownership of the name buffer and becomes responsible for
releasing it via `0020A760`.

**Downstream:** a JSON load, and two flags that reach `WorldActor_UpdateRuntimeAndScriptExecutionState` and gate whether an actor's script stands down for the frame (§10). The slot array is read by four
functions and the per-slot flags by fourteen.

**Do not confuse with the marker at `01DFE40C`.** It is written here but read by 24 functions across
the engine; it is shared context, not this system's private state, and its other readers were not
examined.

---

## 6. Modding notes

- **Depth of field is opt-in by filename.** To give a scene the cinematic camera, its asset name must
  contain `sum_` and a `JsonData/CutScenes/<name>.json` must exist with the two keys. No code change
  is required, which makes this the cheapest cinematic-look intervention in the engine.
- **`0001` and `spc_` set flags, not behaviour, here.** What the two accessors' callers do with them
  was not read. Do not assume the flags cause anything on their own.
- **The change guard will silently swallow an edit.** If you rewrite a scene's JSON but the slot
  already holds that name, nothing re-reads it — the guard compares the *name*, not the file. Force
  a different name, or a different slot, when iterating.
- **Regenerates itself:** the slot records and both flags. Write the name, not the derived state.
- **Breaks if:** a name is 3 bytes or shorter — every test is skipped and the scene is treated as
  unclassified, silently.
- **Five slots, hard.** The index is bounds-checked rather than masked, so a sixth concurrent scene
  is dropped rather than aliased onto slot 0.
- **Multiplayer / XIIOnline:** local presentation configuration. Not authoritative state.

---

## 7. What is not known

- [x] **UQ-335.** **What `sum_` and `spc_` denote.** ~~Eight~~ Seven authored `sum_?0001` identifiers and one `spc_z0000`
      exist in the executable's id table. The bridge that would name them is authored data in the
      VBF archives, not code. **`ff12-vbf` can open those**, which makes this tractable rather than
      merely open. **PROPOSED-repos9e-17.**
      *Half answered 2026-09-15 (FABLE): `sum_` is the summon scenes; `spc_` stays open.* This reads the full extract
      `D:/FFXII_TZA_extract` (`work/FABLE/drift4/uq335_sum_spc.py`).
      - **The executable has seven `sum_` ids, not eight** (`j`, `a`, `f`, `i`, `m`, `l`, `h`, all `…0001`). A search
        of the whole image for `sum_?NNNN` / `spc_?NNNN` finds those seven and `spc_z0000`, nothing more.
      - **The event data has thirteen `sum_` families, `sum_a` … `sum_m`.** Each has three scenes under
        `plan_master/<lang>/event/`:
        - `0000`, 2,368–2,560 B;
        - `0001`, 10,944–34,304 B, the long one;
        - `0002`, 1,600 B.
        Each of the 39 scenes also has a `JsonData/CutScenes/<name>.json`.
      - **The scripts name themselves summons.** All 39 `.ebp` files carry the authored name `summon`. The 13
        `0000` scenes carry `summon_event` and `summon_appear`, and three scripts also carry `summon_weapon`. `sum_c0001` labels its
        cuts `sum_cut02` … `sum_cut06`.
      - **Thirteen matches the Espers.** The action table has thirteen summon rows, Belias … Zodiark
        ([the action definition row](../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)).
        Which letter is which Esper is not bound here: no script string names one.
      - **`spc_z0000` is a single event.** It has a 3,008-byte script whose names are only `init`, `main`, `message`,
        `messageterm`, `target00` and `PC00`, plus a sound bank and `.vpc` / `.vpcjp` files. ~~What `spc` abbreviates is
        not settled by these names.~~
      - **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): `spc_` is the special-attack (`spattack`) event.** A census of
        every call instruction in the 1,123 `us` and `bin` `.ebp` files — call opcodes `0x58` / `0x59` / `0x5D` / `0x5E`
        plus a 16-bit id, the CR-2 method — finds each verb of the `spattack` family exactly once, and all four in
        `spc_z0000.ebp`. The verbs are `0x2A8` `openspattackwindow`, `0x2A9` `spattackwindowsync`, `0x29E`
        `spattacksync` and `0x2A1` `isfusion_spattack`. No other script calls any of them. `0x2A8` is also the only
        producer of UI request 12, the window a dedicated router arm builds
        ([the request router](../../16-UI/Request-Router/ui-request-router.md), UQ-162). So `spc_z0000` is the scene that
        opens and drives the special-attack window.

        *Not established:* the player-facing name. The labels `spattack` and `fusion` suggest the Quickening and its
        concurrence, but no string was read. Also not established: which `sum_` letter is which Esper.
- [x] ~~What the two flags cause.~~ **ANSWERED 2026-09-03, §10.** They gate whether an actor's
      script stands down for the frame after the VM runs a step: a `spc_` scene **suppresses** one
      stop condition in world states 1-2, a `sum_…0001` scene **enables** one in state 3.
      **PROPOSED-repos9e-18 closes** — with the bound that one consumer of three (flag A) and of
      four (flag B) was read.
- [x] **UQ-336.** **The other consumers of the two flags.** `0034CF90` and `0034D790` (137 B each) have **zero
      callers by graph or bytes**; `00180120` is now read — a two-predicate conjunction (`001EC5C0`/`001EC560`, a mode-indexed probe) called by the PauseMenu handler `00229590` ([game-application §`00229590` subtree](../../00-Engine-Core-Runtime/Application-Root/game-application.md)); it does not name flag B, so the consumer count stands. **PROPOSED-repos9e-20.**
      *Both named consumers are now READ (2026-09-15, OPUS): identical twins applying a rate
      multiplier that ships as 1.*
      - **`0034CF90` and `0034D790` are the same function with one call swapped.** Byte for byte the
        same shape: take a value from `00267E10` into `edi`, read a fifth stack argument
        `rsi = [rsp+0x50]`, test `[rsi+0x28] == 3`, then run the same two-predicate gate
        (`001EC5C0`, `001ED180`). **On the passing path they call different wrappers** —
        `0034CF90` calls `00265880`, `0034D790` calls `00265860` — and store the result to the
        out-pointer `rbx`. **On the failing path both store the input UNCHANGED** (`0034D00C`,
        `0034D80C`).
      - **Both wrappers do one thing, and it is the same thing.** `00265860` (32 B) calls `001EDDA0`
        and, **only if it returns zero**, applies `imul ebx, [01DFE0B4]`; `00265880` (46 B) is the
        same with one extra leading test through `001EDC80`. §11 already identifies `001EDDA0`
        as one of *“two faces of one runtime mode”*.
      - **The multiplier ships as 1.** Read from the image — `01DFE0B4` is `.data` at file offset
        `0x1CDC6B4`, well below the file-backed bound `01F7E400` — and its dword is **`1`**, with
        its float twin at `01DFE0B8` shipping as **`1.0`** (`0x3F800000`). **So in the shipped image
        the transform is an identity**, and what these consumers do with the flags is scale a
        scheduling value by a factor that is currently one.
      - ~~**Still open, and the row stays open for it:** whether these two exhaust the consumer set.
        §10 counts **three** consumers for flag A and **four** for flag B with one of each read;
        this reads the two named here and `00180120` was already read, which does not account for
        all seven.~~
        **ANSWERED 2026-09-15 (OPUS, accepting FABLE's census from `16243926`, re-derived): the seven
        are CALL SITES, not functions, and the set IS closed.** `001EC5C0` (flag B) × 4 — `00180124`,
        `0025E0F0`, `0034CFDC`, `0034D7DC` — and `001EC5E0` (flag A) × 3 — `0025E100`, `0034CFB7`,
        `0034D7B7` — fall in **four** functions: `00180120`, `0025DF00`
        (`WorldActor_UpdateRuntimeAndScriptExecutionState`, §10's own subject), `0034CF90` and
        `0034D790`. **All four are read.** No `u64` or `u32` pointer to either wrapper, or to
        `0020AA30` / `0020AA40`, exists anywhere in the mapped image, so no table reaches them.
        *Bound:* a call through a pointer assembled rather than stored, or a read through a computed
        address, would be invisible to all three scans.
      - *(Unchanged: both have zero callers by graph and by byte decode.)*
- [x] ~~The predicates in the gate.~~ **ANSWERED 2026-09-03, §11.** All five read. `00357770` is a
      **veto** raised by native script commands mid-operation; `001ED130` is a two-case field-id
      exception that consults the cutscene slot marker; `001ED180` requires one of three transition
      field ids; `001EDDA0`/`001EDE80` are two faces of one runtime mode.
      **PROPOSED-repos9e-21 closes.**
- [x] ~~**UQ-337.** **What the hard-coded ids name** — field `0x19`, `0x10C7`; transition `0x2F4`, `0x2E9`,
      `0x27B`. Same VBF-side bridge as `-17`. **PROPOSED-repos9e-22.**~~ **ANSWERED 2026-09-25 (FABLE, Claude
      Opus 5.5).** The three transition ids name the maps **`alc_a01`** (`0x27B`), **`alc_f01`** (`0x2E9`) and
      **`alc_c01`** (`0x2F4`), through the per-map path table the field loader indexes. **`0x19` and `0x10C7`
      are not field ids.** `00265270` returns the story-progress variable, so they are progress values
      **25** and **4295**. Which story beats those values mark is not established. See
      [§ UQ-337 answered](#uq-337-answered--three-maps-and-two-story-progress-values-fable-claude-opus-55-2026-09-25).
- [x] ~~What the 15 ScriptVM commands named in §11 do.~~ **ANSWERED 2026-09-03, §12.** All 23
      handler bodies read. **They are the script's waiting commands** — eight wait for a button,
      two for a condition, one for a frame count, two produce a value and yield, two are a bracket.
      **PROPOSED-repos9e-23 closes.**
- [x] ~~`FUN_00267310`, the shared escape.~~ **ANSWERED 2026-09-03, §13.** It reads byte `+0x201`
      of a 648-byte **actor-manager record**, indexed by `actor[0x15]`. It is a **bitmask**, set one
      bit at a time from two ScriptVM commands and four engine paths; **65 functions read it**,
      including the simulation tick and movement steering. Waits test the **whole byte**, so any bit
      ends every wait belonging to that manager. **PROPOSED-repos9e-24 closes.**
- [x] **UQ-338.** **The eight bit assignments in `+0x201`.** None recovered; the constants sit in the four
      setter callers, none read. **PROPOSED-repos9e-25.**
      **ANSWERED 2026-09-15 (FABLE), static — the bits are an index, not eight named flags: bit *k* is the manager's
      skip request *k*.** Both setter paths are read on
      [the world tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md), *Slot 0's byte
      is never set*.
      - The only bit-level writer is `0026A5B0(manager, on, bit)`, which runs `bts` / `btr` on `+0x201`
        (`0026A5CF` / `0026A5DA`).
      - **Its two callers pass the request index as the bit.**
        - Skip begin `00360710(k, m)` calls it as `(m, 1, k)` with `r8d = r14d = k` (`00360854`–`0036085B`).
        - Skip end `00360A50(k, m)` calls it as `(m, 0, k)` (`00360AD6`–`00360AFA`).
        - *k* indexes the manager's eight 16-byte skip-request entries at `022CB730 + (m × 8 + k) × 16`.
      - **The "four setter callers" are routes to these two, not four constants.**
        - ScriptVM `skipexec` (1337) pops *k* from the script.
        - Command 1306's poll handler calls skip end for its request.
        - The engine loop `003603F0` walks *k* = 0 … 7.
        - The engine path `00360880` passes the index of the set pending bit.
      - **So a bit means "request *k* of this manager is running".** Every wait's escape and the world tick's
        fast-forward test the whole byte, meaning any skip in progress. Which scene numbers its requests 0–7 is
        script data, not an engine assignment.
      - *Re-verified from the bytes before publication (2026-09-15, FABLE).* `0026A5B0(ecx, edx, r8d)` indexes
        `02098E10 + ecx × 0x288`, reads `+0x201`, and runs `bts`/`btr` with **`r8d` as the bit**
        (`0026A5CF` / `0026A5DA`). The begin path reaches it with `edx = 1` (`ebp` set at `0036078B`) and the end
        path with `edx = 0` (`xor edx, edx` at `00360AF8`); in both, `r8d = r14d`, and `r14 = movsxd ecx` is the
        function's **first** argument while `rsi = movsxd edx` is the manager — which is also the entry index
        `022CB730 + (r14 + rsi × 8) × 16`. **One correction of emphasis:** `0026A5B0` is the only *bit-level*
        writer, but not the only writer. `ActorManager_BindLoadedDefinitionPayload` stores the **whole byte** at
        `0026CC38`, inside a run of stores that all take their value from the zeroed `rbx` — a clear on bind,
        which is consistent with the reading rather than against it. Readers of the byte are
        `WorldActorScriptVM_InterpretBytecode` (`0025E5C5`) and the getter `00267300`. *Bound:* a displacement
        scan sees `[reg + 0x201]`; a write through another addressing form would not appear.
- [x] **UQ-339 ANSWERED 2026-09-15 (OPUS) — the file holds far more: **116 distinct keys**, and
      it is an *editor document* of which the shipped build reads a subset. Censused over every
      shipped sidecar, not inferred.**
      - **Corpus.** `jsondata/CutScenes/` and `jsondata/cutscenes/` hold **674** files. **620 parse**,
        **52 are zero bytes**, and 2 more have syntax errors. Together they carry **7,560 sections**.
      - **Shape.** Each file is an object of sections: **`Common`** plus **`Cut 1` … `Cut 61`**
        (61 is the highest seen). Section sizes cluster hard: **9 keys** in 5,148 sections and
        **4 keys** in 1,360, with a rich **80-key** variant in 530.
      - **Four keys appear in every one of the 7,560 sections** — `mShadowValueLerpMinForMap`,
        `mShadowValueLerpMinForChr`, `mContrastR` and `m_iPCFBlurSize` — so the document is a
        **post-process and shadow parameter block**, not a depth-of-field pair.
      - **The DoF family is five keys, and the code reads two of them.** `mDofApertureFnumber`
        (6,154 sections), `EnableDof` (6,146), `mDofFocusDistance` (6,122), `mDofFocusDistanceLock`
        (5,510) and `mDofApertureFnumberLock` (5,508). §'s reading that `001C5750` takes
        `mDofFocusDistance` and `mDofApertureFnumber` is unchanged and correct.
      - **But 70 of the 116 keys exist as strings in the image**, so the sidecar is consumed well
        beyond this loader — shadows (`mCascadePartition0/1/2`, `m_iPCFBlurSizeForMap`,
        `EnableShadow`), SSAO and HBAO (`mSAO*`/`mHBAO*` for `Chr` and `Sce`), unsharp mask
        (`mUSM*`), glare, gamma, image-based lighting (`EnableIBL`), and **`EnableYebis`**.
      - ⚠ **46 keys are shipped in the data with NO literal string in the image, and that does not
        make all of them unread.** **32 are `PresetDof 1` … `PresetDof 32`** (564 sections each), and
        **those are read.** ~~authoring tool state~~ *(corrected 2026-09-15, OPUS, accepting
        FABLE-CONTRA-OPUS-UQ339-PRESETDOF-IS-READ after re-deriving it from the bytes)*. `001C3D50`
        composes the key at run time: when the cut's preset index
        `[01F81400 + ([01F813F8] + cut × 2) × 4]` is not `-1` (`001C4037`–`001C404D`) it copies the
        10-byte literal `"PresetDof "` (`008FB310`, `001C40D8`–`001C40F2`), appends the index as text
        (`001C4107`), and reads `Common` → that key → `mDofApertureFnumber` / `mDofFocusDistance`
        (`001C4157`–`001C41C1`) into `00194250` (`001C41E9`). Only at `-1` does it read the cut's own
        values (`001C421E`–`001C4274`). `001C6E20` (`ReadPresetDofForCutSceneObj`) writes the index
        table at `001C720D`. **A string search misses the key because it is never one literal.**
        The rest are the `*Lock` flags — `EnableDofLock`, `EnableYebisLock`, `mDofFocusDistanceLock`,
        `mDofApertureFnumberLock`, `mGammaValueLock`, `mGlareLuminanceLock`, `mGlareThresholdLock` —
        and no reference to any of them was found; `mCascadeNumber`, which nothing reads, is `3`
        wherever it is authored and the reader hardcodes `3`; and the six `mCascadePartitionN_2` /
        `_3` keys **are read** — `001C7940` composes them from the template
        `"mCascadePartition%d_%d"`
        ([the render-parameter page](../../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md)
        §8d, `761bee78`). **Two of the keys this page once called authoring state are composed at run
        time, which is why a literal search never finds them.**
      - **That names what *part* of the file is.** The lock checkboxes are authoring-tool state:
        **`mDofFocusDistanceLock` appears in 5,510 sections and nothing in the shipped image reads
        it.** **The preset bank is not in that class:** whenever a cut names a preset, the engine uses
        that preset's aperture and focus distance instead of the cut's own.
      - **How the cascade half was established, and who got it wrong first.** The loop is
        `001C9190`–`001C9209`: `c ∈ {0,1,2}`, `q ∈ {1,2,3}`, into a **3 × 3 float matrix** whose sink
        `001A9B00` rejects either index `>= 3` — which is also why `mCascadeNumber` needs no reader,
        being `3` in all 284 sections that author it. **FABLE published the opposite as `W-9` earlier
        the same day and corrected it within hours** (`d42683db` → `761bee78`), by the identical
        method that produced this page's original `PresetDof` error: comparing authored names against
        **literals**. **Of the 46, only the seven `*Lock` flags and `mCascadeNumber` are now
        unreferenced.**
      - *Control, so the absences mean something:* the two keys `001C5750` is known to read are both
        found by the same string search that reports the other 46 missing. **The control has a limit
        that `PresetDof` and `mCascadePartition%d_%d` both expose: a key composed at run time is
        invisible to a string search**, so a missing literal is evidence about the *search*, not about
        the key. **UQ-339.**
- [x] **UQ-340.** **The other ~15 functions** in `001C…`/`001EC…` referencing the same three strings. Only the
      path reachable from `0020AC30` was read.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): twelve functions, not about fifteen, and each has a role.** A
      `rip`-target sweep over the three strings (`008FB2B4` `".json"`, `008FA470` `"mDofFocusDistance"`, `008FA488`
      `"mDofApertureFnumber"`) finds these:
      - **The two DoF keys are read by six:**
        - this page's sidecar `001C5750`;
        - the two scene-parameter loaders, the cutscene one `001C3D50` (`001C4179`–`001C4248`) and the map one
          `001C7940` (`001C7AE2`–`001C7B30`). They are the loaders that fill the render-parameter block (the
          post-processing contract, §4a);
        - the slot setters `001EC520` and `001EC540`, which tail-jump `001C5570` with one key each (UQ-341 above);
        - a 158-byte per-index recorder, reached from a script-VM handler. When its first argument is 0 it reads both keys
          from the document at `01F81328` and records them, with the argument, in a per-index table. It is named by role
          here because the script-VM crossing it would import is not this page's to account; the register row carries its
          address.
      - **One writes them back:** `001CC800` publishes `EnableDof` and both keys into the current slot's document (read
        on [the shared command-state word](../../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md)).
      - **Five compose a `.json` path:** `0020AC30` (this page's path); `001C53F0` (`name + ".json"`); `001C5930`
        (`JsonData/CutScenes/<name>.json`, and a `<name>_2ndScreen.json` variant that no shipped cutscene file has);
        `001C5F20` (`JsonData/FontCluts/<name>.json`; `jsondata/fontcluts/` ships); and `001C61F0`
        (`JsonData/Maps/<name>.json`, the map loader's driver).
      So the family is the scene-JSON loaders and their DoF slot plumbing. None of the twelve reads a DoF key from a
      source other than a scene JSON document.
- [x] ~~**UQ-341.** **What the 16 readers of `01DFE40C` do with it — and why it has 7 writers.** Corrected from
      "24 readers" (§14). A marker written from seven sites is not a slot index one place publishes;
      whatever it is, this document's §2 description of it is too simple.~~
      **ANSWERED 2026-09-14 (FABLE): it is a current-slot latch.** Every entry point that takes a slot index stores
      it there first, and the internal accessors act on whatever slot was stored last. Its `.data` value is
      `0xFFFFFFFF` (none).
      - **The seven writers are the seven slot-taking entry points** (RIP census):
        - Four small setters store `ecx` clamped to 0–4, anything larger becoming `−1` (`cmp ecx, 4` / `cmova`):
          `001EC520` (`001EC532`) and `001EC540` (`001EC552`) then tail-jump `001C5570` with a key string
          (`008FA470` / `008FA488`); `001EC620` (`001EC638`) then calls `0018CA40`; `001EC680` (`001EC689`) only stores.
        - `0020AC30`, the slot fill, stores the index unchecked (`0020AC64`), then tests `≤ 4`. It resets the latch to
          `−1` when the name does not parse (`0020AE48`).
        - `0020A760`, the slot clear, stores the index (`0020A760`), empties that slot's strings and zeroes
          `01F832B0[i]`, and always ends by resetting the latch to `−1` (`0020A7E7`).
        - `0020AF10` stores the index (`0020AF5B`) and copies a string into that slot.
      - **The sixteen readers are the per-slot accessors.** Each loads the latch sign-extended, bounds it `≤ 4`, and
        indexes a per-slot table with it. For example `001EC500` returns `01F832B0[latch]` (0 when none), and
        `001EC560` / `001EC600` test that entry before acting. They take no slot argument of their own, which is why
        the entry points must set the latch.

      So §2's "slot index" is right about the value and too simple about the protocol: select by storing, then
      call. An entry point that omits the store acts on the previously selected slot.

---

## `UQ-249` answered from the shipped sidecars — and the `"0001"` test explains itself (FABLE, 2026-09-22)

This page has the mechanism: the two branches, the flags `01F832E8` / `01F832E9`, and the three
literals. **What it asks is what the prefixes denote, and the shipped data answers it.** The
sidecars live in `jsondata/cutscenes/` — **337 files** across about forty `xxx_` families.

| family | files | groups | sequences | non-empty |
|---|--:|---|---|--:|
| **`sum_`** | **39** | **13** — `a`…`m` | `0000`, `0001`, `0002` | **13** |
| **`spc_`** | **1** | 1 — `z` | `0000` | 1 |

### Why the image tests `"0001"` (FABLE, 2026-09-22)

> **All 13 non-empty `sum_` sidecars are the `0001` one, and every `sum_` file at `0000` or `0002`
> is ZERO BYTES.** The corpus makes it exact: there are **26 zero-byte sidecars in all 337**, they
> are **all `sum_`**, and they split **13 at `0000` and 13 at `0002`**.

**So `"0001"` is not a magic number — it is the only sequence slot a summon cutscene actually
ships data in.** The `0000` and `0002` slots exist as named placeholders and are empty. *Flag A at
`01F832E8`, set when a `sum_` name also contains `0001`, is therefore “this cutscene has a real
sidecar”* — and that is why the `spc_` branch never tests for `0001`: `spc_z0000` is non-empty at
sequence **`0000`**, so the same test would have rejected the one file it needs.

**The seven `sum_` letters this page recovered from the image (`j a f i m l h`, each with `0001`)
are a subset of the thirteen on disk**, and every one of them is at the single sequence that
carries data — the two readings agree, and the disk supplies the six the slot table does not list.

### What the sidecar carries (FABLE, 2026-09-22)

`spc_z0000.json` and the `sum_?0001.json` files share one schema: a **`Common`** block of **80
keys** followed by per-cut overrides named **`Cut 1`, `Cut 2`, …**. The keys are render tuning —
`mGammaValue`, `mUSMBlur` / `mUSMIntensity` / `mUSMThreshold`, `mDofFocusDistance`,
`mDofApertureFnumber`, `mShadowValueLerpMinForMap` / `…ForChr`, `mCascadeNumber`,
`mCascadePartition0`… **So the sidecar is per-cutscene, per-cut visual tuning**, which is what the
`.json` lookup in the `sum_` branch is for.

> **What the prefixes stand for, stated as the reading the counts support rather than as proof.**
> Thirteen `sum_` groups is exactly the number of Espers FFXII ships, and `sum` is the ordinary
> abbreviation for *summon*; `spc_` reads as *special*, and there is exactly one of it. **The bytes
> give the structure and the count; they do not spell either word**, and no string in the image or
> the sidecars names an Esper, so this stays a reading.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Five slots, bounds-checked, 32-byte records | complete exact-current body of `0020AC30` | 1 |
| The change guard: length then `memcmp`, skip on equal | same body | 1 |
| The three substring tests and their exact nesting | same body, with the needle addresses read from `.rdata` | 1 |
| The needles are `"sum_"`, `"spc_"`, `"0001"`, `".json"` | bytes at `00905988`, `00905998`, `00905990`, `008FB2B4` | 2 |
| The sidecar path and the two DoF keys | `"JsonData/CutScenes/"`, `"mDofFocusDistance"`, `"mDofApertureFnumber"`, each the target of a RIP-relative `LEA` inside `001C5750` | 2 |
| The authored id table and its `sum_`/`spc_` members | contiguous `.rdata` strings at `00902540`ff | 2 |
| The marker at `01DFE40C` is referenced by **23** functions — **16 read it, 7 write it, 2 do both**; per-slot flags 14 | displacement census over `.text` (**corrected 2026-09-03, was "24 readers"** — see §14) | 11 |

### It is reached through a thunk, and that is why it looked dark

This function was published as one of two residual functions with **no admissible incoming reference
of any kind**. That was wrong, and the reason is worth more than the correction.

```
route 1  call-graph incoming edges              : 0
route 2  direct CALL/JMP, decoded from bytes    : 1   <- 001EC660, thunk_FUN_0020ac30
route 3  RIP-relative LEA to it                 : 0
route 4  8-byte / 4-byte encoding in the file   : 0 / 0
```

*Control for route 2:* the same scan finds 10 calls **out of** `0020AC30`, so it can see call
instructions in this neighbourhood. **PASS.**

**The census that missed it used the call graph, and a thunk is a sink in the call graph.** This
database already documents that, in
[the thunk layer](../../24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md),
whose §1 calls it *"the single most common way a measurement of this binary comes out wrong"* and
whose §2 states that a graph census **loses the path at the thunk**. The warning was written down and
was not consulted.

**The cost across the whole population was measured rather than assumed.** Comparing graph callers
against byte-decoded callers for all 158 residual functions:

| | count |
|---|---:|
| callers in both graph and bytes | 143 |
| graph only | 0 |
| **bytes only — the graph missed them** | **1** (`0020AC30`) |
| neither | 14 |

So the thunk hole cost exactly one function — and that one function was half of the "two are
evidence-free" result. **The corrected figure is 144 of 158 with a direct caller, and 1 of 158 with
no admissible reference of any kind.**

### It does not weaken the dead-code finding next door

[`00392A10`](../Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md) was established
dead by the same four routes, and route 2 there is byte-level, so a thunk would have been caught.
Re-checked explicitly for indirect thunks: the `FF 25` (`jmp [rip+disp32]`) form occurs **291 times**
in `.text` (control: the form is present and found, **PASS**), but such a thunk needs a pointer slot
holding the target address, and the 8-byte encoding of `00392A10` occurs **zero** times anywhere in
the file. **No indirect thunk can reach it.** That finding is now stronger than when it was
published, not weaker.

---

## 14. Instrument note — three narrow matchers in one session

Recorded because the pattern matters more than any of the three corrections.

**My RIP-relative instruction matcher has been too narrow three times today, and every time a
control caught it, never review:**

| where | what was missing | what caught it |
|---|---|---|
| Audio boundary pass | the modrm **REG** field was hardcoded to `0`, so only `EAX`-sourced stores matched — it reported `02091098` as having **zero** writers | requiring the scan to find six writers **the document under attack itself named** |
| Spawn pass | only the `BT`/`BTS`/`BTR`/`BTC` family, so a 64-bit bit test encoded as `mov r64, imm64` was invisible — it found bit 26 and nothing else | a **partial positive in the same body**: bit 26 appearing made the absence of 45 and 49 suspicious rather than conclusive |
| this global's census | **`MOVSXD` (`63 /r`)** absent from the form list, so sixteen `movsxd rax, dword [rip]` readers were invisible — it reported 7 referencing functions where there are 23 | a **known positive I had read myself**: `001ED130`'s decompiled body plainly reads this global and the scan did not find it |

**The lesson is not "add more forms".** An x86 form list is never complete, and each of these three
looked complete while it was being used. The rule that actually works:

> **Every absence claim from an instruction matcher needs a known-positive control, chosen before
> the scan runs.** The cheapest source is the document under attack: any document stating a positive
> fact has handed you a set the scan must find.

All three of mine were caught that way and none by inspection. **A scan that finds nothing has told
you nothing until it has found something you already knew was there.**

## 9. Related

- [`../Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md`](../Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md)
  — the other function from the same pair, and genuinely dead.
- [`../Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`](../Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
  — §16, the reference census this corrects.
- [`../../24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`](../../24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
  — the recorded warning this pass walked into.
- [`../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)
  — where the authored data that would name `sum_` and `spc_` lives.

## 10. What the two flags cause — `PROPOSED-repos9e-18` answered

§2 established that the two flags are set from the cutscene's name and read by two tiny accessors.
This section follows them to their consumer. **They gate whether an actor's script yields for the
frame after the script VM runs.**

### The path from flag to decision

Each flag has exactly one reader in the whole binary, and each reader has exactly one caller:

```
01F832E8  flag A  ->  0020AA40  (8 B)  ->  001EC5E0  (17 B, zero-extends the byte)  ->  3 consumers
01F832E9  flag B  ->  0020AA30  (8 B)  ->  001EC5C0  (17 B, zero-extends the byte)  ->  4 consumers
```

Both adapters are pure pass-throughs — `return reader();` — and their caller sets are identical in
the call graph and in a byte-level decode, so no thunk is hiding a consumer here.

### The gate, in `WorldActor_UpdateRuntimeAndScriptExecutionState`

The named consumer runs a per-frame loop over an actor's script entries — `0x28` bytes each,
indexed by a current-entry byte. In entry states 1 and 2 it runs bytecode and then decides whether
to stop:

```c
result = WorldActorScriptVM_InterpretBytecode(worldActor, actor, entry);

if ( (   result != 0
      || (  ( FUN_001ed130() != 0 && (worldState - 1u) < 2 && flagB() == 0 )   // states 1,2
         ||  ( worldState == 3 && flagA() != 0 )                               // state 3
         ||  ( DAT_022C7F84 != 0 ) ) )
     && FUN_00357770() == 0 )
{
        entry[0x16] = 1;
}
goto endOfFrameForThisActor;
```

`(worldState - 1u) < 2` is unsigned, so it means **`worldState` is 1 or 2** — and the `worldState == 3`
arm is a separate, disjoint case.

**So the two flags act in opposite directions, and in different states:**

| flag | set when the loaded name… | effect on the gate |
|---|---|---|
| **B** (`01F832E9`) | does **not** contain `sum_` but does contain `spc_` | **must be CLEAR** for the state-1/2 arm to contribute — a `spc_` scene **suppresses** it |
| **A** (`01F832E8`) | contains `sum_` **and** `0001` | **must be SET** for the state-3 arm to contribute — a `sum_…0001` scene **enables** it |

### What `entry[0x16]` does

It is a one-shot stop marker, and the same loop consumes it on the next pass:

```c
do {
    if (FUN_001ed180() && !FUN_001ede80()) break;
    entry = actor->entries + actor->currentEntry * 0x28;
    if (FUN_001edda0() == 0) {
        if (entry[0x16] != 0) {
            entry[0x16] = 0;                     // consume it
            if (FUN_001ed180() == 0) break;      // and stop for this frame
        }
    } else {
        entry[0x16] = 0;                         // cleared unconditionally on the other branch
    }
    switch (entry[5]) { ... }
} while (...);
```

Set at the end of a bytecode step, cleared and acted on at the start of the next — **a script that
runs a step and then stands down until the following frame.**

**So the player-facing consequence is that the name of the currently-loaded cutscene changes how
often actor scripts stand down during that scene.** A `spc_` scene removes one reason to stop in two
world states; a `sum_…0001` scene adds a reason to stop in a third. Whatever else the naming
convention encodes, it reaches past the depth-of-field sidecar and into script pacing.

### Bounds on this reading, stated

- **One consumer of three (flag A) and of four (flag B) was read.** The others are `0034CF90` and
  `0034D790` — 137 bytes each, and **each has zero callers by both the call graph and a byte-level
  decode**, so they are in the position `00392A10` was before it was read. `00180120` (39 B,
  called from `00229590`) is now read — it conjoins `001EC5C0` and `001EC560` (a `[01DFE40C]`-indexed
  table probe), neither of which names flag B; it is a PauseMenu-side predicate, not a confirmed
  consumer. **The gate above is one use of these flags, not the only one.**
- **`entry[0x16]` is described by its behaviour in this loop.** Whether anything outside this
  function reads it was not established.
- `FUN_001ed130`, `FUN_001ed180`, `FUN_001edda0`, `FUN_001ede80` and `FUN_00357770` are treated as
  opaque predicates. Naming what they test would sharpen the gate considerably and none was read.
- The world-state value (`param_1[5]`) is used as 1, 2 or 3 and its meaning is not established here.

## 11. The five gate predicates, named — `PROPOSED-repos9e-21` answered

§10 stated the stand-down gate with five opaque terms. All five are read here. **The most important
is `00357770`, which can veto every other arm — and it turns out to be the script telling the engine
it is still working.**

### `00357770` — "a native script command is mid-operation"

Seven bytes: `return DAT_022C7F88;`. Its partner `00357760` is eleven bytes: `DAT_022C7F88 = 0;`,
and the consumer calls it **immediately before** running bytecode:

```c
FUN_00357760();                                       // clear
result = WorldActorScriptVM_InterpretBytecode(...);   // run one step
if ( (...arms...) && FUN_00357770() == 0 )            // was it raised during the step?
        entry[0x16] = 1;                              // only then stand down
```

So the flag is **cleared before every step and tested after** — it reports what happened *inside*
that step. Who raises it settles what it means. Scanning `.text` for RIP-relative writes:

| writers | how |
|---|---|
| 6 functions | `MOV dword [rip], 1` |
| 7 functions | read-modify-write through a register |
| `00357760` | the clear, `= 0` |

**Thirteen of those fourteen writers are ScriptVM native command handlers**, located by looking them
up in the dispatch table at `01EED720` documented in
[the ScriptVM native dispatch table](../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md):

```
cmd   45  00356C40  (+0x10)      cmd 1018  00340C70  (+0x10)
cmd   46  00357530  (+0x10)      cmd 1019  003414E0  (+0x10)
cmd   47  0033F8E0  (+0x10)      cmd 1020  00341D70  (+0x10)
cmd   48  003401F0  (+0x10)      cmd 1021  00342450  (+0x10)
cmd  641  0034BBD0  (+0x10)      cmd 1304  0034AF20  (+0x00)
cmd 1056  0034A1D0  (+0x10)      cmd 1305  0034B290  (+0x00)
cmd 1415  0034E630  (+0x10)
```

*Control:* that table's record census reproduces the documented figure exactly — **1,234 records with
a non-null field `+0`**, as `scriptvm-native-dispatch-table.md` §4 states. **PASS.** A wrong base or
stride would not land on it.

**Eleven of the thirteen write from field `+0x10`**, the third handler slot — the one that runs while
a command is still in progress rather than at its start. So the flag means: **a native script command
signalled during this step that it has not finished.** When it is raised, the stand-down is vetoed
outright, whatever the other arms say.

### `DAT_022C7F84` — an authored begin/end bracket

The gate's third arm is a bare global test. It has exactly two writers, and both are ScriptVM
commands:

```
cmd 1485  00341030  (+0x00)   ->  DAT_022C7F84 = 1
cmd 1486  003413E0  (+0x00)   ->  DAT_022C7F84 = 0
```

A paired set/clear on consecutive command ids is a **scripted bracket**: authored data turns the
behaviour on for a region of script and off again. Because it sits in an `OR`, raising it makes the
stand-down fire on every step until command 1486 clears it.

### `001ED130` — a field-id exception list, wired to the cutscene slot

```c
fieldVar = FieldData_GetVariable0();
slotFlag = (DAT_01DFE40C < 5) ? perSlotFlag[DAT_01DFE40C] : 0;
return !( fieldVar == 0x19 || (fieldVar == 0x10C7 && slotFlag == 5) );
```

**It reads `DAT_01DFE40C` — the current-slot marker `0020AC30` publishes (§2) — and
`01F832B0`, the same per-slot flag array.** The two systems are wired together in both directions:
the slot setter publishes which slot is loading, and this predicate consults it.

The function returns true *except* in two hard-coded situations: field variable `0x19`, or field
variable `0x10C7` while the loading slot's flag is exactly `5`. **Two specific places in the game are
carved out by id.** What those ids name is not established here. *(2026-09-25, UQ-337: `FieldData_GetVariable0`
is the story-progress variable, so these are progress values 25 and 4295, not places.)*

### `001ED180` — three clear predicates and a three-id allowlist

```c
id = WorldTransition_GetTransitionFieldId();
return (FUN_001ec560() == 0 && FUN_00265760() == 0 && FUN_002e0540() == 0)
    && (id == 0x2F4 || id == 0x2E9 || id == 0x27B);
```

Another hard-coded id list — three transition field ids, and every one of three unrelated predicates
must be clear. This is the term that makes the state-1/2 arm fire at all, so **that arm is inactive
except during three specific world transitions.**

### `001EDDA0` and `001EDE80` — a two-global runtime mode, and its inverse

```c
001EDDA0:  return !(DAT_01DFE0C0 == 0 && DAT_01F82E38 != 0);
001EDE80:  if (DAT_01F82E38 != 0 && DAT_01DFE0C0 == 0)
                   return FUN_0022A080() + FUN_0022A030();
           return 1;
```

They test the **same two globals on opposite polarity**, so they are the two faces of one runtime
mode: `01F82E38` set and `01DFE0C0` clear. `01DFE0C0` has a single writer (`001EDEF0`) and
`01F82E38` is set to 1 by `001EDDC0`. `001EDDA0` has **50 callers** across the image, which makes it
a general engine-mode question rather than anything specific to this gate; `001EDE80` carries a GFZ
*core runtime / scheduling* mechanism note.

In the §10 loop, `001EDDA0` decides whether the stop marker is *consumed* or merely cleared, and
`001EDE80` is one of the two conditions that can break the loop before any of this runs.

### The gate, restated with the terms named

```c
FUN_00357760();                        // clear "command in progress"
result = InterpretBytecode(...);

standDown =
      result != 0                                                  // the VM itself said stop
   || ( inOneOfThreeWorldTransitions()                             // 001ED180
        && worldState is 1 or 2
        && !fieldExceptionApplies()                                // 001ED130
        && flagB == 0 )                                            // NOT a spc_ scene
   || ( worldState == 3 && flagA != 0 )                            // a sum_...0001 scene
   || scriptedBracketActive();                                     // cmd 1485 on / 1486 off

if (standDown && !commandStillInProgress())                        // 00357770 vetoes everything
        entry[0x16] = 1;
```

**Every term is now either named or a stated unknown**, and the shape is legible: the script VM's own
result, three narrowly-gated situational arms, and a hard veto from any command that says it has not
finished.

### Still not established

- ~~**What field ids `0x19`, `0x10C7`, `0x2F4`, `0x2E9`, `0x27B` name.** They are authored ids; the
  bridge is the same VBF-side data that would name `sum_`/`spc_`. **PROPOSED-repos9e-22.**~~ *Answered
  2026-09-25 (UQ-337): three are maps, and two are story-progress values, not field ids.*
- **What ScriptVM commands 45–48, 641, 1056, 1304, 1305, 1415, 1018–1021, 1485 and 1486 are.** They
  are located in the dispatch table and none of their bodies was read. **PROPOSED-repos9e-23.**
- **What the `01F82E38` / `01DFE0C0` mode is.** 50 callers; not this document's to settle.
- `FUN_001EC560`, `FUN_00265760`, `FUN_002E0540`, `FUN_0022A030`, `FUN_0022A080` remain opaque —
  the second rank of predicates behind the first.

## 12. What the fifteen commands are — `PROPOSED-repos9e-23` answered

§11 located the commands that raise the veto but read none of them. All twenty-three handler bodies
behind the fifteen command ids are read here — 1,184 bytes in total, the largest 147.

**They are the script's *waiting* commands.** `DAT_022C7F88` does not mean "something happened"; it
means **a script command is still waiting**, and the engine must not stand the script down while one
is.

### The player-facing version

**"Press X to continue."** A cutscene script that pauses for a button, for a condition, or for a
count of frames raises this flag every frame it is still waiting. The gate in §10 then refuses to
stand the script down, so the wait is re-polled on the very next frame instead of once per
stand-down cycle. **That is why a prompt in a cutscene responds the instant you press it.**

### Family A — wait for a button (eight commands)

Eight of the fifteen are the same routine against eight different input accessors:

```c
bool poll(ctx, actor, uint *mask) {
    uint held = InputGameplay_Get<Variant>();
    if ((held & *mask) == 0) {
        DAT_022C7F88 = 1;        // still waiting
        return true;             // keep this command active
    }
    return false;                // pressed - the command completes
}
```

| cmd | poll handler | input accessor |
|---:|---|---|
| 45 | `00356C40` | `InputGameplay_GetRemappedHistoryMask04` |
| 46 | `00357530` | `InputGameplay_GetRemappedHistoryMask08` |
| 47 | `0033F8E0` | `InputGameplay_GetRemappedHistoryMask0C` |
| 48 | `003401F0` | `InputGameplay_GetRemappedHistoryMask10` |
| 1018 | `00340C70` | `InputGameplay_GetActorStateAwareRemappedMask04` |
| 1019 | `003414E0` | `InputGameplay_GetActorStateAwareRemappedMask08` |
| 1020 | `00341D70` | `InputGameplay_GetActorStateAwareRemappedMask0C` |
| 1021 | `00342450` | `InputGameplay_GetActorStateAwareRemappedMask10` |

Two banks of four: a **history** bank and an **actor-state-aware** bank, at the same four offsets.
The button mask is the command's argument, popped from the VM value stack by the shared secondary
handler `003567F0` (25 B), which nine of the fifteen commands share:

```c
void secondary(ctx, actor, int *arg0, VMValueStack *stack) {
    *arg0 = VMValueStack_PopInt32CoerceFloat32(stack);
}
```

So an authored `wait-for-button` is one command id plus one integer mask on the stack.

> **This closes a loop opened at the start of this session.** The four
> `InputGameplay_GetActorStateAwareRemappedMask04/08/0C/10` functions are exactly the four that
> [the-unresolved-158 §11](../the-unresolved-158.md) identified as the readers of the eight-slot
> actor registry at `0209C4D0`. The cutscene stand-down gate, the ScriptVM wait commands and that
> registry are one connected mechanism, arrived at from three unrelated directions.

### Family B — wait for a condition (two commands)

```c
// cmd 641, poll handler 0034BBD0
uint state = FUN_002673D0(actor);
if (arg0 != 0) state |= FUN_002E7330(actor);       // a second source, opt-in by argument
if (state == 0 && FUN_00267310(actor[0x15]) == 0) {
        DAT_022C7F88 = 1;
        return 1;                                   // keep waiting
}
return 0;
```

Command 1056 (`0034A1D0`) is the same shape through `FUN_003EB720` / `FUN_002E4CE0` / `FUN_002E7380`,
resolving its subject from `arg1` rather than the calling actor. Its secondary handler `00349CB0`
pops **two** stack values into `arg0` and `arg1`; command 641's (`0034B860`) pops one.

`FUN_00267310(actor + 0x15)` appears in **both**, and again in family C — a shared escape that ends
the wait regardless of the condition.

### Family C — wait a number of frames (one command)

```c
// cmd 1415, poll handler 0034E630
*counter = *counter - 1;
if (*counter < 0) return 0;                        // finished
if (FUN_00267310(actor[0x15]) != 0) *counter = 0;  // the escape
DAT_022C7F88 = 1;                                  // still waiting

if (FUN_001ED180() != 0) {                         // <- the three-transition predicate from S11
        *counter = *counter - 1;                   // decrement a SECOND time
        if (*counter < 0) return 0;
        if (FUN_00267310(actor[0x15]) != 0) *counter = 0;
        return 1;
}
return 1;
```

**A frame countdown that runs at double rate during exactly the three world transitions `001ED180`
identifies** (§11). The same predicate that decides whether the state-1/2 arm of the stand-down gate
can fire also halves every scripted wait during those transitions. Scripted timing is not uniform
across the game.

### Family D — produce a value and yield anyway (two commands)

```c
// cmd 1304, 0034AF20        // cmd 1305, 0034B290
value = FUN_002E12B0();      value = FUN_002E1290();
VMResult_WriteInt32(out, value);
DAT_022C7F88 = 1;            // raised UNCONDITIONALLY
```

These write a result and raise the flag with no test at all. Both are begin-only commands. Whatever
they read, the act of reading it costs the script its stand-down for that frame.

### Family E — the authored bracket (two commands)

```c
// cmd 1485, 00341030          // cmd 1486, 003413E0
DAT_022C7F84 = 1;              DAT_022C7F84 = 0;
FUN_00182D10();                FUN_00182DA0();
FUN_002B5B60();                FUN_002B5C90();
```

Each also calls a matched pair of helpers, so the bracket does more than set a flag — it is a
begin/end on three things at once. What the two helper pairs do was not read.

### The protocol, stated

**Field `+0x10` of a dispatch record is the poll handler**, and eleven of the thirteen veto-raisers
write from it. A command returns *true* from its poll handler to stay active, and raises
`DAT_022C7F88` on the same path. So the flag and the return value carry the same information to two
different consumers: the return value keeps the command alive, and the flag tells the frame loop not
to stand the whole script down.

### Still not known

- **`FUN_00267310`**, the shared escape used by families B and C, tested against `actor[0x15]`.
  Naming it would say what cancels every scripted wait — likely the highest-value single lookup left
  in this thread. **PROPOSED-repos9e-24.**
- What families B and D actually test and read — `002673D0`, `002E7330`, `002E4CE0`, `002E7380`,
  `003EB720`, `002E12B0`, `002E1290`.
- The two helper pairs in the bracket: `00182D10`/`00182DA0` and `002B5B60`/`002B5C90`.
- Command ids are *located*, not *named* — this section says what each handler does, not what the
  authored mnemonic for it is. That remains authored-data work (`-17`, `-22`).

## 13. The escape on every scripted wait — `PROPOSED-repos9e-24` answered

§12 left one function unnamed: `FUN_00267310`, tested against `actor[0x15]` by every waiting command,
and able to end a wait regardless of the wait's own condition. It is twenty-two bytes.

```asm
00267310  48 63 c1              movsxd rax, ecx
          48 69 c8 88 02 00 00  imul   rcx, rax, 0x288        ; 648-byte records
          48 8d 05 f0 1c e3 01  lea    rax, [rip+0x1E31CF0]   ; -> 02099011
          0f b6 04 01           movzx  eax, byte [rax+rcx]
          c3                    ret
```

**It reads one byte out of a 648-byte record, indexed by the actor's manager id.**

### The table

The base `02099011` is `02098E10 + 0x201`. That the array starts at `02098E10` is not assumed — it
is the lowest base paired with this stride anywhere in `.text`. Sweeping for
`imul r64, r64, 0x288` finds **55 sites in 46 functions** *(control: the instruction form is present
and found — **PASS**)*, and the bases they pair with resolve to a consistent field map:

```
array at 02098E10, stride 0x288 = 648 bytes per record

  +0x000   32 sites      +0x0A8    +0x0E0    +0x108   ActorManager_SetResourceTeardownCallback
  +0x010    3 sites      +0x0B0    +0x0F0
  +0x013                 +0x0D8    +0x0F8    +0x201   <- this byte
  +0x0A0                           +0x100
```

The one named user of the stride, `ActorManager_SetResourceTeardownCallback`, works at `+0x108` of
the same records — **so this is the actor-manager record array**, and `actor[0x15]` is the byte
saying which manager an actor belongs to.

### It is a bitmask, not a boolean

The setter is 53 bytes and sets or clears **one bit at a time**:

```c
void SetManagerFlagBit(int managerIndex, int on, uint bit) {
    byte *f = &table[managerIndex * 0x288 + 0x201];
    if (on) *f |=  (byte)(1 << (bit & 0x1F));
    else    *f &= ~(byte)(1 << (bit & 0x1F));
}
```

A second reader, `00267300` (8 bytes), returns the same byte from a record *pointer* rather than an
index — the same field reached two ways.

### Who sets it

| route | path |
|---|---|
| ScriptVM **cmd 1337** (`0034ECF0`, begin handler) | → `00360710` → the bit setter |
| ScriptVM **cmd 1306** (`0034DB30`, poll handler) | → `00360A20` → `00360A50` → the bit setter |
| engine | `00228130` → `00360880` → `00360710` → the setter |
| engine | `002628B0` → `003603F0` → `00360A50` → the setter |
| `ActorManager_BindLoadedDefinitionPayload` | writes the byte directly |

> **A wrong expectation, caught by the control.** I expected the two immediate callers of the setter
> to be dispatch-table entries, as the `022C7F88` writers were. **They are not** — the membership
> test returned 0 of 4, and only one hop further up did two ScriptVM commands appear. Had I asserted
> the shape by analogy instead of testing it, the section would claim script-only control of a byte
> the engine also writes on four other paths.

### Who reads it

**65 functions call `00267310`**, graph and byte-level agreeing exactly. Among them:

- `World_UpdateSimulationTick`
- `Movement_UpdateSteeringTowardTarget`
- roughly fifty ScriptVM command handlers, including every waiting command in §12
- `WorldActorScriptVM_InterpretBytecode` reads the field directly rather than through the accessor

**So this is not a cutscene mechanism.** It is consulted by the simulation tick and by movement
steering as well as by the script VM; the waiting commands are one consumer among many.

### What it does to a wait

Every waiting command in families B and C tests it the same way:

```c
if (FUN_00267310(actor[0x15]) != 0)     // ANY bit set
        -> the wait ends now, whatever its own condition says
```

**The test is against the whole byte, not a specific bit.** So *any* bit set in a manager's flag byte
terminates *every* scripted wait belonging to that manager — a wait cannot opt out, and a bit set for
one purpose ends waits that had nothing to do with it. That is the single most important fact in this
section for anyone modding cutscene flow.

### What the player is looking at

A manager-wide switch that makes scripted waits stop waiting. **Whatever sets a bit, the visible
result is that a scene which was holding for a button or a timer stops holding and runs on.** That is
what skipping or fast-forwarding through scripted content looks like from the outside — but **which
bit means what is not established here**, and naming any bit as "the skip button" would need the
assignments, which live behind the same authored-data boundary as `-17` and `-22`.

### Still not known

- **The bit assignments.** Eight bits, and this pass recovered none of their meanings. The setter
  takes the bit index as a runtime argument, so the constants sit in the callers — `00360710`,
  `00360A50`, `00360880`, `003603F0` — none of which was read. **PROPOSED-repos9e-25.**
- What ScriptVM commands **1306** and **1337** are, beyond reaching the setter.
- The rest of the 648-byte record. Twelve field offsets are located by the stride sweep and none is
  identified.

## 14. Falsification pass 1 — 2026-09-03, by a session with no stake in this document

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`. Body sizes and caller counts
were taken from a call graph regenerated from a fresh import; **tags were not used**, because a stale
dump goes stale about tags and not about addresses or extents.

### Two corrections, and the first is a repeat

**1. Route 4 tests the VA encoding, not "the address".** §8's escape-route table reads
*"8-byte / 4-byte encoding in the file : 0 / 0"*. Searching the **RVA** form (`VA − 0x120000`)
finds `0EAC30` **twice**:

| where | what |
|---|---|
| `.pdata` | `RUNTIME_FUNCTION{Begin=0EAC30, End=0EAE6C, Unwind=1C426F0}` |
| `.rdata` at RVA `1C42730` | `0x40` past that record's own unwind info — inside this function's unwind block |

This image has no `.xdata` section, so unwind data lives in `.rdata`. **Both hits are `.pdata` /
unwind — inadmissible by this project's evidence rules, not absent.** The conclusion is untouched and
the wording is wrong: the row should read **"no *admissible* RVA entry"**, because the next reader who
repeats the search will find hits, and treating them as reachability is precisely the `.pdata`
contamination that cost this project 182 classifications.

**This is the second document with the identical defect** — the same table shape and the same
VA-only scope appears in
[the dead nine-patch renderer](../Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md),
corrected the same day. **Two instances is a habit, not a slip:** the escape-route table is a good
instrument whose route 4 has been written as a stronger claim than it measures, twice.

**2. The `01DFE40C` census counts 23 functions, not 24 — and seven of them write it.**

```
distinct functions referencing 01DFE40C : 23      (document said 24 readers)
   read only  : 16
   write      : 7
   both       : 2
```

The count is a tier-11 corroborating figure and a difference of one is not worth much on its own.
**The reader/writer split is.** A marker described as having "24 readers" reads as a flag that
something else sets; a marker with **seven writers across the image** is a different object, and §7's
open question about what the marker *is* should be read with that in mind.

### Attacked and confirmed

| claim | result |
|---|---|
| every body size in the document's tables | **14 of 14 exact** |
| `001EDDA0` has 50 callers | **50** — exact |
| the thunk route: `0020AC30` reached from `001EC660`, graph edges 0 | reproduced |
| **the 158-function population claim** | **reproduced exactly: 143 both · 0 graph-only · 1 bytes-only (`0020AC30`) · 14 neither** |

That population claim is the one I most expected to break — it is the shape that failed in three
documents this session — and it came back whole, by an independent byte-decode over all 38,161
bodies rather than by re-reading the figure.

### What I tried that failed to break it

- Re-derived the residual partition from scratch instead of checking the arithmetic. Same four
  numbers.
- Attacked the body-size table because I had **fabricated seven body sizes myself earlier the same
  day** and wanted to know whether this author had done the same. They had not: 14 of 14.
- Attacked the caller counts and produced a false mismatch of my own — my pattern attributed
  "50 callers" to `01F82E38`, a data global, when the sentence attributes it to `001EDDA0`. **My
  instrument, not their claim**, and it is recorded here because a phantom mismatch reported as a
  finding costs the next reader a re-derivation.
- Ran the neighbour check first: 88 cited addresses, four shared with `the-unresolved-158.md` and two
  with the dead-renderer document — which is how the repeated route-4 defect surfaced.


## `00392A10` opened — a sliced box emitter with per-region colour

The last entry on the *leaned on and never opened* cut. **Extent checked**: 205 instructions, ends
`ret` at `00392CD2`, no `jmp` leaves the extent.

### It reads a rect with four insets and computes two centre spans

```asm
00392A47  movsx ecx,  word ptr [rdx + 8]     ; inset A
00392A4B  movsx edx,  word ptr [rdx + 0xa]   ; inset B
00392A5B  movsx eax,  word ptr [rdi + 4]     ; total width
00392A64  sub   eax, edx
00392A6B  sub   eax, ecx                     ; centre span = total - A - B
00392A4F  movsx r13d, word ptr [rdi + 0xe]   ; inset C
00392A57  movsx ebx,  word ptr [rdi + 0xc]   ; inset D
00392A5F  movsx r14d, word ptr [rdi + 6]     ; total height
00392A70  sub   r14d, r13d
00392A76  sub   r14d, ebx                    ; centre span = total - C - D
```

**Seven `word` fields from argument 2** — a position pair, a size pair, and **four insets, two per
axis** — and both centre spans are `total − inset − inset`. **That is the arithmetic of a nine-piece
sliced box**: fixed corners, stretched edges, a stretched centre.

The emit loop indexes three ways on each axis (`cmp esi, 1`, `cmp esi, 2`), accumulating positions with
`add r14d, edi` and `add r15d, r13d`.

### Four colours, masked to 24 bits, distributed across the regions

```asm
00392A84  and   ecx, 0xffffff
00392A93  and   r9d, 0xffffff
00392AA0  and   edx, 0xffffff
00392AA9  and   eax, 0xffffff
```

**Four dwords are read from argument 3 and each is masked to `0xFFFFFF`** — the top byte is discarded —
then written into eighteen distinct frame slots. **Four source colours fanned out across the box's
regions**, so corners and edges can differ while sharing sources.

> **The mask is the finding.** Whatever the top byte of those dwords is, **this function does not pass
> it on** — so anything encoded there (an alpha, a flag) is dropped before the box is built.

### A capability check selects a simpler path

```asm
00392AE4  call 0x2dd4b0
00392AE9  test eax, eax
00392AEB  jne  sliced_path
00392AF6  call 0x392ce0        ; the simple path, same three arguments
00392AFB  jmp  exit
```

**When `002DD4B0` returns zero the whole sliced construction is skipped** and a different function is
called with the same arguments. **Two renderers behind one entry point**, chosen at run time — the same
shape as the sound family's four policies and the rebinding function's two, **a third subsystem where
the policy is the call, not the data.**

### What is not established

- [x] ~~**UQ-342.** What `002DD4B0` tests. It decides which of two renderers runs and is unread.~~ **Answered 2026-09-14 (FABLE):** `002DD4B0` is a 7-byte getter, `mov eax, [0215E6D0]` / `ret`, and `0215E6D0` is **the draw-bracket-open flag** answered under UQ-348: set to 1 only when the bracket-open command `0x10000000` has been submitted, and cleared by the close `0x11000000` (UQ-348 below). So `00392A10` runs the sliced construction only while a draw bracket is open, and otherwise hands the same arguments to `00392CE0` (`00392AE4`–`00392AF6`). That branch's one emitter, `002DC290`, tests the same flag and emits nothing while the bracket is closed.
- [x] **UQ-343.** What the discarded top byte of each colour dword holds. **ANSWERED 2026-09-18 (FABLE) as to what the byte is: the vertex alpha (UQ-349).** OPUS's narrowing stands for its *contents* - the array is argument 3 of a function nothing calls, so no value exists in the image to read.
      *Narrowed 2026-09-15 (OPUS): **not answerable from the image**, and the reason is structural
      rather than a gap in effort — the colour array is **argument 3 of a function nothing
      calls**.*
      - **The four colours are the caller's array.** `00392A41 mov rsi, r8` makes `rsi` the third
        argument, and the dwords are read straight out of it: `[r8+0x00]` (`00392A54`), then
        `[rsi+0x04]`, `[rsi+0x08]`, `[rsi+0x0C]` (`00392A73`, `00392A81`, `00392A90`).
      - **The top byte is not discarded inside the function — only excluded from the command.**
        Each dword is stored to a frame local **before** it is masked: `00392A79` saves the full
        value to `[rbp-0x11]` and `00392A8D` to `[rbp-0x05]`, and only then do `00392A84`,
        `00392A93`, `00392AA0` and `00392AA9` apply `and reg, 0x00FFFFFF`. So the function keeps the
        byte and chooses not to emit it.
      - **And no caller exists to supply a value.** A whole-image census of `00392A10` (positive
        control `022D8EB4`, 26 references, so absence is meaningful) returns **zero references** —
        no call, no stored pointer, no table entry. That is the finding
        [the box renderer that is never called](../Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md)
        is about: *“complete, coherent, and dead”*, with four more functions reachable only
        through it. **This row had not been connected to it.**
      - **So the byte's CONTENTS are not in the executable at all.** They would have come from a
        caller, and there is none. Closing this needs the authored data a caller would have passed,
        or a live read of a path that never runs — which is to say it is not closable offline.
        **`NO ADMISSIBLE SOURCE` is deliberately NOT assigned:** that disposition needs a reviewer
        who is not the author (`EVIDENCE-STANDARD` 15bk requirement 4), and the author here is
        OPUS.
- [x] **UQ-344.** Whether the nine regions are drawn from one texture; **no texture handle is read in this
      function.**
      **ANSWERED 2026-09-18 (FABLE): from no texture at all - on either back-end the nine regions are plain alpha-blended quads.** The sliced path is `002DD1E0` (open), `002DC7F0` three times and `002DD090` (close). *PS2 side:* the opener's GIF tag is `0x8026400000000001` with the register list `0x41414141` (`002DD294`, `002DD2B2`): eight registers, RGBAQ and XYZF2 four times, PRIM = triangle strip, Gouraud, blending on, **texturing off** - no ST or UV register anywhere in it. *PC side:* the batcher takes its texture as a **name string** - the third argument of `00181930`, copied into the singleton at `+0x3938` by `001B2410`, or an empty string when the pointer is null (`001B2426`..`001B2432`) - and the close passes `(1, 1, null, 0)` (`002DD1A6`..`002DD1B3`), as the rectangle does. The opener sets the colour from the draw context as `(w5A, w5A, w5A, w58)` through `001816F0` (`002DD2C4`..`002DD2D2`) - a brightness repeated three times and an alpha, the same four values the quad emitter puts in its thirteenth vector - and the two state handles go to the blend and alpha-test setters (`+0x3A68`, `+0x3A70`). So a window frame drawn this way would be nine flat-tinted, vertex-coloured rectangles; a textured frame is some other renderer's work. Static; and the renderer itself still has no caller.
      *Bearing, 2026-09-18 (FABLE), not an answer:* every quad that reaches the shared emitter is **untextured** - its GIF tag's PRIM has texturing off and its vertices carry no ST / UV register (UQ-347). Whether the sliced renderer's other two callees bind a texture was not read.
- [x] ~~**UQ-345.** What `00392CE0`, the simple path, does differently.~~ **ANSWERED 2026-09-14 (FABLE), by the
      section below plus when it runs.**
      - **What differs** (below, re-verified):
        - it reads the same rectangle fields;
        - it keeps each colour dword's top byte, with no `and …, 0xFFFFFF` in the body, where `00392A10` has four;
        - it emits through one callee, `002DC290`. The sliced path uses `002DD1E0`, `002DC7F0` (×3) and `002DD090`.
      - **When it runs.** Its only caller is `00392A10`, which calls the getter `002DD4B0` (the draw-bracket flag
        `0215E6D0`, UQ-348). It takes the simple path **only when the flag is 0** (`00392AE4`–`00392AF6`) and the
        sliced path otherwise.
      - **What that implies.** The simple path's one emitter, `002DC290`, tests the same flag first and returns
        without emitting when it is 0 (`002DC2AF`–`002DC2BC` → `002DC7CC`). On this route the simple path's quads
        are therefore dropped, unless something sets the flag between the test at `00392AE4` and the one at
        `002DC2AF`. UQ-348's census found the bracket open `002DD4C0` as its only RIP-relative writer of 1, and
        pointer writes were not excluded.

      So the top byte the simple path keeps (UQ-346, UQ-349) is kept on a route that, as read, emits nothing.

### `00392CE0` — the simple path, and what the mask was hiding

Opening `00392A10` put its sibling on the cut, since that section cited it at its entry. It is read
here, and it settles a question the first read could only pose.

**Extent**: 161 instructions, ends `jmp 0x392e70` — **inside its own body**, a loop back edge, not a
tail call. **The check is the target, not the mnemonic.**

It reads **the same geometry fields** — `[rect+4]`, `[rect+6]`, `[rect+0xC]`, `[rect+0xE]`, `[+8]`,
`[+0xA]` — so both renderers consume one layout format. **What differs is the colour handling:**

```asm
00392D0A  movzx eax, byte ptr [r8 + 3]      ; the TOP byte of colour 0
00392D12  mov   byte ptr [rbp + 0x19], al   ; kept, on its own
00392D18  movzx eax, byte ptr [r8 + 0xb]    ; the top byte of colour 2
...
00392D20  mov   ecx, dword ptr [r8]         ; and the dwords, unmasked
```

**`00392A10` contains four `and …, 0xFFFFFF`; this function contains none**, and instead reads the top
bytes **explicitly, as separate fields.**

> **The fourth byte of each colour dword is a real field, not padding.** The simple renderer extracts
> it and keeps it apart from the colour; **the sliced renderer masks it away and never passes it on.**
> Neither function alone shows this — **the first could only say a byte was discarded, and the second
> is what shows it was worth keeping.**

**One callee** (`002DC290`) against the sliced path's three, and the same three-way index (`cmp rsi, 2`),
so the simpler path is simpler in emission rather than in geometry.

- [x] **UQ-346.** What the top byte means. **Both halves of the evidence are now in hand — one function preserves
      it and one discards it — and neither says what it is.**
      **ANSWERED 2026-09-18 (FABLE): vertex alpha.** See UQ-349 below for the packet that says so; the byte one renderer keeps and the other masks is the A of RGBAQ.

### `002DC290` — the shared emitter, and where that fourth byte goes

The bottom of the family: **eleven callers across seven address neighbourhoods**, including both
renderers above. **Extent**: 256 instructions, ends `ret` at `002DC7E2`, no `jmp` leaves the extent.

**It emits one four-vertex quad into a ring of command buffers.**

```asm
002DC2AF  cmp   dword ptr [0215E6D0], 0     ; a global enable — zero and nothing is emitted
002DC2C2  mov   eax, dword ptr [02EBEFF0]   ; the current buffer index
002DC2DB  lea   rdi, [rax + rax*2]
002DC2EE  mov   rbx, qword ptr [02EBEFC0 + rdi*8 + 8]
002DC2F7  mov   dword ptr [rbx + 0x18], 0x10000000
002DC2FE  mov   dword ptr [rbx + 0x1c], 0x6c0d8000    ; two command words
```

Then **four vertices**, each built the same way:

| vertex | colour dwords | position dwords |
|---:|---|---|
| 0 | `+0x50 +0x54 +0x58 +0x5C` | `+0x60 +0x64 +0x68` |
| 1 | `+0x70 +0x74 +0x78 +0x7C` | `+0x80 +0x84 +0x88` |
| 2 | `+0x90 +0x94 +0x98 +0x9C` | `+0xA0 +0xA4 +0xA8` |
| 3 | `+0xB0 +0xB4 +0xB8 +0xBC` | `+0xC0 +0xC4 +0xC8` |

**Sixteen bytes are read from the third argument — offsets `0` through `15` — and each is widened to
its own dword.** Four bytes per vertex, four vertices.

> **So the fourth byte of each colour has a destination: `+0x5C`, `+0x7C`, `+0x9C`, `+0xBC` of the
> emitted vertex.** The question the two renderers posed is answered from the bottom — **the slot
> exists in the command either way, and `00392A10` deliberately zeroes it while `00392CE0` fills it.**
> **Masking is a choice about what to send, not a discard of something the format has no room for.**

Submission advances the ring cursor by the bytes written, **16-byte aligned**, then calls
`RenderCommand_SubmitCurrentBufferAndSwap`:

```asm
002DC55B  sub  ecx, ebx
002DC55D  and  rcx, 0xfffffffffffffff0
002DC561  add  qword ptr [02EBEFC0 + rdi*8 + 8], rcx
002DC566  call RenderCommand_SubmitCurrentBufferAndSwap
```

**The buffer descriptor is 24 bytes** (`rax + rax*2` then `*8`), and the cursor lives at `+8` of it.

### What is not established

- [x] **UQ-347.** What the two command words `0x10000000` and `0x6C0D8000` select.
      **ANSWERED 2026-09-18 (FABLE): it is a VIF1 UNPACK header - 'thirteen four-component vectors to VU address 0' - with a padding word in front.** The command the emitter `002DC290` writes is a PS2 VIF1 packet, and it decodes whole with the field layout the image's own VIF1 decoder uses ([the VIF1 / VU1 page](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.1: top byte = command, `0x60`-`0x7F` = UNPACK with NUM in bits 16-23, ADDR in the low ten bits and flags in bits 14 / 15). With `p` = command `+0x10`: `p+0x0C` = `0x6C0D8000` is **UNPACK, format `0x6C` (four 32-bit components), NUM = 13, ADDR = 0, bit 15 set**, and exactly thirteen 16-byte vectors follow at `p+0x10`..`p+0xDF` - the 4x4 transform (four), then colour and position for each of four vertices (eight), then one more from the context's words `+0x58` / `+0x5A` (`002DC468`..`002DC48E`). `p+0xEC` = `0x6C048100` is a second UNPACK of the same format, **NUM = 4, ADDR = 0x100**, and exactly four vectors follow (`p+0xF0`..`p+0x12F`): the qword `0x1000000000000002` with `0x0E` beside it, the context's `+0x80` qword with `0x47`, its `+0x78` qword with `0x42`, and `0x2026400000008004` with `0x41` (`002DC484`..`002DC50D`). Read as GS GIF tags those are: a tag of two address+data writes (NREG 1, register list `E`) setting register `0x47` (TEST_1) and `0x42` (ALPHA_1) from the draw context, then a tag with NLOOP 4, end-of-packet, PRIM present = **triangle strip, Gouraud, alpha blending on, texturing off** (PRIM `0x4C`), NREG 2 with register list `1`, `4` = **RGBAQ, XYZF2** - four vertices of colour plus position, which is what the thirteen vectors carry. The packet closes with a word whose top byte is `0x14` (MSCAL) built at `002DC506`..`002DC52C`. The `0x10000000` in front of each UNPACK is the other half of an 8-aligned pair and its top byte `0x10` is not among the codes the decoder acts on, so it is padding that brings the payload to a 16-byte boundary. Three counts check the reading from inside the packet: NUM 13 = vectors written, NUM 4 = vectors written, NLOOP 4 = vertices. *Not traced here:* the route from the ring at `02EBEFC0` to the decoder; the decode rests on the packet's own internal counts and on the decoder's field layout, not on having watched it consumed. Static. *Traced later the same day, and it is a dead end:* the ring's submit path ends in a register kick that hands the buffer to nothing ([the handshake page](../../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md), UQ-211), and after submitting, this same emitter draws the quad again through the immediate-mode batcher (`002DC5CF`..`002DC7A7`), whose colour setter takes `(r, g, b, a)` and whose begin sets all four to `0x80` - see [the rectangle page](../drawing-one-coloured-rectangle.md) section 4. The packet is a faithful description nobody reads; the alpha reading of the fourth byte holds on both paths.
      *Narrowed 2026-09-15 (OPUS): **they are not two words. They are one 64-bit constant,**
      `0x6C0D800010000000`.*
      - **`0x6C0D8000` occurs exactly FOUR times in `.text`, and every one is a writer.** An
        immediate census over the whole image finds `002717B6`, `002DC2FE`, `003C2F67` and
        `003F2F40` — all `mov dword ptr [reg + disp], 0x6c0d8000`, **no `cmp` anywhere**.
      - **In all four it is the HIGH half of a qword whose low half is `0x10000000`,** written by
        the immediately preceding instruction at the adjacent lower dword:
        `003F2F20` writes `+0x08` then `+0x0C`; `00271760` writes `+0x08` then `+0x0C`; `003C2E60`
        writes `+0x08` then `+0x0C`; and this page's own emitter `002DC290` writes `+0x18` then
        `+0x1C` (`002DC2F7`–`002DC2FE`), sixteen bytes further in because its command carries a
        header. **Every one of those pairs is 8-aligned**, so little-endian they are the single
        qword **`0x6C0D800010000000`**.
      - **So the question's premise does not hold.** `0x10000000` is not a selector at all: it has
        **427 `.text` occurrences**, because it is both the low half of many different 64-bit
        constants and an ordinary bit-28 mask. Only the pair means anything.
      - **Two of the four also write `0x13000000` at `+0xE0`** (`002717BD`, `003F2F47`) — a second
        constant on the same commands, not examined here.
      - **Still open, and it is what the row now asks:** what the 64-bit value selects. **No
        instruction in `.text` compares against it**, so it is consumed downstream — by the driver
        or GPU, or by a test on a masked field rather than the whole word. Neither was read here,
        and the ring's consumer was not found: a census of `02EBEFC0` returns thirty-plus
        functions and every one takes the address to WRITE.
- [x] ~~**UQ-348.** What `0215E6D0` gates — **with it zero this function emits nothing at all**, which makes it a
      global draw kill-switch, but nothing here says who sets it.~~ **Answered 2026-09-14 (FABLE):**
      **`0215E6D0` is not a kill-switch; it records that a draw bracket is open.** RIP census of the dword:
      - **One writer of 1: `002DD4C0`, which opens the bracket.** It writes a command whose dwords `+8` and `+0xC`
        are both `0x10000000`, submits it through `RenderCommand_SubmitCurrentBufferAndSwap`, then calls `002B4710`.
        That function submits again and sets byte `+0x1103` of the object at `[0209CC40]`. The flag is set last
        (`002DD53E`).
      - **Two writers of 0.**
        - `002DD420` closes the bracket. It writes a command with dwords `0x11000000` and 0, submits it, calls
          `002B4700` (which clears byte `+0x1103`) and then clears the flag (`002DD485`).
        - `002DD4A0` clears the flag and tail-jumps to `002B4700` without emitting anything. Its one caller is the
          tail of the save-buffer binder `00253970`, reached from one call site, `0022A415`, in the core runtime start-up.
      - **Who brackets.** The bracket's only two callers, `002450B0` and `00245110`, have the same shape. Each
        stores 0 or 1 in `0208F564`, opens the bracket, runs the widget-tree draw pass `00245E60` on root
        `0208EC90` (with `00245510` conditionally and `00249FD0(0)` in between) and tail-jumps to the close.
        - `002450B0` is reached from `MainLoop_Draw` and from twelve sites in the `002528A0` / `002529F0` /
          `00252A20` / `00252A70` / `00252840` group.
        - `00245110` is reached from `00252990`.
        - `002528A0` and `00252990` are each called from `MainLoop_UpdateAndRenderFrame` and from `0022BC20`.
      - **Readers.** Five inline tests (`002D9C40`, `002DAF30`, `002DB080` (domain-labelled screen capture), this emitter and
        `002DD1E0`), plus the getter `002DD4B0` with ten call sites. `002DB080`
        interior verified 2026-09-17 (SWE2-FRONTIER): `00181560` heads the body at
        [`002DB218`](../../_index/ADDRESS-INDEX.md), then `00202B70` walk pairs
        with `00397910`/`00398C50` reads — the screen-capture label holds.
      **So a primitive this emitter is asked for outside an open bracket is dropped, not queued.** Only
      RIP-relative writes were censused; pointer writes into the dword were not excluded. What the two bracket
      command words mean to the render thread is UQ-347's territory and is not read here.
- [x] **UQ-349.** What the fourth colour byte *means* — **three functions now agree it has a slot, and none of them
      says what fills it with meaning.**
      **ANSWERED 2026-09-18 (FABLE): it is the A of a GS RGBAQ vertex colour - vertex alpha - in a primitive drawn with alpha blending on.** The emitter's packet is decoded whole under UQ-347: its GIF tag declares each vertex as RGBAQ then XYZF2 and its PRIM word turns blending on and texturing off, with the blend equation (ALPHA_1) and the alpha test (TEST_1) taken from the draw context's `+0x78` and `+0x80`. The four bytes the emitter widens per vertex are therefore R, G, B, A in that order, and the fourth decides how much of the quad's colour reaches the frame under that equation. So `00392CE0` sends the caller's alpha and the sliced renderer `00392A10` sends alpha 0 for every vertex. What either draws depends on the ALPHA_1 value in the context, and what numeric alpha counts as opaque is the GS's convention; neither was read here. Static.
- [x] ~~**UQ-350.** What the 64 bytes copied from argument 1 into both a global at `022D8F30` and the command are.~~
      **ANSWERED 2026-09-14 (FABLE): the primitive's 4×4 transform, taken from the widget draw context.**
      - **Argument 1 is the draw context.** Three of the emitter's callers load it as `[widget + 0x38]`: `0029D38A`,
        `002C95E2` and `0056EAAB`. The widget draw pass `00245E60` points `+0x38` at its context (`00245EB0`).
      - **The context's first 64 bytes are a composed matrix.** The draw pass calls `00217150` (through the thunk
        `00202D70`) with `rcx = context`, `rdx = rbp+0xB0` and `r8 = rbp+0xF0` (`00246136`–`00246148`).
        `00217150` is a 4×4 float matrix product: each output element is a sum of three or four row × column
        products of the two inputs, starting `00217165`–`0021720C`. So the context holds the widget's local transform
        times its parent's.
      - **The root parent is the identity.** `00247CD9` stores the identity into `0208ED10` through the 44-byte identity store, whose
        rows are `008C5F80` (1,0,0,0) … `008C5FD0` (0,0,0,1). The draw pass copies that matrix in with the 64-byte
        copy `00202C70` (`00245F24`–`00245F2B`).
      - **Where the copies go.** The emitter writes the matrix into the four 16-byte cells `022D8F30`–`022D8F6F`,
        which are GPR `v0`–`a1` of the PS2-emulation [the register bank](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md). It writes them again into the command at
        `+0x20`–`+0x5F` (`002DC317`–`002DC37A`). The command is what the render thread receives.

      **Not claimed:** why the matrix is mirrored into the emulated register cells (no reader in this function) and
      the row/column convention the render thread applies.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named `002B5C90` only at its entry. The interior addresses below were read in the
shipping image.

| body | interior cite | what is there |
|---|---|---|
| `002B5C90` | `002B5D33` | `mov byte ptr [rip+…], …` — writes `01E0CE28` mid-body, between `movdqa` constant loads and the `002878B0`/`001E0BD0` call pair |

*(Pass 22 adjacency, 2026-09-14: `002628B0` calls **party** `00358B40`/`00359200` (2 edges) —
cutscene slot code reads party state, the direction is slot-out.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**StoryEvent — SERVICE.** `0020AC30` on this page calls `FUN_0020a800`, owned by that layer. What it reaches is a 554-byte routine in a `0x100`-byte frame that opens by calling an import through `008C2448`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT (SWE2-EC7-164, 504 edges).** The sidecar's subjects are
consulted across the Presentation layer — `0017FC50` is called by `002528A0`,
`00180120` calls `001EC560`, and `00181330` is called by `00274CB0`/
`002AFDC0` there (+500 more of the same shape) — and `00248F40`, the scorer this page's
`00367ED0` accumulator runs, is itself shared with that layer. The slot
machinery feeds presentation; no shared ownership.

**UI — CLIENT (SWE2-EC7-164, 48 edges).** `00181330`/`00181560`/`001816B0`/
`00181870` are all called by `002A0440` on the UI layer (+44 more) — the slot
records are read by the widget side. Consultation, not shared ownership.

**ActorEntity — CLIENT and SERVICE (SWE2-EC7-168, 31 edges).** `00202C70` — the string copy
this page names — is called by `003F1E90`, and `0025DF00` reaches `00359B80`/`003DB2A0`/
`003DB550` on the actor layer (+27 more). The sidecar's shared helpers touch the actor
layer; no actor ownership here. Edge list from `edges.tsv`.

## The `00392A10` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`00392A10` (707 B) is the sliced box emitter this page opened: it checks the
draw-bracket flag via `002DD4B0` (`0215E6D0`) and either runs its own
per-region construction or hands the same arguments to `00392CE0`
(`00392AE4`–`00392AF6`, per UQ-342). The exclusive members complete the
pipeline.

| member | role | interior |
| --- | --- | --- |
| `002DC7F0` (2,194 B) | the slice-geometry builder — initialises the quad struct (`0`/`1.0f` diagonal, `002DC837`–`002DC8B0`), and per flag bit (`test r13b, 4` at `002DC8B8`) builds each region's rect: `w = x2 − x1`, `h` likewise, `00202B70` basis construction, `divss` normalised UVs (`002DC8FF`–`002DC94F`) — the 2 KB engine behind the sliced construction | [`002DC8B8`](../../_index/ADDRESS-INDEX.md) |
| `002DD090` (332 B) | the packet submitter — counts `(end − begin − 0x20) >> 4` packets, writes the `0x10000000` bracket-open command and the `0x6C008000 \| (count << 16)` header (`002DD0BF`–`002DD0CC`), and when count == 5 flushes the chain via `0016D6A0` + `003A1DB0`; otherwise marks `[rax−0x64] \|= 1` and emits the `{0x1000000000000002}` qword, `0x6C038100`, the `0xE`/`0x47`/`0x42` A+D register writes taking `[rdx+0x80]`/`[+0x78]`, then `002DD350` and the `00181930`/`00181910`/`001816B0`/`00181330` submit sequence | [`002DD13A`](../../_index/ADDRESS-INDEX.md) |
| `002DD1E0` (268 B) | the bracketed quad submitter — gated on the same `0215E6D0` flag (`002DD1E6`), snapshots `rdx`'s 0x40-byte quad header into `022D8F30`–`022D8F60` *and* the ring slot's `[+0x10]` buffer, emits `[rbx+0x58]`/`[+0x5A]` as a 0x10 record under tag `0x8026400000000001` with the `0x41414141` filler, then `00181560`, `001816F0`, tail `00181870(3)` | [`002DD221`](../../_index/ADDRESS-INDEX.md) |
| `00392CE0` (589 B) | the non-bracket emitter — copies the four corner colours whole (top byte kept, per UQ-342's comparison), derives nine region widths from the `[r13+4..0xE]` word deltas (`00392D4A`–`00392D85`), iterates the nine slices and calls the shared emitter `002DC290` per slice (`00392E73`) | [`00392D4A`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `002DD4B0` (the flag getter),
`002DC290` (the per-slice emitter), `00202B70`, `002DD350`, `0016D6A0`,
`003A1DB0`, `00181330`/`00181560`/`001816B0`/`001816F0`/`00181870`/`00181910`/
`00181930`, `00808C40`.


### Interior citation — frontier hub `00181930` (2026-09-18, SWE2-EC7)

`00181930` — 98 B, 13 callers: the submit-sequence step `002DD090` runs. It
resolves a context through `001B1C00()`, then forwards a five-argument call to
`001B2410` ([`00181978`](../../_index/ADDRESS-INDEX.md)) — `(rcx=ctx, edx=arg0,
r8=arg1, r9=arg2, stack5=ebx)` — with the other stack slots zeroed. A shaped
adapter between the packet submitter and the lower emit.

### Interior citation — frontier hub `002DD350` (2026-09-18, SWE2-EC7)

`002DD350` — 109 B, 9 callers: the packet-finalise the submit sequence runs
after `002DD090`. Writes `{0, 0x10000000, edx | 0x14000000}` into the
`[rcx+0x10]` cursor record and advances it 0x10; recomputes the packet count
`(cursor - [+8] - 0x10) >> 4`; calls `0016D6A0` (the ret-0 guard) then
`003A1DB0` — `RenderCommand_SubmitCurrentBufferAndSwap` — at
[`002DD3B2`](../../_index/ADDRESS-INDEX.md). The emit tail shared with the
`002B4730` family.
## SWE2-EC7-18 update (2026-05-15) — `001EC5C0` flag-B zero-extend tail

`001EC5C0` (17 B) is the flag-B helper the slot table row names ("zero-extends flag B for its 4 consumers"): a `0x28` frame around `0020AA30` whose `al` result is `movzx`-extended into `eax` before return (`001EC5C4`..`001EC5D0`) — a byte-result shim over the shared flag reader, which is why the row shows no standalone body beyond the call.
## SWE2-EC7-31 update (2026-09-18) — `002529F0` draw bracket + `002450B0` bracket body

`002529F0` (40 B) is one of the twelve sites the bracket census
names: `001FBD80(1)` opens the draw state, `002450B0` runs the
bracket on the `0208EA48` object, `00252500()` follows, and a
tail `jmp 001FBE50` closes — the full draw-bracket sequence on
one root. Interior anchor `00252A0F` (the `jmp 001FBE50` tail).

`002450B0` (91 B) is the bracket itself: `0208F564` resets to 0,
`002DD4C0()` runs, `00245E60(obj, 0208EC90)` walks the object's
list against the `0208EC90` table; only when `byte[0208ED58] & 1`,
`dword[0208F568] == 0` and `dword[obj+0xC0] == 1` does
`00245510(obj)` run — then `00249FD0(0)` and a tail `jmp 002DD420`
close the pair. Interior anchor `002450F5` (the gated `call
00245510`).
## SWE2-EC7-32 update (2026-09-18) — `001ED180` triple-veto kind test + `001ED130` field-id exception, verified

`001ED180` (83 B) is the transition test the cutscene veto
paragraph describes: `ebx = 00314910()` is the current kind, then
three vetoes — `001EC560()`, `00265760()`, `002E0540()` — any
non-zero returning 0; only `ebx` in `{0x2F4, 0x2E9, 0x27B}`
returns 1. Interior anchor `001ED1A8` (the `cmp ebx, 0x2F4`
first kind test).

`001ED130` (73 B) is the two-case field-id exception the section
names: `edx = movsx(00265270())` is the field id, `ecx` the
`01F832B0` table value at `dword[01DFE40C]` (0 when the index
passes 4); the function returns 0 for field `0x19`, and 0 for
field `0x10C7` exactly when the table value is 5 — every other
combination returns 1. Interior anchor `001ED156` (the `cmp edx,
0x19` test).

## SWE2-EC7-41 update (2026-09-19) - `002D9C40`

`002D9C40` (354 B) is a cutscene-slot body - `0215E6D0`/`022D8F30`..`022D8F60`/`02EBEFC0`/`02EBEFF0`, `00181560`/`001816F0` pair. Interior anchor `002D9D75` (an `00181560` call).

## SWE2-EC7-43 update (2026-09-19) - `002B5B60`

`002B5B60` (292 B) is a cutscene-slot body - `"#210"` literal, `01E0CE30`/`01E0CE3A`/`00916720`-`009167B0`/`01F44830`, `0017E210`/`001E0B90`/`001E0BD0`/`001E0DA0`/`001E0DC0`/`00808C40`. Interior anchor `002B5B89` (an `0017E210` call).

## SWE2-EC7-45 update (2026-09-19) - `002528A0`

`002528A0` (240 B) is a body - `0017FC50`/`001FBD80`/`00229EA0`/`002450B0`/`0024A710`/`00252500`/`00365990`. Interior anchor `002528A9` (an `0017FC50` call).

## SWE2-EC7-49 update (2026-09-19) - `001C34D0`

`001C34D0` (186 B) is a call-free needle scan - `byte[r8]` searched in `[rcx,r10)`, then a byte-compare from `rdi`; `r8+1 == r9` and `rcx == rdx` short-circuits. Interior anchor `001C3500` (the scan loop head).

## SWE2-EC7-52 update (2026-09-19) - `0024A710`

~~`0024A710` (711 B) is a cutscene-slot body - `003A1F20`/`003A1FE0`/`0024AF50` plus `0208F5B8`/`02EBEFC0`/`02EBEFF0`.~~ **Corrected 2026-09-30 (SWE2-EC7, SWE2-CONTRACT's DD batch 6):** `0024A710` (711 B) is not cutscene code. It is the UI atlas registry's texture-memory layout pass: from `0208F5B8` (slot 0 `+0x38`) it steps `0x48` per slot, takes the slots whose flags hold bits 5, 6, 7 and the caller's bit `k` (`mov ebx, 0xe0; bts ebx, ecx`), queues their transfers through `0024AF50` from a base of `0x3520`, and stores each slot's packed texture descriptor at `+0x30`, which the sprite emitter reads (SWE2-CONTRACT's B1-B6/E1-E3, [a typed list measured once](../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md) section 5d; control [roles2_control.py](../../_index/candidates/ec7-role-corrections-2-0930/roles2_control.py) T1-T5). It was filed on this page by the 2026-09-19 batch and stays here as history. Interior anchor `0024A745` (a `003A1F20` call).

## SWE2-EC7-53 update (2026-09-19) - `0024AF50`

`0024AF50` (368 B) is a cutscene-slot body - `0024B150`/`003A2090`/`003A21A0`. Interior anchor `0024AF9D` (a `003A2090` call).

## SWE2-EC7-55 update (2026-09-19) - `00252500`

`00252500` (271 B) is a `0208EA48` bracket body - `00248E10`/`00248EB0` plus `022D8EAC`/`022D8EB4`. Interior anchor `00252509` (a `00248EB0` call).



## SWE2-EC7-66 update (2026-09-19) - `003603F0`

`003603F0` (130 B) is the cutscene engine loop - `002260E0`/`002EFA70`/`003600D0`/`003601C0`/`00360A50` (walks k = 0..7). Interior anchor `00360414` (a `00360A50` call).


## SWE2-EC7-87 update (2026-09-20) - `003DE210` one-shot object promote measured

`003DE210` (40 B) is the promote-once step the cutscene-slot
callers run: when `[02B58C48]` is live the object's `dword[+4]`
is copied to `dword[+0]`, `dword[+0x28]` is set to 1, the global
slot is cleared, and the body tails `0024EB20` either way.
Interior anchor `003DE233` (the `0024EB20` tail).

## SWE2-EC7-99 update (2026-09-20) - `002CCBC0` measured

`002CCBC0` (105 B) is the tagged flag write `00228130` and
`00229590` call: the same `0209AC30` `+0x290` table
supplies the object, a null object or `byte[+0x7C]` bit 5
set returns quietly, `edx <= 0` skips the write entirely,
`edx >= 0x1000` clears bit 11 of `+0x7C` and sets
`0x10000` in `+0x40`, and `edx < 0x1000` folds `dx << 22`
into `+0x7C` (mask `0x3FF7FF`, bit 11 set) - then the
second `0209AC30`-indexed pointer tails `00244F00` - the
encode-and-notify the slot arms run.
Interior anchor `002CCC02` (the `dx << 22` fold arm).

## SWE2-EC7-110 update (2026-09-20) - `001B38B0` measured

`001B38B0` (131 B) is the
EASTL string constructor
`001B31E0`, `001C3390` and
`001C3420` run: the three-pointer
head at `rcx`/`+8`/`+0x10`
zeros, `001EDF00(rcx + 0x18,
r9)` binds the allocator, then
capacity `r8 + 1` decides -
`> 1` calls `vtable[+0x18][+0x10]
(0, capacity)` and points all
three head words at the block
with `end = start + capacity`;
`<= 1` binds the `02EBA2E0` /
`02EBA2E1` empty-string
sentinel pair instead. The
first byte always latches 0.
Interior anchor `001B38DF`
(the `cmp ebx, 1` capacity
test).

`00245510` (142 B) is the conditional middle `002450B0`/`00245110` run inside their bracket: `00368300(rcx)` gates the whole body; when nonzero it `002D8C00`s a stack record, triple-stores `[rbx+0x98]` at `+0x60`/`+0x68`/`+0x70`, writes the `[rbx+0xA0]` byte as a word at `+0x78`, dispatches `00202D70(&rec, 0208EC10, 0208EC90)` — the same descriptor pair the bracket uses — then `00367940`s the record. A silent no-op whenever the gate returns 0.

Interior anchor `00245541` (function `00245510`).

`00367940` (346 B) is the slot state `00245510` calls: `word[022CBE30]` zero short-circuits; `022CBE32` bit `0x800` is masked off (`&= 0xF7FF`) when set; `022CBE90`/`022CBE98` both non-null then calls `00367AA0` on the record - the sidecar's gated hand-off.

Interior anchor `0036799B` (function `00367940`).

`00367ED0` (193 B) is the parameter accumulator `00367940`/`00367200` call: `00367FA0` must return nonzero, then `byte[022CBE32] & 0x10` arms the whole write. `byte[022CBE3D]` selects the arm - `2` runs `00248F40(word[022CBE3E], byte[022CBE41])` and keeps `cvttss2si(xmm0 * [01CEBC70])` directly, `3` runs the same call on `byte[022CBE42]` and keeps `4 - eax` instead; `word[022CBE36] == 2` negates the result, and `byte[022CBE3C]` picks `word[rbx]` (mode 0) or `word[rbx + 2]` (mode 1) as the accumulate target - the sidecar's signed field tick.

Interior anchor `00367ED9` (function `00367ED0`).

`003676D0` (324 B) is the `022CBExx` sidecar accumulator `00367200` calls: gated on `word[022CBE30]==2` + `byte[022CBE32]&4`; `00248F40(word[022CBE5C], sword[022CBE60], sword[022CBE5E])` scores the pair, then a second `word[022CBE30]==2` arm adds `word[022CBE58]`/`word[022CBE5A]` into the `022CBE48`-`022CBE4E` quad (else the quad reads unmodified), and `(r8w - ax) * xmm0` comes out through cvtdq2ps/mulss - the sidecar's scaled-delta write `00367940`/`00367ED0` sit beside.

Interior anchor `00367705` (function `003676D0`).

`00368940` (148 B) is the `022CBExx` sidecar writer `0027CD00`/`003676D0`/`00367820` call: `rcx` nonnull copies `word[rcx]`/`word[rcx+2]` into `022CBE38`/`022CBE3A` and replicates the pair across `022CBE48`/`022CBE4A`/`022CBE4C`/`022CBE4E`; `rcx` null installs the signed defaults (`022CBE38`/`022CBE4C`/`022CBE50` = `0x80008000`, `022CBE76`/`022CBE7A`/`022CBE7E`/`022CBE82` = `0xFFFF8000`) and clears `byte[022CBE70]`; `word[022CBE3E]` resets either way - the block's parameter publish/reset the accumulators sit beside (call-free).

Interior anchor `0036897D` (function `00368940`).

## UQ-337 answered — three maps and two story-progress values (FABLE, Claude Opus 5.5, 2026-09-25)

*Static, from the shipping bytes.*

**The two values in `001ED130` are story progress, not places.**
- `001ED130` compares `FieldData_GetVariable0` (`00265270`, `001ED134`) against `0x19` and `0x10C7`
  (`001ED156`, `001ED15B`).
- `00265270` returns the `u16` at `[02098E58]` when `02098E20` bit 0 is set, else 0. The handbook
  page's gate table already identifies that word as `global_flag[0]`, the story-progress variable
  every story-gated record compares against
  ([`hchk-hctg-hdat-handbook-indexes.md`](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md)).
- **So the predicate is false at story progress 25, and at 4295 while the loading slot's flag is 5.**
  Earlier sections of this page called them field ids, and they are corrected in place.

**The three transition ids name maps.** A field id reaches the map loader unchanged:
1. `WorldTransition_StageFieldTransition` (`003145E0`) takes it in `ecx`. It writes it to the pending
   cell `01EED064` (`0031467F`) and to the save payload's `+0x105C` (`003146D3`), which is what
   `WorldTransition_GetTransitionFieldId` (`00314910`) returns to `001ED180`.
2. `World_UpdateSimulationTick` passes the pending cell to
   `WorldSimulation_ProcessDeferredModeRequest(0, id)` (`003140B2`–`003140BA`). That calls
   `ActorResource_BeginManagerResourceSetLoad(0, id)` (`0032FC7B`).
3. For manager 0 that function takes path kind **5** at index **`id × 3`** (`0032FD1B` → `0032FD3F`–`0032FD44`).
   It loads that entry and the next two, which are the map's `.ebp` script, `.mot` and `.fpk`.

Reading kind 5's array (the `lea` before the store at `002DFC03`, `01EE23A0`) at `3 × id`:

| transition id | map |
|---|---|
| `0x27B` (635) | `plan_map\alc_a\alc_a01\global\alc_a01.ebp` / `.mot` / `.fpk` |
| `0x2E9` (745) | `plan_map\alc_f\alc_f01\global\alc_f01.ebp` / `.mot` / `.fpk` |
| `0x2F4` (756) | `plan_map\alc_c\alc_c01\global\alc_c01.ebp` / `.mot` / `.fpk` |

*Control, from live evidence recorded for another purpose.* The
[`spawn-live-load`](../../_experiments/evidence/spawn-live-load/README.md) run recorded field id
`0x132` (306) while the player stood in **Rabanastre / Southgate**, and kind 5 at `3 × 306` is
**`rbn_a18`**, a Rabanastre map. The same run's title-screen id 12 reads `ttl_a01`. So the index
really is the field id. Index 0 reads `tst_a01`, the test map, consistent with
[the resource path tables](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md).

**So `001ED180`'s allowlist is three `alc` maps, `a01`, `c01` and `f01`.** The state-1/2 arm fires only
when the current transition targets one of them and the three predicates are clear.

**Not established.**
- Which story beats progress values 25 and 4295 mark. That needs the scripts that set the variable
  to those values.
- The in-game place name of the `alc` area. The table gives file names, not display names.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

**Save_Load_Settings — CLIENT.** The UQ-337 section cites
`WorldTransition_StageFieldTransition` `003145E0`, which writes the transition field id into the
save payload at `+0x105C` through `SaveImage_GetPersistentPayloadBase` `002EF2B0`. That stored word
is what `WorldTransition_GetTransitionFieldId` returns to `001ED180`. The page reads one value that
the save payload holds and claims nothing about how the payload is saved or loaded.

**SaveLoad — CLIENT.** The same stager calls `WorldTransition_ShouldAutosave` `0020E500`
(`00314774`) after staging. The UQ-337 answer does not depend on that call and says nothing about
autosaving.

*These two paragraphs cover only the edges the UQ-337 citations add.* The page's earlier edges into
both layers, from `002EFA70`, `00252840`, `00253970` and `002628B0` in other sections, are not
dispositioned here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Audio — MECHANICAL, 11 edges.** `002628B0` calls `00360B50`, `00360DD0`, `003636A0`; `001EDDA0` is called by `003B99D0`; `00202C70` is called by `00362850`; `00229590` calls `002DF370`; `00229EA0` is called by `003638B0`; `002DB080` calls `00182E80`; `0034DB30` calls `003608D0`; `003601C0` is called by `00361460`; `00360710` calls `002DEDD0`.

**CoreRuntimeScheduling — MECHANICAL, 42 edges.** `002529F0` is called by `0022A770`, `MainLoop_UpdateAndRenderFrame` (`0022B8C0`), `0022BC20`; `0018CA40` is called by `0017CCD0`, `001E0590`; `001EC560` is called by `001EC760`, `0022A770`; `001EDDA0` is called by `00265860`, `00265880`; `001EDE80` calls `0022A030`, `0022A080`; `002528A0` is called by `MainLoop_UpdateAndRenderFrame` (`0022B8C0`), `0022BC20`; `00252990` is called by `MainLoop_UpdateAndRenderFrame` (`0022B8C0`), `0022BC20`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) calls `001EDDA0`, `001EDE80`; `0017E210` is called by `0022A0B0`; `001B1C00` is called by `0017D4C0`; `001EDC80` is called by `00265880`; `001EDDC0` is called by `0022BDF0`; `001FBD80` calls `001A1470`; `001FBD80` is called by `MainLoop_UpdateAndRenderFrame` (`0022B8C0`); `001FBE50` calls `001A1470`; `001FBE50` is called by `MainLoop_UpdateAndRenderFrame` (`0022B8C0`); `00229590` calls `00229EA0`; `0022A030` is called by `001EDE80`; `0022A080` is called by `001EDE80`; `0022BC20` calls `00374FD0`; `0022BC20` is called by `0022A580`; `002528A0` calls `00229EA0`; `00252A20` is called by `0022B6E0`; `00252A70` is called by `0022B7E0`; `00253970` is called by `0022A0B0`; `002628B0` calls `00229EE0`; `FieldData_GetVariable0` (`00265270`) is called by `001EC760`; `00265760` is called by `0022A770`; `00265860` calls `001EDDA0`; `00265880` calls `001EDDA0`; `0034CF90` calls `00265880`; `0034D790` calls `00265860`; `0034DB30` calls `00229EB0`.

**Input — MECHANICAL, 43 edges.** `0022BC20` calls `0017DE60`, `InputGameplay_RebuildFrameSnapshotFromChannelHistory` (`002498B0`), `0035AE30`, `0035AF10` and 4 more; `002B5B60` calls `001E0B90`, `001E0BD0`, `001E0DA0`, `001E0DC0`; `002B5C90` calls `001E0B90`, `001E0BD0`, `001E0DA0`; `00182D10` calls `00198690`, `InputManager_GetSingleton` (`00198790`); `00182DA0` calls `00198710`, `InputManager_GetSingleton` (`00198790`); `001E0BD0` calls `00197710`, `InputManager_GetSingleton` (`00198790`); `001E0DA0` calls `00197790`, `InputManager_GetSingleton` (`00198790`); `001E0DC0` calls `00197870`, `InputManager_GetSingleton` (`00198790`); `00253970` calls `00249840`, `0035FF60`; `0017E210` is called by `0022A4F0`; `002628B0` calls `0035B5D0`; `FieldData_GetVariable0` (`00265270`) is called by `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`); `00267310` is called by `002E09A0`; `0033F8E0` calls `InputGameplay_GetRemappedHistoryMask0C` (`0036FFD0`); `003401F0` calls `InputGameplay_GetRemappedHistoryMask10` (`0036FFE0`); `00340C70` calls `InputGameplay_GetActorStateAwareRemappedMask04` (`00248F10`); `00341030` calls `00182D10`; `003413E0` calls `00182DA0`; `003414E0` calls `InputGameplay_GetActorStateAwareRemappedMask08` (`00248EE0`); `00341D70` calls `InputGameplay_GetActorStateAwareRemappedMask0C` (`00248F00`); `00342450` calls `InputGameplay_GetActorStateAwareRemappedMask10` (`00248EF0`); `0034AF20` calls `002E12B0`; `0034B290` calls `002E1290`; `00356C40` calls `InputGameplay_GetRemappedHistoryMask04` (`0036FF70`); `00357530` calls `InputGameplay_GetRemappedHistoryMask08` (`0036FFC0`).

**Movement — MECHANICAL, 30 edges.** `002628B0` calls `00263560`, `0026A1D0`, `00379070`, `003791C0` and 2 more; `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) calls `Movement_SetRequestedSpeed` (`0026D6F0`), `002E4A10`, `Movement_UpdateActorFrame` (`002E5030`), `002E5750` and 1 more; `PartyFocus_ClearCurrentActorIfEligible` (`00358B40`) calls `002681D0`, `Actor_StopRequestedMovement` (`0026D6D0`), `002EC5B0`; `00202C70` is called by `00230790`, `PartyFollow_SolveFormation` (`00338490`); `00267310` is called by `Movement_UpdateSteeringTowardTarget` (`002E45E0`), `002E5750`; `001EC5C0` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`); `001EC5E0` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`); `001ED130` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`); `001ED180` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`); `001EDDA0` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`); `001EDDC0` calls `00337A00`; `001EDE80` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`); `0022BC20` calls `00263560`; `00252A70` calls `00357780`; `00357760` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`); `00357770` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`); `PartyControl_SetMovementSuppressionBit` (`00359200`) calls `Actor_StopRequestedMovement` (`0026D6D0`).

**Script_VM_Native_Bridge — MECHANICAL, 136 edges.** `00267310` is called by `0033F330`, `00340260`, `00340FA0`, `00341590` and 52 more; `003EB720` is called by `0033FAD0`, `00340530`, `003417F0`, `00347B00` and 15 more; `002EFA70` is called by `003559B0`, `00355EB0`, `00356270`, `00356650` and 2 more; `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) calls `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`), `ScriptVM_WaitList_HasAnyActorChannelActive` (`00267420`), `ScriptVM_WaitList_HasAnyActorResourceEntryActive` (`002674B0`), `00357760` and 1 more; `003601C0` is called by `00345140`, `003464D0`, `0034C370`, `003506A0`; `001ED180` is called by `0034CF90`, `0034D790`, `0034E630`; `001EC5C0` is called by `0034CF90`, `0034D790`; `001EC5E0` is called by `0034CF90`, `0034D790`; `001EC600` is called by `00354B20`, `00354E80`; `001EC680` is called by `00354B20`, `00354E80`; `001ED130` is called by `0034CF90`, `0034D790`; `002673D0` is called by `00342EC0`, `0034BBD0`; `002E7330` is called by `00342EC0`, `0034BBD0`; `00182D10` is called by `00341030`; `00182DA0` is called by `003413E0`; `001EC500` is called by `00352F00`; `001EC520` is called by `003526F0`; `001EC540` is called by `00352B30`; `001EC620` is called by `0034C7E0`; `002260E0` is called by `0034E6D0`; `00229EA0` is called by `00354D00`; `00265860` is called by `0034D790`; `00265880` is called by `0034CF90`; `002B5B60` is called by `00341030`; `002B5C90` is called by `003413E0`; `002E1290` is called by `0034B290`; `002E12B0` is called by `0034AF20`; `002E4CE0` is called by `0034A1D0`; `002E7380` is called by `0034A1D0`; `00349CB0` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`); `0034A1D0` is called by `thunk_FUN_0034a1d0` (`0034AD90`); `0034AF20` calls `VMResult_WriteInt32` (`0026B4E0`); `0034B290` calls `VMResult_WriteInt32` (`0026B4E0`); `0034B860` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`); `0034BBD0` is called by `thunk_FUN_0034bbd0` (`0034C700`); `0034CF90` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`); `0034D790` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`); `0034ECF0` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`); `003567F0` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`); `003600D0` is called by `0034E6D0`; `00360710` is called by `0034ECF0`; `00360A20` is called by `0034DB30`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
