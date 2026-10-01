"""Affected actual reader refusals; retain the existing positive without rerun."""
import hashlib
import importlib.util
import json
import pathlib
import sys

W = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("checked_delivery", W / "prepare-residue-packet-publication.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
out = W / "title-cleanup-count-selector-controls-01"
out.mkdir()
positive = json.loads((W / "title-cleanup-count-selector-result-01.json").read_text())
if positive.get("producer_complete") is not True or len(positive["normal_cfgs"]) != 2:
    raise ValueError("existing positive incomplete/zero")
checks = []
for name in ["first-return-only", "wrong-selected-offset", "wrong-root-metadata"]:
    case = out / name
    case.mkdir()
    source = json.loads((W / "title-cleanup-count-selector-source-01.json").read_text())
    if name == "first-return-only":
        q = next(q for q in source["ranges"] if q["start"] == "0x623df0")
        q["instructions"] = [i for i in q["instructions"] if int(i["pc"], 16) < 0x623E0E]
        q["end_exclusive"] = "0x623e0e"
        q["sha256"] = hashlib.sha256(bytes.fromhex("".join(i["bytes"] for i in q["instructions"]))).hexdigest()
    elif name == "wrong-selected-offset":
        q = next(q for q in source["ranges"] if q["start"] == "0x623df0")
        i = next(i for i in q["instructions"] if i["pc"] == "0x623e06")
        i["args"] = "rax, 0x30"
    else:
        source["pdata_entry"][2] += 4
    with (case / "title-cleanup-count-selector-source-01.json").open("x") as f:
        json.dump(source, f, indent=2)
    target = case / "must-not-exist.json"
    error = None
    try:
        M.checked_run([sys.executable, str(W / "prove-title-cleanup-count-selector.py"),
                       str(target), str(case)], timeout=45, receipt_prefix=case / "actual-cli")
    except RuntimeError as e:
        error = str(e)
    if error is None or target.exists():
        raise ValueError("failed prerequisite accepted " + name)
    checks.append(dict(case=name, status="PASS_REFUSED_NO_RESULT", labelled_synthetic=True, error=error))
with (out / "result.json").open("x") as f:
    json.dump(dict(status="PASS_AFFECTED_PRODUCER_CONTROLS_INDEPENDENT_PENDING", checks=checks,
                   positive_sha256=hashlib.sha256((W / "title-cleanup-count-selector-result-01.json").read_bytes()).hexdigest(),
                   driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                   limits="Three actual prerequisite refusals; existing positive reused. No native/live, semantic independent acceptance or natural zero-count claim"), f, indent=2)
print("Missing second return branch, false field offset and wrong root metadata refused; positive reused")
