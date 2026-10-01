# UQ-194 — event-entry binding, stability and the two callers' effects

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `uq194_event_entry.py` (10 checks, FAILS 0).

The question is on
[render-event-selection-evidence.md](../../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md)
§5. It asks three things:

1. what native initialisation and scheduling keep the getter's records stable;
2. how presentation entries are bound and owned;
3. every effect of "the two event-entry callers" — the other two direct callers of the policy `004235C0` that §4 names,
   `00424550` and `00424D80`.

## 1. Stability

**Initialisation (U1).** `CharacterRenderRecord_ResetDefaults` (`0041F730`) sets `ebp = -1` (`0041F768`). It stores
that into:
- `+0xC4` and `+0xC8` as dwords (`0041F7A3`, `0041F7B0`);
- `+0xCC` and `+0xCE` as words (`0041F7A9`, `0041F7B6`).

So a fresh record has no bound entry and event −1, and the getter `0041FCA0` returns `+0xCC` through its `+0xC8 == -1`
arm.

**Scheduling (U2).** Nothing reaches these functions from outside the main thread. The walk starts from each of the
eleven thread procedures the image starts, the same list as the F-1 control. None of those walks reaches any of:
- the getter `0041FCA0`;
- the policy `004235C0`;
- the lookup `0051F240`;
- the event entry `00423B10`;
- any of the seven render-record functions that store one of the four fields.

The walker is not empty: the two large workers' walks reach 705 and 700 functions.

**No writer inside the getter's own call (U3).** The getter reads `+0xCC` as the selector at `0041FCB2`. The policy
re-reads it at `00423605`. Between the two, only `0020E600` and `0051B9E0` run; the latter is a `jmp` to `0051F240`.
Over their whole callee closure (`0020E600`, `0051F240`, `003AB7F0`, `0036B130`), the only non-stack store is the
container entry's cache at `0051F2B7` (`[rbx + 0x18]`).

So on one thread, `+0xCC` cannot change between the two reads, and §4's conclusion holds for every value `+0xCC` can
take.

**The selector value never matters (U10).** The policy returns 1 unless both normalised kinds, the candidate's and the
current event's, are 1 or 2 (`004236B0`–`0042372D`). That test runs before the selector switch at `00423735`. A
`+0xCC` of 0, 1 or 2 has kind 0 as the current event, so it returns 1 there. This is §4's argument, confirmed by
bytes.

It differs from the pool-lifecycle contract §19, which states the getter's choice of `+0xCE` as holding "if and only
if `+0xCC` is never 0, 1 or 2". With U3 and U10, the choice does not depend on that condition. The correction is
routed to OPUS, §19's author, and this record does not edit §19.

**Blind spot (as F-1 and CG-3).** Thread starts through the guarded trampoline's `ctx + 8` and the Tk workers'
callback tables are indirect and are not followed.

## 2. Binding and ownership

**Store census (U4).** The render-record code stores the four fields at exactly 22 sites.

Live ids come only from the admission `0051BA80`:
- `+0xC8` takes its return at `004247B2` / `004247CA` in `00424550`;
- `+0xC4` takes its return at `00425251` in `00424D80`.

Every other `+0xC4` / `+0xC8` store writes −1. UQ-193's control proves the six releasing sites.

The two event words:
- `+0xCE` (the alternate event) is written only by ResetDefaults and `004247D0`.
- `+0xCC` (the current event) is written by:
  - `00424D80`: the candidate at `00424FAB` and `00425274`;
  - `00424D80`: a temporary `0x2005` around a selector-2 policy call (`00424E61`, restored at `00424E8B`);
  - UQ-195's forced selection (`00423F6B` / `00423FA0`);
  - the −1 cancels at `00422AEB` / `00422C5B`.

**Binding.** A bound entry gets:
- `+0x2E0` = the render record (a back-pointer);
- `+0x2C0` = render `+0x108`.

The record then sets `+0x2A0 = 0xF`:
- in `00424550` at `004247FF` / `00424815` / `0042481F`;
- in `00424D80` at `00425362` / `00425370` / `0042537C`, through `CharacterRenderRecord_ResolveActivePresentationEntry`.

**Ownership.** The ids index the container at root `+0xDA8`; the root is resolved from render `+0x10`. The render
record owns each id: it admits it, stores it, and releases it (UQ-193).

