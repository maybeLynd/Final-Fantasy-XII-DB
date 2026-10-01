"""UQ-46: the bracketed startup-object sizes, by running each builder whole (OPUS, 2026-09-27). Control. Static + emulation.

The census in 00-Engine-Core-Runtime/Startup-Data-Construction/members (builder_store_census.py) decodes the two hubs'
`call` instructions and takes each builder's own stores. Two things it cannot see decide five of its six open objects:
  E1 REGRESSION against '66 pairs': each hub ENDS with `lea rcx, [obj]; jmp builder` - 0037E0D8/0037E0E3 (02AE1EF0,
     004A8860) and 0037E334/0037E33F (02AEAFC0, 004C3610) - so the hubs hand out 28 + 49 = 77 (object, builder) pairs,
     68 of them to builders in 00480000-004FFFFF, not 66
  E2 every builder run whole in Unicorn (callees and tail jumps followed, the memset import bridged, rcx = the object):
     with all 77 objects placed, 71 of the 76 that have a next object are written exactly to it, none past it; the
     five short ones are 02AE06B0, 02AE3330, 02AE4F20, 02AE9290 and 02AE9EE0. POSITIVE CONTROL: for every object the
     census lists, the run's extent is >= the census's store extent
  E3 02AEC660 is exact (0x200): its builder 004E7980 tail-jumps to 004E7A90 with rcx = obj + 0x10 (004E7998, 004E79AF);
     the census's 0x10 stops at the jump
  E4 02AE1DA0 is exact (0x150): the next object is 02AE1EF0, the first hub's missed tail pair
  E5 02AE06B0 is 0x1A0: references split at the extent - 004574B0 uses +0x8..+0x170, 0044D4A0 starts at +0x1A0 and hands
     02AE0850 to 003A3010 with size 0x150 (0044D7ED / 0044D7F2); 0x1A0 + 0x150 is the gap 0x2F0
  E6 02AE4F20 is 0xC70: 0045BFB0 uses +0x8..+0x360, 00453150 starts at +0xC70 and takes it as its own base (lea r12 at
     004535F3); what lies at +0xC70 is 0xDC0 to the gap, the size of the three 0xDC0 objects - noted, not claimed
  E7 02AE9EE0 is 0x150 by its own DMA tag: 008631D0 writes qwc at +0 and id byte 0x10 (cnt); qwc 20 declares 0x150,
     the written extent; nothing references +0x150..+0x1EF, and 003B6020 reads +0x1F0 as a separate table
  E8 02AED330 (the last object) is bracketed [0x130, 0x160]: extent 0x130, the first referenced address past it is the
     qword at +0x160, and nothing references +0x130..+0x15F
Not claimed: what 02AE9EE0's +0x150..+0x1EF and 02AED330's +0x130..+0x15F hold; data reached only through pointers
(a RIP-relative / absolute reference census cannot see those); builders' untaken branches (the run follows one path,
which is why E2 compares against the all-paths census and only ever finds it >=).
"""
import struct, sys, bisect, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_MEM_WRITE, UC_HOOK_CODE, UC_PROT_ALL
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RAX, UC_X86_REG_RIP

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def D(f): return list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
def I(f): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(f)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

def pairs(h):
    out = []; rcx = None
    for x in D(h):
        if x.mnemonic == "lea" and x.op_str.startswith("rcx,") and x.operands[1].mem.base == X86_REG_RIP:
            rcx = x.address + x.size + x.operands[1].mem.disp
        elif x.mnemonic in ("call", "jmp") and x.operands[0].type == X86_OP_IMM:
            out.append((h, rcx, x.operands[0].imm, x.mnemonic, x.address)); rcx = None
    return out
P = pairs(0x37DF90) + pairs(0x37E0F0)
tails = [(o, b, a) for h, o, b, m, a in P if m == "jmp"]
inband = [p for p in P if 0x480000 <= p[2] < 0x500000]
check("E1 each hub ends in lea rcx + jmp builder: 77 pairs (28 + 49), 68 in band, not 66",
      tails == [(0x2AE1EF0, 0x4A8860, 0x37E0E3), (0x2AEAFC0, 0x4C3610, 0x37E33F)] and len(P) == 77
      and sum(1 for p in P if p[0] == 0x37DF90) == 28 and len(inband) == 68 and len({p[1] for p in P}) == 77,
      "pairs %d, in band %d, tails %s" % (len(P), len(inband), [("%08X" % o, "%08X" % b) for o, b, a in tails]))

