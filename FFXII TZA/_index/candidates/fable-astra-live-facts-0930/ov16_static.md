# OV-16 static pass: how a script wait can be abandoned (FABLE, Claude Opus 5.5, 2026-09-30)

OV-16 asks whether shipped play re-arms a notification key (issuer channel, continuation offset) while an older request
with the same key is still pending. The probe notes (`../ov-rt-probes-0929/notes.md` section 3) show a stale
notification can satisfy a later wait only if the earlier wait was **abandoned**: the issuer's entry is removed while it
waits, or its channel restarts.

This record works out statically which paths can remove a live entry. It narrows what an observation would still have to
show. Scripts: [`kind_args.py`](kind_args.py) / [`kind_args.out`](kind_args.out) and [`kind_back.py`](kind_back.py) /
[`kind_back.out`](kind_back.out), run from `Database/Tools/work/FABLE/takebacks/`.

## Who removes entries

`ActorResource_RemoveActiveEntry` `003DB2A0` has seven raw callers (E8/E9 index):
- the two consumes: `0025B456` and `0025E0B0`, which remove a matched notification;
- two interpreter sites: `00261241` and `002613E5`, which remove the actor's running entry `[actor+0x62]` and select the
  next one. These are the return/end opcodes, which post the end notification; they complete a request, they do not
  abandon a wait;
