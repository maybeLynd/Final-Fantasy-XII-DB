"""console_interior.py [--apply] - interior citations for the F-frontier functions that what-the-console-tunes.md cited by
entry only (OPUS, 2026-10-01). All 35 read by hand from the certified image; every rip target was resolved with retool.py
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

P = os.path.join(DB, "00-Engine-Core-Runtime", "Developer-Tuning-Console", "what-the-console-tunes.md")
ROWS = [
 ("0015CC00", "stores the pointer `001F0850()` returns in qword `01F812C8`", [("0015CC09", "mov")]),
 ("0017E010", "returns the address of the 8-byte entry `01DF0018 + 8*[dword 01DF0010]`", [("0017E017", "lea"), ("0017E01E", "mov")]),
 ("0017E7A0", "adds `ecx` to dword `01DF0010` and stores the sum, except that a negative sum is stored as 2 and a sum above 2 as 0", [("0017E7AA", "mov"), ("0017E7BA", "cmovg"), ("0017E7BD", "mov")]),
 ("0017F5E0", "returns dword `+0x168` of the object `001AD440()` returns, or -1 when there is none", [("0017F5F3", "mov"), ("0017F5FE", "or")]),
 ("00182E10", "when `001DDAB0()` is non-null, calls `001DC940(it, cl)`, then tail-jumps to `001DC730` with `001DDAB0()` in `rcx`", [("00182E2E", "call"), ("00182E40", "jmp")]),
 ("001846B0", "calls `001E0580` and `001EB940(001EBA40())`, copies float `01F7F53C` to `02CB8138`, then tail-calls `0018CCF0(0018CA40(), 1)`", [("001846C1", "call"), ("001846CE", "movss"), ("001846E4", "jmp")]),
 ("001846F0", "calls `001E0580`, copies float `02CB8138` back to `01F7F53C` and zeroes `02CB8138`, calls `0018CCF0(0018CA40(), 0)`, then tail-calls `001EB7B0(001EBA40(), ecx)`", [("00184708", "movss"), ("00184710", "movss"), ("00184722", "call"), ("00184736", "jmp")]),
 ("00189110", "copies byte `+8` of the object at qword `+0x10` to byte `+9` of the object that object's first qword points to", [("00189117", "movzx"), ("0018911B", "mov")]),
 ("0018A790", "returns 1 when bytes `+0` and `+1` are both non-zero, else 0", [("0018A795", "cmp"), ("0018A79B", "mov")]),
 ("0018A7B0", "returns 1 when bytes `+0` and `+2` are both non-zero, else 0", [("0018A7B5", "cmp"), ("0018A7BB", "mov")]),
 ("00196710", "works on the pointer table at qword `+0xDF8` of `00796E20()`: for entries at offsets `0x118`-`0x148` up to the first null, calls `00861EC0(entry + 0x30, 0, 0x100)`; for each non-null entry at `0x88`-`0x110`, zeroes the 17 bytes at `+0x30`; for the entry at `0x150`, zeroes word `+0x1E0` and byte `+0x1E2`", [("0019673B", "mov"), ("00196741", "call"), ("00196782", "mov"), ("001967B5", "mov"), ("001967BC", "mov")]),
 ("001AC7A0", "returns `rcx + 0x204 + 32*[dword +0x200]` (32-byte records from `+0x204`)", [("001AC7A7", "shl"), ("001AC7AB", "add")]),
 ("001AC7C0", "when byte `+0xA4` is non-zero and dword `+0xA8` is -2, sets `+0xA8` to -1 and, when `001F0850()` is non-null, tail-calls `001EF540(it, 1)`", [("001AC7C4", "cmp"), ("001AC7CD", "cmp"), ("001AC7D6", "mov"), ("001AC7F8", "jmp")]),
 ("001AD4D0", "stores `edx` modulo the qword count of the vector at `[+0xE8]` in dword `+0x168`, or 0 when that vector is empty", [("001AD4E1", "sar"), ("001AD4F9", "div"), ("001AD4FC", "mov"), ("001AD503", "mov")]),
 ("001BD9D0", "takes float `01DFE194` when byte `01DFE190` is set and its magnitude is at least 0.001 (double `008F9558`), else 0.0; stores that in float `02CB8154`, or 0.0 when byte `+0x118` of `001EBA40()` is set", [("001BD9EA", "movss"), ("001BDA0B", "comisd"), ("001BDA19", "cmp"), ("001BDA22", "movss"), ("001BDA3E", "movss")]),
 ("001BE660", "zeroes qwords `+0`, `+8` and `+0x10`, calls `001EDF00(rcx + 0x18, r8)`, then `001A4BF0(rcx, rdx, rdx + strlen(rdx))` for the C string in `rdx`; returns `rcx`", [("001BE66F", "mov"), ("001BE684", "call"), ("001BE693", "cmp"), ("001BE6A3", "call")]),
 ("001C0440", "returns float `+0x20` of the record at qword `+0x18` when the count of 40-byte elements in `[+0x58, +0x60)` is non-zero and qword `+0x10` is non-null, else 0.0", [("001C0452", "imul"), ("001C0455", "sar"), ("001C046B", "cmp"), ("001C0476", "movss")]),
 ("001C0630", "returns float `+0x34` of the record at qword `+0x18` when the count of 40-byte elements in `[+0x58, +0x60)` is non-zero and qword `+0x10` is non-null, else 0.0", [("001C0642", "imul"), ("001C0657", "cmp"), ("001C0662", "movss")]),
 ("001C4F50", "starts a stack vector from the constant (1, 0, 0, 1) at `008FCCA0`; calls `00203170` on a stack block, `00202F70` with the stack (fifth) argument and `00202F00` with `xmm3`, each multiplied by 3.14159 (`008FCC94`) and divided by 180 (`008F3138`), then `00202B70`; stores the result's first float through `rcx`, its second through `rdx` and its third, negated by the sign mask `01CEBDA0`, through `r8`", [("001C4F73", "movaps"), ("001C4FA4", "mulss"), ("001C4FB1", "divss"), ("001C4FF2", "call"), ("001C500D", "xorps")]),
 ("001D5230", "steps dword `+0xC` up when `dl` is non-zero, else down, wrapping 4 to 0 and a negative value to 3", [("001D5234", "inc"), ("001D5239", "dec"), ("001D5244", "mov"), ("001D5256", "cmovs")]),
 ("001DBB00", "tail-calls `002112D0(00210B30(), edx != 0, ecx)`", [("001DBB0E", "setne"), ("001DBB11", "call"), ("001DBB29", "jmp")]),
 ("001DC940", "steps an index up when `dl` is non-zero, else down, with wrap-around: when dword `+8` of `[01F82D20]` is 0, dword `+0x38` modulo `[+0x20]` (plus one slot when the 28-byte entry `[+0x40] + 0x1C*[+0x20]` has non-zero dwords `+0` and `+4`); otherwise dword `+0x24` modulo `[+0x20]`", [("001DC947", "cmp"), ("001DC955", "imul"), ("001DC976", "div"), ("001DC99A", "div")]),
 ("001DC9C0", "returns `[+0x78] + 0x140*[dword +0x48]` (320-byte records)", [("001DC9C3", "lea"), ("001DC9C7", "shl"), ("001DC9CB", "add")]),
 ("001DD090", "returns dword `+0x130` of the 320-byte record `[+0x78] + 0x140*[+0x48]`, or dword `+0x5C` when `[+0x78]` is null", [("001DD094", "test"), ("001DD0A0", "shl"), ("001DD0A4", "mov"), ("001DD0AC", "mov")]),
 ("001E3E90", "returns qword `+0x80` of `[[rcx+0x18]]` minus its low bit", [("001E3E94", "mov"), ("001E3EA5", "and"), ("001E3EA8", "sub")]),
 ("001EF500", "sets dwords `+0x130` and `+0x134` to 6 when `+0x130` was 2, else to 2", [("001EF50A", "cmp"), ("001EF510", "cmove"), ("001EF519", "mov")]),
 ("0020D9F0", "calls virtual slot 1 (`[vtable+8]`) on `rcx`, then on each object along the qword `+8` links, until one returns non-zero; returns 1 when one did, else 0", [("0020DA0A", "call"), ("0020DA11", "mov"), ("0020DA25", "call"), ("0020DA43", "xor")]),
 ("002112D0", "on a stack object: `007A4380`, `007A4C70(r8d)`, then `007A45C0` with float 1.0 (`01CEBBA8`) when `dl` is non-zero, else 0.0, and finally `001243B0`", [("002112EF", "call"), ("002112FC", "call"), ("00211316", "movss"), ("0021131E", "call"), ("00211329", "call")]),
 ("002D4F90", "for `ecx` 1 to 5, stores it in dword `01E0CF88` and zeroes dword `0209E65C`; any other value is ignored", [("002D4F93", "cmp"), ("002D4F98", "mov"), ("002D4F9E", "mov")]),
 ("002F1CD0", "stores `ecx` in dword `022BE7D8` and `edx` in dword `01EEBAE0`", [("002F1CD6", "mov")]),
 ("002F4510", "stores `ecx` in dword `022BE7DC` and `edx` in dword `01EEBAE4`", [("002F4516", "mov")]),
 ("00308E80", "reads qword entry `ecx` of the table at `022C24E0`; when it is non-null and its byte `+4` is below 6, returns qword entry `[+4]` of the table at `01EEC268`; otherwise returns the string `\"Nobody\"` at `00D10394`", [("00308E8A", "mov"), ("00308E9B", "cmp"), ("00308EA2", "mov"), ("00308EAB", "lea")]),
 ("003091C0", "calls `0031ABF0(003272F0())`; when that is non-null and `00265970` on it is non-null, calls `00265020(it, rcx, rdx, r8)`", [("003091DD", "call"), ("003091E4", "call"), ("003091F4", "call"), ("0030920A", "call")]),
 ("0050D360", "when `00267E10(r9)` is non-zero, tail-calls `0026FAD0(0, 00265920(), byte +0x15 of rdx)`; otherwise tail-calls `0026FE50(0)`", [("0050D36C", "call"), ("0050D375", "movzx"), ("0050D38A", "jmp"), ("0050D396", "jmp")]),
 ("005DDDB0", "passes the qword vector at `+0x1010` to `001A5A80` with its capacity in qwords and zeroes its three pointers; then, for the buffers at `+0x4A8` (size dword `+0x4A0`) and `+0x480` (size dword `+0x478`), calls `005F01B0` and `005F03A0` when bit 31 of the size is clear, and zeroes pointer and size", [("005DDDEB", "call"), ("005DDDF1", "mov"), ("005DDE0D", "btr"), ("005DDE18", "call"), ("005DDE47", "call")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`console_interior.py`](../../_index/candidates/opus-console-interior-1001/console_interior.py): every "
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
