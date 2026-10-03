"""check.py - FABLE byte check for the uq147-native-relation-invariant consumption (FABLE, 2026-10-03).

Checks every site and fact the two staged clauses (apply.py E1, E2) state, at the shipping image (sha256 pinned by
rvlib), with FABLE's own reader (rvlib.py from fable-review-astra-ov42-caller-quotient-bound-1002, imported unchanged;
struct + capstone only). It does not run or import ASTRA's producer or its reducer.

Groups (each a function over an image, so a control can rerun it on a patched private copy):
  N  notify leg  - 00310780+0x67 `xor r8d, r8d`, r8 not rewritten before +0x76 `call 0x313b30`; +0x7E the second call.
  P  packet      - 00313B30: r12d := r8d at 00313B56 and never rewritten; flag byte = sete(r12d == 0) stored at +1;
                   kind = 1 + setne stored at +0; uid/aid/tid at +4/+8/+0xC; per-record call 002ED2A0. Context only:
                   the r8 / target-mask logic is the commit contract's section 13a and is not re-proved.
  W  route       - 002ED2A0 tail-jumps 003E6B50, which adds 0x650 to the render record and jumps to 00512F30.
  H  handler     - 00512F30..00513144 (532 B) decodes exactly, seven-fragment .pdata chain rooted at its entry, int3
                   after; only transfers out are 00513005 call / 00513022 jmp to 00512CD0 (no indirect, no other
                   call); 26 persistent writes, every one inside the named envelope; pool base 02CA81F0, cursor
                   02CA83F0, counters 02EBA480/1; kind dispatch; kind-1 flag-1 arm writes only the nibble clear.
  L  remover     - 00512CD0..00512D72 (162 B) decodes exactly, no covering .pdata row, next entry 00512D80, int3 pad;
                   no call; 11 persistent writes, all byte-wide at +0xC..+0xF (never the identity words +0/+4/+8);
                   straight-line tail: `and [node+0xF],0xF0`, `dec [owner+0xE]`, `dec [02EBA481]`, ret (no
                   occupancy or zero test); does not write rbx / rdi / r11.
  Q  reducer     - polarities DERIVED FROM THE DECODED jcc's (so an image control can flip them): creation guard,
                   remove-1 (flag 1 and row target == record target), remove-2 (record recipient == record target).
                   FABLE's own enumeration of the 203 set partitions of six identities x flags {0,1}: 20 coherent,
                   0 double removals, 0 invariant breaks without removal; creation always yields target != recipient;
                   the all-equal flag-1 witness reaches both removals.
  X  clause text - each `00310780`+0xNN is an instruction boundary; each clause cites no 8-hex token new to its page
                   at HEAD; every relative link in E1/E2 resolves from its page, every link in README.md from this
                   folder; the evidence manifest hashes as SWE2-AUDIT-SPEC recorded.
Controls: each must first PASS on the clean baseline (unpatched image / unmutated text), then FAIL on the defect.
Image controls patch a private in-memory copy; the exe on disk is never written. Prints FAILS N last.
"""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img, Body, Report, expect, check_manifest, find_exe  # noqa: E402

sys.path.insert(0, HERE)
import apply as AP  # noqa: E402  (the clause texts; apply.py's main() is not run)

REL = 0x310780
NTF = 0x313B30
EDP = 0x2ED2A0
HND, HND_END = 0x512F30, 0x513144
RMV, RMV_END = 0x512CD0, 0x512D72
POOL, CURSOR, CNT_MAX, CNT_LIVE = 0x2CA81F0, 0x2CA83F0, 0x2EBA480, 0x2EBA481
MANIFEST_SHA = "e1db8d80874a9a1c9b38948d5a3e56eeff8fe659586a5b094e0628a0fd85ac3c"


def rip_target(I, m):
    return I.address + I.size + m["disp"]


def persistent_writes(B):
    out = []
    for a in B.order:
        I = B[a]
        if I.mnemonic in ("push", "call"):
            continue
        for m in I.mems:
            if m["write"] and m["base"] != "rsp":
                out.append((a, I, m))
    return out


