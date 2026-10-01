"""SWE2-AUDIT-SEM: (3) the harness's AMBIGUOUS guard. For each mutant in mutate_rule.MUTANTS (read by exec of the list
only, no mutation run), count the anchor's occurrences in documented_rule.py, and how many characters the anchor has
(short anchors are the ones at risk of becoming ambiguous under a later edit). Sensitivity of the guard itself: the
guard line is `if SRC.count(old) != 1`; a duplicated anchor is simulated in memory by doubling the source, which must
make every anchor count 2."""
import io, re
H = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\status-currency-ruling-fable"
src = io.open(H + r"\mutate_rule.py", encoding="utf-8").read()
start = src.index("MUTANTS = [")
end = src.index("\n]\n", start) + 3
ns = {}
exec(src[start:end], ns)
rule = io.open(H + r"\documented_rule.py", encoding="utf-8").read()
for name, old, new in ns["MUTANTS"]:
    print("%-34s anchor chars %4d  occurrences %d" % (name, len(old), rule.count(old)))
print("guard sensitivity: every anchor counts 2 in a doubled source:",
      all((rule + rule).count(old) == 2 for n, old, new in ns["MUTANTS"]))
