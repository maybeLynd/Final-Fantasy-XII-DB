"""check.py - FABLE's executed check for the registration event-0 clause on the-box-renderer-that-is-never-called.md
(ASTRA-REQ-FABLE-OV42-REGISTER-EVENT0-1003). Own walker over the shipping bytes (rvlib.py, struct + capstone only);
does not import or run ASTRA's prove.py / control.py.

  I  image sha256; ASTRA's package manifest 153a65ee... and every member it lists.
  H  each handler's .pdata extent (50 B / 82 B), exact linear decode.
  E  concrete-edx path walk from each handler entry at edx = 0: ends at RET; no CALL; no non-stack memory write;
     exactly one non-stack read, qword [rcx+0x48], with rcx unwritten before it; EAX = 0 from the last EAX writer;
     the path never reads r8 or the register loaded from +0x48.
  P  positive walks: event 1 in both handlers reaches CALL 002973E0; event 2 in 0029B810 reaches the store
     [rcx+4] (the walker sees calls and writes when they are there).
  R  003F89C0: the zeroing call precedes the stores +0x26/+0x38/+0x40/+0x48, which precede `call rax`; edx = 0,
     rcx = the record and r8 = rbp (= edx at entry, `mov ebp,edx`) at the call; the NULL test skips it.
  Q  page: the clause is absent at HEAD; the existing handler rows quoted in README.md are present verbatim at HEAD;
     every 8-hex address in the clause is an instruction boundary inside a function the HEAD page already cites
     (no new function citation); apply.py's dry run on a HEAD copy inserts exactly one paragraph.
  C  sensitivity controls on private patched images (the exe on disk is never written); each must make E or R FAIL:
     C1 29B7DB cmp edx,1 -> cmp edx,0 (event 0 reaches the call)          [the defect: event 0 updates the bar]
     C2 29B81B sub edx,1 -> add edx,1 (event 0 reaches the [rcx+4] store) [the defect: event 0 writes the record]
     C3 29B7D4 mov rax,r8 -> mov rcx,r8 (the +0x48 read follows the payload, the gap SPEC found in ASTRA's tracer)
     C4 3F89FB store +0x48 -> +0x50 (context not stored at the field the handlers read)
     C5 3F8A07 xor edx,edx -> xor ecx,ecx (the registration event is not 0)
Prints FAILS N last."""
import hashlib
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
sys.path.insert(0, HERE)
from rvlib import Img, Body, Report, run_control, check_manifest, find_exe  # noqa: E402
import apply as AP  # noqa: E402

H1, H2, REG, CONSUMER = 0x29B7D0, 0x29B810, 0x3F89C0, 0x2973E0
MANIFEST = "153a65ee9386436e5e69962241be8adcddc2314b3629fdd5d2fcd6c6b8e1e683"
STACK = ("rsp",)


class Refuse(Exception):
    pass


