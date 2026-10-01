/* SECTION-07: original arena movement and demand-driven EFX refresh controls.
 * Linux x86-64 host, Microsoft x64 calling convention, private original PE image.
 * The diagnostic formatter is substituted; three CRT imports use host adapters.
 * All resource/state fixtures are synthetic. See REVIEW.md before interpreting results.
 * Mutants modify only private process memory, never the input executable.
 */
#define _GNU_SOURCE
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <asm/prctl.h>
#include <signal.h>
#include <ucontext.h>
#define ABI __attribute__((ms_abi))
#define H ((uintptr_t)0x40000000)
#define P6 ((uintptr_t)0x30000000)
#define P8 ((uintptr_t)0x31000000)
#define PS 0x200000
#define TEB ((uintptr_t)0x43000000)
static unsigned checks,failures,formats;
static uintptr_t watch_src, watch_slot;
static unsigned copy_hits, copy_published, copy_old_free, copy_overlap;
static const char*phase="init";
static const char*mutant;
static int overlap_probe;
static uint8_t r8(uintptr_t p){
    uint8_t v;
    memcpy(&v,(void*)p,1);
    return v;
}
static uint16_t r16(uintptr_t p){
    uint16_t v;
    memcpy(&v,(void*)p,2);
    return v;
}
static uint32_t r32(uintptr_t p){
    uint32_t v;
    memcpy(&v,(void*)p,4);
    return v;
}
static uint64_t r64(uintptr_t p){
    uint64_t v;
    memcpy(&v,(void*)p,8);
    return v;
}
static void w8(uintptr_t p,uint8_t v){
    memcpy((void*)p,&v,1);
}
static void w16(uintptr_t p,uint16_t v){
    memcpy((void*)p,&v,2);
}
static void w32(uintptr_t p,uint32_t v){
    memcpy((void*)p,&v,4);
}
static void w64(uintptr_t p,uint64_t v){
    memcpy((void*)p,&v,8);
}
static void eq(const char*n,int64_t a,int64_t e){
    int ok=a==e;
    printf("%s{\"name\":\"%s\",\"pass\":%s,\"actual\":%lld,\"expected\":%lld}",checks?",\n":"",n,ok?"true":"false",(long long)a,(long long)e);
    checks++;
    failures+=!ok;
    if(!ok&&mutant){
        printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);
        exit(1);
    }
}
static void __attribute__((unused)) bytes(const char*n,uintptr_t p,const void*exp,size_t sz){
    eq(n,memcmp((void*)p,exp,sz)==0,1);
}
static void*ABI msset(void*p,int c,size_t n){
    return memset(p,c,n);
}
static void*ABI mscopy(void*p,const void*s,size_t n){
    uintptr_t d=(uintptr_t)p,a=(uintptr_t)s;
    if(a==watch_src && n){
        copy_hits++;
        copy_published+=r64(watch_slot+8)==d-0x40;
        copy_old_free+=(r8(a-0x2c)&1)==0;
        copy_overlap+=(d<a+n && a<d+n);
    }
    if(n && d<a+n && a<d+n && d!=a){
        /* Overlap behavior is a separate import boundary: never silently emulate
         * the original Windows memcpy for an overlapping case. */
        if(overlap_probe){
            printf("{\"evidence\":\"stopped at original memcpy import before copying\",\"destination\":%llu,\"source\":%llu,\"length\":%llu,\"slot_published\":%u,\"old_source_freed\":%u,\"overlap\":true}\n",(unsigned long long)d,(unsigned long long)a,(unsigned long long)n,copy_published,copy_old_free);
            exit(0);
        }
        fprintf(stderr,"overlapping memcpy requires separate CRT evidence\n");exit(3);
    }
    return memcpy(p,s,n);
}
static char* ABI mscopyname(char*d,const char*s,size_t n){
    size_t i=0;
    for(;i<n&&s[i];i++)d[i]=s[i];
    for(;i<n;i++)d[i]=0;
    return d;
}
static int ABI fmt(uintptr_t dst,uintptr_t format,uintptr_t a,uintptr_t b){
    (void)format;
    (void)a;
    (void)b;
    formats++;
    w8(dst,0);
    return 0;
}
static void patch(uintptr_t p,uintptr_t fn){
    unsigned char a[12]={
        0x48,0xb8
    }
    ;
    memcpy(a+2,&fn,8);
    a[10]=0xff;
    a[11]=0xe0;
    memcpy((void*)p,a,12);
}
static void fault(int n,siginfo_t*i,void*ctx){
    ucontext_t*u=ctx;
    dprintf(2,"fault phase=%s sig=%d addr=%p rip=%llx\n",phase,n,i->si_addr,(unsigned long long)u->uc_mcontext.gregs[REG_RIP]);
    _exit(128+n);
}
static void map(uintptr_t p,size_t n,int prot){
    if(mmap((void*)p,n,prot,MAP_ANONYMOUS|MAP_PRIVATE|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){
        perror("mmap");
        exit(2);
    }
}
static void load(const char*path){
    FILE*f=fopen(path,"rb");
    if(!f){
        perror(path);
        exit(2);
    }
    fseek(f,0,SEEK_END);
    long len=ftell(f);
    rewind(f);
    unsigned char*b=malloc((size_t)len);
    if(!b||len<512||fread(b,1,(size_t)len,f)!=(size_t)len)exit(2);
    fclose(f);
    uintptr_t q=(uintptr_t)b;
    uint32_t pe=r32(q+0x3c);
    if(pe+256>(uint64_t)len||r32(q+pe)!=0x4550)exit(2);
    uintptr_t op=q+pe+24;
    uintptr_t base=r64(op+24);
    uint32_t size=r32(op+56);
    if(r16(op)!=0x20b||base!=0x120000||size>0x10000000)exit(2);
    map(base,size,PROT_READ|PROT_WRITE|PROT_EXEC);
    for(unsigned j=0;j<r16(q+pe+6);j++){
        uintptr_t s=op+r16(q+pe+20)+j*40;
        uint32_t va=r32(s+12),rs=r32(s+16),ra=r32(s+20);
        if(s+40>q+(uintptr_t)len||(uint64_t)ra+rs>(uint64_t)len||(uint64_t)va+rs>size)exit(2);
        memcpy((void*)(base+va),b+ra,rs);
    }
    free(b);
    map(H,0x1000000,PROT_READ|PROT_WRITE);
    map(P6,PS,PROT_READ|PROT_WRITE);
    map(P8,PS,PROT_READ|PROT_WRITE);
    map(TEB,0x1000,PROT_READ|PROT_WRITE);
    if(syscall(SYS_arch_prctl,ARCH_SET_GS,TEB))exit(2);
    w64(TEB+0x10,0);
    w64(0x8c2a60,(uintptr_t)msset);
    w64(0x8c2a68,(uintptr_t)mscopy);
    w64(0x8c2f70,(uintptr_t)mscopyname);
    patch(0x17d2e0,(uintptr_t)fmt);
    struct sigaction sa={
        0
    }
    ;
    sa.sa_sigaction=fault;
    sa.sa_flags=SA_SIGINFO;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGSEGV,&sa,NULL);
    sigaction(SIGBUS,&sa,NULL);
    sigaction(SIGILL,&sa,NULL);
    sigaction(SIGTRAP,&sa,NULL);
    sigaction(SIGFPE,&sa,NULL);
}
static void init_arena(unsigned k,uintptr_t p){
    ((void(ABI*)(unsigned,uintptr_t,unsigned,unsigned))0x369d30)(k,p,PS,32);
}
static void select_arena(unsigned k){
    ((void(ABI*)(unsigned,unsigned))0x36c1d0)(k,10);
}
static void pop(void){
    ((void(ABI*)(void))0x36c140)();
}
static uintptr_t alloc(size_t n,unsigned k){
    select_arena(k);
    uintptr_t p=((uintptr_t(ABI*)(unsigned))0x36a100)((unsigned)n);
    pop();
    if(!p){
        fprintf(stderr,"allocation null\n");
        exit(2);
    }
    return p;
}
static void release(uintptr_t p){
    ((void(ABI*)(uintptr_t))0x3697f0)(p);
}
static int allocated(uintptr_t p){
    return (r16(p-0x40)==0xff12)&&(r8(p-0x2c)&1);
}
static uint32_t usage(unsigned k){
    uint32_t a=0;
    for(unsigned j=0;j<9;j++)a+=r32(0x22d7fd0+k*0xa8+0x68+j*4);
    return a;
}
static void reset(void){
    phase="reset";
    memset((void*)H,0,0x1000000);
    memset((void*)P6,0xA5,PS);
    memset((void*)P8,0xA5,PS);
    memset((void*)0x22d7fd0,0,0x1000);
    memset((void*)0x20910a0,0,0x1200);
    memset((void*)0x2ebcd80,0,0xe40);
    memset((void*)0x2ebef70,0,0x50);
    memset((void*)0x2f97340,0,0x10);
    memset((void*)0x2ec32c4,0,0x10);
    w64(0x1f83530,0);
    w64(0x22c6f28,H+0x100000);
    w32(H+0x100000+0x48800,0xffffffff);
    init_arena(6,P6);
    init_arena(8,P8);
    select_arena(8);
    formats=0;watch_src=watch_slot=0;copy_hits=copy_published=copy_old_free=copy_overlap=0;
}
static void makefile(uintptr_t p,unsigned family,unsigned n,unsigned subtype){
    memset((void*)p,0,n+0x40);
    memcpy((void*)p,(void*)0xd11c70,8);
    w32(p+0xc,n+0x10);
    w32(p+0x10,n);
    w16(p+0x14,0x100);
    w16(p+0x16,(uint16_t)family);
    w32(p+0x18,0);
    w16(p+0x1c,1);
    w8(p+0x1e,(uint8_t)subtype);
}

