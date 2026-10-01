"""soundvoice_interior.py [--apply] - interior citations for the F-frontier functions that
how-a-sound-request-becomes-a-voice.md cited by entry only (OPUS, 2026-10-01). All 42 read by hand from the certified
image; every rip target was resolved with retool.py and every string read from the image.

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

P = os.path.join(DB, "18-Audio", "Audio-Boundary", "how-a-sound-request-becomes-a-voice.md")
ROWS = [
 ("0015CAF0", "stores the pointer `00193D50()` returns in qword `01F81300`", [("0015CAF4", "call"), ("0015CAF9", "mov")]),
 ("002031A0", "compares the byte range `[rcx, rdx)` with `[r8, r9)`, each byte first passed through `0020B000(fifth argument, byte)`; returns the position in the first range just past a prefix equal to the whole second range, else `rcx`", [("002031E3", "call"), ("002031F4", "call"), ("002031FF", "cmp"), ("0020320C", "cmove")]),
 ("002032E0", "with bit 8 of its sixth argument set tail-jumps to `00203240`, with bit 11 set to `002031A0`; otherwise does the same prefix test with plain byte equality: returns the position in `[rcx, rdx)` just past a prefix equal to the whole of `[r8, r9)`, else `rcx`", [("002032EA", "bt"), ("002032F8", "jb"), ("00203318", "cmp"), ("00203324", "cmove")]),
 ("00203330", "zeroes the three qwords at `rcx`, then for a non-empty `[rdx, r8)` allocates its length through `001DF990`, copies the bytes through the import at `008C2A40` and sets begin, end and capacity end", [("0020335E", "mov"), ("00203371", "call"), ("00203394", "call"), ("0020339E", "mov")]),
 ("002038A0", "for `rdx` 16-byte elements from `rcx`, zeroes both qwords of each (the stores are skipped when `rcx` is null)", [("002038B9", "mov"), ("002038C0", "add"), ("002038C4", "sub")]),
 ("00203900", "for `rdx` 24-byte elements from `rcx`, zeroes qwords `+0` and `+8` and byte `+0x10` of each (the stores are skipped when `rcx` is null)", [("00203919", "mov"), ("00203920", "mov"), ("00203923", "add")]),
 ("00203940", "copies the 24-byte elements of `[rcx, rdx)` to `r8` (the stores are skipped when `r8` is null) and returns the destination end", [("00203957", "movups"), ("0020395E", "movsd"), ("00203969", "add"), ("00203976", "mov")]),
 ("002044C0", "passes the vector at `+0x28` to `00209B50` with its capacity in 16-byte elements and the vector at `+8` to `00209AD0` with its capacity in dwords, zeroing each one's three pointers", [("002044E8", "sar"), ("002044EC", "call"), ("00204511", "sar"), ("00204515", "call"), ("0020451A", "mov")]),
 ("00204710", "copies qwords `+0` and `+0x20` from `rdx` to `rcx`, calls `00204820(rcx + 8, rdx + 8)` and `00204950(rcx + 0x28, rdx + 0x28)`, and returns `rcx`", [("00204720", "mov"), ("00204732", "mov"), ("00204736", "call"), ("00204743", "call")]),
 ("00205800", "allocates a 0x30-byte node through `00210EC0` with vtable `009059D8`, dword `+8` = 6 and the rest 0; links it after the node `[rcx+8]` (node `+0x18` = that node, node `+0x10` = its `+0x10`, whose `+0x18` is pointed back at the new node) and stores it in `[rcx+8]`", [("0020580E", "call"), ("00205820", "mov"), ("00205827", "lea"), ("0020586C", "mov"), ("00205878", "mov")]),
 ("00205C30", "returns 1 when dword `+8` of the node `[rcx+8]` is 8, 13 or 20 (bit set `0x102100`), or when it is 2 and dword `+8` of that node's `+0x18` node is 8, 13 or 20; else 0", [("00205C34", "mov"), ("00205C41", "bt"), ("00205C46", "cmp"), ("00205C4B", "mov"), ("00205C57", "bt")]),
 ("00205FE0", "zeroes the three qwords at `rcx`; for a non-zero `rdx` above `0x3FFFFFFFFFFFFFFF` calls the import at `008C2618` with the string \"vector<T> too long\" (`008F6820`), otherwise allocates `rdx` dwords through `00209950`, sets begin, end and capacity end, and returns 1", [("00205FEF", "mov"), ("0020600C", "cmp"), ("00206011", "lea"), ("0020601F", "call"), ("0020602E", "lea")]),
 ("00206050", "zeroes the three qwords at `rcx`; for a non-zero `rdx` above `0x0FFFFFFFFFFFFFFF` calls the import at `008C2618` with \"vector<T> too long\" (`008F6820`), otherwise allocates `rdx` 16-byte elements through `002099D0`, sets begin, end and capacity end, and returns 1", [("0020605F", "mov"), ("0020607C", "cmp"), ("0020608F", "call"), ("0020609D", "shl"), ("002060A4", "mov")]),
 ("00206E90", "calls `00205C70(rcx + 0x40)`, then `00206D30(rcx)`, then `00207E90(rcx + 0x40, the first result)`, and stores the first result in qword `+0x48`", [("00206EA6", "call"), ("00206EB1", "call"), ("00206EBD", "call"), ("00206EC7", "mov")]),
 ("00206EE0", "increments dword `+0x18`, calls `00205D60(rcx + 0x40, the new count)`, `00206D30(rcx)` and `00207E90(rcx + 0x40, that result)`, then `0020A5C0(rcx + 0x20, count + 1, 0)`, and sets bit number dword `+0x20` of the result in the dword bit array at qword `+0x20`", [("00206EEF", "inc"), ("00206EFC", "call"), ("00206F27", "call"), ("00206F45", "shr"), ("00206F50", "bts")]),
 ("002076D0", "calls `00208C60(rcx + 0x40, 8)` and `00206D30(rcx)`, then tail-calls `00207E90(rcx + 0x40, the first result)`", [("002076E2", "mov"), ("002076EB", "call"), ("002076F6", "call"), ("00207711", "jmp")]),
 ("002086D0", "returns 0 when the cursor qword `+0` plus 1 equals the end qword `+0x10`; otherwise returns 1 when the byte there is `(` or `)` and bit 3 of dword `+0x80` is clear, or when it is `{` or `}` and bit 4 is clear; else 0", [("002086D6", "cmp"), ("002086E3", "test"), ("002086EC", "sub"), ("002086F2", "test"), ("002086FB", "sub")]),
 ("00209BC0", "frees an array of `r8` 24-byte elements at `rdx` through `00210EB0`; a count above `0x0AAAAAAAAAAAAAAA` calls the import at `008C2DA8`, and for 0x1000 bytes or more it first checks the 32-byte-aligned block header (`[rdx-8]` below `rdx` by 8 to 0x27 bytes, calling `008C2DA8` otherwise) and frees that real block", [("00209BCE", "cmp"), ("00209BDA", "lea"), ("00209BE2", "cmp"), ("00209BF6", "mov"), ("00209C2D", "jmp")]),
 ("0020B680", "calls `005CD4F0(rcx + 0x58)` and looks key `edx` up in the search tree with header `+0x28` (root qword `+0x38`, node key dword `+0x20`); on a hit it calls `0020B0F0(rcx, [r8])`, then `0020C300` on the hit's record (node `+0x28`), and returns that after `005CD820(rcx + 0x58)`; on a miss it fills the record `001BA860(rcx + 0x98)` returns (when it returns one) with qword `[r8]`, dword `+8` = `r9d`, byte `+0x10` = 1 and the fifth argument in dword `+0x14` (words `+0xC`/`+0xE` set per kind 5, 3 or other), maps it under `edx` through `0020B5F0(rcx + 0x20)`, calls `005CD820(rcx + 0x58)`, adds `r9` to qword `+0x90` and returns a new 16-byte `00217A60(it, [r8], r9d, 0)` object", [("0020B6C8", "cmp"), ("0020B726", "call"), ("0020B746", "call"), ("0020B7DC", "call"), ("0020B819", "add")]),
 ("0020C300", "increments dword `+0x88` and byte `+0x10` of key `edx`'s record (`0020B5F0(rcx + 0x20)`); when the fifth argument is 5 and the sixth is 1-4 it also sets the record's dword `+0x14` to 5; when neither is 5, a fifth argument of 3 copies word `+0xE8` of `[+0x18]` to the record's word `+0xE` and one of 1, 2 or 4 copies word `+0x80` to its word `+0xC`; returns a new 16-byte `00217A60(it, r8, r9d, 0)` object, or 0 when `00210EC0` returns null", [("0020C328", "inc"), ("0020C354", "inc"), ("0020C368", "mov"), ("0020C3C3", "mov"), ("0020C41B", "call")]),
 ("00210A60", "calls `00212910` on qwords `+8` and `+0x10`, then tail-calls it on qword `+0x20`", [("00210A6D", "call"), ("00210A76", "call"), ("00210A84", "jmp")]),
 ("00210C50", "when `r8d` is non-zero, calls `00212B80([+8], r8d)` and tail-calls `00212B80([+0x10], r8d)`; otherwise tail-calls `0021B640([+8], r9d with bit 31 set)` when `edx` is 0, or `0021A100([+0x10], r9d)` when it is not", [("00210C65", "or"), ("00210C6D", "cmovne"), ("00210C7D", "call"), ("00210CA9", "jmp"), ("00210CBC", "jmp")]),
 ("00212910", "walks the ring headed at `+8` (next link qword `+0`) and calls `00222050` on each node's qword `+0x10`", [("00212922", "cmp"), ("00212927", "mov"), ("0021292B", "call"), ("00212930", "mov")]),
 ("00212B80", "walks the ring headed at `+8` (next link qword `+0`) and calls `00222390(node's qword +0x10, edx)` on each node", [("00212BA0", "mov"), ("00212BA6", "call"), ("00212BAB", "mov")]),
 ("00221F40", "walks the ring headed at `+8` through each node's qword `+8` link and returns the first node's qword `+0x10` for which `00225690` on it equals `edx`, else 0", [("00221F5D", "cmp"), ("00221F74", "mov"), ("00221F7F", "call"), ("00221F84", "cmp"), ("00221F8B", "cmp")]),
 ("00222200", "calls `0016D6A0(rcx != 0)` and `0016D6A0(dword +0x30 == 1)`; when `+0x30` is 1 it tail-calls virtual slot 8 (`[vtable+0x40]`); otherwise it calls `00212300(002125E0(), rcx, rdx)` and virtual slot 2 (`[vtable+0x10]`), then writes 0 to address 0", [("00222215", "setne"), ("00222225", "sete"), ("00222243", "call"), ("00222251", "mov"), ("00222277", "jmp")]),
 ("002226A0", "calls `00221780(rcx, 1)`, sets the vtable to `00907910`, calls `007A9060(rcx + 0x38)`, sets qword `+0x40` to `00907880`, zeroes qword `+0x48`, sets dword `+0x50` to -1 and returns `rcx`", [("002226BB", "call"), ("002226C8", "mov"), ("002226CF", "call"), ("002226DB", "mov"), ("002226E7", "mov")]),
 ("00223160", "calls `00223190` with its four register arguments, its fifth argument, then byte 0 and qword 0", [("00223164", "mov"), ("00223168", "mov"), ("00223171", "mov"), ("0022317A", "call")]),
 ("00223300", "for `edx` = -4 tail-calls virtual slot 1 (`[vtable+8]`); for any other value tail-calls `002225B0(rcx, 0)`", [("00223305", "cmp"), ("0022330D", "jmp"), ("00223311", "xor"), ("00223313", "jmp")]),
 ("00224540", "calls `00224570` with its four register arguments, its fifth argument, then byte 0 and qword 0", [("00224544", "mov"), ("00224548", "mov"), ("00224551", "mov"), ("0022455A", "call")]),
 ("00224870", "for `edx` = -1 tail-calls `002225B0(rcx, 0)`; for -4 virtual slot 1 (`[vtable+8]`); otherwise `00222410(rcx, edx)`", [("00224873", "jne"), ("00224877", "jmp"), ("0022487C", "cmp"), ("00224884", "jmp"), ("00224888", "jmp")]),
 ("00225280", "calls `00221E60(rcx, 0)`; when that is non-null, calls `002256F0(it, r9d, r8d)` (the last two arguments swapped)", [("0022528A", "xor"), ("00225292", "call"), ("0022529F", "mov"), ("002252A4", "call")]),
 ("00271500", "returns -1 when `003A1180()` is -1; otherwise tail-calls `002DF220(it, 0x40, 0x7F)`", [("00271504", "call"), ("00271509", "cmp"), ("00271516", "mov"), ("0027151D", "lea"), ("00271525", "jmp")]),
 ("002D09F0", "calls `002D3BA0(ecx, word 02F97392, word 02F97394, word 02F97390, 0, 0)`", [("002D09F4", "movzx"), ("002D09FE", "movzx"), ("002D0A06", "movzx"), ("002D0A15", "call")]),
 ("002DEC30", "calls `001DBC10(ecx)`, then `001DBB50(ecx, edx)` when `ecx` is not negative, and stores `ecx` in dword `0215EF44`", [("002DEC3E", "call"), ("002DEC45", "js"), ("002DEC4B", "call"), ("002DEC50", "mov")]),
 ("002DEC80", "when `ecx` is not negative (or else dword `0215EF44` is, standing in for it) sets byte `0215EF4D` to `0x7F` and calls `001DBC70(that value, 0x7F)`; then calls `001DBC10(ecx)` and, when `ecx` is not negative, `001DBBA0(ecx, edx)`; stores `ecx` in dword `0215EF44`", [("002DEC92", "mov"), ("002DECA1", "mov"), ("002DECA8", "call"), ("002DECBC", "call"), ("002DECC1", "mov")]),
 ("002DED30", "calls `001DBC10(ecx)`, then `001DBBD0(ecx)` when `ecx` is not negative, and stores `ecx` in dword `0215EF44`", [("002DED38", "call"), ("002DED43", "call"), ("002DED48", "mov")]),
 ("002DED70", "when `ecx` is not negative (or else dword `0215EF44` is, standing in for it) sets byte `0215EF4D` to `0x7F` and calls `001DBC70(that value, 0x7F)`; then calls `001DBBD0(ecx)` when `ecx` is not negative and stores `ecx` in dword `0215EF44`", [("002DED7C", "mov"), ("002DED8B", "mov"), ("002DED92", "call"), ("002DED9D", "call"), ("002DEDA2", "mov")]),
 ("002DEDB0", "calls `001DBBD0(ecx)` when `ecx` is not negative and stores `ecx` in dword `0215EF44`", [("002DEDB8", "test"), ("002DEDBC", "call"), ("002DEDC1", "mov")]),
 ("002DEE30", "when `ecx` is not negative (or else dword `0215EF44` is, standing in for it) stores `dl` in byte `0215EF4D` and tail-calls `001DBC70(that value, dl)`; otherwise returns", [("002DEE34", "mov"), ("002DEE3E", "mov"), ("002DEE44", "jmp")]),
 ("002DF010", "returns 0 when `003603C0(ecx)` is non-zero; otherwise tail-calls `001DBDB0(1 when bit 31 of ecx is clear else 0, ecx without bit 31, 0x40, 0x7F)`", [("002DF018", "call"), ("002DF01D", "test"), ("002DF031", "shr"), ("002DF034", "btr"), ("002DF048", "jmp")]),
 ("00360C20", "searches the four 24-byte slots at `022CB9F0` for one whose byte `+0` is non-zero and byte `+1` equals `ecx`, and returns that slot's byte `+0`, else -1 (the first empty slot it notes is not returned)", [("00360C30", "cmp"), ("00360C3B", "cmp"), ("00360C4F", "add"), ("00360C53", "cmp"), ("00360C66", "movzx")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`soundvoice_interior.py`](../../_index/candidates/opus-soundvoice-interior-1001/soundvoice_interior.py): "
        "every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*\n\n"
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
