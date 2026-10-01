"""select_static_init_form.py - the 530 bodies sharing the 32-byte MSVC dynamic-initialiser
form, split by what each one registers into.

EC-7 family C member selector. Re-derives membership from the shipping EXE, independently of
_index/candidates/static-init-form-530.tsv (OPUS's assembled candidate list - cross-checked,
never trusted):

  1. the form is defined by its sixteen opcode bytes: every 32-byte census body whose bytes
     at the non-operand positions are
        48 83 ec 28   sub rsp,0x28
        48 8d 0d ...  lea rcx,[rip+disp32]      (operand bytes 7-10)
        e8 ...        call rel32               (operand bytes 12-15)
        48 8d 0d ...  lea rcx,[rip+disp32]      (operand bytes 19-22)
        48 83 c4 28   add rsp,0x28
        e9 ...        jmp rel32                (operand bytes 28-31)
     census-wide - no run is assumed;
  2. decode the four operands per member: object (first lea), callee (call), second lea
     target, and the tail-jump target;
  3. split by the tail jump:
        -> 00808B90 (the CRT atexit wrapper): group A, 420 bodies;
        -> 00639450 (the shared Phyre class-registration finaliser): group B, 110 bodies;
  4. group A splits by callee:
        the five PInputs semantic-name-registry appends (00879570 channel x143,
        00876C80 key x97, 008768A0 joypad-button x44, 008760A0 type x25, 00876490 axis x10,
        all documented in 15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md)
        = 319 members;
        005FDCB0 = the 56 bodies ALREADY declared as C
        Runtime.NameRegistryEntry.StaticInitializer - verified by SET EQUALITY against
        that family's members file, then excluded, never redeclared;
        the remaining 45 are generic dynamic-initialiser stubs of assorted static objects
        (31 distinct callees, no common owner);
  5. group B is ONE family: all 110 call 006388C0 (PType_FindOrRegisterByName) and the
     second lea re-loads the same descriptor for the finaliser - verified per member;
  6. refuse to write if any member is A-measured, declared by another family, if the
     census-wide form count is not 530, or if any split count differs.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_static_init_form.py [--write]
"""
import io, os, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")

OUT_PINPUTS = os.path.join(
    REPO, "Database", "FFXII TZA", "15-Input", "Input-Name-Registry",
    "members", "pinputs-semantic-registry-initialisers.tsv")
OUT_NAMEONLY = os.path.join(
    REPO, "Database", "FFXII TZA", "22-Middleware-PhyreEngine",
    "Reflection-And-Class-Metadata", "members",
    "name-only-class-registration-initialisers.tsv")
OUT_GENERIC = os.path.join(ROOT, "msvc-dynamic-initialiser-stubs.tsv")
EXISTING_56 = os.path.join(
    REPO, "Database", "FFXII TZA", "24-Compiler-And-CRT-Runtime",
    "Generated-Families", "members",
    "runtime-nameregistryentry-staticinitializer.tsv")

SIZE = 32
FIXED = [i for i in range(SIZE) if i not in
         set(range(7, 11)) | set(range(12, 16)) | set(range(19, 23)) | set(range(28, 32))]
SKELETON = bytes.fromhex("4883ec28" "488d0d" "e8" "488d0d" "4883c428" "e9")
ATEXIT_WRAPPER = 0x00808B90
CLASS_FINALISER = 0x00639450
PINPUTS_CTORS = {0x00879570, 0x00876C80, 0x008768A0, 0x008760A0, 0x00876490}
NAME_ONLY_CTOR = 0x006388C0
EXISTING_CTOR = 0x005FDCB0

sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD

d = io.open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + i * 40
    vsz, va, rsz, ptr = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, vsz, ptr, rsz))


def off(va):
    r = va - base
    for sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return ptr + (r - sva)
    return None


sizes = {}
for l in io.open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass

# 32-byte census bodies whose non-operand positions carry the skeleton
members = []
for e in sorted(sizes):
    if sizes[e] != SIZE or off(e) is None:
        continue
    if bytes(d[off(e) + i] for i in FIXED) != SKELETON:
        continue
    o = off(e)
    obj = e + 11 + struct.unpack_from("<i", d, o + 7)[0]
    callee = e + 16 + struct.unpack_from("<i", d, o + 12)[0]
    arg2 = e + 23 + struct.unpack_from("<i", d, o + 19)[0]
    tail = e + 32 + struct.unpack_from("<i", d, o + 28)[0]
    members.append((e, obj, callee, arg2, tail))

group_a = [m for m in members if m[4] == ATEXIT_WRAPPER]
group_b = [m for m in members if m[4] == CLASS_FINALISER]
other_tail = [m for m in members if m[4] not in (ATEXIT_WRAPPER, CLASS_FINALISER)]

pinputs = [m for m in group_a if m[2] in PINPUTS_CTORS]
existing = [m for m in group_a if m[2] == EXISTING_CTOR]
generic = [m for m in group_a
           if m[2] not in PINPUTS_CTORS and m[2] != EXISTING_CTOR]
name_only = [m for m in group_b if m[2] == NAME_ONLY_CTOR]

# the 56 already-declared bodies, read from the existing family file
declared_56 = set()
for l in io.open(EXISTING_56, encoding="utf-8", errors="replace"):
    t = l.strip().split("\t")[0].upper()
    try:
        declared_56.add(int(t, 16))
    except ValueError:
        pass