# ---------------------------------------------------------------- N
def grp_notify_leg(img, R):
    B = Body(img, REL, 0x310861)
    R.check("N 00310780-00310861 decodes exactly", B.exact)
    expect(R, B, REL + 0x67, "xor r8d, r8d")
    expect(R, B, REL + 0x76, "call 0x313b30")
    expect(R, B, REL + 0x7E, "call 0x2fead0")
    expect(R, B, REL + 0x86, "call 0x308270")
    between = [a for a in B.order if REL + 0x67 < a < REL + 0x76]
    R.check("N r8 is not rewritten between +0x67 and +0x76",
            between and not any("r8" in B[a].reg_writes for a in between),
            " ".join("%08X" % a for a in between))
    R.check("N +0x67 falls through to +0x76 (no branch between)",
            not any(B[a].mnemonic.startswith("j") for a in between))
    R.check("N later calls +0x99 / +0xAC / +0xB9 / +0xD6 are calls",
            all(B.ins.get(REL + o) is not None and B[REL + o].mnemonic == "call" for o in (0x99, 0xAC, 0xB9, 0xD6)))


# ---------------------------------------------------------------- P
def grp_packet(img, R):
    B = Body(img, NTF, 0x313CCA)
    R.check("P 00313B30-00313CCA (410 B) decodes exactly", B.exact)
    ents, ok = img.pdata_cover(NTF, 0x313CCA)
    R.check("P seven .pdata fragments tile 00313B30-00313CCA, chained to the entry", ok and len(ents) == 7, str(len(ents)))
    expect(R, B, 0x313B56, "mov r12d, r8d")
    w12 = [a for a in B.order if "r12" in B[a].reg_writes and a != 0x313B56 and B[a].mnemonic != "push"]
    R.check("P r12 is written only at 00313B56 (= r8d) before the epilogue pop", w12 == [0x313CC7],
            " ".join("%08X" % a for a in w12))
    expect(R, B, 0x313C3D, "test r12d, r12d")
    expect(R, B, 0x313C40, "sete dil")
    expect(R, B, 0x313C59, "mov byte ptr [rsp + 0x31], dil")
    expect(R, B, 0x313C5E, "setne al")
    expect(R, B, 0x313C61, "inc al")
    expect(R, B, 0x313C63, "mov byte ptr [rsp + 0x30], al")
    expect(R, B, 0x313C6E, "mov dword ptr [rsp + 0x34], ecx")
    expect(R, B, 0x313C76, "mov dword ptr [rsp + 0x38], eax")
    expect(R, B, 0x313C7E, "mov dword ptr [rsp + 0x3c], eax")
    expect(R, B, 0x313C54, "lea rdx, [rsp + 0x30]")
    expect(R, B, 0x313C89, "call 0x2ed2a0")


# ---------------------------------------------------------------- W
def grp_route(img, R):
    B = Body(img, EDP, 0x2ED2FD)
    R.check("W 002ED2A0-002ED2FD decodes exactly", B.exact)
    expect(R, B, 0x2ED2E1, "cmp dword ptr [rcx + 0x284], 0")
    expect(R, B, 0x2ED2EA, "mov rdx, rbx")
    expect(R, B, 0x2ED2F2, "jmp 0x3e6b50")
    T = Body(img, 0x3E6B50, 0x3E6B5C)
    expect(R, T, 0x3E6B50, "add rcx, 0x650")
    expect(R, T, 0x3E6B57, "jmp 0x512f30")


