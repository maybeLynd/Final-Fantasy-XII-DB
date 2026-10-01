"""FCP section 7, parsed the way the sequencer reads it (00477370 start, 00477480 per-frame step, 004776D0 value getter).

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract).
Layout read from code, S = payload + u16[payload + 0x0E]:
    S + 2*event                 u16   offset (from S) of that event's record list
    list + 6*variant            6-byte record: u8 slot, u8 pickParam, u16 rel, u8 enabled, u8 ?
    T = record + 2 + rel + 0x10 choice table: u16 T[choice]; the word at T - 2 (record + 2 + rel + 0x0E) is the number of choices
    seq = T + T[choice] + 2*choice     u16 frameCount, then frameCount x { u16 durationTicks, u8 endAction, u8 value }
Predictions, each of which the files could refute:
  P1  every event offset, record, choice table and sequence lies inside section 7
  P2  slot < 8 (the phase entry has eight per-slot arrays)
  P3  frameCount >= 1; the LAST frame's endAction is 0 (stop), 1 (hold) or 2 (loop) - the only values the stepper acts on
  P4  durations are small positive tick counts
The event count is not stated by the code; it is taken as (first offset) / 2, which is itself checked by P1.
A record whose rel is 0xFFFF or whose enabled byte is 0 is skipped by the engine and is skipped here.
FABLE, 2026-09-19.
"""
import os, struct, glob, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
blocks = have7 = 0
oob = collections.Counter(); slots = collections.Counter(); ends = collections.Counter()
nframes = collections.Counter(); durs = collections.Counter(); values = collections.Counter()
nevents = collections.Counter(); nchoices = collections.Counter(); seqs = 0; recs = 0; skipped = 0
for path in glob.glob(os.path.join(ROOT, "**", "*.cm"), recursive=True):
    d = open(path, "rb").read()
    i = d.find(b"@FCP")
    if i < 0:
        continue
    size = struct.unpack_from("<I", d, i + 8)[0]
    pay = d[i + 0x30: i + size]
    blocks += 1
    offs = list(struct.unpack_from("<18H", pay, 0)) + [u16(pay, 0x24)]
    o7 = offs[7]
    if not o7:
        continue
    have7 += 1
    later = sorted(o for k, o in enumerate(offs) if k not in (0, 7) and o > o7)
    end = later[0] if later else len(pay)
    sec = pay[o7:end]
    n_ev = u16(sec, 0) // 2
    nevents[n_ev] += 1
    ev_offs = [u16(sec, 2 * e) for e in range(n_ev)]
    bounds = sorted(set(ev_offs)) + [len(sec)]
    for e, eo in enumerate(ev_offs):
        if eo >= len(sec):
            oob["event offset"] += 1
            continue
        rec = eo                                  # variant 0 only: the variant count is not stated by the code
        if rec + 6 > len(sec):
            oob["record"] += 1
            continue
        slot, pick, rel, enabled = sec[rec], sec[rec + 1], u16(sec, rec + 2), sec[rec + 4]
        recs += 1
        if rel == 0xFFFF or not enabled:
            skipped += 1
            continue
        slots[slot] += 1
        T = rec + 2 + rel + 0x10
        if T > len(sec) or T < 2:
            oob["choice table"] += 1
            continue
        nc = u16(sec, T - 2)
        nchoices[nc] += 1
        for c in range(nc):
            if T + 2 * c + 2 > len(sec):
                oob["choice offset"] += 1
                break
            seq = T + u16(sec, T + 2 * c) + 2 * c
            if seq + 2 > len(sec):
                oob["sequence"] += 1
                continue
            fc = u16(sec, seq)
            nframes[fc] += 1
            if fc < 1 or seq + 2 + 4 * fc > len(sec):
                oob["frames"] += 1
                continue
            seqs += 1
            for f in range(fc):
                durs[u16(sec, seq + 2 + 4 * f)] += 1
                values[sec[seq + 5 + 4 * f]] += 1
            ends[sec[seq + 4 + 4 * (fc - 1)]] += 1

print("control: @FCP blocks:", blocks, "(published 1,066); blocks with a section 7:", have7)
print("events per block (count -> blocks):", sorted(nevents.items())[:10])
print("variant-0 records read:", recs, "; skipped by the engine's own rule (rel 0xFFFF or enabled 0):", skipped)
print("P1  out-of-section references:", dict(oob) if oob else "none")
print("P2  slot byte of live records:", sorted(slots.items()))
print("    choices per record:", sorted(nchoices.items())[:10])
print("P3  sequences parsed:", seqs, "; frame counts:", sorted(nframes.items())[:12])
print("    end action of the last frame:", sorted(ends.items()))
print("P4  durations (ticks -> frames), ten commonest:", sorted(durs.items(), key=lambda kv: -kv[1])[:10], "; largest", max(durs) if durs else None)
print("    values (ten commonest):", sorted(values.items(), key=lambda kv: -kv[1])[:10])

# ---- added 2026-09-19 (FABLE): every DISTINCT authored event, as choices of duration:endAction:value frames ----
print("distinct live events (event, slot, pickParam) x blocks, first example (file, the two sub-object ids):")
shapes = collections.Counter(); example = {}
for path in glob.glob(os.path.join(ROOT, "**", "*.cm"), recursive=True):
    d = open(path, "rb").read(); i = d.find(b"@FCP")
    if i < 0: continue
    size = struct.unpack_from("<I", d, i + 8)[0]; pay = d[i + 0x30: i + size]
    offs = list(struct.unpack_from("<18H", pay, 0)) + [u16(pay, 0x24)]
    o7 = offs[7]
    if not o7: continue
    later = sorted(o for k, o in enumerate(offs) if k not in (0, 7) and o > o7)
    sec = pay[o7:(later[0] if later else len(pay))]
    for e in range(8):
        rec = u16(sec, 2 * e)
        slot, pick, rel, en = sec[rec], sec[rec + 1], u16(sec, rec + 2), sec[rec + 4]
        if rel == 0xFFFF or not en: continue
        T = rec + 2 + rel + 0x10
        ids = (sec[T - 0x10], sec[T - 0xF])
        out = []
        for c in range(u16(sec, T - 2)):
            seq = T + u16(sec, T + 2 * c) + 2 * c
            fc = u16(sec, seq)
            out.append(tuple((u16(sec, seq + 2 + 4 * f), sec[seq + 4 + 4 * f], sec[seq + 5 + 4 * f]) for f in range(fc)))
        key = (e, slot, pick, tuple(out))
        shapes[key] += 1; example.setdefault(key, (os.path.basename(path), ids))
for k, n in sorted(shapes.items(), key=lambda kv: (kv[0][0], -kv[1])):
    print("event", k[0], "slot", k[1], "pick", k[2], "x", n, "eg", example[k])
    for c, s in enumerate(k[3]): print("    choice", c, " ".join("%d:%d:%d" % f for f in s))
