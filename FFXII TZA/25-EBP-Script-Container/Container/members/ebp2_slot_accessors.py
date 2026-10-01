import struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
BASE = 0x2098E10          # actor-manager slot array
STRIDE = 0x288
SECTION_FIELDS = {0xA0, 0xA8, 0xB0, 0xD8, 0xE0, 0xF0, 0xF8, 0x100}
WRITES = {"mov": 1, "or": 1, "and": 1, "inc": 1, "dec": 1}

data = open(EXE, "rb").read()
# .text: VA 0x121000 .. +0x7a0635 maps at file off 0x600
CODE_OFF, CODE_VA, CODE_SZ = 0x600, 0x121000, 0x7A0635
body = data[CODE_OFF:CODE_OFF + CODE_SZ]

md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def rd(va, n):
    if CODE_VA <= va < CODE_VA + CODE_SZ:
        return data[CODE_OFF + va - CODE_VA:CODE_OFF + va - CODE_VA + n]
    return b""

# find every "imul reg,reg,0x288" (REX.W + 69 /r, ModRM.mod==3)
sites = []
for i in range(len(body) - 8):
    if 0x48 <= body[i] <= 0x4F and body[i] & 8 and body[i+1] == 0x69 \
            and (body[i+2] >> 6) == 3 \
            and struct.unpack_from("<i", body, i+3)[0] == STRIDE:
        sites.append(CODE_VA + i)
print("imul-0x288 accessor sites:", len(sites))

REGMAP = {}
for b in ("rax","rbx","rcx","rdx","rsi","rdi","rbp","rsp"):
    REGMAP[b] = b; REGMAP["e"+b[1:]] = b; REGMAP[b[1:]] = b
for i in range(8, 16):
    for s in ("","d","w","b"): REGMAP["r%d%s" % (i, s)] = "r%d" % i
REGMAP.update({"al":"rax","bl":"rbx","cl":"rcx","dl":"rdx","ax":"rax","bx":"rbx","cx":"rcx","dx":"rdx"})

section_reads, section_writes, bookkeeping = [], [], []
for s in sites:
    insns = list(md.disasm(rd(s - 8, 0x90), s - 8))
    i0 = next((k for k, ins in enumerate(insns) if ins.address == s), None)
    if i0 is None: continue
    dreg = REGMAP.get(insns[i0].op_str.split(",")[0].strip().strip("'"))
    fold_field = None; sum_base = None; ops = []
    for ins in insns[i0+1:i0+9]:
        # lea reg,[rip+X] landing inside the slot array => folded field base
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = ins.address + ins.size + op.mem.disp
                if BASE <= t < BASE + 16*STRIDE and ins.mnemonic == "lea":
                    fold_field = t - BASE
                    parts = [p.strip() for p in ins.op_str.split(",")]
                    sum_base = parts[0]
        parts = [p.strip() for p in ins.op_str.split(",")]
        if ins.mnemonic == "add" and len(parts) == 2 and \
                dreg in (REGMAP.get(parts[0]), REGMAP.get(parts[1])):
            sum_base = parts[0] if REGMAP.get(parts[0]) == dreg else parts[1]
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base != X86_REG_RIP:
                b = ins.reg_name(op.mem.base); x = ins.reg_name(op.mem.index)
                if (b and REGMAP.get(b) == dreg) or (x and REGMAP.get(x) == dreg) \
                        or (sum_base and b and REGMAP.get(b) == REGMAP.get(sum_base)):
                    ops.append((ins.mnemonic, ins.address, op.mem.disp))
    if fold_field is not None:
        # folded form: field = fold_field + disp of first mem op (usually 0)
        disp = ops[0][2] if ops else 0
        fld = fold_field + disp
        mnem = ops[0][0] if ops else "?"
        rec = (hex(s), hex(fld), mnem)
        (section_reads if mnem not in WRITES else section_writes).append(rec) \
            if fld in SECTION_FIELDS else bookkeeping.append(rec)
    else:
        for mnem, a, disp in ops:
            rec = (hex(s), hex(disp), mnem)
            (section_reads if mnem not in WRITES else section_writes).append(rec) \
                if disp in SECTION_FIELDS else bookkeeping.append(rec)

print("section-field WRITES:", len(section_writes))
for r in section_writes: print("   ", r)
print("section-field READS :", len(section_reads))
for r in section_reads: print("   ", r)
print("bookkeeping accesses:", len(bookkeeping))

# contract: no imul-pattern reader touches a section field
ok = len(section_reads) == 0 and len(section_writes) == 8
print("CHECK section fields write-only via imul accessors:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
