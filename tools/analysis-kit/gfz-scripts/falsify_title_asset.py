"""Falsification pass 1 on the-title-asset-singleton-and-its-distinct-consumer (OPUS, 2026-09-29), from the shipping image.
Section 8 (SWE2-STRUCT's OV-31 type-store checks S P J X C O K) and the native fixtures are carried, not re-run.
Call counts come from a raw E8/E9 rel32 index over the whole of .text.

  A0  sizes of the nine bodies the page reads
  A1  section 1: the asset factory 00394460 - five calls and a byte store before the guard, the guard at 0039448B on
      02AEE4C0, handler 00394070 at 00394498, 0xD8 at 0039449F, the allocation at 003944A4 (00244F50); the consumer factory
      00394530 - exits unless 02AEE4C0 is nonnull, handles an existing 02AEE4C8, else 0x1D0 at 0039456C with 003939B0 at
      00394571 through 00244F50
  A2  section 2: the consumer's message-1 arm (jump table entry 1 -> 003939F7) takes the message byte, clears rbx, zeroes
      +0xC4 and +0xC8, publishes 02AEE4C8 (00393A11), stores the byte at +0xC0 and calls 002E1C20(1, 0x15)
  A3  section 3: the asset's own handler - message 1 publishes 02AEE4C0 (003940F5), zeroes +0xC0, runs 00393FF0 and sets
      channel 0 bit 21; message 16 ORs bit 0; message 18 calls 0024A680(+0xC8, 1), releases and clears a nonnull +0xD0,
      clears channel 0 bit 21 and zeroes 02AEE4C0 - with no compare of the slot and no write to +0xC8 or +0xC0
  A4  section 3: 00393FF0 - ticket 00249580; 002493D0(ticket, 7, 0x3D, 3, descriptor, 2) -> +0xC8 and the returned
      record's +0x40 = 0; 00249320(ticket, 7, 0x3A) -> +0xD0; tail submit 00249410
  A5  section 3: 00249410 notifies only when words +0x18 and +0x1A are equal, and on a ticket whose +4 is 0 sends message
      0x10 to the owner at +8; 00249580 records the owner at +8
  A6  section 4: the consumer's message-2 arm (entry 2 -> 00393A7A) tests its own +0xC4 bit 0, loads 02AEE4C0, refuses
      null or a clear bit 0 of asset +0xC0, loads asset +0xD0 and calls 003946B0 with selector 5
  A7  section 5: 00245000 and 00244F50 return the receiver in rax; 002465F0 keeps it in rdi and returns the predicate
  A8  CON-202: 00249320 is the class-3 node factory as read (00249210 with r9d 3 and a zero fifth argument, 00249660 at
      +0x10, returns +8), but the title asset's call is 00393FF0's (00394048), reached only from the asset's own handler
      (00394106); the 0x1D0 consumer 003939B0 makes no direct call to it
"""
import bisect, collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


fs = []
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            fs.append((int(p[0], 16), int(p[2])))
        except ValueError:
            pass
fs.sort(); sizes = dict(fs); starts = [a for a, _ in fs]


def owner(va):
    j = bisect.bisect_right(starts, va) - 1
    return fs[j][0] if j >= 0 and va < fs[j][0] + fs[j][1] else None


def body(fa):
    return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}


def rip(a, text, target):
    """a rip-relative operand at `a` in `text` names `target` (next-instruction base found by decoding)."""
    x = next(md.disasm(blob[OFF(a):OFF(a) + 16], a))
    m = re.search(r"rip ([+-]) 0x([0-9a-f]+)", text)
    return m is not None and x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) == target


u32 = lambda va: struct.unpack("<I", blob[OFF(va):OFF(va) + 4])[0]
tx = [s for s in SECS if s[0] == ".text"][0]
T0, TR, TN = tx[1], tx[3], tx[4]
callers = collections.defaultdict(list)
for m in re.finditer(rb"[\xe8\xe9]", blob[TR:TR + TN - 4]):
    i = m.start()
    callers[T0 + i + 5 + struct.unpack("<i", blob[TR + i + 1:TR + i + 5])[0]].append(T0 + i)

# A0
SZ = {0x00394460: 82, 0x00394530: 164, 0x00394070: 190, 0x00393FF0: 118, 0x00249320: 43, 0x00245000: 31, 0x003939B0: 1173,
      0x00249410: 133, 0x00249580: 60}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("A0", not bad, "sizes %s" % (bad or "all nine as read"))

