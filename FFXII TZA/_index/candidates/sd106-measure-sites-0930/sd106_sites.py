"""sd106_sites.py - SD-106: what the five 002B3280 sites display (OPUS, 2026-09-30). Static, the certified image, via
Database/Tools/analysis-kit/gfz-scripts/retool.py.
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


# M1 - 002B3280(element, 0, text, r9d, &w, &h, 0) forwards to the kind-0 builder 002B32D0 with the two out-pointers; the
#      five sites are the only callers
cal = sorted(c["calls"].get(0x002B3280, ()))
check("M1", cal == [(0x00227EE0, 0x00227FE3), (0x00241D40, 0x00241DEB), (0x0057C140, 0x0057C1E2), (0x0057C480, 0x0057C58B),
                    (0x0057C480, 0x0057C5DB)] and txt(0x002B32B6) == "call 0x2b32d0",
      "five sites; 002B3280 forwards to 002B32D0")
# M2 - 00227EE0: the text is the message argument's +8, built in the window's element +0xC0, and the returned size
#      centres it on the screen: x = (01E0C1D8 - w) / 2, y = (01E0C1DC - h) / 2
check("M2", txt(0x00227FB3) == "mov r8, qword ptr [rdx + 8]" and txt(0x00227FC5) == "lea rcx, [rsi + 0xc0]"
      and txt(0x00227FF6).endswith("0x1be41dc]") and txt(0x00227FFF) == "sub eax, dword ptr [rsp + 0x50]"
      and txt(0x00228006) == "sar eax, 1" and txt(0x0022800A).endswith("0x1be41cc]") and txt(0x00228010) == "sub eax, dword ptr [rsp + 0x58]",
      "00227EE0: a one-line message, measured and centred on screen")
# M3 - 00241D40: the confirm dialog's caption buffer +0x1B0 (a leading byte 4 is supplied when it is empty), built in
#      element +0xE0; the width is raised to the minimum at 01E0C0D4
check("M3", txt(0x00241DAB) == "cmp byte ptr [rsi + 0x1b0], 0" and txt(0x00241DB4) == "mov byte ptr [rsi + 0x1b0], 4"
      and txt(0x00241DC6) == "lea r8, [rsi + 0x1b0]" and txt(0x00241DD2) == "lea rcx, [rsi + 0xe0]"
      and txt(0x00241DFE) == "mov ecx, dword ptr [rbp - 0x31]" and txt(0x00241E07).startswith("cmovl ecx, dword ptr [rip"),
      "00241D40: the confirm caption, measured, width clamped to a minimum")
# M4 - 0057C140: adds one choice to the dialog (string pointer into the table at +0 by index, id word +0x5B8, flag
#      +0x5BC, count +0x636), measures it in a frame element, and widens the list: w + 2 * [01E0CDC0] against the rows'
#      widths
check("M4", txt(0x0057C1C3) == "or dword ptr [rsi + rbx*8 + 0x5bc], 1" and txt(0x0057C1CB) == "mov word ptr [rsi + rbx*8 + 0x5b8], bp"
      and txt(0x0057C1D3) == "inc byte ptr [rsi + 0x636]" and txt(0x0057C1D9) == "mov r8, qword ptr [rsi + rdi*8]"
      and txt(0x0057C19B) == "lea rcx, [rsp + 0x50]" and txt(0x0057C1E7) == "mov r10d, dword ptr [rsp + 0x40]"
      and txt(0x0057C207) == "lea ecx, [r9 + r9]" and txt(0x0057C21D) == "cmovg r10d, eax",
      "0057C140: one confirm-dialog choice line, measured to widen the list")
# M5 - 0057C480: the caption again (buffer +0x1B0, element +0xE0), on two paths - after a 0x400-byte clear - and the
#      size read back ([rbp+0x58], [rbp+0x50])  (narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's
#      auditspec-review-sd106-0930 item 4: the 002B3400 lines this check tests are the neighbouring branch, which
#      does not reach 002B3280)
check("M5", txt(0x0057C519) == "lea rdx, [rsi + 0x1b0]" and txt(0x0057C520) == "call 0x2b3400" and txt(0x0057C576) == "lea r8, [rsi + 0x1b0]"
      and txt(0x0057C5A6) == "mov r8d, 0x400" and txt(0x0057C5AC) == "call 0x861ec0" and txt(0x0057C5BF) == "lea r8, [rsi + 0x1b0]"
      and txt(0x0057C5D4) == "lea rcx, [rsi + 0xe0]" and txt(0x0057C59E) == "mov ecx, dword ptr [rbp + 0x58]",
      "0057C480: the confirm caption re-measured on two paths")
print("FAILS %d" % fails)
