"""select_libvpx.py - EC-7 member selector for the libvpx VP8 decoder object in 0016xxxx-0017xxxx (FABLE, 2026-09-13).

  libvpx-vp8-decoder.tsv   census entries from 0016DDD0 up to 0017C890 (exclusive) that are joined to the decoder: reached
                           from the seeds by direct calls or leas inside the range, or held in the decoder's interface /
                           control-map tables, or called only by the video client; less entries also called from other
                           outside code (shared CRT wrappers), bodies referenced from more than one .rdata slot (folded),
                           RTTI-bearing entries, A-measured entries and entries declared by another family.
  Seeds: entries that reference the decoder's string pool 01CEB640-01CEBB3F and entries tagged ThirdParty.Video.LibVPX.

Asserts the interface table vpx_codec_vp8_dx_algo at 01CDB290: name pointer -> 'WebM Project VP8 Decoder v1.6.0', ABI version
5, and its init / destroy / peek / get_si / decode / get_frame pointers inside the range; the control map at 01CDB320 with
ids 1-7 and 0x100-0x103 and a -1 terminator (ids 4-7 share the folded 'return VPX_CODEC_INCAPABLE' body 0016EE70). Edges: 0016DA60 below is a red-black-tree helper game code calls; 0017C890 above is libogg's
oggpack_write.
  libvpx-vp8-dsp-kernels.tsv   entries outside the object referenced (call or lea) only by decoder members or other kernels,
                           to a fixpoint, in no .rdata/.data table, not import thunks.
Usage: python select_libvpx.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "libvpx VP8 decoder object"
LO, HI = 0x16DDD0, 0x17C890
POOL = (0x1CEB640, 0x1CEBB40)
CLIENT = (0x670000, 0x680000)
IFACE, CTRLMAP = 0x1CDB290, 0x1CDB320
inr = lambda a: LO <= a < HI
d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(n):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (0x120000 + va, vs, ro, rs)
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs: return ro + (a - va)
sizes = cd.load_functions()
# UC-1 SERIES BREAK (2026-09-28): the default census now also carries the UC-1 frontier bodies,
# which are frontier BY RULING - never A/B/C, and check_dispositions refuses any members file that
# names one. Leave them out of the selection population, so a re-run reproduces the declared family
# (on 2026-09-29 an unpatched re-run admitted 733 of them into PPFX and failed the libvorbis closure
# assertion). They are also absent from the caller/control attribution below. SWE2-EC7 2026-09-29.
import uc1_band
# FABLE ruling, point 4 (SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930; SWE2-EC7 2026-09-30): the UC-1 bodies stay IN
# the population, so every caller/closure/control test sees calls made by a UC-1 body; they are removed only from
# the written members files (a UC-1 body is frontier by ruling, declared only by an R1 span row).
UC1 = set(uc1_band.frontier_starts())
_out = lambda xs: [e for e in xs if e not in UC1]
ents = sorted(sizes); eset = set(ents)
tags = {}
for line in open(os.path.join(W, "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: tags[int(p[0], 16)] = p[8] if len(p) > 8 else ""
    except ValueError: pass
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and parts[0] not in (NAME, "libvpx VP8 DSP kernels"):
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass
rtti = set()
for line in open(os.path.join(W, "rtti", "methods.tsv"), encoding="utf-8", errors="replace"):
    try: rtti.add(int(line.split("\t")[0], 16))
    except ValueError: pass
q = lambda a: struct.unpack_from("<Q", d, off(a))[0]
# interface fingerprint
name = q(IFACE); assert d[off(name):off(name) + 31] == b"WebM Project VP8 Decoder v1.6.0", hex(name)
assert struct.unpack_from("<I", d, off(IFACE) + 8)[0] == 5
iface_fns = [q(IFACE + k) for k in (0x10, 0x18, 0x28, 0x30, 0x38, 0x40)]
assert all(inr(f) and f in eset for f in iface_fns), ["%08X" % f for f in iface_fns]
assert q(IFACE + 0x20) == CTRLMAP
ctrl = [(q(CTRLMAP + 16 * k + 8), struct.unpack_from("<i", d, off(CTRLMAP + 16 * k))[0]) for k in range(12)]
assert [c[1] for c in ctrl] == [1, 2, 3, 4, 5, 6, 7, 0x100, 0x101, 0x102, 0x103, -1] and all(inr(c[0]) for c in ctrl[:11])
table_fns = set(iface_fns) | {c[0] for c in ctrl if inr(c[0])}

text = secs[".text"]; to = text[2]; tn = text[3]
def owner_of(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
callers = collections.defaultdict(set); callees = collections.defaultdict(set)
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to); t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    f = owner_of(src)
    if f is None or f == t: continue
    callers[t].add(f); callees[f].add(t)
assert tags.get(0x16DA60, "").startswith("ContextAudit") or "RedBlackTree" in tags.get(0x16D840, "")
md = Cs(CS_ARCH_X86, CS_MODE_64); rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")
span = [e for e in ents if inr(e)]
leas = collections.defaultdict(set); pool = set()
for e in span:
    for x in md.disasm(d[off(e):off(e) + sizes[e]], e):
        m = rx.search(x.op_str)
        if not m: continue
        t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if POOL[0] <= t < POOL[1]: pool.add(e)
        if inr(t) and t in eset: leas[e].add(t)
slots = collections.Counter()
rd = secs[".rdata"]
for k in range(0, rd[3] - 8, 8):
    v = struct.unpack_from("<Q", d, rd[2] + k)[0]
    if inr(v): slots[v] += 1
seeds = pool | {e for e in span if "LibVPX" in tags.get(e, "")}
reached = set(seeds); stack = list(seeds)
while stack:
    e = stack.pop()
    for nb in list(callees[e]) + list(callers[e]) + list(leas[e]):
        if inr(nb) and nb not in reached: reached.add(nb); stack.append(nb)
members, excl = [], collections.defaultdict(list)
for e in span:
    out_callers = {f for f in callers[e] if not inr(f)}
    client_only = out_callers and all(CLIENT[0] <= f < CLIENT[1] for f in out_callers) and not any(inr(f) for f in callers[e])
    joined = e in reached or e in table_fns or client_only
    if e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    elif e in rtti: excl["carries RTTI (folded)"].append(e)
    elif slots[e] > 1: excl["referenced from %d .rdata slots (folded shared body)" % slots[e]].append(e)
    elif any(not (CLIENT[0] <= f < CLIENT[1]) for f in out_callers): excl["also called from outside the decoder and its client"].append(e)
    elif not joined: excl["joined to the decoder by nothing"].append(e)
    else: members.append(e)
print("libvpx range: entries %d, pool referencers %d, seeds %d, reached %d, members %d" % (len(span), len(pool), len(seeds), len(reached), len(members)))
for k, v in sorted(excl.items()):
    print("  excluded %-55s %3d  %s" % (k, len(v), " ".join("%08X" % x for x in v)))
outb = collections.Counter()
for e in members:
    for t in callees[e]:
        if not inr(t): outb[t] += 1
print("control outbound targets:", " ".join("%08X(%d)" % kv for kv in sorted(outb.items())))
print("control inbound caller zones:", dict(collections.Counter("%04X" % (f >> 16) for e in members for f in callers[e] if not inr(f))))
# --- the decoder's DSP kernels: entries outside the object whose every direct caller and every lea referencer is a decoder
# member or another kernel (fixpoint), held in no .rdata/.data table, not import thunks
# (the referrer set includes decoder-object entries that have since drifted to A-measured: they are still the decoder
# object). Accounting state does not feed the predicate (FABLE ruling on SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930,
# generalised; SWE2-EC7 2026-09-30): an A-measured span body is a closure source only when it passes the SAME tests a
# member passes (RTTI, folded slots, outside callers, joined); being A alone never qualifies it, and it stays A.
def _member_test(e):
    out_callers = {f for f in callers[e] if not inr(f)}
    client_only = out_callers and all(CLIENT[0] <= f < CLIENT[1] for f in out_callers) and not any(inr(f) for f in callers[e])
    joined = e in reached or e in table_fns or client_only
    if e in rtti or slots[e] > 1: return False
    if any(not (CLIENT[0] <= f < CLIENT[1]) for f in out_callers): return False
    return bool(joined)
# FABLE ruling point 3 (SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930; SWE2-EC7 2026-09-30): another family's
# declaration no longer decides qualification; such a body that passes the predicate is a qualifying node, but
# ownership stays with the declaring family - it is removed from the output and printed as a collision.
qualifying_a = {e for e in span if (e in a_set or e in declared) and _member_test(e)}
print("A-measured span bodies that pass the member predicate (kernel-closure sources, stay A, not members): %d" % len(qualifying_a))
dec = set(members) | qualifying_a
refs = collections.defaultdict(set)
for t, fs in callers.items():
    refs[t] |= fs
for e in ents:
    if not (0x121000 <= e < 0x8C2000) or sizes[e] <= 0: continue
    for x in md.disasm(d[off(e):off(e) + sizes[e]], e):
        if x.mnemonic != "lea": continue
        m = rx.search(x.op_str)
        if not m: continue
        t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if t in eset and t != e: refs[t].add(e)
anyptr = collections.Counter()
for sec in (".rdata", ".data"):
    s0 = secs[sec]
    for k in range(0, s0[3] - 8, 8):
        v = struct.unpack_from("<Q", d, s0[2] + k)[0]
        if v in eset: anyptr[v] += 1
kern = set(); changed = True
while changed:
    changed = False
    for t, fs in refs.items():
        if t in dec or t in kern or not fs or inr(t) or anyptr[t]: continue
        if sizes[t] <= 6 and d[off(t):off(t) + 2] == b"\xff\x25": continue      # import thunk
        if all(f in dec or f in kern for f in fs):
            kern.add(t); changed = True
kernels = sorted(e for e in kern if e not in a_set and e not in declared)
print("DSP kernels (exclusively referenced by the decoder object or each other): %d, zones %s" % (
    len(kernels), dict(sorted(collections.Counter("%04X" % (e >> 16) for e in kernels).items()))))
assert 0x125740 in kern and 0x149DC0 in kern and 0x158B40 in kern

if "--write" in sys.argv:
    open(os.path.join(HERE, "libvpx-vp8-dsp-kernels.tsv"), "w").write(
        "# libvpx 1.6.0 VP8 DSP kernels, referenced only by the decoder object or each other - select_libvpx.py\n"
        + "\n".join("%08X" % e for e in _out(kernels)) + "\n")
    open(os.path.join(HERE, "libvpx-vp8-decoder.tsv"), "w").write(
        "# libvpx 1.6.0 VP8 decoder object, 0016DDD0 up to 0017C890, joined entries only - select_libvpx.py\n"
        + "\n".join("%08X" % e for e in _out(members)) + "\n")
    print("wrote", len(_out(members)))
