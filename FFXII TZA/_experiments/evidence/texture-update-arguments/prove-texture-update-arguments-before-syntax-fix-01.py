"""Retained shipping updater ABI and width-sensitive arithmetic, Method A.

Fresh result [disposable source directory]. No original instructions execute.
Opaque native callees are boundaries, not implemented stubs.
"""
import hashlib, importlib.util, json, pathlib, sys

W = pathlib.Path(__file__).resolve().parent


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, W / file)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


P = module('update_original_cfg', 'prove-title-queue-consumption.py')
S = module('update_actual_roles', 'validate-title-source-annotations.py')
U32 = (1 << 32) - 1
U64 = (1 << 64) - 1
BODY = ('0x622010', '0x6221dc', 'c6c880f7e3a465dd2cc553bfc5dbf60240fe56e52261212eebf17b5ecacf9b95')
LEAF = ('0x621ff0', '0x621ffc', '810781c10549c601701c17816fe2e4596ff61249f027f6586cf70c879b8b2145')


def rounded(value, block):
    """ADD32 then AND32; no real-number replacement or widening."""
    return ((value + 3) & U32) & 0xfffffffc if block else value & U32


def pitch_and_advance(bits, width, height, block):
    rw, rh = rounded(width, block), rounded(height, block)
    # Both IMULs write 32-bit destinations. SHR RAX subsequently reads the
    # zero-extended EAX product, not a 64-bit product of the original factors.
    row = (((bits * rw) & U32) * (4 if block else 1)) & U32
    advance = (((bits * rw) & U32) * rh) & U32
    return dict(rounded_width=rw, rounded_height=rh, row_pitch=row >> 3,
                payload_advance=advance >> 3)


def bounded_arithmetic():
    # These are distinguishing algebraic inputs, NOT original-code executions.
    cases = [
        dict(name='ordinary-uncompressed', bits=32, width=16, height=8, block=False),
        dict(name='ordinary-block-rounded', bits=4, width=5, height=7, block=True),
        dict(name='product-wraps32', bits=32, width=0x10000000, height=1, block=False),
        dict(name='rounding-wraps32', bits=4, width=0xffffffff, height=4, block=True),
        dict(name='height-product-wraps32', bits=8, width=0x10000, height=0x10000, block=False),
        dict(name='zero-entry-dimensions', bits=32, width=0, height=0, block=False),
    ]
    expected = [(16, 8, 64, 512), (8, 8, 16, 32),
                (0x10000000, 1, 0, 0), (0, 4, 0, 0),
                (0x10000, 0x10000, 0x10000, 0), (0, 0, 0, 0)]
    for case, want in zip(cases, expected):
        observation = pitch_and_advance(**{k: case[k] for k in ('bits', 'width', 'height', 'block')})
        if tuple(observation.values()) != want:
            raise ValueError('arithmetic derivation control failed: ' + case['name'])
        case['derived'] = observation
    if cases[2]['derived']['row_pitch'] == (32 * 0x10000000) >> 3:
        raise ValueError('overflow discriminator failed')
    bounds = []
    for requested in (0, 1, 10, 11, 12, 0x80000000, 0xffffffff):
        for no_mips in (False, True):
            last = min(11, 0 if no_mips else requested)
            levels = list(range(last + 1))
            if not levels or len(levels) > 12:
                raise ValueError('mip bound derivation failed')
            bounds.append(dict(requested_u32=requested, flag18_bit1=no_mips,
                               last_mip=last, call_indices=levels))
    return cases, bounds