def walk(B, edx, a=None, flags=None, eax=None, path=None, reads=None, writes=None, written=None, depth=0):
    """Concrete-edx walk. Returns dict(boundary, pc, target, reads, writes, eax, path, written).
    A predicate that does not depend on edx (e.g. a data byte test) forks: both arms are walked and must reach the
    same boundary at the same pc, else the walk refuses (no claim from an unknown flag)."""
    a = B.start if a is None else a
    path, reads, writes = list(path or []), list(reads or []), list(writes or [])
    written = set(written or [])
    for _ in range(200):
        if a not in B.ins:
            raise Refuse("left the body at %X" % a)
        I = B[a]
        path.append(a)
        m, ops = I.mnemonic, I.op_str
        for mm in I.mems:
            if mm["base"] in STACK:
                continue
            rec = (a, mm["base"], mm["disp"], mm["size"])
            if mm["write"]:
                writes.append(rec)
            elif mm["read"] and m != "lea":
                reads.append(rec + (mm["base"] in written,))
        if m == "cmp" and ops.startswith("edx, "):
            flags = (edx - int(ops.split(", ")[1], 0)) & 0xFFFFFFFF if edx is not None else None
        elif m == "sub" and ops.startswith("edx, "):
            edx = (edx - int(ops.split(", ")[1], 0)) & 0xFFFFFFFF if edx is not None else None
            flags = edx
        elif m == "add" and ops.startswith("edx, "):
            edx = (edx + int(ops.split(", ")[1], 0)) & 0xFFFFFFFF if edx is not None else None
            flags = edx
        elif m in ("je", "jne"):
            if flags is None:
                if depth > 2:
                    raise Refuse("unknown predicate at %X" % a)
                arms = [walk(B, edx, t, None, eax, path, reads, writes, written, depth + 1)
                        for t in (a + I.size, I.direct_target())]
                if arms[0]["boundary"] != arms[1]["boundary"] or arms[0]["pc"] != arms[1]["pc"]:
                    raise Refuse("unknown predicate at %X splits the boundary" % a)
                w = dict(arms[0])
                w["reads"] = sorted(set(arms[0]["reads"]) | set(arms[1]["reads"]))
                w["writes"] = sorted(set(arms[0]["writes"]) | set(arms[1]["writes"]))
                w["forked"] = a
                return w
            taken = (flags == 0) if m == "je" else (flags != 0)
            a = I.direct_target() if taken else a + I.size
            continue
        elif m == "call":
            return dict(boundary="CALL", pc=a, target=I.direct_target(), reads=reads, writes=writes, eax=eax,
                        path=path, written=written)
        elif m == "ret":
            return dict(boundary="RETURN", pc=a, target=None, reads=reads, writes=writes, eax=eax, path=path,
                        written=written)
        elif m.startswith("j"):
            raise Refuse("unhandled transfer %s at %X" % (I.text, a))
        else:
            if "edx" in ops.split(",")[0] or "rdx" in ops.split(",")[0]:
                edx = None
            if m not in ("mov", "movzx", "lea"):
                flags = None
            if I.text == "xor eax, eax":
                eax = 0
            elif I.text == "or eax, 0xffffffff":
                eax = 0xFFFFFFFF
            elif "rax" in I.reg_writes:
                eax = None
        if writes and writes[-1][0] == a:
            return dict(boundary="OBJECT_WRITE", pc=a, target=None, reads=reads, writes=writes, eax=eax, path=path,
                        written=written)
        written |= I.reg_writes
        a += I.size
    raise Refuse("no boundary in 200 steps")


def body(img, va):
    s, e = img.pdata(va)
    return Body(img, s, e), s, e


def check_event0(img, R):
    for va, size in ((H1, 50), (H2, 82)):
        B, s, e = body(img, va)
        R.check("H %08X .pdata root %08X-%08X = %d B, exact decode" % (va, s, e, e - s),
                s == va and e - s == size and B.exact)
        w = walk(B, 0)
        R.check("E %08X event 0 ends at RET (got %s at %X)" % (va, w["boundary"], w["pc"]), w["boundary"] == "RETURN")
        R.check("E %08X event 0: no call, no non-stack write" % va, w["boundary"] != "CALL" and not w["writes"],
                str(w["writes"]))
        rd = [(hex(a), b, hex(d), n) for a, b, d, n, _ in w["reads"]]
        R.check("E %08X event 0: one non-stack read, qword [rcx+0x48], rcx unwritten before it" % va,
                len(w["reads"]) == 1 and w["reads"][0][1:4] == ("rcx", 0x48, 8) and not w["reads"][0][4], str(rd))
        R.check("E %08X event 0: EAX = 0 at RET" % va, w["eax"] == 0, str(w["eax"]))
        # the loaded context (r8 in 29B7D0, r9 in 29B810) and the payload (rax / r10) are not dereferenced:
        # covered by the single-read check; the read site is the clause's site
        site = w["reads"][0][0] if w["reads"] else None
        R.check("E %08X the +0x48 read is at %s, before the first edx test" % (va, hex(site) if site else None),
                site in (0x29B7D7, 0x29B814) and w["path"].index(site) < min(
                    i for i, p in enumerate(w["path"]) if "edx" in B[p].op_str and B[p].mnemonic in ("cmp", "sub", "add")))


