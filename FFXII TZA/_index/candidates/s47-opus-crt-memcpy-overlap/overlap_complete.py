"""S-47 RL-8 (OPUS, 2026-09-26): SECTION-07's overlapping movement run PAST the memcpy import, with the copy the bound CRT
performs.

SECTION-07 (ORACLE, _experiments/evidence/continuation-section07-source-movement/native_controls.c) runs the original mover
0x369C60 natively on Linux over a private image. For an overlapping copy its memcpy adapter refuses to emulate the Windows CRT
and stops ('overlap-boundary' mode, M07-7). check.py in this directory has now executed the CRT the game binds: its memcpy export
is jmp memmove, and every overlapping copy - M07-7's shape included, on every dispatch path - produces memmove's result.

This driver:
  1. verifies ORACLE's native_controls.c by SHA-256 and never modifies it; a patched COPY is built in a temporary directory;
  2. applies exactly two textual replacements (each asserted to match once) and appends one case function:
       R1  the overlap branch of the memcpy adapter: in the new mode 'overlap-complete' the copy is performed with memmove
           semantics (what check.py measured for the bound CRT); in 'overlap-complete-backward' (the CONTROL) with a
           byte-by-byte BACKWARD copy, which a downward overlap must corrupt; every other mode keeps ORACLE's behaviour;
       R2  main() dispatches the two new modes before ORACLE's variants;
       +   overlap_complete(): M07-7's layout (0x100 hole, 0x400 source, no barrier) -> the real compactor -> exact_move's
           post-state assertions (payload, size, slot, header, backlink, generation, tree, accounting, latch, handle, cleanup),
           plus the copy being observed once and overlapping;
  3. compiles in WSL with ORACLE's own flags and runs: ORACLE's baseline on the patched copy (123 checks must pass, unchanged),
     'overlap-boundary' (must still stop exactly as ORACLE recorded), 'overlap-complete' and 'overlap-complete-backward'.
Evidence class: isolated original-instruction execution (SECTION-07's class), synthetic arenas; the one CRT adapter's overlap
semantics are the executed bound CRT's (check.py). live_game false. Writes overlap_result.json.
"""
import hashlib
import json
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
S07 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_experiments", "evidence", "continuation-section07-source-movement"))
SRC = os.path.join(S07, "native_controls.c")
SRC_SHA = "c24a9fd9e13d166df24c10dd74a9b1209e30e132f6258ee4fead0083e062a5be"
EXE_WIN = r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe"
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"


def wsl_path(p):
    p = os.path.abspath(p)
    return "/mnt/" + p[0].lower() + p[2:].replace("\\", "/")


src = open(SRC, "rb").read()
assert hashlib.sha256(src).hexdigest() == SRC_SHA, "SECTION-07 source changed"
assert hashlib.sha256(open(EXE_WIN, "rb").read()).hexdigest() == EXE_SHA
text = src.decode("utf-8")

R1_OLD = '''        fprintf(stderr,"overlapping memcpy requires separate CRT evidence\\n");exit(3);
'''
R1_NEW = '''        if(overlap_complete_mode==1){return memmove(p,s,n);}
        if(overlap_complete_mode==2){unsigned char*dd=p;const unsigned char*ss=s;for(size_t i=n;i-->0;)dd[i]=ss[i];return p;}
        fprintf(stderr,"overlapping memcpy requires separate CRT evidence\\n");exit(3);
'''
R2_OLD = '''    if(argc>2&&!strcmp(argv[2],"overlap-boundary")){overlap_probe=1;overlap_boundary();return 2;}
'''
R2_NEW = '''    if(argc>2&&!strcmp(argv[2],"overlap-boundary")){overlap_probe=1;overlap_boundary();return 2;}
    if(argc>2&&(!strcmp(argv[2],"overlap-complete")||!strcmp(argv[2],"overlap-complete-backward"))){
        overlap_complete_mode=strcmp(argv[2],"overlap-complete")?2:1;
        printf("{\\"evidence_class\\":\\"isolated original-instruction execution; synthetic arenas; overlap copy per bound CRT\\",\\"cases\\":[\\n");
        overlap_complete();
        printf("\\n],\\"checks\\":%u,\\"failures\\":%u}\\n",checks,failures);return failures?1:0;
    }
'''
DECL_OLD = "static int overlap_probe;\n"
DECL_NEW = "static int overlap_probe;\nstatic int overlap_complete_mode;\nstatic void overlap_complete(void);\n"
CASE = r'''
/* OPUS 2026-09-26: M07-7's layout carried past the import (see overlap_complete.py). */
static uintptr_t oc_dst, oc_src; static size_t oc_len;
static void overlap_complete(void){
    reset();phase="overlap_move_completed_per_bound_crt";
    uintptr_t hole,sep,tail;uint32_t h;motion_layout(0x100,0x400,0,&hole,&sep,&tail,&h);(void)sep;
    uintptr_t old=resolve(h),slot=h&~3u;unsigned char payload[0x400];memcpy(payload,(void*)old,sizeof(payload));
    eq("movement_latch_initially_clear",moved_flag(),0);
    release(hole);uint32_t before=usage(6);uint16_t gen=r16(slot+6);
    watch_src=old;watch_slot=slot;
    int moves=compact(0);uintptr_t now=resolve(h);
    printf(",\n{\"name\":\"layout\",\"hole\":%llu,\"old_source\":%llu,\"new_source\":%llu,\"moves\":%d}",
           (unsigned long long)hole,(unsigned long long)old,(unsigned long long)now,moves);
    eq("m07_7_source_address",old,0x30000500);
    eq("overlap_move_reports_one_move",moves,1);
    eq("overlap_move_lands_at_m07_7_destination",now,0x300003c0);
    eq("overlap_move_goes_down_by_hole_plus_header",old-now,0x140);
    bytes("overlap_mover_preserves_full_payload",now,payload,sizeof(payload));
    eq("overlap_mover_keeps_source_size",r32(now-0x28),0x400);
    eq("overlap_mover_keeps_live_handle_slot",r8(slot+5),1);
    eq("overlap_mover_updates_slot_header",r64(slot+8),now-0x40);
    eq("overlap_mover_updates_header_slot_backlink",r32(now-0x20),(uint32_t)slot);
    eq("overlap_mover_updates_generation_pair",r16(slot+6),r16(now-0x24));
    eq("overlap_mover_changes_generation_not_handle_value",r16(slot+6)!=gen,1);
    eq("overlap_mover_reinserts_tree_membership",r8(now-0x2b)&2,2);
    eq("overlap_mover_preserves_arena_payload_accounting",usage(6),before);
    eq("overlap_mover_marks_compaction_change",r8(arena(6)+0x62),1);
    eq("overlap_copy_boundary_observed_once",copy_hits,1);
    eq("overlap_copy_regions_do_overlap",copy_overlap,1);
    eq("overlap_slot_published_before_payload_copy",copy_published,1);
    eq("overlap_old_block_freed_before_payload_copy",copy_old_free,1);
    eq("overlap_stable_handle_resolves_new_source",pin(h),now);unpin(h);
    destroy(h);release(tail);
    eq("overlap_move_cleanup_accounting",usage(6),0);
    eq("overlap_move_no_diagnostics",formats,0);
    eq("overlap_movement_latch_set",moved_flag(),1);clear_moved();
    (void)oc_dst;(void)oc_src;(void)oc_len;
}
'''
for old, new in ((R1_OLD, R1_NEW), (R2_OLD, R2_NEW), (DECL_OLD, DECL_NEW)):
    assert text.count(old) == 1, old[:60]
    text = text.replace(old, new)
