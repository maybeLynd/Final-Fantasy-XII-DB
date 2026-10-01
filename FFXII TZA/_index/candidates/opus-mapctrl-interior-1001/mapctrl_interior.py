"""mapctrl_interior.py - interior citations for the F-frontier functions that the-map-ctrl-pack.md cited by entry only
(OPUS, 2026-10-01). Every body was read by hand from the certified image (retool.py dis with its '; ->' annotations); every
rip-relative address named in a sentence was resolved by that annotation. Nothing skipped.

Before writing, the script VERIFIES every anchor against the image: it must be an instruction boundary strictly inside its
function's extent (functions.tsv) and decode to the recorded mnemonic. Any mismatch -> FAILS, nothing written.
Then it appends one OPUS section to the page (byte-preserving, CRLF-aware, idempotent). Prints VERIFY lines,
PATCHED / ALREADY, FAILS n. Same pattern as opus-gameapp-interior-1001/gameapp_interior.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "03-World-Area-Field", "Map-Pack", "the-map-ctrl-pack.md")
ROWS = [
 ("001806F0", "when `001A9930()` returns an object, stores `ecx` in its dword `+0x20`", [("00180700", "je"), ("00180702", "call"), ("00180707", "mov")]),
 ("00180730", "calls `001A9B70` with the `001A9930()` object as the first argument, followed by this function's own four register arguments and three stack arguments", [("0018074F", "call"), ("00180754", "mov"), ("00180786", "call")]),
 ("001807A0", "when `001A9930()` returns an object, calls `001A9BF0(object, byte +0x1C of 00189120() is non-zero, ecx, edx)`", [("001807C4", "cmp"), ("001807C7", "setne"), ("001807DA", "call")]),
 ("00182280", "when `00189120()` returns an object, calls `00185CD0` on it with this function's four float arguments and its two byte stack arguments", [("001822B3", "je"), ("001822C0", "movzx"), ("001822E6", "call")]),
 ("001A9B70", "passes `r8d` on as 1, 2, 3 or 4 when it is 1 to 4 and as 0 otherwise, calling `001E5790(rdx, that value, r9, ...)` with its four stack arguments passed on (the first in `r9`)", [("001A9B7A", "sub"), ("001A9B96", "mov"), ("001A9BDF", "call")]),
 ("001ACF80", "when `001A9930()` returns an object, walks the list at `+0x10` (`0016D6D0` steps it) for the node whose payload `+0x40` has a non-null `+0x100` and whose string `+0x20` equals the string at that object's `+0x241`; on a match it decrements `+0x30`, unlinks the node (`0016DA60`), frees the node's string and the 0x48-byte node through the allocators at node `+0x38` and this `+0x38`, calls `001AC4B0(this, payload +0x100, payload +0x108)`, sets byte `+0x130`, frees payload `+0x100` (`00210EB0`) and the 0x118-byte payload (`00809950`)", [("001ACFE0", "movzx"), ("001AD014", "dec"), ("001AD078", "call"), ("001AD09D", "call")]),
 ("001E5540", "stores the floats `xmm1` at `+0x1FC` and `xmm2` at `+0x200`, then calls `0060EC30(element, r9d)` for each qword of the array [`+0x18`, `+0x20`)", [("001E5564", "movss"), ("001E5570", "movss"), ("001E5595", "call")]),
 ("00231F50", "zeroes the nine qwords `+0x00` to `+0x40`", [("00231F52", "mov"), ("00231F6D", "mov"), ("00231F71", "mov")]),
 ("0026E290", "on the object `*(0209A670)` with dword `+0x120` non-zero: when dword `0209A708` is set, calls `002F7380(object, *0209A668)` and clears `0209A708`; then calls the object's function pointer `+0x130` with (object, `ecx`) when it is set", [("0026E2A8", "cmp"), ("0026E2C4", "call"), ("0026E2C9", "mov"), ("0026E2E4", "call")]),
 ("0026EDB0", "calls the function pointer at `+0x128` when it is set, then `0016D6A0` on `+0x40` and on `+0xA8`", [("0026EDC9", "call"), ("0026EDD7", "call"), ("0026EDDC", "add")]),
 ("002F6740", "stores the count `[rdx]` at `+0x22C`; when it is positive, stores `rdx + 0x10` at `+0x1A0`, allocates count * 12 bytes through `003EC8D0(6, ...)` into `+0x1D8`, and fills each 12-byte entry with the qword 1 and the float 1.0 at `+8`", [("002F674B", "mov"), ("002F676B", "call"), ("002F679D", "mov"), ("002F67A6", "mov")]),
 ("0034DC70", "tail-calls `003E9020(00267E10(argument 4), 00377B90())`", [("0034DC79", "call"), ("0034DC80", "call"), ("0034DC8F", "jmp")]),
 ("00355300", "when `00267310(byte +0x15 of argument 2)` is non-zero, calls `00473680`, `003E8AA0` (with that byte) and `00466DD0`; then returns 1 when `003E82F0(dword [argument 3])` is non-zero, else 0", [("00355314", "call"), ("0035532A", "call"), ("00355336", "call"), ("00355344", "setne")]),
 ("0037A9B0", "in record `ecx` (0x50 bytes) of the table at `02EBF420`, scans the 8-byte entries from `+0x10` of the list at `+0x18` (count `+4`) for the word equal to `edx` and sets that entry's byte `+2` to 1", [("0037A9BD", "lea"), ("0037A9E3", "cmp"), ("0037A9F7", "mov")]),
 ("0037ACA0", "for `ecx` up to 4, clears byte `+0x4C` of record `ecx` of `02EBF420` (address `02EBF46C`); for `ecx` 0 with the qword `02EBF420` null, tail-jumps to `003774C0`", [("0037ACAF", "lea"), ("0037ACB6", "mov"), ("0037ACC6", "je")]),
 ("0037ACD0", "for `ecx` up to 4, sets byte `+0x4C` of record `ecx` of `02EBF420` to 1 when its qword `+0` is non-null; for `ecx` 0 with the qword `02EBF420` null, tail-jumps to `00379290`", [("0037ACE6", "cmp"), ("0037ACED", "mov"), ("0037ACFE", "je")]),
 ("0037B290", "returns word `+0x10` of the list at `+0x18` of record `ecx` of `02EBF420` when the list exists with a non-zero count `+4`, else -1", [("0037B2A1", "mov"), ("0037B2B1", "movzx"), ("0037B2B6", "or")]),
 ("003B40F0", "with v = its double argument xored with the 16 bytes at `01CEBD90`, returns (float `02B404A8` + float `02B40498` * v) / (float `02B404AC` + float `02B4049C` * v), computed in doubles and rounded through a float", [("003B40F7", "movss"), ("003B4118", "mulsd"), ("003B4133", "divsd"), ("003B4137", "cvtpd2ps")]),
 ("003CD5D0", "for slot `cl` of the 0x40-byte records at `*(02B47790)`: when its dword `+4` equals `ecx`, decrements byte `02B47770`, clears `+4`, clears dword `+0x30` of each node on its `+0x28` chain (linked through `+0x38`), unlinks the record from the list linked through `+0x18` / `+0x20` (ends `02B47778` / `02B47780`) and returns 1; otherwise 0", [("003CD5DE", "cmp"), ("003CD5E3", "dec"), ("003CD600", "mov"), ("003CD61F", "mov")]),
 ("003E8230", "resolves id `ecx` in the table at `*(02B5D080)`: below word `+8`, splits it into id / 100 and id % 100; the group directory at word `+0xC` holds the group count, and each 4-byte group entry a member count (word `+2`) and an offset (word `+4`); returns table + offset + (id % 100) * word `+6`, or 0 when out of range", [("003E8244", "cmp"), ("003E8252", "imul"), ("003E826B", "cmp"), ("003E8289", "imul")]),
 ("003E82A0", "tail-calls `0037B030(0, ecx)`", [("003E82A2", "xor"), ("003E82A4", "jmp")]),
 ("003E82F0", "resolves `ecx` through `003E8230`; when found, tail-calls `003E8350(record, table + word +0xE, 00265920())`, else returns 0", [("003E8306", "call"), ("003E830B", "movzx"), ("003E831B", "call"), ("003E8333", "jmp")]),
 ("003E8860", "clears bit 3 of word `+0` of the record `003E8230(ecx)` resolves", [("003E886E", "call"), ("003E887D", "and")]),
 ("003E8890", "sets bit 3 of word `+0` of the record `003E8230(ecx)` resolves", [("003E889E", "call"), ("003E88A8", "or")]),
 ("003E88C0", "on the record `003E8230(edx)` resolves: clears bit 3 and sets bit 4 of word `+0`, stores `cl` in byte `+0x15` and keeps only the low four bits of byte `+0x12`", [("003E88D3", "call"), ("003E88E8", "mov"), ("003E88EC", "or"), ("003E88F0", "and")]),
 ("003E8900", "as `003E88C0`, and also sets bit 4 of byte `+0x12`", [("003E8913", "call"), ("003E8930", "mov"), ("003E8934", "or")]),
 ("003EC910", "between `0036C1D0(..., 0xB)` and `0036C140`, allocates `edx` bytes through `0036A190`; on null calls `00862690(00D11BF0)` and returns null; otherwise calls `r8` on the block when it is set and returns the block", [("003EC924", "call"), ("003EC92B", "call"), ("003EC944", "call"), ("003EC95F", "call")]),
 ("003EC970", "for `ecx` up to 7, returns the 0x38-byte record `ecx` at `02EBB820` when its qword `+0` is non-null, else 0", [("003EC97A", "lea"), ("003EC981", "imul"), ("003EC98B", "cmove")]),
 ("003ECA70", "for `ecx` >= 0, on record `ecx` (0x38 bytes) at `02EBB820`: calls `003EC8A0` when dword `+8` is positive, clears qword `+0` and dword `+8`, and decrements dword `02EBB9E4`", [("003ECA97", "call"), ("003ECA9E", "mov"), ("003ECAA4", "dec")]),
 ("003ED840", "stores `rcx` at `02B5F1A0`; with n = dword `[rcx + ([rcx] + 1) * 4]` AND `0xFFFFFF`, stores `rcx + n * 16` at `02B5F1B0` when `edx` is greater than n (signed)", [("003ED844", "mov"), ("003ED84F", "mov"), ("003ED865", "mov")]),
 ("00466B10", "for each of the dword `02EBB6E0` 0x50-byte records at `*(02EBB6F0)`, passes `+0x20` and `+0x28` to `003EC8A0`; then passes `02EBB6F0` itself, and clears qword `02EBB6F8` and the count", [("00466B3B", "call"), ("00466B44", "call"), ("00466B5F", "call"), ("00466B6F", "mov")]),
 ("00467D00", "zeroes qword `+0x10`, dword `+0`, qword `+8` and qword `+0x18`", [("00467D02", "mov"), ("00467D08", "mov"), ("00467D0C", "mov")]),
 ("0051EDC0", "returns the qword `+0x70`, `+0x78` or `+0x80` of `*(0209AC30)` for `ecx` 1, 2 or 3, and `+0x68` otherwise", [("0051EDDA", "mov"), ("0051EDE2", "mov"), ("0051EDE7", "mov"), ("0051EDEC", "mov")]),
 ("00536060", "returns 0 when word `+0xE` is 0, else `rcx` + word `+0xC` + dword `+8`", [("0053606A", "xor"), ("0053606D", "movzx"), ("00536077", "add")]),
 ("005360C0", "allocates dword `+0x10` + 0x10 bytes through `003EC8D0(6, ...)`, stores `rcx` at the block's `+0`, links the block through `+8` (the block takes `[rcx+8]`'s old value, that node points at it, `[rcx+8]` becomes it), copies dword `+0x10` bytes from `rdx` to the block's `+0x10` through `00861EBA`, and increments dword `+0x14`", [("005360DB", "call"), ("005360E3", "mov"), ("005360F9", "mov"), ("00536101", "call"), ("00536106", "inc")]),
 ("00291D90", "dispatches on the message `[rdx]`: 1 stores itself at `*(0209AC30) + 0x300`, resets `+0x168` with 1 in its bits 16-19, clears the ten 16-byte slots at `+0xC8` and calls `00247950`; `0x12` clears `*(0209AC30) + 0x300`; 2 steps a state machine kept in bits 16-19 of `+0x168` whose steps copy the ten slots from `0209BEA0`, request `0024A440(qword +0xD0, *01E0C210, 2)` into `+0xC0`, test each slot with `0032E4D0`, release `+0xC0` through `0024A680`, and in one state call `00244F00` on itself; any other message goes to `005C5230`, whose result it returns; messages 1, 2 and `0x12` return 0", [("00291DB7", "cmp"), ("00291F96", "mov"), ("00291F2D", "call"), ("00291E4A", "call")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*The functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`mapctrl_interior.py`](../../_index/candidates/opus-mapctrl-interior-1001/mapctrl_interior.py): every "
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
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
