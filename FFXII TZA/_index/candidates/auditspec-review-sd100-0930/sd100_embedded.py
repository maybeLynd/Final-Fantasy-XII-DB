"""sd100_embedded.py - SWE2-AUDIT-SPEC: mode-byte writes to text elements that are NOT addressed as [element + 0xB0].

sd100_instances.out shows elements built on the stack ([rsp+0x20/0x30/0x40] passed to 002AC1E0 / 002B3C30) and one
embedded at container +0xD0 (002A3730 passes rdi+0xD0 to 002B3950 and reads byte [rdi+0x180]). A write to such an
element's mode byte has displacement K + 0xB0, which the +0xB0 census cannot see.

  A  for each stack-element function: every write, on ANY base, whose operand covers byte (K + 0xB0) of rsp, and every
     write covering (K + 0xB0 - d) through a frame register set as lea rbp,[rsp+d] (none found = printed as such);
     also any rep stos / call memset-like in the body is listed (block initialisers);
  B  image-wide: every write covering displacement 0x180 (the container +0xD0 element's mode byte), any base,
     grouped by .pdata root, restricted to the text cluster 0029E000..002B6000 plus a count outside it.
Control: 002A3790 (movzx eax, byte [rdi+0x180]) must be found as a READ in B.
"""
import bisect, collections, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_REG, CS_AC_WRITE, CS_AC_READ
from capstone.x86 import X86_REG_RSP, X86_REG_RBP


def is_w(i, op):
    """capstone 5.0.7 marks the memory destination of movups / movq / movlps / movhps as READ; a mov-family
    instruction whose FIRST operand is this memory operand is a store."""
    if op.access & CS_AC_WRITE:
        return True
    o0 = i.operands[0] if len(i.operands) else None
    return (o0 is not None and o0.type == CS_OP_MEM and o0.mem.base == op.mem.base and o0.mem.disp == op.mem.disp
            and o0.mem.index == op.mem.index and i.mnemonic.startswith(("mov", "vmov"))
            and i.mnemonic not in ("movzx", "movsx", "movsxd"))

dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
_o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, _o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def chain_root(e):
    for _ in range(32):
        uo = T.off(T.IB + e[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
        if not (fl & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)
    return None


def root(va):
    rva = va - T.IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    return chain_root(PD[j])


def ranges(r):
    """all .pdata ranges whose chain root is r"""
    return sorted((T.IB + e[0], T.IB + e[1]) for e in PD if chain_root(e) == r)


def body(r):
    out = []
    for a, b in ranges(r):
        out += T.dis(a, b)
    return out


print("== A: stack elements")
STACK = [(0x002A5460, 0x30), (0x002B3050, 0x20), (0x002B5390, 0x30), (0x002A1B00, 0x40)]
for r, K in STACK:
    ins = body(r)
    tgt = K + 0xB0
    frame = {}
    for i in ins:
        if i.mnemonic == "lea" and len(i.operands) == 2 and i.operands[0].type == CS_OP_REG and i.operands[0].reg == X86_REG_RBP \
                and i.operands[1].mem.base == X86_REG_RSP:
            frame["rbp"] = i.operands[1].mem.disp
    hits, blk = [], []
    for i in ins:
        if i.mnemonic.startswith("rep") or i.mnemonic in ("stosb", "stosd", "stosq", "movsb", "movsq"):
            blk.append(i)
        for op in i.operands:
            if op.type != CS_OP_MEM or not is_w(i, op):
                continue
            m = op.mem
            if m.base == X86_REG_RSP and m.disp <= tgt < m.disp + op.size:
                hits.append(i)
            if m.base == X86_REG_RBP and "rbp" in frame and m.disp <= tgt - frame["rbp"] < m.disp + op.size:
                hits.append(i)
    rs = ranges(r)
    print("%08X  element [rsp+0x%X] -> mode byte rsp+0x%X  body %d ins in %d range(s) %s  frame %s" % (
        r, K, tgt, len(ins), len(rs), ["%08X-%08X" % x for x in rs], frame or "none"))
    for i in hits:
        print("    write  %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
    for i in blk:
        print("    block  %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
    if not hits:
        print("    no write covers the mode byte through rsp / rbp")

print("== B: displacement 0x180 (container +0xD0 element's mode byte)")
EXEC = [(n, v, vs, p, rs) for n, v, vs, p, rs, x in T.SECS if x]
sites = {}
for n, v, vs, p, rs in EXEC:
    blob = T.raw[p:p + min(vs, rs)]
    for D in range(0x161, 0x181):
        pat = struct.pack("<i", D)
        k = blob.find(pat)
        while k >= 0:
            for back in range(11, 0, -1):
                if k - back < 0:
                    continue
                insl = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                if not insl:
                    continue
                i = insl[0]
                if not (i.address < v + k and v + k + 4 <= i.address + i.size):
                    continue
                mops = [op for op in i.operands if op.type == CS_OP_MEM and op.mem.disp == D and op.mem.base != T.X86_REG_RIP
                        and op.mem.base != T.X86_REG_INVALID]
                if mops:
                    sites[i.address] = (i, mops[0], D)
                    break
            k = blob.find(pat, k + 1)
w_in, r_in, w_out = [], [], 0
for a, (i, op, D) in sorted(sites.items()):
    if not (D <= 0x180 < D + op.size):
        continue
    inreg = 0x0029E000 <= a < 0x002B6000
    if is_w(i, op):
        if inreg:
            w_in.append((a, i, op))
        else:
            w_out += 1
    elif inreg:
        r_in.append((a, i))
print("control read 002A3790 present: %s" % any(a == 0x002A3790 for a, _ in r_in))
print("text cluster: writes %d, reads %d; writes outside the cluster: %d" % (len(w_in), len(r_in), w_out))
for a, i, op in w_in:
    r = root(a)
    print("    write  %s  %08X  %dB  %s %s" % ("%08X" % r if r else "--------", a, op.size, i.mnemonic, i.op_str))
for a, i in r_in:
    r = root(a)
    print("    read   %s  %08X  %s %s" % ("%08X" % r if r else "--------", a, i.mnemonic, i.op_str))