# ---------------------------------------------------------------- H
def grp_handler(img, R):
    B = Body(img, HND, HND_END)
    R.check("H 00512F30-00513144 (532 B) decodes exactly", B.exact)
    ents, ok = img.pdata_cover(HND, HND_END)
    R.check("H seven .pdata fragments tile the body, chained to 00512F30", ok and len(ents) == 7, str(len(ents)))
    R.check("H int3 padding at 00513144", img.read(HND_END, 1) == b"\xcc")
    xfer = []
    for a in B.order:
        I = B[a]
        m = I.mnemonic
        if m == "call" or (m.startswith("j") and (I.direct_target() is None or not (HND <= I.direct_target() < HND_END))):
            xfer.append((a, m, I.direct_target()))
    R.check("H only transfers out: 00513005 call / 00513022 jmp -> 00512CD0",
            xfer == [(0x513005, "call", RMV), (0x513022, "jmp", RMV)], str([("%X" % a, m, t and "%X" % t) for a, m, t in xfer]))
    R.check("H no memory-indirect or register-indirect transfer",
            not any(B[a].mnemonic in ("call", "jmp") and B[a].direct_target() is None for a in B.order))
    expect(R, B, 0x512F44, "je 0x5130fd")
    expect(R, B, 0x512F4D, "je 0x5130cb")
    lea = B.ins.get(0x512F58)
    R.check("H 00512F58 lea r10 resolves to the pool 02CA81F0",
            lea is not None and lea.mnemonic == "lea" and rip_target(lea, lea.mems[0]) == POOL)
    for a, t in ((0x512F77, "add rbx, r10"), (0x512FB6, "add rax, r10"), (0x512FD6, "add rax, r10")):
        expect(R, B, a, t)
    ws = persistent_writes(B)
    R.check("H 26 persistent write sites", len(ws) == 26, str(len(ws)))
    bad = []
    for a, I, m in ws:
        b, d = m["base"], m["disp"]
        if b == "rip":
            ok_w = rip_target(I, m) in (CURSOR, CNT_MAX, CNT_LIVE)
        elif b == "r11":
            ok_w = d in (0, 4, 8, 0xC, 0xD, 0xE, 0xF)
        elif b in ("rbx", "rax"):
            ok_w = d in (0, 4, 8, 0xD, 0xE, 0xF)
        elif b == "r10":
            ok_w = m["index"] is not None and d == 0xE
        else:
            ok_w = False
        if not ok_w:
            bad.append("%08X %s" % (a, I.text))
    R.check("H every write is in the envelope: receiver inline block, pool row, cursor, counters", not bad, str(bad))
    # creation guard (sites only; polarity in Q)
    expect(R, B, 0x512F94, "cmp byte ptr [rdi + 1], 0")
    expect(R, B, 0x512F9D, "cmp dword ptr [rdi + 4], eax")
    expect(R, B, 0x512F9A, "mov eax, dword ptr [rdi + 0xc]")
    for a, t in ((0x513067, "mov ecx, dword ptr [rdi + 4]"), (0x51306A, "mov dword ptr [rax], ecx"),
                 (0x51306C, "mov ecx, dword ptr [rdi + 8]"), (0x51306F, "mov dword ptr [rax + 4], ecx"),
                 (0x513072, "mov ecx, dword ptr [rdi + 0xc]"), (0x513075, "mov dword ptr [rax + 8], ecx")):
        expect(R, B, a, t)
    # matched kind-2 arm
    expect(R, B, 0x512F80, "cmp al, dl")
    expect(R, B, 0x512F87, "cmp dword ptr [rbx + 4], eax")
    expect(R, B, 0x512F84, "mov eax, dword ptr [rdi + 8]")
    expect(R, B, 0x512FF1, "cmp byte ptr [rdi + 1], 1")
    expect(R, B, 0x512FF7, "mov eax, dword ptr [rdi + 0xc]")
    expect(R, B, 0x512FFA, "cmp dword ptr [rbx + 8], eax")
    expect(R, B, 0x513005, "call 0x512cd0")
    expect(R, B, 0x51300A, "mov eax, dword ptr [rdi + 0xc]")
    expect(R, B, 0x51300D, "cmp dword ptr [rdi + 4], eax")
    expect(R, B, 0x513022, "jmp 0x512cd0")
    expect(R, B, 0x513027, "mov dword ptr [rbx + 8], eax")
    R.check("H the call at 00513005 returns into 0051300A (the second test runs after a first removal)",
            0x51300A in B.succ(0x513005) and 0x513027 in B.reach(0x51300A))
    # kind-1 arm, flag 1: nibble clear only, or nothing
    expect(R, B, 0x5130FD, "cmp byte ptr [rdi + 1], 1")
    expect(R, B, 0x513104, "jne 0x51311b")
    expect(R, B, 0x513106, "cmp dword ptr [r11 + 8], eax")
    expect(R, B, 0x51310A, "jne 0x512feb")
    expect(R, B, 0x513110, "and byte ptr [r11 + 0xf], 0xf0")
    k1 = B.reach(0x513106)
    k1w = [a for a, I, m in ws if a in k1]
    R.check("H kind-1 flag-1 path writes only 00513110 (the nibble clear)", k1w == [0x513110],
            " ".join("%08X" % a for a in k1w))
    miss1 = B.reach(0x512FE6)
    R.check("H the creation-refused exit 00512FE6 writes nothing", not [a for a, I, m in ws if a in miss1])