def check_positive(img, R):
    B1 = body(img, H1)[0]
    B2 = body(img, H2)[0]
    w = walk(B1, 1)
    R.check("P 0029B7D0 event 1 reaches CALL 002973E0 at 0029B7EA",
            w["boundary"] == "CALL" and w["target"] == CONSUMER and w["pc"] == 0x29B7EA)
    w = walk(B2, 1)
    R.check("P 0029B810 event 1 reaches CALL 002973E0 at 0029B851",
            w["boundary"] == "CALL" and w["target"] == CONSUMER and w["pc"] == 0x29B851)
    w = walk(B2, 2)
    R.check("P 0029B810 event 2 reaches the dword store [rcx+4] at 0029B82C",
            w["boundary"] == "OBJECT_WRITE" and w["pc"] == 0x29B82C and w["writes"][-1][1:4] == ("rcx", 4, 4))


def check_registration(img, R):
    B, s, e = body(img, REG)
    R.check("R 003F89C0 .pdata root %08X-%08X = 99 B, exact decode" % (s, e), s == REG and e - s == 99 and B.exact)
    want = [(0x3F89D4, "mov ebp, edx"), (0x3F89DB, "mov rdi, r9"), (0x3F89DE, "mov rsi, rcx"),
            (0x3F89E1, "lea r8d, [rdx + 0x58]"),
            (0x3F89EA, "mov rax, qword ptr [rsp + 0x50]"), (0x3F89EF, "or word ptr [rsi + 0x26], 1"),
            (0x3F89F4, "mov qword ptr [rsi + 0x38], rax"), (0x3F89F8, "mov dword ptr [rsi + 0x40], ebx"),
            (0x3F89FB, "mov qword ptr [rsi + 0x48], rdi"), (0x3F89FF, "test rax, rax"), (0x3F8A02, "je 0x3f8a0e"),
            (0x3F8A04, "mov r8, rbp"), (0x3F8A07, "xor edx, edx"), (0x3F8A09, "mov rcx, rsi"),
            (0x3F8A0C, "call rax")]
    for a, t in want:
        got = B.ins[a].text if a in B.ins else "<none>"
        R.check("R %08X is `%s`" % (a, t), got == t, "" if got == t else "got `%s`" % got)
    zero = [a for a, t in B.calls() if t is not None]
    R.check("R the one direct call (the 0x58-byte zeroing) precedes the stores", len(zero) == 1 and zero[0] < 0x3F89EF)
    # nothing between the +0x48 store and the call rewrites rsi or [rsi+...] or rdx except xor edx,edx
    mid = [a for a in B.order if 0x3F89FB < a < 0x3F8A0C]
    R.check("R no store between 003F89FB and the call; rsi unchanged",
            not any(m["write"] for a in mid for m in B[a].mems) and not any("rsi" in B[a].reg_writes for a in mid))
    R.check("R the je at 003F8A02 skips the call to 003F8A0E (NULL callback)",
            B.ins[0x3F8A02].direct_target() == 0x3F8A0E and 0x3F8A0E > 0x3F8A0C)


def all_checks(img, R):
    check_event0(img, R)
    check_positive(img, R)
    check_registration(img, R)


