# VS2015 `<regex>` identification of 24 FFXII_TZA.exe functions

Date: 2026-09-27. Read-only; nothing under `C:\Users\Kristian\source\repos` was written.

Files in this folder:
- `regex_match.py`: re-runnable (`python regex_match.py`, about 3 s). It prints the evidence for each function, a confusion matrix, a negative sample and image-wide sweeps, and writes `regex-members.tsv`.
- `regex_match.out`: the last run's output.
- `regex-members.tsv`: one row per function, with address, size, identification, confidence and the checks that passed.
- `pelib.py`: section-aware PE reader, capstone wrapper and RTTI resolver.
- `dump.py ADDR`: annotated disassembly (vtables, imports and strings resolved).
- `eh_parent.py ADDR`: walks the x64 EH metadata from a catch funclet back to its parent function.

Header used: `C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\include\regex` (V6.50:0009). The binary matches this revision of the header:
- `_Match` (002035B0) sets `_Max_complexity_count = 0x989680`, which is 10000000 (`_REGEX_MAX_COMPLEXITY_COUNT`).
- It sets `_Max_stack_count = 0x258`, which is 600 (the `_WIN64` value of `_REGEX_MAX_STACK_COUNT`).
- `_Match_pat` throws `error_stack` (0xC) and `error_complexity` (0xB) from these two counters.

## RTTI (COL-resolved; every node vtable has a single slot, the scalar deleting destructor)

| vtable | class | dtor |
|---|---|---|
| 009058C0 | `_Node_base` | 00204C10 |
| 009058D0 | `_Root_node` | 00204CE0 |
| 009058E0 | `_Node_end_group` | 00204C40 |
| 009058F0 | `_Node_assert` | 00204BD0 |
| 00905900 | `_Node_capture` | 00204C40 |
| 00905910 | `_Node_back` | 00204C40 |
| 00905920 | `_Node_endif` | 00204C10 |
| 00905930 | `_Node_if` | 00204C70 |
| 00905940 | `_Node_end_rep` | 00204C40 |
| 00905950 | `_Node_rep` | 00204CB0 |
| 009059D8 | `_Node_str<char>` | 00204B30 |
| 00905A28 | `_Node_class<char,regex_traits<char>>` | 00204AF0 |
| 00905888 | `collate<char>` | slots: dtor 00204B80, do_compare 00209C40 (`_Strcoll`), **do_transform 00209CD0**, do_hash 00209C90 (FNV-1a constants) |

The linker's identical-COMDAT folding merged some destructors:
- 00204C40 serves four node classes: end_group, capture, back and end_rep.
- 00204C10 serves `_Node_base` and `_Node_endif`.

So a destructor address alone does not name a class.

In 00200000-0020C000, 20 functions `lea` a node vtable. 19 of them lie in 002043A0..00208C60, which matches the brief. The 20th is 00203F70, which does `new 0x30` and installs `_Root_node` (the `_Builder` constructor path). **None of the 24 targets installs a vtable.** They are parser, matcher, builder and library members, not node constructors.

## Layouts used (x64, computed from the header, each confirmed by at least one access in the code)

- **`_Parser<const char*,char,regex_traits<char>>`:**
  - `_Pat` 0, `_End` 0x10, `_Grp_idx` 0x18, `_Disj_count` 0x1C.
  - `_Finished_grps` 0x20 (`_Mysize` 0x38).
  - `_Nfa` 0x40 (`_Current` 0x48).
  - `_Traits` 0x68, `_Flags` 0x70, `_Val` 0x74, `_Char` 0x78, `_Mchar` 0x7C, `_L_flags` 0x80.
- **`_Builder`:** `_Root` 0, `_Current` 8, `_Flags` 0x10, `_Traits` 0x18, `_Bmax` 0x20, `_Tmax` 0x24.
- **`_Matcher`:**
  - `_Tgt_state` 0 (`_Cur` 0, `_Grp_valid` 8, `_Grps` 0x28).
  - `_Loop_vals` 0x80, `_Begin` 0x98, `_End` 0xA0.
  - `_Sflags` 0xB8, `_Mflags` 0xBC, `_Traits` 0xD0.
  - Complexity counter 0xDC, stack counter 0xE0.
- **Nodes:**
  - `_Node_base` is 0x20 bytes (`_Kind` 8, `_Flags` 0xC, `_Next` 0x10).
  - `_Node_class`: `_Coll` 0x20, `_Small` 0x28, `_Large` 0x30, `_Ranges` 0x38.
  - `_Node_rep`: `_Min` 0x20, `_Max` 0x24, `_End_rep` 0x28, `_Loop_number` 0x30, `_Simple_loop` 0x34.
  - `_Root_node::_Refs` is at 0x2C.
