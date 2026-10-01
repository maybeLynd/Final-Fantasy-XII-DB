"""vp8_pbi_names.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
Vp8DecoderInstance (libvpx VP8D_COMP) fields named by the engine's own allocation-failure text, and fields read by
the frame-receive, get-frame, thread-creation and temp-buffer allocation bodies, each with its receiver proven.

  N  THE ENGINE NAMES TWELVE POINTERS. libvpx's CHECK_MEM_ERROR stores the allocation, tests it, and on failure calls
     vpx_internal_error(&pc->error, VPX_CODEC_MEM_ERROR, "Failed to allocate " #lval), so each string is the text of the
     lvalue just stored. In 00171480 (rbx = rcx = pbi) and 00171AE0 (rsi = rcx = pbi), the store of each allocation
     precedes the lea of its string, and the error context is pbi + 0x12C0:
       (pbi->h_decoding_thread) +0x4420, (pbi->h_event_start_decoding) +0x4428, (pbi->mb_row_di) +0x4410,
       (pbi->de_thread_data) +0x4418, pbi->pmutex +0x43B0, (pbi->mt_current_mb_col) +0x43A8, (pbi->mt_yabove_row) +0x43E0,
       (pbi->mt_uabove_row) +0x43E8, (pbi->mt_vabove_row) +0x43F0, (pbi->mt_yleft_col) +0x43F8, (pbi->mt_uleft_col) +0x4400,
       (pbi->mt_vleft_col) +0x4408
  C  00171480 (vp8_decoder_create_threads): zeroes +0x4380 and +0x4390; InitializeCriticalSection(+0x43B8); core count =
     min([+0x4384], 8), then bounded by [+0x34E8]; when above 1 it sets +0x4380 = 1 and +0x438C = count - 1, sizes every
     per-thread array by +0x438C, fills 24-byte thread records {i, pbi, &mb_row_di[i]}, starts each thread with
     _beginthreadex, creates each start semaphore and then +0x4430 with CreateSemaphoreW, and finally copies +0x438C into +0x4390
  S  00171AE0 (vp8mt_alloc_temp_buffers): the width rounded up to 16 selects +0x43A4 = 1 (< 640), 8 (<= 1280), 16 (<= 2560)
     or 32; every row-array count is [pbi + 0x12C0 + 0xBB4] = +0x1E74 (the store's mbRows)
  E  0016DE20 (vpx_internal_error) on the record at pbi + 0x12C0: +0 = code, +4 = has-detail 0 / 1,
     __stdio_common_vsprintf into +8 with count 0x4F, NUL at +0x57, then if [+0x58] != 0 longjmp(+0x60, code)
  R  0016F840 (vp8dx_receive_compressed_data; rdi = rcx = pbi, rbx = pbi + 0x12C0): clears the error code; finds the
     first zero of the four counts at +0x1C80 and sets it to 1; stores the index at +0x1C90; sets the four pointers
     +0x12A0..+0x12B8 to &frameBuffers[idx] for the indices at +0x1C90 / +0x1C94 / +0x1C98 / +0x1C9C (stride 0x90 from
     +0x1A40); __intrinsic_setjmp(+0x1320); +0x1318 = 1; calls 00175EF0(pbi). On the setjmp return path it sets the
     +0x88 dword of the record at +0x1C94's index and decrements the count at +0x1C90's index. After the decode, when
     [+0x1E68] != 0 it increments +0x34DC and copies +0x1EB0 to +0x1EB8. It then stores the fourth argument at +0x4438,
     sets +0x4440 = 0 and clears +0x1318
  G  0016EA80 (vp8_get_frame; pbi = [ctx + 0x1B0]): returns when [+0x4440] == 1 or [+0x1E68] == 0, otherwise sets
     +0x4440 = 1 and hands pbi + 0x12C0 to 00177A70
  P  REGRESSION (FAILS before): the rows below are in the store; VpxInternalErrorInfo and Vp8DecodeThreadData exist and tile
The earlier scoped absence rows at +0x1E68 and +0x1EB8 (UQ-308 / UQ-310) stay true for the bodies they listed; the readers
here are outside that list.
Usage: python vp8_pbi_names.py [--patch]
"""
import hashlib, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True); pe.parse_data_directories([pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
IMP = {i.address - pe.OPTIONAL_HEADER.ImageBase + B: i.name.decode() for e in pe.DIRECTORY_ENTRY_IMPORT for i in e.imports if i.name}
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, b): return list(cs.disasm(d[off(a):off(b)], a))
def rip(x):
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0) if m else None
def imp(x): return IMP.get(rip(x)) if x.mnemonic == "call" and "rip" in x.op_str else None
def thunk(t):   # a jmp [IAT] thunk
    x = next(cs.disasm(d[off(t):off(t) + 6], t)); return IMP.get(rip(x)) if x.mnemonic == "jmp" else None
