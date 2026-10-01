/* SECTION-08: original source-owner completion/deletion and resource view discipline.
 * Linux x86-64 host, Microsoft x64 ABI, private original PE image and synthetic state.
 * One diagnostic formatter substitution and three CRT import bridges; no IO or live game.
 * Real queue submission and done/error helpers run; the full queue pump is NOT run.
 * Mutants alter private mapped instructions only. See REVIEW.md and run_review.py.
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
static uintptr_t watch_src;

static const char*phase="init";
static const char*mutant;
static unsigned copy_pin_observations, copy_pin_ok;

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
static void*ABI msset(void*p,int c,size_t n){
    return memset(p,c,n);
}
static void*ABI mscopy(void*p,const void*s,size_t n){
    uintptr_t d=(uintptr_t)p,a=(uintptr_t)s;
    if (a==watch_src && n && phase && strcmp(phase,"copy_pins_source")==0) {
        copy_pin_observations++; copy_pin_ok+=!(r8(a-0x2b)&2);
    }
    if(n && d<a+n && a<d+n && d!=a){
        /* Overlap behavior is a separate import boundary: never silently emulate
         * the original Windows memcpy for an overlapping case. */
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
    formats=0;
    memset((void*)0x2b581a0,0,0x8e0);
    memset((void*)0x22c31c0,0,0x2040);
    w8(0x2b62e10,1); w64(H+0x100000+0x48830,H+0x180000);
    copy_pin_observations=copy_pin_ok=0; watch_src=0;
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
static uint32_t halloc(unsigned n){
    select_arena(6);
    uint32_t h=((uint32_t(ABI*)(unsigned))0x36b160)(n);
    pop();
    if(!h){fprintf(stderr,"native halloc failed\n");exit(2);}return h;
}
static uintptr_t resolve(uint32_t h){return ((uintptr_t(ABI*)(uint32_t))0x36b130)(h);}
static uintptr_t pin(uint32_t h){return ((uintptr_t(ABI*)(uint32_t))0x36a000)(h);}
static void destroy(uint32_t h){((void(ABI*)(uintptr_t))0x3ab7c0)(h);}
static int compact(int all){return ((int(ABI*)(unsigned,int))0x369c60)(6,all);}

