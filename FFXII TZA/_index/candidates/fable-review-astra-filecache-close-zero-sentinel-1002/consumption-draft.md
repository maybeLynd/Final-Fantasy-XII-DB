# Consumption draft: four ASTRA filecache packets → FABLE's path-to-bytes page

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

**Status: draft, not applied.** The reviewer prepared it for FABLE. Nothing here edits a page.

**Target page:** [how-a-path-is-resolved-to-bytes.md](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md)
(PrimaryOwner: Resource, FABLE).

**The four reviews.** Each draft sentence below stays inside the scope its review accepted.

| packet | producer | review | verdict | checks |
|---|---|---|---|---|
| `filecache-zero-handle-return` | `5b659b28d` | [REVIEW](../fable-review-astra-filecache-zero-handle-return-1002/REVIEW.md) | ACCEPT-WITH-NARROWING | 52 checks, 52 PASS, 0 FAIL; 11 controls |
| `filecache-open-sentinel` | `446a56af9` | [REVIEW](../fable-review-astra-filecache-open-sentinel-1002/REVIEW.md) | ACCEPT | 32 checks, 32 PASS, 0 FAIL; 8 controls |
| `filecache-read-zero-view` | `4a818c6d3` | [REVIEW](../fable-review-astra-filecache-read-zero-view-1002/REVIEW.md) | ACCEPT | 34 checks, 34 PASS, 0 FAIL; 8 controls |
| `filecache-close-zero-sentinel` | `a30d4772a` | [REVIEW](REVIEW.md) | ACCEPT | 28 checks, 28 PASS, 0 FAIL; 8 controls |

**Existing text this qualifies.** A grep of the page for IsOpen, Close, Read, the three slot addresses, "sentinel"
and "zero view" finds the following:
- **§2 slot table, rows 1 and 5.** These change, as E1 and E2.
- **§2's slot-2 and slot-5 paragraphs.** These change, as E3 and E4.
- **§3's selector-5 sentence.** This is optional, as E5.
- **The falsification row R1** ("false only when `+0x28 == -1`, `+0x30 == 0` and `+0x40 == -1`") is still correct.
  It stays unchanged.
- **The §8 note that IsOpen tests `+0x28`, `+0x30` and `+0x40`** is correct. It stays unchanged.
- **§7a's Input-layer IsOpen caller** stays unchanged. Its consequences are not read here.

**New addresses this draft cites on the page.** Run the neighbour/xlayer pre-check on these before publishing:
- `0020C300`, the only new function entry;
- `0020C1B0`, `001D6D20` and `0059EE90`, at new offsets;
- `00597970`, at a new offset.

The draft deliberately does not cite these by address: the malloc wrapper and thunk, the view constructor, the
unlock, the cookie check, and the Read and Close helpers. The reviews cite them.

---

## E1. §2 table, row 1

OLD:
```
| 1 | `0059BD40` | **Close** - releases the buffer backing, then the second backing, returns true |
```
NEW:
```
| 1 | `0059BD40` | **Close** - releases the buffer if `+0x30` is non-zero, then the `+0x40` backing if it is signed-positive; returns AL 1 on every path; never touches the `+0x28` handle (§5c) |
```

## E2. §2 table, row 5

OLD:
```
| 5 | `0059D4B0` | **Read** - from the buffer, else `ReadFile`, else the second backing |
```
NEW:
```
| 5 | `0059D4B0` | **Read** - from the buffer, else `ReadFile`, else the `+0x40` backing; returns 0, calling nothing, when none applies (§5c) |
```

## E3. §2, the slot-2 paragraph

Only the middle sentence changes. The first sentence and the queue link stay.

OLD:
```
`!(+0x28 == -1 && +0x30 == 0 && +0x40 == -1)` - false in exactly the state the constructor writes,
true as soon as any one of the three backings is bound. That is the test
```
NEW:
```
`!(+0x28 == -1 && +0x30 == 0 && +0x40 == -1)`, comparing all three as full 64-bit values, and it sets only AL
(RAX bits 8-63 are not assigned). It is false in exactly the state the constructor writes, and true as soon as any
one of the three fields leaves its sentinel. *That is weaker than "a backing is bound".* A `+0x40` of 0 is not the
`-1` sentinel, so a stream whose route-1 view failed to allocate counts as open (§5c). That is the test
```