- **Allocation sizes:** `_Bitmap` = 0x20, `_Buf<char>` = 0x10. Both sizes are seen at `new` (00210EC0) call sites.

## Results (all 24: high; 0 medium, 0 low, 0 unmatched)

| addr | identification | key evidence |
|---|---|---|
| 00203240 | `_Cmp_chrange<const char*,const char*,_Cmp_icase<regex_traits<char>>>` | 2× `ctype<char>::tolower` per step; returns saved `_Begin1` on mismatch, `cmove` on `_Begin2==_End2`; entered from `_Compare` (002032E0) `bt flags,8` (icase) |
| 00203980 | `std::equal` (4 iterators + pred) with `_Cmp_icase<_Regex_traits<char>>`, random-access path | length compare first, then tolower==tolower loop; the pred holds the traits pointer (`[traits+8]` = `_Pctype`); sole caller 00203A30 = `lookup_classname` (walks `_Names`, `or bx,3` = lower\|upper on icase). Whether the out-of-line body is `equal` or the inner `_Equal_unchecked` cannot be told apart; both compile to this. |
| 00204820 | `vector<unsigned int>::operator=` (the `_Myvec` of `vector<bool>`, i.e. `_Grp_valid = ...`) | self-assign guard, 3 memmove paths, element size 4. In `_Do_rep` it is called on `&_Tgt_state._Grp_valid`, with `_Mysize` copied separately just before. The element type comes from the call sites. |
| 00204950 | `vector<_Tgt_state_t<const char*>::_Grp_t>::operator=` | same shape, element size 16; called on `&_Tgt_state._Grps` (+0x28) |
| 00205890 | `_Parser::_Alternative()` | see note 1 |
| 00205B40 | `_Parser::_AtomEscape()` | see note 2 |
| 00206430 | `_Parser::_CharacterEscape()` | see note 3 |
| 00206890 | `_Parser::_ClassEscape(bool)` | `_L_esc_bsl` (0x4000) and `\\` gives `_Val=0x5C`, returns 1; `_L_esc_wsd` plus `_CharacterClassEscape` returns 2; `_DecimalDigits` and `_Val!=0` throws error_escape; otherwise `_CharacterEscape ? 1 : 0`. Caller is `_ClassAtom` (00206640). |
| 00206960 | `_Parser::_ClassRanges()` | see note 4 |
| 00206CD0 | `_Builder::_Discard_pattern()` | see note 5 |
| 00206F60 | `_Matcher::_Do_class` | icase gives tolower; `_Coll`, then `_Lookup_coll` (00203520); `_Ranges` with collate `translate`, then an inline pair loop; `_Small` bitmap test; negate compare against `_Flags&1`. The `_Large`/`_Classes`/`_Equiv` arms are not in the code: for `char`, `_Ch < _Bmp_max` is always true, so the compiler dropped them. |
| 002070A0 | `_Parser::_Do_ex_class(_Meta_type)` | see note 6 |
| 00207B40 | `_Matcher::_Do_rep(_Node_rep*,bool,int)` | `_Simple_loop==1` goes to `_Do_rep0` (00207720); `_Loop_vals[_Loop_number]` in 16-byte entries; `_Max`/`_Min`/`1 < _Init_idx` tests; ≥4 recursions into `_Match_pat` |
| 002080D0 | `_Parser::_HexDigits(int)` | `_Do_digits(16,n)` and `value(ch,16)` are inlined; there is no octal branch; `_Val = _Val*16 + d`; if count remains, throws error_escape. Called only from `_CharacterEscape`, with 2 or 4. |
| 002085B0 | `_Parser::_IsIdentityEscape() const` | jump tables decoded from the image: in the ECMA arm, `cdDsSwW` return false and the rest return true. In the POSIX arm, `. [ \ * \| ^ $` return true, `( ) + ? { }` return bit 23 (`_L_ident_ERE`) and `" /` return bit 24 (`_L_ident_awk`). |
| 00208710 | `_Matcher::_Match_pat` | stack counter throws 0xC, complexity counter 0xB, default arm 0xD; 21-way switch on `_Kind`; `_Is_wc` strchr word-char string; the `_N_str`, `_N_class`, `_N_if` and `_N_rep` arms call `_Compare`, `_Do_class`, `_Do_if` (00207310) and `_Do_rep` |
| 00208DE0 | `_Parser::_Quantifier()` | `* + ? {`; `_Min=0`, `_Max=-1` / 1 / 1; `{m,n}` throws error_badbrace (7) ×3; `_Mark_final` (`or [cur+0xC],4`); `_L_ngr_rep` (0x400) and `?` call `_Add_rep(..,false)` (002054D0) |
| 00209360 | `basic_regex<char>::_Tidy()` | `lock xadd [_Rep+0x2C],-1`; on old==1 the inline `_Destroy_node` runs; then `_Rep=0` |
| 00209840 | `_Parser::_Wrapped_disjunction()` | see note 7 |
| 00209CD0 | `std::collate<char>::do_transform` (**`<locale>`, not `<regex>`**) | slot 4 of the `collate<char>` vtable; `_Strxfrm` with `&_Coll` (this+0x10); grow/resize loop. It has no direct callers and is reached virtually from `regex_traits::translate`. |
| 00209E00 | `std::vector<bool>::erase(const_iterator,const_iterator)` (**`<vector>`**) | `_Make_iter` guard (`0 < _Mysize`); 32-bit-word iterator arithmetic; bts/btr copy loop; `_Trim`. Called from 0020A5C0 = `vector<bool>::resize`, which `_Match` and `_Do_capture_group` call. |
| 00203490 | `_Buf<char>::_Insert<const char*>(first,last)` | realloc `_Nchrs+16` (`_Buf_incr`), `_Xbad_alloc`; sole caller `_Char_to_elts` (002061A0) |
| 00204E50 | `_Builder::_Add_char_to_array(char)` | icase gives tolower; `_Current->_Large` (+0x30) gets `new _Buf` of 0x10; `_Insert` |
| 00205330 | `_Builder::_Add_range(char,char)` | see note 8 |

