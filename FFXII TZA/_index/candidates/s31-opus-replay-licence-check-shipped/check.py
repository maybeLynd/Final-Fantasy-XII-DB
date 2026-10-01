"""S-31: execute CONTRACT-license-check.md's entries - the ask 00323EC0, the prerequisite test 00323BB0, the mask builder 002F8FA0,
the Quickening count 00324020 and the slot-row search 0030A330 - as shipped code over the SHIPPED licence, ability and party-slot
tables, bound from battle_pack.bin by shipped code (OPUS, 2026-09-25, block 326).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session with stack arguments)
supplies the image, the IAT traps and the named bridges; its world is built once. No application stub and no stop boundary.
EXP-140 executed these bodies over planted descriptors; this runs them over the shipped data.
THE TABLES ARE THE SHIPPED ONES: battle_pack.bin (us) is copied raw to 0x76100000; 003846F0(&[0208E680], blob, 0) - the
delivery stub 00238850's first call - relocates the directory; then the three slot bindings this path reads are made by the
same shipped call 00236C30 makes for them, 003845F0(slot, dir[off]): 02EBF038 <- +0x34 (00236D67, the licence records),
02EBF130 <- +0x44 (00236DAB, the party-slot rows) and 02EBF138 <- +0x3C (00237FDE, the first call of 00237FC0, the ability
rows). 00236C30 is not run whole: 00237FC0 and 00238880 go on to allocate from engine heap 6, which halts unbuilt.
The codec base stays at the image's 0 (block 324: the delivery path requires it). Fixtures: the BattleStatsRecord (46-byte
owned mask at +0x194, +4 slot, +5 kind) and the 0x2E-byte mask buffer.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn.x86_const import UC_X86_REG_RAX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
PACK = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "repos-2d", "vbf", "ps2data", "image", "ff12", "test_battle", "us",
                    "binaryfile", "battle_pack.bin")
PACK_SHA = "d1bb89aac759cfcd4eb181715d9e88afb78d62a9a3fcffa6242f365f182cbc98"
ASK, PREREQ, BUILD, COUNT, SEARCH, RELOCATE, SLOTBIND, VALIDATE = 0x323EC0, 0x323BB0, 0x2F8FA0, 0x324020, 0x30A330, 0x3846F0, 0x3845F0, 0x322C50
W.ALLOWED |= {0x16D6A0} | set().union(*(W.closure(f) for f in (ASK, PREREQ, BUILD, COUNT, SEARCH, RELOCATE, SLOTBIND)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
B, REC, BUF = 0x76100000, 0x76180000, 0x76181000
LIC, SLOTS, ABIL = 0x2EBF038, 0x2EBF130, 0x2EBF138


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def run(fn, *args):
    ok = S.call(fn, *args)
    assert ok, (hex(fn), (S.st["bad"] or S.st["faults"])[:2])
    return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-36s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- bind ----
pack = open(PACK, "rb").read()
assert hashlib.sha256(pack).hexdigest() == PACK_SHA
uc.mem_write(B, pack)
run(RELOCATE, 0x208E680, B, 0)
d = lambda off: r(B + off, "<I")[0]
for slot, off in ((LIC, 0x34), (SLOTS, 0x44), (ABIL, 0x3C)):
    run(SLOTBIND, slot, d(off))


def table(slot):
    h = r(slot, "<Q")[0]
    _, n, stride, _, enc = r(h, "<IIHHI")
    return h, n, stride, enc


lic_h, lic_n, lic_s, lic_d = table(LIC)
ab_h, ab_n, ab_s, ab_d = table(ABIL)
sl_h, sl_n, sl_s, sl_d = table(SLOTS)
record("bind_shipped_tables", lic_h == B + 0x8E48 and ab_h == B + 0x13210 and sl_h > B,
       licence=[lic_n, lic_s], ability=[ab_n, ab_s], party_slots=[sl_n, sl_s],
       note="003845F0 binds the three slots from the relocated directory: licence records %d x %d, ability rows %d x %d, party-slot "
            "rows %d x %d" % (lic_n, lic_s, ab_n, ab_s, sl_n, sl_s))


# ---- the stats record ----
def rec(slot=0, kind=0, owned=()):
    uc.mem_write(REC, bytes(0x200))
    w(REC + 4, "<BB", slot, kind)
    for b in owned:
        v = r(REC + 0x194 + b // 8, "<B")[0]
        w(REC + 0x194 + b // 8, "<B", v | (1 << (b % 8)))
    return REC


# ---- an independent model of the licence records (raw file bytes + the kind -> class map read at 003241D0 / 00323890) ----
def kind_class(c):
    x = {1: 0x15, 2: 0x15, 3: 0x15, 4: 0x16, 5: 0x16, 6: 0x16, 7: 0x17, 8: 0x18, 9: 0x19, 10: 0x19, 11: 0x19, 12: 0x19, 13: 0x19,
         14: 0x1A, 15: 0x1B, 16: 0x1B, 17: 0x1B, 18: 0x1C, 19: 0x1D, 20: 0x1D, 30: 0x1E}.get(c)
    return {0x15: 0, 0x16: 0, 0x17: 0, 0x18: 0, 0x19: 1, 0x1A: 1, 0x1B: 2, 0x1C: 2, 0x1D: 1, 0x1E: 3}.get(x, -1)


records = []
for i in range(lic_n):
    a = lic_d + i * lic_s
    records.append((pack[a - B + 5], list(struct.unpack_from("<8H", pack, a - B + 8))))


def model_mask(kind, action):
    return {i for i, (k, ids) in enumerate(records) if kind_class(k) == kind and action in ids}


# ---- the builder over every ability id, kind 1 ----
mism, masks = [], {}
for a in range(ab_n):
    uc.mem_write(BUF, b"\xAA" * 0x40)
    n = run(BUILD, 1, a, BUF)
    got = {i for i in range(lic_n) if r(BUF + i // 8, "<B")[0] >> (i % 8) & 1}
    if got != model_mask(1, a) or n != len(got):
        mism.append([a, sorted(got)[:6], sorted(model_mask(1, a))[:6]])
    masks[a] = got
granted = sorted(a for a in masks if masks[a])
low_bits = sorted({b for a in masks for b in masks[a] if b < 18})
record("builder_every_ability_matches_model", not mism, abilities=ab_n, with_a_licence=len(granted), mismatches=mism[:5],
       licence_bits_0_17_in_any_kind1_mask=low_bits,
       note="002F8FA0(1, id) over all %d shipped ability ids: the mask agrees with an independent decode of the licence records "
            "every time; %d ids are granted by at least one record" % (ab_n, len(granted)))

# ---- I3: the escape bit, over every ability id, with a kind-0 slot-0 record that owns nothing ----
esc_model = [a for a in range(ab_n) if r(ab_d + a * ab_s + 0x2C, "<H")[0] & 0x2000]
licensed_empty = [a for a in range(ab_n) if run(ASK, rec(), a)]
quick = list(range(0xD0, 0xE2))
record("I3_escape_bit_census", [a for a in licensed_empty if a not in quick] == [a for a in esc_model if a not in quick],
       escape_rows=len(esc_model), licensed_with_empty_board=len(licensed_empty),
       note="with nothing owned, exactly the %d rows whose +0x2C has bit 0x2000 are licensed (Quickening ids aside)" % len(esc_model))

# ---- I4: owning ANY one record that lists the id licenses it ----
i4 = []
for a in granted[:40]:
    bits = sorted(masks[a])
    one = [run(ASK, rec(owned=[b]), a) for b in bits]
    other = [b for b in range(18, lic_n) if b not in masks[a]][:1]
    no = run(ASK, rec(owned=other), a) if other else 0
    esc = a in esc_model
    i4.append(all(one) and (no == 0 or esc))
record("I4_any_single_square", all(i4), checked=len(i4),
       note="for 40 granted ids: owning any single one of the records that list the id licenses it; owning an unrelated record does not")

# ---- I5: Quickenings, over the shipped party-slot rows ----
qrows = {s: list(r(sl_d + s * sl_s + 4, "<3B")) for s in range(7)}
i5 = {}
for s in range(6):
    for n in (0, 1, 2, 3):
        i5.setdefault(s, {})[n] = [run(ASK, rec(slot=s, owned=range(n)), a) for a in qrows[s]]
i5_ok = all(i5[s][n] == [1 if k < n else 0 for k in range(3)] for s in range(6) for n in (0, 1, 2, 3))
# the signed setl edge on shipped rows: an id from ANOTHER slot's row is 'absent' (0030A330 -> 3) and passes once 4 bits are owned
cross = {}
for s in range(7):
    other = [a for a in quick if a not in qrows[s]][0]
    cross[s] = {"id": "%02X" % other, "search": run(SEARCH, sl_d + s * sl_s, other),
                "3_bits": run(ASK, rec(slot=s, owned=range(3)), other), "4_bits": run(ASK, rec(slot=s, owned=range(4)), other)}
cross_ok = all(v["search"] == 3 and v["3_bits"] == 0 and v["4_bits"] == 1 for v in cross.values())
covered = sorted(x for s in range(6) for x in qrows[s])
record("I5_quickenings_counted_over_shipped_rows", i5_ok and cross_ok and covered == quick and qrows[6] == [0, 0, 0],
       slot_rows={s: ["%02X" % x for x in v] for s, v in qrows.items()}, per_slot_counts=i5, cross_slot=cross,
       note="slots 0..5 each name three Quickening ids and together cover 0xD0..0xE1 exactly; slot 6's row is 00 00 00. The k-th id is "
            "licensed once k+1 of bits 0..17 are owned. ANOTHER slot's id is absent from the row (0030A330 -> 3) and is licensed as "
            "soon as 4 bits are owned (signed setl) - for every slot, including slot 6")

# ---- what bits 0..17 are in the shipped licence records ----
low = [{"record": i, "kind": records[i][0], "class": kind_class(records[i][0]), "ids": ["%04X" % x for x in records[i][1] if x != 0xFFFF]}
       for i in range(18)]
record("licence_records_0_17", all(x["kind"] == 19 and not x["ids"] for x in low) and not low_bits, records=low, in_any_kind1_mask=low_bits,
       note="licence records 0..17 - the bits 00324020 counts - are all kind 19 and list no id; no kind-1 mask over the 543 ability "
            "ids sets any of them, so they are read only as the Quickening count")

json.dump({"ok": allok, "battle_pack_sha256": PACK_SHA, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