The two binders differ (U7):
- **`00424550` always admits a fresh slot.** It releases `+0xC8` and sets it to −1 (`004245CC` / `004245D1`) before
  passing it to `0051BA80` (`00424798`).
- **`00424D80` re-binds in place.** It passes the *current* `+0xC4` (`0042522F`); `0051BA80` opens a new slot only
  for −1. It keeps the old id (`00425249`) and tests it at `00425333` to recognise a first bind.

**Routing (U8).** The route through `00423B10` is also read on FT-2's row:
- `00423B10` tail-jumps to `00424550` when `00422FD0` answers non-zero (`00423C4F` / `00423C70`).
- Otherwise it calls `00424D80` with sixth argument 0 (`00423C96`, `00423D73`).
- `CharacterRenderRecord_UpdateRootAnimationPresentationPhase` (`0042C410`) calls `00424D80` with event `0x2001` and
  sixth argument 1.

The sixth argument is the only stack argument `00424D80` reads (`00424DFF`); it is the policy selector.

## 3. Every direct effect of the two callers

These are complete store and call censuses of each body (U5, U6). A callee's own effects are cited to where it is read.

### `00424550(render, source, event)` — 10 stores, 12 callees; returns −1, −2 or 1 (U9)

1. **Resolve the source.** `003AB7F0(source)` resolves it.
2. **Tear down any alternate binding (`+0xC8 != -1`).** This happens before the source is tested.
   - Resolve the render resource entry (`ResourceTable_ResolveEntryByIndex(root + 0xD98, +0x18)`).
   - Release the entry (`0051BA40`).
   - Store `+0xC8 = -1` (`004245D1`).
   - Reset the bones through `00372280`, the per-bone state reset.
   - **A null source therefore still tears the binding down, then returns −1.**
3. **Copy the name.** `00409090` returns the source's 32-byte name at `+0x10`. It returns a default instead when the
   source's first dword equals every key on the `01EFF940` chain. The body copies the result to the stack.
4. **Check the render resource.** If `+0x18 == -1`, it returns 1 without binding.
5. **Find the section.** The name is looked up by tag with `00409FA0`, trying `@FMC`, then `@FRP`, then `@FMN`. If
   none is found, it returns 1 without binding.
6. **Admit.** It calls `0051BA80(container, -1, resolved +0x2FC, +0x488, &args)`. The argument block holds:
   - root `+0xD90` and `+0xD98`;
   - `+0x18`;
   - the name;
   - the section index;
   - the event;
   - byte `+0x413`;
   - resolved `+0x2FC`;
   - the resource entry's word `+0x8A`;
   - render word `+0`;
   - `+0x48C`.
7. **Store the result.** `+0xC8` = the result (`004247B2`). On −1 it returns −2. Otherwise it stores `+0xC8` again
   (`004247CA`) and `+0xCE = event` (`004247D0`).
8. **Set up the entry.** `0041D4D0(entry, 1)`:
   - sets entry `+0xC` bit 12 and `+0x33C = 1`;
   - sets bit 5 of the `+0xC6` word in each of the entry's `+0x28` channels (stride `0xA0`).

   Then:
   - entry `+0x2E0` = render;
   - entry `+0x2C0` = render `+0x108`;
   - render `+0x2A0` = `0xF`.
9. **Ask the policy.** It calls `004235C0(render, 0x2005, 0)`:
   - rejected → set entry `+0xC` bit 29 (`00424832`);
   - accepted → clear bit 29 (`0042483B`).
10. **Finish.** Clear render `+0x284` bit 10 (`00424842`) and return 1.

### `00424D80(render, r13, source, event, …, selector)` — 37 stores, 20 callees; returns −1, −2 or 1 (U9)

1. **Resolve the source.** `003AB7F0(source)`. If it is null, return −1.
2. **Clear the override bits.** `00420EA0(render, 0)`:
   - clears render `+0x284` bit 24;
   - clears `+0xC` bit 18 on the active and alternate entries;
   - tail-calls `004213E0(render, 0)`.
3. **Stop gate.** If `003E7D10(+0x6A4, 3)` is set and the event has no kind nibble, return −1.
4. **Policy, for an event with a kind.**
   - Call `004235C0(render, event, selector)`. A rejection returns −1.
   - Event `0x3009` while `+0xCC == 0x2009` returns −1.
   - `0x3001` and `0x4001` fold to `0x1001`.
   - With an alternate bound: set `+0xCC = 0x2005`, ask `004235C0(render, event, 2)`, and on acceptance set the
     alternate entry's `+0xC` bit 29. Then restore `+0xCC`.
