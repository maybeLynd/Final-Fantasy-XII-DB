"""teardown.py - PKG-GP-SPAWN-RESPAWN items P7 and P8: when a dead body is torn down, and when its slot is released (FABLE, Claude
Opus 5.5, 2026-09-29). STATIC, certified image.

  G  THE TEARDOWN GATE in the idle path of the per-unit frame (002340B4..00234100): the unit is torn down
     (BattleUnit_TeardownAndDespawn 00300E40, edx = 0) only when ALL hold: unit qword bit 33 (set by the reaction handler on the
     death events), byte +4 bit 2 = qword bit 34, and "result" - where result = 00322310(p) || !003228E0(p) with
     p = 0030CA50(unit) (the presentation-slot record's dword +0x24, the slot index being unit byte +0x695, or -1). Both
     predicates query 0024DE70(p), the encoded-id class state: 00322310 is 1 for a missing handle (p in {0, -1}) or state 0;
     003228E0 is state >= 3. So the body waits while its presentation handle's state is >= 3
  K  BIT 34 is set by BattleUnit_HandleActorTimelineEvent 00319F50: its kind switch (dword [event], 0..8, table read here) sends
     kind 6 to 0031A198 (sets bit 34 unconditionally) and kind 4 to 0031A100, which sets it at 0031A147 behind the field-bit
     query 00313F60
  R  THE SLOT RELEASE ActorSystem_ReleaseBattleUnitSlotForActor 00234200 has one rel32 caller, 0025B225, inside the fragment
     0025B205 of ActorSystem_ReleaseManagerRecords 0025B070: for an actor record with byte +0x14 >= 0x80 and a bound unit (+0x30)
     - i.e. the release is part of the actor system's record release, not of death
  P  THE POSTERS (added 2026-09-29): every rel32 field in the image (call, jmp, jcc, rip-relative operand) that resolves to
     00319F50 or to its wrapper 002EB740 is listed. The handler is reached only by the wrapper's tail jmp 002EB77B; the wrapper
     has six call sites, two in 002FC010 and four in the action-timeline interpreter 003B8670 (BQ-12)
  T  WHICH TIMELINE OPCODE POSTS WHICH KIND: 003B8670's opcode byte (1..0x80) -> byte map image+0x29994C -> jump table
     image+0x299854. Opcode 3 -> kind 0 (ebp = 0), 13 -> kind 1 (r12d = 1), 26 -> kind 3 / 6 / 7 / 8 for entry dword +4 = 0 / 1 /
     2 / 3, 34 -> kind 2, 37 -> kind 4. Every one of these posts passes the action context's acting unit ([ctx] +8) as the
     wrapper's first id and 0 as the second
  U  THE UNIT THAT GETS BIT 34 is the handler's first argument's battle unit (rbx = 00263E30(rcx)), i.e. the acting unit
  Not claimed: which authored tracks carry opcode 26 with +4 = 1 or opcode 37 (a data census of the per-action tracks); that
  no other code sets bit 34 (no image-wide writer census of qword bit 34 was run); what the class states mean.
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(a) + (b - a)], a)}
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
g = dis(0x2340B9, 0x234105); p1 = dis(0x322310, 0x322341); p2 = dis(0x3228E0, 0x322913); ca = dis(0x30CA50, 0x30CA7B)
G = at(g, {0x2340BC: "call 0x30ca50", 0x2340C5: "call 0x322310", 0x2340CC: "jne 0x2340dd", 0x2340D0: "call 0x3228e0",
           0x2340D7: "je 0x2340dd", 0x2340DD: "mov eax, 1", 0x2340E2: "movabs rcx, 0x200000000", 0x2340F1: "test byte ptr [rbx + 4], 4",
           0x2340FB: "xor edx, edx", 0x234100: "call 0x300e40"}) \
    and at(p1, {0x322316: "lea eax, [rcx + 1]", 0x32231B: "cmp eax, 1", 0x322320: "call 0x24de70", 0x322327: "sete bl"}) \
    and at(p2, {0x3228F0: "call 0x24de70", 0x3228F5: "cmp eax, 3", 0x3228F8: "setge bl"}) \
    and at(ca, {0x30CA50: "movzx eax, byte ptr [rcx + 0x695]", 0x30CA57: "cmp al, 0x1f", 0x30CA73: "mov eax, dword ptr [rcx + 0x24]"})
def result(p, state): return (p in (0, -1)) or state == 0 or not (state >= 3)
check("G", G and result(-1, 9) and result(5, 2) and not result(5, 3),
      "teardown needs bit 33, bit 34 and a presentation state below 3 (or no handle): %s" % G)
base = 0x319FCC - 0x1F9FCC; tab = base + 0x1FA200
kinds = [base + struct.unpack_from("<I", d, off(tab) + 4 * i)[0] for i in range(9)]
k6 = dis(0x31A198, 0x31A1A4); k4 = dis(0x31A13A, 0x31A14B)
check("K", kinds[6] == 0x31A198 and kinds[4] == 0x31A100 and k6.get(0x31A198) == "or dword ptr [rbx + 4], 4"
      and k4.get(0x31A13A) == "call 0x313f60" and k4.get(0x31A147) == "or dword ptr [rbx + 4], 4",
      "timeline kinds -> %s; kind 6 and kind 4 set bit 34" % ["%08X" % k for k in kinds])
hits = []
for vs, va, rs, ro in SECS:
    blob = d[ro:ro + rs]
    for i in range(len(blob) - 5):
        if blob[i] in (0xE8, 0xE9) and B + va + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == 0x234200: hits.append(B + va + i)
r = dis(0x25B212, 0x25B232)
check("R", hits == [0x25B225] and at(r, {0x25B212: "cmp byte ptr [rax + 0x14], 0x80", 0x25B218: "cmp qword ptr [rax + 0x30], 0",
                                         0x25B225: "call 0x234200", 0x25B22D: "call 0x2eb780"}),
      "00234200 callers %s; gated on record +0x14 >= 0x80 and a bound unit" % ["%08X" % h for h in hits])
# P: every rel32 field, of any instruction form, that resolves to the handler or its wrapper
T = {0x319F50: [], 0x2EB740: []}
for vs, va, rs, ro in SECS:
    blob = d[ro:ro + rs]
    for i in range(1, len(blob) - 4):
        r = struct.unpack_from("<i", blob, i)[0]
        for extra in (0, 1, 4):
            t = B + va + i + 4 + extra + r
            if t in T: T[t].append(B + va + i - 1)
wrap = dis(0x2EB740, 0x2EB780)
check("P", T[0x319F50] == [0x2EB77B] and wrap.get(0x2EB77B) == "jmp 0x319f50"
      and T[0x2EB740] == [0x2FC103, 0x2FC158, 0x3B887D, 0x3B8988, 0x3B8A1C, 0x3B9208],
      "handler reached from %s; wrapper called from %s" % (["%08X" % a for a in T[0x319F50]], ["%08X" % a for a in T[0x2EB740]]))
# T: opcode -> arm, and each arm's kind store and post
lin = {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(0x3B8670):off(0x3B9300)], 0x3B8670)}
bmap, jt = B + 0x29994C, B + 0x299854
arm = lambda op: B + struct.unpack_from("<I", d, off(jt) + 4 * d[off(bmap) + op - 1])[0]
want_arms = {3: 0x3B87E7, 13: 0x3B894E, 26: 0x3B89A9, 34: 0x3B91AE, 37: 0x3B9234}
stores = {0x3B8822: "mov dword ptr [rsp + 0x30], ebp", 0x3B895F: "mov dword ptr [rsp + 0x30], r12d",
          0x3B89A9: "mov ecx, dword ptr [rbx + 4]", 0x3B89ED: "mov dword ptr [rsp + 0x30], 3",
          0x3B89D7: "mov dword ptr [rsp + 0x30], 6", 0x3B89CD: "mov dword ptr [rsp + 0x30], 7",
          0x3B89C3: "mov dword ptr [rsp + 0x30], 8", 0x3B91B5: "mov dword ptr [rsp + 0x30], 2",
          0x3B923B: "mov dword ptr [rsp + 0x30], 4", 0x3B926A: "jmp 0x3b91fb", 0x3B9208: "call 0x2eb740",
          0x3B86CD: "xor ebp, ebp", 0x3B86F2: "lea r12d, [rbp + 1]",
          0x3B8A13: "mov ecx, dword ptr [r9 + 8]", 0x3B8A11: "xor edx, edx", 0x3B9206: "xor edx, edx"}
got_arms = {op: arm(op) for op in want_arms}
check("T", got_arms == want_arms and at(lin, stores),
      "opcode -> arm %s; kinds 0/1/2/3/4/6/7/8 stored as read" % {op: "%08X" % a for op, a in got_arms.items()})
h = dis(0x319F89, 0x319FA0)
check("U", h.get(0x319F92) == "call 0x263e30" and h.get(0x319F97) == "mov rbx, rax" and k6.get(0x31A198) == "or dword ptr [rbx + 4], 4",
      "bit 34 is set on 00263E30(first argument)")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
