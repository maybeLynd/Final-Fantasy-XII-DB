#!/usr/bin/env python3
"""diff_group_completion.py - the reconstruction of `00306F00` against the shipped bytes.

What is compared
----------------
Both sides are given the **same image** and the **same call order**, and both mutate it. Three
things are then compared:

1. the return value of every call -- 1 when the mask is complete, including repeated calls;
2. the **event** each completion dispatched, `0x2005` or `0x2008`, and how many times the
   three-call prologue ran;
3. an FNV-1a digest over **every byte of every region**, because this path exists to write two
   masks and a flag, and "the returns match" would be a worthless claim on its own. That lesson
   is `name_registry`'s: compare what must not move, not only what does.

The four side effects
---------------------
`00307140(1)`, `00238B70(1)`, `00238AE0(1)` and `BattleUnit_DispatchActorPresentationEvent` are
**not** reproduced. In the emulator they are `ret` stubs whose entries are counted; in the
reconstruction they are individually reported hook invocations. The comparison covers *whether and in what order* the
side effects fire, not what they do -- which is stated rather than blurred.

The bit index
-------------
The cases deliberately include slots **31** and **32+**. `00306F00` computes the dead-mask bit
with a 32-bit `shl` followed by `cdqe`, so slot 31 sets bits 31..63 and slot 32 aliases onto bit
0. A reconstruction using `1ull << slot` passes every case that avoids those two and fails the
moment one is included, which is exactly why they are here.
"""
import argparse
import hashlib
import json
import os
import random
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UcError
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX,
                              UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_R8)

REFERENCE_SHA256 = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'

FUNC_VA, FUNC_LEN = 0x00306F00, 303
BKEI_VA, BKEI_LEN = 0x00263D30, 8          # movzx eax, word [rcx+0xF6] / ret
LANE_VA, LANE_LEN = 0x002360D0, 39         # the bkei -> slot map lookup
STUBS = (0x00307140, 0x00238B70, 0x00238AE0, 0x003299B0)
DISPATCH_VA = 0x003299B0

LEDGER_BASE, LEDGER_STRIDE, LEDGER_COUNT = 0x02EC13C0, 24, 64
# TRUNCATED ON PURPOSE, one entry short of a whole one. The region ends immediately after group
# 64's `deadMask`, so the qword read AND the qword write at `ledger + 63*24 + 8` finish exactly on
# the final byte -- the only place `load_q`/`store_q`'s `need` of 8 can be wrong. With a round
# 64*24 nothing sat on a boundary and both survived mutation.
#
# Group 64's `flags` byte would fall one past the end, so no group-64 unit may take the arm that
# writes it: the emulator's page-granular mapping would accept that write while the image model
# refuses, and the two would differ for a reason that is not a defect. Group 64 is therefore
# excluded from the random draw and used only by a planted arm-B unit.
LEDGER_LEN = LEDGER_STRIDE * (LEDGER_COUNT - 1) + 16

UNITS_VA, UNIT_STRIDE = 0x10000000, 0x1000
MAPS_VA = 0x10100000
RECS_VA = 0x10200000                        # the +0x698 records and the +0x10 objects
STACK_BASE = 0x40000000
RET_MAGIC = 0x50000000

U_FLAGS, U_P10, U_MAP, U_P698, U_GROUP, U_ARM = 0x000, 0x010, 0x040, 0x698, 0xE98, 0xE99
BKEI_OFF = 0x0F6


def read_exe(path):
    data = open(path, "rb").read()
    if hashlib.sha256(data).hexdigest() != REFERENCE_SHA256:
        raise ValueError('reference executable identity mismatch')
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, pe + 6)[0]
    opt = struct.unpack_from("<H", data, pe + 20)[0]
    base = struct.unpack_from("<Q", data, pe + 24 + 24)[0]
    if base != 0x120000:
        raise ValueError('reference image base mismatch')
    secs = []
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        va = struct.unpack_from("<I", data, o + 12)[0]
        vsz = struct.unpack_from("<I", data, o + 8)[0]
        raw = struct.unpack_from("<I", data, o + 20)[0]
        rsz = struct.unpack_from("<I", data, o + 16)[0]
        secs.append((base + va, vsz, raw, rsz))

    def rd(va, n):
        for sva, vsz, raw, rsz in secs:
            if sva <= va < sva + vsz:
                off = va - sva
                # SizeOfRawData, never the virtual range: past it the file holds the NEXT section
                avail = max(0, min(n, rsz - off))
                out = data[raw + off: raw + off + avail]
                return out + b"\0" * (n - len(out))
        raise SystemExit("va %08X is in no section" % va)
    return rd


