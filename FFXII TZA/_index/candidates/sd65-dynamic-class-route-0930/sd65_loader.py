"""sd65_loader.py - when the cluster loader 0059AC00 takes the dynamic route (OPUS, 2026-09-30; register SD-65).
Asserts over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py. The corpus side is
sd65_census.py (output sd65_census.out).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c = T.R, T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# L1 - one caller each: 00632B30 (PClassDataMemberDynamic) only from 006393A0, and 006393A0 only from 0059AC00 at 0059AEA7
cb = sorted(c["calls"].get(0x00632B30, ()))
ca = sorted(c["calls"].get(0x006393A0, ()))
check("L1", cb == [(0x006393A0, 0x0063942C)] and ca == [(0x0059AC00, 0x0059AEA7)],
      "00632B30 <- 006393A0 @0063942C <- 0059AC00 @0059AEA7, nothing else")
# L2 - the class pass: for each 0x30-byte class entry with no native descriptor (+0x10 == 0) whose file record (+8) has
#      bit 0 of +0x1C set, the loader reads the record's +0 as a 1-based super-class index and builds a 0x140-byte
#      dynamic descriptor (00632E80) under that super class; the error strings name it
check("L2", txt(0x0059AC84) == "cmp qword ptr [r14 + rbp + 0x10], 0" and txt(0x0059AC90) == "mov rax, qword ptr [r14 + rbp + 8]"
      and txt(0x0059AC95) == "test byte ptr [rax + 0x1c], 1" and txt(0x0059AC9F) == "mov r8d, dword ptr [rax]"
      and txt(0x0059ACA7) == "lea eax, [r8 - 1]" and txt(0x0059AD27) == "mov ecx, 0x140" and txt(0x0059AD49) == "call 0x632e80"
      and T.cstr(0x00D27610) == "Unable to find super class %d (of %d) when creating dynamic class '%s'\n"
      and T.cstr(0x00D27658) == "Invalid super class '%s' when creating dynamic class '%s'\n"
      and T.cstr(0x00D27698) == "Namespace already includes the specified class: '%s'\n",
      "dynamic class: record +0x1C bit 0 set and no native descriptor; record +0 = 1-based super-class index")
# L3 - an entry that still has no descriptor with the bit set fails the load with 0x13
check("L3", txt(0x0059ADD7) == "cmp qword ptr [rdx + rax*8 + 0x10], 0" and txt(0x0059ADE4) == "test byte ptr [rax + 0x1c], 1"
      and txt(0x0059ADF2) == "mov eax, 0x13",
      "a flagged class left without a descriptor returns 0x13")
# L4 - the member pass: only in classes with a descriptor, bit 0 of +0x1C and a non-zero +0x0C member count; each
#      0x38-byte member entry with no native member (+0x10 == 0) gets a dynamic one (006393A0), flagged from the file
#      member record's +0x10 bit 1; an unresolved type logs 'Type not found for "%s::%s"'
check("L4", txt(0x0059AE17) == "mov r14, qword ptr [r15 + 0x10]" and txt(0x0059AE28) == "test byte ptr [rax + 0x1c], 1"
      and txt(0x0059AE32) == "mov ecx, dword ptr [rax + 0xc]" and txt(0x0059AE45) == "cmp qword ptr [rsi + rbx + 0x10], 0"
      and txt(0x0059AE57) == "mov r9d, dword ptr [rax + 0x10]" and txt(0x0059AE5B) == "and r9d, 2"
      and txt(0x0059AEAC) == "mov qword ptr [rsi + rbx + 0x10], rax" and txt(0x0059AEB6) == "add rsi, 0x38"
      and T.cstr(0x00D276D0) == 'Type not found for "%s::%s"\n',
      "dynamic members only in flagged classes, for file members with no native member")
print("FAILS %d" % fails)
