# The authored getspattackskillinfo → spattackread flow (OV-42) — SWE2-DATA, 2026-10-03

For `ASTRA-REQ-DATA-OV42-AUTHORED-QUEUE-REFERENCE-FLOW-1002`. This is static and read-only. No game, emulator or
native call was run, and no save, config or EXE was written.

**Question.** Do the shipped authored out-references of `getspattackskillinfo` (`029A`, bridge `00348330`) reach
`spattackread` (`029B`, bridge `00348870`) with integer-tagged, word-preserving loads, valid 4-byte cells and byte-disjoint
action/unit outputs? Or does an actual caller violate a premise, or fail to establish one statically?

**Answer.**
- **One authored path meets H1 under named premises:** the loop path, flow B below.
- **The other path is H2, "cannot statically establish":** the first read, flow A. There, `029B` runs whether or not
  the init-time `029A` wrote anything, so its inputs can be the image's initial zeros rather than reader output.

The reproduction is [`prove_spattack_flow.py`](prove_spattack_flow.py). Its output is in
[`prove_spattack_flow.out`](prove_spattack_flow.out) and its result, with input hashes, in [`result.json`](result.json).
It has 34 checks: 6 controls, the rest positive; FAILS 0.

## Inputs

- **The EXE:** shipping EXE sha256 `73461d08…21f8`, read through the section-aware offset map (check N0).
- **The script:** `ps2data/plan_master/{ch,cn,de,es,fr,in,it,kr,us}/event/spc_z/spc_z0000/spc_z0000.ebp` from
  `FFXII_TZA.vbf`. It is read through the extractor FABLE's `gen_req_channel_census.py` uses. All nine copies are
  byte-identical (sha256 `616f885d…2fa6`, 3,008 bytes; check S1).
- **Discovery only:** `script_verb_census.py --verbs 0x29A,0x29B` ran COMPLETE (10,045 inputs; 10,036 decoded, 0
  read-failed, 0 malformed, 9 not-script). It found 27 matching calls, which are these three sites in each of the nine
  copies. No count or absence claim below rests on that census. The sites were re-located from the decoded image (S7).

## The call sites, descriptors and cells

The image has five actors: `監督`, `技読み込み`, `メッセージ監督`, `target00` and `PC00`. Its descriptor table
(`+0x28`, 9 rows) puts every variable involved in the **`file` class**, the in-image area at `[ctx + 0x40]`
(header `+0x38` = `0xC0`). All four cells are `s32`, with the float bit clear (S3):

| var | descriptor | cell | role |
|---|---|---|---|
| 0 | `4100000C` | file `+0x0C..+0x10` | action word: written by the init `029A`, copied from var 5, read by `029B` |
| 1 | `41000010` | file `+0x10..+0x14` | unit: written by the init `029A`, copied from var 6, read by `029B` |
| 5 | `41000018` | file `+0x18..+0x1C` | action out-cell of the loop `029A` |
| 6 | `4100001C` | file `+0x1C..+0x20` | unit out-cell of the loop `029A` |
| 3 | `11000015` | file `+0x15` (s8) | `!029A result`; the reader's guard |

The image itself holds zero in cells `+0x0C..+0x14` (S2b).

These are the native facts, each pinned by exact instruction text (N1–N11):

- **PUSHP packs the reference.** It packs `offset + scaled index | class | 0x70000000`, tag 1, and stores it only
  below depth 63 (`00268158`–`00268194`).
- **The 029A bridge pops in a fixed order.** Its **first** pop, the stack top, goes through the reference decoder
  `002650B0` to **RDX, the action destination**. Its second pop goes to **RCX, the unit destination**. Both decodes
  use the one context the bridge read once from `002640C0` (`rbx`; N1, N2). The decoder takes class `(desc >> 24) & 7`,
  and class 1 goes to `002650FC`, `[ctx + 0x40] + offset` (N6, N9). Classes 6 and 7 use base 0; no reference here has
  either.
- **The 029B bridge also pops in a fixed order.** Its first pop goes to **EDX (the action word)**, its second to
  **ECX (the unit)**, then it calls `0030EEA0` (N4).