def cstr(va):
    o = off(va); return d[o:d.index(b"\0", o)].decode("latin-1")
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(L, pairs): return all(any(x.address == a and (x.mnemonic, x.op_str) == v for x in L) for a, v in pairs)

# N ------------------------------------------------------------------------------------------------------------------
NAMED = {0x4420: "(pbi->h_decoding_thread)", 0x4428: "(pbi->h_event_start_decoding)", 0x4410: "(pbi->mb_row_di)",
         0x4418: "(pbi->de_thread_data)", 0x43B0: "pbi->pmutex", 0x43A8: "(pbi->mt_current_mb_col)",
         0x43E0: "(pbi->mt_yabove_row)", 0x43E8: "(pbi->mt_uabove_row)", 0x43F0: "(pbi->mt_vabove_row)",
         0x43F8: "(pbi->mt_yleft_col)", 0x4400: "(pbi->mt_uleft_col)", 0x4408: "(pbi->mt_vleft_col)"}
FN = [(0x171480, 0x171790, "rbx", 0x17148E), (0x171AE0, 0x172160, "rsi", 0x171B05)]
found = {}
for lo, hi, reg, setp in FN:
    L = ins(lo, hi); entry_ok = any(x.address == setp and (x.mnemonic, x.op_str) == ("mov", "%s, rcx" % reg) for x in L)
    for i, x in enumerate(L):
        if x.mnemonic == "lea" and x.op_str.startswith("r8, [rip"):
            s = cstr(rip(x))
            if not s.startswith("Failed to allocate "): continue
            nm = s[len("Failed to allocate "):]
            if nm.endswith("[i]"): continue
            win = L[max(0, i - 6):i]
            st = [int(m.group(1), 16) for y in win for m in [re.fullmatch(r"qword ptr \[%s \+ (0x[0-9a-f]+)\], \w+" % reg, y.op_str)] if y.mnemonic == "mov" and m]
            near = L[max(0, i - 6):i + 3]   # the error-context load sits just before or just after the string's lea
            ctx = any(y.mnemonic == "lea" and y.op_str == "rcx, [%s + 0x12c0]" % reg for y in near) or any(y.mnemonic == "mov" and y.op_str == "rcx, rdi" for y in near)
            call = any(y.mnemonic == "call" and y.op_str == "0x16de20" for y in L[i + 1:i + 4])
            if entry_ok and st and ctx and call: found[st[-1]] = nm
check("N", found == NAMED, "twelve 'Failed to allocate <lvalue>' strings each follow the store they name: %s"
      % ", ".join("+0x%X %s" % (k, v) for k, v in sorted(found.items())))
# 00171AE0's error context rdi is pbi + 0x12C0
L2 = ins(0x171AE0, 0x171B10)
check("N2", has(L2, [(0x171AFB, ("lea", "rdi, [rcx + 0x12c0]")), (0x171B05, ("mov", "rsi, rcx"))]), "00171AE0: rdi = pbi + 0x12C0 (the error context and the base of [rdi + 0xBB4]), rsi = pbi")

