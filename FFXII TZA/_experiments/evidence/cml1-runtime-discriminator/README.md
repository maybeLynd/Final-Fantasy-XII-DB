# Correct the CML1 runtime discriminator before taking a live sample

Task `OPUS-REQ-ASTRA-CML1-COLUMN-STABILITY`; consumer OPUS, with FABLE's section008
and scripted-camera interpretation. **Method A only; actual overwrite/reachability
question remains open.** No FF12 launch, input, memory read/write or isolated
original-code execution occurred in this package.

Player version: the proposed camera test would read the wrong table entry if its
8-byte wording were followed. Also, the two candidate shots in the named scene
contain identical camera data, so looking at the camera picture cannot tell which
index the game chose. Correct the address and observe the index itself.

## Exact question and existing evidence

The pending request asks whether `byu_x0100` entry1's authored index14 survives
initialization or becomes first-name-match8, and whether the resolver's index store
003DA28F executes. It calls the records8 bytes and lists003DA35E,003DA456,003DD29F
as three CML1 readers. The existing section008 already documents16-byte entries;
FABLE's retained census already identifies the14-versus8 pair and equal records.
The queue has drifted from its supporting evidence. This package validates the
small discriminating slice against original bytes, not a new bulk format census.

H1: initialized entry retains14. H2: initialization/another writer replaces it,
possibly with first match8. H3: a flawed observer reads a reserved field or the
shake list and mistakes its value for the CML1 index. Offline original instructions
and the named file settle H3's address and presentation pitfalls. They cannot decide
all actual initialized writes or prove that an instruction never runs.

## Primary correction

[check.py](check.py), [observation.json](observation.json), [validation.txt](validation.txt)
retain three complete shipping bodies,490 bytes, exact raw bytes/hashes/disassembly,
and the named [authored EBP](byu_x0100.ebp). Executable identity is
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

| Consumer | Blob binding | Entry address calculation |
|---|---|---|
|003DA330 / read003DA35E|manager+D8|003DA35B doubles RAX; read scale8, displacement14h|
|003DA400 / read003DA456|manager+D8|003DA44A doubles RAX; read scale8, displacement14h|
|003DD230 / read003DD29F|manager+F0, **shake list**|003DD290 doubles RAX; same scale8/displacement14h|

For an admitted entry number `i`, the effective column is **blob+14h+10h*i**.
For `byu_x0100` entry1 (`cut2_2`), it is **blob+24h**, value14 in the authored file.
The erroneous8-byte calculation reads **blob+1Ch**, a reserved zero in entry0.
Entry0 is a poor stride control because both formulas agree there. Entry1 is a
positive discriminator. The copied file has CML1 count15 and CAM7 count16; its
section tags, entry name and all16 length-delimited CAM7 records are checked.

The only name matches are records8 and14. **Both full records are byte-identical**,
not just their names. The existing census already reported their equal payloads;
this bounded recheck also compares the complete record headers/lengths. An otherwise
unqualified screenshot of that shot cannot identify which duplicate index was used.
This does not prove universal presentation parity: runtime channel/context/timing
remain separate variables. Read the actual entry and accepted channel index.

## Corrected future observation specification

Method C is necessary only for the actual initialized/consumer-bound state:

1. FRONTIER/preparation must supply a backed-up save and exact ordinary scene/script
   trigger for `byu_x0100`, or a separately justified labelled resource-load
   intervention with established ABI/thread/ownership preconditions. None is
   established in this package. Do not substitute any ordinary area load.
2. Identify the manager slot and loaded blob through its+D8 binding, original CML1
   count15, entry1 name `cut2_2`, extent and corresponding CAM7 count16/resource
   identity. A magic tag or arithmetic address alone is insufficient.
3. Capture the bound entry1 column at **blob+24h** after load readiness and at the
   relevant normal camera start/hit-check boundary, preserving binding brackets.
   Distinguish14,8, another value, missing resource and failed read. If measuring
   downstream selection, establish actual entry1 invocation/channel identity;
   an injected start call proves that intervention only.
4. Positive controls: exact build/modules/read detector, nonzero known read, rejected
   null read, bound resource/name/count match, entry0/1 stride discriminator and a
   demonstrably executed camera action. Screenshot is presentation evidence only.
5. Start with at most two samples at each of two qualified states (four total,
   <=2KiB of focused identity/entry/channel data per sample, excluding existing
   code-identity controls); <=15 minutes after launch. No broad export or trace.
   Stop on missing trigger/binding, control failure, fatal dialog, takeover or budget.
6. Accept only the sampled initialized value/action. `14` at both endpoints means
   those endpoints retain14; it does not rule out an intermediate overwrite/restore.
   A bounded no-hit trace cannot establish **never executes**. If that stronger
   temporal distinction matters to the consumer, prepare a separately controlled
   focused observer, informed by EXP127's pending failure review; no unchanged
   breakpoint experiment or broad retry is authorized by this specification.
7. Use the established fresh save/config backup, Cloud protection, ordinary health
   checks, normal exit, handle cleanup, full restoration hashes and immediate PC
   reset. Return raw receipts/screenshots, reducer/controls and affected claims.

Required preparation remains **exact reachable save/scene trigger, manager/resource
binding and action identity**. The read-only correction is complete; CML1's actual
runtime overwrite question is not. OPUS should update the queued address/reader
description; FABLE's canonical16-byte layout stands. No L1/L2 claim is waived and
no live percentage/count target is advanced.

An initial attempt to reuse the camera-RNG collector rejected this narrower body
set because that collector requires its own five-slot caller; it emitted no result.
The bounded reader here reuses the same PE-section mapping and Capstone approach
without changing the existing instrument or claiming a successful failed run.
