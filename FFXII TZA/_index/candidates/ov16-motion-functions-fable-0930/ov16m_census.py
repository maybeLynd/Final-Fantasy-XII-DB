"""ov16m_census.py - OV-16 motion route, script half (research helper for FABLE, 2026-09-30). Read-only.

Question: does any function that 00268EA0 files (footer slot 16 = entry +0x22, footer slot 17 = entry +0x24, or the
override words +0xE8 / +0xEA that REQCHG slot 16 / 17 writes) contain a waited request?

Population: every distinct shipped .ebp under D:/FFXII_TZA_extract (md5-deduplicated), decoded with the rules of
fable-astra-live-facts-0930/ov16_opcode_histogram.py and FABLE's decoder gen_req_channel_census.decode (section at 0x80
tag 0x8000000B; directory at +0x18, stride 0x30; 1-byte ops below 0x48, 3-byte ops at or above).
Per actor (directory entry; section-000-bytecode.md section 4, BW-5):
  +0x08 scriptStartOff, +0x10 nameOff -> {u32 n; {u32 nameOffInPool, u32 offsetWithinScript}[n]},
  +0x18 sepaOff -> tFuncFooter {u16 count; u16 special[18]}  (special[k] at +2+2k; k 16 = +0x22, k 17 = +0x24).
A function's body is [offset_i, next larger offset in the same actor) and the last one runs to the actor's end (the
next actor start, the directory, or the section end: the histogram's own bound).
Waited opcodes: primary REQSW 0x24 / REQEW 0x27 (and FREQSW 0x25, TREQSW 0x26, FREQEW 0x28, TREQEW 0x29); secondary
REQWAIT 0x32, REQALL 0x5F, REQWAITALL 0x61, REQIALL 0x63 (they park on another entry but file no keyed notification of
their own - listed so a zero on the primary set is not mistaken for "never parks").
REQCHG 0x34 pops (value, actor, slot) (bf1-opcode-semantics row 0x34, handler 002615BA -> 0025AF60): pushed order is
slot, actor, value. Sites with slot 16 / 17 are resolved with gen_req_channel_census.resolve_args(need=3).

Controls (the run exits 1 if any fails):
  C1 partition: summed over functions, the counts of REQSW / REQEW / RETN / RETTN / REQCHG equal a whole-actor decode
     of the same files, and those equal the histogram's 27,898 / 115,766 / 135,429 / 6,039 / 26,604.
  C2 positive: REQSW + REQEW are found in non-slot-16/17 functions (the census can see a waited request).
  C3 the slot-16/17 footer words resolve to functions named talkhold* / talkterm* (rc12 Part B's names).
  C4 every REQCHG slot-16/17 value resolves to a function of the target actor.
"""
import collections, hashlib, io, os, struct, sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G  # noqa: E402

EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
PRIMARY = {0x24: "REQSW", 0x25: "FREQSW", 0x26: "TREQSW", 0x27: "REQEW", 0x28: "FREQEW", 0x29: "TREQEW"}
SECONDARY = {0x32: "REQWAIT", 0x5F: "REQALL", 0x61: "REQWAITALL", 0x63: "REQIALL"}
CTRL_OPS = {0x24: 27898, 0x27: 115766, 0x2E: 135429, 0x30: 6039, 0x34: 26604}
verbs = G.load_verbs()


def cstr(b, o):
    return b[o:b.find(b"\0", o)].decode("cp932", "replace")