# C ------------------------------------------------------------------------------------------------------------------
L = ins(0x171480, 0x171790)
c1 = has(L, [(0x17148E, ("mov", "rbx, rcx")), (0x171491, ("mov", "dword ptr [rcx + 0x4380], r14d")), (0x171498, ("mov", "dword ptr [rcx + 0x4390], r14d")),
             (0x17149F, ("add", "rcx, 0x43b8")), (0x1714AC, ("mov", "ecx, dword ptr [rbx + 0x4384]")), (0x1714B2, ("mov", "eax, 8")), (0x1714B9, ("cmovg", "ecx, eax")),
             (0x1714BC, ("mov", "eax, dword ptr [rbx + 0x34e8]")), (0x1714C4, ("cmovg", "ecx, eax")), (0x1714C7, ("cmp", "ecx, 1")),
             (0x1714D0, ("lea", "eax, [rcx - 1]")), (0x1714EE, ("mov", "dword ptr [rbx + 0x4380], 1")), (0x1714FB, ("mov", "dword ptr [rbx + 0x438c], eax")),
             (0x1716DA, ("mov", "dword ptr [rdx + rax], ebp")), (0x1716E4, ("mov", "qword ptr [rdx + rax + 8], rbx")), (0x1716FA, ("mov", "qword ptr [rdx + rax + 0x10], rcx")),
             (0x171764, ("mov", "qword ptr [rbx + 0x4430], rax")), (0x17176B, ("mov", "eax, dword ptr [rbx + 0x438c]")), (0x171771, ("mov", "dword ptr [rbx + 0x4390], eax"))])
c2 = [imp(x) for x in L if imp(x)]
check("C", c1 and c2[:1] == ["InitializeCriticalSection"] and "CreateSemaphoreW" in c2 and "_beginthreadex" in c2,
      "00171480: maxThreads +0x4384 clamped to 8 and to +0x34E8; +0x4380 = 1, +0x438C = count - 1; records {i, pbi, &mb_row_di[i]}; +0x4430 a semaphore; +0x4390 = +0x438C (imports %s)" % c2)

# S ------------------------------------------------------------------------------------------------------------------
L = ins(0x171B63, 0x171BC0)
check("S", has(L, [(0x171B66, ("mov", "edx, 0x10")), (0x171B77, ("cmp", "r14d, 0x280")), (0x171B7E, ("jge", "0x171b8c")), (0x171B80, ("mov", "dword ptr [rsi + 0x43a4], 1")),
                   (0x171B8C, ("cmp", "r14d, 0x500")), (0x171B93, ("jg", "0x171ba1")), (0x171B95, ("mov", "dword ptr [rsi + 0x43a4], 8")), (0x171BA1, ("cmp", "r14d, 0xa00")),
                   (0x171BA8, ("mov", "eax, 0x20")), (0x171BAD, ("cmovle", "eax, edx")), (0x171BB0, ("mov", "dword ptr [rsi + 0x43a4], eax")),
                   (0x171BB6, ("movsxd", "rax, dword ptr [rdi + 0xbb4]"))]),
      "00171AE0: syncRange +0x43A4 = 1 / 8 / 16 / 32 by the 16-aligned width (640 / 1280 / 2560); row counts from +0x12C0 + 0xBB4 = +0x1E74")

# E ------------------------------------------------------------------------------------------------------------------
L = ins(0x16DE20, 0x16DEB7)
check("E", has(L, [(0x16DE37, ("mov", "dword ptr [rcx], edx")), (0x16DE3C, ("mov", "dword ptr [rcx + 4], 0")), (0x16DE57, ("mov", "dword ptr [rcx + 4], 1")),
                   (0x16DE68, ("lea", "rdx, [rdi + 8]")), (0x16DE78, ("mov", "r8d, 0x4f")), (0x16DE95, ("mov", "byte ptr [rdi + 0x57], 0")),
                   (0x16DE99, ("cmp", "dword ptr [rdi + 0x58], 0")), (0x16DEA4, ("mov", "edx, dword ptr [rdi]")), (0x16DEA6, ("lea", "rcx, [rdi + 0x60]"))])
      and [imp(x) for x in L if imp(x)] == ["__stdio_common_vsprintf", "longjmp"],
      "0016DE20: code +0, has-detail +4, detail +8 (79 chars + NUL at +0x57), armed flag +0x58, longjmp(+0x60, code)")

