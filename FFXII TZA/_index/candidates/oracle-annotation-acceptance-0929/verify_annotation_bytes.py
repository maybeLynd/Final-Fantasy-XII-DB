"""verify_annotation_bytes.py - SWE2-ORACLE's owner check of FABLE's three dated annotations (b17be47ac), read from the
shipping image (SWE2-ORACLE, run by OPUS's Claude subagent, 2026-09-29).

It decodes the instructions each annotation rests on and derives the annotated fact from the decoded operands, then
asserts that the fact contradicts the superseded sentence (the negative control: the old reading must be rejected by
the same derivation).

  A189  0030B6A0's reset tail: `lea rax,[rcx+0x57C8]; mov ecx,8` then a loop of qword stores advancing 0x40 per turn
        -> zeroed bytes = turns * stores * 8; then `lea rax,[r10+0x59C8]; mov ecx,0x80; and byte ptr [rax],0xF8`
        advancing 1 -> ANDed bytes. Expected 512 zeroed at +0x57C8, 128 ANDed with 0xF8 at +0x59C8.
        Old reading "8 dwords" (32 bytes) must be rejected.
  A086  0016D6A0 is C2 00 00 (ret 0, 3 bytes) + int3 padding; 0030E360 selects it at 0030E710..0030E727:
        `lea rcx,->0046A800; test edi,edi; lea rax,->0016D6A0; cmovne rax,rcx; ...; call rax`, with edi loaded from
        [rsp+0x44] (0030E6E3), written at 0030E3C2..0030E3CB as setbe((edx-3) <= 1). So 0016D6A0 is the shipped
        target for every mode except 3 and 4. Old reading "stand-in" / "single-byte ret" must be rejected.
  A230  00325A00: `test ecx,0x7FFFFFFE; jne T; cmp ecx,1; jne R; T: jmp 003DC780; R: ret` -> skip set over a probe
        vector derived from the decoded immediates. Expected skips exactly {0, 0x80000000, 0x80000001}; ecx=1 reaches
        the tail. Old reading "calls 3DC780 only when ecx not in {0,1}" must be rejected.

Static decode only: it says what the bytes are, not what 003DC780 does or which values reach the guard at runtime.
Usage: python verify_annotation_bytes.py [--exe PATH]   (default: the kit image; its sha256 is checked)
"""
import hashlib, os, subprocess, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
from disasm_fn import Image  # noqa: E402

SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
exe = sys.argv[sys.argv.index("--exe") + 1] if "--exe" in sys.argv else os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
raw = open(exe, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "not the authority image"
img = Image(exe)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def ck(tag, ok, msg):
    global fails
    fails += not ok
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))


def dis(va, n):
    return [(i.address, i.mnemonic, i.op_str) for i in cs.disasm(img.read(va, n), va)]


def imm(s):
    return int(s.split(",")[-1].strip(), 0)


# ---- A189 ----
t = dis(0x30B702, 0x5B)
m = {a: (mn, op) for a, mn, op in t}
z_base = m[0x30B702]
z_turns = imm(m[0x30B709][1])
body = [x for x in t if 0x30B710 <= x[0] < 0x30B733]
stores = [x for x in body if x[1] == "mov" and x[2].startswith("qword ptr [rax") and x[2].endswith(", r11")]
step = [x for x in body if x[1] == "lea" and x[2] == "rax, [rax + 0x40]"]
zeroed = z_turns * len(stores) * 8
a_base, a_n, a_op = m[0x30B739], imm(m[0x30B740][1]), m[0x30B750]
ok189 = (z_base == ("lea", "rax, [rcx + 0x57c8]") and len(step) == 1 and zeroed == 512 and len(stores) * 8 == 0x40
         and a_base == ("lea", "rax, [r10 + 0x59c8]") and a_n == 0x80 and a_op == ("and", "byte ptr [rax], 0xf8")
         and m[0x30B753] == ("lea", "rax, [rax + 1]"))
ck("A189", ok189, "zeroed %d bytes at +0x57C8 (%d turns x %d qword stores), ANDed %d bytes with 0xF8 at +0x59C8"
   % (zeroed, z_turns, len(stores), a_n))
ck("A189-old-rejected", zeroed != 8 * 4, "old '8 dwords' = 32 bytes vs decoded %d" % zeroed)

# ---- A086 ----
b = img.read(0x16D6A0, 16)
ret3 = b[:3] == b"\xC2\x00\x00" and b[3:] == b"\xCC" * 13
s = {a: (mn, op) for a, mn, op in dis(0x30E3C0, 0x10) + dis(0x30E6E3, 0x8) + dis(0x30E710, 0x19)}
sel = (s.get(0x30E3C2) == ("lea", "ecx, [rdx - 3]") and s.get(0x30E3C5) == ("cmp", "ecx, 1")
       and s.get(0x30E3C8) == ("setbe", "al") and s.get(0x30E3CB) == ("mov", "dword ptr [rsp + 0x44], eax")
       and s.get(0x30E6E3) == ("mov", "edi, dword ptr [rsp + 0x44]")
       and s.get(0x30E710) == ("lea", "rcx, [rip + 0x15c0e9]") and 0x30E717 + 0x15C0E9 == 0x46A800
       and s.get(0x30E717) == ("test", "edi, edi")
       and s.get(0x30E719) == ("lea", "rax, [rip - 0x1a1080]") and 0x30E720 - 0x1A1080 == 0x16D6A0
       and s.get(0x30E720) == ("cmovne", "rax, rcx") and s.get(0x30E727) == ("call", "rax"))
ck("A086", ret3 and sel, "0016D6A0 = C2 00 00 + 13 x CC; 0030E727 calls 0016D6A0 unless (mode-3)<=1 (mode 3/4 -> 0046A800)")
import json  # noqa: E402
bj = json.load(open(os.path.join(REPO, "Database", "FFXII TZA", "_experiments", "evidence", "status-write-execution",
                                 "bodies.json"), encoding="utf-8"))
pin = [e for e in bj["real_bodies_executed"] if e["va"].upper() == "0X16D6A0"]
pin_len = [n for n in range(1, 17) if pin and hashlib.sha256(img.read(0x16D6A0, n)).hexdigest() == pin[0]["sha256"]]
ck("A086-old-rejected", ret3 and sel and pin_len == [1],
   "bodies.json pins %s byte(s) of the 3-byte instruction; the selector names 0016D6A0 for modes other than 3 and 4, "
   "so 'single-byte ret' and 'stand-in' are both rejected" % pin_len)

# ---- A230 ----
g = dis(0x325A00, 0x13)
shape = [(mn, op) for _, mn, op in g]
want = [("test", "ecx, 0x7ffffffe"), ("jne", "0x325a0d"), ("cmp", "ecx, 1"), ("jne", "0x325a12"), ("jmp", "0x3dc780"), ("ret", "")]
mask, one = imm(g[0][2]), imm(g[2][2])
probe = [0, 1, 2, 3, mask, 0x7FFFFFFF, 0x80000000, 0x80000001, 0x80000002, 0xFFFFFFFE, 0xFFFFFFFF]
skips = sorted(v for v in probe if not (v & mask) and v != one)
ck("A230", shape == want and skips == [0, 0x80000000, 0x80000001], "skips %s; ecx=1 -> 003DC780" % [hex(v) for v in skips])
old = sorted(v for v in probe if v in (0, 1))
ck("A230-old-rejected", old != skips and 1 not in skips, "old skip set %s vs decoded %s" % ([hex(v) for v in old], [hex(v) for v in skips]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
