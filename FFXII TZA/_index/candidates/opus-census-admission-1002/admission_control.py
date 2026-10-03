"""admission_control.py - script_verb_census.py's input admission under ASTRA's three fixture cases plus --allow-partial
(OPUS, 2026-10-02; ASTRA-REQ-OPUS-AUTHORED-CENSUS-ADMISSION-1002).

The fake input services are ASTRA's (Tools/work/ASTRA/runtime-residue-method-retriage/authored-census-admission-
frozen-ready/fixture_entry.py): a two-member synthetic archive whose read_entry raises a labelled OSError for the second
member, for both, or for neither, and a one-CALL fake decoder. The COMMITTED collector's real main() runs in a child
process per case. This exercises the collector's admission path only - no real VBF, bytecode or game behaviour.
Last line: 'FAILS n'.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
COLLECTOR = os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts", "script_verb_census.py")

CHILD = r'''
import json, runpy, struct, sys, types
fail_mode, out, extra = sys.argv[1], sys.argv[2], sys.argv[3:]
def blob(verb, name):
    b = bytearray(0x80 + 0xE0); sec = memoryview(b)[0x80:]
    struct.pack_into("<II", sec, 0, 0x8000000B, 0xE0); struct.pack_into("<I", sec, 0x18, 0xA0)
    struct.pack_into("<I", sec, 0x4C, 0x70); struct.pack_into("<I", sec, 0xA0, 1)
    struct.pack_into("<I", sec, 0xA4, 0); struct.pack_into("<I", sec, 0xAC, 0x60)
    sec[0x60:0x63] = bytes([0x58, verb & 255, verb >> 8]); s = name.encode(); sec[0x70:0x70 + len(s)] = s
    return bytes(b)
inputs = {"fixture/a.ebp": blob(0x29A, "fixture_first"), "fixture/b.ebp": blob(0x29B, "fixture_second")}
def read_entry(f, names, blocks, path):
    if fail_mode == "all" or (fail_mode == "second" and path == "fixture/b.ebp"):
        raise OSError("LABELLED synthetic extraction failure")
    return inputs[path]
G = types.ModuleType("gen_req_channel_census")
G.VBF = sys.executable
G.V = types.SimpleNamespace(load_index=lambda f: (dict.fromkeys(inputs), []), read_entry=read_entry)
G.load_verbs = lambda: {0x29A: (2, None, "getspattackskillinfo"), 0x29B: (2, None, "spattackread")}
G.decode = lambda code: ([(0, 0x58, int.from_bytes(code[1:3], "little"))], None)
G.resolve_args = lambda ins, j, need, verbs: ([("synthetic-reference", 1), ("synthetic-reference", 2)], "ok")
G.OPN = {0x58: "CALL"}
sys.modules["gen_req_channel_census"] = G
sys.argv = [COLLECTOR, "--verbs", "0x29A,0x29B", "--out", out] + extra
runpy.run_path(COLLECTOR, run_name="__main__")
'''

fails = 0


def check(ok, msg):
    global fails
    print(("PASS  " if ok else "FAIL  ") + msg)
    fails += 0 if ok else 1


def run(case, fail_mode, extra=()):
    d = tempfile.mkdtemp(prefix="census-adm-%s-" % case)
    out = os.path.join(d, "calls.tsv")
    p = subprocess.run([sys.executable, "-B", "-c", "COLLECTOR = %r\n" % COLLECTOR + CHILD, fail_mode, out] + list(extra),
                       capture_output=True, text=True)
    rows = open(out, encoding="utf-8").read().splitlines()[1:] if os.path.exists(out) else None
    st = json.load(open(out + ".status.json")) if os.path.exists(out + ".status.json") else None
    print("--- %s: rc %d | stdout %r | stderr %r" % (case, p.returncode, p.stdout.strip()[:160], p.stderr.strip()[:200]))
    return p, rows, st


p, rows, st = run("all-readable", "none")
check(p.returncode == 0 and rows is not None and len(rows) == 2, "all readable: exit 0, both 029A and 029B rows")
check(st and st["status"] == "COMPLETE" and st["inputs"]["decoded"] == 2 and not st["not_decoded"],
      "all readable: status COMPLETE, 2 decoded, nothing undecoded")

p, rows, st = run("one-extraction-fails", "second")
check(p.returncode == 1 and rows is None and st is None, "second read fails: REFUSE (exit 1), nothing written")
check("INCOMPLETE" in p.stderr and "fixture/b.ebp" in p.stderr, "second read fails: stderr names INCOMPLETE and the failed path")

p, rows, st = run("one-extraction-fails-allow-partial", "second", ["--allow-partial"])
check(p.returncode == 0 and rows is not None and len(rows) == 1 and "0x29A" in rows[0], "--allow-partial: exit 0, the one real 029A row kept")
check(st and st["status"] == "PARTIAL" and st["inputs"]["read_failed"] == 1
      and st["not_decoded"]["read_failed"][0]["path"] == "fixture/b.ebp", "--allow-partial: status PARTIAL, b.ebp listed as read_failed")
check("PARTIAL" in p.stdout, "--allow-partial: stdout says PARTIAL")

p, rows, st = run("all-extractions-fail", "all")
check(p.returncode == 1 and rows is None and "REFUSE" in p.stderr, "all reads fail: REFUSE (exit 1), nothing written")
print("FAILS %d" % fails)
