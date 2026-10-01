"""uq215_routes.py - UQ-215: no loaded-data VIF command stream reaches the UNPACK decoder (FABLE, Claude Opus 5.5, 2026-09-27).
Static read of the authorised exe; section-aware addressing.

  R1 the VIF1 interpreter 001DB550 is reachable only as GiVmax vtable slot 0: 009007E8 is the only qword in .rdata/.data
     holding 001DB550, and the GiVmax ctor 001DB220 is the only instruction that materialises 009007E8.
  R2 chunks enter a GiVmax command only through 001DB340, called only by the builder 001DB840 and the thunk 001DB7D0
     (jmp), which the effect finalisers' 001DB7E0 command uses.
  R3 every payload handed to the four VU1 registrars (003A34D0, 003A35E0, 003A2F70, 003A33B0) is an exe .data template
     (rip-relative into 02ADE000..02AEE000), a stack buffer, or the type-0x67 record block; no payload pointer is a
     resolved resource. Counted per class.
  R3c sensitivity: the same classifier, on type 0x97's call 0045BE73, does not class the resolved resource pointer (r8)
     as a template and does class the exe template 02AE3460 (rcx) as one.
  R4 type 0x67's record block is initialised from the exe template 02AEC860 (0045FD50 loop at 0046003A), whose builder
     004E79C0 writes STCYCL 0x01000404 and UNPACK 0x6C22001E (V4_32, NUM 34); the walk's 0x200-byte copy lands inside
     that payload; its work buffer (elem+0x338) is filled by 00532EF0 (memset + 003D8E50), not from data.
  R5 where resource bytes do enter an effect packet, the finaliser builders write the UNPACK header themselves:
     0054C10E and 0054D9EE 'or ecx, 0x6c000064' (V4_32) right before the payload memcpy; 005466E0 'or eax, 0x6c00'.
  R6 the one data-borne VIF stream, effect type 0x97's resource payload (0045BE30..0045BEE0), is appended through
     003A2E30 / 003A31A0, the raw-packet path the PC drain 003A3740 never submits (UQ-204 record); control: both calls.
Exit 1 on any FAIL.
"""
import re, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
_pe = struct.unpack_from("<I", d, 0x3C)[0]; _n = struct.unpack_from("<H", d, _pe + 6)[0]; _opt = struct.unpack_from("<H", d, _pe + 20)[0]
SECS = []
for i in range(_n):
    b = _pe + 24 + _opt + i * 40
    SECS.append((d[b:b + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, b + 8))
def off(v):
    for _, vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
SIZES = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = l.rstrip("\n").split("\t")
    try: SIZES["%08X" % int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
BODY = {}
def body(f):
    if f not in BODY:
        a = int(f, 16); o = off(a)
        BODY[f] = [] if o is None or SIZES.get(f, 0) <= 0 else list(cs.disasm(d[o:o + SIZES[f]], a))
    return BODY[f]
def txt(x): return "%s %s" % (x.mnemonic, x.op_str)
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

holders = []
for nm, vs, va, rs, ro in SECS:
    if nm in (".rdata", ".data"):
        blob = d[ro:ro + rs]; i = blob.find(struct.pack("<Q", 0x001DB550))
        while i >= 0:
            holders.append(0x120000 + va + i); i = blob.find(struct.pack("<Q", 0x001DB550), i + 1)
leas, calls340, callsreg = [], collections.defaultdict(list), collections.defaultdict(list)
REG = {"003A34D0", "003A35E0", "003A2F70", "003A33B0"}
for f in SIZES:
    fa = int(f, 16)
    if not 0x121000 <= fa < 0x8C0000: continue
    for x in body(f):
        if x.mnemonic == "lea" and rip(x) == 0x009007E8: leas.append(f)
        if (x.mnemonic == "call" or x.mnemonic.startswith("j")) and x.op_str.startswith("0x"):
            t = "%08X" % int(x.op_str.split()[0], 16)
            if t == "001DB340" and f != t: calls340[f].append(x.address)
            if t in REG and f not in REG: callsreg[t].append((f, x.address))
check("R1 001DB550 held only by vtable 009007E8, materialised only by the GiVmax ctor 001DB220",
      holders == [0x009007E8] and leas == ["001DB220"], "holders=%s leas=%s" % ([hex(h) for h in holders], leas))
check("R2 001DB340's callers are 001DB840 and the thunk 001DB7D0", sorted(calls340) == ["001DB7D0", "001DB840"], str(sorted(calls340)))

def payload(fb, k, reg):
    """classify the payload register/slot at call index k: template / stack / other"""
    for j in range(k - 1, max(-1, k - 400), -1):
        x = fb[j]; o = x.op_str
        if x.mnemonic == "call": break
        dst = o.split(",")[0].strip()
        if dst != reg: continue
        if x.mnemonic == "lea":
            t = rip(x)
            if t is not None: return "template" if 0x02ADE000 <= t < 0x02AEE000 else "rip:%08X" % t
            if "rsp" in o or "rbp" in o: return "stack"
            m = re.match(r"\w+, \[(\w+)", o)
            return "lea-off:" + (m.group(1) if m else "?")
        if x.mnemonic == "mov":
            src = o.split(",", 1)[1].strip()
            if re.fullmatch(r"r\w+", src): return payload(fb, j, src)
            return "load:" + src
    return "entry"
cls = collections.Counter(); odd = []
for t, sites in callsreg.items():
    for f, a in sites:
        fb = body(f); k = next(i for i, x in enumerate(fb) if x.address == a)
        # 003A34D0 and 003A33B0 take the payload at [rsp+0x20]; 003A35E0 and 003A2F70 in r9
        if t in ("003A35E0", "003A2F70"):
            c = payload(fb, k, "r9")
        else:
            c = "?"
            for j in range(k - 1, max(-1, k - 40), -1):
                m = re.fullmatch(r"qword ptr \[rsp \+ (?:0x20|32)\], (r\w+)", fb[j].op_str)
                if fb[j].mnemonic == "mov" and m: c = payload(fb, j, m.group(1)); break
        if c.startswith("lea-off") and f == "00460170": c = "type-0x67 block"
        cls[c] += 1
        if c not in ("template", "stack", "type-0x67 block"): odd.append((t, f, hex(a), c))
check("R3 registrar payloads: templates, stack buffers and the type-0x67 block only", not odd and cls["template"] >= 90,
      "%s odd=%s" % (dict(cls), odd))

fb97 = body("0045BAE0"); k97 = next(i for i, x in enumerate(fb97) if x.address == 0x0045BE73)
c_res, c_tpl = payload(fb97, k97, "r8"), payload(fb97, k97, "rcx")
check("R3c sensitivity: at 0045BE73 the resolved resource pointer (r8) is not classed a template, the exe template (rcx) is",
      c_res not in ("template", "stack") and c_tpl == "template", "r8=%s rcx=%s" % (c_res, c_tpl))
tb = {x.address: txt(x) for x in body("004E79C0")}
lp = [x for x in body("0045FD50") if x.address == 0x0046003A]
check("R4 type 0x67: records from template 02AEC860 (STCYCL 4/4, UNPACK V4_32 NUM 34), work buffer filled by 00532EF0",
      tb.get(0x004E79D5) == "mov dword ptr [rbx + 8], 0x1000404" and tb.get(0x004E7A02) == "mov dword ptr [rbx + 0xc], 0x6c22001e"
      and lp and rip(lp[0]) == 0x02AEC860
      and any(txt(x) == "mov rbx, qword ptr [rcx + 0xb8]" for x in body("00532EF0"))
      and any(txt(x) == "call 0x861ec0" for x in body("00532EF0")))
r5 = {x.address: txt(x) for f in ("0054BE70", "0054D740") for x in body(f)}
r5b = [txt(x) for x in body("005466E0")]
check("R5 finaliser builders write V4_32 headers over copied payloads",
      r5.get(0x0054C10E) == "or ecx, 0x6c000064" and r5.get(0x0054D9EE) == "or ecx, 0x6c000064" and "or eax, 0x6c00" in r5b)
r6 = {x.address: txt(x) for x in body("0045BAE0")}
check("R6 type 0x97's resource stream goes to the raw-packet appenders 003A2E30 / 003A31A0",
      r6.get(0x0045BE73) == "call 0x3a2e30" and r6.get(0x0045BEE0) == "call 0x3a31a0", str([r6.get(0x0045BE73), r6.get(0x0045BEE0)]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
