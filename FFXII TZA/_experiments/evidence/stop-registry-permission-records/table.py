rows = [l.rstrip("\n").split("\t") for l in open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "records.tsv"))][1:]
CAT = ["F", "P", "T0", "T127", "T3", "R", "H"]
ORDER = [0, 1, 4, 3, 2, 5, 6]   # print order: focus, party, types 1/2/7, type 3, other types, request actor, handles
def stopped(q, base):
    s = [CAT[c] for c in ORDER if ((q >> (base + c)) & 1) == 0]
    return "all" if len(s) == 7 else (" ".join(s) if s else "—")
def s3(A):
    s = [CAT[c] for c in ORDER if not (((A >> 28) & 1) and ((A >> (8 + c)) & 1))]
    return "all" if len(s) == 7 else (" ".join(s) if s else "—")
GL = [("A", 24, 1), ("B", 24, 1), ("A", 25, 3), ("B", 25, 3), ("A", 29, 1), ("A", 30, 1), ("B", 32, 1), ("B", 33, 1), ("B", 35, 1), ("A", 36, 2), ("B", 36, 2), ("A", 39, 1), ("B", 40, 5)]
def cleared(A, B):
    out = []
    for rec, lo, n in GL:
        q = A if rec == "A" else B
        bits = [lo + i for i in range(n) if ((q >> (lo + i)) & 1) == 0]
        if bits:
            out.append(rec + ",".join(str(b) for b in bits))
    return " ".join(out) if out else "—"
WHO = {0: "UI requests 1/4/20", 1: "*no start site*", 2: "UI requests 3/24", 3: "*no start site*", 4: "field hold mode 1; boot",
       5: "field hold mode 0", 6: "event script takes actor; `talkfadeout`", 7: "field hold mode 2", 8: "*no start site*", 9: "*no start site*",
       10: "`settimestopmagic`; target cursor", 11: "`seteventtimestop`", 12: "`settutorial00timestop`", 13: "full-screen menus",
       14: "*no start site*", 15: "`002E2240`", 16: "mask verbs", 17: "`ucon`", 18: "`0025C830`", 19: "definition load", 20: "*no start site*",
       21: "*no start site*", 22: "`0035C7B0` (game-over route)", 23: "`…dispdenystatus`", 24: "`…ctrldenystatus`", 25: "`…dispdenystatus_by_menu`",
       26: "`…ctrldenystatus_by_menu`", 27: "`skipexec`"}
print("| id | raised by | flag | A `+0` | B `+0` | 1 movement | 2 script | 3 | 4 | 5 animation | 6 unit `+0x004` b5 | 7 unit flag b36 | managers | global bits cleared |")
print("|---:|---|:-:|---|---|---|---|---|---|---|---|---|:-:|---|")
for idv in range(28):
    rs = [r for r in rows if int(r[0]) == idv and r[2] == "0"]
    variants = {}
    for r in rs:
        variants.setdefault((r[3], r[5]), []).append(r[1])
    for (a, b), flags in variants.items():
        A = int(a, 16); B = int(b, 16)
        fl = "any" if len(variants) == 1 else flags[0]
        mgr = "1" if (A >> 31) & 1 else "3"
        print(f"| {idv} | {WHO[idv]} | {fl} | `{a}` | `{b}` | {stopped(A,0)} | {stopped(A,8)} | {s3(A)} | {stopped(B,0)} | {stopped(B,8)} | {stopped(A,16)} | {stopped(B,16)} | {mgr} | {cleared(A,B)} |")
