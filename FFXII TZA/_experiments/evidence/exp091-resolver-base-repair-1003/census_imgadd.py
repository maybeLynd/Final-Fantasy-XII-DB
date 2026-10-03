# SWE2-ORACLE census for ASTRA-REQ-ORACLE-EXP091-RESOLVER-BASE-CONTROL-1003.
# Executes every check_repaired.py case and mutant fixture ONLY to list which
# paths call 0020E600 ("imgadd") and which read either base cell
# (0x1F83530 repaired / 0x1F85D30 old). It prints no PASS/FAIL: case checks
# are not evaluated here, so this is a reachability census, not a re-run of
# the EXP-091 campaign.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_repaired as H
from unicorn import UC_HOOK_MEM_READ

CELLS = {H.G_IMGB: "1F83530", H.G_IMGB_OLD_WRONG: "1F85D30"}

def census(case, raw, secs, iat_names):
    w = H.build(case, raw, secs, iat_names)
    reads = []
    def on_read(uc, access, addr, size, value, _):
        for base, nm in CELLS.items():
            if base <= addr < base + 8:
                reads.append(nm)
    for base in CELLS:
        w.uc.hook_add(UC_HOOK_MEM_READ, on_read, begin=base, end=base + 7)
    for ph in case.get("phases", [{}]):
        H.invoke(w, ph.get("entry", case.get("entry")),
                 rcx=ph.get("rcx", case.get("rcx", 0)),
                 rdx=ph.get("rdx", case.get("rdx", 0)),
                 r8=ph.get("r8", case.get("r8", 0)),
                 r9=ph.get("r9", case.get("r9", 0)),
                 stack=ph.get("stack", case.get("stack", ())))
    names = [t[0] for t in w.trace]
    return names.count("imgadd"), names.count("tvalid"), sorted(set(reads))

def main():
    raw, secs, iat_names = H.load_image()
    cases, mutants = H.build_cases()
    by_name = {c["name"]: c for c in cases}
    rows = []
    for c in cases:
        rows.append(("case", c["name"]) + census(c, raw, secs, iat_names))
    for m in mutants:
        c = dict(by_name[m["probe"]])
        c["patch"] = list(c.get("patch", [])) + m["patch"]
        rows.append(("mutant", m["name"]) + census(c, raw, secs, iat_names))
    print("fixtures executed: %d cases + %d mutants" % (len(cases), len(mutants)))
    hit = [r for r in rows if r[2] or r[3] or r[4]]
    print("fixtures with imgadd>0, tvalid>0 or a base-cell read: %d" % len(hit))
    for kind, name, ni, nt, rd in hit:
        print("  %-6s %-22s imgadd=%d tvalid=%d base_cell_reads=%s"
              % (kind, name, ni, nt, rd or "-"))
    print("fixtures with imgadd>0: %s"
          % [r[1] for r in rows if r[2]])

if __name__ == "__main__":
    main()
