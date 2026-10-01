import copy,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 data=[]
 for p in s['refs']:
  b=(HERE/p['retained']).read_bytes() if p['retained'] else Path(p['path']).read_bytes()
  assert len(b)==p['bytes'] and sha(b)==p['sha256'];data.append(b)
 events=json.loads(data[0])['hits'];assert events
 times=[h['unix'] for h in events];lo,hi=min(times),max(times)
 assert s['event_unix_range']==[lo,hi]
 for selected,t in zip(s['selected_raw_events'],[lo,hi]):
  assert selected['event']==events[selected['raw_index']] and selected['event']['unix']==t
 assert s['event_recorded_utc_range']==[datetime.fromtimestamp(t,timezone.utc).isoformat() for t in [lo,hi]]
 error=json.loads(data[1]);health=json.loads(data[2]);review=data[5].decode().replace('\r\n','\n');page=data[4].decode().replace('\r\n','\n')
 assert s['health_fields']==health and s['dialog_observed_utc']==error['at']==health['observed_at']
 assert 'onset_at' not in error and 'failure_onset_at' not in health
 assert health['runtime_error_observed'] is True and health['responsive_action_observed'] is False
 assert health['disposition'].startswith('INVALID_POST_TRACE') and health['root_cause'].startswith('UNKNOWN;')
 det=datetime.fromisoformat(error['at'].replace('Z','+00:00'));gap=det.timestamp()-hi
 assert abs(s['reported_clock_gap_seconds']-gap)<1e-8 and 47<gap<49
 assert 'Microsoft Visual C++ Runtime Library' in error['accessibility']['tree'] and 'FFXII_TZA.exe' in error['accessibility']['tree']
 assert '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' in data[3].decode()
 assert 'The hits\n  precede the failure; they are not contaminated by it.' in review
 assert 'The error\'s exact onset and cause were not captured.' in page
 assert 'any semantic promotion' in review and 'ACCEPT-WITH-NARROWING' in review
 return {'recorded_chronology':{'last_hit_recorded_utc':s['event_recorded_utc_range'][1],
  'dialog_observed_utc':error['at'],'reported_clock_gap_seconds':gap},
  'established':'Raw recorded event timestamps precede the recorded dialog observation timestamp under the recorded UTC interpretation.',
  'not_established':'When the fatal condition began, whether it affected events before detection, causal independence, a healthy intervening session or the cause of the failure.',
  'review_correction':'Replace hits precede failure / not contaminated by it with hits precede recorded dialog observation; retain accepted raw sequence/count/pairing, INVALID_POST_TRACE, no semantic promotion and unknown cause.',
  'scope':'Focused review-wording correction, not independent re-review of all hits/contexts, no new gate/platform, no invalid traces promoted.',
  'recovered_review_path':s['board_review_recovery']['actual_review_path'],
  'limits':s['limits'],'consumer_status':'Pending independent review-owner qualification and OPUS acknowledgement.'}
def main():
 s=json.loads((HERE/'primary.json').read_text());out=derive(s);controls=[]
 for name,change in [('dialog-relabelled-as-failure-onset',lambda q:q.update(dialog_observed_utc='failure_onset:'+q['dialog_observed_utc'])),
  ('missing-unknown-cause-qualification',lambda q:q['health_fields'].update(root_cause='TRACE CAUSED CRASH'))]:
  q=copy.deepcopy(s);change(q)
  try:derive(q)
  except AssertionError:controls.append({'name':name,'rejected':True});continue
  raise AssertionError('INVALID_CONTROL '+name)
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS','controls':controls,'class':'Historical timestamp/receipt integrity; no live/native/instrument control or campaign'},indent=2)+'\n')
 print('PASS recorded detection chronology only; actual failure onset/cause and semantic health remain unknown/invalid.')
if __name__=='__main__':main()
