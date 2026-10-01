---
system: How a gamepad becomes a controller object - DirectInput enumeration, the three controller kinds the engine names, hot-plug, and the Steam Input action names
category: 15-Input
status: DOCUMENTED
owner_layer: PrimaryOwner:Input
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the DirectInput initialiser 00797910, the two enumeration callbacks 00796230 and 00798A40, the per-device
    body 00797690, the controller base constructor 00792940 and its three derived constructors 00792CB0, 00792AB0 and
    00792B70 disassembled from the authority image and read whole, 2026-09-19; the three log strings, the action-set
    name and the eighteen action names read out of the image
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-gamepad-falsification-pass-1
  note: written by FABLE while placing one of FRONTIER's uncited bodies (00797690). Static. Read in part only and
    described by role - the per-frame device update, the window procedure's device-change arm, and the XInput test;
    not read - the mouse and keyboard arms, the three kinds' poll methods; pending first review
---

# How a gamepad becomes a controller object

The game does not ask "is there a pad?" It asks DirectInput to **list every attached device**, and for each one a small
callback decides what to build. A pad ends up as **one of three kinds of controller object**, and the engine's own log
lines name them: a **Steam Controller**, an **XInput Device**, or a **DirectInput Device**. The same walk is repeated
whenever Windows reports that a device has arrived, which is all hot-plugging is.

## 1. Start-up - `00797910` (147 B)

1. The Steam controller interface is fetched from the Steam API context and kept in `02EA9508`; if present its first
   method (initialise) is called. *A build without Steam leaves this null, and every Steam step below is skipped.*
2. `DirectInput8Create` (version `0x0800`) fills `02EA5370`. Failure returns error 9.
3. `EnumDevices` is called for **every device class**, **attached devices only**, with the callback `00796230`.

## 2. The callbacks - `00796230` (75 B) and `00798A40` (55 B)

Both switch on the low byte of the device-type word (`+0x24` of the enumerated descriptor) and always answer "continue":

| device type | start-up callback | hot-plug callback |
|---|---|---|
| `0x12` mouse | the mouse arm | the mouse arm |
| `0x13` keyboard | the keyboard arm | **ignored** |
| `0x14` joystick, `0x15` gamepad, `0x18` first-person | `00797690` | `00797690` |
| anything else, including `0x19` | ignored | ignored |

So a keyboard is bound once, at start-up; mice and pads can arrive later.

## 3. One enumerated pad - `00797690` (638 B)

1. **Is it an XInput device?** The product GUID goes to the standard test - a WMI walk of `Win32_PNPEntity` under
   `\\.\root\cimv2` looking for `IG_` in a `DeviceID` with matching `VID_` / `PID_`. A sticky byte (`02EA5379`) records
   that at least one XInput device has been seen.
2. **Already have it?** The registered-device list (`01F401E8`) is searched for a device whose kind method answers 2
   and whose stored instance GUID equals this one's; if found, nothing is built. *This is what makes the hot-plug
   re-enumeration safe for the kinds that store the descriptor. ~~Which kinds answer 2 was not read; the Steam object
   stores no descriptor, so this test cannot recognise it, and whether a later walk builds a second one was not
   established.~~ **Answered 2026-09-29 (OPUS, falsification pass 1, G4): every controller class answers 2 (the
   shared leaf `00290180`). The Steam object's zeroed descriptor never matches, so while Steam reports a controller
   each walk builds a new Steam object for every pad with no stored twin.***
3. **Steam first.** If the Steam interface exists it is pumped once and asked for its connected controllers; if there
   is at least one, the log says `Creating new Steam Controller` and a `0x458`-byte object is built (section 5).
4. **XInput.** If the device passed the test of step 1 and fewer than **four** XInput devices exist, the log says
   `Creating new XInput Device: %d`, a `0x470`-byte object is built with the next user index, and the count
   (`02EA9500`) goes up. A fifth XInput pad is counted but not built.
   *(CORRECTED 2026-09-29, OPUS, CON-188: this step does not depend on step 3. An XInput pad seen while Steam reports
   a controller gets both objects.)*
5. **Otherwise DirectInput** - only if step 3 built nothing: `Creating new DirectInput Device`, then `CreateDevice` on
   the instance GUID, `SetDataFormat`, `SetCooperativeLevel` with flags 6 (**non-exclusive, foreground** - the pad goes
   quiet when the window loses focus), an `EnumObjects` pass with its own callback, `Acquire`, and a `0x458`-byte
   object wrapping the device. ~~Any failing step abandons the pad silently; a cooperative-level answer of
   "not implemented" does too.~~ **A failed `CreateDevice`, `SetDataFormat` or `EnumObjects` abandons the pad
   silently. `SetCooperativeLevel` abandons it only on "not implemented" (`0x80004001`); any other failure continues.
   `Acquire` is not checked. No abandon path releases the created device (CORRECTED 2026-09-29, OPUS, CON-189).**

**The order matters:** an XInput pad is never opened through DirectInput, and when Steam reports a controller the
DirectInput path is skipped for every device in that walk.

