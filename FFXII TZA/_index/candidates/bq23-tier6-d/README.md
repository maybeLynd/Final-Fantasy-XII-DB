# BQ-23: the 24 regex-span members matched to VS2015 `<regex>` - the last residue (FABLE, Claude Opus 5.5, 2026-09-27)

This follows [`bq23-tier6-b/`](../bq23-tier6-b/README.md) (ordered containers) and
[`bq23-tier6-c/`](../bq23-tier6-c/README.md) (six node builders). What remained unmatched was:
- 21 `StdRegex.Runtime` members;
- three `ContainerAllocatorSupport` members in the same span.

They are checked here against the VS2015 v140 headers, installed with the user's approval.

**Provenance.** The matching was a FABLE-delegated read-only subagent (Claude Opus 5.5) working in FABLE's scratchpad.
FABLE re-ran `regex_match.py` from this folder, and the output is identical. FABLE also independently spot-checked
`basic_regex::_Tidy` (`00209360`) against the header:
- `lock xadd [rep + 0x2c], -1`, then a compare against 1, then the node-destroy loop over `_Next` at `+0x10`;
- that is `_MT_DECR(_Rep->_Refs)` and `_Destroy_node`, with `_Refs` at `+0x2C` after `_Fl` / `_Loops` / `_Marks`.

## Result (`regex_match.py`, output `regex_match.out`, table `regex-members.tsv`): 24 of 24, all high confidence

| addr | VS2015 function |
|---|---|
| `00203240` | `_Cmp_chrange<const char*, const char*, _Cmp_icase<regex_traits<char>>>` |
| `00203490` | `_Buf<char>::_Insert<const char*>` *(labelled ContainerAllocatorSupport)* |
| `00203980` | `std::equal` with `_Cmp_icase` (caller `lookup_classname`) - generic, pulled in by `<regex>` |
| `00204820` | `vector<unsigned int>::operator=` (the `_Grp_valid` copy) - generic |
| `00204950` | `vector<_Tgt_state_t<const char*>::_Grp_t>::operator=` (the `_Grps` copy) - generic |
| `00204E50` | `_Builder::_Add_char_to_array` *(labelled ContainerAllocatorSupport)* |
| `00205330` | `_Builder::_Add_range` *(labelled ContainerAllocatorSupport)* |
| `00205890` | `_Parser::_Alternative` |
| `00205B40` | `_Parser::_AtomEscape` |
| `00206430` | `_Parser::_CharacterEscape` |
| `00206890` | `_Parser::_ClassEscape(bool)` |
| `00206960` | `_Parser::_ClassRanges` |
| `00206CD0` | `_Builder::_Discard_pattern` (only caller: `_Parser::_Compile`'s catch-all, which rethrows) |
| `00206F60` | `_Matcher::_Do_class` |
| `002070A0` | `_Parser::_Do_ex_class(_Meta_type)` |
| `00207B40` | `_Matcher::_Do_rep` |
| `002080D0` | `_Parser::_HexDigits(int)` |
| `002085B0` | `_Parser::_IsIdentityEscape` (its two jump tables decode to the header's character lists) |
| `00208710` | `_Matcher::_Match_pat` |
| `00208DE0` | `_Parser::_Quantifier` |
| `00209360` | `basic_regex<char>::_Tidy` |
| `00209840` | `_Parser::_Wrapped_disjunction` |
| `00209CD0` | `collate<char>::do_transform` (slot 4 of the `collate<char>` vtable) - generic `<locale>` |
| `00209E00` | `vector<bool>::erase(const_iterator, const_iterator)` - generic |

**Evidence used:**
- node sizes from the header's x64 layout (allocations of 0x20, 0x28, 0x30 and 0x38);
- the error codes passed to `_Xregex_error`;
- the metacharacters each parser function compares;
- the language-flag masks;
- call-site context.

**The header revision is this one.** `_Matcher`'s limits are 10,000,000 and 600, the 64-bit values in this header.

**Controls:**
- **C1, confusion matrix.** Each check list passes fully only on its own function. The closest miss is 3/4, between
  the two `vector::operator=`, which differ only in element size.
- **C2, negative sample.** 200 random functions outside the span (fixed seed): no full pass; the best partial score is
  0.25.
- **C3, image-wide sweeps.** Calls to `_Xregex_error`, `ctype<char>::tolower`, the metacharacter compares and the
  inlined escape test: 12 / 7 / 5 / 17 functions inside the span, **0 outside**.
- **Known-answer checks.** Guards on the extractor itself.

## Label consequences (routed to SWE2-EC7, not edited here)

- The three "ContainerAllocatorSupport" members are `<regex>` members.
- Five of the 21 "StdRegex.Runtime" members are generic library code that `<regex>` pulls in: `std::equal`, the two
  `vector::operator=`, `vector<bool>::erase` and `collate<char>::do_transform`.
- None of the 24 installs a node vtable. The 20 vtable installers are separate, including `00203F70`, which creates the
  root node.
- The linker merged identical destructors. `00204C40` serves four node classes and `00204C10` two, so a node class is
  named by its vtable, never by its destructor address.

## Limits

- Static, against the tier-6 VS2015 header; the matching is by feature checks, not byte reproduction.
- Code dead for `char` was stripped (`_Do_class` has no large-set branches, and `_HexDigits` no octal branch).
- The caller index and the C3 sweeps need the disassembly cache (`Y1P_CACHE`). The committed `.out` carries the run
  with it.

## Files

- `regex_match.py`, `pelib.py`, `regex_match.out`, `regex-members.tsv`, `notes.md`.
- `consumer-check.md`.
