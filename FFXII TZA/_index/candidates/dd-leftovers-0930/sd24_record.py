"""SD-24: which record a Sound object's +0x30 holds - SabFile::Sound or SabFile::Sequence (SWE2-DATA 2026-09-30),
static: the original code and every shipped .sab.

Code.
  R1 the view the select walkers build over [this+0x30] (007E5939 / 007E593D in Order 007E58D0; 007E681D / 007E6828
     in 007E67C0) pairs it with vtable 01CB43E0; the vtable's RTTI complete-object locator names its class.
  R2 the entry accessor 007CFAC0 locates the entry table at u16 [rec+0x1A] when the record version byte is above 5,
     at u16 [rec+2] otherwise, and returns a view with vtable 01CB6E40 (SoundSequenceInfo); the by-key resolver's views
     use 01CB4D58 (Sequence) / 01CB4D48.
  R3 the bind 007BDDA0 stores the source's +0x18 at +0x30 (007BDDDD / 007BDDE1) and then reads that record's version
     byte against 0x0C and its byte +0x4E (007BDE49 / 007BDE4E) - a field past the end of a 64-byte record.
  R4 the SwitchSound parameter getter 007BD9D0 reads the same pointer [this+0x30] and takes its name path when that
     record's version is 10 or more and its byte +4 is 5 (007BD9FB..007BDA0A) - the Sound record's class byte, 5 =
     SwitchSound (the factory 007B2F70), not a Sequence field.
Data (all shipped .sab under D:/FFXII_TZA_extract):
  D1 every 'snd ' record is version 16 and every 'seq ' record version 4, 64 bytes apart;
  D2 read as a Sound record (version 16 > 5: table at u16 +0x1A, count byte +5, 16-byte entries), every entry's
     u16 +4 key is a valid index into the same bank's 'seq ' table (the resolver's table);
  D3 over every snd record, byte +4 (the class byte) is 0 or 1 and byte +5 (the entry count) is 0 or 1, so no shipped
     record reaches R4's name path (it needs +4 = 5) although every one passes its version test (16 >= 10);
  X  control: the same snd records read with the version-4 rule (table at u16 +2) do not give valid keys throughout,
     so D2 discriminates between the two readings.
"""
import glob, os, re, struct, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def q(va):
    return struct.unpack_from("<Q", d, off(va))[0]


def rtti(vt):
    col = q(vt - 8)
    td = 0x120000 + struct.unpack_from("<I", d, off(col + 12))[0]
    o = off(td + 16)
    return d[o:d.index(b"\0", o)].decode()


