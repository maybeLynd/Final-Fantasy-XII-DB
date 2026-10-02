# Consumption draft: ov42-actor-predicate-domain (OV-42)

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

This draft is for FABLE to apply. Nothing here has been edited into a page. The draft follows the accepted scope of
[REVIEW.md](REVIEW.md) (ACCEPT-WITH-NARROWING) and keeps the packet's limits.

## Candidate pages and their leads

Leads are counted with `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | Lead by commit subject | Role |
|---|---|---|
| `07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` | **FABLE 5** (the largest single prefix; OPUS 2; the SWE2-EC7 batch prefixes are each 1) | FABLE's availability page. It holds the cascade (§2), the per-unit leg, and the 2026-10-02 OV-42 subsection that names "the unit's raw record (`002FFD05`)". **FABLE may edit it.** |
| `09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md` | OPUS 6, S-25 3, FABLE 2 | It states "Class 20 accepts exactly 0–0x21E, because `[02EBF138]` has 543 rows". **Route to OPUS.** |
| `12-Items-Equipment-Shops-License/CONTRACT-license-check.md` | OPUS 6 | It already says `00322C50` never reads the incoming R8D and that `00323EC0` takes RCX = statsRecord. That agrees with this review. **Route to OPUS** only as corroboration; no change is needed. |

The packet names an OPUS "low16 argument and source-order contract". No OPUS-led page found by grep states
`002FFCF0`'s argument contract. Route that item to OPUS (below).

## Edits to the FABLE page (`battle-command-availability-and-reason-codes.md`)

### A. Per-unit leg pseudo-code (§2, "The per-unit leg, and the License Board")

The parameter `00306480` receives is the parsed record, not the unit. FABLE's own cascade names it `raw`, and
OPUS's license contract calls it statsRecord.

OLD:

```
if (unit == NULL)                                        return 0x2C;
```

NEW:

```
if (raw == NULL)  /* RDX = 002FFCF0's RDI, q[unit+0x698] */  return 0x2C;
```

OLD:

```
if (BattleStats_HasRequiredLicenseForAction(unit, actionId))     return 0;
```

NEW:

```
if (BattleStats_HasRequiredLicenseForAction(raw, actionId))      return 0;
```

### B. The 2026-10-02 OV-42 subsection, bullet "What does not exclude 511..534", first sub-bullet

OLD:

> Class `0x14` accepts 0..542. The count is `[02EBF138]+4` = 543 (`00322F84`, `0032302C`..`0032303B`).

NEW:

> Class `0x14` accepts 0..542. The count is the runtime value `[02EBF138]+4` (`00322F84`, `0032302C`..`0032303B`).
> 543 is the shipped table's row count, and that is a premise: `02EBF138` lies in `.data`'s virtual tail, so it is 0
> at load, and a NULL descriptor refuses every id.

### C. Same subsection, bullet "What does exclude them", leg (a), first sentence

OLD:

> (a) `0030DB70`'s record arm. If the unit's raw record (`002FFD05`) has byte `+5` = 0, `003060E0` returns 5 for
> `+0x1E` 7 (`00306300`).

NEW:

> (a) `0030DB70`'s record arm. If the unit's raw record has byte `+5` = 0, `003060E0` returns 5 for `+0x1E` 7
> (`00306300`). That record is the pointer `002FFCF0` loads from incoming RDX `+0x698` at `002FFD05` and keeps in
> RDI. It passes the pointer as RDX to `00306480` (`002FFE97`), which forwards it unchanged to `003060E0`, where
> `00306129` reads `+5`. The later reloads of `+0x698` (`002FFD38`, `002FFDB4`) do not replace it. The `+5` test
> therefore concerns that parsed record, not a byte of the outer unit.

### D. New paragraph appended to the same subsection, before "**Limits kept.**"

> **What a zero availability reason proves about the id** *(FABLE 2026-10-02, from ASTRA's
> [`ov42-actor-predicate-domain`] (page-relative link: `../../_experiments/evidence/ov42-actor-predicate-domain/README.md`) (`2b341ca3a`),
> FABLE independent review [`fable-review-astra-ov42-actor-predicate-domain-1002`] (page-relative link: `../../_index/candidates/fable-review-astra-ov42-actor-predicate-domain-1002/REVIEW.md`),
> ACCEPT-WITH-NARROWING).*
>
> - `002FFCF0` has two returns: the early constant 2, and the shared reason return.
> - The only EAX definition that can make the shared return 0 is the final cost call `00303BD0`. That call is
>   reachable only through the class-success edge after `002FFD8B`.
> - The class query receives EDX = the zero-extended low 16 bits of the incoming id (`002FFD0C`), ECX = `0x14` and
>   R8D = 1. The class-`0x14` arm and the shared tail never read R8.
> - So a normal zero reason requires class `0x14` to accept the id. Under the count-543 premise the id is then
>   0..542, which still includes 511..534.
> - This is a necessary condition only. A zero reason also requires `0030E9C0`, `0031A7B0`, `00306480` and
>   `00303BD0` each to return 0. It does not show that any of 511..534 passes those gates.
> - The record's byte `+5` staying unchanged between `002FFD05` and the `00306480` leg is a premise. Two callees on
>   that path, `0030E9C0` and `0031A7B0`, receive the record pointer itself.

### Limits to keep beside D

The packet's limits are kept unchanged:

- no caller, natural state or zero-result feasibility;
- no committed producers or override writers;
- no loader, I/O, owner or lifetime closure;
- no pointer stability observed in a running game.

Whole OV-42 stays OPEN.

## Routed to OPUS (not FABLE-led)

- **`CONTRACT-gambit-walk.md` (OPUS).** Its "Class 20 accepts exactly 0–0x21E, because `[02EBF138]` has 543 rows" is
  consistent with this review. Optional qualification: the count is runtime-bound (`02EBF138` is in `.data`'s virtual
  tail). A NULL descriptor refuses everything with reason 4.
- **The argument contract.** At `002FFD8B`, EDX = `movzx` low 16 of the incoming CX, ECX = `0x14` and R8D = 1. At
  `002FFE9D`, ECX = the same low 16, RDX = the RDI record and R8D = 0. That R8D = 0 is forwarded to `003060E0`'s third
  parameter (`003060F8`). No instruction in `00322C50` reads the incoming R8. The class-1 arm's call `00309440` would
  pass it on unchanged.

## OPEN-QUESTIONS.md, OV-42 row (not edited)

The row's 2026-10-02 narrowing says "nor class `0x14` (accepts 0..542) excludes rows 511..534" and "`0030DB70`'s
record arm when the raw record's byte +5 is 0". Both stay true. **No lead-word change is needed.** One optional
qualification would match narrowing 2: change "(accepts 0..542)" to "(accepts 0..542 under the runtime count-543
premise; a zero availability reason implies it, as a necessary condition only)". "raw record" already names the
parsed record, so the byte-+5 clause needs no change.
