[Home](../../README.md) / [Saving, loading and settings](README.md) / Save transaction

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Save transaction: its steps, the storage queue and its worker, the slot scan, the space requirement, the save-data check and the file layer | system | Saving, loading and settings | Saving and loading | How a manual save is written: the six-step transaction that zeroes the header, queues three deletes that remove no file, writes the image and stamps the header, the storage queue and the worker that runs its commands, the slot scan that reads every slot's header, the space a save needs, the title screen's save-data check, and the file layer's read and write rules. | 0x005819F0, 0x00581DA0, 0x00581B70, 0x00582040, 0x003BB920, 0x003BB9B0, 0x003BB2F0, 0x00866A00, 0x00862590, 0x00866AD0, 0x00582860, 0x00862130, 0x003BA990, 0x008621E0, 0x003BA680, 0x003BB790, 0x02B407C0 |

## What the player sees

A save writes the game's live save image to the slot's file, and a save interrupted part-way through is left on disk
with its first eight bytes zeroed. The title screen asks whether any save file exists before it offers loading.

## How it works

### The save transaction

`0x005819F0` opens the transaction on message 1: it copies the request's slot, counter and flags into
the record (`+0xCD` slot, `+0xD0` counter, `+0xC8` = request `+0x18` bit `0x1`, the short variant),
keeps the image's header dword `+0x50` at `+0xD4`, sets the gauge total to `0x1DA`, or `0x17C` for
the short variant (`0x005817D0`, target minus `0x19`), registers the completion callback `0x00581B70`
on the storage queue, and runs step 1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581DA0` |

</details>

In more detail, message 1 sets `0x02CA99B0` to 1¹, keeps the request's first two qwords at `+0xC0`
and `+0xE0`², and stores 0 in the index `+0xCE`, the state `+0xCC` and the progress total
`+0xDC`³. It calls `0x00244960([+0xC0], record)`, `0x00247870(record, 0)`,
`0x00247930(record, 0x64)` and `0x00254CB0(1)`⁴. The callback goes in as a kind-1 packet
`{1, 0x00581B70, low 32 bits of the record}`, queued only when the queue `0x02CA99C0` exists⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581A57` |
| ² | `0x00581A7F`, `0x00581A8A` |
| ³ | `0x00581A9B`, `0x00581ABD`, `0x00581B1B` |
| ⁴ | `0x00581ACA`-`0x00581AEB` |
| ⁵ | `0x00581B25`-`0x00581B47` |

</details>

`0x00247870(widget, on)` leaves a null widget alone¹. For a widget with bit `0x20` of its dword `+0x40` it
sets bit `0x2` there before `0x002473F0(widget, on)` when on is not 0, and clears it after `0x002473F0(widget, on)` when
on is 0². For any other widget it only copies on's low bit into bit `0x2` of `+0x40`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00247873` |
| ² | `0x00247884`-`0x002478A2` |
| ³ | `0x002478B1`-`0x002478BB` |

</details>

Message `0xF` stores 0 in `0x02CA99B0`, calls `0x00254CB0(0)` and then `0x00247510([+0xC0], 0xF, 0xA)`¹; message `0x12` calls `0x00247510([+0xC0], 0x12, 0xA)`². Both return 0; every
other message goes to `0x005C5230`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581A24`-`0x00581A47` |
| ² | `0x00581A1D` |
| ³ | `0x00581A18` |

</details>

`0x00581DA0(record, state)` does nothing when `state` equals the current state `+0xCC`¹, and for a
state outside 1-8 it only stores the state². Otherwise, after the step and its weight
(the table below), it hands the new total to the gauge's `0x00581860`³ and stores the state
in `+0xCC`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581DD2` |
| ² | `0x00581DEA`, `0x00581FF4` |
| ³ | `0x00581FE3`-`0x00581FEF` |
| ⁴ | `0x00581FF4` |

</details>

Step 7 queues its kind-8 packet only when the queue `0x02CA99C0` exists¹, named through `0x00583700`² with one descriptor³; its weight counts either way. States 5 and 6 run state 4's arm,
the companion name of kind `+0xCE + 2`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581F47` |
| ² | `0x00581F3B` |
| ³ | `0x00581F77` |
| ⁴ | `0x00581E9E`-`0x00581EAB` |

</details>

`0x00583700(slot, flag)` answers 0 with no controller at `0x02CA99B8`¹. Otherwise it formats the
prefix `0x003935C0(buffer, 0x20)` and the slot with `0x0017D2E0(name, "%s%03d", prefix, slot)`². With a flag
other than 0 it formats that name again into the controller's `+0x128` with `0x0017D2E0(+0x128, "/%s", name)`³, and with a flag of 0 it copies the name there. It answers the address of `+0x128`⁴ and checks its stack cookie with `0x00808C40(cookie)`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0058371F`-`0x00583730` |
| ² | `0x009153E4` |
| ³ | `0x00D23EE4` |
| ⁴ | `0x00583735`-`0x005837BE` |
| ⁵ | `0x005837D0` |

</details>

`0x00584610(buffer, size, kind, slot)` builds the names of `0x005837F0(kind, slot)` (The files) into its buffer¹. In both, kind 1 formats only when the prefix past its first two
characters is shorter than `0x40`², and for a kind above 4 the stack
buffer is copied out without having been written³. Both check their
stack cookie with `0x00808C40(cookie)`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583826`-`0x005838BE`, `0x00584640`-`0x005846DE` |
| ² | `0x00583871`-`0x0058388D`, `0x00584695`-`0x005846AD` |
| ³ | `0x0058384B`-`0x0058384E`, `0x0058466F`-`0x00584672` |
| ⁴ | `0x0058390A`, `0x0058470A` |

</details>

`0x005837F0`'s null answer and its copy to the controller's `+0x128` are at `0x0058380F`-`0x00583821` and
`0x005838C4`-`0x005838FD`. `0x00584610` writes nothing when its size is below `0x40`, a signed compare¹; otherwise it copies the name into the buffer².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00584610`-`0x00584613` |
| ² | `0x005846E4`-`0x005846FD` |

