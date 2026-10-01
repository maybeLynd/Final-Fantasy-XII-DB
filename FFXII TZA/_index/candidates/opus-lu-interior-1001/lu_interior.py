"""lu_interior.py - interior citations for the F-frontier functions that the-largest-unclassified-functions.md cited by entry
only (OPUS, 2026-10-01). Every body was read by hand from the certified image (retool.py dis with its '; ->' annotations); every
rip-relative address named in a sentence was resolved by that annotation. Jump and index tables that sit just past a body
(after 0024E210, 003AA470 and 003B0AD0) are not named, so no text-gap citation is added. Nothing skipped.

Before writing, the script VERIFIES every anchor against the image: it must be an instruction boundary strictly inside its
function's extent (functions.tsv) and decode to the recorded mnemonic. Any mismatch -> FAILS, nothing written.
Then it appends one OPUS section to the page (byte-preserving, CRLF-aware, idempotent). Prints VERIFY lines,
PATCHED / ALREADY, FAILS n. Same pattern as opus-mapctrl-interior-1001/mapctrl_interior.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "99-Unresolved-Residual", "Largest-Unclassified-Code", "the-largest-unclassified-functions.md")
H = "the bucket `020910F0[(handle >> 28) & 0xF]`"
POLL = "otherwise, when `0053DD10()` returns 0, calls `0016D6A0(1)` and returns 1; else returns 0"
ROWS = [
 ("0024E210", "walks " + H + " through `+0x348` for the record whose words `+4` / `+6` equal the handle's low / high words; for a selector `edx` of 0 to 5 returns one bit of that record's word `+0x36A` (bit 5, 6, 7, 8, 9 or 10, picked through a jump table); returns 0 when no record matches or `edx` is above 5", [("0024E225", "mov"), ("0024E238", "cmp"), ("0024E254", "cmp"), ("0024E267", "jmp")]),
 ("0024ED50", "dispatches on the handle's class (`(ecx >> 28) & 0xF`): class 1 tail-calls `002FCFB0`, classes 5, 6 and 9 tail-call `003B0F30`, any other class returns", [("0024ED58", "cmp"), ("0024ED60", "test"), ("0024ED6C", "jmp"), ("0024ED71", "jmp")]),
 ("0024F8D0", "for a non-zero class, walks " + H + " through `+0x348` for the record whose dword `+4` equals the handle and writes `dx & 7` into bits 12-14 of its word `+0x36A`", [("0024F8DA", "lea"), ("0024F8F0", "cmp"), ("0024F90B", "and"), ("0024F916", "or")]),
 ("0024FE30", "dispatches on the handle's class (`(ecx >> 28) & 0xF`): 1 tail-calls `002FD0C0`, 5, 6 and 9 tail-call `003B1260`, 7 tail-calls `003B2830`, any other class returns 0", [("0024FE3B", "je"), ("0024FE45", "jbe"), ("0024FE54", "jmp"), ("0024FE59", "jmp")]),
 ("002EFD80", "when dword `022BDEB8` is non-zero, releases it through `0024CFF0` and clears it; then calls `0036E750(0, 0, &local, ecx, 9)`", [("002EFD92", "call"), ("002EFD97", "mov"), ("002EFDB5", "call")]),
 ("002EFDC0", "the same release of dword `022BDEB8` as `002EFD80`, then stores the result of `0036E750(0, 0, &local, ecx, 9)` in `022BDEB8`", [("002EFDD7", "mov"), ("002EFDF5", "call"), ("002EFDFA", "mov")]),
 ("002FC9B0", "walks the list at `*(02EC3D60)` through `+0x28` and, for each node whose byte `+0x23` low nibble is 5 to 7, adds `word[02EC19C4 + 8 * word +0x20] & 0x1F`; returns the sum", [("002FC9D9", "cmp"), ("002FC9E2", "movzx"), ("002FC9EB", "add"), ("002FC9EE", "mov")]),
 ("002FCB60", "for a non-zero handle, calls `003B0820`; when slot `handle & 0x3F` is below `0x30` and the 0x38-byte record at `02EC32E0 + 0x38 * slot` holds the handle in its dword `+0`, selects arena 8 with `0xA` (`0036C1D0`), calls `002FC3C0(record)` and, when that returns 1, `002FC350(record)`, restores the arena (`0036C140`) and returns 1; else 0", [("002FCB9A", "cmp"), ("002FCBA6", "call"), ("002FCBAE", "call"), ("002FCBBB", "call")]),
 ("002FCFB0", "for a handle whose slot record at `02EC32E0 + 0x38 * (handle & 0x3F)` (slot below `0x30`) holds it and has an object at `+0x10`, sets bit `0x800` of that object's word `+0x36A`", [("002FCFCD", "cmp"), ("002FCFD2", "mov"), ("002FCFE1", "or")]),
 ("002FCFF0", "for each of `0x200` indices stores `0032E400(k, index)` - `k` is `0x26` when `002DEBB0()` returns 0 and `0xB` otherwise - in the dword at `02EC19C0 + 8 * index`; then sets byte `02EC3D7D` to 1", [("002FD024", "cmove"), ("002FD027", "call"), ("002FD02F", "mov"), ("002FD04A", "mov")]),
 ("00341F90", "when the operand's word `+0` and dword `+4` (at `r8`) are both non-negative and `00360C00(dword +4)` returns neither 0 nor 5, calls `00314D40(1)` and returns 1; otherwise, when the operand's byte `+3` has bit `0x40` and `0053DD10()` returns 0, calls `0016D6A0(1)` and returns 1; else 0", [("00341FB6", "cmp"), ("00341FBE", "call"), ("00341FC8", "test"), ("00341FDE", "call")]),
 ("003433A0", "when `002638C0(rdx)` returns a handle, releases it through `0024CFF0` and tail-calls `00269DD0(rdx, 0)`", [("003433AC", "call"), ("003433B7", "call"), ("003433C6", "jmp")]),
 ("00345250", "returns 0 when `003DF0F0(operand +4, operand +0)` is 0; when `003DF0A0` of the same pair is 0 it calls `00314D40(1)` and returns 1; " + POLL, [("00345260", "call"), ("00345274", "call"), ("0034528F", "call"), ("003452A3", "call")]),
 ("00346AA0", "when byte `+0x20` of `rdx` is non-negative and `0036ECA0` of it is not 3, calls `00314D40(1)` and returns 1; " + POLL, [("00346AB3", "call"), ("00346AB8", "cmp"), ("00346AC0", "call"), ("00346ADA", "call")]),
 ("0034D740", "when `0036E540(operand +0)` is non-zero, calls `00314D40(1)` and returns 1; " + POLL, [("0034D747", "call"), ("0034D755", "call"), ("0034D770", "call")]),
 ("0034EF60", "when `00267310(byte +0x15 of rdx)` is 0 it is waiting while `0036E5A0(operand +0)` is non-zero, otherwise it calls `0036DDC0(operand +0)` and is not waiting; while waiting it returns 1; " + POLL, [("0034EF6D", "call"), ("0034EF81", "setne"), ("0034EF86", "call"), ("0034EF9D", "call")]),
 ("0036DF80", "clamps `ecx` to 0..`0x1F` and, when word `+4` of the 24-byte entry at `022D94B0 + 24 * index` is non-zero, tail-calls `003B27A0(entry dword +0)`", [("0036DF8F", "cmovg"), ("0036DFA0", "cmp"), ("0036DFAB", "jmp")]),
 ("0036E500", "returns dword `+0` of the 24-byte entry at `022D94B0 + 24 * index`, index `ecx` clamped to 0..`0x1F`", [("0036E51F", "cmovg"), ("0036E530", "mov")]),
 ("0036E540", "for the clamped entry at `022D94B0 + 24 * index`: when its word `+4` is 1 and `0024DE70(dword +0)` returns 2 or 3, sets word `+4` to 2 and returns 0; when it returns anything else, returns 1; when word `+4` is not 1, returns 0", [("0036E566", "cmp"), ("0036E574", "call"), ("0036E586", "mov"), ("0036E592", "mov")]),
 ("0036E5A0", "returns the signed word at `022D94B4 + 24 * index` (word `+4` of the entry), index `ecx` clamped to 0..`0x1F`", [("0036E5C0", "cmovg"), ("0036E5D1", "movsx")]),
 ("0036E5E0", "when word `+4` of the clamped entry at `022D94B0 + 24 * index` is 3, tail-calls `0024FDA0(entry dword +0)`; else returns 0", [("0036E5EF", "cmovg"), ("0036E600", "cmp"), ("0036E60B", "jmp")]),
 ("0039C550", "calls `0039B550(02AEECB0)` and `00399600(rcx, &value)`; when that returns 0, passes the 16-byte value and `edx` to `0039D970` when dword `02AEE900` is non-zero and to `0039D890` otherwise", [("0039C575", "call"), ("0039C582", "call"), ("0039C58B", "cmp"), ("0039C5A5", "call")]),
 ("003A28C0", "stores the raw bits of its second (float) argument, sign-extended, at qword `022D8F30`, copies the 16 bytes from `022D8F30` to `022D92F0`, adds that float to every lane of the vector at `rcx` and writes the sum to `rcx` and `022D92E0`", [("003A28CE", "mov"), ("003A28DC", "movups"), ("003A28E7", "addps"), ("003A28F1", "movups")]),
 ("003A2B60", "converts `edx` to a float, stores it at `022D92F0`, multiplies every lane of the vector at `rcx` by it and writes the product to `022D92E0` and `rcx`", [("003A2B6A", "cvtdq2ps"), ("003A2B70", "movss"), ("003A2B7C", "mulps"), ("003A2B86", "movups")]),
 ("003AA470", "looks along the list at `*(02EBEF70)` (each step resolving the next record's handle through `0020E600`) for a record whose word `+0xC` and bytes `+0xE` / `+0xF` match the first dword of the argument, and on a match calls `00500A60(record, argument + 4)`; otherwise, for byte 2 of that dword minus `0x50` in 0..5, it allocates a kind-specific record through `0036A100` (one of `0x190`, `0x1D0`, `0xC0`, `0x48`, `0x1C` or `0x20` bytes), constructs it from the dword and initialises it from `argument + 4`, appends it to that list (handles through `0020E620`) and increments the list's word `+0x18`", [("003AA490", "cmp"), ("003AA4C2", "call"), ("003AA4F6", "jmp"), ("003AA4FD", "call"), ("003AA623", "inc")]),
 ("003B0AD0", "finds the 24-byte entry holding handle `ecx` among those from `02EBEC00` to `02EBEF60`; returns 0 when there is none or its object at `+8` is null; returns 1 unless the object's word `+0x378` has bit `0x100` and its byte `+0x370` is at most 6, in which case a jump table on that byte returns 1, 2, 3, 4 or 5", [("003B0AE3", "cmp"), ("003B0AFC", "mov"), ("003B0B0B", "test"), ("003B0B31", "jmp")]),
 ("003B0B70", "counts the leading 24-byte entries from `02EBEC00` whose dword `+0` is non-zero, up to the table end `02EBEF60`, and returns half that count (rounded toward zero)", [("003B0B80", "cmp"), ("003B0BA9", "add"), ("003B0BB6", "sar")]),
 ("003B0C30", "calls `003B02A0(rcx, 0, 0, edx, 5)`", [("003B0C37", "mov"), ("003B0C44", "call")]),
 ("003B0F30", "for a non-zero handle found among the first `0x24` entries at `02EBEC00` (the search stops at an empty entry), sets bit `0x800` of word `+0x36A` of the entry's object at `+8`", [("003B0F43", "cmp"), ("003B0F68", "mov"), ("003B0F76", "or")]),
 ("003B0FD0", "finds handle `ecx` among the entries from `02EBEC00` to `02EBEF60` (stopping at an empty one) and stores `edx` in that entry's dword `+4`", [("003B0FE8", "cmp"), ("003B0FF7", "mov")]),
 ("003B27A0", "for `edx` from 0 to 10: finds handle `ecx` among the 48-byte entries from `02EBE5E0` to `02EBEBE0` (stopping at an empty one); with an object at `+0x10` calls `0024ED80(object)` and, when that object's `+0x130` is non-null, `003339C0(it, edx as a byte)` and returns 1; else 0", [("003B27B4", "cmp"), ("003B27D6", "cmp"), ("003B27F9", "call"), ("003B2812", "call")]),
 ("003B4A50", "walks the list at `*(02B404C8)` through `+0x10`, skipping nodes whose byte `+0x2D` shares a bit with byte `02B404C1`; it stores `node + 0x20` in the output array `rdx` for each node that passes its kind test - byte `+0x22` 1: dword `+0x24` must equal `ecx` when byte `+0x23` is 2 and differ from it when byte `+0x23` is 4; byte `+0x22` 2: with byte `+0x23` 1, `0024E2F0(+0x24, ecx)` must be non-zero, with 2 `0024E6D0(+0x24, ecx)`, with 3 either, and any other value fails; other kinds always pass - and, once one is stored, stops at a node whose byte `+0x2C` is below the smallest seen so far; returns the count", [("003B4A94", "test"), ("003B4ADA", "call"), ("003B4B17", "cmp"), ("003B4B29", "mov")]),
 ("003C8A20", "when qword `02B47730` is null, creates a `0xD8`-byte object with procedure `003C8B70` through `00244F50` and stores it there", [("003C8A31", "lea"), ("003C8A3D", "call"), ("003C8A42", "mov")]),
 ("003CD590", "for the 64-byte entry `*(02B47790) + 64 * (low byte of ecx)` whose dword `+4` equals `ecx`: clears dword `+0x30` of every node on its chain at `+0x28` (linked through `+0x38`), clears byte `+0` and qwords `+0x28` / `+0x30`, and returns 1; else 0", [("003CD59E", "cmp"), ("003CD5B0", "mov"), ("003CD5BC", "mov")]),
 ("003CD650", "for the 80-byte node `*(02B47798) + 80 * (low byte of ecx)` whose dword `+0x30` equals `ecx`: clears it, decrements byte `+0` of its owner entry (`*(02B47790) + 64 * byte +4`) and unlinks the node from the owner's list (next `+0x38`, previous `+0x40`; owner head `+0x28`, tail `+0x30`); returns 1, else 0", [("003CD662", "cmp"), ("003CD685", "dec"), ("003CD694", "mov"), ("003CD6AB", "mov")]),
 ("003CD6C0", "returns the 64-byte entry `*(02B47790) + 64 * (low byte of ecx)` when its dword `+4` equals `ecx`, else 0", [("003CD6D0", "cmp"), ("003CD6D3", "cmove")]),
 ("003CD7C0", "when that 64-byte entry's dword `+4` equals `ecx`, sets bit 6 of its byte `+1` to bit 0 of `dl`", [("003CD7CF", "cmp"), ("003CD7D5", "and"), ("003CD7E0", "or")]),
 ("003D7E90", "returns -1 when `00181DD0()` is non-zero and dword `+0x80` is 0; otherwise, for the 30 dwords at `+8`, zeroes each non-zero one for which `002DEE80` returns 0 and returns how many it kept", [("003D7EAF", "cmp"), ("003D7EDE", "call"), ("003D7EE7", "mov"), ("003D7EEB", "inc")]),
 ("003E69E0", "when `003E55B0(rcx)` returns an object, calls `00504610(object, edx, r8d)`", [("003E69EF", "call"), ("003E6A01", "call")]),
 ("003EA430", "for the 64-byte entry `02B5D0B0 + 64 * ecx`: stores the qword at `+0x20 + 8 * 002DEBB0()` in `+0x30`; when byte `+4` is 3 and that table holds more than `edx` entries (its dword `+4`), calls `002DF610(table dword at +0x10 + 16 * edx, r8d)` when that dword is non-zero", [("003EA462", "mov"), ("003EA467", "mov"), ("003EA472", "cmp"), ("003EA491", "call")]),
 ("003EA540", "the same selection as `003EA430`, calling `002DF6A0` instead of `002DF610`", [("003EA572", "mov"), ("003EA582", "cmp"), ("003EA5A1", "call")]),
 ("00478070", "when `002ED570(rcx, signed dx)` returns an object, calls `00504C40(object)` and then `0051FCF0(rcx, signed dx)`", [("00478082", "call"), ("0047808F", "call"), ("00478099", "call")]),
 ("00504610", "for slot `edx` below `0x10`: with `r8d` = `0xFFFF` it releases the id at `+0x140 + 4 * slot` through `003CD590` and `003CD5D0`, sets it to -1 and resets to `0xFF` each of the 20 bytes at `+0x180` whose high nibble is the slot; otherwise it finds the byte `(slot << 4) OR (r8 AND 0xF)` among those 20, releases the id at `+0x194 + 4 * index` through `003CD650` and resets that byte to `0xFF`", [("00504641", "call"), ("0050467A", "mov"), ("005046A5", "cmp"), ("005046D4", "call")]),
 ("0050D5E0", "uses `00267E10(r9)` (or, when negative, the word at `rdx`) as the index into `002640C0()`'s records through `00358940`; when the record's byte `+3` top three bits are `0x60` and `002EA6A0(record)` is non-zero, passes `00409090(0036B130(002E9A00(record)))` with the string at `008F4438` to `0017D280`", [("0050D5F0", "call"), ("0050D608", "call"), ("0050D61C", "cmp"), ("0050D64E", "call")]),
 ("00521250", "for the 48-byte entry `*(02CA8450) + 48 * (low byte of cx)`: decrements word `+0x24`; when it reaches 0 or below, sets word `+0` and dword `+4` to `0xFFFF` and decrements dword `02CA8458`", [("00521265", "dec"), ("00521275", "mov"), ("00521278", "mov"), ("0052127B", "dec")]),
 ("005375B0", "calls `004FF2B0(this)`; when byte `+0x10` is non-zero, stores `0020E620(003AA280(0, 0x58, that byte))` in dword `+0x1C`; returns `this + 0x20`", [("005375B9", "call"), ("005375D1", "call"), ("005375DE", "mov"), ("005375E1", "lea")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*The functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`lu_interior.py`](../../_index/candidates/opus-lu-interior-1001/lu_interior.py): every "
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
