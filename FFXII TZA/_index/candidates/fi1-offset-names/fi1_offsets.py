"""fi1_offsets.py - FI-1: the actor storage record's touched offsets that had no store row, named (FABLE, Claude Opus 5.5,
2026-09-27). Static.

  N1 the premise, re-measured: the field-map page flags 34 offsets "*not in the store*" (not 41), and every one now has
     an ActorStorageRecord row in _types/fields.tsv.
  N2 +0xC8..+0xEB is one u16[18] array: the initialiser fills exactly 18 words with 0xFFFF
     (002668A0 lea rdi,[rbx+0xc8] / 002668AB mov ecx,0x12 / 002668B0 rep stosw, ax = 0xFFFF), and the 12 flagged band
     offsets all fall inside it.
  N3 it is read as a per-slot override with an authored fallback: the indexed readers bound the slot to 0x11 (002652D9)
     or pick slot 7 / 14 (00269860), and fixed-slot readers load word +0xC8+2k, test 0xFFFF, and on 0xFFFF read element
     k of the count-prefixed s16 list at the authored entry's +0x18 (0025C490 and 0025CFA5 for k = 3; the initialiser's
     00266915 for k = 15). Planted negative: the same test at a non-band offset finds no such pattern.
  N4 writers: 0025AF60 stores into it by slot (0025AFA1, slot <= 0x11, value bit 15 clear) and is called by the script VM
     interpreter 0025E4C0; 0025AE00 stores at 0025AEC2 (called by setentrygroupall's handler 00340970).
  N5 the event post: 002EB030 (and 002EB430 with the constant 0x1001) resets +0xF5 = 0xFF and +0xEC = 0 and stores the
     event at +0xF0, then forwards to 002EB0D0.
  N6 +0x20 is a signed byte handle: the initialiser stores -1 (00266670 or ecx,-1 / 00266698) and 002E3AF0 releases a
     non-negative one through 0036EC10 and stores 0xFF.
  N7 +0x108 is only ever stored as 0: 0025DF1F xor ebp,ebp, no write to ebp before 0025E134 mov [rdi+0x108], ebp.
  N8 +0x100: 0025C230's dword accesses at +0x100 go through rbp = [rdx+0xB8] (the primary context), not the record; the
     record's word is read by 00263A10 only when +0x102 < 0.
  N9 +0x0A: the command-candidate builder 0046B690 clears it per record (0046B740) and sets 0x10 / 4 / 1
     (0046B7C3 / 0046B7EE / 0046B7FE); 002647E0 returns it by packed id.
  N10 +0xF4: both readers pass it as the third argument of 003DF760, which stores it as a dword into the slot table at
     02B59CC0 (00268E72 with slot 3, 0025D0E4 with slot 2); the initialiser's stores do not cover it.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
W = ROOT / "Database/Tools/work"
d = (W / "exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(W / "graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: SIZES[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
def body(a): return list(cs.disasm(d[off(a):off(a) + SIZES[a]], a))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

page = (DB / "04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md").read_text(encoding="utf-8")
flag = [int(m.group(1), 16) for m in re.finditer(r"^\| `\+0x([0-9A-F]+)` \|[^\n]*\*not in the store\*", page, re.M)]
st = [r for r in csv.DictReader(open(DB / "_types/fields.tsv", encoding="utf-8"), delimiter="\t") if r["type"] == "ActorStorageRecord"]
def covered(o): return any(int(r["offset"], 16) <= o < int(r["offset"], 16) + int(r["size"] or 1) for r in st)
check("N1 the page flags 34 offsets 'not in the store', and all 34 now have a store row",
      len(flag) == 34 and all(covered(o) for o in flag), "%d flagged, %d covered" % (len(flag), sum(covered(o) for o in flag)))

i = dis(0x26689A, 0x2668B3)
band = [o for o in flag if 0xC8 <= o < 0xEC]
check("N2 the initialiser fills 18 words at +0xC8 with 0xFFFF; the 12 flagged band offsets lie inside",
      i.get(0x26689A) == "mov r12d, 0xffff" and i.get(0x2668A0) == "lea rdi, [rbx + 0xc8]" and i.get(0x2668A7) == "movzx eax, r12w"
      and i.get(0x2668AB) == "mov ecx, 0x12" and i.get(0x2668B0) == "rep stosw word ptr [rdi], ax"
      and len(band) == 12 and all(o % 2 == 0 for o in band), "band %s" % ["+0x%X" % o for o in band])

def disp(v): return ("+ %d]" % v) if v < 10 else ("+ 0x%x]" % v)   # capstone prints small displacements in decimal
def fallback_at(site, k):
    x = dis(site, site + 0x40); ks = sorted(x)
    return (x[ks[0]].endswith("word ptr [rdi + 0x%x]" % (0xC8 + 2 * k)) and any(t == "mov ecx, 0xffff" for t in x.values())
            and any(t == "mov eax, %d" % k for t in x.values()) and any(t.endswith(disp(2 + 2 * k)) and t.startswith("movsx") for t in x.values()))
r1 = dis(0x2652D0, 0x265313); r2 = dis(0x26992D, 0x269959); r3 = dis(0x2668EC, 0x26691D)
check("N3 read as a per-slot override with the authored fallback (bounded / fixed slots); planted negative at a non-band offset",
      r1.get(0x2652D9) == "cmp r8d, 0x11" and r1.get(0x26530B) == "movzx eax, word ptr [rdx + rsi*2 + 0xc8]"
      and r2.get(0x269932) == "mov ebx, 0xe" and r2.get(0x26994D) == "cmovb ebx, r8d" and r2.get(0x269951) == "movzx eax, word ptr [rdi + rbx*2 + 0xc8]"
      and fallback_at(0x25C490, 3) and fallback_at(0x25CFA5, 3)
      and r3.get(0x2668EC) == "movzx eax, word ptr [rbx + 0xe6]" and r3.get(0x26690A) == "mov eax, 0xf" and r3.get(0x266915) == "movsx r8d, word ptr [rcx + rdi + 0x20]"
      and not fallback_at(0x25C311, 3))

w1 = dis(0x25AF7E, 0x25AFA9); w2 = dis(0x25AEC2, 0x25AECB)
calls_af60 = [x.address for x in body(0x25E4C0) if x.mnemonic == "call" and x.op_str == "0x25af60"]
calls_ae00 = [x.address for x in body(0x340970) if x.mnemonic == "call" and x.op_str == "0x25ae00"]
check("N4 writers: 0025AF60 by slot (<= 0x11, value bit 15 clear), called by the interpreter; 0025AE00 from 00340970",
      w1.get(0x25AF7E) == "cmp ebx, 0x11" and w1.get(0x25AFA1) == "mov word ptr [rax + rbx*2 + 0xc8], di"
      and dis(0x25AF77, 0x25AF7C).get(0x25AF77) == "bt r9d, 0xf" and w2.get(0x25AEC2) == "mov word ptr [rax + rdi*2 + 0xc8], r15w"
      and len(calls_af60) >= 1 and len(calls_ae00) >= 1, "interp calls %d, 00340970 calls %d" % (len(calls_af60), len(calls_ae00)))

e1 = dis(0x2EB030, 0x2EB07D); e2 = dis(0x2EB430, 0x2EB484)
check("N5 the event post resets +0xF5 = 0xFF and +0xEC = 0 and stores the event at +0xF0, then forwards to 002EB0D0",
      e1.get(0x2EB03C) == "mov byte ptr [rcx + 0xf5], 0xff" and e1.get(0x2EB043) == "mov dword ptr [rcx + 0xec], 0"
      and e1.get(0x2EB04D) == "mov dword ptr [rcx + 0xf0], edx" and e1.get(0x2EB073) == "call 0x2eb0d0"
      and e2.get(0x2EB43C) == "mov byte ptr [rcx + 0xf5], 0xff" and e2.get(0x2EB443) == "mov dword ptr [rcx + 0xec], 0"
      and e2.get(0x2EB44D) == "mov dword ptr [rcx + 0xf0], 0x1001" and e2.get(0x2EB47A) == "call 0x2eb0d0")

h = dis(0x266670, 0x26669B); g = dis(0x2E3BD0, 0x2E3BE4)
check("N6 +0x20 starts at -1 and 002E3AF0 releases a non-negative handle through 0036EC10, then stores 0xFF",
      h.get(0x266670) == "or ecx, 0xffffffff" and h.get(0x266698) == "mov byte ptr [rbx + 0x20], cl"
      and not any(k > 0x266670 and t.split(",")[0].split()[-1] in ("ecx", "cl", "cx") and t.startswith(("mov ecx", "xor ecx", "movzx ecx", "mov cl")) for k, t in h.items())
      and g.get(0x2E3BD0) == "movzx eax, byte ptr [rbx + 0x20]" and g.get(0x2E3BD6) == "js 0x2e3be4"
      and g.get(0x2E3BDB) == "call 0x36ec10" and g.get(0x2E3BE0) == "mov byte ptr [rbx + 0x20], 0xff")

span = [x for x in body(0x25DF00) if 0x25DF1F <= x.address <= 0x25E134]
ebp_writes = [x.address for x in span[1:-1] if x.op_str.split(",")[0].strip() in ("ebp", "rbp", "bp", "bpl") and x.mnemonic not in ("cmp", "test", "push")]
check("N7 +0x108 is stored only as 0: ebp is zeroed at 0025DF1F and not written before 0025E134",
      span[0].mnemonic == "xor" and span[0].op_str == "ebp, ebp" and span[-1].address == 0x25E134
      and span[-1].op_str == "dword ptr [rdi + 0x108], ebp" and ebp_writes == [], "ebp writes %s" % ["%08X" % a for a in ebp_writes])

c = dis(0x25C268, 0x25C26F); c2 = dis(0x25C311, 0x25C318); q = dis(0x263A10, 0x263A25)
check("N8 0025C230's +0x100 is the context's (rbp = [rdx+0xB8]); the record's word is read by 00263A10 only when +0x102 < 0",
      c.get(0x25C268) == "mov rbp, qword ptr [rdx + 0xb8]" and c2.get(0x25C311) == "mov r12d, dword ptr [rbp + 0x100]"
      and not any(x.op_str.startswith("rbp,") and x.mnemonic in ("mov", "lea") and x.address != 0x25C268 for x in body(0x25C230))
      and q.get(0x263A10) == "cmp word ptr [rcx + 0x102], 0" and q.get(0x263A18) == "jge 0x263a22"
      and q.get(0x263A1A) == "movzx eax, word ptr [rcx + 0x100]")

a = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in body(0x46B690)}; r = dis(0x2647E0, 0x2647F7)
check("N9 +0x0A: the candidate builder clears it and sets 0x10 / 4 / 1; 002647E0 returns it by packed id",
      a.get(0x46B740) == "mov byte ptr [rax + 0xa], 0" and a.get(0x46B7C3) == "or byte ptr [rbx + 0xa], 0x10"
      and a.get(0x46B7EE) == "or byte ptr [rbx + 0xa], 4" and a.get(0x46B7FE) == "or byte ptr [rbx + 0xa], 1"
      and r.get(0x2647E4) == "call 0x3588b0" and r.get(0x2647EE) == "movzx eax, byte ptr [rax + 0xa]")

s1 = dis(0x268E5A, 0x268E84); s2 = dis(0x25D0CE, 0x25D0F1); t = dis(0x3DF760, 0x3DF790)
check("N10 +0xF4 is the value 003DF760 stores into the 02B59CC0 slot table (slot 3 / slot 2)",
      s1.get(0x268E5A) == "movzx ebx, byte ptr [rdi + 0xf4]" and s1.get(0x268E72) == "mov r8d, ebx" and s1.get(0x268E7A) == "mov edx, 3"
      and s1.get(0x268E7F) == "call 0x3df760" and s2.get(0x25D0CE) == "movzx ebx, byte ptr [rdi + 0xf4]" and s2.get(0x25D0E4) == "mov r8d, ebx"
      and s2.get(0x25D0EC) == "mov edx, 2" and t.get(0x3DF77F) == "mov dword ptr [rdx + r10*4 + 0x2a39cc0], r8d"
      and t.get(0x3DF768) == "lea rdx, [rip - 0x2bf76f]" and 0x3DF76F - 0x2BF76F + 0x2A39CC0 == 0x2B59CC0)
print("FAILS", fails)
sys.exit(1 if fails else 0)