# A1
f, c = body(0x00394460), body(0x00394530)
pre = [a for a, t in f.items() if a < 0x0039448B and t.startswith("call ")]
ok = (len(pre) == 5 and f.get(0x00394470) == "mov byte ptr [rax + 0xde6], 0" and rip(0x0039448B, f[0x0039448B], 0x02AEE4C0)
      and f.get(0x00394493) == "jne 0x3944a9" and rip(0x00394498, f[0x00394498], 0x00394070) and f.get(0x0039449F) == "mov ecx, 0xd8"
      and f.get(0x003944A4) == "call 0x244f50"
      and rip(0x00394543, c[0x00394543], 0x02AEE4C0) and c.get(0x0039454B) == "je 0x3945c2" and rip(0x0039454D, c[0x0039454D], 0x02AEE4C8)
      and c.get(0x00394557) == "jne 0x394594" and c.get(0x0039456C) == "mov ecx, 0x1d0" and rip(0x00394571, c[0x00394571], 0x003939B0)
      and c.get(0x0039457D) == "call 0x244f50")
check("A1", ok, "asset: %d calls before the 02AEE4C0 guard, 0xD8 via 00244F50; consumer: needs 02AEE4C0, 0x1D0 via 00244F50" % len(pre))

# A2 (the consumer's jump table: entry k -> message k + 1)
J = [BASE + u32(0x00393E48 + 4 * k) for k in range(19)]
v = body(0x003939B0)
ok = (v.get(0x003939E2) == "lea rdx, [rip - 0x2739e9]" and 0x003939E9 - 0x2739E9 == BASE and v.get(0x003939EB) == "mov ecx, dword ptr [rdx + rax*4 + 0x273e48]"
      and J[0] == 0x003939F7 and v.get(0x003939D1) == "mov rbx, rdx" and v.get(0x003939D6) == "mov rsi, rcx"
      and v.get(0x003939F7) == "movzx eax, byte ptr [rbx + 8]" and v.get(0x003939FB) == "xor ebx, ebx"
      and v.get(0x003939FD) == "mov dword ptr [rsi + 0xc4], ebx" and v.get(0x00393A03) == "mov qword ptr [rsi + 0xc8], rbx"
      and rip(0x00393A11, v[0x00393A11], 0x02AEE4C8) and v[0x00393A11].endswith("rsi") and v.get(0x00393A18) == "mov byte ptr [rsi + 0xc0], al"
      and v.get(0x00393A23) == "lea edx, [rbx + 0x15]" and v.get(0x00393A26) == "lea ecx, [rbx + 1]" and v.get(0x00393A29) == "call 0x2e1c20")
check("A2", ok, "message 1 -> 003939F7: message byte to consumer +0xC0, +0xC4/+0xC8 zeroed, 02AEE4C8 published, 002E1C20(1, 21)")

# A3
h = body(0x00394070)
m18 = [t for a, t in h.items() if 0x00394097 <= a <= 0x003940E2]
ok = (h.get(0x00394079) == "mov ecx, dword ptr [rdx]" and h.get(0x0039407E) == "je 0x3940f2" and h.get(0x00394083) == "je 0x3940e3"
      and h.get(0x00394085) == "cmp ecx, 2" and h.get(0x00394088) == "je 0x394097"
      and rip(0x003940F5, h[0x003940F5], 0x02AEE4C0) and h.get(0x003940FC) == "mov dword ptr [rbx + 0xc0], 0"
      and h.get(0x00394106) == "call 0x393ff0" and h.get(0x0039410B) == "mov edx, 0x15" and h.get(0x00394110) == "xor ecx, ecx"
      and h.get(0x00394112) == "call 0x2e1c20" and h.get(0x003940E3) == "or dword ptr [rbx + 0xc0], 1"
      and h.get(0x00394097) == "mov rcx, qword ptr [rbx + 0xc8]" and h.get(0x0039409E) == "mov edx, 1" and h.get(0x003940A3) == "call 0x24a680"
      and h.get(0x003940B2) == "je 0x3940c4" and h.get(0x003940B4) == "call 0x3697f0" and h.get(0x003940B9) == "mov qword ptr [rbx + 0xd0], 0"
      and h.get(0x003940C4) == "mov edx, 0x15" and h.get(0x003940C9) == "xor ecx, ecx" and h.get(0x003940CB) == "call 0x2e1ca0"
      and rip(0x003940D2, h[0x003940D2], 0x02AEE4C0) and not any(t.startswith("cmp") for t in m18)
      and not any(t.startswith(("mov dword ptr [rbx + 0xc0]", "and dword ptr [rbx + 0xc0]", "mov qword ptr [rbx + 0xc8]")) for t in m18))
check("A3", ok, "message 1 publishes, zeroes +0xC0, requests, sets channel 0 bit 21; 16 ORs bit 0; 18 releases with no slot compare")

