"""vif_templates.py: decode every pre-built VIF1 packet template into one TSV.

Two builder families:
  - the 66 startup objects: (data ptr, builder) pairs harvested from the hubs
    0037DF90 / 0037E0F0 (flat `lea rcx,[rip+data]; call builder` sequences);
  - the 37 MPG packet builders: callers of the record emitter 008631E0
    (from FABLE's vu1_census.json).

Per builder, in object-offset order: the memset size, the header/MPG
registration calls, and every immediate store. The stored bytes are then
parsed as a VIF1 stream: commands are named, their payload sizes are skipped
with the VIF1 layout rules, and stores not attributed to a command are the
control count. Loops that write the buffer (backward branch around induction
stores) are reported as repeated-block regions rather than unrolled.
"""
import struct, json, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP

EXE   = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
CEN   = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\vu1_census.json"
BASE  = 0x120000
MEMSET, HDR, MPG = 0x00861EC0, 0x008631D0, 0x008631E0
HUBS = (0x0037DF90, 0x0037E0F0)

sizes = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    if d[o:o + 8].rstrip(b"\0") == b".text":
        va = struct.unpack_from("<I", d, o + 12)[0]
        ro = struct.unpack_from("<I", d, o + 20)[0]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def body(a):
    return list(md.disasm(d[ro + a - BASE - va: ro + a - BASE - va + sizes[a]], a))

# ---------------- static scan: calls + immediate stores ----------------

def scan(a):
    """Return calls, stores, loop store groups for one builder.
    stores: (obj_off, width, imm, insn_addr).  Base register aliases of rcx
    are tracked through mov/lea; integer immediates tracked per register for
    call args and loop trip counts."""
    ins = body(a)
    calls, stores = [], []
    aliases = {"rcx": 0}            # reg -> offset from obj
    imm32 = {}                      # reg -> last 32-bit immediate
    for i in ins:
        ops = i.operands
        if not ops: continue
        # alias propagation
        if i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
            s = ops[1].reg; sname = i.reg_name(s)
            dname = i.reg_name(ops[0].reg)
            if sname in aliases:
                aliases[dname] = aliases[sname]
            elif ops[0].size == 8:
                aliases.pop(dname, None)
            if ops[0].size == 4 and ops[1].type == X86_OP_REG:
                imm32.pop(dname, None)
        elif i.mnemonic == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM:
            s = i.reg_name(ops[1].mem.base); dname = i.reg_name(ops[0].reg)
            if s in aliases:
                aliases[dname] = aliases[s] + ops[1].mem.disp
            elif ops[1].mem.base == X86_REG_RIP:
                imm32[dname] = i.address + i.size + ops[1].mem.disp  # rip-absolute target addr
            else:
                aliases.pop(dname, None)
        elif i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_IMM:
            imm32[i.reg_name(ops[0].reg)] = ops[1].imm
        elif i.mnemonic == "xor" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG and ops[0].reg == ops[1].reg:
            imm32[i.reg_name(ops[0].reg)] = 0
        # immediate store into an alias of the object
        if i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_IMM:
            b = i.reg_name(ops[0].mem.base)
            if b in aliases:
                stores.append((aliases[b] + ops[0].mem.disp, ops[0].size,
                               ops[1].imm & ((1 << (ops[0].size * 8)) - 1), i.address))
        # calls of interest
        if i.mnemonic == "call" and ops and ops[0].type == X86_OP_IMM:
            t = ops[0].imm
            if t == MEMSET:
                calls.append(("memset", i.address, imm32.get("r8d"), imm32.get("edx")))
            elif t == HDR:
                calls.append(("header", i.address, imm32.get("edx"), aliases.get("rcx")))
            elif t == MPG:
                calls.append(("mpg", i.address, imm32.get("rdx"), imm32.get("r8d")))
    return calls, stores, ins

# ---------------- hub pair harvest ----------------

def hub_pairs():
    pairs = []
    for h in HUBS:
        last_data = None
        for i in body(h):
            if i.mnemonic == "lea" and i.operands[0].type == X86_OP_REG \
               and i.operands[1].type == X86_OP_MEM and i.operands[1].mem.base == X86_REG_RIP:
                if i.reg_name(i.operands[0].reg) == "rcx":
                    last_data = i.address + i.size + i.operands[1].mem.disp
            if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM:
                pairs.append((i.operands[0].imm, last_data, h))
    return pairs

