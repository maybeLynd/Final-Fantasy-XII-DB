"""gr6_row24_check.py - GR-6: what the 436 action-row +0x24 words with bit 15 clear select (OPUS, 2026-09-30).
Static reads of the certified image (kit retool.py, regval.py, structflow.py) plus the shipped action rows (the UQ-80
record's pack.py, battle_pack directory 0x3C, 543 x 60 B).

G1  every reader of row +0x24 (structflow from every 02EBF138 row-pointer formation, depth 3): nine functions, fourteen
    sites - 00309230, 0030A190, 0030AC50, 0030CA80, 00310DB0, 0031ADB0 (3), 00325260 (3), 003257D0 (3).
G2  the four readers that let a bit-15-clear word through use it as an EFFECT id:
    0030A190  returns it (not 0xFFFF, +0x0C bit 30 clear, bit 15 clear) -> 0030CBE0 effect request / 0030C890 budget;
    0030CA80  same three tests, then 002FCB40(word) = bit 5 of the 8-byte effect-table entry at 02EC19C4 + word*8;
    00310DB0  word with bit 15 cleared (btr) -> 002EACD0(.., 1, .., word) -> 003B02A0(.., kind 5): effect instantiation;
    00309230  returns the row's word to 00306BD0, which passes it to WorldSimulation_ProcessDeferredModeRequest(3, word).
G3  the other readers route a bit-15-clear word nowhere: 0030AC50 takes only bit 15 set; 0031ADB0 sends bit 15 set to
    the +0x34 reaction path (0031B254 jl) and skips the rest (0031B2AC); 00325260 / 003257D0 test 0xFFFF (di = 0xFFFF)
    and return on any other word (00325702 / 003259E3 are the exits the row left unread).
G4  the shipped rows: 0xFFFF on 68 (43 + 25), bit 15 set on 39, bit 15 clear on 436 = 374 with +0x0C bit 30 clear
    (340 distinct words, 0..396: the effect ids 0030A190 / 0030CA80 serve) + 62 with bit 30 set (rows 148..274, the
    summon-class rows 0030A190 refuses; their word is what 00306BD0 loads).
Prints PASS/FAIL per check and FAILS n last.
"""
import collections, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "uq80-table-field-coverage")))
import retool as T  # noqa: E402
import regval as V  # noqa: E402
import structflow as S  # noqa: E402
import pack  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


# G1
g = S.Flow([0x24, 0x25], 3)
g.run(S.slot_functions())
sites = sorted((h[0], h[1]) for h in g.hits)
fns = sorted({f for f, _ in sites})
check("G1", fns == [0x00309230, 0x0030A190, 0x0030AC50, 0x0030CA80, 0x00310DB0, 0x0031ADB0, 0x00325260, 0x003257D0]
      and len(sites) == 14 and all(h[2] == "r" for h in g.hits),
      "%d functions walked; +0x24 readers %s (%d sites)" % (len(g.entry), ["%08X" % f for f in fns], len(sites)))
# G2
ok_a = txt(0x0030A213) == "movzx eax, word ptr [rbx + 0x24]"
ok_b = txt(0x0030CB77) == "movzx eax, word ptr [rcx + 0x24]" and txt(0x0030CB85) == "test dword ptr [rcx + 0xc], 0x40000000" \
    and txt(0x0030CB8E) == "test ax, ax" and txt(0x0030CB91) == "js 0x30cb9f" and txt(0x0030CB96) == "call 0x2fcb40" \
    and txt(0x002FCB4A) == "movzx eax, byte ptr [rcx + rax*8]" and txt(0x002FCB4E) == "shr eax, 5" \
    and 0x002FCB4A + 0x2BC4E7A == 0x02EC19C4
ok_c = txt(0x0031105A) == "movzx r9d, word ptr [rcx + 0x24]" and txt(0x0031105F) == "btr r9d, 0xf" \
    and txt(0x0031106B) == "call 0x2eacd0" and txt(0x002EACE5) == "mov dword ptr [rsp + 0x20], 5" and txt(0x002EACF0) == "call 0x3b02a0"
ok_d = txt(0x003092C5) == "movzx eax, word ptr [rbx + 0x24]" and txt(0x00306C4D) == "call 0x309230" \
    and txt(0x00306C52) == "mov edx, eax" and txt(0x00306C56) == "call 0x32fc30" \
    and V.value_at(0x00306BD0, 0x00306C56, "rcx", 1) == {("C", 3)}
check("G2", ok_a and ok_b and ok_c and ok_d,
      "effect id at 0030A190 (%s), 0030CA80 -> 002FCB40 effect-table bit 5 (%s), 00310DB0 -> 002EACD0 -> 003B02A0 kind 5 (%s); "
      "00309230 -> 00306BD0 -> deferred mode request 3 (%s)" % (ok_a, ok_b, ok_c, ok_d))
# G3
ok = txt(0x0030AD10) == "movzx eax, word ptr [rdi + 0x24]" \
    and txt(0x0031B254) == "cmp word ptr [rax + 0x24], bp" and txt(0x0031B258) == "jl 0x31b300" \
    and V.value_at(0x0031ADB0, 0x0031B254, "rbp", 1) == {("C", 0)} \
    and txt(0x0031B2A7) == "cmp word ptr [rax + 0x24], r15w" and txt(0x0031B2AC) == "jne 0x31b3a9" \
    and txt(0x00325476) == "cmp word ptr [rcx + 0x24], di" and txt(0x0032547A) == "jne 0x325702" \
    and txt(0x00325702) == "mov eax, 1" and txt(0x00325711) == "ret" \
    and txt(0x00325968) == "cmp word ptr [rcx + 0x24], di" and txt(0x0032596C) == "jne 0x3259e3" and txt(0x003259F7) == "ret" \
    and V.value_at(0x00325260, 0x00325476, "rdi", 0) == {("C", 0xFFFF)} and V.value_at(0x003257D0, 0x00325968, "rdi", 0) == {("C", 0xFFFF)}
check("G3", ok, "0030AC50 bit-15 path only; 0031ADB0 bit 15 set -> 0031B300, else skip; 00325260 / 003257D0 return on any non-0xFFFF word")
# G4
recs, _h = pack.records(0x3C)
cls = collections.Counter()
words = collections.defaultdict(set)
rows = collections.defaultdict(list)
for i, r in enumerate(recs):
    w = struct.unpack_from("<H", r, 0x24)[0]
    b30 = (struct.unpack_from("<I", r, 0x0C)[0] >> 30) & 1
    k = "FFFF" if w == 0xFFFF else ("b15" if w & 0x8000 else "clear")
    cls[(k, b30)] += 1
    words[(k, b30)].add(w)
    rows[(k, b30)].append(i)
ok = len(recs) == 543 and cls[("FFFF", 0)] + cls[("FFFF", 1)] == 68 and cls[("b15", 0)] + cls[("b15", 1)] == 39 \
    and cls[("clear", 0)] == 374 and cls[("clear", 1)] == 62 and len(words[("clear", 0)]) == 340 \
    and max(words[("clear", 0)]) == 396 and rows[("clear", 1)][0] == 148 and rows[("clear", 1)][-1] == 274
check("G4", ok, "rows by (+0x24 class, +0x0C bit 30): %s; bit-15-clear distinct words: %d (bit 30 clear, max %d), %d (bit 30 set)"
      % (dict(sorted(cls.items())), len(words[("clear", 0)]), max(words[("clear", 0)]), len(words[("clear", 1)])))
print("FAILS %d" % fails)
