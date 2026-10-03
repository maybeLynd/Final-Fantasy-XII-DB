"""uc1_credible.py - FABLE's UC-1 route ruling, test 1 ("a credible body"), measured for the UC-1 frontier bodies that
are still F-unmet (OPUS, 2026-10-03; ruling fable-uc1-gamecode-route-ruling-1003).

Per body: its uc1_band extent; direct call / jmp sites into the start (retool scan); rip references to the start;
aligned qwords anywhere in the image equal to the start (tables); and what precedes the start (the previous listed
body's end, int3 / nop padding, a ret or a jmp just before). Verdict:
  ENTERED      a direct site, a rip reference or a table qword reaches the start;
  FOLLOWS      nothing references it, but it starts right after a ret / tail jmp / int3-or-nop padding;
  ARTEFACT?    neither: a decode artefact until shown otherwise (needs a census admission first).
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
DBR = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA"))
sys.path.insert(0, KIT)
import check_dispositions as CD  # noqa: E402
import uc1_band  # noqa: E402
import retool  # noqa: E402


def main():
    sizes = CD.load_functions()
    explained = set(CD.evaluate(DBR, sizes)["explained_set"])
    band = uc1_band.load()["frontier"]
    todo = sorted(a for a in band if a in sizes and a not in explained)
    sc = retool.scan()
    calls, refs = sc["calls"], sc["refs"]
    # all aligned qwords in every section, once
    R = retool.R
    import pefile
    pe = pefile.PE(R.b.EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    want = set(todo)
    table = {}
    for s in pe.sections:
        d = s.get_data()
        for o in range(0, len(d) - 7, 8):
            v = struct.unpack_from("<Q", d, o)[0]
            if v in want:
                table.setdefault(v, []).append(base + s.VirtualAddress + o)
    # 2026-10-03 (SWE2-AUDIT-SPEC REJECT on the UC-1 rows): retool's call index holds call/jmp only, so `0F 8x`
    # conditional jumps and 32-bit image-relative fields were missed. Add every decoded jcc / short jump into a body,
    # and RVA dwords in .rdata/.data that are not inside a printable run (.pdata starts are unwind entries, not ways in).
    import re as _re
    for f, n in sizes.items():
        d = R.at(f, n)
        if not d:
            continue
        for i in R.md.disasm(d, f):
            if i.mnemonic.startswith("j") and i.mnemonic != "jmp" and _re.fullmatch(r"0x[0-9a-f]+", i.op_str):
                t = int(i.op_str, 16)
                if t in want and f != t:
                    calls.setdefault(t, set()).add((f, i.address))
    rv = {t - base: t for t in want}
    for s in pe.sections:
        if s.Name.rstrip(b"\0") not in (b".rdata", b".data"):
            continue
        d = s.get_data()
        for o in range(0, len(d) - 3, 4):
            v = struct.unpack_from("<I", d, o)[0]
            if v in rv and sum(32 <= c < 127 for c in d[max(0, o - 2):o + 6]) < 5:
                table.setdefault(rv[v], []).append(base + s.VirtualAddress + o)
    out = []
    for a in todo:
        n = band[a]
        direct = sorted(calls.get(a, ()))
        rip = sorted(refs.get(a, ()))
        tab = table.get(a, [])
        prev = R.at(a - 16, 16) or b""
        lastb = prev[-1:] if prev else b""
        pad = lastb in (b"\xcc", b"\x90")
        after_ret = lastb == b"\xc3"
        # a 5-byte jmp rel32 ending exactly at the start
        after_jmp = len(prev) >= 5 and prev[-5] == 0xE9
        if direct or rip or tab:
            v = "ENTERED"
        elif pad or after_ret or after_jmp:
            v = "FOLLOWS"
        else:
            v = "ARTEFACT?"
        out.append({"body": "%08X" % a, "size": n, "verdict": v,
                    "direct": ["%08X@%08X" % x for x in direct][:6], "rip": ["%08X@%08X(%s)" % x for x in rip][:6],
                    "tables": ["%08X" % t for t in tab][:6], "prev_byte": lastb.hex(), "after_ret": after_ret,
                    "after_jmp": after_jmp, "pad": pad, "aligned16": a % 16 == 0})
    import collections
    print(collections.Counter(o["verdict"] for o in out))
    for o in out:
        print("%s %4d %-9s direct=%s rip=%s tab=%s prev=%s%s" % (
            o["body"], o["size"], o["verdict"], ",".join(o["direct"][:2]) or "-", ",".join(o["rip"][:2]) or "-",
            ",".join(o["tables"][:2]) or "-", o["prev_byte"], "" if o["aligned16"] else " UNALIGNED"))
    json.dump(out, open(os.path.join(HERE, "uc1_credible.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
