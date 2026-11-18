[Home](../../README.md) / [Scripts and script commands](README.md) / Script interpreter

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Script interpreter: the hundred opcodes, the value stack, the registers and how a script waits and resumes | system | Scripts and script commands | The script machine | The bytecode interpreter 0x0025E4C0 that runs every zone script: who calls it each frame, the 100-entry opcode dispatch and the two coupled tables that drive it, the shared value stack at 0x02099AC0, the per-actor registers, the wait slot that lets a native call suspend and resume at the same instruction, the instruction budget and the stop rule, and what each of the hundred opcodes does, with the full table in script-interpreter-opcodes.tsv. | 0x0025E4C0, 0x0025DF00, 0x0025D9E0, 0x00261DF8, 0x01EFEA60, 0x02099AC0, 0x00267E10, 0x00267DB0, 0x00267F90, 0x00267F60, 0x0025D740, 0x00267560, 0x002621D0, 0x003589E0, 0x008620C0, 0x0025B500, 0x0025E60A, 0x0025E613 |

## What the player sees

Every door, treasure chest, townsperson, cutscene and boss script in the game is bytecode in the
area's script file, run by one interpreter a little at a time each frame. When a script tells an
actor to walk somewhere and wait, the interpreter stops at that instruction, hands the frame back
to the game, and picks the same instruction up next frame until the walk is done. Nothing a player
sees is drawn by the interpreter itself; it only decides what the engine is asked to do next.

## How it works

### Who runs it

Once per frame the field runtime pass `0x0025D9E0` walks the actor manager slots
(`0x02098E10 + index × 0x288`) and runs `0x0025DF00(slot, actor)` for each world actor. That driver
selects the actor's current wait slot, `[actor + 0xA8] + (s8)[actor + 0x11] × 0x28`, and acts on
its kind byte `+0x14`: kinds 1 and 2 enter the interpreter, `0x0025E4C0(slot, actor, waitSlot)`,
with `0x02099D80` set to the actor for the duration.

Kinds 3 to 7 are waits on another actor's
entry, a notification, a channel bit or a list ([script requests](script-requests.md)), and a
wait that is satisfied becomes kind 1 and runs in the same call. The interpreter has exactly one
call site, `0x0025E0D3` in that driver.

### Entry, budget and stop

The interpreter keeps the manager slot in `r13`, the actor record in `r15`, the wait slot in `rsi` and the program
counter in `r14`, loaded from the wait slot's first qword.

It zeroes the shared stack depth at `0x02099AC0` before any test (`0x0025E4D8`), then checks the actor's flag byte
`+0x14`: bit `0x40` (halted) returns 1 at once (`0x0025E4FF`-`0x0025E502`, `0x0025E511`); bit `0x10` clear returns 1 after
`0x0025B500(actor)` (`0x0025E504`-`0x0025E50C`); when `+0x13` bit `0x1` is set or `+0x10C` is non-zero, `+0x0B` bit `0x20`
must be set or the call returns 1 without that call (`0x0025E524`-`0x0025E53A`); and then bit `0x20` clear returns 1 after
`0x0025B500(actor)` (`0x0025E53C`-`0x0025E53F`).

The loop has a budget of `0x10000` instructions per call (`0x0025E4FA`), which ends the call only through the stop rule
below. Each iteration fetches the opcode byte at the PC; for opcodes at or above `0x47` it also pre-decodes a
little-endian 16-bit operand from the two following bytes (`0x0025E5A9`-`0x0025E5C2`), which is one opcode early (`0x47`
has length 1).

It loads the slot's skip mask `+0x201` ([native commands](native-commands.md)) into `edx`, refuses opcodes above
`0x63` to the stop arm (`0x0025E5D1`-`0x0025E5D4`), and jumps through the table at `0x00261DF8`: 100 image-relative 32-bit
offsets rebased on `0x00120000`, every target inside the interpreter itself. 92 targets are distinct; `0x01`, `0x02`,
`0x19`, `0x1A`, `0x31` and `0x47` share the stop arm `0x0025E60A`, `0x2A` to `0x2C` share `0x0026121A`, and `0x51` and
`0x60` share `0x002618A8`.

Two epilogues end a handler. `0x0025E60A` raises the stop request and falls into `0x0025E613`, which
advances the PC by the instruction's length, read as a signed word at `0x01EFEA60 + opcode × 24`:
0 for `0x00` to `0x02`, 1 for `0x03` to `0x47`, 3 for `0x48` to `0x63`.