static uintptr_t bank_setup(unsigned capacity,unsigned occupied){
 uintptr_t b=H+0x2000,slot=H+0x3000,page=H+0x4000,entry=H+0x5000;
 w64(b+0x38,slot);w64(b+0x10,page);w32(b+0x40,occupied?0:0xffffffff);w32(b+0x44,occupied?0:0xffffffff);
 w32(b+0x48,0x50);w32(b+0x4c,5);w32(b+0x50,31);w32(b+0x54,capacity);w32(b+0x58,occupied);
 w8(b,1);w16(b+0x22,1);w32(b+0x18,0xffffffff);
 for(unsigned i=0;i<32;i++){w32(slot+i*16,0xffffffff);w32(slot+i*16+4,0xffffffff);w32(slot+i*16+8,0xffffffff);}
 if(occupied)w32(slot,0);
 w32(page+0x10,(uint32_t)entry);w32(page+0x14,occupied);
 ((void(ABI*)(uintptr_t))0x409710)(entry);
 w64(H+0x180000+0xd90,b);return b;
}
static void source_data(uintptr_t p,const char*name,unsigned marker){
 memset((void*)p,0xC3,0x400);memcpy((void*)p,"TEST",4);w32(p+8,0x400);
 memset((void*)(p+0x10),0,0x20);strncpy((char*)(p+0x10),name,31);
 makefile(p+0x40,0x800,0x2b0,255);w8(p+0x3ff,marker);
}
static uintptr_t ownrec(unsigned group,unsigned index){return 0x2b581a0+(group*16+index)*0x1c;}
static void request_delete(unsigned group,unsigned index){((void(ABI*)(int,int))0x3dd420)(group,index);}
static void complete(uintptr_t rec){((void(ABI*)(uint32_t))0x3dd850)((uint32_t)rec);}
static uint32_t published(unsigned group,unsigned index){return ((uint32_t(ABI*)(int,int))0x3dd740)(group,index);}
static void entry_setup(uintptr_t e,uintptr_t s,unsigned mode){((void(ABI*)(uintptr_t,uintptr_t,unsigned))0x409a60)(e,s,mode);}
static uintptr_t view(uintptr_t e,uint32_t tag){return ((uintptr_t(ABI*)(uintptr_t,uint32_t,uintptr_t))0x409960)(e,tag,0);}
static void view_end(uintptr_t e){((void(ABI*)(uintptr_t))0x409c00)(e);}
static void external_delete(uintptr_t repr){((void(ABI*)(uintptr_t,uintptr_t))0x41e490)(H+0x180000,repr);}
static void setup_owner(unsigned capacity,uint32_t*h,uintptr_t*p,uintptr_t*rec){
 reset();bank_setup(capacity,0);*h=halloc(0x400);*p=resolve(*h);source_data(*p,"owner-A",0x81);
 *rec=ownrec(1,3);w32(*rec,*h);w32(*rec+4,3);w8(*rec+0xd,0xA7);pin(*h);
}
static void copy_and_views(void){
 reset();phase="copy_pins_source";bank_setup(32,1);uint32_t h=halloc(0x400);uintptr_t p=resolve(h),e=H+0x5000;
 source_data(p,"copy-A",0x91);watch_src=p;entry_setup(e,h,0);
 eq("copy_source_was_pinned_at_actual_copy_import",copy_pin_ok,1);eq("one_source_copy_observed",copy_pin_observations,1);
 eq("copy_returns_source_to_movable_tree",r8(p-0x2b)&2,2);eq("copy_allocates_independent_backing",r64(e+0x18)!=p,1);
 eq("copy_preserves_marker",r8(r64(e+0x18)+0x3ff),0x91);
 ((void(ABI*)(uintptr_t))0x409730)(e);destroy(h);eq("copy_no_heap_leak",usage(6)|usage(8),0);
 reset();phase="nested_pin_not_counted";bank_setup(32,1);h=halloc(0x400);p=resolve(h);source_data(p,"copy-B",0x42);pin(h);entry_setup(e,h,0);
 eq("copy_releases_preexisting_pin_too",r8(p-0x2b)&2,2);((void(ABI*)(uintptr_t))0x409730)(e);destroy(h);
 reset();phase="tagged_entry_view";bank_setup(32,1);uintptr_t hole=alloc(0x400,6),sep=alloc(0x100,6);h=halloc(0x400);p=resolve(h);uintptr_t tail=alloc(0x80,6);
 source_data(p,"view-A",0x67);entry_setup(e,h,1);w64(e+0x38,p);release(hole);
 eq("borrow_setup_retains_handle_not_resolved_pointer",r64(e+0x30),h);
 eq("borrow_setup_does_not_pin",r8(p-0x2b)&2,2);
 eq("valid_view_resolves_payload",view(e,0x54534554),p);eq("valid_view_pins_source",r8(p-0x2b)&2,0);
 eq("pinned_view_prevents_exact_movement",compact(0),0);eq("pinned_view_keeps_address",resolve(h),p);
 eq("second_view_returns_same_pointer",view(e,0x54534554),p);
 view_end(e);eq("one_end_unpins_two_views",r8(p-0x2b)&2,2);
 eq("end_restores_movement_eligibility",compact(0),1);uintptr_t now=resolve(h);
 eq("source_relocated_after_view_end",now!=p,1);eq("entry_retains_stale_cache_before_next_lookup",r64(e+0x38),p);
 eq("next_view_refreshes_cache_and_returns_new_pointer",view(e,0x54534554),now);eq("cache_now_matches_tag_resolution",r64(e+0x38),now);
 view_end(e);destroy(h);release(sep);release(tail);eq("view_test_allocation_cleanup",usage(6),0);
 reset();phase="failed_view_has_no_acquire";bank_setup(32,1);h=halloc(0x400);p=resolve(h);source_data(p,"view-B",0);entry_setup(e,h,1);w64(e+0x38,p);
 eq("wrong_section_returns_null",view(e,0x12345678),0);eq("failed_lookup_leaves_eligibility_unchanged",r8(p-0x2b)&2,2);
 destroy(h);
}
static void normal_and_full(void){
 uint32_t h;uintptr_t p,rec;setup_owner(32,&h,&p,&rec);phase="completion_registers_external_owner";
 eq("not_published_while_submitted",published(1,3),0);complete(rec);
 eq("completion_marks_owner_published",r32(rec+4),4);eq("lookup_publishes_handle",published(1,3),h);
 eq("completion_unpins_source",r8(p-0x2b)&2,2);eq("original_registration_adds_bank_row",r32(H+0x2000+0x58),1);
 eq("registered_row_borrows_tagged_owner",r64(H+0x5000+0x30),h);eq("registered_row_mode_is_reference",r32(H+0x5000+4),1);
 eq("plain_non_efx_source_has_no_context_ticket",r32(H+0x5000+0x44),0xffffffff);
 request_delete(1,3);eq("published_owner_delete_frees_source",allocated(p),0);eq("published_owner_delete_removes_bank_row",r32(H+0x2000+0x58),0);
 eq("synchronous_delete_clears_handle_and_state",r64(rec),0);eq("synchronous_delete_clears_aux_byte",r8(rec+0xd),0);
 eq("delete_does_not_publish_stale_handle",published(1,3),0);eq("normal_lifecycle_no_heap_leak",usage(6)|usage(8),0);
 setup_owner(0,&h,&p,&rec);phase="registration_failure_does_not_stop_state4";complete(rec);
 eq("full_bank_has_no_new_entry",r32(H+0x2000+0x58),0);eq("callback_ignores_registration_failure",r32(rec+4),4);
 eq("state4_lookup_is_not_registry_success_test",published(1,3),h);request_delete(1,3);eq("unregistered_owner_still_freed",allocated(p),0);
}
static void deferred_delete(void){
 uint32_t h;uintptr_t p,rec;setup_owner(32,&h,&p,&rec);phase="delete_while_inflight";
 request_delete(1,3);eq("inflight_delete_selects_state5",r32(rec+4),5);eq("deferred_delete_keeps_owner_handle",r32(rec),h);
 eq("deferred_delete_keeps_source_live",allocated(p),1);eq("deferred_delete_keeps_source_pinned",r8(p-0x2b)&2,0);
 eq("deferred_delete_preserves_aux_byte",r8(rec+0xd),0xA7);request_delete(1,3);eq("repeat_delete_stays_pending",r32(rec+4),5);
 complete(rec);eq("completion_observes_pending_delete_and_frees",allocated(p),0);eq("cancel_completion_clears_state",r32(rec+4),0);
 eq("cancel_completion_preserves_numeric_handle",r32(rec),h);eq("cancel_completion_preserves_aux_byte",r8(rec+0xd),0xA7);
 eq("state0_hides_retained_handle",published(1,3),0);eq("cancel_completion_does_not_register",r32(H+0x2000+0x58),0);
 eq("cancel_lifecycle_no_heap_leak",usage(6)|usage(8),0);
 for(unsigned state=0;state<=5;state++){
  if(state==3||state==4||state==5)continue;
  setup_owner(32,&h,&p,&rec);phase="delete_state_matrix";w32(rec+4,state);request_delete(1,3);
  char n[100];snprintf(n,sizeof n,"delete_state_%u_handle",state);eq(n,r32(rec),state==1?0:h);
  snprintf(n,sizeof n,"delete_state_%u_allocation",state);eq(n,allocated(p),state==1?0:1);
  snprintf(n,sizeof n,"delete_state_%u_final_state",state);eq(n,r32(rec+4),state==1?0:state);
  if(state!=1)destroy(h);
 }
}
static void tagged_disposal_with_context(void){
 reset();phase="owner_destruction_removes_real_borrowed_context";tickets();bank_setup(32,1);
 uint32_t h=halloc(0x500);uintptr_t p=resolve(h),rec=ownrec(2,4),e=H+0x5000;
 source_data(p,"context-A",0);entry_setup(e,h,1);w64(e+0x38,p);uint32_t ticket=attach(h,0x40);uintptr_t c=r64(0x2ebcd80+0x18);w32(e+0x44,ticket);
 w32(rec,h);w32(rec+4,4);uintptr_t root=H+0x100000;w32(root+0x48800,0);w16(root+4,0xffff);
 w64(root+0xe0,h);w64(root+0xd8,p);w64(root+0xf8,p);w64(root+0xf0,h);
 request_delete(2,4);
 eq("owner_delete_reclaims_context",allocated(c),0);eq("owner_delete_reclaims_external_payload",allocated(p),0);
 eq("handle_matched_render_pair_is_cleared",r64(root+0xe0)|r64(root+0xd8),0);
 eq("context_cancel_clears_other_pair_via_second_sweep",r64(root+0xf8)|r64(root+0xf0),0);
 eq("entry_ticket_invalid_after_cancellation",r32(e+0x44),0xffffffff);eq("owner_delete_all_heap_usage_gone",usage(6)|usage(8),0);
 reset();phase="raw_pointer_is_not_entry_reference_identity";bank_setup(32,1);h=halloc(0x400);p=resolve(h);source_data(p,"identity-A",0x11);entry_setup(e,h,1);w64(e+0x38,p);
 external_delete(p);eq("raw_delete_does_not_match_tagged_entry",r32(H+0x2000+0x58),1);eq("raw_delete_keeps_external_allocation",allocated(p),1);
 external_delete(h);eq("tagged_delete_matches_entry",r32(H+0x2000+0x58),0);eq("entry_delete_alone_does_not_free_external_owner",allocated(p),1);destroy(h);
}
static void same_name_reuse(void){
 uint32_t h1;uintptr_t p1,r1;setup_owner(32,&h1,&p1,&r1);phase="equal_key_is_reuse_not_reload";complete(r1);
 uint32_t h2=halloc(0x400);uintptr_t p2=resolve(h2),r2=ownrec(1,4);source_data(p2,"owner-A",0xD7);w32(r2,h2);w32(r2+4,3);pin(h2);complete(r2);
 eq("equal_name_keeps_one_entry",r32(H+0x2000+0x58),1);eq("equal_name_keeps_first_owner_representation",r64(H+0x5000+0x30),h1);
 eq("equal_name_keeps_first_cached_source",r64(H+0x5000+0x38),p1);eq("second_owner_is_marked_state4",r32(r2+4),4);
 eq("original_entry_still_reads_first_payload",r8(p1+0x3ff),0x81);eq("second_payload_has_different_value",r8(p2+0x3ff),0xD7);
 request_delete(1,4);eq("delete_second_owner_frees_only_second_source",allocated(p2),0);eq("delete_second_owner_keeps_first_source",allocated(p1),1);
 eq("delete_second_owner_keeps_existing_entry",r32(H+0x2000+0x58),1);request_delete(1,3);eq("delete_first_owner_removes_entry",r32(H+0x2000+0x58),0);eq("both_owners_reclaimed",usage(6)|usage(8),0);
}
static void submission(void){
 uint32_t h;uintptr_t p,rec;setup_owner(32,&h,&p,&rec);phase="original_queue_submission";
 ((void(ABI*)(void))0x32e450)();w8(0x2b5e111,0);w16(rec+0x10,9);w16(rec+0x12,12);w32(rec+0x14,0x180);w32(rec+0x18,0x1234);w32(rec+4,1);
 ((void(ABI*)(uintptr_t))0x3dda70)(rec);uintptr_t slot=0x22c31c0;
 eq("submission_sets_state3",r32(rec+4),3);eq("submission_enqueues_real_request",r64(0x22c51c0),slot);
 eq("submission_queue_destination_is_resolved_payload",r64(slot+0x70),p);eq("submission_callback_is_original_completion",r64(slot+0x40),0x3dd850);
 eq("submission_callback_argument_is_record_address",r32(slot+0x60),(uint32_t)rec);eq("submission_has_no_cancel_callback",r64(slot+0x48),0);
 eq("submission_does_not_unpin_payload",r8(p-0x2b)&2,0);eq("submission_uses_requested_count",r32(slot+0x28),0x180);
 eq("submission_uses_aligned_offset",r32(slot+0x2c),0x1000);
 // No IO/pump is run. Run its ORIGINAL completion helper against the submitted slot.
 request_delete(1,3);
 eq("owner_delete_does_not_cancel_queued_request",r64(0x22c51c0),slot);
 eq("owner_delete_keeps_original_completion_callback",r64(slot+0x40),0x3dd850);
 ((void(ABI*)(uintptr_t))0x32e330)(slot);
 eq("real_completion_helper_delivers_pending_delete",r32(rec+4),0);
 eq("real_completion_helper_reclaims_payload",allocated(p),0);
 eq("completion_helper_itself_does_not_recycle_queue",r64(0x22c51c0),slot);
 // Isolate fixture cleanup from the tested completion; no queued IO was started.
 ((void(ABI*)(void))0x32e450)();
 setup_owner(32,&h,&p,&rec);phase="error_helper_without_owner_callback";((void(ABI*)(void))0x32e450)();
 w8(0x2b5e111,0);w16(rec+0x10,9);w16(rec+0x12,12);w32(rec+0x14,0x180);
 ((void(ABI*)(uintptr_t))0x3dda70)(rec);((void(ABI*)(uintptr_t))0x32e370)(slot);
 eq("positive_count_error_helper_omits_owner_callback",r32(rec+4),3);
 eq("positive_count_error_helper_leaves_source_pinned",r8(p-0x2b)&2,0);
 eq("positive_count_error_helper_leaves_source_live",allocated(p),1);
 ((void(ABI*)(void))0x32e450)();destroy(h);
 setup_owner(32,&h,&p,&rec);phase="rejected_submit_still_sets_state3";((void(ABI*)(void))0x32e450)();w16(rec+0x10,9);w16(rec+0x12,0xffff);w32(rec+4,1);
 ((void(ABI*)(uintptr_t))0x3dda70)(rec);eq("rejected_index_enqueues_nothing",r64(0x22c51c0),0);eq("rejected_index_still_sets_owner_state3",r32(rec+4),3);
 request_delete(1,3);eq("failed_submit_delete_waits_in_state5",r32(rec+4),5);eq("failed_submit_has_no_completion_queued",r64(0x22c51c0),0);
 destroy(h); // synthetic invalid index, not claimed reachable by the normal producer
}

