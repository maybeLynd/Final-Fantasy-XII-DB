# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-BATCH3-PASSES · SWE2-AUDIT-SEM 2026-09-29

Passes: `abc1a9b94`, `e31d421b6`, `fb29f8885`, `e7d2e1eda` — ten contracts.
All ten regressions re-run non-author: enmity / weapon_recipes /
element_scaling / system_stop / env_variant / trigger_points /
actor_storage_init / native_lifecycle / world_tick / workbench — FAILS 0.
Image `73461D08…21F8`.

## Named attacks — all fail

**CON-168 ordering** — my own disasm: `002665EB mov word[rbx],r10w` is
preceded by record stores `and byte[rbx+0x14],0x7f` (266573),
`mov qword[rbx+0xEC],r13` (26657A), `mov byte[rbx+0xF5],0xFF` (266581),
`mov byte[rbx+0x14]` (2665D7), `mov word[rbx+0xF6]` (2665E0) and the calls
`00266AD0` (2665A9), `00266BD0` (2665B1). Six stores + two calls before the
index write — it is not the first field written.

**Env-variant fifth global** — V5 reproduces `002EF2B0()` = `02164480`
= `02164280 + 0x200`; the register writes `+0x1060`/`+0x1061` land at
`021654E0`/`021654E1` — the selector global is exactly `021654E0`.

**TP-7 draw-and-set** — P6 confirms exactly two bodies (`002F8060`,
`002FAFD0`) both draw and set among 7 setters.

**TW-4 census — reproduced exactly** under my own per-body instrument:
267 functions touch `022D8F00`–`022D9500` rip-relative; 249 write; 18
read-only. Numbers match 267/249/18 verbatim.

## Verdict

**ACCEPT** all four passes and the CON-168 correction.