# R ------------------------------------------------------------------------------------------------------------------
L = ins(0x16F840, 0x16FA25)
r1 = has(L, [(0x16F859, ("lea", "rbx, [rcx + 0x12c0]")), (0x16F860, ("mov", "rdi, rcx")), (0x16F868, ("mov", "dword ptr [rbx], 0")),
             (0x16F884, ("cmp", "dword ptr [rbx + rax*4 + 0x9c0], 0")), (0x16F890, ("cmp", "ecx, 4")), (0x16F89B, ("mov", "dword ptr [rbx + rax*4 + 0x9c0], 1")),
             (0x16F8AA, ("mov", "dword ptr [rbx + 0x9d0], ecx")), (0x16F8B4, ("add", "rax, 0x780")), (0x16F8BD, ("mov", "qword ptr [rdi + 0x12a0], rax")),
             (0x16F8C4, ("movsxd", "rax, dword ptr [rbx + 0x9d4]")), (0x16F8DD, ("mov", "qword ptr [rdi + 0x12a8], rax")),
             (0x16F8E4, ("movsxd", "rax, dword ptr [rbx + 0x9d8]")), (0x16F8FD, ("mov", "qword ptr [rdi + 0x12b0], rax")),
             (0x16F904, ("movsxd", "rax, dword ptr [rbx + 0x9dc]")), (0x16F91D, ("lea", "rcx, [rdi + 0x1320]")), (0x16F924, ("mov", "qword ptr [rdi + 0x12b8], rax")),
             (0x16F92B, ("call", "0x861ef6")), (0x16F930, ("mov", "rbx, qword ptr [rsp + 0x40]")),
             (0x16F942, ("movsxd", "rax, dword ptr [rdx + 0x9d4]")), (0x16F950, ("mov", "dword ptr [rdx + rcx*8 + 0x808], 1")),
             (0x16F984, ("mov", "dword ptr [rbx + 0x1318], 1")), (0x16F98E, ("call", "0x175ef0")), (0x16F9BF, ("mov", "dword ptr [rbx + 0x12c0], 1")),
             (0x16F9CB, ("mov", "rdi, qword ptr [rsp + 0x28]")), (0x16F9E1, ("cmp", "dword ptr [rdi + 0xba8], 0")), (0x16F9EA, ("inc", "dword ptr [rdi + 0x221c]")),
             (0x16F9F0, ("mov", "rax, qword ptr [rdi + 0xbf0]")), (0x16F9F7, ("mov", "qword ptr [rdi + 0xbf8], rax")), (0x16F9FE, ("mov", "rax, qword ptr [rsp + 0x58]")),
             (0x16FA03, ("mov", "qword ptr [rbx + 0x4438], rax")), (0x16FA0A, ("mov", "dword ptr [rbx + 0x4440], 0")), (0x16FA14, ("mov", "dword ptr [rbx + 0x1318], 0"))])
r2 = has(L, [(0x16F84A, ("mov", "qword ptr [rsp + 0x20], r9")), (0x16F84F, ("mov", "qword ptr [rsp + 8], rcx")), (0x16F854, ("push", "rdi")), (0x16F855, ("sub", "rsp, 0x30")),
             (0x16F863, ("mov", "qword ptr [rsp + 0x28], rbx"))])
check("R", r1 and r2 and thunk(0x861EF6) == "__intrinsic_setjmp",
      "0016F840: counts +0x1C80[4], index +0x1C90, refs +0x12A0..+0x12B8 from +0x1C90..+0x1C9C, setjmp(+0x1320) armed at +0x1318; show_frame +0x1E68 gates +0x34DC++ and +0x1EB8 = +0x1EB0; +0x4438 = arg4, +0x4440 = 0")

# G ------------------------------------------------------------------------------------------------------------------
L = ins(0x16EA80, 0x16EB2A)
check("G", has(L, [(0x16EA92, ("mov", "rdi, rcx")), (0x16EA9E, ("mov", "rcx, qword ptr [rcx + 0x1b0]")), (0x16EAE8, ("cmp", "dword ptr [rcx + 0x4440], 1")),
                   (0x16EAF5, ("cmp", "dword ptr [rcx + 0x1e68], 0")), (0x16EB02, ("mov", "dword ptr [rcx + 0x4440], 1")), (0x16EB11, ("add", "rcx, 0x12c0")),
                   (0x16EB25, ("call", "0x177a70"))]),
      "0016EA80 (pbi = [ctx + 0x1B0]): returns when +0x4440 == 1 or +0x1E68 == 0; else +0x4440 = 1 and pbi + 0x12C0 goes to 00177A70")