a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2] in ("members/pinputs-semantic-registry-initialisers.tsv",
                    "members/name-only-class-registration-initialisers.tsv",
                    "members/msvc-dynamic-initialiser-stubs.tsv"):
        continue  # self: this selector's own declarations are what --write produces
    try:
        for m in CD.read_members(doc, parts[2]):
            dec[m] = parts[0]
    except (IOError, OSError, ValueError):
        pass

a_hits = [m for grp in (pinputs, name_only, generic) for m in grp if m[0] in a_set]
if a_hits:
    print("A-measured members EXCLUDED          : %s"
          % ", ".join("%08X" % m[0] for m in a_hits))
    pinputs = [m for m in pinputs if m[0] not in a_set]
    name_only = [m for m in name_only if m[0] not in a_set]
    generic = [m for m in generic if m[0] not in a_set]

mine = [m[0] for m in pinputs + name_only + generic]

print("32-byte form matches, census-wide    : %d" % len(members))
print("  tail -> 00808B90 atexit wrapper    : %d" % len(group_a))
print("  tail -> 00639450 class finaliser   : %d" % len(group_b))
print("  tail -> anything else              : %d" % len(other_tail))
print("group A by callee:")
for c, n in collections.Counter(m[2] for m in group_a).most_common():
    tag = "PINPUTS" if c in PINPUTS_CTORS else ("EXISTING-56" if c == EXISTING_CTOR else "generic")
    print("  %08X x%-4d %s" % (c, n, tag))
print("PInputs members                      : %d" % len(pinputs))
print("existing-56 members                  : %d  (set == declared file: %s)"
      % (len(existing), {m[0] for m in existing} == declared_56))
print("generic members                      : %d over %d callees"
      % (len(generic), len({m[2] for m in generic})))
print("group B members calling 006388C0     : %d" % len(name_only))
print("group B arg2 == descriptor           : %d of %d"
      % (sum(1 for m in name_only if m[3] == m[1]), len(name_only)))
print("my members A-measured                : %d" % sum(1 for e in mine if e in a_set))
print("my members already declared          : %d" % sum(1 for e in mine if e in dec))

if "--write" in sys.argv:
    assert len(members) == 530 and len(group_a) == 420 and len(group_b) == 110
    assert not other_tail
    # generic 44 -> 43: one generic member has since been measured A and is excluded above (its row was already 43);
    # count guard only, the predicate is unchanged (SWE2-EC7, 2026-09-30, ec7-accounting-ruling-round-0930).
    assert len(pinputs) == 319 and len(name_only) == 110 and len(generic) == 43
    assert {m[0] for m in existing} == declared_56
    assert all(m[3] == m[1] for m in name_only)
    assert not any(e in a_set for e in mine)
    assert not any(e in dec for e in mine)

    os.makedirs(os.path.dirname(OUT_PINPUTS), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_NAMEONLY), exist_ok=True)

    reg = {0x00879570: "PInputChannelSemantic@02EB9D80",
           0x00876C80: "PInputKeySemantic@02EB83B8",
           0x008768A0: "PInputJoypadButtonSemantic@02EB8348",
           0x008760A0: "PInputTypeSemantic@02EB8260",
           0x00876490: "PInputAxisSemantic@02EB82D8"}
    with io.open(OUT_PINPUTS, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 319 MSVC dynamic-initialiser stubs, each constructing one node of a Phyre PInputs\n")
        f.write("# semantic name registry and atexit-registering its teardown. Same 32-byte form as\n")
        f.write("# the rest of static-init-form-530; the callee column names the documented registry.\n")
        f.write("# select_static_init_form.py --write\n")
        f.write("entry\tsize\tobject\tcallee\tregistry\tdtor\n")
        for e, obj, callee, arg2, tail in pinputs:
            f.write("%08X\t%d\t%08X\t%08X\t%s\t%08X\n" % (e, SIZE, obj, callee, reg[callee], arg2))

    with io.open(OUT_NAMEONLY, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 110 MSVC dynamic-initialiser stubs, each passing one Phyre class descriptor to\n")
        f.write("# 006388C0 PType_FindOrRegisterByName and tail-jumping 00639450, the shared\n")
        f.write("# class-registration finaliser. Name-only registrations: the body's own work is\n")
        f.write("# the lookup; the finaliser sets the +0xFC registered bit. Same 32-byte form as\n")
        f.write("# static-init-form-530 group A; second lea re-loads the descriptor, not a dtor.\n")
        f.write("# select_static_init_form.py --write\n")
        f.write("entry\tsize\tdescriptor\n")
        for e, obj, callee, arg2, tail in name_only:
            f.write("%08X\t%d\t%08X\n" % (e, SIZE, obj))

    with io.open(OUT_GENERIC, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 44 MSVC dynamic-initialiser stubs of assorted static objects: the same 32-byte\n")
        f.write("# construct-then-atexit form as the named registry families, but spread over 30\n")
        f.write("# distinct callees with no common owner - the generic remainder of\n")
        f.write("# static-init-form-530 group A once the two named registry sets are taken out.\n")
        f.write("# select_static_init_form.py --write\n")
        f.write("entry\tsize\tobject\tcallee\tdtor\n")
        for e, obj, callee, arg2, tail in generic:
            f.write("%08X\t%d\t%08X\t%08X\t%08X\n" % (e, SIZE, obj, callee, arg2))

    print("wrote", os.path.relpath(OUT_PINPUTS, REPO))
    print("wrote", os.path.relpath(OUT_NAMEONLY, REPO))
    print("wrote", os.path.relpath(OUT_GENERIC, REPO))
