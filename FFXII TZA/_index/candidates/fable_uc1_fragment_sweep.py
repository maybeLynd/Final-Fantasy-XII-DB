# uc1_fragment_sweep.py - decode every listed body and every admitted 1-64 B `admit` block linearly; collect
# every direct branch (jcc / jmp, not call). A block that is a FUNCTION is entered at its start by call or
# by a tail jmp; a block entered by a jcc, or anywhere past its start, is a FRAGMENT of the branching
# function. Known positive: 0076666F is the target of four jcc in 007651F0 (the pred_branch finding).
import bisect, collections, io, os, struct, sys
import capstone
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
EXE = os.path.join(ROOT, r"Database\Tools\work\exe\FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, r"Database\Tools\work\graph\functions.tsv")
BAND = os.path.join(ROOT, r"Database\FFXII TZA\_index\candidates\uc1-band-1-64-fable-2026-09-25.tsv")
ADM = os.path.join(ROOT, r"Database\FFXII TZA\99-Unresolved-Residual\Unlisted-Code\unlisted-body-admissions.tsv")
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    if d[o:o + 8].rstrip(b"\0") == b".text":
        vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
TVA = 0x120000 + va
def off(v):
    return ro + v - TVA if TVA <= v < TVA + min(vs, rs) else None
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
listed = []
for line in io.open(FUNCS, encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    try:
        listed.append((int(p[0], 16), int(p[2])))
    except (ValueError, IndexError):
        pass
band = [l.rstrip("\n").split("\t") for l in io.open(BAND, encoding="utf-8") if not l.startswith("#")][1:]
admit = sorted((int(r[0], 16), int(r[1])) for r in band if r[8] == "admit")
allbody = sorted((int(r[0], 16), int(r[1])) for r in
                 (l.rstrip("\n").split("\t") for l in io.open(ADM, encoding="utf-8") if not l.startswith("#"))
                 if len(r) > 8 and r[8] == "body")
starts = [s for s, _ in admit]
def which(t):
    k = bisect.bisect_right(starts, t) - 1
    if k >= 0 and starts[k] <= t < starts[k] + admit[k][1]:
        return admit[k][0]
    return None
hits = collections.defaultdict(list)          # block -> [(site, mnemonic, at_start)]
calls = collections.Counter()
def sweep(v, n, src):
    o = off(v)
    if o is None or n <= 0:
        return
    for i in md.disasm(d[o:o + n], v):
        if i.op_str.startswith("0x") and (i.mnemonic.startswith("j") or i.mnemonic == "call"):
            t = int(i.op_str, 16)
            b = which(t)
            if b is None or (v <= t < v + n and src == "admitted"):
                continue
            if i.mnemonic == "call":
                calls[b] += 1
            else:
                hits[b].append((i.address, i.mnemonic, t == b, src))
for v, n in listed:
    sweep(v, n, "listed")
for v, n in allbody:
    sweep(v, n, "admitted")
print("known positive (0076666F is not in `admit`, so test via a direct decode of 007651F0):")
kp = [i for i in md.disasm(d[off(0x7651F0):off(0x7651F0) + 0x2000], 0x7651F0)
      if i.mnemonic.startswith("j") and i.op_str == "0x76666f"]
print("   jcc into 0076666F found:", len(kp))
frag = {b: h for b, h in hits.items() if any(m != "jmp" or not st for _, m, st, _ in h)}
tail = {b: h for b, h in hits.items() if b not in frag}
print("admit rows:", len(admit), " entered only by call/tail-jmp at start or not at all:",
      len(admit) - len(frag), " entered by jcc or past the start:", len(frag))
print("   of the clean rows, called:", sum(1 for s, _ in admit if calls[s]), " tail-jmp'd:", len(tail))
for b in sorted(frag):
    print("  FRAGMENT? %08X" % b, ["%08X %s %s %s" % (s, m, "start" if st else "interior", src) for s, m, st, src in frag[b][:4]])
