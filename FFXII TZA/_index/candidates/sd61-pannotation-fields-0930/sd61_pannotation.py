"""sd61_pannotation.py - what a Phyre::PAnnotation's +0x18 / +0x20 / +0x28 carry, and what it annotates (OPUS, 2026-09-30;
register SD-61). Asserts over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import collections, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c, SZ = T.R, T.scan(), T.sizes()
fails = 0
CTOR, KEYCTOR, ATTACH, MEMBER = 0x006B66C0, 0x006B66F0, 0x006B67D0, 0x00632960


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def target(i):
    return i.address + i.size + i.operands[1].mem.disp


# F1 - the constructor: vtable PAnnotation, a self-linked list node at +8 / +0x10, rdx -> +0x18, r8 -> +0x20, r9d -> +0x28
check("F1", [txt(a) for a in (0x006B66C0, 0x006B66C4, 0x006B66C7, 0x006B66D8, 0x006B66DC, 0x006B66E0)] ==
      ["lea rax, [rcx + 8]", "mov qword ptr [rax], rax", "mov qword ptr [rax + 8], rax", "mov qword ptr [rcx + 0x18], rdx",
       "mov qword ptr [rcx + 0x20], r8", "mov dword ptr [rcx + 0x28], r9d"] and T.rtti_class(0x00D80930) == "Phyre::PAnnotation",
      "006B66C0: PAnnotation {vtbl, node +8/+0x10, +0x18 = rdx, +0x20 = r8, +0x28 = r9d}")
# F2 - every call site: rdx, r8, r9d, the member it follows, the derived vtable and the value stored after it
rows = collections.Counter()
for f, a in sorted(c["calls"].get(CTOR, ())):
    body = list(R.md.disasm(R.at(f, SZ.get(f, 0x400)), f))
    k = [i.address for i in body].index(a)
    before, after = body[max(0, k - 80):k], body[k + 1:k + 8]
    rdx = next((target(i) for i in reversed(before) if i.mnemonic == "lea" and i.op_str.startswith("rdx, [rip")), None)
    r8 = next((i.op_str for i in reversed(before) if i.op_str.startswith("r8,")), None)
    r9 = next((i.op_str for i in reversed(before) if i.op_str.startswith("r9d,") or i.op_str.startswith("r9,")), None)
    mem = None
    for j in range(len(before) - 1, -1, -1):
        if before[j].mnemonic == "call" and before[j].op_str == "0x632960":
            nm = next((target(x) for x in reversed(before[max(0, j - 12):j]) if x.mnemonic == "lea" and x.op_str.startswith("r9, [rip")), None)
            mem = T.cstr(nm) if nm else None
            break
    dvt = next((target(i) for i in after if i.mnemonic == "lea" and i.op_str.startswith("rax, [rip")), None)
    val = next((i.op_str.split(", ")[-1] for i in after if i.mnemonic == "mov" and i.op_str.startswith("dword ptr [rip")), None)
    rows[("%08X" % rdx if rdx else "arg", r8, r9, mem, T.rtti_class(dvt) if dvt else None, val)] += 1
for k, v in rows.most_common():
    print("      %2d x key %s, r8 %s, r9 %s, follows member %r, derived %s, value %s" % ((v,) + k))
main = rows.most_common(1)[0]
check("F2", main[1] == 69 and sum(rows.values()) == 70 and main[0][0] == "02CF8570" and main[0][1] == "r8, rax" and main[0][2] == "r9d, r9d"
      and main[0][3] == "m_count" and main[0][4] == ".?AV?$PAnnotationWithValue@I@Phyre@@" and main[0][5] == "0x7fffffff",
      "69 of 70 sites: key 02CF8570, value type from 00630180, +0x28 = 0, on a member named m_count, derived "
      "PAnnotationWithValue<unsigned int>, value 0x7FFFFFFF")
# F3 - the key 02CF8570 is a {name, 0} object named "WriteMask" (001641C0 -> 006B66F0); 00630180 returns 01F2E5A0, whose
#      vtable (installed by 006315B0 at 00631683) is PTypeDefault<unsigned int>
check("F3", txt(0x001641C4).startswith("lea rdx, [rip") and T.cstr(0x00D56508) == "WriteMask" and txt(0x001641D2) == "call 0x6b66f0"
      and txt(0x006B66F0) == "mov qword ptr [rcx], rdx" and txt(0x006301A7).startswith("lea rax, [rip")
      and target(next(R.md.disasm(R.at(0x006301A7, 16), 0x006301A7, 1))) == 0x01F2E5A0
      and T.rtti_class(0x00D311B0) == ".?AV?$PTypeDefault@I@Phyre@@" and txt(0x00631683) == "mov qword ptr [rip + 0x18fcf16], rax",
      "key = \"WriteMask\"; value type = PTypeDefault<unsigned int>")
# F4 - attach: 006B67D0(list head, annotation) links the annotation's node (+8) into the head; in 005B4E00 the head is
#      02CB3C98 = the member 02CB3C60 (registered by 00632960 as "m_count") + 0x38
check("F4", [txt(a) for a in (0x006B67D0, 0x006B67D3, 0x006B67D7, 0x006B67DA, 0x006B67DE, 0x006B67E1)] ==
      ["mov rax, qword ptr [rcx]", "add rdx, 8", "mov qword ptr [rdx], rax", "mov qword ptr [rdx + 8], rcx", "mov qword ptr [rcx], rdx",
       "mov qword ptr [rax + 8], rdx"] and txt(0x005B5045) == "call 0x6b67d0" and txt(0x005B4F9A) == "call 0x632960"
      and target(next(R.md.disasm(R.at(0x005B4F93, 16), 0x005B4F93, 1))) == 0x02CB3C60
      and target(next(R.md.disasm(R.at(0x005B503E, 16), 0x005B503E, 1))) == 0x02CB3C98,
      "the annotation is linked into the annotated member's list at member + 0x38")
print("FAILS %d" % fails)
