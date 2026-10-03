"""Shipping-source-bound counter invariant; no original-code execution."""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py').is_file())
DEFAULT = HERE / 'retained' if (HERE / 'retained/source-01.json').is_file() else ROOT / 'Database/FFXII TZA/_experiments/evidence/sd194-stale-name-slice'
EXE = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
PINS = {
    'source-01.json': '2c66378a2f9fb4125671f1f5f5ee4211a7397abf52e904137ba474a07e5a9fa8',
    'capture.py': '005b4e6643972d9296495595f7ae0a79d910fee871fb13c33e9ea3224b0a65dc',
}
OPS = [
    (0x2df880, 'movsxd', 'rax, ecx'), (0x2df883, 'mov', 'r11, r8'),
    (0x2df886, 'lea', 'r8, [rip + 0x1e7f773]'), (0x2df88d, 'movsxd', 'rcx, edx'),
    (0x2df890, 'xor', 'r10d, r10d'), (0x2df893, 'mov', 'rax, qword ptr [r8 + rax*8]'),
    (0x2df897, 'mov', 'rax, qword ptr [rax + rcx*8]'), (0x2df89b, 'test', 'rax, rax'),
    (0x2df89e, 'jne', '0x2df8a4'), (0x2df8a0, 'or', 'eax, 0xffffffff'), (0x2df8a3, 'ret', ''),
    (0x2df8a4, 'mov', 'rdx, r11'), (0x2df8a7, 'movsxd', 'r9, r9d'), (0x2df8aa, 'sub', 'rdx, rax'),
    (0x2df8ad, 'mov', 'r8, rax'), (0x2df8b0, 'neg', 'r8'),
    (0x2df8b3, 'movzx', 'ecx, byte ptr [rax]'), (0x2df8b6, 'inc', 'r10d'),
    (0x2df8b9, 'mov', 'byte ptr [rdx + rax], cl'), (0x2df8bc, 'lea', 'rax, [rax + 1]'),
    (0x2df8c0, 'lea', 'rcx, [r8 + rax]'), (0x2df8c4, 'cmp', 'rcx, r9'),
    (0x2df8c7, 'jge', '0x2df8ce'), (0x2df8c9, 'cmp', 'byte ptr [rax], 0'),
    (0x2df8cc, 'jne', '0x2df8b3'), (0x2df8ce, 'movsxd', 'rax, r10d'),
    (0x2df8d1, 'mov', 'byte ptr [rax + r11], 0'), (0x2df8d6, 'xor', 'eax, eax'), (0x2df8d8, 'ret', ''),
]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result

def require(condition, text):
    if not condition: raise ValueError(text)

def selected_count(limit, first_zero_after_zero):
    # Derived from the source's post-copy limit check and NEXT-byte test.
    return max(1, limit) if first_zero_after_zero is None else min(max(1, limit), first_zero_after_zero)

