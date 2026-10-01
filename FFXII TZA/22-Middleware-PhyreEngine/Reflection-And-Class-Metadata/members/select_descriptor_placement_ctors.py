"""select_descriptor_placement_ctors.py [--write] - EC-7 selector for the
PClassDescriptorConcrete<T> slot-10 (+0x50) placement default constructors
(SWE2-EC7, 2026-09-29; FABLE family ruling R2, _index/candidates/fable-family-ruling-0929).

Slot 10 of the Phyre reflection template PClassDescriptorConcrete<T> is "construct a default T at
the given address when it is non-null, and return 1": `if (rdx) T::T(rdx); return 1`. The meaning
is stated once for the class of bodies on class-descriptor-and-metadata-system.md (carried-table
slot map, "+0x50 ... the class's placement default constructor").

A census body is a member when BOTH halves hold, each read from the image:

  1. RTTI (the upstream boundary): every appearance of the body in rtti/methods.tsv is slot 10 of a
     `Phyre::PClassDescriptorConcrete<...>` vtable (RTTI-exclusive; a body that also sits at any
     other class's or slot's position is not admitted);
  2. SHAPE (the wrapper, strict form): the body has exactly one `ret`, as its last instruction;
     `test rdx, rdx` is immediately followed by `je X`; X is a `mov al, 1` / `mov eax, 1`; and only
     `add rsp, imm` / `pop reg` lie between X and the `ret`. So the null path and the constructed
     path both return 1, and everything between the `je` and X is the constructor for T.

and it is neither A-measured nor a member of another declared family, and not a UC-1 frontier body
(frontier by ruling, never A/B/C by default).

What a member's B disposition covers: THE WRAPPER - the slot's role, the null test and the return
value. The constructor code between the `je` and X - the inlined T::T and any base or member
constructor it calls - is class T's default constructor, and is explained (or not) with class T's
own type entry, not by this family.

Controls printed:
  positive - every A-measured or already-declared body of the same RTTI population passes the
             shape half (the ruling's test: all 108 of them);
  negative - the `xor al, al ; ret` stub 00657140 that sits at +0x50 on the abstract classes and on
             the classes without a default constructor is refused by the shape half, so the shape
             test can fail;
  census   - RTTI-exclusive slot-10 bodies that fail the shape are printed, never admitted.

Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe (sha256 73461D08...21F8),
Tools/work/rtti/methods.tsv, graph/functions.tsv (via check_dispositions.load_functions) + uc1_band.
"""
import collections, csv, io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd
import uc1_band
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

SELF = "pclassdescriptorconcrete-placement-default-ctors.tsv"
OUT = os.path.join(HERE, SELF)
STUB = 0x657140

d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((0x120000 + va, vs, ro, rs))


def off(a):
    for va, vs, ro, rs in secs:
        if va <= a < va + rs:
            return ro + (a - va)


md = Cs(CS_ARCH_X86, CS_MODE_64)


RET1 = ("al, 1", "eax, 1")
RAX = ("rax", "eax", "ax", "al")


def epilogue(y):
    """pop reg / add rsp, imm / restore of a saved non-rax register from the frame."""
    if y.mnemonic == "pop" or (y.mnemonic == "add" and y.op_str.startswith("rsp, ")):
        return True
    return (y.mnemonic == "mov" and "ptr [rsp + " in y.op_str and y.op_str.split(",")[0].strip() not in RAX
            and not y.op_str.startswith(("qword ptr", "dword ptr", "word ptr", "byte ptr")))


def shape(a, size):
    """Strict wrapper form; returns (True, calls-in-constructor) or (False, reason).

    Two compiled spellings of `if (rdx) T::T(rdx); return 1`, both requiring al = 1 at the single
    trailing ret on the null path and the constructed path alike:
      join    - `je X` where X is `mov al/eax, 1`, and only epilogue follows X;
      hoisted - `mov al/eax, 1` precedes the `test`, nothing after it writes al/eax/rax, the
                constructor makes no call (a call would clobber rax), and `je X` lands in the epilogue.
    """
    ins = list(md.disasm(d[off(a):off(a) + size], a))
    if not ins or ins[-1].mnemonic != "ret" or sum(1 for x in ins if x.mnemonic == "ret") != 1:
        return False, "not one trailing ret"
    t = next((i for i, x in enumerate(ins) if x.mnemonic == "test" and x.op_str == "rdx, rdx"), None)
    if t is None or t + 1 >= len(ins) or ins[t + 1].mnemonic != "je":
        return False, "no test rdx,rdx ; je"
    try:
        x = int(ins[t + 1].op_str, 16)
    except ValueError:
        return False, "indirect je"
    k = next((i for i, y in enumerate(ins) if y.address == x), None)
    if k is None:
        return False, "je target outside the body"
    if ins[k].mnemonic == "mov" and ins[k].op_str in RET1:          # join spelling
        if not all(epilogue(y) for y in ins[k + 1:-1]):
            return False, "non-epilogue after the return value"
        return True, sum(1 for y in ins[t + 2:k] if y.mnemonic == "call")
    h = [i for i, y in enumerate(ins[:t]) if y.mnemonic == "mov" and y.op_str in RET1]   # hoisted spelling
    if not h:
        return False, "no al = 1 on both paths"
    later = ins[h[-1] + 1:]
    if any(y.mnemonic == "call" for y in later):
        return False, "hoisted al = 1 with a call after it"
    if any(y.op_str.split(",")[0].strip() in RAX for y in later if y.mnemonic not in ("test", "cmp", "je", "ret")):
        return False, "hoisted al = 1 overwritten"
    if not all(epilogue(y) for y in ins[k:-1]):
        return False, "je target is not the epilogue"
    return True, 0


