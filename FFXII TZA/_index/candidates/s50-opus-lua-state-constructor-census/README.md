# S-50 DA-1, bounded statically: the shipping image cannot create a `lua_State` (OPUS, 2026-09-26)

**Evidence class: STATIC (a census over the SHA-asserted image), with positive controls. Domain: this image only.**

**The question.** `CONTRACT-lua-chunk-loader.md` §13 says that what would fill `DA-1` is first *"whether a `lua_State`
exists at all in a running game"*. The S-50 replay (`../s50-opus-replay-lua-loader/`) records that *"no `lua_State`
constructor has been located"*.

**How the question can be answered statically.** In Lua 5.2, a state is created only by `lua_newstate`, whose protected
body `f_luaopen` does four things that leave markers in code:
- `luaT_init` (`ltm.c`) interns the tag-method names from `luaT_eventname`;
- `luaX_init` (`llex.c`) interns the reserved words from `luaX_tokens`;
- `lstate.c` stores the literal `MEMERRMSG`, `"not enough memory"`;
- `luaL_newstate` (`lauxlib.c`) wraps `lua_newstate` and installs a panic function whose message is
  `"PANIC: unprotected error in call to Lua API (%s)"`.

`census.py` searches the whole `.text` for each marker's reference, in both reference forms:
- a rip-relative displacement;
- the image-base form that `luaX_token2str` uses (`lea rax, [rip → 00120000]`, then `[rax + disp]`).

It also searches every qword in the image, which catches pointer tables.

**8 / 8 pass; `result.json` is byte-identical over two runs (md5 `6783059d…`).**

| case | expected | observed |
|---|---|---|
| `M1_no_MEMERRMSG_literal` | absent | `"not enough memory"` does not occur in the image |
| `M2_no_luaL_newstate_panic_message` | absent | the panic message does not occur |
| `M3_tag_method_names_never_interned` | absent | the name table (`01CCBA90`) and the `"__newindex"` string have **no code reference**; the table is referenced only as data |
| `M4_reserved_words_read_only_by_token2str` | absent | `luaX_tokens` (`01CCBBE0`) is read by **`00824340` only**: that is `luaX_token2str`, the error-message path, not `luaX_init` |
| `P1_ldo_messages_referenced` | present | `"C stack overflow"` (`0081D900`, `0081E5A0`) and `"error in error handling"` (`0081E760`): `ldo.c` is linked |
| `P2_luaX_setinput_references_ENV` | present | `"_ENV"` is referenced by `008242A0` (`luaX_setinput`) and `0081CF80`: `llex.c` is linked |
| `P3_image_base_form_detected_via_token2str` | present | the second reference form is detected (`00824340`), so M3 and M4 are not blind to it |
| `P4_lauxlib_linked` | present | `"_LOADED"` is referenced (`008286D0`, `00828D30`): `lauxlib.c` is linked, so M2's absence is `luaL_newstate`'s alone |

**Reading.** The parser, the undump, `ldo.c` and `lauxlib.c` are linked; the constructor is not. The markers are
independent of inlining: an inlined `luaT_init` or `luaX_init` would still reference the table or its strings. So
**no code in this image can create a `lua_State`**, and `00683C30` can be entered with a live state only if a state
built **outside the image** is handed in.

**What this does not settle.**
- Whether another module does that in a shipped or modded process: a mod loader DLL, for example.
- What the three callers of `00683C30` (`00684D10`, `00684F60`, `00686280`) read the state from. That is `EB-1`.
- It is a census of this image, and a negative census applies only to the measured domain.
