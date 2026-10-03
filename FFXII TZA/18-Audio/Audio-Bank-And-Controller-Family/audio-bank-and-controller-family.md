---
system: Audio bank and controller family — two vtable layouts, one bank format, two id spaces
category: 18-Audio
status: DOCUMENTED
evidence_tier: 1
owner_layer: PrimaryOwner:Audio
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-13
audit:
  passes: 1               # one falsification pass, recorded in section 10
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: false
  reopened_count: 1
---

# The audio bank and controller family

**Twelve classes, and the family name is misleading.** `AudioBank` and `AudioController` are **two
unrelated vtable layouts**, not one hierarchy — and the `Seb`/`Sep` split that looks like two kinds of
audio is **one bank format with two id widths**.

## 1. What the player sees

**Sound effects, and how the game finds them on disc.**

When FFXII plays a sound effect it builds a path and loads a bank file. There are two id spaces over
the same format:

```
se003/se004.win.sab        <- three-digit id
se003/se000123.win.sab     <- six-digit id
```

Music takes a different format entirely (`.win.mab`) and a flat path. **So the practical division is
not "sound effects vs music vs voice" as the class names suggest — it is one sound-effect bank format
addressed two ways, plus music.**

## 2. Native mechanism

### Two layouts, not one hierarchy

The single most useful correction to the family's appearance:

| | banks | controllers |
|---|---|---|
| scalar deleting destructor | **slot 7** | **slot 0** |
| the *other* slot | slot 0 is an ordinary method | slot 7 is an adjustor thunk |

**Nothing means the same thing across the two halves.** The cross-check that settles it:
`MusicAudioBank` *also* has a slot 0, and it is **not** a destructor (101 B, no `free` call). If the
two layouts were one hierarchy shifted by an offset, that slot would have been a destructor too.

All six banks' slot 7 is a 52-byte body in the exact MSVC idiom, and all confirmed to call `free`:

```asm
call <real destructor>
test bl, 1
je   skip
mov  edx, <OBJECT SIZE>     ; sized operator delete
call free
```

### Four of the five controllers carry a second base at `+0x20`

> **Corrected, falsification pass 1 (2026-09-02).** This read *"**Every** controller's slot 7 is an
> adjustor thunk"* while listing four. There are **five** concrete controllers, and
> **`StreamAudioController` has no slot 7 at all** — its vtable is 7 slots long, the same length as
> the `AudioController` base. It does **not** carry the secondary base. See §10.

Four of the five controllers' slot 7 is an **adjustor thunk**, and all four are the same two
instructions:

```asm
MusicAudioController  00218980   add rcx, 0x20 ; jmp 0x2187D0
SebAudioController    0021B150   add rcx, 0x20 ; jmp 0x21AF80
SepAudioController    00219B10   add rcx, 0x20 ; jmp 0x2199C0
ShoutAudioController  0021C440   add rcx, 0x20 ; jmp 0x21C280
```

`add rcx, 0x20` before dispatch is the `this`-adjustment for a **secondary base subobject at +0x20** —
a real second inheritance path. The four jump targets are **four separate 161-byte bodies with
identical prologues**, not one folded body.

### The vtable slots, read individually (BD-3)

Every slot of both layouts, read from the bodies (SWE2-FRONTIER,
`FABLE-REQ-SWE2-FRONTIER-AUDIO-SLOTS`). "Entry" below means one node of the intrusive list the bank
keeps at `+0x8` (payload at node `+0x10`); the `002256xx` bodies are its field accessors
(`00225680` → `+0x10` state, `00225690` → `+0x24`, `002256A0` → `+0x14`).

**AudioBank** (base `ret 0` = `0016D6A0` wherever a slot is empty):

| slot | what it is |
|---|---|
| 0 | **broadcast — self-dispatch over the entry list.** `00222550` walks the `+0x8` entry list and calls the bank's **own** `vtable[+0x48]` (= slot 9) once per entry, passing the entry payload `[node+0x10]` as `rdx` and the caller's arg as `r8` (`00222580`: ~~`rax = [this]` loaded once before the loop~~ `rax = [this]` reloaded every iteration - `00222580` is the loop-back target of `00222596` *(corrected 2026-10-01, OPUS, as C-BK AC-4 says)*, `rcx = this`, `0022258D`); the vtable is the bank's, not the node's. Music's `00222C00` is driver-shaped instead: `007A7010` on `[this+0x38]`, then a result-switch — arg≠0 and result−1 ≤ 1 tail-jumps `007A8590` (`00222C3C`), arg==0 and result==3 calls `007A7A20` (`00222C41`). It never calls `00210B30`/`00210930` — those are Music **slot 10** `00222C70`'s first two calls. |
| 1, 3, 4, 5, 8 | **empty in the base** (`ret 0`); only Seb/Sep implement them — they are the sound-effect machinery. Sep slot 1 `00223490` and Seb `00224A30` are driver-backed entry ops (`007A7010`/`007A84A0`, accessor `00225680`). |
| 2 | **teardown.** Base `00222000`: if `+0x30 == 1`, frees handle `+0x28` by zeroing its slot in the 128-entry global table `01FD36C0` (`00212A70`, `00222014`), runs `00222080`, then driver-frees `[+0x20]+8` through `007A88F0`. Music `00222BD0` calls `007A84A0` on `this+0x38` (43 B) then **tail-jumps the base `00222000`** (`00222BF6`) — the driver call plus the full teardown, not driver-only; Sep `00222FE0`, Seb `00223E60`, Shout `00224D40` route their cleanup through `002255B0` + `00809950`. |
| 3, 4, 5 | **Sep: three id-range-gated re-dispatches to slot 0.** `00223100` fires when ~~`[+0x38] ≥ 151000` (`0x249F0 + 0x3E8`)~~ `[+0x38]` lies **outside** `[0x249F0, 0x249F0+999]`: it computes `[+0x38] − 0x249F0` and returns on an unsigned `< 0x3E8`, so ids below 150000 pass as well as ids from 151000 up (*corrected 2026-09-26, FABLE; `s41-opus-replay-bank-family` AC-7 case*). It also needs `+0x50` set and `+0x49 & 0x68 == 0, & 1 == 1`; `002230D0` is the same gate with mask `0x69`; `00223130` fires when `[+0x38]` lies **in** `[0x249F0, 0x249F0+999]`, `+0x50 != 0` and `+0x49 & 1 == 0` — ~~the six-digit id space splits at 150999/151000~~ one 1000-id band, 150000–150999, is treated apart (slots 3/4 skip it, slot 5 acts only inside it), and the flag byte picks the state. **Seb: three 258–266 B copies of one iterator** (`00224180`/`00223FA0`/`00224360`): walk `+0x8` entries, skip when state `00225680 == 2` or `[+0x24] / 1000 == 150` (reciprocal `0x10624dd3`, `sar 6`, `cmp 0x96` — ~~the `≥ 150000` six-digit range~~ exactly the band 150000–150999, the same window the Sep gates use), read `[+0x14]` via `002256A0`, then probe the `+0x60`/`+0x70` map — **the BD-3 "one operation with a varying parameter" is confirmed**: same body, the differing bytes are the constant/field used per slot. |
| 6 | base `00657140` = `ret 0`. Sep `00222D30`: get entry `00221E60`, require state 1 + `+0x49 & 0x40`, then `002224F0` when arg equals `[+0x38]` else `002225B0` (both with `0x120`). Seb `002238F0` (292 B) runs the same predicate family plus driver `007A84A0`. |
| 7 | scalar deleting destructors — the 52 B `free`-calling bodies §2 already proves. |
| 9 | **arm one entry.** Base `00222340` loads a float constant (`008C5F6C`), then tail-jumps a driver on `rdx+8` — `007A8590` when `r8 != 0` (`0022237B`), `007A7A20` when `r8 == 0` (`0022238A`). Seb `00223F40` is the filtered variant: forwards when `[+0x38] != 0` **or** (`+0x38 == 0` and entry `[+0x14]` ∉ {2, `0x59`}) — `+0x38 != 0` alone forwards unconditionally (`00223F5C`); only the `+0x38 == 0` path reads the entry type. |
| 10 | **manager-gated replay — a ~~five-bit~~ six-bit command mask** *(corrected 2026-10-01, OPUS: `0x01`-`0x20`)*. All four concrete banks read the shared manager through `00210B30`→`00210930` and test its `+0x3C` flag byte: Music `00222C70` needs `& 1` and re-dispatches **slot 0**; Sep `00223540` and Seb `00224B30` (the latter also requires `[+0x38] != 0`) need `& 2` and re-dispatch **slot 9**; Shout/Stream `00225440` need `& 4`, also to slot 9. The byte carries three more commands, all with `edx = 1`: Sep `00223540` continues, but only when bit 2 is clear (bit 2 is a tail jump that ends slot 10), with `& 8` → own `vtable[+0x18]` (**slot 3**), `& 0x10` → `[+0x20]` (**slot 4**), `& 0x20` → `[+0x28]` (**slot 5**) (`00223596`–`002235CF`); Seb `00224B30`, again only when bit 2 is clear, calls the entry-level copies of the same op family — `& 8` → `00224290`, `& 0x10` → `002240B0`, `& 0x20` → `00224470` (each opens with the `00225690` accessor + `/1000` quotient test on the rdx entry). |

