"""sign_check.py - OPUS (Claude Opus 5.5), 2026-09-28, the non-author check behind OPUS's signature on UQ-212 as
OUT OF EVIDENCE BOUNDARY (FABLE-REQ-OPUS-SIGN-OEB-UQ212). STATIC.

FABLE's uq212_no_names.py shows the page's twelve functions reference no string, and are no vtable slot (so no RTTI
name). This check widens the negative to the DATA path, the one admitted route FABLE's record does not test: the
0x60-byte records arrive from a loaded resource, whose container could have named them.

  K1 the loader 002F6AB0 walks a section directory of packed u32 entries: kind = entry >> 24 (a byte, tested
     against 0x21 at 002F6CC3), offset = (entry AND 0xFFFFFF) << 4 (002F6C9A / 002F6CA1), dispatched through a 34-entry
     jump table at 002F72F8. A section is selected by a NUMBER; no string takes part.
  K2 kind 0x0E is the texture-record bank: its case (002F6E97) builds the 0x20-byte bank object with 00467D20 from
     the section data and stores it at object +0x150, which 002F7380 walks (+8 = records, stride 0x60). Kind 0x0C
     (002F6E7C) is its consumer, 00468160 with +0x150.
  K3 FABLE's uq212_no_names.py still passes (N1-N3).
Exit 1 on any failed check.
"""
import hashlib, os, struct, subprocess, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
d = open(os.path.join(DB, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image")  # guard per ASTRA-CONTRA-OPUS-MATRIX-CONSUMER-IDENTITY
    sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]
n, opt = struct.unpack_from("<H", d, pe + 6)[0], struct.unpack_from("<H", d, pe + 20)[0]
S = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
fails = 0


def off(v):
    for vs, va, rs, ro in S:
        if B + va <= v < B + va + rs:
            return v - B - va + ro


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


md = Cs(CS_ARCH_X86, CS_MODE_64)
ins = {i.address: (i.mnemonic, i.op_str) for i in md.disasm(d[off(0x2F6AB0):off(0x2F6AB0) + 0x480], 0x2F6AB0)}
k1 = (ins.get(0x2F6C9A) == ("and", "r14d, 0xffffff") and ins.get(0x2F6CA1) == ("shl", "r14, 4")
      and ins.get(0x2F6CBD) == ("sar", "ecx, 0x18") and ins.get(0x2F6CC3) == ("cmp", "eax, 0x21")
      and ins.get(0x2F6CCC, ("", ""))[1] == "ecx, dword ptr [r13 + rax*4 + 0x1d72f8]")
check("K1", k1, "directory entry = kind<<24 or offset>>4; kind byte bounded by 0x21; jump table at 002F72F8")
tab = {k: B + struct.unpack_from("<I", d, off(0x2F72F8 + 4 * k))[0] for k in range(0x22)}
k2 = (tab[0x0E] == 0x2F6E97 and tab[0x0C] == 0x2F6E7C and ins.get(0x2F6EB4) == ("call", "0x467d20")
      and ins.get(0x2F6EBB) == ("mov", "qword ptr [rsi + 0x150], rdi")
      and ins.get(0x2F6E86) == ("mov", "rdx, qword ptr [rsi + 0x150]") and ins.get(0x2F6E8D) == ("call", "0x468160"))
check("K2", k2, "kind 0x0E -> %08X builds the bank (00467D20) into +0x150; kind 0x0C -> %08X reads it"
      % (tab[0x0E], tab[0x0C]))
r = subprocess.run([sys.executable, os.path.join(HERE, "..", "uq212-class3", "uq212_no_names.py")],
                   capture_output=True, text=True)
check("K3", r.returncode == 0 and "FAILS 0" in r.stdout, "uq212_no_names.py: " + r.stdout.strip().splitlines()[-1])
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
