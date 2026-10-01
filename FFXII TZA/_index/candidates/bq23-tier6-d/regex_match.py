"""regex_match.py - identify 24 FFXII_TZA.exe functions against VS2015 (v140, 14.0.24215) <regex>.

Re-runnable, read-only. Reads the exe + functions.tsv, disassembles each target with capstone,
extracts features, and checks each function against a spec derived from the header source
(C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\include\\regex, xutility, vector, locale).

Controls:
  C1 confusion matrix  - every spec is run against every one of the 24 functions; an identification
                         is only discriminative if its spec passes on exactly one function.
  C2 negative sample   - every spec is run against a fixed-seed random sample of non-regex functions.
  C3 image-wide sweeps - who calls _Xregex_error / ctype<char>::tolower / contains the inlined
                         _Parser::_Next escape idiom / reads [reg+0x7c] as _Mchar with a metachar compare.
  C4 planted positive  - the feature extractor must find known values in a known function
                         (e.g. 00205890 must yield error codes {4,5,6,10}) or the run aborts.
Writes regex-members.tsv next to this file.
"""
import sys, os, re, random, struct, pefile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pelib import Image, load_sizes, rip_target, branch_target, rtti

img = Image()
SIZES = load_sizes()
TDS, COLS, VT = rtti(img)
img.pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
IMP = {}
for e in img.pe.DIRECTORY_ENTRY_IMPORT:
    for i in e.imports:
        IMP[i.address] = (e.dll.decode() + "!" + (i.name.decode() if i.name else "ord%d" % i.ordinal))

def imp_addr(sub):
    hits = [a for a, n in IMP.items() if sub in n]
    assert len(hits) == 1, (sub, hits)
    return hits[0]

XREGEX = imp_addr("?_Xregex_error@std@@")
TOLOWER = imp_addr("?tolower@?$ctype@D@std@@QEBADD@Z")
REALLOC = imp_addr("!realloc")
XBADALLOC = imp_addr("?_Xbad_alloc@std@@")
STRXFRM = imp_addr("!_Strxfrm")
STRCHR = imp_addr("VCRUNTIME140.dll!strchr")
MEMMOVE = imp_addr("VCRUNTIME140.dll!memmove")
OPNEW = 0x210EC0     # operator new wrapper (size in ecx)

REGEX_VT = {va: n for va, (n, col, o) in VT.items()
            if n.startswith(".?AV_Node") or n.startswith(".?AV_Root") or n.startswith(".?AV?$_Node")}
COLLATE_VT = [va for va, (n, c, o) in VT.items() if n == ".?AV?$collate@D@std@@"]

TARGETS = [0x203240, 0x203980, 0x204820, 0x204950, 0x205890, 0x205B40, 0x206430, 0x206890,
           0x206960, 0x206CD0, 0x206F60, 0x2070A0, 0x207B40, 0x2080D0, 0x2085B0, 0x208710,
           0x208DE0, 0x209360, 0x209840, 0x209CD0, 0x209E00,
           0x203490, 0x204E50, 0x205330]
ALLOC_LABELLED = {0x203490, 0x204E50, 0x205330}


class Feat:
    def __init__(self, a):
        self.addr = a
        self.size = SIZES[a]
        self.ins = img.disasm(a, self.size)
        self.text = "\n".join("%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in self.ins)
        self.calls = []          # (site, target)
        self.tailjmps = []       # jmp outside the body
        self.imports = []
        self.xerr = []           # error_type codes passed to _Xregex_error
        self.new_sizes = []
        self.vt_lea = []
        self.strs = []
        self.mchar_cmp = set()   # immediates compared with dword [reg+0x7c]  (_Parser::_Mchar)
        self.char_cmp = set()    # immediates compared with byte [reg+0x78] or a byte loaded from it
        self.lflag_masks = set() # masks tested on _Parser::_L_flags  ([reg+0x80])
        lf_regs, ch_regs, mc_regs = set(), set(), set()
        prev = []
        end = a + self.size
        for ins in self.ins:
            m, o = ins.mnemonic, ins.op_str
            t = rip_target(ins)
            if m == "call":
                bt = branch_target(ins)
                if bt is not None:
                    self.calls.append((ins.address, bt))
                    if bt == OPNEW:
                        sz = self._last_ecx(prev)
                        self.new_sizes.append(sz)
                elif t in IMP:
                    self.imports.append(t)
                    if t == XREGEX:
                        self.xerr.append(self._last_ecx(prev))
            if m == "jmp":
                bt = branch_target(ins)
                if bt is not None and not (a <= bt < end):
                    self.tailjmps.append(bt)
            if m == "lea" and t is not None:
                if t in REGEX_VT:
                    self.vt_lea.append(REGEX_VT[t])
                elif img.sec_of(t) == ".rdata":
                    s = img.cstr(t, 80)
                    if len(s) >= 8:
                        self.strs.append(s)
            # Register tracking is deliberately NOT flow-aware and never kills: a register once loaded
            # from _L_flags/_Mchar/_Char keeps that role for the rest of the body. This can only ADD
            # candidate values (over-credit), which the confusion matrix (C1) and the negative sample
            # (C2) are there to catch; it cannot hide a value that the code tests.
            ml = re.match(r"(\w+), (?:dword|byte) ptr \[r\w+ \+ (0x7c|0x78|0x80)\]$", o)
            if m in ("mov", "movzx", "movsx") and ml:
                al = self._aliases(ml.group(1))
                {"0x80": lf_regs, "0x7c": mc_regs, "0x78": ch_regs}[ml.group(2)].update(al)
            mi = re.match(r"(\w+), (-?0x[0-9a-f]+|-?\d+)$", o)
            # _Mchar compares
            mm = re.match(r"dword ptr \[r\w+ \+ 0x7c\], (-?0x[0-9a-f]+|-?\d+)$", o)
            if m == "cmp" and mm:
                self.mchar_cmp.add(int(mm.group(1), 0))
            if m == "cmp" and mi and mi.group(1) in mc_regs:
                self.mchar_cmp.add(int(mi.group(2), 0))
            # _L_flags masks
            mt = re.match(r"dword ptr \[r\w+ \+ 0x80\], (0x[0-9a-f]+|\d+)$", o)
            if m == "test" and mt:
                self.lflag_masks.add(int(mt.group(1), 0))
            if mi and mi.group(1) in lf_regs:
                v = int(mi.group(2), 0)
                if m in ("test", "and"):   # `and eax, 0x80; je` is how 00205890 tests _L_asrt_wrd
                    self.lflag_masks.add(v)
                elif m == "bt":
                    self.lflag_masks.add(1 << v)
            # _Char compares
            mc = re.match(r"byte ptr \[r\w+ \+ 0x78\], (0x[0-9a-f]+|\d+)$", o)
            if m == "cmp" and mc:
                self.char_cmp.add(int(mc.group(1), 0))
            if m == "cmp" and mi and mi.group(1) in ch_regs:
                self.char_cmp.add(int(mi.group(2), 0))
            prev.append(ins)
        self.callset = {t for s, t in self.calls} | set(self.tailjmps)

    @staticmethod
    def _aliases(r):
        base = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi",
                "ebp": "rbp", "al": "rax", "bl": "rbx", "cl": "rcx", "dl": "rdx", "sil": "rsi",
                "dil": "rdi", "bpl": "rbp"}
        fam = {"rax": ["rax", "eax", "al"], "rbx": ["rbx", "ebx", "bl"], "rcx": ["rcx", "ecx", "cl"],
               "rdx": ["rdx", "edx", "dl"], "rsi": ["rsi", "esi", "sil"], "rdi": ["rdi", "edi", "dil"],
               "rbp": ["rbp", "ebp", "bpl"]}
        for n in range(8, 16):
            fam["r%d" % n] = ["r%d" % n, "r%dd" % n, "r%db" % n]
            for x in fam["r%d" % n]:
                base[x] = "r%d" % n
        b = base.get(r, r)
        return set(fam.get(b, [r]))

    @staticmethod
    def _last_ecx(prev):
        for ins in reversed(prev[-6:]):
            mm = re.match(r"ecx, (0x[0-9a-f]+|\d+)$", ins.op_str)
            if ins.mnemonic == "mov" and mm:
                return int(mm.group(1), 0)
            mm = re.match(r"ecx, \[r(\w+) ([+-]) (0x[0-9a-f]+|\d+)\]$", ins.op_str)
            if ins.mnemonic == "lea" and mm:
                return "lea(%s%s%s)" % (mm.group(1), mm.group(2), mm.group(3))
            if ins.mnemonic == "xor" and ins.op_str == "ecx, ecx":
                return 0
        return None

    def has(self, pat):
        return re.search(pat, self.text, re.M) is not None


