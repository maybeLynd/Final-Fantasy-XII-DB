# BQ-23: six of the nine unmatched ContainerAllocatorSupport members are MSVC VS2015 STL node builders (FABLE, Claude Opus 5.5, 2026-09-27)

Follows [`bq23-tier6-b/`](../bq23-tier6-b/README.md). That record left nine `ContainerAllocatorSupport` members
unmatched, six of them as a lead: node builders whose allocation-failure path calls `_invalid_parameter_noinfo_noreturn`.
The v140 (VS2015) headers were needed to check it; they are now installed, with the user's approval.

## Result (`bq23_buynode.py`, 4 checks, FAILS 0; output `bq23_buynode.out`, run with the v140 include dir)

| members | what they are | image shape (B1/B2) | VS2015 source (B3) |
|---|---|---|---|
| `00714860`, `007148C0`, `00714920`, `0071F180` | `std::_Tree::_Buynode0` | `operator new(size)` (`00210EC0`), null → `_invalid_parameter_noinfo_noreturn`, then node `+0` / `+8` / `+0x10` = the head | `_Left` / `_Parent` / `_Right` constructed from `_Myhead()` |
| `0075EE00`, `00786980` | `std::_List::_Buynode0` | the same allocation; a null next argument points the node at itself | `if (_Next == _Nodeptr()) { _Next = _Pnode; _Prev = _Pnode; }` |

**Why the failure path is decisive.** VS2015's `_Allocate` takes the normal-block branch for small nodes:
`_Ptr = ::operator new(_User_size); _SCL_SECURE_ALWAYS_VALIDATE(_Ptr != 0);`. In a retail build that macro expands, through
`_SCL_SECURE_INVALID_ARGUMENT_NO_ASSERT` and the UCRT's `_CRT_SECURE_INVALID_PARAMETER`, to
`_invalid_parameter_noinfo_noreturn()`.

**Sensitivity (B4).** EASTL's node creation (`DoCopySubtree` `001FC770`) allocates through the allocator's virtual slot
and never calls that import.

## Still open (BQ-23)

- The three allocator members in the `<regex>` span: `00203490`, `00204E50`, `00205330`.
- The 21 `StdRegex.Runtime` members. The VS2015 `<regex>` header is now available for them.

## Files

- `bq23_buynode.py`, `bq23_buynode.out` and `consumer-check.md`.
