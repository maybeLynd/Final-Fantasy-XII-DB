"""gg1_msg31.py - GG-1: the message-31 reader 003CAB00 reads the snapshot inside the arbiter, just before its first clear
(FABLE, Claude Opus 5.5, 2026-09-28). Static; companion to ../gg1-message10-readers/ (whose decoder and census this
imports) and ../gg1-chain-procs/.

  S1  003CAB00's jump table sends message 31 to 003CAC6A, and both of its reads of 02F9736A (003CAC80, 003CACBA) lie in
      that arm, tested against the masks 0029DBE0 returns for actions 0x10E and 0x10D
  S2  the census used for message 10 (constant stack records passed in rdx; .rdata records loaded into rdx) finds three
      {31} builders and no .rdata record: 003CA200, 00551E00, 00551F00
  S3  003CA200 calls the proc stored at [[02B47758] + 0x2A0] with rcx = [02B47758] + 0x2A0.
      - 02B47758 is stored only by 003CA280, with the window 00244F50 creates for the proc 003CA860.
      - the window initialiser 00245000 -> 002465F0 stores its r8 argument (the proc) at [window + 0]
      - 003CA860 creates its +0x2A0 child window with the proc 003CAB00 (003CA913, the only reference to 003CAB00) and
        links it under itself (00244960 at 003CA93A)
  S4  00551E00 and 00551F00, installed only by 005528C0, send their {31} through 00275440 on their own window. 00275440
      walks that window's child list ([rcx + 0x10], then each child's + 0x10)
  S5  003CA200's only caller is the arbiter 00253C70 at 00253F6B. The next instruction, 00253F70, is the first of the
      arbiter's five clears of 02F9736A
  C1  control: the decoder reads 003CAB00's message 1 arm as 003CAB54, the instruction after the table jump
  C2  control: the same census finds the known message-12 sender 00247510's store at 00247523
Limit: a message record that is copied from elsewhere (a queue, an argument) instead of built by constant stores is outside
the census, as it was for message 10.
"""
import os, re, struct, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, "../gg1-message10-readers/gg1_msg10_readers.py"), encoding="utf-8").read().split("def is_read")[0])
def is_read(s): return "=>02F9736A" in s and not (s.startswith("mov") and "ptr [rip" in s.split(",")[0])
def census(v):
    st, rr = [], []
    for f, ins in body.items():
        for i, (a, s) in enumerate(ins):
            m = re.match(r"mov dword ptr \[rsp \+ (0x[0-9a-f]+)\], (0x[0-9a-f]+|\d+)$", s)
            if m and int(m.group(2), 0) == v and any(re.match(r"lea rdx, \[rsp \+ %s\]$" % m.group(1), s2) for a2, s2 in ins[i + 1:i + 14]):
                st.append((f, "%08X" % a))
            m = re.match(r"lea rdx, \[rip [^\]]*\] ; =>([0-9A-F]{8})$", s)
            if m:
                b = rd(int(m.group(1), 16), 4)
                if b and len(b) == 4 and struct.unpack("<I", b)[0] == v: rr.append((f, "%08X" % a))
    return sorted(st), rr
arms = decode("003CAB00")
reads = [a for a, s in body["003CAB00"] if is_read(s)]
starts = sorted(set(arms.values()))
arm_of = {a: max(t for t in starts if t <= a) for a in reads}
masks = [s for a, s in body["003CAB00"] if 0x003CAC76 <= a <= 0x003CACB5 and s.startswith("mov ecx, 0x10")]
ok("S1", arms[31] == 0x003CAC6A and reads == [0x003CAC80, 0x003CACBA] and set(arm_of.values()) == {0x003CAC6A}
   and [m for m, t in arms.items() if t == 0x003CAC6A] == [31] and masks == ["mov ecx, 0x10e", "mov ecx, 0x10d"],
   "003CAB00: message 31 -> 003CAC6A (and only 31); reads %s in that arm, against action masks 0x10E / 0x10D" % ["%08X" % a for a in reads])