static void tickets(void){
    for(unsigned i=0;i<64;i++){
        uintptr_t p=0x2ebcd80+i*0x38;
        w32(p,0x20000000|i);
        w64(p+0x20,i==63?0:p+0x38);
        w64(p+0x28,i?p-0x38:0);
    }
    w64(0x2ebdb88,0x2ebcd80);
}
static uint32_t attach(uintptr_t src,unsigned offset){
    return ((uint32_t(ABI*)(uint32_t,int32_t))0x3b38b0)((uint32_t)src,(int32_t)offset);
}
static void cancel(uint32_t id){
    ((void(ABI*)(uint32_t))0x3b37e0)(id);
}
static uintptr_t arena(unsigned k){return 0x22d7fd0+k*0xa8;}
static uint32_t halloc(unsigned n){
    select_arena(6);
    uint32_t h=((uint32_t(ABI*)(unsigned))0x36b160)(n);
    pop();
    if(!h){fprintf(stderr,"native halloc failed\n");exit(2);}return h;
}
static uintptr_t resolve(uint32_t h){return ((uintptr_t(ABI*)(uint32_t))0x36b130)(h);}
static void unpin(uint32_t h){((void(ABI*)(uint32_t))0x36d170)(h);}
static uintptr_t pin(uint32_t h){return ((uintptr_t(ABI*)(uint32_t))0x36a000)(h);}
static void destroy(uint32_t h){((void(ABI*)(uintptr_t))0x3ab7c0)(h);}
static int compact(int all){return ((int(ABI*)(unsigned,int))0x369c60)(6,all);}
static void pattern(uintptr_t p,unsigned n){for(unsigned i=0;i<n;i++)w8(p+i,(uint8_t)((i*37+11)^(i>>3)));}
static void motion_layout(unsigned hole_size,unsigned source_size,int barrier,
                          uintptr_t*hole,uintptr_t*sep,uintptr_t*tail,uint32_t*h){
    *hole=alloc(hole_size,6);*sep=barrier?alloc(0x100,6):0;
    *h=halloc(source_size);*tail=alloc(0x80,6);
    uintptr_t p=resolve(*h);pattern(p,source_size);
    if(p<=*hole){fprintf(stderr,"fixture allocation order differs\n");exit(2);}
}
static int moved_flag(void){return ((int(ABI*)(unsigned))0x369cf0)(6);}
static void clear_moved(void){((void(ABI*)(unsigned))0x3697c0)(6);}
/* Executes only the 0024D565..0024D6A9 list/refresh window. The prologue
 * reproduces the original stack and R14 setup; an explicit boundary at
 * 0024D6AA restores it. The earlier five service calls and later rendering
 * are NOT executed or validated. No saved game/session order is inferred. */
