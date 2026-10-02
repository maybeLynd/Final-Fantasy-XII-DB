"""ov33_incorp.py - narrow the OV-33 register cell with ASTRA's ov33-e2-six-cache-keys (ACCEPTed by SWE2-AUDIT-SPEC)
(OPUS, 2026-10-01; ASTRA-RETURN-OPUS-OV33-E2-SIX-CACHE-KEYS-0930). Byte-preserving, idempotent; PATCHED / ALREADY, FAILS n."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "..", "..", "OPEN-QUESTIONS.md")
NOTE = (" *(Narrowed 2026-10-01, OPUS, on ASTRA's ov33-e2-six-cache-keys, ACCEPTed by SWE2-AUDIT-SPEC "
        "(_index/candidates/auditspec-review-ov33-cache-keys-1001/REVIEW.md): the six retained FST-sized archive-missing "
        "kind-1 paths (US 129/130/131, UK 131/132, CN 127, both edx modes) hash under 00674A00 to keys that collide with none "
        "of the 89,414 shipped archive-name keys. So, with the unchanged ASCII normalisation and an archive-name-only "
        "FileCache population, none of them passes the cache-membership gate, whatever the map-jump timing: E2 cannot occur "
        "for those six. Still OPEN: alternate inserts and indirect writers into the FileCache map, locale, cache "
        "initialisation and lifetime, and the raw kind 0xFF paths. No OV row closes.)*")
fails = 0
b = open(REG, "rb").read()
lines = b.split(b"\n")
idx = [i for i, l in enumerate(lines) if l.startswith(b"| OV-33 ")]
n = NOTE.encode("utf-8")
if len(idx) != 1:
    print("REFUSING: OV-33 rows x%d" % len(idx)); fails += 1
elif n in lines[idx[0]]:
    print("ALREADY OV-33")
elif b"|" in n:
    print("REFUSING: pipe in note"); fails += 1
else:
    row = lines[idx[0]]
    cr = row.endswith(b"\r")
    body = row[:-1] if cr else row
    k = body.rfind(b" |")
    if k < 0 or body[k:].strip() != b"|":
        print("REFUSING: row does not end with a cell delimiter"); fails += 1
    else:
        lines[idx[0]] = body[:k] + n + b" |" + (b"\r" if cr else b"")
        open(REG, "wb").write(b"\n".join(lines))
        print("PATCHED OV-33")
print("FAILS", fails)
sys.exit(1 if fails else 0)
