"""S-37: execute CONTRACT-text-control-codes-and-dyngeo-draw.md's entries as shipped code - the control-code interpreter
002AC5F0 over every lead byte and every escape selector, the eleven escape parsers, and the DynGeo shared draw 002142A0 -
and test I-1, I-2, I-3, I-6, I-7 and section 3's DynGeo layout (OPUS, 2026-09-25, block 313).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NO application stub. ALLOWED = the
static closures of the entries; entering anything else fails a case. IMPORTS: the import directory is parsed from the image,
EVERY IAT slot points at a unique trap, and only memcpy / memmove are bridged by name; any other import fails the case by
name (reported, not hidden).
ONE FIXTURE CALLBACK: the DynGeo draw's render target (its rdx) is a planted object whose vtable slots 0 / 1 / 4 / 8 point at
recording callbacks (slot 0 returns a buffer, slot 1 returns a token, slots 4 and 8 record their arguments). This is an
in-scope callback fixture standing in for the device-side target, which has no statically constructible instance.
Fixtures (planted data only): the text context (rcx), the painter singleton [0209CC40], the parsers' lookup base
[02AEE870], the sink singleton [01F811F8] (0017FAE0 stores its argument at +0x28), the DynGeo instance's ten layers.
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP,
                               UC_X86_REG_RAX)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, WORLD, BRIDGE, CB = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000, 0x75000000
TCTX, PAINTER, TEXT, OUTF, OUTI, DYN, TARGET, TVT, VBUF, LUT = (WORLD, WORLD + 0x1000, WORLD + 0x3000, WORLD + 0x3100,
                                                             WORLD + 0x3108, WORLD + 0x4000, WORLD + 0x5000, WORLD + 0x5100,
                                                             WORLD + 0x10000, WORLD + 0x8000)
INTERP = 0x2AC5F0
G_SINK, SINK = 0x1F811F8, WORLD + 0x6000           # 0017FAE0(x) stores x at [01F811F8]+0x28
G_PAINTER, G_ADV_A, G_ADV_B, G_LUT = 0x209CC40, 0x209CC60, 0x209CC68, 0x2AEE870
PARSERS = [0x3FFAB0, 0x3FFB00, 0x3FFB90, 0x3FFBC0, 0x3FFC60, 0x3FFCE0, 0x3FFD70, 0x3FFDA0, 0x3FFDF0, 0x3FFEE0, 0x3FFF10]
DYN_DRAW = 0x2142A0
BRIDGED = {"memcpy", "memmove"}

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
graph = collections.defaultdict(set)
for r in csv.DictReader(open(GRAPH + r"\edges.tsv", encoding="utf-8"), delimiter="\t"):
    if r["callee_external"] != "true":
        graph[int(r["caller"], 16)].add(int(r["callee"], 16))


def closure(s):
    seen, st = set(), [s]
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        st.extend(graph[x])
    return seen


ALLOWED = set()
for e in [INTERP, DYN_DRAW] + PARSERS:
    ALLOWED |= closure(e)
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40


def import_slots():
    def r2o(rva):
        for v, vs, ra, rs in secs:
            if v - IMG <= rva < v - IMG + max(vs, rs):
                return ra + rva - (v - IMG)
    imp_rva = struct.unpack_from("<I", raw, pe + 24 + 112 + 8)[0]
    out, dd = [], r2o(imp_rva)
    while True:
        oft, ts, fc, name, ft = struct.unpack_from("<IIIII", raw, dd)
        if not (oft or name or ft):
            return out
        th, i = r2o(oft or ft), 0
        while True:
            e = struct.unpack_from("<Q", raw, th + 8 * i)[0]
            if e == 0:
                break
            nm = "ord%d" % (e & 0xFFFF) if e >> 63 else raw[r2o(e) + 2:raw.index(b"\x00", r2o(e) + 2)].decode()
            out.append((IMG + ft + 8 * i, nm))
            i += 1
        dd += 20


uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x40000)
uc.mem_map(BRIDGE, 0x2000)
uc.mem_map(CB, 0x1000)
uc.mem_write(RET, bytes([0xF4]))
uc.mem_write(BRIDGE, bytes([0xC3]) * 0x2000)
uc.mem_write(CB, bytes([0xC3]) * 0x1000)
BR = {}
for i, (slot, name) in enumerate(import_slots()):
    uc.mem_write(slot, struct.pack("<Q", BRIDGE + 4 * i))
    BR[BRIDGE + 4 * i] = name
CBS = {CB + 0x00: "slot0_map", CB + 0x10: "slot1_unmap", CB + 0x20: "slot4_draw", CB + 0x30: "slot8_bind"}
state = {"bad": [], "faults": [], "entered": set(), "cb": [], "copies": []}


def on_code(u, a, n, _):
    if a in BR:
        nm = BR[a]
        if nm not in BRIDGED:
            state["bad"].append("import " + nm)
            u.emu_stop()
            return
        d, s, c = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        u.mem_write(d, bytes(u.mem_read(s, c)) if c else b"")
        state["copies"].append([d, s, c])
        u.reg_write(UC_X86_REG_RAX, d)
        return
    if a in CBS:
        nm = CBS[a]
        rec = {"cb": nm, "rdx": u.reg_read(UC_X86_REG_RDX), "r8": u.reg_read(UC_X86_REG_R8), "r9": u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF}
        state["cb"].append(rec)
        if nm == "slot0_map":
            u.reg_write(UC_X86_REG_RAX, VBUF)
        elif nm == "slot1_unmap":
            u.reg_write(UC_X86_REG_RAX, 0x1234)
        return
    if a in FSTARTS:
        state["entered"].add(a)
        if a not in ALLOWED:
            state["bad"].append("%08X" % a)
            u.emu_stop()


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


def call(entry, rcx=0, rdx=0, r8=0, r9=0):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
        uc.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
    state.update(bad=[], faults=[], entered=set(), cb=[], copies=[])
    try:
        uc.emu_start(entry, RET, count=3000000)
    except UcError as e:
        state["faults"].append(str(e))
    return uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]


def q(a):
    return struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]


def world():
    uc.mem_write(WORLD, bytes(0x40000))
    uc.mem_write(G_PAINTER, struct.pack("<Q", PAINTER))
    uc.mem_write(G_LUT, struct.pack("<Q", LUT))
    uc.mem_write(G_SINK, struct.pack("<Q", SINK))


def interp(text):
    """one interpreter call on `text`; returns (ok, eax, cursor advance, out2)"""
    uc.mem_write(TEXT, bytes(0x100))
    uc.mem_write(TEXT, text)
    uc.mem_write(OUTF, struct.pack("<Q", TEXT))            # the cursor, passed by reference
    uc.mem_write(OUTI, struct.pack("<I", 0x55555555))
    uc.mem_write(G_ADV_A, struct.pack("<QQ", 0xDEADBEEF, 0xDEADBEEF))
    ok = call(INTERP, TCTX, OUTF, WORLD + 0x3200, OUTI)
    eax = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    adv = q(OUTF) - TEXT
    return ok, eax, adv, struct.unpack("<I", bytes(uc.mem_read(OUTI, 4)))[0], (q(G_ADV_A), q(G_ADV_B))


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-36s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# A. ordinary bytes >= 0x10 and 0x0B..0x0D: return 0, cursor untouched; every entry zeroes the advance pair and *out2
world()
bad = []
for b in list(range(0x10, 0x100)) + [0x0B, 0x0C, 0x0D]:
    ok, eax, adv, o2, advp = interp(bytes([b, 0x41, 0]))
    if not (ok and eax == 0 and adv == 0 and o2 == 0 and advp == (0, 0)):
        bad.append(["%02X" % b, ok, eax, adv, hex(o2), [hex(x) for x in advp], state["faults"][:1], state["bad"][:1]])
record("A_ordinary_bytes_I1_I7", not bad, n=243, failing=bad[:10],
       note="243 lead bytes: return 0, cursor not advanced, *out2 = 0 and [0209CC60]/[0209CC68] zeroed on entry")

# B. the end of the run: a zero byte, and the painter's terminator word at +0x10C8
world()
ok0, eax0, adv0, _, _ = interp(b"\x00")
uc.mem_write(PAINTER + 0x10C8, struct.pack("<Q", WORLD + 0x3F00))
uc.mem_write(WORLD + 0x3F00, b"\x41\x42")
okt, eaxt, advt, _, _ = interp(b"\x41\x42\x43")
uc.mem_write(PAINTER + 0x10C8, struct.pack("<Q", 0))
record("B_end_of_run", ok0 and eax0 == 0 and okt and eaxt == 0, zero_byte=[ok0, eax0, adv0], terminator_word=[okt, eaxt, advt],
       note="a zero byte and a match of the painter's +0x10C8 terminator word both stop with 0")

# C. every lead token 0x01..0x0F, observed (return, advance, functions entered, import or fault if any)
tokens = {}
for t in range(1, 0x10):
    world()
    ok, eax, adv, o2, _ = interp(bytes([t, 0x21, 0x22, 0x23, 0x24, 0]))
    tokens["%02X" % t] = {"ok": ok, "ret": eax, "advance": adv, "entered": len(state["entered"]),
                          "stopped_at": (state["bad"] or state["faults"])[:1]}
i1 = all(v["ret"] in (0, 1) for v in tokens.values() if v["ok"])
record("C_lead_tokens_observed", i1 and tokens["08"]["ok"] and tokens["08"]["ret"] == 1 and tokens["08"]["advance"] == 3
       and tokens["09"]["ret"] == 1 and tokens["09"]["advance"] == 1, tokens=tokens,
       note="observed per token; asserted: every completed call returns 0 or 1 (I-1), 0x08 skips 3, 0x09 skips 1")

# D. the escape 0x0F: every selector byte
sel = {}
for s in range(0x100):
    world()
    ok, eax, adv, o2, _ = interp(bytes([0x0F, s, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0]))
    sel[s] = {"ok": ok, "ret": eax, "advance": adv, "stopped_at": (state["bad"] or state["faults"])[:1]}
outside = [s for s in range(0x100) if not (0x20 <= s <= 0x70)]
i6 = all(sel[s]["ok"] and sel[s]["ret"] == 1 and sel[s]["advance"] == 1 for s in outside if s != 0)
i3 = all(sel[s]["ok"] and sel[s]["ret"] == 1 and sel[s]["advance"] == 1 for s in (0x30, 0x5F))
# the consequence: after an unrecognised selector the NEXT call reads the selector byte as an ordinary character
world()
ok1, e1, a1, _, _ = interp(b"\x0F\x7Fz\x00")
uc.mem_write(OUTF, struct.pack("<Q", TEXT + a1))
okn = call(INTERP, TCTX, OUTF, WORLD + 0x3200, OUTI)
e2 = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
a2 = q(OUTF) - TEXT
record("D_escape_selectors_I3_I6", i6 and i3 and ok1 and e1 == 1 and a1 == 1 and okn and e2 == 0 and a2 == 1,
       outside_range_ok=i6, zero_and_underscore_do_nothing=i3, next_call_after_7F=[e2, a2],
       in_range_observed={"%02X" % s: sel[s] for s in range(0x20, 0x71)},
       note="outside 0x20..0x70 (and '0', '_'): return 1 having consumed ONLY the 0x0F byte; the next call returns 0 at the "
            "selector byte - an unrecognised selector is left in the stream as an ordinary character")

# E. the eleven parsers (I-2): the length each returns, over several payloads
parse = {}
payloads = [bytes([0x41, 0x01, 0x05, 0x00, 0x09, 0x02, 0x00, 0x00]), bytes([0x41, 0xC7, 0x85, 0x10, 0x30, 0x31, 0x32, 0x00]),
            bytes([0x5A, 0x3F, 0x7F, 0x7F, 0x00, 0x00, 0x00, 0x00]), bytes([0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])]
for p in PARSERS:
    rets = []
    for pl in payloads:
        world()
        uc.mem_write(TEXT, bytes(0x100))
        uc.mem_write(TEXT, pl + b"\x0f\x0f\x0f\x0f")
        ok = call(p, TEXT, WORLD + 0x3200, WORLD + 0x3210, WORLD + 0x3220)
        rets.append([ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, (state["bad"] or state["faults"])[:1]])
    parse["%08X" % p] = rets
const3 = all(all(r[0] and r[1] == 3 for r in parse["%08X" % p]) for p in (0x3FFAB0, 0x3FFB90, 0x3FFC60, 0x3FFDA0, 0x3FFEE0))
const4 = all(all(r[0] and r[1] == 4 for r in parse["%08X" % p]) for p in (0x3FFCE0, 0x3FFF10))
selfd = [r[1] for r in parse["003FFD70"]] == [(pl[2] & 0x7F) + 3 for pl in payloads]
record("E_parsers_I2", const3 and const4 and selfd, returns=parse,
       note="five return 3 on every payload, two return 4, 003FFD70 returns (byte 2 & 0x7F) + 3; the others are reported")

# F. the DynGeo shared draw: ten layers, a null source skips the layer, batches of at most 480 vertices of 48 bytes
world()
uc.mem_write(TARGET, struct.pack("<Q", TVT))
slots = {0: CB + 0x00, 1: CB + 0x10, 4: CB + 0x20, 8: CB + 0x30}
for k, v in slots.items():
    uc.mem_write(TVT + 8 * k, struct.pack("<Q", v))
layers = {0: (1000, True), 1: (0, True), 2: (300, False), 3: (480, True), 9: (481, True)}
VERT = WORLD + 0x20000
for i, (cnt, src) in layers.items():
    uc.mem_write(DYN + 0x08 + 8 * i, struct.pack("<Q", 0x5000 + i if src else 0))
    uc.mem_write(DYN + 0x58 + 8 * i, struct.pack("<Q", VERT + 0x1000 * i))
    uc.mem_write(DYN + 0xA8 + 4 * i, struct.pack("<I", cnt))
okd = call(DYN_DRAW, DYN, TARGET)
binds = [c["rdx"] for c in state["cb"] if c["cb"] == "slot8_bind"]
draws = [(c["rdx"], c["r9"]) for c in state["cb"] if c["cb"] == "slot4_draw"]
maps = [c["rdx"] & 0xFFFFFFFF for c in state["cb"] if c["cb"] == "slot0_map"]
copies = [(s - VERT, c) for d, s, c in state["copies"]]
want_binds = [0x5000 + i for i in sorted(layers) if layers[i][1]]
want_maps = [480, 480, 40, 480, 480, 1]
want_copies = [(0, 480 * 48), (480 * 48, 480 * 48), (960 * 48, 40 * 48), (0x3000, 480 * 48), (0x9000, 480 * 48), (0x9000 + 480 * 48, 48)]
f_ok = okd and binds == want_binds and maps == want_maps and copies == want_copies and all(d[0] == 2 for d in draws) \
    and [d[1] for d in draws] == want_maps
record("F_dyngeo_draw_layout", f_ok, binds=[hex(x) for x in binds], map_counts=maps, copies=copies, draws=draws,
       note="layers with a source bind once; 1000 -> 480+480+40; 481 -> 480+1; the copy is count x 48 bytes from base + done x 48; "
            "draw(2, n); a layer with a null source is skipped even with a count; a zero count binds and draws nothing")

json.dump({"pass": sum(1 for v in results.values() if v["pass_"]), "total": len(results), "ok": allok, "allowed_functions": len(ALLOWED),
           "results": results}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("%d/%d pass (allowed %d functions)" % (sum(1 for v in results.values() if v["pass_"]), len(results), len(ALLOWED)))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