static void ABI __attribute__((naked)) combined_entry(int unused __attribute__((unused))){
    __asm__ volatile("sub $0x28,%rsp\nmov %r14,0x20(%rsp)\nmov %ecx,%r14d\nmov $0x24d565,%eax\njmp *%rax");
}
static void ABI __attribute__((naked)) combined_end(void){
    __asm__ volatile("mov 0x20(%rsp),%r14\nadd $0x28,%rsp\nret");
}
static void exact_move(void){
    reset();phase="original_exact_hole_mover";
    uintptr_t hole,sep,tail;uint32_t h;motion_layout(0x400,0x400,1,&hole,&sep,&tail,&h);
    uintptr_t old=resolve(h),slot=h&~3u;unsigned char payload[0x400];memcpy(payload,(void*)old,sizeof(payload));
    eq("movement_latch_initially_clear",moved_flag(),0);
    eq("tagged_new_block_tree_eligible",r8(old-0x2b)&6,2);
    release(hole);uint32_t before=usage(6);uint16_t gen=r16(slot+6);
    watch_src=old;watch_slot=slot;
    int moves=compact(0);uintptr_t now=resolve(h);
    eq("exact_fit_reports_one_move",moves,1);
    eq("exact_fit_moves_across_raw_barrier",now,hole);
    bytes("mover_preserves_full_payload",now,payload,sizeof(payload));
    eq("mover_keeps_source_size",r32(now-0x28),0x400);
    eq("mover_keeps_live_handle_slot",r8(slot+5),1);
    eq("mover_updates_slot_header",r64(slot+8),now-0x40);
    eq("mover_updates_header_slot_backlink",r32(now-0x20),(uint32_t)slot);
    eq("mover_updates_generation_pair",r16(slot+6),r16(now-0x24));
    eq("mover_changes_generation_not_handle_value",r16(slot+6)!=gen,1);
    eq("mover_reinserts_tree_membership",r8(now-0x2b)&2,2);
    eq("mover_does_not_free_raw_barrier",allocated(sep),1);
    eq("mover_preserves_arena_payload_accounting",usage(6),before);
    eq("mover_marks_compaction_change",r8(arena(6)+0x62),1);
    eq("copy_boundary_observed_once",copy_hits,1);
    eq("slot_published_before_payload_copy",copy_published,1);
    eq("old_block_freed_before_payload_copy",copy_old_free,1);
    eq("tested_copy_regions_do_not_overlap",copy_overlap,0);
    eq("old_raw_payload_is_no_longer_allocation",allocated(old),0);
    eq("stable_handle_resolves_new_source",pin(h),hole);unpin(h);
    destroy(h);release(sep);release(tail);
    eq("exact_move_cleanup_accounting",usage(6),0);
    eq("exact_move_no_diagnostics",formats,0);
    eq("movement_latch_survives_release",moved_flag(),1);clear_moved();
    eq("movement_latch_explicitly_cleared",moved_flag(),0);
    eq("empty_tree_compaction_returns_zero",compact(1),0);
    eq("no_move_does_not_set_latch",moved_flag(),0);
}
static void mobility_gates(void){
    reset();phase="membership_exclusion_and_bit4";
    uintptr_t hole,sep,tail;uint32_t h;motion_layout(0x400,0x400,1,&hole,&sep,&tail,&h);
    uintptr_t old=resolve(h);release(hole);
    eq("pin_returns_current_payload",pin(h),old);
    eq("unlinked_block_is_not_moved",compact(1),0);
    eq("unlinked_handle_stays_old",resolve(h),old);
    unpin(h);w8(old-0x2b,r8(old-0x2b)|4);
    eq("member_with_inhibit_bit_is_not_moved",compact(1),0);
    eq("inhibit_preserves_source",resolve(h),old);
    w8(old-0x2b,r8(old-0x2b)&~4);
    eq("clear_inhibit_allows_real_move",compact(1),1);
    eq("allowed_move_reaches_hole",resolve(h),hole);
    destroy(h);release(sep);release(tail);eq("gate_cleanup",usage(6),0);
    reset();phase="nonexact_nonadjacent_candidate";
    motion_layout(0x800,0x400,1,&hole,&sep,&tail,&h);old=resolve(h);release(hole);
    eq("nonadjacent_smaller_candidate_not_best_fit",compact(1),0);
    eq("nonexact_nonadjacent_stays",resolve(h),old);
    destroy(h);release(sep);release(tail);eq("nonexact_cleanup",usage(6),0);
    reset();phase="adjacent_unequal_original_slide";
    motion_layout(0x800,0x400,0,&hole,&sep,&tail,&h);old=resolve(h);release(hole);
    unsigned char exp[0x400];memcpy(exp,(void*)old,sizeof(exp));
    watch_src=old;watch_slot=h&~3u;
    eq("adjacent_unequal_can_move",compact(0),1);
    eq("adjacent_unequal_destination",resolve(h),hole);
    bytes("adjacent_payload_preserved",hole,exp,sizeof(exp));
    eq("adjacent_test_copy_nonoverlap",copy_overlap,0);
    destroy(h);release(tail);eq("adjacent_cleanup",usage(6),0);
    reset();phase="lower_member_is_not_relocated_upwards";
    h=halloc(0x400);old=resolve(h);hole=alloc(0x400,6);tail=alloc(0x100,6);release(hole);
    eq("lower_source_not_moved_to_higher_hole",compact(1),0);
    eq("lower_source_location_preserved",resolve(h),old);
    destroy(h);release(tail);eq("lower_source_cleanup",usage(6),0);
}
static void real_move_to_refresh(void){
    reset();phase="real_compaction_to_context_refresh";tickets();
    uintptr_t hole,sep,tail;uint32_t h;motion_layout(0x400,0x400,1,&hole,&sep,&tail,&h);
    uintptr_t old=resolve(h);makefile(old,0x800,0x2b0,255);
    uint32_t id=attach(h,0);uintptr_t c=r64(0x2ebcd80+0x18),table=r64(c+0x848);
    eq("consumer_initial_handle_binding",r32(c+0x860),h);
    eq("consumer_initial_source",r64(c+0x858),old);
    eq("consumer_initial_table_pointer",r64(table+8),old+32);
    release(hole);eq("integrated_native_move_occurs",compact(0),1);
    eq("original_slot_now_points_at_hole",resolve(h),hole);
    eq("allocator_does_not_repair_consumer_base",r64(c+0x858),old);
    eq("allocator_does_not_repair_consumer_lookup",r64(table+8),old+32);
    ((void(ABI*)(uintptr_t,uintptr_t))0x3b3480)(c,0);
    eq("original_refresh_reads_actual_moved_slot",r64(c+0x858),hole);
    eq("original_refresh_repairs_actual_moved_pointer",r64(table+8),hole+32);
    eq("original_refresh_preserves_stale_run_origin",r64(c+0x870),old+16);
    ((void(ABI*)(uintptr_t,uintptr_t))0x3b3480)(c,0);
    eq("actual_move_repeat_refresh_is_not_double_delta",r64(table+8),hole+32);
    cancel(id);destroy(h);release(sep);release(tail);
    eq("actual_move_context_cleanup",usage(8),0);eq("actual_move_owner_cleanup",usage(6),0);
    eq("actual_move_no_diagnostics",formats,0);
}