img = max(va + vs for ch, vs, va, rs, ro in SECS)
def run(builder, obj, span):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(BASE, (img + 0xFFFF) & ~0xFFFF, UC_PROT_ALL); mu.mem_write(BASE, d[:0x1000])
    for ch, vs, va, rs, ro in SECS: mu.mem_write(BASE + va, d[ro:ro + min(rs, vs)])
    STK = 0x7FF00000; mu.mem_map(STK, 0x100000, UC_PROT_ALL)
    RET = 0x7FE00000; mu.mem_map(RET, 0x1000, UC_PROT_ALL); mu.mem_write(RET, b"\xF4")
    rsp = STK + 0x80000; mu.mem_write(rsp, struct.pack("<Q", RET))
    mu.reg_write(UC_X86_REG_RSP, rsp); mu.reg_write(UC_X86_REG_RCX, obj)
    w = set()
    def hw(uc, access, addr, sz, val, ud):
        for k in range(sz):
            if obj <= addr + k < obj + span: w.add(addr + k - obj)
    def memset(uc, addr, size, ud):          # 00861EC0 = jmp [IAT memset]
        dst, v, cnt = uc.reg_read(UC_X86_REG_RCX), uc.reg_read(UC_X86_REG_RDX) & 0xFF, uc.reg_read(UC_X86_REG_R8)
        uc.mem_write(dst, bytes([v]) * cnt); w.update(a - obj for a in range(dst, dst + cnt) if obj <= a < obj + span)
        uc.reg_write(UC_X86_REG_RAX, dst); sp = uc.reg_read(UC_X86_REG_RSP)
        uc.reg_write(UC_X86_REG_RIP, struct.unpack("<Q", bytes(uc.mem_read(sp, 8)))[0]); uc.reg_write(UC_X86_REG_RSP, sp + 8)
    mu.hook_add(UC_HOOK_MEM_WRITE, hw); mu.hook_add(UC_HOOK_CODE, memset, begin=0x861EC0, end=0x861EC0)
    err = None
    try: mu.emu_start(builder, RET, count=2_000_000)
    except Exception as e: err = "%s at %08X" % (e, mu.reg_read(UC_X86_REG_RIP))
    return (max(w) + 1 if w else 0), bytes(mu.mem_read(obj, 16)), err
objs = sorted(p[1] for p in P)
gap = {o: (objs[i + 1] - o if i + 1 < len(objs) else None) for i, o in enumerate(objs)}
R = {}
for h, o, b, m, a in P: R[o] = (b,) + run(b, o, gap[o] or 0x1000)
census = {}
for l in open(DB / "00-Engine-Core-Runtime/Startup-Data-Construction/members/builder-store-extents.tsv", encoding="utf-8"):
    c = l.rstrip("\n").split("\t")
    if c[0] != "hub": census[int(c[1], 16)] = int(c[7], 16)
withgap = [o for o in objs if gap[o]]
exact = [o for o in withgap if R[o][1] == gap[o]]; short = sorted(o for o in withgap if R[o][1] < gap[o]); over = [o for o in withgap if R[o][1] > gap[o]]
errs = [o for o in objs if R[o][3]]
ge = [o for o in census if o in R and R[o][1] < census[o]]
check("E2 every builder run whole: 71 of 76 exact, none past its next object; short: 02AE06B0 02AE3330 02AE4F20 02AE9290"
      " 02AE9EE0; POSITIVE CONTROL the run is never below the census's store extent",
      len(withgap) == 76 and len(exact) == 71 and not over and not errs and short == [0x2AE06B0, 0x2AE3330, 0x2AE4F20, 0x2AE9290, 0x2AE9EE0]
      and len(census) == 75 and not ge,
      "exact %d, short %s, over %d, errors %d, below-census %s" % (len(exact), ["%08X" % o for o in short], len(over), len(errs), ["%08X" % o for o in ge]))

B7 = I(0x4E7980)
check("E3 02AEC660 exact 0x200: 004E7980 tail-jumps to 004E7A90 with rcx = obj + 0x10; the census stops at 0x10",
      B7.get(0x4E7998) == "lea rcx, [rbx + 0x10]" and B7.get(0x4E79AF) == "jmp 0x4e7a90" and R[0x2AEC660][1] == 0x200 == gap[0x2AEC660]
      and census.get(0x2AEC660) == 0x10)
check("E4 02AE1DA0 exact 0x150: its next object is 02AE1EF0, the first hub's tail pair",
      R[0x2AE1DA0][1] == 0x150 == gap[0x2AE1DA0] and 0x2AE1DA0 + 0x150 == 0x2AE1EF0 and census.get(0x2AE1DA0) == 0x150)

