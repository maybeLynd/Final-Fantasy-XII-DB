"""sd100_census.py - SWE2-AUDIT-SPEC independent writer census of the text element's mode byte +0xB0 (2026-09-30).

Written without the package's `pe` function list or regex. Image-wide over executable sections of the certified image
(loader: ../auditspec-review-ov31-type-store-0929/ov31_indep.py, sha256 asserted):

  - every disp32 in 0x91..0xB0 (a store at D of width W covers byte +0xB0 when D <= 0xB0 < D + W; widths up to 32),
    found by raw byte search and the longest valid back-decode whose displacement field is the hit;
  - ANY base register (rbp / rsp / index forms included), ANY mnemonic whose memory operand capstone marks WRITE;
  - each write classified by whether it can change the low byte of +0xB0 (and / or / xor / bt* immediates tested
    bit by bit; mov / add / sub / inc / dec / set* / xchg / movups and wider always can);
  - the .pdata chain root of each site ("--------" = outside every .pdata range).

Controls: the package's 20 byte stores must all appear; the stepper's read 002ABF79 must appear as a READ.
Output: all low-byte-changing writes, grouped by root, plus counts.
"""
import bisect, collections, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_IMM, CS_AC_WRITE, CS_AC_READ


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
o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def root(va):
    rva = va - T.IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    e = PD[j]
    for _ in range(32):
        uo = T.off(T.IB + e[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
        if not (fl & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)
    return None


EXEC = [(n, v, vs, p, rs) for n, v, vs, p, rs, x in T.SECS if x]
sites = {}
for n, v, vs, p, rs in EXEC:
    blob = T.raw[p:p + min(vs, rs)]
    for D in range(0x91, 0xB1):
        pat = struct.pack("<i", D)
        k = blob.find(pat)
        while k >= 0:
            for back in range(11, 0, -1):
                if k - back < 0:
                    continue
                ins = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                if not ins:
                    continue
                i = ins[0]
                if not (i.address < v + k and v + k + 4 <= i.address + i.size):
                    continue
                mops = [op for op in i.operands if op.type == CS_OP_MEM and op.mem.disp == D and op.mem.base != T.X86_REG_RIP
                        and op.mem.base != T.X86_REG_INVALID]
                if mops:
                    sites[i.address] = (i, mops[0], D)
                    break
            k = blob.find(pat, k + 1)


def lowbyte_changes(i, op, D):
    sh = (0xB0 - D) * 8
    mn = i.mnemonic
    imms = [x.imm for x in i.operands if x.type == CS_OP_IMM]
    if mn in ("or", "xor", "and") and imms:
        m = (imms[0] & ((1 << (op.size * 8)) - 1)) >> sh & 0xFF
        return m != 0xFF if mn == "and" else m != 0
    if mn in ("bts", "btr", "btc") and imms:
        return sh <= imms[0] < sh + 8
    if mn in ("or", "xor", "and", "bts", "btr", "btc"):
        return "reg"          # register operand: value unknown statically
    return True


writes, reads = [], []
for a, (i, op, D) in sorted(sites.items()):
    if not (D <= 0xB0 < D + op.size):
        continue
    if is_w(i, op):
        writes.append((a, i, op, D, lowbyte_changes(i, op, D)))
    elif op.access & CS_AC_READ or i.mnemonic == "lea":
        reads.append(a)

print("sites decoded with a disp in 0x91..0xB0 (non-rip base): %d" % len(sites))
print("covering byte +0xB0: writes %d, reads %d" % (len(writes), len(reads)))
print("control read 002ABF79 present: %s" % (0x002ABF79 in reads))
pkg = [0x002A5E75, 0x002ABFC3, 0x002AC1A4, 0x002AC239, 0x002B3D68, 0x002A8D2B, 0x002A9923, 0x002A989E, 0x002A9428,
       0x002A9193, 0x002B199A, 0x002A97EA, 0x002A98B5, 0x002AD225, 0x002A67DB, 0x002A9AA2, 0x002A9D1C, 0x002A3556,
       0x002B3963, 0x002A9A27]
wa = {w[0] for w in writes}
print("control: package's 20 stores present: %d of 20 %s" % (sum(a in wa for a in pkg), [("%08X" % a) for a in pkg if a not in wa]))

chg = [w for w in writes if w[4] is not False]
print("writes that can change the low byte: %d (of which register-operand and/or/xor/bt*: %d); cannot: %d" % (
    len(chg), sum(1 for w in chg if w[4] == "reg"), len(writes) - len(chg)))
byroot = collections.defaultdict(list)
for w in chg:
    r = root(w[0])
    byroot[r].append(w)
kinds = collections.Counter()
for w in chg:
    kinds["%s %dB" % (w[1].mnemonic, w[2].size)] += 1
print("by form: %s" % ", ".join("%s x%d" % kv for kv in kinds.most_common()))
print("roots: %d (outside .pdata: %d sites)" % (len(byroot), len(byroot.get(None, []))))
print("--- every low-byte-changing write, sorted by site (root | site | D | width | instruction | pkg?)")
for w in sorted(chg, key=lambda w: w[0]):
    a, i, op, D, c = w
    r = root(a)
    print("%s  %08X  D=0x%02X %2dB  %s %s%s%s" % ("%08X" % r if r else "--------", a, D, op.size, i.mnemonic, i.op_str,
          "   [pkg]" if a in pkg else "", "   [reg-operand]" if c == "reg" else ""))