</details>

`0x00581DA0(record, state)` performs one step and adds its weight to the progress total `+0xDC`:

| State | What it queues | File | Weight |
|---|---|---|---|
| 1 | zeroes the image's first 8 bytes in memory and writes them (kind 7) | the slot file | `0x10`, short `0x50` |
| 2 | delete (kind `0xB`) | `icon.sys` | `0x10`, short `0x14` |
| 3 | delete | the slot file | `0x10` |
| 4 | delete | `static.ico` | `0x10` |
| 7 | builds the submission descriptor (`0x005832B0`), runs the header finaliser `0x00583D60` and keeps its return, the plain CRC (`0x00583F97`), at `+0xD8`, then writes the whole image (kind 8, `0x56690` bytes) | the slot file | `0x168`, short `0xE6` |
| 8 | puts `{checksum, 1}` in the image's first 8 bytes and writes them (kind 7) | the slot file | `0x32` |

The callback `0x00581B70(kind, error, record)` accepts only the kind the current state waits for
(7 for states 1 and 8, `0xB` for 2-4, 8 for 7) and steps on:

- 1 to 2; 2 to 3, or to 7 in the short variant¹; 3 to 4 with the counter
  `+0xCE` cleared; 4 to 7; 7 to 8.
- States 5 and 6 share state 4's arm, and no call reaches them: the dispatcher's two callers² ask for steps 1, 2, 3, 4, 7 and 8, and for 4 + index only while the index is below 1
  (`0x00581C94`-`0x00581CA0`, after the increment at `0x00581C81`).
- On the last completion, or on any error, it posts message `0x1D` with class `0xF`, the device
  byte from the queue's `+0x39A` and the error code to the controller, and releases the record.
  The device byte is `0xFF` when no queue exists³. The message goes through
  `0x00247510([+0xC0], 0x1D, message)`⁴ and the release is `0x00244F00(record)`⁵.
- On success it first runs `0x005813E0`⁶.
- On an error it also restores the image's `+0x50` from `+0xD4` and raises bit `0x4` in the gauge's
  flags.
- A callback of another kind, or in a state outside 1-8, returns with nothing done⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581BFD`-`0x00581C06` |
| ² | `0x005819F0`, `0x00581B70` |
| ³ | `0x00581D00` |
| ⁴ | `0x00581D52` |
| ⁵ | `0x00581D5A` |
| ⁶ | `0x00581D19` |
| ⁷ | `0x00581B97`, `0x00581BB6` |

</details>

So a full save runs states 1, 2, 3, 4, 7, 8 and a short save 1, 2, 7, 8: the short variant still
queues the delete of `icon.sys`, and keeps the old slot file until step 7 overwrites it. No queued delete
removes a file (The storage queue below), so in the full variant too the old slot file stays until step 7
overwrites it. Between step 1 and step
8 the file on disk carries a zeroed header; the second dword is 1 only on a finished save. The
finished file carries the plain CRC at `+0x00`; the finaliser's complement exists only in the image
between step 7 and step 8.

### The storage queue

`0x00582730(path, buffer, size)` queues kind 7, `0x005826D0(path)` kind `0xB`, and the transaction
itself kind 8, all through `0x00582540` on the queue object `0x02CA99C0`. `0x00582040` starts the front
packet:

| Kind | Handler | What the handler sets and runs |
|---|---|---|
| 1 | copies the packet's callback into the queue (`+0xC0`, `+0xC8`) | nothing |
| 2 | `0x003BB730`; the device byte to `+0x39A` | nothing |
| 3 | `0x003BB2C0` | command 5, busy flag clear, no driver |
| 4 | `0x003BB3B0` | command 4, busy flag clear, no driver |
| 5 | `0x003BB740` | copies the name to `0x02B4055C`, sets busy, runs `0x003BAC90` |
| 6 | `0x003BB6A0(index < 200, ptr, name)` | stores the 8 bytes at `ptr` in `0x02B407C0[index]`, command 8, runs `0x003BA720` |
| 7 | `0x003BB920(name, 0, buffer, size)` | command 2, runs the worker `0x003BAEB0`; refused for a zero size |
| 8 | `0x003BB9B0(name, descriptors, count)` | command 2 with up to 5 descriptors of `0x38` bytes, runs `0x003BAEB0` |
| 9 | `0x003BB440(name, 0, buffer, size)` | the read of `size` bytes |
| `0xA` | `0x003BB4C0` | copies a `0x138`-byte record to `0x02B40FF0`, command 6, runs `0x003BA990` |
| `0xB` | `0x003BB2F0` | command 7, runs `0x003BA5F0`, whose step 1 calls `0x00862130`; the name is not passed on (below) |
| `0xC` | `0x003BB380` | the format command |

`0x00582040(queue)` returns 0 and starts nothing when the queue is null, holds no packet (`+0x398` = 0) or its
front packet has already started (`+0xDC` bit `0x1`)¹. Otherwise it sets that bit² and returns 1 for kinds 1 and 2, which finish at once, and for kind 0 and kinds above `0xC`, which
run no handler³. Kinds 3 to `0xC` return 0, the packet still running.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00582064`-`0x0058207D` |
| ² | `0x005820BD` |
| ³ | `0x005820B8` |

</details>

