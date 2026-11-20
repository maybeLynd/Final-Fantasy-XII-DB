[Home](../../README.md) / [Graphics](README.md) / Character effects

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Character effects: the ticket and instance-handle tables, the stamped ids, the trigger states and the deferred trigger write | system | Graphics | Visual effects / Effects On Characters And Menus | The effect a character's model carries: the two tables of 32 records that hold effect tickets and model-effect instance handles, the id with a 22-bit serial that makes a stale handle a no-op, how a model's bind makes its instance and the record's teardown frees it, the per-frame flags the presentation pass and the draw gate trade through the handle, the trigger entry with its ten states, and the script verb charefftrigger whose request is stored in the render record and delivered by the next dirty walk. | 0x003B3160, 0x003B3400, 0x003B3550, 0x003B3300, 0x003B2F90, 0x003B39E0, 0x003B38B0, 0x003B37E0, 0x003B3B10, 0x003B33D0, 0x003B3080, 0x003B33A0, 0x003B3C00, 0x003B3480, 0x0024FE70, 0x003401D0, 0x002E73C0, 0x003E6AA0, 0x00427DE0, 0x0024B9B0, 0x0024D770, 0x02EBCD80, 0x02EBD480 |

## What the player sees

A character's model can carry an effect of its own, authored into the model's `@FEF` section. It plays
with the model, advances only while the character is processed, is drawn only while the character's
presentation pass allows it, and can be told by a script to start one of up to ten authored cues; the cue
starts the next time the game passes over the render records that have changed. When
the character's record is torn down, the
effect's instance ends with it.

## How it works

### Two tables of 32 records

`0x003B3160`, run at start-up by `0x00259180` under arena 8, builds two arrays of 32 records of `0x38`
bytes that sit back to back: the effect tickets at `0x02EBCD80` and the model-effect instance handles at
`0x02EBD480`. Every record is zeroed, gets `0x30000000 | slot` as its id at `+0x00`, and is chained
through `+0x20` (next) and `+0x28` (previous) into its table's free list: ticket head `0x02EBDB88`, handle
head `0x02EBDBA0`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B3190`-`0x003B32EC` |

</details>

The used lists start empty (tickets `0x02EBDB80` head and
`0x02EBDB90` tail; handles `0x02EBDB98` head and `0x02EBDBA8` tail) and both serials, `0x02EBDBB0` and
`0x02EBDBB4`, start at 0; the builder ends with `0x0024C550(3)`, which empties effect group 3
([effect element runtime](effect-element-runtime.md#emptying-a-group)).

The tickets are the registration side, on [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md#effect-sections-and-tickets):
a ticket is made when a source with an `@FEF` section is registered and holds the parsed effect data's
context. The handles are the playing side: one per render record whose model has such a ticket. This
page covers both tables' records and lists, the id, the handle's life, the trigger and the verb.

### The id

An id is three fields: mask `0x3F` the slot, mask `0xFFFFFC0` a 22-bit serial, mask `0xF0000000` the constant 3. An
allocation adds 1 to the table's serial and writes it into the bits under mask `0xFFFFFC0` (`0x003B394B`-`0x003B3967` for a
ticket, `0x003B3457`-`0x003B3470` for a handle); a release keeps only bits under mask `0xF000003F` (`and 0xF000003F`,
`0x003B3888`, `0x003B3387`).

Every helper that takes a handle id, and the ticket release `0x003B37E0`, first compares the id with the
dword at the slot `id & 0x3F` names and does nothing on a mismatch, so a handle kept across a release
names nothing until the serial wraps after 4,194,304 allocations of that table. Two id-taking routines
do not look at a slot: `0x003B3550` finds the context by the ticket id's low 16 bits¹ and
`0x003B39E0` matches the id against each handle's `+0x18`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B3594` |
| ² | `0x003B3A0A` |

</details>

