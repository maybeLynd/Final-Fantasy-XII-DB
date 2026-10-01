# ASTRA — S-44 rebind discriminator falsification, 2026-09-21 UTC

**Result: do not run the proposed rebind as a closure test for the 243 unexplained
settings-table dwords.** Its name-absence premise is false, one compared table
has the wrong extent, and its expected observation does not distinguish the
competing explanations. The remaining S-44 meaning question stays open.

Player version: the game already contains names for these input numbers. Changing
a keyboard control would show that the active controls work, but would not explain
the separate unused tables. This review also caught an old record-reading error
whose two mistakes cancelled, making its examples appear correct.

## ASTRA question, hypotheses and method

Request: `FABLE-REQ-ASTRA-S44-ONE-REBIND-ANCHORS-THE-ID-SPACE`. Major systems:
S-44 settings configuration and Input. Consumers: FABLE semantic owner; OPUS
S-44 L2 verdict and CON-125 adjudication. Canonical incorporation is pending their
acceptance; this is not a self-awarded independent audit.

- H1: the three first-run value tables contain legacy input-binding defaults in
  the same domain as the live keymap, with unknown slot roles.
- H2: the tables share integers with the named input domain, but their intended
  interpretation or slot roles are different; live rebinding affects an
  independent active keymap.

**Method A suffices to reject the proposed discriminator.** Verify the shipping
bytes, table boundaries, named registry records, and a retained live input control.
No fresh live observation or isolated execution is required. Under either H1 or
H2, rebinding an active control may change `keymap.ini` and its live binding slot
identically while the unused config tables stay unchanged. That outcome does not
select H1. A finite no-change observation does not select H2 either.

Even assuming a common domain, one fixed point cannot determine an arbitrary
permutation or name 81 slot roles. It requires an independently established mapping
rule. Known input-code names and unexplained table-slot semantics are different
questions.

## ASTRA exact source identity and raw evidence

- EXE SHA256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
- PE32+ image base: `0x120000`. Only file-backed section bytes are read.
- Decoder: Capstone 5.0.7; Python 3.14 in the existing analysis venv.
- [observations.json](observations.json) retains raw hex, hashes and decoded
  instructions for five entry-based complete recorded bodies, six bounded data
  spans, both keyboard translation tables, and 240 registry nodes with their
  pointed-to ASCII names. No address was treated as an identity merely because
  it was arithmetically close to another.
- [check.py](check.py) rereads the exact EXE, checks every retained field and
  verifies each node against the existing registry TSV. It also reproduces the
  rival record framing and re-reduces the retained Enter capture from raw bytes.
- [validation.txt](validation.txt) is the receipt. Run from the repository root:

```text
Collaboration/Tools/analysis/venv/Scripts/python.exe Database/FFXII TZA/_experiments/evidence/s44-rebind-discriminator/check.py
```

Quote the script path in a shell because it contains spaces. `--exe PATH` accepts
another copy only when its whole-file hash matches. `--write` is initial capture
only and refuses to overwrite retained observations.

## ASTRA observation 1 — names exist; the absence search missed them

The existing Input-Name-Registry TSV identifies 97 key nodes and 143 channel nodes.
All 240 were checked against the shipping image, including name pointer and type
pointer identity. Actual record layout is:

```text
+00 type pointer (qword)
+08 ASCII name pointer (qword)
+10 next pointer (qword; zero in the image)
+18 numeric value (signed dword)
stride 20 hex
```

| Actual key node | Stored name | Value at node+18 |
|---|---|---:|
| `01F462C8` | `Key_A` | 28 |
| `01F462A8` | `Key_B` | 29 |
| `01F45CA8` | `Key_Enter` | 77 |
| `01F45AA8` | `Key_Up` | 93 |

Every one of the **47 distinct nonzero integers** in the three S-44 tables has a
registered name at the **same integer**. `91..100` are Left, Right, Up, Down, Home,
End, PageUp, PageDown, Insert and Delete. `11..26` have pad aliases; 11..13 also
have mouse aliases. Zero names `Empty` in these registries, but that does not prove
every zero S-44 slot means an empty binding.

This directly falsifies “no input name family exists” and “only live observation
can name one input id.” It is **an integer join, not proof that S-44 uses that
domain**. The request's six-prefix search did not include `Key_` or `Button_` in
their actual case/spelling. No broad new string census was needed.

## ASTRA observation 2 — the compared extents change the argument

`001DF240` really copies 81 dwords from each source: `01DFDA10`, `01DFDB60`,
`01DFDCB0`, into config `+7C`, `+1C0`, `+304`; it then stores 81 at `+448`.
That copy does not establish what the destination slots mean.

The three addresses used as the live-keymap comparison are **three differently
shaped source groups**, not three interchangeable 81-dword profiles:

| Source | Verified consumed extent | Structure |
|---|---:|---|
| `01DF09C0` | 192 bytes | 3 profiles × 16 button codes |
| `01DF0A80` | 768 bytes | 3 profiles × 16 records of `{kind, subKind, codeA, codeB}` |
| `01DF1470` | **16 bytes** | four values: **65, 66, 67, 118** |

The complete materializer `00198B60` increments its first source by `40` hex
(`00198DE9`), its record source by `100` hex (`00198E27`), runs three iterations,
and finally performs exactly one 16-byte read of `01DF1470` at `00198E3F`.
The claimed long permuted run beginning at that last address is outside its
consumed extent. It cannot count as evidence from that four-value table.