**AudioController:**

| slot | what it is |
|---|---|
| 0 | scalar deleting destructors (§3 size table). |
| 1 | **Sep only** (`00219970`): walk `+0x8` entries and `00223300(node, -1, 0)` every node whose `+0x49` matches the arg byte — a selective entry stop/reset. No other controller overrides it (RTTI matrix). |
| 2 | all classes `0021B0D0`: walk `+0x8`, call each node's `vtable[+0x30]` (bank slot 6), **or-accumulate** the boolean results (`0021B123`–`0021B12D`) — "does any managed bank answer true". |
| 3 | **erase a keyed entry from the `+0x60` map.** Shared `0021D570` is a `+0x20` adjustor to `00219D80`: tree-walk by key `rdx`, then `00199DB0` + `dec [+0x80]` + ~~`0016D6D0` unlink + `0016DA60` pool-free~~ `0016D6D0` (a red-black tree iterator step, no stores) + `0016DA60` (the red-black erase: transplant, colour swap at `+0x18`, rotations `0016D780` / `0016D7E0`; corrected 2026-09-15, `OPUS-CONTRA-AUDIO-UNLINK-IS-A-READ`) + a release via `[+0x88]` vtable slot 3. Sep `00219C40` logs first (`005CD4F0`) then erases; Seb `0021B290` erases then calls `00222170`. |
| 4 | `00212860` walks `+0x8` and runs `00221FB0` on each node with `+0x2C == 0` and `+0x30 == 0` — idle-entry housekeeping; Stream has its own `0021D4E0` (137 B): counts the `+0x8` list and fires only at **exactly 4 entries** (`0021D50B`), then calls the head payload's `vtable[+0x10]`, own `vtable[+0x18]` (slot 3) on that payload, unlinks the head node (`0021D531`–`0021D54B`), and calls `[this+0x18]`'s `vtable[+0x18]` — three indirect dispatches plus a list mutation, not self-contained. |
| 5 | all classes `00212810`: calls the linked object's (`[this+0x18]`) `vtable[+0x10]` with `edx = 0x18` (`00212830`), stores the arg into `[ret+0x10]`, and splices the returned node into the `+0x8` list (`0021283F`–`00212851`) — entry **registration**, not a one-line delegation. |
| 6 | **pop a request, or make one — then dispatch it.** Music `00218920`: call own slot 7 (the `+0x20` queue drain); if it returns nothing, call slot 4 and retry the drain (`0021893B`–`0021894D`); then tail-dispatches the popped request through own `vtable[+0x28]` = **slot 5** (`00218966`, `rdx` = the popped entry). Shout `0021C3D0` same shape; Stream `0021D3D0` does the identical sequence directly on `+0x20` through `0021D280` — consistent with Stream's missing slot 7. |
| 7 | the `+0x20` request-queue drain — the adjustor/`161 B`-body family of §2, fully read under BD-4 below. |

~~The +0x50 field the Sep slot-8 bodies require non-null is the driver's voice/handle object
(lazy-created through `00221D10` → `00221710` → `00220CE0`); `00221780` constructs the callback
wrapper it carries (vtable `009078B0`).~~ *(Corrected 2026-10-01, OPUS, at the bytes: the Sep slot-8 body `00222F20` requires `+0x50` non-null (`00222F26`) and passes it to `007A48C0` (`00222F61`); the voice/handle object it also needs is cached at `+0x20`, lazily created through `00221D10` -> `00221710` -> `00220CE0` (`00221D16`, `00221D47`), as SWE2-EC7-68 below says. `00221780` is the `AudioBank` base constructor (vtable `009078B0`).)*

## 3. Key addresses

**Object sizes, stated by the code itself** (from the `mov edx, <size>` in each deleting destructor):

| class | size | deleting destructor |
|---|---:|---|
| `AudioController` | **0x20** | `002127D0` |
| `AudioBank` | **0x38** | `00218260` |
| `StreamAudioBank` | **0x48** | `0021CD80` |
| `MusicAudioBank` | **0x58** | `002182A0` |
| `SepAudioBank` | **0x68** | `002195D0` |
| `ShoutAudioBank` | **0x68** | `0021BF20` |
| `SebAudioBank` | **0xA0** | `0021ABC0` |
| `MusicAudioController` | 0xB8 | — |
| `ShoutAudioController` | 0xB8 | — |
| `StreamAudioController` | 0xB8 | — |
| `SebAudioController` | 0xE0 | — |
| `SepAudioController` | 0xE0 | — |

The seven with an address are the ones re-verified here from their own deleting destructor; the five
concrete controllers' sizes come from `FUN_002105E0`'s allocation sites (section 8).

**The AudioManager** — built by `FUN_002105E0`, one `new` per controller:

```
+0x00  MusicAudioController    0xB8   ctor 00217FD0
+0x08  SebAudioController      0xE0   ctor 0021A9F0
+0x10  SepAudioController      0xE0   ctor 00219400
+0x18  StreamAudioController   0xB8   ctor 0021CC10
+0x20  ShoutAudioController    0xB8   ctor 0021BDB0
+0x28  = &[00906A18]
+0x30  = 0xFFFFFFFF
+0x34  subobject built by FUN_007A59F0
+0x38  = 0
```

