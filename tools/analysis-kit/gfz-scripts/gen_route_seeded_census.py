#!/usr/bin/env python3
"""gen_route_seeded_census.py - offset-tracked access census seeded from the store's own route.

WHY THIS EXISTS. gen_offset_tracked_census.py carries a displacement through lea, add/sub and
argument slots, which is what a plain "does this register hold the object" census does not, and
on ManagerSingleton0209BE80 that difference refuted two published absence claims. But it was
hard-wired to one type and one seeding shape, and running it against SavePayload exposed the
next limit: ONE OF THE FOUR REGIONAL CONTROLS CAME BACK EMPTY. `ImageBackedStateBlock`, embedded
at SavePayload +0x8000, got zero offsets - not because nothing touches it, but because it is a
DECLARED TYPE WITH ITS OWN ROUTE (`PTR 0x020927C0`), so code reaches it through its own base and
never through payload+0x8000+d. A CENSUS SEEDED AT THE PARENT IS BLIND TO A CHILD REACHED
DIRECTLY, and a zero it reports over such a child means nothing.

SO THIS SEEDS FROM THE STORE'S `route` COLUMN, and with --with-children it also seeds every
embedded child that has a route of its own and folds that child's offsets back in at the embed
offset. The three route forms it understands are the ones the store actually uses for reachable
objects:

    PTR 0xADDR [+0xOFF]   the object pointer is loaded from that global: `mov rX,[rip->ADDR]`;
                          with +0xOFF the instance is *(ADDR)+OFF and the loaded pointer
                          carries -OFF, the same convention as FN's return
    FN 0xADDR+0xDELTA     the base is that function's return plus DELTA: RAX carries -DELTA
    STATIC 0xADDR         the object IS at that address: `lea rX,[ADDR]`
    ARRAY 0xADDR stride=0xS   the elements are at ADDR + i*S: `lea rX,[ADDR]` and the element
                          base is COMPUTED, `imul rY,rI,S` then `add rX,rY`

    PARRAY 0xADDR [+0xOFF] stride=0xS   element i at `*(ADDR) + OFF + i*S`: the block base is
                          LOADED like PTR, the element base then composes like ARRAY
    SLOTPTR 0xADDR [stride=0xS]         instance i is `*(ADDR + i*S)`, a pointer table - each
                          indexed load yields an object base directly
    PTABLE 0xADDR stride=0xS            instance i is `*(*(ADDR) + i*S)`, a pointer table
                          behind a CELL - `mov rB,[rip->ADDR]` marks rB a table base and a
                          qword load off it yields an element base

    CHAIN Parent +0xOFF   the child is a member of Parent - embedded when Parent's field row
                          at OFF declares the child's own type, a POINTER MEMBER when it
                          declares `X*`. Resolved recursively to a seedable ROOT route, then
                          walked in root coordinates: `off == OFF` names the child base, a
                          pointer-member load seeds `off[d] = off[b] + disp`, and emission
                          filters to the child's window with the access register at the
                          deepest deref or below.
    EMBED Parent +0xOFF   the same relation spelled as the route kind (always embedded)
    RELOFF Parent +0xOFF  the image-format idiom: child base is `Parent + *(int32*)(Parent
                          + OFF)` - the dword load is tracked as a rel and combined with the
                          base by the add/lea handlers.

DYNAMIC routes are NOT handled - `unseedable`, never silently zero. A derived alternative whose
parent chain reaches no seedable route is likewise named unresolved. A CHAIN member with no
declared field row at its offset stays unresolved rather than guessing pointer-vs-embedded.

ARRAY WAS MODELLED BUT UNREACHABLE until 2026-09-20. `Census.stride` recognises the computed
element base and has since it was written - its own comment says that shape "is why seventeen
ARRAY-routed types had no census" - but nothing ever SET it, because `parse_route` accepted
only PTR/FN/STATIC, so every ARRAY route fell out at "not one this tool models". The store
holds 19 ARRAY routes over 17 distinct types, which is that comment's own number. Wiring the
parser to the machinery is the whole change; the walk is untouched.
BY CONSTRUCTION NO EXISTING CENSUS MOVES: `stride` is set only for an ARRAY rule, and an ARRAY
route previously produced no output at all. Checked rather than asserted - a PTR census
regenerated after the change is byte-identical.

A STATED LIMIT, so a ZERO IS NOT READ AS ABSENCE. A tracked pointer is propagated into a callee
only through ARG_REGS (rcx/rdx/r8/r9). An object passed as the FIFTH OR SIXTH argument - on the
stack - is dropped at the call, and the callee's accesses are then invisible. Two declared types
census to zero for exactly this reason: ChunkedSlotEntry (0x02CA7540) and ChunkedSlotBankEntry
(0x02CA74A0) are passed by 00477EE0 to 0051F9F0 as the 6th and 5th arguments
(`mov [rsp+0x28], rax` / `mov [rsp+0x20], rax`), and 0051F9F0 stores them into its object at
+0x10 and +0x38 and walks them there. Seeding 0051F9F0 directly is NOT the fix: it has three
callers, each supplying its own table pair, so a census seeded there conflates three instances -
the conflation emit_seeded_census.py records as measured. Tracked as
OPUS-PROPOSE-CENSUS-STACK-ARGUMENT-SEEDING (2026-09-20, OPUS).

THE OFFSET RULE, unchanged and load-bearing: a LOAD THROUGH A TRACKED POINTER KILLS THE OFFSET.
The value read is a different object, and conflating the two is how a census starts attributing
another type's displacements to this one - which ManagerSingleton0209BE80 has had retracted
three times.

WHAT IT REPORTS. Every distinct offset inside the declared size, grouped by the field row it
falls in, and for each row that reads as a gap, whether anything lands in it. It does NOT split
anything: a displacement is an observation and a layout is a reading, and the gap between those
two is where this store's retractions live.

HOW MUCH THE `--shared-at` THRESHOLD MATTERS: measured, and the answer is almost not at all.
Swept on ManagerSingleton0209BE80, the type with the most exposure to measure:

    --shared-at      5     10     20     40     80    160
    accesses       520    508    475    471    450    315
    of 1,417     36.7%  35.9%  33.5%  33.2%  31.8%  22.2%

**Flat across a 32-fold range**, because the propagation does the work: once a genuinely generic
helper is caught - 00246AD0 at 126 callers, 00244F00 at 168 - its whole subtree is marked at any
threshold below its own caller count, and those subtrees are where the volume is. The default of
20 is therefore not a number the result balances on.

AND THE CONCLUSIONS DO NOT MOVE AT ALL. Regenerating this type and its seven projected children
at --shared-at 5 (1,026 rows excluded) and at 160 (630 excluded) and running
check_census_widths.py over both gives **0 disagreements either way** - roughly 400 more rows
admitted as width evidence at the permissive end, and they still agree with every declared row.
Re-run it with a shell loop over the flag; nothing here needs a special mode.

usage: gen_route_seeded_census.py --type <name> [--with-children] [--max-depth 6]
                                  [--shared-at N] [--out PATH]
"""
import argparse
import collections
import csv
import io
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import call_graph as CG  # noqa: E402
import check_default_instance_writers as W  # noqa: E402

import capstone  # noqa: E402
import reg_tracking as RT  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86


def W_OF(text):
    """Operand width of a census instruction, via the checker's own parser - so the
    run detection here and the exclusion there cannot disagree about what a width is."""
    import check_census_widths as _C
    return _C.width_of(text)


# PTR accepts the grammar's optional `+0xOFF` (`instance at *(ADDR) + OFF` - the loaded
# pointer then carries -OFF, the same convention FN uses for its return). STATIC tolerates
# a trailing ` -> note` annotation, the same way ARRAY already accepts trailing text.
R_PTR = re.compile(r"^PTR\s+0x([0-9A-Fa-f]+)(?:\s*\+\s*0x([0-9A-Fa-f]+))?(?:\s.*)?$")
# `bank=0xD` qualifies a BANK-GENERIC getter: the callee's element type is decided by the
# bank it is handed in arg1, not by the function, so one FN address serves several types
# (002ED570 decodes stride and mask out of the bank itself and serves 0x50, 0xC0 and 0x260
# elements). With the qualifier, a call site seeds the return only when rcx's provenance
# there is a field load at displacement D - followed through register copies and callee
# argument edges by classify_slot_resolver_sites.site_slot_map, and dropped whenever any
# feeding path disagrees.
R_FN = re.compile(r"^FN\s+0x([0-9A-Fa-f]+)\s*\+\s*0x([0-9A-Fa-f]+)"
                  r"(?:\s+bank=0x([0-9A-Fa-f]+))?\s*$")
R_STATIC = re.compile(r"^STATIC\s+0x([0-9A-Fa-f]+)(?:\s.*)?$")
# `count=` and `index=` are deliberately NOT required and NOT read. The walk needs the base and
# the stride and nothing else, and the store writes counts this tool must not try to parse -
# `count=byte[window+0x3C2]` is a real one. An unknown count is not a reason to refuse a census.
R_ARRAY = re.compile(r"^ARRAY\s+0x([0-9A-Fa-f]+)\s+stride=0x([0-9A-Fa-f]+)(?:\s.*)?$")
# `PARRAY 0xADDR [+0xOFF] stride=0xS` - element i at `*(ADDR) + OFF + i*S`: the ARRAY machinery
# over a base that is LOADED, not lea'd. The pointer load seeds the register at -OFF exactly
# like PTR, and the element base then forms by the same imul/add/indexed-operand composition.
# `SLOTPTR 0xADDR [stride=0xS]` - instance i is `*(ADDR + i*S)`, a pointer TABLE: each indexed
# load yields an object base directly, no element arithmetic. `stride` is documented as
# required but `SLOTPTR 0x022C1788 count=4` omits it - a qword table is stride 8.
R_PARRAY = re.compile(r"^PARRAY\s+0x([0-9A-Fa-f]+)(?:\s*\+\s*0x([0-9A-Fa-f]+))?\s+stride=0x([0-9A-Fa-f]+)(?:\s.*)?$")
R_SLOTPTR = re.compile(r"^SLOTPTR\s+0x([0-9A-Fa-f]+)(?:\s+stride=0x([0-9A-Fa-f]+))?(?:\s.*)?$")
# THE DERIVED ROUTES - the child is reached THROUGH a parent object rather than at an image
# address of its own. `CHAIN P +0xOFF` is a member of P: embedded when P's field at OFF is
# declared with the child's own type, a POINTER MEMBER when the field is `X*` - the field
# declaration, not the route word, decides. `EMBED P +0xOFF` is the same relation spelled as
# the route kind (the store writes EMBED for a route alternative). `RELOFF P +0xOFF` is the
# image-format idiom: the array base is `P + *(int32*)(P + OFF)`, a dword field that must be
# READ before the address exists.
# A CHAIN may carry further `+0xN` terms: each is a DECLARED dereference through an
# anonymous intermediate (`CHAIN Ctx +0x150 +0x8` = `*(*(ctx+0x150)+8)`). Only the first
# offset is arbitrated by a field row - there is no type to arbitrate the deeper ones, and
# writing the term asserts the deref.
R_CHAIN = re.compile(r"^CHAIN\s+(\w+)((?:\s*\+\s*0x[0-9A-Fa-f]+)+)(?:\s.*)?$")
R_RELOFF = re.compile(r"^RELOFF\s+(\w+)\s*\+\s*0x([0-9A-Fa-f]+)(?:\s.*)?$")
R_EMBED = re.compile(r"^EMBED\s+(\w+)\s*\+\s*0x([0-9A-Fa-f]+)(?:\s.*)?$")
# `SLOTPTR Type +0xOFF stride=0xS` - the parent-relative form: P embeds a pointer TABLE at
# +0xOFF and element i is `*(P + OFF + i*S)`, a DERIVED route (ActorStorageRecord's
# `*(*(ActorManagerSlot +0x08) + 8 + i*8)` through the pool). The absolute form keeps its
# own kind; the two never collide because a type name cannot start `0x`.
R_PSLOT = re.compile(r"^SLOTPTR\s+(\w+)\s*\+\s*0x([0-9A-Fa-f]+)(?:\s.*)?$")
# `PTABLE 0xADDR stride=0xS` - a pointer table behind a CELL: the table base is `*(ADDR)`
# and element i is `*(*(ADDR) + i*S)` (Category's `*(*(0x02EAD008) + i*8)`). One more
# indirection than SLOTPTR, whose table sits AT the address.
R_PTABLE = re.compile(r"^PTABLE\s+0x([0-9A-Fa-f]+)\s+stride=0x([0-9A-Fa-f]+)(?:\s.*)?$")
# A PACK-REFERENCE RESOLVER level: `PKREF 0xFN Parent +0xOFF` declares that the dword at
# parent+OFF is a 32-bit pack offset whose decoding goes through FN - `0020E600` is the
# build's resolver (`mov eax, ecx ; add rax, qword [01F83530] ; ret`). The parent may be a
# store type (`NavRunStateBlock`) or a bare cell (`0x02EBF118`, an `AuthoredTableHeader`
# registry slot - the header TYPE is band-shared, so the slot itself is the parent).
R_PKREF = re.compile(r"^PKREF\s+0x([0-9A-Fa-f]+)\s+(\w+)\s*\+\s*0x([0-9A-Fa-f]+)(?:\s.*)?$")
# `VTABLE 0xADDR` - the object is reached ONLY through virtual dispatch: no caller ever
# holds a `this` the store can name, so there is no seed site at all. The hosts are the
# vtable's own entries, each walked with rcx marked at 0 - `this` at method entry. The
# table is read out of the image: consecutive qwords that are known function entries,
# stopping at the first non-function qword. The seed is honest because every call site
# is `call [rax + slot]` off a loaded object - rcx IS the instance at entry.
R_VTABLE = re.compile(r"^VTABLE\s+0x([0-9A-Fa-f]+)(?:\s.*)?$")
# `ARG reg 0xFUNC` - the object is in `reg` at the entry of a NAMED function, proven by a cited
# instruction in the row (the grammar form candidates/derived-route-parent-roots.md proposed for
# the three argument-rooted parents). Seeded exactly like one VTABLE entry: the function is the
# host, and `reg` is marked at offset 0 in its body.
R_ARG = re.compile(r"^ARG\s+(rcx|rdx|r8|r9)\s+0x([0-9A-Fa-f]+)(?:\s.*)?$", re.I)