static void bulk_delete(void){
 reset();phase="single_group_bulk_deletion";bank_setup(32,1);
 uint32_t a=halloc(0x100),b=halloc(0x100),c=halloc(0x400),d=halloc(0x100);
 uintptr_t pa=resolve(a),pb=resolve(b),pc=resolve(c),pd=resolve(d),e=H+0x5000;
 source_data(pc,"bulk-C",0x22);entry_setup(e,c,1);w64(e+0x38,pc);
 uintptr_t ra=ownrec(0,0),rb=ownrec(0,5),rc=ownrec(0,15),rd=ownrec(1,0);
 w32(ra,a);w32(ra+4,1);w8(ra+0xd,0x77);w32(ra+8,0xabcdef12);
 w32(rb,b);w32(rb+4,3);pin(b);w32(rc,c);w32(rc+4,4);w8(rc+0xd,0x66);
 w32(rd,d);w32(rd+4,1);
 ((void(ABI*)(int))0x3dd380)(0);
 eq("bulk_frees_allocated_state1",allocated(pa),0);
 eq("bulk_defers_submitted_state3",r32(rb+4),5);
 eq("bulk_preserves_inflight_allocation",allocated(pb),1);
 eq("bulk_clears_last_ready_slot",r64(rc),0);
 eq("bulk_reclaims_last_ready_allocation",allocated(pc),0);
 eq("bulk_removes_registered_entry",r32(H+0x2000+0x58),0);
 eq("bulk_clears_aux_only_on_free_paths",r8(ra+0xd)|r8(rc+0xd),0);
 eq("bulk_preserves_unassigned_record_bytes",r32(ra+8),0xabcdef12);
 eq("bulk_does_not_touch_other_group",r32(rd),d);
 eq("bulk_preserves_other_group_allocation",allocated(pd),1);
 complete(rb);request_delete(1,0);eq("bulk_fixture_all_allocations_reclaimed",usage(6)|usage(8),0);
}

