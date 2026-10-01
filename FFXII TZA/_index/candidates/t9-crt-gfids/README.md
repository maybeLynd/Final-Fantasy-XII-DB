# T-9: the twelve `.gfids` dwords are the static CRT's own `.gfids$y` symbol indices (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (T-9):** what the 12 nonzero `.gfids` dwords (10–113) actually are.

Already established:
- they are one `.gfids$y` input contribution passed through unconverted (the image's POGO record, 2026-09-26);
- resolving them needs the contributing objects' symbol tables, which the image does not carry.

OPUS's lost-build review declined NAS: the source is the public VS2015 Update 3 static runtime. With the user's
approval, the MSVC v140 toolset was installed on 2026-09-27 and the test was run.

## Result (`t9_crt_gfids.py`, output `t9_crt_gfids.out`, FAILS 0)

The image reads **49 48 19 10 13 16 69 113 10 98 55 11**. For each position, the table gives the x64 static release
runtime objects whose *whole* `.gfids$y` run equals the value(s) there, and the function each index names in that
object's own symbol table:

| pos | value | object (library) | function indexed |
|---:|---:|---|---|
| 2 | 19 | `std_type_info_static.obj` (libcmt) | `type_info`'s vector deleting destructor (`??_Etype_info`) |
| 3 | 10 | `winapisupp.obj` (libcpmt) | `initialize_pointers` |
| 4 | 13 | `jbcxrval.obj` (libvcruntime) | `_guard_check_icall_nop` |
| **6–7** | **69, 113** | **`exe_winmain.obj` (libcmt)**, a two-value run in place | `_matherr`, `_RTC_Terminate` |
| 8 | 10 | an object with a `[10]` run (`winapisupp` also fits, or another) | as above |
| 9 | 98 | `thread_safe_statics.obj` (libcmt) | `__scrt_uninitialize_thread_safe_statics` |
| 10 | 55 | `utility_desktop.obj` (libcmt) | `__scrt_unhandled_exception_filter` |
| 11 | 11 | `guard_support.obj` / `lconv_unsigned_char.obj` (libcmt) | `_guard_check_icall_nop` / `__initialize_lconv_for_unsigned_char` |

**The chance control (C4).**
- The real twelve match **8 positions**, one of them by a multi-value run.
- Of 2,000 random twelves drawn from the same range 10–113, **0.0%** match as many positions, and **0.65%** match any
  multi-value run.
- So the fit is not coincidence. The twelve are the `.gfids$y` data of the game's **statically linked C/C++ runtime**.
  This agrees with the VC_FEATURE record: 49 guard-aware objects, and the game's own code was not compiled with
  `/guard:cf`.

**The three positions not matched here, with the reason:**
- **0–1 (49, 48).** The installed SDK's UCRT `initialization.obj` run contains 49, 48 consecutively. That is inside a
  25-value run from a much later UCRT (10.0.26100); the VS2015-era UCRT (10.0.10240–14393) is not installable here.
- **5 (16).** `tlsdyn.obj` (libcmt, `__dyn_tls_init`) runs `[16, 16]` in the installed build.
- **The installed v140 runtime is build 24237**, a later Update 3 servicing build. The image's prebuilt runtime objects
  are 24123 / 24210 / 23026 (Rich header), so individual runs can differ by a build.

**Amendment, same day.** The v140 install also brought the Windows 10 SDK 10.0.10240 UCRT. Its `libucrt.lib` carries **no `.gfids$y` at all**, so the UCRT reading of positions 0–1 would need a later SDK (10.0.10586 or 14393), or those two values come from another guard-aware object. The VC_FEATURE record's 49 guard-aware objects leave room for that. The eight named positions and the chance control are unaffected.

## Limits

- The identification is by whole-run match against a neighbouring build, controlled for chance. It is not a byte
  reproduction of the link.
- The exact 24210 static libraries and the 10.0.10240/14393 UCRT would settle the three inferred positions and the
  link order. Both are public downloads outside the Visual Studio installer.

## Files

- `t9_crt_gfids.py` and `t9_crt_gfids.out`.
  *Invocation (added 2026-09-27, FABLE, Claude Opus 5.5; the script needs both arguments):* `python t9_crt_gfids.py "<VS 14.0>/VC/lib/amd64" "<Windows Kits>/10/Lib"`.
  Re-run 2026-09-27 at HEAD `3d95e439c`: output identical to `t9_crt_gfids.out`, FAILS 0.
- `consumer-check.md`.