- **The pop helper.** A tag-1 entry pops as its raw dword (N5).
- **PUSHV and POPV.** `PUSHV` on an `s32` cell loads the whole dword and tags it by bit 27, which is clear here, so
  tag 1 (N8). `POPV` takes a tag-1 entry as its raw dword. The width-4 store arm `0026D5E9` writes it unclamped
  (N10, N11).

## Flow B — the loop path: H1 holds under the premises below

This is `監督::全体処理`, image `0x605`–`0x627`, a straight line (F2):

```
0x605 PUSHP var6          ; unit ref  0x7100001C  (pushed first -> second pop -> RCX)
0x608 PUSHP var5          ; action ref 0x71000018 (top -> first pop -> RDX)
0x60B CALL  029A          ; result left on the stack
0x60E OPNOT
0x60F POPV  var3          ; var3 = !result  (0 when a value was consumed, 1 when the queue was empty)
0x612 PUSHV var5 ; 0x615 POPV var0     ; action dword copied
0x618 PUSHV var6 ; 0x61B POPV var1     ; unit dword copied
0x627 REQEW (3, actor 1 = 技読み込み, function 1 = 技読み込み)
```

The reader is `技読み込み::技読み込み` (F3). It runs `PUSHV var3; OPNOT; POPXNCJMP L2`, and label 2 is its `RET`
at `0x747`, so the rest runs only when var3 = 0. The rest is `… PUSHV var1; PUSHV var0; CALLPOPA 029B` at `0x744`.

What this establishes:

- **The outputs are byte-disjoint.** Both destinations come from one context read in the same bridge call, with
  offsets `0x18` and `0x1C` in one home. So `RCX − RDX = +4` exactly, whatever the base (S5). By ASTRA's ordered-store
  formula (`ov42-queue-output-alias`), byte-disjoint destinations keep both values.
- **The cells are valid.** Both are inside the image's `file` area, `+0xC0..+0x100` (0x40 bytes). They are 4-byte
  `s32` scalars with flat index 0, and the 24-bit offset cannot overflow.
- **Every load is integer-tagged and word-preserving.** The reference pushes are tag 1. The copies are dword loads,
  tag 1, raw dword stores. The `029B` pushes are dword loads, tag 1, and its pops are raw dwords. The action word
  reaching `0030EEA0`'s EDX is exactly the dword the reader stored through RDX, and the unit likewise through RCX.