# ---------------------------------------------------------------- L
def grp_remover(img, R):
    B = Body(img, RMV, RMV_END)
    R.check("L 00512CD0-00512D72 (162 B) decodes exactly", B.exact)
    R.check("L no .pdata row covers 00512CD0; next entry begins at 00512D80",
            img.pdata(RMV) is None and (img.pdata(0x512D80) or (0,))[0] == 0x512D80)
    R.check("L int3 padding 00512D72-00512D80", img.read(RMV_END, 0x512D80 - RMV_END) == b"\xcc" * (0x512D80 - RMV_END))
    R.check("L no call, no transfer out of the body",
            not B.calls() and not B.exits()[1] and not B.exits()[2] and B.exits()[0] == [0x512D71])
    lea = B.ins.get(0x512CD4)
    R.check("L 00512CD4 lea r10 resolves to the pool 02CA81F0",
            lea is not None and lea.mnemonic == "lea" and rip_target(lea, lea.mems[0]) == POOL)
    ws = persistent_writes(B)
    R.check("L 11 persistent write sites", len(ws) == 11, str(len(ws)))
    bad = ["%08X %s" % (a, I.text) for a, I, m in ws
           if not (m["size"] == 1 and (m["base"] == "rip" and rip_target(I, m) == CNT_LIVE or
                                       m["base"] != "rip" and 0xC <= m["disp"] <= 0xF))]
    R.check("L every write is one byte at +0xC..+0xF or the live count 02EBA481 (identity words never written)",
            not bad, str(bad))
    expect(R, B, 0x512D62, "and byte ptr [r8 + 0xf], 0xf0")
    expect(R, B, 0x512D67, "dec byte ptr [r9 + 0xe]")
    expect(R, B, 0x512D6B, "dec byte ptr [rip + 0x29a7710]")
    d = B.ins.get(0x512D6B)
    R.check("L 00512D6B decrements 02EBA481", d is not None and d.mems and rip_target(d, d.mems[0]) == CNT_LIVE)
    expect(R, B, 0x512CDB, "mov r8, rdx")
    expect(R, B, 0x512CDE, "mov r9, rcx")
    tail = [a for a in B.order if a >= 0x512D62]
    R.check("L tail 00512D62..00512D71 is straight-line (no test or branch before either decrement)",
            [B[a].mnemonic for a in tail] == ["and", "dec", "dec", "ret"])
    R.check("L every path reaches 00512D62", all(0x512D62 in B.reach(a) for a in B.order if a < 0x512D62))
    rw = set()
    for a in B.order:
        rw |= B[a].reg_writes
    R.check("L does not write rbx, rdi or r11", not (rw & {"rbx", "rdi", "r11"}), str(sorted(rw)))


# ---------------------------------------------------------------- Q
def partitions(n):
    """Restricted growth strings: every set partition of n labelled elements."""
    out = []

    def rec(prefix):
        if len(prefix) == n:
            out.append(tuple(prefix))
            return
        for b in range(max(prefix) + 2):
            rec(prefix + [b])
    rec([0])
    return out


