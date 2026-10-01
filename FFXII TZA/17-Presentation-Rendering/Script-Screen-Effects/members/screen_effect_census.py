"""Census of the script-driven screen-effect verbs (cut-in, motion blur, soft focus) in the decompiled `us` scripts.

Counts every call of the twenty-four verbs of the family (names from scriptvm-verb-table.tsv, call ids 02AE, 0310-0322,
03AC, 03BB-03BD; a decompiler arity suffix such as `_1a3` is accepted), by verb, and prints the distinct literal argument tuples of the verbs that
choose a type or a mode, with the number of calls and of scripts that use each.
Verbs of the family with no call at all are printed with a zero, so that absence is a row and not a silence.
Control: the per-verb counts must sum to the number of call sites found by a plain substring count of the same names.
"""
import os, re, collections

CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
FAMILY = ("setsoftfocusmode", "cutinplay", "cutinclear", "resetcutinparam", "cutintype", "cutinlinefade", "cutinpos",
          "cutinrotate", "cutinlinewidth", "cutinuv", "cutincolor", "cutinlinecolor", "moveblurplay", "moveblurclear",
          "resetmoveblurparam", "moveblurpresettype", "moveblurcluttype", "moveblurnoisetype", "moveblurscreentype",
          "movebluraplpha", "moveblurcaptureonce", "moveblurfade", "moveblurclearfade", "moveblurfadesync")
STEM = "(?:" + "|".join(sorted(FAMILY, key=len, reverse=True)) + ")"
call = re.compile(r"\b(" + STEM + r"(?:_[0-9a-f]+)?)\(([^()]*)\)")
plainre = re.compile(r"\b" + STEM + r"(?:_[0-9a-f]+)?\(")
TUPLES = ("cutintype", "moveblurpresettype", "moveblurcluttype", "moveblurnoisetype", "moveblurscreentype",
          "setsoftfocusmode", "movebluraplpha", "moveblurfade", "moveblurclearfade", "cutinlinefade")
verbs = collections.Counter()
scripts = collections.defaultdict(set)
tup = collections.Counter()
tupfiles = collections.defaultdict(set)
plain = 0
nested = 0
for fn in sorted(os.listdir(CORPUS)):
    if not fn.endswith(".txt"):
        continue
    t = open(os.path.join(CORPUS, fn), encoding="utf-8", errors="replace").read()
    plain += len(plainre.findall(t))
    for m in call.finditer(t):
        v = m.group(1)
        base = re.sub(r"_[0-9a-f]+$", "", v)
        verbs[v] += 1
        scripts[v].add(fn)
        if base in TUPLES:
            key = (base, ", ".join(x.strip() for x in m.group(2).split(",")))
            tup[key] += 1
            tupfiles[key].add(fn)
parsed = sum(verbs.values())
print("# call sites by substring %d; by parsed call %d; difference %d (calls whose arguments contain a nested call)"
      % (plain, parsed, plain - parsed))
print("verb\tcalls\tscripts")
for v in FAMILY:
    if not any(re.sub(r"_[0-9a-f]+$", "", k) == v for k in verbs):
        verbs[v] = 0
for v, n in sorted(verbs.items()):
    print("%s\t%d\t%d" % (v, n, len(scripts[v])))
print("verb\targuments\tcalls\tscripts")
for (v, a), n in sorted(tup.items()):
    print("%s\t%s\t%d\t%d" % (v, a, n, len(tupfiles[(v, a)])))
