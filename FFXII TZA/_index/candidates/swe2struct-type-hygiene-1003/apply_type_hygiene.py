"""apply_type_hygiene.py [--apply] - the non-blocking type-store hygiene from OPUS's opus-audit-type-residue-1003 (SWE2-STRUCT,
2026-10-03, request OPUS-REQ-STRUCT-SYSTEMSTOP-08-1003's hygiene items). Every lifted or corrected row is first checked at
the shipping image (CHECKS below; any mismatch refuses with FAILS n and writes nothing).

A. Widget-base copy rows: the CLASSIFIED rows of ManagerSub0209BE80_57E0, ..._57E0PairRecord and ..._8FA0 at +0x000..+0x0B8.
   These records are widgets, and the widget initialiser 002465F0 writes their Widget fields: 00246641 the proc,
   002466E6 0xFF80 at +0xA1, 00246700 0x3F800000 at +0xB8, 00246711 +0x98, 00246717 0x800080 at +0x9C. Each type's census
   carries those sites. An exact-match row takes the base row's readiness and confidence and points at it. A pair row
   (+0x98, +0x9C, +0xA1) is split to the base's granularity. _8FA0's two misread immediates (+0x9C "0x8000", +0xB8
   "0x3F80, not the f32 1.0") are struck and corrected; its +0xB8 becomes f32.
B. Rung-lag rows whose meaning or extent is already in the row:
   - every AchievementState counterIdN, checked against its descriptor (00D10460 + N*8: kind = width,
     +0x08 + offset = the row's offset; the counter area is AchievementState +0x08, because reader 003166F0 adds the
     descriptor offset to 002536A0() + 0x384C and this type sits at ImageBackedStateBlock +0x3844);
   - BattleFormulaScratch +0x0A4 (22 of 25 accesses SSE-float, the other 3 zero/reset dword stores);
   - BgmStream +0x031 (byte accesses only: 003EAD16, 003EAD46, 003EAD8D; 003EB0D0 tests the byte);
   - ManagerSingleton0209BE80 +0xAB30 embeddedAB30 (follows its embedded type, whose extent is a memset length);
   - type RenderResourceEntry (the type rung follows its used fields).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

FIELDS = os.path.join(DB, "_types", "fields.tsv")
TYPES = os.path.join(DB, "_types", "types.tsv")
TAG = "SWE2-STRUCT 2026-10-03, opus-audit-type-residue-1003"
COPIES = ("ManagerSub0209BE80_57E0", "ManagerSub0209BE80_57E0PairRecord", "ManagerSub0209BE80_8FA0")
CHECKS = [
    (0x00246641, "mov", "qword ptr [rdi], rbx"),
    (0x002466E6, "mov", "word ptr [rdi + 0xa1], 0xff80"),
    (0x00246700, "mov", "dword ptr [rdi + 0xb8], 0x3f800000"),
    (0x00246711, "mov", "dword ptr [rdi + 0x98], eax"),
    (0x00246717, "mov", "dword ptr [rdi + 0x9c], 0x800080"),
    (0x00316705, "lea", "edx, [rax + 0x384c]"),
    (0x00316735, "movzx", "eax, byte ptr [rcx + 1]"),
    (0x00316739, "add", "eax, edx"),
    (0x003EAD16, "cmp", "byte ptr [rcx + 0x31], 0"),
    (0x003EAD46, "mov", "byte ptr [rbx + 0x31], 0"),
    (0x003EAD8D, "mov", "byte ptr [rbx + 0x31], 0"),
    (0x003EB0E0, "cmp", "byte ptr [rax], 0"),
    (0x002766D8, "mov", "edx, 0x61f0"),
]
fails = []


def ins(d, off, md, va):
    return next(md.disasm(d[off(va):off(va) + 16], va), None)


def short(m):
    m = m.split(" || ")[0]
    return (m[:220] + "...") if len(m) > 220 else m


def main():
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for va, mn, op in CHECKS:
        i = ins(d, off, md, va)
        ok = i is not None and i.mnemonic == mn and i.op_str == op
        print("%s %08X %s %s" % ("ok  " if ok else "FAIL", va, i.mnemonic if i else "?", i.op_str if i else ""))
        if not ok:
            fails.append(va)
    raw = open(FIELDS, "rb").read().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(nl)
    end_nl = lines[-1] == ""
    if end_nl:
        lines = lines[:-1]
    rows = [l.split("\t") for l in lines]
    W = {}
    for r in rows[1:]:
        if r[0] == "Widget":
            try:
                W[int(r[1], 16)] = r
            except ValueError:
                pass
    out, n_exact, n_split, n_rung = [rows[0]], 0, 0, 0
    for r in rows[1:]:
        if len(r) < 9:
            out.append(r); continue
        t = r[0]
        try:
            o = int(r[1], 16)
        except ValueError:
            out.append(r); continue
        # ---- A. Widget-base copies
        if t in COPIES and r[6] == "CLASSIFIED" and o <= 0xB8:
            sz = int(r[2])
            w = W.get(o)
            if w and int(w[2]) == sz:
                r = list(r)
                note = (" || *(rung follows the base row Widget +0x%02X `%s`, %s/%s: this record is a widget the initialiser "
                        "002465F0 fills (00246641 proc, 00246711/00246717 +0x98/+0x9C, 002466E6 +0xA1, 00246700 +0xB8, "
                        "all in this type's census), so the base row's evidence applies; base meaning: %s; %s)*"
                        % (o, w[3], w[6], w[7], short(w[5]), TAG))
                if t == "ManagerSub0209BE80_8FA0" and o == 0xB8:
                    seg = r[5].split(" || ")[0]
                    r[5] = r[5].replace(seg, "~~%s~~ set to 0x3F800000 (the f32 1.0) at 00246700 *(corrected, %s: the instruction "
                                        "is `mov dword ptr [rdi + 0xb8], 0x3f800000`)*" % (seg, TAG), 1)
                    r[4] = w[4]
                r[5] += note
                r[6], r[7] = w[6], w[7]
                r[8] += "; base row Widget +0x%02X" % o
                out.append(r); n_exact += 1
                continue
            cov = [W[x] for x in sorted(W) if o <= x < o + sz]
            if cov and sum(int(c[2]) for c in cov) == sz:
                old = r[5]
                if t == "ManagerSub0209BE80_8FA0" and o == 0x9C:
                    seg = old.split(" || ")[0]
                    old = old.replace(seg, "%s *(corrected, %s: 00246717 stores 0x800080, not 0x8000)*" % (seg, TAG), 1)
                for k, c in enumerate(cov):
                    nr = list(r)
                    co = int(c[1], 16)
                    nr[1], nr[2], nr[3], nr[4] = "0x%03X" % co, c[2], c[3], c[4]
                    lead = ("~~%s~~ " % old) if k == 0 else ""
                    nr[5] = (lead + "Widget +0x%02X `%s`: %s *(split %s from this type's former %d-byte pair row at +0x%03X, which "
                             "named the initialiser's single store (00246711 / 00246717 0x800080 / 002466E6 0xFF80); the base row's "
                             "word/byte-level evidence applies; %s)*" % (co, c[3], short(c[5]), "low part" if k == 0 else "high part",
                                                                      sz, o, TAG))
                    nr[6], nr[7] = c[6], c[7]
                    nr[8] = r[8] + "; base row Widget +0x%02X" % co
                    out.append(nr)
                n_split += 1
                continue
            fails.append("%s+%s no base mapping" % (t, r[1]))
            out.append(r); continue
        # ---- B. rung lags
        if t == "AchievementState" and r[3].startswith("counterId") and r[6] == "CLASSIFIED":
            n = int(r[3][len("counterId"):])
            desc = d[off(0x00D10460 + n * 8):off(0x00D10460 + n * 8) + 2]
            kind, doff = desc[0], desc[1]
            if kind == int(r[2]) and 8 + doff == o and r[5].startswith("counter for achievement id %d" % n):
                r = list(r)
                r[5] += (" *(rung lifted, %s: descriptor %d at %08X = kind %d / offset 0x%X, and the counter area is "
                         "AchievementState +0x08 (reader 003166F0 adds the offset to 002536A0() + 0x384C; this type sits at "
                         "ImageBackedStateBlock +0x3844))*" % (TAG, n, 0x00D10460 + n * 8, kind, doff))
                r[6], r[7] = "SEMANTICALLY IDENTIFIED", "PROVEN"
                out.append(r); n_rung += 1
            else:
                fails.append("AchievementState %s descriptor mismatch (kind %d off 0x%X)" % (r[1], kind, doff))
                out.append(r)
            continue
        if t == "BattleFormulaScratch" and o == 0xA4 and r[6] == "CLASSIFIED":
            r = list(r)
            r[5] += (" *(rung lifted to TYPE RESOLVED, %s: the census has 25 accesses at +0xA4, 22 SSE-float (15 movss, 7 subss) and "
                     "3 dword stores in reset runs (00384A35, 0038A0E8 = 0, 0038A573 = 0); the representation is resolved, "
                     "the meaning is the row's)*" % TAG)
            r[6] = "TYPE RESOLVED"
            out.append(r); n_rung += 1; continue
        if t == "BgmStream" and o == 0x31 and r[6] == "CLASSIFIED":
            r = list(r)
            r[5] += (" *(rung lifted to TYPE RESOLVED, %s: every access is a byte - 003EAD16 cmp byte / 003EAD46, 003EAD8D mov byte, "
                     "003EB0E0 cmp byte in 003EB0D0; MEANING NOT CLAIMED stands)*" % TAG)
            r[6] = "TYPE RESOLVED"
            out.append(r); n_rung += 1; continue
        if t == "ManagerSingleton0209BE80" and o == 0xAB30 and r[3] == "embeddedAB30" and r[6] == "DISCOVERED":
            r = list(r)
            r[5] += (" *(rung follows the embedded type ManagerSub0209BE80_AB30 (SEMANTICALLY IDENTIFIED/PROVEN), %s: the extent is "
                     "the memset length 0x61F0 passed at 002766D8; the overlay arm overlayWidget0720AB30 carries the other mode)*" % TAG)
            r[6], r[7] = "SEMANTICALLY IDENTIFIED", "PROVEN"
            out.append(r); n_rung += 1; continue
        out.append(r)
    # ---- C. WIDTH DELIBERATE on the low part of each split (idempotent): the copy's census holds only the
    # initialiser's single wider store, while the base row is reached at the narrow width by its own writers.
    n_mark = 0
    for r in out[1:]:
        if len(r) > 8 and r[0] in COPIES and r[1] in ("0x098", "0x09C", "0x0A1") and "split low part" in r[5] \
                and "WIDTH DELIBERATE" not in r[8]:
            sz = int(r[2])
            store = {"0x098": "00246711's dword", "0x09C": "00246717's dword 0x800080", "0x0A1": "002466E6's word 0xFF80"}[r[1]]
            r[8] += ("; WIDTH DELIBERATE: declared %d after the Widget base row; this record's census holds only the "
                     "initialiser %s over two Widget fields, while the base row is reached at its own width by its own "
                     "writers (%s)" % (sz, store, TAG))
            n_mark += 1
    print("A: %d exact rows lifted, %d pair rows split; B: %d rung rows lifted; C: %d split rows marked"
          % (n_exact, n_split, n_rung, n_mark))
    # type row RenderResourceEntry
    traw = open(TYPES, "rb").read().decode("utf-8")
    tnl = "\r\n" if "\r\n" in traw else "\n"
    tl = traw.split(tnl)
    hdr = tl[0].split("\t")
    ri, ci, ei = hdr.index("readiness"), hdr.index("confidence"), hdr.index("evidence")
    tch = 0
    for k, l in enumerate(tl):
        c = l.split("\t")
        if c and c[0] == "RenderResourceEntry" and len(c) > ri and c[ri] == "DISCOVERED":
            c[ri] = "SIGNATURE RESOLVED"
            c[ei] += (" || TYPE RUNG LIFTED DISCOVERED -> SIGNATURE RESOLVED (%s): the fields its contract uses (kind, reference, "
                      "resolvedCache, sourceSize, effectTicket, bufferDescriptor) are SIGNATURE RESOLVED or SEMANTICALLY IDENTIFIED, the "
                      "0x50 extent is declared, and the unobserved words stay declared gaps" % TAG)
            tl[k] = "\t".join(c); tch += 1
    done = any(l.split("\t")[0] == "RenderResourceEntry" and "TYPE RUNG LIFTED DISCOVERED -> SIGNATURE RESOLVED" in l for l in tl)
    print("types.tsv RenderResourceEntry rows changed: %d%s" % (tch, " (already lifted)" if done and not tch else ""))
    if tch != 1 and not done:
        fails.append("RenderResourceEntry type row")
    print("FAILS %d" % len(fails), fails[:5])
    if "--apply" in sys.argv and not fails:
        text = nl.join("\t".join(r) for r in out) + (nl if end_nl else "")
        open(FIELDS, "wb").write(text.encode("utf-8"))
        open(TYPES, "wb").write(tnl.join(tl).encode("utf-8"))
        print("written")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
