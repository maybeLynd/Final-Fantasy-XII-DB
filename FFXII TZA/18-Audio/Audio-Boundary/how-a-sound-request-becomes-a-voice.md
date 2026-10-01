---
system: How a sound request becomes a voice — the play call, the two dials, and the bank split
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-how-a-sound-request-becomes-a-voice-pass-1
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
  falsification_passes: 1
  last_falsification: 2026-09-03
  last_falsification_by: repos-9e
  last_falsification_state: GN158 checkpoint, project GFZ_H9E
  falsification_result: 10 overturned (3 census + 7 body sizes), 11 survived, 2 gate findings dispositioned as false positives - see section 10
---

# How a sound request becomes a voice

> The complete path from "play sound 37" to a running voice at a chosen volume and position —
> including what the two mystery constants `0x40` and `0x7F` actually are.

## 1. What the player sees

When you move the cursor in the Battle Menu, land a hit, or open a chest, some piece of game
logic asks for a sound by a small number — the numbers in the shipped code run from about 10 to
108. Those numbers are not absolute. They are **slot numbers inside whichever sound-effect bank
is loaded right now**, which is why the same request makes a different noise in a different
area, and why an area that failed to load its bank makes no noise at all instead of the wrong one.

Two settings travel with every one of those requests, and in **the four convenience wrappers** they
are always the same pair: **full loudness, and dead ahead** *(scope corrected 2026-09-12 — the script
verb `sebsoundplay_2c1` passes its own pair; §2)*. They are not defaults the sound system
supplies — the game passes them explicitly, every time, and they happen to be exactly the values
a fresh voice is reset to. That is why ordinary interface and event sounds are never quieter than
each other and never come from one side: nothing in this path ever asks for anything else. A mod
that wants a positional or a quieter sound has to reach past these wrappers — and the shipped game
already does, through that script verb.

Sound is organised into five kinds of **bank** — music, two flavours of sound-effect bank, battle
shouts, and streamed audio. Music is handled by a completely separate set of controls from the
other four: it has its own current-track number and its own loudness setting, and it cannot be
reached by the ordinary "play sound N" request at all. That separation is why music keeps playing
through things that silence effects, and why stopping music takes a different action than stopping
a sound.

Four separate things can stop a sound before it starts, and **not one of them tells the caller
which** — they only report that it failed:

- **A single global switch.** One value, written from exactly one place in the engine, and that
  place is reachable from the game's own event scripts. When it is set, requests **through three of
  the four wrappers** are abandoned before the game even looks the sound up — the ungated wrapper
  `00271500` and the script verb do not check it (corrected 2026-09-12).
- **A second, independent switch** inside the shared play call, flipped during certain loads and
  transitions.
- **A "the world isn't live" rule.** The most-used request refuses even to *look up* a sound while
  the actor/field runtime for the world is not running or is held. Its sibling request skips that
  check — that one check is the entire difference between the two — and it is why a sound fired
  during a transition can silently never happen.
- **No loaded bank owning that sound.** The request survives all three switches, and then nothing
  is found to play it.

Finally, a trap worth knowing before you debug anything here: the caller gets a receipt number
back, and **a receipt is issued even when no bank matched and nothing was started**. Getting a
handle does not mean a sound is playing.

## 2. Native mechanism

### The request wrapper

