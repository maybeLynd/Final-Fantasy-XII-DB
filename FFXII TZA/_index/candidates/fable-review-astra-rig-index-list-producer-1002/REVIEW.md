# FABLE review: rig index list, borrowed core and relocation cache (ASTRA `f20407498`)

**verdict: ACCEPT** (FABLE, Claude Opus 5.5, 2026-10-02). Request `ASTRA-REQ-FABLE-RIG-INDEX-LIST-PRODUCER-1001`. FABLE
did not author this packet. The packet is
[`_experiments/evidence/rig-index-list-producer/`](../../../_experiments/evidence/rig-index-list-producer/README.md),
producer commit `f20407498` (producer 1 kept, producer 2 additive).

## What was re-derived

[`rv_riglist.py`](rv_riglist.py) -> [`rv_riglist.out`](rv_riglist.out): 131 PASS, 0 FAIL, exit 0. The script uses FABLE's
own reader, [`rvlib.py`](rvlib.py), built on `struct` and capstone 5.0.7. It does not use ASTRA's prover or the role
adapter. It checks the image sha256 and the manifest (sha256 `49f2d7af9808...`; all 63 members hash as listed).

- **Bodies.** `003E1C50` (2,992 bytes), `003E3C30` (109) and `00421D20` (70) decode exactly, 3,171 bytes in total. `.pdata`
  tiles each body. `003E1C50` is five records whose chains, some of them nested, resolve to the root.
- **Codec.** The decoder `0020E600` is `zext32(x) + QWORD [01F83530]`. The encoder `0020E620` is `low32(y) - DWORD
  [01F83530]`. Neither writes memory or rbx/rsi/rdi.
- **Rig +70/+78.**
  - rdi = rig: the only writers are `003E1C5E` and the final pop.
  - The +70 gate is at `003E1C78`. When the decoded +70 is zero, the +78 store at `003E1CC3` cannot be reached, and it is
    the only direct `[rdi+78]` write.
  - When it is nonzero, WORD +68 is compared with -1. Otherwise it is sign-extended and multiplied by 740h, the pool from
    `022C6F28` is added, `cmp [rcx+284], 0` / `cmove 0` follows, then Encode, store +70, Decode and `00421D20`, with no
    test of the derived pointer. The result is encoded into +78.
- **Rig +84.**
  - The DWORD at `003E1D49` is compared with edi, and equality jumps to `003E27F0`. That path reaches only the epilogue
    and writes nothing rdi-relative.
  - `003E27EA` `mov [rdi+84], edi` is the only direct write that overlaps +84, and no encoder call precedes it. Every
    fresh-path (`003E1D6A`) and relocation-path (`003E22B7`) route to the return passes `003E27EA`.
  - The +70/+78 refresh precedes the cache check.
- **Rig +88.**
  - The only direct writes are fresh `003E1D7D` (`lea ecx,[rdi+rax]`) and relocation `003E22CA` (`esi = edi - eax`, then
    `lea ecx,[rsi+rax]`). ecx = old +88 survives to both.
  - No direct rdi-relative access touches +8C in the fixup.
- **Arithmetic.** This is 20,000 random 64-bit bases and pointers, run in Python, not in native code.
  - With a stable base, fresh = low32(old88 + low32(rig)) and relocated = low32(old88 + low32(cur - old84)), exactly. The
    base cancels in the stored value, which is stronger than the packet needs.
  - Pointers 4 GiB apart collide in the cache, and so do a low DWORD of 0 and the cold zero value.
- **Reset, `003E3C30`.**
  - It decodes +88 (`003E3C48`, which dominates the count check) before the unsigned `jbe`/`jb` count compares at
    `003E3C52`/`003E3C85`, and those are the only compares.
  - Count 0 reaches neither the list read nor `00203170`.
  - The index is a DWORD (`003E3C68`). The address is Decode(+78) + 230h + index * 290h in 64-bit arithmetic, and the
    loop steps by 4 bytes.
- **Lookup, `00421D20`.**
  - `push rbx` / `sub rsp` comes first, then `mov ebx, dword ptr [rcx + 0x18]` as the first non-stack access, with no
    rcx test before it.
  - A -1 index or a null row returns 0 (`00421D5E`). Otherwise the row +84 is tail-decoded (`00421D59`).
  - Decode(Encode(0)) is 0 at base 0, so the read is at 18h. At a nonzero base it is not 0. For example, base
    7FF612340000h gives 7FF700000000h.

## Controls (each must be rejected, and is)

Each control reruns the relevant claim group on a patched private copy. All are rejected:
- the count compare made signed (`003E3C58`);
- the loop compare made signed (`003E3C8B`);
- the cache compared against esi instead of edi;
- the +84 store taking esi;
- the `00421D20` first read moved to +1C;
- the encoder reading another cell;
- a wrong 64-bit fresh formula without low32.

The known-answer width control and the capstone `movups` access-flag defect are recorded in the sibling
[render-slot review](../fable-review-astra-render-slot-identity-publication-1002/REVIEW.md). The same `rvlib.py` is used
here.

ASTRA's `prove.py` also passes, with its output in scratch. This review does not rely on it.

## Scope

Nothing in the packet goes beyond its evidence. It already keeps these separate:
- the conditional NULL boundary (not an observed fault or a cause of EXP127);
- the local same-address guard versus native controller idempotence;
- address-domain guarantees, extent, lifetime and initialisation;
- indirect writes to +8C.

Not re-derived here, and left to the retained producer package:
- that the `002ED570` row is a RenderStrideC0Element whose +84 holds the encoded workspace;
- the UQ220 section-2 identity of the rig.

"Inactive" means that the whole DWORD +284h is zero (`cmove` on `cmp [..+284], 0`). It is not a bit test.

run: rv_riglist.py at 1f193fec9
