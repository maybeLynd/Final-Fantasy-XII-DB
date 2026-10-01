"""SWE2-AUDIT-SPEC: decode phyretext.fx.phyre's pointer fixup table with FABLE's CU-3 decoder (candidates/cu3-fixup-tables,
not ASTRA's copy) - only the decoder definitions are executed - and print the entries whose key low byte is 22 or 27.
Also compares ASTRA's copied decoder text with FABLE's."""
import os, sys, struct, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
FAB = os.path.join(HERE, r"..\cu3-fixup-tables\cu3_fixup_tables.py")
AST = os.path.join(HERE, r"..\..\..\_experiments\evidence\phyretext-softedges-field-extent\softedges-resource-source-01\cu3_fixup_tables.py")
src = open(FAB, encoding="utf-8").read()
print("decoder copies identical:", hashlib.sha256(open(FAB, "rb").read()).hexdigest() == hashlib.sha256(open(AST, "rb").read()).hexdigest())
cut = src.index("\nd = (ROOT")
g = {"__file__": FAB, "__name__": "cu3_defs"}
exec(compile(src[:cut], FAB, "exec"), g)
path = r"D:/FFXII_TZA_extract/gamedata/d3d11/artdata/shaders/phyretext.fx.phyre"
w, lists, res = g["check"](path)
print("lists", len(lists), "tables", {k: v[0] for k, v in res.items() if k != "tail"}, "tail", res["tail"])
ptr = res["ptr"][1]
print("pointer entries", len(ptr))
for e in ptr:
    if e[0] & 0x80000000 and (e[0] & 0xff) in (22, 27):
        print("  key %d:" % (e[0] & 0xff), [hex(e[0])] + list(e[1:]))
print("all 0x800000NN keys:", sorted((e[0] & 0xff) for e in ptr if e[0] & 0x80000000))
