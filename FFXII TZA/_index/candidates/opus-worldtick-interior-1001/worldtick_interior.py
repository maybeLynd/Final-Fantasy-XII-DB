"""worldtick_interior.py - interior citations for the 125 F-frontier functions that the world-tick page cites by entry
only (OPUS, 2026-10-01). Each row states what the body does, read from the certified image, anchored on instructions
strictly inside the body.

Verification, before any write: every anchor lies strictly inside its function's extent in functions.tsv, and the
instruction decoded at that address (capstone, the certified EXE) has the recorded mnemonic. Any mismatch is a FAIL and
nothing is written. Then the section is inserted before "## Cross-subsystem neighbours" (byte-preserving, idempotent).
usage: python -B worldtick_interior.py [--check]   (--check verifies only)
Prints CHECKED n anchors, PATCHED / ALREADY, FAILS n."""
import os, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
PAGE = os.path.join(DB, "00-Engine-Core-Runtime", "Battle-Frame", "the-world-tick-and-the-field-frame.md")
ANCHOR = "\n## Cross-subsystem neighbours — FINAL-AUDIT pass 22\n"
HEADING = "## Interior citations for the entry-cited functions (OPUS, 2026-10-01)"

# (function, what the body does, [(interior anchor, expected mnemonic), ...])
ROWS = [('0017DFC0',
  "reads qword `+0xDF8` of `00796E20()`'s result, asks `00197710(00198790(), 0, 2, 3)` and returns 1 when "
  '`0079E6A0(that object, the answer, 0)` is non-zero',
  [('0017DFCB', 'mov'), ('0017DFE2', 'call'), ('0017DFF8', 'setne')]),
 ('001800C0',
  'returns 1 when the ring predicate `001BD620(001BDAB0())` is false',
  [('001800CC', 'call'), ('001800D5', 'sete')]),
 ('00184740',
  'fills three zeroed locals through `0024DE30`; when they read 1 and `0x17A` and dword `01F7F540` is 0 it sets '
  '`01F7F540` and `01F7F500` to 1, and when they do not match it clears `01F7F500`',
  [('0018476F', 'cmp'), ('00184781', 'mov'), ('0018479B', 'mov')]),
 ('00197800',
  'returns the dword at index `edx` (0 to `0x6A`, else -1) of table `01DF1030` when `001D50D0()` returns an object '
  'whose byte `+0xC3D` is set, else of table `01DF0E80`',
  [('00197818', 'cmp'), ('00197831', 'mov'), ('0019784E', 'mov'), ('0019785B', 'or')]),
 ('001BD620',
  "returns whether the object's dword `+0xFC` equals its dword `+0x100`",
  [('001BD626', 'cmp'), ('001BD62C', 'sete')]),
 ('001EB990',
  'returns 1 when byte `+0x26E` or byte `+0x26D` of the object is non-zero, else 0',
  [('001EB999', 'cmp'), ('001EB9A5', 'mov')]),
 ('001EC690',
  'increments dword `01F832C4` (the `inc` at the entry; it is a counter write, not a read) and returns',
  [('001EC696', 'ret')]),
 ('00226BA0',
  'returns 1 unless qword `01FD46B8` AND qword `01FD46A0` is all ones',
  [('00226BA9', 'and'), ('00226BB4', 'setne')]),
 ('002335D0',
  'returns 0, 1 or -1 from the result bytes of `0036FFD0()` and `0036FF70()`: 0 when the first is negative, 1 when '
  'it has bit `0x20`, 0 when it has bit `0x40` and the second is non-negative without bit `0x20`, 1 when it has bit '
  '`0x10` and the second is non-negative without bit `0x20`, else -1',
  [('002335E0', 'js'), ('002335EB', 'lea'), ('0023360F', 'xor'), ('00233635', 'cmove')]),
 ('00233700',
  'combines `00229E20()` and `002DDDA0()`: one set of arms calls `00229ED0(0)` and clears dword `0208E6B4`; the '
  'others call `00229ED0(1 or 2)`, set `0208E6B4` to 1 and tail-call `00182FB0` with the same 1 or 2',
  [('0023373C', 'call'), ('00233741', 'mov'), ('00233760', 'mov'), ('0023376F', 'jmp')]),
 ('002370A0', 'calls `00229ED0(0)` and clears dword `0208E6B4`', [('002370A6', 'call'), ('002370AB', 'mov')]),
 ('0023B020',
  'sets bit 0 of dword `02089340`, stores its pointer argument at qword `0208E6A8` and its dword argument at '
  '`0208E6A4`',
  [('0023B027', 'mov'), ('0023B02E', 'mov')]),
 ('0024DE30',
  'when qword `02F97348` is non-null, writes its byte `+0x3AC`, word `+0x3AE` and word `+0x3A2` plus one to its '
  'three out-pointers',
  [('0024DE43', 'mov'), ('0024DE53', 'mov'), ('0024DE63', 'inc')]),
 ('00250180',
  'stores 0 in dword `020927DC` when its argument is non-zero, else increments it',
  [('00250188', 'inc'), ('0025018C', 'cmovne'), ('0025018F', 'mov')]),
 ('002506D0',
  'when dword `02064AA0` is 0 adds `00184950()` to dword `0208F570`; then runs `002481A0`, `00248030(*0208EA48)`, '
  '`00248190`, `002481C0`, `00244970(*0208EA48)`, `00250CA0` and tail-calls `003676B0(1)`',
  [('002506E2', 'add'), ('002506F4', 'call'), ('0025071D', 'jmp')]),
 ('00254440',
  'when the second argument is negative writes `0x80` (first argument non-zero) or 0 to dword `01E0C320`, else sets '
  'bit `0x40` there; stores the two arguments at `02092744` / `020927EC` and tail-calls `00255330`',
  [('00254452', 'mov'), ('0025445B', 'or'), ('00254462', 'mov'), ('0025446E', 'jmp')]),
 ('00254E50',
  'tail-calls `0027EFA0` when `002805D0()` returns non-zero',
  [('00254E54', 'call'), ('00254E61', 'jmp')]),
 ('00255810',
  'writes -1 to four dwords (`-0x2E0`, `0`, `+0x2E0`, `+0x5C0`) of every `0xBB0`-byte step from `02092C94` up to '
  '`02096704`',
  [('00255820', 'mov'), ('00255844', 'add')]),
 ('002578F0',
  'stores its argument at qword `02096508`; when that is null it walks lists 0 to 4 (`00263C30` count, `003587C0` '
  'entry), calls `0026A3B0(entry, 00358320(), low byte of 00263EB0(...))` for each entry `002EA6A0` accepts other '
  "than `*02096508`, and sets dword `02096510` to 1 when `00263EB0`'s word is negative",
  [('002578F7', 'mov'), ('00257936', 'call'), ('0025798F', 'call'), ('002579A8', 'mov')]),
 ('00259FB0',
  'calls `00259620(float 02098DFC)` and tail-calls `0025A0C0(float 02098E00)`',
  [('00259FBC', 'call'), ('00259FCD', 'jmp')]),
 ('0025A620',
  'for record `ecx` of the `0x860`-byte array at `02097D20`, sets float `+0x850` to float `01CEBBA8` when it is at '
  'least float `009156E0`, else moves it toward `01CEBBA8` by the factor float `008F3108`',
  [('0025A63A', 'comiss'), ('0025A64B', 'movss'), ('0025A664', 'mulss'), ('0025A670', 'movss')]),
 ('0025D580',
  'calls `00238B00(0)`; if byte `02099DA7` is set calls `00250960(0, 0)` and clears it; then `002E1CD0(1, 0)`, '
  '`003601C0(0xC)`, `00225CD0(0x13, -1)` and tail-calls `00226280`',
  [('0025D58B', 'cmp'), ('0025D59D', 'mov'), ('0025D5BE', 'call'), ('0025D5C7', 'jmp')]),
 ('0025D950',
  'sets byte `02099DA3` to 1, keeps it only when qword `*00226B10(0)` has bit 34 set, zeroes it when `002E15F0()` is '
  'non-zero, replaces it with byte `02099DA5` when byte `02099DA4` is set, stores the result and tail-calls '
  '`002E8700` with it',
  [('0025D973', 'test'), ('0025D980', 'mov'), ('0025D9A7', 'cmovne'), ('0025D9B8', 'jmp')]),
 ('00263B50',
  "returns word `+0x1D8 + 2*edx` of actor-manager slot `ecx` (`0x288`-byte stride from `02098E10`) when the slot's "
  '`+0x10` bit 0 is set, else 0',
  [('00263B64', 'test'), ('00263B6D', 'movzx')]),
 ('00263C50',
  "returns word `+0x1D0 + 2*edx` of actor-manager slot `ecx` (`0x288`-byte stride from `02098E10`) when the slot's "
  '`+0x10` bit 0 is set, else 0',
  [('00263C64', 'test'), ('00263C6D', 'movzx')]),
 ('00264610',
  "returns qword `+0x48` of actor-manager slot `ecx` (`0x288`-byte stride from `02098E10`) when the slot's `+0x10` "
  'bit 0 is set, else 0',
  [('00264621', 'test'), ('00264628', 'mov')]),
 ('002677B0',
  'returns 1 when `003148D0()` has bit 3 set and bit 4 clear, else 0',
  [('002677BD', 'test'), ('002677C6', 'test'), ('002677CD', 'cmove')]),
 ('00268650',
  'clears dword `0209A2C0`; when dwords `0209A2B4` and `0209A2B8` are both non-negative and `003587C0` of them '
  'returns an entry, stores `003589B0(entry)` in `0209A2C0`',
  [('0026865A', 'mov'), ('00268672', 'call'), ('00268684', 'mov')]),
 ('0026B730',
  'when bit 0 of byte `02098E20` is set and qword `02098E58` is non-null, stores its word argument through that '
  'pointer',
  [('0026B739', 'mov'), ('0026B745', 'mov')]),
 ('0026E260',
  'when qword `0209A670` is non-null, its dword `+0x120` non-zero and its `+0x138` pointer non-null, tail-jumps '
  'through that pointer',
  [('0026E26C', 'cmp'), ('0026E275', 'mov'), ('0026E281', 'jmp')]),
 ('0027EFA0',
  'when `002EFD20(3)` is non-zero calls `002EFA70(3, 0, 1, 0)`; then `0035C7B0(0xB, 0)` and `00252B40(0xB, 1)`, sets '
  'dword `+0xC8` of the `+0xC0` object of `*0209AC30` to 2, calls `00245020` on its `+0xB8`, clears byte `+0xDEE`, '
  'calls `00251E80`, sets byte `+0xDEF` and tail-calls `003EF750`',
  [('0027EFBE', 'call'), ('0027EFC8', 'call'), ('0027EFE8', 'mov'), ('0027F00C', 'mov'), ('0027F01F', 'mov')]),
 ('002805D0',
  'returns 0 unless `0035C740()` is non-zero, the `*0209AC30` block has non-null `+0xC0` and `+0xB8`, that `+0xB8` '
  "object's dword `+0xD4` is 0 and dword `02092730` minus 2 is at most `0x11`; then dispatches through the byte "
  "table `0028065C` and the offset table `00280650`, whose read arm returns 1 unless the object's dword `+0xC4` is "
  '`0x40` to `0x42`',
  [('002805D4', 'call'), ('002805FA', 'cmp'), ('00280623', 'mov'), ('0028062E', 'jmp'), ('00280639', 'cmp')]),
 ('002C63D0',
  'calls `00861EC0(object, 0, 0x1D90)`, appends the `0x5F` records of `0x40` bytes from `+0x40` to the end of the '
  "`+0x18` chain (each record's `+0x20` set to its predecessor), then sets `+0x1D60` to the object, word `+0x1D78` "
  'to 0 and floats `+0x1D7C` / `+0x1D80` to 5.0 / 17.0',
  [('002C63E1', 'call'), ('002C640D', 'mov'), ('002C6411', 'mov'), ('002C642F', 'mov'), ('002C6439', 'mov')]),
 ('002E0670', 'zeroes the eight qwords `0215F1C0` to `0215F1F8`', [('002E0679', 'mov'), ('002E06A3', 'mov')]),
 ('002E0940',
  'when word `0215F1AC` differs from word `0215F1B0`, stores (`0215F1AC` non-zero) at byte `0215F1A2`, calls '
  '`00254440(that flag, word 0215F1B4 non-zero)` and clears `0215F1B4`; then copies `0215F1AC` into `0215F1B0`',
  [('002E094B', 'cmp'), ('002E096D', 'mov'), ('002E0976', 'call'), ('002E0982', 'mov'), ('002E098E', 'mov')]),
 ('002E4330',
  'returns 0 for a null argument or a first dword of -1; otherwise, when its word id is not -1 and that `0x740`-byte '
  'record of the array at `*022C6F28` has a non-zero dword `+0x284`, calls `00427280` on the record; then returns 1',
  [('002E4339', 'cmp'), ('002E434B', 'imul'), ('002E435B', 'cmp'), ('002E4364', 'call'), ('002E4369', 'mov')]),
 ('002E7E50',
  'returns 0.0 for a null object, a null `+0xC0` or an id of -1 there; otherwise tail-calls `003E6150(id, '
  '0x9000606)` when the second argument is at most 0, else `003E6150(id, 0x9000000)`',
  [('002E7E61', 'mov'), ('002E7E73', 'mov'), ('002E7E7D', 'mov'), ('002E7E87', 'xorps')]),
 ('002E8CC0',
  'sets bit 0 of dword `+0x48818` of `*022C6F28` when byte `0215FD56` is 0, else clears it',
  [('002E8CD0', 'or'), ('002E8CD8', 'and')]),
 ('002F18A0', 'calls `002E1CA0(0xA, 1)` and clears qword `022BE7D0`', [('002F18AC', 'call'), ('002F18B1', 'mov')]),
 ('002FC350',
  'unlinks the record from the `+0x28` / `+0x30` list headed by `02EC3D60` / `02EC3D68`, pushes it at the front of '
  'the list headed at `02EC3D70`, masks its first dword with `0xF000003F` and clears its `+0x10`',
  [('002FC35D', 'mov'), ('002FC37D', 'mov'), ('002FC391', 'mov'), ('002FC3A5', 'and'), ('002FC3AF', 'mov')]),
 ('002FC830',
  "when the handle's low 6 bits are below `0x30` and the `0x38`-byte record at `02EC32E0 + 0x38*low` holds that "
  "handle in its first dword, clears bits 2-3 and sets bits 0-1 of the record's byte `+0x23`",
  [('002FC835', 'cmp'), ('002FC84C', 'cmp'), ('002FC850', 'and'), ('002FC854', 'or')]),
 ('002FCAC0',
  'returns 0 when qword `02EC3D70` is null; otherwise adds the low 5 bits of word `+4` of entry `02EC19C0[word '
  "+0x20]` over the `02EC3D60` list's records whose state nibble (`+0x23` low 4 bits) is 1 to 3 or 5, adds the "
  "argument's own entry, and returns whether the total is at most `0x18`",
  [('002FCAF0', 'movzx'), ('002FCB07', 'movzx'), ('002FCB1C', 'movzx'), ('002FCB28', 'cmp'), ('002FCB2B', 'setle')]),
 ('003045A0',
  'returns the float `003204E0(0031ABF0(3), 1, &out)` writes, multiplied by float `01CEBC08` when bit 1 of dword '
  '`+0x5AE0` of `*02EBF190` is set',
  [('003045B2', 'mov'), ('003045CA', 'call'), ('003045D5', 'test'), ('003045DA', 'mulss')]),
 ('003143D0',
  'calls `003DAA20`, `003DA2F0(0.0)`, `003DD210(0.0)`, `00255810` and `0037D890`, then `0025E3F0(i)` for i = 0 to 4',
  [('003143DE', 'call'), ('003143EB', 'call'), ('003143F9', 'call'), ('00314400', 'cmp')]),
 ('00314410',
  'when dword `01EED060` is negative, calls `0026A5F0(4)` and stores its argument in `01EED060`',
  [('00314426', 'call'), ('0031442B', 'mov')]),
 ('00314940', 'copies float `01CEBBA8` into float `022C2544`', [('00314948', 'movss')]),
 ('0031A230',
  'returns 2 for an argument of -1, else 1 when `002FCAC0(argument)` is non-zero and 0 otherwise',
  [('0031A239', 'lea'), ('0031A241', 'call'), ('0031A24A', 'setne')]),
 ('00325060',
  'advances dword `022C2578` by one, modulo 8',
  [('00325066', 'inc'), ('00325068', 'and'), ('0032506B', 'mov')]),
 ('00325B40',
  'returns 0 unless the unit is non-null, has byte `+0` bit 4 and a non-null `+0x698` record, and (when that '
  "record's dwords `+0x64` or `+0x3C` carry any of bits `0x80000003`) `00313F60()` is non-zero; then tail-calls "
  '`003DCCF0(unit +0x10, second argument, 00325AD0(unit))`',
  [('00325B54', 'test'), ('00325B6B', 'test'), ('00325B7E', 'call'), ('00325B96', 'jmp')]),
 ('00328360',
  'returns -1 for an argument of -1, else tail-calls `0042FCE0`',
  [('00328365', 'or'), ('00328368', 'jmp')]),
 ('0032A650',
  'zeroes the `0x100` bytes at `022C26A0`, raises dword `022C2568` to dword `022C2564` when smaller, and clears '
  '`022C2564`',
  [('0032A663', 'call'), ('0032A674', 'cmovl'), ('0032A67B', 'mov'), ('0032A681', 'mov')]),
 ('0032A6B0', 'returns dword `+0x22C` of the object at `*0209A670`', [('0032A6B7', 'mov')]),
 ('0032A6C0',
  'returns dword `3*ecx` of the dword array that `+0x1D8` of `*0209A670` points to',
  [('0032A6CE', 'mov'), ('0032A6D5', 'mov')]),
 ('003334B0',
  'for a non-null table of 16 pointers, releases every entry whose word `+8` differs from the argument (`0046EE70`, '
  'then `003697F0`) and nulls it, then calls `003A8660(argument)`',
  [('003334DD', 'movzx'), ('003334E5', 'call'), ('003334ED', 'call'), ('003334F2', 'mov'), ('00333501', 'call')]),
 ('00333740',
  'for a non-null table of 16 pointers, releases the first entry whose word `+8` equals the argument (`0046EE70`, '
  'then `003697F0`) and nulls it, then calls `003A8510(argument)`',
  [('00333768', 'movzx'), ('0033377D', 'call'), ('0033378D', 'call'), ('00333792', 'mov'), ('0033379B', 'call')]),
 ('0033B6D0',
  'calls `00338490`, then clears bit 0 of dword `022C7D04` and byte `022C7CE9`',
  [('0033B6D4', 'call'), ('0033B6D9', 'and'), ('0033B6E0', 'mov')]),
 ('003574B0',
  'calls `00267E10(r9)` and `00267F90(r9, 0)`, forwards its four arguments to `00340970`, calls `00263FF0(0)`, '
  "`002348E0` and `0035A6F0`, and tail-calls `00269800` with `00263FF0`'s result",
  [('003574D3', 'call'), ('003574EE', 'call'), ('003574F5', 'call'), ('00357502', 'call'), ('0035751E', 'jmp')]),
 ('003586A0',
  'sets bit `ecx` of byte `022C7F9A` when `edx` is non-zero, else clears it',
  [('003586AB', 'bts'), ('003586B5', 'btr'), ('003586B8', 'mov')]),
 ('00358C60',
  'copies the 16 bytes at `008C5FD0` to `022C7FD0`, calls `0025A520(2, 0)`, and tail-calls `00358CB0` when dword '
  '`022C7FEC` is non-zero or when `002671F0()` is non-zero and dword `022C7FE0` is positive',
  [('00358C6D', 'movaps'), ('00358C77', 'call'), ('00358C84', 'jne'), ('00358C97', 'jle'), ('00358C9D', 'jmp')]),
 ('00359800',
  'steps on word `022C8010`: 1 tail-calls `00359A30`; 3 clears words `022C8024` / `022C8028`, sets 4 and calls '
  '`0037C910`, then continues as 4; 4 sets 5 and tail-calls `00359880` when `0037CB40()` is non-zero; 5 tail-calls '
  '`00359880`; other values return',
  [('0035980E', 'je'),
   ('00359828', 'mov'),
   ('0035983B', 'mov'),
   ('00359855', 'mov'),
   ('00359860', 'jmp'),
   ('00359869', 'jmp')]),
 ('0035A6F0',
  'calls `00473830(0, 1)`, `00238B70(0)` and `00238AE0(0)`, and tail-calls `00267D40(2, 0)`',
  [('0035A6FB', 'call'), ('0035A702', 'call'), ('0035A709', 'call'), ('0035A717', 'jmp')]),
 ('0035AB20',
  'calls `00238B70(1)` and `00238AE0(1)`, and tail-calls `0035A590`',
  [('0035AB29', 'call'), ('0035AB33', 'call'), ('0035AB3C', 'jmp')]),
 ('0035B5D0',
  'calls `0035B1A0` on each non-zero dword of the eight at `022C8030` and zeroes it; then, for each `0x20`-byte '
  'record from `02EC0B82` to `02EC0F82` whose preceding flag byte is set, calls `0035B1A0(word << 8 OR index)` with '
  'the index counted from 1',
  [('0035B5F6', 'call'), ('0035B5FB', 'mov'), ('0035B620', 'cmp'), ('0035B629', 'shl'), ('0035B62E', 'call')]),
 ('0035C700',
  'returns 1 when dword `022C83E8` has bit `0x100` or dword `02092730` is `0x0B` or `0x18`, else whether '
  '`002E12D0()` is non-zero',
  [('0035C704', 'test'), ('0035C720', 'cmp'), ('0035C728', 'je'), ('0035C72A', 'call'), ('0035C733', 'setne')]),
 ('0035C740', 'returns bit 1 of dword `022C83E8`', [('0035C746', 'shr'), ('0035C748', 'and')]),
 ('003606E0',
  'sets byte `022CB9BC` to 1 when any of the three dwords `022CB9DC` to `022CB9E4` is non-zero, else to 0',
  [('003606F0', 'cmp'), ('003606FE', 'mov'), ('00360706', 'mov')]),
 ('00361700',
  'stores its second argument at byte `022CBA9B` and its float argument, clamped to at most float `01CEBBA8` when '
  'the second argument is 0 and to at least 0.0, at float `022CBB28`',
  [('0036170F', 'minss'), ('00361719', 'mov'), ('0036171F', 'maxss'), ('00361723', 'movss')]),
 ('0036EEB0',
  'when byte `022D9B40` is 1 and any `0x18`-byte record in `022D9AB0`..`022D9B40` has state byte 1 or 2, repeats '
  '`0032E040`, `0036D890`, `0035EA30(2)` until `0036F000()` is non-zero; then calls `002DF430(0)` and sets the byte '
  'to 2; byte `022D9B41` gets the same treatment with `002DF430(1)`',
  [('0036EEF5', 'cmp'),
   ('0036EF20', 'call'),
   ('0036EF34', 'call'),
   ('0036EF3F', 'call'),
   ('0036EF44', 'mov'),
   ('0036EF4B', 'cmp'),
   ('0036EFA7', 'mov')]),
 ('0036F460',
  'stores its float argument at float `02AD9B50` (reduced by repeated adds of float `01CEBC9C` while at least float '
  '`01CEBBA8`), passes (argument minus the previous `02AD9B50`) times float `008F8D80`, divided by float `01DFE0B8` '
  'times float `008F8D80`, to `004678E0` and tail-calls `00468520`',
  [('0036F472', 'subss'),
   ('0036F47A', 'movss'),
   ('0036F490', 'addss'),
   ('0036F4B9', 'divss'),
   ('0036F4C0', 'call'),
   ('0036F4C9', 'jmp')]),
 ('0036F530',
  'calls `0026E260` and `003ECCA0`, then tail-calls `003ED7F0(0)`',
  [('0036F534', 'call'), ('0036F539', 'call'), ('0036F544', 'jmp')]),
 ('0036FD90',
  'for index 0 or 1 zeroes the six words `02AD9E24`, `02AD9E28`, `02AD9E2C`, `02AD9E08`, `02AD9E0C`, `02AD9E10` plus '
  'twice the index; any other index calls `00809728`',
  [('0036FD9A', 'cmp'), ('0036FDA9', 'mov'), ('0036FDD1', 'mov'), ('0036FDDE', 'call')]),
 ('00374060',
  "returns 0 when the record's `+0x1C` bit 1 is set and dword `+0x24` is below dword `+0x6C`, provided "
  '`00254A70(record)` is non-zero, or word `020926E4` lacks bit `0x800`, or dword `+0x68` equals `002EF9F0(3)`; '
  'otherwise returns 1',
  [('00374069', 'call'),
   ('00374077', 'test'),
   ('0037408A', 'cmp'),
   ('0037408F', 'test'),
   ('00374098', 'cmp'),
   ('0037409D', 'xor')]),
 ('003A1D50',
  'calls `004FE3C0` on `02EBEFC0` and `02EBEFD8`, clears dword `02EBEFF0`, calls `004FE420(02EBEFC0, 0x200, 0)` and '
  'tail-calls `004FE420(02EBEFD8, 0x200, 0x200)`',
  [('003A1D5B', 'call'), ('003A1D6F', 'mov'), ('003A1D85', 'call'), ('003A1D9D', 'jmp')]),
 ('003A7300',
  'calls `003A7360`, then, for the four dwords `+0x110` to `+0x11C` of `*02F97348`, calls `002FC340` on each '
  'non-zero one and zeroes it',
  [('003A730A', 'call'), ('003A7327', 'mov'), ('003A732E', 'call'), ('003A733A', 'mov'), ('003A7341', 'cmp')]),
 ('003A76F0',
  'zeroes the 256 qwords from `+8` of the block at `*02EBEFA8`, then its dword `+0`',
  [('003A7707', 'mov'), ('003A7710', 'cmp'), ('003A771F', 'mov')]),
 ('003A7D00',
  'allocates `0x400` bytes with `0036A100`, stores the pointer through `*02EBEFA0` and tail-calls `00861EC0(block, '
  '0, 0x400)`',
  [('003A7D09', 'call'), ('003A7D1D', 'mov'), ('003A7D27', 'jmp')]),
 ('003A7EE0',
  'walks the `+0xF0` list from `**02EBEF98` clearing bit 0 of byte `+0x103` on every node, then walks it again '
  'calling `004FF0D0(node, float argument)` on each node whose bit is still clear',
  [('003A7F00', 'and'), ('003A7F30', 'test'), ('003A7F43', 'call')]),
 ('003A9560',
  'allocates `0xA00` bytes with `0036A100`, stores the pointer through `*02EBEF90` and tail-calls `00861EC0(block, '
  '0, 0xA00)`',
  [('003A9569', 'call'), ('003A957D', 'mov'), ('003A9587', 'jmp')]),
 ('003A9920',
  'allocates `0x1800` bytes with `0036A100`, stores the pointer through `*02EBEF78` and tail-calls `00861EC0(block, '
  '0, 0x1800)`',
  [('003A9929', 'call'), ('003A993D', 'mov'), ('003A9947', 'jmp')]),
 ('003A9CC0',
  'zeroes qwords `+0`, `+8`, `+0x10` and words `+0x18`, `+0x1A` of the block at `*02EBEF70`',
  [('003A9CC9', 'mov'), ('003A9CDE', 'mov'), ('003A9CF4', 'mov')]),
 ('003B22D0',
  'searches the `0x30`-byte records from `02EBE5E0` (up to `02EBEBE0`, stopping at a zero entry) for one whose dword '
  "`+0` equals the argument, and sets that record's dword `+0x1C` to 3",
  [('003B22E8', 'je'), ('003B22EA', 'cmp'), ('003B22FA', 'cmp'), ('003B2300', 'mov')]),
 ('003B6C20',
  'zeroes the `0x20` dwords at `02EBCBE0`, the dwords `02EBCC70`, `02EBCC60`, `02EBCBC0`, `02EBCAA0` and the 32 '
  'bytes at `02EBCA80`',
  [('003B6C33', 'mov'),
   ('003B6C39', 'rep stosd'),
   ('003B6C46', 'mov'),
   ('003B6C58', 'movdqu'),
   ('003B6C60', 'movdqu')]),
 ('003DBAE0',
  'calls `003DBCF0(record, third argument, 2)`; when that returns 1 and the record is not the second argument, it '
  'turns state byte 1 into 2 in the `+0x89` entries of `0x14` bytes at `+0xA0` (when byte `+0x63` is set), calls '
  "`003DB6E0(record)` and halves byte `+0x63`; returns `003DBCF0`'s result",
  [('003DBB01', 'call'), ('003DBB12', 'cmp'), ('003DBB35', 'mov'), ('003DBB45', 'call'), ('003DBB4A', 'shr')]),
 ('003DC710',
  'for each of the 16 `0x14`-byte records at `02B57F70` with state byte `+6` 3, byte `+7` 0 and word `+4` 0, adds '
  '`0x10` to dword `+8`, sets the state to 4 and dword `02B58170` to 1, and when bits 4 to 19 of `+8` wrap to zero '
  'replaces it with byte `+0x13` OR `0x10`',
  [('003DC72A', 'cmp'), ('003DC743', 'add'), ('003DC752', 'mov'), ('003DC758', 'mov'), ('003DC76D', 'mov')]),
 ('003DC780',
  'for a positive handle whose record `02B57F70[handle AND 0xF]` (`0x14` bytes) holds it at `+8`, decrements word '
  '`+4`, and at 0 or below stores 0 there and sets dword `02B58170` to 1; then tail-calls `003DCF20` when byte `+7` '
  'is 0 (the body ends at `003DC7C9`; the listed 125-byte extent runs into the next function)',
  [('003DC79A', 'cmp'), ('003DC7A4', 'dec'), ('003DC7B1', 'mov'), ('003DC7BB', 'mov'), ('003DC7C3', 'je')]),
 ('003DF670',
  'clears bit 0 of dword `02B59D18` when `003588B0(003590D0())` returns an actor that `002EA6A0` accepts, else sets '
  'it; when the dword is then 0 tail-calls `003DF810`, otherwise calls `0029CAB0(0, 0, 0, 0)` and zeroes dwords '
  '`02B59D14`, `02B59D10` and qwords `02B59D08`, `02B59D00`',
  [('003DF67B', 'call'),
   ('003DF691', 'and'),
   ('003DF69A', 'or'),
   ('003DF6A7', 'jmp'),
   ('003DF6B6', 'call'),
   ('003DF6D0', 'mov')]),
 ('003E1310',
  "when its second argument is 0 and `0020E600` resolves the record's dword `+0`, stores the low byte of its third "
  'argument at byte `+7` of the resolved object',
  [('003E1326', 'call'), ('003E1337', 'mov')]),
 ('003E8990',
  'clears bits 3 and 4 of word `+0`; when word `+2` is non-negative calls `00473500(it, float 01CEBC9C, float '
  '01CEBC9C)` and `004735D0(it, 0.0)`; when word `+0x10` is at most `0x3E7` calls `00363A90(it, (byte +0x14 >> 4) != '
  '1, 1)`',
  [('003E89A8', 'and'), ('003E89C3', 'call'), ('003E89CD', 'call'), ('003E89D2', 'cmp'), ('003E89F7', 'call')]),
 ('003E8A10',
  'calls `0037A3B0(0, first argument)` when the second argument is non-zero, else `0037A310(0, first argument)`; '
  'returns 0',
  [('003E8A1C', 'call'), ('003E8A2A', 'call'), ('003E8A2F', 'xor')]),
 ('003E8A40',
  'calls `0037A1D0(0, first argument)` when the second argument is non-zero, else `0037A130(0, first argument)`; '
  'returns 0',
  [('003E8A4C', 'call'), ('003E8A5A', 'call'), ('003E8A5F', 'xor')]),
 ('003E8A70',
  'calls `0037B190(0, first argument)` when the second argument is non-zero, else `0037B0F0(0, first argument)`; '
  'returns 0',
  [('003E8A7C', 'call'), ('003E8A8A', 'call'), ('003E8A8F', 'xor')]),
 ('003E9100',
  'calls `00408200` when byte `02B5D090` is set, then clears the byte',
  [('003E910D', 'call'), ('003E9112', 'mov')]),
 ('003EB6C0',
  'for an index up to `0x1F`, releases the pointer `02B5EA20[index]` with `003EB470` when it is non-null and nulls '
  'it',
  [('003EB6C4', 'cmp'), ('003EB6E5', 'call'), ('003EB6EA', 'mov')]),
 ('003EC5F0',
  'for i = 0 to 15 calls `003EB6C0(i)` whenever `00377C20()` returns 0',
  [('003EC5F8', 'call'), ('003EC608', 'call'), ('003EC60F', 'cmp')]),
 ('003EC690',
  'when dword `02B5EC94` is non-zero, calls `002EBD60(it, 0)` and `002E3DC0(it)` and clears it',
  [('003EC6A0', 'call'), ('003EC6AB', 'call'), ('003EC6B0', 'mov')]),
 ('003ED170',
  "copies the 16 bytes at its argument to `02EBB7D0` when the argument's first dword is greater than the dword at "
  '`02EBB7D0`',
  [('003ED176', 'cmp'), ('003ED17D', 'movups')]),
 ('00428F10',
  'sets bit 5 of dword `+0x304` to (second argument non-zero) and sets bit 28 of dword `+0x290`',
  [('00428F19', 'sbb'), ('00428F1E', 'or'), ('00428F24', 'or')]),
 ('0042FCE0',
  'increments dword `02CA4ED4` (the `inc` at the entry) and tail-calls `002FCBF0`',
  [('0042FCE6', 'jmp')]),
 ('00466170',
  'returns byte `+0` OR byte `+4` << 8 OR byte `+8` << 16 OR dword `+0xC` << 24 of its argument',
  [('00466177', 'shl'), ('00466183', 'shl'), ('0046618B', 'or')]),
 ('00466AD0',
  'for an index below dword `02EBB6E0` whose `0x50`-byte entry at `*02EBB6F0` has a non-null `+8`, returns bit 2 of '
  "the entry's dword `+0x4C`; otherwise returns 1",
  [('00466AD4', 'cmp'), ('00466AEE', 'cmp'), ('00466AF8', 'shr'), ('00466AFF', 'mov')]),
 ('00466BB0',
  'for a valid index of the `0x50`-byte table at `*02EBB6F0` (count dword `02EBB6E0`), returns float `+0x24` of the '
  "entry's `+8` object, else 0.0",
  [('00466BD5', 'mov'), ('00466BD9', 'movss'), ('00466BDF', 'xorps')]),
 ('00466C40',
  'for a valid index of the `0x50`-byte table at `*02EBB6F0` (count dword `02EBB6E0`), returns float `+0x20` of the '
  "entry's `+8` object, else 0.0",
  [('00466C65', 'mov'), ('00466C69', 'movss'), ('00466C6F', 'xorps')]),
 ('00467660',
  'for a valid entry of the same table, stores its two float arguments at `+0x3C` and `+0x40`, raising `+0x3C` to '
  "the `+8` object's float `+0x20` and lowering `+0x40` to its float `+0x24` when they lie outside",
  [('00467689', 'movss'), ('0046768E', 'movss'), ('0046769D', 'movss'), ('004676AC', 'movss')]),
 ('004676C0',
  'for a valid entry of the same table, sets bit 1 of dword `+0x4C` to bit 0 of the second argument',
  [('004676E5', 'and'), ('004676EE', 'or')]),
 ('00467700', 'for a valid entry of the same table, stores its float argument at `+0x38`', [('00467725', 'movss')]),
 ('004678E0',
  'when qword `02EBB6F8` is non-null, adds the float argument times float `+0x38` to float `+0x48` of every '
  '`0x50`-byte entry at `*02EBB6F0` (count dword `02EBB6E0`) whose dword `+0x4C` has bit 0',
  [('00467907', 'test'), ('00467911', 'mulss'), ('00467917', 'addss'), ('0046791D', 'movss')]),
 ('00468520',
  'for each `0x40`-byte entry at `*02CA6010` (count dword `02CA6020`) whose dword `+4` is 0, calls `003CD820` with '
  'its dword `+0x14`',
  [('00468547', 'cmp'), ('0046854E', 'mov'), ('00468552', 'call')]),
 ('0046FFA0',
  "when bit `edx` of the record's dword `+0` is clear, sets it, adds 2 to byte `+7` keeping its bit 0, and stores in "
  'byte `+5` the lowest set bit among bits 0 to 13 (`0xFF` when none)',
  [('0046FFB6', 'or'), ('0046FFC1', 'mov'), ('0046FFC9', 'add'), ('0046FFCE', 'mov'), ('0046FFF0', 'mov')]),
 ('00470050',
  "when bit `edx` of the record's dword `+0` is set, clears it, subtracts 2 from byte `+7` keeping its bit 0, and "
  'stores in byte `+5` the lowest set bit among bits 0 to 13 (`0xFF` when none)',
  [('0047006B', 'and'), ('00470076', 'mov'), ('0047007D', 'dec'), ('00470083', 'mov'), ('004700AC', 'mov')]),
 ('0050D240',
  'calls `00267E10(r9)`, passes the result to `0017D280` with the constant at `00D22998`, and tail-calls `0026A5F0` '
  'with it',
  [('0050D249', 'call'), ('0050D259', 'call'), ('0050D265', 'jmp')]),
 ('0051DBF0',
  'when bit `edx` of dword `+0x10` is clear, sets it and rederives the bytes: `+0x19` is 2 with bit 2, else 3 with '
  'bit 3, else `0xFF`; `+0x31` is 0 with bit 0, else 1 with bit 1, else `0xFF`; `+0x33` is bit 4',
  [('0051DC08', 'or'), ('0051DC18', 'mov'), ('0051DC2E', 'mov'), ('0051DC3D', 'mov'), ('0051DC54', 'mov')]),
 ('0051DDC0',
  'when bit `edx` of dword `+0x10` is set, clears it and rederives bytes `+0x19`, `+0x31` and `+0x33` from the '
  'remaining bits exactly as `0051DBF0` does',
  [('0051DDDF', 'and'), ('0051DDEA', 'mov'), ('0051DE00', 'mov'), ('0051DE0F', 'mov'), ('0051DE26', 'mov')]),
 ('0051E620',
  'zeroes dword `+0xD4`; when the `+0x10` member is non-null, calls `003E1350(member, 3)` and clears bit 2 of byte '
  "`+0x1C` of the object `0020E600` resolves from the member's dword `+8`",
  [('0051E62A', 'mov'), ('0051E641', 'call'), ('0051E65B', 'and')]),
 ('0051E670',
  'sets dword `+0xD4` to 1; when the `+0x10` member is non-null, calls `003E1610(member, 3)` unless dword `+0xD0` is '
  "non-zero, and sets bit 2 of byte `+0x1C` of the object resolved from the member's dword `+8`",
  [('0051E67A', 'mov'), ('0051E689', 'cmp'), ('0051E69A', 'call'), ('0051E6B4', 'or')]),
 ('0051E700',
  'zeroes dword `+0xF8`, calls `0051DDC0(object +0x70, 0)` and, when the `+0x10` member is non-null, tail-calls '
  '`003E1350(member, 7)`',
  [('0051E709', 'mov'), ('0051E719', 'call'), ('0051E731', 'jmp')]),
 ('0051E740',
  'sets dword `+0xF8` to 1, calls `0051DBF0(object +0x70, 0)` and, when the `+0x10` member is non-null, tail-calls '
  '`003E1610(member, 7)`',
  [('0051E749', 'mov'), ('0051E759', 'call'), ('0051E771', 'jmp')]),
 ('0051E800',
  'stores 0 (not 1) in dword `+0x128`; when the `+0x10` member is non-null, calls `003E1350(member, 6)` and '
  'tail-calls `0016D6A0(member, 0)`',
  [('0051E809', 'mov'), ('0051E821', 'call'), ('0051E831', 'jmp')]),
 ('0051E840',
  'sets dword `+0x128` to 1; when the `+0x10` member is non-null, calls `003E1610(member, 6)` and tail-calls '
  '`0016D6A0(member, 1)`',
  [('0051E849', 'mov'), ('0051E861', 'call'), ('0051E874', 'jmp')]),
 ('0051E9C0',
  'zeroes dword `+0xD0`; when the `+0x10` member is non-null, calls `003E1610(member, 3)` when dword `+0xD4` is '
  "non-zero, and clears bit 1 of byte `+0x1C` of the object resolved from the member's dword `+8`",
  [('0051E9CA', 'mov'), ('0051E9D9', 'cmp'), ('0051E9EA', 'call'), ('0051EA04', 'and')]),
 ('0051EA10',
  'sets dword `+0xD0` to 1; when the `+0x10` member is non-null, calls `003E1350(member, 3)` when dword `+0xD4` is '
  "non-zero, and sets bit 1 of byte `+0x1C` of the object resolved from the member's dword `+8`",
  [('0051EA1A', 'mov'), ('0051EA29', 'cmp'), ('0051EA3A', 'call'), ('0051EA54', 'or')]),
 ('0051EAE0',
  'zeroes dword `+0xC4`, calls `00470050(object +0x20, 0)` and tail-calls `00428F10(record, 0)`, the record being '
  'the `0x740`-byte entry of `*022C6F28` that word `+4` names (null for -1 or an entry whose dword `+0x284` is 0)',
  [('0051EAEF', 'mov'), ('0051EAFB', 'call'), ('0051EB1C', 'cmp'), ('0051EB38', 'jmp')]),
 ('0051EB40',
  'sets dword `+0xC4` to 1, calls `0046FFA0(object +0x20, 0)` and tail-calls `00428F10(record, 1)` with the same '
  'record lookup as `0051EAE0`',
  [('0051EB49', 'mov'), ('0051EB59', 'call'), ('0051EB7C', 'cmp'), ('0051EB94', 'jmp')]),
 ('0051EBA0',
  'zeroes dword `+0xCC`, calls `00428F10(record, 0)` (record as in `0051EAE0`) and `0051DDC0(object +0x70, 4)`, and '
  'when the `+0x10` member is non-null tail-calls `003E1310(member, 0, 0)`',
  [('0051EBAF', 'mov'), ('0051EBDC', 'call'), ('0051EBEA', 'call'), ('0051EC02', 'jmp')]),
 ('0051EC10',
  'sets dword `+0xCC` to 1, calls `00428F10(record, 1)` and `0051DBF0(object +0x70, 4)`, and when the `+0x10` member '
  'is non-null tail-calls `003E1310(member, 0, 1)`',
  [('0051EC1D', 'mov'), ('0051EC53', 'call'), ('0051EC61', 'call'), ('0051EC7A', 'jmp')]),
 ('00797A20',
  'copies its string argument into a stack buffer sized to it (`00808F10` stack probe, `00861EBA` copy), cuts the '
  'copy at the first comma after its first character, calls `0079FB10(first argument, buffer)` and checks the stack '
  'cookie (`00808C40`)',
  [('00797A53', 'cmp'),
   ('00797A74', 'call'),
   ('00797A84', 'call'),
   ('00797A99', 'cmp'),
   ('00797AA4', 'mov'),
   ('00797AAD', 'call')])]