# the store ----------------------------------------------------------------------------------------------------------
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/vp8-macroblock-decoder/vp8_pbi_names.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
INST, FB, ERR, TD = "Vp8DecoderInstance", "Vp8FrameBuffer", "VpxInternalErrorInfo", "Vp8DecodeThreadData"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "NAMED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was, w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
ENG = lambda s: " Engine text names it: 'Failed to allocate %s' (N)." % s
# (offset, old name) -> replacement rows; 'was' is filled from the old row at patch time
def cutI(o, was):
    I = INST
    if o == 0x12A0: return [r(I, 0x12A0, 32, "decFbRef", FB + "*[4]", "four pointers into frameBuffers (+0x1A40, stride 0x90), set on every receive to the records at the indices +0x1C90 (new), +0x1C94 (last), +0x1C98 (golden) and +0x1C9C (altref) - libvpx dec_fb_ref[INTRA/LAST/GOLDEN/ALTREF]", P, "R", was)]
    if o == 0x12C0: return [r(I, 0x12C0, 0x160, "errorInfo", ERR, "the error record every allocation check and the receive path hand to vpx_internal_error (0016DE20) as pbi + 0x12C0; the receive path clears its code, arms it with setjmp and sets code 1 on a failed decode", P, "E R N", was),
                            r(I, 0x1420, 1560, "unobservedSpan1420", "u8[1560]", "between the error record and frameToShow (+0x1A38); not read by the bodies read here", U, "E R", was)]
    if o == 0x1C80: return [r(I, 0x1C80, 16, "fbIdxRefCnt", "int32[4]", "one reference count per frameBuffers record: the receive path takes the first zero entry, sets it to 1 and stores its index at +0x1C90; the error path decrements the count at +0x1C90's index when above 0", P, "R", was)]
    if o == 0x1C94: return [r(I, 0x1C94, 4, "lastFbIndex", "int32", "index into frameBuffers of the last-frame reference: selects decFbRef[1]; on the error path its record's +0x88 (corrupted) is set to 1", P, "R", was),
                            r(I, 0x1C98, 4, "goldenFbIndex", "int32", "index into frameBuffers of the golden-frame reference: selects decFbRef[2]", P, "R", was),
                            r(I, 0x1C9C, 4, "altRefFbIndex", "int32", "index into frameBuffers of the altref reference: selects decFbRef[3]", P, "R", was)]
    if o == 0x1E68: return [r(I, 0x1E68, 4, "showFrame", "int32", "common.show_frame: when non-zero the receive path increments currentVideoFrame and copies modeInfo to showFrameModeInfo; vp8_get_frame returns no frame while it is zero", P, "R G", was),
                            r(I, 0x1E6C, 8, "unobservedSpan1E6C", "uint8[8]", "not read by the bodies read here, nor by those the earlier scoped absence listed (UQ-308 / UQ-310)", U, "R G", was)]
    if o == 0x1EB8: return [r(I, 0x1EB8, 8, "showFrameModeInfo", "Vp8ModeInfo*", "common.show_frame_mi: the receive path copies modeInfo (+0x1EB0) here after a shown frame", P, "R", was),
                            r(I, 0x1EC0, 3372, "unobservedSpan1EC0", "uint8[3372]", "not read by the bodies read here, nor by those the earlier scoped absence listed (UQ-308 / UQ-310)", U, "R", was)]
    if o == 0x2C20: return [r(I, 0x2C20, 2236, "unobservedSpan2C20", "u8[2236]", "not read by the bodies read here", U, "R C", was),
                            r(I, 0x34DC, 4, "currentVideoFrame", "uint32", "common.current_video_frame: incremented by the receive path after each shown frame", P, "R", was),
                            r(I, 0x34E0, 8, "unobservedSpan34E0", "u8[8]", "not read by the bodies read here", U, "R C", was),
                            r(I, 0x34E8, 4, "processorCoreCount", "int32", "common.processor_core_count: the second bound of the decoder thread count in 00171480, after the clamp to 8", P, "C", was),
                            r(I, 0x34EC, 3540, "unobservedSpan34EC", "u8[3540]", "not read by the bodies read here", U, "R C", was)]
    if o == 0x4384: return [r(I, 0x4384, 4, "maxThreads", "int32", "the configured thread limit: 00171480 clamps it to 8 and then to processorCoreCount; the core count minus one becomes decodingThreadCount", P, "C", was),
                            r(I, 0x4388, 4, "unobservedSpan4388", "u8[4]", "not read by the bodies read here", U, "C", was),
                            r(I, 0x438C, 4, "decodingThreadCount", "uint32", "the number of decoder threads 00171480 creates (core count - 1): the count of every per-thread array it allocates and of its thread-start loop", P, "C", was)]
    if o == 0x4394: return [r(I, 0x4394, 16, "unobservedSpan4394", "u8[16]", "not read by the bodies read here", U, "C S", was),
                            r(I, 0x43A4, 4, "syncRange", "int32", "the column distance between decoder threads: 00171AE0 sets 1 / 8 / 16 / 32 for a 16-aligned width below 640 / up to 1280 / up to 2560 / above", P, "S", was)]
    if o == 0x4438: return [r(I, 0x4438, 8, "lastTimeStamp", "int64", "the receive path stores its fourth argument here after each decoded frame", P, "R", was),
                            r(I, 0x4440, 4, "readyForNewData", "int32", "0 after the receive path decodes a frame; vp8_get_frame returns no frame while it is 1 and sets it to 1 when it hands one out", P, "R G", was)]