`0x003BB920` and `0x003BB9B0` refuse while the machine is busy (`0x02B40E10` = 1), copy the name to
`0x02B40EC8`, set command 2 at `0x02B40E1C` and start the worker `0x003BAEB0`. The delete command runs
`0x00862130`: `_wfopen_s(path, "rb")`, and when that succeeds `fclose` then `_wremove`. `0x00862130(device, name)`
never reads its first argument. It builds the path in a zeroed `0x200`-byte buffer as the save directory
`0x02EAF6E0` followed by the name, with `"%s%S"` through `0x008629C0`¹, and returns 0 on
both paths².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0086214E`-`0x0086217D` |
| ² | `0x008621BC` |

</details>

`0x003BB2F0` takes no name: it never reads the packet's name that `0x00582040` passes¹. It stores command
7, zeroes the retry count, the result and the index, sets the busy flag to 1 with step 0 in one 8-byte store² and jumps to `0x003BA5F0` with 0³; it does not test the busy flag.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005821F1` |
| ² | `0x003BB2F2`-`0x003BB310` |
| ³ | `0x003BB2FC`, `0x003BB31B` |

</details>

`0x003BA5F0` moves from step 0 to step 1¹. In step 1 it calls `0x00862130(device 0x02B40E20, 0x02B40E3E)` and
moves to step `0xC`². In step `0xC` it ends with result 0 when the status it is given is
0 or -4, and with result 9 otherwise³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BA662` |
| ² | `0x003BA63E`-`0x003BA651` |
| ³ | `0x003BA608`-`0x003BA633` |

</details>

The name `0x003BA5F0` gives is the text at `0x02B40E3E`, 22 bytes into the command-8 name `0x02B40E28`. No instruction
addresses `0x02B40E3E` except that read¹. `0x02B40E28` is written only by `0x003BB6A0`'s copy of a kind-6
name², a slot file name of nine characters, `FFXII_` and three digits³, and
by `0x003BB4C0`'s empty name⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BA645` |
| ² | `0x003BB6B9` |
| ³ | `0x0057F2F5`, `0x003935E1` |
| ⁴ | `0x003BB50E` |

</details>

The text at `0x02B40E3E` therefore stays empty, and the path names the save directory itself. `_wfopen_s` cannot
open a directory for reading, so `0x00862130` reaches neither `fclose` nor `_wremove`¹, and the three
deletes the save transaction queues remove no file.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008621A2` |

</details>

The two write starters in detail:

- Both refuse for any non-zero busy flag and then return 0¹. Otherwise they set the busy
  flag to 1 and the step `0x02B40E14` to 0 in one 8-byte store², call `0x003BAEB0(0)` and
  return 1.
- `0x003BB920` also refuses a zero size³. It copies its name up to the NUL⁴,
  stores the buffer at `0x02B40EF0`, the start offset at `0x02B40EFC` and the size at `0x02B40EF8` (descriptor 0's
  `+0x28`, `+0x34` and `+0x30`) and the count 1 with index 0⁵.
- `0x003BB920` zeroes the retry count `0x02B40EC0` and the result `0x02B40E18`⁶.
- `0x003BB9B0` never reads its first argument. It copies `min(count, 5)` descriptors of `0x38` bytes, each with its
  name at `+0x00`, to `0x02B40EC8` (`0x003BB9CC`-`0x003BBA21`; a count of 0 or less copies no descriptor), and
  zeroes the retry count, the result and the index `0x02B40FE4`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BB924`, `0x003BB9B4` |
| ² | `0x003BB996`, `0x003BBA36` |
| ³ | `0x003BB93A` |
| ⁴ | `0x003BB950`-`0x003BB95C` |
| ⁵ | `0x003BB981` |
| ⁶ | `0x003BB967`, `0x003BB96D` |
| ⁷ | `0x003BBA2F`-`0x003BBA48` |

</details>

### The worker's status poll

`0x003BB790` runs at the end of every pass of the request pump `0x0032E070` while `0x0036FD50()` (the byte
`0x02AD9E00`) is non-zero¹. With the busy flag `0x02B40E10` at 0 it stores 0 in the dwords
`0x02B40E00` and `0x02B40E04`² and returns; with a busy value other than 0 or 1 it
returns at once³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032E2B4`-`0x0032E2BD` |
| ² | `0x003BB90F`, `0x003BB915` |
| ³ | `0x003BB7A5` |

</details>

While the machine is busy (1) it reads the status of the last file call, `0x02EAF8E0`, through
`0x00862600(unused, a, b)`, which stores 0 at `a`, the status at `b` and returns 1. `0x003BB790` gives a null `a`¹, which `0x00862600` skips. Its tests for an answer of −1 (clear the busy dword, `0x003BB902`) and for
any answer but 1 (return) therefore never fire².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BB7B0` |
| ² | `0x003BB7B7`-`0x003BB7C3` |

</details>

A status from -19 to -11, from -79 to -70 or from -59 to -40 ends the command with result 4,
and -5 with result 7; both clear the busy flag and the step `0x02B40E14` in one 8-byte store¹. Any other status goes to the command's handler:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BB8EA`, `0x003BB8D2` |

</details>

| Command (`0x02B40E1C`) | Handler |
|---|---|
| 0 | `0x003BAC90` |
| 1 | `0x003BA7B0` |
| 2 | `0x003BAEB0` |
| 3, 4, 5 | no handler: the command ends with result 0 |
| 6 | `0x003BA990`, the slot scan |
| 7 | `0x003BA5F0` |
| 8 | `0x003BA720` |
| 9 | `0x003BA680`, the save-data check |

The handlers are tried in the order 1, 6, 2, 0, then 3 to 5, 7, 8 and 9, and the command is read again after
each handler¹. A handler that changes the command is therefore followed in the same pass
by a later handler for the new one. Commands 3, 4 and 5 store 0 in the step and the result `0x02B40E18` in one
8-byte store and clear the busy dword², and `0x003BB790` then returns without trying 7, 8
or 9.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BB803`-`0x003BB8B7` |
| ² | `0x003BB876`, `0x003BB87D` |

</details>

The result is kept at `0x02B40E18` (`0x003BB420` returns it) and the busy flag at `0x02B40E10`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BB430` |

</details>

The handlers keep their own words beside the command:

