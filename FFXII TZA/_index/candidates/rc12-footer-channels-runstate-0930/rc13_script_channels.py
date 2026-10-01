"""rc13_script_channels.py - RC-13 (ORACLE, 2026-09-30): the first operand the shipped scripts pass to each REQ-family
call, per call form, over the decompiled US corpus (1,114 scripts, FABLE's pub140 corpus).

ff12-script's high decoder (CScriptDecompileHighRequests.cpp) prints opcode 0x21 REQ as sysReq, 0x24 REQSW as sysReqsw,
0x27 REQEW as sysReqew, 0x34 REQCHG as sysReqchg, 0x5F REQALL as sysReqall, 0x63 REQIALL as sysReqiall, 0x32 REQWAIT as
sysReqwait (two operands, no channel) and REQWAITALL as sysReqwaitall; a trailing `i` means an INCINITTAG 0 precedes the
opcode (compileVisitorHighCalls.cpp). The first printed operand is the CHANNEL for REQ / REQSW / REQEW / REQALL /
REQIALL, but for REQCHG it is the SLOT of the record's special-function override array (0025AF60 stores
word [record + 0xC8 + 2*slot], slot <= 0x11), so REQCHG is tallied separately.
Control: the per-form call totals equal a plain `form(` count of the same text.
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "FABLE", "pub140-scratch", "corpus", "us")
FORMS = ["sysReq", "sysReqi", "sysReqsw", "sysReqswi", "sysReqew", "sysReqewi", "sysReqall", "sysReqiall", "sysReqchg"]
CALL = re.compile(r"\b(sysReq(?:i|sw|swi|ew|ewi|all|iall|chg)?)\(\s*([^,()]+?)\s*,\s*([^)]*)\)")
SPECIAL = {"main": 1, "talk": 2, "touch": 3, "touchon": 4, "touchoff": 5, "across": 6, "spawn": 7, "fieldsign1": 8,
           "initevent": 9, "parameter": 11, "mapjump": 12, "fieldsign2": 13, "touch2": 13, "respawn": 14,
           "talkhold": 16, "talkterm": 17}


def main():
    first = collections.defaultdict(collections.Counter)
    plain = collections.Counter()
    parsed = collections.Counter()
    special_on = collections.defaultdict(collections.Counter)   # channel -> special function names requested there
    chg_fn = collections.defaultdict(collections.Counter)       # REQCHG slot -> function-name prefixes
    for fn in sorted(os.listdir(CORPUS)):
        if not fn.endswith(".txt"):
            continue
        t = open(os.path.join(CORPUS, fn), encoding="utf-8", errors="replace").read()
        for f in FORMS:
            plain[f] += len(re.findall(r"\b" + f + r"\(", t))
        for m in CALL.finditer(t):
            form, a0, rest = m.group(1), m.group(2), m.group(3)
            parsed[form] += 1
            v = int(a0, 0) if re.match(r"^-?(0x[0-9a-fA-F]+|\d+)$", a0) else "non-literal"
            first[form][v] += 1
            tgt = rest.split("::")[-1].strip() if "::" in rest else None
            if form == "sysReqchg":
                if tgt:
                    chg_fn[v][re.match(r"[A-Za-z]*", tgt).group(0) or tgt[:4]] += 1
            elif tgt in SPECIAL and isinstance(v, int):
                special_on[v][tgt] += 1
    print("per form: calls parsed / plain count; first operand distribution")
    ok = True
    for f in FORMS:
        dist = ", ".join("%s:%d" % (k, n) for k, n in sorted(first[f].items(), key=lambda kv: (isinstance(kv[0], str), kv[0])))
        print("  %-11s %6d / %6d   %s" % (f, parsed[f], plain[f], dist))
        ok &= parsed[f] == plain[f]
    ch = collections.Counter()
    for f in FORMS:
        if f != "sysReqchg":
            for k, n in first[f].items():
                ch[k] += n
    print("\nchannel operand, all channel-taking forms together:")
    print("  " + ", ".join("%s:%d" % (k, n) for k, n in sorted(ch.items(), key=lambda kv: (isinstance(kv[0], str), kv[0]))))
    print("\nspecial functions requested by name, by channel (the authored channel for an engine-named function):")
    for c in sorted(special_on):
        print("  channel %s: %s" % (c, ", ".join("%s %d" % kv for kv in special_on[c].most_common())))
    print("\nREQCHG slot operand -> requested function-name prefixes:")
    for s in sorted(chg_fn, key=lambda x: (isinstance(x, str), x)):
        print("  slot %s: %s" % (s, ", ".join("%s %d" % kv for kv in chg_fn[s].most_common(6))))
    print("CONTROL parsed == plain for every form: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
