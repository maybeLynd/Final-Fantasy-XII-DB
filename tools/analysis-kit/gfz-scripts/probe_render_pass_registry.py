#!/usr/bin/env python3
"""02CBF998 - the named render-pass registry, and the 60 teardowns that unlink from it.

WHAT THIS EXPLAINS. `02CBF998` is rank 8 of the forty hottest globals in UNEXPLAINED-GLOBALS.md -
1 writer, 63 readers, 58 address-taken, and explained by nothing. It is the head of a singly
linked, NAME-KEYED intrusive registry, and both sides of its contract are read from the bytes here
rather than inferred.

  node layout      +0x00  const char *name
                   +0x08  node *next

  005FDCB0  REGISTER, 132 bytes. Loads name = [rcx]; returns 0x11 if it is null. Walks the list
            from the head doing an inline byte-by-byte strcmp against each node's name; returns
            0x12 on a duplicate name. Otherwise pushes the node on the FRONT - [rcx+8] = head,
            head = rcx - and returns 0.

  005DDD60  UNREGISTER, 79 bytes. Walks from the head comparing the address of each node's `next`
            field against rcx+8, unlinks the node by writing its successor through the previous
            slot, and nulls the removed node's next. Returns with no value.

  x60       teardown wrappers, each 12 bytes: `lea rcx,[its own node] ; jmp 005DDD60`, every one
            registered with the MSVC atexit wrapper 00808B90 by the TAIL-CALL spelling.

WHY THE NAMES ARE NOT IN THE FILE. The nodes live past the raw end of `.data` - uninitialised
tail - so `name` is written at run time by each static's constructor and reading node+0x00 out of
the image yields nothing. A first attempt did exactly that and crashed on a short buffer, which is
the honest failure. The names are recovered instead from the REGISTRATION SITES: the function that
takes a node's address also leas the literal it registers under.

THE ANSWER: they are PhyreEngine render passes and post-process effects - ShadowRender, OpaqueDepth,
RenderFXAA, RenderScreenSpaceReflection, RenderDoFComposite, RenderText_SoftEdgesAndGlow,
PrecomputeSingleScattering, VideoScreen ...

Run from the repository root.
"""
import bisect
import collections
import io
import struct
import sys

EXE = 'D:/FFXII MP Mod/FFXII_TestClient1/x64/FFXII_TZA.exe'
sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import check_dispositions as CD
import check_coverage_cross as CC

DB = 'Database/FFXII TZA'
HEAD = 0x02CBF998
UNREG = 0x005DDD60
REG = 0x005FDCB0
ATEXIT = 0x00808B90

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


def off(va, need=1):
    """File offset, or None. RETURNS NONE IN THE UNINITIALISED TAIL, deliberately: a section's
    virtual size exceeds its raw size and reading past it is how the first version crashed."""
    r = va - base
    for _n, sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            o = ptr + (r - sva)
            return o if (r - sva) < rsz and o + need <= len(d) else None
    return None


def cstr(va, n=80):
    o = off(va)
    if o is None:
        return None
    e = d.find(b'\0', o, o + n)
    if e < 0:
        return None
    s = d[o:e]
    if not s or not all(32 <= c < 127 for c in s):
        return None
    return s.decode('ascii')


sizes = CD.load_functions(None)
body2node = {}
for e, sz in sizes.items():
    if sz != 12:
        continue
    o = off(e, 12)
    if o is None:
        continue
    b = d[o:o + 12]
    if b[0:3] != b'\x48\x8d\x0d' or b[7] != 0xE9:
        continue
    if e + 12 + struct.unpack_from('<i', b, 8)[0] == UNREG:
        body2node[e] = e + 7 + struct.unpack_from('<i', b, 3)[0]
nodes = set(body2node.values())
print("teardown wrappers tail-jumping %08X : %d" % (UNREG, len(body2node)))

_n, tva, tvsz, tptr, trsz = [s for s in secs if s[0] == '.text'][0]
ks = sorted(sizes)


def owner(va):
    i = bisect.bisect_right(ks, va) - 1
    return ks[i] if i >= 0 and ks[i] <= va < ks[i] + sizes[ks[i]] else None


fn = collections.defaultdict(lambda: {'n': set(), 's': []})
for i in range(max(tvsz, trsz) - 7):
    if d[tptr + i] != 0x48 or d[tptr + i + 1] != 0x8D:
        continue
    if (d[tptr + i + 2] & 0xC7) != 0x05:
        continue
    va = base + tva + i
    t = va + 7 + struct.unpack_from('<i', d, tptr + i + 3)[0]
    f = owner(va)
    if f is None:
        continue
    if t in nodes:
        fn[f]['n'].add(t)
    else:
        s = cstr(t)
        if s and 2 < len(s) < 60:
            fn[f]['s'].append(s)

# A registration site names exactly ONE node and leas at least one literal. Requiring exactly one
# node is the control: a function touching several nodes cannot tell us which name is whose.
node2name = {}
for f, v in fn.items():
    if len(v['n']) == 1 and v['s']:
        node2name.setdefault(next(iter(v['n'])), (v['s'][0], f))
print("registration sites naming exactly one node : %d" % len(node2name))
print("of the %d nodes, named                     : %d" % (len(nodes), len(node2name)))

a_set, _e, _a, _dd = CD.measure_a(DB, sizes)
declf = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ('B', 'C', 'D'):
        continue
    try:
        for m in CD.read_members(doc, parts[2]):
            declf.setdefault(m, parts[0])
    except (IOError, OSError, ValueError):
        pass
anyc = CC.cited_anywhere(DB, sizes, CD)
und = [b for b in body2node if b not in a_set and b not in declf and b not in anyc]
print("disposition of the %d wrappers: A %d, declared %d, cited %d, UNTOUCHED %d"
      % (len(body2node), sum(1 for b in body2node if b in a_set),
         sum(1 for b in body2node if b in declf),
         sum(1 for b in body2node if b in anyc), len(und)))

out = DB + '/_index/candidates/render-pass-registry-teardowns-60.tsv'
with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write("# NOT A DECLARED FAMILY. Evidence for the named render-pass registry at %08X.\n" % HEAD)
    f.write("# Each row: a 12-byte teardown `lea rcx,[node] ; jmp %08X`, the registry node it\n" % UNREG)
    f.write("# unlinks, and the name that node is registered under - recovered from the\n")
    f.write("# REGISTRATION SITE, because the nodes sit past the raw end of .data and their\n")
    f.write("# name field is written at run time, not stored in the image.\n")
    f.write("# register %08X: 0 ok, 0x11 null name, 0x12 duplicate name. node: +0 name, +8 next.\n" % REG)
    f.write("teardown\tnode\tregistered_name\tregistration_site\tdisposition\n")
    for b in sorted(body2node, key=lambda x: node2name.get(body2node[x], ('~',))[0]):
        n = body2node[b]
        nm, site = node2name.get(n, ('?', 0))
        st = declf.get(b) or ('A' if b in a_set else ('cited' if b in anyc else 'untouched'))
        f.write("%08X\t%08X\t%s\t%08X\t%s\n" % (b, n, nm, site, st))
print("\nwrote %s (%d rows)" % (out, len(body2node)))
names = sorted(v[0] for v in node2name.values() if v[0] != '?')
print("names, %d of them: %s" % (len(names), ', '.join(names[:10]) + ' ...'))