**Construction order is 0, 8, 0x10, 0x20, 0x18** — Shout is built *before* Stream but stored *after*
it. Construction order is not slot order, and reading one as the other would misassign two classes.

## 4. Data structures and formulas

### The taxonomy, proven from manager offset to format string

The chain is manager field → per-format entry point → loader → string, so the class assignment does
**not** rest on address locality:

| manager | entry loads | entry | loader | format | path template |
|---|---|---|---|---|---|
| `+0x00` | `[rcx]` | `00210980` | `00222740` | **`.win.mab`** | `%s%03d%s` |
| `+0x08` | `[rcx + 8]` | `00210B60` | `00223AD0` | **`.win.sab`** | `%s/se%03d/se%03d%s` |
| `+0x10` | `[rcx + 0x10]` | `00210C40` | `00222DC0` | **`.win.sab`** | `%s/se%03d/se%06d%s` |

**So: `+0x00` is Music, `+0x08` is Seb, `+0x10` is Sep.**

> **The Seb/Sep distinction is narrower than the names suggest.** They are **the same bank format,
> `.sab`**, differing only in the **id width of the path — three digits against six**. Not two kinds
> of audio; **two id spaces over one format.**

That also explains the size distribution: Seb and Sep are the `0xE0` controllers with 10 and 9 bank
methods, carrying the full sound-effect machinery, while Music, Shout and Stream are `0xB8` with 4, 2
and 1.

`AudioFileLoadManager` and `.win.config` live in the same region — `FUN_00212130`, `FUN_00210760`.

## 5. Call chain

```
FUN_002105E0  (AudioManager construction)
   new 0xB8 -> MusicAudioController   -> manager +0x00
   new 0xE0 -> SebAudioController     -> manager +0x08
   new 0xE0 -> SepAudioController     -> manager +0x10
   new 0xB8 -> ShoutAudioController   -> manager +0x20
   new 0xB8 -> StreamAudioController  -> manager +0x18

play/load request
   -> 00210980 / 00210B60 / 00210C40      (per-format entry, selects by manager offset)
        -> 00222740 / 00223AD0 / 00222DC0 (loader, builds the path)
             -> ".win.mab" | ".win.sab"
```

## 6. Modding notes

- **The path templates are the intercept point** for redirecting sound effects: `%s/se%03d/se%03d%s`
  and `%s/se%03d/se%06d%s` are built in the loaders, not read from a table.
- **A bank and a controller are unrelated types** despite the shared naming. Anything walking these
  vtables must not assume a common slot means a common method.
- **XIIOnline:** nothing here is gameplay state. It matters only if remote-triggered sound effects are
  ever routed through the same loaders, which has not been checked.

## 7. What is not known

> **CORRECTED 2026-09-18 (FABLE): the records are bank objects, not voice records.** The mechanism below stands;
> its last two sentences do not. The strides are this page's own bank sizes (§ the sized-destructor table), the pop
> body's per-type callee is each bank's constructor (shared `AudioBank` base constructor, then the `MusicAudioBank` /
> `SebAudioBank` / `SepAudioBank` / `ShoutAudioBank` vtable), and slot 6 is *allocate a bank* - pop, else slot 4 and
> pop again, then register through slot 5. So the constants cap **live banks per class** (2 / 96 / 256 / 4 / 6); voices
> come from the shared 1024-record pool set out on
> [the sound-request page](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md) (UQ-244). Stream's slot 4 firing at
> exactly 4 entries is the same number seen from the other side.
>
> **BR-8 answered 2026-09-12 (FABLE): the five pool constants are per-controller ~~voice-record~~ record
> capacities.** Each constructor hands its constant to a shared 251-byte pool template
> (`00217E10` / `0021A820` / `00219300` / `0021CB10` / `0021BCB0`) that builds an `EASTL set` free
> list at controller `+0x20`, a second set at `+0x58`, and calls the class's reserve function with
> the count (`00218990`, `0021B160`, `00219B20`, `0021D440`, `0021C450` — one body, five strides):
> it grows the record vector at `[this]` to `count` records if smaller (`00218E80`: current capacity
> from `(end − begin) / stride` by reciprocal multiply, `00218EA0`–`00218ECD`), then **inserts every
> record `[this] + i·stride` into the free set** (`002189D0`–`002189FA`, `00199DB0`) and marks
> `+0x90`. The strides are the record sizes: **Music 2 × 0x58, Seb 96 × 0xA0, Sep 256 × 0x68,
> Stream 4 × 0x48, Shout 6 × 0x68** — ~~so 2 concurrent music voices, 96 environmental, 256
> effect, 4 stream and 6 shout records exist to be handed out, and a request for a seventh shout
> or third music voice finds the free set empty. That the free set's consumer is the voice-acquire
> path is the reading the controller names and the set structure give; the acquire function was
> not read here.~~ *(Struck 2026-10-01, OPUS, as the 2026-09-18 correction above withdrew it: so at most 2 Music, 96 Seb, 256 Sep, 4 Stream and 6 Shout bank objects can be live at once; voices come from the shared 1024-record pool, `UQ-244`.)*

- [x] **`ShoutAudioController` and `StreamAudioController` are unidentified.** Neither references any
      inline format or path string anywhere in `0x210000`–`0x227000`; only 17 distinct strings are
      referenced from that whole region and none belongs to them. **BD-1.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): neither loads a file. Each is handed banks already in memory,
      and the region has no path string because the loading happens elsewhere.** Static.
      - **`ShoutAudioController` takes the party's battle-voice banks.**
        - The names `shout00.win.sab`–`shout63.win.sab` exist only as the loader directory's slot 33 (`us`) and
          slot 39 (`jp`) tables, which the directory's installer stores at `0215F108` / `0215F138`. Nothing else reads those two
          cells.
        - Neither file-id decoder produces either slot: the type-letter decoder gives twelve other slots, and the
          actor decoder gives 1, 5 or 8.
        - The one caller that asks for them by number is the load step of the party read-in's voice-pack
          entries ([UQ-50](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md)).
          For the entry's key `+0x14` it sizes and requests the `us` bank from slot `0x21` into handle `+0xC`, then
          the `jp` bank from slot `0x27` into `+0x10`.
        - Each completion callback (`0036EAB0`, `0036E9F0`) hands the loaded buffer to `001DC130`. That wrapper takes
          the audio registry's `+0x20` object, the `ShoutAudioController` (constructor `0021BDB0`, vtable
          `00907FF0`), and enters its intake `0021C680`. The intake reuses the bank whose `+0x3C` matches the id,
          or pops a free one, under a kind-8 handle.
        - The voice-pack tables hold 2 + 4 entries, the same as the controller's six-bank pool (a numeric agreement;
          no code ties the two).
      - **`StreamAudioController` takes the event and map voice packs and the BGM stream.** Its intake `001DC2E0`
        enters registry `+0x18`, the `StreamAudioController` (constructor `0021CC10`, vtable `00908200`), at
        `0021D770`. The stream wrapper in front of it has three callers:
        - the voice-pack cue start `003E9C10`, which checks a `sabf` header first
          ([the voice-pack slots](../the-voice-pack-slots-and-the-voice-verbs.md));
        - the script BGM stream machine
          ([the music control file](../the-music-control-file-and-the-bgm-stream.md));
        - the bootstrap coordinator.
      - Control: `_index/candidates/bd1-shout-stream-load/bd1_load_chains.py`, 15 checks, FAILS 0. It reads the two
        directory tables entry by entry, finds every access to their slot cells, decodes every file-id type letter
        (planted: slot 15 must appear), and reads each hop of both chains, down to the RTTI names.
