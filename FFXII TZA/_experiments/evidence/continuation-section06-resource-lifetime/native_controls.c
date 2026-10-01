/* SECTION-06: bounded resource ownership/lifetime controls.
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
static const char*phase="init";
static const char*mutant;
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
    formats=0;
}
static uintptr_t context(unsigned type,unsigned flags){
    uintptr_t t=H+0x1000;
    memset((void*)t,0,0x890);
    w8(t,(uint8_t)type);
    w8(t+2,(uint8_t)flags);
    return ((uintptr_t(ABI*)(uintptr_t))0x24b3a0)(t);
}
static void dispose(uintptr_t c){
    ((void(ABI*)(uintptr_t))0x24f410)(c);
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
static void parse(uintptr_t p,unsigned n){
    ((void(ABI*)(uintptr_t,unsigned))0x3edad0)(p,n);
}
static void basic(void){
    reset();
    phase="native_allocator_smoke";
    uintptr_t p=alloc(0x500,8);
    eq("original_allocator_marks_live",allocated(p),1);
    release(p);
    eq("original_allocator_releases_block",allocated(p),0);
    eq("allocator_usage_returns_to_zero",usage(8),0);
    eq("allocator_normal_path_no_diagnostic",formats,0);
    reset();
    phase="copy_context";
    uintptr_t c=context(3,0);
    makefile(H+0x10000,0x800,0x2b0,255);
    parse(H+0x10000,0x2c0);
    uintptr_t run=r64(c+0x870);
    eq("copy_run_separate",run!=H+0x10010,1);
    eq("copy_run_live",allocated(run),1);
    eq("parser_sets_bulk_layout",r8(c+3)&1,1);
    eq("lookup_points_inside_copy",r64(r64(c+0x848)+8),run+16);
    eq("input_marker_unmodified_copy",r16(H+0x10010+0x290),0);
    eq("copy_marker_written",r16(run+0x290),1);
    dispose(c);
    eq("context_disposed",allocated(c),0);
    eq("copy_reclaimed",allocated(run),0);
    eq("all_arena8_usage_released",usage(8),0);
    eq("current_context_slot_is_not_lifetime",r64(0x2f97340),c);
    eq("copy_lifecycle_no_diagnostic",formats,0);
    reset();
    phase="borrow_context";
    c=context(3,4);
    uintptr_t in=alloc(0x400,6);
    makefile(in,0x800,0x2b0,255);
    parse(in,0x2c0);
    run=r64(c+0x870);
    eq("borrow_exact_input_run",run,in+16);
    eq("borrow_input_mutated",r16(in+0x2a0),1);
    uintptr_t table=r64(c+0x848);
    dispose(c);
    eq("borrow_source_remains_allocated",allocated(in),1);
    eq("borrow_lookup_table_freed",allocated(table),0);
    eq("borrow_context_usage_gone",usage(8),0);
    release(in);
    eq("caller_source_release_separate",usage(6),0);
    eq("borrow_lifecycle_no_diagnostic",formats,0);
}
/* The routines below run original application bodies against synthetic arenas. */
static void flags_and_reuse(void){
    reset();
    phase="A00_copy";
    uintptr_t c=context(3,0);
    makefile(H+0x10000,0xa00,0x80,255);
    parse(H+0x10000,0x90);
    uintptr_t run=r64(c+0x878);
    eq("A00_copied_run",run!=H+0x10010,1);
    eq("A00_lookup_in_copy",r64(r64(c+0x850)+8),run+16);
    eq("A00_index_write",r16(run+0x52),1);
    eq("A00_input_unchanged",r16(H+0x10010+0x52),0);
    dispose(c);
    eq("A00_owned_storage_released",usage(8),0);
    reset();
    phase="A00_borrow";
    c=context(3,4);
    uintptr_t in=alloc(0x200,6);
    makefile(in,0xa00,0x80,255);
    parse(in,0x90);
    eq("A00_borrowed_run",r64(c+0x878),in+16);
    eq("A00_borrowed_input_mutated",r16(in+0x62),1);
    dispose(c);
    eq("A00_borrowed_owner_survives",allocated(in),1);
    eq("A00_lookup_tables_released",usage(8),0);
    release(in);
    reset();
    phase="unaligned_copy";
    c=context(3,0);
    makefile(H+0x10000,0x800,0x2b3,255);
    memset((void*)(H+0x10010+0x2b0),0x5c,3);
    parse(H+0x10000,0x2c3);
    run=r64(c+0x870);
    eq("unaligned_run_has_rounded_down_copy",r8(run+0x2b0),0xa5);
    eq("unaligned_original_tail_survives",r8(H+0x10010+0x2b0),0x5c);
    dispose(c);
    eq("unaligned_copy_disposed",usage(8),0);
    reset();
    phase="nonbulk_borrowbit";
    c=context(3,4);
    uintptr_t x=alloc(0x300,8);
    w64(r64(c+0x848)+8,x);
    w8(c+3,0);
    dispose(c);
    eq("nonbulk_releases_individual_even_with_borrow_bit",allocated(x),0);
    eq("nonbulk_no_arena_leak",usage(8),0);
    reset();
    phase="repeat_parse";
    c=context(3,0);
    makefile(H+0x10000,0x800,0x2b0,255);
    makefile(H+0x11000,0x800,0x2b0,255);
    parse(H+0x10000,0x2c0);
    uintptr_t old=r64(c+0x870);
    parse(H+0x11000,0x2c0);
    uintptr_t next=r64(c+0x870);
    eq("repeat_parser_replaces_run_pointer",next!=old,1);
    eq("repeat_parser_does_not_release_old_allocation",allocated(old),1);
    dispose(c);
    eq("repeat_teardown_only_releases_latest",allocated(next),0);
    eq("superseded_copy_still_live",allocated(old),1);
    release(old);
    eq("explicit_superseded_cleanup",usage(8),0);
    reset();
    phase="two_context_borrows";
    uintptr_t a=alloc(0x400,6),b=alloc(0x400,6);
    makefile(a,0x800,0x2b0,255);
    makefile(b,0x800,0x2b0,255);
    uintptr_t ca=context(3,4);
    parse(a,0x2c0);
    uintptr_t cb=context(3,4);
    parse(b,0x2c0);
    eq("new_context_does_not_replace_old_borrow",r64(ca+0x870),a+16);
    eq("new_context_has_own_borrow",r64(cb+0x870),b+16);
    eq("global_is_current_selector",r64(0x2f97340),cb);
    dispose(ca);
    eq("older_disposal_preserves_other_context",allocated(cb),1);
    eq("older_disposal_preserves_other_run",r64(cb+0x870),b+16);
    eq("disposal_rebinds_global_to_freed_context",r64(0x2f97340),ca);
    dispose(cb);
    eq("both_contexts_reclaimed",usage(8),0);
    eq("both_borrow_sources_live",allocated(a)&&allocated(b),1);
    release(a);
    release(b);
    eq("caller_releases_both_sources",usage(6),0);
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
static void ticket_cases(void){
    reset();
    phase="ticket_chain";
    tickets();
    uintptr_t src=alloc(0x500,6);
    makefile(src,0x800,0x2b0,255);
    uint32_t id=attach(src,0);
    uintptr_t sl=0x2ebcd80,c=r64(sl+0x18);
    eq("ticket_first_generation",id,0x20000040);
    eq("ticket_type3_context",r8(c),3);
    eq("ticket_borrow_policy",r8(c+2)&4,4);
    eq("ticket_retains_source_identifier",r32(c+0x860),(uint32_t)src);
    eq("ticket_context_borrows_owner_run",r64(c+0x870),src+16);
    unsigned char slot_before[0x38];
    memcpy(slot_before,(void*)sl,0x38);
    cancel(id^0x40);
    bytes("stale_ticket_preserves_slot",sl,slot_before,0x38);
    eq("stale_ticket_preserves_context",allocated(c),1);
    uintptr_t other=context(3,4),i0=alloc(0x400,8),i1=alloc(0x400,8),i2=alloc(0x400,8);
    memset((void*)i0,0,0x400);
    memset((void*)i1,0,0x400);
    memset((void*)i2,0,0x400);
    w64(i0+0x340,c);
    w64(i1+0x340,other);
    w64(i2+0x340,c);
    w64(i0+0x348,i1);
    w64(i1+0x350,i0);
    w64(i1+0x348,i2);
    w64(i2+0x350,i1);
    w64(0x20910f0+3*8,i0);
    w64(i0+0x380,H+0x7000);
    w64(i2+0x380,H+0x7100);
    uintptr_t secondary=0x2ebd480;
    w32(secondary,0x30000040);
    w32(secondary+0x18,id);
    w64(0x2ebdb98,secondary);
    w64(0x2ebdba8,secondary);
    cancel(id);
    eq("ticket_context_reclaimed",allocated(c),0);
    eq("matching_instances_reclaimed",!allocated(i0)&&!allocated(i2),1);
    eq("other_owner_instance_preserved",allocated(i1),1);
    eq("instance_list_repaired",r64(0x20910f0+3*8),i1);
    eq("remaining_instance_previous_cleared",r64(i1+0x350),0);
    eq("remaining_instance_next_cleared",r64(i1+0x348),0);
    eq("deferred_payloads_queued_once",r16(0x209216a),2);
    eq("deferred_first_payload",r64(0x2091950),H+0x7000);
    eq("deferred_second_payload",r64(0x2091958),H+0x7100);
    eq("ticket_active_head_removed",r64(0x2ebdb80),0);
    eq("ticket_free_head_returned",r64(0x2ebdb88),sl);
    eq("ticket_generation_cleared",r32(sl),0x20000000);
    eq("ticket_context_pointer_cleared",r64(sl+0x18),0);
    eq("secondary_ticket_generation_cleared",r32(secondary),0x30000000);
    eq("secondary_free_head_returned",r64(0x2ebdba0),secondary);
    eq("ticket_does_not_free_source",allocated(src),1);
    cancel(id);
    eq("old_ticket_repeat_no_double_queue",r16(0x209216a),2);
    dispose(other);
    eq("other_owner_then_reclaimed",allocated(i1),0);
    eq("all_ticket_heap_gone",usage(8),0);
    release(src);
    eq("ticket_test_no_allocator_diagnostics",formats,0);
    reset();
    phase="ticket_exhausted";
    makefile(H+0x10000,0x800,0x2b0,255);
    eq("empty_ticket_pool_returns_zero",attach(H+0x10000,0),0);
    eq("empty_ticket_pool_allocates_nothing",usage(8),0);
}
static uintptr_t bank(void){
    uintptr_t b=H+0x2000,slot=H+0x3000,page=H+0x4000,entry=H+0x5000;
    w64(b+0x38,slot);
    w64(b+0x10,page);
    w32(b+0x40,0);
    w32(b+0x44,0);
    w32(b+0x48,0x50);
    w32(b+0x4c,5);
    w32(b+0x50,31);
    w32(b+0x58,1);
    w8(b,1);
    w16(b+0x22,1);
    w32(slot,0);
    w32(slot+4,0xffffffff);
    w32(slot+8,0xffffffff);
    w32(page+0x10,(uint32_t)entry);
    w32(page+0x14,1);
    ((void(ABI*)(uintptr_t))0x409710)(entry);
    return b;
}
static void resource_cases(unsigned mode){
    reset();
    phase=mode?"entry_borrowed":"entry_owned";
    tickets();
    uintptr_t b=bank(),entry=H+0x5000,src=alloc(0x600,6);
    memset((void*)src,0xCC,0x500);
    memcpy((void*)src,"TEST",4);
    w32(src+8,0x400);
    memcpy((void*)(src+0x10),"AB\0",3);
    makefile(src+0x40,0x800,0x2b0,255);
    ((void(ABI*)(uintptr_t,uintptr_t,unsigned))0x409a60)(entry,src,mode);
    uintptr_t payload=mode?src:r64(entry+0x18);
    eq(mode?"entry_borrow_identity":"entry_copy_distinct",mode?(payload==src):(payload!=src),1);
    eq(mode?"borrow_entry_source_size":"copy_entry_source_size",r32(entry+0x40),0x400);
    eq(mode?"borrow_normalizes_external_name":"copy_normalizes_original_before_copy",r8(src+0x13),0);
    if(!mode){
        eq("owned_entry_buffer_capacity",r32(entry+0x20),0x400);
        eq("owned_entry_buffer_used",r32(entry+0x28),0x400);
        bytes("owned_entry_payload_copied",payload,(void*)src,0x400);
    }
    w64(entry+0x38,payload);
    uint32_t id=attach(payload,0x40);
    uintptr_t c=r64(0x2ebcd80+0x18);
    w32(entry+0x44,id);
    eq(mode?"borrow_context_points_into_source":"context_borrows_entry_owned_copy",r64(c+0x870),payload+0x50);
    uintptr_t root=H+0x100000,r=root;
    w32(root+0x48800,0);
    w16(r+4,0xffff);
    w64(r+0x68,payload);
    w32(r+0x69c,0x8888);
    w64(r+0xe0,payload);
    w64(r+0xd8,H+0x7770);
    w64(r+0xf8,payload);
    w64(r+0xf0,H+0x7780);
    w32(r+0x42c,(uint32_t)payload);
    w32(r+0x430,(uint32_t)payload);
    w32(r+0x390,(uint32_t)payload);
    w32(r+0x394,0x12345678);
    ((void(ABI*)(uintptr_t,uintptr_t))0x409d60)(b,payload);
    eq(mode?"borrow_cancel_destroys_context":"owned_cancel_destroys_context",allocated(c),0);
    eq(mode?"borrow_owner_not_reclaimed":"owned_entry_copy_reclaimed",allocated(payload),mode?1:0);
    eq(mode?"borrow_original_live":"copy_original_live",allocated(src),1);
    eq(mode?"borrow_bank_count_zero":"owned_bank_count_zero",r32(b+0x58),0);
    eq(mode?"borrow_slot_removed":"owned_slot_removed",r32(H+0x3000),0xffffffff);
    eq(mode?"borrow_entry_reference_cleared":"owned_entry_reference_cleared",r64(entry+0x30),0);
    eq(mode?"borrow_entry_cache_stale":"owned_entry_cache_stale",r64(entry+0x38),payload);
    eq(mode?"borrow_entry_ticket_invalid":"owned_entry_ticket_invalid",r32(entry+0x44),0xffffffff);
    eq(mode?"borrow_render_key_cleared":"owned_render_key_cleared",r64(r+0x68),0);
    eq(mode?"borrow_render_side_pair_cleared":"owned_render_side_pair_cleared",r64(r+0xd8)|r64(r+0xe0)|r64(r+0xf0)|r64(r+0xf8),0);
    eq(mode?"borrow_render_encoded_refs_cleared":"owned_render_encoded_refs_cleared",r32(r+0x42c)|r32(r+0x430)|r32(r+0x390)|r32(r+0x69c),0);
    eq(mode?"borrow_unrelated_render_field_preserved":"owned_unrelated_render_field_preserved",r32(r+0x394),0x12345678);
    eq(mode?"borrow_internal_heap_reclaimed":"owned_internal_heap_reclaimed",usage(8),0);
    release(src);
    eq(mode?"borrow_owner_cleanup_separate":"copy_owner_cleanup_separate",usage(6),0);
    eq(mode?"borrow_complete_chain_no_diagnostic":"owned_complete_chain_no_diagnostic",formats,0);
}
static void resize_case(void){
    reset();
    phase="buffer_resize";
    uintptr_t d=H+0x8000;
    ((void(ABI*)(uintptr_t))0x51ee10)(d);
    ((void(ABI*)(uintptr_t,unsigned,unsigned))0x51f020)(d,0x100,0);
    uintptr_t old=r64(d+8);
    memset((void*)old,0x69,0x100);
    w32(d+0x18,7);
    uintptr_t c=context(3,4);
    w8(c+3,1);
    w64(c+0x870,old+16);
    ((void(ABI*)(uintptr_t,unsigned,unsigned))0x51eeb0)(d,0x200,1);
    uintptr_t newer=r64(d+8);
    eq("resize_replaces_source",newer!=old,1);
    eq("resize_frees_old_source",allocated(old),0);
    eq("resize_copies_capacity_not_only_used",r8(newer+0xff),0x69);
    eq("resize_zero_fills_new_tail",r8(newer+0x100)|r8(newer+0x1ff),0);
    eq("resize_preserves_used_field",r32(d+0x18),7);
    eq("resize_does_not_repair_borrowed_context",r64(c+0x870),old+16);
    dispose(c);
    ((void(ABI*)(uintptr_t))0x51ee80)(d);
    eq("resized_buffer_reclaimed",usage(8),0);
    eq("resize_no_diagnostic",formats,0);
}
static void membership_case(void){
    reset();
    phase="tagged_membership_and_free";
    uintptr_t p=alloc(0x400,6),o=p-0x40,slot=H+0x9000,ar=0x22d7fd0+6*0xa8;
    uint32_t h=(uint32_t)slot|1;
    w16(slot,0xffff);
    w16(slot+2,0xffff);
    w8(slot+4,6);
    w8(slot+5,1);
    w16(slot+6,r16(o+0x1c));
    w64(slot+8,o);
    w64(ar+0x30,slot);
    w64(ar+0x40,0);
    w64(ar+0x48,slot);
    w8(o+0x15,r8(o+0x15)|4);
    uint32_t before=usage(6);
    ((void(ABI*)(uintptr_t))0x3ab940)(h);
    eq("tagged_release_publishes_tree_root",r64(ar+0x50),o);
    eq("tagged_release_sets_membership_bit",r8(o+0x15)&2,2);
    eq("tagged_release_does_not_free_storage",allocated(p),1);
    eq("tagged_release_keeps_usage",usage(6),before);
    ((void(ABI*)(uintptr_t))0x3ab940)(h);
    eq("tagged_repeat_release_same_root",r64(ar+0x50),o);
    uintptr_t got=((uintptr_t(ABI*)(uintptr_t))0x3ab880)(h);
    eq("tagged_acquire_returns_payload",got,p);
    eq("tagged_acquire_removes_tree_membership",r64(ar+0x50),0);
    eq("tagged_acquire_clears_bit",r8(o+0x15)&2,0);
    eq("tagged_repeat_acquire_no_reference_count",((uintptr_t(ABI*)(uintptr_t))0x3ab880)(h),p);
    ((void(ABI*)(uintptr_t))0x3ab940)(h);
    eq("single_release_reinserts_after_two_acquires",r64(ar+0x50),o);
    eq("single_release_storage_still_live",allocated(p),1);
    w16(slot+6,r16(o+0x1c)^1);
    eq("generation_mismatch_acquire_returns_zero",((uintptr_t(ABI*)(uintptr_t))0x3ab880)(h),0);
    eq("generation_mismatch_preserves_membership",r64(ar+0x50),o);
    w16(slot+6,r16(o+0x1c));
    ((void(ABI*)(uintptr_t))0x3ab7c0)(h);
    eq("destroy_tagged_source_frees_payload",allocated(p),0);
    eq("destroy_tagged_source_clears_slot_owner",r64(slot+8),0);
    eq("destroy_tagged_source_clears_live_flag",r8(slot+5),0);
    eq("destroy_tagged_source_unlinks_tree",r64(ar+0x50),0);
    eq("destroy_tagged_source_returns_slot",r64(ar+0x40),slot);
    eq("destroy_tagged_source_reclaims_usage",usage(6),0);
    eq("membership_lifecycle_no_diagnostic",formats,0);
}
static void exact_match_cases(void){
    reset();
    phase="no_matching_resource_entry";
    uintptr_t b=bank(),e=H+0x5000,root=H+0x100000;
    w32(e+4,1);
    w64(e+0x30,H+0x6000);
    w32(root+0x48800,0);
    w16(root+4,0xffff);
    w64(root+0x68,H+0x6100);
    ((void(ABI*)(uintptr_t,uintptr_t))0x409d60)(b,H+0x6100);
    eq("no_matching_entry_does_not_clear_render_references",r64(root+0x68),H+0x6100);
    eq("no_matching_entry_retains_bank_count",r32(b+0x58),1);
    reset();
    phase="null_source_setup";
    e=H+0x5000;
    memset((void*)e,0x7b,0x50);
    unsigned char saved[0x50];
    memcpy(saved,(void*)e,0x50);
    ((void(ABI*)(uintptr_t,uintptr_t,unsigned))0x409a60)(e,0,1);
    bytes("null_entry_source_preserves_entire_entry",e,saved,0x50);
    reset();
    phase="standalone_reference_clear";
    root=H+0x100000;
    w32(root+0x48800,0);
    w16(root+4,0xffff);
    w64(root+0xe0,H+0x6000);
    w64(root+0xd8,H+0x6100);
    ((void(ABI*)(uintptr_t))0x427b00)(H+0x6000);
    eq("reference_clear_does_not_compare_paired_E0",r64(root+0xe0),H+0x6000);
    ((void(ABI*)(uintptr_t))0x427b00)(H+0x6100);
    eq("reference_clear_compares_D8_then_clears_pair",r64(root+0xd8)|r64(root+0xe0),0);
}
static void apply_variant(void){
    struct V{
        const char*name;
        uintptr_t address;
        unsigned n;
        unsigned char old[6],replacement[6];
    }
    ;
    const struct V v[]={
        {
            "borrow_mask",0x3ee11a,1,{
                4
            }
            ,{
                8
            }
        }
        ,
        {
            "skip_owned_run_free",0x3a9617,2,{
                0x75,0x18
            }
            ,{
                0xeb,0x18
            }
        }
        ,
        {
            "skip_lookup_table_free",0x3a9697,5,{
                0xe9,0x54,0x01,0xfc,0xff
            }
            ,{
                0xc3,0x90,0x90,0x90,0x90
            }
        }
        ,
        {
            "copy_unrounded_length",0x3ee15f,1,{
                0xf0
            }
            ,{
                0xff
            }
        }
        ,
        {
            "ignore_ticket_generation",0x3b3801,6,{
                0x0f,0x85,0x93,0,0,0
            }
            ,{
                0x90,0x90,0x90,0x90,0x90,0x90
            }
        }
        ,
        {
            "compare_wrong_reference_side",0x409dee,4,{
                0xe0,0,0,0
            }
            ,{
                0xd8,0,0,0
            }
        }
        ,
        {
            "skip_old_buffer_release",0x51ef5a,5,{
                0xe8,0x61,0xc8,0xe8,0xff
            }
            ,{
                0x90,0x90,0x90,0x90,0x90
            }
        }
        ,
        {
            "skip_context_cancellation",0x409ec0,5,{
                0xe8,0x1b,0x99,0xfa,0xff
            }
            ,{
                0x90,0x90,0x90,0x90,0x90
            }
        }
        ,
        {
            "ignore_tree_membership",0x36a041,1,{
                2
            }
            ,{
                0
            }
        }
        ,
        {
            "skip_context_rebase",0x3b351a,5,{
                0xe8,0x51,0xa4,0xe9,0xff
            }
            ,{
                0x90,0x90,0x90,0x90,0x90
            }
        }
    }
    ;
    if(!mutant)return;
    for(unsigned j=0;j<sizeof(v)/sizeof(v[0]);j++)if(!strcmp(mutant,v[j].name)){
        if(memcmp((void*)v[j].address,v[j].old,v[j].n)){
            fprintf(stderr,"variant preimage mismatch: %s\n",mutant);
            exit(2);
        }
        memcpy((void*)v[j].address,v[j].replacement,v[j].n);
        return;
    }
    fprintf(stderr,"unknown variant\n");
    exit(2);
}
static void same_key_case(void){
    reset();
    phase="same_tag_name_reuses_existing_entry";
    uintptr_t b=bank(),e=H+0x5000,old=alloc(0x400,6),fresh=alloc(0x400,6);
    memset((void*)old,0,0x400);
    memset((void*)fresh,0,0x400);
    memcpy((void*)old,"TEST",4);
    memcpy((void*)fresh,"TEST",4);
    w32(old+8,0x100);
    w32(fresh+8,0x200);
    memcpy((void*)(old+0x10),"SAME",5);
    memcpy((void*)(fresh+0x10),"SAME",5);
    w8(old+0x80,0x11);
    w8(fresh+0x80,0x22);
    ((void(ABI*)(uintptr_t,uintptr_t,unsigned))0x409a60)(e,old,1);
    w64(e+0x38,old);
    unsigned char before[0x50];
    memcpy(before,(void*)e,0x50);
    uint32_t used=usage(6);
    eq("same_tag_name_returns_existing_slot",((int(ABI*)(uintptr_t,uintptr_t))0x409fe0)(b,fresh),0);
    bytes("same_tag_name_does_not_replace_existing_entry",e,before,0x50);
    eq("same_tag_name_retains_old_payload",r8(r64(e+0x30)+0x80),0x11);
    eq("same_tag_name_does_not_acquire_new_backing",usage(6),used);
    eq("same_tag_name_keeps_one_active_entry",r32(b+0x58),1);
    ((void(ABI*)(uintptr_t,uintptr_t))0x409d60)(b,old);
    release(old);
    release(fresh);
    eq("same_key_fixture_reclaims_allocations",usage(6),0);
}
/* Simulated external relocation: the original mover is NOT run. The update driver is. */
static void moved_source_case(void){
    reset();
    phase="original_driver_after_simulated_source_move";
    tickets();
    uintptr_t old=alloc(0x400,6),slot=H+0x9000;
    makefile(old,0x800,0x2b0,255);
    w64(slot+8,old-0x40);
    uint32_t id=attach(slot|1,0);
    uintptr_t c=r64(0x2ebcd80+0x18),table=r64(c+0x848);
    eq("tagged_context_source_initial_binding",r64(c+0x858),old);
    eq("tagged_context_run_initial_binding",r64(c+0x870),old+16);
    uintptr_t replacement=alloc(0x400,6);
    memcpy((void*)replacement,(void*)old,0x400);
    w64(slot+8,replacement-0x40);
    release(old);
    ((void(ABI*)(uintptr_t,uintptr_t))0x3b3480)(c,0);
    eq("driver_publishes_changed_full_base",r64(c+0x858),replacement);
    eq("driver_repairs_table_element",r64(table+8),replacement+32);
    eq("driver_keeps_run_pointer_as_stale_provenance",r64(c+0x870),old+16);
    eq("driver_does_not_replace_owned_table",r64(c+0x848),table);
    eq("driver_does_not_acquire_or_free_new_owner",allocated(replacement),1);
    ((void(ABI*)(uintptr_t,uintptr_t))0x3b3480)(c,0);
    eq("driver_unchanged_base_no_double_delta",r64(table+8),replacement+32);
    cancel(id);
    eq("borrowed_stale_run_not_freed_on_cancel",allocated(replacement),1);
    eq("rebased_context_tables_reclaimed",usage(8),0);
    release(replacement);
    eq("relocation_fixture_owner_cleanup",usage(6),0);
    eq("rebase_path_no_allocator_diagnostic",formats,0);
}
int main(int argc,char**argv){
    if(argc<2)return 2;
    load(argv[1]);
    mutant=argc>2?argv[2]:NULL;
    apply_variant();
    setbuf(stdout,NULL);
    printf("{\"evidence_class\":\"isolated original-instruction execution; synthetic arenas\",\"cases\":[\n");
    basic();
    flags_and_reuse();
    ticket_cases();
    resource_cases(0);
    resource_cases(1);
    resize_case();
    membership_case();
    exact_match_cases();
    same_key_case();
    moved_source_case();
    printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);
    return failures?1:0;
}