tot_fn = collections.Counter()      # opcode totals over the function partition
tot_actor = collections.Counter()   # opcode totals over whole-actor decodes (histogram rule)
files = actors = funcs = 0
slot_rows = []                      # (file, actor, k, fn index, fn name, primary counts, secondary counts, size)
nonslot_primary = collections.Counter()
nonslot_fn_with_primary = 0
chg_rows = []                       # REQCHG slot 16/17 sites
chg_slots = collections.Counter()
fnwait = {}                         # (file, actor index, fn index) -> (name, primary Counter, secondary Counter)
seen = set()
for p in sorted(EX.rglob("*.ebp")):
    b = p.read_bytes()
    h = hashlib.md5(b).digest()
    if h in seen:
        continue
    seen.add(h)
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18)
    cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        continue
    files += 1
    rel = p.relative_to(EX).as_posix()
    pool = U32(sec, 0x4C)
    ents = [diroff + 4 + a * 0x30 for a in range(cnt)]
    starts = sorted(set(U32(sec, e + 8) for e in ents))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    done_actor = set()
    per_actor = {}
    for ai, e in enumerate(ents):
        start = U32(sec, e + 8)
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start:
            continue
        actors += 1
        aname = cstr(sec, pool + U32(sec, e))
        code = sec[start:end]
        ins_a, _ = G.decode(code)            # histogram rule: one decode per directory entry
        for _pc, op, _imm in ins_a:
            tot_actor[op] += 1
        ft = U32(sec, e + 0x10)
        nf = U32(sec, ft)
        foffs = [U32(sec, ft + 4 + 8 * i + 4) for i in range(nf)]
        fnames = [cstr(sec, pool + U32(sec, ft + 4 + 8 * i)) for i in range(nf)]
        sepa = U32(sec, e + 0x18)
        fc = U16(sec, sepa)
        special = [U16(sec, sepa + 2 + 2 * k) if k < fc else 0xFFFF for k in range(18)]
        uniq = sorted(set(o for o in foffs if o < len(code)))
        per_actor[ai] = (aname, fnames, foffs)
        slotfn = {special[16]: 16, special[17]: 17}
        for fi in range(nf):
            o = foffs[fi]
            nxt = min((x for x in uniq if x > o), default=len(code))
            body = code[o:nxt]
            ins, _ = G.decode(body)
            prim = collections.Counter(PRIMARY[op] for _pc, op, _i in ins if op in PRIMARY)
            secd = collections.Counter(SECONDARY[op] for _pc, op, _i in ins if op in SECONDARY)
            fnwait[(rel, ai, fi)] = (fnames[fi], prim, secd, len(body))
            first_of_offset = foffs.index(o) == fi   # two names on one offset share one body; count it once
            if first_of_offset:
                funcs += 1
                for _pc, op, _i in ins:
                    tot_fn[op] += 1
            if fi in slotfn and special[slotfn[fi]] != 0xFFFF:
                pass
            elif prim and first_of_offset:
                nonslot_primary.update(prim)
                nonslot_fn_with_primary += 1
            # REQCHG sites anywhere in this function
            for j, (pc, op, imm) in enumerate(ins):
                if op != 0x34:
                    continue
                args, st = G.resolve_args(ins, j, 3, verbs)
                if st != "ok":
                    chg_slots["unresolved:" + st] += 1
                    continue
                sl, act, val = args
                slv = G.classify_arg(*sl)
                key = slv[1] if slv[0] == "const-int" else "%s:%s" % slv
                chg_slots[key] += 1
                if key in (16, 17):
                    chg_rows.append((rel, ai, aname, fnames[fi], "%x" % (start + o + pc), key, act, val))
        for k in (16, 17):
            w = special[k]
            if w == 0xFFFF:
                continue
            if w >= nf:
                slot_rows.append((rel, ai, aname, k, w, "(out of range, nf=%d)" % nf, None, None, 0))
                continue
            nm, prim, secd, size = fnwait[(rel, ai, w)]
            slot_rows.append((rel, ai, aname, k, w, nm, prim, secd, size))
    fnwait_file = per_actor
    for idx, r in enumerate(chg_rows):
        if r[0] != rel or len(r) != 8:
            continue
        rel_, ai, aname, fname, pc, key, act, val = r
        # actor operand: a PUSHII / PUSHACT immediate whose high word is 0 reaches 0025AF60 as r8d with bit 14/15 clear:
        # manager sar(r8d,16) = 0 and record ordinal r8w (0025AF83-0025AF9C). Reading that ordinal as the directory
        # index of the target actor in the same image is an INFERENCE; C4 checks it by the resolved function's name.
        tgt = None
        if act[0] in ("PUSHACT", "PUSHII") and act[1] is not None and act[1] < 0x4000:
            tgt = act[1]
        vv = G.classify_arg(*val)
        fi = vv[1] if vv[0] == "const-int" else None
        if val[0] == "PUSHII":
            fi = val[1]
        res = None
        if tgt is not None and tgt in fnwait_file and fi is not None and fi < len(fnwait_file[tgt][1]):
            res = fnwait[(rel, tgt, fi)]
        chg_rows[idx] = r + (tgt, fi, res)

print("files %d, actors %d, distinct function bodies %d" % (files, actors, funcs))
ok = True
print("\nC1 partition control (function partition / whole-actor decode / histogram):")
for op, want in CTRL_OPS.items():
    good = tot_fn[op] == tot_actor[op] == want
    ok &= good
    print("  %-7s %7d / %7d / %7d  %s" % (G.OPN[op], tot_fn[op], tot_actor[op], want, "PASS" if good else "FAIL"))
print("  all opcodes: function partition %d, whole-actor %d instructions  %s"
      % (sum(tot_fn.values()), sum(tot_actor.values()), "PASS" if tot_fn == tot_actor else "DIFFER"))
ok &= tot_fn == tot_actor
print("\nC2 positive control: functions NOT named by a footer slot 16/17 that contain a primary waited request: %d; "
      "their opcodes %s  %s" % (nonslot_fn_with_primary, dict(nonslot_primary),
                                 "PASS" if nonslot_fn_with_primary > 0 else "FAIL"))