def main():
    if len(sys.argv) not in (2, 3):
        raise ValueError('fresh result [disposable source directory]')
    out = pathlib.Path(sys.argv[1])
    source = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else W
    if out.exists():
        raise ValueError('immutable result exists')
    pins = []
    raw, ix = P.load(source, 'texture-async-count-path-source-01.json', pins)
    annotations = S.validate(raw)  # Actual default invocation, before inference.
    for wanted in (BODY, LEAF):
        spans = [q for q in raw['ranges'] if q['start'] == wanted[0]]
        if len(spans) != 1 or (spans[0]['start'], spans[0]['end_exclusive'], spans[0]['sha256']) != wanted:
            raise ValueError('required shipping updater/leaf identity changed')
    if [0x622010, 0x6221dc, 0x1d8f424] not in raw.get('pdata_entries', []):
        raise ValueError('required updater normal-root metadata absent')
    table = raw.get('table', {})
    name = '.?AV?$TAsyncUpdate@VPTexture2DD3D11@PRendering@Phyre@@@@'
    if (table.get('address'), table.get('slot0'), table.get('name'), table.get('raw_from_minus8')) != (
            '0xd54348', '0x621ff0', name, '4824d10100000000f01f620000000000c824d10100000000'):
        raise ValueError('required callback object/table identity changed')
    cfg = P.closed(ix, 0x622010, 0x6221dc)
    if cfg['calls'] != [dict(pc='0x62207b', target='0x5fd050'),
                         dict(pc='0x6220fd', target='qword ptr [rax + 0x180]'),
                         dict(pc='0x622190', target='0x584730')]:
        raise ValueError('updater opaque call boundaries changed')
    operations = [
        (0x621ff0, 'mov', 'edx, dword ptr [rcx + 0x10]'),
        (0x621ff3, 'mov', 'rcx, qword ptr [rcx + 8]'),
        (0x621ff7, 'jmp', '0x622010'),
        (0x62202c, 'mov', 'eax, dword ptr [rcx + 0x30]'),
        (0x62202f, 'mov', 'rbx, rcx'),
        (0x622032, 'btr', 'eax, 0x1f'),
        (0x62204d, 'mov', 'edi, dword ptr [rbx + 0x28]'),
        (0x622050, 'mov', 'esi, dword ptr [rbx + 0x2c]'),
        (0x622053, 'mov', 'eax, edx'), (0x622055, 'imul', 'r14, rax, 0x58'),
        (0x622059, 'mov', 'eax, dword ptr [rbx + 0x18]'),
        (0x62205e, 'mov', 'r15, qword ptr [r14 + rcx + 0x28]'),
        (0x622063, 'test', 'al, 1'), (0x622067, 'xor', 'eax, eax'),
        (0x62206b, 'mov', 'eax, dword ptr [rbx + 0x10]'),
        (0x62206e, 'mov', 'r13d, 0xb'), (0x622077, 'cmovb', 'r13d, eax'),
        (0x622080, 'xor', 'ebp, ebp'),
        (0x622082, 'mov', 'r12, qword ptr [rax + 0x110]'),
        (0x622090, 'mov', 'eax, edi'),
        (0x622096, 'mov', 'eax, dword ptr [rbx + 0x28]'),
        (0x622099, 'mov', 'rcx, qword ptr [rbx]'),
        (0x62209c, 'mov', 'edx, 1'),
        (0x6220a1, 'test', 'byte ptr [rcx + 0x18], dl'),
        (0x6220a6, 'add', 'eax, 3'), (0x6220a9, 'mov', 'edx, 4'),
        (0x6220ae, 'and', 'eax, 0xfffffffc'),
        (0x6220b1, 'mov', 'ecx, dword ptr [rcx + 0x14]'),
        (0x6220b4, 'imul', 'ecx, eax'), (0x6220be, 'imul', 'ecx, edx'),
        (0x6220c1, 'shr', 'ecx, 3'),
        (0x6220df, 'xor', 'r9d, r9d'),
        (0x6220e2, 'mov', 'rdx, qword ptr [r14 + rdx]'),
        (0x6220e6, 'mov', 'r8d, ebp'),
        (0x6220e9, 'mov', 'dword ptr [rsp + 0x30], 0'),
        (0x6220f1, 'mov', 'dword ptr [rsp + 0x28], ecx'),
        (0x6220f5, 'mov', 'rcx, r12'),
        (0x6220f8, 'mov', 'qword ptr [rsp + 0x20], r15'),
        (0x622103, 'mov', 'ecx, esi'), (0x622105, 'mov', 'edx, edi'),
        (0x62210b, 'mov', 'edx, dword ptr [rbx + 0x28]'),
        (0x622112, 'mov', 'ecx, dword ptr [rbx + 0x2c]'),
        (0x622115, 'mov', 'rax, qword ptr [rbx]'),
        (0x622118, 'test', 'byte ptr [rax + 0x18], 1'),
        (0x62211e, 'add', 'edx, 3'), (0x622121, 'add', 'ecx, 3'),
        (0x622124, 'and', 'edx, 0xfffffffc'), (0x622127, 'and', 'ecx, 0xfffffffc'),
        (0x62212a, 'mov', 'eax, dword ptr [rax + 0x14]'),
        (0x62212d, 'imul', 'eax, edx'), (0x622132, 'imul', 'eax, ecx'),
        (0x622135, 'shr', 'rax, 3'), (0x622139, 'add', 'r15, rax'),
        (0x622130, 'shr', 'edi, 1'), (0x62213e, 'mov', 'edi, 1'),
        (0x622145, 'cmova', 'edi, eax'),
        (0x622148, 'shr', 'esi, 1'), (0x62214c, 'mov', 'esi, 1'),
        (0x622153, 'cmova', 'esi, eax'),
        (0x622156, 'inc', 'ebp'), (0x622158, 'cmp', 'ebp, r13d'),
        (0x62215b, 'jbe', '0x622090'),
        (0x622161, 'mov', 'eax, dword ptr [rbx + 0x30]'),
        (0x622168, 'cmp', 'eax, 1'), (0x62216b, 'jne', '0x6221bc'),
        (0x62218b, 'mov', 'rcx, qword ptr [r14 + rcx + 0x28]'),
        (0x6221b3, 'mov', 'qword ptr [r14 + rbx + 0x28], 0),
    ]
    for pc, mnemonic, args in operations:
        P.need(ix, pc, mnemonic, args)
    if ix[0x6220f8]['memory'][0]['role'] != 'w' or ix[0x62205e]['memory'][0]['role'] != 'r':
        raise ValueError('required source/argument memory roles changed')
    cases, bounds = bounded_arithmetic()
    result = dict(
        status='PRODUCER_CHECKED_TEXTURE_UPDATE_ARGUMENTS_INDEPENDENT_PENDING', producer_complete=True,
        method='A STATIC_ONLY', exe_sha256=P.SHA, source_pins=pins,
        annotation_prerequisite=annotations, normal_cfg=cfg,
        question='Exact deferred updater argument dependencies, instruction-width arithmetic and cleanup re-selection',
        argument_map=dict(RCX='[5FD050 return+110] captured context', RDX='qword element[index]+0 reselected each iteration',
                          R8D='mip index 0..last inclusive', R9D='0', stack20='entry element[index]+28 payload pointer plus prior advances',
                          stack28='DWORD row pitch', stack30='DWORD 0'),
        instruction_pins=[dict(pc=hex(pc), mnemonic=m, args=a) for pc, m, a in operations],
        formulas=dict(last_mip='min_unsigned(11, (owner18 bit1) ? 0 : u32(owner10))',
                      rounded_dimension='blockflag ? (low32(d+3)&FFFFFFFC) : u32(d)',
                      row_pitch='zeroextend32(low32(low32(bits*roundedWidth)*(blockflag?4:1))) >> 3',
                      payload_advance='zeroextend32(low32(low32(bits*roundedWidth)*roundedHeight)) >> 3',
                      pointer='low64(previousPointer + payloadAdvance)',
                      next_dimension='max_unsigned(1, previousDimension>>1)'),
        algebraic_controls=cases, mip_bound_controls=bounds,
        established=[
            'RTTI-bound leaf loads owner/index and tails622010. Index is zero-extended low32 and multiplied by88; this body has no local index<count validation. Admission validation is a different time/boundary.',
            'Initial width/height and mip limit are loaded before the first opaque context getter. Initial source pointer is selected element+28, not an explicit owner+C0..187 descriptor read. Native slot180 may still use aliased memory; this is no global tail-unread claim.',
            'Resource/count/format fields are re-read inside the loop. Format is read again AFTER each slot180 return for source-pointer advance. A whole immutable admission snapshot is not established by the earlier200B copy.',
            'Under stable valid inputs and normal ABI-preserving returns, last is in0..11 and loop issues last+1 calls. Row-pitch and payload advances use truncated32-bit products. Widened real-number/64-bit multiplication is not bit-exact. ADD32 rounding can wrap before its mask.',
            'Entry dimension0 triggers fallback to owner width/height in the first iteration. After each call EDI/ESI become max_unsigned(1,old>>1). No ordinary positive-dimension premise should silently erase zero-input behavior.',
            'Post-loop maskedcount1 conditionally reselects element+28 as free argument, calls584730, reselects again and zeros+28. With mutable count/storage/payload these are distinct read times, not a guarantee it frees the initially captured pointer. Count!=1 skips this local release/null arm.',
        ],
        assumptions=['Valid nonwrapping object/format/context/selected storage and source pointer for the intended ordinary path',
                     'Stable owner count/storage/index/format/dimensions/payload for the simplified formulas and release of the original field',
                     'Normal ABI-preserving returns from5FD050, native slot180 and584730; their effects/success are not executed or certified'],
        limitations=['Not native/emulated execution, actual graphics effects, GPU presentation or portable200B descriptor semantics',
                     'No complete caller/writer/alias closure, natural initialized index/count/format/payload, scheduler order, cancellation, lifetime/reuse or counter38 ownership guarantee',
                     'Arithmetic examples are conditional input derivations, not evidence of shipping assets selecting overflow/zero values',
                     'An opaque callee or aliased argument can access the owner tail or mutate fields; local explicit reads cannot rule that out'],
        affected_claims=['OPUS Texture2DD3D11Element+28 physical role and deferred update ABI/pitch width',
                         'FABLE Phyre200B copy versus deferred argument reads and release/lifetime assumptions'],
        next_discriminator='Existing primary evidence/peer ownership for element+28 producer and scheduler removal/counter writers; no repeat of settled parameter samples',
        checker_sha256=P.sha(pathlib.Path(__file__)), helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),
        native_runs=0, live_runs=0, new_whole_runtime_rows_closed=0,
        cleanup='Retained source reads and finite foreground reducer only; no PC/game/input/instrument/save/config/reference or peer-process mutation')
    with out.open('x', encoding='utf-8') as file:
        json.dump(result, file, indent=2)
        file.write('\n')
    print('Original updater argument dependencies and32-bit pitch/advance proved; native effects and lifetime OPEN')


if __name__ == '__main__':
    main()
