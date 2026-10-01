"""sd9_input_deadline.py - the deadline arithmetic in 0035E7A0 (constants 0x13A / 0x108) (OPUS, 2026-09-30; register SD-9)

Re-reads each fact from the certified image through Database/Tools/analysis-kit/gfz-scripts/retool.py and asserts it.
Prints PASS/FAIL per fact and `FAILS n` last.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import pefile  # noqa: E402

R, c = T.R, T.scan()
fails = 0
pe = pefile.PE(R.b.EXE, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
DATA = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".data"][0]


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def refs(g):
    return sorted((f, a, k) for f, a, k in c["refs"].get(g, ()))


def zero_init(g):
    return g - (BASE + DATA.VirtualAddress) >= DATA.SizeOfRawData


# F1 - the period: 0x13A unless 00290180() == 2, then 0x108 (0035E7BC..0035E7CE); 00290180 is `mov eax, 2; ret`
f1 = [ins(a) for a in (0x0035E7BC, 0x0035E7C1, 0x0035E7C4, 0x0035E7C9, 0x0035E7CE)]
g = [ins(a) for a in (0x00290180, 0x00290185)]
check("F1", f1[0].op_str == "0x290180" and f1[1].op_str == "eax, 2" and f1[2].op_str == "ebx, 0x13a" and f1[3].op_str == "ecx, 0x108"
      and f1[4].mnemonic == "cmove" and g[0].op_str == "eax, 2" and g[1].mnemonic == "ret",
      "period P = 0x108 always: 00290180 returns the constant 2, so the 0x13A branch is never taken")
# F2 - the three results: acc < P and mode 3 -> P - acc; acc < P otherwise -> 2P - acc; acc >= P -> ceil(acc/P)*P - acc
f2 = [ins(a) for a in (0x0035E7D1, 0x0035E7D5, 0x0035E7DA, 0x0035E7DF, 0x0035E7E1, 0x0035E7F0, 0x0035E7F7, 0x0035E7FC, 0x0035E7FE)]
check("F2", f2[0].op_str == "edi, ebx" and f2[1].op_str == "0x229ea0" and f2[2].op_str == "eax, 3" and f2[3].op_str == "ebx, ebx"
      and f2[4].op_str == "ebx, edi" and f2[5].op_str == "ecx, [rbx + rdi]" and f2[6].mnemonic == "idiv" and f2[7].op_str == "ebx, edx"
      and f2[8].op_str == "ebx, edi" and ins(0x00229EA0).op_str.startswith("eax, byte ptr [rip"),
      "returns P-acc (mode 3, 00229EA0 = movsx [02064AD3]), 2P-acc, or the distance to the next multiple of P")
# F3 - the step [022CA5D0] is zero-initialised and only ever read (0035E7B0, 0035EBF3)
r3 = refs(0x022CA5D0)
check("F3", zero_init(0x022CA5D0) and [k for _, _, k in r3] == ["R", "R"], "step [022CA5D0]: zero-initialised, references %s" % r3)
# F4 - the accumulator [022CA5C4]: zero-initialised; adds the step (0035E7B6, 0035EBF9); cleared by 0035EB70 (r8d = 0)
r4 = refs(0x022CA5C4)
clr = ins(0x0035EC65)
check("F4", zero_init(0x022CA5C4) and clr.op_str.endswith("r8d") and ins(0x0035EC1F).op_str == "r8d, r8d"
      and sorted(a for _, a, k in r4 if k == "W") == [0x0035E7B6, 0x0035EBF9, 0x0035EC65],
      "acc starts 0, gains only the zero step, and is cleared each pass: acc = 0 at every call, so the result is 2P = 528 "
      "(P = 264 in dispatcher mode 3)")
# F5 - the result is stored at [022CA5DC] (0035EC11) and [022CA5D8] holds acc; neither is ever read through rip
r5 = refs(0x022CA5DC) + refs(0x022CA5D8)
check("F5", ins(0x0035EC05).op_str == "0x35e7a0" and ins(0x0035EC11).op_str.endswith("eax")
      and all(k == "W" for _, _, k in r5), "stores only: %s" % ["%08X@%08X" % (f, a) for f, a, _ in r5])
# F6 - no base-pointer route: no stored pointer into 022CA5C0..022CA5E0, and the objects addressed nearby end before it
#      (022CA520 is cleared as 0x98 bytes at 0035D361; the next address taken above is 022CA640)
qn = []
for s in pe.sections:
    data = s.get_data()
    for off in range(0, len(data) - 7, 8):
        if 0x022CA5C0 <= struct.unpack_from("<Q", data, off)[0] < 0x022CA5E0:
            qn.append(BASE + s.VirtualAddress + off)
leas = sorted(g for g, xs in c["refs"].items() if 0x022CA400 <= g < 0x022CA640 and any(k == "lea" for _, _, k in xs))
check("F6", not qn and leas == [0x022CA408, 0x022CA438, 0x022CA480, 0x022CA520] and ins(0x0035D361).op_str == "r8d, 0x98",
      "stored pointers: %d; addresses taken below: %s; 022CA520 + 0x98 = 022CA5B8 < 022CA5C4" % (len(qn), ["%08X" % x for x in leas]))
print("FAILS %d" % fails)