- Each handler is a switch on the step `0x02B40E14`; the worker's has 18 steps¹.
- A file is described by `0x38`-byte descriptors from `0x02B40EC8`: the name at `+0x00`, the buffer at `+0x28`, the size
  at `+0x30` and a start offset at `+0x34`. A positive offset is passed to `0x008625D0` before the read or write
 ².
- `0x003BB9B0` copies up to 5 descriptors; the worker walks them with an index against a count³.
- The write waits before it closes the file: `t = t + max(0.001, (f32)0x0017D270())` adds the frame time, at least
  0.001, to the time t at `0x02B4112C`⁴, until 1.0 has passed while `0x00583920`
  reports a save write, or 0.1 otherwise: it waits while `t < (0x00583920() ? 1.0 : 0.1)`⁵.
- The device check counts its retries and gives up, with the busy flag clear, after the fifth⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BAEEE`-`0x003BAF1E` |
| ² | `0x003BA85B`-`0x003BA860`, `0x003BAB92`-`0x003BAB97`, `0x003BB039`-`0x003BB040` |
| ³ | `0x003BB166`-`0x003BB177` |
| ⁴ | `0x0017D270`, `0x003BB097`-`0x003BB0BB` |
| ⁵ | `0x003BB0C7`-`0x003BB0E9` |
| ⁶ | `0x003BADA0`-`0x003BADBC` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B40548` | `i32` | 0 (zero-filled tail of `.data`) | the phase of the empty-slot requirement: at the start of state `0x10` the extra unit goes to the first empty slot when it is 0 and then to every other one (`0x003BAAB5`, `0x003BAAC0`) | `0x003BA990`, 0 in state 0 (`0x003BAA4E`) | `0x003BA990` (`0x003BAAA9`) |
| `0x02B40558` | `i32` | 0 (zero-filled tail of `.data`) | the slot of the file a command is on, the index of its status entry `0x02B407C0 + 8 x slot` | `0x003BA990`, the answer of `0x003BA320` in state `0x15` (`0x003BAB38`); `0x003BAC90`, the same (`0x003BAD09`); `0x003BB6A0`, its first argument (`0x003BB6E0`) | `0x003BA990` (`0x003BABCA`, `0x003BABE3`, `0x003BAC18`, `0x003BAC47`); `0x003BA720` (`0x003BA76B`, `0x003BA788`) |
| `0x02B40E14` | `i32` | 0 (zero-filled tail of `.data`) | the running command's step | 42 stores in the handlers, the starters and the poll: the worker `0x003BAEB0` at 11 sites (`0x003BAF36` to `0x003BB1BE`), `0x003BA7B0` at 8 (`0x003BA7DB` to `0x003BA930`), the poll `0x003BB790` at `0x003BB876`; `0x003BB440` stores 1 with the result 0 (`0x003BB49C`, an 8-byte store); the 17 8-byte busy stores at `0x02B40E10` zero it: 11 that store 0 in the busy flag, the poll's `0x003BB8D2` and `0x003BB8EA` and `0x003BA61E`, `0x003BA6BA`, `0x003BA8E2`, `0x003BA91C`, `0x003BAE22`, `0x003BAE47`, `0x003BAFC1`, `0x003BAFDF` and `0x003BB145`, and 6 that store 1 in it, `0x003BB310`, `0x003BB5CD`, `0x003BB704`, `0x003BB760`, `0x003BB996` and `0x003BBA36` | `0x003BA5F0` (`0x003BA5F4`), `0x003BA680` (`0x003BA684`), `0x003BA720` (`0x003BA724`), `0x003BA7B0` (`0x003BA7B4`), `0x003BA990` (`0x003BA9A2`), `0x003BAC90` (`0x003BAC96`), `0x003BAEB0` (`0x003BAEEE`) |
| `0x02B40E24` | `i32` | 0 (zero-filled tail of `.data`) | the open file's handle | `0x003BA7B0` (`0x003BA853`), `0x003BA990` (`0x003BAB8A`), `0x003BAEB0` (`0x003BB02E`), each the non-negative result of the open | `0x003BA7B0` (`0x003BA8A8`, the read; `0x003BA8C6`, the close); `0x003BA990` (`0x003BAB9C`, `0x003BABB5`); `0x003BAEB0` (`0x003BB08F`, `0x003BB0EF`) |
| `0x02B40E28` | `char[]` | 0 (zero-filled tail of `.data`) | the file name of command 8 | `0x003BB6A0`, the name copied up to its NUL (`0x003BB6B9`-`0x003BB6DE`); `0x003BB4C0`, an empty name (`0x003BB50E`) | as a path, through its address: `0x003BA720` to `0x003BA3E0` (`0x003BA735`); `0x003BA7B0` to `0x008620D0` (`0x003BA7F7`); `0x003BAEB0` to `0x008620D0` (`0x003BAF4F`, `0x003BAF8B`) |
| `0x02B40EC0` | `i32` | 0 (zero-filled tail of `.data`) | the device check's retry count | `0x003BAC90`, 0 (`0x003BAD5C`) and 1 more (`0x003BADA8`); 0 at 15 other sites in the handlers and starters (`0x003BA66C` to `0x003BBA2F`) | `0x003BAC90` (`0x003BADA0`), which gives up above 4 |
| `0x02B40EFC` | `i32` | 0 (zero-filled tail of `.data`) | descriptor 0's start offset (`+0x34`) | `0x003BB440` (`0x003BB470`) and `0x003BB920` (`0x003BB973`), their second argument; `0x003BB4C0`, 0 (`0x003BB527`) | `0x003BA7B0` (`0x003BA84D`); `0x003BA990` (`0x003BAB82`) |
| `0x02B40FE0` | `i32` | 0 (zero-filled tail of `.data`) | the number of descriptors | `0x003BB920`, 1 (`0x003BB981`, an 8-byte store that also zeroes the index); `0x003BB9B0`, its count (`0x003BB9D3`); `0x003BB4C0`, 0 (`0x003BB53B`) | `0x003BB9B0` (`0x003BBA1B`, its copy loop); `0x003BAEB0` (`0x003BB169`) |
| `0x02B40FE4` | `i32` | 0 (zero-filled tail of `.data`) | the descriptor the worker is on | `0x003BAEB0`, 1 more (`0x003BB170`); 0 from `0x003BB9B0` (`0x003BBA48`) and the other starters (`0x003BB2D2` to `0x003BB77A`, 9 sites); `0x003BB920`, with the count (`0x003BB981`) | `0x003BAEB0` (`0x003BAEBA`), which picks the descriptor `0x02B40EC8 + 0x38 x index` |
| `0x02B40FE8` | `void*` | 0 (zero-filled tail of `.data`) | the cache row of the file being read: `0x02B40EF0` plus the slot times the row size `0x02B40EF8` | `0x003BA990` (`0x003BAB72`) | `0x003BA990` (`0x003BABA9`), as the buffer of the read `0x00862590` |
| `0x02B41128` | `u8` | 0 (zero-filled tail of `.data`) | the save and load screen's mode as the listing command receives it: the controller's byte `+0xC1`, 0 when the screen was opened to save and 1 otherwise | `0x003BB4C0`, its second argument (`0x003BB4CE`, `0x003BB5B5`), which `0x00582040` passes from `[0x02CA99B8] + 0xC1` (`0x005821E0`, `0x005821E7`) | no reader: no RIP-relative, image-base-relative or address-forming reference reads it, the record copy that `0x003BB4C0` makes to `0x02B40FF0` ends `0x138` bytes on, and no 8-byte pointer or 4-byte RVA in the image holds its address |
| `0x02B4112C` | `f32` | 0 (zero-filled tail of `.data`) | the time the write has waited before its close | `0x003BAEB0`: 0 (`0x003BB074`, `0x003BB0F8`), and the frame time added (`0x003BB0BB`) | `0x003BAEB0` (`0x003BB0AB`, `0x003BB0E2`) |

