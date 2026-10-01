# Two selector guards repaired; what the 256 small-shape frontier bodies support (SWE2-EC7, 2026-09-30)

*Follow-up to `ec7-f-shape-pass-0930` and `ec7-accounting-ruling-round-0930`. The guard fixes were run on the accounting-ruling
round's export (F 4,791); the shape census was run after the Phyre application (F 4,563).*

## 1. Two of the three selectors that failed their own guards (SWE2-EC7)

- `select_scalar_conversion_registrars.py` failed two asserts. "No hit is declared" counted the family's **own** row,
  because the self-skip was missing, so the selector could not re-run once its row existed. "No hit is A" also failed:
  two of the 144 form hits (`0058D970`, `0058FEF0`) were measured A after declaration, and the row was already 142.
  The fix skips its own row. Under FABLE's ruling, A hits and hits another family owns are now left out of the output
  and printed, not asserted away. The re-run reproduces the 142-member file exactly.
- `select_static_init_form.py`'s count guard expected 44 generic members. One generic member has since been measured A,
  and the selector already excludes it; the row was already 43. **Count guard only:** 44 -> 43, and the re-run
  reproduces all three of its files.
- The third, `select_guarded_class_registrars.py`, is the DERIVED family. Its twin assert named `005B2860`, a body
  outside every family that matches its predicate. The Phyre application (`ec7-phyre-uniform-0930`) admits `005B2860`
  to PAnimation. Re-run after it, the guard passes and the selector writes the same 99. No code change was needed.

## 2. The small-shape frontier: no form-family population (SWE2-EC7)

[`shape_clusters.py`](shape_clusters.py) groups the 256 non-UC-1 small-shape frontier bodies left after the Phyre application (tiny
leaves, forwarders, getters, setters, thunks) by instruction skeleton, with constants and addresses abstracted. It also counts each
skeleton's twins across the census by disposition. Rows are in [`shape_clusters.tsv`](shape_clusters.tsv).

- **231 distinct skeletons for 256 bodies.** Only 2 skeletons have 3 or more frontier bodies:
  - `mov edx,[rdx+K]; jmp T`: `0042BDD0`, `0042E530`, `0042E540`
  - `cmp byte [rcx],0; jne T; ret`: `0045AEE0`, `0045B2A0`, `0045BAD0`
- **The twins mostly belong to existing families.** Where a skeleton has twins outside the frontier, they are members of
  a static-teardown family, ExplainedCalleeForwarder, DocumentedGlobalAccessor or a library span. Those families'
  selectors already decline these bodies on their own bar: a callee or target test, an exact citation, or a span.

**Proposal.** The census does not support new form families. A form family needs many bodies with one skeleton and a
shared-target control; here almost every body is unique. Admitting them by size or shape would be a bulk disposition
without evidence, which policy rejects. Three routes are open, ranked by yield:
1. **Individual explanation (A).** Most are 1-5 instruction bodies whose meaning is their single caller's or target's.
   An interior citation on the page that explains that caller makes them A. That is page work by the owning lanes, not
   EC-7 work.
2. **Caller-side families.** A body called only from one already-declared object could join that object's family through
   its selector's closure, the way the library selectors join helpers. Each needs the owning family's own predicate.
3. **Two micro-families** of 3 bodies each (the two skeletons above). These are proposed only if FABLE wants form
   families that small. Each would need its target control: whether the three share a callee, and whether their
   callers are one object.

run: shape_clusters.py on a clean export of 4b748e8af with the Phyre application applied (F 4,563).