The writer `0x003B3B10` and the reader `0x003B33D0` of the ticket's effect number compare only the slot
bits (`xor` then `test al, 0x3F`); the reader's two callers pass the current context's 16-bit word
`+0x04`¹, so the serial bits are not there to compare.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024D34C`, `0x0024D262` |

</details>

### A ticket's life

- `0x003B38B0(source, offset)`, from the registration `0x00409FE0`, pops the ticket free head, links the
  ticket to the used tail¹, stamps the serial, stores the resolved source plus offset at
  `+0x08`, zeroes `+0x10`, builds the context with `0x0024B3A0` into `+0x18` and parses the effect data
 ²; it returns the id, or 0 when the free list is empty³.
- `0x003B38B0` runs under arena 8: it calls `0x0036C1D0(8, 10)` before it looks at the free list⁴ and
  `0x0036C140` on both paths⁵. It resolves the source and adds the offset before that test
 ⁶, and it stores the id's low 16 bits in its template's word `+0x04`⁷.
- `0x003B3B10(id, n)`, also from `0x00409FE0`, stores the effect number `n` at `+0x30`: the number parsed
  from a `chara\h%d.efx` name, −1 when the number does not parse⁸. The registration calls
  it only for a source name containing `chara\h`⁹; for any other source `+0x30`
  keeps its old value, 0 on a slot never used since start-up or −1 on a slot released before
  (`0x003B38B0` does not write it).
- `0x003B33D0(id)` returns the number, or −1 for a slot
  whose bits disagree; `0x0024D330` asks it whether the number is `0x34` ([effect element types](effect-element-types.md))
  and `0x0024D140` asks for the soft-particle choice ([effect drawing](effect-drawing.md)).
- `0x003B37E0(id)`, from the disposal `0x00409D60` and the section drop `0x00409CA0`, sets `+0x30` to −1,
  cancels the context¹⁰, recycles every instance handle that names the ticket
 ¹¹, moves the ticket back to the free list, keeps the id's slot and top bits and zeroes
  `+0x08`, `+0x10` and `+0x18`¹².
- `0x003B37E0` cancels the context only when the ticket's `+0x18` is non-null¹³. The move
  unlinks the ticket from the in-use list (head `0x02EBDB80`, tail `0x02EBDB90`; next `+0x20`, previous
  `+0x28`) and pushes it at the free head `0x02EBDB88`¹⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02EBDB90` |
| ² | `0x003EDAD0` |
| ³ | `0x003B38E6`-`0x003B39BD` |
| ⁴ | `0x003B38E1` |
| ⁵ | `0x003B38F2`, `0x003B39B8` |
| ⁶ | `0x003B38D0`-`0x003B38DA` |
| ⁷ | `0x003B3981`-`0x003B3989` |
| ⁸ | `0x0040A1C1` |
| ⁹ | `0x0040A184`, `0x0040A19C` |
| ¹⁰ | `0x0024F4D0`, `0x0024F410` |
| ¹¹ | `0x003B39E0` |
| ¹² | `0x003B3807`-`0x003B3896` |
| ¹³ | `0x003B3812` |
| ¹⁴ | `0x003B382C`-`0x003B3881` |

</details>