The controller's `+0xC1` comes from the screen's creation. The request dispatcher `0x0027F5D0` keeps its request's
second dword at `+0xD4`¹ and passes it to `0x00583930`², whose creation block, made
by `0x00244F50(0x5A0, 0x00582860, block)`³, holds the dword 0 at `+0x00`, the flag as a qword 0 or 1 at
`+0x08`⁴ and the second argument, 1 from this caller⁵, the same way at `+0x10`⁶; the screen procedure `0x00582860` copies the flag to `+0xC1` on message 1⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0027F74F` |
| ² | `0x0027F979`, `0x0027F984` |
| ³ | `0x00583974` |
| ⁴ | `0x0058394E`, `0x00583955` |
| ⁵ | `0x0027F97F` |
| ⁶ | `0x00583966` |
| ⁷ | `0x005828C2`, `0x005828CB` |

</details>

A request argument of 0 is the save: the dispatcher first builds the save image with `0x005844A0`¹. `0x00583930` checks its stack cookie with `0x00808C40(cookie)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0027F8DB`, `0x0027F953` |
| ² | `0x00583981` |

</details>

### The slot scan

`0x0057F6B0` queues kind 1 with the callback `0x0057F630`, then kind `0xA` with the pattern `FFXII_*`, the
header cache and a row size of `0xA0`. `0x00393630(buffer, size)` writes the pattern with
`sprintf("%s*")` and returns an empty string when the buffer is under 64 bytes. Kind `0xA`¹ copies the pattern to `0x02B4055C`, the buffer and row size to `0x02B40EF0` and `0x02B40EF8`, and
starts command 6, `0x003BA990`, which steps on each call:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BB4C0` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | State 0 sets every status entry to `{1, 0}`, takes the free space `0x02B4054C` from `0x02B40E0C` and lists the files with `0x008621E0(device, pattern, 0, 200, 0x02B41140)`. With no file found it goes to state `0x10`, otherwise to `0x15`. |   |
| 2 | State `0x15` handles one listed file per call. `0x003BA320(name)` gives its slot; the file is opened for reading, read for `0xA0` bytes into the cache at `slot * 0xA0` and closed. | `0x008624D0`<br>`0x00862590`<br>`0x008620E0` |
| 3 | A full read stores status 2. A short read stores 4, with the room flag 1 when the requirement from `0x003BA3E0` fits the free space (which it then reduces) and 0 otherwise. |   |
| 4 | State `0x10`, after the last file: every entry still at status 1 becomes `{5, 1}` when its requirement fits the free space, which it reduces, and `{3, 0}` when it does not. The machine is then idle. |   |

The requirement for an empty slot alternates between 95 and 94 units:
`(0x02B40540 + 1) / 2 + 0x02B40544 + 1`, plus 1 for every other slot.

`0x003BA320(name)` counts the pattern's characters before the `*` (ignoring `/`), requires two decimal
digits at that position of the name, and returns `atoi` of up to three characters from there; anything
else returns -1.

`0x008621E0(device, pattern, unused, count, out)` does not read the directory; it probes names:

- With `count` = 1 it opens the save directory plus the pattern (`"%s%S"`), copies the name to
  `out + 0x20` and the file size to `out + 0x10`, and returns 1 when the file exists, else 0.
- Otherwise the prefix is the pattern without its `*`, and the function tries prefix plus `%03d` for 0
  to `count - 1`. Each file that opens adds a `0x40`-byte row to `out`: the size at `+0x10` and the name
  at `+0x20`. It returns the number of rows.
- Either way the return value is also stored as the status `0x02EAF8E0`.