text = text.replace("int main(int argc,char**argv){", CASE + "int main(int argc,char**argv){", 1)

res = {"live_game": False, "section07_source_sha256": SRC_SHA, "exe_sha256": EXE_SHA,
       "replacements": {"R1": [R1_OLD, R1_NEW], "R2": [R2_OLD, R2_NEW], "DECL": [DECL_OLD, DECL_NEW]}, "appended_case": CASE}
with tempfile.TemporaryDirectory(prefix="opus-s47-", dir=HERE) as td:
    c = os.path.join(td, "native_controls_overlap.c")
    open(c, "w", encoding="utf-8", newline="\n").write(text)
    res["patched_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    b = wsl_path(os.path.join(td, "nc"))
    comp = subprocess.run(["wsl", "-e", "gcc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-fPIE", "-pie", wsl_path(c), "-o", b],
                          capture_output=True, text=True, timeout=120)
    res["compile"] = {"rc": comp.returncode, "diag": (comp.stdout + comp.stderr)[:2000]}
    assert comp.returncode == 0 and not (comp.stdout + comp.stderr).strip(), res["compile"]
    ver = subprocess.run(["wsl", "-e", "gcc", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    res["gcc"] = ver
    exe = wsl_path(EXE_WIN)
    runs = {}
    for mode in ("", "overlap-boundary", "overlap-complete", "overlap-complete-backward", "overlap-complete"):
        args = ["wsl", "-e", b, exe] + ([mode] if mode else [])
        r = subprocess.run(args, capture_output=True, text=True, timeout=120)
        key = mode or "baseline"
        if key in runs:
            key += "_repeat"
        try:
            out = json.loads(r.stdout)
        except Exception:
            out = {"raw": r.stdout[:3000]}
        runs[key] = {"rc": r.returncode, "stderr": r.stderr[:500], "out": out}
res["runs"] = runs
base, bnd, oc, bw, rep = (runs[k] for k in ("baseline", "overlap-boundary", "overlap-complete", "overlap-complete-backward", "overlap-complete_repeat"))


def fails(o):
    return [c for c in o.get("cases", []) if isinstance(c, dict) and c.get("pass") is False]


cases = {
    "oracle_baseline_unchanged_on_patched_copy_123_checks": base["rc"] == 0 and base["out"].get("checks") == 123 and base["out"].get("failures") == 0,
    "oracle_overlap_boundary_unchanged": bnd["rc"] == 0 and bnd["out"].get("evidence") == "stopped at original memcpy import before copying"
        and bnd["out"].get("destination") == 0x300003C0 and bnd["out"].get("source") == 0x30000500 and bnd["out"].get("length") == 0x400,
    "overlap_complete_every_assertion_passes": oc["rc"] == 0 and oc["out"].get("failures") == 0 and oc["out"].get("checks", 0) >= 20,
    "overlap_complete_repeat_identical": oc["out"] == rep["out"],
    "control_backward_copier_fails_exactly_the_payload_assertion": bw["rc"] == 1 and [c.get("name") for c in fails(bw["out"])] == ["overlap_mover_preserves_full_payload"],
}
res["cases"] = cases
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "overlap_result.json"), "w"), indent=1, sort_keys=True)
print("gcc:", res["gcc"])
for k in ("baseline", "overlap-boundary", "overlap-complete", "overlap-complete-backward"):
    o = runs[k]["out"]
    print(k, "rc", runs[k]["rc"], "checks", o.get("checks"), "failures", o.get("failures"), [c.get("name") for c in fails(o)][:5], runs[k]["stderr"][:200])
for k, v in cases.items():
    print("%-62s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