static int start_child(uint32_t id,int n){return ((int(ABI*)(uint32_t,int))0x3b3c00)(id,n);}
static void request_child(uintptr_t rec,unsigned n){((void(ABI*)(uintptr_t,unsigned))0x3e6aa0)(rec,n);}
static void walk_dirty(void){((void(ABI*)(int))0x427de0)(0);}
static void dirty_delivery(void){
    reset();phase="dirty_delivery_after_original_move";tickets();
    uintptr_t hole,sep,tail;uint32_t h;motion_layout(0x400,0x400,1,&hole,&sep,&tail,&h);
    uintptr_t old=resolve(h);makefile(old,0x800,0x2b0,255);
    uint32_t cid=attach(h,0);uintptr_t c=r64(0x2ebcd80+0x18),table=r64(c+0x848);
    uintptr_t obj=H+0x5000,rec=H+0x100000;uint32_t ticket=0x51000040;
    w32(0x2ebd480,ticket);w64(0x2ebd480+0x10,obj);w64(obj+0x340,c);w64(obj+0x390,old);
    w16(rec+4,0xffff);w16(rec+6,0xffff);w32(rec+0x48800,0);w32(rec+0x288,ticket);
    w32(rec+0x304,0x1234567);
    request_child(rec,9);eq("request_sets_pending_bit",r32(rec+0x294)&0x08000000,0x08000000);
    eq("request_preserves_low27",r32(rec+0x304)&0x7ffffff,0x1234567);
    eq("request_selects_high_five_bits",r32(rec+0x304)>>27,9);
    request_child(rec,2);eq("later_request_replaces_not_appends",r32(rec+0x304)>>27,2);
    request_child(rec,33);eq("issuer_truncates_to_five_bits",r32(rec+0x304)>>27,1);
    release(hole);eq("dirty_fixture_original_move",compact(0),1);
    eq("pending_does_not_itself_repair_context",r64(c+0x858),old);
    eq("pending_does_not_itself_repair_container",r64(obj+0x390),old);
    eq("negative_child_index_rejected",start_child(ticket,-1),0);
    eq("eleven_is_excluded",start_child(ticket,11),0);
    eq("rejected_index_does_not_refresh",r64(c+0x858),old);
    eq("zero_child_index_returns_success",start_child(ticket,0),1);
    eq("zero_success_is_not_a_refresh",r64(c+0x858),old);
    eq("zero_success_leaves_lookup_old",r64(table+8),old+32);
    w32(rec+0x288,0xffffffff);walk_dirty();
    eq("unbound_record_keeps_pending_bit",r32(rec+0x294)&0x08000000,0x08000000);
    eq("unbound_record_keeps_stale_context",r64(c+0x858),old);
    w32(rec+0x288,ticket+0x40);walk_dirty();
    eq("stale_full_ticket_retires_pending_bit",r32(rec+0x294)&0x08000000,0);
    eq("stale_ticket_did_not_refresh",r64(c+0x858),old);
    w32(rec+0x288,ticket);request_child(rec,11);walk_dirty();
    eq("invalid_child_retires_pending_bit",r32(rec+0x294)&0x08000000,0);
    eq("invalid_child_left_context_old",r64(c+0x858),old);
    request_child(rec,0);walk_dirty();
    eq("zero_child_retires_pending_bit",r32(rec+0x294)&0x08000000,0);
    eq("zero_child_dirty_delivery_does_not_refresh",r64(c+0x858),old);
    request_child(rec,1);walk_dirty();
    eq("failed_start_still_consumes_pending_bit",r32(rec+0x294)&0x08000000,0);
    eq("full_dirty_driver_repairs_context_after_move",r64(c+0x858),hole);
    eq("full_dirty_driver_repairs_lookup_after_move",r64(table+8),hole+32);
    eq("full_dirty_driver_repairs_container_base",r64(obj+0x390),hole);
    eq("full_dirty_driver_keeps_old_run_origin",r64(c+0x870),old+16);
    w64(c+0x858,old);w64(table+8,old+32);w64(obj+0x390,old);
    eq("no_group_has_no_successful_start",start_child(ticket,10),0);
    eq("ten_is_admitted_and_runs_refresh",r64(c+0x858),hole);
    walk_dirty();eq("no_pending_repeat_preserves_lookup",r64(table+8),hole+32);
    w64(0x2ebd480+0x10,0);eq("null_container_rejects",start_child(ticket,1),0);
    cancel(cid);destroy(h);release(sep);release(tail);
    eq("dirty_fixture_context_cleanup",usage(8),0);eq("dirty_fixture_source_cleanup",usage(6),0);
    eq("dirty_fixture_no_diagnostics",formats,0);
}

