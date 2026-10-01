"""Independent MP16 public-path boundaries. No producer test suite/server."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback

sys.dont_write_bytecode = True
PIN = 'b47e084f994abcfdb12a4edb43088934b118eff241d33d002e5e6ac5438a2d84'
COMMIT = '0aa544606e35de0b2f6056b0af469fa048d7fe8a'
P = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, default=P/'terminal-01/requirements.py')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise ValueError('refusing to overwrite an existing result')
    receipt = json.loads((P/'terminal-01/git-source-receipt.json').read_text())
    if (receipt.get('returncode') != 0 or receipt.get('stderr')
            or receipt.get('stdout_bytes', 0) <= 0
            or receipt.get('sha256') != PIN or receipt.get('commit') != COMMIT):
        raise ValueError('required successful original-source receipt missing')
    if hashlib.sha256(args.source.read_bytes()).hexdigest() != PIN:
        raise ValueError('required exact original source identity failed')
    spec = importlib.util.spec_from_file_location('astra_original_requirements_0aa', args.source)
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)

    subs = P/'terminal-01/subsystems.tsv'
    cmap_file = P/'terminal-01/category-map.tsv'
    # Real public input readers, no monkey-patched producer functions.
    cmap = R.load_map(cmap_file)
    reporter = json.loads((P/'terminal-01/reporter-base.json').read_text())
    facts = json.loads((P/'terminal-01/facts.json').read_text())
    board = {'tasks': []}
    gate_not = {'verdict': 'NOT_MET', 'remaining': 'fixture: no accepted receipt',
                'detail': ['acceptance: UNMET -- fixture: no receipt']}
    gate_ok = {'verdict': 'MET', 'remaining': None,
               'detail': ['acceptance: OK -- fixture: accepted full run']}
    cases = []
    counter_values = [-1, *range(32), None, True, False, '29', 29.0]
    for accepted, gate in [(False, gate_not), (True, gate_ok)]:
        for i, k in enumerate(counter_values):
            rep = copy.deepcopy(reporter)
            rep['levels']['terminal_certification']['final_audits_declared'] = k
            observed = (None if accepted or type(k) is not int or not 0 < k < 30
                        else {'pass': k, 'of': 30})
            cases.append((f'counter-{int(accepted)}-{i}', rep, gate, False,
                          30 if accepted else 0, observed))
        for i, req in enumerate([0, 29, 31, None, True, False, '30', 30.0]):
            rep = copy.deepcopy(reporter)
            rep['levels']['terminal_certification']['required_consecutive'] = req
            cases.append((f'invalid-required-{int(accepted)}-{i}', rep, gate, True, None, None))
        rep = copy.deepcopy(reporter)
        del rep['levels']['terminal_certification']['required_consecutive']
        cases.append((f'protocol-default-{int(accepted)}', rep, gate, False,
                      30 if accepted else 0, None))
    for label, terminal in [('none', None), ('list', [])]:
        rep = copy.deepcopy(reporter)
        rep['levels']['terminal_certification'] = terminal
        cases.append((f'invalid-terminal-{label}', rep, gate_not, True, None, None))
    rep = copy.deepcopy(reporter)
    del rep['levels']
    cases.append(('missing-levels', rep, gate_not, True, None, None))
    for label, details in [('absent', None), ('empty', [])]:
        gate = copy.deepcopy(gate_not)
        if details is None:
            del gate['detail']
        else:
            gate['detail'] = details
        cases.append((f'no-acceptance-{label}', reporter, gate, False, 0, None))

    records = []
    for label, rep, gate, invalid, expected_t, expected_obs in cases:
        raw = {'case': label, 'reporter': rep, 'gate': gate,
               'expected': {'invalid_T': invalid, 'accepted_T': expected_t,
                            'observed': expected_obs}}
        checks = {}
        try:
            try:
                tf, acc, req = R.terminal_facts(gate, rep)
                raw['terminal_facts'] = {'facts': tf, 'accepted': acc, 'required': req}
            except Exception as e:
                raw['terminal_facts_exception'] = {'type': type(e).__name__, 'text': str(e)}
            try:
                raw['terminal_observed'] = R.terminal_observed(gate, rep)
            except Exception as e:
                raw['terminal_observed_exception'] = {'type': type(e).__name__, 'text': str(e)}
            m = R.measure(copy.deepcopy(facts), cmap, board, rep, gate, str(subs))
            raw['measure'] = m
            if invalid:
                checks['helper_refuses'] = 'terminal_facts_exception' in raw
                checks['public_prerequisite_failure'] = ('T' in m['failed'] and
                    m['terminal'] == {'accepted': None, 'required': 30} and
                    not m['measured'] and not m['ready'])
            else:
                f = raw['terminal_facts']
                checks['complete_thirty_facts'] = (f['required'] == 30 and
                    [x['k'] for x in f['facts']] == [f'T:{i:02}' for i in range(1, 31)])
                checks['accepted_all_or_none'] = (f['accepted'] == expected_t and
                    sum(x['ok'] for x in f['facts']) == expected_t and
                    all(x['ok'] == bool(expected_t) for x in f['facts']))
                checks['public_T'] = (m['terminal'] == {'accepted': expected_t, 'required': 30}
                    and m['families']['T'] == {'accepted': expected_t, 'total': 30})
                # Four required MET L2 cells plus one accepted K fixture = five.
                checks['union_excludes_observed_counter'] = (m['scopes']['union'] ==
                    {'accepted': 5 + expected_t, 'total': 35})
                checks['public_readiness'] = (m['measured'] and not m['failed'] and
                    m['ready'] == (gate['verdict'] == 'MET' and expected_t == 30))
                o = raw.get('terminal_observed')
                norm = None if o is None else {k: o[k] for k in ('pass', 'of')}
                checks['observed_separate'] = (norm == expected_obs and m['terminal_observed'] == o
                    and (o is None or o['state'] == 'observed, not accepted'))
        except Exception as e:
            raw['unexpected_exception'] = {'type': type(e).__name__, 'text': str(e),
                                            'traceback': traceback.format_exc()}
            checks['no_unexpected_exception'] = False
        raw['checks'] = checks
        raw['pass'] = bool(checks) and all(checks.values())
        records.append(raw)
    passed = bool(records) and len(records) == len(cases) and all(r['pass'] for r in records)
    out = {'method': 'exact historical dashboard Python on labelled fixtures, not game/live/whole deployment',
           'source_commit': COMMIT, 'source_sha256': PIN,
           'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'python': sys.version, 'case_count': len(records),
           'input_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [subs, cmap_file, P/'terminal-01/reporter-base.json', P/'terminal-01/facts.json']},
           'records': records, 'complete': len(records) == len(cases) and bool(records),
           'status': 'PASS_SCOPED_MP16' if passed else 'FAIL_OR_INCOMPLETE'}
    args.out.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': out['status'], 'case_count': len(records),
                      'failures': [r['case'] for r in records if not r['pass']]}))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
