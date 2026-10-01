"""One selected shipping resource, reusing the established VBF entry reader."""
import hashlib,json,struct,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT/'agent_flow/tools'));import vbfextract
archive=Path('D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FFXII_TZA.vbf')
entry='gamedata/d3d11/artdata/chr/chara/c10/c1004/mws/c1004.dae.phyre'
with archive.open('rb') as f:
    names,blocks=vbfextract.load_index(f);assert names[entry][1]<=16*1024*1024
    raw=vbfextract.read_entry(f,names,blocks,entry)
    retained=Path('D:/FFXII MP Mod/extracted')/entry;assert retained.read_bytes()==raw
    assert raw[:4]==b'RYHP';hs,ns,platform,nlists=struct.unpack_from('<4I',raw,4)
    assert hs==84 and 0<ns<65536 and 0<nlists<128 and hs+ns+nlists*36<=len(raw)
    (HERE/'mesh.phyre').write_bytes(raw)
    for filename,a,n in [('header.bin',0,hs),('namespace.bin',hs,ns),('listheaders.bin',hs+ns,nlists*36)]:
        (HERE/filename).write_bytes(raw[a:a+n])
    f.seek(0);index_size=struct.unpack('<4sI',f.read(8))[1];assert 0<index_size<64*1024*1024
    f.seek(0);index=f.read(index_size);assert len(index)==index_size
    selected_blocks=[];sb,size,off=names[entry];cursor=off
    for i in range((size+65535)//65536):
        stored=blocks[sb+i] or 65536;f.seek(cursor);b=f.read(stored);assert len(b)==stored
        selected_blocks.append({'index':sb+i,'archive_offset':cursor,'bytes':stored,'sha256':hashlib.sha256(b).hexdigest()});cursor+=stored
    result={'method':'A one original authored resource; no game execution',
      'archive':str(archive),'archive_size':archive.stat().st_size,'archive_mtime_ns':archive.stat().st_mtime_ns,
      'archive_index_bytes':index_size,'archive_index_sha256':hashlib.sha256(index).hexdigest(),
      'entry':entry,'entry_tuple':names[entry],'entry_bytes':len(raw),'entry_sha256':hashlib.sha256(raw).hexdigest(),
      'selected_stored_blocks':selected_blocks,'retained_extract_identical':True,
      'extractor_sha256':hashlib.sha256((ROOT/'agent_flow/tools/vbfextract.py').read_bytes()).hexdigest(),
      'slices':{fn:{'entry_offset':a,'bytes':n,'sha256':hashlib.sha256(raw[a:a+n]).hexdigest()} for fn,a,n in [('header.bin',0,hs),('namespace.bin',hs,ns),('listheaders.bin',hs+ns,nlists*36)]},
      'limits':'Whole31GB archive content not hashed. Exact index, stored selected blocks, complete decompressed entry and retained-equality are recorded. Authored list is not observed runtime allocation.'}
    assert len(index)==index_size
    (HERE/'source.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Selected',entry,len(raw),'bytes; namespace',ns,'lists',nlists,'retained equality true')
