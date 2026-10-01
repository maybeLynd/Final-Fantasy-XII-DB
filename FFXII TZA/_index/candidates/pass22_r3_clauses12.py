"""pass22_r3_clauses12.py (from pass22_r3_delta.py; R3MODE=12 body+whole-word, R3MODE=2 whole-word on full text) - measure the population change R3 (PASS22-WHAT-ACCOUNTING-MEANS §4.3) would cause, before any vote.
Runs audit_crossrefs' own pair enumeration twice over the working tree:
  current  : doc_accounts_for as shipped (alias substring anywhere in text or folder path), then R1 registry clearing
  tightened: body only (YAML front matter and markdown link targets removed), whole-word alias matches, and the ordinary-word
             aliases dropped; folder path still counts; R1 registry clearing unchanged
Prints both finding counts, the delta by subsystem and a sample of pairs that R3 would newly report."""
import importlib.util, io, os, re, sys, collections, random
K = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts\audit_crossrefs.py"
spec = importlib.util.spec_from_file_location("ac", K); ac = importlib.util.module_from_spec(spec)
sys.argv = [K]; spec.loader.exec_module(ac)
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
G = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
fn = ac.load_functions(os.path.join(G, "functions.tsv"))
ac.register_ledger_aliases({v["owner"] for v in fn.values()})
ac.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
callers, callees = ac.load_edges(os.path.join(G, "edges.tsv"))
disposed, _unk = ac.load_dispositions(DB)
DROP = set()
MODE = __import__("os").environ.get("R3MODE", "12")
FM = re.compile(r"^---\n.*?\n---\n", re.S)
LINKT = re.compile(r"\]\([^)]*\)")


def tight_accounts(body_low, folder_low, sub):
    aliases = ac._ALIAS_NORM.get(ac._canon(sub))
    if aliases is None:
        aliases = [w for w in re.split(r"[_/ ]+", sub.lower()) if len(w) > 3]
    for al in aliases:
        if al in DROP:
            continue
        if al in folder_low:
            return True
        if re.search(r"(?<![a-z0-9])" + re.escape(al) + r"(?![a-z0-9])", body_low):
            return True
    return False


cur = collections.Counter(); tig = collections.Counter(); new_pairs = []
for dirpath, _d, files in os.walk(DB):
    if os.sep + "_templates" in dirpath:
        continue
    for name in sorted(files):
        if not name.lower().endswith(".md"):
            continue
        path = os.path.join(dirpath, name); rel = os.path.relpath(path, DB).replace(os.sep, "/")
        if "_index/" in rel or rel.startswith("_"):
            continue
        text = io.open(path, encoding="utf-8").read(); low = text.lower(); folder_low = rel.lower()
        body_low = LINKT.sub("]", FM.sub("", text.replace("\r\n", "\n"), count=1)).lower()
        cited = sorted(set(ac.ADDR.findall(text)))
        if not cited:
            continue
        lines = text.split("\n")
        ctrl = {c for c in cited if all(re.search(r"\bcontrol\b", ln, re.I) for ln in lines if c in ln) and any(c in ln for ln in lines)}
        cited = [c for c in cited if c not in ctrl]
        subs = set()
        for addr in cited:
            if addr not in fn or ac.is_substrate(fn.get(addr)) or len(callers.get(addr, ())) > ac.HUB_FANIN:
                continue
            for table in (callers, callees):
                for other in table.get(addr, ()):
                    sub = ac.subsystem_of(fn.get(other))
                    if sub and sub not in ac.SUBSTRATE:
                        subs.add(sub)
        for sub in subs:
            if (rel, sub) in disposed:
                continue
            c = not ac.doc_accounts_for(low, folder_low, sub)
            t = not tight_accounts(body_low if MODE == "12" else low, folder_low, sub)
            if c:
                cur[sub] += 1
            if t:
                tig[sub] += 1
                if not c:
                    new_pairs.append((rel, sub))
print("findings now (after R1):", sum(cur.values()))
print("findings under R3      :", sum(tig.values()), " (+%d)" % (sum(tig.values()) - sum(cur.values())))
print("delta by subsystem:")
for s in sorted(set(cur) | set(tig), key=lambda s: -(tig[s] - cur[s]))[:25]:
    print("  %-32s %4d -> %4d  (+%d)" % (s, cur[s], tig[s], tig[s] - cur[s]))
random.seed(3)
for p in random.sample(new_pairs, min(12, len(new_pairs))):
    print("  new:", p[0], "|", p[1])