The 125 character effect files `h0001`-`h0125` ([effect file list](effect-file-list.md)) are the files those
`chara\h` names reach. `0x0019FFD0` stores them into 144 model-name slots¹: 82 `m`, 27 `n`, 9
`g` and 26 `s` names, and 14 of the files serve more than one model.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001A003E`-`0x001A0793` |

</details>

### An instance handle's life

The model bind `0x0041F340` makes the handle: when the record's `+0x288` is −1 and the model row has an
`@FEF` entry, it calls `0x003B3550(record index, ticket id)` with the bank entry's ticket `+0x44` and
stores the id at record `+0x288` and row `+0x240` (`0x0041F6C8`-`0x0041F70A`,
[model effects](model-effects-and-motion-commands.md#the-records-effect-handle)). `0x003B3550` runs under
arena 8 (`0x0036C1D0(8, 10)`):

- it finds the ticket's context by a stack template `{type 3, word +4 = the ticket id's low 16 bits}`
  (`0x003B3594`; `0x0024F610` walks the list at `0x020910A0[3]` comparing the context's word `+0x04`, which
  `0x003B38B0` set from the same 16 bits at `0x003B3981`), and returns 0 without one;
- `0x003B3400` pops the handle free head `0x02EBDBA0`, appends it to the used tail (`0x02EBDBA8`, head
  `0x02EBDB98`) and stamps the serial; with no free handle `0x003B3550` returns 0;
- for a borrowing context (`+0x02` bit `0x4`) it publishes the context and its tables¹ and repairs it against a moved source (`0x0024D970` when the resolved
  `+0x860` plus `+0x864` differs from `+0x858`; [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md#repairing-effect-data-after-its-source-moves));
- every ticket context is a borrower: `0x003B38B0` sets bits `0x4` and `0x8` of its template's byte `+0x02`
 ² and `0x0024B3A0` copies the template into the context³, so the
  branch above always runs for a character effect;
- it zeroes a `0x3B0`-byte template, sets its word `+0x00` to `0x103` and dword `+0x04` to the handle
  id, and makes the instance with `0x0024B270` ([effect element runtime](effect-element-runtime.md#instances-emitters-and-elements));
- it clears bits `0x1` and `0x2` of the slot's flags `+0x30`, stores the instance at `+0x10` and the ticket
  id at `+0x18`, and fills the instance: `+0x08` the record index, `+0x340` the context, state word
  `+0x370` = `0x102` and `+0x373` = 1, scale 1.0 at `+0x320`-`+0x328` and `+0x39C`, colours
  `0x80808080` at `+0x330`, `+0x334` and `+0x398`, `0xFF` at `+0x2D0`, `+0x2E0` and `+0x2F0`;
- it sets `+0x368` bit `0x1` and `+0x378` bit `0x100`, takes `+0x368` bit `0x4000` and `+0x36A` bit `0x8` from bits `0x1` and `0x2`
  of byte `+0x17` of the record the context holds at `+0x48` (both clear without one), sets `+0x36A`
  bit `0x800`, and for a borrower copies the context's `+0x858` to `+0x390`; then it returns the id.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02F97340`, `0x02EBEF70`-`0x02EBEFA8` |
| ² | `0x003B3984` |
| ³ | `0x0024B3D3`-`0x0024B432` |

</details>

Three routines free handles. `0x003B3300(id)`, from the record teardown `0x0041E860`, ends the instance¹, moves the slot to the free list, keeps the id's slot and top bits and clears `+0x10`.
It does nothing for a stale id² and ends no instance when `+0x10` is null³; the slot goes to the free head with `+0x28` = 0⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024EE60` |
| ² | `0x003B3319`-`0x003B331B` |
| ³ | `0x003B3321`-`0x003B3324` |
| ⁴ | `0x003B332B`-`0x003B338D` |

</details>

`0x003B39E0(ticket id)`, from `0x003B37E0`, does the same list move for every stamped handle whose `+0x18`
names the ticket, without ending the instance (the ticket's context release ends it). `0x003B2F90`, from
the field teardown `0x0024E910`, walks the used list, ends every instance, frees every slot and then runs
`0x0024C460(3)` ([effect element runtime](effect-element-runtime.md#the-effect-teardown)).

`0x003B2F90` frees from the used head `0x02EBDB98` until the list is empty, skips `0x0024EE60` for a slot whose `+0x10`
is null, and reaches `0x0024C460(3)` by a tail jump, also when the list starts empty¹. Each
pass frees the slot the head's id names, `0x02EBD480 + 0x38 x (id & 0x3F)`, and only when that slot's dword
`+0x00` equals the id². On a mismatch it jumps to the loop test with the head it already
holds³, without the reload at `0x003B3044`, so the pass repeats without end.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B2F94`-`0x003B306C` |
| ² | `0x003B2FC0`-`0x003B2FD0` |
| ³ | `0x003B304B` |

</details>

### The per-frame flags

The slot's byte `+0x30` carries three bits the record's presentation pass sets and the effect passes
consume ([model effects](model-effects-and-motion-commands.md#the-records-effect-handle) lists the other
helpers that reach the instance through the handle):

- bit `0x1` is the advance permit: `0x003B3080(id)` sets it from the per-record presentation pass `0x0042D830`.
  The update pass `0x0024B9B0` looks the slot up by the instance's dword `+0x04` and, when the bit is set,
  clears it and lets the instance advance; when it is clear it holds the instance for that step
 ¹, so a model's effect advances only while its character is processed;
- bit `0x2` is the refresh token and bit `0x4` the visibility: `0x003B33A0(id, b)` sets bit `0x2` and stores `b` in
  bit `0x4`, from `0x0042D830`, the distance-fade callback `0x0042D7A0` and `0x0042CBF0`;
- the draw gate `0x0024D770(instance, consume)` reads them²: an instance whose
  slot has no token is not drawn unless its `+0x36A` bit `0x8` is set (then bit `0x4` is cleared instead); with
  `consume` set the token is cleared; bit `0x4` is copied into the instance's `+0x36A` bit `0x1`.
- before that arm the gate refuses every instance whose word `+0x364` is non-zero, then sets `+0x36A` bit `0x1`
  and picks its arm by the kind byte `+0x00` through the jump table `0x0024D920`; kind 3, the low byte of
  `0x003B3550`'s template word `0x103`, takes this one³;
- the arm takes the slot from the low six bits of the instance's dword `+0x04` without comparing the id
 ⁴, and passes the instance only when byte `+0x39B`, the last byte of the colour
  `+0x398` (`0x80` from `0x003B3550`), is non-zero⁵.
- kind 2 passes only when bit `0x2` is set in both the channel byte `0x02F8F23C` + word
  `+0x04` and the manager byte `0x02F8F27C` + word `+0x06`⁶; kind 4
  passes only when `0x003B2CA0(instance)`, which stops at a free record⁷, gives a
  record whose byte `+0x20` has bit `0x1` clear⁸; kinds 7 and 8 and every kind
  outside 2 to 9 pass
  (`0x0024D7AB`-`0x0024D7B1`, table entries 5 and 6).
- kinds 5, 6 and 9 share one arm⁹. It needs bit `1 << (kind - 1)` of the
  AND of the words `0x02092162`, `0x02092164` and `0x02092166`, or else an entry from
  `0x003B0BF0(dword +0x04)` whose byte `+0x13` has bits `0x6` equal to `0x2`
 ¹⁰. With `+0x36A` bit `0x10` set it also
  needs bit `0x1` of that AND¹¹.
- in the same arm an instance with `+0x36A` bit `0x8000` set is refused when
  `0x00254A70()` answers 0, bit `0x800` of the word `0x020926E4` is set and the dword `+0x04`
  differs from `0x002EF9F0(3)`¹².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024BB04`-`0x0024BB26` |
| ² | `0x0024D87B`-`0x0024D8DE` |
| ³ | `0x0024D799`-`0x0024D7CB` |
| ⁴ | `0x0024D87B`-`0x0024D88C` |
| ⁵ | `0x0024D8D7`-`0x0024D90F` |
| ⁶ | `0x0024D7CD`-`0x0024D7E9` |
| ⁷ | `0x003B2CB4` |
| ⁸ | `0x0024D8F4`-`0x0024D909` |
| ⁹ | `0x0024D7FC` |
| ¹⁰ | `0x0024D77A`-`0x0024D797`, `0x0024D7FC`-`0x0024D81B` |
| ¹¹ | `0x0024D81D`-`0x0024D82C` |
| ¹² | `0x0024D82E`-`0x0024D86E` |

</details>

`0x003B3B50` clears `+0x368` bit `0x2` of every stamped handle's instance and `0x003B3BA0(list, n)` sets it on
the instances whose `+0x08` is in the list: the hold a time stop puts on a character's effect
([effect element runtime](effect-element-runtime.md#the-effect-teardown),
[time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).

### The trigger and its ten states

`0x003B3C00(id, n)` signals the handle's instance¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B3C00`-`0x003B3C93` |

</details>

- `n` below 0 or above 10 returns 0; a stale id returns 0; a slot without an instance returns 0;
- `n` = 0 returns 1 and does nothing;
- `n` = 1 to 10: `0x003B3480(context, instance)` rebases a borrowing context against a moved source
  (the same repair as above, plus `0x0024D940` for the instance's `+0x390`), then under arena 8
  `0x0024FE70(instance, n)` runs the signal; `0x003B3480` does nothing for a context whose byte `+0x02`
  lacks bit `0x4`¹, and with an instance it makes the instance current² first;
- the signal makes the instance current; an instance without a player (`+0x130`) is started when its
  state byte `+0x370` is 2, the value the bind wrote³, or given a player when
  the state is 1 or 7 (`0x003A7460`, `0x0024FEF5`, with `+0x378` bit `0x400`), and the state becomes 1;
- it then opens the sub-entry that byte `+0x0A + n` of the emitter record names on the first player
  (`0x0024FF23`, `0x00333280`; [effect element runtime](effect-element-runtime.md#timeline-tracks)); `0x003B3C00`
  returns 1 when a sub-entry was opened, 0 when the cue byte is 0, when a player-less instance is in
  a state other than 1, 2 or 7, or when the start produced no player⁴.
- both starts take the instance's byte `+0x373`. For state 2 the signal sets `0x02092720` to 1 around `0x003A74F0`
  (an `n` of 0 leaves it as it was) and to 0 after it, and sets the state to 1 whether or not a player came
 ⁵. For states 1 and 7 the player is `[[0x02EBEFB0]]`, and only when it is non-null does
  the state become 1 and `+0x378` get bit `0x400`⁶;
- the cue byte is read from the player's emitter record `+0x80`, and the sub-entry is
  `0x0020E600(dword +0x2C + cue x 4)` of that record, opened with `0x00333280(player, sub-entry, n)`
 ⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B348A` |
| ² | `0x0024ED80` |
| ³ | `0x003A74F0`, `0x0024FEC7` |
| ⁴ | `0x0024FEE3`, `0x0024FF07` |
| ⁵ | `0x0024FEAF`-`0x0024FED9` |
| ⁶ | `0x0024FEFA`-`0x0024FF15` |
| ⁷ | `0x0024FF1C`-`0x0024FF42` |

</details>

So the ten states are the ten cue bytes `+0x0A + 1` to `+0x0A + 10` of the effect's record, and 0 is the
empty request. Two callers reach it: the dirty walk below, and `0x003B8670`, which looks a record up by
index¹ and passes its own dword `+0x04`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003326C0` |
| ² | `0x003B937C`-`0x003B939F` |

</details>

### The deferred write: charefftrigger

The script verb `charefftrigger(n)` (`0x325`, one argument; [verb table](../Scripts-And-Script-Commands/verb-table.md))
has the handler `0x003401D0`: it pops `n`¹ and calls `0x002E73C0(actor, n)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00267E10` |

</details>

`0x002E73C0` takes the
actor's presentation context (`+0xC0`), its record index (word `+0x00`, −1 for no record; a negative dword
`+0x00` also means no record, and a null actor or context returns at once, `0x002E73C3`-`0x002E73DD`) and the
render record
`[0x022C6F28] + index × 0x740` (the array pointer held at `0x022C6F28`, `0x002E73EA`; it returns when that address
is 0, `0x002E73F1`), and for a record whose `+0x284` is non-zero tail-jumps to
`0x003E6AA0(record, n)`, which stores `n` in bits `0xF8000000` of `+0x304` and sets `+0x294` bit `0x8000000`¹. Nothing plays yet.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E6AA0`-`0x003E6ABD` |

</details>

The dirty walk `0x00427DE0` delivers it: in its fourth pass, for a record with `+0x284` bit `0x40000000` clear¹, `+0x294` bit `0x8000000` set and a handle at `+0x288` (not −1, `0x0042864D`), it calls
`0x003B3C00(+0x288, +0x304 >> 27)` and clears the bit (`0x0042863B`-`0x00428660`;
[character render records](character-render-records.md#the-dirty-words)). A record without a handle
keeps the bit, so the request waits for the handle.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00428521` |

</details>

`0x003E6AA0` keeps only the low five bits of `n`
(`shl edx, 0x1B`, `0x003E6AB4`), so `n mod 32` is delivered: 11 to 31 are refused by `0x003B3C00`, and a
value whose low five bits are 1 to 10 (33, for example, or −31) plays that cue.

The same request is raised by other code: `0x002E73C0` from the chocobo ride (the off branch of the ride
setter `0x00303D90`, the turbo `0x00303F00`, the ride step `0x00304440`, the dismount `0x00304680` and
`0x002FE8D0`; all pass state 3 where the value is a constant, `0x00303E1B` and `0x003046BA`;
[party control modes](../Engine-Core/party-control-modes.md),
[chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md)).

`0x003E6AA0` is called from the
presentation command `0x28` (`0x00520720`, [authored presentation commands](authored-presentation-commands.md#the-registered-handlers))
and from the summon effect filter routines `0x003B4B60`, `0x003B4DA0`, `0x003B4E50`, `0x003B4FD0`, `0x003B5180`,
`0x003B54C0` and `0x003B5520` (six sites, called from `0x003B4FD0`), and from `0x003B8260`, which the battle
effect program `0x003B8670` calls twice and which passes 10 at `0x003B846F`.

A loaded effect file is signalled without the record: `0x003B2830(id, n)` calls
`0x0024FE70` on the queue entry's instance ([effect file loading](effect-file-loading.md)).

## Layouts

<details>
<summary>Show the memory layouts</summary>

### An effect ticket (0x38 bytes, 0x02EBCD80 + slot × 0x38)

| Offset | Type | Field |
|---|---|---|
| `+0x00` | `u32` | id: slot in the bits under mask `0x3F`, serial `0x02EBDBB0` in the bits under mask `0xFFFFFC0`, 3 in the bits under mask `0xF0000000` |
| `+0x08` | `void*` | the resolved source plus the `@FEF` section offset (`0x003B396E`); 0 at start-up and release |
| `+0x10` | `u64` | 0 at start-up, allocation and release (`0x003B3963`, `0x003B3892`); no reader |
| `+0x18` | `void*` | the effect context `0x0024B3A0` built (`0x003B39A9`); read by the release to cancel it |
| `+0x20` | `void*` | next record in its list |
| `+0x28` | `void*` | previous record in its list |
| `+0x30` | `i32` | the effect number from the `chara\h%d.efx` name (`0x003B3B10`): −1 when the name's number does not parse or after a release; a source without `chara\h` leaves the old value |
| `+0x34` | `u8[4]` | 0 from start-up's qword store; not touched afterwards |

### An instance handle (0x38 bytes, 0x02EBD480 + slot × 0x38)

| Offset | Type | Field |
|---|---|---|
| `+0x00` | `u32` | id: slot in bits `0x3F`, serial `0x02EBDBB4` in the bits under mask `0xFFFFFC0`, 3 in the bits under mask `0xF0000000` |
| `+0x08` | `u8[8]` | 0 from start-up; not touched afterwards |
| `+0x10` | `void*` | the `0x3B0`-byte instance (`0x003B367A`); 0 at start-up and on every release |
| `+0x18` | `u32` | the ticket id the instance was made for (`0x003B367E`); `0x003B39E0` matches it |
| `+0x1C` | `u8[4]` | 0 from start-up's qword store; not touched afterwards |
| `+0x20` | `void*` | next record in its list |
| `+0x28` | `void*` | previous record in its list |
| `+0x30` | `u8` | flags: bit `0x1` the advance permit, bit `0x2` the refresh token, bit `0x4` the visibility value |
| `+0x31` | `u8[7]` | 0 from start-up's qword store; not touched afterwards |

### The render record's trigger fields

- `+0x288` `u32`: the instance handle id: −1 before a bind; `0x0041F703` stores `0x003B3550`'s result
  unconditionally, so after a failed bind (no context, no free handle, or `0x0024B270` returning 0,
  `0x003B37A7`) it is 0, which names no slot and, since the bind runs only on −1, is never retried. A
  failed `0x0024B270` also leaves the handle `0x003B3400` took on the used list with `+0x10` = 0.
- `+0x294` bit `0x8000000`: the pending trigger, set by `0x003E6AA0`, cleared by the dirty walk at `0x00428660` once it is delivered.
- `+0x304` bits `0xF8000000`: the requested state, written by `0x003E6AA0` and read at `0x00428652`.

The access tables beside this page list every instruction reaching a record of either table:
[the tickets](character-effects-effect-ticket-accesses.tsv) and
[the instance handles](character-effects-instance-handle-accesses.tsv).

</details>

## State

<details>
<summary>Show the state it keeps</summary>

- `0x02EBDB80` and `0x02EBDB90`: the ticket used list's head and tail; `0x02EBDB88` its free head.
- `0x02EBDB98` and `0x02EBDBA8`: the handle used list's head and tail; `0x02EBDBA0` its free head.
- `0x02EBDBB0` and `0x02EBDBB4`: the two serials, one per table.
- `0x02F97340`: the current context, which `0x003B3550` and `0x003B3480` publish for a borrowing context.

</details>

## Modding notes

- A handle is only an id: nothing dangles. To play with a model's effect from a hook, take `+0x288` of
  its render record and go through `0x003B3C00` or the helpers; a stale id is refused silently.
- The trigger states are the record's cue bytes, so a model whose `@FEF` authors no cue at `+0x0A + n`
  plays no cue for `charefftrigger(n)`; an instance without a player is still started by the signal
  before the cue byte is read. Only the low five bits of `n` are kept: 11 to 31 are refused, 32 and
  above wrap.
- The serial wraps at 2^22 allocations per table: one per model bind¹ and one per `@FEF`
  registration². A hook that allocates in a loop reaches it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0041F6FE` |
| ² | `0x0040A174` |

</details>

## Related

- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md): the registration that makes a ticket and the disposal order.
- [Model effects and motion commands](model-effects-and-motion-commands.md): `@FEF`, the record's effect handle and its helpers.
- [Effect element runtime](effect-element-runtime.md): the instance, the update pass, the signal and the teardown.
- [Effect file list](effect-file-list.md): the character effect files the ticket numbers name.
- [Character render records](character-render-records.md): the dirty words the deferred write uses.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 74 calls with 19 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [debug menu](../Engine-Core/debug-menu.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [ko and game over](../Status-Effects-And-KO/ko-and-game-over.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0024E910`](effect-lifecycle.md) (on effect lifecycle) | is called by | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003B8670`](effect-file-loading.md) (on effect file loading) | calls | [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes)<br>[`0x0026A430`](effect-file-loading.md) (on effect file loading)<br>[`0x002EB740`](character-effects.md)<br>[`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |

**Sound and music** (explained on [animation sounds](../Sound-And-Music/animation-sounds.md), [force fight mode](../Engine-Core/force-fight-mode.md), [effect drawing](effect-drawing.md), [sound effects](../Sound-And-Music/sound-effects.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [effect anchors and targets](effect-anchors-and-targets.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003326C0`](character-effects.md) | is called by | [`0x00332C40`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |
| [`0x003B3E40`](character-effects.md) | calls | [`0x002DF0F0`](../Sound-And-Music/sound-effects.md) (on sound effects) |
| [`0x003B3E40`](character-effects.md) | is called by | [`0x003B3D20`](effect-drawing.md) (on effect drawing) |
| [`0x003B3EA0`](character-effects.md) | calls | [`0x002DF170`](../Sound-And-Music/sound-effects.md) (on sound effects) |
| [`0x003B3EA0`](character-effects.md) | is called by | [`0x00332C40`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |
| [`0x003B8670`](effect-file-loading.md) (on effect file loading) | calls | [`0x002DF660`](../Sound-And-Music/audio-manager.md) (on audio manager)<br>[`0x003B3EA0`](character-effects.md)<br>[`0x003B99D0`](effect-anchors-and-targets.md) (on effect anchors and targets) |

**Battle actions** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [battle orders](../Battle-Actions/battle-orders.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0024F410`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) | is called by | [`0x002FC3C0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x002E73C0`](character-effects.md) | is called by | [`0x002FE8D0`](character-effects.md) |
| [`0x00303D90`](character-effects.md) | is called by | [`0x00306760`](../Party/party-table.md) Battle action: update special presentation sequence (on party table) |

**Engine core** (explained on [global state accessors](../Engine-Core/global-state-accessors.md), [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) | calls | [`0x001EDDA0`](effect-lifecycle.md) (on effect lifecycle) |
| [`0x00259180`](../Engine-Core/startup-constants.md) (on startup constants) | is called by | [`0x0022A0B0`](../Saving-Loading-And-Settings/languages.md) (on languages) |
| [`0x003B8670`](effect-file-loading.md) (on effect file loading) | calls | [`0x001EDDA0`](effect-lifecycle.md) (on effect lifecycle) |

**Gameplay** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00303F00`](character-effects.md) | calls | [`0x0030D9A0`](../Scripts-And-Script-Commands/party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 (on party during scenes) |
| [`0x00304440`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) | calls | [`0x0030D9A0`](../Scripts-And-Script-Commands/party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 (on party during scenes) |
| [`0x00304680`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) | is called by | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |

**Movement and pathfinding** (explained on [party control modes](../Engine-Core/party-control-modes.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md), [effect anchors and targets](effect-anchors-and-targets.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00304440`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) | calls | [`0x00311E20`](../Engine-Core/party-control-modes.md) (on party control modes) |
| [`0x003B8670`](effect-file-loading.md) (on effect file loading) | calls | [`0x0024B6F0`](effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0024C6B0`](effect-element-runtime.md) (on effect element runtime)<br>[`0x0024C870`](effect-element-runtime.md) (on effect element runtime)<br>[`0x0024F9B0`](effect-file-loading.md) (on effect file loading)<br>[`0x00265200`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0026AF80`](effect-file-loading.md) (on effect file loading)<br>[`0x0026B5A0`](effect-file-loading.md) (on effect file loading) |

**Party** (explained on [party control modes](../Engine-Core/party-control-modes.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E73C0`](character-effects.md) | is called by | [`0x00303F00`](character-effects.md) |
| [`0x00303D90`](character-effects.md) | calls | [`0x0031ABF0`](../Engine-Core/debug-menu.md) (on debug menu) |
| [`0x00303F00`](character-effects.md) | calls | [`0x0031ABF0`](../Engine-Core/debug-menu.md) (on debug menu) |
| [`0x00304440`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) | calls | [`0x00303CC0`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x0031ABF0`](../Engine-Core/debug-menu.md) (on debug menu) |
| [`0x00304680`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) | calls | [`0x0031ABF0`](../Engine-Core/debug-menu.md) (on debug menu) |

**Game files and data tables** (explained on [resource lifecycle](../Game-Files-And-Data-Tables/resource-lifecycle.md), [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md), [resource sections](../Game-Files-And-Data-Tables/resource-sections.md), [identifier spaces](../Engine-Core/identifier-spaces.md), [character render records](character-render-records.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0024F410`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) | is called by | [`0x003B37E0`](character-effects.md) |
| [`0x0024F4D0`](character-effects.md) | is called by | [`0x003B37E0`](character-effects.md) |
| [`0x003B37E0`](character-effects.md) | is called by | [`0x00409CA0`](character-effects.md)<br>[`0x00409D60`](character-effects.md) |
| [`0x003B38B0`](character-effects.md) | is called by | [`0x00409FE0`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) |
| [`0x003B39E0`](character-effects.md) | is called by | [`0x003B37E0`](character-effects.md) |
| [`0x003B3B10`](character-effects.md) | is called by | [`0x00409FE0`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) |
| [`0x003B8260`](character-effects.md) | calls | [`0x002ED570`](skeleton-entries-and-bones.md) Resource table: resolve entry by index (on skeleton entries and bones) |
| [`0x00409CA0`](character-effects.md) | calls | [`0x002ED570`](skeleton-entries-and-bones.md) Resource table: resolve entry by index (on skeleton entries and bones)<br>[`0x003B37E0`](character-effects.md)<br>[`0x00409730`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal)<br>[`0x0051FCF0`](skeleton-entries-and-bones.md) (on skeleton entries and bones)<br>[`0x0051FE30`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) |
| [`0x00409D60`](character-effects.md) | calls | [`0x002ED570`](skeleton-entries-and-bones.md) Resource table: resolve entry by index (on skeleton entries and bones)<br>[`0x003B37E0`](character-effects.md)<br>[`0x00409730`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal)<br>[`0x0051FCF0`](skeleton-entries-and-bones.md) (on skeleton entries and bones)<br>[`0x0051FE30`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) |
| [`0x00409FE0`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) | calls | [`0x001D6EC0`](effect-file-list.md) (on effect file list)<br>[`0x002DF960`](../Game-Files-And-Data-Tables/file-size-tables-fst.md) (on file size tables fst)<br>[`0x002ED570`](skeleton-entries-and-bones.md) Resource table: resolve entry by index (on skeleton entries and bones)<br>[`0x00409710`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal)<br>[`0x00409A30`](animation-playback.md) (on animation playback)<br>[`0x00409A60`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal)<br>[`0x0051FBB0`](character-render-records.md) (on character render records)<br>[`0x0051FE30`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) |
| [`0x0041F340`](animation-playback.md) (on animation playback) | calls | [`0x002ED570`](skeleton-entries-and-bones.md) Resource table: resolve entry by index (on skeleton entries and bones)<br>[`0x00409660`](../Game-Files-And-Data-Tables/resource-sections.md) (on resource sections)<br>[`0x00409F50`](model-files-cm-ca.md) (on model files cm ca)<br>[`0x00409FA0`](animation-playback.md) (on animation playback) |

**Scripts and script commands** (explained on [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E73C0`](character-effects.md) | is called by | [`0x003401D0`](character-effects.md) |
| [`0x00303F00`](character-effects.md) | is called by | [`0x0050F8A0`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) |
| [`0x003401D0`](character-effects.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**Menus and HUD** (explained on [frame update order](../Engine-Core/frame-update-order.md), [small bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0024ED80`](effect-drawing.md) (on effect drawing) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x0024EE60`](character-effects.md) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x00303F00`](character-effects.md) | is called by | [`0x003CAB00`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) |
| [`0x003A74F0`](effect-lifecycle.md) (on effect lifecycle) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00304440`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) | is called by | [`0x00234590`](../Battle-Actions/quickenings-and-summons.md) Battle system: run field frame orchestrator (on quickenings and summons) |

</details>