Notes for the longer rows:

1. **00205890 `_Parser::_Alternative()`**
   - `_Mchar` is compared with `\| ) . \ [ ( ^ $ * + ? { } ]`.
   - It throws exactly {4 brack, 5 paren, 6 brace, 10 badrepeat}.
   - `_New_node` is called with kinds 5 (dot), 4 (wbound), 2 (bol) and 3 (eol).
   - `\b` and `\B` are handled under `_L_asrt_wrd`; `_Negate` is `xor [cur+0xC],1`.
   - `_L_paren_bal` (0x10000000) gates `) } ]`.
2. **00205B40 `_Parser::_AtomEscape()`**
   - Tests the flags `_L_bckr`, `_L_bzr_chr`, `_L_lim_bckr` and `_L_esc_wsd`.
   - Checks `_Val>9` (`_BRE_MAX_GRP`), `_Grp_idx`, `_Finished_grps` size and bit.
   - Throws error_escape (2) and error_backref (3).
   - Tail-jumps to `_Add_backreference` (00204D10: new 0x28 `_Node_back`) and to `_Add_char`.
3. **00206430 `_Parser::_CharacterEscape()`**
   - eos throws error_escape.
   - Inline `_Do_ffn` maps f/n/r/t/v to 0xC/0xA/0xD/9/0xB; inline `_Do_ffnx` maps a/b to 7/8.
   - `c` uses `isctype` alpha (mask 0x103) and `%32`.
   - `x` and `u` call `_HexDigits(2)` and `_HexDigits(4)`; `_OctalDigits` follows.
   - `_Val > 0xFF` throws error_escape; otherwise it tail-calls `_IdentityEscape`.
4. **00206960 `_Parser::_ClassRanges()`**
   - Loops on `_ClassAtom`.
   - Handles `-` ranges; under collate, `translate` is called on both ends.
   - error_range (8) is thrown ×2.
   - Calls `_Add_range` and `_Add_char_to_class`, including a literal `-`.
5. **00206CD0 `_Builder::_Discard_pattern()`**
   - Inline `_Destroy_node` over `*this`, then `_Root=0`. There is no refcount, which rules out `basic_regex::_Tidy`.
   - Its only caller is catch funclet 008996A0. The funclet passes `&parser+0x40` (`&_Nfa`) and then `_CxxThrowException(0,0)` (rethrow).
   - The EH-metadata walk puts that funclet's parent at 00206AD0. That function is `_Parser::_Compile`: `_Begin_capture_group(0)`, `_Disjunction`, error_syntax, `_End_group`, `_New_node(_N_end=0x15)`, `_Fl`, `_Marks=_Grp_idx+1`, `_Calculate_loop_simplicity`.