> **SCOPE CORRECTED 2026-09-12 (OPUS-CONTRA-FABLE-SOUND-REQUEST-SCOPE, re-derived by FABLE from the
> bodies).** This page read **two** wrappers over **two** resolvers on **one** handle and concluded that
> every request carries `(0x40, 0x7F)`. The image has more, and the conclusion was an artefact of the
> sweep, not a deliberate boundary. What stands: every function the page read is read correctly —
> `globalSoundId = bankSlot × 512 + localIndex`, the liveness precondition as the only difference
> between `003A1180` and `003A11F0`, and `(0x40, 0x7F)` = (pan, volume). What was missing:
>
> | entry | gate `02091098` | resolver | play |
> |---|---|---|---|
> | `00249C60` | yes | `003A1180` (live) | `002DF220(id, 0x40, 0x7F)` |
> | `00249CA0` | yes | `003A11F0` (no live test) | same |
> | **`00271500`** (42 B) | **no** — the `00249C60` shape with the gate deleted | `003A1180` | same |
> | **`0024A1A0`** (46 B) | yes | none — takes a raw id | `002DEE80(id)` then `002DF0F0(id, 0)`: not a play (§7) |
> | **script verb `sebsoundplay_2c1`** (`0x02C1`, handler `00357040`) | **no** | chosen by operand 1: `1` → `003A1100`, `2` → `003A1070`, else `003A1180` | `002DF220(id, operand 3, operand 4)` — **script-chosen pan and volume** — unless `00267310` for the actor's manager is set (`003570B0`–`003570C8`) |
>
> **~~Four~~ FIVE resolvers over three handles** (*corrected 2026-09-12 by the contract's falsification pass — `003A1240` is a fifth, and takes its handle as a PARAMETER, which is why a census anchored on the three handle globals returns four*), all against the one table at `02AEEDC0` with the same `×512`
> arithmetic: `003A1180` / `003A11F0` read `02AEF3FC`; `003A1100` reads `02AEF400` (live-gated);
> `003A1070` **tests `02AEF400 != −1` and then resolves through `02AEF404`** (`003A1076`, `003A1095`) — a
> cross-handle dependency whose reason is not read. **The handles are three sound banks loaded once at
> boot**: `003A13F0` (called from `00266D10`) requests files `(0x20, 0)`, `(0x20, 1)` and `(0x20, 3)`
> through `002ED8C0`, each into an arena buffer and an asynchronous read whose completion callback sets
> one handle — `003A1390` → `02AEF3FC`, `003A1330` → `02AEF400`, `003A12D0` → `02AEF404`
> (`003A14E9`, `003A1568`, `003A15E7`); it first resets all three to `−1`. The file names behind
> namespace `0x20` are not resolved here. So `(0x40, 0x7F)` is a property of the **four wrappers**, not
> of the path, and `02091098` is not a master mute: `00271500` and the script verb never read it.

The most-called audio entry point in the game is `00249C60` — **100** distinct non-Audio callers and
none inside Audio. *(§10: 99 until a byte-level decode found a caller `edges.tsv` omits.)* It takes **one argument**: the sound's index within the current bank. The
complete body, in machine terms:

```
00249C60  sub  rsp, 0x28
          cmp  dword [0x02091098], 0        ; global gate
          jne  fail
          call 0x003A1180                   ; resolve; ECX untouched -> the caller's own arg 1
          cmp  eax, -1
          je   fail
          mov  edx, 0x40                    ; pan  = 64
          mov  ecx, eax                     ; id
          lea  r8d, [rdx + 0x3f]            ; volume = 0x40 + 0x3F = 0x7F = 127
          add  rsp, 0x28
          jmp  0x002DF220                   ; tail call: the play call's result IS ours
fail:     or   eax, -1                      ; 0xFFFFFFFF
          ret
```

Two details the decompiled C loses. First, `ECX` is never written before the `call`, so the
caller's first argument passes straight through into the resolver — **`00249C60` is not a nullary
function**. Second, `lea r8d,[rdx+0x3f]` is the compiler building `0x7F` out of `0x40`; the two
constants are related only by that peephole, not by meaning.

`00249CA0` is the same 51 bytes with `003A11F0` as the resolver instead. `0024A1A0` is a third
sibling that checks the same global gate and then routes through `002DF0F0` -> `001DBE90` ->
`00210C50` — a *different* controller entry point from the play path's `00210C00`. What `00210C50`
does was not read; see §7.

### Resolving an index into a global sound id

Both resolvers do exactly the same arithmetic against exactly the same two globals — this is the
answer to *what do they resolve against*. There is a 32-bit **bank-slot handle** at `02AEF3FC`
(index in the low 16 bits, a validation key above it) and a **24-byte-per-entry slot table** based
at `02AEEDC8`. The resolver validates the handle against its own table entry, then computes:

```c
slot        = handle & 0xFFFF;                     /* low half indexes the table   */
key         = handle & 0x7FFFFFFF;                 /* bit 31 stripped              */
entryDword  = (u16)[base + slot*24 + 2] << 16 | (u16)[base + slot*24];
if (handle == 0xFFFFFFFF || entryDword != key) return -1;
return (u32)(u16)[base + slot*24] * 512 + localIndex;
```

Because the equality test forces `entry[+0] == slot`, that last line is simply:

**`globalSoundId = bankSlot * 512 + localIndex`** — every loaded bank owns a 512-entry block of
the global id space. That is the whole reason the argument is a small number: it is an offset
inside the current bank's 512 slots.

The **only** difference between `003A1180` and `003A11F0` is a precondition. `003A1180` first calls
`00267330(0)` and bails with `-1` if it returns non-zero; `003A11F0` does not. `00267330(i)` reads
a flag byte in the ActorManager slot array (`02098E20`, stride `0x288`) and answers "is slot *i*
live and not held". So `00249C60` will not even look a sound up while the world runtime is down or
suspended; `00249CA0` will. That is the real reason there is a family of near-identical wrappers,
and it is not about "resolving against different things".

`003A1180` also contains a **provably dead branch**: `test edx,edx / js` on a value that was just
zero-extended from 16 bits can never be negative. It is defensive code that never fires.

### The play call — and what `0x40` and `0x7F` are

`002DF220(id, p2, p3)` is 92 bytes and does three things: refuse `-1`, consult a second gate, and
forward with the arguments reshaped. The reshaping is the evidence:

```
002DF220  cmp  ecx, -1        -> return 0
          call 0x003603C0     ; second gate: movsx eax, byte [0x022CB726]
          test eax, eax
          jne  return 0
          and  edi, 0x7f      ; p3 masked to 7 bits   -> 0..127
          movzx r8d, sil      ; p2 truncated to 8 bits -> 0..255
          btr  ebx, 0x1f      ; id: bit 31 cleared
          mov  r9d, edi
          mov  edx, ebx
          xor  ecx, ecx       ; selector = 0, hardcoded
          jmp  0x001DBDB0
```

**The two constants are not the same kind of value, and the masks prove it before anything else
does.** `p3` is masked to seven bits — twice, here and again downstream. `p2` is only truncated to
a byte and is never masked to seven bits anywhere on the path. A field that is deliberately allowed
the full 0–255 range is not a companion to a 0–127 field.

Following them to where they are consumed settles it. After the dispatcher and the bank lookup,
`00224570` makes two calls on the newly-acquired voice:

- `002256F0(voice, p2, 0)` — writes `voice+0x20` and sets a **pan** through the driver.
- `002257E0(voice, p3, 0)` — writes `voice+0x1C` and sets a **volume** through the driver.

And `002256B0`, the voice reset, writes those same two fields with those same two literals:

```
002256B0  mov dword [rcx+0x1C], 0x7F      ; volume default = 127
          mov dword [rcx+0x20], 0x40      ; pan    default = 64
```

So `(0x40, 0x7F)` is **(pan = 64, volume = 127)** — literally the voice's own reset values, passed
back in explicitly by the wrapper family. Volume 127 is full scale in a 0–127 field. Pan 64 is the
centre of a **0–255** field, not a 0–127 one: the setter branches at `0x80`, mapping `0x00..0x7F`
to one axis and `0x80..0xFF` to the mirrored axis, and 64 lands on offset zero — dead ahead. The
exact formulas are in §4.

### The dispatcher and the bank split

`001DBDB0(selector, id, pan, volume)` fetches the audio singleton (`00210B30`, lazily constructed by
`00210AF0` from a 64-byte allocation) and hands off to `00210C00`, which is the fork in the road.

**The singleton is not one controller — it is a registry of five, one per bank class.** `002105E0`
heap-allocates and constructs five objects and stores their pointers in the first five slots. Each
derives from `AudioController` (each constructor calls the base `00212710`, then stamps its own
vftable), and each is named by real RTTI:

| slot | constructor | class | pool constant |
|---|---|---|---:|
| `+0x00` | `00217FD0` | `MusicAudioController` | 2 |
| `+0x08` | `0021A9F0` | `SebAudioController` | 0x60 (96) |
| `+0x10` | `00219400` | `SepAudioController` | 0x100 (256) |
| `+0x18` | `0021CC10` | `StreamAudioController` | 4 |
| `+0x20` | `0021BDB0` | `ShoutAudioController` | 6 |

So the fork is not "two lists of one controller" — it is **a choice between the Seb and the Sep
bank managers**:

```
00210C00  mov   eax, r8d               ; id
          movzx r8d, r9b               ; pan, byte
          mov   r9d, [rsp+0x28]
          and   r9d, 0x7f              ; volume, 7 bits
          test  edx, edx               ; selector
          mov   edx, eax
          jne   .sep
          mov   rcx, [rcx+8]           ; -> SebAudioController
          jmp   0x0021B5B0
.sep:     mov   rcx, [rcx+0x10]        ; -> SepAudioController
          jmp   0x00219EA0
```

Both branches carry all four values — a point the decompiler gets wrong, rendering the first branch
as a one-argument call that drops the sound id. Read from the machine code, nothing is dropped.

The selector is not free. `002DEF40` and `002DF010` compute it as `~(id >> 31) & 1`, so **bit 31 of
the id chooses the backend**; `002DF220` hardcodes it to `0`, which is the `0021B5B0` side. And
`003A0E20` shows a second flag bit: if **bit 30** is set it abandons this path entirely and calls
`002DF4D0((id >> 8) & 0xFF, id & 0xFF, …)`, a completely different two-byte id encoding.

The two sides then find the bank differently, and this is where the 512 comes back:

- `0021B5B0` walks an intrusive list and matches `bank[+0x3C] == id / 512` — **the exact inverse of
  the resolver's `slot*512 + local`**.
- `00219EA0` matches `bank[+0x38] == id` — the whole id, no division — and checks the bank's
  load-state field `bank[+0x30] == 2` first.

Whichever matches, `00212950` has already issued the receipt: a 31-bit counter that increments,
wraps, and skips zero. It is issued **before** the list walk and returned **whether or not the walk
finds anything**, so a handle proves a request was made, never that a voice exists.

### The five bank classes

The image ships genuine MSVC RTTI for this hierarchy, and the base constructor `00221780(this,
kind)` stamps the kind into `+0x34`, so the enum is recoverable exactly:

| kind | class | vftable | constructor |
|---:|---|---|---|
| 1 | `MusicAudioBank` | `00907910` | `002226A0` |
| 2 | `SebAudioBank` | `00907D80` | `002235F0` |
| 4 | `SepAudioBank` | `00907B48` | `00222CB0` |
| 6 | `StreamAudioBank` | `009081A0` | `00225160` |
| 8 | `ShoutAudioBank` | `00907F90` | `00224BF0` |

Of the five, the one whose container format is visible is `SepAudioBank`: `002DF070` walks
16-byte-aligned chunks whose magic is the authored 5-byte string **`SeSep`** at `00917290`.

The odd one out is `MusicAudioBank`, and it explains the whole `0215EFxx` block. Every other
subclass constructor writes `-1` into the qword at `+0x38`, initialising the two match keys
`+0x38` and `+0x3C` that the two lookups read. `MusicAudioBank` instead constructs an
`SQEX::Sd::Driver::MusicCallback` sub-object there. **A music bank therefore has no match key and
cannot be found by either lookup** — which is exactly why music is driven by a separate command
block (a current-track handle at `0215EF44` and a 0–127 level at `0215EF4D`) rather than by the
play call.

### The music block, and why music is not on this path

The `MusicAudioController` in slot `+0x00` is never selected by `00210C00` — the fork only ever
picks `+0x08` or `+0x10`. Music is driven instead by a small block of globals in the `0215EFxx`
range, whose complete initial state is set by `002DE360`:

```c
DAT_0215EFD8 = 0;            /* group mask                */
DAT_0215EF4C = 0;
DAT_0215EF48 = 0;
for (i = 0; i < 0x10; i++) {                 /* 16 registration slots at 0215EF50, 8 bytes each */
    *(u16 *)(0x0215EF50 + i*8)     = 0;      /* flags; the byte at +1 is the sticky flag  */
    *(u8  *)(0x0215EF52 + i*8)     = i;      /* the slot's own index                      */
    *(u16 *)(0x0215EF54 + i*8)     = 0xFFFF; /* key: 0xFFFF = free                        */
    *(u16 *)(0x0215EF56 + i*8)     = 0;      /* refcount                                  */
}
DAT_0215EF4D = 0;            /* level, 0..127             */
DAT_0215EF44 = 0xFFFFFFFF;   /* current track: none       */
DAT_0215EF4E = 1;
```

That initialiser is what makes the two names honest rather than inferred: `0215EF44` starts at
`-1` and every accessor treats `-1` as "none", so it is a **current-track handle**, not a general
state word; and `0215EF4D` is a 0–127 **level**, initialised to 0 and set to `0x7F` by every
track-switch path before it hands over. The switch family (`002DEC30`, `002DEC80`, `002DECE0`,
`002DED30`, `002DED70`, `002DEDB0`) all end with `DAT_0215EF44 = newTrack`, and the ones that
cross-fade first restore the **outgoing** track to full level:

```c
if (newTrack >= 0 || DAT_0215EF44 >= 0) {
    DAT_0215EF4D = 0x7F;
    Music_SetLevel(newTrack >= 0 ? newTrack : DAT_0215EF44, 0x7F);
}
```

`001DBC70` and `001DBCA0`, the forward targets of that family, go to `00210A40`/`00210A50`, which
dereference slot **`+0x00`** — the `MusicAudioController`. So music has its own controller, its own
current-track handle and its own level, and the play call cannot reach any of them. A modder
silencing sound effects through `02091098` will not touch the music, and that is why.

### Where the two gates come from

`02091098` — the global gate — has, across the whole image, **one writer and three readers**. The
writer is `00249FC0`, a 7-byte store. One of its three callers is `00512080`, a
`Script_VM_Native_Bridge` function that pops an integer off the VM value stack and passes it
straight in: the game's authored event scripts can open and close the audio gate. `002D6F90` closes
it (writes `0`) as part of a larger state transition.

`022CB726` — the second gate, inside `002DF220` — is read only by `003603C0` and written by three
functions: `00360110` (to `0`), `003601D0` (to `1`), and `00360370`, a block reset that clears it
alongside five neighbouring bytes and writes `0x5A` at `022CB724`.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00249C60` | `Audio_RequestSound_WorldLiveResolve` | 51 B | the most-called audio entry point; takes a bank-local index; global gate → resolve (world-live) → tail-call play |
| `00249CA0` | `Audio_RequestSound_PlainResolve` | 51 B | **the same global gate**; differs only in using the resolver that skips the world-live check |
| `0024A1A0` | `Audio_GatedRequest_AltDispatch` | 46 B | same global gate; requires `002DEE80(x) != 0`, then `002DF0F0(x, 0)` → `00210C50`, not the play path |
| `00249FC0` | `Audio_SetGlobalRequestGate` | 7 B | **the only writer** of `02091098` |
| `00512080` | `ScriptVM_SetAudioRequestGate` | 44 B | pops an int off the VM stack into `00249FC0` — authored-script control of the gate |
| `003A1180` | `Audio_ResolveBankLocalId_WorldLive` | 111 B | `bankSlot*512 + local`, refused unless `00267330(0) == 0` |
| `003A11F0` | `Audio_ResolveBankLocalId` | 79 B | the same arithmetic with no precondition |
| `003A0E20` | `Audio_PlayByEncodedId` | 41 B | routes on **bit 30** to a two-byte id encoding |
| `003A1390` | `Audio_SelectBankSlot` | 83 B | sets the active bank-slot handle `02AEF3FC` |
| `003A13F0` | `Audio_ReleaseBankSlots` | 582 B | invalidates `02AEF3FC` to `0xFFFFFFFF` |
| `00267330` | `ActorSlot_IsLiveAndUnheld` | 39 B | reads the ActorManager slot flag byte; the world-live precondition |
| `002671F0` | `ActorSlot_IsLive` | 25 B | bit 0 only |
| `00267360` | `ActorSlot_IsLiveAndUnheld2` | 50 B | bit 0, plus bit 7 or the neighbouring byte's bit 0 |
| `002DF220` | `Audio_PlayResolvedSound` | 92 B | the shared play call; second gate, masks, hardcoded selector 0 |
| `002DEF40` | `Audio_PlayResolvedSound_BitSelector` | 95 B | same, but derives the selector from **bit 31** of the id |
| `002DF010` | `Audio_PlayResolvedSound_PanOnly` | 61 B | same shape, passes only `0x40` |
| `003603C0` | `Audio_ReadSecondGate` | 8 B | `movsx eax, byte [022CB726]` |
| `00360110` | `Audio_OpenSecondGate` | 8 B | writes `0` |
| `00360370` | `Audio_ResetGateBlock` | 52 B | clears the gate and five neighbours, writes `0x5A` at `022CB724` |
| `001DBDB0` | `AudioController_Dispatch` | 76 B | singleton fetch + forward |
| `00210B30` | `AudioRegistry_Get` | 33 B | returns the singleton `01FD36A0` |
| `00210AF0` | `AudioRegistry_EnsureCreated` | 64 B | lazy construction from a 64-byte allocation |
| `00210C00` | `AudioRegistry_RouteBySelector` | 40 B | the fork: `+0x08` Seb → `0021B5B0`, `+0x10` Sep → `00219EA0` |
| `0021B5B0` | `SebController_PlayByBankBlock` | 138 B | matches `bank[+0x3C] == id / 512` |
| `00219EA0` | `SepController_PlayByWholeId` | 157 B | matches `bank[+0x38] == id`, requires load-state `2` |
| `00212950` | `Audio_AllocatePlayHandle` | 28 B | the receipt: 31-bit counter, wraps, skips zero |
| `00224540` | `AudioBank_StartVoice_Thunk` | 36 B | pads the argument frame with `0, NULL` |
| `00223160` | `AudioBank_StartVoiceStream_Thunk` | 36 B | the same for the stream side |
| `00224570` | `AudioBank_StartVoice` | 763 B | the real voice-start; spins on load-state 1, RB-tree lookup by `id % 512`, applies pan then volume |
| `00223190` | `AudioBank_StartVoiceStream` | 356 B | the stream-side counterpart |
| `002256F0` | `Voice_SetPan` | 197 B | **the pan setter** — see §4 for the exact formula |
| `002257E0` | `Voice_SetVolume` | 76 B | **the volume setter** — clamped 0..127, normalised by 127.0 |
| `002256B0` | `Voice_ResetToDefaults` | 44 B | writes volume `0x7F` and pan `0x40` — the corroborating body |
| `00221780` | `AudioBank_ctor` | 135 B | base constructor; stamps the kind at `+0x34` |
| `002105E0` | `AudioRegistry_ctor` | 231 B | constructs the five per-class controllers into slots `+0x00`..`+0x20` |
| `00212710` | `AudioController_ctor` | 78 B | the base every per-class controller derives from; one EASTL list at `+0x08`/`+0x10` |
| `00217FD0` | `MusicAudioController_ctor` | 62 B | slot `+0x00`; pool constant 2 |
| `0021A9F0` | `SebAudioController_ctor` | 97 B | slot `+0x08`; pool constant 0x60 |
| `00219400` | `SepAudioController_ctor` | 97 B | slot `+0x10`; pool constant 0x100 |
| `0021CC10` | `StreamAudioController_ctor` | 62 B | slot `+0x18`; pool constant 4 |
| `0021BDB0` | `ShoutAudioController_ctor` | 62 B | slot `+0x20`; pool constant 6 |
| `002226A0` | `MusicAudioBank_ctor` | 87 B | kind 1; puts a `MusicCallback` where the match keys would be |
| `00222CB0` | `SepAudioBank_ctor` | 63 B | kind 4 |
| `002235F0` | `SebAudioBank_ctor` | 177 B | kind 2 |
| `00224BF0` | `ShoutAudioBank_ctor` | 64 B | kind 8 |
| `00225160` | `StreamAudioBank_ctor` | 54 B | kind 6 |
| `002DEC00` | `Music_GetCurrentTrackHandle` | 7 B | reads `0215EF44`; 12 non-Audio callers |
| `002DE350` | `Music_GetLevel` | 8 B | reads `0215EF4D`; the only reader |
| `002DECE0` | `Music_SwitchTrack` | 69 B | sets the level to `0x7F` then swaps the track handle |
| `002DEDE0` | `Music_StopTrack` | 80 B | clears `0215EF44` to `-1` when it matches |
| `002DEE30` | `Music_SetLevel` | 26 B | writes `0215EF4D`, guarded by a disjunction |
| `002DEE50` | `Music_SetLevelAndForward` | 27 B | same guard, different forward target |
| `002DEE80` | `Audio_IsRequestRoutable` | 11 B | zero → refuse; used by `0024A1A0` |
| `002DEB40` | `Audio_ReleaseRegistration` | 69 B | ref-counted 16-entry table at `0215EF50` |
| `002DF070` | `SepBank_WalkChunks` | 124 B | the `SeSep` container walk |
| `002DF370` | `Audio_SetGroupMask` | 151 B | set/clear bits of the group mask `0215EFD8` |
| `002DF530` | `Audio_SetMode` | 34 B | clamps its argument to `[0, 2]` |
| `002DF660` | `Audio_PostSequenced` | 30 B | post-increments the sequence counter `0215EFDC` |
| `00360C20` | `AudioTrack_FindSlot` | 80 B | 4-entry, 24-byte-stride table at `022CB9F0` |
| `00360D70` | `AudioTrack_SweepSlots` | 82 B | per-pass sweep; state `5` → stop + release + free |
| `00361200` | `AudioTrack_ScheduleAll` | 306 B | schedules a callback per live slot |
| `00361630` | `AudioTrack_FindOrReserveSlot` | 182 B | find-or-reserve; states `3` then `4` |
| `003D7F30` | `Audio_ReleaseRefCounted` | 190 B | 32-entry, 132-byte-stride table at `02EBBA00` |
| `00221F40` | `AudioBank_FindVoiceByKey` | 108 B | matches `voice[+0x24]` |
| `00225580` | `Voice_SetPlayHandle` | 4 B | writes `voice+0x18` — see the note in §8 |
| `00225680` | `Voice_GetState` | 4 B | reads `voice+0x10` |
| `00225690` | `Voice_GetKey` | 4 B | reads `voice+0x24` |
| `0016D6A0` | `_guard_check_icall` | 3 B | a bare `ret` carrying many folded identities (open question **BA-1**); **not** a control-flow guard at these call sites — see §8 |

Addresses are Ghidra image base `0x00120000`. Body sizes are exact-current body extents from a
`DumpFullCoverageGraph.java` run against the GN checkpoint, reproduced independently in this block.

> **Seven of these were wrong and are corrected — §10.2.** `002105E0`, `00212710`, `00217FD0`,
> `00219400`, `0021A9F0`, `0021BDB0` and `0021CC10` read 196 / 66 / 46 / 66 / 66 / 46 / 46 until
> 2026-09-03. **The provenance sentence above did not hold for those seven rows**, and the error
> underneath them was a false size grouping, not seven slips.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02091098` | global request gate | `u32` | non-zero abandons a request before id resolution; one writer image-wide |
| `022CB726` | second gate | `s8` | non-zero makes `002DF220` return `0` |
| `022CB724` | gate block field | `u32` | set to `0x5A` by the block reset |
| `02AEF3FC` | active bank-slot handle | `u32` | slot index in the low 16 bits; `0xFFFFFFFF` = none |
| `02AEEDC8` | bank-slot table | 24 B/entry | `+0` and `+2` form the validating handle; `+5` marked on select |
| `02098E20` | ActorManager slot flags | `u8`, stride `0x288` | bit 0 = live, bit 7 = held |
| `01FD36A0` | audio registry singleton | pointer | lazily created, 64 bytes; five per-class `AudioController` pointers at `+0x00`..`+0x20` |
| `01FD36B4` | play-handle counter | `u32` | 31-bit, wraps, skips zero |
| `0215EF44` | current music track handle | `s32` | `-1` = none |
| `0215EF4D` | music level | `u8` | 0–127; three writers set it to `0x7F` |
| `0215EF50` | registration table | 16 × 8 B | `+4` key (`0xFFFF` = free), `+6` refcount, `+1` sticky flag |
| `0215EFD8` | group mask | `u32` | bitmask maintained by `002DF370` |
| `0215EFDC` | sequence counter | `u32` | post-incremented by `002DF660` |
| `022CB9F0` | audio track slots | 4 × 24 B | `+0` state, `+1` key, `+2` flags, `+3` handle |
| `02EBBA00` | ref-counted registrations | 32 × 132 B | `+0` kind, `+2` refcount |
| `00917290` | `SeSep` magic | 5-byte string | the `SepAudioBank` container marker |
| `008F6D54` | frame divisor | `f32` | `60.0` |
| `008C5B34` | pan step scale | `f32` | `0.0078125` = 1/128 |
| `00906A44` | volume normaliser | `f32` | `127.0` |
| `01CEBBA8` | pan axis, front | `f32` | `+1.0` |
| `01CEBC9C` | pan axis, rear | `f32` | `-1.0` |
| `009078B0` | `AudioBank` vftable | vftable | base class |
| `00906CD0` | `AudioController` vftable | vftable | the base of the five per-class controllers — **not** the singleton's own class |

## 4. Data structures and formulas

### The request, as the engine actually evaluates it

```c
uint32_t Audio_RequestSound_WorldLiveResolve(int localIndex)   /* 00249C60 */
{
    if (*(int32_t *)0x02091098 != 0)  return 0xFFFFFFFF;   /* global gate closed   */
    int id = Audio_ResolveBankLocalId_WorldLive(localIndex);   /* 003A1180 */
    if (id == -1)                     return 0xFFFFFFFF;   /* not resolvable       */
    return Audio_PlayResolvedSound(id, /*pan*/ 0x40, /*volume*/ 0x7F);  /* tail call */
}
```

### Resolving a bank-local index to a global sound id

```c
int Audio_ResolveBankLocalId(int localIndex)           /* 003A11F0 */
{
    uint32_t handle = *(uint32_t *)0x02AEF3FC;
    if (handle == 0xFFFFFFFF) return -1;

    uint32_t slot = handle & 0xFFFF;                   /* low half indexes the table */
    uint32_t key  = handle & 0x7FFFFFFF;               /* bit 31 stripped            */
    uint16_t lo   = *(uint16_t *)(0x02AEEDC8 + slot*24 + 0);
    uint16_t hi   = *(uint16_t *)(0x02AEEDC8 + slot*24 + 2);
    if ((((uint32_t)hi << 16) | lo) != key) return -1;

    return lo * 512 + localIndex;                      /* == slot * 512 + localIndex */
}
```

`003A1180` is the same function with one extra line at the top:

```c
if (ActorSlot_IsLiveAndUnheld(0) != 0) return -1;      /* 00267330(0) */
```

### The world-live precondition

```c
uint8_t ActorSlot_IsLiveAndUnheld(int i)               /* 00267330 */
{
    uint8_t f = *(uint8_t *)(0x02098E20 + (int64_t)i * 0x288);
    if ((f & 1) == 0) return 1;                        /* not live  -> block        */
    return f >> 7;                                     /* held(bit7) -> block       */
}
/* resolution proceeds only when (f & 0x81) == 0x01 */
```

### The play call

```c
uint32_t Audio_PlayResolvedSound(uint32_t id, uint8_t pan, uint32_t volume)  /* 002DF220 */
{
    if (id == 0xFFFFFFFF)                   return 0;
    if (*(int8_t *)0x022CB726 != 0)         return 0;  /* second gate */
    return AudioController_Dispatch(/*selector*/ 0,
                                    id & 0x7FFFFFFF,
                                    (uint8_t)pan,
                                    volume & 0x7F);
}
```

`002DEF40` differs in exactly one term — the selector is derived rather than fixed:

```c
selector = (~(id >> 31)) & 1;      /* id bit31 set -> 0 (bank-block path)
                                      id bit31 clear -> 1 (whole-id path) */
```

and `003A0E20` intercepts a third encoding before either:

```c
if (id == 0xFFFFFFFF)          return 0;
if ((id >> 30) & 1)            return Audio_002DF4D0((id >> 8) & 0xFF, id & 0xFF, pan, volume);
else                           return Audio_PlayResolvedSound(id, pan, volume);
```

### The bank fork and the 512 split

```c
/* 00210C00 — both branches carry all four values */
pan    = (uint8_t)pan;
volume = volume & 0x7F;
if (selector == 0)  SebController_PlayByBankBlock(reg->seb /* +0x08 */, id, pan, volume);
else                SepController_PlayByWholeId  (reg->sep /* +0x10 */, id, pan, volume);

/* 0021B5B0 — the inverse of the resolver */
bankBlock = id / 512;                                  /* sar edi,9 after the sign fix-up */
for (node = seb->list; node != seb->list; node = node->next)
    if (node->bank->field_3C == bankBlock) { start(node->bank, handle, id, pan, volume); break; }
/* the handle is allocated BEFORE this loop and returned even when no bank matches */

/* 00219EA0 */
for (node = sep->list; node != sep->list; node = node->next)
    if (node->bank->field_38 == id) break;             /* whole id, no division */
/* requires bank->field_30 == 2 */

/* 00224570 — inside the matched bank */
localIndex = id & 0x1FF;                               /* id % 512 */
```

### The play handle (the receipt)

```c
uint32_t Audio_AllocatePlayHandle(void)                /* 00212950 */
{
    uint32_t h = (*(uint32_t *)0x01FD36B4 + 1) & 0x7FFFFFFF;
    if (h == 0) h = 1;                                 /* cmove: never returns 0 */
    *(uint32_t *)0x01FD36B4 = h;
    return h;
}
```

### Pan — `002256F0(voice, pan, fadeFrames)`

```c
float fade = (float)fadeFrames / 60.0f;                /* 008F6D54 = 60.0        */

if (pan < 0x80) { offset = pan - 0x40;   axis = +1.0f; }   /* 01CEBBA8 */
else            { offset = 0xBF - pan;   axis = -1.0f; }   /* 01CEBC9C */

Sd_SetPanMode(voice + 8, 1);                                       /* 007A7E00 */
Sd_SetPanVector(voice + 8,
                (float)offset * 0.0078125,   /* 008C5B34 = 1/128 -> [-0.5, +0.4921875] */
                axis,                          /* +1 front half, -1 rear half            */
                0.0f,
                fade);                                             /* 007A7E90 */
voice->pan /* +0x20 */ = pan;
```

Worked values, so the range is unambiguous:

| `pan` | `offset` | lateral term | axis | meaning |
|---:|---:|---:|---:|---|
| `0x00` | −64 | −0.5 | +1 | one extreme, front half |
| `0x40` | **0** | **0.0** | +1 | **dead ahead — the value this family always passes** |
| `0x7F` | +63 | +0.4921875 | +1 | other extreme, front half |
| `0x80` | +63 | +0.4921875 | −1 | rear half begins |
| `0xFF` | −64 | −0.5 | −1 | rear half extreme |

*Added 2026-09-18 (FABLE): what the driver makes of these.* The lateral term is an angle in half-turns and the axis is the sign of a radial term (UQ-242, answered below): `0x00` is 270 degrees, `0x40` dead ahead, `0x7F` 88.6 degrees; with the axis at -1 the driver adds half a turn, so `0x80` is 268.6 degrees, `0xBF` directly behind and `0xFF` 90. The "meaning" column's two halves are right; the direction of travel within the rear half is the reverse of the front's.

### Volume — `002257E0(voice, volume, fadeFrames)`

```c
int v = (volume < 0) ? 0 : volume;                     /* cmovns */
float fade = (float)fadeFrames / 60.0f;                /* 008F6D54 = 60.0 */
if ((float)v >= 127.0f) v = 0x7F;                      /* 00906A44 = 127.0, cmovae */
voice->volume /* +0x1C */ = v;
Sd_SetVolume(voice + 8, (float)v / 127.0f, fade, 0xFFFFFFFF);      /* 007A81F0 */
```

`0x7F / 127.0f == 1.0f` exactly — full scale, no rounding.

### The voice record

```
Voice
  +0x08  SQEX::Sd sound object   every driver call takes voice+8, never voice
  +0x10  u32  state              002256B0 sets 2; 00225680 reads it
  +0x14  u64  = 0xFFFFFFFFFFFFFFFF on reset (covers +0x14 and +0x18)
  +0x18  u32  playHandle         the receipt; written by 00225580
  +0x1C  u32  volume  0..127     default 0x7F
  +0x20  u32  pan     0..255     default 0x40
  +0x24  u32  key                default 0xFFFFFFFF; read by 00225690, matched by 00221F40
  +0x28  u32  = 0 on reset
  +0x2C  u32  kind               tested by the pan setter's assert
```

### The bank record

```
AudioBank                                    (constructor 00221780)
  +0x00  ptr  vftable            one of the six recovered vftables
  +0x08  ptr  entry list head    EASTL list, allocator named "EASTL list"
  +0x10  ptr  entry list tail
  +0x18  ...  allocator
  +0x20  u64  = 0
  +0x28  u32  = 0xFFFFFFFF
  +0x2C  u8   = 0
  +0x30  u32  load state         1 = loading (00224570 spins with Sleep(0)); 2 = ready
  +0x34  u32  kind               1 Music, 2 Seb, 4 Sep, 6 Stream, 8 Shout
  +0x38  u32  whole-id key       -1 in every non-Music subclass; MusicCallback object in Music
  +0x3C  u32  bank-block key     matched against id / 512
```

### The `SeSep` container walk

```c
size = (length + 15) & ~15;                            /* 16-byte alignment */
while (size > 0x10
       && chunk[0..3] == 'SeSe' && chunk[4] == 'p'
       && (chunk->size & 0x7FFFFFFF) <= size) {
    result = Load(chunk->field_8, chunk + 16);
    size  -= chunk->size & 0x7FFFFFFF;
    chunk  = (char *)chunk + (chunk->size & 0x7FFFFFFF);
    if (size < 0x11) break;
}
```

### The four-slot track table

```
022CB9F0, 4 entries of 24 bytes, scanned while index < 4 and pointer <= 0x022CBA50
  +0x00  u8   state       0 = free, 3 = reserving, 4 = active, 5 = pending release
  +0x01  u8   key         the caller's track id
  +0x02  u8   flags       bit0/bit1 maintained by the sweep; cleared with & 0xFC
  +0x03  u8   handle      the value returned to callers
  +0x08  u64  = 0 on reserve
  +0x10  u32  = 0 on reserve
  +0x14  u32  = thunk_001DBB80(key)
```

## 5. Call chain

```
UI / event script / battle logic decides a sound should happen
  -> 00249C60(localIndex)                       [AUTHORITY * -> 18]
     |                                        first transition labelled under CALL-CHAINS.md
     |                                        rule 6, 2026-09-18. AUTHORITY because Audio's
     |                                        own gate below can refuse the whole request
     |                                        and the caller never learns why; `*` because
     |                                        UI, event script and battle logic all enter
     |                                        here, which the line above names.
     -> gate 02091098                           (non-zero -> 0xFFFFFFFF, nothing else runs)
     -> 003A1180(localIndex)                    [resolve]
        -> 00267330(0)                          (world not live/held -> -1)
        -> table 02AEEDC8 via handle 02AEF3FC   -> slot*512 + localIndex
     -> 002DF220(id, 0x40, 0x7F)                [tail call - its result is the caller's]
        -> 003603C0 -> gate 022CB726            (non-zero -> 0)
        -> 001DBDB0(0, id & 0x7FFFFFFF, pan, vol)
           -> 00210B30 -> audio registry 01FD36A0 (five per-class controllers)
           -> 00210C00                          [the fork]
              -> 0021B5B0  (+0x08 SebAudioController)  match bank[+0x3C] == id/512
                 -> 00212950                    the receipt, issued unconditionally
                 -> 00224540 -> 00224570        [voice start]
                    -> 002256F0(voice, 0x40, 0) [pan   -> SQEX Sd 007A7E00 / 007A7E90]
                    -> 002257E0(voice, 0x7F, 0) [volume -> SQEX Sd 007A81F0]
                    -> 007A78B0                 start; non-zero -> 002256B0 resets the voice
              -> 00219EA0  (+0x10 SepAudioController)  match bank[+0x38] == id, state 2
                 -> 00223160 -> 00223190
  -> play handle, or 0xFFFFFFFF
```

### 5a. The same chain, with what is now known at each joint *(synthesis, 2026-09-18, FABLE)*

*No new reading. The diagram above was drawn before the boxes of section 7 and of the two sound-selection pages
were answered; this joins those answers to it, for someone who has to reproduce the behaviour.*

| joint | what is now established | where |
|---|---|---|
| the index | A small index is a **slot of `se000.seb`**, the system sound-effect block, always: the boot routine loads three blocks and gives each its own completion and its own handle, so handle A never names a field's bank. 37 distinct immediate indices exist in the image and all 37 are filled slots of that file. | section 7, UQ-243; [the R2 page](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md) UQ-149 |
| the id | `bank word * 512 + index`; the bank search is `id / 512` against each loaded bank. | the diagram; section 7 |
| the bank | Banks are objects drawn from **per-class pools fixed at start-up: 2 music, 96 Seb, 256 Sep, 4 stream, 6 shout.** A controller that needs a bank pops a free one, and if none is free runs its idle-bank housekeeping and tries once more; the stream controller evicts its oldest when it holds four. | section 7, UQ-244; [the bank page](../Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) section 7 |
| the voice | Voices are **not** per class. Every class takes them from one shared pool of 1,024 records built at audio start-up; when it is empty the Seb, Sep and Shout controllers are asked to give some back and the pop is retried. | section 7, UQ-244 (the 2026-09-14 addition) |
| the stop | `0024A1A0` is a stop by sound id on one or both sound-effect controllers, a 0.1-second fade except where the caller gives a time; negative ids are bulk forms. | section 7 |
| inside the driver | The started sound is one of the `SQEX::Sd::Driver` sound classes and its slot 43 is the **selection rule** for which authored sequence plays: every zero-weight set, plus one weighted draw with an anti-repeat (`RandomSound`); a stepping cursor (`OrderSound`); a draw that avoids groups still sounding (`CycleSound`); a `[low, high)` range on a named parameter (`SwitchSound`). The entry's `u16` names its sequence by ordinal in the bank's `seq ` chunk. | section 12 (corrected today), UQ-250; [the variant page](../Sound-Selection/sound-variant-selection.md) section 12 |
| what ships | In the shipped archives every one of the 11,165 sequence records is version 4 with one candidate in group 0 and no range, and no sound is authored as `CycleSound` or `SwitchSound`: **the selection machinery is complete and never has a choice to make.** | [the trigger page](../Sound-Selection/sound-trigger.md) UQ-259 (SWE2-DATA's census) |

**For a reimplementation.** The observable contract is narrow: resolve the index against `se000`, issue the
receipt before the bank search (a handle is not proof of playback), honour the two gates, take a voice from the
shared pool, start it with pan `0x40` and volume `0x7F` unless the caller supplied others. The variation classes
can be implemented as *play the one candidate* without changing any shipped sound; implementing them fully
matters only to someone authoring new banks. *Not known, unchanged:* ~~the five voice-pack slots (UQ-248, UQ-249)~~ *(2026-09-25: the five slots are the actor managers' loaded-resource names, not voice packs — UQ-248, answered in §11 "What is not established")*, and the
inbound surface's remaining functions (UQ-245).

**Upstream (who causes this).** Across the corrected 168-function inbound surface there are **305
distinct non-Audio callers**.

> **These are floors, not counts — §10.** Every figure in this paragraph is measured over
> `edges.tsv`, which does not record a thunk's outgoing `JMP`. A byte-level decode of the same
> population gives **182 functions, 325 callers, 421 edges**; the graph has **no** edge the decode
> lacks, so the numbers move in one direction only. The partition below is likewise a floor.

Partitioned by the caller's `PrimaryOwner`, the 401 inbound edges are:
274 from functions with no owner tag, 55 `Script_VM_Native_Bridge`, 42 `UI`, 11 `Presentation`, 4
each `Save_Load_Settings` / `ActorEntity` / `WorldAreaField`, 2 each `Resource` /
`Rewards_Progression_Economy` / `CombatFormula`, and 1 `CombatAction`. For `00249C60` alone the 99
callers split 67 unowned, 29 `UI`, 3 `Save_Load_Settings` — **corrected in §10 to 68 / 29 / 3 = 100**.

Two of those callers are named and player-facing: `003112F0`
(`BattleFormula_ApplyTargetResult`, `CombatFormula`) and `0030C650`
(`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`, `Rewards_Progression_Economy`). Both call
`003A1180` and `002DF220` directly rather than through a wrapper — so the wrapper family is a
convenience, not a chokepoint.

**Downstream (what this causes).** The `SQEX::Sd` driver in the `007Axxxx`–`007Fxxxx` range,
documented structurally in
[`../sqex-sd-sound-driver-architecture.md`](../sqex-sd-sound-driver-architecture.md). `00224570`
reaches it through `007A6DB0`, `007A7010`, `007A78B0`, `007A7A20`, `007A8CF0` and the two setters
above, several of which take `EnterCriticalSection`/`LeaveCriticalSection` — the boundary is
crossed under the driver's own lock, not the caller's.

**Do not confuse with:**

- **`003A1180` and `003A11F0` are not two different lookups.** Same global handle, same table, same
  arithmetic. The only difference is `003A1180`'s world-live precondition.
- **`002DF220` is not the only play path.** `002DEF40` and `002DF010` reach the same dispatcher with
  a *derived* selector, `003A0E20` intercepts an entirely different id encoding on bit 30, and two
  named battle functions bypass the wrappers.
- **The play handle is not proof of playback.** `00212950` runs before the bank search.
- **`0016D6A0` is not a control-flow guard here.** Its body is a bare `ret`. See §8.
- **`Boundary.Audio.NativeSupport` is not an audio API.** It is a rejection bucket; the prior
  document establishes this in
  [`what-the-engine-calls-to-make-a-sound.md`](what-the-engine-calls-to-make-a-sound.md).

## 6. Modding notes

- **Best intervention point, by intent:**
  - *Silence what the gated wrappers request:* write non-zero to `02091098`. One store, ahead of id
    resolution, so nothing is looked up, allocated or queued — **not everything**: `00271500` and the
    script verb `sebsoundplay_2c1` bypass it (corrected 2026-09-12); hook `002DF220` to stop all. It is also the point the game's own
    scripts use, via `00512080` — you are using the engine's own switch, not fighting it.
  - *Change what a sound is:* the authored bank data. `003A1180`/`003A11F0` only do arithmetic;
    the identity lives in the bank.
  - *Change how a sound is played (volume/position):* hook `002DF220` and alter arguments 2 and 3.
    This is the only place in the wrapper family where those values are still separable —
    upstream they are compiler-folded literals, downstream they are already floats in the driver.
  - *Add a genuinely positional sound:* you cannot do it by tuning the four wrappers — each passes
    `(0x40, 0x7F)`. From a script, `sebsoundplay_2c1(bank, index, pan, volume)` already does it. Call `002DF220` yourself with a real pan byte, or call
    `002256F0` on a voice you already hold.
- **Regenerates itself:** the play handle counter `01FD36B4` and the voice fields written by
  `002256B0` on a failed start. Do not write voice `+0x1C`/`+0x20` directly — go through
  `002257E0`/`002256F0` so the driver-side value is updated too; writing the shadow alone changes
  nothing you can hear.
- **Breaks if:**
  - You expect the return value to explain a silence. Four distinct refusals — global gate, world
    not live, second gate, no matching bank — and the first two return `0xFFFFFFFF` while the
    second two return `0`. Neither says which.
  - You treat a non-`0xFFFFFFFF` return as "a sound is playing". It is not.
  - You assume the pan byte is 0–127 because the volume is. It is 0–255 and it branches at `0x80`.
  - You hook `002DF220` expecting to see every sound. Bit 30 and bit 31 of the id both route
    elsewhere, and music never comes through here at all.
  - You call into `00224570` while a bank's load state is `1`. It spins with `Sleep(0)` until the
    load completes — on the calling thread.
- **Multiplayer / XIIOnline:** sound is local presentation. What can legitimately cross the wire is
  **the authored bank-local index and the moment it was requested** — the small number the caller
  actually passes, plus enough context to know which bank was loaded. The *resolved* global id is
  worthless remotely, because it is `slot*512 + local` against the **receiving** client's
  `02AEF3FC`, which may point at a different bank. The play handle is a local counter value and has
  no meaning on another machine at all.
- **Mod compatibility:** the bank contents and the `SeSep` container are authored data and are the
  right surface to change. The 512-per-bank block size is compiled into both the resolver
  (`shl edx, 9`) and the lookup (`sar edi, 9`) — a mod cannot widen a bank past 512 entries by
  editing data alone.

## 7. What is not known

- [x] **UQ-239.** *(answered 2026-09-18, at the end of this item)* What `02091098` means in the player's vocabulary. Its effect, its single writer and its
      script-facing setter are all proven; the *policy* it encodes is not. **Killer observation:**
      decompile `0027F5D0` (1,280 B) and find which game state it sets the gate from.
      ***The killer observation was carried out 2026-09-15 (OPUS). The state is found; the policy is
      narrowed to one step short of proven, so this box stays open.***
      `0027F5D0` is a widget message handler. On **message 2** it switches on its own state word
      `[widget+0xC0]`, and the arms are states **1, 8, 10 and 12**:
      
      | state | what the arm does |
      |---|---|
      | 1 | `0027EF00(0)` then `0028E660(1)` — the location-map open path — then state := 0 |
      | 8 | `003CA0C0()`; if non-zero, state := 12 |
      | **10** | **`00249FC0(1)` — raises the gate** — then `002D66A0(word [01E0C2A4])`, then state := 0 |
      | 12 | `003CA1B0(3)`, then state := 9 |
      
      **So the gate is raised in state 10 of that machine, and what state 10 does next is the answer.**
      `002D66A0` is 30 bytes, owned by **Input**, and writes the word it is handed into three input
      globals — `02F973AC`, `02F973AE`, `02F973B0`. The word it is handed is `[01E0C2A4]`, which
      [`AV-6`](../../_index/OPEN-QUESTIONS.md) establishes is the **CANCEL** mask (`01E0C2A0` being
      confirm). **State 10 therefore raises the audio gate and immediately synthesises a cancel press.**
      
      The gate is not lowered in that arm. It is cleared only when the widget is destroyed: message
      **15** with `[widget+0xD4] == 0x42` calls `002D6F90`, which does `xor ecx, ecx` / `00249FC0` —
      gate := 0. So the raised window spans *the synthesised cancel through to the widget's teardown*.
      
      > **What this is in the player's vocabulary, stated as far as the evidence goes.** It is not a
      > general mute. It is a **silence window around an input the game gives itself**: the screen
      > closes itself by pressing its own cancel button, and the gate is raised first so that requests
      > made during that self-close are abandoned before any lookup.
      
      **The last step is NOT claimed.** AV-6 records that a cancel branch *always plays UI sound 3*,
      which would make the gate's purpose exactly “swallow the sound the synthetic cancel would
      otherwise play” — but AV-6 read that in `BattleMenu_UpdateCommandSelectionAndDispatch`, not on
      this widget's path, and whether the map screen's synthesised cancel reaches the same sound route
      is not read here. That one hop is what stands between this and a closed answer.

      **ANSWERED 2026-09-18 (FABLE): the gate mutes the blip of a cancel the game presses for itself - the hop is read, and it lands on the gated sound wrappers whichever screen takes the press.** (1) *Where the synthesised press goes.* The three words `002D66A0` writes are consumed once, by the frame-snapshot builder `002498B0`: after it has copied the raw snapshot `02F97360`.. to the filtered copy `02F97388`.. and masked the copy, it ORs `02F973AC` into the copy's two held words (`02F97388`, `02F97390`), `02F973AE` into its two newly-pressed words (`02F9738A`, `02F97392`) and `02F973B0` into its two repeat words (`02F9738C`, `02F97394`), then zeroes the newly-pressed and repeat injections with one dword store (the held injection `02F973AC` is not cleared there; only the block reset `00249840` covers it). **The raw words are never touched**, so a synthesised press exists only for code that reads the filtered copy. (2) *The map screen's own cancel does not see it.* The widget family's cancel test `0027EA70` reads the **raw** newly-pressed word `02F9736A` (and plays UI sound `3` on it), so the press of state 10 is addressed to something else. (3) *Who does see it.* A rip-relative census of `02F97392` finds two kinds of cancel-testing reader. The 4,810-byte input state machine `002BAF80` tests it against the cancel mask and plays UI sound `3` through `00249C60`. And the list-input dispatcher `002D3BA0` (1,904 B), fed the three filtered words by `002D09F0` and `002D3A50` from the main-menu screens (`00560910`, `005691E0`, `0056B4D0`), on a cancel sends the widget record `0x8002` and then plays the widget's own sound byte `+0xFE` - or `3` when that byte is 0, nothing when it is -1 or when flag `0x400000` of `+0xE0` is set - through `00249C60`, or `00249CA0` when flag `0x20000000` of `+0xE4` is set. (4) *Those are the gate.* `02091098` has exactly three readers in the image - `00249C60`, `00249CA0` and `0024A1A0` - and one writer, `00249FC0`. So the hop AV-6 could not supply is read on this path: the press state 10 synthesises can only be taken by a screen that reads the filtered words, every such cancel arm found answers with a UI sound, and every one of those sounds goes through a wrapper that returns early while the gate is up. **In the player's vocabulary: when the map screen presses cancel on the player's behalf for the screen beneath it, the player does not hear a cancel blip they did not press.** The window stays open until the widget's teardown, so any other UI sound asked for in that interval is dropped with it. *Not established, and a run-time fact:* which of the filtered-word consumers is the live one when state 10 fires. *One default left loose:* `002D3BA0` loads the fallback index as the constant `3` on two paths and as `rbp + 3` on a third where `ebp` was not proven zero. Static evidence only.
- [x] ~~**UQ-240.** What `022CB726` means, likewise. `00360110`, `003601D0` and `00360370` write it; only their
      surrounding state machine can say what for.~~ **Answered 2026-09-14 (FABLE)**, from that surrounding state machine, which was read under UQ-150 on [the force-fight toggle page](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md): **`022CB726` is the flag "a skip reset is in effect".**
      - `00360370` zeroes its block at boot.
      - The per-frame check `00360120` services a pending request byte set by `003603D0` or `003603E0`. It runs the skip-family handler `003601D0`, which stops sound, resets the time scales and sets the flag.
      - `00360110` clears it when `ActorManager_BindLoadedDefinitionPayload` binds the next definition payload.
      Its reader `003603C0` is the refusal predicate this page's sound path consults. So a sound request is refused between a skip reset and the next definition bind.
- [x] **UQ-241.** *(answered 2026-09-18, at the end of this item)* What bit 7 of the ActorManager slot flag byte at `02098E20` represents. It is set and cleared
      inside `ActorManager_RunFieldRuntimePass`, and it blocks sound resolution — but "held" is a
      description of its effect, not a recovered name.
      *Narrowed 2026-09-14 (FABLE), by propagation from `UQ-32`:* bit 7 marks a slot whose start-up has not settled. While
      it is set the field pass runs its start-up branch instead of the ordinary record loop, and it rewrites the bit on each
      start-up pass from whether any record is still running. The sound gate refuses such a slot. Its first setter was not
      located ([the shared-neighbours page](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md) §7, UQ-32).
      **ANSWERED 2026-09-18 (FABLE), by propagation from `UQ-32`, which was answered on 2026-09-17 and had not been carried back here: bit 7 is the slot's *start-up unsettled* flag, and its first setter is the definition-payload binder `ActorManager_BindLoadedDefinitionPayload` `0026C8C0`.** The binder ORs `0x82` into a register copy of the slot's `+0x10` byte and stores the byte whole when a loaded definition payload is bound; its only caller is the load completion `0032F850`. The field pass `0025D9E0` then runs its start-up branch for that slot and rewrites the bit each pass from whether any record is still running, so it falls when the last start-up record finishes; boot clears it with the slot reset `00266D10`. **In the player's vocabulary: the area's scripts have been loaded but have not finished setting the scene, and until they have, a sound asked for on that slot's behalf is refused.** It pairs with `UQ-240` on this page, whose flag is cleared by the same binder: a skip reset refuses sound until the next payload is bound, and the bind then refuses it until the payload's start-up settles. The derivation and its addresses are under `UQ-32` on [the shared-neighbours page](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md); nothing new was read for this entry. Static.
- [x] **UQ-242.** *(answered 2026-09-18, at the end of this item)* The exact geometry `007A7E90` applies. The three floats and the `+1.0`/`-1.0` axis are exact;
      whether the driver treats them as a direction vector, a stereo balance or a 2-D position is a
      claim about `007A7E90`'s body, which was not read.
      *Narrowed 2026-09-14 (FABLE), not answered.* `007A7E90` is read: it only checks the handle kind
      (0 gives `0x82000000`; kinds 2, 8 and 9 pass) and queues action type `0x10` with the three
      floats and the fade at `+0x10..+0x1C`. The consumer `007AB5C0` (table `007AC080`, arm
      `007AB8F1`) resolves the handle through `007AB1E0` and calls the object's slot 9 (`+0x48`).
      For kind 2 that is `007BE590`, shared by `Sound`, `CycleSound`, `OrderSound`, `RandomSound`,
      `SwitchSound` and `VariationSound` (`Driver@Sd@SQEX`; six vtables hold it). Its warning strings
      name the three floats **`pan`**, **`frpan`** and **`udpan`** (`01CB5C30` / `01CB5C68` /
      `01CB5CA0`, "Sound:*SetPanning ... range over!"). They are three independent pan axes, not a
      normalised direction vector:
      - Each value must lie in `[-1.0, +1.0]` (`01CEBC9C`, `01CEBBA8`). An out-of-range value is
        dropped with the warning, not clamped, and the other two axes still apply.
      - Each axis ramps separately through `007CA560` into its own 0x30-byte interpolator at
        `+0x1B8` (pan), `+0x1E8` (frpan) and `+0x218` (udpan).
      - `pan` alone is circular. `007BE590` wraps both the current value and the step into
        `[-1, +1]` with ±2.0 (`01CEBC08`, `008F3148`), so a ramp from `+0.9` to `-0.9` goes the short
        way through ±1. That is the behaviour of an angle whose ends meet behind the listener.
        `frpan` and `udpan` are not wrapped.
      - The preceding `007A7E00(voice, 1)` queues action `0x12` → slot 10 `007BE510`. Mode 1 sets
        `+0x518` bit 0 and gives all three interpolators curve mode 1 with rates `5.0` at
        `+0x28`/`+0x2C`. In `007CA560` mode 1 stretches a ramp to at least |Δ| / 5.0 fade units.
        The caller converts frames with `/60`, so the unit reads as seconds. Even this family's
        fade of 0 therefore slews at no more than 5.0 per second. Mode 0 clears the bit and the
        curve modes.
      - Kind 8 is a `Music@Magi` handle (pool `02EADC20`, "music number is out of range"). Its slot 9
        `007CA370` feeds the same three floats to `+0x520` / `+0x550` / `+0x580` with no range check
        and no wrap. It skips all three when the music header's version byte is 3 or more and bit 3
        of its `+0x0A` byte is set.
      - For kind 9 (pool `02EADCE0`, resolver `007B7FD0`), neither the class nor its slot 9 was identified.

      So in this family's call the second float is `frpan` and the third is `udpan = 0`. The page's
      "front half / rear half" labels match the front/rear axis name. Which sign means front was not
      read. What stays open is how the mixer turns the three interpolated axes into per-channel gains,
      that is, whether `pan` is an azimuth or a left/right balance. That lies in the readers of the
      three interpolators, which were not traced.
      > ***CONFIRMED BY EXECUTING THE ORIGINAL MIXER — 2026-09-21 (FABLE, consuming
      > `ASTRA-RETURN-FABLE-PAN-MATRIX-SPREAD`).*** The azimuth reading below was static. ASTRA ran
      > `007B8430` in isolation on the original bytes — with the original cosine `007B8BA0` and sine
      > `007B8C80` bodies and **no stubs**, canaries around the output and the real security-cookie
      > check in every accepted row — against the front/back-**mirror** alternative:
      >
      > | controlled input | output 0 | output 1 |
      > |---|---:|---:|
      > | mono byte 215 | 0.471396714 | 0.881921172 |
      > | mono byte 240 | 0.183039829 | 0.983105421 |
      > | **the mirrored input for 240** | **0.983105421** | **0.183039844** |
      > | stereo 240, spread 0, source 0 | 0.565731704 | 0.824589252 |
      > | stereo 240, spread 0, source 1 | 0.824589312 | 0.565731645 |
      > | stereo 240, spread 1, either source | 0.183039829 | 0.983105421 |
      >
      > **The azimuth reading is the one the machine agrees with**, and the discriminator is sensitive
      > to precisely the instruction that decides it: NOP-ing the negative-`frpan` half-turn at
      > `007B8769` flips byte 240 to output-0 dominance, so the control would have caught the mirror.
      > Two other boundaries came with it: mono byte **127 favours output 1 while 128 favours output
      > 0**, retaining the wrapper/mixer discontinuity, and **`frpan` zero gives exactly `(0.5, 0.5)`**
      > in the tested mono case.
      >
      > **The `spread` parameter this item left uncharacterized is now measured.** For two source
      > channels and two outputs the pre-wrap offsets are `1.5` and `0.5` — equivalently `-0.5` and
      > `+0.5` — and `007B86BD`–`007B86E6` applies: `s <= 0` leaves `o`; `s > 0 and o > 1` gives
      > `o + (o-1)·s`; `s > 0 and o < 1` gives `o - o·s`; `o == 1` is unchanged. ***So spread `1`
      > collapses the two offsets to the same direction*** modulo the pan coordinate's period of 2,
      > rather than widening them — the opposite of what the name suggests. `-1` and `2` are
      > controlled boundary inputs, not evidence that any caller supplies them, and the ordinary
      > initialized value and permissible caller range stay open.
      >
      > ***And the same package bounds the answer below.*** At spread zero the **two source channels of
      > one stereo voice favour opposite outputs** from identical `pan` and `frpan`. **So a sampled
      > `pan`/`frpan` target alone cannot establish which side a stereo voice is heard on** — the
      > mixer treats each source channel separately, and that is a claim this item would otherwise
      > invite. Applying identical signals to both rows gives about `1.390321` in each output, which is
      > a **linear calculation from coefficients, not rendered audio**: real sample content, phase,
      > levels and later processing decide what is audible. **Numeric output 1 is not identified here
      > as the physical right speaker.**
      >
      > **A caller can also cancel the axis before the mixer sees it.** `007EDE90` reads a `word` at
      > `+0x0A` of the bank payload and, when it is 1, passes zero as `frpan` to both mixer call sites
      > ([the SAB container](../Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md)) — which with
      > the `(0.5, 0.5)` result above is a centred row. Whether any shipped bank carries that value is
      > not established.

      **ANSWERED 2026-09-18 (FABLE): `pan` is an azimuth - an angle of `pan` x pi radians around the listener - and `frpan` is how far out along that direction the sound sits; `udpan` is carried all the way down and then not used.** The three interpolators have one reader, the `Sound` family's virtual slot 28 `007BD6F0` (466 B; the same cell in all six vtables), which evaluates each ramp through the curve function `007A9E50`, wraps `pan` and clamps the other two to `[-1, +1]`. Its caller `007BFD00` hands the three values to every child object the sound owns (handles at `+0x400`, setter `007E73F0`), that object's update `007E7540` passes them to its track (`007E8AF0`), and the track's combiner `007E8410` folds them into the track's own layers: **`pan` and `udpan` add, `frpan` multiplies** - a parent turns its children and scales their distance. The `MaterialTrack` slot 7 `007E9500` then gives the five results (the three axes, a centre weight and a low-frequency level) to the voice routine `007EDE90` (1,123 B), which calls **`007B8430` (1,895 B) once per source channel to fill one row of a source-by-output gain matrix**. That function is the geometry: (1) the angle is `pan` x pi, wrapped into `[0, 2 pi)`; (2) a table indexed by the device's output-channel count (`007AECE0` returns `[02EAD34C]`) gives the ring of speaker angles - 90 and 270 degrees for two outputs, 45 / 135 / 225 / 315 for six, and those plus 90 and 270 for eight ([pan_speaker_tables.py](members/pan_speaker_tables.py), [pan-speaker-tables.tsv](members/pan-speaker-tables.tsv)); (3) the two ring speakers either side of the angle share the sound at **constant power**, `cos` and `sin` of the fraction of the arc times pi/2 (`007B8BA0` and `007B8C80` are seven-term cosine and sine series), so `pan = 0` on two outputs gives 0.7071 to each; (4) `frpan` is then applied to every ring speaker as `gain = |frpan| x gain + 0.5 x cos(|frpan| x pi/2)`: at 1 the sound is fully at its angle, at 0 every ring speaker gets 0.5 and the angle no longer matters - a sound at the listener; (5) a **negative `frpan` adds half a turn to the angle** before the lookup, a reflection through the listener; (6) where the table's centre flag is set (six and eight outputs), the angle lies in the arc between the last and first ring speakers and the centre weight is above 0, a second pairwise pan over the front arc 315 / 0 / 45 is blended into outputs 0 to 2 by that weight, and where the low-frequency flag is set output 3 receives the low-frequency level divided by the source channel count. `udpan` reaches `007B8430` in its third float register and no instruction there reads it. A stereo or four-channel source spreads its channels at fixed offsets either side of `pan` (on two outputs -0.5 and +0.5, otherwise -0.25 and +0.25, then adjusted by a spread parameter whose effect was not characterised), six- and eight-channel sources bypass the angle and map channel to channel with 0.7071 folds, and the voice routine sends a material whose header byte `+0x19` has bit 3 set to output 2 alone, without calling the function. *Read against this page's pan byte:* `0x00` is 270 degrees, `0x40` is 0 and `0x7F` is 88.6 - a continuous front half. For `0x80` and above the wrapper passes `(0xBF - pan) / 128` with `frpan = -1`, which the driver turns into 268.6 degrees for `0x80`, 180 for `0xBF` and 90 for `0xFF`: the rear half runs the opposite way round from what a front-to-back mirror would give, and the byte circle jumps at `0x7F` / `0x80`. On two outputs front and rear are indistinguishable anyway (180 degrees splits equally, as 0 does). *Counted the same day, script side:* the only script verbs that carry a pan byte to this wrapper are `voicepan` and `voicechangepan` (both reach `002256F0` through the stream pan setter `001DC240` and `00225280`; `sebsoundplay` has no pan argument in any of its 6,821 shipped calls). The 1,114 `us` scripts call them **18 times**: `64` eleven times, `96` once, and **six calls in the rear half** - `192` three times (`alc_b0400`, `ozm_b0400` twice), `215` (`naf_b0401`), `240` (`bhm_c0100`) and `250` (`grm_a0200`). Through the driver those are 178.6, 146.3, 111.1 and 97.0 degrees; a front-to-back mirror would have made them 181.4, 213.8, 248.9 and 263.0. `192` is directly behind either way; **for `215`, `240` and `250` the two readings put the voice on opposite sides**, and on two outputs that is an audible left/right difference, so it is a question a listening test can settle. The wrapper's eight other native call sites all pass a parameter through and were not followed. *Inference, kept apart:* that output index 0 is the left speaker and 1 the right (so that angles run clockwise and `pan = +0.5` is hard right) rests on the standard Windows channel order, which the image does not name. *Not covered:* the one-output table points at zero-initialised memory filled at run time, and kind 9 of the narrowing above is still unidentified. Static evidence only.
- [x] **UQ-243.** *(answered 2026-09-18, at the end of this item)* Which sounds the small indices name. 66 of the 211 call sites pass an immediate (`0x0A`
      ×7 sites, `0x25` ×11, `0x51` ×7, and 28 other values from `0x15` to `0x6C`); the other 145
      compute it. Mapping index → audible sound needs the bank data, not the code.
      **ANSWERED 2026-09-18 (FABLE): an index names a slot of `se000.seb`, the system sound-effect block, and always that bank.** The boot routine `003A13F0` submits three kind-32 loads and gives **each its own completion**: SE id 0 (`se000.seb`, path-array entry 0) completes through `003A1390`, which stores the handle in `02AEF3FC` (`003A14E9`, `003A13A4`); SE id 1 (`se007.seb`, entry 1) through `003A1330` into `02AEF400` (`003A1568`, `003A1344`); SE id 2 (`se002.seb`, entry 3, the mapper `002ED8C0` sends 2 to 3) through `003A12D0` into `02AEF404` (`003A15E7`, `003A12E4`). Those three stores and the boot resets are the only rip-relative writes to the three handles, and each completion's only reference in the image is its `lea` in the boot routine (no direct call or jump reaches one), so no field or script bank load passes through them. So the handle both wrappers resolve is `se000.seb`'s from boot onward, whatever order the loads finish in, and the index is the slot number in that file's `i32[128]` table at `+0x10`. *Census* ([se_index_census.py](members/se_index_census.py), [se-index-census.tsv](members/se-index-census.tsv)): 212 direct call or jump sites in 103 listed functions; **162** load the index as an immediate within twelve instructions and 50 compute it. The earlier figure of 66 counted only the values from `0x0A` up and is reproduced exactly (66 sites, 31 values); the other 96 sites pass `1`, `2`, `3`, `4`, `5` or `8`, with `3` at 34 sites and `2` and `5` at 21 each - the handful of sounds almost every menu procedure makes. *Falsification control:* all **37** distinct immediates are filled slots of `se000.seb` (123 of 128 filled; empty are 0, 6, 12, 47 and 127, and no site passes one of those), against 4 of 37 in `se007.seb` and 11 of 37 in `se002.seb`, so the data independently picks the same bank the completions do. What each slot sounds like is a property of the waveform, not an unknown of the program; the owner column of the census says which layer asks for each. Static plus archive data; the backward walk is linear and does not follow branches.
      *Observed while reading the boot routine, not used above:* the reset before the second load stores -1 into `02AEF3FC` again
      (`003A153D`) rather than into `02AEF400`, so handle B has no -1 store anywhere and starts as the zero the loader leaves in
      `.bss`. Whether that matters to the *B is -1* refusal on [the request contract](CONTRACT-sound-request.md) is routed to OPUS.
- [x] ~~`00210C50` is now read: it routes to **both** the Seb (`+0x08`) and Sep (`+0x10`)
      controllers, or to one of them, on two boolean parameters — so `0024A1A0` is a
      broadcast-style operation over the sound-effect controllers, not a play. What
      `0021B640` / `0021A100` / `00212B80` then do was not read, so "stop" remains unproven.~~
      **Answered 2026-09-14 (FABLE): it is a stop. All three routes end in SEAD's `Stop`.**
      - **The SEAD end.** `007A84A0` queues action type `0xB` (`007A853C`), whose arm `007AB81E` calls slot 2 (`+0x10`)
        of the resolved object. For a `Sound` that is `007BED30`. Unless the state `+0x54` is already 0, 6 or 7, it ramps
        the volume entry at `+0xC8` to `0.0` over the given time (or the header's release time at `+0x58`), stops the
        tracks at once when that time is not positive (`007E74A0`), and sets state **6** (`007BEEF7`).
      - **Seb** `0021B640`. A positive id finds the bank `id / 512` on the `+0x08` list (bank `+0x3C`), and `00222410`
        stops each voice in it whose `+0x24` equals the id, with a **0.1 s** fade (`008C5F6C`, `0022245B`). Id `−4`
        walks every bank through `00224870` → the bank's slot `+8`. Ids `−1` / `−2` take a branch (`0021B6E5`) that was not read.
      - **Sep** `0021A100` goes through `00223300`: `−4` → slot `+8`, otherwise `002225B0(…, 0)`, which divides its
        time by 60 and calls `007A84A0` (`002225E8`–`002225FF`).
      - **Both** (`00212B80`, when the third argument is non-zero) → `00222390`, again `007A84A0` with 0.1 s
        (`002223B8`–`002223DB`).

      So `0024A1A0` stops a sound id on one or both sound-effect controllers, and the negative ids are bulk forms. What the
      bank slot `+8` does for `−4`, and the Seb `−1` / `−2` branch, were not opened.
- [x] **UQ-244.** *(answered 2026-09-18, at the end of this item)* What the per-class pool constants passed to each controller's `this+0x20` initialiser mean
      — Music 2, Seb 96, Sep 256, Stream 4, Shout 6. "Simultaneous voice capacity" is the natural
      reading and would be a directly player-facing number, but `00217E10` / `0021A820` /
      `00219300` / `0021CB10` / `0021BCB0` were not read and it is **not claimed**.
      *Narrowed 2026-09-14 (FABLE), not answered: the initialisers are read; what a record is was not traced.* Each
      constant is **the record count of a pre-allocated pool** threaded onto a free list at `this+0x20`. Each
      initialiser calls its class's sizing function with the constant. That function reserves `n` records, pushes
      each onto the list with `00199DB0`, and flips a done byte, `+0x90` for Music (`00218A0B`–`00218A15`):

      | class | initialiser → sizing | records | record size |
      |---|---|---:|---:|
      | Music | `00217E10` → `00218990` (reserve `00218E80`) | 2 | `0x58` |
      | Seb | `0021A820` → `0021B160` | 96 | `0xA0` |
      | Sep | `00219300` → `00219B20` | 256 | `0x68` |
      | Stream | `0021CB10` → `0021D440` | 4 | `0x48` |
      | Shout | `0021BCB0` → `0021C450` | 6 | `0x68` |

      So the numbers are hard caps on how many of each class's records can exist at once. **Whether a record is a
      playing voice or a loaded bank was not established.** The Seb play `0021B5B0` finds a *bank* on the list at
      `+0x08` (matched at bank `+0x3C`) and starts the voice inside it through `00224540`, and neither function takes
      from the `+0x20` pool. "Simultaneous voice capacity" therefore stays unclaimed.
      *Added the same day:* the voice records are **not** these pools. `00223190` takes its voice through `00221D60`, which
      pops from a global pool: `[01FD4138] + 0xA0`, via `00220D30` → `00220550`. That `0x8D8`-byte object is built once by
      `002216B0(0x400, 0x400)` from the audio start-up `00210895`, and `00220F20` sizes its `+0xA0` pool from an argument
      (`0021E6D4`–`0021E6DD`), which is 1024 here. When the pop fails, `00210A60` runs `00212910` → `00222050` over the
      Seb, Sep and Shout controllers and retries. So the five constants above bound something per class other than
      voices (banks or handles is the likely reading, not asserted), and the voice ceiling is the shared pool.
      **ANSWERED 2026-09-18 (FABLE):** **a pool record is a bank object, so each constant is the number of that class's banks that can be alive at once.** Three independent readings agree. (1) *Size.* The five strides (`0x58`, `0xA0`, `0x68`, `0x48`, `0x68`) equal, class for class, the object sizes the banks' sized deleting destructors state (`MusicAudioBank` `0x58`, `SebAudioBank` `0xA0`, `SepAudioBank` `0x68`, `StreamAudioBank` `0x48`, `ShoutAudioBank` `0x68`). (2) *Construction.* The pop body behind each controller's slot 7 takes the leftmost node of the free set, erases it, inserts the record into the second set at `+0x58` and hands the record to a constructor that runs the shared `AudioBank` base constructor and then installs the class vtable whose RTTI names the bank: `00907910` `MusicAudioBank` (id `+0x50` := -1), `00907D80` `SebAudioBank`, `00907B48` `SepAudioBank`, `00907F90` `ShoutAudioBank`; the Stream reserve path installs `009081A0` `StreamAudioBank`. (3) *Use.* Slot 6 is the allocation: pop a record; if the pool is empty run slot 4 and pop again; then register the bank on the `+0x08` list through slot 5 - the list the Seb play and stop paths search by bank `+0x3C`. Stream's slot 4 acts only when the list holds **exactly 4** entries, its own constant, and then evicts the head. So the caps are **2 music banks, 96 Seb banks, 256 Sep banks, 4 stream banks and 6 shout banks**; the ceiling on sounding voices is the shared 1024-record pool described above, not these. Static: bodies read, RTTI read from the complete-object locators. *Not established:* what the other classes' slot 4 frees when a pool is empty beyond the idle test [the bank page](../Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) records (`+0x2C == 0` and `+0x30 == 0`), and what the game does when the retry also fails.
- [x] ~~`00223190` (356 B), the stream-side voice start, was not read.~~ **Read 2026-09-14 (FABLE).** It is reached from
      the **Sep** controller (`00219EA0` → `00223160` → `00223190`, the call chain above), so "stream-side" was the wrong
      label. In order it:
      1. waits, with `Sleep(0)`, while its bank's load state `+0x30` is 1 (`002231B3`–`002231CF`);
      2. for a bank with `+0x44` bit 5 asks the registry (`00210710`, the Sep controller's slot 2, then Seb's) and returns
         when the answer is yes;
      3. takes a voice from the shared pool (`00221D60`, above) and links it into the bank's list;
      4. sets the voice byte `+0x49` from the bank flags;
      5. writes the sound id (`00225580`) and the mode `4` or `5` (`002256E0`), and for mode 4 the pan (`002256F0`) and
         volume (`002257E0`) as the Seb path does;
      6. starts it with SEAD `007A78B0`, whose first float is **4.8** for a bit-5 bank and 0 otherwise (`002232AB`–`002232C1`).

      What 4.8 is (007A78B0's first float parameter) and what the registry question in step 2 asks were not read.
- [x] **UQ-245.** The remaining ~130 functions of the corrected 168-function inbound surface.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md. See the register row.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `00249C60` takes a bank-local index, not `void` | complete exact-current body: `ECX` is never written before `call 0x3A1180`, and `003A1180` consumes `ECX` (`mov ebx,ecx`) and adds it to its result | 1 |
| 66 call sites load that index as an immediate in `0x0A..0x6C` | independent capstone scan of the 105 caller bodies for `call`/`jmp` to `00249C60`/`00249CA0`, walking back ≤12 instructions for the last write to `ECX`; 211 sites found, 66 immediate, 145 computed | 1 |
| `0x7F` is a volume and `0x40` is a pan | complete exact-current bodies of `002DF220`, `00210C00`, `0021B5B0`, `00224570`, `002256F0`, `002257E0` — the two values reach two distinct setters that write two distinct voice fields | 1 |
| …corroborated by the voice reset | complete exact-current body of `002256B0`: `[+0x1C]=0x7F`, `[+0x20]=0x40` — the same offsets the two setters write, in the same function's object | 1 |
| The pan field is 0–255, not 0–127 | `002DF220` truncates it with `movzx r8d,sil` and `00210C00` with `movzx r8d,r9b`; **neither masks it**, while the volume is masked `& 0x7F` in both. `002256F0` then branches at `0x80` and handles `0x80..0xFF` | 1 |
| `volume/127.0` and `(pan-0x40)/128.0` with a `/60.0` fade | RIP displacements resolved against the authorized EXE: `0x22580A+0x6E123A=0x906A44=127.0f`, `0x22578B+0x6A03A9=0x8C5B34=0.0078125`, `0x225729+0x6D162B=0x8F6D54=60.0f`, `0x225750+0x1AC6458=0x1CEBBA8=+1.0f`, `0x22575D+0x1AC653F=0x1CEBC9C=-1.0f` | 1 |
| `globalSoundId = bankSlot*512 + localIndex` | complete exact-current bodies of `003A1180` / `003A11F0` (`shl edx,9; add edx,ebx`), with the table equality forcing `entry[+0] == slot` | 1 |
| …and its exact inverse downstream | complete exact-current body of `0021B5B0` (`cdq; and edx,0x1ff; lea edi,[rdx+rax]; sar edi,9` = signed `/512`) matching `bank[+0x3C]`, and `00224570`'s `id & 0x1FF` | 1 |
| The two resolvers differ only by `00267330(0)` | complete exact-current bodies; both resolve `[0x02AEF3FC]` against the table at `0x02AEEDC8` — the same two RIP targets, computed independently for each function | 1 |
| `02098E20` is the ActorManager slot flag array | `DumpDataXrefs.java` over the whole image: writers/readers include `ActorSystem_InitializeManagerRuntime` (`OR [RBX+0x10],0x1`), `ActorManager_RunFieldRuntimePass` (`AND …,0x7f`, `CMP …,0x80`), `ActorManager_BindLoadedDefinitionPayload` | 1 + 8 |
| `02091098` has exactly one writer image-wide | `DumpDataXrefs.java`: 1 WRITE (`00249FC0`), 3 READs (`00249C60`, `00249CA0`, `0024A1A0`) | 8 |
| Authored script can set that gate | complete exact-current body of `00512080`: `VMValueStack_PopInt32CoerceFloat32` → `00249FC0`. Cited as authored **intent**; the native seam is `00249FC0` | 9 (intent) + 1 (body) |
| The five bank classes and the kind enum | MSVC RTTI recovered **independently of the GFZ**, straight from the authorized EXE: `.?AV<name>@@` type descriptors → complete-object locators (signature 1) → vftables, then the constructors' literal argument to `00221780(this, kind)` | 4 + 1 |
| `SeSep` is an authored container magic | the 5 bytes at `00917290`, referenced by `002DF070`'s comparison | 2 |
| A handle is issued even when nothing plays | complete exact-current body of `0021B5B0`: `call 0x212950` precedes the list walk, `EAX` survives it, and both no-match exits fall into `mov eax, esi` | 1 |
| `MusicAudioBank` has no match key | `002226A0` constructs a `MusicCallback` sub-object at `+0x38`, where the other four subclasses write `-1` into the qword covering `+0x38`/`+0x3C` | 1 + 4 |
| The singleton is a five-controller registry, one per bank class | complete exact-current body of `002105E0` (five `malloc` + ctor pairs into slots `+0x00`..`+0x20`) and of the five constructors, each of which calls the base `00212710` then stamps its own vftable | 1 + 4 |
| The `0215EFxx` block drives the `MusicAudioController` | `001DBC70`/`001DBCA0` → `00210A40`/`00210A50`, both of which dereference slot `+0x00` | 1 |
| `0215EF44` is a current-track handle and `0215EF4D` a 0–127 level | complete exact-current body of the initialiser `002DE360`: `0215EF44 = 0xFFFFFFFF`, `0215EF4D = 0`, and the 16 registration slots seeded with key `0xFFFF` and refcount `0` | 1 |
| Population figures (2,064 / 174 / 168 / 305) | edge census over a call graph regenerated in this block by `DumpFullCoverageGraph.java` from a freshly imported, freshly verified parent. Positive control: the instrument returns `00249C60` with 99 non-Audio / 0 Audio callers, and each of `00249CA0`, `002DF220`, `003A1180`, `002DEC00`, `002DEE50` in the set with the counts §3 states | 11 (corroboration) |

### The decompiler dropped arguments the machine code passes

`00210C00` decompiles as `FUN_0021b5b0(*(undefined8 *)(param_1 + 8))` — a **one-argument** call in
which the sound id, pan and volume vanish. The disassembly shows `EDX`, `R8D` and `R9D` all loaded
*before* the branch, so both tail calls carry four arguments. Reading only the C would have produced
a confident, wrong statement that the selector-0 path discards the sound.

The same defect appears in `002DF010`, whose C shows three arguments where the register setup shows
four. **Every argument claim in this document was taken from disassembly, not from the decompiler's
signature.**

### `0016D6A0` is a bare `ret`, and it carries many identities at once

The body at `0016D6A0` is three bytes: `C2 00 00` — `ret 0`. It does nothing. The PE load
configuration's `GuardCFCheckFunctionPointer` slot (`008C31C0`) does hold this address, which is
where the `_guard_check_icall` name comes from, and the guard function table is empty
(`GuardCFFunctionCount = 0`).

But the call sites on this path are not control-flow guards. `00210B30` does
`cmp [01FD36A0], rcx; setne cl; call 0016D6A0` and `00219EA0` does
`cmp edx,2; sete r15b; mov ecx,r15d; call 0016D6A0` — in both, the argument is a **comparison
result**, and **no indirect call follows**. That is the shape of a retail-stripped
`Assert(condition)`, not a CFG check.

**The mechanism is `/OPT:ICF` folding, and it is larger than this path.** A peer session measured
roughly **273 `ret`-bodied functions folded onto this one address** — tracked as open question
**BA-1**. Its reference census, reconciled across two instruments: **2,479 distinct calling
functions** (identical sets from `getCalledFunctions` and from `DumpDataXrefs` filtered to `CALL`),
**2,867 call sites**, and **2,511 functions referencing it at all**, 1,515 of those through data
pointer slots. An earlier figure of 2,480 circulated across four documents and was withdrawn: it was
not reproducible under any of those definitions, having been quoted before anyone asked which noun
it counted. So `0016D6A0` does not have *an* identity to recover; it has many, and every
name attached to it (`_guard_check_icall` from the load config, an assert helper here) is correct
for some subset of its callers and wrong for the rest. The same is true of `00225690`, which this
document names `Voice_GetKey` and the vtable index names `btTriangleIndexVertexArray` — one folded
address, two genuine identities, not a disagreement.

That has a consequence beyond naming: a folded `ret` **executes nothing**. `repos-f1` established
that 1,606 deleting destructors route their sized-delete branch through this address and therefore
free nothing (**BQ-27**). On the audio path the consequence is milder but the same in kind: reading
`_guard_check_icall(bank->state == 2)` in `00219EA0` as a protection is wrong twice over — the call
is a no-op, and the comparison it names is never acted on.

### The inbound surface is 168, not 174

The prior document measured **174** Audio-owned functions with at least one non-Audio caller and
correctly labelled it an upper bound, estimating the overcount at two. Re-deriving the census from a
call graph regenerated in this block reproduces 174 exactly, and then subtracts the peer-established
retraction set — the seven `PrimaryOwner:Audio` functions carrying a `SUPERSEDES` / `RECLASSIFY`
correction the tags do not reflect:

| Address | Body | Non-Audio callers | In the 174? |
|---|---:|---:|---|
| `00182E80` | 41 B | 6 | yes |
| `001DC3D0` | 130 B | 2 | yes |
| `00225570` | 5 B | 1 | yes |
| `00225580` | 4 B | 18 | yes |
| `00225680` | 4 B | 3 | yes |
| `00225690` | 4 B | 13 | yes |
| `002256A0` | 4 B | 0 | **no** — it has no non-Audio caller, so it was never in the set |

Six of the seven are in the 174. **The corrected inbound surface is 168.** The overcount was six,
not two, because the earlier estimate was made when only two of the seven retractions had been
found. All seven were excluded from every population figure in this document.

> **This correction went in one direction only — §10.** 174 is an upper bound for the reason above
> *and* a lower bound for an unrelated one: the call graph omits thunk `JMP` edges, and 19 such
> edges reach Audio functions from non-Audio thunks. Corrected in both directions the surface is
> **182**, not 168.

One nuance worth stating, because it is easy to misread as a contradiction: `00225580` is one of the
retracted functions *and* it is a real part of this mechanism — `00224570` calls it to write the play
handle into `voice+0x18`. The retraction is about **ownership** ("cross-subsystem reuse proves it is
not Audio-specific"), not about this call site. A function can be genuinely used by Audio and
correctly denied Audio owner credit; that is exactly what the two-layer model is for.

**Superseded readings:**

- *This document's own first version called `01FD36A0` "the `AudioController` singleton" and read
  `00210C00`'s two branches as "list A at `+8`" and "list B at `+0x10`" of one controller.* **Both
  wrong.** `00212710`, the real `AudioController` constructor, builds a single EASTL list whose head
  and tail are at `+0x08` and `+0x10` — which is what made the misreading plausible — but the
  singleton is not an `AudioController` at all. `002105E0` heap-allocates and constructs **five**
  objects into slots `+0x00`..`+0x20`, each of which derives from `AudioController` and stamps its
  own RTTI class: `MusicAudioController`, `SebAudioController`, `SepAudioController`,
  `StreamAudioController`, `ShoutAudioController`. So `00210C00`'s fork is a choice between the
  **Seb** and **Sep** bank managers.
  **How the error was reached, because that is the useful part:** `00212760` (an `AudioController`
  destructor) sits four bytes from `00212950` and near `00210B30`, and it was the only class name in
  the neighbourhood. Attaching it to the singleton was address-adjacency reasoning wearing a class
  name — precisely the inference this database bans. It was caught by reading `00212710` and finding
  a layout that could not produce the accesses `00210A40` and `00210C00` actually make.
- *This document's own first version named `00249C60` `Audio_RequestSound_Gated` and `00249CA0`
  `Audio_RequestSound_Ungated`.* **Both are gated.** Each tests `DAT_02091098` — confirmed twice
  over, in the disassembly (`00249C64` and `00249CA4` both `CMP dword [0x02091098], 0`) and in the
  whole-image `DumpDataXrefs.java` run, which lists exactly three readers of that global and both
  wrappers among them. The difference between them is in the *resolver*, and the names have been
  corrected to `_WorldLiveResolve` / `_PlainResolve`, which is where the difference actually is.
  Recorded rather than quietly fixed because it is the dangerous kind of wrong name: it asserted a
  distinction that is not in the body, in a place where a real distinction exists one call deeper.
  Caught by `check_consistency.py` cross-checking this document against a peer's, within minutes of
  it landing.
- *This document's own first version called `0024A1A0` `Audio_StopRequest_Gated` and said it "routes
  to the stop/fade path".* Not proven. `002DF0F0` → `001DBE90` → `00210C50` was traced, but
  `00210C50`'s body was not read; "stop" came from the cleanup context of two of `002DF0F0`'s other
  callers, which is caller inference, not mechanism. Renamed and filed in §7.
- *"`00249C60` … Its complete body is five lines: `int id = ResolveSoundId();`"* — the prior
  document's pseudocode makes both the wrapper and the resolver nullary. Both take the bank-local
  index, and it is the wrapper's own first argument passed through in `ECX`. The reading was
  reachable because Ghidra's decompiler prints `FUN_003a1180()` with no arguments when it has no
  signature for the callee, and the pass-through is invisible in C.
- *"the pairing of a mid-scale 64 with a full-scale 127 is the shape of a volume-and-pan pair in a
  0–127 range"* — filed there explicitly as a hypothesis. The pair is confirmed and the volume's
  0–127 range is confirmed; **the pan's range is wrong**. The pan is a 0–255 byte with a branch at
  `0x80`. The reading was reachable because 64 is the midpoint of 0–127 as well as of 0–128, and
  both literals appear together at every call site; only the asymmetric masking distinguishes them,
  and that is invisible until the disassembly is read.
- *"`003A11F0` … id resolution for `00249CA0`"* with the two resolvers listed as the reason for a
  wrapper family — they resolve against the same globals with the same arithmetic. The family exists
  because of the world-live precondition, and because bit 30 and bit 31 of the id select other paths
  entirely.
- *"174 (upper bound — see §8)"* → **168**, per the table above.

## 9. Related

- [`what-the-engine-calls-to-make-a-sound.md`](what-the-engine-calls-to-make-a-sound.md) — the
  boundary census this document extends; establishes that `Boundary.Audio.NativeSupport` is a
  rejection bucket and that the GFZ carries unhonoured retractions
- [`../sqex-sd-sound-driver-architecture.md`](../sqex-sd-sound-driver-architecture.md) — the driver
  the two setters call into
- [`../sead-function-identification.md`](../sead-function-identification.md) — driver-side function identity
- [`../sead-engine-identity-and-diagnostics.md`](../sead-engine-identity-and-diagnostics.md) — driver-side diagnostics
- [`../Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md`](../Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md)
  — the bank/controller classes whose kind enum and vftables this document recovers
- [`../Sound-Selection/sound-trigger.md`](../Sound-Selection/sound-trigger.md) — selection above this seam
- [`../Sound-Selection/sound-variant-selection.md`](../Sound-Selection/sound-variant-selection.md) — variant choice above this seam
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the positive-control and
  GFZ-can-be-wrong rules this document applies

## 10. Falsification pass 1 — 2026-09-03, session `repos-9e`

**The first deliberate attempt to destroy this document**, by a session that did not write it, against
the GN158 checkpoint. **Ten claims overturned — three about the census (§10.1 below) and seven body
sizes (§10.2) — eleven survived, and two standing gate findings dispositioned as false positives
(§10.2, §10.3).**

This document is unusually resistant. Its machine-code listings are byte-exact, its RTTI table is
correct in every row, and three separate global reference counts reproduce to the function. **All
three failures are the same failure**: every population figure in it was measured over the call
graph, and the call graph omits the thunk layer.

### 10.1 Overturned — the census

**1. `00249C60` has 100 distinct non-Audio callers, not 99.** §2's headline count and §5's
`67 unowned / 29 UI / 3 Save_Load_Settings` split both come from `edges.tsv`, which has 99 rows for
this callee. A byte-level decode of every `E8`/`E9` in `.text` finds one more, verified at
instruction level:

```
0058066A   e8 f1 95 cc ff      call 00249C60          inside 0057FE80 (2,105 B)
context:   83 f8 01            cmp  eax, 1
           0f 85 e9 00 00 00   jne  +0xE9
           8d 48 01            lea  ecx, [rax+1]      <- builds the bank-local index
           e8 f1 95 cc ff      call 00249C60
```

`0057FE80` is unowned, so the corrected split is **68 unowned / 29 UI / 3 Save_Load_Settings = 100**.

> The call site is worth keeping for a second reason: `lea ecx,[rax+1]` immediately before the call
> **independently corroborates §2's central claim that `00249C60` takes its argument in `ECX`** —
> from a call site this document never saw.

**2. The inbound-surface census is a floor, not a count.** Every figure in §5 and §8 reproduces from
`edges.tsv` *exactly* — 174, six retractions in the set, 168, 305, 401. Re-derived from a byte-level
decode of the same population:

| | document (graph) | byte decode |
|---|---:|---:|
| Audio functions with ≥1 non-Audio caller | 174 | **188** |
| corrected surface after the 6 retractions | **168** | **182** |
| distinct non-Audio callers | **305** | **325** |
| inbound edges | **401** | **421** |

**The disagreement is one-directional for this population: the graph has 0 edges the byte decode
lacks**, so every figure in this document is a lower bound and the true values are about 8 % higher.

> **Over-drawn, corrected 2026-09-03 by the same session.** *"It never invents an edge, only omits"*
> was stated as a property of the instrument and is not one. Across the whole image the call graph
> holds **384 edges a direct `E8`/`E9` decode does not** — indirect and computed calls Ghidra
> resolved that a byte scan cannot see. **Neither route bounds the other in general**; they see
> different things. The zero above is real *for the non-Audio→Audio edges of this population*, which
> is why the figures here still move only upward — but the general claim was one population's result
> promoted to a rule. See
> [what the engine calls to make a sound §11](what-the-engine-calls-to-make-a-sound.md).

**3. The §8 correction went in one direction only.** *"The inbound surface is 168, not 174"* subtracts
six retracted functions from a figure §8 itself notes was "correctly labelled an upper bound". It is
also a **lower** bound, for an unrelated reason, and that correction was never applied. The number is
simultaneously an overcount and an undercount; only the overcount was found.

### The cause, named

Of the 20 non-Audio→Audio edges the graph omits, **19 are `JMP` tail calls and 17 of those come from
functions Ghidra itself names `thunk_FUN_…`**:

```
002DF2B0  thunk_FUN_001dba60   --JMP-->  001DBA60      002DF450  thunk_FUN_001dc130  --JMP-->  001DC130
002DED60  thunk_FUN_001dbbf0   --JMP-->  001DBBF0      002DF620  thunk_FUN_001dc240  --JMP-->  001DC240
002DF420  thunk_FUN_001dc0c0   --JMP-->  001DC0C0      ... 12 more in the same shape
0057FE80  FUN_0057fe80         --CALL->  00249C60      <- the only genuine CALL among the twenty
00355960  FUN_00355960         --JMP-->  003633B0      <- two non-thunk tail calls
```

**A thunk is a sink in the call graph** — the edge *out* of the thunk to its target is not recorded,
so the target's caller list omits the thunk, and the thunk's own callers never reach it. This
database documents exactly that in
[the thunk layer](../../24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md),
whose §1 calls it *"the single most common way a measurement of this binary comes out wrong."*

The thunks here are not Audio-owned while their targets are, so **each one adds a non-Audio caller
to an Audio function** — which is precisely the quantity this document's census counts.

### Survived — attacked and not broken

Recorded because an unrecorded audit did not happen. Everything below was re-derived from the image,
not re-read.

| Claim | How attacked | Result |
|---|---|---|
| `00249C60` is 51 bytes with that exact body | full body dumped and every displacement recomputed | **byte-exact**, including `lea r8d,[rdx+0x3f]` |
| the gate it tests is `02091098` | `83 3D` displacement resolved: `249C6B + 1E4742D` | **`02091098`** exactly |
| `00249CA0` is "the same 51 bytes with `003A11F0`" | both bodies dumped and both call targets computed | **exact** — same gate, resolver `003A11F0` |
| `002256B0` writes `0x7F` to `+0x1C`, `0x40` to `+0x20` | 44-byte body dumped | **exact** |
| `0016D6A0` is three bytes, `C2 00 00`, `ret 0` | body dumped | **exact** — and the document gives the bytes rather than saying "a ret" |
| `SeSep` is a 5-byte magic at `00917290` | bytes read | **exact** |
| the five bank kinds, vftables and constructors | each constructor searched for a `LEA` to its stated vftable and a `mov edx, kind` | **all five correct on both** |
| `02091098`: one writer, three readers image-wide | full RIP-relative scan, 13 instruction forms | **exact** — writer `00249FC0`, readers `00249C60`/`00249CA0`/`0024A1A0` |
| `022CB726`: written by three, read only by `003603C0` | same scan | **exact**, all four addresses |
| `0215EF4D`: "three writers set it to `0x7F`"; `002DE350` the only reader | same scan | **exact** — there are seven writers, and precisely three write the immediate `0x7F`. The sentence says what it means |
| `002DEC00` has 12 non-Audio callers | graph **and** bytes | **12 on both routes** |

**The `check_layout_units.py` finding on this document is a false positive, and it is dispositioned
here.** The gate has been reporting one suspect stride on this file continuously:

```
+0x14  u64  = 0xFFFFFFFFFFFFFFFF on reset (covers +0x14 and +0x18)
declared u64 (8 bytes) but next field starts 4 byte(s) later
```

The machine code settles it. `002256B0` opens with `48 c7 41 14 ff ff ff ff` — `mov qword [rcx+0x14], -1`,
which covers `+0x14`–`+0x1B` — and the next write is `c7 41 1c 7f 00 00 00`, a **dword at `+0x1C`**.
There is no write to `+0x18` at all. **So `+0x18` is genuinely inside the qword the reset clears, and
the document already says so in the row itself.** This is the checker's own documented legitimate
case — "deliberately overlapping views" — and the tool's header calls each hit a question rather than
a defect. It has been answered: **not a defect. The document was right and the gate was noise.**

### What this pass did not test

- **§4's formulas** — the pan/volume setters, the resolver arithmetic and the `SeSep` walk were read
  for structure but their constants were not re-derived from the bodies.
- **§2's music block**, `002DE360`'s 16-slot initialiser, and the claim that `00210C00` never selects
  slot `+0x00`.
- **The five controller constructors** and their pool constants.
- The `0016D6A0` reference census (2,479 / 2,867 / 2,511) — cited from a peer session and not
  re-derived here.

### The killer observations, named

- *The body listings would be false if any byte or displacement differed.* Every one was recomputed
  from the image; none did.
- *The reference counts would be false if a properly length-aware scan found different writers.* One
  did not — **but only after the scan was fixed.** The first version of it hardcoded the modrm `REG`
  field to `0` and so saw only `EAX`-sourced stores; it reported `02091098` as having **zero**
  writers. The control that caught it was requiring the scan to find the six writers of `0215EF44`
  this document names. **A scanner too narrow to see a `MOV [rip], ECX` would have "refuted" a claim
  that is true.**
- *The census would be false if a second route disagreed.* It did, in one direction, for a reason the
  database had already written down.

### 10.2 The seven body sizes — and the claim underneath them

A fresh `audit_crossrefs` run surfaced seven `BODY DRIFT` findings, all in this document's §3. **All
seven confirmed against the certified function list**, and the interesting part is not the numbers.

| address | §3 said | actual | delta |
|---|---:|---:|---:|
| `002105E0` `AudioRegistry_ctor` | 196 B | **231 B** | +35 |
| `00212710` `AudioController_ctor` | 66 B | **78 B** | +12 |
| `00217FD0` `MusicAudioController_ctor` | 46 B | **62 B** | +16 |
| `0021A9F0` `SebAudioController_ctor` | 66 B | **97 B** | +31 |
| `00219400` `SepAudioController_ctor` | 66 B | **97 B** | +31 |
| `0021CC10` `StreamAudioController_ctor` | 46 B | **62 B** | +16 |
| `0021BDB0` `ShoutAudioController_ctor` | 46 B | **62 B** | +16 |

**The deltas are not constant, and no measurement rule reproduces the claimed values.** Two
candidate mistakes were tested and both fail: measuring to the first return instruction would give
225 / 78 / 56 / 97 / 97 / 35 / 56, and there is no tail `JMP` in any of the seven. So these did not
come from a systematic mis-measurement of the current program — and §3's provenance sentence, *"exact
current body extents from a `DumpFullCoverageGraph.java` run against the GN checkpoint, reproduced
independently in this block"*, is **not true of these seven rows**. Where they did come from is not
established here; it is a question for the document's author.

**But three claimed sizes for seven functions is a grouping, and the grouping is the real claim.**
Tested directly:

| the group §3 implies | actual sizes | verdict |
|---|---|---|
| `00217FD0`, `0021CC10`, `0021BDB0` all "46 B" | all **62 B** | **holds** |
| `002105E0` alone at "196 B" | **231 B** | holds trivially |
| `00212710`, `0021A9F0`, `00219400` all "66 B" | **78**, 97, 97 | **breaks** |

**`00212710` is the base `AudioController` constructor and it is not the same size as the two derived
constructors the document grouped it with.** That is a claim about identity hiding inside a size
column, and it is the one that fails.

**The two groupings that survive are stronger than the document had them.** Byte-diffing confirms
these are genuine families, which §3 never says:

```
00217FD0 vs 0021BDB0 :   6 of 62 bytes differ
00217FD0 vs 0021CC10 :   6 of 62 bytes differ
00219400 vs 0021A9F0 :  12 of 97 bytes differ
```

Six differing bytes across 62 is a vftable displacement and a pool constant — **`MusicAudioController`,
`StreamAudioController` and `ShoutAudioController` are one emitted constructor specialised three
ways**, and `SebAudioController`/`SepAudioController` are a second such pair. The base at 78 B belongs
to neither family. **So the corrected picture is two constructor families and a base, where the
document had three sizes and an implied grouping that was one-third wrong.**

### 10.3a The deeper reason nothing references `02AEEDC8` — two origins for one table

**Re-derived 2026-09-12 (OPUS).** §10.3 is right that the checker's `BODYSIZE` complaint was an
artefact. But the address really is referenced by **nothing**: a controlled scan (`02AEEDC0` as the
positive control, which passes) finds **0 references to `02AEEDC8` image-wide**.

The cause is not a checker and not an error — **this document and the instructions use different
origins for the same table**:

| | base | the validating handle |
|---|---|---|
| the resolvers' own `lea` | **`02AEEDC0`** | `[base + slot*24 + 8]` and `+0xA` |
| §3 and §7 of this page | `02AEEDC8` | `+0` and `+2` |

`02AEEDC0 + 24N + 8` **is** `02AEEDC8 + 24N`, so the two descriptions cover the same bytes and
neither is wrong about the data. But **only `02AEEDC0` is an address the image computes**;
`02AEEDC8` is this page's chosen entry origin, and that is precisely why no instruction names it.
§9's corrected block and
[`CONTRACT-sound-request`](CONTRACT-sound-request.md) both use `02AEEDC0`, so the two documents
describe one table from two origins — **worth stating once here rather than leaving a reader to
discover it from a `24`-byte stride that starts in different places.**

### 10.3 The `GHOST ADDRESS` on `02AEEDC8` is a checker artefact

`audit_crossrefs` reports `02AEEDC8` as a cited address that is not a function. **It is not a
function, and this document never says it is.** It appears only in §3's *"Data addresses cited by this
document"* block, which the template requires and which this document has:

```
| Address    | Name            | Kind        | Contents                                    |
| 02AEEDC8   | bank-slot table | 24 B/entry  | +0 and +2 form the validating handle; ...   |
```

> **Resolved 2026-09-03 — the checker was wrong and has been fixed; this row was always correct.**
> `audit_crossrefs.py`'s `BODYSIZE` pattern ended in `\b`, which the `/` in `24 B/entry` satisfies, so
> **a stride written in a stride column parsed as a body extent.** The pattern now requires the size
> to end its cell. `24 B/entry` stands as written.
>
> **A retraction of my own, recorded because it is the more instructive half.** I first "fixed" this
> by rewording the cell to `24-byte entries` — which would have made the gate green **without
> changing a single claim**, on a row that was never wrong. That is silencing a checker, and the
> session that attacked this document declined to do exactly that, on the correct grounds that
> whether the tool or the document is wrong is a decision to make and not to route around. I made
> the wrong call and reverted it. **A gate turning green is not evidence that anything was
> repaired.**

The `Kind` column holds `u32`, `s8`, `pointer`, `u8, stride 0x288` for the other rows and
`24 B/entry` for this one — a **stride**, in the column meant for it. The checker matches the
`NN B` shape anywhere in the row and reads it as a body-extent claim.

**The document is compliant with the template and the finding is a false positive.** It is the second
such in this file: `check_layout_units.py` has also been reporting the `+0x14` voice-record stride on
every run all session, and §10 dispositions that one too. Neither should be corrected in the
document — writing `24-byte entries` instead of `24 B/entry` would silence the checker without
changing the claim, but that is a decision about the tool, not about the evidence, and it is left to
the coordinator. **What should not happen is the row being deleted or the stride removed to make a
gate go quiet.**

> Two gates have now been red on this document continuously, both falsely, and neither had been
> dispositioned before this pass. **An undispositioned false positive is not free: it is the noise a
> real finding hides in**, and this document was carrying seven genuine `BODY DRIFT` findings behind
> them the whole time.

## 11. Opened 2026-09-03 — `0020AC30`, and the engine reading meaning out of a bank's filename

`0020AC30` (572 B) was on the *located, never opened* list: cited by nine documents, including
[what-the-engine-calls-to-make-a-sound.md](what-the-engine-calls-to-make-a-sound.md), and by every one
of them **at its entry only**. It is opened here.

**Extent checked first.** The list came with a warning that this executable's decompiled output can
render a tail call as a body, so the function's end is not to be trusted from a rendering. Disassembled
from the image, `0020AC30` runs 151 instructions and **ends in `ret` at `0020AE6B` with no `jmp`
leaving its extent** — the hazard does not apply here, and that was measured rather than assumed.

### What it is

**A setter for one of five named audio bank slots, which derives two booleans from the name.**

```c
void AudioBank_SetSlotNameAndClassify(int slot /*ecx*/, string *name /*rdx*/)
{
    g_flagB = 0;  g_flagA = 0;                     /* 01F832E9, 01F832E8 */
    g_currentSlot = slot;                          /* 01DFE40C */
    if (slot > 4)              goto done;          /* five slots, 0..4 */
    if (!Validate(name))       goto done;
    tmp = MakeString(name);
    entry = 01F832F0 + slot * 32;                  /* 32 bytes per slot */
    if (lengths match && memcmp(entry, tmp) == 0) goto cleanup;   /* unchanged -> do nothing */
    if (*(dword*)(01F832B0 + slot*4) != 0) Release(slot);
    Assign(entry, tmp);                            /* store the new name */
    ...classify by substring...
done:
    g_currentSlot = -1;
}
```

### The classification is string matching on the filename

```asm
0020AD23  lea   r9,  [rip + 0x6fac62]   ; "sum_"  end
0020AD2A  lea   r8,  [rip + 0x6fac57]   ; "sum_"  begin
0020AD37  call  Find(begin, end, "sum_")
0020AD3F  je    else_branch             ; not found
0020AD50  lea   r8,  [rip + 0x6f055d]   ; ".json"
0020AD61  call  ...                     ; resolve a .json sidecar for this name
0020ADB8  lea   r8,  [rip + 0x6fabd1]   ; "0001"
0020ADC5  call  Find(...)
0020ADD6  mov   byte ptr [01F832E8], 1  ; found -> flag A
else_branch:
0020ADEB  lea   r8,  [rip + 0x6faba6]   ; "spc_"
0020ADF8  call  Find(...)
0020AE04  movzx ecx, byte ptr [01F832E9]
0020AE13  cmovne ecx, 1                 ; found -> flag B, otherwise KEEP the old value
0020AE16  mov   byte ptr [01F832E9], cl
```

**Four literals, all read from the image:** `"sum_"`, `".json"`, `"0001"`, `"spc_"`.

> **The engine decides audio behaviour from the name of the bank, not from a field inside it.** A bank
> whose name contains `sum_` is taken down a different path — including a `.json` sidecar lookup — from
> one containing `spc_`, and a `sum_` bank additionally carrying `0001` sets a flag that nothing else
> in this function sets. **Renaming a bank file changes what the engine does with it.**

### Three details worth carrying

- **An unchanged name is a no-op.** The lengths are compared and then `memcmp`; on a match the
  function jumps straight to cleanup without re-classifying or releasing. **Re-setting the same bank
  name costs nothing and clears no flag.**
- **Flag B is sticky, flag A is not.** Both are zeroed on entry, but flag B's write is
  `cmovne` against **its own current value**, so a `spc_` match sets it and a non-match leaves whatever
  the zeroing left. Flag A is written only on the positive path. Two flags in one function with two
  different update rules.
- **`01DFE40C` holds the slot index only for the duration of the call** and is set to `-1` on every
  exit path, including the early ones. **That is a "currently being set" indicator, not a record of the
  last slot used** — anything reading it outside this call sees `-1`.

### Addresses

| Address | What |
|---|---|
| `0020AC30` | the function |
| `01F832F0` | five slot name strings, **32 bytes per slot** |
| `01F832B0` | per-slot dword; nonzero means a release runs before reassignment |
| `01DFE40C` | the in-progress slot index; `-1` at rest |
| `01F832E8` | flag A — set by `sum_` **and** `0001` |
| `01F832E9` | flag B — sticky, set by `spc_` |
| `00905988` / `00905990` / `00905998` / `008FB2B4` | `"sum_"`, `"0001"`, `"spc_"`, `".json"` |

### What is not established

- [x] ~~**UQ-246.** What flags A and B **do**. They are set here and read elsewhere; no reader was traced.~~
      **UQ-246 ANSWERED 2026-09-15 (FABLE): they gate whether an actor's script yields for the frame after the
      script VM runs a step — and the reader set is closed, not merely untraced.**
      - **The chain, derived here independently and then found to agree with an existing page.** Each flag byte
        has exactly one accessor: `0020AA40` (8 B) reads flag A `01F832E8`, `0020AA30` (8 B) reads flag B
        `01F832E9`. Each accessor has exactly one caller, a zero-extending pass-through: `001EC5E0` for A and
        `001EC5C0` for B. **The consumers are four functions across seven call sites** —
        `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`, both flags: `0025E0F0`, `0025E100`),
        `0034CF90` (both), `0034D790` (both) and `00180120` (**flag B only**, `00180124`). That is **3 for A**
        and **4 for B**, which is what
        [the cutscene name slots page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
        §10 counted when it answered the *effect* on 2026-09-03: a `spc_` bank's flag B **suppresses** one stop
        condition in world states 1–2, and a `sum_…0001` bank's flag A **enables** one in state 3.
      - **Why "no reader was traced" can now be replaced by "the reader set is closed".** Three scans, each with
        its own blind spot, and they agree:
        1. a rip-relative scan of `.text` over `01F832E8`–`01F832E9` finds **three** functions — the setter
           `0020AC30` on this page and the two accessors;
        2. a byte-level `rel32` `call`/`jmp` decode finds **one** caller for each accessor and **4 / 3** for the
           two wrappers;
        3. a search of the **whole mapped image** for an 8-byte or 4-byte little-endian pointer to any of
           `0020AA30`, `0020AA40`, `001EC5C0`, `001EC5E0` finds **none** — so no vtable, function table or
           static registration reaches them indirectly.
        **The bound:** a read through an address computed at run time, or a call through a pointer assembled
        rather than stored, would be invisible to all three. Nothing suggests either here, and the flags are
        one byte each in `.data`.
      - **Consequence for another page, routed rather than applied.** `UQ-336` asks whether the two consumers it
        named exhaust the set, and says reading `0034CF90`, `0034D790` and `00180120` *"does not account for all
        seven"*. The seven are **call sites, not functions**: `0025DF00` × 2, `0034CF90` × 2, `0034D790` × 2 and
        `00180120` × 1, and all four functions are read. That page is uncommitted in a peer's working tree, so
        the finding is filed to its owner instead of edited in here.
- [x] ~~**UQ-247.** What the `.json` sidecar is used for on the `sum_` path — two calls consume it and were not
      followed.~~ **UQ-247 ANSWERED 2026-09-15 (FABLE): it is the cutscene depth-of-field sidecar, and the two
      calls are a string concatenation and a two-key read.**
      - **The two calls, named.** `0020AD61` is `001B31E0(out, bankName, ".json")` — a plain append of the
        bank name and the literal, returning `out` (`001B3254`/`001B3265`, two `001A52A0` appends). `0020AD6A`
        is `001C5750(thatString)`, 467 B, the consumer.
      - **What the consumer does.** `001C5750` prefixes the literal `"JsonData/CutScenes/"` (`008F9E70`, `0x13`
        bytes at `001C5802`–`001C581C`), appends the name, parses that file into a JSON value (`001FE8B0`
        then `00200BF0` at `001C5841`), and reads **exactly two keys**: `Common.mDofApertureFnumber` and
        `Common.mDofFocusDistance` (`001C5853`–`001C589F`). **So the sidecar is not an audio file at all** —
        it is the same per-cutscene render-settings document
        ([the ordered render command list](../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md)
        §7, `UQ-232`), reached here by bank name rather than by scene name.
      - **Where the two numbers go.** `00194250(ctx, dl, xmm2, xmm3, …)` writes the enable byte `+0x110 = dl`,
        `+0x114 = focus distance`, `+0x118 = aperture f-number`, `+0x11C` = the value it just read back from
        `+0x11C` (preserved) and `+0x120` = the constant `35.0f` at `008F312C`. `ctx` is `[01F81300]`, which
        `0015CAF0` sets to `00193D50()` — **the same `0x4A8`-byte post-process parameter context cached at
        `01F7F5F0`** that `UQ-233` is about. Those five offsets are therefore a contribution to that field map.
      - **The call is unconditional and `dl` is `1`.** `001C5750` does not test whether the parse produced
        anything before calling `00194250` with `dl = 1` (`001C58BE`).
      - **What that means for the shipped `sum_` banks, measured.** Of the 337 files in
        `JsonData/CutScenes/`, the summon scenes' `0000` and `0002` sidecars are **26 zero-byte files** —
        `sum_a0000.json`, `sum_a0002.json` … `sum_m0002.json`, one pair per Esper letter `a`–`m`. Their
        `0001` siblings are real (5,396–7,164 B), and so is `spc_z0000.json` (4,656 B). For an empty file the
        parse yields nothing; `001FF740` → `001FF6B0` is a **mutating `operator[]`** — on a node that is not
        type `3` it destroys it, makes it an empty EASTL map and inserts the missing key — so the lookups
        succeed structurally and return a **null** node, and `00200B50` returns `0.0f` for any type that is
        not `1` (int) or `2` (double). **So on those 26 banks the engine enables depth of field with an
        aperture and a focus distance of zero.** What the shader does with a zero aperture is **not read
        here**, so no visual consequence is claimed — only that the values are zero and the enable byte is set.
      - **Not established:** whether any other consumer of `01F81300 +0x110`–`+0x120` overwrites these in the
        same frame, and what `sum_` abbreviates (that stays `UQ-249`).
- [x] ~~**UQ-248.** What the five slots mean, and whether the index is a category or a priority.~~
      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): neither. The slot is the actor-manager index 0–4,
      and the name is the resource that manager is loading.** `0020AC30` has one caller, through its
      thunk `001EC660`: `ActorResource_BeginManagerResourceSetLoad` at `0032FD64`. It passes
      `ecx = edi`, the manager index, and `rdx` = the path it just resolved with `002DF980(kind, index)`:
      - manager 0: path kind 5 at `3 × field id`, the map's `.ebp`;
      - managers 1–3: kind 8 at `4 × set id`, an event script. That table holds the `sum_a0000` …
        summon events that `UQ-249` names.
      - manager 4: kind 1 at `set id + 0x6B`, the `obj_finish\…\*.ca` files.

      So "slot" means "which actor manager". The `sum_`/`spc_` flags classify whichever event script a
      manager has just loaded. Read at `0032FD19`–`0032FD64` and in the five-kind store block of
      `ResourcePath_Init`. The "voice-pack slots" wording in §5a is corrected there.
- [x] ~~**UQ-249.** What `sum_`, `spc_` and `0001` stand for. The obvious expansions are guesses and are not made
      here; **the evidence is that the strings are matched, not what they abbreviate.**~~
      **ANSWERED 2026-09-22 (FABLE) from the shipped sidecars — and this bullet's caution was right.**
      They are cutscene-name families in `jsondata/cutscenes/` (337 sidecars). `sum_` is 13 groups
      `a`…`m` × 3 sequences, of which **only the `0001` file is non-empty** — all 26 zero-byte sidecars
      in the corpus are `sum_` at `0000`/`0002` — **so `"0001"` is matched because it is the only slot
      that ships data**, not because of what it abbreviates. `spc_z0000` is non-empty at `0000`, which
      is why that branch never tests `0001`. *The expansions remain a reading and are labelled as one.*
      See [the cutscene name slots](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md).

## 12. Opened 2026-09-03 — `007E5160`, `Sd::Driver::RandomSound` slot 43, and a false positive of a second kind

`007E5160` (1,400 B) came off the *leaned on and never opened* cut with **six citing documents**. **Five
of the six are table rows.** `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` is a
2,645-line index that lists it as `Sd::Driver::RandomSound`, **vtable slot 43** — a row that *locates*
the function and makes no claim about its behaviour.

> **That is a false positive of a different kind from `0022A0B0`.** There the proxy misfired because a
> function had been read without an interior citation. **Here the cut's "cited by N documents" is
> satisfied by an index**, and an index does not lean on anything. **Both are worth having found: the
> cut's two failure modes are now instances rather than predictions.**

**But the function itself was genuinely unread, and the index row is what made it worth reading** — a
class and a slot number are a much better starting point than an address.

**Extent checked**: 364 instructions, ends `ret` at `007E56D7`, **no `jmp` leaves the extent**.

### What it does

~~**It walks the driver's sequence list and reports every entry it cannot resolve.**~~

> **CORRECTED 2026-09-18 (FABLE): this is the selection method, not a validation pass, and the error string is not its.**
> The reading below rested on two adjacencies. (1) `01CB4D58` was taken for an *error descriptor* because the
> string `[sead][!!error!!]sequence NULL!!` begins at `01CB4D60`, eight bytes after it. `01CB4D58` is a one-slot
> vtable (its slot is the 43-byte deleting destructor that also serves `01CB4D48`), and its complete-object locator
> names **`SQEX::Sd::SabFile::Sequence`**; the string simply follows it in `.rdata`. The string's one rip-relative
> reference is at `007B5444`, in the audio tick's walk of the active sequence list (head `02EAD620`): a node whose
> sequence pointer `+0x20` is null takes that arm, which formats the string with the list object `02EAD600`.
> Nothing in this method touches it. (2) `007CF9C0` was read as *did it resolve?*. It returns the
> resolved record's **weight byte** (`+4` up to version 2, `+0x10` from version 3), and `007BD240` is the **sound
> trigger**, the common play entry. So the loop quoted here is pass 1 of `RandomSound::Select`: **every entry whose
> weight is 0 is played**, and the weighted entries go on to the `rand() % 101` draw; the whole method is set out on
> [the sound-variant page](../Sound-Selection/sound-variant-selection.md) §12. The instruction listing below is
> exact; its comments *did it resolve*, *error descriptor* and *report* are the superseded reading and are kept as
> written. What survives: the list at `this+0x30`, the byte count at `+5`, the `u16` at element `+4`, and the
> five-function accessor family.

```asm
007E51C9  mov   rax, qword ptr [r15 + 0x30]     ; the list object
007E51CD  lea   rcx, [rip + …]                  ; -> 01CB43E0, an accessor vtable
007E51DA  mov   qword ptr [rbp - 0x39], rcx     ; {vtable, data} pair on the stack
007E51F5  cmp   byte ptr [rax + 5], sil         ; count, a BYTE at +5 of the list
007E51F9  jbe   0x7e5325                        ; empty -> nothing to do
007E520B  call  0x7cfac0                        ; element(index) via the accessor pair
007E5214  mov   rcx, qword ptr [rax + 8]
007E5226  movzx r8d, word ptr [rcx + 4]         ; a u16 id from the element
007E522F  call  0x7cf9e0                        ; resolve it
007E523B  call  0x7cf9c0                        ; did it resolve?
007E5242  jne   0x7e525f                        ; yes -> next
007E5256  mov   qword ptr [rbp - 9], rbx        ; no  -> the error descriptor at 01CB4D58
007E525A  call  0x7bd240                        ; report
```

The descriptor at `01CB4D58` carries the format string, read from the image:

```
[sead][!!error!!]sequence NULL!! listaddr:0x%p
```

~~**So slot 43 is a validation pass**: for each entry in the list at `this+0x30`, resolve a `u16` id, and
on failure emit a `sead` error naming the list address.~~ *(Superseded, see the correction above: slot 43 is the
class's selection method, and this loop plays the zero-weight entries.)* The loop count is a **byte** at `+5` of the
list object, so the list is bounded at 255 entries by its own header.

### Two things worth carrying

- **The `sead` diagnostic layer is present and reachable in the shipped executable.** This is a
  retail build emitting a formatted engine-error string on a data fault, not a stripped one — the
  message and its `%p` argument are both in the image. *(2026-09-18: true of the image, but the emitter is the
  sequence-list update called from the audio tick, not this method; see the correction above.)*
- **`0x7CF9A0`, `0x7CF9C0`, `0x7CF9E0`, `0x7CFA30`, `0x7CFAC0`** are a five-function accessor family,
  27–135 bytes each, called 29 times between them from this one method. They are the container API
  this driver code is written against, and **all five are unnamed.** *(2026-09-18: the RTTI of the descriptors
  they return names their classes: `007CFA30` yields a `SabFile::SequenceChunk`, `007CFAC0` a
  `SabFile::SoundSequenceInfo`, `007CF9E0` a `SabFile::Sequence`; `007CF9A0` and `007CF9C0` are `Sequence`'s
  group and weight getters.)*

### What is not established

- [x] ~~**UQ-250.** What the `u16` at element `+4` indexes, and what `0x7CF9E0` resolves it against.~~
      **ANSWERED 2026-09-18 (FABLE): it is the index of a sequence record in the bank's `seq ` chunk, and `007CF9E0` is the chunk's get-by-index.** The context the resolver is handed is built by `007CFA30`, which walks the bank header's 16-byte chunk directory for the tag `seq ` (`01CB6EE0`, `007CFA80`..`007CFA97`) and returns the pair {`01CB6EA0`, chunk}; the RTTI behind `01CB6EA0` is `SQEX::Sd::SabFile::SequenceChunk`. `007CF9E0` (77 B, read whole) rejects a negative index or one at or above the chunk's `u16 +4` count (`007CF9E0`..`007CF9F1`), otherwise reads the `u32` at chunk + `u16 [+2]` + 4 * index and adds it to the chunk base (`007CF9F3`..`007CFA09`), and returns the pair {`01CB4D58`, record}, or {`01CB4D58`, 0} on rejection; the RTTI behind `01CB4D58` is `SQEX::Sd::SabFile::Sequence`. So the element (a 16-byte `SabFile::SoundSequenceInfo`, `01CB6E40`) names its candidate sequence by ordinal within the same bank. The same placement was reached from the data side on [the sound-variant page](../Sound-Selection/sound-variant-selection.md) (G-2, 2026-09-18), where the census finds every shipped list is one entry long. Static: both accessors read whole, RTTI names read from the complete-object locators.
- [x] ~~**UQ-251.** Whether slot 43 is called at load time or on demand — **no caller was traced**; the vtable index
      locates the slot but not its invocation.~~
      **Answered 2026-09-14 (FABLE): on demand, once per sound instance, when the instance dispatches.** Image-wide in the
      audio range there is exactly one call through vtable `+0x158` (slot 43), in the 274-byte sound-instance stepper (the
      function the trigger page's state table calls *the stepper*).
      - **When it runs.** In states 1–3 the stepper first checks the bank from `+0x30` byte `+6`.
        - A missing bank or a negative status sends the instance to state 7.
        - Status 1 also goes to 7.
        - Status 2 parks the instance in state 3 for the next update.
        - Only any other status, or an instance already past state 3, falls through to the dispatch step.
      - **When it does not.** It skips the call when the held path applies: the object from `+0x20` answers 2 and
        the held-dispatch call fails, or mode `+0x58` is 2. Either way the state goes to 4.
      - **What follows.** Right after slot 43, the stepper sets state 5 and notifies the `+0x38` listener
        .
      - **Who drives the stepper.** It has two callers: the sound's per-update slot (42) and one other body.
      - **So** the selection pass in slot 43 (called a validation pass on this page until 2026-09-18) is part of starting a sound, not of loading its bank. The
        state table on [the sound trigger page](../Sound-Selection/sound-trigger.md) records the same step as *dispatched (live)*.
- [x] ~~What the other three `{vtable, data}` descriptors used here (`01CB5A00`, `01CB4D48`, and the
      accessor at `01CB43E0`) are for; only the error one was identified, by its string.~~
      **ANSWERED 2026-09-13 (OPUS): all three carry MSVC RTTI, and their type descriptors name them
      outright. They are SAB file-format reader classes.**

      | descriptor | RTTI type descriptor | demangled |
      |---|---|---|
      | `01CB43E0` | `.?AVSound@SabFile@Sd@SQEX@@` | **`SQEX::Sd::SabFile::Sound`** |
      | `01CB4D48` | `.?AV?$BaseClass@USABSEQUENCEHEADER@Sd@SQEX@@@AudioBinaryFile@Sd@SQEX@@` | **`SQEX::Sd::AudioBinaryFile::BaseClass<SABSEQUENCEHEADER>`** |
      | `01CB5A00` | `.?AV?$BaseClass@USABSOUNDSEQUENCEINFO@Sd@SQEX@@@AudioBinaryFile@Sd@SQEX@@` | **`SQEX::Sd::AudioBinaryFile::BaseClass<SABSOUNDSEQUENCEINFO>`** |
      | `01CB43D0` | `.?AV?$BaseClass@USABSOUNDHEADER@Sd@SQEX@@@AudioBinaryFile@Sd@SQEX@@` | **`SQEX::Sd::AudioBinaryFile::BaseClass<SABSOUNDHEADER>`** — a **fourth**, adjacent to `01CB43E0` and not in this bullet |

      **So the group is one template over three SAB record types** — `SABSOUNDHEADER`,
      `SABSEQUENCEHEADER`, `SABSOUNDSEQUENCEINFO` — plus the `SabFile::Sound` accessor. Every one is
      `SQEX::Sd`, the sound driver's own namespace, which is also what the `[sead]` tag in the
      neighbouring error string abbreviates.
      **The route, because it generalises past this page.** Each vtable's **complete-object locator**
      sits one qword *before* slot 0; its `+0x0C` is the RVA of a type descriptor whose name begins
      at `+0x10`. `007A5F80` and its siblings are the scalar-deleting destructors that install these
      vtables (`mov [rcx], rax` then `test dl, 1`), which is how the pairs were reachable at all.
      > **THIS BULLET SAYS THE ERROR ONE WAS IDENTIFIED "BY ITS STRING".** A format string is a lucky
      > break; **RTTI is a name the compiler was obliged to emit**, and it names all four without
      > needing one. Where a descriptor has a vtable, read the locator before hunting for literals.
      **Not established:** the layout of the three SAB record types, and what `SabFile::Sound`
      exposes. **These are names, not structures.**
- [x] ~~**UQ-252.** **The count byte at `+5` here is unrelated to the battle-record kind byte at `+5`** documented in~~
      *Withdrawn as a question 2026-09-14 (FABLE): this box records a disambiguation, not an unknown. The two bytes are
      shown to be different fields of different structures; the note stays below as written.*
      `04-Actor-Entity`. Same offset, different structure, and **no connection is claimed**.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Two corrections, both propagated from the contract's own pass rather than found afresh here.

**The resolver count.** §9's scope-correction block said *"four resolvers over three handles"*. There
are **five**: `003A1240` runs the same `entry[+8] × 512 + localIndex` on the same table with the same
handle validation and the same provably dead sign test. **It was missed because every other resolver
names one of the three handle globals and this one takes its handle as a parameter** — a census keyed
on the data cannot find a function that never names the data. Corrected in place.

**The table's origin.** `02AEEDC8` has **zero** references image-wide (controlled scan, `02AEEDC0`
passing). §10.3 attributes the checker's complaint to a `BODYSIZE` regex artefact, which is true but
not the whole reason: this page takes the entry origin **eight bytes past the address the resolvers'
`lea` computes**, describing the handle at `+0`/`+2` where the instructions read `+8`/`+0xA`. Both
descriptions cover the same bytes — `02AEEDC0 + 24N + 8 = 02AEEDC8 + 24N` — but only `02AEEDC0` is an
address the image ever forms. Recorded as §10.3a.

**Not claimed:** nothing else in this page was re-derived, and the runtime evidence it carries is
untouched.

## The `0020AC30` exclusive subtree — the slot setter's 24 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 24 frontier functions to `0020AC30`
(`AudioBank_SetSlotNameAndClassify`, §11). All signature-swept 2026-09-15 (`bshape.py`); the
tree is the `0020xxxx` object-model band beneath it:

| cluster | members | role |
|---|---|---|
| object registrar | `0020A800` (554 B — `00203E60`/`001AA6C0`/`00206B70`/`00209780`/`00203F70`/`00209530`/`00206AD0`/`00209AD0`/`00203790`, `[r8]`/`[rax+0x10]`/`[rax]` indirect, `008C2448`/`00905958`/`85`) | the register call that pairs the name with the bank object |
| `008C24xx`/`008C26xx` triples | `0020A2D0`/`0020A3D0` (252 B twins — `00209000`/`00209090` + `002038A0`/`002038D0`, `008C2618`/`008F6820`), `0020A4D0` (`00209290` + `00203900`), `00209000`/`00209090` (144 B twins — `002099D0`/`00209B50` + rip-indirect), `00209290` (200 B — `008C2618`/`008F6820`), `00209A50` (`00210EC0` ×2 + four rip-indirects, `008C2608`/`008C2DA8`), `00207FB0` (281 B — `00210EC0`/`0020A020`/`00195200`, `008C2458`–`80`/`00905888`), `0020A020` (457 B — `00210EB0` ×2 + `001A5630`/`001A4C90`, **eight** rip-indirect calls, `008C2DA8`) | the object's method-table install — same rip-indirect shape as the config cluster's `001DE5D0` (whose indirect calls resolved to IAT thunks, not a table fill — corrected 2026-09-17) |
| resolve/fetch chain | `002035B0` (475 B — `0020A4D0` ×2 + `0020A5C0`/`0020A2D0`/`00208710` — interior read 2026-09-17, SWE2-FRONTIER: 1,275 B, carries the `a-zA-Z0-9_` alphabet table, `002032E0` ×2 at [`002088FF`](../../_index/ADDRESS-INDEX.md) and a self-call at `0020897C` (two-stage name lookup)), `00203790` (`002044C0` ×2 + `00204010`/`002035B0`/`00209B50`), `00204010` (`00206B70` ×2/`0020A3D0`), `00206AD0` (`00205D60`/`00206D30`/`00207E90`/`00208C60`/`002060C0`, `008C2430`), `00209120` (`00209A50`/`00203940`/`00209BC0`), `002060C0` (221 B — calls itself twice; a two-stage retry) | intermediate lookups between the registrar and the leaf accessors |
| record materializer | `001C5750` (467 B — `001FF740` ×4 + `001EDF00`/`00200B50` ×2 + `001A52A0`/`001FE8B0`/`00200BF0`/`00193D50`/`00194250`/`001FEA00`, templates `008F9E70`/`83`, `008FA3CC`), `0020AA50` (476 B — `001EDF00` ×2 + `001A9E50`, `02EBA2E0`/`E1` pair) | two record builders on the `008F9Exx`/`008FA3xx` templates |
| leaves | `002038A0`, `002038D0`, `00203900`, `00203940`, `00203E60` (263 B — `00207FB0`/`00861ECC`/`00808850`, `008C2580`–`008C2630`/`008F3618`), `00203F70` (`009058D0`) | small bodies, `008C2xxx` string/const bank readers |

The pattern matches §11's shape: the setter stores a name and derives two booleans — everything
beneath it is object bookkeeping (`0020A800`'s register call → the `0020Axxx` method-table fills
→ `001C5750`/`0020AA50` record materialization), not audio logic.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Party — CLIENT.**
  - The 25-byte `002671F0` is read by `PartyFocus_UpdatePrimarySecondaryActorProcessing`,
    `PartyFocus_ClearCurrentActorIfEligible` and `PartyControl_UpdateControlledActorLocomotion`.
  - The per-slot availability test `00267330` is read by `PartyFocus_TryGetCurrentActorWorldPosition` and
    `PartyControl_ApplyAnalogLocomotionToActor`.

  **Party control asks the same per-slot state the voice path asks.**
- **Platform — SERVICE and MECHANICAL.**
  - `00223190` and `00224570` ask the 78-byte QPC seconds timer.
  - `00219400` / `0021A9F0` call a 63-byte helper.
  - The retracted `00225690` is read by four Platform bodies.
  - The `std::string` append `001A5630` is shared with the GPU-id parser (1,512 B), the MAC formatter (758 B) and the
    Steam language query (832 B, **PlatformOnlineAchievements**).
- **Developer — CLIENT.** `001FE8B0` and `001FEA00` are read by the 1,046-byte `MultipleDebugDisplay` update, and
  `00200B50` by the 2,261-byte Developer body.
- **Input and Movement — CLIENT and SERVICE.**
  - The retracted getters `00225570` / `00225680` are read by 21- and 25-byte Input helpers.
  - The manager-slot readers `00267310` / `00267360` are read by the 1,002-byte Input body. `00267310` is also read by
    `Movement_UpdateSteeringTowardTarget` and a 935-byte movement body.
  - The boot and area initialisers call the Input initialisers and three movement helpers.
  - `0027F5D0` and `002D6F90` call small Input helpers.
- **Items_Equipment_Shops_License — SERVICE.** `BattleFormula_ApplyTargetResult` grants items through the item write.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — SERVICE and CLIENT.** `BattleFormula_ApplyTargetResult` calls three status bodies (`BattleStats_RecomputeDerivedStateAndAutoStatuses`, `BattleStats_ChangeStatusAndProcessSideEffects`, `BattleStats_ModifyStatusLayerStateAndProcessSideEffects`), and is called by two of them and by `BattleUnit_RunPeriodicCombatMaintenance`. `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` also calls the recompute.

**Presentation — CLIENT (SWE2-EC7-158, 97 edges).** The boundary's helpers exchange calls with the render side — `00180120` calls `001EC560`, `00182E80` is called by `00186CD0`/`00187950`/`002DB0..` — the voice path consults presentation state, not a shared responsibility.

**Resource — CLIENT (SWE2-EC7-158, 117 edges).** Batch-123's `001A9E50` names the shared container helpers `001EDF00`/`001A4BF0`, whose callers (`001AD130` for `001A4BF0`, `001A7A50`/`0019F490`/`0020B150` among them) sit on the resource layer — shared fan-in, no second owner.

## The `002DF070` exclusive subtree — the `SeSep` walk and its record factory (SWE2-FRONTIER, exclusive-subtrees package)

`002DF070` (`SepBank_WalkChunks`, 124 B) is the container walk this page describes
at §`00917290`: `edi = (bankLength + 0xF) & ~0xF`, then per 16-byte record header —
dword magic `SeSep` (`00917290`), byte `+4` version (`00917294`), dword `+8` the
sound id handed on, dword `+0xC` chunk length with bit 31 masked off — it calls
`001DBE60(id, payload)` and advances `rbx += length`, stopping when the rounded
remainder drops to `≤ 0x10` or a header fails the magic/version/size test.

| member | role | interior |
| --- | --- | --- |
| `001DBE60` (43 B) | per-chunk adapter — `00210B30()` obtains the bank-context object, then tails into `00210C40(obj, id, payload)` | [`001DBE85`](../../_index/ADDRESS-INDEX.md) |
| `00210C40` (9 B) | one hop — `rcx = [obj + 0x10]` then tails into `0021A040`; the list the records live in hangs off `+0x10` | [`00210C44`](../../_index/ADDRESS-INDEX.md) |
| `0021A040` (182 B) | find-or-create — walks the intrusive list at `[ctx + 8]` for an element whose `[elem + 0x10] + 0x38` equals the sound id; on a miss, when `002129F0` reports capacity and the payload is non-null, calls the context vtable `+0x30` factory and hands the fresh object to `00222DC0` | [`0021A0A9`](../../_index/ADDRESS-INDEX.md) |
| `00222DC0` (346 B) | record constructor — asserts `[+0x50] == 0` and `[+0x38] == -1` via `0016D6A0`, stores `+0x28` = capacity count, `+0x3C` = `id / 100` (the `0x10624DD3` magic divide — the bank/section group), copies the chunk's two dwords + version byte into `+0x40`–`+0x49`, `+0x38` = id, `+0x30` = 1; formats a debug name through `0017D2E0` using templates `00908998`/`009089A8`, then allocates a registration record via `002125E0`/`002120E0` (`[+0]=1`, `[+8]` = callback `00222200`, `[+0x10]` = parent, `[+0x18]=1`, `[+0x20]` a `0x100`-byte string copy, `[+0x120]` = `&parent + 0x50`) and links it through `002121C0` | [`00222E31`](../../_index/ADDRESS-INDEX.md) |

Shared callees — deliberately outside the census: `00210B30`, `002129F0`,
`00212A70`, `0016D6A0`, `0017D2E0`, `002125E0`/`002120E0`/`002121C0`, `00808C40`.
The `id / 100` group at `+0x3C` is measured (`imul 0x10624DD3`, `sar 6`, sign
fixup — round-toward-zero divide by 100).


## Interior citation — frontier hubs `00195200`, `002DEE80` (2026-09-18, SWE2-EC7)

`00195200` — 133 B, 68 callers; the sized-delete validation body behind the `008C2DA8`
IAT slot this page's object-install row names. Interior verified: `[rcx+0x18]` is the
recorded size (`0019520D`), `+1` must stay under `0x1000` (`00195219`), and three header
checks — alignment `cl & 0x1F`, block-start `[rcx-8] >= rcx`, header distance `<= 0x27` —
each call the `008C2DA8` report import on failure ([`00195226`/`00195236`/`00195246`/`00195253`](../../_index/ADDRESS-INDEX.md))
then `int3`. The CRT's sized-delete fast path with its own corruption tripwires.

`002DEE80` — 11 B, 15 callers; the conditional sound-call tail. Interior verified:
`test ecx, ecx; jne 001DBCE0` at [`002DEE82`](../../_index/ADDRESS-INDEX.md) — a nonzero
sound handle forwards to the Audio `001DBCE0`; zero returns 0. The guard in front of the
voice-verbs' poll.

### Interior citation — frontier hubs 001A9E10, 002DF0F0 (2026-09-18, SWE2-EC7)

Two hubs the request path's helpers call:

- **001A9E10** (35 B, 4 A-measured callers) — `basic_string` assign: initialises a string header (`+0x18/+0x19/+0x1A` zeroed, `+0x1C = 0x10` SBO size) then `001A5500` — batch-14's MSVC insert — to fill it. The support-record names the request builder stages. Anchor [`001A9E33`](../../_index/ADDRESS-INDEX.md).
- **002DF0F0** (41 B, 4 A-measured callers) — the arg swizzle: `edx == -1` → all-zero + `jmp 001DBE90`; else `r8d = edx` with bit 31 cleared (`btr`), `ecx = sign(edx)`, tail `001DBE90` — normalises a channel index before the voice allocator sees it. Anchor [`002DF10A`](../../_index/ADDRESS-INDEX.md).

## SWE2-EC7-27 update (2026-09-18) — `002DF530` `Audio_SetMode` confirmed

`002DF530` (34 B) is the function this page names `Audio_SetMode`:
clamps `ecx` into `[0, 2]` (negative -> 0, `> 2` -> 2), loads
`dword[0215EF44]` as `rcx`, and tail-jumps `001DBAC0` with the clamped
mode in `edx`. Interior anchor `002DF53F` (the `cmovg` clamp).

## SWE2-EC7-37 update (2026-09-19) - `0020A800`

`0020A800` (554 B) is the object registrar the page names - `008C2448`/`00905958`/`00905985`, the `plan_master\<name>\event` regex, `00203E60`/`001AA6C0`/`00206B70`/`00209780`/`00203F70`/`00209530`/`00206AD0`/`00209AD0`/`00203790`. Interior anchor `0020A849` (a `00203E60` call).

## SWE2-EC7-38 update (2026-09-19) - `0020AA50`

`0020AA50` (476 B) is the record materializer the page names - `008F6600`/`02EBA2E0`/`02EBA2E1`, `"EASTL basic_string"`, `001EDF00` pair plus `001A9E50`. Interior anchor `0020AA89` (an `001EDF00` call).

## SWE2-EC7-38 update (2026-09-19) - `002035B0`

`002035B0` (475 B) is an audio-boundary body - `0020A4D0` pair plus `0020A5C0`/`0020A2D0`/`00208710`. Interior anchor `002035D8` (an `0020A4D0` call).

## SWE2-EC7-38 update (2026-09-19) - `0020A020`

`0020A020` (457 B) is a sound-request sibling - `008C2DA8` octet/`01F44830`, `00210EB0` pair plus `001A5630`/`001A4C90`/`00808C40`. Interior anchor `0020A0B2` (an `001A5630` call).

## SWE2-EC7-39 update (2026-09-19) - `00209530`

`00209530` (432 B) is a sound-request body - `00205C30` pair plus `008C2A10` thunk and `002086D0`. Interior anchor `00209564` (an `008C2A10` thunk call).

## SWE2-EC7-39 update (2026-09-19) - `0020A5C0`

`0020A5C0` (407 B) is a sound-request sibling - `00208220`/`00209E00`. Interior anchor `0020A659` (a `00208220` call).

## SWE2-EC7-41 update (2026-09-19) - `00206D30`

`00206D30` (350 B) is a sound-request body - `009058C0`, `00205890` pair/`00208C60`/`00207E90` pair/`00205DF0`/`00209530`/`00210EC0`. Interior anchor `00206D3F` (an `00205890` call).

## SWE2-EC7-41 update (2026-09-19) - `0027EA70`

`0027EA70` (328 B) is a sound-request body - `01E0C2A4`/`0209AC20`/`0209AC30`/`02F9736A`, `002470D0`/`002F9860` pair/`0020E620` pair/`002814E0`/`00249C60`/`002CA110`. Interior anchor `0027EAB8` (a `002470D0` call).

## SWE2-EC7-42 update (2026-09-19) - `002D3A50`

`002D3A50` (324 B) is a sound-request body - `01E0CF84`/`01E0CF88`/`0209E65C`/`02F97390`, `001E0E30`/`001E0A10`/`002D0580`/`002D3BA0` pair/`002D4F10`. Interior anchor `002D3A7B` (an `001E0E30` call).

## SWE2-EC7-42 update (2026-09-19) - `00361200`

`00361200` (306 B) is a sound-request body - `022CB9F0`/`022CB9F1`/`022CBA51`, `002DEE50`/`00184950`/`002F16B0`. Interior anchor `0036125E` (a `002DEE50` call).

## SWE2-EC7-43 update (2026-09-19) - `00207FB0`

`00207FB0` (281 B) is a sound-request body - `008C2458`-`008C2480`/`00905888` import calls, `01F44830`, `00195200`/`0020A020`/`00210EC0`/`00808C40`. Interior anchor `00207FFF` (a `00195200` call).

## SWE2-EC7-44 update (2026-09-19) - `001AA6C0`

`001AA6C0` (270 B) is a registrar-family body `0020A800` calls - `008C25F0`/`008C2628`/`008C2630`/`008C25A0` import calls, `00808850`/`00861ECC`. Interior anchor `001AA6E3` (an `00808850` call).

## SWE2-EC7-44 update (2026-09-19) - `00203E60`

`00203E60` (263 B) is a registrar-family body `0020A800` calls - `008C25F0`/`008C2628`/`008C2630` imports plus `call [rdx+8]`, `00207FB0`/`00808850`/`00861ECC`. Interior anchor `00203E80` (an `00808850` call).

## SWE2-EC7-45 update (2026-09-19) - `0020A2D0`

`0020A2D0` (252 B) is a registrar-family body - `008C2618` import call, `002038A0`/`00209000`. Interior anchor `0020A352` (the import call).

## SWE2-EC7-45 update (2026-09-19) - `0020A3D0`

`0020A3D0` (252 B) is a registrar-family body - `008C2618` import call, `002038D0`/`00209090`. Interior anchor `0020A452` (the import call).

## SWE2-EC7-45 update (2026-09-19) - `0020A4D0`

`0020A4D0` (237 B) is a registrar-family body - `00203900`/`00209290`. Interior anchor `0020A53F` (a `00203900` call).

## SWE2-EC7-47 update (2026-09-19) - `002060C0`

`002060C0` (221 B) is a call-free record-slot walker - `[rsi+8]` type code 0xA..0x13 case select, `rdi` link chasing, `+0x34` field writes, `+0x20`/`+0x28` chains. Interior anchor `002060F9` (the type load).

## SWE2-EC7-47 update (2026-09-19) - `00203790`

`00203790` (214 B) is a registrar-family body - `002035B0`/`00204010`/`002044C0`/`00209B50`. Interior anchor `002037E3` (a `002035B0` call).

## SWE2-EC7-47 update (2026-09-19) - `00209120`

`00209120` (214 B) is a registrar-family body - `00203940`/`00209A50`/`00209BC0`. Interior anchor `00209146` (a `00203940` call).

## SWE2-EC7-48 update (2026-09-19) - `00209290`

`00209290` (200 B) is a registrar-family body - `008C2618` import call only. Interior anchor `00209304` (the import call).

## SWE2-EC7-49 update (2026-09-19) - `003D7F30`

`003D7F30` (190 B) is `Audio_ReleaseRefCounted` - the 32-entry, 132-byte-stride table at `02EBBA00`: `002DEB40`/`002DF050`/`003D7E90`. Interior anchor `003D7FAE` (a `002DEB40` call).

## SWE2-EC7-50 update (2026-09-19) - `00361630`

`00361630` (182 B) is `AudioTrack_FindOrReserveSlot` - `002DEC70` single call; find-or-reserve states `3` then `4`. Interior anchor `003616C1` (the `002DEC70` call).

## SWE2-EC7-50 update (2026-09-19) - `00207E90`

`00207E90` (181 B) is a body - `00210EC0` single call. Interior anchor `00207ECF` (the `00210EC0` call).

## SWE2-EC7-50 update (2026-09-19) - `00209780`

`00209780` (179 B) is a registrar-family body - `008C2618`/`008C2A40` import calls only. Interior anchor `0020979E` (the first import call).

## SWE2-EC7-51 update (2026-09-19) - `00206B70`

`00206B70` (173 B) is a body - `00203870`/`00209950` plus a `008C2618` import call. Interior anchor `00206BC4` (a `00203870` call).

## SWE2-EC7-52 update (2026-09-19) - `00205890`

`00205890` (674 B) is a sound-request body - `00208C60`/`00209530`/`00208CF0` runs (21 direct calls). Interior anchor `002058E9` (a `00208C60` call).

## SWE2-EC7-53 update (2026-09-19) - `00209E00`

`00209E00` (542 B) is a sound-request body - `00204A80`/`00209780`. Interior anchor `00209FDA` (a `00209780` call).


## SWE2-EC7-53 update (2026-09-19) - `00208220`

`00208220` (367 B) is a sound-request sibling - `00204A80`/`00208390`. Interior anchor `00208254` (a `00208390` call).

## SWE2-EC7-54 update (2026-09-19) - `00208390`

`00208390` (531 B) is a sound-request body - `0020A1F0` single call plus one vcall, `008C2618`/`009059A0` and the `"vector<bool> too long"` literal. Interior anchor `00208401` (a `0020A1F0` call).

## SWE2-EC7-55 update (2026-09-19) - `00205DF0`

`00205DF0` (242 B) is a sound-request body - `00210EC0` single call plus `00905920`/`00905930` and the `"pL "` literal. Interior anchor `00205E0F` (a `00210EC0` call).

## SWE2-EC7-56 update (2026-09-19) - `0020A1F0`

`0020A1F0` (209 B) is a sound-request body - `00203870`/`00209200`. Interior anchor `0020A255` (a `00209200` call).

## SWE2-EC7-60 update (2026-09-19) - `002121C0`

`002121C0` (156 B) is a sound-request body - `00212050`/`005CD4F0`/`005CD820` plus one vcall. Interior anchor `002121EE` (a `00212050` call).

## SWE2-EC7-61 update (2026-09-19) - `00206AD0`

`00206AD0` (151 B) is a sound-request registrar body - `00205D60`/`002060C0`/`00206D30`/`00207E90`/`00208C60` plus one vcall, `008C2430`. Interior anchor `00206AF6` (a `00205D60` call).

## SWE2-EC7-62 update (2026-09-19) - `00221D60`

`00221D60` (146 B) is the voice-path body `00223190` goes through - `0016D6A0`/`00210A60`/`00210B30`/`00220D30`/`00221710` plus one vcall. Interior anchor `00221D6D` (a `00221710` call).



## SWE2-EC7-63 update (2026-09-19) - `00203F70`

`00203F70` (145 B) is an object-registrar body - `00210EC0` single call plus `009058D0`. Interior anchor `00203F8D` (a `00210EC0` call).



## SWE2-EC7-63 update (2026-09-19) - `00209000`

`00209000` (144 B) is a `008C24xx`/`008C26xx` triple body - `002099D0`/`00209B50` plus `008C2A40` and one vcall. Interior anchor `00209026` (a `002099D0` call).



## SWE2-EC7-63 update (2026-09-19) - `00209090`

`00209090` (144 B) is a `008C24xx`/`008C26xx` triple sibling - `002099D0`/`00209B50` plus `008C2A40` and one vcall. Interior anchor `002090B6` (a `002099D0` call).



## SWE2-EC7-64 update (2026-09-19) - `00205D60`

`00205D60` (141 B) is a resolve/fetch body - `00210EC0` single call plus `00905900`. Interior anchor `00205D74` (a `00210EC0` call).



## SWE2-EC7-65 update (2026-09-19) - `00221780`

`00221780` (135 B) is the callback base constructor - `001EDF00`/`002218D0` plus `008F3CC0`/`009078B0` ('EASTL list','P%'). Interior anchor `002217C9` (a `001EDF00` call).



## SWE2-EC7-65 update (2026-09-19) - `00208C60`

`00208C60` (134 B) is a resolve/fetch body - `00210EC0` single call plus `009058C0`. Interior anchor `00208C74` (a `00210EC0` call).



## SWE2-EC7-66 update (2026-09-19) - `00360120`

`00360120` (134 B) is the per-frame pending-request check - `0017F740`/`00182810`/`001830A0`/`001EC4B0`/`003321E0`/`003601D0` plus `022CB720`-`022CB72A`. Interior anchor `00360124` (a `003321E0` call).



## SWE2-EC7-66 update (2026-09-19) - `00209200`

`00209200` (130 B) is an indirect-only `vector<T>` resize - `0x3FFFFFFFFFFFFFFF` max, `"vector<T> too long"` (`0020D8A0` sibling). Interior anchor `0020923D` (the `"vector<T> too long"` `lea`).


## SWE2-EC7-67 update - `001A4C90`

`001A4C90` (129 B) is an indirect-only `std::string` move-assign - `[rdx+0x18]<0x10` frees via `call [008C2A40]`, copies ptr/len/cap, source cap=0xF. Interior anchor `001A4CB1` (the `call [008C2A40]` free).

## SWE2-EC7-67 update - `00209950`

`00209950` (128 B) is a sound-request body - `00210EC0` x2 plus `008C2608`/`008C2DA8` import pairs (`00209A50` twin). Interior anchor `0020999A` (an indirect call).

## SWE2-EC7-67 update - `00209A50`

`00209A50` (128 B) is a sound-request body - `00210EC0` x2 plus `008C2608`/`008C2DA8` import pairs (`00209950` twin). Interior anchor `00209A9A` (an indirect call).

## SWE2-EC7-68 update (2026-09-19) - `00212A70` request-slot clear

`00212A70` (23 B) is the slot clear the sound-request path runs:
`ecx <= 0x7F` gates a `dword[01FD36C0 + rcx*8] = 0` write - the low
dword of the 128-entry request table - and out-of-range indices
return untouched. Call-free. Interior anchor `00212A7F` (the table
store).

## Crossing accounted 2026-09-19 (FABLE): Gameplay

**Gameplay - SERVICE.** The field pass `0025D9E0` on this page calls `00234150`, owned by the Gameplay layer (104 B, read
whole): for each of the four roster selectors whose battle unit has flag bit 4, it asks whether the unit should be in
its engaged state and calls the engaged-state setup or its counterpart. It sits in the field pass beside the sound
work and has nothing to do with it; the crossing is that call.

## SWE2-EC7-77 update (2026-09-20) - `00222050` + `002218D0` + `002129F0` audio helpers measured

`00222050` (36 B) is the paired `00222280` call: first on `rcx+8`
(result kept in `bl`), then on the global `01FD4140` - a two-target
invoke, not a loop.
Interior anchor `00222069` (the `01FD4140` call).

`002218D0` (101 B) is the circular-list drain: it walks the
`[rcx]`-linked nodes, calling the `+0x18` vtable slot of the
`[rcx+0x10]`-pointed object on each with `r8d = 0x18` (element size),
then resets the head - `[rcx] = rcx`, `[rcx+8] = rcx`.
Interior anchor `00221904` (the `call [rax+0x18]`).

`002129F0` (30 B) is the clear-on-error wrapper: `00212970(rcx)`; a
negative return writes `dword[rbx] = 0`. Non-negative returns leave
the field alone.
Interior anchor `00212A02` (the `mov dword [rbx], 0`).

## SWE2-EC7-102 update (2026-09-20) - `0028E790` measured

`0028E790` (161 B) is the five-call state publish
`0027F5D0`, `002804E0` and `00281ED0` run on
`0209BE80`: `003CB410()` opens; when
`byte[+0x10FA2] != 3` the `+0x10FA6` word is zeroed;
`00550400` takes the `+0x10FA2` mode byte and the
`+0x10FA6` word; `00550510` takes
`(dword[+0x10F68] >> 0xC) & 1`; `dword[+0x10FA8]` is
packed into a two-qword stack record for
`00550540`; and `00550610()` closes - the
mode-fields publish the sound-request boundary
runs.
Interior anchor `0028E7D6` (the `00550400`
call).

## SWE2-EC7-109 update (2026-09-20) - four audio-boundary helpers measured

`00210710` (68 B) is the
two-sink virtual fallback
`00223190` and `00224570` run:
`vtable[ qword[rcx + 0x10] ][+0x10]
(edx, r8d)` is tried first; only
when it answers false does the
same slot on `qword[rcx + 8]`
get the identical arguments - a
primary/secondary dispatch pair.
Interior anchor `0021072E` (the
first `call qword [rax + 0x10]`).

`002099D0` (124 B) is the
16-byte aligned allocator
`00204230`, `00206050`,
`00209000` and `00209090` call:
`rdx` elements of 16 bytes; under
`0x1000` it is a plain
`00210EC0(size)`, at or above it
requests `size + 0x27`, aligns
`(rax + 0x27) & ~0x1F` and
stashes the raw block at
`[aligned - 8]`; overflow and
null failure both throw through
`008C2608` / `008C2DA8`.
Interior anchor `00209A27` (the
`add rax, 0x27` align step).

`00209AD0` (114 B) is the
matching aligned free `0020B680`,
`0020C300` and the `00899520`
family call: `r8 * 4 >= 0x1000`
selects the big-allocation path -
`rdx & 0x1F` must be 0, the raw
block comes back from
`[rdx - 8]`, and the delta must
sit in `8..0x27` before the
`00210EB0` tail-free; every
violation throws through
`008C2DA8`.
Interior anchor `00209B06` (the
`[rdx - 8]` base recovery).

`00204A80` (112 B) is the
fixed-point step `00208220` and
`00209E00` apply to the
`{qword, qword}` pair at `rcx`:
`r8` (signed) accumulates into
the low word, each full 32 units
carries `4` into the high word
(`(low >> 5) * 4`), the residue
keeps `low & 0x1F`, and a
negative `r8` borrows through
the `or rcx, -1` path - a 5-bit
fraction accumulator written
back to `rdx`.
Interior anchor `00204ACC` (the
`shr rcx, 5` carry).

`00203870` (43 B) is the dword
fill `00206B70` and `0020A1F0`
run: `dword[r8]` is written to
`rcx`, `rcx + 4`, ... `rdx`
times - the counted replication
helper behind buffer clears.
Interior anchor `00203887` (the
`mov eax, [r8]` load).

`00550610` (117 B) is the close `0028E790` runs last (and `0028E690`'s world-map arm shares): with `02CA8F38` live and `word[+0x170]` bits 0 and 2 both set, bit 1 clears and `00246AD0` attaches the widget under `0208EA20` then its `+0x160` child under `0208EA28`; on any other flag state `+0x170` bit 1 is set — the pending-open mark. A null widget returns untouched.

Interior anchor `00550643` (function `00550610`).

`00550400` (110 B) is the lazy create behind `02CA8F38` that `0028E690`/`0028E790` run before every publish: when the world-map widget host is null, `002901D0`/`0035C080` preface `00244F50(0x188, 00552250, &ctx{0, ecx, dx})` — the `00552250` widget record is built and stored to `02CA8F38`; a live host is returned untouched.

Interior anchor `00550449` (function `00550400`).

`00550510` (35 B) is the bit-3 flag write `0028E790` feeds `(dword[+0x10F68] >> 0xC) & 1` into: `(cl & 1) << 3` folds into `02CA8F38`'s `+0x170` under mask `0xFFF7` — one flag bit of the publish.

Interior anchor `0055051B` (function `00550510`).

`00550540` (194 B) is the record publish `0028E790` packs its two-qword stack record for: `rdx`'s `{+0, +8, +0xC}` words land in `02CA8F38`'s `+0x178`, `+0x17A` and `+0x180`, `+4`'s bits toggle `+0x170` bits 0x20 and 0x100, then `00249580` resolves a child, `00562F90(widget+0xC0, ret)` binds it, `00249410(ret)` registers, and `003BC440(widget)` notifies — the mode-fields write-through.

Interior anchor `005505B7` (function `00550540`).

`00562F90` (231 B) is the child-bind `00550540` runs on `widget+0xC0` after `00249580` resolves: `00249210(widget, 7, 3, 0xA8)` types it, then an eleven-entry loop walks the `00D231C0` 16-byte-entry table — `002493D0(widget, 7, i+0xAA, 2, &table[i])` files each bind into `[widget+0x20+i*8]` for `i < 8` and `i > 9`, slots 8 and 9 stay unbound, and `i == 0xA` takes `0024A5A0(01E0C220)` instead; the tail runs `00249350(widget, 7, 2, 0xA6)` into `+0x18` and parks `+0x88` at `-1`.

Interior anchor `0056301F` (function `00562F90`).

`002901D0` (73 B) is the `+0x10FA4`/`+0x10FAC` mailbox setter `00550400` and `005528C0` run on the same `[0209BE80]` type store: when the store is live, `word[+0x10FA4] = cx`; a zero `cx` then zeroes `dword[+0x10FAC]`, a nonzero one files `003C0250(cx)` — the `02B457E0` `+0xD8` keyed table's paired value — there. Two more parked mailboxes flanking the world-map opener's `+0x10FA2`/`+0x10FA6`/`+0x10FA8` triple.

Interior anchor `00290202` (function `002901D0`).

`00207310` (956 B) is the name-table body `00208710` runs: `00204160` x2, `00204230` x2, `00204820` x4, `00204950` x4, `00208710` x2 and `00210EB0` x4 walk the lookup chain - the two-stage name lookup's inner table walk.

Interior anchor `0020745C` (function `00207310`).

`00204820` (297 B) is the name-table bodies `00207310` (x4), `00207720`, `00207B40`, `00208710` and `00204710` call: `[rdx]`/`[rdx+8]` deref the chain head and `00203450`, `00209AD0`, `00205FE0` do the lookup steps - the two-stage name lookup's shared inner resolve.

Interior anchor `002048C1` (function `00204820`).

`00204160` (194 B) is the same four callers run beside `00204820`: `[rcx]` is written on entry and `00209950` performs the single lookup step - the name-table walk's short companion helper.

Interior anchor `002041D1` (function `00204160`).

`00207B40` (671 B) is the record-assembly stage the request dispatcher `00208710` calls: `dword[rdx+0x34] == 1` shortcuts to `00207720`, otherwise `00204160`/`00204230` snapshot the input pairs, `rbx + 0x30` indexes the 16-byte record under `rdi + 0x80`, and `00204820`/`00204950`/`00207720`/`00208710`/`00209AD0`/`00209B50` run the field fills - the `0020xxxx` family's pre-voice gather.

Interior anchor `00207B7D` (function `00207B40`).

`00204950` (294 B) is the splice-in `00204710`/`00207310`/`00207720`/`00207B40` call: `rsi`'s begin/end/cap triple and `r14`'s source range are counted at stride 16, fits-tail runs two `008C2A40` memmoves, fits-capacity runs `00203450` plus one memmove, otherwise `00209B50` takes the reallocation path - the request vector's insert.

Interior anchor `002049EC` (function `00204950`).

`00204230` (194 B) is the range-copy `00207310`/`00207720`/`00207B40` call: `rsi`'s triple is zeroed, `(rdx.end-rdx.begin)>>4` bounded by `0x0FFFFFFFFFFFFFFF` throws the "vector<T> too long" literal, `002099D0` allocates and `008C2A40` copies - the request vector's clone.

Interior anchor `002042A1` (function `00204230`).

`00207720` (1050 B) is the snapshot-and-dispatch `00207B40` calls (its main loop): `00204160`/`00204230` copy `rdi`'s two ranges to stack, the `dword[rsi+0x20]`-counted loop calls `00208710` per element with `[rdi]` head-change detection advancing `ebx`, and `00204820`/`00204950`/`00210EB0`/`00861EC0` run the mutation arms - the request's apply loop.

Interior anchor `0020779A` (function `00207720`).

`00203450` (49 B) is the move helper the splice `00204950` (and `00204820`) call: `memmove(r8, rcx, rdx - rcx)` through `008C2A40`, returns `rbx + r8` - the request vector's copy-and-advance.

Interior anchor `0020346C` (function `00203450`).

`001A9E50` (118 B) is the bounded range-copy `0020AA50`/`001DA290` (and four uncited callers) share: `eax = [rcx+8] - [rcx] - r8d` is the remaining span, `cmovb` clamps `r9d` to it, `rbx = base + r8d`/`rdi = base + r8d + r9d` bracket the source, `001EDF00` copies the `+0x18` header into `rsi`, then `001A4BF0` moves the range - a clamped span clone.

Interior anchor `001A9EA0` (function `001A9E50`).

`00208DE0` (398 B) is the path classifier `00205890` calls: `dword[rcx + 0x7C]` selects `esi` (`0x2A` -> 0, `0x2B` -> `rdi + 2`), `[rbx + 0x48]` gets `| 4` at `+0xC`, and the `[rbx]`..`[rbx + 0x10]` string is walked for `0x5C` separators via `00209530` before `00208CF0`/`00206C20`/`002054D0` resolve - the voice request's path splitter.

Interior anchor `00208E57` (function `00208DE0`).

`00208CF0` (73 B) is the separator scan `00208DE0`/`00205890`/`00206430`/`00206640`/`00209840` call: walks `[rcx]` toward `[rcx + 0x10]` for `0x5C`, then unless `byte[rcx + 0x80]` bit 8 (0x28/0x29 exempt) or bit 0x10 (0x7B-0x7D exempt) applies, stores the found offset back to `[rcx]` - the request path's token advance.

Interior anchor `00208CFC` (function `00208CF0`).

`002054D0` (811 B) is the state dispatch `00208DE0` calls: `[rcx + 8]`'s record with `[rax + 8] == 6` and `[rax + 0x24] > 1` decrements the count and feeds `byte[[rax + 0x28] + old]` to `00204DA0`; then `dword[r13 + 8]` switches across seven `00210EC0` arms - the voice request's mode router.

Interior anchor `00205508` (function `002054D0`).

`00204DA0` (169 B) is the byte submit `002054D0`/`00205890`/`00205B40` call: `[rcx + 8]` record `[+8]==6` without `+0xC` bit 4 runs `00205800` first; `dword[rbx + 0x10]` bit 8 takes the IAT write (`[rax + 8]`, `008C2440`), bit 0xB takes `0020B000`; then `rbx = [rbx + 8]`, `[rbx + 0x20] <= [rbx + 0x24]` gates a `[rbx + 0x28] + (eax + 0x10)` write - the voice record's payload post.

Interior anchor `00204DC0` (function `00204DA0`).

`00204010` (336 B) is the out-struct `00203790` calls: `rcx + 8` gets three zeroed qwords, then `00206B70`/`0020A3D0` build the payload through `rbp`/`rsi`/`r12` - the voice path's record init.

Interior anchor `00204066` (function `00204010`).

`00206F60` (315 B) is the classifying scan `00208710` calls on the `rcx` request: `dword[+0xB8]&0x100` runs `byte[rax]` through the `008C2440` IAT classify into `bpl`; `rsi+0x20` nonzero then `00203520(rdi, [rbx+0xA0])` scans for the match point at `rdi+1` (hit -> `r14`, `r9d`=1), else the `rsi+0x38` arm applies `0020B000` when `+0xB8&0x800` and walks `r10 = dword[r8+4]` - the name-driven branch the request boundary takes.

Interior anchor `00206FA1` (function `00206F60`).

`0020B000` (194 B) is the one-byte map `002031A0`/`00204DA0`/`00206960`/`00206F60` call: `0020AFE0` converts `[rcx]`'s character into the `rsp+0x28` small-string (cap 0x10, `rsp+0x20` fallback byte); a produced length of 1 at `[rsp+0x38]` returns `bl` = the buffer's first byte (SSO head or heap block), any other length returns the `dl` argument, and `>=0x10` buffers free through `00210EB0` after the `008C2DA8` header checks (`+1` size < 0x1000, 0x20 alignment, `[-8]` bounds) - the name-classify byte the request boundary's `0x800` arm applies.

Interior anchor `0020B02B` (function `0020B000`).

`00209840` (269 B) is the refcounted dispatch `00205890` runs on the request: `dword[rcx+0x1C]` bumps on entry and drops on every exit; `dword[+0x80]` bit `0x1B` with `+0x7C == 0x29` asserts (`008C2430`, code 5); bit `0x20` with `+0x7C == 0x3F` double-runs `00208CF0` then switches on `+0x7C` - `0x3A` runs `002076D0` returning 1, `0x21`/`0x3D` run `00206E90` with `dl` 1/0 returning 0, anything else asserts code `0xE`; otherwise `dword[+0x70] & 0x200` runs `00208C60(rcx+0x40, 8)` into `00206D30` and `00207E90(rsi+0x40, result)` returning 1, else `00206EE0` returning 1 - the state-keyed verb table the request body drives.

Interior anchor `00209907` (function `00209840`).

`00205EF0` (238 B) is the bitmask-pair membership probe `00208710` runs: `dword[rcx+0xC4]` counts the entries; per index the `i >> 5`/`i & 0x1F` `bt` must pass on both the `[rcx+0x48]` and `[rcx+8]` bitmaps, then the 16-byte key at `[[rcx+0x28] + i*16]` must equal `[[rcx+0x68] + i*16]` - a mismatch diverts through `[rcx+0x98]` before `0`/`1` returns - the dual-bitset key compare the voice allocator consults.

Interior anchor `00205F5C` (function `00205EF0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

**ActorEntity — PROVIDER.** The UQ-248 answer cites `ActorResource_BeginManagerResourceSetLoad`
(`0032FCA0`, call site `0032FD64`) as the only caller of `0020AC30`. The relationship runs one way:
**the actor-manager loader hands this page's slot setter a manager index and a path.** The answer
rests only on those two arguments and the path-kind branch that picks the path (`0032FD19`–`0032FD44`).
Nothing about how the loader stages, admits or completes a manager's resources is claimed here.

**WorldAreaField — PROVIDER, at one remove.** For manager 0 the path the loader passes is the
`.ebp` of the field the transition selected. This page cites that chain only to say what slot 0's
name is. The field transition's own behaviour belongs to its pages.

*These two paragraphs cover only the edges the UQ-248 citations add.* The page's other ActorEntity
and WorldAreaField edges, from earlier sections, are not dispositioned here. **Neither are the page's
`World` and `Script_VM_Native_Bridge` findings.** The neighbour gate reports them "accounted for by
this publish" only because it matches layer names as substrings of this text. The count falling by
four after this publish overstates what was answered by two.

`00206250` (229 B) is the escape skipper `00205890` runs on the lexer's `+0x40` stream: on a `^` marker (`+0x7C == 0x5E`) it flips `rax+0xC` bit `0`, consumes a `\`-escaped character honouring `+0x80` bits `0x08`/`0x10` for `(`/`)`/`{`/`}` literals, and steps `00209530`; the same block repeats for `]` (`0x5D`) when `+0x80` bit `0x20000000` is set - then it tails `00206960` on the record

Interior anchor `002062F3` (function `00206250`).

`00206960` (355 B) is the token loop `00206250` tails into: `00206640` lexes per iteration - token kind `2` skips; a `-` (`+0x7C == 0x2D`) under `+0x80` bit `0x100000` consumes a `\`-escaped literal honouring the `0x08`/`0x10` flag bits then `00209530`-steps; under `+0x70` bit `0x800` it folds the `[rbx+0x68]` accumulator through `0020B000` twice against byte `+0x74`, and `00205330`/`00204F00` push onto `+0x40` - `008C2430` invalid-argument deaths on the `2`/`8` outs

Interior anchor `00206A0F` (function `00206960`).

`00205B40` (225 B) is the charset-bitmap dispatch `00205890` runs on the same lexer record: `+0x80` bit `0x100` set and `00206C20()` passing bounds `[rbx+0x74]` (against `9` when bit `0x200` is set, else against `[+0x18]`/`[+0x38]`), tests bit `edx` in the `[rbx+0x20]` u32 bitmap (`idx >> 5` dword, `1 << (idx & 0x1F)`) and tails `00204D10` on `+0x40` on a hit; the bit-`0x100`-clear path runs `00206430` then `00204DA0`, and `+0x80` bit `0x20000` gates a `00206340(1)` early-out - every dead path dies through `008C2430`

Interior anchor `00205BA9` (function `00205B40`).

`00206C20` (165 B) is the decimal-integer accumulator `00205B40`/`00208DE0` run on the lexer record: `+0x74` folds `+0x78` digits (`*10 + d`) for up to `0x7FFFFFFF` iterations, each iteration consuming the `\`-escape pair under the `+0x80` `0x08`/`0x10` flags and stepping through `00209530` - returns whether any digit was consumed

Interior anchor `00206C56` (function `00206C20`).

`00204F00` (135 B) is the single-bit bitmap setter `00206250`/`00206960` run: under `+0x10` bit `0x100` the index `dl` is first mapped through `[+0x18]+8`'s `008C2440` import; the `+0x28` 0x20-byte bitmap is `00210EC0`-allocated lazily and `bts` sets bit `index` (dword `index>>3`, bit `index&7`) - the charset 'seen' mark

Interior anchor `00204F6B` (function `00204F00`).

`00206640` (581 B) is the next-token lexer `00206960` calls per iteration: `+0x7C == 0x5C` consumes the `\` escape then dispatches on `+0x80` - bit `0x15` tails `00206890`, bit `0x10` runs `002072C0(+0x78)`, bit `0x8000` maps `+0x78` 'a'/'b' to `+0x74` codes 7/8 via `00208CF0`; `+0x7C == 0x5B` reads ahead and on a `.`/`:`/`=` separator (bitmask `0x2400400000000000`) consumes and `002070A0`s it, returning 2; `]`/EOF return 0 and every other char lands in `+0x74` with a return of 1

Interior anchor `0020669E` (function `00206640`).

`00206430` (524 B) is the C-escape decoder `00205B40` runs on the `0x200`-clear path: `[+0x7C] == -1` dies via `008C2430`; `\f`/`\n`/`\r`/`\t`/`\v`/`\a`/`\b` map to `+0x74` codes `0xC`/`0xA`/`0xD`/`9`/`0xB`/`7`/`8`; `x` parses hex through `00208CF0` x2 + `002080D0` (result > 0xFF dies via `008C2430`); `u` and `c` run their own `00208CF0`/`00208D40` sequences

Interior anchor `002064FC` (function `00206430`).

`00205330` (414 B) is the range-bitmap setter `00206960` runs: under `+0x10` bit `0x100` both `dl`/`r8b` bounds pass through the `[+0x18]+8` `008C2440` mapping; `ebx..edi` inclusive get `bts` marks in the lazily-`00210EC0`-allocated `[+0x28]` bitmap while `edi < [+0x20]`, and a wider range past `+0x20` splits to the `008C2B58`/`008C2608` fill pair - the `[a-b]` class-membership writer

Interior anchor `002053DD` (function `00205330`).

`00206340` (236 B) is the wide-char emit `00205B40` runs as its `1`-armed early-out: `[rcx] == [+0x10]` fails; `00203A30([+0x68], cursor+1, (+0x70>>8)&1)` decodes the next char and a zero decode fails too; `dil` set pushes through `00204F90([+0x40])`, then `00205030([+0x40], +0x48, char, classtable[+0x78]&1)` appends char+class before the usual `\`-escape consume and `00209530` step - returns 1

Interior anchor `00206376` (function `00206340`).

`00204F90` (146 B) is the `[+0x40]`-list node constructor `00206250` and `00206340` push through: `00210EC0(0x50)` allocates a node stamped with vtable `00905A28` (RTTI `00204AF0`), zeroed `+0xC..+0x48` payload, then links it head-of-list - `[rbx+8]`'s old head takes `new` at `+0x10`/`+0x18` and `[rbx+8] = new` - the lexer's per-token record allocator

Interior anchor `00204FB7` (function `00204F90`).

`002070A0` (535 B) is the `[`-separator consumer `00206640` calls on the `0x2400400000000000`-mask hit: it scans forward until `+0x7C` returns `0x3A` (consuming `\(`/`)` pairs when `+0x80` bit3 is set, `{`/`}`/`~`/`|` when bit4 is clear), then dispatches - `:` decodes via `00203A30` and appends with `00205030`, `=` runs `00205120` over the scanned span, `.`/`0x2E` falls to the `+0x48` path; mismatched or empty separators die via `008C2430`

Interior anchor `00207145` (function `002070A0`).

`00205030` (238 B) is the charset-table append `00206340`/`002070A0` emit through: per `bl` it tests the `[+0x18]->+8->+0x18` u16 category table (`bp == -1` uses mask `0x107`, else caller's mask) and on mismatch lazily `00210EC0`s a 0x20-byte bitmap at `[rsi+0x28]` and `bts`-sets the char's bit - the 'mark this char as emitted' hook behind the lexer

Interior anchor `002050B2` (function `00205030`).

`00203A30` (201 B) is the codec-table scan `00206340` and `002070A0` call: it walks the 24-byte records at `00905A30`, calling `00203980(arg2, arg3, entry+0, entry+0 + [entry+0x10])` per live (`[entry] != 0`) slot until one accepts, then returns that entry's `+0x14` word - `bx |= 3` when the flag arg is set and `bl & 3` was nonzero - the 'find the conversion row for this char' step behind the lexer

Interior anchor `00203A80` (function `00203A30`).

`00205120` (522 B) is the `=`-arm builder `002070A0` runs over the scanned span: for each code 0..255 it `00203B00`s the char-name string and `00861ED2`-compares it against the target (`00203CB0` product at `[rax+0x10]/+0x18`); on equality it lazily `00210EC0`s a 0x20-byte bitmap at `[r15+0x28]` and `bts`-sets the code's bit, closing with the `00210EB0` CRT aligned-free on the temporaries - the set of all codes whose name matches, as a 256-bit map

Interior anchor `00205170` (function `00205120`).

`002080D0` (205 B) is the hex-digit accumulator `00206430` calls for `\x` escapes: per `[rbx+0x78]` char it decodes `0-9`/`a-f`/`A-F` to a nibble (`-0x30`/`-0x57`/`-0x37`), folds `+0x74 = (+0x74 << 4) | nibble` for the requested digit count, honouring the `\` + `(`/`)`/`{`/`}` adjacency skip under `+0x80` bits 3/4, and any non-hex char dies via `008C2430` error 2

Interior anchor `002080F0` (function `002080D0`).

`00203CB0` (416 B) is one of the two string-assign arms `00205120` uses to materialise a character-name string: it ranges `[r10, r11)` through the codec helper into a stack `std::string`, `0020AFE0`-constructs and `00204760`-assigns it into the caller's out string, then runs the MSVC scalar-delete free checks (`0x1000` size, `0x1F` alignment, `0x27` block bound) before `00210EB0` releases the temporary

Interior anchor `00203D6C` (function `00203CB0`).

`00203B00` (416 B) is the twin arm of the same helper: identical frame, same `00203330`-driven span walk, `0020AFE0`/`00204760` construct+assign into the out string and the same guarded `00210EB0` free - the pair differ only in how the caller's span is presented

Interior anchor `00203B89` (function `00203B00`).

`0020AFE0` (32 B) is the thin virtual-call forwarder `00203B00`, `00203CB0` and `0020B000` all run to materialise a string: it invokes slot `+0x20` of `*rcx` (the character-source vtable) and returns the caller's `rdx` out pointer unchanged - the shared construct step of the name-string assign family

Interior anchor `0020AFEC` (function `0020AFE0`).

`00206890` (196 B) is the backslash arm of the audio lexer: entered when `+0x80` bit 0x4000 is set and `[+0x78]` is `0x5C`, it stamps `+0x74 = 0x5C`, walks `[rcx]` forward over the escape, skipping `(` `)` unless flag `0x8` and `{` `}` unless flag `0x10`, then `00209530`s and returns 1; bit 0x20000 unset falls through to `00206C20` (decimal accumulate, trapping via `008C2430` if `+0x74` is still nonzero) or `00206430`, returning 2/`al` on those lanes

Interior anchor `00206904` (function `00206890`).

`00207DE0` (173 B) is the request-node link `00206D30` runs on the pending list: `[r8+0x10]` detaches onto `rsi`, `r8` splices ahead of `[rcx+8]`'s old head through the `+8`/`+0x10` link pairs, then after walking `rbx`'s `[+0x28]` chain to its tail a `00210EC0(0x30)` node is stamped `{+0 = "pL " tag, +8 = 0x10, +0x20 = rdi, +0x10 = rsi}` and sewn onto the tail with `[rsi+0x18]` pointing back at it

Interior anchor `00207E32` (function `00207DE0`).

`00203980` (171 B) is the case-insensitive name compare `00203A30` runs against request names: `rdx - rcx` must equal `r9 - r8` (length match) before the per-byte loop, which `tolower`s each side through the locale facet at `[arg5+8]` via IAT `008C2440` and returns false on the first mismatch

Interior anchor `002039E1` (function `00203980`).

`00204E50` (170 B) is the byte-append `00205330` uses to build the request name: `[rcx+0x10] & 0x100` decides whether `dl` is `tolower`-folded through the `[rax+8]` facet (IAT `008C2440`), then the `[rbx+8]` record's `+0x30` buffer struct (`00210EC0(0x10)` when absent) grows by `+0x10` through realloc (`008C2B58`, failure raising via `008C2608`) and the byte lands at `buf[len++]`

Interior anchor `00204EC4` (function `00204E50`).

`002061A0` (166 B) is the keyed node lookup-or-insert `002070A0` runs on the `*rbx` list: it walks `+0x18`-next nodes until `dword[node] >= edi` or the chain ends, reuses the matching node when present, else `00210EC0(0x20)` builds `{edi, 0, 0}` spliced at the slot with `+0x18` holding the displaced link - then `node+8`, `r14`, `rbp` tail-jump `00203490`

Interior anchor `002061F3` (function `002061A0`).

`00208D40` (159 B) is the octal-digit accumulator `00206430` runs: up to three rounds take `byte[+0x78] - 0x30` in `0`..`7` and fold it into `+0x74` as `acc*8 + digit`, each step optionally skipping `\`-escaped `(`/`)`/`{`/`}` per the `+0x80` mode bits before `00209530` advances; returns whether fewer than three digits landed

Interior anchor `00208DC5` (function `00208D40`).

`00208F70` (142 B) is the `vector<dword>` assign `00209200` runs: `00209950` carves `n*4` bytes through `008C2A40`, the old span is counted (`(end-begin)>>2`) and `00209AD0` destroys it when non-empty, then `begin`/`end`/`cap` are rewritten as `rsi`, `rsi + count*4`, `rsi + r14*4` - the re-allocating resize on the voice request's dword list.

Interior anchor `00208FB0` (function `00208F70`).

`00203490` (139 B) is the byte-append `002061A0` runs on the voice request's growable buffer: the `{+0 capacity, +4 used, +8 data}` record doubles through `008C2B58` realloc in `+0x10` steps when full, then each byte of `[rdx, r8)` is stored and `+4` bumped - the push-half the `002035B0`-shaped `0xD8` request record feeds.

Interior anchor `002034D3` (function `00203490`).

`00204D10` (138 B) is the request-node factory `00205B40` calls to queue a sound request: `00210EC0` carves 0x28 bytes, the `00905910` vtable, `+8` capacity `0xF` and `+0x20`=`edx` stamp in, then the node links onto `[rcx+8]`'s `+0x10`/`+0x18` chain as the new head - the intrusive-list record allocator the voice path feeds.

Interior anchor `00204D36` (function `00204D10`).