- `00262708` in `002626C0`: every kind-4 entry on channel 3 or 5 (by the class byte `[actor+3] & 0x1F`);
- `00262788` in `00262740`: every kind-5 entry on channel 4 or 6;
- `003DB506` in `ActorResource_RecycleEntryRange` `003DB420`, reached from three interpreter opcodes: `RETN` `0x2E`, `RETTN` `0x30` and
  `REQCANCEL` `0x35` (`00261312`, `0026133A`, `00261499`; mnemonics per the opcode table in
  `worldactor-scriptvm-interpreter.md` and `../bf1-opcode-semantics/`) and `Actor_RequestResourceReentry`. It walks the actor's channel lists over a channel range,
  or a single channel: `edx` is the start, bounded by `[actor+0x88]`, and the active-channel mask is `word [actor+6]`
  (`003DB432`-`003DB4AC`). On each list it takes the first entry whose run state `+0x11` (the scheduling page's section 2.5) is non-zero and fits
  the mode in `r8d` (modes 3 and 4 special-cased at `003DB466` / `003DB479`), and removes it. **This is the script-driven channel
  cancel,** and it can remove a channel's running entry, including one that is waiting.
- *(Narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's ACCEPT-WITH-NARROWING, `../auditsem-review-livefacts-0930/REVIEW.md` §6, N2, the verb route this list missed:)* `freqcancel` / `freqcancel2` (`00352980`) and their two-argument forms (`00353660`, another actor) recycle channels from their argument upward through `003DB420` mode 4; the shipped scripts call `freqcancel` / `freqcancel2` 84 times, 77 of them `freqcancel(0)`.

## What kind an entry has

The kind is `entry byte +0x12 >> 1`, compared at `003DBF0F` in `003DBEA0`. `ActorResource_InsertEntryFromDescriptor`
`003DB7A0` stores the whole of `desc+8` into `+0x12`. It runs two bitfield merges with mask 1 (`003DB8E5`-`003DB903`),
and the second stores the source byte itself.
- **Script requests.** `ScriptVM_SubmitActorRuntimeRequest` `00268850` stores `desc+8 = 1` (`002689C0`), so their kind is 0.
  The R / F / T letters of `REQ` / `FREQ` / `TREQ` are the descriptor's `+0` kind (0 / 2 / 4), which is **not stored**:
  it selects the insert behaviour (scheduling page section 2.4). So they are a different field from `+0x12`.
- **Notifications.** The posters `003DBE5F` and `003DC122` also store `desc+8 = 1`, so they are kind 0 too.
- **`ActorResource_SubmitRequestDescriptor` `003DBB60`** takes `desc+8` from its fifth argument (`003DBB64` ->
  `003DBBBF`). All 23 call sites resolve to kind 0, 1 or 2:
  - four sites pass constants;
  - `r13d` is zeroed in `ActorStorage_InitializeRecord`;
  - `eax` is zeroed right before the store at `0025C230`'s three sites. An earlier note misread the `mov eax, 8` at
    `0025C630`, which is a compare operand;
  - the rest are `sete` values or registers bounded to 0..3.
- **`003DBBF0`** takes the kind from its **sixth** argument: `byte [rsp+0x78]`, doubled, with bit 0 OR'd in
  (`003DBBFA`-`003DBC11`).
  - The motion setter `00268EA0` passes 5 (`00268FDD`) at `00268FF2`, with channel 4 or 6 in `r8d`.

**So the kind-4/5 entries are motion entries, and the only code that clears them is the motion setter itself.** It
removes the old kind-4/5 entries (`00268FA6` / `00268FAE`) and then submits new ones: a replace-current-motion pattern on
channels 3 to 6.

## What this narrows

There are two abandonment routes: the motion replacement below, and the script-driven cancel (`003DB420`) above.
Through the motion route, a script wait can be abandoned only if all of these hold:
1. a function started as a kind-4/5 motion entry on channel 3 to 6 runs bytecode that issues `sysReqsw` / `sysReqew`;
2. the motion setter replaces that entry while it waits;
3. the same function later re-runs to the same continuation offset while the old request's notification is still
   unconsumed.

Script-issued requests (kind 0) are never removed by the motion clears.

What static and authored evidence can still settle:
- the ids the motion setter starts (`r9w` / `desc+4`, from the table at `[rcx+rbx+0x22]`, `00268F68`), and whether those
  authored functions contain a waited request;
- which shipped scripts use `RETN` / `RETTN` / `REQCANCEL` so that they recycle a channel that can be waiting. These
  opcodes are not visible as named verbs in the decompiled corpus (`corpus/us/*.txt`), so this needs a bytecode-level
  count over the `.s000` blocks.

If no motion function contains a waited request, and no shipped cancel targets a channel that is waiting, OV-16 closes
statically. If one does, the fact left for an observation is the **interleaving**: whether a motion replacement lands
while that function waits, and whether it re-runs to the same offset before the stale notification is consumed. That
depends on frame timing and script scheduling, not on a code path.

## The shipped scripts use the recycle route heavily (opcode census)

[`ov16_opcode_histogram.py`](ov16_opcode_histogram.py) ([output](ov16_opcode_histogram.out)) counts every instruction in
the 7,565 distinct shipped `.ebp` files: 198,302 scripts, 114,878,319 instructions, 0 decode anomalies. The decode rules
are those of `../bf5-inert-opcodes/`.
- `REQCANCEL` `0x35`: **0**. ~~No shipped script cancels a request explicitly.~~ *(Narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's ACCEPT-WITH-NARROWING, `../auditsem-review-livefacts-0930/REVIEW.md` §6, N2:)* No shipped script uses the `REQCANCEL` opcode; explicit cancels go through the `freqcancel` verbs.
- `RETN` `0x2E`: **135,429**, and `RETTN` `0x30`: **6,039**. `RETN`'s handler (`0026131C`) pops a depth and calls
  `003DB420` from channel `depth + 1` upward with mode 0 (`0026133A`), but only when `depth + 1` is at most the running
  channel `[record + 0x11]` (`00261327`-`0026132E`; otherwise it skips). `REQCANCEL`'s handler (`00261301`) would recycle
  from `index + 1` unconditionally (`00261312`), but no shipped script uses it. So the recycle route sits behind
  141,468 shipped instructions, each gated by its popped depth against the running channel. Whether the gate opens is
  set by that operand and the channel the function runs on. Neither was censused here.
- The waited requests `REQSW` `0x24` (27,898) and `REQEW` `0x27` (115,766) are common. The `F`/`T` variants
  (`0x22`/`0x23`/`0x25`/`0x26`/`0x28`/`0x29`) are 0.

So OV-16 **is not closed statically** by showing the abandonment route unused: its entry points are pervasive in the
shipped content. The `RETN` operand census below completes the static side. The specific fact no static reading supplies is **the interleaving**: whether a `RETN` / `RETTN`
recycle, or a motion replacement, removes a channel's entry while that entry is parked in a `REQSW` / `REQEW` wait, and
whether the same function then re-runs to the same continuation offset before the old notification is consumed. That
depends on frame timing and script scheduling. The probe sites in `../ov-rt-probes-0929/successor-request.md` item (3)
remain a suggestion; ASTRA selects the method.

## The RETN operands (census, 2026-09-30)

[`retn_depths.py`](retn_depths.py) ([output](retn_depths.out)) reads the instruction before every shipped `RETN` / `RETTN`.
The control is the histogram's totals, which match: 135,429 / 6,039.
- **Every one is preceded by `PUSHII`**, so the depth is an immediate.
- `RETN` depths are 0 (133,665), 1 (1,143) and 3 (621). `RETTN` depths are all 1 (6,039).

`003DB420` walks channels from the actor's slot count (`[actor+0x88]`) minus 1 down to `depth + 1` (`003DB432`-`003DB48B`).
So `RETN 0`, run on any channel of 1 or more (the gate at `0026132E`), recycles channels 1 upward. That includes any
higher channel parked in a `REQSW` / `REQEW` wait, whose request's notification then arrives with no waiter.

~~The static side is therefore complete.~~ *(Narrowed 2026-09-30, FABLE, on SWE2-AUDIT-SEM's ACCEPT-WITH-NARROWING, `../auditsem-review-livefacts-0930/REVIEW.md` §6, N3:)* The RETN side is complete statically; the motion route's static question (whether a function the motion setter starts contains a waited request) is still open. The abandonment route is armed by ordinary shipped code. What stays run-time is
which channel a function runs on at that moment (`[record+0x11]`), whether a higher channel is waiting then, and whether the
same function later re-arms the same continuation offset before the stale notification is consumed.

**Parked 2026-09-30.** Next: the id map for motion entries, and the three cancel opcodes' verb names and their uses in
the script corpus.