def main(output, source):
    require(not output.exists(), 'fresh output required')
    receipt = json.loads((source / 'capture-01.status.json').read_text())
    require(receipt.get('terminal') is True and receipt.get('exit') == 0 and receipt.get('exception') is None
            and receipt.get('driver_sha256') == sha(source / 'capture.py')
            and (source / 'capture-01.stdout').read_bytes() and not (source / 'capture-01.stderr').read_bytes(),
            'upstream capture failed/incomplete')
    require(sha(source / 'source-01.json') == PINS['source-01.json'] and sha(source / 'capture.py') == PINS['capture.py'],
            'retained source identity changed')
    data = json.loads((source / 'source-01.json').read_text())
    require(data.get('wrapper_complete') is True and data.get('exe_sha256') == EXE
            and data.get('wrapper_sha256') == PINS['capture.py'], 'retained wrapper identity incomplete')
    validator = source / 'dependencies/validate-title-source-annotations.py'
    require(sha(validator) == '7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13', 'reviewed validator changed')
    annotations = module('reviewed_roles', validator).validate(data)
    body = next(r for r in data['ranges'] if r['start'] == '0x2df880')
    require((body['end_exclusive'], body['sha256']) == ('0x2df8d9', 'f71f6f4a0633fa327a47b23f16231e23be086270b133f30357e49520d74f9800'),
            'complete copier body missing')
    require([(int(i['pc'], 16), i['mnemonic'], i['args']) for i in body['instructions']] == OPS,
            'complete copier operation sequence changed')
    index = {int(i['pc'], 16): i for r in data['ranges'] for i in r['instructions']}
    require((index[0x377e03]['mnemonic'], index[0x377e03]['args']) == ('mov', 'r9d, 0x103')
            and (index[0x377e09]['mnemonic'], index[0x377e09]['args']) == ('call', '0x2df880'), 'caller limit boundary changed')
    require(index[0x2df8b9]['memory'][0]['role'] == 'w' and index[0x2df8d1]['memory'][0]['role'] == 'w', 'store roles changed')
    graph_path = source / 'dependencies/prove_owner_reload_order.py'
    require(sha(graph_path) == '43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864', 'reviewed CFG helper changed')
    graphs = module('reviewed_cfg', graph_path)
    graph = graphs.graph(index, 0x2df880, 0x2df8d9)
    null = graphs.graph(index, 0x2df880, 0x2df8d9, fixed={0x2df89e: False})
    require(sorted(graph['returns']) == [0x2df8a3, 0x2df8d8] and null['returns'] == [0x2df8a3]
            and not any(m['role'] in ('w', 'rw') for pc in null['visited'] for m in index[pc]['memory']), 'null branch writes or CFG changed')
    require(not graph['calls'], 'unexpected opaque operation')

    # Induction over all signed-32 C, not enumeration of 2**32 inputs:
    # At loop entry i>=0: RAX=S+i, R10D=i, RDX=D-S, R8=-S.
    # The body reads S+i, writes D+i, increments to t=i+1; RCX=t.
    # Every back edge requires t<C (signed 64) AND byte[S+t]!=0.
    # Thus C<=1 cannot take a back edge. For C>=2, i<C and t<=C;
    # R10D never overflows, because C<=INT_MAX. Exit appends NUL at D+t.
    partition = [dict(limits=[-2147483648, 1], iterations='1', maximum_written_offset='1'),
                 dict(limits=[2, 2147483647], iterations='1..C', maximum_written_offset='C')]
    require(1 - (-2147483648) > 0 and 1 >= 1 and 2147483647 < 2**31, 'signed-domain induction boundary failed')
    cases = []
    for limit in [-2147483648, -1, 0, 1, 2, 258, 259, 260, 2147483647]:
        for next_zero in [1, 2, 258, 259, 260, None]:
            count = selected_count(limit, next_zero)
            require(1 <= count <= max(1, limit) and count < 2**31, 'derived counter bound failed')
            cases.append(dict(limit=limit, next_zero_offset=next_zero, count=count,
                              copied_offsets=[0, count - 1], appended_zero_offset=count))
    require(selected_count(259, None) == 259 and selected_count(0, None) == 1
            and selected_count(-1, None) == 1 and selected_count(259, 2) == 2, 'distinguishing boundary control failed')
    result = dict(producer_complete=True, method='A STATIC_ONLY: complete original source and signed-counter invariant; no machine-code or game execution',
        driver_sha256=sha(Path(__file__)), source_sha256=PINS['source-01.json'], exe_sha256=EXE,
        source_pins=[dict(path='retained/source-01.json', sha256=PINS['source-01.json'])],
        upstream_status_sha256=sha(source / 'capture-01.status.json'), annotation_prerequisite=annotations,
        body=body['sha256'], operation_pins=len(OPS), limit_partition=partition, calculation_controls=cases,
        invariant='At iteration i: RAX=S+i, R10D=i, RDX=D-S, R8=-S. Post-copy t=i+1. Back edge iff signed t<C and current byte[S+t]!=0. Final destination terminator D+t.',
        null_branch='valid resolved null name slot: EAX=-1, no destination read/write, no limit-derived initialization guarantee',
        nonnull_branch='EAX=0, unconditional first byte copied, at most max(1,signed32(R9D)) copied bytes followed by NUL; limit is not capacity',
        stable_disjoint_source='For source and destination disjoint/noninterfering, t=min(max(1,C), first NUL offset at least1); source NUL at offset0 does not stop the loop itself.',
        caller_259='nonnull successful lookup: writes only destination offsets0..259, guarantees a NUL by259; requires260 writable bytes. Null lookup does not guarantee a NUL or a bounded inherited string.',
        affected_claims=['SD194 successful lookup vs null-slot buffer-bound preconditions', 'Namespace copier signed character-limit contract'],
        limitations=['Valid table/index resolution and all accessed memory; normal ABI; no concurrent changes. No capacity or pointer validation is implemented.',
                    'Counter bound survives sequential aliasing; unchanged-source next-NUL formula needs disjoint/noninterfering source and destination.',
                    'No actual inherited null-slot bytes, natural field reachability, request acceptance, imported memcpy behavior or game consequences.',
                    'Boundary calculations and prerequisite refusal tests are producer controls; independent acceptance pending.'])
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(producer_complete=True, operation_pins=len(OPS), boundary_calculations=len(cases), native_or_live_runs=0)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('output', type=Path); parser.add_argument('--source', type=Path, default=DEFAULT)
    args = parser.parse_args(); main(args.output, args.source)
