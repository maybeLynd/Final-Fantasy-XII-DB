"""fix_uc1_entries.py - apply SWE2-AUDIT-SPEC's 15 entry-statement replacements (review
auditspec-review-opus-referenced-code-the-list-never-had-uc1-1002) to the UC-1 record's rows.json (OPUS, 2026-10-03).
Idempotent: a row already carrying its replacement is left alone."""
import io
import json
import os

D = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\opus-referenced-code-the-list-never-had-uc1-1002"
OLD = "no direct reference was found (call/jump, rip-reference and table scans)"
NEW = {
    "00195340": "entered through the 32-bit image-relative destructor field at `01DEAAA4` of the C++ throw-info record for `std::bad_cast` at `01DEAAA0`",
    "002969D0": "entered by a conditional jump (`jne`) from `002905B0` + 0x13",
    "002E4C90": "entered by a conditional jump (`je`) from `002673D0` + 0xD",
    "002E5B00": "entered by a conditional jump (`je`) from `0026A420` + 0x8",
    "002ED250": "entered by a conditional jump (`jge`) from `003EB8C0` + 0xC",
    "002ED350": "entered by a conditional jump (`jge`) from `003EB960` + 0xC",
    "0031AD90": "entered by a conditional jump (`jne`) from `00359B80` + 0xC",
    "00365660": "entered by a conditional jump (`jg`) from `0029CCF0` + 0x5",
    "00379F50": "entered by a conditional jump (`jne`) from `00379860` + 0x8",
    "0037AA00": "entered by a conditional jump (`jne`) from `003DEA10` + 0x2",
    "003DCF20": "entered by a conditional jump (`je`) from `003DC780` + 0x43",
    "003F5030": "entered by a conditional jump (`jne`) from `00290BE0` + 0x16",
    "003F7000": "entered by a conditional jump (`jne`) from `00290940` + 0x13",
    "004278D0": "entered by a conditional jump (`jne`) from `002EB4A0` + 0x3A",
    "0042FCC0": "entered by a conditional jump (`ja`) from `00317EC0` + 0x6",
}
p = os.path.join(D, "rows.json")
d = json.load(io.open(p, encoding="utf-8"))
n = 0
for r in d["rows"]:
    if r["fn"] in NEW and r["text"].startswith(OLD):
        r["text"] = NEW[r["fn"]] + r["text"][len(OLD):]
        n += 1
if n:
    d.setdefault("corrections", []).append({
        "fn": ", ".join(sorted(NEW)),
        "why": "SWE2-AUDIT-SPEC REJECT (auditspec-review-opus-referenced-code-the-list-never-had-uc1-1002): the first census "
               "missed 0F 8x conditional jumps and 32-bit image-relative fields, so these 15 rows said no direct reference "
               "was found; entry statements replaced with SPEC's verified sites; uc1_entry_check.py is the regression"})
    json.dump(d, io.open(p, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print("replaced", n)