def rip_t(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


names = {vt: rtti(vt) for vt in (0x01CB43E0, 0x01CB6E40, 0x01CB4D58, 0x01CB4D48)}
for vt, n in names.items():
    print("   vtable %08X -> %s" % (vt, n))
o = {x.address: x for x in dis(0x007E58D0)}
w = {x.address: x for x in dis(0x007E67C0)}
check("R1 both walkers pair [this+0x30] with vtable 01CB43E0, whose RTTI class is SabFile::Sound",
      o[0x007E5939].op_str == "rdx, qword ptr [r15 + 0x30]" and rip_t(o[0x007E593D]) == 0x01CB43E0
      and w[0x007E681D].op_str == "rax, qword ptr [rdi + 0x30]" and rip_t(w[0x007E6828]) == 0x01CB43E0
      and names[0x01CB43E0] == ".?AVSound@SabFile@Sd@SQEX@@", names[0x01CB43E0])
a = {x.address: x for x in dis(0x007CFAC0)}
check("R2 007CFAC0: version > 5 -> table u16 [+0x1A], else u16 [+2]; entries are SoundSequenceInfo views",
      a[0x007CFACB].op_str == "byte ptr [r9], 5" and a[0x007CFAD1].op_str == "eax, word ptr [r9 + 2]"
      and a[0x007CFAD8].op_str == "eax, word ptr [r9 + 0x1a]" and rip_t(a[0x007CFAE3]) == 0x01CB6E40
      and names[0x01CB6E40] == ".?AVSoundSequenceInfo@SabFile@Sd@SQEX@@")
check("R2b the resolved candidate's view class is SabFile::Sequence", names[0x01CB4D58] == ".?AVSequence@SabFile@Sd@SQEX@@")
b = {x.address: x for x in dis(0x007BDDA0)}
check("R3 007BDDA0 stores source +0x18 at +0x30 and reads that record's version >= 0x0C and byte +0x4E",
      b[0x007BDDDD].op_str == "rax, qword ptr [rdx + 0x18]" and b[0x007BDDE1].op_str == "qword ptr [rcx + 0x30], rax"
      and b[0x007BDE49].op_str == "byte ptr [rax], 0xc" and b[0x007BDE4E].op_str == "eax, byte ptr [rax + 0x4e]")
g = {x.address: x for x in dis(0x007BD9D0)}
check("R4 007BD9D0 reads [this+0x30], version >= 0x0A and byte +4 == 5 (the class byte of SwitchSound)",
      g[0x007BD9FB].op_str == "r8, qword ptr [rdi + 0x30]" and g[0x007BD9FF].op_str == "byte ptr [r8], 0xa"
      and g[0x007BDA05].op_str == "byte ptr [r8 + 4], 5")

U32 = lambda b_, o_: struct.unpack_from("<I", b_, o_)[0]
U16 = lambda b_, o_: struct.unpack_from("<H", b_, o_)[0]


def chunks(blob):
    out = {}
    o_ = 0x20
    while o_ + 16 <= len(blob):
        tag = blob[o_:o_ + 4]
        if not all(32 <= c < 127 for c in tag):
            break
        co = U32(blob, o_ + 8)
        if co == 0 or co >= len(blob):
            break
        out[tag] = co
        o_ += 16
    return out


def table(blob, co):
    n = U32(blob, co + 4)
    return [co + U32(blob, co + 0x10 + 4 * i) for i in range(n)]


files = sorted(glob.glob("D:/FFXII_TZA_extract/**/*.sab", recursive=True))
ver_snd, ver_seq, seq_len = collections.Counter(), collections.Counter(), collections.Counter()
cls, cnt5 = collections.Counter(), collections.Counter()
ent = ok16 = bad16 = ok2 = bad2 = 0
banks = 0
for f in files:
    blob = open(f, "rb").read()
    c = chunks(blob)
    if b"snd " not in c or b"seq " not in c:
        continue
    banks += 1
    snd, seq = table(blob, c[b"snd "]), table(blob, c[b"seq "])
    for s in seq:
        ver_seq[blob[s]] += 1
    for a_, b_ in zip(seq, seq[1:]):
        seq_len[b_ - a_] += 1
    for r in snd:
        ver_snd[blob[r]] += 1
        cls[blob[r + 4]] += 1
        cnt5[blob[r + 5]] += 1
        cnt = blob[r + 5]
        t16 = r + U16(blob, r + 0x1A)
        t2 = r + U16(blob, r + 2)
        for i in range(cnt):
            ent += 1
            k16 = U16(blob, t16 + 16 * i + 4) if t16 + 16 * i + 6 <= len(blob) else 1 << 20
            k2 = U16(blob, t2 + 16 * i + 4) if t2 + 16 * i + 6 <= len(blob) else 1 << 20
            ok16 += k16 < len(seq)
            bad16 += not (k16 < len(seq))
            ok2 += k2 < len(seq)
            bad2 += not (k2 < len(seq))
print("   banks with snd + seq: %d of %d files; snd versions %s; seq versions %s; seq spacing (top) %s"
      % (banks, len(files), dict(ver_snd), dict(ver_seq), seq_len.most_common(3)))
check("D1 every snd record is version 16 and every seq record version 4, 64 bytes apart",
      set(ver_snd) == {16} and set(ver_seq) == {4} and seq_len.most_common(1)[0][0] == 64)
print("   snd entries %d: keys valid under the Sound reading (table u16 +0x1A) %d, invalid %d; under the version-4 "
      "reading (u16 +2) %d valid, %d invalid" % (ent, ok16, bad16, ok2, bad2))
check("D2 read as SabFile::Sound records, every entry key indexes the bank's seq table", ent > 0 and bad16 == 0)
print("   snd class byte +4 %s; entry count +5 %s" % (dict(cls), dict(cnt5)))
check("D3 every snd record's class byte +4 is 0 or 1 and its entry count +5 is 0 or 1 (none reaches R4's +4 == 5)",
      set(cls) <= {0, 1} and set(cnt5) <= {0, 1} and sum(cls.values()) == 13150)
check("X  control: the version-4 reading does not give valid keys throughout (the check discriminates)", bad2 > 0)
print("RESULT this+0x30 is a SabFile::Sound record (snd chunk, version 16); its SoundSequenceInfo entries key "
      "SabFile::Sequence records of the seq chunk")
print("FAILS %d" % FAILS)
