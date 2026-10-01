"""eastl_dd_check.py - OPUS DD owner read of eastl-strings-containers-and-the-logging-allocator.md (2026-09-30): the facts the
page edits rest on. Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = ins(a)
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return a + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)


# N1 - the allocator_memory_log constructor 001EDF00 keeps no name: it is 14 bytes, stores the vtable 00902720 and returns
#      this; no instruction reads rdx (the name argument) (BS-6)
body = list(R.md.disasm(R.at(0x001EDF00, SZ[0x001EDF00]), 0x001EDF00))
check("N1", SZ[0x001EDF00] == 14 and not any("rdx" in i.op_str or "edx" in i.op_str for i in body)
      and any(i.mnemonic == "lea" and "rip" in i.op_str and rip(i.address) == 0x00902720 for i in body)
      and body[-1].mnemonic == "ret",
      "001EDF00: vtable store + return; the name in rdx is never read")
# F1 - 001FF6B0 makes a JsonBox value an object (type 3; a 0x38-byte map built with an allocator named 'EASTL map'
#      at 008F4120) when it is not one, then tail-jumps to the find 001FF4F0
check("F1", SZ[0x001FF6B0] == 130 and txt(0x001FF6CF) == "cmp dword ptr [rcx], 3" and txt(0x001FF6D9) == "mov dword ptr [rbx], 3"
      and txt(0x001FF6DF) == "mov ecx, 0x38" and rip(0x001FF6F6) == 0x008F4120 and txt(0x001FF702) == "call 0x1edf00"
      and txt(0x001FF70D) == "call 0x1fe510" and txt(0x001FF72D) == "jmp 0x1ff4f0",
      "001FF6B0: ensure-object, then tail-jump to the find 001FF4F0")
# F2 - 001FF740 (the C-string adapter) has 17 calling functions, at 669 call sites
fns = set(f for f, s in c["calls"].get(0x001FF740, ()))
check("F2", len(fns) == 17 and len(c["calls"].get(0x001FF740, ())) == 669,
      "001FF740: 17 calling functions, 669 call sites")
# A1 - each string initialiser registers its own destructor, an 008Axxxx body, through the atexit wrapper 00808B90 by
#      tail jump (two sampled, one of each size)
check("A1", rip(0x0015C62B) == 0x008A69F0 and txt(0x0015C63F) == "jmp 0x808b90" and rip(0x0015D6E7) == 0x008A70F0
      and txt(0x0015D6FB) == "jmp 0x808b90",
      "the destructors 008A69F0 / 008A70F0 go to 00808B90 by tail jump")
print("FAILS %d" % fails)