def jump_table(base_va, idx_off, tbl_off, n_idx, idx_bias):
    """MSVC two-level table: byte index table then dword RVA table (both relative to image base)."""
    out = {}
    for k in range(n_idx):
        b = img.read(img.base + idx_off + k, 1)[0]
        rva = img.d(img.base + tbl_off + 4 * b)
        out[k + idx_bias] = img.base + rva
    return out


def word_table(tbl_off, n, bias):
    return {k + bias: img.base + img.d(img.base + tbl_off + 4 * k) for k in range(n)}


def _drefs(rva):
    t = struct.pack('<I', rva); out = []; i = img.data.find(t)
    while i != -1:
        out.append(img.va_of_off(i)); i = img.data.find(t, i + 1)
    return out


def eh_parent(funclet):
    """Walk x64 MSVC EH data: funclet -> HandlerType -> TryBlockMapEntry -> FuncInfo -> UNWIND_INFO -> .pdata."""
    parents = set()
    for h in _drefs(funclet - img.base):
        if img.sec_of(h) != ".rdata":
            continue
        for tb in _drefs(h - 12 - img.base):
            for fr in _drefs(tb - 16 - img.base):
                fi = fr - 16
                if img.d(fi) & 0xFFFFFFF0 != 0x19930520:
                    continue
                p0, p1, pva = img.sec_range(".pdata")
                for u in _drefs(fi - img.base):
                    for off in range(p0, p1, 12):
                        b, e, ui = struct.unpack_from("<3I", img.data, off)
                        if 0 < (u - img.base) - ui < 64 and b + img.base != funclet:
                            parents.add(b + img.base)
    return parents


def funclet_discards_nfa(F):
    """0x206CD0's only caller is a catch funclet; its EH parent must be _Parser::_Compile
    (00206AD0: _Begin_capture_group(0), _Disjunction, error_syntax, _New_node(_N_end=0x15)) and the
    funclet must pass [frame+0x40]+0x40 (&_Nfa) then _CxxThrowException(0,0) (rethrow)."""
    callers = CALLERS.get(F.addr, set())
    if len(callers) != 1:
        return False
    fl = next(iter(callers))
    ftxt = "\n".join("%s %s" % (i.mnemonic, i.op_str) for i in img.disasm(fl, SIZES.get(fl, 36)))
    if not re.search(r"add rcx, 0x40\ncall 0x206cd0\nxor edx, edx\nxor ecx, ecx\ncall 0x861ecc", ftxt):
        return False
    thunk = img.disasm(0x861ECC, 6)[0]
    if IMP.get(rip_target(thunk), "").split("!")[-1] != "_CxxThrowException":
        return False
    par = eh_parent(fl)
    if par != {0x206AD0}:
        return False
    P = Feat(0x206AD0)
    return ({0x206D30, 0x208C60} <= P.callset and 0xE in P.xerr and "mov edx, 0x15" in P.text)


# ---------------------------------------------------------------- specs
# Each spec: (VS2015 name, confidence, [ (description, predicate(F)) ... ])
# Offsets used below come from the header layouts on x64:
#  _Parser<const char*,char,regex_traits<char>>: _Pat 0 _Begin 8 _End 0x10 _Grp_idx 0x18 _Disj_count 0x1C
#     _Finished_grps(vector<bool>: _Myvec 0x20.., _Mysize 0x38) _Nfa 0x40 (_Current 0x48) _Traits 0x68
#     _Flags 0x70 _Val 0x74 _Char 0x78 _Mchar 0x7C _L_flags 0x80
#  _Builder: _Root 0 _Current 8 _Flags 0x10 _Traits 0x18 _Bmax 0x20 _Tmax 0x24
#  _Matcher<const char*,char,regex_traits<char>,const char*>: _Tgt_state 0 (_Cur 0, _Grp_valid 8, _Grps 0x28)
#     _Res 0x40 _Loop_vals 0x80 _Begin 0x98 _End 0xA0 _First 0xA8 _Rep 0xB0 _Sflags 0xB8 _Mflags 0xBC
#     _Traits 0xD0 _Max_complexity_count 0xDC _Max_stack_count 0xE0
#  _Node_base 0x20 (_Kind 8, _Flags 0xC, _Next 0x10, _Prev 0x18); _Node_class 0x50 (_Coll 0x20 _Small 0x28
#     _Large 0x30 _Ranges 0x38 _Classes 0x40 _Equiv 0x48); _Node_rep 0x38 (_Min 0x20 _Max 0x24 _End_rep 0x28
#     _Loop_number 0x30 _Simple_loop 0x34); _Root_node 0x30 (_Refs 0x2C); _Bitmap 0x20; _Buf<char> 0x10
NEXT_IDIOM = r"cmp +byte ptr \[r\w+\], 0x5c\n(?:.*\n){0,12}.*sub +al, 0x28\n.*cmp +al, 1\n(?:.*\n){0,4}.*sub +al, 0x7b\n.*test +al, 0xfd"
F_NEXT = 0x208CF0      # out-of-line _Parser::_Next (callers below)
F_TRANS = 0x209530     # _Parser::_Trans
F_NEWNODE = 0x208C60   # _Builder::_New_node (new 0x20, _Node_base vtable)

