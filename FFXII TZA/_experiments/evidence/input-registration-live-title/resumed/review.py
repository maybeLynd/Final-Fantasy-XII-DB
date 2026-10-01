"""Verify preserved live captures; never turns absent keyboard positives into PASS."""
from pathlib import Path
import json,gzip,hashlib,statistics,datetime
E=Path(__file__).resolve().parent
j=json.loads((E/'observation.json').read_text());assert j['status']=='INCONCLUSIVE_POSITIVE_NOT_ESTABLISHED'
sha=lambda b:hashlib.sha256(b).hexdigest()
for label,meta in j['raw'].items():
 zipped=(E/meta['file']).read_bytes();raw=gzip.decompress(zipped)
 assert len(zipped)==meta['gzip_bytes'] and sha(zipped)==meta['gzip_sha256']
 assert len(raw)==meta['raw_bytes'] and sha(raw)==meta['raw_sha256']
 r=json.loads(raw);s=r['samples'];w=j['windows'][label]
 assert len(s)==w['samples']==3647 and r['status']=='RECORDED_ONLY' and r['read_handle_closed']
 assert r['null_read_rejected'] and r['known_read_control']==r['known_read_control_after']=='19930d0a1a0a'
 assert r['module_verdict']==r['module_verdict_after']=='clean'
 assert len(r['modules'])==w['module_count'] and len(r['modules_after'])==w['post_module_count']
 assert r['code_identity']==w['code_identity'] and len(r['code_identity'])==1
 assert r['code_identity'][0]['matches'] and r['code_sha256_after']==r['code_identity'][0]['disk_sha256']
 assert all(x['status']=='STABLE_CHAIN' and x['chain_before']==x['chain_after'] and bytes.fromhex(x['raw'])==bytes(256) and x['nonzero_indices']==[] for x in s)
 assert w['nonzero_samples']==0 and w['all_raw_bytes_zero']
 starts=[x['start_unix'] for x in s];gaps=[1000*(b-a) for a,b in zip(starts,starts[1:])]
 assert w['sample_gap_ms']==dict(min=min(gaps),median=statistics.median(gaps),max=max(gaps))
 assert w['start_unix']==starts[0] and w['end_unix']==starts[-1]
 assert w['stamp_values']==sorted({x['frame_before'] for x in s}|{x['frame_after'] for x in s})==[0]
 assert w['chain_addresses']==sorted({x['array_address'] for x in s})
 if label=='positive':
  inp=j['input'];assert starts[0]<inp['start_unix']<inp['end_unix']<starts[-1]
  assert sum(inp['start_unix']<=t<=inp['end_unix'] for t in starts)==inp['samples_starting_during_call']==9
bad=json.loads((E/'noinput-initial-invalid.json').read_text());assert bad['status']=='INVALID' and bad['module_verdict']=='unreadable' and bad['samples']==[]
c=json.loads((E/'cleanup.json').read_text());b=json.loads((E/'save-before.json').read_text());assert c['status']=='RESTORED' and c['processes']==[] and c['files']==b['files'] and len(c['files'])==26 and c['backup_unchanged']
print('Verified two3647-sample captures and initialINVALID, lossless raw hashes, input-time bracket and26-file cleanup; keyboard positive remains NOT ESTABLISHED.')
