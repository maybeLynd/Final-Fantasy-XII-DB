"""Reproduce the four offline release/stop controls without OS input."""
import json
from pathlib import Path
import pulse

results = []
for mode in ('positive', 'lost_focus', 'escape_before_down', 'partial_down'):
    elapsed, down, sent, reads = [0.0], [False], [], [0]

    def clock():
        return elapsed[0]

    def sleep(n):
        elapsed[0] += n

    def snapshot():
        reads[0] += 1
        return dict(status='STABLE_CHAIN', array_address=1234,
                    nonzero_indices=[49] if down[0] else [])

    def send(up):
        sent.append(up)
        down[0] = not up
        return 1 if mode == 'partial_down' and not up else 2

    def guard():
        if mode == 'lost_focus' and down[0]:
            raise AssertionError('STOP: foreground changed')
        if mode == 'escape_before_down':
            raise AssertionError('STOP: Escape input')

    record, error = {}, None
    try:
        pulse.pulse(snapshot, send, guard, record, 49, clock, sleep)
    except AssertionError as exc:
        error = str(exc)
    assert not down[0]
    if mode == 'positive':
        assert not error and record['registration'] and sent == [False, True]
    elif mode == 'escape_before_down':
        assert error and sent == []
    else:
        assert error and sent == [False, True]
    results.append(dict(case=mode, error=error, send_up_flags=sent,
                        down_after=down[0], reads=reads[0]))

original = json.loads(Path(__file__).with_name('guard-controls.json').read_text())
assert original['results'] == results
print('Four original offline guard controls reproduced; no OS input or process access.')