Every loop head decrements the budget counter, a signed dword (`0x0025E570`), and a negative result raises the stop flag
(`0x0025E57B`-`0x0025E57D`); with the counter not negative and the flag clear the head goes straight to the fetch
(`0x0025E579`, `0x0025E586`-`0x0025E588`). With the flag raised:

- an empty stack ends the call (`0x0025E58A`-`0x0025E58D`), the only jump to the exit;
- a non-empty stack is cleared to depth 0 (`0x0025E593`-`0x0025E596`) before the next instruction runs.

The counter first goes negative at the head after instruction 65,536 and stays negative through
head 65,536 + 2^31, 2^31 heads in all, each of which raises the flag again. So once the budget is
spent, the call ends at the first of those heads that finds the stack empty: every instruction that
leaves a value on the stack is followed by one more.

A push at depth 63 is refused and the PC advances as usual (`0x0025E696`-`0x0025E69A`, `0x0025F226`; the
int push `0x00267F90` at `0x00267F93`-`0x00267F96`), so the push limit never ends the loop. Once the budget
is spent the clear resets the depth before each instruction, so no push is refused.

The stop arm, the wait arms and a busy native call raise the same flag. The CALL handlers store the
result of `0x002621D0` into it (`0x002619BB`, `0x00261A1E`, `0x00261AD9`), so a finished verb lowers it. The
return opcodes `0x2D` to `0x30` store 1 or the result of `0x0025B400`, which is 1 or 0 (`0x0025B441`,
`0x0025B45F`), into it (`0x002612F5`, `0x00261397`, `0x0026146F`, `0x002614D7`), so a return can raise or lower it.

The exit stores the PC into the wait slot (`0x00261DD3`) and returns 0 when the last opcode run is `0x58`,
`0x59`, `0x5D` or `0x5E` (`0x00261DC1`-`0x00261DE3`), and the flag's value otherwise (`0x00261DE6`).

### The value stack

