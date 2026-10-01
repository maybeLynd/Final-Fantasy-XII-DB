"""SWE2-AUDIT-SEM BIT46 counterexample hunt, part 2 (own code): every write the published battle-unit census
(04-Actor-Entity/Battle-Unit/battle-unit-accesses.tsv) records on the flag qword (displacement 0x0-0x7, kind with 'w').
Q  immediate forms: the effect on bit 46 of each immediate after x86 sign extension (a qword and/or with an imm32 is
   sign-extended; a dword at +4 covers bits 32-63; a byte at +5 covers bits 40-47).
R  register forms (whole-qword mov, and/or/xor with a register): the 14 instructions before the site are printed, and
   the source register's last writer is shown, to read what value reaches the store.
The producer excluded two whole-qword writers (00300EAA, 00300198); this lists every one the census holds."""
import csv, re, os
import img

HERE = os.path.dirname(os.path.abspath(__file__))
TSV = next(p for p in (
    os.path.join(HERE, "..", "..", "..", "04-Actor-Entity", "Battle-Unit", "battle-unit-accesses.tsv"),  # review dir
    os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA", "04-Actor-Entity", "Battle-Unit",
                 "battle-unit-accesses.tsv"),  # Tools/work
) if os.path.exists(p))
rows = []
with open(TSV, encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        if r["disp"] in ("0x0", "0x4", "0x5", "0x6", "0x7") and "w" in r["kind"]:
            rows.append(r)
seen = set()
uniq = []
for r in rows:
    if r["site"] in seen:
        continue
    seen.add(r["site"])
    uniq.append(r)
uniq.sort(key=lambda r: int(r["site"], 16))
print("census write rows on the flag qword (unique sites):", len(uniq))

def ctx(a, n):
    for back in range(n * 7, 0, -1):
        xs = list(img.md.disasm(img.rd(a - back, back + 16), a - back))
        if any(x.address == a for x in xs):
            i = [k for k, x in enumerate(xs) if x.address == a][0]
            return xs[max(0, i - n):i + 1]
    return []

def bit46_effect(mn, size_kw, disp, imm):
    # returns 'sets', 'clears', 'keeps', 'n/a'
    if size_kw == "qword":
        v = imm & 0xFFFFFFFF
        if v & 0x80000000:
            v |= 0xFFFFFFFF00000000
        b = (v >> 46) & 1
    elif size_kw == "dword" and disp == 4:
        b = (imm >> 14) & 1
    elif size_kw == "byte" and disp == 5:
        b = (imm >> 6) & 1
    elif size_kw == "word" and disp == 4:
        b = (imm >> 14) & 1
    else:
        return "n/a (does not cover bit 46)"
    if mn == "or":
        return "SETS" if b else "keeps"
    if mn == "and":
        return "keeps" if b else "CLEARS"
    if mn == "xor":
        return "FLIPS" if b else "keeps"
    if mn == "mov":
        return "STORES %d" % b
    if mn in ("bts", "btr", "btc"):
        return "n/a"
    return "?"

imm_re = re.compile(r"^(\w+) (byte|word|dword|qword) ptr \[[^\]]+\], (-?0x[0-9a-f]+|-?\d+)$")
for r in uniq:
    ins = r["instruction"]
    m = imm_re.match(ins)
    disp = int(r["disp"], 16)
    if m:
        mn, kw, imm = m.group(1), m.group(2), int(m.group(3), 0)
        if mn in ("bts", "btr", "btc"):
            eff = "SETS/CLEARS" if imm == 46 - 8 * disp else "n/a (bit %d)" % (imm + 8 * disp)
        else:
            eff = bit46_effect(mn, kw, disp, imm)
        print("Q %s %s %-44s -> %s" % (r["function"], r["site"], ins, eff))
for r in uniq:
    ins = r["instruction"]
    if imm_re.match(ins):
        continue
    a = int(r["site"], 16)
    src = ins.split(",")[-1].strip()
    print("R %s %s %s   (%s)" % (r["function"], r["site"], ins, r["name"]))
    xs = ctx(a, 14)
    for x in xs:
        mark = "  <" if x.op_str.split(",")[0].strip() in (src, src.replace("r", "e", 1) if src.startswith("r") and src[1:].isalpha() else src) else ""
        print("     %08X %s %s%s" % (x.address, x.mnemonic, x.op_str, mark))
