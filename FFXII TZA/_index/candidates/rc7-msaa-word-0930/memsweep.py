"""memsweep.py - ORACLE, 2026-09-30.  Linear-sweep every .pdata fragment of the image (chain-root owners) and record
every instruction with a memory operand: (va, root, mnemonic, op_str, operand index, base reg, index reg, scale, disp,
access size, rip target or None, write flag).  Write flag: the memory operand is operand 0 of an instruction with more
than one operand that is not cmp/test/bt, or the single operand of inc/dec/not/neg/set*/pop.  Cached to memsweep.pkl.
Blind spot: bytes not covered by any .pdata fragment (leaf functions without unwind data) are not swept; the callers of
each question's key functions are checked separately."""
import os, pickle, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

import tempfile
CACHE = os.path.join(tempfile.gettempdir(), "oracle_memsweep_73461d08.pkl")   # 50 MB cache, kept out of the record
ONE_OP_WRITE = ("inc", "dec", "not", "neg", "pop")


def build():
    recs = []
    for b, e, _u in img.PDATA:
        root = img.FRAG_ROOT[b]
        for x in img.md.disasm(img.rd(b, e - b), b):
            ops = x.operands
            for k, o in enumerate(ops):
                if o.type != X86_OP_MEM:
                    continue
                m = o.mem
                rip = x.address + x.size + m.disp if m.base == X86_REG_RIP else None
                w = (k == 0 and len(ops) > 1 and not x.mnemonic.startswith(("cmp", "test", "bt", "ucomis", "comis"))
                     and x.mnemonic != "lea") or (len(ops) == 1 and (x.mnemonic in ONE_OP_WRITE or x.mnemonic.startswith("set")))
                recs.append((x.address, root, x.mnemonic, x.op_str, k,
                             x.reg_name(m.base) if m.base else None, x.reg_name(m.index) if m.index else None, m.scale,
                             m.disp, o.size, rip, w))
    # leaf bodies without .pdata: functions.tsv entries whose start no fragment covers
    FUNCS = os.path.join(os.path.dirname(img.EXE), "..", "graph", "functions.tsv")
    for i, line in enumerate(open(FUNCS, encoding="utf-8", errors="replace")):
        p = line.rstrip("\n").split("\t")
        if i == 0 or len(p) < 3:
            continue
        try:
            a, n = int(p[0], 16), int(p[2])
        except ValueError:
            continue
        if img.owner(a) is not None or n <= 0:
            continue
        for x in img.md.disasm(img.rd(a, n), a):
            ops = x.operands
            for k, o in enumerate(ops):
                if o.type != X86_OP_MEM:
                    continue
                m = o.mem
                rip = x.address + x.size + m.disp if m.base == X86_REG_RIP else None
                w = (k == 0 and len(ops) > 1 and not x.mnemonic.startswith(("cmp", "test", "bt", "ucomis", "comis"))
                     and x.mnemonic != "lea") or (len(ops) == 1 and (x.mnemonic in ONE_OP_WRITE or x.mnemonic.startswith("set")))
                recs.append((x.address, a, x.mnemonic, x.op_str, k,
                             x.reg_name(m.base) if m.base else None, x.reg_name(m.index) if m.index else None, m.scale,
                             m.disp, o.size, rip, w))
    return recs


def load():
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, "rb"))
    r = build()
    pickle.dump(r, open(CACHE, "wb"))
    return r


if __name__ == "__main__":
    r = load()
    print(len(r), "memory-operand records")
