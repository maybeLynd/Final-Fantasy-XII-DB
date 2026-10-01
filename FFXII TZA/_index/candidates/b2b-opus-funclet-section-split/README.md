# B-2/b: group D against `atexit` thunks, told apart by the image's own section record (OPUS, 2026-09-26)

**Evidence class: STATIC. `live_game: false`.**

**The question.** The funclet page's group D is 128 unwind funclets whose bodies look exactly like an `atexit`
destructor thunk: `lea rcx,[rip+global]; …; jmp dtor`. Their funclet identity rested on two things:
- tier 8: nothing takes their address;
- the table parse.

B-2/b asked whether they could be separated by body evidence alone.

**6 / 6 pass. `run_output.txt` and `result.json` are byte-identical over two runs (md5 `0acba738fdc0e89678734e0064e3aa65`).**

| case | observed |
|---|---|
| `S1` | The image's POGO debug record (type 13, `GCTL`) names its section contributions. **`.text$x` is `00896280`–`008A6970`**, MSVC's EH-funclet contribution. **`.text$yd` is `008A6970`–`008C1635`**, its dynamic-`atexit`-destructor contribution. |
| `S2` | All **4,518** FuncInfo records pass the magic check. For both `__CxxFrameHandler3` and `__GSHandlerCheck_EH`, the handler data leads with the FuncInfo RVA. Their unwind actions and catch handlers declare **3,892** funclet addresses. **3,891 are in `.text$x`.** The one outside, `00861EAE`, is not a body: it is the `jmp [__std_terminate]` import thunk used directly as an unwind action. |
| `S3` | Group D is rebuilt by the page's own rule: a declared funclet that does not use RDX as the frame (A), does not tail-jump to `_Init_thread_abort` (B), and does not reach `__std_terminate` (C). It comes to **128, every one in `.text$x`**, in three shapes: 75 `lea; jmp`, 34 `lea; add rcx,N; jmp`, and 19 `lea; add rcx,8; jmp`. |
| `S4` | `atexit` registrations are `lea rcx,[rip+F]` right before a call or jmp to `00808B90`. They register **1,569** functions: **1,567 in `.text$yd`, none in `.text$x`**, and 2 in the CRT itself (`00809244`, `00809CD4`). The page's controls `008A81D0` and `008A9240` are among them. |
| `S5` | **By body alone, no, for 75 of the 128.** **1,144** registered `.text$yd` thunks have exactly the `lea rcx,[rip+N]; jmp N` shape. The 53 `add rcx` variants have no registered twin in this image. |
| `S6` | `.text$x` holds only funclets. Its 425 `.pdata` starts are 418 declared funclets and 7 RDX-frame bodies (`mov rbp, rdx`, the SEH scope-table handlers). None of them is registered with `atexit`. |

**Answer.** Body evidence alone cannot separate the whole group: 75 of the 128 are byte-shape twins of 1,144 real
`atexit` thunks. The separation no longer rests on the absence of references, though. The linker's own contribution
record, shipped in the image, puts all 128 inside the EH-funclet contribution `.text$x`, which holds nothing but
funclets. It puts every registered `atexit` thunk in `.text$yd`. That is a positive, image-stated classification: a
property of where each body was emitted, not of who references it.

**Run:** `python check.py` (under a minute). It needs `Tools/work/exe/FFXII_TZA.exe`.
