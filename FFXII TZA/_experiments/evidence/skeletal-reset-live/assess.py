"""Offline EXP127 normalization; trace API success is not session health.

No game control. Historical inputs remain untouched. The regression deliberately
feeds the observed CPU-positive/runtime-error combination through the final gate.
It detects over-promotion, not the unknown native cause of the runtime error.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

E = Path(__file__).resolve().parent


def read(name):
    return json.loads((E / name).read_text(encoding='utf-8-sig'))


def session_status(trace_ok, positive_hits, health, restored):
    if health.get('runtime_error_observed'):
        return 'INVALID_POST_TRACE'
    if not trace_ok or positive_hits <= 0:
        return 'INVALID_INSTRUMENT'
    if not (health.get('responsive_action_observed') is True
            and health.get('runtime_error_observed') is False
            and restored is True):
        return 'INCOMPLETE'
    return 'SESSION_CHECKS_SATISFIED'


def assess():
    summary = {'method': 'offline normalization of original-process intervention receipts',
               'arms': {}, 'semantic_acceptance': 'PENDING_INDEPENDENT_REVIEW',
               'cause_of_runtime_error': 'UNKNOWN; no causal experiment performed'}
    for arm in ('control', 'skeletal'):
        run = read(f'{arm}/run.json')
        trace = read(f'{arm}/capture/result.json')
        live = read(f'{arm}/liveness.json')
        hits = trace['hits']
        counts = Counter(f'{h["rip"]:08X}' for h in hits)
        before = [s for s in live['samples'] if live['window_start_unix'] + s['seconds'] < run['capture_start_unix']]
        after = [s for s in live['samples'] if live['window_start_unix'] + s['seconds'] > run['capture_end_unix']]
        assert hits and before and after
        assert all(b['unix'] >= a['unix'] for a, b in zip(hits, hits[1:]))
        assert all(ok for _, ok in trace['arming'] + trace['cleanup']['clears'] + trace['cleanup']['verified'])
        assert trace['status'] == 'PASS' and trace['detach'] and not trace['errors']
        assert trace['cleanup']['status'] == 'PASS'
        assert len(after) >= 100 and after[-1]['cpu_seconds'] > after[0]['cpu_seconds']
        assert not any(s['held'] for s in live['samples'])
        assert not any(s['debugger_present'] for s in before + after)
        assert set(s['foreground_pid'] for s in live['samples']) == {run['process']['pid']}
        assert counts['003A1C50'] > 0
        summary['arms'][arm] = {
            'hits': dict(counts), 'thread_ids': sorted(set(h['tid'] for h in hits)),
            'first_hit_unix': hits[0]['unix'], 'last_hit_unix': hits[-1]['unix'],
            'armed_threads': len(trace['arming']),
            'cleared_and_readback_threads': len(trace['cleanup']['verified']),
            'liveness_samples': len(live['samples']), 'post_samples': len(after),
            'post_cpu_seconds': after[-1]['cpu_seconds'] - after[0]['cpu_seconds'],
            'post_observation_seconds': after[-1]['seconds'] - after[0]['seconds'],
            'trace_api_checks': 'SATISFIED; not a session-health verdict'}
    # Pair only observed pre/post boundaries on the same thread and stack depth.
    # A return breakpoint alone is not a memory-effect capture or allocation proof.
    hits = read('skeletal/capture/result.json')['hits']
    pending, entries, pairs, orphan_post, overwritten_pre = {}, {}, [], [], []
    entry_depth_matches = 0
    for i, h in enumerate(hits):
        tid = h['tid']
        if h['rip'] == 0x3E3C30:
            entries[tid] = h
        elif h['rip'] == 0x3E3C7A:
            if tid in pending:
                overwritten_pre.append(pending[tid][0])
            pending[tid] = (i, h)
            if tid in entries and entries[tid]['rsp'] - h['rsp'] == 40:
                entry_depth_matches += 1
        elif h['rip'] == 0x3E3C7F:
            pre = pending.pop(tid, None)
            if pre and pre[1]['rsp'] == h['rsp']:
                pairs.append((pre[0], i))
            else:
                orphan_post.append(i)
    entry = [h for h in hits if h['rip'] == 0x3E3C30]
    pre = [h for h in hits if h['rip'] == 0x3E3C7A]
    summary['skeletal_order'] = {
        'same_thread_same_stack_pre_post_pairs': len(pairs),
        'orphan_posts': orphan_post, 'overwritten_pres': overwritten_pre,
        'open_pres_at_window_end': [i for i, _ in pending.values()],
        'pres_with_matching_40_byte_entry_frame': entry_depth_matches,
        'distinct_entry_rcx': len(set(h['rcx'] for h in entry)),
        'entry_rcx_range_hex': [hex(min(h['rcx'] for h in entry)), hex(max(h['rcx'] for h in entry))],
        'precall_rcx_range_hex': [hex(min(h['rcx'] for h in pre)), hex(max(h['rcx'] for h in pre))],
        'first_pair_raw_indices': pairs[0] if pairs else None,
        'limits': 'No dereference of captured RCX here; no lifetime, ownership, count, index-array, matrix-write or all-callers inference.'}
    health = read('session-health.json')
    cleanup = read('cleanup.json')
    summary['session_status'] = session_status(True, summary['arms']['skeletal']['hits']['003A1C50'],
                                               health, cleanup['all_26_match_fresh_backup'])
    summary['base_samples'] = [
        {'source': name, 'purpose': r['purpose'], 'unix': r['start_unix'], 'hex': r['hex']}
        for name in ('title-memory.json', 'loaded-before-memory.json', 'loaded-after-memory.json')
        for r in read(name)['reads'] if r['address'] == 0x1F83530]
    summary['input_hashes'] = {
        p.relative_to(E).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in E.rglob('*') if p.is_file() and '__pycache__' not in p.parts
        and p.name not in ('normalized.json', 'assessment-checks.json', 'README.md')}
    return summary


def regression():
    observed = read('session-health.json')
    assert session_status(True, 205, observed, True) == 'INVALID_POST_TRACE'
    assert session_status(True, 205, {}, True) == 'INCOMPLETE'
    assert session_status(True, 205, {'runtime_error_observed': False}, True) == 'INCOMPLETE'
    nominal = {'runtime_error_observed': False, 'responsive_action_observed': True}
    assert session_status(True, 0, nominal, True) == 'INVALID_INSTRUMENT'
    assert session_status(False, 205, nominal, True) == 'INVALID_INSTRUMENT'
    assert session_status(True, 205, nominal, False) == 'INCOMPLETE'
    assert session_status(True, 205, nominal, True) == 'SESSION_CHECKS_SATISFIED'
    return {'actual_runtime_error_rejects_despite_cpu_and_api_positive': True,
            'missing_health_missing_response_zero_hits_bad_trace_missing_restoration_rejected': True,
            'synthetic_nominal_gate_control': True,
            'limit': 'Gate logic regression only; no repaired native instrument or successful live rerun.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--write', action='store_true')
    args = p.parse_args()
    summary, checks = assess(), regression()
    if args.write:
        for name, value in [('normalized.json', summary), ('assessment-checks.json', checks)]:
            with (E / name).open('x', encoding='utf-8') as f:
                json.dump(value, f, indent=2)
                f.write('\n')
    print(json.dumps({'session_status': summary['session_status'], 'order': summary['skeletal_order'], 'checks': checks}, indent=2))
