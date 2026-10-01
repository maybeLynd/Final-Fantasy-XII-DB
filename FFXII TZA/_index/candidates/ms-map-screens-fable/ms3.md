# MS-3: which ancestors of a map container can be released (FABLE, Claude Opus 5.5, 2026-09-29)

[`ms3.py`](ms3.py) runs K, P, N and F: FAILS 0 ([output](ms3.out)). Static.

**Answer: none.** Each map container, location (`0209E5F0`) and track (`0209E5C0`), is a parentless widget that is never
attached, so it has no ancestor.

- **K.** The constructor only allocates (on the heap: the containers are `0x179E0` bytes) and zeroes.
- **P.** The creators attach only the page, under the container.
- **N.** None of the 125 call sites of the three tree-attach routines loads a container global in the 40 bytes before it.
- **F.** From each of the 48 loads of either global, no tree-attach routine is called within 12 instructions.

The map page's lifetime narrowing said "an ancestor's release would also end a container … which ancestors can be released
is not read here". That route is empty. The container ends only through its own per-frame step, after a closer.

**Found while controlling.** A first version counted `00247570` as an attach routine. F flagged its call at `002B9EFA`,
which passes the page, and reading the call showed it attaches a transition descriptor (`+0x48`), not a tree link. It was
removed from the set. The discrepancy came from the instrument.

**Limits:**
- N and F are bounded sweeps. A global loaded further back and carried in a register would escape them.
- A manager-wide release of every widget, if one exists, is not read here. It would not be an ancestor's release.

affected: `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` (the lifetime narrowing's ancestor sentence; the
status line's MS-3)

consumer: [the widget contract](../../../16-UI/Widget-Object-Model/CONTRACT-widget-object.md) agrees. Its constructor and
attach rows are the evidence, and a parentless widget is attached only by `00247950`.

run: ms3.py at 7b719237a, FAILS 0.
