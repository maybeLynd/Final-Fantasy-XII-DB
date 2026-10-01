"""DD residue batch 17 (SWE2-STRUCT for OPUS, 2026-10-01): the checks behind the residue answered on one page,
16-UI/Widget-Object-Model/the-widget-message-protocol.md.

Run: python -B b17_checks.py   (last line FAILS n; must be FAILS 0)
Inputs: the certified image through retool.py (sha 73461d08...); the owner pages named by the P checks (read only).

  E1-E4  9a, channel 0: no curve kind decides whether the tween finishes. 00248F40 returns exactly 1.0f
         (01CEBBA8) whenever duration <= elapsed (signed), before it reads the kind; the snap test in 00246C20
         compares the same two values unsigned; the rate is 1.0 or 1.0 / 00229E70(), and 00229E70 never returns
         a value <= 0
  F1-F3  9c, message 8's flag: 00244830 sends {8, flag != 0}; its only two callers pass 1 (002448D0, the pop on
         teardown: focus returns to the previous holder) and 0 (002470D0, the push: a widget takes the focus)
  S1-S4  9f, the 29 sender 002B6DB0: a base procedure that only 002B7B80 calls, with its own self and message; the
         send is in its id-14 arm after it writes +0xD0/+0xD2, +0xD4 = 100, the 002B7210 viewport reconcile and
         +0xD8 = 0x100; 002B7B80 hands 29 back to it, and its id-29 arm rebuilds the clamp rect +0xF8 and re-clamps
         the cursor +0xC8/+0xCC
  L1-L9  9d, message 26's link: the receivers' [self + 0xD8] is the grid list their own layout build created, and
         that list's +0xC8 delegate is the receiver, so the list that sends 26 reads back the origin the receiver
         wrote (005651E0 through 00564010; 005691E0 the same way)
  C1-C5  9 / 8, message 16's senders: the stack/.rdata census reproduces 8's 163 sites and 49 ids (control);
         16 has 20 sites in 20 functions, 3 of them the framework's 00249410 / 002494F0 / 002495C0, which lie above
         widget_messages.py's core band end 00249000; so 17 application senders, still the most of any id; their
         receivers and payloads
  B1-B3  the +0x40 bit 0x20 author: the root procedure 002445D0 sets it on message 1; attach 00248220 copies it
         from the parent and pushes it through the subtree with the 002418E0 visitor; teardown 00245020 tests it
  P1-P8  pointer targets for the STALE and BOUNDARY notes (text present on the named page or record)
"""
import collections, hashlib, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP  # noqa: E402

FAILS = 0
PASSES = 0


def check(name, ok, detail=""):
    global FAILS, PASSES
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if ok:
        PASSES += 1
    else:
        FAILS += 1


SZ = T.sizes()


