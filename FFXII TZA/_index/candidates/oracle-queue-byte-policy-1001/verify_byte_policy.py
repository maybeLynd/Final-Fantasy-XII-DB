"""Re-run the ORACLE byte-policy control for
ASTRA-REQ-ORACLE-QUEUE-BYTE-POLICY-0930. Ends 'FAILS 0'.

Checks, against the live tree:
1. leaf .gitattributes carries '-text' coverage for every packet
   member (git check-attr text -> unset).
2. git hash-object filtered == --no-filters for every member still
   inside the leaf (the helper's own guard, ~line 496).
3. sha256(worktree) == reviewed-sha256.json for every in-leaf
   member (exact frozen bytes, no normalized fake raw).
4. The moved member _index/_inbox/ASTRA.md retains its reviewed
   preimage at
   Database/Tools/work/ASTRA/runtime-residue-method-retriage/
   publication-title-queue-consumption-01/astra-pre-restoration-01.txt
   (sha256 5aa02126...) and that the live file has indeed moved.
"""
import hashlib, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
PUB = ROOT / "Database/Tools/work/ASTRA/runtime-residue-method-retriage/publication-title-queue-consumption-01"
LEAF = ROOT / "Database/FFXII TZA/_experiments/evidence/title-queue-consumption"
ASTRA_MD = "Database/FFXII TZA/_index/_inbox/ASTRA.md"

fails = []
def ck(cond, label):
    if not cond:
        fails.append(label)
        print("FAIL", label)

paths = json.loads((PUB / "paths.json").read_text())
expected = json.loads((PUB / "reviewed-sha256.json").read_text())

# 1. attribute coverage
out = subprocess.run(["git", "check-attr", "text", "--"] + paths,
                     cwd=ROOT, capture_output=True, text=True).stdout
for line in out.splitlines():
    path, _, val = line.partition(": text:")
    if path.strip() == ASTRA_MD:
        continue  # moved member, outside the leaf — checked separately
    ck(val.strip() == "unset", f"text not unset: {path.strip()}")

# 2. filtered == unfiltered on in-leaf members
inleaf = [p for p in paths if p != ASTRA_MD]
data = ("\n".join(inleaf) + "\n").encode()
norm = subprocess.run(["git", "hash-object", "--stdin-paths"], cwd=ROOT,
                      input=data, capture_output=True).stdout.splitlines()
unf = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"],
                     cwd=ROOT, input=data, capture_output=True).stdout.splitlines()
ck(len(norm) == len(inleaf), "hash-object count")
for i, p in enumerate(inleaf):
    ck(norm[i] == unf[i], f"filter divergence: {p}")

# 3. sha256 preimage pins (in-leaf members unchanged since review)
for p in inleaf:
    got = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
    ck(got == expected[p], f"sha256 moved: {p}")

# 4. moved member: reviewed preimage retained; live file moved
pre = PUB / "astra-pre-restoration-01.txt"
ck(pre.is_file(), "retained preimage missing")
ck(hashlib.sha256(pre.read_bytes()).hexdigest() == expected[ASTRA_MD],
   "retained preimage != reviewed sha256")
ck(hashlib.sha256((ROOT / ASTRA_MD).read_bytes()).hexdigest() != expected[ASTRA_MD],
   "live ASTRA.md unexpectedly matches reviewed sha256")

print(f"members: {len(paths)}, in-leaf: {len(inleaf)}, FAILS {len(fails)}")
sys.exit(1 if fails else 0)