`0x0057F6B0(widget, message)` queues the scan above only while the message's dword `+0x08` is 0 or 1, an unsigned
compare¹. Each packet goes out only when the queue object exists, the header cache is
`[widget + 0xD8]`, and it then sets the phase byte `+0xCC` to 2².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F6CB`-`0x0057F6D2` |
| ² | `0x0057F6D8`-`0x0057F772` |

</details>

For a larger value it queues nothing: it stores `0xA` at `+0xE0`, the device byte `+0x39A` of the queue object at
`+0xE4` (`0xFF` with no queue object) and the value at `+0xE8`, and sets the phase `+0xCC` to 4¹. It checks its stack cookie with `0x00808C40(cookie)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F774`-`0x0057F7A4` |
| ² | `0x0057F7B6` |

</details>

The callback `0x0057F630(kind, result, widget)` stores the same three fields `+0xE0`, `+0xE4` and `+0xE8` for kind
`0xA`, with the result at `+0xE8`¹. With a result of 0 it runs `0x0057F280(widget)` and sets the
phase `+0xCC` to 3 when that answers 0; a result other than 0, or an answer other than 0, sets the phase to 4². For kind 6 it runs `0x0057F280(widget)` and sets the phase to 4 when that answers
other than 0³. Other kinds do nothing⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F639`-`0x0057F661` |
| ² | `0x0057F667`-`0x0057F683`, `0x0057F695` |
| ³ | `0x0057F684`-`0x0057F695` |
| ⁴ | `0x0057F687` |

</details>

`0x0057F280(widget)` starts at the slot in byte `+0xCF` and looks for the next slot below 200 whose status record
`0x003BB3E0(slot)` holds 2 and whose row of the header cache `[widget + 0xD8]`, `0xA0` bytes a slot, has a dword `+0x04`
of 0¹. With no such slot it answers 1². Otherwise it names the file with
`0x005837F0(1, slot)`, queues kind 6 with the name, the slot byte and the dword 4 through `0x00582540(queue, packet)` when
the queue object exists, stores slot + 1 at `+0xCF` and answers 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F28D`-`0x0057F2CD` |
| ² | `0x0057F2CF`-`0x0057F2D7` |
| ³ | `0x0057F2ED`-`0x0057F34D` |

</details>

### The space requirement

The figures come from the PS2 memory card. `0x00393600(kind)` gives a file size for the kinds of the name
formatter `0x005837F0`: 964 bytes for kind 0 (`icon.sys`), `0xE240` (57,920) for kind 1 (the slot file)
and `0x8398` (33,688) for kinds 2-4 (`static.ico`). `0x003936B0` passes the sizes of kinds 0-2 to
`0x003BB630`, which stores the count, 3, at `0x02B40540` and the total in 1 KB units, each size rounded up
(1 + 57 + 33 = 91), at `0x02B40544`, and returns the total in bytes. `0x003936B0` adds `0x2400` and returns
102,400.

- The storage queue keeps that value at `+0xD0`¹.
- The popup opener `0x00583FD0` rounds it up to KB for the "at least ... KB" text of popups 1, 7 and 9
  (popup-table kinds 3 and 4), which therefore reads 100.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005823B0` |

</details>

`0x003BA3E0(name, out, n)` ignores the name. It sets `out` to `(max(0, 0x02B40540 - 2 * ((n - 1) / 2)) + 1)
/ 2`, adds `0x02B40544` and subtracts the rounded-up KB of the first `n` rows of the table at
`0x02B405D0` (stride `0x40`), and clamps the result at 0; it always returns 1. The free space comes from
the device check (command 0, `0x003BAC90`): `0x00862490` writes `0x2000000` to `0x02B40E0C`, 2 to
`0x02B40E08` and 1 to `0x02B41130`, and sets the status to 0.

### The save-data check

The title-screen script asks whether any save exists with two verbs:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `fsttl_opendatacheck` (`0x00511F20`, a jump to `0x00394600`) creates the `0x108`-byte widget `0x00393EA0` unless a check is running (`0x01EFAC10` = 2). |   |
| 2 | The widget's message 1 sets `0x01EFAC10` to 2. On its first message 2 it calls `0x0036FD80(1)`, writes the pattern `FFXII_*` with `0x00393630`, selects device 0 and starts command 9 with `0x003BB320`. | `0x003BB730` |
| 3 | `fsttl_getdatacheckstatus` returns `0x01EFAC10` through `0x00394440`: 2 while running, 1 when a save file exists, 0 when no save file does, and 3, the byte's value in the image, before the first check. | `0x00511F30` |

`0x003BB320(pattern)` copies the pattern to `0x02B4055C`, sets command 9 at `0x02B40E1C`, the busy flag and
state 1. The handler `0x003BA680` lists the files (`0x008621E0(device, 0x02B4055C, 0, 200, 0x02B41140)`) and
moves to state `0xD`; on the next poll a positive count ends the command with result 0, anything else
with result 9.

The device is the byte `0x02B40E20`¹. The count is the handler's argument, the status `0x02EAF8E0` that
the poll passes and `0x008621E0` stored. Result 0 is one 8-byte store that zeroes the step and the result², followed by clearing the busy flag³. Result 9⁴ is followed by an 8-byte
store that clears the busy flag and the step⁵. In state 0 the handler only moves to state 1 and zeroes
`0x02B40554` and the retry count `0x02B40EC0`⁶; in any other state it returns⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BA6C6` |
| ² | `0x003BA69E` |
| ³ | `0x003BA6A5` |
| ⁴ | `0x003BA6B0` |
| ⁵ | `0x003BA6BA` |
| ⁶ | `0x003BA6FD`-`0x003BA70F` |
| ⁷ | `0x003BA696` |

</details>

When the machine is idle the widget reads the result: 0 sets `0x01EFAC10` to 1; otherwise it runs
command 9 once more and then sets `0x01EFAC10` to 1 or 0 from the second result. Either way it calls
`0x0036FD70` and closes itself.

The title script `ttl_a01` waits until the status is 0 or 1 and passes it to `fsttl_opencommand` (`0x00511F90`, then
`0x00394530`). When the title asset `0x02AEE4C0` exists and no title command consumer is open¹,
`0x00394530` builds the consumer `0x003939B0`, which stores the byte at its `+0xC0`² and reads it once, on the
tick that sets up its command list after the asset's `+0xC0` bit `0x1` is set, to move that list to that row
(`0x00393A80`-`0x00393A9F`, `0x00393BC8`-`0x00393BD6`; [widgets](../Menus-And-HUD/widgets.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00394543`-`0x00394557` |
| ² | `0x00393A18` |

