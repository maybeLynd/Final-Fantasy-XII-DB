"""Additional discriminator controls; reuse the already validated original-code runner."""
from pathlib import Path
import hashlib

instrument=Path('Database/Tools/work/ASTRA/render_event_probe.py')
text=instrument.read_text()
exec(compile(text[:text.index("case('cached-full-width-control'")],str(instrument),'exec'))
output=WORK/'render-event-selection-controls.json'
out['base_instrument_sha256']=hashlib.sha256(instrument.read_bytes()).hexdigest()
out['limits'][-1]='Exact 64-byte shipping priority window mapped; only indices1/5 tested, not the full table extent.'
original_setup=setup
priority=json.loads((WORK/'render-event-priority.json').read_text())
assert priority['exe_sha256']==sha
priority_bytes=bytes.fromhex(priority['hex'])
assert hashlib.sha256(priority_bytes).hexdigest()==priority['sha256']
out['priority_source_sha256']=hashlib.sha256((WORK/'render-event-priority.json').read_bytes()).hexdigest()

def setup(**kw):
    return original_setup(**kw)+[(0x1F00410,priority_bytes)]

case('selector2-rejects-lower-priority',0x4235C0,(RECORD,0x2001,2,0),0,cc=0x2005,cached=PAYLOAD)
case('getter-same-events-selects-alternate',0x41FCA0,(RECORD,0,0,0),0x2001,cc=0x2005,ce=0x2001,cached=PAYLOAD)
case('selector2-accepts-higher-priority',0x4235C0,(RECORD,0x2005,2,0),1,cc=0x2001,cached=PAYLOAD)
case('selector0-entry-bit12-clear-rejects',0x4235C0,(RECORD,0x2001,0,0),0,cc=0x2005,cached=PAYLOAD)
case('selector0-entry-bit12-set-accepts',0x4235C0,(RECORD,0x2001,0,0),1,cc=0x2005,cached=PAYLOAD,entry_flags=0x1000)
case('selector1-accepts',0x4235C0,(RECORD,0x2001,1,0),1,cc=0x2005,cached=PAYLOAD)
case('selector-other-accepts',0x4235C0,(RECORD,0x2001,0x2005,0),1,cc=0x2005,cached=PAYLOAD)
print('Completed distinct caller-policy controls:',len(out['cases']))
