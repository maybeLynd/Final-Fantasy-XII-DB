"""ov42_check.py - the byte facts OPUS re-read before consuming FABLE's routed OV-42 type-store text (OPUS, 2026-10-02).
Rejecting regression over the shipping image through retool.py; last line 'FAILS n'."""
import os
import re
import subprocess
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
RETOOL = os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts", "retool.py")
fails = 0


def dis(addr, n):
    out = subprocess.run([sys.executable, "-B", RETOOL, "dis", addr, "--n", str(n)], capture_output=True, text=True,
                         cwd=os.path.dirname(RETOOL)).stdout
    rows = [l.split(None, 1) for l in out.splitlines() if re.match(r"^[0-9A-F]{8}\s", l)]
    return [(a, " ".join(i.split(";")[0].split())) for a, i in rows]


def at(rows, base, off):
    k = "%08X" % (int(base, 16) + off)
    return next((i for a, i in rows if a == k), "")


def check(ok, msg):
    global fails
    print(("PASS  " if ok else "FAIL  ") + msg)
    fails += 0 if ok else 1


A, B = dis("00306760", 260), dis("00306BD0", 140)
for base, rows, stride, ref in (("00306760", A, 0x152, 0x13F), ("00306760", A, 0xC7, 0xB4), ("00306BD0", B, 0xAC, 0x99)):
    check(at(rows, base, stride) == "movzx ecx, word ptr [rax + 8]", "%s + 0x%X reads the u16 stride +0x08" % (base, stride))
    check(at(rows, base, ref) == "mov ecx, dword ptr [rax + 0xc]", "%s + 0x%X reads the array ref +0x0C" % (base, ref))
    seq = [i for a, i in rows if int(base, 16) + ref <= int(a, 16) <= int(base, 16) + stride + 6]
    check(any(i == "call 0x20e600" for i in seq) and sum(i.startswith("mov rax, qword ptr [rip") for i in seq) >= 1
          and any(i.startswith("div ") for i in seq) and not any(i.startswith(("test ecx", "jecxz")) for i in seq),
          "%s: lookup call, a second descriptor load, an unguarded unsigned div" % base)
check(at(A, "00306760", 0x174).startswith("mov dword ptr [rip"), "00306760 + 0x174 stores the queue DWORD (022C2178)")

R, G = dis("0031B860", 40), dis("00387090", 60)
check(R[-1][0] == "0031B8B2" and R[-1][1] == "ret", "0031B860 is 83 B")
check(at(R, "0031B860", 0x9) == "test rcx, rcx" and at(R, "0031B860", 0xE) == "xor eax, eax", "a NULL query returns 0 first")
check(at(R, "0031B860", 0x32) == "cmp qword ptr [rax + 0x698], rdi" and at(R, "0031B860", 0x44) == "jl 0x31b886",
      "first index-order match on +0x698, signed loop compare")
check(G[-1][0] == "00387124" and G[-1][1] == "ret", "00387090 is 149 B")
check(sum(i == "call 0x31b860" for a, i in G) == 2, "the getter calls the resolver twice (O1, O2)")
check(at(G, "00387090", 0x34).startswith("mov qword ptr [rip"), "O1 is stored to 02EBF188")
check(at(G, "00387090", 0x88) == "movzx eax, word ptr [rax + 0x714]", "the O2 +0x714 read is reachable with RAX = 0")
check(at(G, "00387090", 0x7E) == "movzx eax, word ptr [rbx + 0x10]", "00387090 + 0x7E reads record +0x10 (the 0x9F swap)")
print("FAILS %d" % fails)
