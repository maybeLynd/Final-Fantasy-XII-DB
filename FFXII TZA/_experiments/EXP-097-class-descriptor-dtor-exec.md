---
experiment: EXP-097
title: Phyre class descriptor destructor under isolated original execution
contract: ../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md
method: B
live_game: false
tool: evidence/class-descriptor-dtor-exec/check.py
---
# EXP-097 — class-descriptor-dtor-exec

**Status:** complete · **15/15 cases, 10/10 mutants, stable across two processes**
**Evidence:** `evidence/class-descriptor-dtor-exec/` (`check.py`, `result.json`,
`bodies.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-phyre-class-descriptor.md`'s destructor pilot
(`diff_class_descriptor_dtor.py`) ran `00633390` with **both** list-callees
stubbed — what `0063D640` does to the `+0x70` sub-object and what `006B6700`
does to the `+0x60` list was the open residual. This experiment executes the
destructor and both callees — plus the TLS context getter `006373D0` inside
the detach path — as real shipped bytes. Only the heap stays scripted.

| VA | role | execution |
|---|---|---|
| `00633390` | class-descriptor destructor | **real** |
| `0063D640` | `+0x70` sub-object registry detach | **real** |
| `006B6700` | `+0x60` intrusive-list drain | **real** |
| `006373D0` | TLS context getter (current-object lookup) | **real** — planted initialized TLS state |
| `00584730` | `_aligned_free` | **scripted at entry** — `rcx` logged in call order; heap internals are the disclosed boundary, exactly as the pilot left them |

The observable is the call trace plus post-state inspection of every list
head and node: `d` = destructor entry, `S<arg>` = `0063D640` entry with its
`rcx` (the sub-object pointer), `T` = `006373D0` call, `F<addr>` = free
boundary argument, `L<off>` = `006B6700` entry with `rcx - obj`.

## Executed bodies (real shipping bytes)

4 bodies, spans + sha256 in `bodies.json` (`real` array); the free boundary
is listed separately (`stubbed`).

| VA | span | role |
|---|---|---|
| `00633390` | 500 B | destructor — vtable swap `0xD581C0`→`0xD31168`, counter guard `0x2CF8260`, six-list teardown |
| `0063D640` | 109 B | sub-object detach — embedded-node unlink, registry conditional detach |
| `006373D0` | 99 B | TLS ctx getter — `gs:[0x58]` → slot `[0x2EAED3C]` → `0x1F2E330` |
| `006B6700` | 71 B | `+0x60` drain — pure unlink loop, no frees |

## Fixture surface

- Descriptor object at `0x40000000`; heap arena `0x40000000–0x40400000`
  (sub-object `+0x10000`, node arena `+0x100000`, payloads `+0x200000`,
  registry heads `+0x300000`/`+0x310000`).
- Counter dword `0x2CF8260`; descriptor counter field at `obj+0xE8`.
- TLS: `gs_base` → fixture TLS; `gs:[0x58]` → slot array; index dword
  `0x2EAED3C` = 3; slot → ctx; `ctx+4 = 4` vs lazy-state `0x2CF94EC = 0`
  → the initialized arm returns `0x1F2E330` without entering lazy init.
- Node layout (from the bodies): intrusive circular list `{flink@0,
  blink@8}`; owned-node payload pointer `@+0x18`; ownership byte `+0x20`
  bit 0. List heads are sentinels self-linked `{flink=head, blink=head}`.
- `obj+0x50/+0x58` is the descriptor's own embedded node (unlinked by
  `0063D640` from whatever list owns it — planted into `OBJREG` when linked).
- `obj+0x70` → sub-object; `sub+0x10` = its member-list head; `sub+0/+8` =
  its registry node into `REG`.
- All IAT slots nulled; the destructor's call edges reach only the four
  bodies above.

## Findings (native-verified)

1. **Vtable discipline verified.** `0xD581C0` is stored at entry and
   `0xD31168` at exit; `m-vtbl2` (final write NOP'd) leaves the derived
   vtable in the object and diverges in all 15 cases.
2. **Counter guard verified.** `[obj+0xE8]` is incremented, compared to
   `0x2CF8260`, and the global is decremented only on equality
   (`counter-eq`: field 4, counter 5→4). `counter-wrap` proves the wrap
   edge: field `0xFFFFFFFF` + 1 wraps to 0 == counter 0, and the guarded
   decrement stores `0xFFFFFFFF`. `m-inc` (increment removed) and
   `m-counteq` (`jne`→`je`) both diverge everywhere.
3. **`0063D640`'s real argument order is `(rcx=sub-object, rdx=obj)`** —
   the destructor passes `[obj+0x70]` in `rcx` and `obj` in `rdx`. It
   unlinks `obj`'s embedded node at `rdx+0x50/+0x58` (self-links it
   afterward: `objnode-linked`, `objnode-linked-members`), checks whether
   the **sub-object's** `+0x10` member list is empty, and only then
   compares the sub-object against the TLS-registered current object —
   detaching `sub+0/+8` from `REG` iff the list is empty AND the
   sub-object is not current.