def skip_polarity(B, jcc_addr, skip_target):
    """For `cmp; jcc skip`: 'eq' when the action runs on equality (jcc = jne), 'ne' when it runs on inequality."""
    I = B.ins.get(jcc_addr)
    if I is None or I.direct_target() != skip_target:
        raise ValueError("jcc at %08X does not skip to %08X" % (jcc_addr, skip_target))
    return {"jne": "eq", "je": "ne"}[I.mnemonic]


def grp_reducer(img, R):
    B = Body(img, HND, HND_END)
    # creation: flag test (cmp [rdi+1],0 ; jne exit) and recipient/target (cmp [rdi+4],[rdi+0xc] ; je exit)
    c_flag = skip_polarity(B, 0x512F98, 0x512FE6)   # 'eq': create only when flag == 0
    c_ut = skip_polarity(B, 0x512FA0, 0x512FE6)     # 'ne': create only when recipient != target
    r1_flag = skip_polarity(B, 0x512FF5, 0x51300A)  # 'eq': remove-1 only when flag == 1
    r1_tt = skip_polarity(B, 0x512FFD, 0x51300A)    # 'eq': remove-1 only when row target == record target
    r2_ut = skip_polarity(B, 0x513010, 0x513027)    # 'eq': remove-2 only when record recipient == record target
    R.check("Q polarities read from the image: create flag==0 and pu!=pt; remove-1 flag==1 and nt==pt; remove-2 pu==pt",
            (c_flag, c_ut, r1_flag, r1_tt, r2_ut) == ("eq", "ne", "eq", "eq", "eq"),
            str((c_flag, c_ut, r1_flag, r1_tt, r2_ut)))

    def holds(pol, same):
        return same if pol == "eq" else not same

    P = partitions(6)
    R.check("Q 203 set partitions of six identities", len(P) == 203, str(len(P)))
    PU, PA, PT, NU, NA, NT = range(6)
    coherent = double = broke = 0
    created_bad = 0
    for p in P:
        eq = lambda i, j: p[i] == p[j]  # noqa: E731
        for flag in (0, 1):
            if holds(c_flag, flag == 0) and holds(c_ut, eq(PU, PT)):
                # stores 0051306A/6F/75: row recipient := pu, row target := pt
                if p[PU] == p[PT]:
                    created_bad += 1
            if not (eq(PU, NU) and eq(PA, NA) and not eq(NT, NU)):
                continue
            coherent += 1
            r1 = holds(r1_flag, flag == 1) and holds(r1_tt, eq(NT, PT))
            r2 = holds(r2_ut, eq(PU, PT))
            if r1 and r2:
                double += 1
            if not r1 and not r2 and eq(PT, NU):
                broke += 1
    R.check("Q 20 coherent cases (10 partitions x 2 flags)", coherent == 20, str(coherent))
    R.check("Q 0 coherent double removals", double == 0, str(double))
    R.check("Q 0 coherent cases where the stored target equals the recipient without a removal", broke == 0, str(broke))
    R.check("Q creation never yields a row with target == recipient", created_bad == 0, str(created_bad))
    w1 = holds(r1_flag, True) and holds(r1_tt, True)
    w2 = holds(r2_ut, True)
    R.check("Q broken-premise witness (all six equal, flag 1) reaches both removals", w1 and w2)


# ---------------------------------------------------------------- X
def git_head(rel):
    db = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=db, capture_output=True).stdout.decode().strip()
    full = os.path.relpath(os.path.join(db, *rel.split("/")), top).replace("\\", "/")
    return subprocess.run(["git", "show", "HEAD:" + full], cwd=db, capture_output=True).stdout.decode("utf-8")


SITE = re.compile(r"`(00310780)`\+0x([0-9A-F]+)((?:\s*(?:/|,|and|, and)\s*\+0x[0-9A-F]+)*)")
LINK = re.compile(r"\]\(([^)\s]+)\)")