## E4. §2, the slot-5 paragraph

OLD:
```
**Slot 5 is where the three backings show themselves.** It reads from the in-memory buffer if there
is one; otherwise, if its third argument is set and `+0x28` is not `-1`, it calls
**`KERNEL32!ReadFile`** on that handle (resolved from the import directory, not guessed); otherwise
it falls to `+0x40`. So a stream is backed by *a buffer, a Win32 handle, or a package entry*, and
`IsOpen` is the disjunction of the three.
```
NEW:
```
**Slot 5 is where the three backings show themselves.** It tries them in this order:
- **The buffer.** If `+0x30` is non-zero, it reads from the in-memory buffer.
- **A zero-byte request.** Otherwise, if the low 32 bits of its third argument (the byte count) are zero, it
  returns 0 at once.
- **The handle.** Otherwise, if `+0x28` is not `-1`, it calls **`KERNEL32!ReadFile`** on that handle (resolved
  from the import directory, not guessed). It returns the DWORD count that ReadFile wrote into a slot Read zeroed
  first, not ReadFile's BOOL.
- **The `+0x40` backing.** Otherwise it reads from `+0x40`, but only if that value is signed-positive. If it is
  not, Read returns 0 and calls nothing.

So a stream is backed by *a buffer, a Win32 handle, or a package entry*. `IsOpen` tests only that the three fields
are not all at their sentinels, which is weaker than any one of them being a usable backing (§5c).
```

*Reviewer's note, not part of the draft: §2 calls the `+0x40` backing "a package entry", but §8's answered item
says route 1, the RAM cache, stores its source at `+0x40`. E4 keeps the page's existing words. FABLE may want to
reconcile the two names.*

## E5 (optional). §3, the selector-5 sentence

This edit is within the zero-handle review's re-derived arms of `0020C300`. That review shows that on a hit the view
is still allocated for selector 5.

OLD:
```
*Construction is the whole operation.* Resolving with selector 5 takes a branch in §5's lookup that
bumps a counter and stamps the entry rather than delivering bytes - so **a prefetch token is a
resolve-and-mark, not a read**, which is what "handed to the file cache" was standing in for.
```
NEW:
```
*Construction is the whole operation.* On a route-1 hit, selector 5 takes the arm of §5's lookup
that bumps the counters and, when the entry's kind is 1-4, stamps it to 5 (§5c). The small view
onto the cached bytes is still allocated, but the loop closes the stream without ever reading it -
so **a prefetch token is a resolve-and-mark, not a read**, which is what "handed to the file cache"
was standing in for.
```

## E6. New section, inserted after §5b and before "## 6. Route 2"