fails = 0
sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
n_anchors = 0
for f, text, anchors in ROWS:
    fa = int(f, 16)
    if fa not in sizes:
        print("FAIL %s: not a functions.tsv entry" % f); fails += 1; continue
    n = sizes[fa]
    for a, mn in anchors:
        aa = int(a, 16)
        if not fa < aa < fa + n:
            print("FAIL %s: anchor %s not strictly inside [%s, +%d)" % (f, a, f, n)); fails += 1; continue
        o = off(aa)
        ins = next(md.disasm(d[o:o + 16], aa), None)
        if ins is None or ins.mnemonic != mn:
            print("FAIL %s: anchor %s decodes as %r, expected %r" % (f, a, ins and ins.mnemonic, mn)); fails += 1; continue
        n_anchors += 1
print("CHECKED %d anchors over %d functions" % (n_anchors, len(ROWS)))

lines = [HEADING, "",
         "*Every function below is cited on this page by its entry only. Each row was read from the certified image "
         "(`73461D08...`, image base `00120000`) and states what the body does - access and representation, not meaning - "
         "anchored on instructions strictly inside the body. The applier re-decodes every anchor and refuses on any "
         "mismatch ([record](../../_index/candidates/opus-worldtick-interior-1001/README.md)). Where a row differs from an "
         "earlier line of this page, the row is what the bytes show; the record lists those cases.*", "",
         "| function | size | what the body does | interior anchors |", "|---|---|---|---|"]
for f, text, anchors in ROWS:
    lines.append("| `%s` | %d B | %s | %s |" % (f, sizes.get(int(f, 16), 0), text, ", ".join("`%s` %s" % (a, m) for a, m in anchors)))
SECTION = "\n".join(lines) + "\n"

if fails:
    print("FAILS", fails); sys.exit(1)
if "--check" in sys.argv:
    print("FAILS 0"); sys.exit(0)
b = open(PAGE, "rb").read()
if HEADING.encode("utf-8") in b:
    print("ALREADY")
else:
    a = ANCHOR.encode("utf-8")
    if b.count(a) != 1:
        print("REFUSING: anchor x%d" % b.count(a)); print("FAILS 1"); sys.exit(1)
    b = b.replace(a, ("\n" + SECTION).encode("utf-8") + a, 1)
    open(PAGE, "wb").write(b)
    print("PATCHED")
print("FAILS 0")
