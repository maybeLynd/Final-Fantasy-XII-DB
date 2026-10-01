"""One bounded shipping status table, no live process access."""
import hashlib,json,struct,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'agent_flow/tools'));import vbfextract
archive=Path('D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FFXII_TZA.vbf')
entry='ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin'
sha=lambda b:hashlib.sha256(b).hexdigest()
with archive.open('rb') as f:
    names,blocks=vbfextract.load_index(f);assert names[entry][1]<1024*1024
    raw=vbfextract.read_entry(f,names,blocks,entry)
    table=struct.unpack_from('<I',raw,0x40)[0]
    assert raw[table:table+4]==b'st2e',hex(table)
    count,stride=struct.unpack_from('<IH',raw,table+4)
    relative=struct.unpack_from('<I',raw,table+12)[0]
    assert count==32 and stride==40 and relative==0x20
    end=table+relative+count*stride;assert end<=len(raw)
    (HERE/'status-table.bin').write_bytes(raw[table:end])
    (HERE/'directory.bin').write_bytes(raw[:0x44])
    f.seek(0);index_size=struct.unpack('<4sI',f.read(8))[1];assert 0<index_size<64*1024*1024
    f.seek(0);index=f.read(index_size);assert len(index)==index_size
    selected=[];sb,size,off=names[entry];cursor=off
    for i in range((size+65535)//65536):
        stored=blocks[sb+i] or 65536;f.seek(cursor);b=f.read(stored);assert len(b)==stored
        selected.append({'index':sb+i,'archive_offset':cursor,'bytes':stored,'sha256':sha(b)});cursor+=stored
    record={'method':'A: exact authored resource; no live or isolated execution',
      'archive':str(archive),'archive_size':archive.stat().st_size,'archive_mtime_ns':archive.stat().st_mtime_ns,
      'index_bytes':index_size,'index_sha256':sha(index),'entry':entry,'entry_tuple':names[entry],
      'entry_bytes':len(raw),'entry_sha256':sha(raw),'stored_blocks':selected,
      'directory_bytes':0x44,'directory_sha256':sha(raw[:0x44]),'table_file_offset':table,
      'table_bytes':end-table,'table_sha256':sha(raw[table:end]),
      'extractor_sha256':sha((ROOT/'agent_flow/tools/vbfextract.py').read_bytes()),
      'observer_path':'Database/Tools/analysis-kit/gfz-scripts/hwbp.py',
      'observer_sha256':sha((ROOT/'Database/Tools/analysis-kit/gfz-scripts/hwbp.py').read_bytes()),
      'limits':'One US entry, no other languages. Whole archive content not hashed. Table values do not prove readers, native binding, lifecycle or meaning.'}
    (HERE/'source.json').write_text(json.dumps(record,indent=2)+'\n')
    data=raw[table+relative:end];slots=[0x11,0x12,*range(0x14,0x20)]
    for rowid in (3,6,14,26):
        row=data[rowid*stride:(rowid+1)*stride]
        print(rowid, row[:4].hex(), {hex(i):row[i] for i in slots if row[i]!=255})
    print('SOURCE',hex(table),len(raw),end-table,flush=True)
