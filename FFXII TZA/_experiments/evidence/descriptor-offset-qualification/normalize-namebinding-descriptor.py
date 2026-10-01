"""Qualify one frozen descriptor label from retained shipping dataflow.

This is the current consumer/producer path for this descriptor. The historical
pin-exception driver/result remain immutable; do not re-run them as current
semantics. The error policy is consumed from existing evidence, not retested.
"""
import copy, hashlib, importlib.util, json, pathlib, struct, sys
W = pathlib.Path(__file__).resolve().parent

def module(name, file):
    spec = importlib.util.spec_from_file_location(name, W / file)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

P = module('descriptor_proof', 'prove-title-queue-consumption.py')
S = module('descriptor_roles', 'validate-title-source-annotations.py')

OLD = 'Submitter2EAD50 builds callback2E4D20, DWORD low32 record user data, flags0 and NULL cancellation function. It passes the36A000(handle) return as destination, metadata kind/index and a newly queried size to32E620. This is original descriptor and call dataflow, not proof the read is accepted or executed.'
NEW = OLD.replace('flags0', 'initial file offset0 (descriptor+0)')

def main():
    out = pathlib.Path(sys.argv[1]); src = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else W
    normalized = out.with_name('namebinding-pin-exception-qualified-02.json')
    if out.exists() or normalized.exists(): raise ValueError('immutable qualified output exists')
    affected = json.loads((src / 'descriptor-offset-affected-preimages-01.json').read_text())
    for q in affected['inputs']:
        if P.sha(src / q['path']) != q['sha256']: raise ValueError('affected source/semantic preimage changed')
    prior = json.loads((src / 'descriptor-offset-retained-pin-result-01.json').read_text())
    if prior.get('producer_complete') is not True or prior['descriptor'].get('flags') != 0:
        raise ValueError('missing exact legacy descriptor preimage')
    if [k for k, v in enumerate(prior['established']) if v == OLD] != [3]:
        raise ValueError('missing/nonunique exact established preimage')
    pins = []; ix = {}
    image = (S.ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(image).hexdigest() != P.SHA: raise ValueError('reference image changed')
    pe = struct.unpack_from('<I', image, 60)[0]; opt = struct.unpack_from('<H', image, pe + 20)[0]
    sections = [struct.unpack_from('<IIII', image, pe + 24 + opt + k * 40 + 8)
                for k in range(struct.unpack_from('<H', image, pe + 6)[0])]
    for name in ['descriptor-offset-retained-pin-source-01.json', 'descriptor-offset-retained-adopter-source-01.json']:
        v, instructions = P.load(src, name, pins); S.validate(v)
        for q in v['ranges']:
            a, z = int(q['start'], 16), int(q['end_exclusive'], 16)
            raw = next(image[ro+a-0x120000-va:ro+z-0x120000-va] for _, va, rs, ro in sections
                       if 0x120000+va <= a and z <= 0x120000+va+rs)
            if raw != bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):
                raise ValueError('reference byte identity changed')
        ix.update(instructions)
    for pc, m, args in [
        (0x2ead98, 'xor', 'ecx, ecx'), (0x2ead9e, 'mov', 'dword ptr [rsp + 0x30], ecx'),
        (0x2eadef, 'lea', 'rcx, [rsp + 0x30]'), (0x2eadf7, 'mov', 'qword ptr [rsp + 0x20], rcx'),
        (0x2eae08, 'call', '0x32e620'), (0x32e8ce, 'mov', 'rcx, qword ptr [rsp + 0x60]'),
        (0x32e8db, 'mov', 'eax, dword ptr [rcx]'), (0x32e8fb, 'cdq', ''),
        (0x32e8fc, 'and', 'edx, 0x7ff'), (0x32e90b, 'add', 'eax, edx'),
        (0x32e913, 'and', 'eax, 0xfffff800'), (0x32e918, 'mov', 'dword ptr [r10 + 0x2c], eax'),
        (0x32e92c, 'mov', 'dword ptr [r10 + 0x28], esi')]: P.need(ix, pc, m, args)
    # Distinct signed-offset versus byte-count stores; source is exact original
    # code. Normal callee/ABI and no relevant alias interference remain premises.
    if ix[0x32e8db]['memory'][0]['role'] != 'r' or ix[0x32e918]['memory'][0]['role'] != 'w':
        raise ValueError('reviewed access roles changed')
    policy = json.loads((src / 'namebinding-error-policy-existing-resolution-01.json').read_text())
    if policy['status'] != 'ANSWER_CONSUMED_FROM_EXISTING_CANONICAL_EVIDENCE':
        raise ValueError('existing policy consumption absent')
    value = copy.deepcopy(prior); value['descriptor']['initial_file_offset'] = value['descriptor'].pop('flags')
    value['established'][3] = NEW
    value.update(status='QUALIFIED_PIN_DESCRIPTOR_INDEPENDENT_PENDING',
                 semantic_addendum='Descriptor+0 is initial file offset, not flags. Error byte-count sentinel is independent; natural IO/recovery/scheduling/lifetime remain open.',
                 original_result_sha256=P.sha(src / 'descriptor-offset-retained-pin-result-01.json'),
                 qualification_checker_sha256=P.sha(pathlib.Path(__file__)))
    raw = (json.dumps(value, indent=2) + '\n').encode()
    report = dict(status='PRODUCER_VALID_DESCRIPTOR_OFFSET_QUALIFICATION_INDEPENDENT_PENDING',
                  producer_complete=True, method='A RETAINED_ORIGINAL_CODE', exe_sha256=P.SHA,
                  source_pins=pins, checker_sha256=P.sha(pathlib.Path(__file__)),
                  established=['The issuer descriptor leading zero is an initial file offset; adopter signed-aligns descriptor+0 and stores slot+2C.',
                               'Slot+28 byte count is independent. Existing error-helper count==-1 policy is consumed, not a new experiment.',
                               'Normalized output changes exactly descriptor.flags to initial_file_offset and the one matching established sentence; no record/state flag or prior branch result is changed.'],
                  limitations=policy['unresolved'] + ['Producer validity is not independent review or canonical incorporation. Natural reachability/IO/scheduling/lifetime not certified.'],
                  required_invocation_receipts=[dict(path=n, sha256=P.sha(src/n)) for n in
                      ['descriptor-offset-affected-preimages-01.json', 'namebinding-error-policy-existing-resolution-01.json']],
                  normalized_result=dict(path=normalized.name, sha256=hashlib.sha256(raw).hexdigest()),
                  native_runs=0, live_runs=0, new_whole_runtime_rows_closed=0)
    with normalized.open('xb') as f: f.write(raw)
    with out.open('x', encoding='utf8') as f: json.dump(report, f, indent=2); f.write('\n')
    print('Qualified original descriptor offset; legacy history retained, no new error-policy test')

if __name__ == '__main__': main()