# the RIP-relative / absolute reference census over .text, per object window
WIN = {0x2AE06B0: 0x2F0, 0x2AE4F20: 0x1A30, 0x2AE9EE0: 0x390, 0x2AED330: 0x400}
lo, hi = min(WIN), max(o + g for o, g in WIN.items())
refs = collections.defaultdict(lambda: collections.defaultdict(set))
for ch, vs, va, rs, ro in SECS:
    if not ch & 0x20000000: continue
    for f in keys:
        if not (BASE + va <= f < BASE + va + min(vs, rs)): continue
        for x in cs.disasm(d[off(f):off(f) + sizes[f]], f):
            for op in x.operands:
                t = x.address + x.size + op.mem.disp if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP else (op.imm if op.type == X86_OP_IMM else None)
                if t is not None and lo <= t < hi:
                    for o, g in WIN.items():
                        if o <= t < o + g: refs[o][f].add(t - o)
def span(o, f): s = refs[o].get(f, set()); return (min(s), max(s)) if s else None
L4 = I(0x44D4A0)
check("E5 02AE06B0 is 0x1A0: 004574B0 stays in +0x8..+0x170, 0044D4A0 starts at +0x1A0 and passes 02AE0850 with size 0x150"
      " to 003A3010; 0x1A0 + 0x150 = 0x2F0",
      R[0x2AE06B0][1] == 0x1A0 and span(0x2AE06B0, 0x4574B0) == (0x8, 0x170) and span(0x2AE06B0, 0x44D4A0)[0] == 0x1A0
      and set(refs[0x2AE06B0]) == {0x37DF90, 0x4574B0, 0x44D4A0}
      and L4.get(0x44D7ED) == "mov edx, 0x150" and L4.get(0x44D7F2) == "lea rcx, [rip + 0x2693057]" and L4.get(0x44D7F9) == "call 0x3a3010"
      and 0x44D7F9 + 0x2693057 == 0x2AE0850 and 0x1A0 + 0x150 == gap[0x2AE06B0],
      str({"%08X" % f: tuple(hex(v) for v in span(0x2AE06B0, f)) for f in refs[0x2AE06B0]}))
L5 = I(0x453150)
check("E6 02AE4F20 is 0xC70: 0045BFB0 stays in +0x8..+0x360, 00453150 starts at +0xC70 and takes it as a base (lea r12)",
      R[0x2AE4F20][1] == 0xC70 and span(0x2AE4F20, 0x45BFB0) == (0x8, 0x360) and span(0x2AE4F20, 0x453150)[0] == 0xC70
      and set(refs[0x2AE4F20]) == {0x37DF90, 0x45BFB0, 0x453150}
      and L5.get(0x4535F3) == "lea r12, [rip + 0x2692596]" and 0x4535FA + 0x2692596 == 0x2AE4F20 + 0xC70,
      "tail to the gap 0x%X" % (gap[0x2AE4F20] - 0xC70))
H = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x8631D0):off(0x8631D0) + 15], 0x8631D0)}
qwc, tid = struct.unpack_from("<H", R[0x2AE9EE0][2], 0)[0], R[0x2AE9EE0][2][3]
inside = sorted(k for f, s in refs[0x2AE9EE0].items() for k in s)
check("E7 02AE9EE0 is 0x150 by its own DMA tag: 008631D0 writes qwc at +0 and id 0x10 (cnt); qwc 20 -> 0x150 = the"
      " extent; nothing references +0x150..+0x1EF; 003B6020 reads +0x1F0",
      H.get(0x8631D0) == "mov word ptr [rcx], dx" and H.get(0x8631D3) == "mov byte ptr [rcx + 3], 0x10"
      and tid == 0x10 and 16 * (qwc + 1) == 0x150 == R[0x2AE9EE0][1]
      and not [k for k in inside if 0x150 <= k < 0x1F0] and span(0x2AE9EE0, 0x3B6020) == (0x1F0, 0x1F0),
      "qwc %d id 0x%02X; referenced offsets %s" % (qwc, tid, sorted(set(hex(k) for k in inside))))
past = sorted(k for f, s in refs[0x2AED330].items() for k in s if k >= 0x130)
check("E8 02AED330 bracketed [0x130, 0x160]: extent 0x130, first referenced address past it +0x160, none in between",
      R[0x2AED330][1] == 0x130 and gap[0x2AED330] is None and past[0] == 0x160,
      "%d functions reference +0x160" % sum(1 for f, s in refs[0x2AED330].items() if 0x160 in s))
print("FAILS", fails)
sys.exit(1 if fails else 0)
