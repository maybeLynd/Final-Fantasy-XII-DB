"""families.py - OV-25, the "other external-owner families" half (FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

An external-owner family here means: a record that holds a loaded source's handle, is handed to the tail requester
0032E620 as the completion argument, and whose completion REGISTERS the loaded source (the spawn thunk 0041E580 ->
00409FE0), as the indexed owner's 003DD850 does.

  R  REGISTRATION CENSUS: 00409FE0 has one caller, the 12-byte thunk 0041E580; 0041E580 has exactly four callers, each
     inside a completion callback that a requester site loads with `lea` (clients.py C): 003DD850 (the indexed owner,
     site 003DDAB9), 003DC340 (site 003DC683), 002E4D20 (site 002EAE08), 002E4E50 (site 002E700C). Raw sweeps: no
     rel32 jcc, no rip-relative operand and no absolute 8-byte pointer in any section names either address
  M  THE MOTION CACHE (16 slots x 0x14 at 02B57F70; +0 handle, +4 refcount, +6 state, +8 generation-tagged id):
     M1 submit 003DC5B0 runs only on state 1, stores the handle, submits with the slot's address, writes 2 AFTER the call
     M2 completion 003DC340 writes 3, unpins (0036D170), registers (0041E580)
     M3 release 003DC780(id) matches the slot id, decrements the refcount, and at 0 zeroes it and raises the sweep flag
     M4 the three sweeps 003DC420 / 003DC6A0 / 003DC710 write 4 only on a state-3 slot; no other byte-store of 4 to +6 in
        the twelve functions that address the table (a store through a slot pointer held elsewhere is not excluded) (003DC6A0 also requires refcount 0
        and bumps the id by 0x10)
     M5 drain 003DC4A0 (flag 02B58170 set): each state-4 slot is released (0041E490), freed (00369800), cleared to 0
     So an in-flight slot (state 2) is never released: it needs no deferred-delete state
  S  THE SCRIPT NAME-BINDING RECORD (completion 002E4D20, argument = the record address): unpins +0x10's handle, then
     REGISTERS unless flag byte +0x18 has bit 4 (then it sets bit 8 instead); then 002EA6E0(record, 3) and, on 0, bit 2
  L  THE PER-LANE SUB-RECORD (completion 002E4E50; argument = record index << 16 | lane; records 0x120 B at 02161DA0,
     lane handle at +0x60 + 4*lane; masks +0x24 loaded, +0x2C release requested, +0x34 pending):
     L1 completion sets the loaded bit and clears the pending bit; registers only when the record's node (0x40 B at
        0215FDA0, index +0x22) still carries the record's generation (+0x5C == node +0x24); otherwise 002EAFA0
     L2 release request 002EAFA0 sets the requested bit if the lane is pending, loaded or +0x28; links the record onto
        the sweep list 0215FD90 only when the lane is loaded
     L3 sweep 002E6A80 releases a lane only when requested AND loaded: 002E6E30 releases (0041E490), frees (00369800),
        clears the handle and both bits. A lane requested while pending is not released in flight
  U  RELEASE CENSUS: 0041E490 has eight callers - the indexed owner's three (003DD380, 003DD420, 003DD850), the motion
     cache drain 003DC4A0, the lane release 002E6E30, and 002E65A0 / 002E6900 / 002E6D60 (the per-frame gate's drain and
     list code; not attributed to a family here)
  K  SENSITIVITY: each scanner R relies on finds a known positive: the call scan 003DDAB9, the rip-operand scan the lea
     of 003DD850 at 003DDA83 (the first draft of that scan decoded from a fixed offset and found nothing, not even this),
     the pointer scan the .rdata qword at 008C31C0 -> 0016D6A0
Not claimed: the script name-binding record's deletion policy (who sets +0x18 bit 4; 002EAEB0 and 002EA6E0 unread past
their flag writes); whether a per-lane release requested in flight whose node then goes stale reaches the sweep list
(002EAFA0 returns early when the requested bit is already set; 002EB890 unread); authored reachability of any state.
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

# R
c580 = callers(0x41E580)
check("R", callers(0x409FE0) == [0x41E587] and dis(0x41E580, 0x41E58C) == {0x41E580: "mov rcx, qword ptr [rcx + 0xd90]", 0x41E587: "jmp 0x409fe0"}
      and c580 == [0x2E4DB4, 0x2E4EFA, 0x3DC371, 0x3DD8AB]
      and not jcc(0x41E580) and not jcc(0x409FE0) and not ptrs(0x41E580) and not ptrs(0x409FE0)
      and not riprefs(0x41E580) and not riprefs(0x409FE0),
      "00409FE0 <- only the thunk 0041E580; 0041E580 <- %s; no jcc, pointer or rip reference to either" % " ".join("%08X" % a for a in c580))
LEAS = {0x3DD850: (0x3DDA83, 0x3DDAB9), 0x3DC340: (0x3DC650, 0x3DC683), 0x2E4D20: (0x2EADA2, 0x2EAE08), 0x2E4E50: (0x2E6FB3, 0x2E700C)}
req = callers(0x32E620)
check("R2", all(min(riprefs(cb)) == lea and site in req for cb, (lea, site) in LEAS.items()),
      "each registering completion is taken by a lea before a requester site: %s"
      % "; ".join("%08X at %08X -> call %08X" % (cb, lea, site) for cb, (lea, site) in LEAS.items()))
# M
m1 = dis(0x3DC5B0, 0x3DC69E)
check("M1", at(m1, {0x3DC5B9: "cmp byte ptr [rcx + 6], 1", 0x3DC5C0: "jne 0x3dc697", 0x3DC634: "mov dword ptr [r14], eax",
                    0x3DC67E: "mov dword ptr [rsp + 0x38], r14d", 0x3DC683: "call 0x32e620", 0x3DC692: "mov byte ptr [r14 + 6], 2"}),
      "motion-cache submit: state 1 only; handle stored; slot address as the argument; state 2 after the call")
check("M2", at(dis(0x3DC340, 0x3DC376), {0x3DC346: "mov ebx, ecx", 0x3DC34A: "mov byte ptr [rbx + 6], 3", 0x3DC34E: "call 0x36d170",
                                         0x3DC371: "jmp 0x41e580"}), "completion: state 3, unpin, register")
check("M3", at(dis(0x3DC780, 0x3DC7CA), {0x3DC79A: "cmp dword ptr [rcx + rax*4 + 8], edx", 0x3DC7A4: "dec word ptr [rcx + 4]",
                                         0x3DC7B1: "mov dword ptr [rip + 0x277b9b5], 1", 0x3DC7BB: "mov word ptr [rcx + 4], ax"}),
      "release by id: refcount -1; at 0 the sweep flag 02B58170 is raised")
w4 = {0x3DC420: (0x3DC45A, 0x3DC478, "mov byte ptr [rcx + 6], 4"), 0x3DC6A0: (0x3DC6BA, 0x3DC6DA, "mov byte ptr [r9 + rax*4 + 6], 4"),
      0x3DC710: (0x3DC72A, 0x3DC752, "mov byte ptr [r9 + rax*4 + 6], 4")}
ok4 = all(dis(f, f + 0x80).get(c, "").endswith("+ 6], 3") and dis(f, f + 0x80).get(w) == s for f, (c, w, s) in w4.items())
# every byte-store of 4 to a +6 field in the ten functions that address 02B57F70
tbl = [0x3DC380, 0x3DC420, 0x3DC4A0, 0x3DC5B0, 0x3DC6A0, 0x3DC710, 0x3DC780, 0x3DC7D0, 0x3DCA00, 0x3DCB90, 0x3DCBC0, 0x3DCD00]
stores4 = sorted(set(a for f in tbl for a, s in dis(f, f + 0x200).items() if re.match(r"mov byte ptr \[.*\+ 6\], 4$", s) and a < f + 0x200))
check("M4", ok4 and at(dis(0x3DC6A0, 0x3DC6E0), {0x3DC6C2: "cmp word ptr [r9 + rax*4 + 4], 0", 0x3DC6CB: "add dword ptr [r9 + rax*4 + 8], 0x10"})
      and set(stores4) <= {0x3DC478, 0x3DC6DA, 0x3DC752},
      "in the twelve functions that address the table, state 4 is written only from state 3 (%s)" % " ".join("%08X" % a for a in stores4))
check("M5", at(dis(0x3DC4A0, 0x3DC5A5), {0x3DC4A7: "cmp dword ptr [rip + 0x277bcc2], 0", 0x3DC4FA: "cmp byte ptr [r13 + rbx*4 + 6], 4",
                                         0x3DC522: "call 0x41e490", 0x3DC529: "call 0x369800", 0x3DC52E: "mov byte ptr [r13 + rbx*4 + 6], r12b",
                                         0x3DC53D: "mov dword ptr [r13 + rbx*4], r12d"}),
      "drain: state-4 slots released, freed, cleared")
# S
check("S", at(dis(0x2E4D20, 0x2E4DFE), {0x2E4D3E: "movsxd rdi, ecx", 0x2E4D4B: "mov esi, dword ptr [rdi + 0x10]", 0x2E4D89: "call 0x36d170",
                                        0x2E4D92: "test al, 4", 0x2E4D94: "je 0x2e4d9d", 0x2E4D96: "or al, 8", 0x2E4DB4: "call 0x41e580",
                                        0x2E4DC6: "call 0x2ea6e0", 0x2E4DCF: "or byte ptr [rdi + 0x18], 2"}),
      "name-binding completion: unpin; register unless +0x18 bit 4 (then bit 8); 002EA6E0(record, 3); bit 2")
# L
check("L1", at(dis(0x2E4E50, 0x2E4F34), {0x2E4E5A: "movzx esi, cx", 0x2E4E5D: "sar ecx, 0x10", 0x2E4EA9: "cmp dword ptr [rcx + 0x24], eax",
                                         0x2E4EBE: "or dword ptr [rbx + 0x24], ebp", 0x2E4EC5: "and dword ptr [rbx + 0x34], eax",
                                         0x2E4EFA: "call 0x41e580", 0x2E4F15: "call 0x2eafa0"}),
      "per-lane completion: loaded bit set, pending bit cleared, register only on a matching node generation, else 002EAFA0")
check("L2", at(dis(0x2EAFA0, 0x2EB027), {0x2EAFB0: "test edx, ecx", 0x2EAFB2: "jne 0x2eb026", 0x2EAFB4: "mov eax, dword ptr [r8 + 0x34]",
                                         0x2EAFC9: "mov dword ptr [r8 + 0x2c], ecx", 0x2EAFCD: "test edx, r9d", 0x2EAFD0: "je 0x2eb026",
                                         0x2EB01F: "mov qword ptr [rip + 0x1e74d6a], rax"}),
      "release request: requested bit; linked onto 0215FD90 only when loaded")
check("L3", at(dis(0x2E6A80, 0x2E6B00), {0x2E6AA0: "test dword ptr [rdi + 0x2c], ebx", 0x2E6AA5: "test dword ptr [rdi + 0x24], ebx",
                                         0x2E6AAF: "call 0x2e6e30"})
      and at(dis(0x2E6E30, 0x2E6EA9), {0x2E6E6F: "call 0x41e490", 0x2E6E77: "call 0x369800", 0x2E6E93: "and dword ptr [rdi + 0x24], eax",
                                       0x2E6E96: "and dword ptr [rdi + 0x2c], eax"}),
      "sweep: a lane is released only when requested AND loaded")
# U
c490 = callers(0x41E490)
check("U", c490 == [0x2E6635, 0x2E698C, 0x2E6DDD, 0x2E6E6F, 0x3DC522, 0x3DD3DB, 0x3DD471, 0x3DD882],
      "0041E490 <- %s" % " ".join("%08X" % a for a in c490))
# K
check("K", 0x3DDAB9 in req and min(riprefs(0x3DD850)) == 0x3DDA83 and 0x8C31C0 in ptrs(0x16D6A0) and not callers(0x41E581),
      "sensitivity: each scanner finds a known positive - the call scan 003DDAB9, the rip scan 003DDA83 (lea of 003DD850), the pointer scan .rdata 008C31C0 -> 0016D6A0")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
