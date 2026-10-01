"""rc30_census.py - RC-30: can any request or path lookup name kind 7 ids 0xE2..0xE4 (Loca_gil / Loca_bhm / Loca_rbl
.cl2)? ORACLE, 2026-09-30. Static. An independent census of EVERY call site of the resource request and path APIs, with
the (kind, id) arguments resolved by OPUS's value-set dataflow (../rc9-log-channels-0930/rc9_channels.py: per-function
forward dataflow over the function's own control flow, entry-register values resolved through every caller from
edges.tsv, recursively to depth 4).

APIs (kind register, id register):
  ecx, edx : ResourcePath_Get 002DF980, ResourcePath_Copy 002DF880, 0032E400 (size), 0032E620 (request), 0024AB90
  edx, r8  : the pool front ends 00249180, 00249210, 002493D0, 00249350, 00249320, 00249380 (each passes edx/r8
             unchanged to 00249210, which hands them to 0032E400 / 0032E620 as ecx/edx)
Call sites inside the API set itself are pass-through and are skipped (their callers are enumerated directly).

Per site: kind = the resolved set of the kind register; id = the resolved set of the id register.
  EXCLUDED  kind resolved and 7 not in it
  CONST7    kind = {7} and id resolved: listed only if it hits 0xE2..0xE4
  OPEN      kind or id unresolved where kind may be 7: listed with the dataflow's note, for hand bounding in the README
Controls:
  K1  the Loca.mrp request 00404107 (in 00404060) resolves to kind 7, id 0xBF;
  K2  the item_gra loop 00291D04 (in 00291C80) resolves to kind 7 (the loop-carried id 0x98..0xA1 exceeds the
      dataflow and is left OPEN, which is what an honest dataflow must do);
  K3  00365810's request 003658C7 resolves to kind 7, ids {130..135, 218..223} through its table? - no: it is an
      indexed load, so it must come out OPEN or as that set; it must not come out EXCLUDED.
Output: rc30_census.tsv (every site) and a summary.
"""
import collections, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import rc9_channels as V  # noqa: E402

API_C = {0x002DF980: ("rcx", "rdx"), 0x002DF880: ("rcx", "rdx"), 0x0032E400: ("rcx", "rdx"), 0x0032E620: ("rcx", "rdx"),
         0x0024AB90: ("rcx", "rdx")}
API_P = {a: ("rdx", "r8") for a in (0x00249180, 0x00249210, 0x002493D0, 0x00249350, 0x00249320, 0x00249380)}
API = {**API_C, **API_P}
LOCA = {0xE2, 0xE3, 0xE4}


def rset(f, st, reg):
    v = st.get(reg, V.UNK)
    v = V.trunc32(v) if v is not V.UNK else V.UNK
    return V.resolve(f, v)


rows = []
for g, (kr, ir) in sorted(API.items()):
    for f in sorted(V.CALLERS.get(g, ())):
        if f in API:
            continue
        try:
            st, _ = V.analyse_keep(f)
            sites = V.call_sites_to(f, g)
        except Exception as e:  # noqa: BLE001
            rows.append((g, f, 0, "ERROR", str(e)[:80], "", ""))
            continue
        if not sites:
            rows.append((g, f, 0, "NOSITE", "edges.tsv edge with no decoded site on the entry's control flow", "", ""))
        for s in sites:
            if s not in st:
                rows.append((g, f, s, "UNREACHED", "", "", ""))
                continue
            kv, kn = rset(f, st[s], kr)
            if kv is not None and 7 not in kv:
                rows.append((g, f, s, "EXCLUDED", "", ",".join("%d" % k for k in sorted(kv)), ""))
                continue
            iv, inn = rset(f, st[s], ir)
            if kv == {7} and iv is not None:
                cls = "CONST7-LOCA" if iv & LOCA else "CONST7"
                rows.append((g, f, s, cls, "", "7", ",".join("0x%X" % i for i in sorted(iv))[:300]))
                continue
            note = "; ".join(sorted(set((kn or []) + (inn or []))))[:200]
            rows.append((g, f, s, "OPEN", note, "?" if kv is None else ",".join("%d" % k for k in sorted(kv)),
                         "?" if iv is None else ",".join("0x%X" % i for i in sorted(iv))[:300]))

with io.open(os.path.join(HERE, "rc30_census.tsv"), "w", encoding="utf-8", newline="\n") as o:
    o.write("api\tfunction\tsite\tclass\tnote\tkind\tid\n")
    for r in rows:
        o.write("%08X\t%08X\t%08X\t%s\t%s\t%s\t%s\n" % r)

cnt = collections.Counter(r[3] for r in rows)
print("sites by class: %s" % dict(cnt))
fails = 0


def find(site):
    return [r for r in rows if r[2] == site]


k1 = find(0x00404107)
k2 = find(0x00291D04)
k3 = find(0x003658C7)
ok1 = bool(k1) and k1[0][3] == "CONST7" and k1[0][6] == "0xBF"
ok2 = bool(k2) and k2[0][5] == "7"
ok3 = bool(k3) and k3[0][3] != "EXCLUDED"
for ok, nm in ((ok1, "K1 00404107 -> kind 7, id 0xBF %r" % (k1,)), (ok2, "K2 00291D04 -> kind 7 (its loop-carried id is left to the hand bound) %r" % (k2[0][3:] if k2 else k2,)),
               (ok3, "K3 003658C7 is not excluded %r" % (k3[0][3:6] if k3 else k3,))):
    print("%s  %s" % ("PASS" if ok else "FAIL", nm))
    fails += not ok
print("\nsites that resolve to a loca_*.cl2 id (kind 7, id 0xE2..0xE4): %d" % cnt.get("CONST7-LOCA", 0))
for r in rows:
    if r[3] == "CONST7-LOCA":
        print("  %08X in %08X via %08X ids %s" % (r[2], r[1], r[0], r[6]))
print("\nOPEN sites (kind may be 7 and kind or id not resolved): %d" % cnt.get("OPEN", 0))
for r in rows:
    if r[3] == "OPEN":
        print("  %08X in %08X via %08X kind=%s id=%s  %s" % (r[2], r[1], r[0], r[5], r[6][:60], r[4][:150]))
print("\nUNREACHED / NOSITE / ERROR:")
for r in rows:
    if r[3] in ("UNREACHED", "NOSITE", "ERROR"):
        print("  %s %08X in %08X via %08X %s" % (r[3], r[2], r[1], r[0], r[4]))
print("\nFAILS %d" % fails)
sys.exit(1 if fails else 0)
