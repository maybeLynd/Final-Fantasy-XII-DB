"""Across ALL 12-byte `lea rcx,[a static] ; jmp` bodies: how each is registered with atexit,
split against whether an EC-7 family declares it.

Addendum 13ao found the Control Flow Guard family's selector matched `call 00808B90` and missed
the tail-call spelling `add rsp,N ; jmp 00808B90`. This asks whether that is one family's slip or
something wider - and the answer is neither of the two things I guessed.

IT IS NOT A SHARED SELECTOR BUG. Six of the seven families holding any of this population are
`call`-spelled almost perfectly; the seventh is NAMED for the other spelling
(NativeAdapter.StaticAddressTailCall) and declares 35 where 141 bodies use it. The population is
under-covered because the one family scoped to it stopped early, not because a tool is broken.

AND IT REOPENS A BOUNDARY. NativeAdapter already declares members at 0016D6A0 - the Control Flow
Guard family's own single target - by the tail-call spelling. So a 12-byte body that jumps to
0016D6A0 and registers by tail call satisfies BOTH families' definitions, and which one owns it is
an adjudication between two accepted families rather than a members-file refresh. That is why the
route this script supports asks for a ruling and not for a regeneration.

Run from the repository root.
"""
import io, struct, sys, collections

EXE = 'D:/FFXII MP Mod/FFXII_TestClient1/x64/FFXII_TZA.exe'
sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import check_dispositions as CD
import check_coverage_cross as CC

DB = 'Database/FFXII TZA'
ATEXIT = 0x00808B90
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
pop, leas = {}, {}
for e, sz in sizes.items():
    if sz != SIZE:
        continue
    o = off(e)
    if o is None or o + SIZE > len(d):
        continue
    b = d[o:o + SIZE]
    if b[0:3] != b'\x48\x8d\x0d' or b[7] != 0xE9:
        continue
    pop[e] = e + SIZE + struct.unpack_from('<i', b, 8)[0]
    leas[e] = e + 7 + struct.unpack_from('<i', b, 3)[0]
print("12-byte `lea rcx,[a static] ; jmp` bodies : %d" % len(pop))

# How is each registered? Accept BOTH spellings - an instrument that accepts only E8 reports a
# clean discriminator that is an artefact of itself. See addendum 13ao.
_n, tva, tvsz, tptr, trsz = [s for s in secs if s[0] == '.text'][0]
form = {}
for i in range(max(tvsz, trsz) - 24):
    if d[tptr + i] != 0x48 or d[tptr + i + 1] != 0x8D:
        continue
    if (d[tptr + i + 2] & 0xC7) != 0x05:
        continue
    va = base + tva + i
    tgt = va + 7 + struct.unpack_from('<i', d, tptr + i + 3)[0]
    if tgt not in pop:
        continue
    j, cur = tptr + i + 7, va + 7
    if d[j] == 0x48 and d[j + 1] == 0x83 and d[j + 2] == 0xC4:      # add rsp,imm8
        j += 4
        cur += 4
    if d[j] in (0xE8, 0xE9):
        dst = cur + 5 + struct.unpack_from('<i', d, j + 1)[0]
        if dst == ATEXIT:
            form[tgt] = 'call' if d[j] == 0xE8 else 'jmp'

declf = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ('B', 'C', 'D'):
        continue
    try:
        for m in CD.read_members(doc, parts[2]):
            declf.setdefault(m, parts[0])
    except (IOError, OSError, ValueError):
        pass
a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
anyc = CC.cited_anywhere(DB, sizes, CD)

tab = collections.Counter()
for e in pop:
    tab[('declared' if e in declf else 'NOT declared', form.get(e, 'no-lea'))] += 1
print("\nREGISTRATION SPELLING x DECLARATION")
print("   %-14s %8s %8s %14s" % ('', 'call', 'jmp', 'no lea site'))
for g in ('declared', 'NOT declared'):
    print("   %-14s %8d %8d %14d" % (g, tab[(g, 'call')], tab[(g, 'jmp')], tab[(g, 'no-lea')]))
for sp in ('call', 'jmp'):
    tot = tab[('declared', sp)] + tab[('NOT declared', sp)]
    print("   declared rate, %-4s-registered : %d/%d = %.1f%%"
          % (sp, tab[('declared', sp)], tot, 100.0 * tab[('declared', sp)] / max(tot, 1)))

per = collections.defaultdict(collections.Counter)
for e in pop:
    f = declf.get(e)
    if f:
        per[f][form.get(e, 'no-lea')] += 1
print("\nPER FAMILY - this is what shows there is NO shared bug:")
print("   %-54s %6s %5s %7s" % ('family', 'call', 'jmp', 'no-lea'))
for f, c in sorted(per.items(), key=lambda kv: -sum(kv[1].values())):
    print("   %-54s %6d %5d %7d" % (f[:54], c['call'], c['jmp'], c['no-lea']))

NA = 'NativeAdapter.StaticAddressTailCall'
natg = collections.Counter(pop[e] for e in pop if declf.get(e) == NA)
und = sorted(e for e in pop if e not in declf and form.get(e) == 'jmp')
undtg = collections.Counter(pop[e] for e in und)
print("\nUNDECLARED tail-call-registered bodies: %d" % len(und))
print("   %-10s %11s %22s" % ('target', 'undeclared', 'already in NativeAdapter'))
for t, n in undtg.most_common():
    print("   %08X %11d %22d %s" % (t, n, natg.get(t, 0), '<- SHARED TARGET' if t in natg else ''))
shared = sum(n for t, n in undtg.items() if t in natg)
print("   -> %d of %d sit at a target that family has ALREADY accepted members from,"
      % (shared, len(und)))
print("      so for those its own declared control already reaches them.")

out = DB + '/_index/candidates/tailcall-registered-undeclared-121.tsv'
with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write("# NOT A DECLARED FAMILY AND NOT ONE FAMILY.\n")
    f.write("# 12-byte `lea rcx,[a static] ; jmp` bodies that register with the atexit wrapper\n")
    f.write("# 00808B90 by the TAIL-CALL spelling (add rsp,N ; jmp) and that no EC-7 family\n")
    f.write("# declares. They fall in several target clusters and are almost certainly several\n")
    f.write("# families - derive each form from its own members rather than from the shared\n")
    f.write("# spelling, which is a place to look and not provenance.\n")
    f.write("#\n")
    f.write("# %d of them sit at a target NativeAdapter.StaticAddressTailCall already declares\n"
            % shared)
    f.write("# members at, and 0016D6A0 is also the sole target of the Control Flow Guard\n")
    f.write("# family - so ownership of that cluster is a boundary question between two\n")
    f.write("# accepted families, not a members-file refresh.\n")
    f.write("address\ttail_target\tlea_target\tlea_section\tdisposition\n")
    for e in und:
        st = 'A' if e in a_set else ('cited' if e in anyc else 'untouched')
        f.write("%08X\t%08X\t%08X\t%s\t%s\n" % (e, pop[e], leas[e], sect(leas[e]), st))
print("\nwrote %s (%d rows)" % (out, len(und)))
print("   untouched frontier among them: %d"
      % sum(1 for e in und if e not in a_set and e not in anyc))