4. **Registry-detach conditions verified both ways.** `empty` (list empty,
   not current): `T T` — the getter is called twice — and `REG`
   self-links. `sub-members` (list nonempty): no `T` at all, `REG` keeps
   the node. `sub-current` (empty list, sub == `0x1F2E330`): one `T`,
   compare fails, no detach. `m-regcmp` (`je`→`jne`) detaches the current
   object and diverges in 13 cases.
5. **Ownership-pass ordering verified.** In `+0x90`/`+0xA0` the destructor
   walks the list once: owned nodes (`byte[node+0x20] & 1`) are unlinked,
   payload `node+0x18` freed, then the node itself freed — free order in
   `l90-two-owned` is `F<pay0> F<node0> F<pay1> F<node1>`. Unowned nodes
   are skipped in pass 1 and unlinked (not freed) in pass 2
   (`l90-unowned`, `la0-mixed`; `m-ownbit` and `m-payoff` killed).
6. **Four unlink-only drains verified.** `+0x80`, `+0x90`, `+0xA0`,
   `+0xB0` are each walked and every survivor node unlinked with no free
   calls (`l80-drain`, `lb0-drain` carry owned-flagged nodes and still
   free nothing — the ownership test exists only in the pass-1 walks).
   `m-selflink` leaves stale links observable in `l90-unowned`.
7. **`006B6700` is a pure drain.** It unlinks the `+0x60` circular list
   node-by-node until the head self-links — no payload reads, no frees
   (`l60-drain`, `all-lists`; `m-list60` corrupts the drain and diverges).
8. **All five lists populated simultaneously** (`all-lists`) — the order
   of operations is fixed: `S` → `T T` → pass-1 frees for `+0x90` then
   `+0xA0` → unlink drains → `L60` last.

## Mutants (10/10 killed)

| mutant | site | semantic |
|---|---|---|
| `m-counteq` | `0x6333CF` `jne`→`je` | counter decrements when NOT equal |
| `m-ownbit` | `0x633418` imm `1`→`2` | owned nodes never freed |
| `m-payoff` | `0x633439` disp `0x18`→`0x10` | wrong payload address freed |
| `m-drain90` | `0x6334EA` `je`→`jne` | empty `+0x90` head enters the drain |
| `m-sublink` | `0x63D655` `mov [rdx+8],rax` NOP | embedded node half-detached |
| `m-regcmp` | `0x63D68B` `je`→`jne` | detaches the current object |
| `m-list60` | `0x6B6736` `mov [rcx+8],rax` NOP | corrupt `+0x60` drain |
| `m-vtbl2` | `0x633568` vtable store NOP | object keeps derived vtable |
| `m-inc` | `0x6333C5` `inc eax` NOP | counter compare off by one |
| `m-selflink` | `0x6334F1` `mov [rcx+8],rax` NOP | pass-2 survivors keep stale links |

## Not exercised (disclosed, not claimed)

- `00584730` `_aligned_free` internals — entry-hooked, `rcx` logged in
  order. Heap allocator behavior is a boundary, not a claim.
- `006373D0`'s lazy-init arm (`008092FC` / `00808B90` / `0080929C`) — the
  fixture plants the initialized state (`ctx+4 > 0x2CF94EC`); only the
  already-initialized path is proven.
- Every other descriptor method (`006388C0`, `0063D550`, the deleting
  destructor), the ctor that populates these lists, and all live-process
  behavior.
- What the five lists *mean* — this proves the teardown mechanics, not the
  roles of `+0x60`/`+0x80`/`+0x90`/`+0xA0`/`+0xB0`.

## Harness notes

- `emu_start` pushes no return address — fixture stack-args sit one slot
  higher than an ABI caller would write them (same discipline as EXP-094).
- `m-drain90`'s patch initially landed one byte early (on the disp of the
  preceding `cmp`); verified against shipped bytes before rerunning.
  `m-ownbit` likewise — the test's immediate is at insn+4, not +3.
- The pilot's prose suggested `0063D640(obj, subobj)`; the body reads
  `rcx` as the sub-object and `rdx` as the descriptor. Fixture mapping was
  corrected to match the body, not the prose.

## Owner qualification - node observation and `m-selflink` (SWE2-ORACLE, 2026-09-30)

Answers `ASTRA-RETURN-ORACLE-EXP097-NODE-OBSERVER-AND-MUTATION`.
- **The node post-state is heads only.** `run_case`'s observation records list heads and free calls, not list-member
  spans. Read "post-state inspection of every list" above as that. A corrupted member `prev` behind an empty head is not
  visible to this harness.
- **ASTRA's raw-node control covers that case.** It runs the original `006B6700` and a full-store NOP of `006B6740`:
  the same empty head, a corrupted node `prev`, and a raw-span detector that rejects it (`29df1a564`). OPUS consumed it
  in `280cc7570`.
- **`m-selflink` is not a self-link mutation.** At `006334F1` it NOPs the 3-byte `mov rcx, [rdx]` pointer load and part
  of the next instruction. Its kill is not isolated self-link coverage. The intended targets are the self-link stores
  `006334FF` / `00633502`, and the neighbour-unlink store `006334F8`.
- **Owner decision.** The historical driver is qualified, not re-run. The raw-node regression is ASTRA's control. The
  10/10 kills and the head/free-call observations stand as recorded. Node allocation provenance stays out of scope.
