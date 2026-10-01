"""The CFG static-guard adapter family declares 145; the form its own note describes holds 185.

This does NOT assert the family is wrong. check_dispositions already documents this exact shape:
a gap between a family's declared members and the population its control describes is
"almost always STALENESS, not a bad family ... re-run its selector". The job here is to measure
the gap precisely and to try to FALSIFY it - to find a discriminator, other than form and target,
that would justify excluding the extras. If one exists the family is simply right and I say so.

Controls, all of which can come out either way:
  1. Do any DECLARED members fall OUTSIDE my form? If yes my form is over-narrow and the
     comparison is void.
  2. Are the extras dispositioned elsewhere? A member of another family is a legitimate
     exclusion, because the gate refuses cross-family collisions.
  3. Is the lea destination's SECTION a discriminator? If the declared 145 point into one
     section and the extras into another, the family is selecting correctly and I am wrong.
  4. Is the gap an ADDRESS RANGE - a selector run over a span rather than over the form?
  5. Is Control Flow Guard, which the family is NAMED after, present in this image at all?
  6. HOW is each body registered with atexit? This is the one that explains the gap.

Result: 1-4 find no discriminator, 5 shows the name is unsupported, and 6 finds the cause -
the selector saw the `call` spelling of the atexit registration and missed the tail-call
spelling, so the gap is mechanical rather than a judgement about what belongs.

AND A WARNING ABOUT CONTROL 6, WHICH IS WHY IT IS WRITTEN THE WAY IT IS. Its first version
accepted only E8 (call) after the lea. It reported 0 of 36 registered against 144 of 145 - a
clean discriminator that would have vindicated the family and retracted a TRUE finding. The
36 register by tail call, `add rsp,N ; jmp`, and an instrument blind to a tail call converts a
real gap into a false all-clear. Every earlier instrument error in this register over-counted;
this one under-counted, wearing the shape of the answer I was looking for.
"""
import io, struct, sys, collections

EXE = 'D:/FFXII MP Mod/FFXII_TestClient1/x64/FFXII_TZA.exe'
sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import check_dispositions as CD
import check_coverage_cross as CC

DB = 'Database/FFXII TZA'
FAMILY_DOC = (DB + '/24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown/'
                   'static-initialisers-and-teardowns.md')
MEMBERS = 'members/cfg-static-guard-adapters.tsv'
TARGET = 0x0016D6A0
SIZE = 12

d = io.open(EXE, 'rb').read()
pe = struct.unpack_from('<I', d, 0x3c)[0]
nsec = struct.unpack_from('<H', d, pe + 6)[0]
optsz = struct.unpack_from('<H', d, pe + 20)[0]
base = struct.unpack_from('<Q', d, pe + 24 + 24)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + i * 40
    name = d[o:o + 8].rstrip(b'\0').decode('latin1')
    vsz, va, rsz, ptr = struct.unpack_from('<IIII', d, o + 8)
    secs.append((name, va, vsz, ptr, rsz))


def off(va):
    r = va - base
    for _n, sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return ptr + (r - sva)
    return None


def sect(va):
    r = va - base
    for n, sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return n
    return '?'


sizes = CD.load_functions(None)

# ---- the form, stated as bytes, not as a description -------------------------------------
# 48 8D 0D <disp32>     lea rcx, [rip+disp]
# E9       <rel32>      jmp <target>
hits = []
for e, sz in sizes.items():
    if sz != SIZE:
        continue
    o = off(e)
    if o is None or o + SIZE > len(d):
        continue
    b = d[o:o + SIZE]
    if b[0:3] != b'\x48\x8d\x0d' or b[7] != 0xE9:
        continue
    disp = struct.unpack_from('<i', b, 3)[0]
    rel = struct.unpack_from('<i', b, 8)[0]
    hits.append((e, e + 7 + disp, e + 12 + rel))

by_target = collections.Counter(t for _e, _l, t in hits)
print("12-byte `lea rcx,[x]; jmp y` bodies census-wide : %d" % len(hits))
print("distinct tail-jump targets                      : %d" % len(by_target))
for t, n in by_target.most_common(8):
    print("   %08X  x%-5d" % (t, n))

