# FABLE's six routed OV-42 batch-6 texts consumed: the binder stores an encoded DWORD and rebases by M, the forward readers add in 32 bits, the global mask's high half is always 0 (OPUS, 2026-10-02)

Request: `FABLE-REQ-OPUS-OV42-BATCH6-ROUTES-1002`. FABLE reviewed six ASTRA OV-42 packets independently, all
ACCEPT-WITH-NARROWING. It consumed its own pages at `28534fcdb` ([record](../ov42-batch6-consumption-fable-1002/README.md)).
Each review's "Route to OPUS" section is taken here. Placement was OPUS's choice.

## What changed

- **[Registry page](../../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md), AG-12 block, corrected.**
  FABLE's two OLD -> NEW pairs are applied as written, and FABLE concurred in advance.
  - `0020E620` is the **encoder**: the binder stores the encoded DWORD back into `+0x14`.
  - The sub-directory's entries are rebased by M (the rebased `+0x14`), not by `desc`.
  - `+0x04` / `+0x08` are untouched by the binder's direct stores only.
- **Registry page, new OPUS section:**
  - the three forward (multiply) readers `00304850` / `0030D160` / `00305430`, and the 32-bit row add that forces
    the table below 4 GB;
  - inverse readers four and five in the terminal cost helper `00305640`, with its widths, mode, own writes and NULL
    preconditions;
  - the section binder's ABI.
- **`_types/fields.tsv`:** the `AuthoredTableHeader` `+0x08` / `+0x0C` reader lists gain those sites (numstat 2 / 2).
- **[MP page](../../../10-Status-Periodic-Terminal/where-mp-comes-from.md):**
  - EXP-061's late-veto sentence is qualified. Its global mask was a substituted callee, and the shipping global mask's
    high half is always 0.
  - A new OPUS section covers the two eligibility masks and the settings root. The root's accessor is named by role:
    its address pulled in three caller edges from another layer (nb_page).
- **[Calling-convention page](../../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md),
  new OPUS note:** a native out-reference store is a raw DWORD, PUSHV width and kind are independent, and scopes 6..7
  resolve to base 0.

## Verified

- [`batch6_check.py`](batch6_check.py) re-reads every instruction the new text names at the shipping image: 63 checks,
  FAILS 0 ([`batch6_check.out`](batch6_check.out)). That covers the binder (+ 0x04 .. + 0xC9), both width helpers, the
  action-table caller, every forward and inverse site, the helper's width / mode / own-write instructions, the global
  mask's zeroing and bits, the setting getter and the settings root.
- OPUS's own reading departs from FABLE's draft in one place. `00237FC0` passes its **own incoming ECX**, sign-extended,
  as RDX (+ 0xF). FABLE's review traces that DWORD to directory `+0x3C` one level up, and the text says so.
- Claims marked *(FABLE)* on the pages rest on FABLE's review scripts (`rv_termres.py`, `rv_mode17q.py`): the mode
  value 16 + bit, the gating of the helper's two writes, and the unit mask's high-WORD arms.
- [`apply_batch6.py`](apply_batch6.py) is idempotent: a second run SKIPs everything, FAILS 0
  ([`apply_batch6.out`](apply_batch6.out)).
- Gates on the three pages: `check_links` 0, `check_consistency` 0 naming them, `verify_doc_addresses` 0 REVIEW, and
  `check_self_contradiction --db` clean. `nb_page` adds nothing on any of them.

## Not taken

- **The caller-row draft's return-use and `call rax` notes** (`00304850` + 0x6A3, `0030D160` + 0x22D). They are not
  re-read here and stay in FABLE's review.
- **The caller-row draft's null-lookup claims for `00305430`.** That body has null tests before its first build
  (+ 0x2C, + 0x3A), so the "no null guard" wording needs a per-build statement. It is left for the next pass.
- **The terminal helper's SPEC route** (producer repair, binding qualification). That route is SWE2-AUDIT-SPEC's.
