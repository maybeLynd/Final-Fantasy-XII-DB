"""renderrec_interior.py [--apply] - interior citations for the F-frontier functions that the-character-render-record-array.md cited
by entry only (OPUS, 2026-10-01). All 27 read by hand from the certified image; every rip target was resolved with retool.py
and every float constant read from the image.

Verifies every anchor in the image (instruction boundary strictly inside the function's extent, recorded mnemonic) and
refuses a pipe in any sentence. Without --apply it only verifies; with --apply it appends one OPUS section
(byte-preserving, CRLF-aware, idempotent). Prints VERIFY, PATCHED / ALREADY / DRY, FAILS n."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "17-Presentation-Rendering", "Character-Render-Records", "the-character-render-record-array.md")
ROWS = [
 ("0015CC90", "calls `001E1520(01F82D60, 20000)`, then tail-jumps to `00808B90(008A6C70)`", [("0015CC94", "mov"), ("0015CCA0", "call"), ("0015CCB0", "jmp")]),
 ("002E87F0", "for a non-null `rcx` whose dword `+0` and word `+0` are not -1, takes the 0x740-byte record (signed word `+0`) of `[022C6F28]`; when its dword `+0x284` is non-zero: with `edx` non-zero clears bit 13 and sets bit 12 of dword `+0x304`, with `edx` 0 clears bits 12-13; either way sets bit 22 of dword `+0x290`", [("002E8817", "imul"), ("002E8827", "cmp"), ("002E8830", "and"), ("002E883A", "or"), ("002E887F", "and")]),
 ("00332510", "stores `022C6F30` in qword `022C6F20` and calls `001EB150(\"display character : preprocessing\" at 00D10A38)`, `004264A0` and `001EB110`; stores it again and calls `001EB150(\"display character : draw objects\" at 00D10A80)`, `0041E4D0([022C6F20])` and `001EB110`; calls `001EB150(\"display character : after emission\" at 00D10AA8)` and `00425DC0` with qword `022C6F28` as read before the second string, then tail-jumps to `001EB110`", [("00332528", "mov"), ("0033252F", "call"), ("0033255F", "call"), ("00332578", "call"), ("00332587", "jmp")]),
 ("00342410", "calls `002E88A0(rdx, 1)`, then tail-calls `002E8900(rdx)` with `xmm1` = `00267DB0(r9)`", [("00342421", "call"), ("00342431", "call"), ("00342446", "jmp")]),
 ("00342CF0", "calls `002E8950(rdx, 1)`, then tail-calls `002E89B0(rdx)` with `xmm1` = `00267DB0(r9)`", [("00342D01", "call"), ("00342D11", "call"), ("00342D26", "jmp")]),
 ("003B6000", "clears bit 0 of byte `+0x40` of record `cl` of the 0xE0-byte records at `[02B40528]` when its dword `+0x10` equals `ecx`", [("003B6003", "imul"), ("003B600A", "add"), ("003B6011", "cmp"), ("003B6016", "and")]),
 ("0041CEA0", "when qword `+0x18` is non-null, sets bit 3 of dword `+0xC` when `edx` is 1, else clears it", [("0041CEA7", "cmp"), ("0041CEAC", "or"), ("0041CEB1", "and")]),
 ("00423050", "when dword `+0xC4` is not -1, looks up `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC4)` and tail-calls `0041C6B0` on it; returns 0 when there is none", [("00423056", "cmp"), ("00423065", "call"), ("00423077", "call"), ("00423089", "jmp"), ("0042308E", "xor")]),
 ("00423570", "when dword `+0xC4` is not -1, looks up `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC4)` and, when found, calls `0041CEA0(it, edx)`", [("0042357A", "cmp"), ("0042359D", "call"), ("004235AC", "call")]),
 ("00423AB0", "stores `xmm1` in float `+0x2BC`; when dword `+0xC4` is not -1, looks up `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC4)` and, when found, calls `0041C7C0(it)` with `xmm1`", [("00423AC8", "movss"), ("00423AE7", "call"), ("00423AF7", "call")]),
 ("004270A0", "when `xmm1` is 0.0, calls `00426FA0` and sets dword `+0x294` to (itself AND `0xFFFDFA7F`) OR 0x20; otherwise stores `xmm1` in float `+0x308` and sets `+0x294` to (itself AND `0xFFFDFB5F`) with bit 8 set", [("004270AC", "ucomiss"), ("004270B3", "call"), ("004270BE", "and"), ("004270D2", "movss"), ("004270E5", "bts")]),
 ("004272C0", "sets bit 23 of dword `+0x294`, stores `xmm1` in float `+0x3C0` and `r8d` in dword `+0x3C4`", [("004272CA", "movss"), ("004272D2", "mov")]),
 ("004272E0", "sets dword `+0x294` to (itself AND `0xFFFDFA7F`) OR 0x20", [("004272E6", "and"), ("004272EB", "or"), ("004272EE", "mov")]),
 ("00427300", "sets bit 15 of dword `+0x294` and stores `xmm1` in float `+0x3BC`", [("0042730A", "movss")]),
 ("00427880", "sets bit 16 of dword `+0x294` and stores `xmm1`, `xmm2` and `xmm3` in floats `+0x3C0`, `+0x3C4` and `+0x3C8`", [("0042788A", "movss"), ("00427892", "movss"), ("0042789A", "movss")]),
 ("004278B0", "sets bit 22 of dword `+0x294` and stores `edx` in dword `+0x3C4`", [("004278BA", "mov")]),
 ("00428DE0", "sets bit 10 of dword `+0x304` when `edx` is non-zero, else clears it, and sets bit 29 of dword `+0x290`", [("00428DEA", "neg"), ("00428DEE", "and"), ("00428DF3", "or"), ("00428DF9", "or")]),
 ("00428E10", "sets bit 11 of dword `+0x304` when `edx` is non-zero, else clears it, and sets bit 30 of dword `+0x290`", [("00428E1A", "neg"), ("00428E1E", "and"), ("00428E23", "or"), ("00428E29", "or")]),
 ("0042D810", "copies bit 0 of byte `+0x60` of `rdx` into bit 3 of byte `+0x4B7`", [("0042D814", "shl"), ("0042D81D", "and"), ("0042D81F", "xor")]),
 ("0042E300", "when word `+0x2F2` is non-zero, copies word `+0x20` of `rdx` to word `+0x3FA`", [("0042E308", "je"), ("0042E30A", "movzx"), ("0042E30E", "mov")]),
 ("0042E320", "when word `+6` is -1 or word `+0x2F2` is 1, tail-calls `0016D6A0(rcx, qword +0x18 of rdx, 0, 1)`", [("0042E327", "cmp"), ("0042E331", "mov"), ("0042E33B", "xor"), ("0042E33E", "jmp")]),
 ("0042E350", "when word `+6` is -1 or word `+0x2F2` is 1, tail-calls `0016D6A0(rcx, qword +0x18 of rdx, dword +0x20 of rdx, 1)`", [("0042E357", "cmp"), ("0042E361", "mov"), ("0042E36B", "mov"), ("0042E36F", "jmp")]),
 ("0042E4B0", "when word `+6` is -1 or word `+0x2F2` is 1, calls `0016D6A0` with its own incoming arguments; then, when word `+6` is -1, zeroes dword `+0x58` of `rdx`", [("0042E4C7", "cmp"), ("0042E4D1", "call"), ("0042E4D6", "cmp"), ("0042E4DD", "mov")]),
 ("00504740", "returns 1.0 (`01CEBBA8`) unless a match is found: for a non-null `rcx` with dword `+0x208` not -1, takes A = dword `+0x1F8` + dword `+0x208` (a 32-bit sum used as an address), scans the byte `A+0x30` count of 0xE0-byte records from `A` + word `A+0x38` for one whose byte `+0` equals signed byte `+0xB8` of `rcx`, and returns that record's float `+0x18`", [("0050475E", "add"), ("00504764", "movzx"), ("0050478B", "cmp"), ("00504796", "add"), ("005047AD", "movss")]),
 ("0051EE10", "zeroes dwords `+0` and `+0x10` and qword `+8`, and stores 0x800 in qword `+0x14`", [("0051EE12", "mov"), ("0051EE1A", "mov"), ("0051EE1C", "mov"), ("0051EE20", "mov")]),
 ("0051EE30", "copies from `rdx` its qword `+8` passed through `003AB880` (null stays null) and its dwords `+0x10`, `+0x14` and `+0x18`", [("0051EE4F", "call"), ("0051EE54", "mov"), ("0051EE5B", "mov"), ("0051EE67", "mov")]),
 ("0051F020", "stores `003AB8B0(edx, dword [rcx])` in qword `+8` and `edx` in dword `+0x10`, calls `003AB880` on the new qword, and when `r8d` is 1 zeroes `edx` bytes at `003AB7F0(qword +8)` with `00861EC0`", [("0051F03C", "call"), ("0051F044", "mov"), ("0051F04B", "call"), ("0051F059", "call"), ("0051F066", "call")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`renderrec_interior.py`](../../_index/candidates/opus-renderrec-interior-1001/renderrec_interior.py): every "
        "anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*\n\n"
        "| function | size | what the body does | interior anchors |\n|---|---|---|---|\n")
fails = 0
sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
for fn, text, anchors in ROWS:
    f = int(fn, 16)
    n = sizes.get(f)
    if not n:
        print("VERIFY FAIL %s: not a function entry" % fn); fails += 1; continue
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for a, mn in anchors:
        av = int(a, 16)
        if not (f < av < f + n):
            print("VERIFY FAIL %s: anchor %s outside the body" % (fn, a)); fails += 1
        elif ins.get(av) != mn:
            print("VERIFY FAIL %s: %s decodes to %r, recorded %r" % (fn, a, ins.get(av), mn)); fails += 1
    if "|" in text:
        print("VERIFY FAIL %s: pipe in text" % fn); fails += 1
print("VERIFY %d functions, %d anchors" % (len(ROWS), sum(len(r[2]) for r in ROWS)))
if not fails:
    body = HEAD + "".join("| `%s` | %d B | %s | %s |\n" % (fn, sizes[int(fn, 16)], text, ", ".join("`%s`" % a for a, _m in anchors))
                          for fn, text, anchors in ROWS)
    b = open(P, "rb").read()
    crlf = b"\r\n" in b[:4000]
    s = body.encode("utf-8")
    if crlf:
        s = s.replace(b"\n", b"\r\n")
    if HEAD.splitlines()[0].encode("utf-8") in b:
        print("ALREADY")
    elif "--apply" not in sys.argv:
        print("DRY (verified; --apply writes)")
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