def ins(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    got = ins(a)
    check(name, text in got, "%08X  %s" % (a, got))


def body(f):
    return list(T.R.md.disasm(T.R.at(f, SZ[f]), f))


def rip_target(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    d = int(m.group(2), 16)
    return i.address + i.size + (d if m.group(1) == "+" else -d)


def u32(a):
    return struct.unpack("<I", T.R.at(a, 4))[0]


def f32(a):
    return struct.unpack("<f", T.R.at(a, 4))[0]


def jt(base_bytes, base_dw, n, image=0x00120000):
    """byte-mapped rel32 table: id i+1 -> image + dword[base_dw + 4*byte[base_bytes + i]]"""
    return {i + 1: image + u32(base_dw + 4 * T.R.at(base_bytes, n)[i]) for i in range(n)}


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")
SC = T.scan()


def callers(f):
    return sorted(SC["calls"].get(f, ()))


# ============================================================ E: channel 0 and the curve kinds
pin("E1 00248F40 compares duration (edx) with elapsed (r8d) first", 0x00248F44, "cmp edx, r8d")
pin("E1 ... and computes a curve only when duration > elapsed (signed jg)", 0x00248F47, "jg 0x248f56")
check("E1 ... otherwise returns the constant 01CEBBA8", rip_target(0x00248F49) == 0x01CEBBA8 and ins(0x00248F51).startswith("add rsp") and ins(0x00248F55) == "ret ")
check("E1 01CEBBA8 is 1.0f exactly", T.R.at(0x01CEBBA8, 4) == b"\x00\x00\x80\x3f")
first_ecx = next(i for i in body(0x00248F40) if "ecx" in i.op_str)
check("E1 the kind (ecx) is first read after the early return", first_ecx.address == 0x00248F6A and first_ecx.mnemonic == "sub",
      "%08X %s %s" % (first_ecx.address, first_ecx.mnemonic, first_ecx.op_str))
pin("E2 kind 1 arm", 0x00248F6D, "je 0x249060")
pin("E2 kind 2 arm", 0x00248F76, "je 0x249023")
pin("E2 t = elapsed / duration", 0x00248F7C, "divss xmm7, xmm1")
pin("E2 kind 3 arm", 0x00248F83, "je 0x248fe8")
pin("E2 kind 4 arm", 0x00248F8B, "je 0x248fc9")
pin("E2 kind 5 is the last compare", 0x00248F8D, "cmp ecx, 1")
pin("E2 every other kind returns t unchanged", 0x00248F90, "jne 0x249074")
check("E2 00249074 returns xmm0 = t (set at 00248F85)", ins(0x00248F85) == "movaps xmm0, xmm7" and ins(0x0024907D) == "ret ")
check("E3 00246C20 holds 1.0f in xmm6 from the same constant", ins(0x00246C5D).startswith("movss xmm6") and rip_target(0x00246C5D) == 0x01CEBBA8)
pin("E3 channel 0 duration = dword [+0x90]", 0x00246CA2, "mov r9d, dword ptr [rbx + 0x90]")
pin("E3 scaled elapsed = cvttss2si(elapsed x rate)", 0x00246CE4, "cvttss2si edi, xmm0")
pin("E3 00248F40(kind, duration, scaled elapsed)", 0x00246CD2, "mov edx, r9d")
pin("E3 ... r8d = the scaled elapsed", 0x00246CE8, "mov r8d, edi")
pin("E3 snap when the eased value is 1.0", 0x00246CF8, "je 0x246d5b")
pin("E3 ... or when duration <= scaled elapsed, UNSIGNED", 0x00246CFA, "cmp dword ptr [rbx + 0x90], edi")
pin("E3 ... (jbe)", 0x00246D00, "jbe 0x246d5b")
pin("E3 finished only on equality with 1.0", 0x00246D7E, "ucomiss xmm6, xmm2")
pin("E3 ... which clears bit 0", 0x00246D8C, "and byte ptr [rbx + 0x80], 0xfe")
for f, one, inv in ((0x002468A0, 0x0024699C, 0x002469DA), (0x00244DD0, 0x00244DE1, 0x00244E0F), (0x00247130, 0x0024721E, 0x0024724C)):
    check("E4 %08X writes rate +0xB8 = 1.0f, or 1.0f / 00229E70()" % f,
          ins(one) == "mov dword ptr [%s + 0xb8], 0x3f800000" % ins(one).split("[")[1].split(" ")[0] and
          ins(inv).startswith("movss dword ptr [rbx + 0xb8], xmm1") and "divss xmm1, xmm0" in ins(inv - 4) and
          rip_target(inv - 12) == 0x01CEBBA8, "%s / %s" % (ins(one), ins(inv)))
pin("E4 constructor default rate 1.0f", 0x00246700, "mov dword ptr [rdi + 0xb8], 0x3f800000")
check("E4 00229E70 returns its global only when 0 < it, else resets it to 1.0f",
      ins(0x00229E7B) == "comiss xmm0, xmm1" and ins(0x00229E7E) == "jb 0x229e91" and rip_target(0x00229E80) == 0x01CEBBA8
      and rip_target(0x00229E88) == rip_target(0x00229E70))

# ============================================================ F: message 8's flag
pin("F1 00244830 keeps the flag (r8d)", 0x0024484B, "mov edi, r8d")
pin("F1 {8, ...}", 0x00244887, "mov dword ptr [rsp + 0x20], 8")
pin("F1 ... a = (flag != 0)", 0x00244891, "setne al")
pin("F1 ... stored at +8", 0x00244898, "mov qword ptr [rsp + 0x28], rax")
check("F2 00244830 has exactly two callers", [c for c, _ in callers(0x00244830)] == [0x002448D0, 0x002470D0], str(callers(0x00244830)))
pin("F2 002448D0 passes flag 1", 0x00244920, "mov r8d, 1")
pin("F2 002470D0 passes flag 0", 0x0024711C, "xor r8d, r8d")
check("F3 002448D0 is the pop: the dying widget is the focus top [0208EBC0], the depth 0208EBC8 drops",
      rip_target(0x002448D6) == 0x0208EBC0 and rip_target(0x0024490A) == 0x0208EBC8 and "dec eax" in ins(0x00244908))
check("F3 ... and the incoming widget is the entry below it on 0208EAC0",
      rip_target(0x002448F4) == 0x0208EAC0 and ins(0x00244919) == "mov rcx, qword ptr [r8 + rcx*8]")
check("F3 002470D0 is the push: 00244640(self), then 00244830([0208EBC0], self, 0)",
      ins(0x00247110) == "call 0x244640" and rip_target(0x00247115) == 0x0208EBC0 and ins(0x0024711F) == "mov rdx, rbx")
check("F3 00245020 runs the pop first", (0x00245020, next(s for c, s in callers(0x002448D0) if c == 0x00245020)) in callers(0x002448D0),
      str([x for x in callers(0x002448D0)]))

# ============================================================ S: the message-29 sender 002B6DB0
pin("S1 002B6DB0 dispatches on the message id", 0x002B6DC8, "mov eax, dword ptr [rdx]")
t6 = jt(0x002B71E4, 0x002B71BC, 0x27)
live = {k: v for k, v in t6.items() if v != 0x002B719B}
check("S1 its id set is 1, 2, 3, 10, 14, 15, 29, 36, 39", sorted(live) == [1, 2, 3, 10, 14, 15, 29, 36, 39], str(sorted(live)))
check("S1 id 14 -> 002B6E1B, id 29 -> 002B6EAA", t6[14] == 0x002B6E1B and t6[29] == 0x002B6EAA)
check("S2 the 29 send is in the id-14 arm, after its writes",
      ins(0x002B6E5F) == "mov word ptr [rbx + 0xd0], ax" and ins(0x002B6E50) == "mov word ptr [rbx + 0xd2], cx"
      and ins(0x002B6E66) == "mov dword ptr [rbx + 0xd4], 0x64" and ins(0x002B6E70) == "call 0x2b7210"
      and ins(0x002B6E22) == "mov edi, 0x100" and ins(0x002B6E75) == "mov word ptr [rbx + 0xd8], di")
check("S2 ... {29} with a zeroed record to its own handler",
      ins(0x002B6E7C) == "mov dword ptr [rsp + 0x38], 0x1d" and ins(0x002B6E8A) == "movdqu xmmword ptr [rsp + 0x40], xmm0"
      and ins(0x002B6E84) == "mov rax, qword ptr [rbx]" and ins(0x002B6E9E) == "mov rcx, rbx" and ins(0x002B6EA1) == "call rax")
check("S2 the +0xD0/+0xD2 pair comes from 00403600 on the +0xC0 child (default 0x100, 0x100)",
      ins(0x002B6E1B) == "mov rdx, qword ptr [rbx + 0xc0]" and ins(0x002B6E41) == "call 0x403600")
cs = callers(0x002B6DB0)
check("S3 only 002B7B80 calls 002B6DB0 (3 sites), so it is a base procedure", sorted(set(c for c, _ in cs)) == [0x002B7B80] and len(cs) == 3, str(cs))
for s in (0x002B7DDD, 0x002B833F, 0x002B8E27):
    check("S3 %08X passes 002B7B80's self (r14) and message (rbx)" % s, ins(s - 6) == "mov rdx, rbx" and ins(s - 3) == "mov rcx, r14")
pin("S3 002B7B80 keeps its message in rbx", 0x002B7BD5, "mov rbx, rdx")
t7 = jt(0x002B8EB0, 0x002B8E70, 0x2A)
check("S3 002B7B80 sends 29 to its default 002B8E21, which calls 002B6DB0", t7[29] == 0x002B8E21 and ins(0x002B8E27) == "call 0x2b6db0")
TSV = os.path.join(DB, "16-UI", "Widget-Object-Model", "widget-message-handlers.tsv")
rows = {l.split("\t")[0]: l.split("\t") for l in open(TSV, encoding="utf-8").read().splitlines()[1:] if l.strip()}
check("S3 002B6DB0 is not a row of the handler table; 002B7B80's row has no 29",
      "002B6DB0" not in rows and "29" not in rows["002B7B80"][6].split(","), rows["002B7B80"][6])
check("S4 the id-29 arm rebuilds the 24px cell rect at +0xF8 (002B6950) from +0x9C/+0x9E and +0xD0/+0xD2",
      ins(0x002B6EB1) == "lea rcx, [rbx + 0xf8]" and ins(0x002B6ED3) == "call 0x2b6950" and
      ins(0x002B6EAA) == "movsx eax, word ptr [rbx + 0xd2]" and ins(0x002B6EB8) == "movsx r9d, word ptr [rbx + 0xd0]")
check("S4 ... and re-clamps the cursor +0xC8 / +0xCC into it",
      ins(0x002B6F69) == "mov dword ptr [rbx + 0xc8], r10d" and ins(0x002B6F72) == "mov dword ptr [rbx + 0xcc], edx")

# ============================================================ L: message 26's link
check("L1 002D14E0 builds the grid list G: 0x150 bytes, handler 002D2DB0",
      ins(0x002D14F4) == "mov ecx, 0x150" and rip_target(0x002D14ED) == 0x002D2DB0 and ins(0x002D14FC) == "call 0x244f50")
check("L1 ... and one 0xC0 child with handler 002D1420 at G + 0xC0",
      ins(0x002D150B) == "mov ecx, 0xc0" and rip_target(0x002D1504) == 0x002D1420 and ins(0x002D1526) == "mov qword ptr [rbx + 0xc0], rax")
check("L1 ... G+0xC8 = descriptor +0x28, G+0xD8 = descriptor +8, G+0x120 = descriptor +0x20",
      ins(0x002D16AC) == "mov rax, qword ptr [rdi + 0x28]" and ins(0x002D16B0) == "mov qword ptr [rbx + 0xc8], rax"
      and ins(0x002D16A1) == "mov rax, qword ptr [rdi + 8]" and ins(0x002D16A5) == "mov qword ptr [rbx + 0xd8], rax"
      and ins(0x002D1696) == "mov rax, qword ptr [rdi + 0x20]" and ins(0x002D169A) == "mov qword ptr [rbx + 0x120], rax")
check("L2 002D1420 (msg 4) runs the senders with r8 = its parent [child + 0x10] = G",
      ins(0x002D1493) == "mov r8, qword ptr [rcx + 0x10]" and ins(0x002D14AE) == "call 0x2d2600" and ins(0x002D14C1) == "call 0x2d28e0")
check("L2 002D2600 and 002D28E0 are called only from 002D1420",
      [c for c, _ in callers(0x002D2600)] == [0x002D1420] and [c for c, _ in callers(0x002D28E0)] == [0x002D1420])
check("L3 002D2600: rbx = G; {26} goes to G's own handler; the cell origin is read back from G +0x114 / +0x116",
      ins(0x002D2647) == "mov rbx, r8" and ins(0x002D278E) == "mov rax, qword ptr [rbx]" and ins(0x002D279B) == "mov rcx, rbx"
      and ins(0x002D279E) == "call rax" and ins(0x002D27C6) == "add cx, word ptr [rbx + 0x114]" and ins(0x002D27E0) == "add cx, word ptr [rbx + 0x116]")
check("L3 ... and the per-cell callback [G+0x120] is called with rcx = [G+0xD8]",
      ins(0x002D265A) == "mov rcx, qword ptr [r8 + 0x120]" and ins(0x002D2829) == "mov rcx, qword ptr [rbx + 0xd8]"
      and ins(0x002D2837) == "call qword ptr [rsp + 0x40]")
pin("L4 G's handler 002D2DB0 hands 26 to its +0xC8 delegate", 0x002D2E11, "mov rcx, qword ptr [rbx + 0xc8]")
check("L5 0029F930 (layout row kind 8): descriptor +0x28 = its r8 (the owner), +8 = 0, +0x20 = 0",
      ins(0x0029F953) == "mov rbp, r8" and ins(0x0029F9AC) == "mov qword ptr [rsp + 0x48], rbp" and ins(0x0029F988) == "lea rcx, [rsp + 0x20]"
      and ins(0x0029F96E) == "xor edx, edx" and ins(0x0029F970) == "mov qword ptr [rsp + 0x28], rdx" and ins(0x0029F9A7) == "mov qword ptr [rsp + 0x40], rdx"
      and ins(0x0029F9B1) == "call 0x2d14e0")
check("L5 ... stores G at the row's +0x18 and links it under the owner",
      ins(0x0029F9B6) == "mov qword ptr [r14 + 0x18], rax" and ins(0x0029F9FB) == "mov rcx, rbp" and ins(0x0029FA14) == "mov rdx, qword ptr [r14 + 0x18]"
      and ins(0x0029FA18) == "call 0x244960")
k8 = 0x00120000 + u32(0x00120000 + 0x123538 + 7 * 4)
check("L6 002432B0: row kind byte +1 = 8 -> 0029F930 with r8 = r13 = its own r9 (the owner)",
      k8 == 0x0024347F and ins(0x0024347F) == "mov r8, r13" and ins(0x00243488) == "call 0x29f930" and ins(0x002432CB) == "mov r13, r9")
w13 = [i for i in body(0x002432B0) if i.op_str.startswith("r13,") and i.address != 0x002432CB]
check("L6 ... and r13 is written nowhere else in 002432B0", not w13, str([(hex(i.address), i.mnemonic) for i in w13]))
check("L6 ... the rows go to the pointer array at (rcx + 0x10), so W + 0x60 for rcx = W + 0x50",
      ins(0x002433AA) == "mov qword ptr [r15 + 0x10], rax" and ins(0x002433E4) == "mov qword ptr [rsi + rcx], rbx")
check("L7 00564010 (the four 00563xxx rows' message-1 helper) builds the layout with itself as owner",
      ins(0x0056403E) == "add rcx, 0x50" and ins(0x00564042) == "mov r9, rbx" and ins(0x00564049) == "call 0x2432b0"
      and [c for c, _ in callers(0x00564010)] == [0x005636F0, 0x00563930, 0x00563B10, 0x00563D20])
check("L7 ... W+0xD8 = [[W+0x60] + i*8] + 0x18 (the row's G), G+0x120 = its callback, G+0xD8 = W",
      ins(0x00564099) == "mov rax, qword ptr [rbx + 0x60]" and ins(0x005640B7) == "mov rcx, qword ptr [rax + rcx*8]"
      and ins(0x005640BF) == "mov rcx, qword ptr [rcx + 0x18]" and ins(0x005640C6) == "mov qword ptr [rbx + 0xd8], rcx"
      and ins(0x005640D1) == "mov qword ptr [rcx + 0x120], rax" and ins(0x005640DB) == "mov rax, qword ptr [rbx + 0xd8]"
      and ins(0x005640E2) == "mov qword ptr [rax + 0xd8], rbx")
for f, j in ((0x005636F0, 0x00563721), (0x00563930, 0x00563953), (0x00563B10, 0x00563B41), (0x00563D20, 0x00563D43)):
    pin("L8 %08X forwards (26 among them) to 005651E0 by tail jump" % f, j, "jmp 0x5651e0")
check("L8 005651E0 keeps self in rdi and writes [self+0xD8] +0x114 / +0x116, then returns 0",
      ins(0x005651EF) == "mov rdi, rcx" and ins(0x00565571) == "mov rcx, qword ptr [rdi + 0xd8]" and ins(0x00565581) == "mov word ptr [rcx + 0x114], ax"
      and ins(0x0056558A) == "mov word ptr [rcx + 0x116], dx" and ins(0x00565588) == "xor eax, eax")
check("L9 005691E0: the same build with itself as owner (002432B0, r9 = self, three layouts)",
      all(ins(a) == "mov r9, rbx" for a in (0x00569306, 0x0056934B, 0x0056938D)) and all(ins(a) == "call 0x2432b0" for a in (0x0056931A, 0x0056935F, 0x005693A1)))
check("L9 ... +0xD8 = row 0's +0x18, its +0x120 = 00568BB0, its +0xD8 = self",
      ins(0x005693F6) == "mov rax, qword ptr [rcx + 0x18]" and ins(0x00569401) == "mov qword ptr [rbx + 0xd8], rax"
      and rip_target(0x005693FA) == 0x00568BB0 and ins(0x00569408) == "mov qword ptr [rax + 0x120], rcx" and ins(0x00569416) == "mov qword ptr [rax + 0xd8], rbx")
check("L9 ... and its 26 callee 00568FE0 writes [self+0xD8] + 0x114",
      ins(0x00568FF1) == "mov rsi, rcx" and ins(0x0056901F) == "mov rax, qword ptr [rsi + 0xd8]" and ins(0x00569028) == "mov dword ptr [rax + 0x114], edx")

# ============================================================ C: message 16's senders (widget_messages.py --senders, re-implemented)
md = T.R.md
md.detail = True
sends = []
for f in sorted(SZ):
    n = SZ[f]
    if n <= 0 or n > 0x20000:
        continue
    try:
        code = list(md.disasm(T.R.at(f, n), f))
    except Exception:
        continue
    pend = {}
    for k, i in enumerate(code):
        m, ops = i.mnemonic, i.operands
        if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_IMM:
            mem = ops[0].value.mem
            if mem.base and mem.index == 0 and 0 <= ops[1].value.imm <= 400 and i.op_str.startswith("dword"):
                pend[(mem.base, mem.disp)] = ops[1].value.imm
        elif m == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG and i.reg_name(ops[0].value.reg) == "rdx" and ops[1].type == X86_OP_MEM:
            mem = ops[1].value.mem
            mid = None
            if mem.base == X86_REG_RIP:
                try:
                    v = u32(i.address + i.size + mem.disp)
                except Exception:
                    continue
                if 0 <= v <= 400:
                    mid = v
            else:
                mid = pend.get((mem.base, mem.disp))
            if mid is None:
                continue
            for j in range(k + 1, min(k + 7, len(code))):
                if code[j].mnemonic == "call" and code[j].operands and code[j].operands[0].type != X86_OP_IMM:
                    sends.append((mid, f, code[j].address))
                    break
check("C1 control: the census reproduces section 8's 163 send sites and 49 distinct ids",
      len(sends) == 163 and len(set(s[0] for s in sends)) == 49, "%d sites, %d ids" % (len(sends), len(set(s[0] for s in sends))))
s16 = sorted((f, c) for mid, f, c in sends if mid == 16)
check("C2 id 16: 20 sites in 20 functions", len(s16) == 20 and len(set(f for f, _ in s16)) == 20)
fw = [f for f, _ in s16 if 0x00244000 <= f < 0x0024A000]
check("C2 three of them are the framework's batch completions 00249410, 002494F0, 002495C0", fw == [0x00249410, 0x002494F0, 0x002495C0], str([hex(x) for x in fw]))
src = open(os.path.join(KIT, "widget_messages.py"), encoding="utf-8").read()
check("C2 ... which lie above widget_messages.py's core band end, so its 'application' count included them",
      "CORE_LO, CORE_HI = 0x00244000, 0x00249000" in src and all(f >= 0x00249000 for f in fw))
APP = [0x002A1FB0, 0x002B6570, 0x002BA040, 0x0037E4F0, 0x0037F190, 0x0037F1F0, 0x0037F340, 0x0037F4D0, 0x003BC3E0,
       0x003C2100, 0x003CB0C0, 0x00553F40, 0x00558FB0, 0x00561390, 0x005770A0, 0x00577180, 0x00577BD0]
app = [f for f, _ in s16 if not (0x00244000 <= f < 0x0024A000)]
check("C3 17 application senders, exactly these", app == APP, str([hex(x) for x in app]))
appc = collections.Counter(mid for mid, f, c in sends if not (0x00244000 <= f < 0x0024A000))
top = appc.most_common(2)
check("C4 16 is still the most widely sent application id (next: %d with %d)" % top[1], top[0] == (16, 17) and top[1][1] < 17, str(top))
check("C5 constant payload records: 00915BB0 = {1, 0}, 00D111C0 = {8, 0}, 00D111D0 = {9, 0}",
      T.R.at(0x00915BB0, 16) == struct.pack("<QQ", 1, 0) and T.R.at(0x00D111C0, 16) == struct.pack("<QQ", 8, 0) and T.R.at(0x00D111D0, 16) == struct.pack("<QQ", 9, 0))
check("C5 {16, 1} from 0037F1F0 and 00577180, {16, 8} from 0037F340, {16, 9} from 0037E4F0 and 0037F4D0",
      rip_target(0x0037F224) == 0x00915BB0 and rip_target(0x005771B6) == 0x00915BB0 and rip_target(0x0037F367) == 0x00D111C0
      and rip_target(0x0037E559) == 0x00D111D0 and rip_target(0x0037F5AB) == 0x00D111D0)
check("C5 0037F1F0, 0037F340, 0037F4D0 and 00577180 send to the object at +0xC0",
      all(ins(a) == "mov rcx, qword ptr [%s + 0xc0]" % r for a, r in ((0x0037F211, "rcx"), (0x0037F358, "rcx"), (0x0037F59C, "rbx"), (0x005771A7, "rbx"))))
check("C5 0037E4F0(w) sends to w: {16, 10} (00D111E0) when [02AED490]+0xE0 bit 7 is set, else stores w at [02AED490]+0xC0 and sends {16, 9}",
      ins(0x0037E505) == "mov rbx, rcx" and rip_target(0x0037E508) == 0x02AED490 and ins(0x0037E51A) == "shr eax, 7"
      and rip_target(0x0037E527) == 0x00D111E0 and T.R.at(0x00D111E0, 16) == struct.pack("<QQ", 10, 0) and ins(0x0037E52F) == "jmp 0x37e561"
      and rip_target(0x0037E536) == 0x02AED490 and ins(0x0037E53D) == "mov qword ptr [rcx + 0xc0], rbx" and ins(0x0037E57C) == "mov rcx, rbx")
for f, entry, call in ((0x002A1FB0, 0x002A1FC9, 0x002A25F6), (0x00553F40, 0x00553F60, 0x00553FD5), (0x00558FB0, 0x00558FCC, 0x005591F4),
                       (0x00561390, 0x005613A9, 0x005617A7)):
    check("C5 %08X sends {16, 0, 0} to its own widget" % f, ins(entry) == "mov rdi, rcx" and ins(call) == "mov rcx, rdi" and ins(call + 3) == "call rax")
check("C5 003CB0C0 builds a 0x1E0 child at its +0xC0, links it, and sends it {16, 0, 0}",
      ins(0x003CB0E3) == "add rcx, 0xc0" and ins(0x003CB0ED) == "mov edx, 0x1e0" and ins(0x003CB0F2) == "call 0x245000"
      and ins(0x003CB100) == "call 0x244960" and ins(0x003CB128) == "mov rcx, rdi" and ins(0x003CB12B) == "call r8")
for f, idst, rec in ((0x002A1FB0, 0x002A25DE, "rsp + 0x40"), (0x002B6570, 0x002B65BD, "rsp + 0x28"), (0x002BA040, 0x002BA106, "rsp + 0x28"),
                     (0x003C2100, 0x003C2149, "rsp + 0x28"), (0x003CB0C0, 0x003CB105, "rsp + 0x28"), (0x00553F40, 0x00553FBC, "rbp - 0x48"),
                     (0x00558FB0, 0x005591DC, "rsp + 0x38"), (0x00561390, 0x0056178F, "rsp + 0x38"), (0x00577BD0, 0x00577BED, "rsp + 0x28")):
    win = [i for i in body(f) if idst - 0x20 <= i.address <= idst + 0x20]
    ok = any(i.mnemonic == "xorps" and i.op_str == "xmm0, xmm0" for i in win) and \
        any(i.mnemonic == "movdqu" and i.op_str == "xmmword ptr [%s], xmm0" % rec for i in win)
    check("C5 %08X: the record's argument words are zeroed (xorps / movdqu [%s])" % (f, rec), ok)
check("C5 003C2100 sends to [arg + 8]; 00577BD0 sends to [02CA9730]",
      ins(0x003C2120) == "mov rdi, rcx" and ins(0x003C2142) == "mov rcx, qword ptr [rdi + 8]" and rip_target(0x00577BE3) == 0x02CA9730)
check("C5 caller-supplied code: 003BC3E0(w, code) and 005770A0(w, code) send {16, code, 0}",
      ins(0x003BC3F8) == "movsxd rax, edx" and ins(0x003BC3FB) == "mov qword ptr [rsp + 0x28], rax" and ins(0x003BC40B) == "mov qword ptr [rsp + 0x30], 0"
      and ins(0x005770B8) == "mov eax, edx" and ins(0x005770BA) == "mov qword ptr [rsp + 0x28], rax" and ins(0x005770CA) == "mov qword ptr [rsp + 0x30], 0")
check("C5 0037F190(w, rec) sends {16, rec[1], rec[1] == 2 ? word rec[4] : 0}",
      ins(0x0037F1A8) == "movzx eax, byte ptr [rdx + 1]" and ins(0x0037F1C2) == "cmp al, 2" and ins(0x0037F1C6) == "movzx eax, word ptr [rdx + 4]")
check("C5 002B6570 / 002BA040 set +0x179D2 bits 0-1 and send {16, 0} to [0209E5C0] / [0209E5F0]",
      rip_target(0x002B6583) == 0x0209E5C0 and rip_target(0x002BA053) == 0x0209E5F0 and ins(0x002B65AF) == "or word ptr [rcx + 0x179d2], 3"
      and ins(0x002BA102) == "or ax, 3")

# ============================================================ B: the +0x40 bit 0x20 author
pin("B1 the root procedure 002445D0 sets bits 0, 1 and 5 on message 1", 0x002445D8, "or dword ptr [rcx + 0x40], 0x23")
check("B2 attach 00248220 copies bit 5 from the parent to the child",
      ins(0x0024826B) == "test byte ptr [rbx + 0x40], 0x20" and ins(0x00248271) == "or dword ptr [rdx + 0x40], 0x20")
lea_vis = [i for i in body(0x00248220) if i.mnemonic == "lea" and "rip" in i.op_str and rip_target(i.address) == 0x002418E0]
check("B2 ... and runs 002463F0 with the visitor 002418E0 (bit 5 = argument & 1) over the subtree",
      bool(lea_vis) and ins(0x002482A0) == "call 0x2463f0" and ins(0x002418E0) == "and dword ptr [rcx + 0x40], 0xffffffdf" and ins(0x002418E7) == "shl edx, 5")
pin("B3 teardown 00245020 tests bit 5 (kept, not released)", 0x00245072, "test byte ptr [rdi + 0x40], 0x20")

# ============================================================ P: pointer targets


def page(rel):
    return open(os.path.join(DB, rel), encoding="utf-8").read()


ME = page("16-UI/Widget-Object-Model/the-widget-message-protocol.md")
check("P1 285: the licence-board page answers it (GI-3)", "**Id 285 (`0x11D`) is the reply a shared dialog posts to the widget that opened it:**"
      in page("16-UI/License-Board-View/the-license-board-screen-widgets.md"))
check("P2 289: the gambit page reads it as the list's destroy notice to its editor child",
      "| 0x121 | `00569EE3` (peeled `cmp`/`je`, not a table entry) | parent-destroy notification" in page("16-UI/Gambit-Screens/the-gambit-screens.md"))
check("P3 287: the Config page reads 00280DE0's arm", "Id `0x11F` is the batch twin" in page("16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md"))
check("P4 00393460 / 003933F0: the typed-list page's call chain",
      "-> 00393460 -> 002493D0 -> 0024A4E0 (register 'dataface_c')" in page("02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md"))
astra = page("_index/candidates/fable-astra-live-facts-0930/README.md")
check("P5 the snapshot-reader order: FABLE's static pass is recorded and the rest is run-time object state",
      "WHERE-THE-SNAPSHOT-READERS-SIT-RELATIVE-TO-THE-ARBITER" in astra and "snap_order.py" in astra and "run-time object state" in astra)
for k, t in (("P6 11 named from its sender", "**Message 11 is named from its sender — 2026-09-25"),
             ("P6 26 named", "**Message 26 is a per-cell pre-draw hook — named 2026-09-25"),
             ("P6 30 dispositioned", "**Message 30 is application-defined, not a framework message — dispositioned 2026-09-25"),
             ("P6 53 named", "### 9e. Message 53 is a destroy request"),
             ("P6 the clip suspension's raiser found", "**Found — it is in a different message, which is why no body balanced.**"),
             ("P6 DL-3 answered", "**`DL-3` answered 2026-09-13 (FABLE): the order is not guaranteed.**"),
             ("P6 the stale walker's release branch read", "- **bit 10 set** — a widget kept by teardown (below) — it caches the next sibling"),
             ("P6 1, 2, 15, 18 named from their senders", "## 9. The lifecycle, end to end")):
    check(k, t in ME)
b10 = page("_index/candidates/swe2contract-ddres-b10-0930/README.md")
check("P7 every handler's id set is read (DD batch 10, W1-W3)", "W1–W4" in b10 and "264 exact rows, 0 upper-bound rows and 3 unparsed rows" in b10)
check("P8 DL-1 answered for the whole recount (section 7 correction)", "`DL-1` was answered on 2026-09-25 for every id of the 56-id recount" in ME)

print("PASSES %d" % PASSES)
print("FAILS %d" % FAILS)