def store(db):
    tr = list(csv.reader(io.open(os.path.join(db, "_types", "types.tsv"),
                                 encoding="utf-8", newline=""), delimiter="\t"))
    h = tr[0]
    ir, isz, ict = h.index("route"), h.index("size"), h.index("ctor")
    types, routes = {}, {}
    for r in tr[1:]:
        if not r or len(r) <= max(ir, isz):
            continue
        routes[r[0]] = r[ir].strip()
        try:
            sz = int(r[isz], 16)
        except ValueError:
            continue
        types[r[0]] = (sz, r[ir].strip(), (r[ict] if len(r) > ict else "").strip())
    fr = list(csv.reader(io.open(os.path.join(db, "_types", "fields.tsv"),
                                 encoding="utf-8", newline=""), delimiter="\t"))
    fields = collections.defaultdict(list)
    for r in fr[1:]:
        if len(r) >= 5:
            try:
                fields[r[0]].append((int(r[1], 16), int(r[2]), r[3], r[4]))
            except ValueError:
                pass
    # `routes` carries EVERY row's route text, including size-UNRESOLVED types like
    # ActorRecordPool: derivation needs a parent's route but never its size, so a parent
    # that `types` drops must still be reachable.
    return types, fields, routes


def parse_route(route):
    """Every rule is a 4-tuple (kind, addr, aux, stride): `aux` is the PTR/PARRAY offset or the
    FN delta (0 elsewhere), `stride` is set on the three array classes (0 elsewhere). A
    bank-qualified FN carries a fifth element: the arg1 slot displacement, or None."""
    m = R_PTR.match(route)
    if m:
        return ("PTR", int(m.group(1), 16), int(m.group(2) or "0", 16), 0)
    m = R_FN.match(route)
    if m:
        return ("FN", int(m.group(1), 16), int(m.group(2), 16), 0,
                int(m.group(3), 16) if m.group(3) else None)
    m = R_STATIC.match(route)
    if m:
        return ("STATIC", int(m.group(1), 16), 0, 0)
    m = R_ARRAY.match(route)
    if m:
        return ("ARRAY", int(m.group(1), 16), 0, int(m.group(2), 16))
    m = R_PARRAY.match(route)
    if m:
        return ("PARRAY", int(m.group(1), 16), int(m.group(2) or "0", 16),
                int(m.group(3), 16))
    m = R_SLOTPTR.match(route)
    if m:
        return ("SLOTPTR", int(m.group(1), 16), 0, int(m.group(2) or "8", 16))
    m = R_PTABLE.match(route)
    if m:
        return ("PTABLE", int(m.group(1), 16), 0, int(m.group(2), 16))
    m = R_PKREF.match(route)
    if m:
        # (kind, parent, member_off, resolver) - parent is a type name, or the bare
        # cell as an int when spelled `0x...`. The resolver rides in the stride slot.
        p = m.group(2)
        return ("PKREF", int(p, 16) if p.startswith("0x") else p,
                int(m.group(3), 16), int(m.group(1), 16))
    m = R_VTABLE.match(route)
    if m:
        return ("VTABLE", int(m.group(1), 16), 0, 0)
    m = R_ARG.match(route)
    if m:
        # (kind, host-fn, arg-register index into W.ARG_REGS) - the register slot
        # carries what a VTABLE rule's implicit rcx carries.
        return ("ARG", int(m.group(2), 16),
                ("rcx", "rdx", "r8", "r9").index(m.group(1).lower()), 0)
    m = R_CHAIN.match(route)
    if m:
        sm = re.search(r"stride=0x([0-9A-Fa-f]+)", m.group(0))
        offs = [int(x, 16) for x in re.findall(r"0x([0-9A-Fa-f]+)", m.group(2))]
        rule = ("CHAIN", m.group(1), offs[0], int(sm.group(1), 16) if sm else 0)
        # trailing `+0xN` terms ride along as a fifth element - declared derefs
        # through anonymous intermediates (see R_CHAIN)
        return rule + ((tuple(offs[1:]),) if len(offs) > 1 else ())
    for r, k in ((R_RELOFF, "RELOFF"), (R_EMBED, "EMBED"),
                 (R_PSLOT, "PSLOT")):
        m = r.match(route)
        if m:
            sm = re.search(r"stride=0x([0-9A-Fa-f]+)", m.group(0))
            # A CHAIN/EMBED alternative's stride is the child's ELEMENT size when the
            # member is an interior array (element i at parent + OFF + i*S).
            return (k, m.group(1), int(m.group(2), 16),
                    int(sm.group(1), 16) if sm else 0)
    return None


def parse_routes(route):
    """Every alternative this tool models, as (rule, text) - the store's route column is a
    `|`-separated LIST and matching the whole string refuses perfectly good types.

    `gen_ptr_census.py` has always split on `|`; this one did not, so it answered "route ... is
    not one this tool models" for three types whose alternatives it models perfectly well -
    including `PostProcessParamContext`, `PTR 0x01F7F5F0 | PTR 0x01F81300`, which is the store's
    canonical TWO-SLOT singleton and the type this tool's own control was validated against.
    An object reachable two ways is accessed through both, so every modelled alternative is
    seeded and the row records which one reached it.
    """
    out = []
    for alt in route.split("|"):
        alt = alt.strip()
        rule = parse_route(alt)
        if rule:
            out.append((rule, alt))
    return out


SEEDABLE = ("PTR", "FN", "STATIC", "ARRAY", "PARRAY", "SLOTPTR", "PTABLE", "VTABLE", "ARG")
DERIVED = ("CHAIN", "RELOFF", "EMBED", "PSLOT", "PKREF")


_BANK_SITES = {}


def bank_sites(img, getter, want_disp):
    """The (entry, call-site) pairs at which a call to `getter` provably receives the
    bank whose pointer lives in a `+0xD`-slot field - 'provably' meaning the resolved
    provenance class is exactly {('fld', want_disp)}: a site fed by two different
    slots, or by anything the slice cannot prove, qualifies for no type. The
    per-site classification (register copies and callee argument edges followed to a
    fixed point) lives in classify_slot_resolver_sites.site_slot_map; the result is
    cached per (getter, slot) because it is a full-image pass."""
    key = (getter, want_disp)
    if key not in _BANK_SITES:
        import classify_slot_resolver_sites as CL
        smap = CL.site_slot_map(lambda e: img.body(e), list(img.sizes),
                                img.md, getter)
        _BANK_SITES[key] = {k for k, v in smap.items()
                            if v == frozenset({("fld", want_disp)})}
    return _BANK_SITES[key]


def _level_kind(kind, fields, parent, off):
    """What `CHAIN Parent +0xOFF` means physically. The parent's own field row at OFF is
    authoritative: a `X*` ctype is a pointer member, a plain `X`/`X[N]` is embedded. With no
    field row there is nothing to arbitrate between the two - the level stays unresolved
    rather than guessing which side of a dereference the child sits on."""
    if kind == "EMBED":
        return "embed"
    if kind == "RELOFF":
        return "rel"
    if kind == "PKREF":
        # the member is a u32 pack offset by declaration - no pointer/embed ambiguity
        # to arbitrate, so no field row is required.
        return "pkref"
    for fo, _fs, _fn, ctype in fields.get(parent, ()):
        if fo == off:
            if kind == "PSLOT":
                # a `SLOTPTR Type +0xOFF` level is a table OF POINTERS in one of two
                # physical shapes, and the field ctype arbitrates them. `X**` (pBegin
                # `void**`) is a POINTER TO a heap table - `mov t,[b+OFF]` loads the
                # table pointer and elements are `[t + i*S + k]`. `X*` (recordPtr
                # `ActorStorageRecord*`) reads as the table's own base member - the
                # object IS the table and elements are `[b + i*S + OFF]` directly.
                ct = ctype.strip()
                if ct.endswith("**"):
                    return "ptable_ptr"
                if ct.endswith("*"):
                    return "ptable"
                return None
            return "ptr" if ctype.strip().endswith("*") else "embed"
    return None


def _fold_element(dv, d, breg):
    """EMBED interior arrays: an access through element k > 0 folds onto element 0 (SWE2-STRUCT, 2026-10-03).

    A derived EMBED run's emit window is ONE element (`span` = the stride), so a register standing at element k's base
    (root offset rebase + k*stride) had every access dropped. SystemStopRecord lost all 82 bank-B accesses of its builder
    00227680 that way: the caller passes r8 = registry + 0x2A0 + i*0x18 (element 28 + i). When the route declares
    `count=N`, a displacement inside rebase .. rebase + span*N is element-relative: both d and the register's base move
    back by the same k*span, so the base-depth checks are unchanged. Without a declared count nothing changes."""
    cnt = dv.get("count") or 1
    rb, sp = dv["rebase"], dv["span"]
    if cnt > 1 and sp and rb + sp <= d < rb + sp * cnt:
        k = (d - rb) // sp
        return d - k * sp, breg - k * sp
    return d, breg