def newnode_kinds(F):
    return {int(k) for k in re.findall(r"mov +edx, (\d+)\n\S+ call +0x208c60", F.text)}

SPECS = {
 0x203240: ("std::_Cmp_chrange<const char*,const char*,std::_Cmp_icase<std::regex_traits<char>>>", "high", [
    ("two tolower() calls per iteration (translate_nocase on both chars)", lambda F: F.imports.count(TOLOWER) == 2),
    ("returns saved _Begin1 (r12) on mismatch; cmove _Begin1 if _Begin2==_End2", lambda F: F.has(r"cmove +r12, rbx")),
    ("reached only from _Compare's icase arm (bt flags,8 -> jb here)", lambda F: True if 0x2032E0 in CALLERS.get(F.addr, set()) else False),
    ("no allocation, no error throw", lambda F: not F.new_sizes and not F.xerr),
 ]),
 0x203980: ("std::equal<const char*,const char*,std::_Cmp_icase<std::_Regex_traits<char>>> (4-iterator+pred; random-access _Equal_unchecked inlined)", "high", [
    ("length compare first: (last1-first1) != (last2-first2) -> false", lambda F: F.has(r"sub +r9, r8\n.*sub +rax, rcx") and F.has(r"cmp +rax, r9")),
    ("loop: tolower(*it1) == tolower(*it2)", lambda F: F.imports.count(TOLOWER) == 2),
    ("pred is 5th arg (stack) holding traits*, uses [traits+8]=_Pctype", lambda F: F.has(r"mov +rcx, qword ptr \[rax \+ 8\]")),
    ("sole caller is _Regex_traits<char>::lookup_classname (00203A30, walks _Names table)", lambda F: CALLERS.get(F.addr) == {0x203A30}),
 ]),
 0x204820: ("std::vector<unsigned int>::operator=(const vector&) (vector<bool>::_Myvec copy; _Grp_valid assignment)", "high", [
    ("self-assign guard cmp this,&right", lambda F: F.has(r"cmp +rcx, rdx\n.*je")),
    ("element size 4 (sar 2)", lambda F: F.has(r"sar +r\w+, 2") and not F.has(r"sar +r\w+, 4")),
    ("memmove copy paths + _Buy/deallocate helpers", lambda F: F.imports.count(MEMMOVE) >= 3 and len(F.calls) >= 3),
    ("called from _Matcher::_Do_rep with rcx=&_Tgt_state._Grp_valid (this+8)", lambda F: 0x207B40 in CALLERS.get(F.addr, set())),
 ]),
 0x204950: ("std::vector<_Tgt_state_t<const char*>::_Grp_t>::operator=(const vector&) (16-byte elements; _Grps assignment)", "high", [
    ("self-assign guard", lambda F: F.has(r"cmp +rcx, rdx\n.*je")),
    ("element size 16 (sar 4 / and -16)", lambda F: F.has(r"sar +r\w+, 4") and F.has(r"and +rax, 0xfffffffffffffff0")),
    ("memmove copy paths", lambda F: F.imports.count(MEMMOVE) >= 3),
    ("called from _Matcher::_Do_rep with rcx=&_Tgt_state._Grps (this+0x28)", lambda F: 0x207B40 in CALLERS.get(F.addr, set())),
 ]),
 0x205890: ("_Parser::_Alternative()", "high", [
    ("_Mchar compared with | ) . \\ [ ( ^ $ * + ? { } ]",
        lambda F: {0x7c, 0x29, 0x2e, 0x5c, 0x5b, 0x28, 0x5e, 0x24, 0x3f, 0x7b, 0x7d, 0x5d} <= F.mchar_cmp),
    ("errors: brack(4) paren(5) brace(6) badrepeat(10)", lambda F: set(F.xerr) == {4, 5, 6, 10}),
    ("_New_node(00208C60) kinds dot(5) wbound(4) bol(2) eol(3)", lambda F: {5, 4, 2, 3} <= newnode_kinds(F)),
    ("'*','+' via lea eax,[rcx-0x2a]; cmp eax,1 -> error_badrepeat", lambda F: F.has(r"lea +eax, \[rcx - 0x2a\]\n.*cmp +eax, 1")),
    ("_Char compared with 'b' / 'B' under _L_asrt_wrd (0x80)", lambda F: {0x62, 0x42} <= F.char_cmp and 0x80 in F.lflag_masks),
    ("_L_paren_bal (0x10000000) gates ) } ]", lambda F: 0x10000000 in F.lflag_masks),
    ("_Negate inline: xor [_Current+0xC],1", lambda F: F.has(r"xor +dword ptr \[rax \+ 0xc\], 1")),
    ("calls _Wrapped_disjunction(00209840) and _Quantifier(00208DE0)", lambda F: {0x209840, 0x208DE0} <= F.callset),
 ]),
 0x205B40: ("_Parser::_AtomEscape()", "high", [
    ("_L_bckr(0x100) _L_bzr_chr(0x100000) _L_lim_bckr(0x200) _L_esc_wsd(0x20000)", lambda F: {0x100, 0x100000, 0x200, 0x20000} <= F.lflag_masks),
    ("_Val > _BRE_MAX_GRP(9) check", lambda F: F.has(r"cmp +edx, 9\n.*ja")),
    ("_Grp_idx(+0x18) and _Finished_grps._Mysize(+0x38) / bit test", lambda F: F.has(r"cmp +dword ptr \[rbx \+ 0x18\], edx") and F.has(r"cmp +qword ptr \[rbx \+ 0x38\], rdx")),
    ("errors escape(2) backref(3) (+ one computed lea ecx,[rdx+2] with rdx=_Val=0 -> 2)", lambda F: {2, 3} <= {x for x in F.xerr if isinstance(x, int)} and "lea(dx+2)" in F.xerr),
    ("tail-jumps to _Add_backreference(00204D10, new 0x28 _Node_back) and _Add_char(00204DA0)", lambda F: {0x204D10, 0x204DA0} <= set(F.tailjmps)),
    ("calls _DecimalDigits(00206C20) _CharacterEscape(00206430) _CharacterClassEscape(00206340)", lambda F: {0x206C20, 0x206430, 0x206340} <= F.callset),
 ]),
 0x206430: ("_Parser::_CharacterEscape()", "high", [
    ("_Mchar == _Meta_eos(-1) -> error_escape", lambda F: -1 in F.mchar_cmp),
    ("_Do_ffn inline: f n r t v -> 0xC 0xA 0xD 9 0xB", lambda F: {0x66, 0x6e, 0x72, 0x74, 0x76} <= F.char_cmp and all(F.has(r"mov +dword ptr \[rbx \+ 0x74\], %s$" % v) for v in ("0xc", "0xa", "0xd", "9", "0xb"))),
    ("_Do_ffnx inline: a b -> 7 8", lambda F: {0x61, 0x62} <= F.char_cmp and F.has(r"\[rbx \+ 0x74\], 7$") and F.has(r"\[rbx \+ 0x74\], 8$")),
    ("'c' ctrl escape: isctype alpha (mask 0x103) and _Char % 32", lambda F: 0x63 in F.char_cmp and F.has(r"mov +eax, 0x103") and F.has(r"and +eax, 0x8000001f")),
    ("'x' -> _HexDigits(2), 'u' -> _HexDigits(4) (002080D0)", lambda F: {0x78, 0x75} <= F.char_cmp and 0x2080D0 in F.callset and F.has(r"mov +edx, 4")),
    ("flags _L_esc_ffn 0x10000 _L_esc_ffnx 0x8000 _L_esc_ctrl 0x40000 _L_esc_hex 0x1000 _L_esc_uni 0x800 _L_esc_oct 0x2000",
        lambda F: {0x10000, 0x8000, 0x40000, 0x1000, 0x800, 0x2000} <= F.lflag_masks),
    ("_Val > 0xFF (numeric_limits<unsigned char>::max) -> error_escape", lambda F: F.has(r"cmp +dword ptr \[rbx \+ 0x74\], 0xff")),
    ("else tail-jump _IdentityEscape (002081A0)", lambda F: 0x2081A0 in F.tailjmps),
 ]),
 0x206890: ("_Parser::_ClassEscape(bool)", "high", [
    ("_L_esc_bsl(0x4000) && _Char=='\\\\' -> _Val='\\\\', return _Prs_chr(1)", lambda F: 0x4000 in F.lflag_masks and 0x5c in F.char_cmp and F.has(r"\[rcx \+ 0x74\], 0x5c")),
    ("_L_esc_wsd(0x20000) && _CharacterClassEscape -> return _Prs_set(2)", lambda F: 0x20000 in F.lflag_masks and 0x206340 in F.callset and F.has(r"mov +eax, 2")),
    ("_DecimalDigits then _Val!=0 -> error_escape(2)", lambda F: 0x206C20 in F.callset and 2 in F.xerr),
    ("fallback _CharacterEscape ? 1 : 0", lambda F: 0x206430 in F.callset and F.has(r"setne +cl")),
    ("caller is _ClassAtom (00206640)", lambda F: CALLERS.get(F.addr) == {0x206640}),
 ]),
 0x206960: ("_Parser::_ClassRanges()", "high", [
    ("loops on _ClassAtom (00206640), ret 2=_Prs_set skipped", lambda F: F.text.count("call 0x206640") == 3 and F.has(r"cmp +eax, 2")),
    ("_Val==0 && !_L_bzr_chr(0x100000) -> error_escape(2)", lambda F: 0x100000 in F.lflag_masks and 2 in F.xerr),
    ("_Mchar == '-' range", lambda F: 0x2d in F.mchar_cmp),
    ("collate(0x800 in _Flags) -> translate both ends (0020B000)", lambda F: F.has(r"test +dword ptr \[rbx \+ 0x70\], 0x800") and F.text.count("call 0x20b000") == 2),
    ("error_range(8) twice (set after dash; hi<lo)", lambda F: F.xerr.count(8) == 2),
    ("_Add_range(00205330) and _Add_char_to_class(00204F00) incl. literal '-'", lambda F: {0x205330, 0x204F00} <= F.callset and F.has(r"mov +dl, 0x2d")),
 ]),
 0x206CD0: ("_Builder::_Discard_pattern() (inlined _Destroy_node(_Root); _Root=0)", "high", [
    ("walks list from *this: tmp=nx; nx=nx->_Next(+0x10); tmp->_Next=0; delete via vtable slot0 (edx=1)", lambda F: F.has(r"mov +rbx, qword ptr \[rcx\]") and F.has(r"lea +rax, \[rbx \+ 0x10\]") and F.has(r"mov +edx, 1\n.*mov +qword ptr \[rax\], rdi") and F.has(r"call +qword ptr \[rax\]")),
    ("stores 0 to [this+0] (_Root = 0) on both paths", lambda F: F.text.count("qword ptr [rsi], rdi") + F.text.count("qword ptr [rcx], rdi") == 2),
    ("no _Refs decrement (distinguishes basic_regex::_Tidy)", lambda F: not F.has(r"lock")),
    ("only caller is a catch funclet (008996A0): (&_Parser + 0x40 = &_Nfa)->this, then _CxxThrowException(0,0) rethrow; EH parent = _Parser::_Compile (00206AD0)", funclet_discards_nfa),
 ]),
 0x206F60: ("_Matcher::_Do_class(_Node_base*)", "high", [
    ("_Sflags(+0xB8) icase(0x100) -> tolower via _Traits(+0xD0)", lambda F: F.has(r"test +dword ptr \[rcx \+ 0xb8\], 0x100") and TOLOWER in F.imports),
    ("_Coll(+0x20) -> _Lookup_coll(00203520) against _End(+0xA0)", lambda F: F.has(r"qword ptr \[rsi \+ 0x20\]") and 0x203520 in F.callset and F.has(r"\[rbx \+ 0xa0\]")),
    ("_Ranges(+0x38) with collate(0x800) translate; inline _Lookup_range pair loop (+2)", lambda F: F.has(r"cmp +qword ptr \[rsi \+ 0x38\], 0") and F.has(r"test +dword ptr \[rbx \+ 0xb8\], 0x800") and F.has(r"add +edx, 2")),
    ("_Small(+0x28) bitmap _Find (shr 3 / and 7)", lambda F: F.has(r"qword ptr \[rsi \+ 0x28\]") and F.has(r"shr +rax, 3") and F.has(r"and +ecx, 7")),
    ("_Found == (_Flags(+0xC) & _Fl_negate) -> false; else _Tgt_state._Cur = _Res0", lambda F: F.has(r"mov +eax, dword ptr \[rsi \+ 0xc\]\n.*and +eax, 1") and F.has(r"mov +qword ptr \[rbx\], r14")),
    ("_Large/_Classes/_Equiv arms absent (dead for char: _Ch < _Bmp_max always)", lambda F: not F.has(r"\[rsi \+ 0x30\]") and not F.has(r"\[rsi \+ 0x48\]")),
 ]),
 0x2070A0: ("_Parser::_Do_ex_class(_Meta_type)", "high", [
    ("_Errtype: ':'->ctype(1) '='->collate(0) '.'->collate(0) else syntax(0xE)", lambda F: F.has(r"cmp +edx, 0x3a") and F.has(r"cmp +esi, 0x3d") and F.has(r"cmp +esi, 0x2e") and F.has(r"mov +ebp, 0xe")),
    ("scan loop stops at : = . eos (bitmask 0x4000800000000001 over _Mchar+1)", lambda F: F.has(r"movabs +r15, 0x4000800000000001") and 0x3a in F.mchar_cmp),
    ("':' -> lookup_classname(00203A30) with icase bit; 0 -> error; _Add_elts(00205030)", lambda F: {0x203A30, 0x205030} <= F.callset and F.has(r"shr +r9d, 8")),
    ("'=' -> _Add_equiv(00205120); '.' -> _Char_to_elts(002061A0) on &_Current->_Coll (+0x20)", lambda F: {0x205120, 0x2061A0} <= F.callset and F.has(r"add +rax, 0x20")),
    ("_Beg==_Pat -> error_collate(0) (xor ecx,ecx) twice", lambda F: F.xerr.count(0) == 2),
    ("_Next then _Expect(_Meta_rsq, _Errtype) inline; tail _Trans", lambda F: 0x5d in F.mchar_cmp and F.has(NEXT_IDIOM) and F_TRANS in F.tailjmps),
 ]),
 0x207B40: ("_Matcher::_Do_rep(_Node_rep*, bool, int)", "high", [
    ("_Simple_loop(+0x34)==1 -> _Do_rep0 (00207720)", lambda F: F.has(r"cmp +dword ptr \[rdx \+ 0x34\], 1") and 0x207720 in F.callset),
    ("_Loop_vals(+0x80)[_Loop_number(+0x30)] with 16-byte _Loop_vals_t", lambda F: F.has(r"mov +r14d, dword ptr \[rbx \+ 0x30\]\n.*shl +r14, 4\n.*add +r14, qword ptr \[rdi \+ 0x80\]")),
    ("_Max(+0x24) >= 0 && _Max <= _Init_idx; _Init_idx < _Min(+0x20)", lambda F: F.has(r"mov +eax, dword ptr \[rbx \+ 0x24\]\n.*test +eax, eax\n.*js") and F.has(r"cmp +r15d, dword ptr \[rbx \+ 0x20\]")),
    ("recursion into _Match_pat(00208710) on _Next and _End_rep->_Next", lambda F: F.text.count("call 0x208710") >= 4 and F.has(r"mov +rdx, qword ptr \[rbx \+ 0x28\]\n.*mov +rdx, qword ptr \[rdx \+ 0x10\]")),
    ("!_Progress && 1 < _Init_idx", lambda F: F.has(r"cmp +r15d, 1\n.*jg")),
    ("state restore via vector operator= (00204820/00204950)", lambda F: {0x204820, 0x204950} <= F.callset),
 ]),
 0x2080D0: ("_Parser::_HexDigits(int) (with _Do_digits(16,n) and regex_traits<char>::value(ch,16) inlined)", "high", [
    ("_Val = 0 on entry", lambda F: F.has(r"mov +dword ptr \[rcx \+ 0x74\], 0")),
    ("value(): '0'-'9' (-0x30), 'a'-'f' (-0x57), 'A'-'F' (-0x37); no base-8 branch", lambda F: F.has(r"sub +eax, 0x30") and F.has(r"sub +eax, 0x57") and F.has(r"sub +eax, 0x37") and not F.has(r"cmp +\w+, 7\b")),
    ("_Val = _Val*16 + digit", lambda F: F.has(r"shl +ecx, 4")),
    ("count left != 0 -> error_escape(2)", lambda F: F.xerr == [2]),
    ("_Next inline + _Trans", lambda F: F.has(NEXT_IDIOM) and F_TRANS in F.callset),
    ("called only from _CharacterEscape with 2 or 4", lambda F: CALLERS.get(F.addr) == {0x206430}),
 ]),
 0x2085B0: ("_Parser::_IsIdentityEscape() const", "high", [
    ("_L_ident_ECMA(0x400000) switch on _Char", lambda F: 0x400000 in F.lflag_masks),
    ("ECMA table (byte idx 0x208630 -> dword 0x208628, referenced by this body): c d D s S w W -> false, other chars -> true", lambda F: JT_ECMA_OK and F.has(r"\+ 0xe8630\]") and F.has(r"\+ 0xe8628\]")),
    ("POSIX table: . [ \\ * | ^ $ -> true; ( ) + ? { } -> _L_ident_ERE(bit 23); \" / -> _L_ident_awk(bit 24)", lambda F: JT_POSIX_OK and F.has(r"\+ 0xe8674\]") and F.has(r"\+ 0xe8664\]")),
    ("reached only via _IdentityEscape (002081A0)", lambda F: CALLERS.get(F.addr) == {0x2081A0}),
 ]),
 0x208710: ("_Matcher::_Match_pat(_Node_base*)", "high", [
    ("_Max_stack_count(+0xE0) -> error_stack(0xC); _Max_complexity_count(+0xDC) -> error_complexity(0xB); default -> error_parse(0xD)", lambda F: {0xC, 0xB, 0xD} <= set(F.xerr)),
    ("switch over _Kind-1 with 21 cases (_N_nop.._N_end)", lambda F: F.has(r"lea +eax, \[rdx - 1\]\n.*cmp +eax, 0x14")),
    ("word-char strchr string (_Is_wc inlined)", lambda F: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_" in F.strs),
    ("_N_str -> _Compare(002032E0), _N_class -> _Do_class(00206F60), _N_rep -> _Do_rep(00207B40), _N_if -> _Do_if", lambda F: JT_MATCHPAT_OK and F.has(r"\+ 0xe8c0c\]") and {0x2032E0, 0x206F60, 0x207B40} <= F.callset),
    ("dot fails on '\\n' and '\\r'", lambda F: F.has(r"cmp +cl, 0xa") and F.has(r"cmp +cl, 0xd")),
 ]),
 0x208DE0: ("_Parser::_Quantifier()", "high", [
    ("_Mchar * + ? {", lambda F: {0x2a, 0x2b, 0x3f, 0x7b} <= F.mchar_cmp),
    ("_Min=0,_Max=-1 defaults; '+' -> _Min=1; '?' -> _Max=1", lambda F: F.has(r"or +edi, 0xffffffff") and F.has(r"lea +esi, \[rdi \+ 2\]") and F.has(r"lea +edi, \[rax - 0x3e\]")),
    ("{m,n}: _DecimalDigits(00206C20), ',' and '}' checks, error_badbrace(7) x3", lambda F: 0x206C20 in F.callset and {0x2c, 0x7d} <= F.mchar_cmp and F.xerr.count(7) == 3),
    ("_Mark_final inline: or [_Current+0xC], 4 (_Fl_final)", lambda F: F.has(r"or +dword ptr \[rax \+ 0xc\], 4")),
    ("_L_ngr_rep(0x400) && '?' -> _Add_rep(min,max,false) else true (002054D0)", lambda F: 0x400 in F.lflag_masks and 0x2054D0 in F.callset and F.has(r"xor +r9d, r9d") and F.has(r"mov +r9b, 1")),
 ]),
 0x209360: ("basic_regex<char>::_Tidy()", "high", [
    ("_MT_DECR on _Rep->_Refs (+0x2C): lock xadd -1, old==1 -> destroy", lambda F: F.has(r"lock xadd +dword ptr \[rcx \+ 0x2c\], eax") and F.has(r"cmp +eax, 1")),
    ("inlined _Destroy_node walk (+0x10 next, delete via vtable)", lambda F: F.has(r"lea +rax, \[rbx \+ 0x10\]") and F.has(r"call +qword ptr \[rax\]")),
    ("_Rep = 0 on both paths", lambda F: F.text.count("mov qword ptr [rsi], rdi") == 2),
 ]),
 0x209840: ("_Parser::_Wrapped_disjunction()", "high", [
    ("++_Disj_count(+0x1C) on entry, -- on every exit", lambda F: F.has(r"inc +dword ptr \[rcx \+ 0x1c\]") and F.text.count("dec dword ptr [rsi + 0x1c]") == 5),
    ("!_L_empty_grp(bit 27) && ')' -> error_paren(5)", lambda F: 0x8000000 in F.lflag_masks and 0x29 in F.mchar_cmp and 5 in F.xerr),
    ("_L_nc_grp(0x20) && '?' then ':' '!' '=' else error_syntax(0xE)", lambda F: 0x20 in F.lflag_masks and F.has(r"cmp +ebx, 0x3a") and F.has(r"cmp +ebx, 0x21") and F.has(r"cmp +ebx, 0x3d") and 0xE in F.xerr),
    ("_Do_assert_group(true/false) (00206E90) returning false", lambda F: F.text.count("call 0x206e90") == 2),
    ("nosubs(0x200 in _Flags) -> inline _Do_noncapture_group: _New_node(_N_group=8), _Disjunction(00206D30), _End_group(00207E90)", lambda F: F.has(r"test +dword ptr \[rcx \+ 0x70\], 0x200") and F.has(r"mov +edx, 8\n(?:.*\n){0,3}.*call +0x208c60") and {0x206D30, 0x207E90} <= F.callset),
    ("else _Do_capture_group (00206EE0)", lambda F: 0x206EE0 in F.callset),
 ]),
 0x209CD0: ("std::collate<char>::do_transform(const char*, const char*) const  [<locale>, not <regex>]", "high", [
    ("is slot 4 (do_transform) of the .?AV?$collate@D@std@@ vtable", lambda F: any(img.q(v + 8 * 4) == F.addr for v in COLLATE_VT)),
    ("calls _Strxfrm with &_Coll (this+0x10)", lambda F: STRXFRM in F.imports and F.has(r"lea +rbp, \[rcx \+ 0x10\]")),
    ("string result: SSO capacity 0xF init, resize helper (00195CF0)", lambda F: F.has(r"mov +qword ptr \[rdx \+ 0x18\], 0xf") and 0x195CF0 in F.callset),
 ]),
 0x209E00: ("std::vector<bool>::erase(const_iterator, const_iterator) (reached from vector<bool>::resize shrink)", "high", [
    ("_Make_iter guard: if (0 < _Mysize) (test [this+0x18])", lambda F: F.has(r"mov +rdi, qword ptr \[rcx \+ 0x18\]") and F.has(r"test +rdi, rdi")),
    ("iterator arithmetic over 32-bit words: shl 5 / shr 5 / and 0x1f", lambda F: F.has(r"shl +r\w+, 5") and F.has(r"shr +r\w+, 5") and F.has(r"and +r\w+, 0x1f")),
    ("bit-copy loop (bts/btr)", lambda F: F.has(r"\bbts\b") and F.has(r"\bbtr\b")),
    ("then _Trim (00209780) and begin()+_Off (00204A80)", lambda F: {0x209780, 0x204A80} <= F.callset),
 ]),
 0x203490: ("_Buf<char>::_Insert<const char*>(const char*, const char*) (range insert; _Insert(ch)/_Expand inlined)", "high", [
    ("loop over [first,last)", lambda F: F.has(r"cmp +rdx, r8\n.*je") and F.has(r"cmp +rdi, r14\n.*jne")),
    ("_Sz <= _Nchrs -> realloc(_Chrs, _Nchrs+16) (_Buf_incr=16), null -> _Xbad_alloc", lambda F: F.has(r"lea +ebp, \[rax \+ 0x10\]") and REALLOC in F.imports and XBADALLOC in F.imports),
    ("_Chrs[_Nchrs++] = ch  (layout _Sz 0, _Nchrs 4, _Chrs 8)", lambda F: F.has(r"inc +dword ptr \[rbx \+ 4\]")),
    ("sole caller _Builder::_Char_to_elts (002061A0)", lambda F: CALLERS.get(F.addr) == {0x2061A0}),
 ]),
 0x204E50: ("_Builder::_Add_char_to_array(char)", "high", [
    ("_Flags(+0x10) & icase(0x100) -> translate_nocase via _Traits(+0x18)->_Pctype", lambda F: F.has(r"test +dword ptr \[rcx \+ 0x10\], 0x100") and F.has(r"mov +rax, qword ptr \[rcx \+ 0x18\]") and TOLOWER in F.imports),
    ("_Current(+8)->_Large(+0x30): new _Buf<char> (0x10) zero-initialised", lambda F: F.has(r"cmp +qword ptr \[rbx \+ 0x30\], 0") and F.new_sizes == [0x10]),
    ("_Large->_Insert(ch): realloc +16 / _Xbad_alloc", lambda F: REALLOC in F.imports and F.has(r"lea +esi, \[rax \+ 0x10\]")),
 ]),
 0x205330: ("_Builder::_Add_range(char, char)", "high", [
    ("icase -> translate_nocase both ends, sign-extended (movsx) as in `_E0 = translate_nocase((_Elem)_E0)`", lambda F: F.imports.count(TOLOWER) == 2 and F.text.count("movsx") >= 2),
    ("bitmap loop while _E0<=_E1 && _E1 < _Bmax(+0x20); _Small(+0x28) new _Bitmap (0x20)", lambda F: F.has(r"cmp +edi, dword ptr \[rbp \+ 0x20\]") and F.has(r"\[rsi \+ 0x28\]") and 0x20 in F.new_sizes),
    ("_E1 - _E0 < _Tmax(+0x24) -> _Add_char_to_array (00204E50) loop", lambda F: F.has(r"cmp +eax, dword ptr \[rbp \+ 0x24\]") and 0x204E50 in F.callset),
    ("else _Ranges(+0x38) new _Buf (0x10), insert _E0 then _E1", lambda F: F.has(r"\[rsi \+ 0x38\]") and 0x10 in F.new_sizes and F.imports.count(REALLOC) == 2),
    ("caller _Parser::_ClassRanges (00206960)", lambda F: CALLERS.get(F.addr) == {0x206960}),
 ]),
}


# ---------------------------------------------------------------- caller index (raw, image-wide E8/E9/jcc from capstone text cache)
def build_callers():
    cache = os.environ.get("Y1P_CACHE", os.path.join(os.path.dirname(HERE), "y1p_all.txt"))
    want ={"%x" % a for a in TARGETS}
    out = {}
    rx = re.compile(r"^([0-9A-F]{8}) ([0-9A-F]{8}) (call|jmp|j[a-z]+) 0x([0-9a-f]+)$")
    with open(cache) as f:
        for line in f:
            m = rx.match(line.rstrip())
            if m and m.group(4) in want:
                tgt = int(m.group(4), 16)
                src = int(m.group(2), 16)
                if src != tgt:
                    out.setdefault(tgt, set()).add(src)
    return out


CALLERS = build_callers()

# jump tables (decoded from the image, not assumed)
# 002085B0: ECMA arm: idx = _Char - 0x44, 0x34 entries, byte table 0x208630 -> dword table 0x208628
ecma = jump_table(0, 0xE8630, 0xE8628, 0x34, 0x44)
ret_false = {t for t in ecma.values()}  # classify by target
ecma_targets = {}
for ch, t in ecma.items():
    ecma_targets.setdefault(t, []).append(chr(ch))
# the default arm (mov al,1) is at 002085E7
JT_ECMA_OK = False
non_default = [t for t in ecma_targets if t != 0x2085E7]
if len(non_default) == 1:
    JT_ECMA_OK = sorted(ecma_targets[non_default[0]]) == sorted("cdDsSwW") and img.read(non_default[0], 2) == b"\x32\xc0"
posix = jump_table(0, 0xE8674, 0xE8664, 0x5C, 0x22)
posix_targets = {}
for ch, t in posix.items():
    posix_targets.setdefault(t, []).append(chr(ch))
JT_POSIX = {("%08X" % t): "".join(v) for t, v in posix_targets.items()}
def _first_ins(t):
    i = img.disasm(t, 16)[0]
    return i.mnemonic + " " + i.op_str
JT_POSIX_DESC = {("%08X" % t): (_first_ins(t), "".join(v)) for t, v in posix_targets.items()}
JT_POSIX_OK = (sorted(posix_targets.get(0x208611, [])) == sorted("()+?{}")
               and sorted(posix_targets.get(0x20861B, [])) == sorted('"/')
               and sorted(posix_targets.get(0x2085E7, [])) == sorted(".[\\*|^$"))

mp = word_table(0xE8C0C, 0x15, 1)   # _Match_pat: kind 1..21
def _calls_in_arm(t, n=0x60):
    return [branch_target(i) for i in img.disasm(t, n) if i.mnemonic == "call" and branch_target(i)]
JT_MATCHPAT = {k: "%08X" % v for k, v in mp.items()}
JT_MATCHPAT_OK = (0x2032E0 in _calls_in_arm(mp[6]) and 0x206F60 in _calls_in_arm(mp[7])
                  and 0x207B40 in _calls_in_arm(mp[18]) and len(set(mp.values())) >= 12)


def run_spec(a, F):
    name, conf, checks = SPECS[a]
    res = []
    for d, p in checks:
        try:
            ok = bool(p(F))
        except Exception as e:  # a crashing check is a failed check
            ok = False
        res.append((d, ok))
    return res


def main():
    out = []
    P = out.append
    P("# regex_match.py output  (image base 0x%X)" % img.base)
    P("Imports: _Xregex_error=%08X ctype<char>::tolower=%08X realloc=%08X _Strxfrm=%08X" % (XREGEX, TOLOWER, REALLOC, STRXFRM))
    P("\n## RTTI: <regex> node vtables (COL-resolved)")
    for va in sorted(REGEX_VT):
        P("  %08X %-55s slot0(scalar deleting dtor)=%08X" % (va, REGEX_VT[va], img.q(va)))
    for v in COLLATE_VT:
        P("  %08X .?AV?$collate@D@std@@ slots: %s" % (v, " ".join("%08X" % img.q(v + 8 * k) for k in range(6))))

    # vtable installers image-wide (context: the 19 functions in 002043A0..00208C60)
    P("\n## Functions that lea a <regex> node vtable (image-wide, from functions.tsv bodies in .text span 00200000-0020C000)")
    inst = {}
    for a in sorted(SIZES):
        if not (0x200000 <= a < 0x20C000):
            continue
        F = Feat(a)
        if F.vt_lea:
            inst[a] = F
    for a, F in inst.items():
        P("  %08X size=%-5d vtables=%s new_sizes=%s" % (a, F.size, sorted(set(v.replace(".?AV", "").replace("@std@@", "") for v in F.vt_lea)), F.new_sizes))
    P("  count=%d" % len(inst))

    # C4 planted positive: extractor sensitivity
    k = Feat(0x205890)
    assert set(k.xerr) == {4, 5, 6, 10}, ("extractor failed planted positive", k.xerr)
    assert 0x10000000 in k.lflag_masks and 0x7c in k.mchar_cmp
    k2 = Feat(0x208C60)
    assert k2.new_sizes == [0x20] and k2.vt_lea == [".?AV_Node_base@std@@"], (k2.new_sizes, k2.vt_lea)
    P("\n## C4 planted positives: extractor finds error codes {4,5,6,10} in 00205890 and new(0x20)+_Node_base vtable in 00208C60: OK")

    P("\n## Jump tables decoded from the image")
    P("  002085B0 ECMA arm targets: %s" % {("%08X" % t): "".join(v) for t, v in ecma_targets.items()})
    P("  002085B0 POSIX arm targets (first instruction, chars): %s" % JT_POSIX_DESC)
    P("  00208710 _Match_pat kind->arm: %s" % JT_MATCHPAT)

    feats = {a: Feat(a) for a in TARGETS}
    P("\n## Per-function evidence")
    rows = []
    for a in TARGETS:
        F = feats[a]
        name, conf, checks = SPECS[a]
        res = run_spec(a, F)
        npass = sum(ok for d, ok in res)
        final_conf = conf if npass == len(res) else ("medium" if npass >= len(res) - 1 else "unmatched")
        final_name = name if final_conf != "unmatched" else "unmatched"
        P("\n### %08X size=%d%s -> %s  [%s, %d/%d checks]" % (a, F.size, " (allocator-labelled)" if a in ALLOC_LABELLED else "", final_name, final_conf, npass, len(res)))
        P("  callers(raw index): %s" % ", ".join("%08X" % c for c in sorted(CALLERS.get(a, set()))) or "none")
        P("  callees: %s" % ", ".join("%08X" % c for c in sorted(F.callset)))
        P("  imports: %s" % sorted(set(IMP[i].split("!")[1] for i in F.imports)))
        P("  Xregex_error codes: %s  new sizes: %s  vtables: %s" % (F.xerr, F.new_sizes, F.vt_lea))
        P("  _Mchar cmps: %s  _Char cmps: %s  _L_flags masks: %s" % (
            sorted("%s" % (repr(chr(x)) if 0x20 <= x < 0x7f else x) for x in F.mchar_cmp),
            sorted(repr(chr(x)) for x in F.char_cmp if 0 <= x < 0x80),
            sorted("0x%X" % m for m in F.lflag_masks)))
        for d, ok in res:
            P("  [%s] %s" % ("PASS" if ok else "FAIL", d))
        summ = "; ".join(d for d, ok in res if ok)
        rows.append((a, F.size, final_name, final_conf, summ))

    # C1 confusion matrix
    P("\n## C1 confusion matrix: spec (row) x function (col); cell = checks passed / total; '*' = full pass")
    hdr = "          " + " ".join("%04X" % (a & 0xFFFF) for a in TARGETS)
    P(hdr)
    fullpass_off_diag = []
    for s in TARGETS:
        cells = []
        for a in TARGETS:
            res = run_spec(s, feats[a])
            n = sum(ok for d, ok in res)
            full = n == len(res)
            if full and s != a:
                fullpass_off_diag.append((s, a))
            cells.append(("  * " if full else "%d/%d" % (n, len(res))).rjust(4))
        P("  %04X    %s" % (s & 0xFFFF, " ".join(cells)))
    P("  off-diagonal full passes: %s" % (fullpass_off_diag or "none"))

    # C2 negative sample
    rnd = random.Random(20260927)
    pool = [a for a in SIZES if not (0x200000 <= a < 0x20C000) and 60 <= SIZES[a] <= 1500 and img.sec_of(a) == ".text"]
    sample = rnd.sample(pool, 200)
    worst = []
    full_neg = []
    for a in sample:
        try:
            F = Feat(a)
        except Exception:
            continue
        for s in TARGETS:
            res = run_spec(s, F)
            n = sum(ok for d, ok in res)
            if n == len(res):
                full_neg.append((s, a))
            worst.append((n / len(res), s, a))
    worst.sort(reverse=True)
    P("\n## C2 negative sample: 200 random .text functions outside 00200000-0020C000 (seed 20260927), all 24 specs")
    P("  full passes: %s" % (full_neg or "none"))
    P("  highest partial scores: %s" % ", ".join("spec %08X on %08X = %.2f" % (s, a, f) for f, s, a in worst[:5]))

    # C3 image-wide sweeps from the text cache
    cache = os.environ.get("Y1P_CACHE", os.path.join(os.path.dirname(HERE), "y1p_all.txt"))
    xr, tl, mch = set(), set(), set()
    with open(cache) as f:
        for line in f:
            if "=>%08X" % XREGEX in line and " call " in line:
                xr.add(int(line[9:17], 16))
            if "=>%08X" % TOLOWER in line and " call " in line:
                tl.add(int(line[9:17], 16))
            if re.search(r" cmp dword ptr \[r\w+ \+ 0x7c\], (0x7c|0x29|0x5b|0x5d|0x7b|0x7d)$", line):
                mch.add(int(line[9:17], 16))
    def span(s):
        ins = sorted(x for x in s if 0x200000 <= x < 0x20C000)
        out_ = sorted(x for x in s if not (0x200000 <= x < 0x20C000))
        return "%d inside 00200000-0020C000, %d outside %s" % (len(ins), len(out_), ["%08X" % x for x in out_][:20])
    P("\n## C3 image-wide sweeps (all functions in the 1.79M-line disassembly cache)")
    P("  functions calling _Xregex_error: " + span(xr))
    P("  functions calling ctype<char>::tolower: " + span(tl))
    P("  functions comparing dword [reg+0x7c] with | ) [ ] { }: " + span(mch))
    # inline _Next idiom: sub al,0x28 / cmp al,1 ... sub al,0x7b / test al,0xfd
    idiom = set()
    lines_by_f = {}
    with open(cache) as f:
        prev = []
        for line in f:
            if line.endswith("sub al, 0x7b\n"):
                idiom.add(int(line[9:17], 16))
    P("  functions containing 'sub al, 0x7b' (the _Is_esc '{'/'}' test inside inlined _Next): " + span(idiom))

    with open(os.path.join(HERE, "regex-members.tsv"), "w", newline="\n") as f:
        f.write("address\tsize\tidentified_vs2015_function\tconfidence\tevidence_summary\n")
        for a, sz, n, c, s in rows:
            f.write("%08X\t%d\t%s\t%s\t%s\n" % (a, sz, n, c, s.replace("\t", " ")))
    counts = {}
    for r in rows:
        counts[r[3]] = counts.get(r[3], 0) + 1
    P("\n## Counts: %s" % counts)
    print("\n".join(out))


if __name__ == "__main__":
    main()