def build(rng, n_units):
    """-> (regions, cases, plan). One ledger, one map, one unit block, one record block."""
    if not 3 <= n_units <= 128:
        raise ValueError('units must be 3..128: planted cases need three units; regions must not overlap')
    ledger = bytearray(LEDGER_LEN)
    units = bytearray(UNIT_STRIDE * n_units)
    # Sized to EXACTLY the count byte plus its slots, so the last slot read lands on the
    # region's final byte. With a round 0x1000 nothing ever sat near a boundary and every
    # `need` argument of GroupImage_At survived mutation -- the same blindness
    # name_registry had, for the same reason.
    maps = bytearray(1 + 10)
    # The +0x698 records occupy 0x40 each from the base; the +0x10 objects the same from
    # +0x800. Sized from n_units rather than a round number, because a fixed 0x1000 silently
    # ran off the end at 48 units.
    recs = bytearray(0x800 + UNIT_STRIDE + 0x40 * n_units + 0x200)

    # One map shared by every unit: count, then one slot byte per bkei index.
    # The slots chosen are the point of the test -- 31 and 32 are the two the machine treats
    # differently from a 64-bit shift, and 0xFF is the empty-lane sentinel.
    slots = [0, 1, 5, 30, 31, 32, 33, 63, 0xFF, 7]
    maps[0] = len(slots)
    for i, s in enumerate(slots):
        maps[1 + i] = s

    plan = []
    for i in range(n_units):
        base = i * UNIT_STRIDE
        group = rng.choice([0, 1, 1, 2, 2, 3, 7])           # 0 disables; 64 is reserved above
        arm = rng.choice([0, 1])
        bkei = rng.randrange(0, len(slots) + 2)             # +2 so out-of-range is exercised
        kind_ok = rng.random() < 0.85
        has_698 = rng.random() < 0.92

        rec_va = RECS_VA + 0x40 * i
        p10_va = RECS_VA + 0x800 + 0x40 * i
        struct.pack_into("<Q", units, base + U_P10, p10_va)
        struct.pack_into("<Q", units, base + U_MAP, MAPS_VA)
        struct.pack_into("<Q", units, base + U_P698, rec_va if has_698 else 0)
        units[base + U_GROUP] = group
        units[base + U_ARM] = arm
        struct.pack_into("<Q", units, base + U_FLAGS, rng.getrandbits(64))
        recs[rec_va - RECS_VA + 5] = 1 if kind_ok else rng.choice([0, 2, 9])
        struct.pack_into("<H", recs, p10_va - RECS_VA + BKEI_OFF, bkei)
        plan.append((UNITS_VA + base, group, arm, bkei, kind_ok, has_698))

    # Seed the ledgers so completion is reachable: a member mask built from the slots a unit can
    # actually set, or the test would only ever exercise the "not complete" return.
    for g in range(1, LEDGER_COUNT + 1):
        off = (g - 1) * LEDGER_STRIDE
        m = 0
        for s in slots:
            if s != 0xFF and rng.random() < 0.5:
                m |= (1 << (s & 31))
        struct.pack_into("<Q", ledger, off, m)

    # ---- PLANTED CASES -------------------------------------------------------------------
    # Mutation testing scored the first suite 68 %, and the survivors fell into groups the RNG
    # cannot reach on purpose. Each of these exists to make one of them observable.
    planted = []

    # 1. a NULL unit. `00306F00` opens `test rcx,rcx`, and no random unit address is ever 0, so
    #    the very first branch of the function was untested.
    planted.append(0)

    # 2. bkei 0 selecting slot 0, with EVERY other gate passing. `bkei < 0` and `slot < 0` are
    #    both `< 0` tests whose mutants (`< 1`) differ only at exactly zero, and nothing
    #    guaranteed a zero got through the group/kind/record gates.
    i = n_units - 1
    base = i * UNIT_STRIDE
    rec_va, p10_va = RECS_VA + 0x40 * i, RECS_VA + 0x800 + 0x40 * i
    units[base + U_GROUP] = 5
    units[base + U_ARM] = 0
    struct.pack_into("<Q", units, base + U_P698, rec_va)
    recs[rec_va - RECS_VA + 5] = 1
    struct.pack_into("<H", recs, p10_va - RECS_VA + BKEI_OFF, 0)      # bkei 0 -> slots[0] == 0
    planted.append(UNITS_VA + base)

    # 3. a bkei whose HIGH byte is non-zero. The index is composed as
    #    `bk[0] | (bk[1] << 8)`, and with every index under 256 that composition is
    #    indistinguishable from `bk[0]` alone -- four mutants on that line survived. With
    #    bk[1] = 1 the true index is 256+x, which the map bound rejects, while a mutant reading
    #    only bk[1] sees 1 and proceeds. The two then disagree.
    i = n_units - 2
    base = i * UNIT_STRIDE
    rec_va, p10_va = RECS_VA + 0x40 * i, RECS_VA + 0x800 + 0x40 * i
    units[base + U_GROUP] = 6
    units[base + U_ARM] = 1
    struct.pack_into("<Q", units, base + U_P698, rec_va)
    recs[rec_va - RECS_VA + 5] = 1
    struct.pack_into("<H", recs, p10_va - RECS_VA + BKEI_OFF, 0x0102)  # 258: the two bytes
    #                                                                 DIFFER, so a mutant
    # reading bk[1] where bk[0] belongs sees 1 rather than the same value twice. 0x0101
    # was the first attempt and made that mutant indistinguishable.
    planted.append(UNITS_VA + base)

    # 4. a group-64 unit on arm B that COMPLETES, so the ledger read and write at the truncated
    #    region's final qword actually happen. Arm B writes no flags, which is what makes the
    #    truncation safe -- see the note on LEDGER_LEN.
    i = n_units - 3
    base = i * UNIT_STRIDE
    rec_va, p10_va = RECS_VA + 0x40 * i, RECS_VA + 0x800 + 0x40 * i
    units[base + U_GROUP] = 64
    units[base + U_ARM] = 0                                          # arm B: no flags write
    struct.pack_into("<Q", units, base + U_P698, rec_va)
    recs[rec_va - RECS_VA + 5] = 1
    struct.pack_into("<H", recs, p10_va - RECS_VA + BKEI_OFF, 1)     # bkei 1 -> slots[1] == 1
    planted.append(UNITS_VA + base)

    cases = [p[0] for p in plan]
    cases += [rng.choice(cases) for _ in range(len(cases))]   # repeated masks can still repeat callbacks
    rng.shuffle(cases)
    cases += planted                                          # after the shuffle: order matters

    # Give group 5 and group 6 a member mask the planted units can actually satisfy, or cases
    # 2 and 3 would only ever exercise the "not complete" return.
    struct.pack_into("<Q", ledger, (5 - 1) * LEDGER_STRIDE, 1 << 0)
    struct.pack_into("<Q", ledger, (6 - 1) * LEDGER_STRIDE, 1 << 1)
    # Group 64 waits for exactly the bit the planted arm-B unit sets, so the completion -- and
    # therefore the boundary read and write -- actually occurs.
    struct.pack_into("<Q", ledger, (64 - 1) * LEDGER_STRIDE, 1 << 1)
    # ...and its deadMask starts NON-ZERO, with a bit outside memberMask so it does not
    # complete on its own. Otherwise reading deadMask as 0 -- which is exactly what an
    # out-of-bounds `load_q` returns -- produces the same stored value as reading it
    # correctly, and the boundary read is unobservable however well placed it is.
    struct.pack_into("<Q", ledger, (64 - 1) * LEDGER_STRIDE + 8, 1 << 5)

    regions = [(LEDGER_BASE, ledger), (UNITS_VA, units), (MAPS_VA, maps), (RECS_VA, recs)]
    assert len(ledger) == LEDGER_LEN and len(maps) == 1 + len(slots)
    assert len(recs) >= 0x800 + 0x40 * n_units + BKEI_OFF + 2
    return regions, cases, plan