def derive_specs(types, fields, routes, child, alt, seen=None):
    """Resolve one CHAIN/RELOFF/EMBED/PSLOT alternative `(kind, parent, off, stride)` to
    concrete census specs. Returns (specs, failures): each spec is

        (root_rule, root_alt_text, derived, path_text)

    where `derived` is the dict the walk reads:

        rebase  - the child's base expressed as an offset from the ROOT object's base
        derefs  - root-coordinate member offsets that are pointer loads (the loaded register
                  then stands at that offset in the walk's coordinate frame)
        ptables - root-coordinate offsets of INLINE pointer tables: a qword load
                  `[b + i*S + off]` (or slot 0 `[b + off]`) fetches element i
        tptrs   - root-coordinate offsets of POINTER-TO-TABLE members: a `mov t,[b+off]`
                  loads the table pointer itself (tracked in `tptr`), and elements come
                  only from loads through a proven table-pointer register
        rels    - root-coordinate offsets that are rel-offset dwords (`base + *(base+off)`)
        decodes - {resolver fn: member coordinate} for PKREF levels: at a call to the
                  resolver with rcx carrying that coordinate's rel dword, rax becomes
                  the child base (`rax = ecx + arena` for 0020E600)
        last    - the deepest deref offset; an access only belongs to the child when the
                  register it came through stood at `last` or deeper (this is what keeps
                  the pointer fetch itself, made through a shallower register, out of
                  the census)
        span    - the child's emit width (its size; an interior-array child's stride)

    The parent is itself resolved recursively, so a two-level chain (`A -> *B -> *C`)
    composes to one spec with both derefs; every alternative of every level produces its own
    spec. The parent's ROUTE comes from `routes`, not `types` - a size-UNRESOLVED parent
    (`ActorRecordPool`) still seeds a derivation because its size is never used here.
    A level whose parent cannot be seeded is a failure, named - never silently zero.
    """
    seen = seen or frozenset()
    kind, parent, off, stride = alt[0], alt[1], alt[2], alt[3]
    extras = list(alt[4]) if len(alt) > 4 else []
    lvl = _level_kind(kind, fields, parent, off)
    if lvl is None:
        return [], ["%s +0x%X: member kind unresolved (no field row at the offset)"
                    % (parent, off)]
    child_size = types.get(child, (0, "", ""))[0]
    specs, fails = [], []

    def fold(spec):
        """Lay this alternative's offsets over a resolved parent spec (or the zero spec
        of a seedable parent). Each offset is cumulative in root coordinates; the first
        level's kind is field-arbitrated (`lvl`), every further `+0xN` term is a declared
        dereference through an anonymous intermediate."""
        d2 = {"rebase": spec["rebase"], "derefs": set(spec["derefs"]),
              "ptables": set(spec["ptables"]), "tptrs": set(spec["tptrs"]),
              "rels": set(spec["rels"]), "decodes": dict(spec["decodes"]),
              "last": spec["last"],
              "span": stride if (lvl == "embed" and stride) else child_size}
        if lvl == "embed" and stride:
            # the declared element count of THIS alternative, read from the child's own route text (the alt tuple
            # carries no count); _fold_element uses it to fold element k > 0 onto element 0
            mc = re.search(r"EMBED\s+%s\s*\+\s*0x0*%X\s+stride=0x0*%X\s+count=(\d+)" % (re.escape(str(parent)), off, stride),
                           str(routes.get(child, "")), re.I)
            d2["count"] = int(mc.group(1)) if mc else 1
        for j, e in enumerate([off] + extras):
            d2["rebase"] += e
            lk = lvl if j == 0 else "ptr"
            if lk in ("ptr", "ptable", "ptable_ptr"):
                d2["derefs"].add(d2["rebase"])
                d2["last"] = d2["rebase"]
                if lk == "ptable":
                    d2["ptables"].add(d2["rebase"])
                elif lk == "ptable_ptr":
                    d2["tptrs"].add(d2["rebase"])
            elif lk == "rel":
                d2["rels"].add(d2["rebase"])
                d2["last"] = d2["rebase"]
            elif lk == "pkref":
                # the member's dword is the rel-offset-like load (marks `rels`), and
                # `call FN` with rcx carrying it yields the child base at this same
                # coordinate - `rebase` stays put, so the window opens here.
                d2["rels"].add(d2["rebase"])
                d2["decodes"][alt[3]] = d2["rebase"]
                d2["last"] = d2["rebase"]
        return d2

    zero = {"rebase": 0, "derefs": set(), "ptables": set(), "tptrs": set(),
            "rels": set(), "decodes": {}, "last": 0}
    if isinstance(parent, int):
        # `PKREF 0xFN 0xCELL +0xOFF` - the parent is a bare global cell (a band-shared
        # header's registry slot). Synthesise the PTR-on-cell root: the cell load seeds
        # coordinate 0, the member dword marks `rels`, the resolver call marks rax.
        specs.append((("PTR", parent, 0, 0), "PTR 0x%08X" % parent, fold(zero),
                      "pkref *%08X +0x%X" % (parent, off)))
        return specs, fails
    if parent in seen:
        return [], ["chain cycle through %s" % parent]
    ptext_route = routes.get(parent)
    if ptext_route is None:
        return [], ["parent %s not in the store" % parent]
    palts = parse_routes(ptext_route)
    if not palts:
        fails.append("parent %s route unmodelled" % parent)
    for prule, ptext in palts:
        if prule[0] in SEEDABLE:
            specs.append((prule, ptext, fold(zero),
                          "%s %s +0x%X" % (kind.lower(), parent, off)))
        elif prule[0] in DERIVED:
            sub, sf = derive_specs(types, fields, routes, parent, prule, seen | {parent})
            for rrule, rtext, rspec, rpath in sub:
                specs.append((rrule, rtext, fold(rspec),
                              "%s %s +0x%X via %s"
                              % (kind.lower(), parent, off, rpath)))
            fails += sf
        else:
            fails.append("parent %s alternative %r unmodelled" % (parent, ptext[:40]))
    return specs, fails


def prologue_adjust(img, entry):
    """How far rsp has moved below the entry rsp once the prologue is done, or None.

    THIS IS THE WHOLE RISK OF STACK-ARGUMENT SEEDING and it is why the feature was proposed
    before it was written: the FIFTH argument lives at `entry_rsp + 0x28`, but inside the body
    it is addressed as `[rsp + adjust + 0x28]`, and getting `adjust` wrong attributes another
    object's displacements to this one.

    Only three shapes are accepted, and anything else STOPS the scan and returns None rather
    than guessing: `push reg` (8), `sub rsp, imm` (imm), and a home-slot save
    `mov [rsp + N], reg`, which does not move rsp at all. A function that touches rsp any other
    way - a dynamic alloca, `lea rsp`, a frame pointer - is refused.

    Worked against 0051F9F0, whose prologue is four home saves, `push r14` and `sub rsp,0x20`:
    adjust = 0x28, so its `mov rax, qword ptr [rsp + 0x50]` is `entry_rsp + 0x28`, the FIFTH
    argument. That is the read this feature exists to follow, and it was checked by hand - and
    mis-read as the sixth on the first pass - before any of this was written.
    """
    body = img.body(entry)
    if not body:
        return None
    adjust = 0
    for i in body:
        m = i.mnemonic
        if m == "push":
            adjust += 8
            continue
        if (m == "sub" and len(i.operands) == 2
                and i.operands[0].type == X86_OP_REG
                and W.norm(i.operands[0].reg) == X.X86_REG_RSP
                and i.operands[1].type == X86_OP_IMM):
            adjust += i.operands[1].imm
            continue
        if (m == "mov" and len(i.operands) == 2
                and i.operands[0].type == X86_OP_MEM
                and W.norm(i.operands[0].value.mem.base) == X.X86_REG_RSP
                and not i.operands[0].value.mem.index):
            continue                      # home-slot save; rsp unchanged
        break
    return adjust


