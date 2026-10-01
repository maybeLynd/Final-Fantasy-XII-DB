"""UC-5a (OPUS, 2026-09-26): the 7 `call`-predecessor blocks (548 B), and whether any continuation tail hides an entry
the four-form reference union (rel32 / RIP-lea / DIR64 / .pdata) cannot see. STATIC over the shipped image.
  U1 the admissions table's `call`-predecessor rows: 7 blocks, 548 bytes (4 `table`, 3 `ambiguous`).
  U2 the 4 table blocks are switch data end to end: DWORD case tables and MSVC byte-index tables, each part named by an
     image-base-relative operand in the predecessor. Every index byte is below its table's entry count; 007E3CC5 opens
     with a 3-byte alignment nop.
  U3 00829E85 and 0082A657 are one dangling `mov rdi,[rsp+0x40]` each, followed by int3 padding. Nothing branches to
     them. The call before each (00824330) never returns:
       00824330 -> 00823860, then int3;
       00823860 -> 0081E2C0, then int3;
       0081E2C0's two exits are the longjmp thunk + int3 and the panic call + an imported abort + int3.
  U4 0082E041 is reached by the predecessor's own `ja` at 0082DE8B. It is a cold path of 0082DCE0:
     call 00823710 (-> 0081D3A0, then int3), then int3.
  U5 the continuation tails: every DWORD position in the mapped image, at any alignment, is compared with each tail's
     RVA. The only aligned data hit is 0036F22E's .pdata entry, the route pass 6 bans and the page already discounts.
     The other hits sit inside instructions of other functions, as parts of an immediate or rel32, and are listed.
     Control: the same scan finds the switch-table RVA stored at 0020FAD4.
Exit 1 on any FAIL; writes result.json."""
import os, re, struct, json, sys, bisect, collections
from pathlib import Path
import pefile, capstone
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[4]
pe = pefile.PE(str(ROOT / "Database/Tools/work/exe/FFXII_TZA.exe")); img = pe.get_memory_mapped_image(); IB = 0x120000
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
imp = {i.address: i.name.decode() for e in pe.DIRECTORY_ENTRY_IMPORT for i in e.imports if i.name}
F = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    c = l.split("\t")
    try: F[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
S = sorted(F)
T = ROOT / "Database/FFXII TZA/99-Unresolved-Residual/Unlisted-Code/unlisted-body-admissions.tsv"
rows = [l.rstrip("\n").split("\t") for l in open(T, encoding="utf-8") if l[:1] not in ("#", "s") and l.strip()]
def dis(a, n): return list(md.disasm(img[a - IB:a - IB + n], a))
def thunk(a):
    o = a - IB
    return imp.get(a + 6 + struct.unpack_from("<i", img, o + 2)[0]) if img[o] == 0xFF and img[o + 1] == 0x25 else None
res = {}; cases = {}
# ---- U1
cp = [r for r in rows if r[3] == "call"]
res["call_rows"] = [[r[0], int(r[1]), r[2], r[8]] for r in cp]
cases["U1_7_call_blocks_548_bytes_4_table_3_ambiguous"] = len(cp) == 7 and sum(int(r[1]) for r in cp) == 548 and \
    collections.Counter(r[8] for r in cp) == {"table": 4, "ambiguous": 3}
# ---- U2
def table_parts(blk, n, prev):
    ins = dis(prev, F[prev]); parts = []
    for i in ins:
        for m in re.finditer(r"\+ 0x([0-9a-f]+)\]", i.op_str):
            v = int(m.group(1), 16) + IB
            if blk <= v < blk + n: parts.append((v, "byte" if i.op_str.startswith(("eax, byte", "ecx, byte")) or "byte ptr" in i.op_str else "dword", i.address))
    parts.sort()
    cov = []; ok = True; detail = []
    for k, (v, kind, at) in enumerate(parts):
        end = parts[k + 1][0] if k + 1 < len(parts) else blk + n
        seg = img[v - IB:end - IB]
        if kind == "dword":
            ents = [struct.unpack_from("<I", seg, j)[0] + IB for j in range(0, len(seg) - len(seg) % 4, 4)]
            ok &= len(seg) % 4 == 0 and all(prev <= e < prev + F[prev] for e in ents); nent = len(ents)
            detail.append(("%08X" % v, "dword x%d" % len(ents), "%08X" % at))
        else:
            nd = max((len(img[p[0] - IB:(parts[q + 1][0] if q + 1 < len(parts) else blk + n) - IB]) // 4) for q, p in enumerate(parts) if p[1] == "dword")
            ok &= max(seg) < nd; detail.append(("%08X" % v, "byte x%d (max %d)" % (len(seg), max(seg)), "%08X" % at))
        cov.append((v, end))
    start = cov[0][0] if cov else blk + n
    pad = img[blk - IB:start - IB]
    ok &= start - blk in (0, 3) and (start == blk or pad == b"\x0f\x1f\x00")
    return ok, detail, start - blk
tabs = {}
tab_ok = True
for r in cp:
    if r[8] != "table": continue
    ok, det, padn = table_parts(int(r[0], 16), int(r[1]), int(r[2], 16)); tab_ok &= ok
    tabs[r[0]] = {"parts": det, "leading_nop": padn, "ok": ok}
res["tables"] = tabs
cases["U2_the_4_table_blocks_are_switch_data_end_to_end"] = tab_ok and len(tabs) == 4
# ---- U3
def ends_int3_after_call(a, callee):
    for i in dis(a, 0x200):
        if i.mnemonic == "call" and i.op_str == hex(callee):
            nxt = dis(i.address + i.size, 1)
            return bool(nxt) and nxt[0].mnemonic == "int3"
    return False
chain = ends_int3_after_call(0x824330, 0x823860) and ends_int3_after_call(0x823860, 0x81E2C0)
exits = [(i.address, i.mnemonic, i.op_str) for i in dis(0x81E2C0, 0x90) if i.mnemonic == "call"]
lj = any(o.startswith("0x") and thunk(int(o, 16)) == "longjmp" for _, m, o in exits)
ab = None
for i in dis(0x81E334, 0x20):
    m = re.match(r"qword ptr \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
    if i.mnemonic == "call" and m: ab = imp.get(i.address + i.size + int(m.group(1), 16))
def any_branch_to(t):
    for m in re.finditer(rb"[\xE8\xE9]", img[0x1000:0x8C0000 - IB]):
        o = m.start() + 0x1000
        if o + IB + 5 + struct.unpack_from("<i", img, o + 1)[0] == t: return True
    k = bisect.bisect_right(S, t - 1) - 1; f = S[k]
    return any(i.mnemonic.startswith("j") and i.op_str == hex(t) for i in dis(f, F[f] + 16))
dangling = {}
for a in (0x829E85, 0x82A657):
    ins = dis(a, 12)
    dangling["%08X" % a] = [ins[0].mnemonic + " " + ins[0].op_str, ins[1].mnemonic, any_branch_to(a)]
u3 = chain and lj and ab == "abort" and all(v[0] == "mov rdi, qword ptr [rsp + 0x40]" and v[1] == "int3" and not v[2] for v in dangling.values())
res["dangling"] = dangling; res["noreturn_chain"] = {"00824330->00823860 int3": ends_int3_after_call(0x824330, 0x823860),
    "00823860->0081E2C0 int3": ends_int3_after_call(0x823860, 0x81E2C0), "0081E2C0 longjmp": lj, "0081E2C0 panic path import": ab}
cases["U3_two_dangling_restores_after_a_call_that_never_returns"] = u3
# ---- U4
ja = [i for i in dis(0x82DCE0, F[0x82DCE0]) if i.mnemonic.startswith("j") and i.op_str == hex(0x82E041)]
blk = dis(0x82E041, 6)
u4 = [("%08X" % i.address, i.mnemonic) for i in ja] == [("0082DE8B", "ja")] and blk[0].op_str == hex(0x823710) and blk[1].mnemonic == "int3" \
     and ends_int3_after_call(0x823710, 0x81D3A0)
res["cold_path"] = {"branches": [("%08X" % i.address, i.mnemonic) for i in ja], "body": [i.mnemonic + " " + i.op_str for i in blk]}
cases["U4_0082E041_is_a_cold_path_reached_by_its_own_ja"] = u4
# ---- U5
tails = [int(r[0], 16) for r in rows if r[8] == "continuation"]
rv = {t - IB: t for t in tails}; b = bytes(img); hits = collections.defaultdict(list)
for off in range(len(b) - 3):
    v = b[off] | b[off + 1] << 8 | b[off + 2] << 16 | b[off + 3] << 24
    if v in rv: hits[rv[v]].append(off + IB)
secs = [(s.VirtualAddress + IB, s.VirtualAddress + IB + s.Misc_VirtualSize, s.Name.rstrip(b"\0").decode()) for s in pe.sections]
sec = lambda a: next((n for lo, hi, n in secs if lo <= a < hi), "?")
aligned_data = {"%08X" % t: ["%08X %s" % (a, sec(a)) for a in v if a % 4 == 0 and sec(a) != ".text"] for t, v in hits.items()}
aligned_data = {k: v for k, v in aligned_data.items() if v}
inside = {}
for t, v in hits.items():
    for a in v:
        if sec(a) != ".text": continue
        k = bisect.bisect_right(S, a) - 1; f = S[k]
        ins = next((i for i in dis(f, F[f]) if i.address <= a < i.address + i.size), None)
        inside["%08X@%08X" % (t, a)] = ("%08X %s %s" % (ins.address, ins.mnemonic, ins.op_str)) if ins else None
unaligned_rdata = sorted("%08X" % a for v in hits.values() for a in v if sec(a) == ".rdata")
ctrl = struct.unpack_from("<I", img, 0x20FAD4 - IB)[0]
res["tails"] = len(tails); res["aligned_data_hits"] = aligned_data; res["text_hits_inside_instructions"] = inside
res["rdata_hits"] = unaligned_rdata
cases["U5_no_route_outside_the_union_names_a_tail_but_the_banned_pdata"] = \
    set(aligned_data) == {"0036F22E"} and all(x.endswith(".pdata") for x in aligned_data["0036F22E"]) and all(inside.values()) \
    and all(int(a, 16) % 4 for a in unaligned_rdata) and ctrl + IB == 0x20F4C2
out = {"evidence": ["STATIC"], "live_game": False, "results": res, "cases": cases, "ok": all(cases.values())}
json.dump(out, open(HERE / "result.json", "w"), indent=1, sort_keys=True)
print(json.dumps(res, indent=1, sort_keys=True))
for k, v in cases.items(): print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
sys.exit(0 if out["ok"] else 1)