def digest(regions):
    h = 1469598103934665603
    for _va, blob in regions:
        for b in bytes(blob):
            h = ((h ^ b) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h


def run_emulated(rd, regions, cases, instruction_limit=200000):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    mapped = set()

    def page(a):
        return a & ~0xFFF

    def ensure(va, size):
        lo, hi = page(va), page(va + size - 1) + 0x1000
        for p in range(lo, hi, 0x1000):
            if p not in mapped:
                uc.mem_map(p, 0x1000)
                mapped.add(p)

    for va, ln in ((FUNC_VA, FUNC_LEN), (BKEI_VA, BKEI_LEN), (LANE_VA, LANE_LEN)):
        ensure(va, ln)
        uc.mem_write(va, rd(va, ln))
    for s in STUBS:
        ensure(s, 1)
        uc.mem_write(s, b"\xC3")            # ret: counted, never executed for effect
    for va, blob in regions:
        ensure(va, len(blob))
        uc.mem_write(va, bytes(blob))
    ensure(STACK_BASE, 0x10000)
    ensure(RET_MAGIC, 1)
    uc.mem_write(RET_MAGIC, b"\xF4")

    records = []
    def memory():
        return [(va, bytes(uc.mem_read(va, len(blob)))) for va, blob in regions]
    for index, unit in enumerate(cases):
        rsp = STACK_BASE + 0x8000
        uc.mem_write(rsp, struct.pack("<Q", RET_MAGIC))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, unit)
        seen = []

        def on_code(uc_, address, _size, _ud):
            if address in STUBS:
                # At the dispatch stub, edx carries the event id -- the arm selection is a
                # behavioural claim, so capture it rather than only counting the call.
                args = ([uc_.reg_read(UC_X86_REG_RCX),
                         uc_.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF,
                         uc_.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF] if address == DISPATCH_VA
                        else [uc_.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF])
                seen.append(dict(target=address, args=args, memory='%016X' % digest(memory())))

        h = uc.hook_add(__import__("unicorn").UC_HOOK_CODE, on_code)
        try:
            uc.emu_start(FUNC_VA, RET_MAGIC, count=instruction_limit)
            if uc.reg_read(UC_X86_REG_RIP) != RET_MAGIC or uc.reg_read(UC_X86_REG_RSP) != rsp + 8:
                raise ValueError('emulation did not reach expected return boundary for case %d' % index)
        except UcError as e:
            raise ValueError("invalid emulation at %08X: %s"
                             % (uc.reg_read(UC_X86_REG_RIP), e)) from e
        finally:
            uc.hook_del(h)
        records.append(dict(case=index, unit=unit, **{'return':uc.reg_read(UC_X86_REG_RAX) & 0xFF},
                            calls=seen, memory='%016X' % digest(memory())))

    after = [(va, bytes(uc.mem_read(va, len(blob)))) for va, blob in regions]
    return records, after