static void mutation(uintptr_t a,const unsigned char*old,const unsigned char*val,size_t n){if(memcmp((void*)a,old,n)){fputs("mutation preimage differs\n",stderr);exit(2);}memcpy((void*)a,val,n);}
static void apply_variant(void){
 if(!mutant)return;
 if(strcmp(mutant,"copy_without_acquire")==0){mutation(0x409ba7,(const unsigned char[]){0xe8,0xd4,0x1c,0xfa,0xff},(const unsigned char[]){0xe8,0x44,0x1c,0xfa,0xff},5);return;}
 if(strcmp(mutant,"view_without_acquire")==0){mutation(0x4099cc,(const unsigned char[]){0xe8,0xaf,0x1e,0xfa,0xff},(const unsigned char[]){0xe8,0x1f,0x1e,0xfa,0xff},5);return;}
 if(strcmp(mutant,"skip_cache_publication")==0){mutation(0x4097f9,(const unsigned char[]){0x48,0x89,0x43,0x38},(const unsigned char[]){0x90,0x90,0x90,0x90},4);return;}
 if(strcmp(mutant,"match_cache_instead_of_reference")==0){mutation(0x4095d5,(const unsigned char[]){0x49,0x39,0x59,0x30},(const unsigned char[]){0x49,0x39,0x59,0x38},4);return;}
 if(strcmp(mutant,"keep_completion_pinned")==0){mutation(0x3dd85e,(const unsigned char[]){0xe8,0x0d,0xf9,0xf8,0xff},(const unsigned char[]){0x90,0x90,0x90,0x90,0x90},5);return;}
 if(strcmp(mutant,"discard_pending_delete")==0){mutation(0x3dd490,(const unsigned char[]){0xc7,0x47,0x04,0x05,0x00,0x00,0x00},(const unsigned char[]){0xc7,0x47,0x04,0x00,0x00,0x00,0x00},7);return;}
 if(strcmp(mutant,"erase_cancelled_handle")==0){mutation(0x3dd88e,(const unsigned char[]){0xc7,0x47,0x04,0x00,0x00,0x00,0x00},(const unsigned char[]){0x48,0xc7,0x07,0x00,0x00,0x00,0x00},7);return;}
 if(strcmp(mutant,"submission_claims_ready")==0){mutation(0x3ddabe,(const unsigned char[]){0xc7,0x43,0x04,0x03,0x00,0x00,0x00},(const unsigned char[]){0xc7,0x43,0x04,0x04,0x00,0x00,0x00},7);return;}
 if(strcmp(mutant,"bulk_skips_last_slot")==0){mutation(0x3dd392,(const unsigned char[]){0xbe,0x10,0,0,0},(const unsigned char[]){0xbe,0x0f,0,0,0},5);return;}
 fputs("unknown variant\n",stderr);exit(2);
}
int main(int argc,char**argv){
 if(argc<2||argc>3)return 2;
 mutant=argc==3?argv[2]:NULL;load(argv[1]);apply_variant();printf("{\"cases\":[\n");
 copy_and_views();normal_and_full();deferred_delete();tagged_disposal_with_context();same_name_reuse();submission();bulk_delete();
 printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);return failures?1:0;
}
