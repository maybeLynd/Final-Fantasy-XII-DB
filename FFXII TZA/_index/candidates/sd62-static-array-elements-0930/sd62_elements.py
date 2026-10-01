"""sd62_elements.py - the two non-type elements 01F2E330 / 01F2E780 of the 0x50-stride static array (OPUS, 2026-09-30;
register SD-62). Asserts over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import collections, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c, SZ = T.R, T.scan(), T.sizes()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


q = lambda g, n: list(struct.unpack("<%dQ" % n, R.at(g, 8 * n)))
A, B = q(0x01F2E330, 8), q(0x01F2E780, 10)
# F1 - both are statically initialised data, not built at run time: each accessor's cold path only registers an exit
#      destructor (006373D0 -> 008AF490, 00637440 -> 008AFDE0) - and neither starts with a vtable
check("F1", txt(0x006373F7).startswith("lea rax, [rip") and txt(0x00637418).startswith("lea rcx, [rip") and txt(0x0063741F) == "call 0x808b90"
      and txt(0x00637467).startswith("lea rax, [rip") and txt(0x00637488).startswith("lea rcx, [rip") and txt(0x0063748F) == "call 0x808b90"
      and T.rtti_class(A[0]) is None and T.rtti_class(B[0]) is None,
      "static data with exit destructors 008AF490 / 008AFDE0; +0 is a self pointer, not a vtable, in both")
# F2 - 01F2E330: three self-linked list heads (+0x00, +0x10, +0x28) and zeros; it is the object every class descriptor
#      is constructed against: 384 of the 385 calls to the descriptor constructor 00632D80 pass 006373D0() as rdx, which
#      00632D80 stores at the new descriptor's +0x70 (00632DD6)
heads = A[0] == A[1] == 0x01F2E330 and A[2] == A[3] == 0x01F2E340 and A[4] == 0 and A[5] == A[6] == 0x01F2E358 and A[7] == 0
par = collections.Counter()
for f, a in sorted(c["calls"].get(0x00632D80, ())):
    ins = [i for i in R.md.disasm(R.at(f, SZ.get(f, 0x400)), f) if i.address < a][-30:]
    for k in range(len(ins) - 1, -1, -1):
        if ins[k].op_str.startswith("rdx,") and ins[k].mnemonic in ("mov", "lea"):
            cl = next((x.op_str for x in reversed(ins[:k]) if x.mnemonic == "call"), None) if ins[k].op_str == "rdx, rax" else None
            par[cl] += 1
            break
check("F2", heads and par.get("0x6373d0") == 384 and sum(par.values()) == 384 and len(c["calls"].get(0x00632D80, ())) == 385
      and txt(0x00632DD6) == "mov qword ptr [rcx + 0x70], rdx",
      "01F2E330 = list heads +0x00/+0x10/+0x28; 384/385 descriptor constructions pass it as rdx (stored at descriptor +0x70)")
# F3 - 01F2E780: six self-linked qwords (01F2E780-01F2E7A8, a 0x30-byte header); the next object, 01F2E7B0, self-links
#      its own +0x00/+0x08 and holds +0x10 = 02CF8A80 (the PWorld class descriptor: its constructor 00164100 installs
#      00D56D10, RTTI PClassDescriptorWithoutDefaultConstructor<PWorld>) and +0x18 = "getInstanceCount".
#      Corrected 2026-09-30 (OPUS, adjudicating SWE2-ORACLE L5/L6, sd62-registry-list-links-0930): the bytes read here are
#      unchanged; the label used to read B[8]/B[9] as 01F2E780 +0x40/+0x48.
check("F3", B[0] == B[1] == B[2] == B[3] == B[4] == B[5] == 0x01F2E780 and B[6] == B[7] == 0x01F2E7B0 and B[8] == 0x02CF8A80
      and T.cstr(B[9]) == "getInstanceCount" and txt(0x00164160).endswith("rcx")
      and T.rtti_class(0x00D56D10) == ".?AV?$PClassDescriptorWithoutDefaultConstructor@VPWorld@Phyre@@@Phyre@@",
      "01F2E780 = six self-linked qwords; 01F2E7B0 = its own links, +0x10 the PWorld descriptor, +0x18 \"getInstanceCount\"")
cal = sorted(set(f for f, _ in c["calls"].get(0x00637440, ())))
check("F4", cal == [0x0059B430, 0x0062FC90, 0x006388C0, 0x006389C0, 0x00638A50, 0x0063BEF0],
      "00637440's callers %s (0059B430 hashes a name against it)" % ["%08X" % f for f in cal])
print("FAILS %d" % fails)
