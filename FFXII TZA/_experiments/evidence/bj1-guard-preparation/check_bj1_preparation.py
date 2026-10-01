"""Checked original-input and actual invocation receipts; no live game actions."""
import json
from pathlib import Path
import sys
import bj1_guard_capture as target


def main(folder):
    cov = json.loads((folder/'bj1-retained-coverage-01.json').read_text())
    if cov != target.retained_coverage():
        raise ValueError('retained coverage/current original preimage differs')
    for prefix, driver, expected in [('bj1-retained-coverage-run-01','bj1_guard_capture.py',0),
                                     ('bj1-transport-controls-run-04','control_bj1_guard_capture.py',0)]:
        status = json.loads((folder/(prefix+'.status.json')).read_text())
        if status['exit']!=expected or status['driver_sha256']!=target.digest(folder/driver):
            raise ValueError('required upstream execution failed/stale')
        if not (folder/(prefix+'.stdout')).read_bytes().strip() or (folder/(prefix+'.stderr')).read_bytes():
            raise ValueError('missing/error upstream output')
    controls = json.loads((folder/'bj1-transport-controls-04.json').read_text())
    if (controls['status']!='PASS_TRANSPORT_ONLY_CONTEXT_STILL_REQUIRED' or
            controls['collector_sha256']!=target.digest(folder/'bj1_guard_capture.py') or
            controls['driver_sha256']!=target.digest(folder/'control_bj1_guard_capture.py') or
            controls['reused_reader_sha256']!=target.digest(target.ROOT/'Database/Tools/analysis-kit/gfz-scripts/runtime_probe.py')):
        raise ValueError('instrument invocation identity changed')
    positive = controls['positive_capture']
    expected = [0,0xFFFFFFFF,0x80000001,0x80000000,1]+[0x80000000+i for i in range(6,1682)]
    if (positive['status']!='COLLECTED_CONTEXT_PENDING' or
            [x['value'] for x in positive['guard_values']]!=expected or
            len(controls['controls'])!=4 or not all(c['refused'] for c in controls['controls']) or
            controls['popen_pid']!=controls['fixture']['pid'] or
            controls['redirector_control']['same_pid'] or not controls['handle_closed'] or
            controls['child_exit']!=0 or controls['redirector_cleanup']['exit']!=0 or
            controls['child_stderr'] or controls['redirector_cleanup']['stderr']):
        raise ValueError('control/cleanup incomplete')
    # Preserve failed results as failed; no downstream PASS may hide them.
    for n in [1,2]:
        if json.loads((folder/('bj1-transport-controls-run-%02d.status.json'%n)).read_text())['exit']!=1:
            raise ValueError('historical failed control status overwritten')
        if json.loads((folder/('bj1-transport-controls-%02d.json'%n)).read_text())['status']!='INVALID':
            raise ValueError('historical invalid result promoted')
    if [c['covered_targets'] for c in cov['captures']]!=[0,0,3] or cov['captures'][2]['closure_eligible'] is not False:
        raise ValueError('invalid retained values escaped scope')
    print('BJ1_PREPARATION_VALID_LIVE_QUESTION_OPEN; upstream/identities/controls/cleanup checked; no game semantics')


if __name__=='__main__':
    main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent)
