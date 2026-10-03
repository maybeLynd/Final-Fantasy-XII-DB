# Required class descriptor of each PObjectAccessor<T>::Get (FABLE, 2026-10-03)

*FABLE, under SWE2-AUDIT-SPEC's ruling on template-family members (2026-10-03, relayed by the Devin stand-in): a member
of a family whose shared shape is explained once counts for engine_explained only through an interior citation that
anchors the instruction distinguishing that member and states the member-specific value, verified against the image.
Page lead OPUS: request `FABLE-REQ-OPUS-ACCESSOR-DESCRIPTOR-ROWS-1003`. Spread line in progress.py: SWE2-DATA,
`FABLE-REQ-DATA-EE-TEMPLATE-SPREAD-1003`.*

## What the section adds

[phyre-script-object-accessors](../../../22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md)
gets one section, `section.txt` here. It states the shared shape once and gives one row per verified member: the
accessor, its appendix type, the interior anchor (the member's `lea rdx,[rip+X]` before the base-chain compare) and
X with the class name X's constructor stores. Nothing on the page is changed.

## The checker, `desc_check.py`

It covers all 747 appendix bodies and gives each one a disposition:

| disposition | count | row |
|---|--:|---|
| verified: compare `lea` found, X named in the image, name = the appendix type's leaf | 591 | yes |
| getter form: no compare `lea`; the descriptor comes back from `call G ; mov r9,rax` | 156 | no |
| unresolved (compare `lea`, X never named) | 0 | - |
| mismatch (X named, name differs from the appendix type) | 0 | - |

**Naming X from the image.** Each name is the string a descriptor's constructor stores at `[X + 0x30]`. The accessors'
diagnostic path reads that same field as the class name (`mov r8, qword ptr [r9 + 0x30]`). There are three routes:

1. **Direct.** A call to `00632D80` / `00632C90` with `lea rcx,X` and `lea r8,name`. `00632D80` stores r8 with
   `mov qword ptr [rcx + 0x30], r8`.
2. **Wrapper.** Most classes go through a per-class wrapper W(rcx = descriptor) that loads the name into r8 and
   calls the constructor. The static initialiser then does `lea rcx,X` and calls W. This route has 330 wrappers.
3. **Core constructor.** Nine core classes have constructors of their own: `006318A0` PBase, `00631A60`
   PClassDataMemberDynamic, `00631C40` PClassDescriptor, `00631E20` PClassDescriptorDynamic, `00632000` PClassMember,
   `006321E0` PCluster, `006323C0` PClusterDependencyList, `006325A0` PNamespace and `00632780` PWorld. These call
   neither `00632D80` nor `00632C90`. Each stores its literal name with `lea rax,[rip+S] ; mov qword ptr [rbx + 0x30],
   rax`, and a static initialiser in `00163DB0`..`00164180` calls it with `lea rcx,X`.

Route 3 is what upgrades the 13 core-class members that the first run left unresolved. AUDIT-SPEC's follow-up allowed
exactly that: "if their descriptor address is tied to the class by another verified route". Discovery and calls are
raw `E8` scans of `.text`, and each caller is decoded from its listed entry.

**Self-test (the control).** `00599770` checked with its own descriptor must give verified. The same body checked
against another class's named descriptor (`02D363A0`) must give mismatch. Both hold. A checker that matched any name
to any type would fail the second case.

**Independent control.** OPUS's
[`phyre-class-descriptor-vtable.tsv`](../../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/phyre-class-descriptor-vtable.tsv)
links an accessor to its class by a different route: slot `+0x28` of the class's descriptor vtable is its pointer
accessor. This checker links the accessor through its own `lea` X instead. Both take the class NAME from the
constructor's string, so this control tests the accessor-to-descriptor link, not the naming. 315 of the 591 verified
accessors appear in that table's `s28_accessor` column, and its class agrees with this checker's on all 315.

**The `__LINE__` immediates are shared within a form.** Every reference-form member stores 143 and 141, and every
pointer-form member stores 106 and 118. So, per the ruling, no row repeats them. `build_section.py` measured this
(Tools/work/FABLE/accessors/).

**The 156 getter-form members get no row.** For 58 of them G's own descriptor is named, and for the container types
among them (`PArray<E>`, `PSharray<E>`) it is the element type E's. The ruling says this shape earns nothing without
a distinguishing instruction and value of its own.

## Row marker, review and adjudication

- **Row marker.** Each row carries the literal `template member: distinguishing operand`. SWE2-DATA's progress.py
  spread keys on it (`6b7ff727e`): engine_explained is printed with and without these rows (AUDIT-SPEC condition 3).
- **Page lead.** OPUS said yes (`FABLE-REQ-OPUS-ACCESSOR-DESCRIPTOR-ROWS-1003`), and the section follows OPUS's
  layout:
  - it sits at the page end;
  - one family paragraph states the shared shape;
  - it cross-links the existing descriptor-vtable section;
  - its columns are Get body | T | descriptor X | interior anchor, with the anchor also given as entry + offset;
  - there are no rows for the getter form.
- **Rule.** OPUS adopted the family sentence (`opus-ee-rulings-1003`). It counts a member on its declaring page only
  through a row whose committed checker derives every row from the image and refuses a swapped value. That is
  `desc_check.py` here.
- **Review.** SWE2-AUDIT-SPEC reviewed this package (`FABLE-REQ-AUDITSPEC-ACCESSOR-DESCRIPTORS-1003`).

## Files

- `desc_check.py`, `desc_check.out`, `accessor_desc.json`: the checker, its run, and every body's disposition.
- `section.txt`: the section as it will be appended (built by Tools/work/FABLE/accessors/build_section.py).
- `applier.py`: re-checks every row at the bytes before patching. Each anchor must be a `lea rdx,[rip->X]` strictly
  inside the accessor's listed extent, and each type must be the appendix's. It refuses while the page is dirty.

run: desc_check.py --self-test at 202e59a0a (747 dispositioned: 591 verified, 156 getter form, 0 mismatch; FAILS 0);
applier dry run in a clean HEAD worktree: 591 rows checked at the bytes, FAILS 0
