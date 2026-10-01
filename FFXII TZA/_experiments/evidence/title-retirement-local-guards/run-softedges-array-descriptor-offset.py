"""One checked invocation of the named original F4 source capture.

Read METHODS.md first. No failed/old output may reach reduction. Controls below
exercise this actual procedure with disposable labelled producer output; they
are procedural tests, not original-code executions or FF12 evidence.
"""
import hashlib, importlib.util, json, pathlib, sys

W = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('delivery', W/'prepare-residue-packet-publication.py')
delivery = importlib.util.module_from_spec(spec); spec.loader.exec_module(delivery)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def capture_then_read(argv, output, driver_hash, receipt, stages):
    stages.append('check_fresh_output')
    if output.exists(): raise ValueError('existing output: immutable/stale, reconcile instead of reading')
    stages.append('invoke_checked_producer')
    delivery.checked_run(argv, timeout=45, receipt_prefix=receipt)
    stages.append('verify_output_exists')
    if not output.is_file(): raise ValueError('successful exit without evidence output')
    stages.append('read_output')
    r = json.loads(output.read_text())
    if r.get('wrapper_complete') is not True or r.get('invocation_driver_sha256') != driver_hash:
        raise ValueError('incomplete/wrong-driver source output')
    stages.append('source_available_for_reduction')
    return r

def main():
    controls = W/'softedges-array-offset-invocation-controls-01'
    controls.mkdir()  # refuse a rerun over historical fixtures/receipts
    outcomes = []
    for name, command, expected in [
        ('failed-writes-readable-output',
         "import pathlib,sys;pathlib.Path(sys.argv[1]).write_text('{\"wrapper_complete\":true,\"invocation_driver_sha256\":\"fixture\"}');sys.exit(7)",
         'upstream exit 7'),
        ('zero-exit-missing-output', 'pass', 'successful exit without evidence'),
        ('preexisting-stale-output', 'raise AssertionError("must not invoke")', 'existing output'),
    ]:
        output = controls/(name+'.json'); stages = []
        if name == 'preexisting-stale-output': output.write_text('{"wrapper_complete":true}')
        error = None
        try:
            capture_then_read([sys.executable, '-c', command, str(output)], output, 'fixture', controls/(name+'-receipt'), stages)
        except (RuntimeError, ValueError) as e: error = str(e)
        if error is None or expected not in error or 'read_output' in stages:
            raise AssertionError('required failed prerequisite reached read: '+name)
        outcomes.append(dict(control=name, status='REFUSED_BEFORE_READ', stages=stages, error=error,
                             labelled_synthetic=True, output_exists=output.exists()))
    producer = W/'capture-softedges-array-descriptor-offset.py'
    output = W/'softedges-array-descriptor-offset-code-01.json'; stages=[]
    driver_hash = sha(producer)
    r = capture_then_read([sys.executable, str(producer)], output, driver_hash,
                          W/'softedges-array-descriptor-offset-repaired-invocation-02', stages)
    result = dict(status='VALID_SOURCE_CAPTURE_NOT_SEMANTIC_CLOSURE',
                  actual_invocation_stages=stages, controls=outcomes,
                  producer=producer.name, producer_sha256=driver_hash,
                  source=output.name, source_sha256=sha(output),
                  runner_sha256=sha(pathlib.Path(__file__)),
                  checked_run_helper_sha256=sha(W/'prepare-residue-packet-publication.py'),
                  ranges=[dict(start=x['start'],end_exclusive=x['end_exclusive'],sha256=x['sha256']) for x in r['ranges']],
                  limits='Method A original bytes. Three actual procedural refusals and successful current producer; no native or game execution. Timeout raises/kills child before read; timeout receipt handling is not certified here.')
    with (W/'softedges-array-descriptor-offset-invocation-02.json').open('x') as f: json.dump(result,f,indent=2)
    print('Checked current source available; three failed/stale/missing prerequisites refused before read')

if __name__ == '__main__': main()