def parse_driver(stdout, cases):
    """Reject missing, surplus, reordered or malformed records before comparing any pairs."""
    lines = stdout.splitlines()
    if not cases or len(lines) != len(cases) + 2 or lines[0] != 'SCHEMA GROUP_COMPLETION_V2':
        raise ValueError('driver schema/output census mismatch')
    footer = lines[-1].split()
    if len(footer) != 2 or footer[0] != 'DIGEST' or len(footer[1]) != 16:
        raise ValueError('missing or malformed final digest')
    int(footer[1], 16)
    records = [json.loads(line) for line in lines[1:-1]]
    for i, record in enumerate(records):
        if set(record) != {'case','unit','return','calls','memory'} or record['case'] != i or record['unit'] != cases[i]:
            raise ValueError('case identity/order mismatch')
        if type(record['return']) is not int or not -(2**31) <= record['return'] < 2**31:
            raise ValueError('invalid return value')
        if not isinstance(record['calls'], list) or len(record['memory']) != 16:
            raise ValueError('invalid call log or memory digest')
        int(record['memory'],16)
        for call in record['calls']:
            if set(call) != {'target','args','memory'} or type(call['target']) is not int:
                raise ValueError('invalid callback record')
            if not isinstance(call['args'],list) or not all(type(v) is int and 0 <= v < 2**64 for v in call['args']):
                raise ValueError('invalid callback arguments')
            if len(call['memory']) != 16:
                raise ValueError('invalid callback memory digest')
            int(call['memory'],16)
    return records, footer[1].upper()