static void allocation_pressure(void){
    reset();phase="real_allocation_fallback_compaction";
    uintptr_t hole=alloc(0x800,6);uint32_t h=halloc(0x400);uintptr_t old=resolve(h);
    pattern(old,0x400);unsigned char original[0x400];memcpy(original,(void*)old,sizeof(original));
    uintptr_t hole2=alloc(0x800,6),freehead=r64(arena(6)+0x90);
    unsigned rest=r32(freehead+0x18);uintptr_t tail=alloc(rest,6);
    eq("pressure_fixture_has_no_spare_free_head",r64(arena(6)+0x90),0);
    release(hole);release(hole2);
    eq("pressure_first_gap_is_only_0800",r32(r64(arena(6)+0x90)+0x18),0x800);
    watch_src=old;watch_slot=h&~3u;
    uintptr_t result=alloc(0xc00,6);
    eq("larger_request_succeeds_after_original_fallback",result!=0,1);
    eq("allocation_itself_moves_prior_source",resolve(h),hole);
    eq("allocation_fallback_executed_original_copy",copy_hits,1);
    bytes("allocation_fallback_preserves_prior_contents",resolve(h),original,sizeof(original));
    eq("allocation_fallback_result_is_separate",result!=resolve(h),1);
    eq("allocation_fallback_marks_movement",r8(arena(6)+0x62),1);
    release(result);destroy(h);release(tail);
    eq("fallback_all_allocations_reclaimed",usage(6),0);
    eq("fallback_no_diagnostic_substitution_used",formats,0);
}
static void two_moves_without_repeat(void){
    reset();phase="one_public_call_two_selection_passes";
    uintptr_t a=alloc(0x400,6),sep=alloc(0x100,6);uint32_t h1=halloc(0x400);
    uintptr_t b=alloc(0x800,6);uint32_t h2=halloc(0x400);uintptr_t tail=alloc(0x100,6);
    uintptr_t p1=resolve(h1),p2=resolve(h2);pattern(p1,0x400);pattern(p2,0x400);
    release(a);release(b);
    int count=compact(0);
    eq("repeat_zero_can_still_report_two_moves",count,2);
    eq("first_selection_moved_exact_member",resolve(h1),a);
    eq("second_selection_moved_adjacent_member",resolve(h2),p1);
    eq("two_passes_changed_second_location",resolve(h2)!=p2,1);
    destroy(h1);destroy(h2);release(sep);release(tail);
    eq("two_pass_cleanup",usage(6),0);
}