st31, rr31 = census(31)
ok("S2", [f for f, a in st31] == ["003CA200", "00551E00", "00551F00"] and not rr31, "{31} builders: %s; .rdata {31} in rdx: %s" % (st31, rr31))
s200 = [s for a, s in body["003CA200"]]
w = sorted((f, "%08X" % a) for f, ins in body.items() for a, s in ins if s.startswith("mov qword ptr [rip") and "=>02B47758" in s)
s280 = [s for a, s in body["003CA280"]]
refs_ab00 = [(f, "%08X" % a) for f, ins in body.items() for a, s in ins if "=>003CAB00" in s]
s860 = {a: s for a, s in body["003CA860"]}
ok("S3", "mov rax, qword ptr [rbx + 0x2a0]" in s200 and "lea rcx, [rbx + 0x2a0]" in s200 and "call rax" in s200
   and w == [("003CA280", "003CA2A4"), ("003CA2B0", "003CA2C5")] and any("=>003CA860" in s for s in s280) and "call 0x244f50" in s280
   and refs_ab00 == [("003CA860", "003CA913")] and s860.get(0x003CA92B) == "call 0x245000" and s860.get(0x003CA93A) == "call 0x244960"
   and s860.get(0x003CA930) == "lea rdx, [rdi + 0x2a0]" and "call 0x2465f0" in [x for a, x in body["00245000"]]
   and {0x00246607: "mov rbx, r8", 0x0024661D: "mov rdi, rcx", 0x00246641: "mov qword ptr [rdi], rbx"}.items() <= {a: x for a, x in body["002465F0"]}.items(),
   "003CA200 calls the proc at [[02B47758] + 0x2A0]; 02B47758 stored by %s (003CA2B0 stores 0); 003CA860 creates the +0x2A0 window with 003CAB00 %s and links it under itself" % (w, refs_ab00))
inst = sorted((f, "%08X" % a) for f, ins in body.items() for a, s in ins if "=>00551E00" in s or "=>00551F00" in s)
b440 = [s for a, s in body["00275440"]]
def sends_self(f):
    ins = body[f]
    return any(s == "call 0x275440" and any(x == "mov rcx, rdi" for y, x in ins[max(0, i - 6):i]) for i, (a, s) in enumerate(ins)) and ("mov rdi, rcx" in [s for a, s in ins[:12]])
ok("S4", inst == [("005528C0", "005530DA"), ("005528C0", "005534C5")] and all(sends_self(f) for f in ("00551E00", "00551F00"))
   and "mov rbx, qword ptr [rcx + 0x10]" in b440 and "mov rbx, qword ptr [rbx + 0x10]" in b440 and "call rax" in b440,
   "00551E00/00551F00 installed only by 005528C0 (%s); they send {31} through 00275440 on their own window, which walks its child list" % inst)
callers = sorted((f, "%08X" % a) for f, ins in body.items() for a, s in ins if re.match(r"(call|jmp) 0x3ca200$", s))
arb = {a: s for a, s in body["00253C70"]}
ok("S5", callers == [("00253C70", "00253F6B")] and "=>02F9736A" in arb.get(0x00253F70, "") and arb[0x00253F70].startswith("mov word ptr [rip") and arb[0x00253F70].split(";")[0].split(",")[1].strip() == "di",
   "003CA200's only caller is the arbiter at 00253F6B; 00253F70 = %r" % arb.get(0x00253F70))
ok("C1", arms[1] == 0x003CAB54, "control: 003CAB00's message 1 arm is 003CAB54, right after the table jump")
st12, rr12 = census(12)
ok("C2", ("00247510", "00247523") in st12, "control: the census finds 00247510's {12} store at 00247523 (%d {12} builders)" % len(st12))
print("FAILS", fails); sys.exit(1 if fails else 0)
