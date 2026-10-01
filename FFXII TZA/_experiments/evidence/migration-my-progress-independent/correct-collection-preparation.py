import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;p=W/'collection-controls.py';d=W/'collection-preparation-v1';assert not d.exists(),'Preserve original correction lineage';d.mkdir()
original=p.read_bytes();(d/p.name).write_bytes(original)
facts=W/'collection-01/facts-READY.json';r=json.loads(facts.read_text())
(d/'failure.json').write_text(json.dumps({'status':'INVALID_FIXTURE_STATUS_SHAPE','driver_sha256':hashlib.sha256(original).hexdigest(),
 'facts_sha256':hashlib.sha256(facts.read_bytes()).hexdigest(),'collection_finished':False,
 'cause':'Fixture used DOCUMENTED (SUPERSEDED ...) parenthetical status. Original progress._status_word strips reasons only after space-em-dash-space or space-hyphen-space; full parenthetical token is not STATUS_BEARING.',
 'observed':'Actual collector marked parenthetical page not documented. No completed DD-split acceptance from this attempt.',
 'correction':'Use supported DOCUMENTED - SUPERSEDED reason delimiter; preserve original source/fixture/facts/driver. Add error receipt hook to current collection driver; no producer rule weakened or changed.',
 'limits':'Original fixture contains intentionally stale DOCUMENTED/open-box page. DD literal status parsing is not certification of the five-condition DOCUMENTED ruling; P residue must remain visible.'},indent=2)+'\n')
s=original.decode().replace("D=W/'collection-01'","D=W/'collection-02'").replace('status: DOCUMENTED (SUPERSEDED accepted-disposition residue W-901)','status: DOCUMENTED - SUPERSEDED accepted-disposition residue W-901')
needle="observed={}\nfor state in ('READY','DONE'):"
replacement="""def retain_failure(kind,value,tb):
 raw['fatal']={'type':kind.__name__,'reason':str(value)}
 (D/'raw.json').write_text(json.dumps(raw,indent=2)+'\\n')
 sys.__excepthook__(kind,value,tb)
sys.excepthook=retain_failure
observed={}
for state in ('READY','DONE'):"""
assert s.count(needle)==1;s=s.replace(needle,replacement);p.write_text(s)
print('PRESERVED_STATUS_SHAPE_FAILURE_ADDED_CURRENT_ERROR_RECEIPT',flush=True)