def clause_sites(text):
    out = []
    for m in SITE.finditer(text):
        fn = int(m.group(1), 16)
        offs = [m.group(2)] + re.findall(r"\+0x([0-9A-F]+)", m.group(3) or "")
        out += [(fn, int(o, 16)) for o in offs]
    return out


def bad_links(text, base_dir):
    bad = []
    for t in LINK.findall(text):
        if t.startswith("http") or t.startswith("#"):
            continue
        p = os.path.normpath(os.path.join(base_dir, t.split("#")[0]))
        if not os.path.exists(p):
            bad.append(t)
    return bad


def grp_text(img, R, e1=None, e2=None):
    e1 = AP.E1_CLAUSE if e1 is None else e1
    e2 = AP.E2_CLAUSE if e2 is None else e2
    B = Body(img, REL, 0x310861)
    sites = clause_sites(e1) + clause_sites(e2)
    R.check("X the clauses cite %d call-site offsets" % len(sites), len(sites) >= 8, str(len(sites)))
    bad = ["%08X+0x%X" % (f, o) for f, o in sites if (f + o) not in B.ins]
    R.check("X every cited fn+0xNN is an instruction boundary", not bad, str(bad))
    db = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
    for name, rel, clause in (("E1", AP.STATUS, e1), ("E2", AP.POLICY, e2)):
        head = git_head(rel)
        toks = sorted(set(re.findall(r"(?<![0-9A-Fa-fx])[0-9A-F]{8}(?![0-9A-Fa-f])", clause)))
        new = [t for t in toks if t not in head]
        R.check("X %s cites only 8-hex functions its page already cites (%s)" % (name, ",".join(toks) or "none"),
                not new, str(new))
        bl = bad_links(clause, os.path.dirname(os.path.join(db, *rel.split("/"))))
        R.check("X %s: every relative link resolves from its page (%d links)" % (name, len(LINK.findall(clause))),
                not bl, str(bl))


def grp_readme(R):
    p = os.path.join(HERE, "README.md")
    if not os.path.exists(p):
        R.check("K README.md exists", False)
        return
    t = open(p, encoding="utf-8").read()
    # links inside the clause code blocks are page-relative by design; check the prose outside the fences
    prose = re.sub(r"```.*?```", "", t, flags=re.S)
    bl = bad_links(prose, HERE)
    R.check("K README.md: every relative link resolves from the record folder (%d links)" % len(LINK.findall(prose)),
            not bl, str(bl))
    heads = [l for l in t.split("\n") if l.startswith("#")]
    R.check("K README.md: every heading contains FABLE (%d headings)" % len(heads),
            heads and all("FABLE" in h for h in heads), str([h for h in heads if "FABLE" not in h]))
    tail = t.rstrip("\n").split("\n## Consumer check (FABLE)\n")
    R.check("K README.md ends with '## Consumer check (FABLE)'", len(tail) == 2 and "\n## " not in tail[1])
    if len(tail) == 2:
        aff = [l for l in tail[1].split("\n") if l.startswith("affected:")]
        want = ["affected: Database/FFXII TZA/" + AP.STATUS, "affected: Database/FFXII TZA/" + AP.POLICY]
        R.check("K affected: lines are exactly the two edited pages, nothing after the path", aff == want, str(aff))
        R.check("K a `run: check.py at <sha> (FAILS 0)` line", re.search(r"^run: check\.py at [0-9a-f]{7,12} \(FAILS 0\)$",
                                                                       tail[1], re.M) is not None)


# ---------------------------------------------------------------- controls
def quiet_fails(fn, *a, **k):
    R = Report("ctl")
    R.quiet = True
    try:
        fn(*a, R, **k)
        return R.fails
    except Exception:
        return 1