Using the button values, the record code fields (not kind/subKind), and the four
extra codes gives **42 distinct nonzero codes, 19 shared with S-44**. Those shared
codes are `28,30,31,35,44,46,50,51,53,64,65,66,67,77,78,91,92,93,94`.
The claimed shared full `11..26` run is absent from these bounded source groups.
The `91..94` directional relationship survives. These corrections weaken the
stated structural argument without proving H1 false.

## ASTRA observation 3 — two old errors cancel in the code-name mapping

The keymap page claims `keymapCode = PInputKeySemantic - 1` and reports a 28/28
semantic fit. Its older record framing starts at `01F45700`, a node's **value**,
then reads the **next node's** type and name. These nodes descend by one. Repeating
that exact rival framing across all 95 alleged records produces names whose real
stored values are one lower than the mispaired values, in **all 95 cases**.

Concrete boundary control:

```text
01F462A8  actual Key_B node, stored value29 at01F462C0
01F462C0  old framing starts here: value29
01F462C8  next node's type pointer: actual Key_A node
01F462D0  next node's name pointer: "Key_A"
01F462E0  actual Key_A value28
```

Subtracting one repairs the wrong pairing's output, not the record layout. The
registry page already corrected the layout but says the minus-one rule is
“untouched”; that sentence needs correction too. For the keyboard examples
verified here the names' registered values agree directly with the code domain.
This does not collapse mouse/pad/device-specific domains into one global index.

Independent controls already exist: the raw ASCII translation table maps `A/a`
to28 and carriage return to77, and the keyboard scancode table at code77 minus28
contains `1C` hex. The retained PID22784 Enter pulse independently observed **array
index49**. Its exact raw receipt SHA256 is
`3c5ad2507a7fb4692d8b398518a74ddd8465ec2c4aa61889e3d62867a0f4a02b`.
Re-reduction verifies 35 zero baseline samples, 34 held samples (32 positive at49,
no other nonzero indices), and one zero release. `49 + 28 = 77`, the actual
`Key_Enter` value. Empty and no-detection versions are rejected by the reducer.

This is reuse of the prior input-registration control, **not a new live run**.
It establishes sampled registration, not action execution or the 81-slot mapping.
The old input receipt retains the original module identity, tool identities,
sequential-sampling limits and cleanup. No historical evidence was replaced.

## ASTRA observation 4 — reuse OPUS's existing serialization correction

OPUS already corrected the binary-file premise in **CON-125**, commit
`22479b09e`. This is not a new ASTRA finding. The retained writer bytes corroborate
it: `001DFD68` takes config `+450` as the file **path**; `001DFD8C` and `001DFDCE`
call `001DEE90` to measure/fill a temporary serialization buffer. `+450` is not
the beginning of a persisted struct payload. The raw mode strings are narrow
`r` and `w`. The serializer walks 31 named settings. A settings-file diff must
therefore be interpreted as text; active keyboard bindings have their separate
`keymap.ini` path and profile array.

Also, `001DFA70` returns true when config `+64` is zero. The materializer skips
its swap when that result is nonzero (`00198D0D`), and swaps when the setting is
nonzero. The request's “swaps when zero” preparation sentence reverses the branch.

## ASTRA claims, limits, consumers and next discriminating evidence

**Refuted:** absence of input names; the long-run interpretation of `01DF1470`;
the stated 35-code overlap based on those extents; the need for a fresh live run
to name one ordinary keyboard code; the one-rebind S-44 closure criterion; the
literal minus-one explanation using correctly framed registry nodes.

**Retained:** the exact 243 copied dwords and their first-run copy mechanism;
the named input registry; the directional-code resemblance; prior observed input
registration. OPUS's no-reader census is inherited, not rerun here.

**Unresolved:** intended purpose and slot roles of the three unused tables,
their causal/type relationship to live bindings, any historical platform/profile
meaning, and the required S-44 L2 disposition. No runtime pointer stability,
universal initialization, normal command reachability or lifetime is inferred.

Return to FABLE: correct the proposal and its supporting note, including the
remaining minus-one claims in both input pages. Return to OPUS: revisit S-44 and
CON-125's preserved name-absence clause using this receipt. The board holds
`ASTRA-CONTRA-FABLE-S44-REBIND-NONDISCRIMINATOR` and
`ASTRA-CONTRA-OPUS-S44-REBIND-NONDISCRIMINATOR`; consumer agreement is pending.

A useful further experiment must connect a **specific S-44 slot** to a known
semantic consumer or distinguish a stated schema relation. Observing another
ordinary key binding alone does neither. If a consumer is identified, prepare
its exact object/save/trigger, baseline, positive observation, read budget,
invalidation and cleanup before any C run. Otherwise leave the mapping unresolved
and continue another independent evidence question.

**Cleanup:** no FF12 launch, process attach, breakpoint, input, configuration/save
write or PC-control session occurred. The evidence tool reads the reference copy
and retained artifacts only. Fresh process census found no FF12 process. No new
restoration was needed, and no claim is made that old backups describe today's
user files. EXP124/127 reviews remain with their existing owners; neither was
recaptured, replayed, promoted or self-audited. Database completion is not claimed.
