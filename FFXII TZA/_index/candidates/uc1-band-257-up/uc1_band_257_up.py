"""uc1_band_257_up.py - OPUS (Claude Opus 5.5), 2026-09-28. Derived from ../uc1-band-65-256/uc1_band_65_256.py with only the
band bounds, file names and the added U / X columns changed. UC-1's band above 256 B (the last one), as FABLE's ruling (uc1-band-ruling-fable-
2026-09-25.md s4) set it: "per-row review of the rows that pass every signal, with a byte-table test added before any
vote". STATIC, certified EXE only. This proposes nothing about the population; it produces the per-row evidence.

Per `body` row of more than 256 B in unlisted-body-admissions.tsv (50 rows):
  FABLE's signals, reused from fable_uc1_band_ruling.py's own definitions (not re-implemented):
    gate      the admissions TSV's decodes_to_end
    aligned16 / referenced (pass-6 admissible column) / multi (more than one straight-line body) / pred_branch
  NEW - the byte-table test (the gate cannot see data that decodes as code):
    BT1 operand hits: any instruction of a LISTED body whose memory operand targets the block's interior (start excluded):
        a rip-relative operand, or a displacement read as an image-base RVA ([reg + index*scale + rva], MSVC's
        switch-table form). An indexed hit means a table lives inside the block.
    BT2 table-row targets: any u32 image-base RVA inside the 431 classified `table` rows that lands in the block: the
        block is a switch arm of another body, i.e. a continuation, not a separate body.
    BT3 rip-relative LEAs from listed bodies to the block's interior: an interior entry or embedded data.
Per-row outcome (evidence, not a ruling): 'clean' = gate, not multi, not pred_branch, aligned or referenced, and no BT
hit; otherwise the first failing reason.
Controls:
  C1 BT1 fires on known tables: every 1-64 B `table` row whose `why` names an inline jump table is hit by BT1 or BT2 or
     lies inside a listed body's indexed operand range (reported as a rate - the test's sensitivity)
  C2 BT1 / BT2 / BT3 find no interior hit in the 694 admitted 1-64 B rows except the ones FABLE's ruling already held
     (a specificity control on accepted bodies)
Writes uc1-band-257-up-rows.tsv beside this file (only with --write). Usage: python uc1_band_257_up.py [--write]
"""
import bisect, collections, hashlib, io, os, struct, sys
import capstone
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP, X86_REG_INVALID
HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(CAND, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
if hashlib.sha256(open(EXE, "rb").read()).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
# FABLE's definitions (read-only prefix of her instrument: image load, dis / shape / multi / branches_into, listed sizes)
src = io.open(os.path.join(CAND, "fable_uc1_band_ruling.py"), encoding="utf-8").read()
prefix = src.split("\nif not listed:")[0]
g = {"__file__": os.path.join(CAND, "fable_uc1_band_ruling.py")}
exec(compile(prefix, "fable_uc1_band_ruling.py[prefix]", "exec"), g)
d, multi, branches_into, listed = g["d"], g["multi"], g["branches_into"], g["listed"]
sizes = dict(listed); off = g["off"]; B = 0x120000
rows = [l.rstrip("\n").split("\t") for l in io.open(g["ADM"], encoding="utf-8") if not l.startswith("#")][1:]
band = [r for r in rows if r[8] == "body" and int(r[1]) > 256]
small = [r for r in rows if r[8] == "body" and 1 <= int(r[1]) <= 64]
tables = [r for r in rows if r[8] == "table"]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

# intervals of every candidate block (both bands) for BT lookups
blocks = sorted((int(r[0], 16), int(r[1]), r[0]) for r in band + small)
bstarts = [b[0] for b in blocks]
def block_of(t):
    i = bisect.bisect_right(bstarts, t) - 1
    return blocks[i] if i >= 0 and blocks[i][0] <= t < blocks[i][0] + blocks[i][1] else None
IMG_END = B + struct.unpack_from("<I", d, struct.unpack_from("<I", d, 0x3C)[0] + 24 + 56)[0]  # SizeOfImage
hits = collections.defaultdict(list)          # block start hex -> [(kind, site)]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail = True
# sources: the listed bodies, and (for BT4 only) the unlisted body blocks themselves - the frontier bodies of the applied
# 1-64 B band and this band's own rows can branch into a neighbour's interior too
SRC = [(f, n, True) for f, n in listed] + [(b[0], b[1], False) for b in blocks]
for f, n, is_listed in SRC:
    o = off(f)
    if o is None or n <= 0: continue
    for x in md.disasm(d[o:o + n], f):
        # BT4 (alternative entries): a direct call / jmp / jcc into a block's interior (not from inside that block)
        if (x.mnemonic == "call" or x.mnemonic.startswith("j")) and len(x.operands) == 1 and x.operands[0].type == X86_OP_IMM \
                and (is_listed or block_of(x.address) != block_of(x.operands[0].imm)):
            t = x.operands[0].imm; bk = block_of(t)
            if bk and t != bk[0]:
                hits[bk[2]].append(("BT4", x.mnemonic, "%08X" % x.address, "+0x%X" % (t - bk[0])))
        if not is_listed: continue                    # BT1 / BT3 read listed bodies only, as documented
        for op in x.operands:
            if op.type != X86_OP_MEM: continue
            m = op.mem
            if m.base == X86_REG_RIP:
                t = x.address + x.size + m.disp; kind = "lea" if x.mnemonic == "lea" else "rip"
            elif m.index != X86_REG_INVALID and 0x1000 <= m.disp < IMG_END - B:
                t = B + m.disp; kind = "indexed-rva"
            else:
                continue
            bk = block_of(t)
            if bk and t != bk[0]:
                hits[bk[2]].append(("BT3" if kind == "lea" else "BT1", kind, "%08X" % x.address, "+0x%X" % (t - bk[0])))
for r in tables:
    s, n = int(r[0], 16), int(r[1])
    o = off(s)
    for k in range(0, n - 3, 4):
        v = struct.unpack_from("<I", d, o + k)[0]
        bk = block_of(B + v)
        if bk:
            hits[bk[2]].append(("BT2", "table-entry", r[0], "+0x%X" % (B + v - bk[0])))

PD = [x for x in g.get("SECS", [])] if False else None
import struct as _st, pefile as _pe
_p = _pe.PE(EXE, fast_load=True); _pd = [x for x in _p.sections if x.Name.startswith(b".pdata")][0]
_RF = [_st.unpack_from("<III", d, _pd.PointerToRawData + 12 * k) for k in range(_pd.SizeOfRawData // 12)]
_RF = [(b0 + B, e0 + B) for b0, e0, u in _RF if b0]
def unwind(v, n):
    """(pdata at or covering start, pdata beginning strictly inside) for [v, v + n)"""
    at = any(b0 <= v < e0 for b0, e0 in _RF); inside = any(v < b0 < v + n for b0, e0 in _RF)
    return at, inside
def nonleaf(v, n):
    for x in md.disasm(d[off(v):off(v) + n], v):
        if x.mnemonic in ("call", "push") or (x.mnemonic == "sub" and x.op_str.startswith("rsp")): return True
    return False
def outcome(r):
    v, n, pv = int(r[0], 16), int(r[1]), int(r[2], 16)
    al, ref = v % 16 == 0, r[4] == "yes"
    gate = r[7] == "yes"; m = multi(v, n); pb = branches_into(pv, sizes.get(pv, 0), v, v + n)
    h = hits.get(r[0], [])
    why = ("gate" if not gate else "multi" if m else "pred_branch" if pb else
           "unaligned-unreferenced" if not (al or ref) else ("byte-table:" + h[0][0]) if h else "clean")
    at, inside = unwind(v, n); nl = nonleaf(v, n)
    if why == "clean" and inside: why = "pdata-inside"
    if why == "clean" and nl and not at: why = "nonleaf-no-unwind"
    return (r[0], n, r[2], "yes" if gate else "no", "yes" if al else "no", "yes" if ref else "no", "yes" if m else "no",
            "yes" if pb else "no", len(h), "; ".join("%s %s %s %s" % x for x in h[:3]), "yes" if at else "no", "yes" if inside else "no",
            "yes" if nl else "no", why)
out = [outcome(r) for r in band]
cnt = collections.Counter(o[-1].split(":")[0] for o in out)
print(">256 B band: %d rows; outcomes %s" % (len(out), dict(cnt)))
for o in out:
    if o[-1] != "clean": print("   %s %3d %s" % (o[0], o[1], o[-1]), o[9][:90])
# C1: sensitivity on known inline jump tables of the 1-64 band's neighbours - rows classified `table` must be seen as
# data targets by BT1 (their own start or interior is an indexed / rip operand target) - measured as a rate
tset = sorted((int(r[0], 16), int(r[1])) for r in tables); tst = [t[0] for t in tset]
seen = set()
for f, n in listed:
    o = off(f)
    if o is None or n <= 0: continue
    for x in md.disasm(d[o:o + n], f):
        for op in x.operands:
            if op.type == X86_OP_MEM and op.mem.index != X86_REG_INVALID and 0x1000 <= op.mem.disp < IMG_END - B:
                t = B + op.mem.disp; i = bisect.bisect_right(tst, t) - 1
                if i >= 0 and tset[i][0] <= t < tset[i][0] + tset[i][1]: seen.add(tset[i][0])
rate = len(seen) / max(1, len(tset))
check("C1", rate > 0.5, "indexed image-base-RVA operands reach %d of %d classified table rows (%.0f%%) - the test sees tables"
      % (len(seen), len(tset), 100 * rate))
sm = [r[0] for r in small if hits.get(r[0])]
fr = {l.split("\t")[0]: l.rstrip("\n").split("\t")[-1] for l in io.open(os.path.join(CAND, "uc1-band-1-64-fable-2026-09-25.tsv"),
      encoding="utf-8") if not l.startswith("start")}
check("C2", sm and all(fr.get(k) in ("hold-ambiguous", "extend-predecessor") for k in sm) and "007C2A29" in sm,
      "1-64 B rows with an interior hit: %s - each one FABLE held or extended (%s), none she admitted; 007C2A29 is the "
      "extend-listed row whose instruction and native extents differ" % (sm, [fr.get(k) for k in sm]))
lst = sorted(listed); lst_st = [f for f, n in lst]
def collide(v, n):
    i = bisect.bisect_left(lst_st, v + n) - 1
    return i >= 0 and lst[i][0] < v + n and lst[i][0] + lst[i][1] > v
cl = [o for o in out if o[-1] == "clean"]
check("C3", not [o for o in cl if collide(int(o[0], 16), o[1])],
      "no clean row's [start, start + bytes) overlaps a listed body (the 007EE7F0 class): %d clean rows" % len(cl))
if "--write" in sys.argv:
    with io.open(os.path.join(HERE, "uc1-band-257-up-rows.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("start_va\tbytes\tprev_entry\tgate\taligned16\treferenced\tmulti\tpred_branch\tbt_hits\tbt_first\tpdata_at\tpdata_inside\tnonleaf\toutcome\n")
        for o in out: fh.write("\t".join(map(str, o)) + "\n")
    print("wrote uc1-band-257-up-rows.tsv")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
