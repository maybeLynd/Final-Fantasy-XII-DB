"""pfgate_interior.py - interior citations for the 41 F-frontier functions that CONTRACT-per-frame-update-gate.md cited by
entry only (OPUS, 2026-10-01). Every body was read by hand from the certified image (anchor_prep.py / retool.py).

Before writing, the script VERIFIES every anchor against the image: it must be an instruction boundary strictly inside its
function's extent (functions.tsv) and decode to the recorded mnemonic. Any mismatch -> FAILS, nothing written.
Then it appends one OPUS section to the page (byte-preserving, idempotent). Prints VERIFY lines, PATCHED / ALREADY, FAILS n."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "00-Engine-Core-Runtime", "CONTRACT-per-frame-update-gate.md")
ROWS = [
 ("0017F000", "gets the object `001BC000` returns; when it is non-null, calls `001BB2B0(object, id, &out)` and returns `out`; otherwise returns 0", [("0017F021", "call"), ("0017F026", "mov")]),
 ("00271530", "fills a ten-qword header at `rcx`: `+0` = (signed `edx` << 15) OR `0x1000000000000004`, then the constants `0xE`, `0x53001`, `0x47`, `0x44`, `0x42`, 1, `0x1A`, `0x54` (`0x5C` when `r8d` is 0) and 0; returns `rcx + 0x50`", [("00271551", "mov"), ("0027156C", "cmove"), ("00271593", "lea")]),
 ("002716C0", "writes four dwords at `rcx`: 0, `0x13000000`, `0x10000000` and `0x50000000` OR ((`edx` - `rcx` - 0x10) >> 4), the 16-byte count of the span after the header", [("002716CB", "mov"), ("002716D5", "or"), ("002716E2", "mov")]),
 ("00272710", "adds word `+0x16` to word `+0x14`; at or above `0x400` it clamps to `0x400` and returns 1, else returns 0", [("00272714", "add"), ("00272726", "mov"), ("0027272A", "mov")]),
 ("00272F30", "resolves `003588B0`; with no record it returns the float at `01CEBBA8`, else `002645D0(record)` scaled by the float at `00901B34`", [("00272F3E", "movss"), ("00272F4E", "call"), ("00272F53", "mulss")]),
 ("002760A0", "walks the list at `rdx` through `+0x18` for a block with room for `r8d + 0x20` bytes after its used span; carves a node there (`[node] = node + 0x20`, `+8` = size), links it after the block and stores it at `rcx+0x10`; returns the node, or 0 when none fits", [("002760B9", "cmp"), ("002760E9", "mov"), ("0027610D", "mov"), ("00276115", "xor")]),
 ("00276120", "when the head `[rcx]` lies above `[rcx+0x20]` and the gap holds `edx + 0x20` bytes, carves a node at `[rcx+0x20]` and makes it the new head (`[rcx]` and `+0x10`); returns it, else 0", [("0027615D", "mov"), ("00276183", "mov"), ("0027618B", "xor")]),
 ("002767C0", "asks `002753F0(this, {0x2C, ...})` for key `0x2C`; returns the answer, or the signed word `+0x61B8` when the answer is 0", [("002767FD", "call"), ("0027680A", "movsx")]),
 ("00289970", "runs `0028A550`, then `0028A350`, then tail-calls `0028A620`, all on the same object", [("00289981", "call"), ("0028998E", "jmp")]),
 ("0028C850", "counts the nodes of the chain linked through `+0xD70`", [("0028C860", "mov"), ("0028C867", "inc")]),
 ("0028C970", "calls `0028D260(this, this, a2, a3, -1)`, then `0028D8A0` for the two 0x20-byte entries at `+0x30` and `+0x50`", [("0028C99E", "call"), ("0028C9C7", "call"), ("0028C9CE", "cmp")]),
 ("0028CA30", "tail-calls `00861EC0(rcx, 0, 0x80)`", [("0028CA32", "mov"), ("0028CA38", "jmp")]),
 ("0028E1D0", "with the singleton `*(0209BE80)` present and its `+0x10F68` bit `0x40` clear, calls `002BDB60` on its `+0x8FA0` part, then tail-calls `002BDCA0(part, 1)`", [("0028E1E0", "test"), ("0028E1F0", "call"), ("0028E211", "jmp")]),
 ("00290B10", "on the singleton `*(0209BE80)`: calls `0028C4F0` on `+0x10F00` when set; when the record at `+0x10EF0` has word `+0xD54` = 3, sets its `+0xD4C` bit 3; then clears `+0x10EF0`", [("00290B30", "call"), ("00290B4B", "or"), ("00290B59", "mov")]),
 ("002964D0", "runs `002962D0` and `0035BC40`; when `0035BB60()` is non-zero, makes a `0xB68`-byte object through `00244F50`, sets its `+0x40` bit `0x8000` when `002544B0()` is 1, starts it with `00246AC0` and returns it; else 0", [("002964E3", "test"), ("00296502", "call"), ("00296519", "or"), ("00296523", "call")]),
 ("00296940", "tail-calls `00245000(rcx, 0x720, 002985D0, 0)`", [("00296943", "lea"), ("0029694F", "jmp")]),
 ("002BDCA0", "when `+0x1080` and `+0x1058` are set, writes bit 0 of word `+0x40B6` of the `+0x1058` object as the inverse of `dx` bit 0", [("002BDCBE", "and"), ("002BDCC9", "or")]),
 ("002BE090", "sets `+0x10FA` bit 1 and stores `dx` in word `+0x10F8`", [("002BE098", "mov")]),
 ("002BE230", "with a child at `+0x1030`: sets its `+0x280` bit `0x20` and its word `+0x294` = `dx`; without one: sets `+0x103E` bit 1 and word `+0x103C` = `dx`", [("002BE24B", "mov"), ("002BE253", "or"), ("002BE25B", "mov")]),
 ("002BE270", "stores `edx` in the `+0x1030` child's `+0x298`, or in `+0x1040` when there is no child", [("002BE27C", "mov"), ("002BE283", "mov")]),
 ("0031C200", "when byte `02089340` bit `0x10` is set, resolves `003588B0` -> `00263E30` -> `+0x698` and returns that record's byte `+4` (unless `0xFF`); otherwise -1", [("0031C224", "mov"), ("0031C230", "movzx"), ("0031C241", "or")]),
 ("00377750", "returns 1 when `00314AE0()` is 1, 0 when it is 2, otherwise calls `003148F0` and returns 1", [("0037775C", "je"), ("00377763", "call"), ("00377772", "xor")]),
 ("0037B2F0", "when byte `02ADD932` is not 4, copies it to `02ADD930`, calls `0037B3D0`, and copies it to `02ADD931`", [("0037B307", "mov"), ("0037B30D", "call"), ("0037B312", "mov")]),
 ("003C5400", "stores `edx` in the dword table at `02B45970`, index `ecx`", [("003C5403", "lea"), ("003C540A", "mov")]),
 ("003C8070", "on the object `*(02B476B0)`: clears `+0x40` bit `0x10000`, sets it again (and clears dword `02B476E4`) when `002544B0()` is 1 or `02B476E4` is non-zero, then tail-calls `00244F00(object)`", [("003C8082", "and"), ("003C809C", "or"), ("003C80B5", "jmp")]),
 ("003F24A0", "calls `003F1E90` on every node of the chain linked through `+0x9B0`", [("003F24B3", "call"), ("003F24B8", "mov")]),
 ("003F6100", "calls `003F5CB0` on every node of the chain linked through `+0x868`", [("003F6113", "call"), ("003F6118", "mov")]),
 ("003F80D0", "tail-jumps to `003F7E80` when `+0x984` bit 0 is set, else returns", [("003F80D7", "jne"), ("003F80DD", "ret")]),
 ("003F8EA0", "clears qword `+0x52A0`, then tail-calls `00861EC0(rcx + 0x4020, 0, 0x1280)`", [("003F8EAD", "add"), ("003F8EB4", "mov"), ("003F8EBA", "jmp")]),
 ("002E6E30", "for slot `edx`: when the handle at `+0x60 + 4*slot` is non-zero, resolves it against `[022C6F28]+0x48830` (`0020E600`), unregisters it through `0041E490`, frees it through `00369800`, zeroes the slot and clears bit `slot` in `+0x24` and `+0x2C`", [("002E6E6F", "call"), ("002E6E77", "call"), ("002E6E83", "mov"), ("002E6E93", "and")]),
 ("002EA6E0", "when `+0x18` bit `0x04` is clear and `002ED950(+0x14)` finds an entry, takes a command record from `002F16B0`, copies `edx` dwords from `r8` into `+0x30`, and fills the record (`+4` = `0x30009`, `+0x10` = `002E60F0`, `+0x28` = this); returns 1, else 0", [("002EA6EF", "test"), ("002EA70B", "call"), ("002EA722", "mov"), ("002EA73D", "mov"), ("002EA744", "mov")]),
 ("0036F460", "stores its float argument at `02AD9B50` (taking the difference from the previous value), steps the stored value down by a constant while it is at or above a limit, scales the difference by constants and hands it to `004678E0`, then tail-calls `00468520`", [("0036F472", "subss"), ("0036F490", "addss"), ("0036F4B9", "divss"), ("0036F4C0", "call")]),
 ("003F00F0", "fills a transform block: the two imported math functions `00861F08` / `00861F0E` of 0.0 go to `+0x60` / `+0x6C` and `+0x64` / negated `+0x68`, `+0xC` = 1.0, `+0x80` and `+0xF0` = 0, `+0xEC` = -1, and two 16-byte constants to `+0x70` and `+0x10`", [("003F0101", "call"), ("003F012E", "movss"), ("003F0133", "mov"), ("003F0152", "mov")]),
 ("003F80E0", "zeroes the four dwords at `+0x960`, then copies row `edx` of the 16-byte table at `00D11D80` into them; row 1 is skipped while dword `02092730` is 4", [("003F8103", "mov"), ("003F8115", "cmp"), ("003F8121", "mov")]),
 ("003FA6E0", "when argument 2 has `+0x272` bit 0 and is on this object's `+0x2490` chain (linked through `+0x278`), calls `00202C90(argument 3)` and returns 1; else 0", [("003FA700", "cmp"), ("003FA705", "mov"), ("003FA71B", "call")]),
 ("003FA730", "the same membership test as `003FA6E0`; returns argument 2's dword `+0x260`, else 0", [("003FA745", "cmp"), ("003FA759", "mov")]),
 ("00356160", "takes two floats from `00267DB0` and an id from `00267E10` (all on argument 4), builds a direction through `00203170`, `00202F00`, `00202E90` and `00202B70` with w = 1.0, passes it through `003A1890` and hands it with the id to `003DEA70`", [("0035619E", "call"), ("003561CD", "call"), ("003561FD", "mov"), ("00356211", "call")]),
 ("003F7760", "forms the vector from `+0x280` to `+0x290` (`00203080`), zeroes its w, passes it through `00202DE0` and `00270A10`, and updates `+0x2A0` from it with a constant through `00270CF0`", [("003F778B", "call"), ("003F779D", "movss"), ("003F77CE", "call")]),
 ("003F7CC0", "runs `003F2F20` on this and `+0xF0`; writes the `0x13000000` / `0x10000000` code words at `+0xE0`..`+0xEC` and `+0x1D0`..`+0x1DC`; copies `+0xB0`..`+0xBC` to `+0x2C0`..`+0x2CC`; sets the floats 0.21 at `+0x1A4`, 0.2 at `+0x1AC` and 127.0 at `+0x1B0`, `+0x1B4` and `+0x1B8` (a qword store, so `+0x1BC` = 0); derives `+0x2B0`..`+0x2BC` from the four floats at argument 2; then builds its records with `00271650` / `002716C0` (`+0x1E0`), `003F77F0`, and `00271530` (`+0x230`) / `002716C0` (`+0x220`)", [("003F7CE7", "call"), ("003F7CEC", "mov"), ("003F7D46", "mov"), ("003F7D8E", "mov"), ("003F7E36", "call"), ("003F7E51", "call"), ("003F7E6F", "jmp")]),
 ("003FAAF0", "when `00273A20(this)` is non-zero, stores `edx` in dwords `+0x28`..`+0x34` of parts 0, 1 and 2 (`[this+0x60][k]`)", [("003FAB0B", "call"), ("003FAB31", "mov"), ("003FAB37", "mov"), ("003FAB43", "mov")]),
 ("00505500", "in mode `+0x3C` = 2: counts `+0x44` down first (returning 0), then raises word `+0x38` by 6 until `0x80` and by word `+0x3A` after that, returning 1 once it passes `0x100`; in other modes adds `+0x3A` and returns 1 once it passes `0x25`", [("0050550D", "dec"), ("00505523", "add"), ("0050553D", "cmp"), ("0050554D", "add")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Forty-one functions this contract named only at their entry. Each was read from the certified image; the sentence "
        "states what the body does (access and representation, not purpose), and the anchors are instructions inside it that "
        "do it. Verified by [`pfgate_interior.py`](../_index/candidates/opus-pfgate-interior-1001/pfgate_interior.py): every "
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