def run_image_control(R, img, label, grp, patches):
    base = quiet_fails(grp, img)
    im = img
    for va, old, new in patches:
        cur = im.read(va, len(old))
        if cur != old:
            R.check("CONTROL %s: expected original bytes at %08X" % (label, va), False, cur.hex())
            return
        im = im.patched(va, new)
    after = quiet_fails(grp, im)
    R.check("CONTROL %s: %s passes on the clean image, FAILS on the patched copy" % (label, grp.__name__),
            base == 0 and after > 0, "baseline fails %d, patched fails %d" % (base, after))


def run_text_control(R, img, label, e1=None, e2=None):
    base = quiet_fails(grp_text, img)
    after = quiet_fails(grp_text, img, e1=e1, e2=e2)
    R.check("CONTROL %s: grp_text passes on the clean clauses, FAILS on the mutated text" % label,
            base == 0 and after > 0, "baseline fails %d, mutated fails %d" % (base, after))


def main():
    exe = find_exe()
    before = hashlib.sha256(open(exe, "rb").read()).hexdigest()
    img = Img.load()
    R = Report("fable-uq147-native-relation-1003")
    print("image %s base %X" % (before[:16], img.base))
    for g in (grp_notify_leg, grp_packet, grp_route, grp_handler, grp_remover, grp_reducer, grp_text):
        g(img, R)
    grp_readme(R)
    check_manifest(R, "uq147-native-relation-invariant", MANIFEST_SHA)

    h = bytes.fromhex
    run_image_control(R, img, "c1 00512FFD jne -> je (reversed matching-target branch)", grp_reducer,
                      [(0x512FFD, h("75"), h("74"))])
    run_image_control(R, img, "c2 00512FA0 je -> jne (creation inequality inverted)", grp_reducer,
                      [(0x512FA0, h("74"), h("75"))])
    run_image_control(R, img, "c3 00512D62 and [r8+0xF] -> [r8+0x8] (remover writes the target word)", grp_remover,
                      [(0x512D62, h("4180600ff0"), h("41806008f0"))])
    run_image_control(R, img, "c4 00513005 call 00512CD0 -> call rax (an opaque callback)", grp_handler,
                      [(0x513005, h("e8c6fcffff"), h("ffd0909090"))])
    run_image_control(R, img, "c5 00512D62 -> je over the count decrement (an occupancy guard)", grp_remover,
                      [(0x512D62, h("4180600ff0"), h("7407909090"))])
    run_image_control(R, img, "c6 005130F3 store [r11+8] -> [r11+0x7F] (write outside the envelope)", grp_handler,
                      [(0x5130F3, h("41894308"), h("4189437f"))])
    run_image_control(R, img, "c7 00310780+0x67 xor r8d,r8d -> mov r8b,1 (non-zero third argument)", grp_notify_leg,
                      [(REL + 0x67, h("4533c0"), h("41b001"))])
    run_image_control(R, img, "c8 003E6B50 add rcx,0x650 -> 0x640 (another receiver)", grp_route,
                      [(0x3E6B53, h("50060000"), h("40060000"))])
    run_text_control(R, img, "t1 E1 cites `00310780`+0x77 (not an instruction boundary)",
                     e1=AP.E1_CLAUSE.replace("`00310780`+0x76", "`00310780`+0x77", 1))
    run_text_control(R, img, "t2 E1 names the handler by address `00512F30` (a new neighbour edge)",
                     e1=AP.E1_CLAUSE.replace("native relation-event handler", "native relation-event handler `00512F30`", 1))
    run_text_control(R, img, "t3 E2 names `00310780` (not cited on the capability page)",
                     e2=AP.E2_CLAUSE.replace("the release's contributor", "the release `00310780`'s contributor", 1))
    run_text_control(R, img, "t4 E1 links a page that does not exist",
                     e1=AP.E1_CLAUSE.replace(AP.ALLONES, "../../00-Engine-Core-Runtime/no-such-page.md", 1))

    after = hashlib.sha256(open(exe, "rb").read()).hexdigest()
    R.check("image on disk unchanged after the controls (sha256 re-read)", after == before)
    print("FAILS %d" % R.fails)
    return 1 if R.fails else 0


if __name__ == "__main__":
    sys.exit(main())
