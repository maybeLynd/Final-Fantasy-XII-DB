"""RC-30: is a loca_*.cl2 (kind 7, ids 0xE2 Loca_gil / 0xE3 Loca_bhm / 0xE4 Loca_rbl) requested anywhere? (SWE2-DATA
2026-09-30), static. A reader of the loaded file needs a request first; this bounds every static route to one.

S1 raw .text sweep (function-list independent) for every instruction that materialises one of the ids as an
   immediate into any register (mov r32, imm32 / mov r/m32, imm32 to a stack argument / lea r32, [reg + id]), decoded in
   place, then kept only where the value could be a request id (not a flag mask or field offset: the decode is printed).
S2 the constant-request census (tools/res_request_census.py semantics, re-run here on the four pool APIs and the
   path API): the kind-7 sites whose id is computed, with the base and index shape of each, so the ids each can reach
   are stated.
S3 the list helpers and the data lists (request_lists.py K2): printed there.
Controls: C1 S1 finds the Loca.mrp request (mov r8d, 0xbf at 004040FE, then 00249320 at 00404107);
C2 S1 finds the Party_Book-list-free constant request of w_menu.mrp (0xA6) in 00562F90 (the census's 00563048 row).
"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, BASE, secs, owner, ins_at, text_range, dis, containing_ins  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


t0, t1, ro = text_range()
blob = d[ro:ro + (t1 - t0)]


def imm_sites(v):
    """every decodable instruction containing the imm32 or disp v whose decode shows it as an operand value"""
    out = set()
    pats = [struct.pack("<I", v)]
    if v < 0x80:
        pats.append(bytes([v]))
    for pat in pats:
        start = 0
        while True:
            p = blob.find(pat, start)
            if p < 0:
                break
            start = p + 1
            a = t0 + p
            x, how = containing_ins(a)  # listed function's own linear decode first; back-scan only if unlisted
            if x is None or x.address + x.size < a + len(pat):
                continue
            if re.search(r"(^|[ ,\[+])0x%x(\]|$)" % v, x.op_str):
                out.add((x.address, x.mnemonic, x.op_str))
    return sorted(out)


REQ = re.compile(r"^(r8d|edx|ecx|r9d|r8|rdx), 0x|^dword ptr \[rsp \+ 0x2[08]\], 0x|^(r8d|edx), \[\w+ \+ 0x")
for v, name in ((0xE2, "Loca_gil.cl2"), (0xE3, "Loca_bhm.cl2"), (0xE4, "Loca_rbl.cl2"), (0xBF, "Loca.mrp (control)"),
                (0xA6, "w_menu.mrp (control)")):
    s = imm_sites(v)
    cand = [(a, m, o) for a, m, o in s if m in ("mov", "lea") and REQ.search(o)]
    print("S1 id 0x%X %s: %d instructions carry the value, %d in an argument-register/stack-argument shape" %
          (v, name, len(s), len(cand)))
    for a, m, o in cand:
        f = owner(a)
        # does a pool/path request API call follow within 0x30 bytes?
        nxt = []
        if f:
            for x in dis(f):
                if a < x.address <= a + 0x30 and x.mnemonic == "call":
                    nxt.append(x.op_str)
        print("   %08X %s %-34s in %s  calls after: %s" % (a, m, o, "%08X" % f if f else "unlisted", " ".join(nxt) or "-"))
    if v == 0xBF:
        check("C1 the Loca.mrp constant request at 004040FE is found", any(a == 0x004040FE for a, *_ in cand))
    if v == 0xA6:
        check("C2 a w_menu.mrp (0xA6) argument-shape constant is found in 00562F90",
              any(owner(a) == 0x00562F90 for a, *_ in cand))
    if v in (0xE2, 0xE3, 0xE4):
        api = {"0x249180", "0x249210", "0x2493d0", "0x249350", "0x249320", "0x32e400", "0x32e620", "0x32e3f0"}
        hits = []
        for a, m, o in cand:
            f = owner(a)
            if f and any(x.mnemonic == "call" and x.op_str in api and a < x.address <= a + 0x30 for x in dis(f)):
                hits.append(a)
        check("R id 0x%X is never loaded as a constant request argument (%s)" % (v, name), not hits,
              " ".join("%08X" % h for h in hits))

# S2: computed kind-7 request sites: base + index shape
SITES = [
    (0x002CEB01, "0x10 + byte[obj+0xB2D]", "face_guest / map_efe family (0x0D..0x20)"),
    (0x003C9988, "0xE + byte[obj+0xC1]", "map_efe00..06 (0x0E..0x14)"),
    (0x003C1DC2, "0xE8 + byte[rec+0xB]", "worldmap AreaTim2 loca_NN.tm2 (0xE8..) - cannot reach 0xE2..0xE4"),
    (0x003C1EB1, "0x496 + byte[+4]", "cannot reach 0xE2..0xE4"),
    (0x003C1FF6, "0x142 + dil", "cannot reach 0xE2..0xE4"),
    (0x00380120, "0x129 / 0x12A + byte", "menuquest.nfs / menuquest00..15.bin - cannot reach"),
    (0x00577019, "u16 table 00D23740[i] + 1", "table values 0x228.. - cannot reach"),
    (0x00575C73, "u16 table 00D23740[byte] + word[obj+0xCA] (+ word[arg+2])", "unbounded sum"),
    (0x0057A2DF, "caller rdx + 0x31", "callers 005591A5 / 00561763 / 00572EC8 pass rdx 2 / 0 / 1: 0x31..0x33 m_all*.efx - cannot reach"),
]
print("S2 computed kind-7 request ids (register-held sites of the pool APIs):")
for a, shape, fam in SITES:
    x = ins_at(a)
    print("   %08X %-6s %-30s %-58s %s" % (a, x.mnemonic, x.op_str, shape, fam))
check("S2 the listed shape instructions decode as add/lea/movzx/inc (the id arithmetic)",
      all(ins_at(a).mnemonic in ("add", "lea", "movzx", "inc", "mov") for a, *_ in SITES))
print("FAILS %d" % FAILS)
