"""FE-4 part 2 page regression (OPUS, 2026-09-27). The battle-stats field map may not state, unstruck:
  P1 that +0x1C3 (u16) / +0x1C5 are unaccounted 'survivors' / 'sentinels' (they are the three u8 selectors, 2.3b);
  P2 that every 2.3b gap is alignment padding / 'no unexplained region' (+0x5C..+0x63 is an 8-byte untouched region, FE-4);
  P3 that +0x5C is private to 00386C70 (FE-3: the result record's +0x5C + 4i);
  P4 a layout line typing +0x5C as a u32 or +0x1C3 as a u16.
A claim inside ~~...~~ counts as struck. FAILS on the page before FE-4 part 2; PASS after. Usage: python fe4_page_check.py [page]"""
import re, sys, pathlib
P = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[3] /
                 "08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md")
s = P.read_text(encoding="utf-8")
live = re.sub(r"~~.*?~~", "", s, flags=re.S)
checks = {
    "P1 survivor sentinels": "Two of the survivors are known from a direct read" not in live,
    "P2 every gap pads": "There is no unexplained region" not in live and "every one of them\nsitting exactly where a compiler pads" not in live.replace("\r\n", "\n"),
    "P3 +0x5C private": "is private to `BattleFormula_AdvanceStatusTimersAndBuildResult`" not in live,
    "P4 layout types": "+0x5C u32 (timer builder)" not in live and "+0x1C3 u16, +0x1C5 u8 sentinels" not in live,
}
fails = 0
for k, ok in checks.items():
    print("PASS" if ok else "FAIL", k); fails += not ok
print("FAILS", fails); sys.exit(1 if fails else 0)
