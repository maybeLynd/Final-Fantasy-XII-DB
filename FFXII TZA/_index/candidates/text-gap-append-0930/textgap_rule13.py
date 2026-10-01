"""Hand verdicts (OPUS, 2026-09-30) for the 13 appended text-gap rows the verifier still listed as pending.
Edits only rows appended below the 2026-09-30 APPENDED marker; earlier rows are untouched. Idempotent."""
import io
REG = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\text-gap-citations-250.tsv"
RUN = ("interior point of the unlisted SIMD run 0012B980..00133B40, which carries no .pdata entry at all "
       "(checked 2026-09-30 against the image's 35,713 RUNTIME_FUNCTION ranges: the nearest ends at 0012573F); "
       "admission of that run as bodies is UC-1's question, like the rows under 0012A290")
V = {
    "0013344C": ("UNCONFIRMED", RUN), "0012FBF8": ("UNCONFIRMED", RUN), "001309A4": ("UNCONFIRMED", RUN),
    "0012D9D8": ("UNCONFIRMED", RUN), "0012DA1C": ("UNCONFIRMED", RUN), "00131B50": ("UNCONFIRMED", RUN + "; the unlisted-code page holds it as a continuation candidate (rule L)"),
    "00129640": ("UNLISTED", "a body start: the previous body ends `pop rbp; ret` at 00129635/36, and 00129640 opens `push rbp; mov rbp,rsp` and spills rcx/rdx/r8/r9 to [rbp+0x10..0x28] - a full frame prologue; no .pdata covers it (unwind-less run)"),
    "00808ED9": ("UNCONFIRMED", "interior of 00808D78's real extent: the .pdata entry 00808D78..00808EE4 covers it, and the listed body is cut short before it (the-bodies-the-list-cuts-short.md); the instruction is the epilogue `mov rbx,[rsp+0x40]` - a code address, not data"),
    "00121E11": ("UNCONFIRMED", "the last byte of 00121DB0's .pdata extent 00121DB0..00121E12 (cited as the body's end); interior of a real function, not data"),
    "0015AE4A": ("UNCONFIRMED", "interior of 0015AC50's .pdata extent 0015AC50..0015AE52 - its epilogue `pop r14 ... ret`; the listed body is cut short before it"),
    "0036F22E": ("UNCONFIRMED", "the start of a separate .pdata fragment 0036F22E..0036F23B (a chained unwind fragment of the body 0036F0F0 lists); code, not data"),
    "00148F41": ("UNCONFIRMED", "the recorded end of the listed body 00148F10, which the list cuts short (the-bodies-the-list-cuts-short.md): an alignment `nop dword [rax]` at the cut, in the unwind-less run; code, not data"),
    "001491CE": ("UNCONFIRMED", "the recorded end of the listed body 001491A0, which the list cuts short (the-bodies-the-list-cuts-short.md): an alignment `nop` at the cut, in the unwind-less run; code, not data"),
}
lines = io.open(REG, encoding="utf-8", newline="").read().split("\n")
marker = next(i for i, l in enumerate(lines) if l.startswith("# APPENDED 2026-09-30 (OPUS)"))
n = 0
for i in range(marker + 1, len(lines)):
    c = lines[i].rstrip("\r").split("\t")
    if len(c) >= 10 and c[0] in V and c[8] in ("UNCONFIRMED",) and not c[9]:
        c[8], c[9] = V[c[0]]
        lines[i] = "\t".join(c) + ("\r" if lines[i].endswith("\r") else "")
        n += 1
io.open(REG, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("ruled", n)