RENAME = {0x4390: ("allocatedDecodingThreadCount", None, " 00171480 zeroes it before creating threads and copies decodingThreadCount into it after they start (C)."),
          0x43A8: ("mtCurrentMbCol", None, ENG("(pbi->mt_current_mb_col)") + " 00171AE0 allocates one int32 per macroblock row (mbRows * 4) and zeroes it."),
          0x43B0: ("pmutex", None, ENG("pbi->pmutex") + " 00171AE0 allocates one 0x28-byte CRITICAL_SECTION per macroblock row and initialises each."),
          0x43E0: ("mtYaboveRow", None, ENG("(pbi->mt_yabove_row)")), 0x43E8: ("mtUaboveRow", None, ENG("(pbi->mt_uabove_row)")),
          0x43F0: ("mtVaboveRow", None, ENG("(pbi->mt_vabove_row)")), 0x43F8: ("mtYleftCol", None, ENG("(pbi->mt_yleft_col)")),
          0x4400: ("mtUleftCol", None, ENG("(pbi->mt_uleft_col)")), 0x4408: ("mtVleftCol", None, ENG("(pbi->mt_vleft_col)")),
          0x4410: ("mbRowDi", None, ENG("(pbi->mb_row_di)")), 0x4418: ("deThreadData", TD + "*", ENG("(pbi->de_thread_data)") + " 00171480 fills one 24-byte Vp8DecodeThreadData per thread."),
          0x4420: ("hDecodingThread", None, ENG("(pbi->h_decoding_thread)") + " 00171480 stores each _beginthreadex handle here."),
          0x4428: ("hEventStartDecoding", None, ENG("(pbi->h_event_start_decoding)") + " 00171480 stores each CreateSemaphoreW handle here."),
          0x4430: (None, None, " 00171480 creates it with CreateSemaphoreW after the per-thread loop (C).")}
FBCUT = [r(FB, 0x64, 36, "unobservedSpan0064", "u8[36]", "not read here", U, "R", "unobservedSpan0064 u8[44]"),
         r(FB, 0x88, 4, "corrupted", "int32", "the record's corrupted flag: the receive path's setjmp return sets it to 1 on the last-frame reference; frameToShow's +0x88 is what the corrupted-frame control reports", P, "R", "unobservedSpan0064 u8[44]"),
         r(FB, 0x8C, 4, "unobservedSpan008C", "u8[4]", "not read here", U, "R", "unobservedSpan0064 u8[44]")]
NEWT = [[ERR, "0x160", "23-Third-Party-Libraries", "one at Vp8DecoderInstance +0x12C0 (libvpx common.error)", "EMBEDDED in Vp8DecoderInstance", "none read", "none - part of its owner", P[0], P[1], "L1",
         "CARVED 2026-09-28 (OPUS, %s E R). Extent: +0x60 plus the MSVC x64 jmp_buf (_JBLEN 16 x SETJMP_FLOAT128 = 256 bytes), the buffer __intrinsic_setjmp and longjmp take. %s" % (REC, EXE),
         "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", "EMBED Vp8DecoderInstance +0x12C0"],
        [TD, "0x18", "23-Third-Party-Libraries", "an array of decodingThreadCount records at [Vp8DecoderInstance +0x4418]; each is the start argument of one decoder thread", "00171480 (vpx_memalign, count * 0x18)", "00171480 fills i / pbi / &mb_row_di[i]", "freed with the array (00172160)", P[0], P[1], "L1",
         "CARVED 2026-09-28 (OPUS, %s C). %s" % (REC, EXE), "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", ""]]