static void combined_refresh_window(void){
    reset();phase="combined_driver_isolated_refresh_window";tickets();
    uintptr_t hole,sep,tail;uint32_t h;motion_layout(0x400,0x400,1,&hole,&sep,&tail,&h);
    uintptr_t old=resolve(h);makefile(old,0x800,0x2b0,255);
    uint32_t id=attach(h,0);uintptr_t c=r64(0x2ebcd80+0x18),table=r64(c+0x848);
    uintptr_t a=H+0x5000,b=H+0x6000;
    w64(a+0x340,c);w64(b+0x340,c);w64(a+0x390,old);w64(b+0x390,old);
    w64(a+0x348,b);w64(0x2091108,a);
    release(hole);eq("combined_fixture_actual_move",compact(0),1);
    combined_entry(1);eq("combined_nonzero_argument_skips_refresh",r64(c+0x858),old);
    combined_entry(0);
    eq("combined_zero_argument_repairs_context",r64(c+0x858),hole);
    eq("combined_walk_repairs_lookup",r64(table+8),hole+32);
    eq("combined_first_container_rebased",r64(a+0x390),hole);
    eq("combined_shared_context_second_container_rebased",r64(b+0x390),hole);
    eq("combined_keeps_old_run_origin",r64(c+0x870),old+16);
    combined_entry(0);eq("combined_repeat_not_double_delta",r64(table+8),hole+32);
    /* These resets reproduce a stale consumer view only; no second source movement. */
    w64(c+0x858,old);w64(table+8,old+32);w64(a+0x390,old);w64(b+0x390,old);
    w8(c+2,r8(c+2)&~4);combined_entry(0);
    eq("combined_nonborrow_context_skips_rebase",r64(c+0x858),old);
    eq("combined_nonborrow_container_skips_rebase",r64(a+0x390),old);
    w8(c+2,r8(c+2)|4);combined_entry(0);
    eq("combined_restore_borrow_repairs_again",r64(table+8),hole+32);
    /* Container nodes are host-backed test records, not allocations owned by
     * the original destructor. Detach this synthetic list before context teardown. */
    w64(0x2091108,0);
    cancel(id);destroy(h);release(sep);release(tail);
    eq("combined_context_cleanup",usage(8),0);eq("combined_owner_cleanup",usage(6),0);
    eq("combined_no_diagnostics",formats,0);
}
static void mutation(uintptr_t at,const unsigned char*old,const unsigned char*rep,size_t n){
    if(memcmp((void*)at,old,n)){fprintf(stderr,"mutation preimage mismatch at %lx\n",(unsigned long)at);exit(2);}
    memcpy((void*)at,rep,n);
}
static void apply_variant(void){
    if(!mutant){return;}
    if(!strcmp(mutant,"skip_payload_copy")){
        mutation(0x36a3a7,(unsigned char[]){0xe8,0x44,0xa3,0x10,0},(unsigned char[]){0x90,0x90,0x90,0x90,0x90},5);
    }else if(!strcmp(mutant,"skip_slot_generation")){
        mutation(0x36a461,(unsigned char[]){0x66,0x89,0x46,6},(unsigned char[]){0x90,0x90,0x90,0x90},4);
    }else if(!strcmp(mutant,"wrong_movement_inhibit_mask")){
        mutation(0x36ab4f,(unsigned char[]){4},(unsigned char[]){8},1);
    }else if(!strcmp(mutant,"skip_context_repair")){
        mutation(0x3b351a,(unsigned char[]){0xe8,0x51,0xa4,0xe9,0xff},(unsigned char[]){0x90,0x90,0x90,0x90,0x90},5);
    }else if(!strcmp(mutant,"admit_child_eleven")){
        mutation(0x3b3c19,(unsigned char[]){0x7d},(unsigned char[]){0x7f},1);
    }else if(!strcmp(mutant,"zero_requests_refresh")){
        mutation(0x3b3c41,(unsigned char[]){0x74,0x41},(unsigned char[]){0x90,0x90},2);
    }else if(!strcmp(mutant,"retain_old_request_index")){
        mutation(0x3e6ab3,(unsigned char[]){7},(unsigned char[]){0xff},1);
    }else if(!strcmp(mutant,"keep_delivered_pending_bit")){
        unsigned char old[]={0x81,0xa3,0x94,2,0,0,0xff,0xff,0xff,0xf7};
        unsigned char nops[10];memset(nops,0x90,10);mutation(0x428660,old,nops,10);
    }else if(!strcmp(mutant,"skip_combined_container_base")){
        mutation(0x24d67f,(unsigned char[]){0x48,0x89,0xb7,0x90,3,0,0},(unsigned char[]){0x90,0x90,0x90,0x90,0x90,0x90,0x90},7);
    }else if(!strcmp(mutant,"skip_movement_latch")){
        mutation(0x369ccf,(unsigned char[]){0xc6,0x47,0x62,1},(unsigned char[]){0x90,0x90,0x90,0x90},4);
    }else{fprintf(stderr,"unknown variant: %s\n",mutant);exit(2);}
}
static void overlap_boundary(void){
    reset();phase="adjacent_overlap_import_boundary";
    uintptr_t hole,sep,tail;uint32_t h;motion_layout(0x100,0x400,0,&hole,&sep,&tail,&h);
    (void)sep;(void)tail;watch_src=resolve(h);watch_slot=h&~3u;release(hole);compact(0);
    fprintf(stderr,"expected overlap boundary not reached\n");exit(2);
}
int main(int argc,char**argv){
    if(argc<2){return 2;}
    load(argv[1]);setbuf(stdout,NULL);
    patch(0x24d6aa,(uintptr_t)combined_end);
    if(argc>2&&!strcmp(argv[2],"overlap-boundary")){overlap_probe=1;overlap_boundary();return 2;}
    mutant=argc>2?argv[2]:NULL;apply_variant();
    printf("{\"evidence_class\":\"isolated original-instruction execution; synthetic arenas\",\"cases\":[\n");
    exact_move();mobility_gates();real_move_to_refresh();dirty_delivery();allocation_pressure();two_moves_without_repeat();combined_refresh_window();
    printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);return failures?1:0;
}
