"""twoframes_interior.py - interior citations for the F-frontier functions that what-happens-between-two-frames.md cited
by entry only (OPUS, 2026-10-01). 41 of 42 read by hand from the certified image; 003ACA60 is skipped (its whole work is
the entry instruction `or byte [02B3F520], cl`, so no interior instruction does it).

Verifies every anchor in the image (instruction boundary strictly inside the function's extent, recorded mnemonic) before
writing; appends one OPUS section (byte-preserving, CRLF-aware, idempotent). Prints VERIFY, PATCHED / ALREADY, FAILS n."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "22-Middleware-PhyreEngine", "The-Frame", "what-happens-between-two-frames.md")
ROWS = [
 ("0017F070", "once: while byte `01F7F50C` is 0 and `0018CA40()` is non-null, sets the byte to 1 and tail-calls `0018C580` on that object", [("0017F074", "cmp"), ("0017F087", "mov"), ("0017F09A", "jmp")]),
 ("0017F330", "when `0018CA40()` and `001A9930()` are non-null and `001A94B0(001A9930())` is true, tail-calls `0018BB70(0018CA40())`", [("0017F350", "call"), ("0017F355", "test"), ("0017F365", "jmp")]),
 ("001809E0", "when `001A9930()` is non-null and `001A94B0` on it is true, calls `001A5A70` on it, then tail-calls `001AA2C0` on it", [("001809F6", "call"), ("00180A07", "call"), ("00180A18", "jmp")]),
 ("00180A30", "when `001A9930()` is non-null and `001A94B0` on it is true, calls `001A8F80` on it; in every case then tail-calls `0018C2A0(0018CA40())`", [("00180A46", "call"), ("00180A57", "call"), ("00180A68", "jmp")]),
 ("00182410", "returns byte `+0xDB9` of the object `00189120()` returns, or 0 when there is none", [("0018241E", "call"), ("00182423", "movzx")]),
 ("001826E0", "when `00189120()` is non-null, tail-calls `0018B970(0018CA40(), [00193D50() + 0x2B8], 0, 0)`", [("001826F8", "mov"), ("00182707", "xor"), ("00182719", "jmp")]),
 ("00182730", "when `00193D50()` is non-null, calls `001944D0` on it with every other argument 0 or 0.0", [("00182743", "xorps"), ("00182757", "xor"), ("00182770", "call")]),
 ("00183120", "when `005C5230()` is non-zero, tail-calls `0018CB30(0018CA40(), ecx)`", [("00183128", "call"), ("00183139", "mov"), ("00183140", "jmp")]),
 ("00184900", "with `0018CA40()` present: when `005C5230()` is non-zero and `0017D8B0()` is not 2, sets dword `+0xC30` of `00189120()` to 3; then tail-calls `0018C860(0018CA40())`", [("0018491C", "cmp"), ("00184926", "mov"), ("0018493C", "jmp")]),
 ("001863F0", "tail-calls `0018BD30(0018CA40(), dl)`", [("001863F9", "call"), ("00186409", "jmp")]),
 ("001A1460", "copies qword `+8` to `+0x18`", [("001A1464", "mov")]),
 ("001A5A70", "copies qword `+0x90` to `+0x98`", [("001A5A77", "mov")]),
 ("00229F20", "when dword `01FD49E8` is non-zero: marks `\"AO render\"` (`001EB150`), runs `0017F670(1)` and `001826E0`; when it is still non-zero and the argument is non-zero, marks `\"Water effect\"` and runs `0017F330`, `00180A30`, `001EB110` and `001826E0`; then `0017ECF0` and a tail call to `001EB110`", [("00229F38", "call"), ("00229F47", "call"), ("00229F60", "call"), ("00229F79", "call"), ("00229F83", "jmp")]),
 ("0022A490", "stores `edx` in dword `02064AA0`, then increments byte `02064AD0` when `0022A580()` is non-zero", [("0022A49A", "call"), ("0022A4A3", "inc")]),
 ("002385D0", "for a group index up to `0x1B`, reads the signed loader id from the byte table `01E09F68`; when it is not negative, calls `008478A0(id)` and returns `00384420(id, rdx, 00914698, that result, 8, 4)`; otherwise 0", [("002385E8", "movzx"), ("002385FA", "call"), ("0023861E", "call"), ("0023862E", "xor")]),
 ("0024B240", "appends `rcx` to the 256-qword array at `02091950` and increments the word count `0209216A`; at 256 entries it tail-jumps to `00182CA0` instead", [("0024B24F", "jae"), ("0024B25F", "mov"), ("0024B263", "inc")]),
 ("00253C20", "returns 1 when `0035D050()` is non-zero and dword `02092730` is 0 or 3, else 0", [("00253C24", "call"), ("00253C2D", "mov"), ("00253C37", "cmp"), ("00253C3C", "mov")]),
 ("0026E1A0", "multiplies the four 16-byte float vectors `0209A380`, `0209A370`, `0209A390` and `0209A3C0` lane by lane and stores the product at `0209A3B0`", [("0026E1A7", "mulps"), ("0026E1B5", "mulps"), ("0026E1BC", "movaps")]),
 ("002D7F20", "returns entry `ecx` of an eleven-dword table built on the stack (the eight dwords at `00917230`, then `0x100`, `0x200`, `0x400`); 0 when `ecx` is above 10", [("002D7F43", "mov"), ("002D7F66", "cmp"), ("002D7F82", "mov")]),
 ("002F3860", "stores into qword `02F97348` either `[[rcx+8]+0x10]` or, when byte `[rcx]` is `0xF0`, `[rcx+0x18]`; then tail-jumps to `0024ED80`", [("002F3863", "je"), ("002F386D", "mov"), ("002F387D", "mov"), ("002F3884", "jmp")]),
 ("0033FA20", "calls `0035B8D0`, then tail-calls `0016D6A0` with `xmm0` = 0.0", [("0033FA24", "call"), ("0033FA29", "xorps"), ("0033FA30", "jmp")]),
 ("00353260", "reads three values from `00267E10` on argument 4; when `00267310(byte +0x15 of argument 2)` is 0, calls `002F1A90(third, second, first)`", [("0035327D", "call"), ("0035329C", "call"), ("003532AC", "call")]),
 ("0035B7D0", "a fixed call sequence: `00358750(0, 1)`, `003586E0`, `00358580`, `00358670`, `003585B0` (each with 0, 0), `003586C0(0)`, `00358560(0)`, `002E1CD0(0, 0)`, `002E1C40(0, 4)`, `00368AA0(0, 0)`, then a tail call to `001848C0`", [("0035B7DB", "call"), ("0035B816", "call"), ("0035B822", "call"), ("0035B834", "jmp")]),
 ("0035EDE0", "returns a mask: for each of bits 0-15 that is set in `edx`, reads the signed byte at `022CB114 + 0x294*ecx + bit`, and when it is not negative sets that bit number in the result", [("0035EDF5", "imul"), ("0035EE1F", "movsx"), ("0035EE2E", "or"), ("0035EE42", "mov")]),
 ("00368AE0", "calls `00863650` with the sign-extended argument, then `00368B00`; it does not return (an `int3` follows)", [("00368AE4", "movsxd"), ("00368AE7", "call"), ("00368AEC", "call")]),
 ("00368C10", "an endless loop over slot `[rcx]` (byte): calls `00863650` with qword `022D7F68 + 8*slot`, calls the function pointer at `022D7F70 + 8*slot` when it is set and clears it, then calls `00863520(dword 022CFEF4 + 4*slot, 0x24)`", [("00368C38", "call"), ("00368C4A", "call"), ("00368C59", "mov"), ("00368C61", "call"), ("00368C66", "jmp")]),
 ("0036E810", "when `ecx` is non-zero, passes a stack record {mode 2 when `edx` is 1 else 1, byte `r8b`, float `xmm3`} to `0024FAE0`; otherwise calls `0024FA40`", [("0036E83B", "movss"), ("0036E841", "mov"), ("0036E84A", "call"), ("0036E861", "call")]),
 ("0036F410", "calls `0026E1A0` and `003ECE60`, then tail-calls `003ED7F0(1)`", [("0036F414", "call"), ("0036F419", "call"), ("0036F427", "jmp")]),
 ("003769E0", "copies the 16 bytes at `020926C0` to `0209A380`", [("003769E7", "movaps")]),
 ("003A1E10", "calls `004FE420(02EBEFC0, rcx, edx)`, then tail-calls `004FE420(02EBEFD8, rcx, rcx + edx)`", [("003A1E2C", "call"), ("003A1E31", "lea"), ("003A1E49", "jmp")]),
 ("003ACA70", "clears the bits of `cl` in byte `02B3F520`", [("003ACA72", "and")]),
 ("003B4770", "indexes the 96-byte records at `[02B404E0]` by `cl`; returns the record plus `0x20` when its dword `+0` equals `ecx`, else 0", [("003B4777", "shl"), ("003B477B", "add"), ("003B4782", "cmp"), ("003B478B", "xor")]),
 ("003B6B80", "indexes the `0xE0`-byte records at `[02B40528]` by `cl`; when the record's dword `+0x10` equals `ecx`, stores `xmm1` at `+0x14`", [("003B6B83", "imul"), ("003B6B91", "cmp"), ("003B6B96", "movss")]),
 ("003E6F70", "tail-jumps to `003E56A0` when qword `+0x400` is non-zero, else returns 0", [("003E6F78", "jne"), ("003E6F7E", "xor")]),
 ("00425DC0", "calls `0051D1D0`, then walks the `0x740`-byte records of `[022C6F28]` from the index in dword `+0x48800`, calling `003E6680` on each and following its word `+4` until -1", [("00425DC4", "call"), ("00425DE3", "imul"), ("00425DEE", "call"), ("00425DFA", "movsx")]),
 ("004264A0", "stores in word `+0x4882C` of `[022C6F28]` the value `002E9B80(003590D0())`, or -1 when `003590D0()` is 0; then calls `00425FB0(0042D050, 0042CBF0, [022C6F28])` and tail-jumps to `00428980`", [("004264AF", "call"), ("004264BB", "mov"), ("004264CE", "mov"), ("004264EA", "call"), ("004264F3", "jmp")]),
 ("00428E40", "when byte `+0x48842` of `[022C6F28]` is 1 and byte `+0x48843` is 0, calls `00426420` and tail-calls `00521440`", [("00428E4B", "cmp"), ("00428E54", "cmp"), ("00428E5D", "call"), ("00428E66", "jmp")]),
 ("0046EDD0", "for id `+0xC`: when `0035B240(id)` has any bit other than bit 2, reads an integer through `00537410`, divides it as a float by the constant at `00906A44`, passes it to `0035B550` and returns 1; otherwise calls `0035B1A0(id)` and returns 0", [("0046EDE1", "test"), ("0046EDF0", "call"), ("0046EE01", "divss"), ("0046EE09", "call"), ("0046EE1C", "call")]),
 ("00474600", "builds a stack record {16 zero bytes, the 24-byte entry `02EBEFC0 + 24*[02EBEFF0]`} and passes it with `rcx` and its fifth argument to `003A22A0`, then calls `003A1DB0`", [("0047461D", "lea"), ("0047462C", "mov"), ("0047463C", "call"), ("00474641", "call")]),
 ("00475390", "when dword `02EBA4C0` is non-zero and dword `02EBA4D0` is 0, tail-calls `00474710(02EBA4C0)`", [("00475399", "cmp"), ("004753A2", "lea"), ("004753A9", "jmp")]),
 ("00504490", "calls `0016D6A0(0)`, then tail-calls `003A1DB0`", [("00504494", "xor"), ("00504496", "call"), ("0050449F", "jmp")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "`003ACA60` is not here: its whole work is the entry instruction. Verified by "
        "[`twoframes_interior.py`](../../_index/candidates/opus-twoframes-interior-1001/twoframes_interior.py): every anchor is "
        "an instruction boundary inside its function and decodes to the recorded mnemonic.*\n\n"
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
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