def compare_records(got, want, expected_count):
    if not expected_count or len(got) != expected_count or len(want) != expected_count:
        raise ValueError('comparison census mismatch')
    return [i for i in range(expected_count) if got[i] != want[i]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True)
    ap.add_argument("--driver", required=True)
    ap.add_argument("--units", type=int, default=48)
    ap.add_argument("--seed", type=int, default=20260908)
    ap.add_argument("--out", type=Path, help="new directory for exact inputs, outputs and identities")
    a = ap.parse_args()
    outdir = a.out.resolve() if a.out else Path(tempfile.mkdtemp(prefix="astra-group-diff-"))
    if a.out:
        outdir.mkdir(parents=True, exist_ok=False)
    receipt = dict(command=sys.argv, status="INCOMPLETE", scope="isolated original code with four ret stubs; no native callback effects or timing",
                   source_note="Adjacent source hashes are not driver build attestation; pair driver hash with the build receipt.")
    try:
        driver = Path(a.driver).resolve()
        rd = read_exe(a.exe)
        receipt['identities'] = {str(p):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in [Path(a.exe).resolve(), driver, Path(__file__).resolve(),
                                           Path(__file__).with_name('group_completion_driver.c'),
                                           Path(__file__).resolve().parents[2]/'Game/Spawn/group_completion.c',
                                           Path(__file__).resolve().parents[2]/'Game/Spawn/group_completion.h']}
        receipt['unicorn_version'] = __import__('unicorn').__version__
        receipt['original_code'] = {hex(va):hashlib.sha256(rd(va,ln)).hexdigest()
                                    for va,ln in [(FUNC_VA,FUNC_LEN),(BKEI_VA,BKEI_LEN),(LANE_VA,LANE_LEN)]}
        regions, cases, plan = build(random.Random(a.seed), a.units)
        rp, cp, post = outdir/'regions.bin', outdir/'cases.txt', outdir/'driver-post.bin'
        with rp.open('wb') as f:
            f.write(struct.pack('<I',len(regions)))
            for va,blob in regions:
                f.write(struct.pack('<QI',va,len(blob))); f.write(blob)
        cp.write_text(''.join('%X\n' % c for c in cases), encoding='ascii')
        receipt['driver_command'] = [str(driver),str(rp),str(cp),str(post)]
        result = subprocess.run(receipt['driver_command'],capture_output=True,text=True)
        (outdir/'driver-stdout.txt').write_text(result.stdout,encoding='utf-8')
        (outdir/'driver-stderr.txt').write_text(result.stderr,encoding='utf-8')
        receipt['driver_exit'] = result.returncode
        if result.returncode:
            raise ValueError('driver failed: %d' % result.returncode)
        got, got_digest = parse_driver(result.stdout,cases)
        want, after = run_emulated(rd,regions,cases)
        (outdir/'original-records.json').write_text(json.dumps(want,indent=2)+'\n',encoding='utf-8')
        expected_bytes = b''.join(blob for va,blob in after)
        (outdir/'original-post.bin').write_bytes(expected_bytes)
        bad = compare_records(got,want,len(cases))
        memory_ok = post.read_bytes() == expected_bytes
        digest_ok = got_digest == '%016X' % digest(after)
        completions = sum(r['return'] for r in want)
        if not completions:
            raise ValueError('no reference completion cases: callback control is unproven')
        receipt.update(cases=len(cases), completions=completions, mismatched_cases=bad,
                       final_bytes_equal=memory_ok, final_digest_equal=digest_ok,
                       status='MATCH' if not bad and memory_ok and digest_ok and completions else 'MISMATCH')
        print('cases %d; completions %d; record mismatches %d; final bytes equal %s' %
              (len(cases),completions,len(bad),memory_ok))
        print('Exact callback identity/order/count/arguments and boundary memory compared; four callees remain ret stubs.')
        print('RESULT:',receipt['status'],'(isolated calculation/state and callback invocation only)')
        return 0 if receipt['status']=='MATCH' else 1
    except (ValueError,OSError,KeyError,TypeError) as e:
        receipt.update(status='INVALID',error=str(e))
        print('INVALID:',e,file=sys.stderr)
        return 2
    finally:
        (outdir/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
        print('Evidence:',outdir)


if __name__ == "__main__":
    raise SystemExit(main())