## 4. What all three share - `00792940` (357 B)

The base constructor links the object into the registered-device list `01F401E8` (an intrusive node at `+8`), keeps the
DirectInput device pointer at `+0x28`, zeroes two 17-byte button arrays (`+0x30` now, `+0x41` before), the stick and
trigger fields up to `+0xA8`, four `0x48`-byte sub-objects at `+0xB0` and the state words at `+0x414`..`+0x450`, and
clears a **`0x244`-byte copy of the enumerated descriptor at `+0x1D0`** - which puts the instance GUID at `+0x1D4`,
the field step 2 above compares.

| kind | constructor | size | adds |
|---|---|---|---|
| DirectInput | `00792AB0` (181 B) | `0x458` | the descriptor copy; the device pointer |
| XInput | `00792CB0` (223 B) | `0x470` | the descriptor copy; **the user index at `+0x458`**; two zeroed qwords after it |
| Steam | `00792B70` (308 B) | `0x458` | see section 5 |

## 5. The Steam controller and its action names - `00792B70`

If Steam reports a controller, its handle is kept (`02EA95A0`), the action set **`Global`** is looked up and activated
for it, and eighteen action handles are fetched by name and cached:

- sixteen **digital** actions (handles at `02EA9510`): `Up`, `Down`, `Left`, `Right`, `Circle`, `Cross`, `Square`,
  `Triangle`, `L1`, `L2`, `L3`, `R1`, `R2`, `R3`, `Start`, `Select`;
- two **analog** actions (handles at `02EA9590`): `LeftAnalog`, `RightAnalog`.

These are the names a Steam Input configuration for the game must use: **PlayStation button names**, one flat set.

## 6. Hot-plug

The window procedure raises a byte (`02EA5363`) when a device-change message arrives with the "device arrived" code
(`0x8000`). The per-frame device update sees it, clears it, and repeats the `EnumDevices` walk with the second callback
before polling every registered device. *Nothing in this walk removes an object: a pad that is unplugged stays in the
list, and what its poll does then was not read.*

## 7. What a reimplementation must keep

- ~~Precedence **Steam → XInput → DirectInput**~~ **XInput or DirectInput, exclusively; Steam is additive and suppresses
  only DirectInput** (CON-188), with at most four XInput pads.
- De-duplication by DirectInput instance GUID, so re-enumeration is idempotent.
- DirectInput pads are foreground-only and non-exclusive.
- The keyboard is enumerated once; pads and mice on every device arrival.

**Not read:** the mouse and keyboard arms; each kind's poll; the `EnumObjects` callback; what happens on removal.

## Evidence

Every body below was read whole.

| body | interior anchors |
|---|---|
| `00797910` DirectInput start-up (147 B) | `0079791D`, `00797927`, `00797936`, `0079795D`, `00797976`, `0079798D` |
| `00797690` one enumerated pad (638 B) | `007976CD`, `007976E3`, `00797711`, `0079773A`, `00797747`, `0079776C`, `0079777E`, `00797791`, `007977AD`, `007977B9`, `007977C8`, `007977E7`, `0079780D`, `0079781B`, `0079783A`, `00797855`, `0079786F`, `0079788B`, `0079788E`, `007978AA`, `007978B9`, `007978DB` |
| `00792940` controller base constructor (357 B) | `0079295A`, `00792976`, `00792988`, `00792992`, `007929CD`, `00792A31`, `00792A96` |
| `00792AB0` DirectInput controller (181 B) | `00792AC3`, `00792AC8`, `00792AD7`, `00792B59` |
| `00792CB0` XInput controller (223 B) | `00792CCA`, `00792CD6`, `00792CE6`, `00792CF4`, `00792D77` |
| `00792B70` Steam controller (308 B) | `00792BAC`, `00792BCB`, `00792BDB`, `00792BF3`, `00792C0A`, `00792C32`, `00792C35`, `00792C62`, `00792C66` |

Strings: `01CB3770` `Creating new Steam Controller`, `01CB3790` `Creating new XInput Device: %d`, `01CB37B0`
`Creating new DirectInput Device`; `01CB38FC` `Global`; the name tables at `01F40210` (16 pointers) and `01F40290` (2).

## Cross-subsystem neighbours

~~None: every body named on this page is owned by the Input layer, and the call graph shows no edge from any of them into another layer.~~
The Steam and DirectInput calls are through interface pointers and imports.

*Corrected 2026-09-29 (FABLE, pass 22): the struck sentence became false when the falsification pass (G4) named the
shared kind leaf `00290180`, which has a caller in the script layer; the entry below names it. Consumer check:
`_index/candidates/pass22-fable-0929/consumer-check-0929-p22-crossings.md`.*

**Script_VM_Native_Bridge - MECHANICAL (1 edge; FABLE 2026-09-29).** `00290180` (`mov eax, 2; ret`), the vtable `+8`
kind leaf every controller class shares, is also called by `003423E0`, the handler of the script verb `is_ntsc`
(`0x4EB`), which pushes `00290180() == 2` and therefore always pushes 1 (`003423E9`-`003423F6`). One six-byte body is
reached under two unrelated meanings, "controller kind 2" here and "NTSC" there; the verb learns nothing about
controllers and nothing on this page depends on it. Verb row in
[the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv). Read from the shipping bytes.