mine = sorted(e for e, _l, t in hits if t == TARGET)
leas = {e: l for e, l, t in hits if t == TARGET}
print("\nBODIES WITH THE FAMILY'S OWN DECLARED TARGET %08X : %d" % (TARGET, len(mine)))

declared = set(CD.read_members(FAMILY_DOC, MEMBERS))
print("members file declares                            : %d" % len(declared))

# CONTROL 1 - is my form over-narrow?
outside = sorted(declared - set(mine))
print("\nCONTROL 1  declared members NOT in my form       : %d" % len(outside))
if outside:
    print("   -> MY FORM IS OVER-NARROW; the comparison is void.")
    for e in outside[:10]:
        print("      %08X size=%s" % (e, sizes.get(e)))

extras = [e for e in mine if e not in declared]
print("bodies in the form but NOT declared by it        : %d" % len(extras))

# CONTROL 2 - are the extras already dispositioned?
a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ('B', 'C', 'D'):
        continue
    try:
        for m in CD.read_members(doc, parts[2]):
            dec.setdefault(m, '%s %s' % (parts[1], parts[0]))
    except (IOError, OSError, ValueError):
        pass
anyc = CC.cited_anywhere(DB, sizes, CD)

other_fam = [e for e in extras if e in dec]
untouched = [e for e in extras
             if e not in a_set and e not in dec and e not in anyc]
print("\nCONTROL 2  disposition of the %d extras:" % len(extras))
print("   A-measured            : %d" % sum(1 for e in extras if e in a_set))
print("   in ANOTHER family     : %d   (a legitimate exclusion)" % len(other_fam))
for e in other_fam:
    print("      %08X  %s" % (e, dec[e]))
print("   cited by some doc     : %d" % sum(1 for e in extras if e in anyc))
print("   UNTOUCHED frontier    : %d" % len(untouched))

# CONTROL 3 - does the lea destination's section separate them?
dsec = collections.Counter(sect(leas[e]) for e in mine if e in declared)
esec = collections.Counter(sect(leas[e]) for e in extras)
print("\nCONTROL 3  section of the lea destination:")
print("   declared 145 -> %s" % dict(dsec))
print("   the extras   -> %s" % dict(esec))
if set(dsec) & set(esec):
    print("   -> SECTION IS NOT THE DISCRIMINATOR. Both land in the same section(s).")
else:
    print("   -> SECTION SEPARATES THEM; the family is selecting correctly and I am wrong.")

# CONTROL 4 - is the gap an ADDRESS RANGE? a selector run over a range would look like this
if declared and extras:
    print("\nCONTROL 4  extent:")
    print("   declared : %08X .. %08X" % (min(declared), max(declared)))
    print("   extras   : %08X .. %08X" % (min(extras), max(extras)))
    inside = [e for e in extras if min(declared) <= e <= max(declared)]
    print("   extras INSIDE the declared extent : %d of %d" % (len(inside), len(extras)))
    if len(inside) == 0:
        print("   -> the extras all sit outside the declared span: consistent with a "
              "selector run over a RANGE rather than over the form.")


# CONTROL 5 - the name. Is Control Flow Guard even enabled in this image?
dllch = struct.unpack_from('<H', d, pe + 24 + 70)[0]
ddoff = pe + 24 + 112 + 10 * 8
lcva, lcsz = struct.unpack_from('<II', d, ddoff)
lo = off(base + lcva)
gft, gfc = struct.unpack_from('<QQ', d, lo + 0x80)
gflags = struct.unpack_from('<I', d, lo + 0x90)[0]
print("\nCONTROL 5  is CFG actually present in this image?")
print("   DllCharacteristics %04X - GUARD_CF (0x4000): %s"
      % (dllch, 'SET' if dllch & 0x4000 else 'CLEAR'))
print("   GuardCFFunctionTable %016X count=%d" % (gft, gfc))
print("   guard flags %08X - FUNCTION_TABLE_PRESENT (0x400): %s"
      % (gflags, 'SET' if gflags & 0x400 else 'CLEAR'))
