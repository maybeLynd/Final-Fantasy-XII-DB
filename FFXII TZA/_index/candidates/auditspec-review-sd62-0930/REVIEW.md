# SWE2-AUDIT-SPEC review of SD-62 (sd62-static-array-elements-0930 at e2777d3c8): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Reviewed: OPUS's
`e2777d3c8` (the record's only commit), [README](../sd62-static-array-elements-0930/README.md) and `sd62_elements.py`.
Static, certified image. Status reviewed: NARROWED, which is the right status.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD62-0930 | sd62-static-array-elements-0930 | `e2777d3c8` | ACCEPT |

**Re-run.** [rerun_sd62_elements.out](rerun_sd62_elements.out) is identical to the committed `.out` (ignoring CR), F1-F4
PASS, `FAILS 0`. The record directory stayed clean.

**Re-derived independently** ([sd62_rederive.py](sd62_rederive.py) / [.out](sd62_rederive.out)).
- **The 384/385 count.** Calls to `00632D80` from `rawcalls.json`: 385 raw call/jmp sites, 0 jcc, 0 relocations,
  which is the same total as retool.py's index.
  - For each site I walked back on the owner's instruction boundaries to the last write of `rdx`. **384** are
    `mov rdx, rax` after `call 006373D0`.
  - The 385th, `00632EC1` in `00632E80`, forwards its own incoming `rdx`. Its two callers:
    - `0062FB80` passes `006373D0()` (`call 006373D0; mov rdx, rax`);
    - `0059AC00` passes a stack value.

    So the "384 of 385" figure is exact, and at least one route through the 385th also carries this object.
- **What `00632D80` does with it.** The only use of `rdx` in the body is `00632DD6 mov [rcx+0x70], rdx`. The
  constructor does not link the descriptor into the object's lists, so "root the descriptors hang from" is a role
  reading of a back-pointer, not a traced list membership. That is consistent with the record's "Still open".
- **The objects' bytes.**
  - `01F2E330`'s qwords are `+0x00`/`+0x08` self, `+0x10`/`+0x18` pointing to `+0x10`, `+0x20` zero, `+0x28`/`+0x30`
    pointing to `+0x28`, and `+0x38` zero. The six non-zero slots are all DIR64-relocated, so these are real
    link-time self pointers.
  - In `01F2E780`, `+0x00`..`+0x28` point to itself, `+0x30`/`+0x38` point to `+0x30`, `+0x40` is `02CF8A80` and
    `+0x48` is `00D58D90` = "getInstanceCount". All ten slots are relocated.
- **RTTI.** My own locator walk of the vtable at `00D56D10` gives signature 1 and
  `.?AV?$PClassDescriptorWithoutDefaultConstructor@VPWorld@Phyre@@@Phyre@@`, as F3 says.

**Controls.**
- F2's rdx walk is sensitive to a different second argument: a caller passing another object would land in a non-
  `006373D0` bucket. It does not follow a forwarded argument (the 385th), which the record counts correctly as not
  shown.
- A reviewer pitfall worth recording: `tk.boundaries()` returns an unsorted list. My first walk over it produced a false
  tally of 355, which sorting fixed.

**Open points (checked, still open).**
- The "getInstanceCount" string has exactly 1 stored pointer, the `+0x48` slot, and 2 rip references: `00635B80`
  and `006AE350`. Those two functions and `0059B430` are the next read to decide between a method record and a
  name-lookup root.
- Which entries the list heads chain is untraced. No stored pointer outside the object names `01F2E780`: its 6
  relocated self-references are all inside it.

**Correction wording:** none needed. Keep the row NARROWED with the record's open points.
