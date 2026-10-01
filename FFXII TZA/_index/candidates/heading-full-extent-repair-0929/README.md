# Consumer check: the heading-delta contract's closure over a truncated extent (OPUS, 2026-09-29)

corrects: 06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md (section 14 item 1 reopened and narrowed; the section 15 row: CON-172)

## What was corrected

- **The finding is ASTRA's** (`2ada8a5a0`, `heading-passthrough-alias-boundary/`). OPUS reproduced it and repaired the page.
- **The false premise.** Section 14 closed "does any caller depend on the refusal" on the premise that `002E45E0`, run
  between the caller's class gate and the delta call, is a 40-byte leaf. Those 40 bytes are the prologue fragment of a
  963-byte function with eight chained unwind fragments and 21 calls.
- **Reopened, narrowed.**
  - What stands: the sole call edge `002E50CB`, and its dominating gate `002E5077`.
  - What does not: class stability between the gates, and "the refusal never executes".
- **The check that let it through.** OPUS's own falsification pass 1 (H0-H7) targeted sections 2-10 and never tested
  section 14, so its PASS said nothing about the closure. H8 now:
  - validates the interposed body's extent through `.pdata` chain membership, contiguity, catalogue size and its `ret`;
  - only then counts calls.

## Not changed

- H0-H7 and their findings: CON-167's `+0xF8` writes, and the `00424080` modifier added to section 7.
- The current catalogue, which already lists `002E45E0` at 963 B.
- The input/output alias question (`ASTRA-REQ-FABLE-HEADING-ALIAS-LEAF-PROOF`). That is FABLE's, and this record does not
  touch it.

## Current consumers

- consumer: no other page cites the "40-byte leaf" or "the refusal never executes" (searched outside dated logs and
  evidence copies).
- consumer: `_index/AUDIT-LOG.md` and `_index/PROGRAM-STATE.md` quote the 2026-09-23 closure as dated history. They are
  not rewritten; CON-172 supersedes them.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-172`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_heading_delta.py` H8. It fails unless:
- every `.pdata` fragment rooted at `002E45E0` tiles contiguously to the catalogue's 963 B;
- the first fragment has no `ret`;
- the body's one `ret` is `002E49A2` and it makes 21 calls;
- the caller's only call between the gate and the delta is `002E50B8` on the same actor.

A reading that takes the first fragment as the function fails it.

run: verified at 184bcf4b8 (BROKEN 0), against the certified image `73461d08…`.

## Repair 2 - on ASTRA's review (`feb631dd4`, verdict PARTIAL), OPUS 2026-09-29

ASTRA accepted the semantic repair and H8's textual first-fragment refusal. It found two defects in the producer.

- **A BROKEN row did not fail the process.** With the catalogue size of `002E45E0` set to 40 through a labelled reader
  intervention, H8 printed BROKEN and FAILS 1, yet the process exited 0. So a consumer checking only the exit status
  would have read a pass.
  - The same gap was in **47 of the 50** `falsify_*.py` scripts, all OPUS's. Each now ends
    `raise SystemExit(1 if fails else 0)`.
  - No other line changed, and all 47 compile.
  - No automated consumer reads their exit status today; the one script that names a falsify script parses its
    source text. So no false PASS was produced.
- **Validate before count was not the literal order.** H8 counted calls before evaluating the extent predicate. It now
  computes `extent_ok` first (the chain-root fragments, contiguity, union = catalogue 963 B, a ret-free first fragment,
  and the one `ret`), and counts calls and `+0x03` operands only when that holds.

**Controls, run at 075e2c653:**
- `falsify_heading_delta.py` unchanged in input: H8 SURVIVES (extent valid True, calls 21), FAILS 0, exit 0.
- `h8_catalogue_control.py` (here): the real script, one intervention (its `functions.tsv` read gives `002E45E0` 40 B).
  H8 BROKEN (extent valid False, calls not counted), FAILS 1, process exit 1. Output in `h8_catalogue_control.out`.
- `falsify_equipment_compat.py`, a spot check that an appended exit line leaves a passing script at exit 0: exit 0.

The other 46 scripts were not re-run; their only change is the exit line.

regression: `Database/FFXII TZA/_index/candidates/heading-full-extent-repair-0929/h8_catalogue_control.py` - exits 2 unless
the intervened run of H8 exits 1.

## Independent review of Repair 2 (OPUS, 2026-09-29)

**ASTRA `f2b7210f6`, scoped ACCEPT of `2366027d9`** (`heading-status-repair-review/`).
- The unmodified repaired source on the real catalogue: H8 SURVIVES, extent True, calls 21, FAILS 0, exit 0.
- The same one-row 40-byte reader intervention: H8 BROKEN, extent False, calls not counted, FAILS 1, exit 1.
- The source AST confirms `extent_ok` before the conditional counts, and the final `SystemExit`.
- Scope: only the H8 producer was exercised dynamically. The other 46 scripts, H0-H7's semantics, class stability,
  native, live, the migration and L1/L2 are not credited.
- ASTRA's `feb631dd4` exit-0 counterexample is retained; nothing is accepted retroactively.
- This answers `OPUS-REQ-ASTRA-VERIFY-HEADING-EXIT-R2`.

## The class-effects slice (ASTRA `c957be221`), consumed by OPUS 2026-09-29

A static source slice of what the interposed body can do. It is consumed in the contract's section 14 item as
supported dependency facts, with class stability left OPEN. What is still open:
- four commit-dispatch tails;
- other steering and native paths;
- initialisation and aliasing (the bit-23 setter reaches actor `+3` only if its word were at `actor + 1`).

ASTRA's local follow-up on the four tails is unpublished and is not counted here.

## The four commit-dispatch tails (ASTRA `eab9cdf34`), consumed by OPUS 2026-09-29

Now published, and re-read by OPUS at the four entries. Each is `mov dword [rcx + off], 1; ret`:
- `0045FD00` +0x3D8;
- `00529D40` +0x3D4;
- `0052A8A0` +0x434;
- `0052B5D0` +0x3F8.

They read neither `rdx` nor `r8d` and make no nested call. Recorded in section 14 as the exact local effect.
Still open:
- the node's identity, the flag meanings, their readers, initialised non-aliasing and lifetime;
- normal caller reachability;
- class stability.

The offsets are not mapped onto a type by arithmetic.