- [x] **No audio API call was traced out of any of the 43 methods.** The taxonomy rests entirely on
      path strings and manager offsets — nothing here shows a call into a mixer, voice or driver
      layer, so *"this class plays sound effects"* is **not** established, only *"this class loads
      `.sab` files named this way"*. **BD-2.** **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5)**: they play audio; see
      the start path below.
      ***Narrowed 2026-09-26 (FABLE, Claude Opus 5.5): they do not only load; they control playback of the sounds they
      own.*** Static.
      - **How SEAD takes the calls.** SEAD's handle API queues commands: allocate (`007AB460`), stamp a type, commit.
        The drain `007AB5C0` switches on the type through the table at `007AC080`, and resolves the handle to a sound
        object whose vtable slot it calls.
      - **What each command does.** In `SQEX::Sd::Driver::Sound` (vtable `01CB5A30`) the slots are named by the state
        their per-sequence step writes at `+0x9C`:
        - command `0xB` → slot 2 `007BED30` = **stop**, with a fade (sequence state 4 or 3);
        - command `0xC` → slot 3 `007BEF30` = **pause**, with a fade: it ramps the gain block `+0x108` to 0 and sets
          state 5;
        - command `0xD` → slot 4 `007BE0B0` = **resume**, with a fade: it ramps `+0x108` back to 1.0 and sets state 2.
      - **Which bank slots issue them.**
        - Bank slot 9, "arm one entry" (`00222340`), posts **pause** (`007A8590`) when its flag is non-zero and
          **resume** (`007A7A20`) when it is zero, both with a 0.1-second fade (`008C5F6C`). So AC-6's manager command
          bits 2 and 4 pause or resume a bank's entries.
        - The teardowns (slot 2 on `AudioBank` and Music, slot 1 on Seb and Sep) post **stop** (`007A84A0`).
        - Music's slot 0 reads the sound's state through `007A7010` and then pauses or resumes.
      - ~~*Not established:* whether any bank method **starts** a sound. Three command types they post are not identified:
        `0xA` and `0x1C` (from `007A78B0`, reached from Seb's slot 2). Neither is the path by which `.sab` data
        gets loaded.~~ *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): no vtable method reaches `007A78B0`, and both
        commands begin playback.* The first version of the control read each body to its first `ret`. Seb's slot 2
        (`00223E60`) is a teardown that ends in a tail jump, so the read ran on into the following functions and
        credited the slot with their calls. Bounded by function starts, no bank vtable slot reaches `007A78B0` within
        two calls. *Command `0xE` (from Seb's slot 6, through `007A81F0`) is identified: it reaches `Sound` slot 7,
        `007BEAF0`, which is **`Sound::SetVolume`**. Its own warning string at `01CB5BC0` reads "`Sound::SetVolume`
        `failed range over %f`" (2026-09-26, FABLE).*
      - **The start path** *(read 2026-09-26, FABLE, Claude Opus 5.5; static)*. `007A78B0` is SEAD's handle-level play
        request, and [the sound trigger](../Sound-Selection/sound-trigger.md) already reads its dispatch and its callers.
        Five non-virtual bank functions call it: the voice starts `AudioBank_StartVoice` and its stream twin that
        [how a sound request becomes a voice](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md) reads, plus
        `00224E40`, `00224F10` and `002252C0`. Every one of them passes fade 0 and offset 0. The wrapper dispatches on
        the handle's type byte: type 2 posts `0xA`, type 8 posts `0x1C`, and type 7 goes to a second queue.
        - **`0xA` arms a `Sound` trigger.** Its arm resolves a type-2 handle and calls `007BDFA0`. That is the state
          1 → 2 step of the trigger page's G-16 lifecycle (bound → armed). It ramps the gain block `+0xC8` to 1.0 over
          the fade and stores the offset at `+0x500`, and the stepper `007BD120` later carries the trigger to dispatch.
        - **`0x1C` arms a `Music`** (`SQEX::Sd::Magi::Music`, vtable `01CB5E38`, whose status slot 21 reads its state
          at `+0xC8` the way `Sound`'s reads `+0x54`). Its arm resolves a type-8 handle and calls `007C8370`. That
          method takes only state 1, ramps `+0x190` to 1.0 over the fade, stores the start fields (`+0xD8`, `+0x638`,
          `+0x700`/`+0x704`) and sets the state to 2.
        - So the bank classes do begin playback, through their non-virtual voice-start functions. Their vtable methods
          pause, resume, stop and set the volume.
      - Control: `_index/candidates/bd2-bank-playback-control/bank_sead_calls.py` (FAILS 0). It enumerates every SEAD
        call from the six vtables to depth 2, each body bounded by the next function start, and classifies each call by
        the command it posts. The known positive: base slot 9 is found reaching both pause and resume. A sensitivity
        check reproduces the unbounded read's false attribution. Further checks read the type dispatch, both drain
        arms, both start methods and the wrapper's callers.
- [x] ~~Bank slots 1–6 and 8–10 individually~~ — **BD-3 ANSWERED (SWE2-FRONTIER):** the per-slot
      table above. The Seb/Sep 3/4/5 shape resolves into two different things: Sep's are 35–41 B
      id-range gates that tail-call slot 0, Seb's are the 258–266 B iterator over `+0x8` entries
      (state/field predicates `00225680`/`00225690`/`002256A0` then a `+0x60` map probe) — one
      operation, three constants. Still open inside it: what the `+0x60`/`+0x70` map is keyed on,
      and which driver verbs `007A48C0`/`007A8590`/`007A88F0`/`007A84A0` are (SQEX Sd layer).
- [x] ~~What the secondary base at controller `+0x20` is. Four 161-byte targets with identical
      prologues, unread.~~ **BD-4 ANSWERED 2026-09-12 (FABLE): not a base at all — an embedded
      request queue, and slot 7 is its drain step.** The RTTI of `MusicAudioController` (`00907970`)
      and `SebAudioController` (`00907DE0`) lists one base each, `AudioController` — no second
      inheritance path — and ~~the base constructor `002130E0` zero-fills `+0x08`–`+0x38` as plain
      data~~ the base constructor `00212710` builds only the entry list at `+0x08` / `+0x10`, and each derived constructor then builds the member at `+0x20` (e.g. `00217FD0` -> `00217E10`) *(corrected 2026-10-01, OPUS: `002130E0` installs `00906DC8`, the `DynGeoFontTextInstance` vtable, and its only caller is `001E8580`)*. The `add rcx, 0x20 ; jmp` thunks are therefore member-object method calls, and the four
      161-byte targets (`002187D0`, `0021AF80`, `002199C0`, `0021C280`) are **one body specialised
      only in its last call**: with `q = controller + 0x20`, if the count `q+0x48` is non-zero, take
      the head node `q+0x30` (its `+0x20` is the request payload), decrement, ~~unlink it
      (`0016D6D0`), return it to the free list at `q+0x28` (`0016DA60`)~~ step the tree iterator (`0016D6D0`, which
      stores nothing) and erase the node from the red-black tree on `q+0x28` (`0016DA60`: transplant, colour swap,
      rotations `0016D780` / `0016D7E0`; corrected 2026-09-15), release its 0x28-byte
      node through the pool vtable at `q+0x50` slot 3, signal `q+0x58` through `00199DB0` — the
      slot allocator this page already sizes per controller — and dispatch the payload to the
      per-type constructor: Music `002226A0` (the `MusicCallback` sub-object this page names), Seb
      `002235F0`, Sep `00222CB0`, Shout `00224BF0`; an empty queue returns 0. So `+0x20` holds the
      controller's queued-request list (`+0x28` free list, `+0x30` head, `+0x48` count, `+0x50` node
      pool, `+0x58` sync), slot 7 pops and dispatches one request, and `StreamAudioController` lacks
      the slot because it queues nothing.
      ***Reworded 2026-09-18 (FABLE): what is popped is a free bank record, not a request.** The structure read above is
      exact; the vocabulary was not. The set on `q+0x28` is the free set the reserve function filled with every
      record of the pool, `q+0x58` is the set of records handed out, and the per-type callee constructs a bank in the
      popped record (it runs the `AudioBank` base constructor and installs the class vtable). Slot 7 is therefore
      *take a free bank*, slot 6 *allocate and register a bank*, and `+0x20` is the controller's bank pool.*

## 8. Evidence

**Tier 1**, and this document is a **two-session result**: the analysis is peer session repos-39's,
independently re-verified here before publication.

**Re-verified in this session, from the shipping image:**

| claim | result |
|---|---|
| bank sizes from the sized deleting destructor | **7 of 7 reproduce exactly**, every one with a confirmed `free` call |
| the three loader format strings | **exact match** — `.win.mab` + `%s%03d%s`, `.win.sab` + both `se` templates |
| the three entry points' manager loads | **exact** — `[rcx]`, `[rcx+8]`, `[rcx+0x10]` |
| controller slot 7 adjustor thunks | **all four** are `add rcx, 0x20 ; jmp <target>` |

**A method worth keeping, and its limit.** MSVC's deleting destructor passes the object size to sized
`operator delete`, so **a class with a virtual destructor states its own size in its own code** —
no constructor call site needed. **But route agreement here is honestly partial and repos-39 said so
rather than implying otherwise:** the five concrete controllers are confirmed a second way at
`FUN_002105E0`'s allocation sites (`mov ecx,<size>`), and **the six banks are not** — their allocation
does not put a literal size in the calling function. **Six of the twelve sizes rest on one route.**

**The two-layout finding is an idiom match, not a statistic**, so no base rate applies:
`test bl,1 / mov edx,N / call free` in a vtable slot is the deleting-destructor signature by
construction. The load-bearing cross-check is `MusicAudioBank`'s slot 0 being 101 B with **no** `free`
call — which is what rules out "one hierarchy, shifted".

**The taxonomy deliberately avoids address locality.** The chain runs manager field offset → entry →
loader → string. Adjacency is a banned evidence class
([`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)) and is not used.

**On Shout's paths.** This document does *not* claim Shout loads from the asset-category directory at
`0x0215F000`. That is a separate finding in this database which is **consistent** with Shout having no
inline strings — but consistency is not derivation, and repos-39 flagged the direction explicitly:
that finding corroborates this negative rather than this negative establishing it.

## 9. Related

- [`../sead-function-identification.md`](../sead-function-identification.md) — 90 audio functions
  named by the strings they emit; the driver layer beneath these loaders.
- [`../sqex-sd-sound-driver-architecture.md`](../sqex-sd-sound-driver-architecture.md) — the SQEX Sd
  driver these banks ultimately feed.
- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)
  — the index these twelve classes were selected from.

## 10. Falsification pass 1 — 2026-09-02, by a session that did not write this document

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`.

**Whether a pass had happened was checked first, not assumed.** `AUDIT-LOG.md` pass 104 is this
document's *authoring* pass — its scope line reads "new document
`18-Audio/Audio-Bank-And-Controller-Family/…`". It is a harder case than a plain authoring pass,
because it **did** include independent re-verification of four load-bearing claims before
publication. But verification is *support*, and
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) is explicit that support is not proof: a
claim earns its place only after someone has tried to **destroy** it. No attack was recorded and
there was no §10. **This is the first falsification pass.**

**Declared conflict of interest.** The auditing session wrote
[`../Audio-Boundary/how-a-sound-request-becomes-a-voice.md`](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md),
which shares five addresses with this document — the five controller constructors. Those overlapping
claims were attacked *harder*, not taken as agreed, and every one was re-derived from the image
rather than from either document.

### Overturned: `StreamAudioController` has no slot 7 and no secondary base

§2 read *"**Every** controller's slot 7 is an adjustor thunk, and all four are the same two
instructions"* — a claim about the family, evidenced by a table of four, while the family has five.
Recovered from RTTI, slot counts per class:

| class | vtable | slots | slot 7 |
|---|---|---:|---|
| `AudioController` (base) | `00906CD0` | **7** | — |
| `MusicAudioController` | `00907970` | 8 | `00218980` adjustor |
| `SebAudioController` | `00907DE0` | 8 | `0021B150` adjustor |
| `SepAudioController` | `00907BA8` | 8 | `00219B10` adjustor |
| `ShoutAudioController` | `00907FF0` | 8 | `0021C440` adjustor |
| **`StreamAudioController`** | `00908200` | **7** | **absent** |

`StreamAudioController`'s vtable is the same length as the base's. **It does not carry the secondary
base at `+0x20`**, so the section heading was false for one class in five.

**Stream is the odd member on four independent counts**, which is the substantive result here:

1. no slot 7 / no secondary base (this pass);
2. `0xB8` with **one** bank method, against Seb and Sep at `0xE0` with 10 and 9 (§4);
3. constructed **fifth** but stored at `+0x18`, before Shout at `+0x20` (§3);
4. never selected by the play call's fork, which reaches only `+0x08` and `+0x10`
   ([the audio boundary document](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md) §2).

None of the four is derived from any other.

### Attacked and survived — every remaining load-bearing claim

| Claim | How it was attacked | Result |
|---|---|---|
| the seven object sizes stated by the deleting destructors | re-decoded the `mov edx, <size>` in each of the seven bodies from the EXE | **7 of 7 exact**: `AudioController` `0x20`, `AudioBank` `0x38`, `StreamAudioBank` `0x48`, `MusicAudioBank` `0x58`, `SepAudioBank` `0x68`, `ShoutAudioBank` `0x68`, `SebAudioBank` `0xA0` |
| "all six banks' slot 7 is a 52-byte body in the exact MSVC idiom" | slot 7 of all six bank vtables | **6 of 6 at 52 B**, identical prologues, each with the `call` to the deallocator |
| the four adjustor targets are "four separate 161-byte bodies with identical prologues", not one folded body | disassembled all four targets | **four distinct addresses, all 161 B, one distinct prologue** — as stated, and not folded |
| the cross-check that the two layouts are not one hierarchy: `MusicAudioBank` slot 0 is "not a destructor (101 B, no `free`)" | read the body | **101 B**, calls `007A7010` and `007A7A20` (SQEX Sd driver), **no deallocation** |
| **the taxonomy chain, manager offset → entry → loader → format string** | re-derived end to end, with a positive control on the string scan | **exact.** `00210980` loads `[rcx+0]` → `00222740` → `.win.mab` / `%s%03d%s`; `00210B60` loads `[rcx+8]` → `00223AD0` → `.win.sab` / `%s/se%03d/se%03d%s`; `00210C40` loads `[rcx+0x10]` → `00222DC0` → `.win.sab` / `%s/se%03d/se%06d%s` |
| the manager layout and construction order `0, 8, 0x10, 0x20, 0x18` | read `002105E0` directly | confirmed — Shout is constructed before Stream and stored after it |

The §4 conclusion — **one sound-effect bank format addressed by two id widths, plus music** — is the
strongest claim in the document and it reproduces in full. Three digits against six is the entire
`Seb`/`Sep` difference at the path level.

### What I tried that failed to break it

- Attacked the size table expecting at least one transcription error across seven values. None.
- Attacked "four separate bodies, not one folded body" specifically because `/OPT:ICF` folding has
  produced false distinctions elsewhere in this database. The four are genuinely distinct addresses.
- Attacked the taxonomy chain with a positive control on the string scan first, because an absence
  or a miss in a string census has already produced a wrong result twice in this project.
- Ran the neighbour check before attacking: 11 addresses shared with
  [the vtable index](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) and 5 with the
  audio boundary document. No contradiction in either direction.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

The family's container primitives are shared, and every crossing here is one of them:

- **Platform and Presentation — MECHANICAL.**
  - The ~~tree-node unlink~~ red-black iterator step `0016D6D0` and the ~~pool free~~ red-black erase `0016DA60` (corrected 2026-09-15) are used by Platform bodies (182 B and 232 B) and six
    Presentation bodies.
  - `00199DB0`, which runs in the family's erase sequence, is used by a 346-byte Presentation body.
  - ~~The base constructor `002130E0` is used by a 3,572-byte Presentation body.~~ *(Struck 2026-10-01, OPUS: `002130E0` is not this family's base constructor - it builds a `DynGeoFontTextInstance`; the family's base constructor is `00212710`.)*
  - The retracted 4-byte `00225690` is read by four Platform bodies and a 1,293-byte Presentation body.
  - The logger `005CD4F0` is called by Platform, Presentation and Input bodies (139–1,950 bytes).
  - `00219400` and `0021A9F0` call a 63-byte Platform helper.
- **Input — CLIENT.** The retracted 4-byte `00225680` is read by a 25-byte Input helper.
- **CoreRuntimeScheduling - SERVICE (1 edge).** `001E8580` reaches bodies filed to core runtime scheduling: `001A1470` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (64 edges).** `005CD4F0`, `005CD820`, `001BA860` are also called by bodies filed to resource: `0020BFA0`, `001A0A90`, `0020B680` (+27 more); `00210760`, `00223AD0`, `00222DC0` reach bodies filed to resource: `002121C0`, `001D6E80`, `001D6EE0` (+4 more) - shared machinery across the layer boundary, no shared ownership.
## The `00218E80` exclusive subtree — all 6 members bound (SWE2-FRONTIER, followup queue)

`00218E80` — the record-vector grow §7 names — owns **6 frontier functions**: the `0x58`-stride
element machinery its relocate-and-insert path runs. Every member was disassembled from the
shipping image; interior cites are one instruction inside each declared extent.

| member | size | role | interior |
|---|---:|---|---|
| `00217BA0` | 135 B | backward range move (`dst` walks `r8` down by `0x58`, src `rdx`→`rcx` down by `0x58`) with per-element `002181A0` sub-copy — the `move_backward` the insert uses to open a hole | `00217BC0` |
| `00217C30` | 135 B | the forward twin — `rcx`→`rdx` up by `0x58` into `r8` | `00217C9B` |
| `00217CC0` | 164 B | construct-fill over a `[begin,end)` range: `00217F10` element ctor per `0x58` step, then stamps the two rodata pointers (`+0x00`, `+0x40`) and copies `+0x38`/`+0x48`/`+0x50` | `00217D18` |
| `00217D70` | 156 B | the count form — `edx` elements at `rcx`, same `00217F10` + dual rodata stamp per element | `00217DC6` |
| `00218880` | 152 B | relocate-and-destroy: forward-moves the tail with `00217C30`, runs each vacated element's `+0x38` virtual destructor, then advances `[this+8]` by `(count)×0x58` via the `0xD1745D1745D1745D` reciprocal | `002188E1` |
| `00218380` | 1,093 B | the insert body: `00217CC0` construct-at-end, `00217BA0` hole-open, `002181A0` element copies, `001EDF00` allocate + `00222700` free on the grow path, virtual `+0x10`/`+0x38`/`+0x18` element calls | `00218491` |

`00217F10` (the element ctor — stamps vtable `01E678B0`), `002181A0` (the element sub-copy),
`001EDF00`/`002226A0`/`00222700` (allocator) are shared callees — deliberately not census
members. The root itself does the capacity probe (`(end−begin)/0x58` by reciprocal
`0x2E8BA2E8BA2E8BA3`, `00218EA7`–`00218ECD`), allocates the new span, calls `00218380` for the
insert, frees the old span, and relocates the tail through `00218880`.

## The `00223AD0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00223AD0` (~500 B) — the `.win.sab` loader on the `[rcx+8]` manager
slot — validates with `0016D6A0` ×6: `[r15+0x50]` non-null
(`00223B1C`), `dword[r15+0x3C]` and `dword[r15+0x38]` vs `-1`
(`00223B28`/`00223B37`), `eax` vs `r13d` (`00223B59`); then
`00223A20` (`00223B67`), `bx` vs `word[rbp+0xA]` (`00223B72`),
`dword[rsi]` vs `-1` gate (`00223B94`), `00221710` + member
`00220CD0` chain (`00223B9D`/`00223BA5`), and an indexed read
`dword[rdx + r8*4]` (`00223BC5`).

| member | role | interior |
| --- | --- | --- |
| `00220CD0` (12 B) | thunk into `002203F0` (`00220CD7`) — member→member edge | [`00220CD7`](../../_index/ADDRESS-INDEX.md) |
| `002203F0` (165 B) | record accessor — `dword[rcx+0x48]` non-null gate (`002203F6`), `rbx = [rcx+0x30]`, `rdi = [rbx+0x20]` (`00220408`/`00220411`) | [`00220411`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0016D6A0`, `00223A20`, `00221710`,
`005CD4F0`, `002204A0`.
## SWE2-EC7-31 update (2026-09-18) — `002181A0` intrusive-list splice

`002181A0` (192 B) is the list-assign the bank code runs: a
self-assign (`rcx == rdx`) returns immediately; otherwise the
two chains are walked pairwise, each source node's `+0x10` value
copied onto its destination peer until either list ends. A
destination with leftovers has each remaining node unlinked —
`[rdx.next].prev = [rdx].prev`, `[rdx.prev].next = [rdx].next` —
and freed through the allocator deleter
`call qword[[[rdi+0x10]]+0x18]` on `rdi+0x10`; a source with
leftovers falls into `00217B10`, the insert-copy arm. The list
head comes back in `rax`. Interior anchor `0021821A` (the `call
qword[rax+0x18]` deleter).
## SWE2-EC7-32 update (2026-09-18) — `00217F10` `P%`-class ctor

`00217F10` (180 B) is the constructor the bank's record builders
reach: the `009078B0` vtable (the `"P%"`-family class) is planted,
`+8`/`+0x10` zeroed, `001EDF00(obj+0x18, src+0x18)` copies the
string member, the `+8` chain self-links, `00217B10` runs the list
init against `src+8`, and `+0x20`/`+0x28`/`+0x2C`/`+0x30`/`+0x34`
copy through from the source. Interior anchor `00217F80` (the
`call 00217B10` list init).

## SWE2-EC7-41 update (2026-09-19) - `00222740`

`00222740` (345 B) is the `.win.mab` bank-path builder the page names - `00908930`/`00908940`/`01E027D8`/`01F44830`, `"%s%03d%s"`/`".win.mab"` strings, `00221710`/`00220C70`/`0016D6A0` pair/`00861EC0`/`0017D2E0`/`00225C40`/`00221D10`. Interior anchor `00222771` (a `00221710` call).

## SWE2-EC7-43 update (2026-09-19) - `002238F0`

`002238F0` (292 B) is the `SebAudioBank` slot-6 row body - `009089BC`, `00225680`/`00225690`/`002256A0`/`002257E0`/`007A84A0`. Interior anchor `00223950` (a `00225680` call).

## SWE2-EC7-44 update (2026-09-19) - `00224180`

`00224180` (266 B) is the `SebAudioBank` slot-3 re-dispatch body - `0016D6A0`/`00225680`/`00225690`/`002256A0` plus a `call [rax+0x48]` vcall. Interior anchor `002241C0` (an `0016D6A0` call).

## SWE2-EC7-44 update (2026-09-19) - `00223FA0`

`00223FA0` (258 B) is the `SebAudioBank` slot-4 re-dispatch body - `0016D6A0`/`00225680`/`00225690`/`002256A0` plus a `call [rax+0x48]` vcall. Interior anchor `00223FE0` (an `0016D6A0` call).

## SWE2-EC7-46 update (2026-09-19) - `00222080`

`00222080` (228 B) is the audio-bank teardown base `00222000` family body - `007A84A0` plus `call [rax+0x10]`/`call [rax+0x18]` vcalls. Interior anchor `002220CF` (the `007A84A0` call).

## SWE2-EC7-50 update (2026-09-19) - `00224B30`

`00224B30` (181 B) is the `SebAudioBank` slot-10 manager-gated replay - `00210930`/`00210B30`/`002240B0`/`00224290`/`00224470`. Interior anchor `00224B40` (a `00210930` call).

## SWE2-EC7-58 update (2026-09-19) - `00223A20`

`00223A20` (170 B) is an audio-bank body - `0016D6D0`/`001AF2B0`/`002211A0`/`00221710` plus one vcall. Interior anchor `00223A40` (a `00221710` call).

## SWE2-EC7-59 update (2026-09-19) - `00212860`

`00212860` (164 B) is the `+0x8`-walker the audio-bank page names - `00221FB0` single call plus three vcalls, `+0x2C`/`+0x30` zero gates. Interior anchor `00212899` (a `00221FB0` call).


## SWE2-EC7-59 update (2026-09-19) - `00219D80`

`00219D80` (161 B) is the `+0x60` map erase the audio-bank page names - `0016D6D0`/`0016DA60`/`00199DB0` plus one vcall. Interior anchor `00219DE1` (a `00199DB0` call).



## SWE2-EC7-64 update (2026-09-19) - `00222170`

`00222170` (139 B) is a `+0x60` map-erase body - `0016D6A0`/`00221ED0`/`00225680`. Interior anchor `002221AC` (a `0016D6A0` call).



## SWE2-EC7-64 update (2026-09-19) - `00217B10`

`00217B10` (138 B) is an indirect-only insert-copy arm - `call [rax+0x10]` per element, `rsi` cursor, `[rax+0x10]` next test. Interior anchor `00217B4D` (the `call [rax+0x10]` site).



## SWE2-EC7-66 update (2026-09-19) - `00222D30`

`00222D30` (131 B) is the `SepAudioBank` body - `00221E60`/`002224F0`/`002225B0`/`00225680` (state 1 + `+0x49 & 0x40` gate). Interior anchor `00222D51` (a `00221E60` call).


## SWE2-EC7-68 update (2026-09-19) - `00221D10` voice-object lazy accessor measured

`00221D10` (70 B) is the lazy voice/handle accessor the page names:
`[rcx+0x20]` is returned when live; otherwise `00221710(rcx)`
fetches the bank context, `00220CE0` constructs the object,
`0016D6A0(obj != 0)` records the publish, and the result is stored
to `+0x20` before returning. Interior anchor `00221D2F` (the
`00220CE0` call).

## SWE2-EC7-108 update (2026-09-20) - `00222700` + `00221ED0` measured

`00222700` (52 B) is the bank
ctor `002182A0`, `00218380`,
`00218E80` and the `00899E10` /
`00899E50` allocators run:
`00907910` onto `[rcx]`,
`00907860` onto `[+0x40]` (the
secondary base), `007A90A0(+0x38)`
for the member-string init, then
tail `00221870(rcx)` - the
two-vtable construction the bank
family shares.
Interior anchor `00222722` (the
`007A90A0` call).

`00221ED0` (108 B) is the
`00879750`-keyed list find
`00222170` and `00225000` call
(11 edge callers total): from the
`rcx + 8` sentinel it walks
`[+8]`-linked nodes, runs
`00879750([node + 0x10])` and
returns that payload when it
equals `edx`, else 0 - the
callback-keyed lookup the bank
lists share.
Interior anchor `00221F0F` (the
`00879750` call).

## SWE2-EC7-109 update (2026-09-20) - `002120E0` measured

`002120E0` (79 B) is the
lock-guarded getter `00222DC0`
and `00223AD0` call:
`005CD4F0(rcx + 0x130)` takes
the object's critical section,
`001BA860(rcx + 0x70)` runs the
real query, `005CD820` releases,
and the inner answer returns in
`rax` - the bounded read the
bank/controller pages share.
Interior anchor `00212110` (the
`001BA860` call).

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-audio-bank-and-controller-family-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0021B2F0` | 91 B | walks the circular list headed at `rcx+8` (next link at node qword `+0`) and for each node calls `00222170(qword node+0x10, edx)`; returns `al` = 1 at the first non-zero result, else 0 once the walk returns to the head | `0021B309`, `0021B316`, `0021B31D`, `0021B322`, `0021B33E` |
| `00222B20` | 70 B | calls `007A7010(rcx+0x38)` with the other incoming registers and, only when it returns non-zero, calls `007A81F0(rcx+0x38, (float)r8d / 127.0, 0.0, -1)` | `00222B34`, `00222B3B`, `00222B4E`, `00222B56` |
| `00223320` | 110 B | when `edx` is non-zero calls `00221ED0` with the incoming registers and, when that returns an object for which `00225680(object)` is non-zero, calls `002257E0(object, r9d, 0)` and returns `al` = 1; when `edx` is 0 and dword `+0x38` of `rcx` equals `r8d` it calls `002224F0(rcx, r9d, 0)` and returns 1; every other path returns 0 | `0022332D`, `00223331`, `00223352`, `00223364`, `0022336F` |
| `00223390` | 122 B | when `edx` is non-zero calls `00221ED0` with the incoming registers and, when that returns an object for which `00225680(object)` is non-zero, calls `007A84A0(object+8, (float)r9d / 60.0, -1)` and returns `al` = 1; when `edx` is 0 and dword `+0x38` of `rcx` equals `r8d` it calls `002225B0(rcx, r9d)` and returns 1; every other path returns 0 | `0022339D`, `002233A1`, `002233C9`, `002233E3`, `002233EB` |
| `00223410` | 114 B | when `edx` is non-zero calls `00221ED0` with the incoming registers and, when that returns an object for which `00225680(object)` is non-zero, calls `002257E0(object, the fifth (stack) argument, r9d)` and returns `al` = 1; when `edx` is 0 and dword `+0x38` of `rcx` equals `r8d` it calls `002224F0(rcx, the fifth argument, r9d)` and returns 1; every other path returns 0 | `0022341D`, `00223421`, `00223444`, `00223456`, `00223463` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-audio-bank-and-controller-family-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0021C680` | 214 B | Walks the circular list headed at `rcx+8` for the first node whose object (`[node+0x10]`) has dword `+0x3C` equal to `edx`, calls `002129F0` with a stack out-dword and 8, and when that out-dword is not greater than zero (signed `jle`) or `r9` is null calls `00212A70` with the `002129F0` result; otherwise it takes the found node's object after calling `00225030` on it with `edx`=-1, or with no match the object returned by the owner's vtable slot `+0x30`, calls `00212A70` the same way when that object is null, and else calls `00224DC0` with the object, `edx`, `r8d`, `r9`, the fifth and sixth arguments and the `002129F0` result; every path returns the out-dword. | `0021C6B4`, `0021C6CB`, `0021C6ED`, `0021C6FA`, `0021C72A` |
| `002204A0` | 161 B | Returns 0 when the dword at `rcx+0x48` is zero (unsigned `jbe`); otherwise it takes the node at `rcx+0x30`, saves the node's qword `+0x20`, decrements `rcx+0x48`, calls `0016D6D0` on the node and `0016DA60` with the node and `rcx+0x28`, calls vtable slot `+0x18` of the object at `rcx+0x50` with the node and 0x28, calls `00199DB0` with `rcx+0x58`, a stack out-slot, the address of the saved qword and its low byte, and returns the result of `00225490` on the saved qword, or 0 when that qword is null. | `002204C0`, `002204CF`, `002204F6`, `0022050D`, `0022051F` |
| `0036E9F0` | 192 B | Picks a 0x18-byte record (a null pointer when `ecx` is -1, otherwise entry `ecx & 0xF` of the table at `022D9AB0` when `ecx & 0xF0` is zero or of the table at `022D9AE0` when it is not), calls `0036A0B0` with the record's dword `+0x10` and `0036C100` on that result, then calls `002DF450` with the record's signed byte `+1` (plus 2 when byte `+2` is non-zero), its signed word `+0x14`, the `0036A0B0` result, the `0036C100` result and 0, and stores the return to dword `+8`; when that return is zero it calls `00369800` with dword `+0x10`, clears `+0x10` and sets byte `+0` to 3, and when it is non-zero it sets byte `+0` to 3 only if dword `+4` is non-zero; it then returns. | `0036EA14`, `0036EA3A`, `0036EA6F`, `0036EA89`, `0036EA96` |
| `007A7010` | 474 B | Reads the qword handle at `[rcx]` and returns 0 when it is zero; by its low byte it picks a lock-getter and lookup pair (7: `007BC2A0`/`007BC2B0`; 2: `007B44B0`/`007B44C0`; 8: `007B7950`/`007B77E0`; 9: `007B8050`/`007B7FD0`; any other type returns 0), enters the returned lock through the import at `008C20B8`, looks the handle up from a stack copy and reads a state from the found object (vtable slot `+0x10` for type 7, slot `+0xA8` for the others, 0 when the lookup returns null), leaves the lock through the import at `008C20C0`, and returns a code: for type 7 the state itself when it is 0, 1 or 3 and 2 for any other value; for types 2, 8 and 9, 0 for state 0, 1 for state 1, 3 for state 4 and 2 otherwise. | `007A7034`, `007A707C`, `007A70EF`, `007A71A8`, `007A71C9` |
| `007A81F0` | 268 B | Returns 0x82000000 when the qword handle at `[rcx]` is zero and -1 when its low byte is not 2, 7, 8 or 9; for type 7 it obtains a command record through `007BAD60` and for types 2, 8 and 9 through `007AB460`, returning that call's result when it is negative (signed `js`), writes the command code (0xD for type 7, 0xE otherwise), the handle at `+8`, the float `xmm1` at `+0x10` and the float `xmm2` at `+0x14` (plus `r9d` at `+0x18` for the 0xE command), submits it with `007BAE50` or `007AB550` and returns that result, every path ending with the stack-cookie check (cookie from `01F44830`) through `00808C40`. | `007A8227`, `007A8258`, `007A8283`, `007A82CD`, `007A82D5` |
| `007C8370` | 208 B | Returns -1 unless the dword at `rcx+0xC8` is 1; otherwise it clears the qword at `rcx+0x1C8`, calls `007CA560` on the sub-object at `rcx+0x190` with the incoming `edx` and `r8`, `r9`=0, `xmm1`=1.0 (from `01CEBBA8`), `xmm2` = the incoming `xmm3` and a zero byte argument, stores the fifth (double) argument to `+0xD8`, `edx` to `+0x638`, `r8d` to `+0x700` and `+0x704` and zero to `+0xD4` and `+0x708`, then calls `007C2280` and, when that returns `al`=0, sets `+0xC8` to 2 and returns 0, else tail-jumps to `007C36C0` with `xmm1`=0. | `007C83BD`, `007C83C5`, `007C8401`, `007C840A`, `007C843B` |

### Crossings into other layers - functions this page's newest interior rows name (OPUS, 2026-10-03)

- **Script VM / native bridge - SERVICE (1 edge).** `00369800` is also reached from `0050DDA0`, a 23-byte body filed to the script VM / native bridge that tail-jumps to it (`0050DDB2 jmp 00369800`) - shared machinery across the layer boundary, no shared ownership.
- **World area / field - SERVICE (1 edge).** `0036C100` is also called by `00378BC0` (940 B), filed to world area (`00378CD5`) - shared machinery across the layer boundary, no shared ownership.