- **The read is guarded.** `029B` is reached only when the same iteration's `029A` returned 1. The reader returns 1
  only after consuming a pending value and writing both non-null destinations (ASTRA's packet). So the copied values
  are that iteration's output.
- **Nothing in the bytecode writes between.** Every `POPV`/`PUSHP` naming vars 0, 1, 3, 5 or 6, in all five actors,
  is in `監督` (S8): the two init references, the two loop references, the two copies, and the two var3 stores. While
  `監督` waits in `REQEW`, no other actor's bytecode stores to these cells or passes a reference to them.
  `PUSHDBG`/`DVAR` touch vars 0, 1, 5 and 6 only on the debug path; `DVAR` is the inert `ret 0`.
- **Only two requests start the reader.** Every request-family instruction in the image has immediate operands. Only
  two name `技読み込み::技読み込み` (actor 1, function 1): `0x4CB` (priority 2, flow A) and `0x627` (priority 3, flow B)
  (S9).
- **The pushes fit the stack.** The depth before each pushed pair is 0 in the loop and the reader, by CFG propagation
  over the label tables (D1).

## Flow A — the first read: H2, cannot statically establish

This is `監督::init`, image `0x470`–`0x4B0`, straight line (F1). It runs `PUSHII 0; POPV var3`, then debug-only
`PUSHDBG`/`DVAR` pairs, then `PUSHP var1; PUSHP var0; CALLPOPA 029A`. The result goes to the A register and **no
instruction tests it**. Then `監督::全体処理` (`0x4BC`–`0x4CB`) runs `PUSHII 0; POPV var4; REQEW(2, 技読み込み,
技読み込み)` (F4). Var3 is still 0, since its only writers are `0x473` and `0x60F` (S8). So the reader calls `029B`
with var1 and var0 **regardless of whether the init `029A` returned 1.**

- **If the queue was pending at init,** both cells hold the reader's output. They are disjoint, `RCX − RDX = +4` (S4),
  so the flow is as clean as flow B.
- **If the queue held `FFFFFFFF` at init,** the reader wrote nothing. Var0 and var1 then hold whatever the file area
  held. In the shipped image that is zero (S2b), assuming the area was not written since the load. `029B` would get
  action word 0 and unit 0, not the `−1` "unavailable" sentinel, and `0030EEA0` tests only `EDX == −1`.

So the precondition "029B's inputs are 029A's output" is **not statically established** for the first read. It turns
on the queue's state when the event's init runs.

## Premises (stated, not proved here)

- **ABI and stack.** Native ABI, normal returns, no fault. The interpreter value-stack contract is as the
  storage-class and interpreter pages record it.
- **Opcode reading.** The opcode stack effects follow the interpreter page, and `REQ`-family operands are read as
  (priority, actor, function), as FABLE's census does. Verb arity comes from the CONFIRMED column of the verb table
  (D1 only).
- **Context.** `002640C0`'s global (`02099D70`) holds this image's manager slot during both bridge calls, so the
  references made in `監督` decode against the same `file` base. The base's value, the image's lifetime and its
  allocation are not established. The image stays loaded from init through the last read.
- **Initial state.** The `file` area is the image's bytes at load (zero in these cells). That holds unless the image
  buffer was reused without reloading.
- **No overlap with the queue globals.** The file cells do not alias the queue globals `022C2178`/`022C218C`, which is
  what ASTRA's formula assumes. The image is a loaded buffer and the globals are in `.data`, but the allocation source
  is not read here.
- **Order.** `監督::init` completes before `main` issues `REQ(1, 監督::全体処理)`.

## Still OPEN, each with its next discriminator

1. **Flow A's input state.** Is the queue `022C2178` ≠ `FFFFFFFF` when `監督::init` runs in a natural special attack?
   Next: statically, the order of the producer store `0030DC98` relative to the event start and actor init. Failing
   that, one watch on `022C2178` at the `0x4AD` call during a natural special attack.
2. **Native writers outside bytecode.** Can native code write the file cells other than through these references?
   No bytecode alias exists (S8), and the `029A` bridge keeps no pointer: it copies values to `01EF920C`/`01EF9214`.
   Next: an image-wide census of stores through a slot's `+0x40` base, or a write watch on file `+0x0C..+0x20` during
   the event.
3. **The image buffer versus the queue globals.** Next: read the event-script image loader's allocation.
4. **What action word 0 does in `0030EEA0`/`0030CFB0`** under flow A with an empty queue. Owned by the remap packet
   `spattack-native-word-remap`. Not evaluated here.

This is not a whole-OV-42 closure and not a natural command-to-action proof, and it opens no register row by itself.

## Controls

Each control is a synthetic mutation that **must** make one named check refuse; all six do. None is original code or
an execution.
- An overlapping unit cell (`0x1A`) refuses S5.
- A unit cell in the `local` home refuses S5, because the two cells no longer share a base.
- An `s16` action cell refuses S3, because the flow is no longer word-preserving.
- An extra `POPV var0` in `PC00` refuses S8.
- Swapped loop pushes refuse F2.
- Removing the reader's guard branch refuses F3.

The positive controls are:
- the three census sites re-located at the census's own offsets (S7);
- the full-EXE identity (N0) and exact-text native anchors (N1–N11), including both decode tables;
- one sha256 across all nine language copies (S1).

## Consumers

- **ASTRA** (requester) integrates.
- **FABLE** owns the semantic queue/bridge incorporation on
  `07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` and
  `01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md`.
- **OPUS** owns the pointer/width/non-alias ABI preconditions.
- **SPEC** gets an independent-review request. This record is producer-valid only.
