"""reregister.py - OV-40: do callers ever register already-relocated borrowed bytes a second time? (FABLE, Claude Opus 5.5,
2026-09-29). STATIC.

The nonempty-registration page (the specialized subtype section) found that disposing and explicitly re-registering the
same already-relocated external bytes repeats the offset additions, and asked what callers do. The registration it studies
is 00409FE0 (bank entry, setup 00409A60, borrowing context 003B38B0 -> 003EDAD0 -> the A00 register 003A9A70 -> rebase).

  E  ENTRIES: 003B38B0 and 00409A60 are called only from 00409FE0; 00409FE0 only from the thunk 0041E580; 0041E580 only
     from the four family completions (../ov25-queue-clients-fable/families.py R)
  C  each completion is taken only by the lea at its submit (rip-operand scan), never called or jumped to, never stored as
     an absolute pointer: it runs only as the queue's completion of that submit's request
  B  each submit reads INTO the backing its completion registers:
     B1 indexed owner: dest = 0036B130(owner +0) at 003DDA79-003DDAA1; 003DD850 registers owner +0 (003DD86E, 003DD8A8)
     B2 motion cache: 0036B160 allocates, the handle goes to slot +0, dest = 0036A000(handle) (003DC62D-003DC676);
        003DC340 registers slot +0 (003DC35A, 003DC36A)
     B3 name binding: dest = 0036A000(record +0x10) (002EAD62-002EADFC); 002E4D20 registers +0x10 (002E4D4B, 002E4DAF)
     B4 per lane: submits only a lane whose handle is 0, allocating it (0036B160) and reading into 0036A000(handle)
        (002E6EED-002E7001); 002E4E50 registers the lane handle (002E4EB0, 002E4EF4)
  So on a delivered read, what is registered is always the bytes that read just delivered, never bytes already rebased.
  F  THE EXCEPTION: the failure helper 0032E370 calls a completion (ok = 0) when the request's byte count is -1, and none
     of the four completions reads ok (r8): it then registers backing the read did not fill (for B2/B4 a fresh allocation;
     for B1/B3 what the backing held). Whether that content can be already-relocated bytes is not established
  K  sensitivity: the rip-operand scan finds each submit's lea; the call scan finds 0041E580's four sites
Not claimed: the five other drivers of the context driver 003EDAD0 (0026FB90, 002FC4A0, 003B0660, 003B2220, 003B29B0)
reach the A00 register outside 00409FE0; whether they re-run a context over bytes it already rebased is OV-41's ground.
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
        for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
TX = [s for s in SECS if s[0] == b".text"][0]
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
def callers(t):
    return [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == t]
def jcc(t):
    return [tb + j for j in range(len(text) - 6) if text[j] == 0x0F and 0x80 <= text[j + 1] <= 0x8F
            and tb + j + 6 + struct.unpack_from("<i", text, j + 2)[0] == t]
def ptrs(t):
    pat = struct.pack("<Q", t); out = []
    for nm, vs, va, rs, ro in SECS:
        blob = d[ro:ro + rs]; k = blob.find(pat)
        while k >= 0: out.append(B + va + k); k = blob.find(pat, k + 1)
    return out
def riprefs(t):
    # any disp32 in .text that resolves rip-relative to t: the displacement is followed by 0, 1, 2 or 4 immediate bytes;
    # the instruction starts 2..9 bytes before it, and must decode as ONE instruction ending exactly there with a rip operand
    # (decoding from a fixed offset lands mid-instruction - the first draft found not even the known lea at 003DDA83)
    out = []
    for j in range(len(text) - 4):
        disp = struct.unpack_from("<i", text, j)[0]
        for tail in (0, 1, 2, 4):
            end = j + 4 + tail
            if tb + end + disp != t: continue
            for back in range(2, 10):
                x = next(cs.disasm(text[j - back:end], tb + j - back, 1), None)
                if x and x.size == back + 4 + tail and "rip" in x.op_str: out.append(x.address)
    return sorted(set(out))

# E
check("E", callers(0x3B38B0) == [0x40A174] and callers(0x409A60) == [0x40A06E, 0x40A099] and callers(0x409FE0) == [0x41E587]
      and callers(0x41E580) == [0x2E4DB4, 0x2E4EFA, 0x3DC371, 0x3DD8AB]
      and not jcc(0x3B38B0) and not jcc(0x409A60) and not riprefs(0x3B38B0) and not riprefs(0x409A60),
      "003B38B0 and 00409A60 <- only 00409FE0 <- only 0041E580 <- the four completions")
# C
SUB = {0x3DD850: 0x3DDA83, 0x3DC340: 0x3DC650, 0x2E4D20: 0x2EADA2, 0x2E4E50: 0x2E6FB3}
check("C", all(min(riprefs(cb)) == lea and max(riprefs(cb)) <= lea + 1 and not callers(cb) and not jcc(cb) and not ptrs(cb)
               for cb, lea in SUB.items()),
      "each completion is taken only by its submit's lea (one instruction; the second hit is its REX-less alias)")
# B
b = [at(dis(0x3DDA79, 0x3DDABE), {0x3DDA79: "mov ecx, dword ptr [rcx]", 0x3DDA7B: "call 0x36b130", 0x3DDAA1: "mov r8, rax", 0x3DDAB9: "call 0x32e620"})
     and at(dis(0x3DD850, 0x3DD8C2), {0x3DD86E: "mov ebx, dword ptr [rdi]", 0x3DD8A8: "mov rdx, rbx", 0x3DD8AB: "call 0x41e580"}),
     at(dis(0x3DC62D, 0x3DC688), {0x3DC62D: "call 0x36b160", 0x3DC634: "mov dword ptr [r14], eax", 0x3DC637: "call 0x36a000",
                                  0x3DC63C: "mov rbx, rax", 0x3DC676: "mov r8, rbx", 0x3DC683: "call 0x32e620"})
     and at(dis(0x3DC340, 0x3DC376), {0x3DC35A: "mov ebx, dword ptr [rbx]", 0x3DC36A: "mov edx, ebx", 0x3DC371: "jmp 0x41e580"}),
     at(dis(0x2EAD62, 0x2EAE0D), {0x2EAD62: "mov ecx, dword ptr [rcx + 0x10]", 0x2EAD65: "call 0x36a000", 0x2EAD7C: "mov r14, rax",
                                  0x2EADFC: "mov r8, r14", 0x2EAE08: "call 0x32e620"})
     and at(dis(0x2E4D20, 0x2E4DFE), {0x2E4D4B: "mov esi, dword ptr [rdi + 0x10]", 0x2E4DAF: "mov edx, esi", 0x2E4DB4: "call 0x41e580"}),
     at(dis(0x2E6EB0, 0x2E7072), {0x2E6EC0: "lea r15, [rcx + 0x60]", 0x2E6EED: "cmp dword ptr [r15], 0", 0x2E6EF6: "jne 0x2e7032",
                                  0x2E6F4D: "call 0x36b160", 0x2E6F52: "mov dword ptr [r15], eax", 0x2E6F96: "mov ecx, dword ptr [r15]",
                                  0x2E6FAC: "call 0x36a000", 0x2E7001: "mov r8, rax", 0x2E700C: "call 0x32e620"})
     and at(dis(0x2E4E50, 0x2E4F34), {0x2E4EB0: "mov r14d, dword ptr [rbx + rsi*4 + 0x60]", 0x2E4EF4: "mov edx, r14d", 0x2E4EFA: "call 0x41e580"})]
check("B", all(b), "B1-B4 each submit reads into the backing its completion registers: %s" % b)
# F
cbs = {cb: dis(cb, cb + 0x100) for cb in SUB}
ends = {0x3DD850: 0x3DD8C2, 0x2E4D20: 0x2E4DFE, 0x2E4E50: 0x2E4F34, 0x3DC340: 0x3DC376}
R8 = r"\br8(d|w|b)?\b"
def reads_r8_on_entry(cb):
    # ok arrives in r8, a volatile register: it is read only if an instruction uses r8 before the first call or before
    # the first plain write to r8 (002E4D20's `mov r8d, [rdi+0x14]` and `lea r8, [rsp+0x24]` are writes after a call)
    for a, s in sorted(dis(cb, ends[cb]).items()):
        if s.startswith(("call", "jmp")): return []
        if re.search(R8, s):
            dst, _, src = s.partition(" ")[2].partition(", ")
            if s.split()[0] in ("mov", "lea", "movzx", "movsxd") and re.fullmatch(R8, dst) and not re.search(R8, src): return []
            return [s]
    return []
reads_ok = {cb: reads_r8_on_entry(cb) for cb in SUB}
check("F", at(dis(0x32E370, 0x32E3AE), {0x32E382: "cmp dword ptr [rcx + 0x28], -1", 0x32E38C: "xor r8d, r8d", 0x32E392: "call rax"})
      and dis(0x32E92C, 0x32E930).get(0x32E92C) == "mov dword ptr [r10 + 0x28], esi"
      and not any(reads_ok.values()) and re.search(r"\br8(d|w|b)?\b", "xor r8d, r8d"),
      "a count -1 failure calls back with ok = 0; no completion reads r8 (the pattern matches 'xor r8d, r8d')")
# K
check("K", min(riprefs(0x3DD850)) == 0x3DDA83 and len(callers(0x41E580)) == 4, "the scans find known positives")
_dis = dis
dis = lambda a, b: {1: "test r8d, r8d", 2: "call 0x1"}; ends[1] = 3; k_read = reads_r8_on_entry(1)
dis = lambda a, b: {1: "mov r8d, dword ptr [rdi]", 2: "test r8d, r8d"}; k_write = reads_r8_on_entry(1)
dis = _dis
check("K2", k_read == ["test r8d, r8d"] and k_write == [], "the ok-read detector flags a synthetic `test r8d, r8d` and passes a write-first body")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