# A4
r = body(0x00393FF0)
ok = (r.get(0x00393FFD) == "call 0x249580" and r.get(0x0039400C) == "mov dword ptr [rsp + 0x28], 2" and r.get(0x00394017) == "mov qword ptr [rsp + 0x20], rdx"
      and r.get(0x0039401C) == "mov edx, 7" and r.get(0x00394021) == "lea r9d, [rdx - 4]" and r.get(0x00394025) == "lea r8d, [rdx + 0x36]"
      and r.get(0x00394029) == "call 0x2493d0" and r.get(0x00394033) == "mov qword ptr [rdi + 0xc8], rax"
      and r.get(0x0039403D) == "mov dword ptr [rax + 0x40], 0" and r.get(0x0039402E) == "mov edx, 7" and r.get(0x00394044) == "lea r8d, [rdx + 0x33]"
      and r.get(0x00394048) == "call 0x249320" and r.get(0x00394050) == "mov qword ptr [rdi + 0xd0], rax" and r.get(0x00394061) == "jmp 0x249410")
check("A4", ok, "002493D0(ticket, 7, 0x3D, 3, descriptor, 2) -> +0xC8, its record's +0x40 = 0; 00249320(ticket, 7, 0x3A) -> +0xD0; submit")

# A5
s, k = body(0x00249410), body(0x00249580)
ok = (s.get(0x00249430) == "movzx eax, word ptr [rcx + 0x18]" and s.get(0x00249434) == "cmp word ptr [rcx + 0x1a], ax" and s.get(0x00249438) == "jne 0x249482"
      and s.get(0x0024943A) == "cmp dword ptr [rcx + 4], 0" and s.get(0x00249456) == "mov rcx, qword ptr [rcx + 8]"
      and s.get(0x0024945D) == "mov dword ptr [rsp + 0x20], 0x10" and s.get(0x0024947D) == "call rax"
      and k.get(0x002495B7) == "mov qword ptr [rax + 8], rcx" and k.get(0x002495B0) == "mov qword ptr [rax + 0x18], rdx")
check("A5", ok, "equal +0x18/+0x1A and +4 == 0 -> message 0x10 to the owner at +8; the ticket records its owner at +8")

# A6
ok = (J[1] == 0x00393A7A and v.get(0x00393A7A) == "mov eax, dword ptr [rsi + 0xc4]" and v.get(0x00393A80) == "test al, 1"
      and rip(0x00393A88, v[0x00393A88], 0x02AEE4C0) and v.get(0x00393A92) == "je 0x393e15" and v.get(0x00393A98) == "test byte ptr [rdx + 0xc0], 1"
      and v.get(0x00393A9F) == "je 0x393e15" and v.get(0x00393AA5) == "mov rdx, qword ptr [rdx + 0xd0]" and v.get(0x00393AAC) == "mov r8d, 5"
      and v.get(0x00393AB2) == "mov rcx, rsi" and v.get(0x00393ABD) == "call 0x3946b0")
check("A6", ok, "message 2 -> 00393A7A: own +0xC4 bit 0; asset from 02AEE4C0, bit 0 of its +0xC0; asset +0xD0 to 003946B0 with 5")

# A7
w, a2, ini = body(0x00245000), body(0x00244F50), body(0x002465F0)
ok = (w.get(0x00245006) == "mov rbx, rcx" and w.get(0x00245011) == "call 0x2465f0" and w.get(0x00245016) == "mov rax, rbx"
      and a2.get(0x00244FCD) == "call 0x2465f0" and a2.get(0x00244FD7) == "mov rax, rbx" and ini.get(0x0024661D) == "mov rdi, rcx"
      and not any(t in ("mov rax, rdi", "lea rax, [rdi]") for t in ini.values())
      and ini.get(0x0024674A) == "call 0x1edda0" and ini.get(0x00246753) == "call 0x314960" and ini.get(0x0024677A) == "ret")
check("A7", ok, "the two wrappers restore the receiver into rax; 002465F0 keeps it in rdi and never moves it to rax")

# A8
n = body(0x00249320)
own = sorted(set(owner(x) for x in callers[0x00249320]))
ok = (n.get(0x00249324) == "mov r9d, 3" and n.get(0x0024932A) == "mov dword ptr [rsp + 0x20], 0" and n.get(0x00249332) == "call 0x249210"
      and rip(0x00249337, n[0x00249337], 0x00249660) and n.get(0x0024933E) == "mov qword ptr [rax + 0x10], rcx"
      and n.get(0x00249342) == "mov rax, qword ptr [rax + 8]"
      and own == [0x003933F0, 0x00393FF0, 0x003F4840, 0x00404060] and 0x00394048 in callers[0x00249320]
      and callers[0x00393FF0] == [0x00394106] and owner(0x00394106) == 0x00394070
      and not any(t in ("call 0x249320", "jmp 0x249320") for t in v.values()) and 0x003939B0 not in own)
check("A8", ok, "00249320 callers %s; the title asset's is 00393FF0 (from its own handler 00394106), not the consumer 003939B0"
      % " ".join("%08X" % x for x in own))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