NEWF = [r(ERR, 0, 4, "errorCode", "int32", "the codec error code: vpx_internal_error stores its second argument; the receive path clears it on entry and sets 1 on a failed decode", P, "E R", "-"),
        r(ERR, 4, 4, "hasDetail", "int32", "1 when a detail message was formatted, else 0 (vpx_internal_error)", P, "E", "-"),
        r(ERR, 8, 80, "detail", "char[80]", "the formatted message: __stdio_common_vsprintf with count 79, then a NUL at +0x57", P, "E", "-"),
        r(ERR, 0x58, 4, "setjmpArmed", "int32", "non-zero while a setjmp on jmp is live: the receive path sets 1 around the frame decode and 0 after; vpx_internal_error longjmps only when it is set", P, "E R", "-"),
        r(ERR, 0x5C, 4, "unobservedSpan005C", "u8[4]", "not read here (alignment before jmp)", U, "E", "-"),
        r(ERR, 0x60, 256, "jmp", "u8[256]", "the jmp_buf: the receive path's __intrinsic_setjmp target and vpx_internal_error's longjmp target", P, "E R", "-"),
        r(TD, 0, 4, "threadIndex", "int32", "the thread's index i", P, "C", "-"),
        r(TD, 4, 4, "unobservedSpan0004", "u8[4]", "not written by 00171480", U, "C", "-"),
        r(TD, 8, 8, "decoder", INST + "*", "the decoder instance (pbi)", P, "C", "-"),
        r(TD, 0x10, 8, "rowDecoder", "Vp8MacroblockDecoder*", "&mb_row_di[i], this thread's record in the array at +0x4410", P, "C", "-")]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]
    out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == INST and REC not in c[8]:
            o = int(c[1], 16); was = "%s %s (%s)" % (c[3], c[4], c[5][:160])
            if c[3].startswith("unobservedSpan") and cutI(o, was):
                out += ["\t".join(x) + e for x in cutI(o, was)]; continue
            if o in RENAME:
                nm, ct, add = RENAME[o]
                c[8] += " || %s 2026-09-28 (OPUS, %s): was %s %s" % ("RENAMED" if nm else "EXTENDED", REC, c[3], c[4])
                if nm: c[3] = nm
                if ct: c[4] = ct
                c[5] += add; out.append("\t".join(c) + e); continue
        if c[0] == FB and c[1] == "0x0064" and c[3] == "unobservedSpan0064" and c[2] == "44":
            out += ["\t".join(x) + e for x in FBCUT]; continue
        out.append(l)
    if not any(cells(l)[0] == ERR for l in out):
        idx = max(i for i, l in enumerate(out) if cells(l)[0] == FB)
        out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in NEWF]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == ERR for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == FB)
        tl[ti + 1:ti + 1] = ["\t".join(x) + te for x in NEWT]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in T and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16)
I = {int(c[1], 16): c for c in F if c[0] == INST}
want = {0x12A0: "decFbRef", 0x12C0: "errorInfo", 0x1C80: "fbIdxRefCnt", 0x1C94: "lastFbIndex", 0x1E68: "showFrame", 0x1EB8: "showFrameModeInfo",
        0x34DC: "currentVideoFrame", 0x34E8: "processorCoreCount", 0x4384: "maxThreads", 0x438C: "decodingThreadCount", 0x4390: "allocatedDecodingThreadCount",
        0x43A4: "syncRange", 0x43A8: "mtCurrentMbCol", 0x43B0: "pmutex", 0x43E0: "mtYaboveRow", 0x4408: "mtVleftCol", 0x4410: "mbRowDi", 0x4418: "deThreadData",
        0x4420: "hDecodingThread", 0x4428: "hEventStartDecoding", 0x4438: "lastTimeStamp", 0x4440: "readyForNewData"}
fbr = {int(c[1], 16): c[3] for c in F if c[0] == FB}
check("P", all(o in I and I[o][3] == n for o, n in want.items()) and all(tiles(t) for t in (INST, FB, ERR, TD)) and fbr.get(0x88) == "corrupted"
      and I[0x12C0][4] == ERR and I[0x4418][4] == TD + "*",
      "the named rows are in the store; Vp8DecoderInstance, Vp8FrameBuffer, VpxInternalErrorInfo and Vp8DecodeThreadData tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
