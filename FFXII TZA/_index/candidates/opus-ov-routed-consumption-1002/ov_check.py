"""ov_check.py - the byte facts OPUS re-read before consuming FABLE's routed OV-10 / OV-16 / OV-42 text (OPUS, 2026-10-02).

Rejecting regression: each check decodes the shipping image through retool.py and fails if the reading the pages now
state were false. Last line: 'FAILS n'.
"""
import os
import re
import subprocess
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
RETOOL = os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts", "retool.py")
fails = 0


def dis(addr, n=130):
    out = subprocess.run([sys.executable, "-B", RETOOL, "dis", addr, "--n", str(n)], capture_output=True, text=True,
                         cwd=os.path.dirname(RETOOL)).stdout
    return [l.split(None, 1) for l in out.splitlines() if re.match(r"^[0-9A-F]{8}\s", l)]


def check(ok, msg):
    global fails
    print(("PASS  " if ok else "FAIL  ") + msg)
    fails += 0 if ok else 1


def at(rows, a):
    return next((" ".join(r[1].split()) for r in rows if r[0] == a), "")


rem = dis("003DB2A0")
check(at(rem, "003DB326") == "mov edx, esi", "003DB2A0+0x86: every pass loads the removed index (mov edx, esi)")
check(at(rem, "003DB32F") == "call 0x3db550" and at(rem, "003DB33F") == "jne 0x3db326",
      "the loop calls 003DB550 and jumps back to +0x86 with edx reloaded from esi (no walk)")
check(at(rem, "003DB2B8") == "mov eax, 1", "index 0xFF returns 1")
check(at(rem, "003DB37D") == "call 0x3dc0d0" and at(rem, "003DB3F0") == "call 0x3db650"
      and at(rem, "003DB3F9") == "mov byte ptr [rbx + 0x60], sil",
      "the end notification precedes the free-list relink and the +0x60 publish")
check(at(rem, "003DB382") == "movzx eax, byte ptr [rdi + 0x12]", "the notification's result is discarded")
check(at(rem, "003DB34D") == "jns 0x3db366" and at(rem, "003DB371") == "cmp byte ptr [rdi + 0x10], 3",
      "the gate needs a non-negative channel and mode 3")
check(at(rem, "003DB2EF") == "and r14d, 1" and at(rem, "003DB402") == "mov eax, r14d", "removal returns +0x12 bit 0")

leaf = dis("003DB550", 12)
check(not any(r[1].startswith(("call", "mov qword", "mov byte", "mov dword", "mov word")) for r in leaf),
      "003DB550 is a pure index leaf (no call, no store)")

ntf = dis("003DBCF0", 30)
check(at(ntf, "003DBD11") == "mov eax, 3" and at(ntf, "003DBD32") == "mov eax, 2"
      and not any(r[1].startswith("call") for r in ntf if r[0] < "003DBD47"),
      "003DBCF0 refuses on the count first (3), then the free head (2), with no call before either")

wrap, alloc, bridge = dis("0030CFB0", 80), dis("0030D070", 90), dis("00348330", 60)
check(wrap[-1][0] == "0030D068" and wrap[-1][1].startswith("ret"), "0030CFB0 is 185 B")
check(alloc[-1][0] == "0030D154" and not any(r[1].startswith("call") for r in alloc), "0030D070 is 229 B, no calls")
check(at(alloc, "0030D14F") == "mov word ptr [rcx + 0x1c], r10w", "the slot word +0x1C is stored last")
check(bridge[-1][0] == "003483D0" and bridge[-1][1].startswith("jmp"), "00348330 is 165 B (tail jmp at +0xA0)")
check(at(bridge, "0034838A") == "call 0x309c00" and at(bridge, "003483A9") == "mov ecx, dword ptr [rbx]"
      and at(bridge, "003483B1") == "mov ecx, dword ptr [rsi]", "the bridge reads both out-references after the writer")

sys.path.insert(0, os.path.dirname(RETOOL))
import kit_paths as KP  # noqa: E402
import pefile  # noqa: E402
pe = pefile.PE(KP.EXE if hasattr(KP, "EXE") else next(getattr(KP, n) for n in dir(KP) if "EXE" in n.upper()),
               fast_load=True)
s = next(x for x in pe.sections if x.Name.rstrip(b"\0") == b".data")
lo = pe.OPTIONAL_HEADER.ImageBase + s.VirtualAddress
check(lo + s.SizeOfRawData <= 0x02EBF138 < lo + s.Misc_VirtualSize, "02EBF138 lies in .data's zero-filled virtual tail")

print("FAILS %d" % fails)