class Census(object):
    def __init__(self, img, size):
        self.img = img
        self.size = size
        self.t = W.Taint(img)
        self.rows = []      # (fn, site, disp, base, kind, text, zero) - the artifact
        self.rule_text = ""  # which route alternative is currently being walked
        self.edges = set()  # (caller, callee) along the descent - for exposure propagation
        # AN `ARRAY` ROUTE'S ELEMENT BASE IS COMPUTED, NOT LOADED, and that is why seventeen
        # ARRAY-routed types had no census: `AiOrderSet` is reached as
        # `imul r13, rax, 0x170` then `add r13, <the lea'd array base>`, so the element
        # pointer never exists as a load this walker could seed. Set `stride` and the walk
        # recognises that two-instruction shape and seeds the result at offset 0.
        # OFF BY DEFAULT: with `stride` None the extra state stays empty and every existing
        # census is byte-identical, which is checked rather than asserted.
        self.stride = None
        # `PARRAY` element arithmetic: the pointer-table load seeds a register at -OFF (the
        # block base), and an element base then reads `block + OFF + i*S`. With parray_off None
        # every check below reduces to `== 0` and existing censuses are byte-identical.
        self.parray_off = None
        # DERIVED (CHAIN/RELOFF/EMBED) RUNS. Set by the driver to the spec `derive_specs`
        # returns; the seed rule passed to `run` is then the ROOT parent's route and `off`
        # stays in root-object coordinates end to end - a register holding the child is the
        # register whose `off` equals `rebase` (a pointer member is seeded to its own field
        # offset, so `*(p + OFF)` yields `off == OFF` downstream). Emission filters to
        # `rebase <= disp < rebase + span` with the register's base at `last` or deeper, which
        # is what excludes the pointer fetch itself (a read through a shallower register).
        # `None` everywhere else: every existing census is byte-identical.
        self.derived = None
        # BANK-QUALIFIED FN SEEDING: when the rule carries `bank=0xD`, the set of
        # (entry, call-site) pairs whose rcx provenance resolves to that slot.
        # None disables the gate - unqualified FN rules seed every caller return
        # exactly as before. Set per rule inside run().
        self.fn_sites = None

    def walk(self, entry, seed, acc, fwd, seed_rule, stack_seed=None):
        starts, blocks, succ = self.t._blocks(entry)
        if not starts:
            return
        # STACK-ARGUMENT SEED: (slot, offset) for a slot of 5 or more, which arrives on the
        # stack and never in a register. Resolved to the one displacement the body will use.
        want_disp = None
        if stack_seed:
            adj = prologue_adjust(self.img, entry)
            if adj is None:
                return                    # unrecognised prologue - refuse rather than guess
            want_disp = adj + 8 * stack_seed[0]
        # The mark a register carries when it holds "the array's base". 0 for ARRAY (the lea'd
        # table IS element 0's base); -OFF for PARRAY (the loaded block base, OFF before the
        # array start). Every composition check is written against this so ARRAY walks are
        # byte-identical to before.
        bmk = -self.parray_off if self.parray_off is not None else 0
        img = self.img
        fsize = img.sizes.get(entry, 0)
        # PER-BLOCK STATE rides `state` as (off, tptr, elems, zero): `off` merges by
        # agreement as before, and the two table-provenance maps now cross block
        # boundaries the same way because the table-pointer load and the element fetch
        # live in different blocks of every iteration loop (pBegin loads in the entry
        # block, `mov e,[it]` in the loop body). `elems` merges by membership
        # intersection - conservative, like the off merge: it can lose a fact, never
        # invent one. `zero` merges by intersection too - a register is provably zero at
        # a join only when EVERY predecessor proves it - and its only use is the
        # null-coalesce rule in the merge below, where a provably-zero alternative does
        # not contradict a mark.
        state = {starts[0]: (dict(seed), {}, set(), set())}
        work = collections.deque([starts[0]])
        n = 0
        while work and n < 20000:
            n += 1
            b = work.popleft()
            off = dict(state[b][0])
            tptr_end = dict(state[b][1])
            elems_end = set(state[b][2])
            # REGISTERS PROVABLY HOLDING ZERO, seeded from the merged predecessor set -
            # intersection semantics, so a register arrives provably zero only when every
            # predecessor proved it. The merged set feeds exactly one thing: the
            # null-coalesce rule in the successor merge, where a mark survives a
            # predecessor that proves the register NULL instead (`x ? marked : 0`
            # codegen - the access through the register on the null side is a dead
            # null-deref, so the mark honestly stands). It is never consulted inside the
            # block walk itself, so the discipline is unchanged: it can miss a zero,
            # never invent one.
            zero = set(state[b][3])
            # Registers holding a multiple of an ARRAY route's stride. Same discipline as
            # `zero`: per block, never merged, so it can miss an element base but cannot
            # invent one.
            mult = set()
            # OUTGOING STACK ARGUMENTS staged for the next call: {rsp displacement: offset}.
            # Same per-block discipline as `zero` and `mult` - never merged across blocks, so
            # it can miss an argument but cannot invent one.
            outgoing = {}
            # REGISTERS HOLDING THE IMAGE BASE. Same per-block discipline as `zero`, `mult` and
            # `outgoing`. The IMAGE-BASE-RELATIVE IDIOM builds an address as `lea rX,[rip->
            # 0x120000]` then `lea rY,[rX + RVA]`, so the table address never appears as a
            # direct lea and an ARRAY route seeded on one is never seeded at all. That cost a
            # real declaration: ActorManagerSlot +0x244 was written `unobserved` on 2026-09-20
            # while ActorManager_BindLoadedDefinitionPayload was zeroing eight qwords there
            # through exactly this shape.
            imgbase = set()
            # REGISTERS HOLDING A SLOTPTR TABLE BASE, reg -> the lea'd address. The common
            # codegen is two instructions - `lea rB,[rip->ADDR]` then `mov rX,[rB + i*S]`
            # with disp 0 - which no single-instruction seed sees: BattleUnit's party
            # table `022C1788` is lea'd in 13 functions and indexed nowhere else. The
            # BIASED form leas an enclosing base and lets the load's displacement finish
            # the address - `lea rB,[02098E10]` then `mov rX,[rB + i*0x288 + 8]` reaches
            # table `02098E18` - so the register carries its lea'd value and the load
            # gate is `value + disp == ADDR` exactly. Same per-block discipline as
            # `imgbase`.
            tablebase = {}
            # REGISTERS HOLDING AN INDIRECT TABLE BASE (`PTABLE 0xADDR`): the register was
            # loaded with `*(ADDR)`, the table's runtime address - the value is unknowable,
            # so the mark is presence-only. A qword load `[b + i*S + k]` or `[b + k]` off
            # one fetches a table slot - an element pointer - and yields an element base.
            ptab = set()
            # REGISTERS HOLDING A LOADED TABLE POINTER of a derived `SLOTPTR` level:
            # reg -> the table's root-coordinate mark. `mov t,[b+M]` with M a ptable
            # mark loads `t` with the heap table itself; every qword load off `t`
            # then fetches an ELEMENT. The dict carries the mark separately from
            # `off` so a slot-iterating `add t,8` doesn't drift the child window.
            # Carried across blocks through `state` - unlike `mult`/`rels` this is
            # provenance, not value shape, so a predecessor that proved it is evidence.
            tptr = tptr_end
            # REGISTERS WHOSE MARK CAME THROUGH A TABLE SLOT FETCH. Needed because a
            # derived ptable level can land on the parent's OWN mark (OrderedObject's
            # table sits at mark 0 - the embedded vector's base): without provenance a
            # `mov rax,[v+8]` read of the vector's pEnd is indistinguishable from an
            # element's field read and would fabricate child rows. The set cannot cross
            # a call boundary - a callee's use of an element argument is missed, not
            # misattributed - but it does cross block boundaries through `state`.
            elems = elems_end
            # REL-OFFSET DWORDS of a derived (RELOFF) spec: reg -> the root-coordinate offset
            # its value was loaded from. The base register combines with one below
            # (`add t,p` / `lea d,[p+t]`) to yield the child base. Same per-block discipline.
            rels = {}
            dv = self.derived
            for i in blocks[b]:
                m = i.mnemonic
                # A MULTI-BYTE NOP IS NOT AN ACCESS. `nop dword ptr [rax]` and
                # `nop word ptr [rax + rax]` are alignment padding that happen to ENCODE a
                # memory operand; they read and write nothing. Recorded as accesses they
                # manufacture evidence out of padding. Measured across the store on
                # 2026-09-20: 60 such rows in 14 committed artifacts, and exactly ONE offset
                # whose only evidence was a nop - ManagerSingleton0209BE80 +0x0, already
                # declared an unobserved span, so no field row ever rested on one. Skipped
                # wholly, which is safe because a nop also writes no register.
                if m.startswith("nop"):
                    continue
                for o in i.operands:
                    if o.type != X86_OP_MEM:
                        continue
                    mm = o.value.mem
                    # THE ELEMENT BASE FOLDED INTO THE OPERAND - a THIRD form of the computed
                    # element base, and the one that cost a store row its citation. 0036C5A0
                    # writes `mov [rcx + rax + 0xa0], rdx` with rcx = id*0xA8 and rax the lea'd
                    # table base: the element pointer is never materialised in a register at
                    # all, so neither the `add` handler nor this one saw it, and the ONLY row
                    # the old census produced for ImageAddressArenaRecord came instead from
                    # that function's OUT-OF-BOUNDS path (`xor eax,eax` then
                    # `mov [rax + 0xa0], rdx` - a null-write trap, base zero, not an access to
                    # any record). The store's `tailQword00A0` cited that trap as its evidence.
                    # STRICTLY scale 1 and strictly one side marked `mult` with the other at
                    # the array's base mark: at any other scale the index is an INNER array's
                    # subscript (`[rbx + rdi*4 + 0x68]` is a counter element), which stays
                    # refused because its value is unknown - the existing conservative rule.
                    # The ONE widening past it: a PARRAY walk also accepts scale == the route's
                    # own stride with the base at the mark, because that scale IS the element
                    # stride and the multiply is the route's own indexing, not an inner array's.
                    if mm.index:
                        bn, xn = W.norm(mm.base), W.norm(mm.index)
                        if (self.parray_off is not None and self.stride
                                and mm.scale == self.stride
                                and off.get(bn) == bmk):
                            # THE PARRAY FOLDED ACCESS - `[block + i*S + OFF + f]`: the scale
                            # does the multiply on a RAW index, so `mult` is not involved.
                            # disp OFF+f resolves to field f via the -OFF the load seeded.
                            d = off[bn] + mm.disp
                        elif (self.stride and mm.scale == 1
                                and ((bn in mult and off.get(xn) == bmk)
                                     or (xn in mult and off.get(bn) == bmk))):
                            d = bmk + mm.disp
                        elif dv and bn in off:
                            # AN ELEMENT-RELATIVE FIELD LOAD under a derived run -
                            # `[array + i*S + f]` with `array` marked never materialises
                            # the element base in a register, but the displacement is
                            # still element field f: the mark does the fold. The same
                            # emit gate applies, INCLUDING the element-provenance check
                            # - an indexed load off a table-pointer register is a slot
                            # fetch handled below, not a field access.
                            d = off[bn] + mm.disp
                            breg = off[bn]
                            d, breg = _fold_element(dv, d, breg)
                            if not (dv["rebase"] <= d < dv["rebase"] + dv["span"]
                                    and breg >= dv["last"]
                                    and ((breg not in dv["ptables"]
                                          and breg not in dv["tptrs"])
                                         or bn in elems)):
                                continue
                            kd = RT.op_kind(i, o, list(i.operands).index(o))
                            self.rows.append((entry, i.address, d - dv["rebase"],
                                              breg - dv["rebase"], kd,
                                              m + " " + i.op_str, False))
                            acc[d - dv["rebase"]].add((entry, i.address,
                                                       breg - dv["rebase"]))
                            continue
                        else:
                            continue
                        if dv:
                            d, _ = _fold_element(dv, d, d)
                            if not (dv["rebase"] <= d < dv["rebase"] + dv["span"]
                                    and dv["last"] == 0):
                                continue
                            d -= dv["rebase"]
                        elif not (0 <= d < self.size):
                            continue
                        kd = RT.op_kind(i, o, list(i.operands).index(o))
                        self.rows.append((entry, i.address, d,
                                          -dv["rebase"] if dv else 0, kd,
                                          m + " " + i.op_str, False))
                        acc[d].add((entry, i.address,
                                    -dv["rebase"] if dv else 0))
                        continue
                    if W.norm(mm.base) not in off:
                        continue
                    breg = off[W.norm(mm.base)]
                    d = breg + mm.disp
                    if dv:
                        d, breg = _fold_element(dv, d, breg)
                        # DERIVED RUN: emit only the child's window, and only when the
                        # register the access came through stood at the deepest deref or
                        # below - `base >= last` is what keeps the pointer fetch itself
                        # (a read through the parent, base < last) out of the census. A
                        # TABLE marks further require ELEMENT provenance: a mark can
                        # coincide with a parent coordinate (a table at +0x00 stands at
                        # the parent's own base), and only a register that fetched a
                        # slot is an element - a plain mark-0 read of the parent's own
                        # fields must not become a child row.
                        if not (dv["rebase"] <= d < dv["rebase"] + dv["span"]
                                and breg >= dv["last"]
                                and ((breg not in dv["ptables"]
                                      and breg not in dv["tptrs"])
                                     or W.norm(mm.base) in elems)):
                            continue
                        d -= dv["rebase"]
                        breg -= dv["rebase"]
                    elif not (0 <= d < self.size):
                        continue
                    # THE ARTIFACT, recorded beside the summary rather than instead of it.
                    # This tool printed a report and wrote no file, so its results were
                    # citable but not re-readable - and on 2026-09-19 that cost twice: two
                    # types carried rows citing a census run that existed only in a console,
                    # and check_census_widths.py had never compared one of their offsets
                    # because there was no file for the map to name. `acc` keeps only
                    # (function, site, base) and a width check needs the INSTRUCTION, so the
                    # detail is accumulated here in parallel. `acc` is untouched: every
                    # existing consumer of it reads the same tuples it always did.
                    kd = RT.op_kind(i, o, list(i.operands).index(o))
                    # IS THIS A STORE OF A REGISTER THAT IS PROVABLY ZERO? Twice now the
                    # same shape has had to be read by hand - BootSingleton01F7F598
                    # +0xD00/+0xD08, and ManagerSub0209BE80_7EA0's four `void*` rows whose
                    # ENTIRE evidence was 0028CA40's `xor eax,eax` followed by six
                    # `mov qword ptr [rcx+N], rax`. A store of a zeroed register says the
                    # bytes are cleared; it says nothing about where the field boundaries
                    # are, and read as a field list it invents one field per store.
                    # The flag is recorded per access; whether a RUN of them is a clear is
                    # decided after the walk, where the neighbours are visible.
                    z = (kd == "w" and len(i.operands) == 2
                         and i.operands[1].type == X86_OP_REG
                         and W.norm(i.operands[1].reg) in zero)
                    self.rows.append((entry, i.address, d, breg,
                                      kd, m + " " + i.op_str, z))
                    # RECORD THE BASE, NOT ONLY THE OFFSET. An access at absolute
                    # +0x223 reached as [rcx+0xA3] with rcx = base+0x180 is a field
                    # of a NESTED object, not a field of this one. Dropping the base
                    # is what turned this census's output into a flat field list that
                    # had to be withdrawn; it was in hand at the moment of the access
                    # all along.
                    acc[d].add((entry, i.address, breg))
                # ARRAY seeds EXACTLY as STATIC does - the `lea` of the table base at offset 0.
                # That is what the computed-element-base handler needs: it combines a register
                # marked `mult` (holding i*stride) with one already at offset 0, so the base
                # must be seeded for the `add` to mean anything. Element 0 and the table base
                # are the same address, so an unindexed access through the base is an element-0
                # field and is recorded as one.
                if seed_rule and seed_rule[0] in ("STATIC", "ARRAY"):
                    v = W.lea_value(i)
                    if v == seed_rule[1]:
                        off[W.norm(i.operands[0].reg)] = 0
                        continue
                if m == "lea" and len(i.operands) == 2 \
                        and i.operands[0].type == X86_OP_REG \
                        and i.operands[1].type == X86_OP_MEM:
                    mm = i.operands[1].value.mem
                    d = W.norm(i.operands[0].reg)
                    ptab.discard(d)     # a lea rewrites d; carried back below off a table reg
                    elems.discard(d)    # same for element provenance
                    tptr.pop(d, None)   # and for a derived table pointer
                    # THE IMAGE-BASE-RELATIVE IDIOM, in its two halves.
                    v = W.lea_value(i)
                    if v == self.img.base:
                        imgbase.add(d)
                        off.pop(d, None)
                        continue
                    if seed_rule and seed_rule[0] == "SLOTPTR":
                        # the lea'd value, under either addressing form - the biased
                        # window accepts a table base lea'd up to 0x400 BELOW the route
                        # address (an enclosing array/struct base); the load gate below
                        # still requires value + disp == ADDR exactly, so a low lea
                        # alone seeds nothing.
                        tv = None
                        if v is not None and 0 <= seed_rule[1] - v <= 0x400:
                            tv = v
                        elif (W.norm(mm.base) in imgbase and not mm.index
                                and 0 <= seed_rule[1] - (self.img.base + mm.disp) <= 0x400):
                            tv = self.img.base + mm.disp
                        if tv is not None:
                            # the register now holds the TABLE address (or its biased
                            # base), not an object
                            tablebase[d] = tv
                            imgbase.discard(d)
                            continue
                    # AN ELEMENT BASE OFF A TABLE BASE - `lea d,[rB + i*S]` - keeps the
                    # table mark: the loaded value is still `table - bias`, the index
                    # lives in the slot choice, and the load's disp finishes `ADDR`.
                    if (seed_rule and seed_rule[0] == "SLOTPTR" and mm.index
                            and W.norm(mm.base) in tablebase):
                        tablebase[d] = tablebase[W.norm(mm.base)]
                        imgbase.discard(d)
                        off.pop(d, None)
                        rels.pop(d, None)
                        continue
                    # the same holds for an INDIRECT table base: `lea d,[b + i*S + k]`
                    # or `lea d,[b + k]` still addresses a slot of the same table
                    if ptab and W.norm(mm.base) in ptab:
                        ptab.add(d)
                        imgbase.discard(d)
                        off.pop(d, None)
                        rels.pop(d, None)
                        continue
                    # and for a DERIVED table pointer: `lea d,[t + i*S + k]` addresses
                    # another slot of the table `t` holds - still a table pointer
                    if W.norm(mm.base) in tptr:
                        off[d] = tptr[W.norm(mm.base)]
                        tptr[d] = tptr[W.norm(mm.base)]
                        imgbase.discard(d)
                        rels.pop(d, None)
                        continue
                    if (seed_rule and W.norm(mm.base) in imgbase and not mm.index
                            and self.img.base + mm.disp == seed_rule[1]):
                        off[d] = 0            # image base + RVA IS the seeded address
                        imgbase.discard(d)
                        continue
                    # A PARRAY ELEMENT BASE formed by indexed lea - `lea e,[block + i*S + OFF]`
                    # with the raw index, or `lea e,[block + mult]` with the imul'd product.
                    # The result is element-relative: off = mark + disp.
                    if self.parray_off is not None and self.stride and mm.index:
                        bn, xn = W.norm(mm.base), W.norm(mm.index)
                        hit = None
                        if xn in mult and off.get(bn) == bmk:
                            hit = off[bn] + mm.disp
                        elif bn in mult and off.get(xn) == bmk:
                            hit = off[xn] + mm.disp
                        elif mm.scale == self.stride and off.get(bn) == bmk:
                            hit = off[bn] + mm.disp
                        if hit is not None:
                            imgbase.discard(d)
                            off[d] = hit
                            continue
                    # A REL-OFFSET COMBINE - `lea d,[base + rel]` where `rel` holds a dword
                    # loaded from the RELOFF member and `base` is the object base. The
                    # result stands at the rel member's own offset in root coordinates.
                    if dv and mm.index and mm.scale == 1:
                        bn2, xn2 = W.norm(mm.base), W.norm(mm.index)
                        if xn2 in rels and off.get(bn2) == 0:
                            off[d] = rels[xn2] + mm.disp
                            rels.pop(d, None)
                            imgbase.discard(d)
                            continue
                        if bn2 in rels and off.get(xn2) == 0:
                            off[d] = rels[bn2] + mm.disp
                            rels.pop(d, None)
                            imgbase.discard(d)
                            continue
                    # AN ELEMENT BASE OFF A TRACKED BASE under a derived run -
                    # `lea d,[b + i*S + x]` with b marked. The index product is unknowable,
                    # but the result is the i-th element of an array whose base sits at
                    # off[b]+x in root coordinates - the same mark the ARRAY route gives a
                    # computed element. This is how the rel-offset arrays are actually
                    # subscripted (`lea rcx,[rdx + rsi*8]` once rdx = header + rel). Derived
                    # runs only: a plain walk keeps dropping the register rather than
                    # guessing which array an index belongs to.
                    if dv and mm.index and W.norm(mm.base) in off:
                        off[d] = off[W.norm(mm.base)] + mm.disp
                        if W.norm(mm.base) in elems:
                            elems.add(d)
                        rels.pop(d, None)
                        imgbase.discard(d)
                        continue
                    imgbase.discard(d)
                    rels.pop(d, None)
                    if W.norm(mm.base) in off and not mm.index:
                        off[d] = off[W.norm(mm.base)] + mm.disp
                        if W.norm(mm.base) in elems:
                            elems.add(d)
                    else:
                        off.pop(d, None)
                    continue
                if m in ("add", "sub") and len(i.operands) == 2 \
                        and i.operands[0].type == X86_OP_REG:
                    d = W.norm(i.operands[0].reg)
                    # THE ELEMENT BASE OF AN `ARRAY` ROUTE IS FORMED HERE, and this check has
                    # to live INSIDE this handler rather than after it: the handler below
                    # `continue`s on every add, so a check placed later never sees the one
                    # instruction that matters. That cost a wrong "0 offsets" reading before
                    # it was found.
                    if ((self.stride or dv) and m == "add"
                            and i.operands[1].type == X86_OP_REG):
                        s2 = W.norm(i.operands[1].reg)
                        # the base a product lands on is bmk for a plain array route and
                        # `rebase` under a derived run - the child base stands at the
                        # member coordinate, not at 0 (StatusDefinitionRecord's
                        # `add ecx, edx` folds stride*index onto the decoded base).
                        bases = ((bmk, dv["rebase"]) if dv else (bmk,))
                        if d in mult and off.get(s2) in bases:
                            off[d] = off[s2]    # index unknown; displacements are element-relative
                            mult.discard(d)
                            elems.discard(d)
                            continue
                        if s2 in mult and off.get(d) in bases:
                            mult.discard(s2)
                            continue
                    # `add rel, base` or `add base, rel` - the RELOFF combine in its add
                    # form; either way the destination comes out holding the child base
                    # in root coordinates.
                    if dv and m == "add" and i.operands[1].type == X86_OP_REG:
                        s2 = W.norm(i.operands[1].reg)
                        if d in rels and off.get(s2) == 0:
                            off[d] = rels.pop(d)
                            elems.discard(d)
                            continue
                        if s2 in rels and off.get(d) == 0:
                            off[d] = rels[s2]
                            elems.discard(d)
                            continue
                    if d in off and i.operands[1].type == X86_OP_IMM:
                        off[d] += i.operands[1].imm if m == "add" else -i.operands[1].imm
                    else:
                        off.pop(d, None)
                        rels.pop(d, None)
                        elems.discard(d)
                    # A TABLE BASE FOLLOWS THE SAME ARITHMETIC: an immediate moves the
                    # lea'd value itself, a tracked index product keeps the mark (the
                    # element-base formation `add rS, i*S` still indexes the same table
                    # through the load's disp), and any other operand makes the address
                    # unknowable - the mark dies rather than drift.
                    if d in tablebase:
                        if i.operands[1].type == X86_OP_IMM:
                            tablebase[d] += (i.operands[1].imm if m == "add"
                                             else -i.operands[1].imm)
                        elif not (i.operands[1].type == X86_OP_REG
                                  and W.norm(i.operands[1].reg) in mult):
                            tablebase.pop(d, None)
                    # an INDIRECT table base keeps its mark through an immediate or a
                    # tracked index product - both still address the same table; anything
                    # else makes the register unknowable and the mark dies
                    if d in ptab and not (
                            i.operands[1].type == X86_OP_IMM
                            or (i.operands[1].type == X86_OP_REG
                                and W.norm(i.operands[1].reg) in mult)):
                        ptab.discard(d)
                    # a DERIVED table pointer iterates slots the same way
                    if d in tptr and not (
                            i.operands[1].type == X86_OP_IMM
                            or (i.operands[1].type == X86_OP_REG
                                and W.norm(i.operands[1].reg) in mult)):
                        tptr.pop(d, None)
                    continue
                # STAGING AN OUTGOING STACK ARGUMENT: `mov [rsp + N], reg` with reg tracked.
                # N of 0x20 is the fifth argument, 0x28 the sixth. Recorded, not acted on -
                # the call handler below turns it into a descent.
                if (m == "mov" and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_MEM
                        and i.operands[1].type == X86_OP_REG):
                    om = i.operands[0].value.mem
                    if (W.norm(om.base) == X.X86_REG_RSP and not om.index
                            and om.disp >= 0x20 and om.disp % 8 == 0
                            and W.norm(i.operands[1].reg) in off):
                        outgoing[om.disp] = off[W.norm(i.operands[1].reg)]
                if m == "mov" and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG:
                    d = W.norm(i.operands[0].reg)
                    rels.pop(d, None)     # mov always rewrites d; a stale rel mark dies here
                    ptab.discard(d)       # same for a table mark - carried back below if copied
                    elems.discard(d)
                    tptr.pop(d, None)
                    s = i.operands[1]
                    # THE CALLEE PICKING UP ITS STACK ARGUMENT - the one load this seed exists
                    # for. Exactly the displacement the prologue scan resolved, nothing near it.
                    if (want_disp is not None and s.type == X86_OP_MEM
                            and W.norm(s.value.mem.base) == X.X86_REG_RSP
                            and not s.value.mem.index and s.value.mem.disp == want_disp):
                        off[d] = stack_seed[1]
                        continue
                    if s.type == X86_OP_REG and W.norm(s.reg) in off:
                        off[d] = off[W.norm(s.reg)]
                        if W.norm(s.reg) in elems:
                            elems.add(d)
                        if W.norm(s.reg) in tptr:
                            tptr[d] = tptr[W.norm(s.reg)]
                        rels.pop(d, None)
                        continue
                    # a TABLE BASE copies like any other address register
                    if s.type == X86_OP_REG and W.norm(s.reg) in tablebase:
                        tablebase[d] = tablebase[W.norm(s.reg)]
                        off.pop(d, None)
                        rels.pop(d, None)
                        mult.discard(d)
                        continue
                    # so does an INDIRECT table base (`PTABLE 0xADDR`)
                    if s.type == X86_OP_REG and W.norm(s.reg) in ptab:
                        ptab.add(d)
                        off.pop(d, None)
                        rels.pop(d, None)
                        mult.discard(d)
                        continue
                    # THE DERIVED DEREFERENCE: `mov d,[b + k]` with `b` tracked and
                    # `off[b] + k` a declared chain offset loads the next level's pointer -
                    # the loaded register then STANDS AT that offset in root coordinates,
                    # which is what lets `d`'s own `[d + f]` accesses record as child
                    # fields. A `rels` offset loads the rel-offset dword instead, to be
                    # combined with the base by the add/lea handlers.
                    if dv and s.type == X86_OP_MEM:
                        mm3 = s.value.mem
                        b3 = off.get(W.norm(mm3.base))
                        # A TABLE-POINTER DEREFERENCE FETCHES AN ELEMENT: any qword load
                        # `[t + i*S + k]` or `[t + k]` off a `tptr` register - one proven
                        # to hold a `SLOTPTR` table's pointer. The element stands at the
                        # TABLE'S mark (the tptr value), not the register's possibly
                        # drifted mark, so a slot-iterating `add t,8` doesn't shift the
                        # child window. Mark-matching the base alone is not enough: for
                        # a table at mark 0 the parent itself stands there, and indexing
                        # the PARENT would fabricate elements.
                        if s.size == 8 and W.norm(mm3.base) in tptr:
                            off[d] = tptr[W.norm(mm3.base)]
                            elems.add(d)
                            rels.pop(d, None)
                            continue
                        if b3 is not None:
                            t3 = b3 + mm3.disp
                            # AN INLINE TABLE ELEMENT: `[b + i*S + M]` or slot 0 `[b + M]`
                            # where M is a `ptable` mark - the object IS the table and the
                            # load yields an element directly.
                            if s.size == 8 and t3 in dv["ptables"]:
                                off[d] = t3
                                elems.add(d)
                                rels.pop(d, None)
                                continue
                            if not mm3.index and t3 in dv["derefs"]:
                                off[d] = t3
                                if t3 in dv["tptrs"]:
                                    # the loaded register holds THE TABLE POINTER -
                                    # the provenance an element fetch above requires
                                    tptr[d] = t3
                                rels.pop(d, None)
                                continue
                            # A RELOFF MEMBER IS AN int32 - only a dword load of it is the
                            # rel idiom; a qword `mov` spanning the member is an adjacent
                            # field's read and must not mark `rels`.
                            if t3 in dv["rels"] and s.size == 4:
                                rels[d] = t3
                                off.pop(d, None)
                                continue
                    if (seed_rule and seed_rule[0] == "PTR" and s.type == X86_OP_MEM
                            and not s.value.mem.index
                            and W.rip_target(i, s) == seed_rule[1]):
                        off[d] = -seed_rule[2]
                        continue
                    if (seed_rule and seed_rule[0] == "PARRAY"
                            and s.type == X86_OP_MEM):
                        mm2 = s.value.mem
                        # THE BLOCK BASE, loaded: `mov d,[rip->ADDR]` (rip form) or
                        # `mov d,[rB + ADDR-imgbase]` (image-base-relative). Either leaves d
                        # holding *(ADDR), the block base - OFF before the array start.
                        if not mm2.index and (
                                W.rip_target(i, s) == seed_rule[1]
                                or (W.norm(mm2.base) in imgbase
                                    and self.img.base + mm2.disp == seed_rule[1])):
                            off[d] = -seed_rule[2]
                            continue
                    if (seed_rule and seed_rule[0] == "SLOTPTR"
                            and s.type == X86_OP_MEM):
                        mm2 = s.value.mem
                        # A POINTER TABLE: `mov d,[rip->ADDR]` is instance 0 (`*(ADDR)`);
                        # `mov d,[i*S + ADDR]` (absolute) or `[rB + i*S + ADDR-imgbase]`
                        # (image-base) is instance i - each yields an object base directly.
                        if not mm2.index and (
                                W.rip_target(i, s) == seed_rule[1]
                                or (W.norm(mm2.base) in imgbase
                                    and self.img.base + mm2.disp == seed_rule[1])
                                or (W.norm(mm2.base) in tablebase
                                    and tablebase[W.norm(mm2.base)] + mm2.disp
                                    == seed_rule[1])):
                            off[d] = 0
                            continue
                        # an x86 scale tops out at 8 - a wider stride arrives as an
                        # `imul`/`shl` product in `mult` with scale 1, so the index
                        # test is `scale == stride OR index holds a tracked product`.
                        # The address gate (`value + disp == ADDR` or the absolute/
                        # image-base forms) is what keeps this honest.
                        if (mm2.index and (mm2.scale == seed_rule[3]
                                           or W.norm(mm2.index) in mult)
                                and ((not mm2.base and mm2.disp == seed_rule[1])
                                     or (W.norm(mm2.base) in imgbase
                                         and self.img.base + mm2.disp == seed_rule[1])
                                     or (W.norm(mm2.base) in tablebase
                                         and tablebase[W.norm(mm2.base)] + mm2.disp
                                         == seed_rule[1]))):
                            off[d] = 0
                            continue
                    if (seed_rule and seed_rule[0] == "PTABLE"
                            and s.type == X86_OP_MEM):
                        mm2 = s.value.mem
                        # THE TABLE-BASE LOAD: `mov d,[rip->ADDR]` or the image-base
                        # `[rB + ADDR-imgbase]` - d then holds `*(ADDR)`, the runtime
                        # address of the pointer table. Qword-gated: the cell holds a
                        # pointer and anything narrower is not the table base.
                        if not mm2.index and s.size == 8 and (
                                W.rip_target(i, s) == seed_rule[1]
                                or (W.norm(mm2.base) in imgbase
                                    and self.img.base + mm2.disp == seed_rule[1])):
                            ptab.add(d)
                            continue
                    # A TABLE SLOT FETCH: `mov d,[b + i*S + k]` or `mov d,[b + k]` off a
                    # ptab-marked register loads element (i + k/S)'s POINTER - d becomes
                    # an element base, exactly like a scalar derived deref. The table
                    # base can also ride in the INDEX operand - `mov rbx,[rsi + rax]`
                    # with rax = *(ADDR) walks rsi up the slots (007AAEA0 does exactly
                    # this). Qword-gated: a narrower read of a slot is part of a
                    # pointer, not an element.
                    if ptab and s.type == X86_OP_MEM and s.size == 8:
                        mm4 = s.value.mem
                        if (W.norm(mm4.base) in ptab
                                or (mm4.index and W.norm(mm4.index) in ptab)):
                            off[d] = 0
                            elems.add(d)
                            ptab.discard(d)
                            continue
                    off.pop(d, None)
                    tablebase.pop(d, None)   # a mov rewrites d; a stale table mark dies
                    ptab.discard(d)
                    continue
                # THE SIGN/ZERO-EXTENDING WRITES the `mov` branch never saw. They matter for
                # exactly two things: a RELOFF level's int32 is loaded by
                # `movsxd d, dword [b+k]` (the MapRefImageHeader idiom at 0026D9xx - a `mov`
                # load never fires for it), and a reg->reg extension like `movsxd rsi, eax`
                # carries an existing mark across the widening. Everything else just rewrites
                # d, and its marks die here exactly as the fallthrough already did. The rel
                # load is gated on the operand being DWORD-sized (`s.size == 4`): a narrower
                # read at the same base - `movzx ebp, word [elem]` on an element base - is a
                # FIELD read, not the rel dword, and must not mark anything.
                if (m in ("movsx", "movzx", "movsxd") and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_REG):
                    d = W.norm(i.operands[0].reg)
                    off.pop(d, None)
                    rels.pop(d, None)
                    mult.discard(d)
                    tablebase.pop(d, None)
                    imgbase.discard(d)
                    ptab.discard(d)
                    elems.discard(d)
                    tptr.pop(d, None)
                    s = i.operands[1]
                    if s.type == X86_OP_REG:
                        n2 = W.norm(s.reg)
                        if n2 in off:
                            off[d] = off[n2]
                            if n2 in elems:
                                elems.add(d)
                            if n2 in tptr:
                                tptr[d] = tptr[n2]
                        elif n2 in rels:
                            rels[d] = rels[n2]
                        elif n2 in ptab:
                            ptab.add(d)
                    elif dv and s.type == X86_OP_MEM and s.size == 4:
                        mm3 = s.value.mem
                        b3 = off.get(W.norm(mm3.base))
                        if (not mm3.index and b3 is not None
                                and (b3 + mm3.disp) in dv["rels"]):
                            rels[d] = b3 + mm3.disp
                    continue
                if m in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM:
                    tgt = i.operands[0].imm
                    if not (entry <= tgt < entry + fsize) and tgt in img.sizes:
                        for k, ar in enumerate(W.ARG_REGS):
                            if ar in off:
                                fwd.add((tgt, k + 1, off[ar]))
                                # THE DESCENT EDGE, kept so exposure can propagate along it.
                                # Caller count alone marks the wrong set: 00217060 has exactly
                                # ONE caller and looks private, and that caller is 00202B70,
                                # the 103-caller copy helper. Its accesses are a vector
                                # transform's, reached through this object only because the
                                # generic helper was. Exposure is a property of the PATH.
                                self.edges.add((entry, tgt))
                        # ARGUMENTS FIVE AND UP, which arrive on the stack. `[rsp+0x20]` is
                        # the fifth, so the slot is disp/8 + 1. Without this a table handed
                        # to a generic routine as argument six is simply invisible, which is
                        # why ChunkedSlotEntry and ChunkedSlotBankEntry censused zero.
                        for disp, o in outgoing.items():
                            fwd.add((tgt, disp // 8 + 1, o))
                            self.edges.add((entry, tgt))
                    if m == "call":
                        # A PACK-REFERENCE RESOLVER level (`PKREF`): the callee takes the
                        # u32 at parent+OFF in ecx and returns the decoded child base -
                        # `0020E600` is `rax = ecx + *(0x01F83530)`. rcx's `rels` mark
                        # must be read BEFORE the volatile clobber below erases it.
                        decoded = dv["decodes"].get(tgt) if dv else None
                        relarg = rels.get(W.ARG_REGS[0])
                        off = {k: v for k, v in off.items() if k not in W.VOLATILE}
                        rels = {k: v for k, v in rels.items() if k not in W.VOLATILE}
                        ptab -= W.VOLATILE
                        elems -= W.VOLATILE
                        tptr = {k: v for k, v in tptr.items() if k not in W.VOLATILE}
                        if seed_rule and seed_rule[0] == "FN" and tgt == seed_rule[1]:
                            # A bank-qualified FN seeds only at the sites the bank
                            # classifier attributed to this type's slot - an
                            # unqualified site means the element's type is not this
                            # one, or not provably one.
                            if (self.fn_sites is None
                                    or (entry, i.address) in self.fn_sites):
                                off[X.X86_REG_RAX] = -seed_rule[2]
                        elif decoded is not None and relarg == decoded:
                            off[X.X86_REG_RAX] = decoded
                    continue
                if m == "call":
                    off = {k: v for k, v in off.items() if k not in W.VOLATILE}
                    rels = {k: v for k, v in rels.items() if k not in W.VOLATILE}
                    ptab -= W.VOLATILE
                    elems -= W.VOLATILE
                    tptr = {k: v for k, v in tptr.items() if k not in W.VOLATILE}
                    continue
                # THE COMPUTED ELEMENT BASE of an `ARRAY` route, recognised as the two
                # instructions that actually form it. Placed BEFORE the write-invalidation
                # below because that would drop the very register being established.
                if self.stride or dv:
                    ops = i.operands
                    if (m == "imul" and len(ops) == 3 and ops[0].type == X86_OP_REG
                            and ops[2].type == X86_OP_IMM
                            and (dv or ops[2].imm == self.stride)):
                        # `continue` is load-bearing: imul WRITES this register, so falling
                        # through to the invalidation below would discard the mark on the
                        # same instruction that earns it.
                        d0 = W.norm(ops[0].reg)
                        off.pop(d0, None)
                        zero.discard(d0)
                        tablebase.pop(d0, None)
                        rels.pop(d0, None)
                        ptab.discard(d0)
                        elems.discard(d0)
                        tptr.pop(d0, None)
                        mult.add(d0)
                        continue
                    # A SHIFT-LEFT PRODUCT IS `i * 2^k`, the same element-offset product an
                    # `imul` gives - `shl rax, 4` at 0026D9F6 scales the weather-block index
                    # by its 0x10 stride before `add rax, r8` folds it onto the header. Any
                    # scaled product under a derived run can be an array index, so it joins
                    # `mult` the same way. Derived runs only: stride runs keep requiring
                    # the route's own stride as the multiply, unchanged.
                    # the TWO-OPERAND imul `imul d, s` (d *= s) is the same product -
                    # StatusDefinitionRecord's `imul ecx, edi` (stride * statusId) is the
                    # index product `add ecx, edx` then folds onto the decoded base.
                    if (dv and m == "imul" and len(ops) == 2
                            and ops[0].type == X86_OP_REG
                            and ops[1].type == X86_OP_REG):
                        d0 = W.norm(ops[0].reg)
                        off.pop(d0, None)
                        zero.discard(d0)
                        tablebase.pop(d0, None)
                        rels.pop(d0, None)
                        ptab.discard(d0)
                        elems.discard(d0)
                        tptr.pop(d0, None)
                        mult.add(d0)
                        continue
                    if (dv and m in ("shl", "sal") and len(ops) == 2
                            and ops[0].type == X86_OP_REG
                            and ops[1].type == X86_OP_IMM):
                        d0 = W.norm(ops[0].reg)
                        off.pop(d0, None)
                        zero.discard(d0)
                        tablebase.pop(d0, None)
                        rels.pop(d0, None)
                        ptab.discard(d0)
                        elems.discard(d0)
                        tptr.pop(d0, None)
                        mult.add(d0)
                        continue
                try:
                    _r, w = i.regs_access()
                except capstone.CsError:
                    w = []
                for r in w:
                    off.pop(W.norm(r), None)
                    tablebase.pop(W.norm(r), None)
                    rels.pop(W.norm(r), None)
                    ptab.discard(W.norm(r))
                    elems.discard(W.norm(r))
                    tptr.pop(W.norm(r), None)
                if self.stride or dv:
                    for r in w:
                        mult.discard(W.norm(r))
                # THE ZERO SET, maintained last so it reflects this instruction's effect on the
                # NEXT one. `xor r,r` and `sub r,r` are the compiler's two ways of writing zero;
                # anything else that writes a register invalidates it, and a call clobbers the
                # volatiles. The set is only ever used to explain away a store, never to admit
                # one, so being wrong in the cautious direction costs nothing but a missed tag.
                if (m in ("xor", "sub") and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_REG
                        and i.operands[1].type == X86_OP_REG
                        and W.norm(i.operands[0].reg) == W.norm(i.operands[1].reg)):
                    zero.add(W.norm(i.operands[0].reg))
                else:
                    for r in w:
                        zero.discard(W.norm(r))
                    if m == "call":
                        zero -= set(W.VOLATILE)
            for s in succ[b]:
                prev = state.get(s)
                if prev is None:
                    state[s] = (dict(off), dict(tptr), set(elems), set(zero))
                    work.append(s)
                else:
                    # THE NULL-COALESCE RULE: a mark survives a predecessor that proves
                    # the register ZERO rather than marking it. `x ? decoded : NULL`
                    # codegen (the resolver call guarded by two null tests, then
                    # `xor ecx,ecx` merging before `[rcx+f]`) is the shape this exists
                    # for - on the zero side the access is a null-deref, i.e. dead, so
                    # every real execution took the marked path. Sound because `zero`
                    # is itself an all-predecessors proof. The reverse direction -
                    # prev proved zero, this edge marks - takes the mark for the same
                    # reason, keeping the merge order-independent.
                    mzero = prev[3] & zero
                    moff = {k: v for k, v in prev[0].items()
                            if off.get(k) == v or k in zero}
                    for k, v in off.items():
                        if k in prev[3] and k not in moff:
                            moff[k] = v
                    mtptr = {k: v for k, v in prev[1].items() if tptr.get(k) == v}
                    melems = prev[2] & elems
                    if (moff, mtptr, melems, mzero) != prev:
                        state[s] = (moff, mtptr, melems, mzero)
                        work.append(s)

    def run(self, rule, hosts, maxdepth, acc=None):
        if acc is None:
            acc = collections.defaultdict(set)
        fwd = set()
        # A BANK-QUALIFIED FN seeds only at the call sites the classifier attributes
        # to this type's slot; every other seeding kind runs ungated (fn_sites None).
        self.fn_sites = None
        if rule[0] == "FN" and len(rule) > 4 and rule[4] is not None:
            self.fn_sites = bank_sites(self.img, rule[1], rule[4])
        # A VTABLE seed is `this` at method entry: every dispatch site is `call
        # [rax + slot]` off the object, so rcx is the instance in every entry body.
        # An ARG seed is the same shape with the register the route names.
        this_seed = ({W.ARG_REGS[0]: 0} if rule[0] == "VTABLE"
                     else {W.ARG_REGS[rule[2]]: 0} if rule[0] == "ARG"
                     else {})
        for e in hosts:
            self.walk(e, this_seed, acc, fwd, rule)
        seen = set(fwd)
        work = collections.deque((x[0], x[1], x[2], 0) for x in fwd)
        while work:
            fn, slot, o, d = work.popleft()
            nf = set()
            if slot <= len(W.ARG_REGS):
                self.walk(fn, {W.ARG_REGS[slot - 1]: o}, acc, nf, None)
            else:
                self.walk(fn, {}, acc, nf, None, stack_seed=(slot, o))
            if d >= maxdepth:
                continue
            for g in nf:
                if g not in seen and len(seen) < 20000:
                    seen.add(g)
                    work.append((g[0], g[1], g[2], d + 1))
        return acc, len(seen)


def vtable_entries(img, addr):
    """The method entries of a vtable: consecutive qwords that are known function
    entries, stopping at the first non-function qword (the next object's RTTI or data
    cell). A MSVC vtable is pure function pointers, so the first miss is the table's
    end - never a hole."""
    raw = img.read(addr, 8 * 256)
    out = []
    if raw:
        for k in range(len(raw) // 8):
            q = struct.unpack_from("<Q", raw, k * 8)[0]
            if q not in img.sizes:
                break
            out.append(q)
    return out


def hosts_for(img, rule, callers):
    kind, addr = rule[0], rule[1]
    if kind == "FN":
        return sorted(callers.get(addr, ()))
    if kind == "VTABLE":
        # the hosts ARE the methods - each is walked with rcx marked at 0
        return vtable_entries(img, addr)
    if kind == "ARG":
        # the host IS the named function - walked with the named arg register at 0
        return [addr] if addr in img.sizes else []
    out = []
    for e in sorted(img.sizes):
        body = img.body(e)
        if not body:
            continue
        if kind in ("PTR", "PARRAY", "PTABLE"):
            # The block base load: `mov rX,[rip->ADDR]`, or the image-base-relative
            # `mov rX,[rB + ADDR-imgbase]` whose rB is lea'd in the same body. PTABLE's
            # first instruction is the same load - the cell holds the table's base.
            hit = any(i.mnemonic == "mov" and len(i.operands) == 2
                      and i.operands[0].type == X86_OP_REG
                      and i.operands[1].type == X86_OP_MEM
                      and W.rip_target(i, i.operands[1]) == addr for i in body)
            if not hit and kind == "PARRAY":
                base_here = any(W.lea_value(i) == img.base
                                for i in body if i.mnemonic == "lea")
                if base_here:
                    hit = any(i.mnemonic == "mov" and len(i.operands) == 2
                              and i.operands[0].type == X86_OP_REG
                              and i.operands[1].type == X86_OP_MEM
                              and not i.operands[1].value.mem.index
                              and img.base + i.operands[1].value.mem.disp == addr
                              for i in body)
        elif kind == "SLOTPTR":
            # A pointer table: the common shape is `lea rB,[ADDR]` (or the image-base
            # `lea rB,[rI + ADDR-imgbase]`) then `mov rX,[rB + i*S]` - so the table's LEA alone
            # nominates the body. Single-instruction forms are covered too: `mov rX,[rip->ADDR]`
            # (slot 0) and `mov rX,[i*S + ADDR]` (absolute indexed).
            stride = rule[3]
            base_here = any(W.lea_value(i) == img.base
                            for i in body if i.mnemonic == "lea")
            # a table reached through a biased base lea - `lea rB,[ADDR - k]` with the
            # load's disp finishing the address - nominates the body the same way a
            # direct table lea does
            hit = any(0 <= addr - (W.lea_value(i) or -1) <= 0x400
                      for i in body if i.mnemonic == "lea")
            if not hit and base_here:
                hit = any(i.mnemonic == "lea" and len(i.operands) == 2
                          and i.operands[1].type == X86_OP_MEM
                          and not i.operands[1].value.mem.index
                          and 0 <= addr - (img.base + i.operands[1].value.mem.disp)
                              <= 0x400
                          for i in body)
            for i in body:
                if hit:
                    break
                if not (i.mnemonic == "mov" and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_REG
                        and i.operands[1].type == X86_OP_MEM):
                    continue
                mm = i.operands[1].value.mem
                if not mm.index:
                    if W.rip_target(i, i.operands[1]) == addr \
                            or (base_here and img.base + mm.disp == addr):
                        hit = True
                        break
                elif (mm.scale == stride
                        and (mm.disp == addr
                             or (base_here and img.base + mm.disp == addr))):
                    hit = True
                    break
        else:
            hit = any(W.lea_value(i) == addr for i in body if i.mnemonic == "lea")
            # THE IMAGE-BASE-RELATIVE IDIOM HAS TO BE FOUND HERE TOO, not only in the walk.
            # A function that builds the address as `lea rX,[rip->imagebase]` +
            # `lea rY,[rX + RVA]` contains NO direct lea of it, so this selector skipped the
            # function entirely and the walk never ran. Discovered by a failed prediction:
            # teaching only the walk changed nothing, because 0026C8C0 was never a host.
            # BOTH halves are required - a lea of the image base somewhere in the body AND a
            # lea whose displacement completes the address - so an unrelated `lea reg,[reg+N]`
            # that happens to arithmetic out cannot nominate a function on its own.
            if not hit:
                base_here = any(W.lea_value(i) == img.base
                                for i in body if i.mnemonic == "lea")
                if base_here:
                    hit = any(i.mnemonic == "lea"
                              and i.operands[1].type == X86_OP_MEM
                              and not i.operands[1].value.mem.index
                              and img.base + i.operands[1].value.mem.disp == addr
                              for i in body if len(i.operands) == 2)
        if hit:
            out.append(e)
    return out


def report_bases(rows, acc, size, limit=12, indent="   "):
    """Accesses grouped by the base they were reached through, resolved against declared rows.

    A BASE IS REPORTED IN ROOT COORDINATES AND THAT IS NOT WHERE IT LIVES. Three bases the first
    version of this report surfaced as unexplained - +0xB0, +0x9A60, +0xABF0 on
    ManagerSingleton0209BE80 - turned out to be formed INSIDE other sub-objects, as
    enclosing+0x10, enclosing+0xAC0 and enclosing+0xC0. Recording the base was the right fix and
    printing it in root coordinates re-created the same confusion one level up, so the row it
    falls in is named and the base is given relative to that row as well.

    Returns the bases that fall in NO declared row. Those are the candidate undiscovered
    sub-objects and they are the only ones worth a reader's time, so they are always printed
    even past the display limit.
    """
    bases = collections.Counter()
    for _d, sites in acc.items():
        for s_ in sites:
            bases[s_[2] if len(s_) > 2 else 0] += 1

    def describe(b):
        if b == 0:
            return "the type itself", False
        if b < 0:
            # A NEGATIVE BASE IS NOT A SUB-OBJECT. With an `FN addr+delta` route the getter's
            # return carries -delta, so anything reached through the raw return - the buffer
            # this type sits inside - is recorded at a negative base. The first version of this
            # classifier called those "candidate sub-objects" and produced two false positives
            # on SavePayload and PersistentFlagPayload, both at -0x200, which is the save image
            # header in front of the payload and a declared type in its own right.
            return ("BEFORE this type's base - the buffer it sits inside, not a sub-object",
                    False)
        encl = None
        for o, sz, n, _ct in rows:
            if o <= b < o + sz and not (o == 0 and sz == size):
                encl = (o, n)
        if encl and encl[0] != b:
            return "inside %s, at that row + 0x%X" % (encl[1], b - encl[0]), False
        if encl:
            return "the base of %s" % encl[1], False
        return "IN NO DECLARED ROW - a candidate sub-object", True

    ordered = sorted(bases.items(), key=lambda kv: -kv[1])
    orphan, shown = [], 0
    for b, k in ordered:
        tag, is_orphan = describe(b)
        if is_orphan:
            orphan.append((b, k))
        if shown < limit or is_orphan:
            print("%s+0x%-7X %5d access(es)   %s" % (indent, b, k, tag))
            shown += 1
    return orphan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True)
    ap.add_argument("--with-children", action="store_true")
    ap.add_argument("--max-depth", type=int, default=6)
    ap.add_argument("--db", default=G.DB)
    ap.add_argument("--with-ctor", action="store_true",
                    help="also seed the constructor named in the store's `ctor` column")
    ap.add_argument("--shared-at", type=int, default=20,
                    help="report contributing functions with more than N callers (default 20)")
    ap.add_argument("--out", default=None,
                    help="write the census as a standard 8-column *-accesses.tsv")
    a = ap.parse_args()

    img = W.Image()
    callers, _c, _s = CG.call_maps(G.EXE, G.FUNCS)
    types, fields, routes = store(a.db)
    if a.type not in types:
        print("no sized type named %r" % a.type)
        return 2
    size, route, ctor = types[a.type]
    rules = parse_routes(route)
    if not rules:
        print("route %r is not one this tool models "
              "(PTR [+off] / FN+delta / STATIC / ARRAY+stride / PARRAY+stride / SLOTPTR /"
              " PTABLE / VTABLE / ARG / CHAIN / RELOFF / EMBED / PKREF only)" % route)
        return 2
    print("%s  size 0x%X  route %s" % (a.type, size, route))
    c = Census(img, size)
    acc, reached, rule = None, 0, rules[0][0]
    for rule, text in rules:
        # PER-RULE, and reset for a non-array alternative: a type routed `ARRAY ... | PTR ...`
        # must not carry the stride into the PTR walk.
        c.stride = rule[3] if rule[0] in ("ARRAY", "PARRAY") else None
        c.parray_off = rule[2] if rule[0] == "PARRAY" else None
        c.derived = None
        if rule[0] in DERIVED:
            # A DERIVED ALTERNATIVE: resolve the parent chain to a seedable root route and
            # run the ROOT's hosts with the derived spec - `off` walks in root coordinates
            # and the emit gate pulls the child's window out of them.
            specs, fails = derive_specs(types, fields, routes, a.type, rule)
            for rrule, rtext, spec, path in specs:
                hosts = hosts_for(img, rrule, callers)
                c.rule_text = "%s <- %s" % (text, rtext)
                c.stride = rrule[3] if rrule[0] in ("ARRAY", "PARRAY") else None
                c.parray_off = rrule[2] if rrule[0] == "PARRAY" else None
                c.derived = spec
                sub, n = c.run(rrule, hosts, a.max_depth, acc)
                acc, reached = sub, reached + n
                print("  %-30s via %-30s seed hosts %-4d cumulative offsets %d"
                      % (path, rtext[:30], len(hosts), len(acc)))
            for f_ in fails:
                print("  %-30s UNRESOLVED: %s" % (text, f_))
            c.derived = None
            continue
        hosts = hosts_for(img, rule, callers)
        c.rule_text = text
        sub, n = c.run(rule, hosts, a.max_depth, acc)
        acc, reached = sub, reached + n
        if len(rules) > 1:
            print("  %-26s seed hosts %-4d cumulative offsets %d" % (text, len(hosts), len(acc)))
        else:
            print("seed hosts: %d" % len(hosts))

    # THE CONSTRUCTOR IS NOT ON THE ROUTE, and for an `FN` route it is not reachable from one.
    # RenderModelInstance is `FN 0x003E55B0+0x0` - a getter's return - so the walk sees every
    # body that USES the object and never the one that builds it, and a ctor is usually the
    # densest writer a type has. gen_ptr_census_ctor.py finds it from the allocation, but only
    # for `PTR` routes. The store already NAMES the constructor in its own `ctor` column, so it
    # is seeded directly here with arg0 at offset 0 - no inference, just reading the column the
    # store keeps for exactly this. Without it RenderModelInstance censused 33 offsets and NONE
    # of the five the ctor writes.
    if a.with_ctor and ctor:
        try:
            cva = int(ctor.split()[0], 16)
        except (ValueError, IndexError):
            cva = None
        if cva and cva in img.sizes:
            before = len(acc)
            nf = set()
            c.walk(cva, {W.ARG_REGS[0]: 0}, acc, nf, None)
            for g in sorted(nf):
                if g[1] <= len(W.ARG_REGS):
                    c.walk(g[0], {W.ARG_REGS[g[1] - 1]: g[2]}, acc, set(), None)
                else:
                    c.walk(g[0], {}, acc, set(), None, stack_seed=(g[1], g[2]))
            print("ctor %08X seeded at arg0: %d offset(s) -> %d"
                  % (cva, before, len(acc)))
        else:
            print("ctor %r is not a function address this image knows" % ctor[:40])

    print("reached (callee, slot, offset) triples : %d" % reached)
    if acc is None:
        # Every rule fell out unseedable (e.g. a CHAIN whose parent resolves to no
        # seedable root). A None accumulator must not become a crash: report the
        # census as unseedable rather than emit an empty file that would read as
        # a measured zero.
        print("UNSEEDABLE: no route yielded a host set; no census emitted")
        return 2
    print("distinct offsets from the parent route : %d" % len(acc))

    folded = 0
    if a.with_children:
        for off, sz, nm, ctype in sorted(fields.get(a.type, [])):
            base = ctype.strip().rstrip("*").split("[")[0].strip()
            if base not in types or base == a.type:
                continue
            csize, croute = types[base][:2]
            crule = parse_route(croute)
            if not crule or crule[0] not in SEEDABLE:
                continue
            chosts = hosts_for(img, crule, callers)
            cc = Census(img, csize)
            cc.stride = crule[3] if crule[0] in ("ARRAY", "PARRAY") else None
            cc.parray_off = crule[2] if crule[0] == "PARRAY" else None
            cacc, _r = cc.run(crule, chosts, a.max_depth)
            new = 0
            for d, sites in cacc.items():
                if 0 <= off + d < size:
                    if off + d not in acc:
                        new += 1
                    acc[off + d] |= sites
            folded += new
            print("   child %-28s at +0x%-6X route %-22s -> %d offsets, %d new"
                  % (base, off, croute, len(cacc), new))
    if a.with_children:
        print("offsets after folding children        : %d  (+%d)" % (len(acc), folded))
    print()

    rows = sorted(fields.get(a.type, []))

    def where(d):
        for o, s, n, _c in rows:
            if o <= d < o + s:
                return n
        return "(outside any row)"
    by = collections.Counter(where(d) for d in acc)
    print("offsets by declared row (top 15):")
    for n, k in by.most_common(15):
        print("   %-34s %d" % (n, k))
    print()

    # THE BASES THE ACCESSES CAME THROUGH. An offset reached through base 0 is a field of this
    # type; one reached through base B is a field of whatever sits at +B. Reporting only the
    # offset conflates them, and that conflation has produced one withdrawal already.
    bases = collections.Counter()
    for d, sites in acc.items():
        for s_ in sites:
            bases[s_[2] if len(s_) > 2 else 0] += 1
    print("accesses by the BASE they were reached through:")
    orphan = report_bases(rows, acc, size)
    if orphan:
        print("   -> %d base(s) in no declared row: candidate sub-objects." %
              len(orphan))
    else:
        print("   -> every base resolves to a declared row.")
    print()
    gaps = [(o, s, n) for o, s, n, _c in rows
            if s >= 256 and ("unobserved" in n.lower() or "gap" in n.lower())]
    print("rows that read as a gap (>=256 B): %d" % len(gaps))
    for o, s, n in gaps:
        hit = sorted(d for d in acc if o <= d < o + s)
        print("   +0x%-7X %-28s %6d B : %d offset(s) %s"
              % (o, n, s, len(hit), " ".join("0x%X" % x for x in hit[:8])))
    print()
    # SHARED-CALLEE EXPOSURE. This census follows the object's displacement into any direct
    # callee, which is what makes it see 326 offsets on ManagerSingleton0209BE80 where a
    # slot-seeded scan sees 42. It also means a LEAF HELPER THE WHOLE IMAGE CALLS is credited
    # with defining this type's layout, and on that very type it did: `movups xmmword ptr
    # [rbx], xmm0` in 00202B70 (103 CALLERS) and 00202C90 (67 CALLERS) supplied the 16-wide
    # evidence that made four declared 8-byte pointers in ManagerSub0209BE80_7EA0 read as
    # mismatches. They are generic 16-byte copy helpers. The gate's bulk rule drops an unrolled
    # SIMD block copy; a single `movups` inside a shared helper is the same thing and survives it.
    #
    # THIS REPORTS AND DOES NOT DECIDE. A high caller count is strong evidence of a generic
    # helper and is not proof - a hot object legitimately has hot accessors - so the number is
    # printed for the operator and `--max-callers` is opt-in. What must not happen again is a
    # census being registered without anybody knowing the question was there.
    # EXPOSURE PROPAGATES ALONG THE DESCENT, which the first version of this report missed and
    # a worked case proved. `ManagerSub0209BE80_7EA0`'s four declared pointers read as 4 wide,
    # and the dominant 4-wide evidence is `00217060` - ONE caller, which looks private. Its one
    # caller is `00202B70`, the 103-caller copy helper, and 00217060 is a vector transform
    # multiplying `[r8]`, `[r8+8]`, `[r8+0xC]` by a matrix. It is reached through this object
    # only because the generic helper was, so a filter that asks each contributing function for
    # its own caller count marks it clean and under-reports. Being generic is a property of the
    # PATH, so the seed set here is every contributing function the image widely calls, and
    # exposure is then closed over the census's own descent edges.
    seed = {r[0] for r in c.rows if len(callers.get(r[0], ())) > a.shared_at}
    succ = collections.defaultdict(set)
    for u, v in c.edges:
        succ[u].add(v)
    exposed, work = set(seed), list(seed)
    while work:
        u = work.pop()
        for v in succ.get(u, ()):
            if v not in exposed:
                exposed.add(v)
                work.append(v)

    shared = collections.Counter()
    for fn in (r[0] for r in c.rows):
        if fn in exposed:
            shared[(fn, len(callers.get(fn, ())))] += 1
    print()
    print("SHARED-CALLEE EXPOSURE  functions the image widely calls, AND what they reach")
    print("  seed: more than %d callers.  exposed: the seed closed over this census's own"
          % a.shared_at)
    print("  descent edges, because a private callee of a generic helper is not private here.")
    if not shared:
        print("  none - every contributing function is called from at most %d place(s), so no"
              % a.shared_at)
        print("  access here comes from a helper the rest of the image shares.")
    else:
        tot = sum(shared.values())
        print("  %d access(es) from %d such function(s)  (%.1f%% of %d)"
              % (tot, len(shared), 100.0 * tot / max(1, len(c.rows)), len(c.rows)))
        for (fn, n), k in shared.most_common(8):
            print("    %08X  %4d callers  %4d access(es)  %s"
                  % (fn, n, k, img.names.get(fn, "")))
        print("  READ THESE BEFORE REGISTERING THE CENSUS. A generic copy or math helper reached")
        print("  through this object records ITS OWN access pattern at this object's offsets.")

    print("A DISPLACEMENT IS AN OBSERVATION AND A LAYOUT IS A READING. Nothing here is split;")
    print("a zero means 'not reached by a tracked displacement from the routes seeded above',")
    print("which does not exclude a wholesale copy or a route this tool does not model.")

    if a.out:
        # The eight columns every other census in this store uses, so check_census_widths.py can
        # read it without a special case. `route` carries the seed AND the base the access was
        # reached through, because this tool's whole point is that an access at +0x223 reached as
        # [rcx+0xA3] with rcx = base+0x180 belongs to a nested object - dropping the base is what
        # got an earlier version of this output withdrawn, and a file that omits it would repeat
        # the mistake in durable form.
        seen, rows = set(), []
        for fn, site, d, base, kind, txt, isz in c.rows:
            if (site, d) in seen:
                continue
            seen.add((site, d))
            rows.append((fn, site, d, base, kind, txt, isz))

        # A SINGLE ZERO STORE IS NOT A CLEAR; A RUN OF THEM IS. One `mov qword ptr [rcx+8], rax`
        # with rax zeroed is perfectly compatible with a genuine 8-byte field being initialised,
        # and calling it a clear would discard real evidence. What is NOT compatible with a field
        # list is a CONTIGUOUS RUN at one width from one function - 0028CA40's six qwords across
        # +0x0..+0x2F, or 00186CD0's two across +0xD00..+0xD0F - because the run's stride is the
        # store width the compiler chose to clear with, and it says nothing about what is inside.
        # Both cases that forced a hand reading are runs; the threshold is two, which is what
        # BootSingleton01F7F598 has, and the cost of that choice is printed below rather than
        # absorbed.
        by = collections.defaultdict(set)
        for fn, site, d, _b, kind, txt, isz in rows:
            if isz:
                w = W_OF(txt)
                if w:
                    by[(fn, w)].add(d)
        clear = set()
        for (fn, w), offs in by.items():
            for d in offs:
                if (d - w) in offs or (d + w) in offs:
                    clear.add((fn, d))

        rows = [(fn, site, d, base, kind, txt, isz and (fn, d) in clear)
                for fn, site, d, base, kind, txt, isz in rows]
        rows.sort(key=lambda x: (x[2], x[1]))
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
            for fn, site, d, base, kind, txt, iscl in rows:
                # `exposed` marks a row reached through a helper the image shares, or through
                # anything below one. check_census_widths.py excludes those from width evidence
                # and counts them separately. THE ROW STAYS IN THE FILE: it is a real access at
                # a real address, and whether that subsystem's view of these bytes is a second
                # view of one field or a different object entirely is a question a later reader
                # needs the row to answer. Dropping it would decide it by deletion.
                fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\troute-seeded %s base+0x%X%s\t\n"
                         % (fn, img.names.get(fn, ""), site, d, kind, txt, route, base,
                            ((" exposed" if fn in exposed else "")
                             + (" zeroclear" if iscl else ""))))
        nex = sum(1 for r in rows if r[0] in exposed)
        ncl = sum(1 for r in rows if r[6] and r[0] not in exposed)
        print()
        print("  of those, %d marked `exposed`, %d more marked `zeroclear`, %d usable as "
              "width evidence" % (nex, ncl, len(rows) - nex - ncl))
        print("wrote %s  (%d distinct access(es) at %d offset(s), %d function(s))"
              % (a.out, len(rows), len({x[2] for x in rows}), len({x[0] for x in rows})))
    return 0


if __name__ == "__main__":
    sys.exit(main())
