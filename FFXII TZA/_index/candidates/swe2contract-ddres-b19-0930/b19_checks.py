"""DD prose-residue batch 19 (SWE2-CONTRACT for OPUS, 2026-10-01): the SD-7 and SD-107 pages.

  15-Input/Input-Stack/input-stack-device-channel-and-bindings.md            (SD-7 box)
  99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md (SD-107 box)

Run: python -B b19_checks.py   (last line FAILS n; must be FAILS 0)
Inputs: the certified image through Database/Tools/analysis-kit/gfz-scripts/retool.py (sha 73461d08...), the register
_index/OPEN-QUESTIONS.md, the answer records under _index/candidates/, git (the publishing commit), and the two pages.
Static only; nothing is executed and nothing is live. This checker does not read or pin either page's status line.

K1-K3  the SD-7 / SD-107 record: published in 59ec09a95, its checker output ends FAILS 0, and it states both answers
A1-A7  SD-7, re-derived independently of the record's own census (the answer note's facts):
       A1 no direct call/jmp targets 0017D1A0; A2 no rip-relative reference names it; A3 the only image qword equal to
       0017D1A0 is 008C57D8 = slot 15 (+0x78) of the GameApplication vtable 008C5760 (RTTI), with a positive control
       (qword_sites finds PrimitiveRendererD3D11's slot 15 006CAB80 at 00D869D8); A4 001989D0 is
       `mov byte [rcx+0x39], dl / ret`; A5 its direct callers are exactly 0017D1A0 (0017D1C5) and 001E0FB0 (001E0FD7);
       A6 001E0FB0 forwards (ecx != 0) and is called only at 002292AD and 00393D33, each after `xor ecx, ecx`, with no
       qword or rip reference to it; A7 0017D1A0 forwards its own argument (movzx ebx, dl) to 001989D0
B1-B4  SD-107 and the column-2 pointer (independent of the record):
       B1 image-wide, the immediate byte stores at [reg+0xA3] are exactly five: 002A49CA=3, 002B3470=2, 002B3C40=0,
       002B3D78=0, 007E7401=1 (the four text builders are the positive control); B2 the only immediate 1 is in 007E73F0,
       which is none of the text-element builders; B3 no rip reference names 009164D0, while 009164C0 has one lea and
       009164C8 two (control) - the "Controls" zero stands; B4 002AF960 reaches column 2 through the image base
       (002AFB6C lea rdi -> 00120000; 002AFCB1 call [rdi + r9*8 + 0x7f64d0] = 009164D0)
P1-P3  the pointer notes' sources: the register rows they cite are ANSWERED; the answer records exist (SD-5's census
       control passes, SD-106 ends FAILS 0);
       the instructions the pointers cite (001DFA70, 0035FC87, 00607DA8, 005FE1F0) are as stated
Z1-Z4  the pages: every batch-19 note is present where the README says, the SD-7 / SD-107 notes sit inside their own
       box items, no batch-19 line carries a strike, and every line of both pages is LF
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TZA = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DB = os.path.abspath(os.path.join(TZA, ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

R, SC, SZ = T.R, T.scan(), T.sizes()
CAND = os.path.join(TZA, "_index", "candidates")
REG = os.path.join(TZA, "_index", "OPEN-QUESTIONS.md")
P1 = os.path.join(TZA, "15-Input", "Input-Stack", "input-stack-device-channel-and-bindings.md")
P2 = os.path.join(TZA, "99-Unresolved-Residual", "Glyph-Run-Rendering", "the-text-element-dispatch-table.md")
TAG = "DD batch 19"
FAILS = 0
PASSES = 0


def check(name, ok, detail=""):
    global FAILS, PASSES
    print(("PASS " if ok else "FAIL ") + name + (" - " + str(detail) if detail != "" else ""))
    if ok:
        PASSES += 1
    else:
        FAILS += 1


def ins(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def pin(name, a, text):
    t = ins(a)
    check(name, t == text, "%08X  %s" % (a, t))


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def before(f, site, k=1):
    L = body(f)
    j = [n for n, i in enumerate(L) if i.address == site][0]
    return L[j - k]


def last_line(p):
    t = open(p, encoding="utf-8").read().strip().splitlines()
    return t[-1] if t else ""


callers = lambda a: sorted(SC["calls"].get(a, ()))

# ============================================================ K: the SD-7 / SD-107 record
REC = os.path.join(CAND, "sd7-sd107-closure-0930")
names = subprocess.run(["git", "-C", TZA, "show", "--name-only", "--format=%h", "59ec09a95"],
                       capture_output=True, text=True).stdout
check("K1 commit 59ec09a95 publishes the sd7-sd107-closure-0930 record (README, checker, .out)",
      all(("sd7-sd107-closure-0930/" + n) in names for n in ("README.md", "sd7_sd107_closure.py", "sd7_sd107_closure.out")),
      names.split("\n")[0])
out = open(os.path.join(REC, "sd7_sd107_closure.out"), encoding="utf-8").read()
check("K2 the record's checker output ends FAILS 0", last_line(os.path.join(REC, "sd7_sd107_closure.out")) == "FAILS 0")
rd = " ".join(open(os.path.join(REC, "README.md"), encoding="utf-8").read().split())   # the README wraps lines
check("K3 the record states both answers (SD-7 CLOSED: slot 15 called nowhere; SD-107: kind 1 has no traced writer)",
      "**SD-7 CLOSED.**" in rd and "called **nowhere**" in rd and "kind 1 still has no traced writer" in rd.lower()
      and "S8" in out and "T5" in out)

# ============================================================ A: SD-7, independently
check("A1 no direct call/jmp targets 0017D1A0", not SC["calls"].get(0x0017D1A0), callers(0x0017D1A0))
check("A2 no rip-relative reference names 0017D1A0", not SC["refs"].get(0x0017D1A0))
qs = T.qword_sites(0x0017D1A0)
vt, cls = T.vtable_start(0x008C57D8)
check("A3 the only image qword equal to 0017D1A0 is 008C57D8 = GameApplication vtable 008C5760 slot 15 (+0x78)",
      qs == [0x008C57D8] and vt == 0x008C5760 and cls == "GameApplication" and (0x008C57D8 - vt) == 0x78,
      "%s vt=%s %s" % (["%08X" % x for x in qs], "%08X" % vt if vt else None, cls))
ctl = T.qword_sites(0x006CAB80)
check("A3c control: qword_sites finds PrimitiveRendererD3D11 (00D86960) slot 15 006CAB80 at 00D869D8",
      0x00D869D8 in ctl and T.rtti_class(0x00D86960) == "PrimitiveRendererD3D11", ["%08X" % x for x in ctl])
check("A4 001989D0 is `mov byte ptr [rcx + 0x39], dl / ret` (the +0x39 poll-gate setter)",
      ins(0x001989D0) == "mov byte ptr [rcx + 0x39], dl" and ins(0x001989D3) == "ret")
c5 = callers(0x001989D0)
check("A5 001989D0's direct callers are exactly 0017D1A0 (0017D1C5) and 001E0FB0 (001E0FD7)",
      c5 == [(0x0017D1A0, 0x0017D1C5), (0x001E0FB0, 0x001E0FD7)], [("%08X" % f, "%08X" % s) for f, s in c5])
c6 = callers(0x001E0FB0)
ok6 = c6 == [(0x00228C70, 0x002292AD), (0x003939B0, 0x00393D33)]
pre = [before(f, s, 1 if s == 0x00393D33 else 2) for f, s in c6] if ok6 else []
check("A6 001E0FB0 is called only at 002292AD (00228C70) and 00393D33 (003939B0), each with ecx = 0 (xor ecx, ecx)",
      ok6 and all(("%s %s" % (i.mnemonic, i.op_str)) == "xor ecx, ecx" for i in pre),
      [("%08X" % f, "%08X" % s) for f, s in c6] + ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in pre])
check("A6b 001E0FB0 forwards (ecx != 0) as dl and has no qword or rip reference",
      ins(0x001E0FC4) == "setne bl" and ins(0x001E0FCF) == "movzx edx, bl" and ins(0x001E0FD7) == "jmp 0x1989d0"
      and not T.qword_sites(0x001E0FB0) and not SC["refs"].get(0x001E0FB0))
check("A7 slot 15 0017D1A0 forwards its own argument: movzx ebx, dl (0017D1AA) and calls 001989D0 at 0017D1C5",
      ins(0x0017D1AA) == "movzx ebx, dl" and ins(0x0017D1C5) in ("call 0x1989d0", "jmp 0x1989d0"), ins(0x0017D1C5))

# ============================================================ B: SD-107 and the column-2 pointer
imm = {}
for f, n in SZ.items():
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        if (i.mnemonic == "mov" and len(i.operands) == 2 and i.operands[0].type == 3 and i.operands[0].size == 1
                and i.operands[0].mem.disp == 0xA3 and i.operands[0].mem.base != T.RIP and i.operands[1].type == 2):
            imm[i.address] = (f, i.operands[1].imm)
want = {0x002A49CA: (0x002A4830, 3), 0x002B3470: (0x002B3400, 2), 0x002B3C40: (0x002B3C30, 0),
        0x002B3D78: (0x002B3D50, 0), 0x007E7401: (0x007E73F0, 1)}
check("B1 image-wide immediate byte stores at [reg+0xA3] are exactly five (the four text builders 0/0/2/3 + 007E7401 = 1)",
      imm == want, {"%08X" % a: ("%08X" % f, v) for a, (f, v) in sorted(imm.items())})
ones = [(a, f) for a, (f, v) in imm.items() if v == 1]
check("B2 the only immediate 1 is in 007E73F0, which is none of the text-element builders (002B3C30/002B3D50/002A4830/002B3400)",
      ones == [(0x007E7401, 0x007E73F0)] and 0x007E73F0 not in (0x002B3C30, 0x002B3D50, 0x002A4830, 0x002B3400))
r0, r8, r10 = SC["refs"].get(0x009164C0, set()), SC["refs"].get(0x009164C8, set()), SC["refs"].get(0x009164D0, set())
check("B3 no rip reference names 009164D0 (column 2); control: 009164C0 has 1 lea, 009164C8 has 2",
      not r10 and len(r0) == 1 and len(r8) == 2 and all(k == "lea" for _, _, k in r0 | r8), (len(r0), len(r8), len(r10)))
check("B4 002AF960 indexes column 2 through the image base: 002AFB6C lea rdi -> 00120000; 002AFCB1 call [rdi+r9*8+0x7f64d0]",
      ins(0x002AFB6C) == "lea rdi, [rip - 0x18fb73]" and 0x002AFB6C + 7 - 0x18FB73 == 0x00120000
      and ins(0x002AFCB1) == "call qword ptr [rdi + r9*8 + 0x7f64d0]" and 0x00120000 + 0x7F64D0 == 0x009164D0)

# ============================================================ P: the pointer notes' sources
reg = {}
for ln in open(REG, encoding="utf-8").read().splitlines():
    m = re.match(r"^\|\s*([A-Z]{1,3}-\d+)\s*\|", ln)
    if m:
        reg.setdefault(m.group(1), ln)
answered = ["SD-5", "SD-6", "SD-8", "SD-9", "SD-106", "AU-1", "AU-5", "AV-6", "AP-8", "AP-9", "GJ-7", "GJ-8", "GJ-11", "BG-11"]
bad = [k for k in answered if k not in reg or "ANSWERED" not in reg[k]]
check("P1 the register rows the pointers cite are ANSWERED: " + ", ".join(answered), not bad, bad)
st = {k: ("PARTIAL" if "**PARTIAL" in reg.get(k, "") else "OPEN" if "**OPEN" in reg.get(k, "") else "ANSWERED"
          if "ANSWERED" in reg.get(k, "") else "?") for k in ("SD-7", "SD-107")}
print("INFO register state now (SWE2-DATA restates; not a check): %s" % st)
s5 = os.path.join(CAND, "sd5-display-requests-0930", "sd5_display_requests.out")   # a census: no FAILS line, control P
s106 = os.path.join(CAND, "sd106-measure-sites-0930", "sd106_sites.out")
okr = {"sd5-display-requests-0930": os.path.isfile(s5) and "PASS  P " in open(s5, encoding="utf-8").read(),
       "sd106-measure-sites-0930": os.path.isfile(s106) and last_line(s106) == "FAILS 0"}
okr.update({d: os.path.isfile(os.path.join(CAND, d, "README.md"))
            for d in ("sd6-recorded-input-0930", "sd8-dispatcher-mode-0930", "sd9-input-deadline-0930")})
check("P2 the cited answer records exist (SD-5 census control P passes; SD-106 output ends FAILS 0)", all(okr.values()), okr)
check("P3a AU-1: 001DFA70 is `cmp dword ptr [rcx + 0x64], 0 / sete al / ret`",
      ins(0x001DFA70) == "cmp dword ptr [rcx + 0x64], 0" and ins(0x001DFA74) == "sete al" and ins(0x001DFA77) == "ret")
pin("P3b AP-8: the repeat filter stores its word at frame + 8 + 2*set", 0x0035FC87, "mov word ptr [r15 + r14*2 + 8], r10w")
check("P3c 00607DA8 takes the thread start 005FE1F0 (lea rdx), and 005FE1F0 is `jmp 006106A0`",
      ins(0x00607DA8) == "lea rdx, [rip - 0x9bbf]" and 0x00607DA8 + 7 - 0x9BBF == 0x005FE1F0
      and ins(0x005FE1F0) == "jmp 0x6106a0")

# ============================================================ Z: the pages
def lines(p):
    return open(p, "rb").read().decode("utf-8").split("\n")


def has(p, anchor):
    """the first line holding `anchor` carries a batch-19 note on it or on the next two lines"""
    L = lines(p)
    for n, t in enumerate(L):
        if anchor in t:
            return any(TAG in x for x in L[n:n + 3]), n + 1
    return False, None


z1 = {
    P1: ["What stays open is registered as SD-5 to", "Whether one can stay set across frames is not read.",
         "The caller of slot 15 is not identified.", "title state did poll.", "What stays open is SD-5 to SD-9.",
         "The 36-byte total and the 660-byte record are unchanged", "**AU-1: read `0x001DFA70`.**",
         "and CodeDomain tags, not yet behaviour.", "the installer is not yet located.", "the arms' real dispatch"],
    P2: ["but no builder has been found, so no shipped text is known to use it (SD-107)",
         "*Not named:* what the five `002B3280` sites display.", "kind 1's instantiation path is the honest residual.",
         "domain is now bounded by what is actually authored", "selector of 2, or ≥4, at `002AFCB1` is a wild call",
         "comes from an instrument that demonstrably reports non-zero", "so the precondition is recorded as unproven",
         "dispatcher references column 2 by address\", which this pass did **not** re-derive"],
}
for p, anchors in z1.items():
    res = [(a[:40], has(p, a)) for a in anchors]
    miss = [(a, n) for a, (ok, n) in res if not ok]
    check("Z1 %s: all %d batch-19 pointer / boundary notes present" % (os.path.basename(p), len(anchors)), not miss, miss)


def box_note(p, head):
    L = lines(p)
    s = [n for n, t in enumerate(L) if re.match(r"^- \[[ x]\] ", t) and head in t]
    if len(s) != 1:
        return False
    e = s[0] + 1
    while e < len(L) and not re.match(r"^(- \[|## |\s*$)", L[e]):
        e += 1
    blk = "\n".join(L[s[0]:e])
    return TAG in blk and "59ec09a95" in blk and "sd7-sd107-closure-0930" in blk


check("Z2 the SD-7 answer note sits inside the SD-7 box item (input page section 5), citing the record and 59ec09a95",
      box_note(P1, "**SD-7.**"))
check("Z2 the SD-107 answer note sits inside the SD-107 box item (dispatch page section 7), citing the record and 59ec09a95",
      box_note(P2, "**Whether anything instantiates kind 1.**"))
batch_lines = [(os.path.basename(p), n + 1, t) for p in (P1, P2) for n, t in enumerate(lines(p)) if TAG in t]
new_strikes = []
for b, n, t in batch_lines:
    note = t[t.find("(SWE2-CONTRACT for OPUS, " + TAG):]
    if "~~" in note:
        new_strikes.append((b, n))
check("Z3 no batch-19 note strikes anything (pointers and answer notes only; no consumer-check needed)",
      batch_lines and not new_strikes, new_strikes)
crlf = {os.path.basename(p): open(p, "rb").read().count(b"\r\n") for p in (P1, P2)}
check("Z4 both pages are LF on every line (as at HEAD before the edit)", all(v == 0 for v in crlf.values()), crlf)
print("INFO batch-19 note lines: " + ", ".join("%s:%d" % (b, n) for b, n, _ in batch_lines))

print("PASSES %d" % PASSES)
print("FAILS %d" % FAILS)
