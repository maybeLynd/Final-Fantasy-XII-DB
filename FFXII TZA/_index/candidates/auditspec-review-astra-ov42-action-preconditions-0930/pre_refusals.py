"""pre_refusals.py - SWE2-AUDIT-SPEC: feed check-special-admission.py altered COPIES of its inputs (built in a temp
dir outside the repo) and record whether each is refused. The packet's own inputs are never modified."""
import json, os, shutil, subprocess, sys, tempfile
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
PKG = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments", "evidence", "ov42-special-action-preconditions")
CHK = os.path.join(PKG, "check-special-admission.py")
tmp = tempfile.mkdtemp(prefix="ov42pre_")


def run(label, raw, rec, tabdir):
    out = os.path.join(tmp, label + ".json")
    r = subprocess.run([sys.executable, CHK, raw, rec, tabdir, out], capture_output=True, text=True)
    last = (r.stderr.strip().splitlines() or [""])[-1] if r.returncode else r.stdout.strip()
    print("%-34s exit=%d  %s" % (label, r.returncode, last[:150]))


RAW = os.path.join(PKG, "special-admission-raw-01.json")
REC = os.path.join(PKG, "action-selectors-01", "result.json")
TAB = os.path.join(PKG, "action-selectors-01", "tables")
run("baseline_fresh", RAW, REC, TAB)

# 1 one table byte changed (row 511 flags cleared of bit30 in the us table)
t1 = os.path.join(tmp, "tab_flag"); shutil.copytree(TAB, t1)
p = os.path.join(t1, "action_data_us.st2e"); b = bytearray(open(p, "rb").read())
b[32 + 511 * 60 + 12 + 3] &= ~0x40; open(p, "wb").write(b)
run("table_row511_bit30_cleared", RAW, REC, t1)

# 2 one table missing
t2 = os.path.join(tmp, "tab_missing"); shutil.copytree(TAB, t2); os.remove(os.path.join(t2, "action_data_kr.st2e"))
run("table_kr_missing", RAW, REC, t2)

# 3 code witness altered: 3092C5 movzx word -> byte
raw = json.load(open(RAW))
for r in raw["ranges"]:
    for x in r["instructions"]:
        if x["pc"] == "0x3092c5":
            x["args"] = "eax, byte ptr [rbx + 0x24]"
p3 = os.path.join(tmp, "raw_width.json"); json.dump(raw, open(p3, "w"))
run("witness_3092C5_byte_width", p3, REC, TAB)

# 4 bit30 test polarity altered: je -> jne at 30CE9A
raw = json.load(open(RAW))
for r in raw["ranges"]:
    for x in r["instructions"]:
        if x["pc"] == "0x30ce9a":
            x["mnemonic"] = "jne"
p4 = os.path.join(tmp, "raw_polarity.json"); json.dump(raw, open(p4, "w"))
run("witness_30CE9A_polarity", p4, REC, TAB)

# 5 role control failed upstream
raw = json.load(open(RAW)); raw["controls"][0]["observed"] = "r"
p5 = os.path.join(tmp, "raw_role.json"); json.dump(raw, open(p5, "w"))
run("upstream_role_control_failed", p5, REC, TAB)

# 6 wrong image hash claimed
raw = json.load(open(RAW)); raw["exe_sha256"] = "0" * 64
p6 = os.path.join(tmp, "raw_sha.json"); json.dump(raw, open(p6, "w"))
run("raw_claims_other_image", p6, REC, TAB)

# 7 receipt with 8 packs
rec = json.load(open(REC)); rec["results"] = rec["results"][:8]
p7 = os.path.join(tmp, "rec8.json"); json.dump(rec, open(p7, "w"))
run("receipt_8_packs", RAW, p7, TAB)

# 8 BLIND SPOT: capture decodes 3092C5 differently but the pinned text kept (raw bytes altered, text unchanged)
raw = json.load(open(RAW))
for r in raw["ranges"]:
    for x in r["instructions"]:
        if x["pc"] == "0x3092c5":
            x["bytes"] = "0fb64324"  # movzx eax, byte [rbx+0x24]
p8 = os.path.join(tmp, "raw_bytes_only.json"); json.dump(raw, open(p8, "w"))
run("witness_bytes_changed_text_kept", p8, REC, TAB)

# 9 existing output path refused
run("existing_output", RAW, REC, TAB) if False else None
open(os.path.join(tmp, "exists.json"), "w").write("{}")
r = subprocess.run([sys.executable, CHK, RAW, REC, TAB, os.path.join(tmp, "exists.json")], capture_output=True, text=True)
print("%-34s exit=%d  %s" % ("existing_output_path", r.returncode, (r.stderr.strip().splitlines() or [""])[-1][:150]))
shutil.rmtree(tmp)
print("temp dir removed:", not os.path.exists(tmp))