## SWE2-EC7-115 update (2026-09-21) - `00797AD0` measured

`00797AD0` (1038 B) is the
DirectInput device match
`00797690` runs: IAT
`008C3150` initializes COM
(`setns` remembers whether
this call did it),
`008C3148` creates the
`01CB36B0`/`01CB36C0` GUID
pair object, three
`008C27C0` string allocs
build the device-path
BSTRs, `vtable[+0x18]`
binds, `008C3140` sets the
cooperative level, and
`vtable[+0x90]` then
`vtable[+0x20]` enumerate
into a 20-pointer stack
buffer (`0x2710` size); per
device the `word[+0x78]==8`
gate runs `008C29E8`
property reads for `IG_`,
`VID_` and `PID_`
(`01CB3728`/`+8`/`+28`),
`007A37B0` parses the hex
values, and
`(vid << 16) | pid` is
compared against
`dword[r15]` - a match sets
the found flag. Every COM
object releases through
`vtable[+0x10]`, the BSTRs
free via `008C27C8`, and
`008C3160` uninitializes
COM only when this call
initialized it.
Interior anchor `00797DB3`
(the VID:PID compare).

## SWE2-EC7-116 update (2026-09-21) - `007A37B0` measured

`007A37B0` (83 B) is the
property-value parse
`00797AD0` runs on the
`VID_`/`PID_` strings:
`0018A320(rcx)` returns the
locale context, its `+0`
cell is ORed with 1, and
IAT `008C2E68(ctx, rdi,
r8 = -1, rbx)` produces the
number the caller reads
back through the out
pointer - the string-to-
value half of the VID:PID
match.
Interior anchor `007A37F5`
(the `008C2E68` call).

## Falsification pass 1 — 2026-09-29 (OPUS): the precedence and the failure rule refuted (CON-188, CON-189); section 3.2's open residue answered

**Attack.** Sections 1 to 6 were turned into checks at their instructions. Script:
`Tools/analysis-kit/gfz-scripts/falsify_gamepad_objects.py`, output `falsify_gamepad_objects.out`, image `73461d08…`,
0 BROKEN after the corrections, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| G0 | sizes | **survives**: all eight |
| G1 | section 1 | **survives**. An `EnumDevices` failure also returns 9 (`00797998`) |
| G2 | section 2 | **survives**: `(type - 0x14) & 0xFA == 0` and type ≠ `0x19` admits exactly `0x14`, `0x15`, `0x18` |
| G3 | section 3.1 | **survives**. The XInput test runs **twice** per device, at `007976CD` for the sticky byte and again at `007977B9` before the build |
| G4 | section 3.2 and its open residue | **survives; the residue is answered.** The walk compares the n-th kind-2 entry, for n < 18, on `+0x1D4` / `+0x1DC`. **Every controller class answers 2.** The vtable `+8` of the base, DirectInput, XInput and Steam classes is the one shared leaf `00290180`, `mov eax, 2; ret`. The Steam object's descriptor cell stays zeroed, so it never matches |
| G5 | sections 3.3, 3.4 and 7: the precedence | **REFUTED (CON-188).** The XInput branch runs whatever the Steam step did. `bl` is tested only at `00797826`, after that branch. So Steam does not pre-empt XInput: an XInput pad seen while Steam reports a controller gets **both** a Steam object and an XInput object. Steam suppresses only the DirectInput path |
| G6 | section 3.5: "any failing step abandons the pad" | **REFUTED (CON-189).** `SetCooperativeLevel` (flags 6) abandons **only** on `E_NOTIMPL` (`0x80004001`); any other failure continues to `EnumObjects`. `Acquire` is not checked. No abandon path releases the device `CreateDevice` returned |
| G7 | section 4: the base | **survives** |
| G8 | section 4's table | **survives, with an addition.** The XInput constructor also calls `00862C70`. That routine loads `.\xinput1_3.dll` with `LoadLibraryW` (a path relative to the current directory) and resolves **ordinal 100** into `02EBA3F0`, once per XInput object built |
| G9 | section 5 | **survives**. The Steam handles are image globals (`02EA95A0`, `02EA9510`, `02EA9590`), rewritten by every Steam object that is built |
| G10 | section 6 | **survives**. A failed re-enumeration returns 9 and skips that frame's poll (`00799A19`) |

**What G4 and G5 mean together, in player terms.**
- While Steam reports a controller, every enumeration walk (start-up and every device arrival) builds a **new Steam
  object** for each pad the walk meets that has no stored twin. An XInput pad stores its GUID, so its second walk
  builds nothing.
- A pad that is neither XInput nor recognised gets no DirectInput object while Steam is up, so nothing stores its GUID.
  Each later walk therefore builds another Steam object for it.
- All those Steam objects share one set of global handles.
- Whether the duplicates cause doubled input depends on each kind's poll, which is still not read.
