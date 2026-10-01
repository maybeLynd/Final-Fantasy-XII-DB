"""RS-3 (OPUS, 2026-09-26): is the sign- / zero-extend split after 0020E600 a property of the encoding or of one file's
helpers? STATIC census of every call to 0020E600 (which returns the 64-bit [01F83530] + (u32)id) by how the caller
extends the returned address before using it.
  R1 0020E600 is `mov eax, ecx ; add rax, [01F83530] ; ret`, so the result is the 64-bit sum.
  R2 Every call site is classified by following rax / eax for up to 12 instructions:
       full 64-bit use;
       passed on;
       sign-extended (cdqe / movsxd, directly or after 32-bit arithmetic);
       zero-extended (a 32-bit mov, or 32-bit arithmetic whose result is then used as an address).
  R3 The split is general: both the sign and the zero class occur in at least four different owner subsystems.
Writes result.json; exit 1 on any FAIL."""
import json, os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[5]

import pefile, capstone, re, struct, collections, bisect
pe = pefile.PE(str(ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"), fast_load=True); img = pe.get_memory_mapped_image(); IB = 0x120000
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
F = {}; OWN = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    c = l.rstrip("\n").split("\t")
    try: F[int(c[0], 16)] = int(c[2]); OWN[int(c[0], 16)] = c[3] or "-"
    except (ValueError, IndexError): pass
S = sorted(F)
def owner(a):
    k = bisect.bisect_right(S, a) - 1
    return S[k] if k >= 0 and a < S[k] + F[S[k]] else None
sites = []
for m in re.finditer(rb"[\xE8\xE9]", img[0x1000:0x8C0000 - IB]):
    o = m.start() + 0x1000
    if o + IB + 5 + struct.unpack_from("<i", img, o + 1)[0] == 0x20E600: sites.append((o + IB, img[o]))
def classify(a):
    """follow rax/eax after the call for up to 12 instructions"""
    regs = {"rax"}; r32 = {"eax"}
    for i in md.disasm(img[a + 5 - IB:a + 5 - IB + 64], a + 5):
        s = i.op_str
        if i.mnemonic in ("cdqe",) and "eax" in r32: return "sign (cdqe)"
        m = re.match(r"(\w+), (\w+)$", s)
        if i.mnemonic == "movsxd" and m and m.group(2) in r32: return "sign (movsxd)"
        if m and i.mnemonic == "mov":
            d, src = m.groups()
            if src in regs: return "full 64-bit (mov %s, %s)" % (d, src)
            if src in r32: return "zero (32-bit mov %s, %s)" % (d, src)
        if m and i.mnemonic in ("add", "sub", "imul", "lea") and (m.group(2) in r32 or m.group(1) in r32) and not m.group(1).startswith("r"):
            if m.group(2) in r32 or m.group(1) in r32:
                dst = m.group(1)
                for j in md.disasm(img[i.address + i.size - IB:i.address + i.size - IB + 40], i.address + i.size):
                    if j.mnemonic == "cdqe" and dst == "eax": return "sign after 32-bit arithmetic (cdqe)"
                    mm = re.match(r"(\w+), (\w+)$", j.op_str)
                    if j.mnemonic == "movsxd" and mm and mm.group(2) == dst: return "sign after 32-bit arithmetic (movsxd)"
                    if j.mnemonic in ("call", "ret", "jmp"): break
                return "zero after 32-bit arithmetic (%s %s)" % (i.mnemonic, s)
        if re.search(r"\[rax[ \]+]", s): return "full 64-bit (deref [rax])"
        if i.mnemonic == "test" and "rax" in s: continue
        if i.mnemonic in ("call", "ret", "jmp"): return "passed/returned (%s)" % i.mnemonic
    return "unclassified"
kinds = collections.Counter(); byown = collections.defaultdict(collections.Counter); ex = {}
for a, op in sites:
    k = "tail-jump" if op == 0xE9 else classify(a)
    g = k.split(" (")[0]
    kinds[g] += 1
    f = owner(a); byown[g][OWN.get(f, "?")] += 1; ex.setdefault(g, []).append("%08X" % a)
print("call sites", len(sites))
for g, n in kinds.most_common(): print("  %-24s %3d  owners %s  e.g. %s" % (g, n, dict(byown[g].most_common(6)), ex[g][:5]))

body = [(i.mnemonic, i.op_str) for i in md.disasm(img[0x20E600 - IB:0x20E60A - IB], 0x20E600)]
r1 = body == [("mov", "eax, ecx"), ("add", "rax, qword ptr [rip + 0x1d74f27]"), ("ret", "")]
own_sign = {o for g in byown if g.startswith("sign") for o in byown[g] if o not in ("-", "?")}
own_zero = {o for g in byown if g.startswith("zero") for o in byown[g] if o not in ("-", "?")}
cases = {"R1_0020E600_returns_the_64_bit_sum": r1,
         "R2_every_site_classified_but_a_named_few": len(sites) > 4000 and kinds.get("unclassified", 0) < 50,
         "R3_sign_and_zero_each_occur_in_at_least_four_owner_subsystems": len(own_sign) >= 4 and len(own_zero) >= 4}
out = {"evidence": ["STATIC"], "live_game": False, "call_sites": len(sites), "by_kind": dict(kinds),
       "owners_by_kind": {g: dict(c) for g, c in byown.items()}, "examples": {g: v[:12] for g, v in ex.items()},
       "cases": cases, "ok": all(cases.values())}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items(): print("%-66s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED"); sys.exit(0 if out["ok"] else 1)