# ---------------- VIF stream decode ----------------

VN = ["S", "V2", "V3", "V4"]; VL = [32, 16, 8, 4]
VLW = {0: 4, 1: 2, 2: 1, 3: 0.5}
def unpack_len(cmd, num):
    vl = cmd & 3; vn = (cmd >> 2) & 3
    bits = num * (vn + 1) * VLW[vl] * 8
    return (bits + 31) // 32 * 4  # dword-rounded payload bytes

def classify(v):
    top, low = v >> 24, v & 0xFFFFFF
    if top == 0x00: return ("NOP", 0)
    if top == 0x01: return ("STCYCL CYCLE=%d WL=%d" % (v & 0xFF, (v >> 8) & 0xFF), 0)
    if top in (0x02, 0x03): return (("OFFSET" if top == 2 else "BASE") + " %d" % (v & 0x3FF), 0)
    if top == 0x04: return ("ITOP %d" % (v & 0x3FF), 0)
    if top == 0x05: return ("STMOD %d" % (v & 3), 0)
    if top == 0x07: return ("MARK 0x%04x" % (v & 0xFFFF), 0)
    if top in (0x10, 0x11, 0x13): return ({0x10: "FLUSHE", 0x11: "FLUSH", 0x13: "FLUSHA"}[top], 0)
    if top in (0x14, 0x15, 0x17): return ({0x14: "MSCAL", 0x15: "MSCALF", 0x17: "MSCNT"}[top] + " %d" % (v & 0xFFFF), 0)
    if top == 0x20: return ("STMASK", 4)            # 1 dword payload
    if top == 0x30: return ("STROW", 16)
    if top == 0x31: return ("STCOL", 16)
    if top == 0x4A: return ("MPG num=%d addr=%d" % (v & 0xFF, (v >> 16) & 0xFF) + " [via record table]", 0)
    if top in (0x50, 0x51): return (("DIRECT" if top == 0x50 else "DIRECTHL") + " %d" % (v & 0xFFFF), (v & 0xFFFF) * 16)
    if 0x60 <= top <= 0x7F:
        num = (v >> 16) & 0xFF; addr = v & 0x3FF
        cmd = top & 0x1F
        name = "UNPACK %s-%d num=%d addr=%d" % (VN[(cmd >> 2) & 3], VL[cmd & 3], num, addr)
        if v & 0x4000: name += " +SgnMask"
        if v & 0x8000: name += " +AddrOffs"
        return (name, unpack_len(top, num))
    return (None, 0)

def decode_stream(stores, patches=()):
    """stores -> ordered event list. Buffer assembled at object offsets;
    walked as a VIF stream from the first command. Returns (events, buf,
    cmd_payload_ranges) where each cmd's payload span is recorded.
    patches: (offset, bytes) final-state writes the helpers stamp over the
    builder's immediates (e.g. 008631D0 sub-headers: word@X, kind@X+3,
    dword 0@X+4)."""
    buf = {}
    width_at = {}
    for off, w, imm, ad in stores:
        for k in range(w):
            buf[off + k] = (imm >> (8 * k)) & 0xFF
            width_at[off + k] = w
    for off, bs in patches:
        for k, b in enumerate(bs):
            buf[off + k] = b
            width_at[off + k] = len(bs)
    events, spans = [], []
    pos = min(buf) if buf else 0
    end = max(buf) + 1 if buf else 0
    while pos + 4 <= end:
        v = struct.unpack_from("<I", bytes(buf.get(p, 0) for p in range(pos, pos + 4)))[0]
        name, plen = classify(v)
        if name is None:
            events.append(("payload", pos, v))
            spans.append((pos, pos + width_at.get(pos, 4)))
            pos += width_at.get(pos, 4)
            continue
        events.append(("cmd", pos, name))
        if plen:
            spans.append((pos + 4, pos + 4 + plen))
        pos += 4 + plen
    return events, buf, spans
