"""Default special-admission source gate: actual bytes, roles and kind witness.

The old checker trusted mnemonic text. Keep that original published record;
this gate revalidates its retained ranges against the verified shipping image.
No recapture, process access or natural reachability claim.
"""
import hashlib, importlib.util, pathlib, struct

W = pathlib.Path(__file__).resolve().parent
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
VALIDATOR_SHA = '7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'
ROOT = next(p for p in W.parents if (p / 'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
BASE = 0x120000


def qualify(raw, exe=None):
    exe = pathlib.Path(exe) if exe is not None else ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe'
    body = exe.read_bytes()
    if hashlib.sha256(body).hexdigest() != EXE_SHA or raw.get('exe_sha256') != EXE_SHA:
        raise ValueError('shipping image identity mismatch')
    if raw.get('image_base') != hex(BASE):
        raise ValueError('shipping image base mismatch')
    helper = W / 'validate-title-source-annotations.py'
    if hashlib.sha256(helper.read_bytes()).hexdigest() != VALIDATOR_SHA:
        raise ValueError('reviewed annotation validator changed')
    spec = importlib.util.spec_from_file_location('reviewed_special_source_annotations', helper)
    s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    validation = s.validate(raw)  # Actual invocation, including reviewed adapter.
    pe = struct.unpack_from('<I', body, 0x3c)[0]
    ns = struct.unpack_from('<H', body, pe + 6)[0]
    opt = struct.unpack_from('<H', body, pe + 20)[0]
    sections = [struct.unpack_from('<IIII', body, pe + 24 + opt + 40*i + 8) for i in range(ns)]
    def read(pc, n):
        for _, va, rs, ro in sections:
            if BASE + va <= pc and pc + n <= BASE + va + rs:
                return body[ro + pc - BASE - va:ro + pc - BASE - va + n]
        raise ValueError('source not backed by shipping image')
    wanted = [(0x30ce10, 0x30cf3f), (0x306bd0, 0x306c5b), (0x309230, 0x3092f7)]
    if [(int(q['start'],16),int(q['end_exclusive'],16)) for q in raw['ranges']] != wanted:
        raise ValueError('missing/different special-admission ranges')
    pins = []
    for q in raw['ranges']:
        pc, end = int(q['start'],16), int(q['end_exclusive'],16)
        blob = bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
        if blob != read(pc, end-pc):
            raise ValueError('retained source differs from shipping bytes')
        pins.append({'start':hex(pc),'end_exclusive':hex(end),'sha256':hashlib.sha256(blob).hexdigest()})
    ix = {int(i['pc'],16):i for q in raw['ranges'] for i in q['instructions']}
    expected = {
        0x30cec7:('jb','0x30cf00'), 0x30cef0:('ja','0x30cf00'),
        0x30cef2:('mov','eax, dword ptr [rip + 0x1fb5268]'),
        0x30cef8:('add','eax, -5'), 0x30cefb:('cmp','eax, 1'),
        0x30cefe:('jbe','0x30cf31'),
        0x306bda:('mov','eax, dword ptr [rip + 0x1fbb580]'),
        0x306be6:('test','eax, eax'), 0x306be8:('je','0x306c05'),
        0x306bea:('cmp','eax, 1'), 0x306bed:('je','0x306bfc'),
        0x306bef:('xor','eax, eax'), 0x306bfb:('ret',''),
        0x306bfc:('cmp','rdi, qword ptr [rip + 0x1fbb565]'),
        0x306c03:('jne','0x306bef'), 0x306c0a:('mov','ebx, 3'),
        0x306c0f:('mov','ecx, ebx'), 0x306c22:('call','0x32f6e0'),
        0x306c27:('test','eax, eax'), 0x306c29:('je','0x306c3d'),
        0x306c2b:('xor','eax, eax'), 0x306c3c:('ret',''),
        0x306c4d:('call','0x309230'), 0x306c52:('mov','edx, eax'),
        0x306c54:('mov','ecx, ebx'), 0x306c56:('call','0x32fc30'),
        0x3092b4:('imul','ecx, edx, 0x113'),
    }
    for pc, pair in expected.items():
        if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args']) != pair:
            raise ValueError('conditional/kind source witness mismatch ' + hex(pc))
    for pc, target in [(0x30cef2,0x22c2160),(0x306bda,0x22c2160),(0x306bfc,0x22c2168)]:
        if ix[pc]['memory'][0]['rip_target'] != hex(target) or ix[pc]['memory'][0]['role'] != 'r':
            raise ValueError('mode/owner address or access mismatch')
    return {'status':'SHIPPING_BYTES_AND_REVIEWED_ANNOTATIONS_VERIFIED',
            'ranges':pins,'annotation_check':validation,'exe_sha256':EXE_SHA,
            'helper_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'kind_selector':{'pc':'0x306c0a','value':3},
            'limits':'Bounded retained normal-prefix code only; no omitted original effects or natural state/reachability'}
