"""Check the actual current producer's failed-prerequisite invocation.

The failed receipt is explicitly synthetic. The child CLI, exception/exit,
driver hash, rejection marker and absent result are actual observations.
"""
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
def main():
    output=P/sys.argv[1];need(not output.exists(),'fresh output required')
    driver=P/'prove-native-relation-invariant.py';dh=sha(driver)
    positive=json.loads((P/'prove-native-relation-invariant-02.status.json').read_text())
    result=json.loads((P/'result-native-relation-invariant-02.json').read_text())
    need(positive.get('terminal') is True and positive.get('exit')==0 and positive.get('exception') is None and positive['driver_sha256']==dh==result['driver_sha256'] and result.get('producer_complete') is True,'matching successful producer required')
    stem='prove-native-relation-refusal-01'
    st=json.loads((P/(stem+'.status.json')).read_text())
    failed=P/'reviewed-boundaries-failed-prerequisite-01.json'
    need(json.loads(failed.read_text())==dict(terminal=True,exit=1,exception=None,label='Synthetic failed qualification receipt'),'labelled failed prerequisite changed')
    need(st.get('terminal') is True and st.get('exit')==1 and st.get('exception') is None and st.get('driver_sha256')==dh,'actual child refusal/identity required')
    need(st['argv'][2:]==[str(driver),'result-native-relation-refused-01.json',failed.name],'actual invocation arguments changed')
    need(b'successful upstream qualification required' in (P/(stem+'.stderr')).read_bytes(),'specific prerequisite rejection required')
    need(not (P/'result-native-relation-refused-01.json').exists(),'failed upstream produced result')
    output.write_text(json.dumps(dict(producer_complete=True,driver_sha256=sha(Path(__file__)),tested_producer_sha256=dh,control='Actual current CLI rejects labelled failed upstream; terminal exit1/exceptionnull/specific marker/no result; matching positive retained',positive_status_sha256=sha(P/'prove-native-relation-invariant-02.status.json'),positive_result_sha256=sha(P/'result-native-relation-invariant-02.json'),failure_status_sha256=sha(P/(stem+'.status.json')),failed_input_sha256=sha(failed),limits='Synthetic qualification defect; actual producer refusal. Not native execution, independent review or gameplay.'),indent=2)+'\n')
    print('Actual prerequisite refusal and matching successful producer verified; no native/game run.')
if __name__=='__main__':main()