`0x02099AC0` is one static stack for every script: depth at `+0`, a tag byte per entry at `+4`
(1 int, 2 float), a kind byte at `+0x44` (below), a reserved dword at
`+0x84` and the 32-bit value at `+0x184`, 64 entries. `0x00267F90` pushes an int and `0x00267F60` a
float, both refusing silently at depth 63, and both store kind 6 (`0x00267F9D`, `0x00267F78`). The
reference push `PUSHP` (`0x00268100`) stores the element's width nibble instead, its descriptor shifted
right by 28 (`0x00268150`-`0x00268185`; [References](script-variables.md#references)).

`0x00267E10` pops as an int, truncating a float entry;
`0x00267DB0` pops as a float, widening an int entry. On an empty stack the int pop returns 0
silently and the float pop returns 0 after calling `0x008620C0`, the leaf that loads the address of the message
`FFXII tried to call exit(), this might be a serious error!` and tail-jumps to the empty stub `0x0016D6A0`, so it
does nothing (`0x008620C0`-`0x008620C9`).

The int pop calls that
leaf only for a tag that is neither 1 nor 2, and then returns 0 with the entry already popped
(`0x00267E1A`-`0x00267E3B`). The float pop returns 0.0 for such a tag without the call, also with the
entry already popped (`0x00267DCF`, `0x00267DFC`).

`0x00267560` reports whether the top two entries are both ints, which the arithmetic
opcodes use to choose an integer or a float path. At a depth below 2 it calls `0x008620C0` and
answers 0 (`0x00267572`-`0x0026757C`).

`0x0025D740` pops two operands and returns -1, 0 or 1 for the six comparisons: 0 when they are equal,
-1 when the operand pushed first is the smaller, and 1 otherwise. When both top tags are 1
(`0x0025D7B8`-`0x0025D7C0`) it pops two ints and compares them signed (`0x0025D839`-`0x0025D859`). Otherwise
it pops two floats, widening an int entry, and compares them with `ucomiss` and `comiss`
(`0x0025D8B2`-`0x0025D8D6`); a NaN operand gives 1.

`0x0025D740` calls `0x008620C0` for a depth below 2: once on entry (`0x0025D75B`) and again for each pop
that finds the stack empty (`0x0025D870`, `0x0025D8AD`), and each missing operand counts as 0.0. A tag
that is neither 1 nor 2 gives 0.0 without the call (`0x0025D78D`, `0x0025D890`). The int path's calls for
such a tag (`0x0025D7E9`, `0x0025D80C`) are never reached, because that path runs only when both top tags
are 1.

### Registers

A script has eight persistent registers in its actor record, `I0` to `I3` at `+0x64` to `+0x70`
(ints) and `F0` to `F3` at `+0x74` to `+0x80` (floats), reached only by the sixteen opcodes
`0x36` to `0x45`; nothing native reads or writes them, and nothing clears them when a record is
reused.

Three more live in the wait slot: `X` at `+8` (the target actor of a native call), `Y` at `+0xC` (the comparison value
of the compare-and-jump opcodes and the result word of a native call) and `A` at `+0x10` (the accumulator the
`…POPA` call forms fill). The slot's `+0x14` is the wait kind, `+0x15` the native call's phase, and `+0x18` onward
its scratch.

`PUSHA`, `PUSHX` and `PUSHY` (`0x1B`, `0x1D`, `0x1E`) push the register as an int through the push at `0x0025E75A`, and
`POPA`, `POPX` and `POPY` (`0x1C`, `0x1F`, `0x20`) pop one value inline into it as `0x00267E10` would: an int as it is,
a float through `cvttss2si`, 0 for an empty stack, 0 after `0x008620C0` for any other tag (`0x0025F322`-`0x0025F48E`).

The manager slot supplies the script image: `+0` the bound definition, `+0x68` the int constant
pool and `+0x70` the float pool (`PUSHI`, `PUSHF`), `+0x78` the variable descriptors
([script variables](script-variables.md)), `+0x80` the per-actor tag tables and `+0x28` the
slot index. The actor record supplies `+0x58`, the bytecode base, `+0x48`, the function table
the request funnel bounds-checks, and `+0x50`, the jump table the jump opcodes index through
`0x003589E0`; an operand at or past its count yields offset 0, so the PC lands on the bytecode
base.

`PUSHACT` reads word `+0xE` of entry `index × 16` of the `+0x80` table for the handle's high word
and leaves the index at `0x02099AB8`. `PUSHTAG` takes that index, selects entry `(index + 1) × 16`,
adds `[slot + 0]` to its dword to reach that actor's tag table and pushes its `[operand × 8 + 8]`
dword, `0x8000` past its count: `PUSHACT n; PUSHTAG k` reads actor `n`'s tag `k`.

### The hundred opcodes

The descriptor table at `0x01EFEA60` has 100 records of 24 bytes: the length word at `+0` is the
only field the engine reads (22 sites, all `opcode × 24`), and the mnemonic pointer at `+8` names
opcode N + 1, so `NOP`'s string at `0x00D11A10` has no record and record 99's slot holds an
unrelated global. [script-interpreter-opcodes.tsv](script-interpreter-opcodes.tsv) gives every
opcode its mnemonic, length, handler and effect. By family:

| Opcodes | Family | Effect |
|---|---|---|
| `0x00` NOP | | advance only |
| `0x03` SYSHALT | halt | sets actor `+0x14` bit `0x40`, rewinds the pc to itself and runs on into the stop arm, raising the stop flag (`0x0025E5EA`-`0x0025E611`); while the bit is set the entry check returns at once, and request selection clears it when it selects an entry (`0x003DB774`) |
| `0x04` SYSTEM | | pops and discards one value |
| `0x05` to `0x09`, `0x10`, `0x11`, `0x17`, `0x18` | logic | pop two (or one) ints, push the logical or bitwise result; `OPSRL` is an arithmetic shift |
| `0x0A` to `0x0F` | compare | `0x0025D740` on two operands, push 0 or 1 for `== != > < >= <=` |
| `0x12` to `0x16` | arithmetic | int when both operands are ints, float otherwise; `OPDIV` yields 0 on a zero divisor, `OPMOD` is an integer `idiv` with no zero test |
| `0x1B` to `0x20` | registers | push or pop `A`, `X`, `Y` |
| `0x21` to `0x29` | requests | pop channel, function and actor and file a request: kinds `REQ` / `FREQ` / `TREQ`, modes plain, start-wait (`SW`) and end-wait (`EW`) |
| `0x2A` to `0x2C`, `0x33` | | pop their arguments and file nothing (`PREQ…`, `PREQWAIT`) |
| `0x2D` to `0x30` | return | retire the entry and resume the caller; `N` forms recycle the entries above a popped depth; `T` forms start the next entry |
| `0x32`, `0x34`, `0x35` | waits | `REQWAIT` parks on another actor's entry (kind 3); `REQCHG` sets an actor's override slot; `REQCANCEL` recycles entries |
| `0x36` to `0x45` | registers | pop into or push from `I0` to `I3`, `F0` to `F3` |
| `0x46` DVAR | | pops one value and calls the stubbed debug-variable hook `0x0016D6A0([slot + 0x28], value, &0x02099D48)`, a bare `ret` |
| `0x48` to `0x4B` | variables | push, pop, print and reference a variable by its descriptor |
| `0x4C` to `0x50` | immediates | push a tag, an actor handle, a pooled int, the operand itself or a pooled float |
| `0x51` to `0x57`, `0x5A` to `0x5C`, `0x60` | jumps | `JMP` to `base + table[operand]`; the `POPCMPY…` forms pop a value and jump on its comparison with `Y`; `POPX…` pop into `X` and jump always, if non-zero or if zero |
| `0x58`, `0x59`, `0x5D`, `0x5E` | native calls | run verb `operand` through `0x002621D0`; `ACT` forms pop the target actor into `X` first; `POPA` forms pop the result into `A` |
| `0x5F`, `0x61`, `0x63`, `0x62` | lists | request or wait on a whole actor list; `INCINITTAG` marks a channel requested without filing; while the skip mask is non-zero, `0x5F` and `0x63` first wait as wait kind 7 until no listed actor has the channel's bit set ([field runtime](../Characters-And-Objects/field-runtime.md); `0x00261B15`, `0x00261C12`, `0x00261B97`), then make the request |
| `0x01`, `0x02`, `0x19`, `0x1A`, `0x31`, `0x47` | | no handler: the stop arm; no shipped script uses them |

`SYSTEM` (`0x04`) pops one value with `0x00267E10` and drops it; like many handlers it ends in the tail
`0x0025E651`-`0x0025E662`, which reloads the depth and goes on to `0x0025E613` (`0x0025E649`-`0x0025E662`).

`OPLOR` (`0x05`) pops two ints with `0x00267E10` and pushes 1 when either is non-zero, else 0 (`0x0025E664`-`0x0025E68C`).
`OPLAND` to `OPAND` (`0x06` to `0x09`) pop their two ints inline by the same rules: an empty stack gives 0, a float
entry goes through `cvttss2si` and any other tag gives 0 after a call of `0x008620C0` (`0x0025E6D8`-`0x0025E74D`,
`0x0025E7A0`-`0x0025E7C8`). `OPLAND` pushes 1 when both are non-zero, else 0 (`0x0025E750`, `0x0025E7D0`-`0x0025E7E2`).

`OPOR`, `OPEOR` and `OPAND` push the bitwise or, exclusive or and and of the two (`0x0025E86F`, `0x0025E92A`, `0x0025E9E5`;
handlers `0x0025E7E7`-`0x0025E8A0`, `0x0025E8A2`-`0x0025E95B` and `0x0025E95D`-`0x0025EA16`). Each of the five pushes inline as
`0x00267F90` does: tag 1, kind 6, the reserved dword 0 and the value, then the depth plus 1, with nothing stored at
depth 63 (`0x0025E68F`-`0x0025E6D3`, `0x0025E762`-`0x0025E79B`, `0x0025E869`, `0x0025E924`, `0x0025E9DF`).

`OPEQ` to `OPLSE` (`0x0A` to `0x0F`) each call `0x0025D740` and push 1 when its answer is 0 (`OPEQ`), not 0 (`OPNE`), 1
(`OPGT`), -1 (`OPLS`), not -1 (`OPGTE`) or not 1 (`OPLSE`), and 0 otherwise, through the push at `0x0025E68F`
(`0x0025EA18`-`0x0025EAA3`).

`OPSLL` and `OPSRL` (`0x10`, `0x11`) pop the count and then the value with the inline int pop and push the value moved
by `shl` or `sar` by `count & 0x1F`, the part of the count those instructions use; at depth 63 nothing is stored
(`0x0025EAA8`-`0x0025EB84`, `0x0025EB86`-`0x0025EC62`).

`OPADD` (`0x12`) has `0x00267560` inline: below depth 2 it calls `0x008620C0` and takes the float path
(`0x0025EC64`-`0x0025EC6C`), and when the top two tags are both 1 it pops two ints inline and pushes their sum as an int
(`0x0025ECBA`-`0x0025EDBE`). `OPSUB`, `OPMUL` and `OPDIV` (`0x13` to `0x15`) call `0x00267560` and on the int path pop with
`0x00267E10` and push `first - last`, `first * last` or `first / last`, `first` being the operand pushed first
(`0x0025EE79`-`0x0025EEA2`, `0x0025EF92`-`0x0025EFB9`, `0x0025F0AC`-`0x0025F0DE`).

The float paths of the four pop both operands inline as `0x00267DB0` does, an int converted, an empty stack 0.0 after
`0x008620C0` and any other tag 0.0 without the call, and push the result with tag 2 and kind 6, nothing at depth 63
(`0x0025EC7F`-`0x0025EE74`, `0x0025EEA7`-`0x0025EF8D`, `0x0025EFC1`-`0x0025F0A7`, `0x0025F0E3`-`0x0025F1D1`).

The float `OPDIV` pushes 0.0 for a divisor equal to 0.0 and `first / last` otherwise, a NaN divisor included
(`0x0025F197`-`0x0025F1A3`). `OPMOD` (`0x16`) pops two ints with `0x00267E10` and pushes `first % last` as `idiv` leaves it
in `edx` (`0x0025F1D6`-`0x0025F221`); a refused push of `OPSUB` to `OPMOD` goes to `0x0025F226`-`0x0025F22D`, of `OPADD` to
`0x0025E61B` (`0x0025ED66`, `0x0025EE49`).

`OPNOT` and `OPBNOT` (`0x17`, `0x18`) pop one int inline and push 1 when it is 0 and 0 otherwise, or `~v`
(`0x0025F232`-`0x0025F2B6`, `0x0025F2B8`-`0x0025F320`).

`REQ` (`0x21`) submits with `0x00268850(slot, actor, stack, wait slot, PC, 0, 1)` and does not use the answer
(`0x0025F7B6`-`0x0025F7D0`). With the skip mask at 0 that call is the whole arm (`0x0025F493`-`0x0025F495`). With the mask
non-zero and the wait slot's byte `+0x15` at 0 (`0x0025F49B`-`0x0025F49F`) the arm first pops the function id, the target
and the channel itself: an int as it is, a float through `cvttss2si`, an empty stack 0, any other tag 0 after
`0x008620C0(1)` (`0x0025F4A5`-`0x0025F56B`, `0x0025F5FF`-`0x0025F64E`).

Bit `0x8000` in the function id or the target puts the three values back and submits (`0x0025F56E`-`0x0025F577`,
`0x0025F677`). Otherwise the channel's low byte goes to the wait slot's `+0x26` and the arm calls
`0x00358940(slot, target)` and `0x003DB640(that record, channel)` (`0x0025F57F`-`0x0025F593`). An answer of 0 puts the three
values back and submits (`0x0025F598`-`0x0025F59A`, `0x0025F653`-`0x0025F70D`). The values go back channel first, and a value
is left out once the depth is 63 or more (`0x0025F66C`, `0x0025F6AD`, `0x0025F6E1`).

A non-zero answer arms the wait instead of submitting: `0x0020E620(record)` goes to the wait slot's
`+0x18`, the target's low word to `+0x24`, the function id's low word to `+0x20`, 0 to `+0x27` and the
word `0x0106` to `+0x14`, and the stop flag is set to 1 (`0x0025F5A0`-`0x0025F5FA`). The arm stores the
address of the `REQ` less its length in the wait slot (`0x0025F5DA`-`0x0025F5ED`) before the tail adds the
length back (`0x0025E61B`-`0x0025E641`), so the address of the `REQ` itself is what the exit store `0x00261DD3`
then writes there.

When the arm runs again with `+0x15` non-zero it pushes byte `+0x26`, word `+0x24` and word `+0x20`,
each zero-extended and each only below depth 63, clears `+0x15` and submits (`0x0025F712`-`0x0025F7B2`).

`RET` (`0x2D`) keeps the answer of `0x003DB2A0(actor, byte +0x62)`, calls `0x003DB6E0(actor)` and takes the
wait slot `[actor + 0xA8] + 0x28 × (s8)[actor + 0x11]` as it is after that call
(`0x00261239`-`0x00261260`). With the actor's byte `+0x10` non-zero it lowers that byte by 1, loads the PC
from the new wait slot and sets the stop flag to 1 (`0x00261264`-`0x0026129A`). With `+0x10` at 0 and bit
`0x40` of `+0x14` set it sets the flag to 1 and loads no PC: the PC stays the one after the `RET`,
while `rsi` already holds the new wait slot (`0x0026129F`, `0x002602F2`).

Otherwise `RET` calls `0x0025B400(actor)`, replaces its answer by 1 when `0x003DB2A0` answered 0, and loads
the PC from the new wait slot. The stop flag takes that value when the new wait slot's byte `+0x14` is
1, and 1 for any other kind (`0x002612AA`-`0x002612F5`).

`RETT` (`0x2F`) does the same, with one more call on its last path: after `0x0025B400` it calls
`0x003DBDC0(actor, 0x003DB550(actor, byte +0x62))`, and only then loads the PC from the new wait slot
(`0x002613DD`-`0x00261476`). Its path for a non-zero `+0x10` is the one inside `RETN`
(`0x00261352`-`0x0026136C`), which joins `RET` at `0x00261273`. On its path for bit `0x40`, `rsi` still
holds the old wait slot (`0x00261401`-`0x00261406`).

`REQCANCEL` (`0x35`) calls `0x003DB420(actor, popped value + 1, 1)` and does not use the answer
(`0x00261301`-`0x00261312`). `PUSHV` (`0x48`) calls `0x00267FC0(slot, actor, stack, operand)` with the operand
zero-extended from 16 bits (`0x00261761`-`0x0026176E`).

`0x5F` calls `0x00268A80(slot, actor, stack, operand, actor, 0)`, and `0x63` the same with 1 as the sixth
argument (`0x00261BEA`-`0x00261C01`, `0x00261CA4`, `0x00261CC4`). With the skip mask non-zero and byte `+0x15`
at 0 both first find the list: the table is at `image + 0x0020E600(image dword +0x30)`, and for an operand
below the table's first dword the list is at `image + 0x0020E600(table dword +4 + 4 × operand)`; any
other operand gives null (`0x00261B27`-`0x00261B55`, `0x00261C24`-`0x00261C52`).

`0x0020E620` of that address goes to the wait slot's `+0x1C`, 0 to word `+0x22` and the low byte of a
popped int to `+0x26`, and `0x00267420(slot, wait slot + 0x18)` is called (`0x00261B57`-`0x00261B83`,
`0x00261C54`-`0x00261C80`). A non-zero answer writes the word `0x0107` to `+0x14`, sets the stop flag to 1
and stores the address of the instruction less its length in the wait slot; the tail adds the length
back, so the address of the instruction itself is what the exit store `0x00261DD3` then writes there
(`0x00261B8C`-`0x00261BB9`).

An answer of 0 pushes byte `+0x26` back and makes the request (`0x00261BBE`-`0x00261BCE`,
`0x00261C8D`-`0x00261CA8`). With `+0x15` non-zero the arm pushes byte `+0x26`, clears `+0x15` and makes the
request (`0x00261BD0`-`0x00261BDC`, `0x00261CAD`-`0x00261CC0`).

`0x62` pops three values as ints and pushes the three ints back in their old order, so a stack that
held three ints is left unchanged (`0x00261D36`-`0x00261D81`); a float comes back as an int, its fraction
dropped, and each pop from an empty stack gives 0 and is still pushed.

With bit `0x4000` set in the second value popped, the manager is its upper half,
shifted arithmetically, and the index its low word; with the bit clear the manager is the slot's dword
`+0x28` and the index the whole value (`0x00261D86`-`0x00261D9A`). The arm then calls
`0x003587C0(manager, index)` and `0x002659F0(that answer, 1 << (third value & 0x1F))`, with no null test
between them (`0x00261D9C`-`0x00261DAB`).

The other eight request arms have the three paths of `REQ`: the submit at once with the mask at 0, the
pops and the wait stores with the mask non-zero and `+0x15` at 0, and the three pushes with `+0x15`
non-zero. They differ in the last two arguments of `0x00268850`. The sixth is the kind: 0 for `0x21`,
`0x24` and `0x27`, 2 for `0x22`, `0x25` and `0x28`, 4 for `0x23`, `0x26` and `0x29`.

The seventh is the mode: 1 for `0x21` to `0x23`, 2 for `0x24` to `0x26`, 3 for `0x27` to `0x29`
(`0x0025FBB8`-`0x0025FBC4`, `0x0025FF8F`-`0x0025FF9B`, `0x002602C3`-`0x002602CB`, `0x002606AE`-`0x002606BE`,
`0x00260A71`-`0x00260A81`, `0x00260DB1`, `0x002610A0`-`0x002610B0`, `0x00261205`-`0x00261215`). For modes 2 and 3
the submit is at `0x002602D0`: an answer of 1 from `0x00268850` sets the wait slot's byte `+0x14` to 4 and
the stop flag to 1; any other answer leaves both as they were (`0x002602E1`-`0x002602FB`, `0x00261610`).

The arms run from their handler to their jump to the submit: `FREQ` `0x0025F7F2`-`0x0025FBC4`, `TREQ`
`0x0025FBC9`-`0x0025FF9B`, `REQSW` `0x0025FFA0`-`0x002602FB`, `FREQSW` `0x00260300`-`0x002606BE`, `TREQSW` `0x002606C3`-`0x00260A81`,
`REQEW` `0x00260A86`-`0x00260DB9`, `FREQEW` `0x00260DBE`-`0x002610B0` and `TREQEW` `0x002610B5`-`0x00261215`; `FREQ` and `TREQ`
jump to the submit of `REQ` at `0x0025F7BF`, `REQEW` to `0x002602CB` and the other four to `0x002602D0`, the submit that
ends the range of `REQSW`.

Their wait paths call `0x00358940`, `0x003DB640` and `0x0020E620` as `REQ`'s does. `FREQEW` puts the target and the function
id back through `0x00267F90` after an answer of 0 (`0x00260FB9`, `0x00260FC4`) and pushes all three through it on its
`+0x15` path (`0x00261071`-`0x00261090`); its other pushes are inline. `TREQEW` pops the values through `0x00267E10` and
puts them back through `0x00267F90` (`0x002610CA`-`0x002610E6`, `0x00261186`-`0x002611F5`).

`RETN` (`0x2E`) and `RETTN` (`0x30`) pop a value and first compare `value + 1`, signed, with the actor's
byte `+0x11`. When it is above, nothing is recycled and no return is made: the script goes on when the
wait slot's byte `+0x14` is 1, and the stop flag is set to 1 for any other kind
(`0x0026131F`-`0x0026132E`, `0x002613C5`-`0x002613D8`, `0x0026147E`-`0x0026148D`, `0x00261521`-`0x00261534`).

Otherwise they call `0x003DB420(actor, value + 1, 0)` and `0x003DB6E0(actor)` and go on as `RET` and `RETT`
do, with the answer of `0x003DB420` in the place of the answer of `0x003DB2A0`
(`0x00261334`-`0x00261344`, `0x00261493`-`0x002614A3`); on the path for bit `0x40`, `rsi` still holds the old
wait slot in both, as in `RETT` (`0x00261371`-`0x00261376`, `0x002614B5`-`0x002614BA`).

`REQWAIT` (`0x32`) pops the function id and then the actor. With bit `0x8000` in either it does
nothing. Otherwise it calls `0x003DBF60(0x00358940(slot, actor), function id, -1)`; an answer of `0xFF`
also does nothing, and any other answer stores `0x0020E620` of the record in the wait slot's `+0x18`,
the function id's low word in `+0x20`, 0 in `+0x27` and 3 in `+0x14`, and sets the stop flag to 1
(`0x00261539`-`0x002615A1`).

`REQCHG` (`0x34`) pops three values and calls `0x0025AF60(slot, third, second, first)`. When the third is
`0x10` or `0x11` and bit `0x8` is set in byte `+0x0B` of the record `0x00358940(slot, second)` gives, it
calls `0x00268EA0` with the running actor, not that record; the record is not tested for null
(`0x002615BA`-`0x0026160B`). `PUSHACT` (`0x4D`) stores its operand in `0x02099AB8` before the range test, and
for an operand at or past the count it stores `0x8000` there and pushes `0x8000`
(`0x00261812`-`0x0026184B`).

### Columns of script-interpreter-opcodes.tsv

| Column | Holds |
|---|---|
| `field16` | the dword at `+0x10` of the opcode's 24-byte record at `0x01EFEA60 + opcode × 24`, as read from the image: 0 on 80 records, 1 on 9 and 2 on 11; no engine code reads it |
| `field20` | the dword at `+0x14` of the same record: 0 on 80 records, 1 on 15 and 2 on 5; no engine code reads it |

### A native call, and how the script waits

`CALL operand` stores the actor's own index in `X`, then runs `0x002621D0(slot, actor, stack,
operand, waitSlot)`. The verb id splits into family `operand >> 12` and command `operand & 0xFFF`;
the three callbacks come from the family tables ([native commands](native-commands.md)), and the
target actor is the issuer unless `X` names another, resolved by ordinal through `0x00358940`.

With phase `+0x15` at 0 the result word `+0xC` is zeroed and the begin callback runs with the scratch
at `+0x18`; then the poll callback runs. A poll that returns an odd value sets the phase to 1 and
returns 1, busy: the handler stores the address of the `CALL` less its length in the wait slot
(`0x002619E4`-`0x002619E7`), the tail adds the length back, the exit store `0x00261DD3` writes the address
of the `CALL` itself there, and the handler leaves
the loop. The next frame re-fetches the same `CALL`; phase 1 skips begin and polls again.

When the poll completes and the family has a result callback, it runs and the phase decides what
is pushed: 0 or 1 pushes an implicit int 0, 2 the int in `+0xC`, and 3 or more the float in `+0xC`
(`0x0026227A`-`0x00262355`); without a result callback an int 0 is pushed whatever the phase; a stack
already at depth 63 gets nothing. The phase resets to 0 and the PC advances past the call.
`CALLPOPA` then pops that value into `A`. `CALLACT` pops the target into `X` only while the phase
is 0, so a resumed call keeps the target it started with.

`SYSHALT`, a busy call and a request arm that arms its wait (`0x21` to `0x29`) are among the handlers that rewind; 21
sites in the body subtract the instruction length to repeat an instruction, against 4 that advance.

## Layouts

```python
wait slot (0x28 each, [actor+0xA8] + (s8)[actor+0x11] * 0x28)
  +0x00 u64 PC   +0x08 X   +0x0C Y / result   +0x10 A   +0x14 kind   +0x15 phase   +0x18.. scratch
value stack 0x02099AC0: +0 depth, +4 tag[64] (1 int, 2 float), +0x44 kind[64], +0x84 u32[64], +0x184 value[64]
actor record: +0x58 bytecode base, +0x48 function table, +0x50 jump table, +0x64 I0..I3, +0x74 F0..F3, +0x14 flags
manager slot: +0 image, +0x28 index, +0x68 int pool, +0x70 float pool, +0x78 variable descriptors, +0x80 tags, +0x201 byte loaded into edx
dispatch 0x00261DF8: u32 rva[100], target = 0x120000 + rva
descriptor 0x01EFEA60: 100 x { s16 length, s16 field2, u32 field4, char* name of opcode N+1, u32, u32 }
instruction: u8 opcode, then u16 operand for 0x48..0x63
```

## Shipped data

| Fact | Value |
|---|---|
| opcodes / distinct handlers | 100 / 92 |
| instruction lengths | 0 ×3, 1 ×69, 3 ×28 |
| opcodes without a handler | 6, not used by any shipped script |
| instructions per call before the budget raises the stop flag | 65,536 |
| value stack | 64 entries, pushes refused at 63 |
| rewind sites / advance sites | 21 / 4 |
| interpreter body | 14,646 bytes, one call site |

## Operations

Per frame: the field runtime pass runs the driver for every actor; the driver runs the
interpreter for every actor whose wait slot is kind 1 or 2. Per call: gate, then budget, fetch,
dispatch, advance or rewind, until a loop head finds the stop flag raised and the stack empty; a stop
instruction, a wait, a busy native call, a return and the spent budget can raise the flag.

## State

The shared stack (depth reset on every entry, contents left), the actor's eight registers, and
the wait slot's PC, registers, kind, phase and scratch, which are what a suspended script resumes
from.

## Modding notes

- Replacing a jump-table entry changes one opcode for every script in the game, but the
  instruction length comes from the descriptor table, so a new instruction must keep its slot's
  length; the four free length-1 slots are `0x19`, `0x1A`, `0x31` and `0x47`, and `0x01` and
  `0x02` have length 0 and would never advance.
- The table entries are offsets from `0x120000`, not addresses.
- A verb that must wait returns an odd poll value; its begin runs once, its poll every frame
  until it completes.
- `OPMOD` by zero and `INT_MIN MOD -1` fault; `OPDIV` yields 0 on a zero divisor, but its int path runs `idiv`
  with no `INT_MIN / -1` test (`0x0025F0D1`-`0x0025F0DA`), so `INT_MIN / -1` faults as well.

## Related

- [Script requests](script-requests.md): the wait kinds 3 to 7 and the request opcodes.
- [Native commands](native-commands.md): the family tables and the begin, poll and result callbacks.
- [Verb dispatch](verb-dispatch.md): the argument convention a verb sees on the stack.
- [Script variables](script-variables.md): the storage classes behind `PUSHV` and `POPV`.
- [`script-interpreter-registers-by-script.tsv`](script-interpreter-registers-by-script.tsv): one row per script:
  its functions, how many of them use the eight persistent registers `I0` to `F3`, how many register opcodes it
  holds, the registers some function reads before writing them, and the count of each register opcode (1,114 rows).

### Columns of script-interpreter-registers-by-script.tsv

| Column | Holds |
|---|---|
| `functions_using_registers` | how many of the script's functions hold at least one of the sixteen register opcodes `0x36` to `0x45`: 0 to 92; 0 on 326 scripts |
| `read_before_write_in_some_function` | the registers that at least one function reads (`PUSH`) before it writes them (`POP`), separated by semicolons: `I1` on 93 scripts, `F0;F1;F2;F3` on 2, `F0` on 1, empty on the other 1,018 |
| `per_opcode` | the count of each register opcode in the script, as `MNEMONIC=count` separated by spaces (for example `POPI0=15 PUSHI0=23`); the counts add up to `register_opcodes` on every row, and the cell is empty on the 326 scripts that hold no register opcode |

---

[Script variables →](script-variables.md)