ok &= nonslot_fn_with_primary > 0

print("\nFOOTER SLOTS 16 / 17 (the ids 00268EA0 reads at 00268F68 / 00268F21 when the override word is 0xFFFF)")
for k in (16, 17):
    rows = [r for r in slot_rows if r[3] == k]
    names = collections.Counter(r[5].rstrip("0123456789_") for r in rows)
    withp = [r for r in rows if r[6]]
    withs = [r for r in rows if r[7]]
    print("  k=%d: %d actors in %d files set it; function names %s" % (k, len(rows), len(set(r[0] for r in rows)),
                                                                       dict(names.most_common(6))))
    print("        with a primary waited request (REQSW/REQEW/F*/T*): %d; with a secondary wait op: %d  %s"
          % (len(withp), len(withs), dict(sum((r[7] for r in withs), collections.Counter()))))
    sizes = collections.Counter(r[8] for r in rows)
    print("        body sizes (bytes: actors): %s" % dict(sorted(sizes.items())[:12]))
    for r in withp[:40]:
        print("        WAIT %s actor %d %s fn %d %s: %s" % (r[0], r[1], r[2], r[4], r[5], dict(r[6])))
    for r in withs[:20]:
        print("        SEC  %s actor %d %s fn %d %s: %s" % (r[0], r[1], r[2], r[4], r[5], dict(r[7])))
c3 = all(r[5].startswith("talkhold" if r[3] == 16 else "talkterm") for r in slot_rows)
odd = [r for r in slot_rows if not r[5].startswith("talkhold" if r[3] == 16 else "talkterm")]
print("C3 every slot-16 word names talkhold*, every slot-17 word talkterm*: %s (%d exceptions)"
      % ("PASS" if c3 else "FAIL", len(odd)))
for r in odd[:10]:
    print("   exception: %s" % (r[:6],))
ok &= c3 and len(slot_rows) > 0

print("\nREQCHG slot operand distribution (all shipped sites, resolve_args need=3): %s"
      % dict(sorted(chg_slots.items(), key=lambda kv: (isinstance(kv[0], str), str(kv[0])))))
print("REQCHG slot 16/17 sites: %d" % len(chg_rows))
c4 = True
chgp = 0
for r in chg_rows:
    rel_, ai, aname, fname, pc, key, act, val, tgt, fi, res = r
    if res is None:
        c4 = False
        print("  UNRESOLVED %s actor %d %s in %s pc %s slot %s actor-arg %s value-arg %s" % (rel_, ai, aname, fname, pc,
                                                                                          key, act, val))
        continue
    nm, prim, secd, size = res
    chgp += bool(prim)
distinct = collections.Counter()
for r in chg_rows:
    if r[10] is None:
        continue
    nm, prim, secd, size = r[10]
    distinct[(r[0].split("/")[-1], r[5], nm, size, str(dict(prim)) if prim else "-", str(dict(secd)) if secd else "-")] += 1
print("  distinct (zone file, slot, target function, bytes, primary waits, secondary waits): sites across languages")
for k, n in sorted(distinct.items()):
    print("    %-14s slot %d -> %-28s %4d B  primary=%s secondary=%s   x%d" % (k + (n,)))
print("C4 every slot-16/17 REQCHG value resolves to a target-actor function: %s" % ("PASS" if c4 else "FAIL"))
ok &= c4
match = sum(1 for r in chg_rows if r[10] and r[10][0].startswith("talkhold" if r[5] == 16 else "talkterm"))
print("C4b name check of the ordinal = directory-index reading: %d of %d resolved targets are talkhold* (slot 16) / "
      "talkterm* (slot 17); the rest are printed above  %s" % (match, len(chg_rows), "PASS" if match * 10 >= 9 * len(chg_rows) else "FAIL"))
ok &= match * 10 >= 9 * len(chg_rows)
allk = [r for r in slot_rows if r[6]]
print("\nRESULT: footer slot-16/17 functions with a primary waited request: %d of %d; REQCHG slot-16/17 override "
      "functions with one: %d of %d" % (len(allk), len(slot_rows), chgp, len(chg_rows)))
with open(os.path.join(HERE, "ov16m_slot_functions.tsv"), "w", newline="\n", encoding="utf-8") as w:
    w.write("file\tactor_index\tactor\tslot\tfn_index\tfn_name\tbytes\tprimary_waits\tsecondary_waits\n")
    for r in slot_rows:
        w.write("%s\t%d\t%s\t%d\t%d\t%s\t%d\t%s\t%s\n" % (r[0], r[1], r[2], r[3], r[4], r[5], r[8],
                                                         dict(r[6]) if r[6] else "", dict(r[7]) if r[7] else ""))
print("CONTROLS: %s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