6. **002070A0 `_Parser::_Do_ex_class(_Meta_type)`**
   - The error type is `:` gives ctype (1), `=` and `.` give collate (0), anything else gives syntax (0xE).
   - The scan loop uses bitmask 0x4000800000000001 over `_Mchar+1`, which covers eos, `.` and `=`.
   - `:` calls `lookup_classname` and `_Add_elts`. (For char, `_Add_named_class` reduces to `_Add_elts`.)
   - `=` calls `_Add_equiv`; `.` calls `_Char_to_elts(&_Current->_Coll)`.
   - Ends with an inline `_Expect(']')`.
7. **00209840 `_Parser::_Wrapped_disjunction()`**
   - `++_Disj_count` on entry, `--` on 5 exits.
   - `!_L_empty_grp` with `)` throws error_paren.
   - `_L_nc_grp` with `?` then handles `: ! =`; anything else throws error_syntax.
   - Calls `_Do_assert_group(true/false)` and returns false.
   - nosubs goes to an inline `_Do_noncapture_group` (`_New_node(8)`, `_Disjunction`, `_End_group`); otherwise it calls `_Do_capture_group`.
8. **00205330 `_Builder::_Add_range(char,char)`**
   - icase applies tolower to both ends, sign-extended (the `(_Elem)` cast in the source).
   - The bitmap loop runs while `_E1 < _Bmax`, with `new _Bitmap` of 0x20.
   - If `_E1-_E0 < _Tmax`, it calls `_Add_char_to_array` (00204E50).
   - Otherwise it does `new _Buf` of 0x10 at `_Ranges`, then inserts E0 and E1.
   - Its caller is `_ClassRanges`.

## Controls (see the matching sections of regex_match.out)

- **C1, confusion matrix:** each of the 24 specs was run against each of the 24 functions. The only full passes are on the diagonal (0 off-diagonal). The highest off-diagonal score is 3/4: the two `vector::operator=` specs against each other. They differ only in element size, and that one check separates them.
- **C2, negative sample:** 200 random `.text` functions outside 00200000-0020C000 (seed 20260927) were checked against all 24 specs. There were 0 full passes, and the best partial score was 0.25 (the generic "no lock prefix" check).
- **C3, image-wide sweeps over the 1.79M-line cache:**

  | feature | functions inside the regex span | outside |
  |---|---|---|
  | calls `_Xregex_error` | 12 | 0 |
  | calls `ctype<char>::tolower` | 7 | 0 |
  | compares `dword [reg+0x7c]` with `\| ) [ ] { }` | 5 | 0 |
  | contains `sub al,0x7b` (the inlined `_Next`/`_Is_esc` idiom) | 17 | 0 |

  So these features are specific to the regex code in this image.
- **C4, planted positives:** the feature extractor must recover error codes {4,5,6,10} from 00205890, and `new(0x20)` plus the `_Node_base` vtable from 00208C60. Otherwise the run aborts.
- **Extractor limitation found and fixed during the work:** 00205890 tests `_L_asrt_wrd` with `and eax,0x80`, not `test`/`bt`. The first run therefore scored 7/8 on that function. After fixing the extractor it scores 8/8. The register tracking does not follow control flow and never kills a register's role. That can only over-credit a value, never hide one, and C1 and C2 bound the risk.

## Surprises / caveats

- 5 of the 21 "StdRegex.Runtime" functions are not `<regex>` members. They are generic library instantiations that `<regex>` pulls in:
  - `std::equal` (`<xutility>`)
  - two `vector::operator=` (`<vector>`)
  - `vector<bool>::erase` (`<vector>`)
  - `collate<char>::do_transform` (`<locale>`)

  The first four are instantiated for regex types or are reached only from regex code. `do_transform` is reached through the `collate<char>` vtable.
- The 3 "allocator-labelled" functions are genuine `<regex>` members: `_Buf::_Insert`, `_Builder::_Add_char_to_array` and `_Builder::_Add_range`. They probably got the label because they call `realloc`, `_Xbad_alloc` or `new`.
- For `char`, the compiler removed code that is dead for this instantiation:
  - `_Do_class` has no `_Large`, `_Classes` or `_Equiv` arms.
  - `_Add_named_class` collapses to `_Add_elts`.
  - `_HexDigits` has no octal branch.

  A byte-level template match against another `_Elem` would therefore differ.
- Identical-COMDAT folding makes one destructor serve up to four node classes. Name a node class by its vtable address, never by its destructor address.
