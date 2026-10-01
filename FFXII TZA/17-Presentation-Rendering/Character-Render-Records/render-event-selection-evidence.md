---
system: Render event selection and presentation-entry reference lookup
category: 17-Presentation-Rendering
status: DOCUMENTED — UQ-192 is NOT A QUESTION (a class-2 process item on its carrier) and UQ-193, UQ-194 and UQ-195 are ANSWERED; every box is closed and the prose residue is answered in place (owner re-status 2026-09-30, OPUS) — peer consumption into capability policy (UQ-192, NOT A QUESTION), caller responsibility for stale ids (UQ-193, answered 2026-09-27); UQ-194 answered 2026-09-27; UQ-195 answered 2026-09-17
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 78 addresses cited - 7 data, 49 entry, 21 interior, 1 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-render-event-selection-evidence-pass-1-peer-consumed
---

# Render event selection and presentation-entry reference lookup

The getter's apparent policy test simplifies under its actual arguments, but the
resource lookup it calls can still refresh a cached pointer or fault on invalid state.
This distinction matters to the battle unit's current presentation event, player
control suppression and the presentation-to-movement coast-down tail.

Evidence is sealed in [the method and raw package](../../_experiments/evidence/render-event-selection/README.md).
This is offline static analysis and isolated execution of shipping instructions with
controlled state. It establishes no live initialization, resource admission or scheduling.
The [capability-policy falsification](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md#11-independent-falsification-polarity-gate-precedence-and-invalid-state)
left the nontrivial selection unexecuted; this package addresses that dependency.

## 1. The entry lookup can write

`0051B9E0` is a five-byte tail jump to `0051F240` (138 bytes). The latter is not a
read-only map lookup. With container in RCX and ID in EDX:

1. Sign-extend the low two bits of `container+4`. Only values 0 and 1 are accepted;
   bit patterns 2 and 3 become -2/-1 and return null.
2. Kind 1 takes the full table pointer from `container+8`. Kind 0 passes that full
   value through `003AB7F0`, whose raw/tagged behavior is already established in
   [the source lifetime evidence](../../02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md#15-efx-relocation-repairs-selected-references-with-a-signed-32-bit-displacement).
3. Add `0x30 * uint16(id)` to that base. Only the resulting pointer is tested for
   zero. There is no capacity, high-ID/generation or occupied-bit check in this body.
4. If entry byte `+0` has bit `0x02`, resolve the full source at entry `+10` through
   `003AB7F0`, add dword `+20` in **EAX**, sign-extend the result, and store it to the
   full cached pointer at entry `+18` (`0051F2B1`–`0051F2B7`).
5. Return full cached pointer `+18`, whether refreshed or not. The refresh flag is
   not cleared here, so another call can refresh again.

The cache refresh is exactly `u64(sign32(low32(resolved_source) + offset32))`, with
32-bit wrapping addition. It is not a general 64-bit base-plus-offset operation.

| Original-code case | Returned pointer / effect |
|---|---|
| Refresh clear, cache `0x180000000` | Full `0x180000000`, no write |
| Source `0x40000000`, offset `0x20`, refresh set | Cache and return `0x40000020` |
| Source `0x80000000`, offset `0x20` | Cache and return `0xFFFFFFFF80000020` |
| Source `0x140000000`, offset `0x20` | Cache and return `0x40000020` |
| Source `0x40000000`, offset `0xC0000000` | Cache and return zero |
| IDs `1` / `0xBEEF0001` | Same slot and full cached result |
| Kind 0 with untagged table provider | Same table/slot result |
| Kind 2 / 3 | Null return before table access |
| Null table, ID 0 | Null return |
| Null table, ID 1 | Invalid read at `0051F2A3`, address `0x30`, before a write |

The last two form a controlled boundary: a null base is not generally a safe miss
once a nonzero index is added. That invalid-state fault is not a claim that ordinary
gameplay reaches it. These runs use untagged provider sources and do not establish
tagged-handle ownership, table capacity or ID lifetime.

## 2. The resource-dependent default is permissive

`00424230` (77 bytes) returns 1 when render dword `+C4 == -1`, or when the entry
lookup returns null. Otherwise it returns entry dword `+2C8` **bit 12**, through
`0041C760` (14 bytes). The bit-clear and bit-set original-code controls return 0/1;
the absent-entry and ID-minus-one controls both return 1.

For a present ID, the route is:

`ImageAddress_ResolveRuntimePointer(render+10) -> root+DA8 -> 0051B9E0(container, render+C4)`.

`0020E600` is the ten-byte decoder `*(u64*)01F83530 + uint32(ECX)`. It has no null
preservation special case, and `root+DA8` is dereferenced unchecked. The
[coast-down contract](../CONTRACT-coast-down-latch.md#7a-the-fourth-stage--added-2026-09-11)
supplied this decoder and lookup as oracles. Their actual semantics can now be
propagated without claiming that the former differential suite executed them.

## 3. Selection policy includes a third argument

The complete 459-byte `004235C0` takes `render`, a candidate event in EDX, and a
selector in R8D. It reads the current event from signed word `render+CC`. Describing
it as a comparison of two event values loses the caller's selector.

First it resolves entry `render+C4` as above; a missing entry returns 1. With an
entry present, both candidate and current event are normalized for classification:

| Event's bits 12–15 | Normalized value |
|---:|---|
| 3 | `0x2036` |
| 4 | `0x2036` if low 12 bits are `0x36`, otherwise `0x2035` |
| 5 | `0x203E` |
| Others | Original value |

The later rejection paths require both normalized event kinds to be 1 or 2. A kind-1
event continues only when render `+284` bit 31 is set; a kind-2 event continues only
when bit 28 is clear. Other kinds or the opposite flags return 1. The special pair
whose original current low 12 bits and normalized candidate low 12 bits both equal
`0x3D` also returns 1.

Only after those gates does the selector matter:

| Selector | Remaining decision |
|---:|---|
| 0 | Return 1 if current priority <= candidate priority; otherwise return `00424230(render)` |
| 1 | Return 1 |
| 2 | Return whether current priority <= candidate priority |
| Other | Return 1 |

Priorities are bytes at `01F00410 + (normalized_event & 0xFFF)`, compared with signed
byte branch conditions. The [captured 64-byte window](../../_experiments/evidence/render-event-selection/priority.json)
has priority 0 for event low index 1 and priority 1 for index 5. It is a bounded
window, not proof of the declared table extent or admission of every 12-bit index.

Original-code controls with current `0x2005`, candidate `0x2001` and both flag gates
continuing show selector 2 rejects. Selector 0 rejects with entry bit 12 clear and
accepts when it is set. Selectors 1 and `0x2005` accept. Reversing the events makes
selector 2 accept. These controls execute the actual entry lookup and bit reader;
the latter is not a Boolean stub.

## 4. The getter's predicate cannot reject under stable valid state

`0041FCA0` structurally returns signed `+CC` when `+C8 == -1` or the predicate
returns zero, and signed `+CE` otherwise. But its actual call is:

`004235C0(render, sign16(render+CE), sign16(render+CC))`.

Under stable, valid and nonoverlapping records, this predicate returns **1** if its
dependency reads complete. The proof is a caller/callee constraint, not a guess
from the helper's name:

- Rejection requires selector 0 or 2, so the getter's current `+CC` must be 0 or 2.
- Both values have normalized event kind 0, which returns 1 before the selector's
  rejection paths.
- For every other `+CC`, selector 1 or the default branch returns 1 if earlier
  permissive gates did not already return it.

Thus the getter returns signed `+CC` when `+C8 == -1`, and signed `+CE` otherwise,
subject to those preconditions. Its predicate call still matters for dependency
reads, cache refresh and faults; this is not permission to remove it from a faithful
effect model.

Controls cover current `0, 1, 2, 0x1001, 0x2001, 0x2037, 0x8000, 0xFFFF` and a
missing entry. Every present-alternate getter selects `+CE`. The strongest paired
control uses current `0x2005` and alternate `0x2001`: the getter selects `0x2001`,
while direct selector 2 rejects the same event pair. No getter case reaches either
priority-table branch. `+C8 == -1` selects `+CC` as the opposite control.

The other direct callers demonstrate why the general helper still needs its full
policy. Complete `00424550` (799 bytes) calls with candidate `0x2005`, selector 0
at `00424829`, then changes entry `+C` bit `0x20000000` based on the result.
Complete `00424D80` (1,607 bytes) first uses a caller-supplied selector at `00424E0C`;
later it temporarily replaces render `+CC` with `0x2005`, calls with selector 2 at
`00424E6E`, and restores the old word at `00424E8B`. Those callers were read,
not executed; their other resource/native effects are not established here. *(2026-09-30, OPUS owner read: since established - UQ-194's record lists both callers' complete store and call censuses, box in §5.)*

## 5. Validation and remaining work

The bounded run and seven additional caller-policy controls produced 31 valid
returns with original code and ABI preserved, plus one separately expected invalid
null-table fault. Eight shipping bodies executed without stubs. Independent review
replayed 317 non-stack reads and four cache writes and checked all final observed
bytes. Deleting a cache write from a private receipt was rejected despite preserving
return and ABI flags. Raw files and hashes are sealed in the evidence package.

- [x] **UQ-192.** Peer consumption into capability policy, battle-unit event field, render-record
      prose, coast-down contract and affected executable consumers/types.
      *NOT A QUESTION 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-2 ruling: the work is carried by the board task `FABLE-CARRIER-PAGE-OWNERSHIP-AND-PROPAGATION-0926`.*
- [x] Root's concrete table capacity, reset/storage order, ID encoding and refresh
      paths are established statically in §6–8. This does not prove live initialization.
- [x] **UQ-193.** Caller responsibility for preventing stale/out-of-range IDs, resource admission,
      source ownership and other generic-container construction paths.
      ***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static.** *Stale ids:* every caller of the release `0051BA40` resets the record's stored id to -1 (`uq193-release-sites`). *Construction:* the container is built once, by `RenderResourceRoot_InitializeSubcontainers` `0041E3A0` through `0051B9D0` (64 slots at `+0x30`); there is no other path. *Admission:* `0051BA80` is the only admission and has two callers, `00424550` and `00424D80`, each passing the record's own stored id (`+0xC8` / `+0xC4`) - -1 admits a new slot after the capacity check, a live id rebuilds its slot in place - so no caller can re-admit through a stale id. *Source ownership:* the source both pass is the record's own resource entry (`[record+0x10]`), which the slot refers to and does not own. [Record and control](../../_index/candidates/uq193-container-contract/README.md) (3 checks, FAILS 0).*
- [x] **UQ-194.** Native initialization and scheduling that keep the getter's records stable;
      presentation binding, ownership and all effects of the two event-entry callers.
      *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: the four fields start at -1, every reader and writer runs on
      the main thread with no store between the getter's two reads, live ids come only from the admission's return,
      and the two callers' complete store and call censuses are listed - see the register row and
      [the record](../../_index/candidates/uq194-event-entry/README.md).*
- [x] ~~**UQ-195.** Meaning/writers of entry bit 12 and the full priority-table extent and event~~
      vocabulary. The observed predicate behavior does not name those semantics.
      ***ANSWERED 2026-09-17 (FABLE): bit 12 is the entry's completion flag, and the priority table is `0x60` bytes of values 0..4.** *Writers.* Set by `PresentationEmbeddedRecord_UpdateCurrentState` (`0041DA90`) in the arm that writes state 2 into the embedded record's word `+4` and calls `0041E000(entry, record, -1)` and `0041C6C0(entry)` (`0041DC34`..`0041DC60`; again at `0041DCD3` when the record already holds state 2), and by `00423F20`, which substitutes its argument for the current event in `render+CC`, sets the bit, calls `0041CEC0(entry)`, then clears the bit and restores the event (`00423F64`..`00423FA0`): a forced selection. Cleared by `00417810` when it starts a new event (state 1 into the record's `+4`, bit 1 of `+8`, a time ratio into `+0x1C`; `004178E6`), by `00423230` on the entry of `render+C4` (a cancel), and by `0041C410` when entry `+C` bit 3 and bit 12 are both set, after `0041CFC0(entry)`, together with `+C` bit 9 (`0041C537`..`0041C54A`). Its readers are `0041C760` (the permissive default: a lower-priority candidate is accepted once the current event has completed), `0041C410` and `PresentationEntry_RebuildAndFastForwardToTime` (`0041D820`, twice). *The table.* `01F00410` holds priority bytes for indices 0..`0x58` (values 0..4, 36 non-zero: 3s and 4s in the first sixteen, a 2 at `0x17`, then 2s and 3s from `0x3F` to `0x58`); bytes `0x59`..`0x5F` are zero, unrelated 16-byte constants follow from `01F00460`, and the next referenced symbol is `01F004A0` (`BattleAction_FindApproachGeometryAroundTarget`). The three readers index it by the low 12 bits (`004235C0`, `00423790`, mask `0xFFF`) or by a byte (`00422DE0`, signed), so an authored index above `0x5F` would read those constants as a priority; the vocabulary the table serves is at most 89 indices, and after the kind normalisation (3, 4, 5 folded to `0x2035`/`0x2036`/`0x203E`) the selector compares kinds 1 and 2 over them. Static; the captured 64-byte window agrees with bytes 0..`0x3F`.*

## 6. The render root constructs 64 reference slots

**ASTRA, 2026-09-12, Method A.** The [lifetime evidence package](../../_experiments/evidence/presentation-entry-lifetime/README.md)
contains 22 complete original bodies, with exact reference/body identity and explicit
unread dependencies. No new execution is claimed for this package.

`0041E3A0` assigns `root+DA8 = root+160`. It calls `0051BA20` on that container at
`0041E42F`, then later calls `0051B9D0` at `0041E470`. The former runs global reset
`0041CCA0`, then `0051F2D0`; the latter overwrites EDX with **`0x40`**, takes table
pointer `container+30`, and tail-calls `0051F170`. The caller's supplied count does
not control this table. Its 64 slots occupy `root+190..root+D8F`, immediately before
the root's `+D90` subcontainer pointers. This is distinct from the 160 render records.

`0051F2D0` sets head/tail `+1C/+20` to -1, clears `+0`, pointer `+8`, capacity/count
`+10/+14`, and search cursor `+18`. It does not initialize container flags `+4`.
`0051F170` then sets low flag bits to kind 1 while retaining upper bits, writes the
table pointer/capacity and clears `+0/+14`. It does **not** initialize cursor/head/
tail itself. Calling storage initialization alone on arbitrary bytes therefore does
not reproduce the root's reset-then-storage sequence.

`0051F2F0` clears node dword `+0`, sets dwords `+4/+8/+C` to -1, and clears qwords
`+10/+18/+20`, over the signed positive capacity. It leaves each node's `+28..+2F`
untouched. It does not allocate or replace table storage. `0041CCA0` separately
zeros two global `0x258`-byte spans at `02CA4410` and `02CA4670`; their wider role
is not inferred from this reset.

| Container offset | Established role |
|---:|---|
| `+4` low two bits | Table source kind; concrete root uses 1 |
| `+8` | Full table/source pointer |
| `+10` | Signed capacity in these loops/checks; concrete root is 64 |
| `+14` | Occupied count |
| `+18` | Next candidate slot cursor |
| `+1C`, `+20` | Full ID of active-list head/tail, -1 empty |

| `0x30`-byte node offset | Established role |
|---:|---|
| `+0` | Nonzero occupied state; bit 0 set on admission, bit 1 requests lookup refresh |
| `+4` | Full ID |
| `+8`, `+C` | Previous/next active-list IDs, -1 ends |
| `+10` | Full payload source passed to `003AB7F0` |
| `+18` | Cached resolved payload pointer |
| `+20` | 32-bit source offset; reset also clears `+24..+27` |

## 7. IDs carry a fixed tag; release does not validate a generation

`0051F150` returns -10 when signed count >= capacity, otherwise the candidate cursor.
`0051F410` performs the admission accounting: rejects a full table, saves the current
cursor as the chosen slot, increments count, and finds the next node whose entire
dword `+0` is zero by advancing/wrapping the cursor. When the table becomes full it
sets the cursor to zero directly. These steps depend on consistent count/cursor/node
state; there is no separate scan bound for a corrupted table with no free node.

`0051F080` sets node occupied bit 0 and optionally refresh bit 1 from incoming R9 bit 1.
It assigns **`slot | 0x10000`** to node `+4` (`0051F0FF bts esi,0x10`), stores source
and offset, computes the initial cached pointer with the same signed 32-bit addition
as lookup, and appends the node using `0051F380`. The high bit is fixed: this path
does not increment a generation on reuse. The same valid slot receives the same ID.
This conclusion is from the complete original builder, not a simulation of invented IDs.

`0051F380` stores full IDs in head/tail and previous/next links, but indexes nodes by
low 16 bits. `0051F4C0` unlinks neighbors by low 16 bits too; only the head/tail
comparisons use the caller's complete ID. It never compares that ID to node `+4`
before touching neighbors. `0051F190` then clears node `+0..+27` to the same reset
values, decrements count unconditionally and sets the candidate cursor to zero if
the count becomes zero. It does not free the payload or validate occupancy/ID.

Consequently, a wrong high half is not made safe by full-ID head/tail comparisons:
neighbor accesses still select the low-half slot, and endpoint updates can be skipped.
Double/stale release and arbitrary out-of-range IDs are outside the established valid
preconditions. This is a local contract, not evidence those calls occur in gameplay.

The wrapper `0051BA40` first uses the mutable lookup, and if non-null reads the
payload's own first dword as the ID. It calls `0041CF00(payload)` before releasing
that ID through `0051F190`. There is no comparison with the original caller ID.
A stale alias that resolves a new occupant can therefore reach that occupant's
reset/release route under the shown code. Caller ownership and invalidation must
provide any lifetime protection; this package does not establish that they fail.

`0041CF00` resets per-entry `0xA0` subrecords, optionally calls `002ED570` / `00372280`
under entry `+C` bit `0x1000`, clears that bit, then tail-calls `0041CB90`. The latter
and the native cleanup effects are not read here *(2026-09-30, OPUS owner read: since read - `0041CB90` in §9, `00372280` in §10, a per-bone state reset with no allocator or release call)*, so this call order is not proof of
complete resource release.

## 8. Refresh is broader than the lookup's flag branch

`0051BA80` constructs a `0x3A0`-byte presentation payload on its stack through
`0041CB90` and `0041D220`. Those initialization semantics remain open here *(2026-09-30, OPUS owner read: read in §9 - `0041CB90`'s defaults table and `0041D220`'s definition copy)*. For a
new ID it calls `0051F080(container, source, offset, **0**)`, so this admission path
does not set the lookup's refresh bit. On success it resolves the node, copies the
whole `0x3A0` template, calls `0041CA70` to rebuild derived pointers, and writes the
full ID into the payload's first dword. Failed resource initialization resets and
releases an existing resolved entry before returning -1. This is static call/order
evidence, not an executed resource initializer.

Nevertheless, `0051B9F0` first calls `0051F620`, which walks **every active-list node**
and rewrites cached `+18` from source/offset with the same signed 32-bit arithmetic,
without testing the node refresh bit. It then calls `0051F580` with callback
`0051BC00 -> 0041CA70` to repair derived payload pointers. Cached-pointer width is
therefore constrained by admission and explicit rebase too, not only lookup refresh.

`0051F580` reads cached `+18`, calls the callback, and **reads next ID `+C` after the
callback returns**. It does not save the next ID before the call. Effects of callbacks
that mutate/release this list cannot be assumed safe from a generic iterator model.

`0041CA70` always publishes `payload+18 = payload+30 + 0xA0 * sign32(payload+20)`.
Its other branches rebuild full pointers at `+368/+370` and in `0xA0` subrecords
through resource helpers, subject to entry flag `+C & 0x20`, resource ID and subrecord
type/count checks. Those helper semantics remain outside this package. Container
node `+18` and payload `+18` are different pointers with different arithmetic; do
not merge them into one field merely because the offsets match.

Remaining architectural questions are the admitted source/resource lifecycle, who
invalidates external IDs before release/reuse, full resource-initializer and cleanup
effects, and native scheduling of rebases/callbacks. Peer propagation of these
bounded initializer/ID facts is pending; they do not close the whole rendering system.

## 9. Payload defaults and resource admission — original instructions

**Method A, 2026-09-12.** The [payload evidence package](../../_experiments/evidence/presentation-payload-admission/README.md)
retains 19 complete newly read bodies, the exact image constants and the previously
read `0041CA70` / `0041CF00` context. No new execution or live observation is claimed.
This narrows the initializer/cleanup gap above; native ownership and scheduling remain open. *(2026-09-30, OPUS owner read: answered in the register - construction, admission and stale ids by UQ-193, and scheduling by UQ-194: every reader and writer runs on the main thread; §5's boxes.)*

`0041CB90` is a 269-byte selected-field reset, with no calls. It does not clear the
whole `0x3A0` payload or its four embedded records. Its exact nonzero defaults are:

| Offset | Width | Reset value |
|---|---|---|
| `00`, `04`, `08`, `324`, `338`, `35C`, `360` | dword | `FFFFFFFF` |
| `318`, `2D8` | word | `FFFF` |
| `2DC` | byte | `FF` |
| `344`, `348`, `34C` | dword | float bits `BF800000` (-1.0) |
| `358` | dword | `10` |
| `340` | dword | binary32 product of current float at `01DFE0BC` and 30.0 at `008F8D80` |

Zero stores are qwords at `18`, `20`, `2B0`, `2C0`, `2C8`, `2D0`, `2E0`, `310`,
`330`, `350`, `368`, `388`; dwords at `0C`, `2B8`, `31A`, `320`, `328`, `33C`;
and words at `28`, `2A`, `2BC`. These are physical store extents, not a declaration
that every store defines one semantic field. The dword at `31A` spans two later
word destinations. The reset **ANDs dword `2E8` with `FFFFFFF8`**, preserving its
other bits, and does not write `370`, `378` or `37C`. The image's initial `01DFE0BC`
bytes encode 1.0; this does not establish the current runtime value at every reset.

`0041D220(payload, definition)` reads a separate descriptor through RDX. It first
ORs payload flags `+C` with `00100001`, then copies these inputs in the shown
instruction sequence (the table follows the stores rather than sorting offsets):

| Definition input | Payload destination | Width |
|---|---|---|
| `+20` | `+31C` | word |
| `+18` string pointer | `+2EC..+30B` name key | 32 bytes through `00409210` |
| `+08` | `+330` | qword |
| `+14` | `+338` | dword |
| `+00` | `+310` | qword |
| `+10` | `+318` | word |
| `+28` | `+2B0` | qword |
| `+30` | `+2B8` | dword |
| `+24` | `+31A` | word |
| `+34` | `+2BE` | word |
| `+38` | `+364` | dword |

It also sets byte `+2DC=FF`, word `+2BC=0` and word `+32A=0`. The descriptor's
pointer fields are copied; this body does not allocate or establish their ownership.
The complete name helper zeroes four qwords, calls imported `strncpy(dst, name, 32)`
and forces byte `+1F=0`. It has no null-name guard. The search wrapper separately
skips normalization for a null wildcard name; the descriptor initializer calls
the normalizer directly. Native CRT effects were not executed here.

Resource wrapper `00409F50(table, wordId)` returns null for `FFFF`; otherwise it
**sign-extends the word** and tail-calls `002ED570`. Thus a word above `7FFF`
does not become a positive 32-bit table index. That table operation can refresh
both cached source pointers through `003AB7F0`, reads the bank token and decodes
it before checking the slot's `-1` key, and has no local capacity check. The bank
index is an arithmetic signed-dword shift of the input, with the shift count read
as a dword at descriptor `+4C` and masked by the machine to its low five bits;
bank-directory stride is `20`. Its final
row offset is `sign32(u32((index & mask) * stride))`, added to the full decoded
bank base. A null slot key does not protect earlier bank accesses.

The initializer obtains the resource entry from descriptor `+00/+10`. It searches
the normalized name for `@FMC` (`434D4640`), falling back to `@FRP` (`50524640`)
only when the first offset is `-1`, and stores the result at payload `+320`.
It sets `+378/+37C=-1` before querying `@FRM` (`4D524640`). If that pointer is
nonnull and its dword `+8` is unsigned greater than `30`, it finds the same
section's offset, stores `offset+30` at `+378`, and adds the section's dword
`+38` into `+37C` only when that dword is nonzero. The retained section pointer
is itself narrowed by `MOVSXD RBX,EAX` at `0041D34C` before the `+38` read.

Then it calls the original derived-pointer rebuild `0041CA70`, calls
`0046E420(payload[330], payload[338])`, and **only afterwards** tests whether
payload `+368` is null. Null returns EAX zero. This is not transactional failure:
the preceding payload writes, lookups and linked-resource refresh have already
occurred. No rollback appears on this branch.

### Successful local path and its additional preconditions

For nonnull `+368`, it writes count word `+28=4`, calls imported memset to clear
`payload+30` for `280` bytes, and initializes four `A0` subrecords. Each receives
the reset pattern visible in the complete body, including `+00=-1`, `+18=001E0000`,
`+20=41F00000` (30.0), word `+50/+52=FFFF`, dword `+68=-1`, and dword `+94=FF`.
These offsets are relative to a subrecord, not to the payload.

It invokes `0041CD30(payload, payload+30, 0)` for authored stream zero. This helper
checks the stream index against resource `+C`, traverses prior streams by their
word `+4` size, and records stream-relative offsets in the subrecord. It selects
the active subrecord when the stream's first byte is 1 or the resource has one
stream, updating payload `+18/+20` and subrecord `+96` bit 0 / byte `+95`.
The record loop uses word command size shifted right by six and byte command count;
first word `FFFF` marks the selected special-command offset at `+90`. Traversal
adds in 32 bits and sign-extends the new pointer. No allocation occurs in this helper.

Afterward `+338 != -1` causes a fresh `002ED570` lookup of the model-group entry.
Whether skipped or returned null, **there is no null guard before the group `+94`
read at `0041D449` and word `+A4` store at `0041D454`**. The earlier `+368` test
therefore does not establish all inputs needed for a successful return. This is
an instruction-level precondition, not evidence that normal gameplay violates it.

The group word `+A4` starts at 25. If its decoded `+94` token is nonnull and
payload `+378 != -1`, the initializer forms
`sign32(low32(payload[370]) + payload[378])`, uses section byte `+2 & 3F` for
that group word, and byte `+1` as the mode argument. Without this section it
retains mode 4. It decodes group `+94` again and calls `003E18D0`, then returns 1.
Actual native dependency failures are not represented by a simple zero/one oracle.

## 10. Concrete cleanup and linked-resource effects

The prior `0041CF00` reset's optional `+C & 1000` path calls `00372280` after
resolving the group. **`00372280` is a 194-byte per-bone state reset, not a free.**
Its only two calls are to the original compressed-pointer decoder `0020E600`.
Both decode group `+84`; one supplies the bone base, the other supplies the list
base after adding `0x290 * sign16(group[88])`. It visits signed word indices from
that list for the signed positive count at group `+8A`, rereading the count at
the loop tail. For each selected `0x290` bone record it performs, in order:

1. Clear bit `10` in word `+280`.
2. Zero qword `+1A4`, then dword `+1A0`; write float 1.0 at `+1AC`.
3. Zero qword `+1C4`, then dword `+1C0`; write float 1.0 at `+1CC`.

No allocator or release callback appears in this complete body, and its decoder
callees have no memory writes. These stores define two selected four-component vectors,
not whole-bone clearing or release of the backing allocation. The meanings of
those channels require their consumers; the stride alone does not identify them.

The caller's flag `1000` also requires a valid group selection: when its group ID
is `-1`, `0041CF00` skips resolution but still calls `00372280` with the zero RCX
established earlier in that function. The callee reads `[rcx+84]` immediately.
There is no safe null-group return at that boundary. The later flag clear and
base reset occur only after this call returns. Valid construction/flag writers
and native caller reachability remain to be established. *(Established 2026-09-30, OPUS, [`opus-render-null-group-0930`](../../_index/candidates/opus-render-null-group-0930/README.md) N1-N5: the only setter of bit `1000` is `0041D4D0`, called only by `00424550` right after an admission that stores a group id checked not to be -1, and the one -1 store, `0041CB90`, runs before that store or after the bit is cleared - so the zero-`RCX` call is not reached.)*

The initializer's earlier `0046E420` refresh has actual state effects too. It
resolves its group unless ID is `-1`, runs `003713C0`, optionally refreshes the
related group named by `+8`, and writes its encoded pointer at group `+C`.
A second relation at `+10` can invoke `00372F60`: that complete body walks the
first group's signed index list and stores an encoded pointer at bone `+278`
for a non-FFFF signed bone index at `+27C` into the second group's `0x290` array.
It leaves `+278` unchanged on the FFFF branch. This is pointer rebinding, not
ownership transfer or allocation.

`003713C0` refreshes group `+84`, `+A0` and conditional `+94` compressed pointers,
and can call `003E1C50` on the resolved animation state. `003E18D0` selects a mode
using global `02B59D64` and current byte `+1A`, calls `0040B5D0`, and writes word
`+60=30` when that callee reports a change. The complete `0040B5D0` updates group
activation bytes and bone flag bytes `+28A/+28B`, calls `0040ED90` for selected
groups and finally writes the new mode byte. `003E1C50` and `0040ED90` effects
remain outside this package; reading their callers is not proof of those effects.

## 11. Resource pointer arithmetic needs explicit widths

The complete `004096C0` returns null for null entry or offset `-1`. Otherwise it
calls `00409600`, performs **`ADD EAX,EBX; CDQE`**, and returns the sign-extended
32-bit sum. `00409660` similarly uses `ADD EAX,[offset]; MOVSXD RBX,EAX` after
its successful find. A full-width base read does not survive these operations.
Also, `004096C0` does not check the returned base: a nonnull entry of unsupported
mode gives base zero, but a positive supplied offset can still produce a nonnull
return. The base getter's own null result is not a general fail-closed lookup.

The child-container selector `004090D0` has a different boundary. Null returns
null; non-`@FRP` returns the original full-width input pointer. For `@FRP`, version
0 child addresses use 32-bit additions and return through EAX (zero extension).
An out-of-range index falls back to the first offset at `+30`. Version 1 optionally
linearizes a row/column index and **reads the offset table before checking the
final index against count**. Zero table entry returns null; an admitted entry
again returns a zero-extended 32-bit sum. Unsupported version returns null.
Neither sign-extension nor bounds behavior should be generalized across helpers.

These formulas refine the unrestricted `base + offset` notation in the resource
addressing page and the pointer assumptions feeding this initializer. Corrections
are routed to the semantic and structured-record owners; closure remains pending
their agreement. The initialized live address domain, source ownership, external
ID invalidation, cleanup-flag producers and remaining native animation callbacks
remain architectural questions. No original-game process was accessed for this package.

## The `02CA4410`/`02CA4670` handler arrays, and who fills them — 2026-09-14 (NOCALLER-INSTALLERS)

§6 noted that `0041CCA0` zeroes the two `0x258`-byte spans at `02CA4410` and `02CA4670`. They are
**75-slot handler-pointer arrays**: `0041D6C0(id, fn)` stores `fn` at `02CA4410 + id*8` and
`0041D6D0(id, fn)` at `02CA4670 + id*8`; `0041D6E0` stores a single pointer at `02CA4668`.
`CharacterRenderSystem_Initialize` (`004269A0`) first walks the `022C6F28` manager array
(`0xA0` records at `0x740` bytes each, `0041F730` per record), stores a context pointer via
`0041D6E0`, then registers **25 command handlers** — every `0052xxxx` body below has no direct
caller; each is reached only by its array slot.

**How a slot becomes a call.** `.data` `01EFFAF0` is a pair table of 16-byte records
`{invoker, dword flag}`; the command id is `word[record] & 0x7F` clamped to `0x4B`
(`0041DB1D`–`0041DB4B`), so the table covers all 75 ids. Three stream drains —
`0041DA90` `PresentationEmbeddedRecord_UpdateCurrentState`, `0041E000`
`PresentationEmbeddedRecord_ExecuteCommandStreamUntilThreshold`, and `0041E1D0`
`PresentationEmbeddedRecord_ExecuteDeferredCommandSubset` — walk command records at
`[arg2+0x368] + [arg1+0x90]` + 4 (`0041DABC`, `0041DAD3`–`0041DAF6`) and
`call qword [01EFFAF0 + id*16]` (`0041DB66`) with `rcx` = the command record, `rdx` = arg1,
`r8` = arg2. A nonzero pair-table flag byte at `+8` suppresses the call on the record-flags
`0x10|0x14` path (`0041DB13`–`0041DB3D`); 33 ids with no generated invoker point at `0016D6A0`,
the shared `ret 0` (`CCCCCCCCCC0000C2` at `0016D6A0`), so those unregistered commands are
no-ops — but the top three slots `0x49`–`0x4B` are **NULL** (a record carrying one would
`call 0`; the producers presumably never emit them).

Most live ids use generated 0x20-byte invokers in `004174F0`+, each embedding its bank slot —
`00417530` (id `0x13`) is representative (`00417530`–`00417546`):

    mov rax, [rip+0x288cf71]   ; 02CA44A8 = bank-A[0x13]
    test rax, rax ; je ret
    mov rdx, rcx               ; arg2 <- command record
    mov rcx, [r8+0x2E0]        ; arg1 <- the stream's render record
    jmp rax

so every handler runs as `handler(render_record, command_record)` — `[arg2+0x2E0]` is the
character render record the stream targets, which is why handlers write the record's
`+0x290`/`+0x294` dirty words directly, and read the command payload at `+2` onward (subtype
at `+2`/`+3`, parameters from `+4`). A few ids carry bespoke invokers instead: `00417AD0`
(id 4) switches on `byte[record+2]` across 12 cases (`00417B02`–`00417B08`) before calling
`bank-A[4]`; `00417C60` (id 5) reads bank-B slot `02CA4698`; `00417DE0` (id `0x2C`) makes **no
calls at all** — it interprets record fields itself and writes `+0x358`/`+0x35A`/`+0xC`
directly (its sole rip ref is the float const at `01CEBBA8`).

| id | address | role | interior |
|---:|---|---|---|
| 5 | `00520C50` | array **B** (`02CA4670[5]`): calls `0046CBA0` | `00520C6F` |
| 0x11 | `00520160` | 23 B — touches `+0x3D0` | `00520160` |
| 0x12 | `005207C0` | `003E6DA0` + `003E29F0` pair | `005207C9` |
| 0x13 | `00520430` | flag work on `+0x290`/`+0x3F4`–`+0x3F6`; `00429500`,`004288B0`,`0042B580` | `00520482` |
| 0x14 | `00520E70` | tail into `0042DC10` region | `00520E70` |
| 0x15 | `00520740` | 58 B — touches `+0x3D1` | `00520740` |
| 0x16 | `00520BD0` | `0042B550`; flag pair `+0x3D2`/`+0x3D3`, `+0x3F8` | `00520BF8` |
| 0x18 | `00520C80` | `00421E20` + `003B0C50`; `+0x60`/`+0x90` fields | `00520C8A` |
| 0x19 | `00520CE0` | 32 B — calls `0046CC70` | `00520CF4` |
| 0x1A | `00520C10` | `00422D50` + `003E6340`; `+0x30`/`+0x370` | `00520C20` |
| 0x1D | `00520D30` | `003E55B0`,`00477610`,`00428B30`,`003E7450`; `+0x413`/`+0x4B7` flags | `00520D60` |
| 0x1E | `00520DF0` | 50 B — `003E6A20`; `+0x413` | `00520E16` |
| 0x1F | `00520140` | 23 B — tail-calls `003E6710` | `0052014B` |
| 0x20 | `005207A0` | 23 B — touches `+0x2F4` | `005207A0` |
| 0x21 | `00520780` | 23 B — touches `+0x2F6` | `00520780` |
| 0x23 | `00520180` | 47 B — calls `004293C0`; `+0x20`/`+0x40` | `005201A3` |
| 0x24 | `005201B0` | id→record lookups `0020E600`×3 + `002ED570`, interior `jmp` loop-head `005201DD`→`005201F0` | `005201D1` |
| 0x25 | `00520320` | same `0020E600`/`002ED570` lookup family, interior `jmp` loop-head `0052034D`→`00520360` | `00520341` |
| 0x28 | `00520720` | 22 B — tail-calls `003E6AA0` | `00520727` |
| 0x29 | `00520D00` | 37 B — calls `0046CC70` | `00520D16` |
| 0x2A | `005206B0` | `003E7140` then CFG-guard `00808C40` | `005206B4` |
| 0x2F | `00520E30` | `0042EF90`; `+0x20`/`+0x28`/`+0x1AF` | `00520E4A` |
| 0x34 | `00520800` | the big one (811 B): `003AFD30`/`003B6930`/`003AFC10`; `+0x1C`–`+0x28` state | `0052081A` |
| 0x3F | `00520510` | 147 B — calls `00426870` | `00520570` |
| 0x48 | `005205B0` | `0020E600`/`002ED570` lookups + `00372800`/`00426870`; interior `jmp` loop-head `005205F2`→`005205F9` | `005205D5` |

`002EA320` — the boot-time request-ring seeder that fills the `0215FDxx`/`02161Dxx` cells —
registers five more array-A handlers in the same `0041D6C0` id space: **id 4 → `002E70C0`,
id 5 → `0016D6A0` (the shared bare `ret` — an explicit empty handler), id 6 → `002E7090`,
id 0xC → `002E70A0`, id 0x26 → `002E7080`**, and two into the separate `022D7FD0` record array
(`0036C5A0(id≤0xE, fn)` writes `fn` at `record + id*0xA8 + 0xA0`): **id 6 → `002E6D60`,
id 0xA → `002E6D60`**. `002E70C0`/`002E7090`/`002E70A0` share the `test …/jz` head that gates on a
state flag; `002E6D60` is their larger sibling.

## Falsification pass 1 — 2026-09-13 (OPUS) — peer consumption of §§6–7

The frontmatter read `primary-evidence-package-awaiting-peer-consumption`. **This is that
consumption.** §§6–7 were taken because they are the parts a reconstruction implements directly: the
64-slot table, the container and node fences, and the ID-tag/release chain.

The package cites an instruction address for nearly every claim, which is the shape that can be
checked one for one. **Every cited address landed on the instruction it names.**

| claim | measured |
|---|---|
| `0041E3A0` assigns `root+DA8 = root+160` | `0041E3FD lea rax, [rsi+0x160]` / `0041E404 mov [rsi+0xda8], rax` |
| it calls `0051BA20` at **`0041E42F`** and `0051B9D0` at **`0041E470`** | both **at exactly those addresses** |
| `0051B9D0` overwrites EDX with `0x40`, takes `container+30`, tail-calls `0051F170` | `lea r8, [rcx+0x30]` / `mov edx, 0x40` / `jmp 0x51f170` — fourteen bytes, all three |
| the 64 slots occupy `root+190..root+D8F`, immediately before `+D90` | **64 × 0x30 = 0xC00**, and `0x190 + 0xC00 = 0xD90` — the span closes on the next field exactly |
| `0051F2D0` sets `+1C`/`+20` to −1, clears `+0`, `+8`, `+10`/`+14`, `+18`, and does **not** touch `+4` | all six, and **no write to `+4`** |
| `0051F170` sets the low flag bits to kind 1 retaining the upper, writes table pointer and capacity, clears `+0`/`+14`, and does **not** touch cursor/head/tail | `and [rcx+4], 0xfffffffd` / `or [rcx+4], 1` / `mov [rcx+0x10], edx` / `mov [rcx+8], r8` / `mov [rcx], eax` / `mov [rcx+0x14], eax` — and nothing at `+18`/`+1C`/`+20` |
| `0051F150` returns **−10** when signed count ≥ capacity | `mov eax, 0xfffffff6` — which is −10 — behind `cmp [rcx+0x14], eax` / `jge` |
| `0051F080` assigns `slot \| 0x10000` at **`0051F0FF bts esi, 0x10`** | **at exactly that address** |
| `0041CCA0` zeros two spans at `02CA4410` and `02CA4670` | both `lea` targets exact |

### Three things the instructions add to the prose

**`0051F170` *ends* in `jmp 0051F2F0`.** § describes the storage init and the node init as successive
steps; they are one call. The node reset is not optional and cannot be skipped by a caller that
stops early — which strengthens §'s point that *storage initialisation alone on arbitrary bytes does
not reproduce the root's sequence*, because the two halves that **are** reached together are exactly
these.

**`0051F2D0`'s stores are qwords, and that is why the fields move in pairs.** `mov qword [rcx+0x1c],
−1` covers `+1C` **and** `+20`; `mov qword [rcx+0x10], rax` covers `+10` **and** `+14`; `mov qword
[rcx+8], rax` covers `+8` **and** `+0C`. §'s field list is right, and the widths explain why head and
tail, and capacity and count, are always written together — a reconstruction writing them as separate
dwords would be correct in effect and wrong in shape.

**The low-16-bit indexing has a stride, and the stride is what makes the hazard a hazard.** § says
`0051F380` and `0051F4C0` "index nodes by low 16 bits". The instructions show how:

```asm
0051F3DC  movzx eax, ax            ; the id, truncated to 16 bits
0051F3DF  movzx ecx, di
0051F3E2  lea   r8, [rax + rax*2]  ; x 3
0051F3E6  add   r8, r8             ; x 6
0051F3F0  mov   eax, [r9 + r8*8 + 4]   ; x 48 = the 0x30 node stride
```

`(id & 0xFFFF) × 0x30`, and `0051F190` does the same (`movzx ecx, si` / `lea rbx, [rcx+rcx*2]` /
`add rbx, [rdi+8]`). **So a wrong high half does not produce an out-of-range address — it produces a
perfectly valid pointer to the wrong-but-real node.** That is precisely why § is right that "a wrong
high half is not made safe by full-ID head/tail comparisons": the failure is silent by construction,
not by oversight. The neighbour writes confirm the other half — `mov [r9 + r8*8 + 0xc], edi` stores
the **full** id into a link while the index that found it was truncated.

**Not claimed:** nothing here was executed or observed live, and this pass adds no execution to a
package that claims none. §§1–5 and §§8–11 were not re-derived; `0041CB90` and the native cleanup
effects remain unread *(2026-09-30, OPUS owner read: as of that pass; both are read since, in §9 and §10)*, so §7's own caveat that the call order "is not proof of complete resource
release" stands untouched.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — CLIENT (9 edges through 2 of this page's functions).** The Audio layer reaches this page at `0046CC70`, `00421E20`. `FUN_00332c40` is the worked example, read in full - it is an 857-byte step that demands bit 2 of `byte[+9]`, takes `word[+4]` as an index and skips the `0xFFFF` sentinel - and it indexes **the same `0x740`-byte records at `[022C6F28]`** the heading-speed step walks, testing their `dword[+0x284]`; **2 of the 9 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT (1 edges, one fan-in).** All 1 edges are Party bodies reaching `0046CC70` on this page. `PartyFocus_GetCurrentPackedActorHandle` is the worked example - it is a seven-byte getter returning the packed handle at `022C7FE0`. The crossing is **one shared subject with 1 callers on that layer**, not 1 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 18 edges).** All 18 edges are the
image-pointer fixup pair — `0020E600` `ImageAddress_ResolveRuntimePointer` (13) and `0020E620`
`RuntimePointer_EncodeImageAddress` (5) — inside this page's evidence-walk bodies
(`002ED570`/`003713C0`/`00372280`/`00372F60`/`003E18D0`/`003E1C50`/`00424D80`/`0046E420`). Runtime
relocation infrastructure, not a scheduling relationship.
- **Movement - CLIENT (2 edges).** `004288B0`, PresentationEntryReferenceContainer_ResolveEntryById (`0051B9E0`) are called by bodies filed to Movement: `002E3110`, Movement_ModifyHeadingSpeedForObjectState (`00424080`) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (56 edges).** ResourceTable_ResolveEntryByIndex (`002ED570`), `003AB7F0`, `004090D0`, `00409210` (+3 more) are called by bodies filed to Resource: ResourceTable_ResolveEntryByIndex (`002ED570`), `00408F80`, ResourceEntry_GetResolvedBasePointer (`00409600`), ResourceEntry_FindSectionPointerByTagAndName (`00409660`) (+17 more); `003713C0`, CharacterRenderRecord_ResolveModelInstance (`003E55B0`), `003E6DA0`, ResourceEntry_FindSectionPointerByTagAndName (`00409660`) (+13 more) reach bodies filed to Resource: ResourceTable_ResolveEntryByIndex (`002ED570`), `00408F80`, `00409090`, `004090D0` (+12 more) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `002EA320` is called by bodies filed to World: `00266D10` - shared machinery across the layer boundary, no shared ownership.