```
### 5c. A cache hit whose view cannot be allocated (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5), consuming four ASTRA packets at the scope FABLE's independent reviews accepted:
`filecache-zero-handle-return` (`5b659b28d`, [review] (page-relative link: `../../_index/candidates/fable-review-astra-filecache-zero-handle-return-1002/REVIEW.md`),
ACCEPT-WITH-NARROWING, 52 checks), `filecache-open-sentinel` (`446a56af9`,
[review] (page-relative link: `../../_index/candidates/fable-review-astra-filecache-open-sentinel-1002/REVIEW.md`), ACCEPT, 32 checks),
`filecache-read-zero-view` (`4a818c6d3`, [review] (page-relative link: `../../_index/candidates/fable-review-astra-filecache-read-zero-view-1002/REVIEW.md`),
ACCEPT, 34 checks) and `filecache-close-zero-sentinel` (`a30d4772a`,
[review] (page-relative link: `../../_index/candidates/fable-review-astra-filecache-close-zero-sentinel-1002/REVIEW.md`), ACCEPT, 28 checks).*

A route-1 hit does not hand the cached bytes straight to the stream. The lookup first allocates a small view onto
them. **That allocation can fail, and a failed one looks like success everywhere downstream.**

**What a hit does before it allocates.** Having found the entry, `0020C1B0` writes the entry's size through the
caller's size pointer (`0020C1B0` + 0xDC). It then calls `0020C300` (`0020C1B0` + 0xF8), passing the selector and
the entry's kind dword `+0x14`, while still holding its lock. `0020C300` does four things:
- It increments the manager's dword `+0x88` (`0020C300` + 0x28).
- It increments the entry's byte `+0x10`, exactly once on every path.
- It may stamp the entry:
  - selector 5, when the kind is 1-4: kind `+0x14` = 5;
  - otherwise, kind 5 or selector 5: no stamp;
  - otherwise, selector 3: word `+0x0E`;
  - otherwise, selector 1, 2 or 4: word `+0x0C`;
  - any other selector: no stamp.
- Last, it asks the CRT `malloc` for 16 bytes.

If the block is null, `0020C300` returns 0 (`0020C300` + 0x123). It does not construct the view, and it undoes
neither the counters nor the stamp. Otherwise it constructs the view in the block and returns it.

**Zero is not a miss.**
- The lookup returns that 0 past its unlock and the cookie check, and `001D6D20` passes it on.
- The resolver stores it in the stream's `+0x40` (`0059EE90` + 0x15A) and tests only its sign (`0059EE90` + 0x161,
  `js`).
- A -1 sends the name to route 2. A 0 takes the cache-success exit: it copies the size into `+0x20` and returns
  status 0 without touching the archive.
- The reader's constructor ignores that status in any case. It overwrites RAX straight after the call
  (`00597970` + 0x4B) and returns the stream.

**The stream left behind** has `+0x28` = -1, `+0x30` = 0, `+0x40` = 0 and a non-zero size at `+0x20`. The three
slots treat it as follows:

| slot | result on this stream | why |
|---|---|---|
| IsOpen | AL 1, "open" | `+0x40` = 0 is not the `-1` sentinel |
| Read | 0, calling nothing, for any byte count | `+0x30` is 0, `+0x28` is -1, and `+0x40` fails the signed `> 0` test |
| Close | AL 1, calling nothing and writing nothing | `+0x30` is 0 and `+0x40` is not positive; IsOpen still returns AL 1 afterwards |

**Close's "true" never means "now closed".** Close never touches `+0x28`. It zeroes `+0x30`, and it sets `+0x40` to
-1 only when `+0x40` was positive. So the IsOpen after a true Close is false only when `+0x28` was already -1 and
`+0x40` was positive or already -1. In particular, this body never makes a handle-backed stream "closed".

**A reimplementation must keep:**
- the three sentinels exactly (`-1`, `0`, `-1`), compared as full 64-bit values;
- the signed test on `+0x40`, in both Read and Close;
- the AL-only booleans;
- Read's full-zero return, and its stack-count return on the ReadFile path;
- a null view as 0, not -1, so that it is not treated as a miss.

**Premises and limits.** These are static, conditional contracts. They hold only if:
- the manager, tree, entry and stream pointers are valid and the frames are private;
- every callee returns normally under the Win64 ABI, including the lock and unlock, the tree helper, the view
  constructor and the release helpers;
- no opaque callee or concurrent writer touches these fields;
- the cookie check succeeds.

Not established here:
- that natural play ever reaches a failed 16-byte allocation;
- what any caller does after a 0-byte Read;
- whether anything leaks, and what the helpers release;
- the counters as live handle counts, and the entry byte `+0x10` wrapping;
- what the stamps mean;
- every writer, all callers, ownership, lifetime and scheduling.
```

## E7. Key addresses table, one added row (after the `0020C440` / `00674A00` row)

```
| `0020C300` | route 1's view allocation on a hit: counters, entry stamp, a 16-byte `malloc`; 0 on failure | §5c |
```

## E8. Evidence table, one added row (after "Route 1's key, hash and tree")

```
| A failed route-1 view allocation leaves an "open" stream that reads 0 and closes "true" | the four FABLE reviews named in §5c (`0020C300`, `0059D920`, `0059D4B0`, `0059BD40` read whole; sandbox runs of the shipped bytes with stubbed callees) | 1 (static) |
```

---

**Kept open, as in the reviews.** E1–E8 add no claim beyond the reviews' accepted scope. None of them claims a
natural failure, a leak, a read fault, a live import binding or caller behaviour.

**Not routed here.** The packets also name OPUS's stream ABI and resource-readiness contracts as consumers. This
draft touches only FABLE's page. Routing to OPUS is FABLE's call.