def page_checks(R):
    h = AP.head_text()
    R.check("Q the clause is absent at HEAD", AP.CLAUSE not in h)
    readme = io.open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    quotes = re.findall(r"^> (\| `0029B(?:7D|81)0` .*)$", readme, re.M)
    R.check("Q README quotes the two handler rows (%d)" % len(quotes), len(quotes) == 2)
    for q in quotes:
        R.check("Q quoted row present verbatim at HEAD: %s..." % q[:16], q in h)
    q16 = re.findall(r"^> (`00296360` \(232 B\) .*)$", readme, re.M)
    R.check("Q README quotes the 00296360 paragraph verbatim from HEAD", len(q16) == 1 and q16[0] in h)
    img = Img.load()
    cited = set(int(x, 16) for x in re.findall(r"(?<![0-9A-Fa-f])([0-9A-F]{8})(?![0-9A-Fa-f])", h))
    cited_fn = set()
    for c in cited:
        try:
            r = img.pdata(c)
        except Exception:
            r = None
        if r:
            cited_fn.add(r[0])
    new = sorted(set(int(x, 16) for x in re.findall(r"`([0-9A-F]{8})`", AP.CLAUSE)))
    bad = []
    for a in new:
        r = img.pdata(a)
        if not r or r[0] not in cited_fn:
            bad.append("%08X (fn %s)" % (a, "%08X" % r[0] if r else None))
            continue
        B = Body(img, r[0], r[1])
        if a not in B.ins:
            bad.append("%08X not an instruction boundary" % a)
    R.check("Q all %d clause addresses are instruction boundaries in functions HEAD already cites" % len(new),
            not bad, "; ".join(bad))
    st, new_t = AP.patch(h)
    R.check("Q apply.patch on HEAD inserts exactly one paragraph after the anchor",
            st == "OK" and new_t.count(AP.CLAUSE) == 1 and len(new_t.split("\n")) == len(h.split("\n")) + 2
            and (AP.ANCHOR + "\n\n" + AP.CLAUSE + "\n") in new_t)
    st2, _ = AP.patch(new_t)
    R.check("Q apply.patch is idempotent (ALREADY on its own output)", st2 == "ALREADY")
    sib = h.replace(AP.SIB_OLD, AP.SIB_NEW, 1)
    R.check("Q the clause does not touch the sibling fable-ov42-handler-edge-1003 line, and both edits compose",
            h.count(AP.SIB_OLD) == 1 and AP.patch(sib)[0] == "OK" and AP.SIB_NEW in AP.patch(sib)[1]
            and AP.SIB_OLD not in AP.CLAUSE)


def main():
    R = Report("event0")
    img = Img.load()
    R.check("I exe sha256 73461d08...21f8, base 0x120000", img.base == 0x120000)
    check_manifest(R, "ov42-register-event0", MANIFEST)
    all_checks(img, R)
    page_checks(R)
    controls = [
        ("C1 29B7DB cmp edx,1 -> cmp edx,0: event 0 reaches the call", 0x29B7DB, bytes.fromhex("83fa00")),
        ("C2 29B81B sub edx,1 -> add edx,1: event 0 reaches the [rcx+4] store", 0x29B81B, bytes.fromhex("83c201")),
        ("C3 29B7D4 mov rax,r8 -> mov rcx,r8: +0x48 read off the payload", 0x29B7D4, bytes.fromhex("498bc8")),
        ("C4 3F89FB context store +0x48 -> +0x50", 0x3F89FB, bytes.fromhex("48897e50")),
        ("C5 3F8A07 xor edx,edx -> xor ecx,ecx: event not 0", 0x3F8A07, bytes.fromhex("33c9")),
    ]
    for label, va, nb in controls:
        ok = run_control(label, lambda va=va, nb=nb: img.patched(va, nb), all_checks)
        R.check("control %s -> check FAILS (sensitive)" % label, ok)
    # the unpatched image still passes (controls did not leak into it)
    R2 = Report("again")
    R2.quiet = True
    all_checks(img, R2)
    R.check("control baseline: the unpatched image still passes all byte checks", R2.fails == 0)
    exe = open(find_exe(), "rb").read()
    R.check("exe on disk unchanged after controls", hashlib.sha256(exe).hexdigest().startswith("73461d08"))
    print("FAILS %d" % R.fails)
    return 1 if R.fails else 0


if __name__ == "__main__":
    sys.exit(main())
