"""Bounded original-byte preparation lookup; not a progress/disposition reporter.

Usage: python locate-retained-span.py START_HEX END_HEX FRESH_OUTPUT
Search source maps including retained subfolders before preparing a new capture.
Physical coverage only. A match does not award semantics, live state or acceptance.
"""
import hashlib,json,struct,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path.cwd();W=Path(__file__).resolve().parent
def main():
 lo,hi=int(sys.argv[1],16),int(sys.argv[2],16);out=Path(sys.argv[3])
 if not 0<hi-lo<=4096 or out.exists():raise ValueError('bounded fresh-output precondition')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 if hashlib.sha256(raw).hexdigest()!=pin:raise ValueError('reference image changed')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];wanted=None
 for k in range(struct.unpack_from('<H',raw,pe+6)[0]):
  vs,rva,sz,off=struct.unpack_from('<IIII',raw,pe+32+opt+40*k)
  if 0x120000+rva<=lo and hi<=0x120000+rva+sz:wanted=raw[off+lo-0x120000-rva:off+hi-0x120000-rva]
 if wanted is None:raise ValueError('requested span not file backed')
 paths=subprocess.run(['rg','--files',str(W),'Database/FFXII TZA/_experiments/evidence','-g','*.json'],capture_output=True,timeout=15)
 if paths.returncode or paths.stderr or not paths.stdout:raise ValueError('source enumeration failed/missing')
 matches=[];malformed=[];examined=0
 for name in paths.stdout.decode().splitlines():
  p=Path(name);parts=[s.casefold() for s in p.parts]
  if any(s.startswith(('controls','metadata-controls','publication-','frozen','history')) or 'frozen-ready' in s for s in parts) or not('source' in p.name.casefold() or 'raw' in p.name.casefold()):continue
  if p.stat().st_size>8*1024*1024:continue
  data=p.read_bytes()
  try:x=json.loads(data)
  except (ValueError,UnicodeError):malformed.append(str(p));continue
  # Some historical source records are lists; they are not this map schema.
  if not isinstance(x,dict) or x.get('exe_sha256')!=pin or not isinstance(x.get('ranges'),list):continue
  examined+=1
  for r in x['ranges']:
   if not isinstance(r,dict) or not all(k in r for k in ['start','end_exclusive','instructions']):continue
   a,b=int(r['start'],16),int(r['end_exclusive'],16)
   if a<=lo and hi<=b:
    blob=bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))
    if len(blob)==b-a and blob[lo-a:hi-a]==wanted:matches.append(dict(path=str(p.resolve()),file_sha256=hashlib.sha256(data).hexdigest(),range=[r['start'],r['end_exclusive']],range_sha256=hashlib.sha256(blob).hexdigest()))
 with out.open('x') as f:json.dump(dict(complete=True,driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),exe_sha256=pin,requested=[hex(lo),hex(hi)],requested_sha256=hashlib.sha256(wanted).hexdigest(),maps_examined=examined,matches=matches,malformed_candidates=malformed,decision='REUSE_VERIFIED_RETAINED_BYTES' if matches else 'NO_COVERING_MAP_IN_SEARCHED_CORPUS',limits='Bounded physical byte coverage in named source-map corpus, not global absence, provenance acceptance, source semantics or live initialization. Retain/check original lineage and receipts before semantic use.'),f,indent=2)
 print(json.dumps(dict(matches=len(matches),decision='REUSE' if matches else 'NO_COVERING_MAP',malformed_candidates=len(malformed))))
if __name__=='__main__':main()