def main():
    sizes = cd.load_functions()
    uc1 = uc1_band.frontier_starts()
    a_set = cd.measure_a(DB, sizes)[0]
    declared = {}
    for doc, parts in cd.parse_families(DB):
        if len(parts) >= 5 and parts[1] in cd.LETTERS and not parts[2].endswith(SELF):
            try:
                for m in cd.read_members(doc, parts[2]):
                    declared.setdefault(m, parts[0])
            except (IOError, OSError, ValueError):
                pass
    app = collections.defaultdict(list)
    for row in csv.DictReader(open(os.path.join(W, "rtti", "methods.tsv"), encoding="utf-8", errors="replace"),
                              delimiter="\t"):
        try:
            app[int(row["address"], 16)].append((row["class"], row["slot"]))
        except (ValueError, TypeError):
            pass
    pop = sorted(a for a, ap in app.items() if a in sizes and ap
                 and all(c.startswith("Phyre::PClassDescriptorConcrete<") and s == "10" for c, s in ap))
    members, ctrl, fail = [], collections.Counter(), []
    for a in pop:
        ok, info = shape(a, sizes[a])
        st = "UC-1" if a in uc1 else "A" if a in a_set else "declared" if a in declared else "frontier"
        ctrl[(st, ok)] += 1
        if not ok:
            fail.append((a, st, info))
        elif st == "frontier":
            members.append((a, sizes[a], info, app[a][0][0]))
    print("RTTI-exclusive PClassDescriptorConcrete<T> slot-10 bodies: %d" % len(pop))
    for (st, ok), c in sorted(ctrl.items()):
        print("  %-9s shape %-4s %4d" % (st, "pass" if ok else "FAIL", c))
    pos_fail = [f for f in fail if f[1] in ("A", "declared")]
    print("positive control: %d of %d A/declared bodies pass the shape half" % (
        sum(c for (st, ok), c in ctrl.items() if st in ("A", "declared") and ok),
        sum(c for (st, ok), c in ctrl.items() if st in ("A", "declared"))))
    for a, st, why in fail:
        print("  shape FAIL %08X (%s): %s" % (a, st, why))
    popset = set(pop)
    outside = collections.Counter()
    for a, sz in sizes.items():
        if a not in popset and 0 < sz <= 256 and off(a) is not None and shape(a, sz)[0]:
            outside["UC-1" if a in uc1 else "A" if a in a_set else "declared" if a in declared else "frontier"] += 1
    print("shape-only census: %d census bodies (<=256 B) outside the RTTI population also pass the shape half %s"
          " - the shape is not the discriminator, the RTTI slot is; none of them is admitted" % (
              sum(outside.values()), dict(outside)))
    neg_ok, neg_why = shape(STUB, sizes.get(STUB, 3))
    print("negative control: %08X (xor al,al ; ret) shape %s (%s)" % (STUB, "pass" if neg_ok else "refused", neg_why))
    assert not neg_ok, "the shape test cannot fail - control broken"
    assert not pos_fail, "an explained body of the population fails the shape half: %s" % pos_fail[:3]
    print("members (frontier, both halves): %d; sizes %d-%d B; with calls inside the constructor: %d" % (
        len(members), min(m[1] for m in members), max(m[1] for m in members), sum(1 for m in members if m[2])))
    if "--write" in sys.argv:
        with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
            f.write("# PClassDescriptorConcrete<T> slot 10 (+0x50) placement default constructors - select_descriptor_placement_ctors.py\n")
            f.write("# B covers the wrapper (if (rdx) T::T(rdx); return 1). The constructor code inside each body is class T's\n")
            f.write("# default constructor, explained (or not) with class T's own type entry, not by this family.\n")
            f.write("address\tbytes\tcalls_in_ctor\tclass\n")
            for a, sz, calls, cls in members:
                f.write("%08X\t%d\t%d\t%s\n" % (a, sz, calls, cls))
        print("wrote %d -> %s" % (len(members), SELF))
    else:
        print("dry run - pass --write to emit the TSV")


if __name__ == "__main__":
    main()
