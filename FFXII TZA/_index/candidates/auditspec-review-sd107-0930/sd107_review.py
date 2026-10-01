"""SWE2-AUDIT-SPEC independent sweep for SD-107 (2026-09-30).
The author's K1 counts only `mov [m], imm` whose byte at +0xA3 is 1. Other store shapes can also leave 1 in a zeroed
kind byte: setcc (stores 0/1), inc, or/add/adc/xor/bts with an immediate. This sweep decodes every function in
functions.tsv with capstone detail (operand widths from capstone, not from op_str text) and classes every memory
destination whose byte range covers +0xA3 off a non-rip, non-rsp base by instruction kind.
Control: the class `mov-imm-1` must list 007E7401 (the author's K1 hit) and the total must be of the order of the
author's 552 (different function lists, so equality is not expected).
"""
import sys, collections, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG
cls = collections.Counter(); lists = collections.defaultdict(list)
for e, sz in tk.flist:
    o = tk.off(e)
    if o is None or sz <= 0 or sz > 0x40000: continue
    for x in tk.md.disasm(tk.d[o:o + sz], e):
        if not x.operands or x.operands[0].type != X86_OP_MEM or not tk.is_store(x, 0): continue
        m = x.operands[0].mem
        b = x.reg_name(m.base) if m.base else None
        if b in ("rip", "rsp", "esp") or b is None: continue
        w = x.operands[0].size or 1
        if not (m.disp <= 0xA3 < m.disp + w): continue
        mn = x.mnemonic
        imm = next((op.imm for op in x.operands[1:] if op.type == X86_OP_IMM), None)
        sh = 8 * (0xA3 - m.disp)
        if mn == "mov" and imm is not None:
            k = "mov-imm-1" if ((imm & ((1 << (8 * min(w, 8))) - 1)) >> sh) & 0xFF == 1 else "mov-imm-other"
        elif mn.startswith("set"):
            k = "setcc"
        elif mn in ("inc", "dec", "neg", "not"):
            k = mn
        elif mn in ("or", "add", "adc", "xor", "bts", "btc", "sub", "sbb", "and", "btr") and imm is not None:
            k = "%s-imm" % mn
        elif mn in ("mov", "movups", "movaps", "movdqu", "movdqa", "movq", "movd", "vmovups", "vmovdqu", "vmovaps") :
            k = "mov-reg"
        else:
            k = "other:" + mn
        cls[k] += 1
        if k in ("mov-imm-1", "setcc", "inc", "dec", "neg", "not") or (k.endswith("-imm") and not k.startswith(("and", "btr"))) or k.startswith("other"):
            lists[k].append("%08X %s %s  [%s]" % (x.address, mn, x.op_str, tk.fname(x.address)))
print("total object stores covering +0xA3: %d" % sum(cls.values()))
for k, n in cls.most_common():
    print("  %-16s %d" % (k, n))
for k in sorted(lists):
    print("%s:" % k)
    for s in lists[k][:40]:
        print("   " + s)
