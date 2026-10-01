"""uq363_icon_record.py - UQ-363: who writes the kind-3 glyph-run record's +0x0C, and what selects its group
(FABLE, Claude Opus 5.5, 2026-09-26; first read by a delegated read-only pass, every step re-checked here).

  I1 the group selector is the sheet header's own u16 at +0x14, not a record or tag field. The draw arm reads
     `movzx eax, word [rcx+0x14]` then `movzx r8d, word [rcx+rax*2+0x14]` (0053E29C, 0053E2A7) and adds the record's
     u16 at +0x0C (0053E2AD, [rsi-0xC] with rsi = record + 0x18). The builder uses the same self-index (0053F22D,
     0053F232).
  I2 the writer. 0053F0D0 takes the window singleton [02CA8A80] (0053F0D6), caps the count at 0x800 (0053F0FD) and
     dispatches its op through the jump table at 0053F3B0. The op-6 arm builds the kind-3 record: +0x00 = [02CA8A88]
     (0053F206), +0x18 = 3 (0053F209), +0x10 = pen y (0053F214), and +0x0C = its third argument (0053F218).
  I3 the op-6 route is a script verb: 00511A40 pops an int (00511A47 call 00267E10), sets edx = 0, r8d = the value and
     ecx = 6, and tail-jumps to 0053F0D0 (00511A4C..00511A58).
  I4 the image object [02CA8A88] is created in 0053EB90 from the resource named "sf_logo_c" (a lea of the string, then
     the store to 02CA8A88), so kind-3 records are staff-roll logo images.
  I5 the {i} tag arm of the tag interpreter 00366110 ('i' -> 0036618D in the letter table at 00366638) only advances the
     cursor ([rsi] = tag + 3, 003661A9): the tag's bytes are stored nowhere.
     Control: the same test on the record builder's op-6 arm finds its stores.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
def txt(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in ins(a, size)}
def rip(x):
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
def cstr(v):
    o = off(v); return d[o:d.find(b"\0", o)].decode("latin-1")
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
D = txt(0x53E290, 0x40); Bd = txt(0x53F220, 0x20)
check("I1 the group selector is the header's own u16 [hdr+0x14]; the record adds its +0x0C",
      D.get(0x53E29C) == "movzx eax, word ptr [rcx + 0x14]" and D.get(0x53E2A7) == "movzx r8d, word ptr [rcx + rax*2 + 0x14]"
      and D.get(0x53E2AD) == "movzx eax, word ptr [rsi - 0xc]"
      and Bd.get(0x53F22D) == "movzx eax, word ptr [r9 + 0x14]" and Bd.get(0x53F232) == "movzx edx, word ptr [r9 + rax*2 + 0x14]")
F = ins(0x53F0D0, 733); T = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in F}
jt = [0x53F0D0 + 0 for _ in range(0)]
tbl = [struct.unpack_from("<i", d, off(0x53F3B0) + 4 * k)[0] for k in range(14)]
arm6 = BASE + tbl[5] if tbl[5] > 0 else None
check("I2 0053F0D0: window singleton, 0x800 cap, and the op-6 arm writes +0x00, +0x18 = 3, +0x10, +0x0C = arg3",
      rip(next(x for x in F if x.address == 0x53F0D6)) == 0x2CA8A80 and T.get(0x53F0FD) == "cmp r10d, 0x800"
      and T.get(0x53F206) == "mov qword ptr [r11], rcx" and T.get(0x53F209) == "mov byte ptr [r11 + 0x18], 3"
      and T.get(0x53F214) == "mov dword ptr [r11 + 0x10], eax" and T.get(0x53F218) == "mov word ptr [r11 + 0xc], r8w"
      and arm6 is not None and arm6 <= 0x53F206 < arm6 + 0x40,
      "table slot 5 (op 6) -> %s" % ("%08X" % arm6 if arm6 else tbl[5]))
V = txt(0x511A40, 0x20)
check("I3 00511A40 pops an int and tail-calls 0053F0D0 with op 6, edx 0, r8d = the value",
      V.get(0x511A47) == "call 0x267e10" and V.get(0x511A4C) == "xor edx, edx" and V.get(0x511A4E) == "mov r8d, eax"
      and V.get(0x511A51) == "lea ecx, [rdx + 6]" and V.get(0x511A58) == "jmp 0x53f0d0")
G = ins(0x53EB90, 0x200)
store = [x for x in G if x.mnemonic == "mov" and rip(x) == 0x2CA8A88 and x.op_str.endswith("rax")]
names = [cstr(rip(x)) for x in G if x.mnemonic == "lea" and rip(x) and off(rip(x)) and 0xD00000 <= rip(x) < 0xE00000]
check("I4 0053EB90 creates [02CA8A88] from the resource named sf_logo_c",
      store and "sf_logo_c" in names and any(x.address < store[0].address for x in G if x.mnemonic == "lea" and rip(x) and off(rip(x)) and cstr(rip(x)) == "sf_logo_c"),
      "store at %s; strings %s" % (["%08X" % x.address for x in store], names))
def mem_writes(a, stop_mn, size=0x40):
    out = []
    for x in ins(a, size):
        if any(op.type == X86_OP_MEM for op in x.operands[:1]) and x.mnemonic in ("mov", "movzx", "add", "sub", "or", "and", "inc", "dec", "movss", "movsd", "movups", "movaps"):
            if x.operands and x.operands[0].type == X86_OP_MEM: out.append(x.address)
        if x.mnemonic == stop_mn: break
    return out
P = txt(0x36616E, 0x20)
slot_i = BASE + struct.unpack_from("<I", d, off(0x366638) + 4 * (ord("i") - ord("a")))[0]
I = ins(0x36618D, 0x30)
end = next((x for x in I if x.mnemonic == "jmp"), None)
W = mem_writes(0x36618D, "jmp"); A = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in I}
check("I5 the tag table sends 'i' to 0036618D; that arm's only write is the cursor advance [rsi] = tag + 3, so the tag's "
      "bytes are stored nowhere; control: the op-6 arm makes several writes",
      P.get(0x36616E) == "sub ecx, 0x61" and P.get(0x366180) == "mov ecx, dword ptr [r15 + rax*4 + 0x246638]" and slot_i == 0x36618D
      and end is not None and W == [0x3661A9] and A.get(0x3661A5) == "lea rax, [rdx + 3]" and A.get(0x3661A9) == "mov qword ptr [rsi], rax"
      and len(mem_writes(0x53F1EA, "jmp", 0xC0)) >= 4,
      "'i' -> %08X; arm writes %s; op-6 arm writes %d" % (slot_i, ["%08X" % a for a in W], len(mem_writes(0x53F1EA, "jmp", 0xC0))))
print("FAILS", fails)
sys.exit(1 if fails else 0)
