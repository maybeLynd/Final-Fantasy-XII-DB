"""sd192_readers.py - SD-192: does each reader of controller +0x14F bit 0 ('attached to another actor's bone', BV-2)
refuse movement on it? (OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ = T.R, T.sizes()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def epilogue(f, a):
    """True if the code at a (inside f) reaches the function's ret without a call or a store to memory."""
    for i in R.md.disasm(R.at(a, 0x40), a):
        if i.mnemonic == "ret" or (i.mnemonic == "jmp" and not i.op_str.startswith("0x")):
            return True
        if i.mnemonic == "call" and i.op_str != "0x808c40":   # 00808C40 = the stack-cookie check
            return False
        if i.mnemonic.startswith("mov") and i.op_str.startswith(("dword ptr [r", "qword ptr [r", "byte ptr [r")) and "rsp" not in i.op_str:
            return False
    return False


# the census: every `test byte [reg+0x14F], 1` in the listed bodies (sweep result, 2026-09-30):
#   selectors 0025B637 / 0025B76F, flat selector 00267286, attach guard 002E274A, integrator side 002E506A / 002E5776 /
#   002E602C / 002E634B / 002EA816, presentation 003B7934 (+ 003B7812's register-mask form) - the last two are BV-2's
#   presentation-visibility writers (2026-09-16 narrowing), the attach guard is 002E26F0 itself.
READERS = [  # (function, test site, branch site, branch target, what the skipped body does)
    (0x0025B600, 0x0025B637, 0x0025B63E, 0x0025B735, "field-pass selector: the flat-motion test for the current field actor"),
    (0x0025B740, 0x0025B76F, 0x0025B776, 0x0025B7CD, "field-pass selector: the same test, tail-calling 00238B20(1) when it passes"),
    (0x00267260, 0x00267286, 0x0026728D, 0x00267272, "Movement_ActorUsesFlatMotion: returns 0 (no flat motion)"),
    (0x002E5030, 0x002E506A, 0x002E5071, 0x002E5164, "Movement_UpdateActorFrame: the whole per-frame movement update"),
    (0x002E5750, 0x002E5776, 0x002E577D, 0x002E5951, "the facing integrator (SD-190's function): the heading update"),
    (0x002E6000, 0x002E602C, 0x002E603F, 0x002E6071, "posts the actor's position (with 00263910's height term) through 003EC3D0"),
    (0x002E6330, 0x002E634B, 0x002E6352, 0x002E639F, "the movement-body step under actor +9 bit 6 (002E9FE0 ...)"),
    (0x002EA7F0, 0x002EA816, 0x002EA81D, 0x002EA858, "returns 0 before reading the movement body's +0xF0"),
]
ok_all = True
for f, t, b, tgt, what in READERS:
    ok = (txt(t) in ("test byte ptr [rax + 0x14f], 1", "test byte ptr [rcx + 0x14f], 1", "test byte ptr [rbx + 0x14f], 1")
          and txt(b) == "jne 0x%x" % tgt and (epilogue(f, tgt) or tgt == 0x00267272))
    ok_all &= ok
    print("      %s %08X: bit 0 set -> %08X %s | skipped: %s" % ("ok " if ok else "BAD", t, tgt, "(epilogue)" if ok else "", what))
check("R1", ok_all, "all eight readers branch on bit 0 to their exit, skipping their movement work")
# R2 - two of them return a refusal value: the flat selector's exit is `xor eax, eax` then ret; 002EA7F0 zeroes edi on
#      entry and returns it
check("R2", txt(0x00267272) == "xor eax, eax" and txt(0x002EA7FA) == "xor edi, edi" and txt(0x002EA858) == "mov eax, edi",
      "00267260 and 002EA7F0 return 0 when attached")
print("FAILS %d" % fails)
