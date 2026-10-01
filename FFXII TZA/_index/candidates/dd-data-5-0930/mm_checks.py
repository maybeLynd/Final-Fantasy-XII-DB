"""DD batch 5, movement-mode pages (SWE2-DATA 2026-09-30): static checks on the shipping image.
  W1 the store sites of the flat-movement gate globals 02B40530 / 02B40534 (full rip-relative sweep, not a function list)
  K1 00263CC0: class 1 -> [+0xB8]+0x38, class 3 -> [+0xB8]+0xA4 ('sub edx,1' then 'cmp edx,2'), else 0.0
  I1 every raw E8/E9 site that reaches the integrator 002E5750, and what each puts in edx (the second argument)
Controls: C1 the same raw call census finds the 29 call sites of 0026C120 that the mode page's section 11 re-derives;
          C2 the W1 sweep finds 003B7730's two gate reads (a reader census it must see).
Terminal FAILS line."""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, dis, text_range, raw_rip_refs, owner, ins_at  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    FAILS += not ok


def raw_calls(target):
    t0, t1, ro = text_range()
    blob = d[ro:ro + (t1 - t0)]
    out = []
    for p in range(len(blob) - 5):
        op = blob[p]
        if op in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", blob, p + 1)[0]
            if t0 + p + 5 + rel == target:
                x = ins_at(t0 + p)
                if x is not None and x.size == 5:
                    out.append(t0 + p)
    return out


# W1
refs = raw_rip_refs(0x02B40530, 0x02B40538)
stores = {0x02B40530: [], 0x02B40534: []}
reads = {0x02B40530: [], 0x02B40534: []}
for a, mn, ops, tgt in refs:
    if tgt not in stores:
        continue
    dst_is_mem = ops.split(",")[0].strip().startswith(("dword ptr [rip", "byte ptr [rip", "word ptr [rip",
                                                       "qword ptr [rip"))
    if mn.startswith("mov") and dst_is_mem:
        stores[tgt].append(a)
    else:
        reads[tgt].append(a)
for g in stores:
    print("   %08X stores %d: %s" % (g, len(stores[g]), " ".join("%08X(%08X)" % (s, owner(s) or 0) for s in stores[g])))
    print("   %08X other refs %d: %s" % (g, len(reads[g]), " ".join("%08X" % s for s in reads[g])))
fn534 = {owner(s) for s in stores[0x02B40534]}
check("W1 02B40534 has eight store sites in eight functions; 02B40530 has two",
      len(stores[0x02B40534]) == 8 and len(fn534) == 8 and len(stores[0x02B40530]) == 2,
      "%d sites / %d functions; 0530 %d" % (len(stores[0x02B40534]), len(fn534), len(stores[0x02B40530])))
check("C2 control: the sweep sees the gate 003B7730 reading both globals",
      any(owner(r) == 0x003B7730 for r in reads[0x02B40530]) and any(owner(r) == 0x003B7730 for r in reads[0x02B40534]))

# K1
k = {x.address: x for x in dis(0x00263CC0)}
check("K1 00263CC0: class 1 -> +0x38, class 3 -> +0xA4 (edx = class - 1 compared with 2)",
      k[0x00263CC9].op_str == "edx, 5" and k[0x00263CCC].op_str == "edx, 1" and k[0x00263CD1].op_str == "edx, 2"
      and k[0x00263CDD].op_str == "xmm0, dword ptr [rax + 0xa4]" and k[0x00263CED].op_str == "xmm0, dword ptr [rax + 0x38]")

# I1
sites = raw_calls(0x002E5750)
nonzero = []
for s in sites:
    fn = owner(s)
    body = dis(fn) if fn else []
    prev = [x for x in body if x.address < s][-8:]
    edx = "unknown"
    for x in reversed(prev):
        if x.op_str.startswith(("edx,", "rdx,", "dl,")) or x.op_str in ("edx, edx",):
            edx = "%s %s" % (x.mnemonic, x.op_str)
            break
    zero = edx.startswith("xor edx, edx") or edx in ("mov edx, 0",)
    print("   %08X in %08X: edx <- %s" % (s, fn or 0, edx))
    if not zero:
        nonzero.append((s, fn, edx))
check("I1 the integrator's raw call sites are found and each edx source is printed", len(sites) >= 1, "%d sites, %d not "
      "a literal zero" % (len(sites), len(nonzero)))

u = {x.address: x for x in dis(0x0025DF00)}
check("I2 the one caller 0025DF00 passes ebp: 1 only when actor +0x0D bit 1 is set, the render record is live and "
      "003E6A70's result has bit 0 set; ebp is 0 otherwise",
      len(sites) == 1 and u[0x0025DF1F].op_str == "ebp, ebp" and u[0x0025E328].op_str == "byte ptr [rdi + 0xd], 2"
      and u[0x0025E35A].op_str == "0x3e6a70" and u[0x0025E36A].op_str == "al, 1" and u[0x0025E36E].op_str == "ebp, 1"
      and u[0x0025E3A5].op_str == "edx, ebp")

# C1
c = raw_calls(0x0026C120)
check("C1 control: 29 raw call sites reach 0026C120", len(c) == 29, str(len(c)))
print("FAILS %d" % FAILS)