5. **Copy the name.** `00409210(buffer, 00409090(source))`.
6. **Already-current test.** It applies when all of these hold:
   - `+0x5E` bit 0 is clear;
   - the `+0xC4` entry is present;
   - entry `+0x2C8` bit 12 (UQ-195's completion flag) is clear;
   - the entry name at `+0x2EC` equals the new name;
   - byte `+0x413` equals entry word `+0x31A`.

   Then:
   - If the event has a kind and equals entry `+0x31C`, it clears `+0x4B7` bit 6 and returns −1. Event `0x203D` is the
     exception and goes on to rebind.
   - If both kinds are 1 or 2 with the same index, a differing kind is switched in place: `+0x60 = +0xCC`, entry
     `+0x324` and `+0x31C` get the event, and `+0xCC` gets the event (`00424F99`–`00424FAB`). Either way it clears
     `+0x4B7` bit 6 and returns −1.
7. **Channel rebuild.** `+0x40B` bit 4 is cleared first. The rest runs only when bits 0–1 of `+0x40B` differ from
   bits 2–3 (the `(b << 2) ^ b` test at `00424FD4`–`00424FD9`):
   - kind-0 events, and kind 3/4 events with index `0x35`/`0x36`, set bit 4;
   - any other event leaves it clear, and `003326C0` + `0041F010` rebuild the channels for words `+0x2C8` and
     `+0x2CA`. These are the widest resolve fan-out on the channel pages.
8. **Index-1 events of kind 1 or 2.** When `003E7D10(+0x6A4, 3)` answers non-zero, `+0xC0` bit 6 is cleared. Kind 1
   also sets `+0x4B7` bit 6.
9. **Resource check.** If `+0x18 == -1`, clear `+0x284` bit 10 and return 1 without binding.
10. **Find the section.** Try `00409FD0(root + 0xD90, r13)` first, then the `@FMC` / `@FRP` / `@FMN` tags. If none is
    found, return −1.
11. **Admit.** Get the resource entry from `003E57D0`. Call `0051BA80(container, current +0xC4, resolved +0x2FC, +0x480,
    &args)`; the block is laid out as in `00424550`, with `+0x484`. Store `+0xC4` = the result. On −1, return −2.
12. **Record stores.**
    - `+0x60` = the old `+0xCC`
    - `+0xD0` = the old entry's `+0x328`
    - `+0xCC` = event
    - `+0x68` = `r13`, the second argument
    - `+0x69C` = `RuntimePointer_EncodeImageAddress(003AB7F0(ImageAddress_ResolveRuntimePointer(r13d)))`
    - `+0x2F4 = 0x03050303`
    - `+0x40E = 0`
    - `+0x412 = 0xFF`
13. **New-entry stores.**
    - `+0x2A` = render `+0x2FA`
    - `+0x35C` / `+0x360` = render `+0x114` / `+0x118`
    - `+0x364` = render word `+0`
    - `+0x324` = render `+0x60` (the previous event)
    - `+0x328` = render `+0xD0`
    - `+0x358` = render `+0x41A`
    - `+0x35A` = render `+0x454`
14. **Scratch-row reset.** `00372510` fills the resource entry's scratch row with `0x7FFF` and clears the resource
    entry's `+0` bit 12.
15. **First bind.** If the old `+0xC4` was −1, render `+0x284` bit 27 is set and `+0x4B7` bit 6 is set, then entry
    `+0xC` bit 1 is set and entry `+0x24 = 1`.
16. **Finish.** Back-link the active entry (`+0x2E0`, `+0x2C0`), set `+0x2A0 = 0xF`, clear `+0x284` bit 10, and
    return 1.

## What this does not claim

- **Indirect thread starts.** They are not followed; see the blind spot above.
- **Callee internals.** The effects of `0051BA80`, `003326C0`/`0041F010`, `004213E0` and `003E7D10` are cited to their
  own pages, not re-read here.
- **Scope of the store census.** It covers the render-record code, meaning the seven functions `0041F730`, `00422A30`,
  `00422C20`, `00423980`, `00423F20`, `00424550` and `00424D80`.
  - An image-wide sweep also finds stores at these displacements in other functions. They are not classified here.
  - The 12 of those that a thread procedure reaches write stack locals, or qword/xmmword/dword fields in middleware
    code. None of them writes a word at `+0xCC` or `+0xCE`.
