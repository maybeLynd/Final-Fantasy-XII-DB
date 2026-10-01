"""Shared helper: the kind-N path arrays as 002DF9A0 installs them (first language arm in address order, as
tools/res_request_census.py reads them): directory 0215F000[kind] -> array of char* per id.
python kind7.py [KIND] [REGEX]  prints id -> path for the kind (default 7)."""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, dis, cstr, u64  # noqa


def directory():
    kinds, last = {}, {}
    for ins in dis(0x2DF9A0):
        m = re.match(r"(r[a-z0-9]+), \[rip ([+-]) 0x([0-9a-f]+)\]$", ins.op_str)
        if ins.mnemonic == "lea" and m:
            v = int(m.group(3), 16)
            last[m.group(1)] = ins.address + ins.size + (v if m.group(2) == "+" else -v)
        elif ins.mnemonic == "mov" and ins.op_str.startswith("qword ptr [rip"):
            reg = ins.op_str.rsplit(", ", 1)[1]
            m2 = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", ins.op_str)
            v = int(m2.group(2), 16)
            dst = ins.address + ins.size + (v if m2.group(1) == "+" else -v)
            if reg in last and 0x215F000 <= dst < 0x215F200 and (dst - 0x215F000) % 8 == 0:
                kinds.setdefault((dst - 0x215F000) // 8, last[reg])
        elif ins.mnemonic == "ret":
            break
    return kinds


def paths(kind=7, limit=4096, stop_on_miss=True):
    """id -> path; the kind-7 'in' arm spans ids 0x5..0x5E0 (pass limit=0x5E1, stop_on_miss=False for all of it)"""
    arr = directory()[kind]
    out, miss = {}, 0
    for i in range(limit):
        p = u64(arr + 8 * i)
        s = cstr(p, 260) if p else None
        if s is None or not s.isprintable() or len(s) < 3:
            miss += 1
            if stop_on_miss and miss > 32:
                break
            continue
        miss = 0
        out[i] = s
    return arr, out


if __name__ == "__main__":
    k = int(sys.argv[1], 0) if len(sys.argv) > 1 else 7
    pat = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
    arr, ps = paths(k)
    print("kind %d array %08X: %d paths" % (k, arr, len(ps)))
    for i, s in ps.items():
        if pat is None or pat.search(s):
            print("  0x%03X %4d  %s" % (i, i, s))
