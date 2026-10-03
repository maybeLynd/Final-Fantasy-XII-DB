"""check.py - FABLE byte check for the uq147-ko-release-partition consumption (FABLE, 2026-10-03).

Checks every site the two staged clauses (apply.py E1, E2) cite, at the shipping image (sha256 pinned by rvlib), with
FABLE's own reader (rvlib.py from fable-review-astra-ov42-caller-quotient-bound-1002, imported unchanged; struct +
capstone only). It does not run or import ASTRA's producer.

Groups (each a function over an image, so a control can rerun it on a patched private copy):
  R  release    - 00310780 (225 B, its own .pdata begin): NULL-receiver / NULL-stats exits; target via 0031B7E0;
                  bit 22 read at +0x3E, `jb` (skip when SET) at +0x43; slot-bit test; the bookkeeping block
                  (+0x5D dec +0xEA8, +0x6A store +0xEA4, calls +0x76 / +0x7E) unreachable without the bit-22-clear
                  fall-through; the restore call at +0x86 on every admitted path; exactly four non-stack stores
                  (+0x5D, +0x6A, +0x8B clearing flag bits 5 and 28 only, +0xA5); no store with displacement
                  +0x714 / +0xBA0; the +0x714 compare at +0xCD; eight direct calls.
  S  restore    - 00308270 (120 B): bit 22 read at 0030827B, `jae` (skip when CLEAR) to the epilogue; the copy-back
                  call to 0030EDA0 and the bit 22 / 46 clear only on the SET path. The copy bound itself is OPUS's
                  (commit contract, restore row); it is cited, not re-proved.
  T  two reads  - on the bookkeeping path exactly three calls lie between the two bit-22 reads.
  D  defeat     - 00300FC0+0x4D calls 00310780 and dominates 00300FC0+0x15E (call 003138D0) / +0x163 (call 0023B040).
  X  clause text - every `00310780`+0xNN / `00300FC0`+0xNN in E1/E2 is an instruction boundary of the cited body;
                  every 8-hex token in each clause is a function the target page already cites at HEAD (no new
                  neighbour edge); the evidence manifest hashes as SWE2-AUDIT-SPEC recorded.
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
RST = 0x308270
DEF = 0x300FC0
MANIFEST_SHA = "ff4cd43a997cb98df7007fdd1e8b2fd73ffc317fee4abcf0fa6e3f7310ac2458"


def S(o):
    return REL + o


def nonstack_writes(B):
    out = []
    for a in B.order:
        I = B[a]
        if I.mnemonic in ("push", "call"):
            continue
        for m in I.mems:
            if m["write"] and m["base"] != "rsp":
                out.append(a)
    return out


# ---------------------------------------------------------------- R
def grp_release(img, R):
    R.check("R .pdata entry begins at 00310780", (img.pdata(REL) or (0,))[0] == REL)
    B = Body(img, REL, 0x310861)
    R.check("R 00310780-00310861 (225 B) decodes exactly, last insn ret", B.exact and B[B.order[-1]].mnemonic == "ret")
    expect(R, B, S(0x0), "test rcx, rcx")
    expect(R, B, S(0x3), "je 0x310860")
    expect(R, B, S(0xE), "cmp qword ptr [rcx + 0x698], 0")
    expect(R, B, S(0x19), "je 0x31085b")
    expect(R, B, S(0x1F), "mov ecx, dword ptr [rcx + 0x710]")
    expect(R, B, S(0x2F), "call 0x31b7e0")
    expect(R, B, S(0x3A), "je 0x310803")
    expect(R, B, S(0x3C), "mov ecx, dword ptr [rbx]")
    expect(R, B, S(0x3E), "bt rcx, 0x16")
    expect(R, B, S(0x43), "jb 0x310803")
    expect(R, B, S(0x45), "movzx ecx, byte ptr [rbx + 0xea9]")
    expect(R, B, S(0x51), "mov eax, dword ptr [rax + 0xea4]")
    expect(R, B, S(0x59), "test edx, eax")
    expect(R, B, S(0x5B), "je 0x310803")
    expect(R, B, S(0x5D), "dec byte ptr [rdi + 0xea8]")
    expect(R, B, S(0x6A), "mov dword ptr [rdi + 0xea4], edx")
    expect(R, B, S(0x86), "call 0x308270")
    expect(R, B, S(0x8B), "and qword ptr [rbx], 0xffffffffefffffdf")
    expect(R, B, S(0xA5), "mov byte ptr [rbx + 0x694], 0xff")
    expect(R, B, S(0xCD), "cmp word ptr [rbx + 0x714], ax")
    expect(R, B, S(0xD4), "jne 0x31085b")
    expect(R, B, S(0xD6), "call 0x317e50")
    # mask clears exactly bits 5 and 28
    I = B.ins.get(S(0x8B))
    cleared = None
    if I is not None and I.mnemonic == "and" and I.imm:
        m = I.imm[-1] & 0xFFFFFFFFFFFFFFFF
        cleared = [b for b in range(64) if not (m >> b) & 1]
    R.check("R +0x8B clears flag bits [5, 28] only", cleared == [5, 28], str(cleared))
    # bookkeeping block only on the bit-22-clear fall-through
    no_ft = B.reach(REL, avoid=[S(0x45)])
    R.check("R +0x5D / +0x6A / +0x76 / +0x7E unreachable without the +0x43 fall-through (bit 22 clear)",
            not any(x in no_ft for x in (S(0x5D), S(0x6A), S(0x76), S(0x7E))))
    R.check("R +0x43 jb target is the merge point +0x83 (skip when SET)",
            B.ins.get(S(0x43)) is not None and B[S(0x43)].direct_target() == S(0x83))
    # restore call on every admitted path
    adm = B.reach(S(0x1F), avoid=[S(0x86)])
    R.check("R every path from the admitted body to +0x8B / +0xA5 / +0xCD passes +0x86",
            not any(x in adm for x in (S(0x8B), S(0xA5), S(0xCD))))
    R.check("R +0x86 reached both with and without the bookkeeping block",
            S(0x86) in B.reach(S(0x43) + 0, avoid=[S(0x45)]) and S(0x86) in B.reach(S(0x45)))
    # direct stores
    ws = nonstack_writes(B)
    R.check("R exactly four non-stack stores at +0x5D, +0x6A, +0x8B, +0xA5",
            ws == [S(0x5D), S(0x6A), S(0x8B), S(0xA5)], " ".join("%08X" % w for w in ws))
    bad = [a for a, m in B.mem_writes(lambda m: m["disp"] in (0x714, 0xBA0)) if m["base"] != "rsp"]
    R.check("R no store with displacement +0x714 or +0xBA0", not bad, str(["%08X" % a for a in bad]))
    calls = [t for a, t in B.calls()]
    R.check("R eight direct calls: 0031B7E0 00313B30 002FEAD0 00308270 0030C970 00319420 00319140 00317E50",
            calls == [0x31B7E0, 0x313B30, 0x2FEAD0, 0x308270, 0x30C970, 0x319420, 0x319140, 0x317E50],
            " ".join("%08X" % (t or 0) for t in calls))
    R.check("R call sites +0x76 / +0x7E / +0x99 / +0xAC / +0xB9 are calls",
            all(B.ins.get(S(o)) is not None and B[S(o)].mnemonic == "call" for o in (0x76, 0x7E, 0x99, 0xAC, 0xB9)))


# ---------------------------------------------------------------- S
def grp_restore(img, R):
    R.check("S .pdata entry 00308270-003082E8", img.pdata(RST) == (RST, 0x3082E8))
    B = Body(img, RST, 0x3082E8)
    R.check("S 00308270-003082E8 (120 B) decodes exactly", B.exact)
    expect(R, B, 0x308276, "mov eax, dword ptr [rcx]")
    expect(R, B, 0x30827B, "bt rax, 0x16")
    expect(R, B, 0x308280, "jae 0x3082e2")
    expect(R, B, 0x3082C6, "call 0x30eda0")
    expect(R, B, 0x3082CB, "movabs rax, 0xffffbfffffbfffff")
    expect(R, B, 0x3082DF, "and qword ptr [rbx], rax")
    clr = B.reach(RST, avoid=[0x308282])
    R.check("S with bit 22 clear (jae taken) neither 003082C6 nor 003082DF is reached",
            0x3082C6 not in clr and 0x3082DF not in clr and 0x3082E2 in clr)


# ---------------------------------------------------------------- T
def grp_tworeads(img, R):
    B = Body(img, REL, 0x310861)
    between = [a for a, t in B.calls() if S(0x3E) < a <= S(0x86)]
    R.check("T three calls between the bit-22 read at +0x3E and the restore's own read (+0x76, +0x7E, +0x86)",
            between == [S(0x76), S(0x7E), S(0x86)], " ".join("%08X" % a for a in between))
    path = B.reach(S(0x45))
    R.check("T the bookkeeping path reaches the restore call", S(0x86) in path)


# ---------------------------------------------------------------- D
def grp_defeat(img, R):
    B = Body(img, DEF, 0x301133)
    R.check("D 00300FC0-00301133 decodes exactly", B.exact)
    expect(R, B, DEF + 0x4D, "call 0x310780")
    expect(R, B, DEF + 0x15E, "call 0x3138d0")
    expect(R, B, DEF + 0x163, "call 0x23b040")
    R.check("D 00300FC0+0x4D dominates +0x15E and +0x163",
            B.dominates(DEF + 0x4D, DEF + 0x15E) and B.dominates(DEF + 0x4D, DEF + 0x163))


# ---------------------------------------------------------------- X
def git_head(rel):
    db = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=db, capture_output=True).stdout.decode().strip()
    full = os.path.relpath(os.path.join(db, *rel.split("/")), top).replace("\\", "/")
    return subprocess.run(["git", "show", "HEAD:" + full], cwd=db, capture_output=True).stdout.decode("utf-8")


SITE = re.compile(r"`(00310780|00300FC0)`\+0x([0-9A-F]+)((?:\s*(?:/|,|and)\s*\+0x[0-9A-F]+)*)")


def clause_sites(text):
    out = []
    for m in SITE.finditer(text):
        fn = int(m.group(1), 16)
        offs = [m.group(2)] + re.findall(r"\+0x([0-9A-F]+)", m.group(3) or "")
        out += [(fn, int(o, 16)) for o in offs]
    return out


def grp_text(img, R, e1=None, e2=None):
    e1 = AP.E1_CLAUSE if e1 is None else e1
    e2 = AP.E2_CLAUSE if e2 is None else e2
    bodies = {REL: Body(img, REL, 0x310861), DEF: Body(img, DEF, 0x301133)}
    sites = clause_sites(e1) + clause_sites(e2)
    R.check("X the clauses cite %d call-site offsets" % len(sites), len(sites) >= 20, str(len(sites)))
    bad = ["%08X+0x%X" % (f, o) for f, o in sites if (f + o) not in bodies[f].ins]
    R.check("X every cited fn+0xNN is an instruction boundary", not bad, str(bad))
    for name, rel, clause in (("E1", AP.STATUS, e1), ("E2", AP.POLICY, e2)):
        head = git_head(rel)
        toks = sorted(set(re.findall(r"(?<![0-9A-Fa-fx])[0-9A-F]{8}(?![0-9A-Fa-f])", clause)))
        new = [t for t in toks if t not in head]
        R.check("X %s cites only 8-hex functions its page already cites (%s)" % (name, ",".join(toks)), not new,
                str(new))


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
    R = Report("fable-uq147-ko-release-1003")
    print("image %s base %X" % (before[:16], img.base))
    for g in (grp_release, grp_restore, grp_tworeads, grp_defeat, grp_text):
        g(img, R)
    check_manifest(R, "uq147-ko-release-partition", MANIFEST_SHA)

    # image controls: (va, original bytes, patched bytes)
    run_image_control(R, img, "c1 +0x43 jb -> jae (bit 22 SET would admit the bookkeeping)", grp_release,
                      [(S(0x43), bytes.fromhex("72"), bytes.fromhex("73"))])
    run_image_control(R, img, "c2 0030827B bt imm 0x16 -> 0x15 (the restore reads bit 21)", grp_restore,
                      [(0x30827B + 4, bytes.fromhex("16"), bytes.fromhex("15"))])
    run_image_control(R, img, "c3 00308280 jae -> jb (restore runs with bit 22 CLEAR)", grp_restore,
                      [(0x308280, bytes.fromhex("73"), bytes.fromhex("72"))])
    run_image_control(R, img, "c4 +0xCD cmp word [rbx+0x714],ax -> mov (a direct +0x714 store)", grp_release,
                      [(S(0xCD), bytes.fromhex("663983"), bytes.fromhex("668983"))])
    run_image_control(R, img, "c5 +0x8B mask also clears bit 22", grp_release,
                      [(S(0x8B) + 3, bytes.fromhex("dfffffef"), bytes.fromhex("dfffbfef"))])
    run_image_control(R, img, "c6 +0x3E bt imm 0x16 -> 0x15", grp_release,
                      [(S(0x3E) + 4, bytes.fromhex("16"), bytes.fromhex("15"))])
    run_image_control(R, img, "c7 +0x76 call -> 5 nops (one call fewer between the reads)", grp_tworeads,
                      [(S(0x76), img.read(S(0x76), 5), b"\x90" * 5)])
    run_image_control(R, img, "c8 00300FC0+0x4D call 00310780 -> 5 nops", grp_defeat,
                      [(DEF + 0x4D, img.read(DEF + 0x4D, 5), b"\x90" * 5)])
    run_image_control(R, img, "c9 +0x6A store +0xEA4 -> +0xBA0 (a direct +0xBA0 store)", grp_release,
                      [(S(0x6A) + 2, bytes.fromhex("a40e0000"), bytes.fromhex("a00b0000"))])
    # text controls
    run_text_control(R, img, "t1 E1 cites `00310780`+0x3F (not an instruction boundary)",
                     e1=AP.E1_CLAUSE.replace("`00310780`+0x3E", "`00310780`+0x3F", 1))
    run_text_control(R, img, "t2 E1 names the restore by address `00308270` (a new neighbour edge)",
                     e1=AP.E1_CLAUSE.replace("restore (`00310780`+0x86)", "restore `00308270` (`00310780`+0x86)", 1))
    run_text_control(R, img, "t3 E2 names `00310780` (not cited on the capability page)",
                     e2=AP.E2_CLAUSE.replace("target-relation", "`00310780` target-relation", 1))

    after = hashlib.sha256(open(exe, "rb").read()).hexdigest()
    R.check("image on disk unchanged after the controls (sha256 re-read)", after == before)
    print("FAILS %d" % R.fails)
    return 1 if R.fails else 0


if __name__ == "__main__":
    sys.exit(main())
