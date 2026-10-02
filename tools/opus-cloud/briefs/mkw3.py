"""mkw3.py - write the wave-3 stream R briefs from the wave-2 template (OPUS, 2026-10-02)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(HERE, "w2-r-05.txt"), encoding="utf-8").read()
OLD = [("OPUS-CLOUD-R-READINESS-05-1002", "OPUS-CLOUD-R-READINESS-{n}-1002"),
       ("FFXII TZA/05-Spawn-Encounter-Lifecycle/", "FFXII TZA/{folder}/"),
       ("cloud-reports/re-readiness/05-spawn.md", "cloud-reports/re-readiness/{n}-{slug}.md"),
       ("cloud/re-readiness-05-spawn", "cloud/re-readiness-{n}-{slug}")]
for a, _ in OLD:
    assert T.count(a) == 1, a
W3 = [("03", "03-World-Area-Field", "world"), ("04", "04-Actor-Entity", "actor"),
      ("11", "11-Party", "party"), ("14", "14-Story-Event-Quest-Hunt", "story")]
for n, folder, slug in W3:
    b = T
    for a, f in OLD:
        b = b.replace(a, f.format(n=n, folder=folder, slug=slug))
    b += (" Note: the snapshot is " "df2c9f47" "; several pages in this folder are being edited by other lanes, so"
          " quote the text exactly as the snapshot has it.")
    p = os.path.join(HERE, "w3-r-%s.txt" % n)
    open(p, "w", encoding="utf-8", newline="\n").write(b)
    print(p)