to = off(TARGET)
print("   %08X is %d bytes: %s" % (TARGET, sizes.get(TARGET, 0),
                                   d[to:to + (sizes.get(TARGET) or 3)].hex()))
if not (dllch & 0x4000) and gfc == 0:
    print("   -> CFG IS NOT ENABLED AND HAS NO FUNCTION TABLE HERE. The name is unsupported.")

# CONTROL 6 - the registration form. THIS is the one that separates them, and the
# first version of this test was WRONG: it accepted only E8 (call) after the lea and
# reported 0 of 36 registered, which looked like a clean discriminator vindicating the
# family. The 36 register by TAIL CALL - `add rsp,N ; jmp` - and an instrument that
# cannot see a tail call turns a true gap into a false all-clear. Both forms are counted.
ATEXIT = 0x00808B90
tsec = [s for s in secs if s[0] == '.text'][0]
_n, tva, tvsz, tptr, trsz = tsec
regform = {}
for i in range(max(tvsz, trsz) - 24):
    if d[tptr + i] != 0x48 or d[tptr + i + 1] != 0x8D:
        continue
    if (d[tptr + i + 2] & 0xC7) != 0x05:
        continue
    va = base + tva + i
    tgt = va + 7 + struct.unpack_from('<i', d, tptr + i + 3)[0]
    if tgt not in leas:
        continue
    j, cur = tptr + i + 7, va + 7
    if d[j] == 0x48 and d[j + 1] == 0x83 and d[j + 2] == 0xC4:   # add rsp,imm8
        j += 4
        cur += 4
    if d[j] in (0xE8, 0xE9):
        dst = cur + 5 + struct.unpack_from('<i', d, j + 1)[0]
        if dst == ATEXIT:
            regform[tgt] = 'call' if d[j] == 0xE8 else 'jmp'
print("\nCONTROL 6  how each body is registered with the atexit wrapper %08X:" % ATEXIT)
print("   registered, either form : %d of %d" % (len(regform), len(mine)))
tab = collections.Counter()
for e in mine:
    tab[('declared' if e in declared else 'NOT declared', regform.get(e, 'unregistered'))] += 1
print("   %-14s %6s %6s %14s" % ('', 'call', 'jmp', 'unregistered'))
for g in ('declared', 'NOT declared'):
    print("   %-14s %6d %6d %14d"
          % (g, tab[(g, 'call')], tab[(g, 'jmp')], tab[(g, 'unregistered')]))
print("   -> both shapes reach the SAME wrapper, so the split is mechanical, not semantic:")
print("      the selector found the `call` spelling and missed the tail-call spelling.")

out = 'Database/FFXII TZA/_index/candidates/cfg-guard-adapter-gap-40.tsv'
with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write("# NOT A DECLARED FAMILY, AND NOT A DEFECT CLAIM ABOUT ANY DECLARED BODY.\n")
    f.write("# Bodies satisfying the form AND the tail-jump target that the accepted family\n")
    f.write("# 'Control Flow Guard static-guard adapters' states as its control, but which\n")
    f.write("# its members file does not list. 4 of the 40 are legitimately excluded as\n")
    f.write("# members of NativeAdapter.StaticAddressTailCall; 36 are untouched frontier.\n")
    f.write("#\n")
    f.write("# CAUSE, from control 6: the registration form is the selector's blind spot.\n")
    f.write("# Both `call 00808B90` and `add rsp,N ; jmp 00808B90` register the same object\n")
    f.write("# with the same atexit wrapper, and all 185 bodies use one or the other.\n")
    f.write("# declared 144 call / 1 jmp;  NOT declared 3 call / 37 jmp.\n")
    f.write("address\tlea_target\tlea_section\tatexit_reg_form\tdisposition\n")
    for e in extras:
        st = dec.get(e) or ('A' if e in a_set else ('cited' if e in anyc else 'untouched'))
        f.write("%08X\t%08X\t%s\t%s\t%s\n"
                % (e, leas[e], sect(leas[e]), regform.get(e, 'unregistered'), st))
print("\nwrote %s (%d rows)" % (out, len(extras)))