</details>

With a consumer already open the value is not stored¹. Nothing else reads the status:
`0x01EFAC10` is read only by `0x00394440` and by the test for 2 in `0x00394600`. The New Game list (Config in mode 1) takes
its rows from `0x01E0B720` without a condition², so New Game+ and New Game- are
offered either way ([strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003945A4`, `0x003945BB` |
| ² | `0x0023ED80`, `0x0023EE10`-`0x0023EF27` |

</details>

### The file layer

The worker reads and writes through a byte vector (`0x01F44D40` begin, `0x01F44D48` end, `0x01F44D50`
capacity):

- Open¹ loads the whole existing file into the vector, decoding the container when it
  is one; in write mode a missing file leaves the vector empty.
- Read (`0x00866A00(cursor, dest, count)`) copies byte by byte while the cursor is inside the vector
  and returns 1 only when every requested byte was copied. The wrapper `0x00862590(mode, ..., size)`
  returns `copied ? size : 0` for mode 0 and -4 otherwise, so a short read overwrites the front of
  the destination, advances the cursor by the bytes it took, and reports 0.
- Write (`0x00866AD0(cursor, src, count)`) overwrites inside the vector and appends past its end; no
  file is touched until close. Its wrapper `0x00862620(mode, src, size)` stores `ok ? size : 0` as the
  status for mode 0 and -4 otherwise.
- `0x00866AD0` returns 0 for a null cursor or source² and 1 for any other call
 ³. A byte whose cursor is at or past the end goes to the end: in place while the end is below the
  capacity `0x01F44D50`⁴, otherwise through `0x00865720(vector, end, src)`⁵. The
  cursor moves on by one byte either way⁶.
- `0x00866A00` returns 0 at once for a null cursor or destination⁷, and 1 for a count of 0
 ⁸.
- Seek (`0x008625D0(mode, offset, origin)`) calls `0x00866A80` for mode 0, which moves the cursor to
  `offset` from the start (origin 0), the cursor (1) or the end (2) only when the new position is inside
  the vector; the status is set to 0 either way.
- Close⁹ writes the vector as a new container to a temporary file and copies it over the
  slot file (see the [save file format page](save-file-format.md)). Every written file is a replaced copy, never written in place;
  step 8's 8-byte write loads the file step 7 wrote, patches its first 8 bytes and rewrites it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008666B0` |
| ² | `0x00866AE0`-`0x00866AEC` |
| ³ | `0x00866B5E` |
| ⁴ | `0x00866B22`-`0x00866B40` |
| ⁵ | `0x00866B4E` |
| ⁶ | `0x00866B53` |
| ⁷ | `0x00866A08`-`0x00866A10` |
| ⁸ | `0x00866A61` |
| ⁹ | `0x00866200` |

</details>

The stream calls keep one open file. Each acts only for handle 0 (`test ecx, ecx` at the head of each) and works on
the object at `0x02EAF8E8`. The opener `0x008624D0` first closes a file still open, writing it out through `0x00866200`¹, and then keeps the new one:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00862508` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAF8E8` | `void*` | 0 (zero-filled tail of `.data`) | the open file's byte-vector object from `0x008666B0` | `0x008624D0`, 0 after closing the old file (`0x0086250D`) and the new object (`0x00862548`); the closer `0x008620E0`, 0 (`0x008620FB`) | `0x008624D0` (`0x008624F4`); `0x008620E0` (`0x008620E8`), which passes it to `0x00866200`; the read `0x00862590` (`0x0086259D`), the seek `0x008625D0` (`0x008625D8`) and the write `0x00862620` (`0x0086262D`) |

## Layouts

<details>
<summary>Show the memory layouts</summary>

### The storage queue object

The queue is the `0x720`-byte widget kept at `0x02CA99C0` with procedure `0x005823B0` (The storage queue above).

`StorageQueue` (`0x720` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x005823B0` |
| `+0x0C0` | `void*` | callback | the completion callback a kind-1 packet installs (`0x005820A5`); the dequeue `0x00582240` calls it with the finished packet's kind, its result and `+0xC8` (`0x00582373`-`0x0058238E`); 0 at construction (`0x005824A9`) |
| `+0x0C8` | `u32` | callbackArg | the callback's argument, copied from the kind-1 packet with the callback (`0x005820B2`) and passed to it as its third argument (`0x0058237F`) |
| `+0x0CC` | `u8` | busy | 1 while a front packet is running: the enqueue sets it when the start `0x00582040` answers 0, the packet still running (`0x005826BA`), and starts nothing new while it is set (`0x00582698`); the dequeue clears it when the queue empties (`0x00582280`); the tick (message 2) completes and starts packets while it is set (`0x00582443`-`0x0058248A`); the device check `0x0057EA40` (`0x0057EA9F`), the poll arm `0x0057EC60` (`0x0057ECC0`) and the disarm `0x0057ED40` (`0x0057ED94`) clear it with the queue; 0 at construction (`0x005824B0`) |
| `+0x0CD` | `u8` | pad0CD | read and written by no function; nothing fixes its width |
| `+0x0CE` | `u8` | pad0CE | read and written by no function; nothing fixes its width |
| `+0x0CF` | `u8` | pad0CF | read and written by no function; nothing fixes its width |
| `+0x0D0` | `u32` | spaceNeeded | the space a save needs, 102,400 bytes from `0x003936B0`, stored by the first tick (`0x0058243D`); the popup opener `0x00583990` rounds it up to KB for the popup text (`0x005839C8`) |
| `+0x0D4` | `u32` | spaceKnown | bit `0x1` set once the first tick has measured `+0xD0` (`0x00582436`), which it does only while the bit is clear (`0x0058240A`); the load lifecycle `0x00582860` waits for it (`0x00582A6A`); 0 at construction (`0x005824B7`) |
| `+0x0D8` | `u8[704]` | queue | the eight `0x58`-byte packets of the queue (The storage queue above) |
| `+0x398` | `u8` | count | the packets queued, 0-8: the enqueue refuses a ninth (`0x0058254E`-`0x0058255D`), copies the packet to entry count (`0x00582570`-`0x005825AD`) and adds 1 (`0x00582692`); the dequeue takes 1 off and moves the rest down (`0x0058224F`-`0x005822D9`); the device check, the poll arm and the disarm empty the queue by setting it to 0 or keep the started packet with 1 (`0x0057EA72`-`0x0057EA98`, `0x0057EC8F`-`0x0057ECB9`, `0x0057ED61`-`0x0057ED8D`); 0 at construction (`0x005824BD`) |
| `+0x399` | `u8` | pad399 | read and written by no function; nothing fixes its width |
| `+0x39A` | `u8` | device | the device byte a kind-2 packet stores (`0x005820FA`), `0xFF` at construction (`0x005824C4`); read by the device-check result `0x0057E950` (`0x0057E9F0`), the presence poll's result `0x0057EBB0` (`0x0057EC0F`), `0x0057F630` (`0x0057F654`), `0x0057F6B0` (`0x0057F78E`) and the save transaction's completion `0x00581B70` (`0x00581D04`) |
| `+0x39B` | `u8` | descriptorNext | the next free entry of the descriptor ring at `+0x3A0`: a kind-8 packet's descriptors are copied from it on (`0x00582608`-`0x0058264C`), the packet's `+0x48` is pointed at the first (`0x0058265F`-`0x0058267F`) and it advances by their count (`0x0058268C`); it restarts at 0 when the count would pass 16 (`0x005825D2`-`0x005825E4`); 0 at construction (the word store at `0x005824C4`) |
| `+0x39C` | `u8[4]` | pad39C | read and written by no function; nothing fixes its width |
| `+0x3A0` | `u8[896]` | descriptors | the ring of sixteen `0x38`-byte file descriptors that kind-8 packets (the save transaction) carry, copied in by the enqueue (`0x00582617`-`0x0058264C`); the handler `0x003BB9B0` reads them through the packet's `+0x48` |

</details>

## Operations

| Function | Role |
|---|---|
| `0x005819F0` | opens the save transaction; `0x00581DA0` runs a step; `0x00581B70` completes it |
| `0x00582730`, `0x005826D0` | queue a write of `size` bytes, queue a delete |
| `0x00582040` | starts the queue's front packet |
| `0x003BB920`, `0x003BB9B0`, `0x003BB2F0` | the write, image-write and delete starters |
| `0x008666B0`, `0x00866A00`, `0x00866AD0`, `0x00866200` | open, read, write, close on the byte vector |
| `0x00862590` | the read wrapper that turns the boolean into a byte count |
| `0x00862130` | delete a file if it exists |
| `0x003BB790`, `0x00862600` | the worker's per-frame status poll, the status getter |
| `0x0057F6B0`, `0x003BA990` | queue the slot scan, run it |
| `0x008621E0` | probe one file, or list `prefix000` to `prefix199` |
| `0x003BA320` | slot number from a file name |
| `0x003936B0`, `0x00393600`, `0x003BB630`, `0x003BA3E0` | the space requirement |
| `0x00393630` | the `FFXII_*` pattern |
| `0x00394600`, `0x00393EA0`, `0x003BB320`, `0x003BA680` | the save-data check |
| `0x008625D0`, `0x00862620` | the seek and write wrappers |

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02CA99C0` | `void*` | the storage queue | the queue owner |
| `0x02CA99B0` | `i32` | a save transaction is open | `0x005819F0` |
| `0x02B40E10` | `i32` | the storage machine is busy | `0x003BB920`, `0x003BB9B0`, `0x003BB2F0` |
| `0x02B40E1C` | `i32` | the worker command | the three starters |
| `0x01F44D40` / `0x01F44D48` / `0x01F44D50` | `void*` | the file vector's begin, end and capacity | `0x008666B0`, `0x00866AD0`, `0x00866200` |
| `0x02B40E18` | `i32` | the last command's result | the command handlers |
| `0x02EAF8E0` | `i32` | the status of the last file call | `0x008621E0`, `0x00862590`, `0x00862620`, `0x008625D0`, `0x00862490` |
| `0x02B4054C` | `i32` | the free space the slot scan draws on | `0x003BA990`, `0x003BA720` |
| `0x01EFAC10` | `u8` | the save-data check: 3 in the image, before the first check; 2 running, 1 a save exists, 0 no save file | `0x00393EA0` |

</details>

## Modding notes

- A tool that writes a slot file must also write the zeroed-header then stamped-header sequence
  only if it wants the game's own semantics; the game never reads the companion files `icon.sys`
  and `static.ico`, it only queues deletes for them, which reach no file (The storage queue).
- A read that falls short reports 0 and leaves the destination partly overwritten; a reimplementation
  must copy before it compares, in that order.
- The game finds saves by probing `FFXII_000` to `FFXII_199` in the save directory, not by listing
  it; a file under any other name is ignored.

## Related

- [Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs](saving-and-loading.md)
- [Save and load screen: the screen's states and popups, the slot list and its status pane, what follows a save or a load, and the screen's widgets](saving-and-loading-screen.md)
- [Area-change autosave: when it runs, which area changes skip it, the shipped list of those area changes, and what a load runs](saving-and-loading-autosave.md)
- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md)
- [`storage-byte-stream-vector-01f44d40-accesses.tsv`](storage-byte-stream-vector-01f44d40-accesses.tsv): every
  access to the file worker's byte vector `0x01F44D40` (its begin, end and capacity pointers) (23 rows).
