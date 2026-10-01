/* group_completion_driver.c - run the reconstruction over the same image the emulator gets.
 *
 *   group_completion_driver <regions.bin> <cases.txt> [post.bin]
 *
 * regions.bin :  u32 count, then per region  u64 va, u32 size, size bytes
 * cases.txt   :  one battle-unit virtual address in hex per line, in call order
 *
 * Prints a schema header, one JSON record per case, and a final DIGEST.
 * Records exact callback identities/arguments/order and memory digests at each boundary.
 * The digest is not decoration: this path's whole purpose is the two masks it writes, and a
 * comparison that comes back "returns match" while a mask differs would be worthless.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../../Game/Spawn/group_completion.h"

typedef struct Call {
    uint32_t target;
    uint64_t args[3];
    int argc;
    uint64_t memory;
} Call;

typedef struct Log {
    const GroupImage *image;
    Call calls[16];
    int n, overflow;
} Log;

static uint64_t digest(const GroupImage *image)
{
    uint64_t h = 1469598103934665603ull;
    size_t r, k;
    for (r = 0; r < image->count; r++)
        for (k = 0; k < image->regions[r].size; k++) {
            h ^= image->regions[r].bytes[k];
            h *= 1099511628211ull;
        }
    return h;
}

static void record(Log *l, uint32_t target, int argc, uint64_t a, uint64_t b, uint64_t c)
{
    Call *call;
    if (l->n == 16) {
        l->overflow = 1;
        return;
    }
    call = &l->calls[l->n++];
    call->target = target;
    call->argc = argc;
    call->args[0] = a; call->args[1] = b; call->args[2] = c;
    call->memory = digest(l->image);
}

static void hook_prologue(void *ctx, uint32_t callee_va, int argument)
{
    record((Log *)ctx, callee_va, 1, (uint32_t)argument, 0, 0);
}

static void hook_dispatch(void *ctx, uint64_t unit, int event, int argument3)
{
    record((Log *)ctx, 0x003299B0u, 3, unit, (uint32_t)event, (uint32_t)argument3);
}

static int read_regions(const char *path, GroupImage *image)
{
    FILE *f = fopen(path, "rb");
    uint32_t count, i;
    if (!f)
        return 0;
    if (fread(&count, 4, 1, f) != 1 || count == 0 || count > 64) {
        fclose(f);
        return 0;
    }
    image->regions = (GroupImageRegion *)calloc(count, sizeof(GroupImageRegion));
    if (!image->regions) { fclose(f); return 0; }
    image->count = count;
    for (i = 0; i < count; i++) {
        uint64_t va;
        uint32_t size;
        if (fread(&va, 8, 1, f) != 1 || fread(&size, 4, 1, f) != 1) {
            fclose(f);
            return 0;
        }
        image->regions[i].va = va;
        image->regions[i].size = size;
        image->regions[i].bytes = (uint8_t *)malloc(size ? size : 1);
        if (!image->regions[i].bytes) { fclose(f); return 0; }
        if (size && fread(image->regions[i].bytes, 1, size, f) != size) {
            fclose(f);
            return 0;
        }
    }
    fclose(f);
    return 1;
}

int main(int argc, char **argv)
{
    GroupImage image;
    GroupCompletionHooks hooks;
    Log log;
    FILE *f;
    char line[64];
    unsigned case_index = 0;

    if (argc != 3 && argc != 4) {
        fprintf(stderr, "usage: %s <regions.bin> <cases.txt> [post.bin]\n", argv[0]);
        return 2;
    }
    if (!read_regions(argv[1], &image)) {
        fprintf(stderr, "cannot read regions %s\n", argv[1]);
        return 2;
    }
    f = fopen(argv[2], "r");
    if (!f) {
        fprintf(stderr, "cannot read cases %s\n", argv[2]);
        return 2;
    }

    hooks.on_complete_prologue = hook_prologue;
    hooks.dispatch = hook_dispatch;
    hooks.ctx = &log;
    puts("SCHEMA GROUP_COMPLETION_V2");

    while (fgets(line, sizeof line, f)) {
        uint64_t unit;
        int r, i;
        char extra;
        if (sscanf(line, "%llx %c", (unsigned long long *)&unit, &extra) != 1)
            return 2;
        memset(&log, 0, sizeof log);
        log.image = &image;
        r = GroupCompletion_RecordDeath(&image, unit, &hooks);
        if (log.overflow) { fprintf(stderr, "callback log overflow\n"); return 2; }
        printf("{\"case\":%u,\"unit\":%llu,\"return\":%d,\"calls\":[", case_index++,
               (unsigned long long)unit, r);
        for (i = 0; i < log.n; i++) {
            int j;
            Call *c = &log.calls[i];
            printf("%s{\"target\":%u,\"args\":[", i ? "," : "", c->target);
            for (j = 0; j < c->argc; j++)
                printf("%s%llu", j ? "," : "", (unsigned long long)c->args[j]);
            printf("],\"memory\":\"%016llX\"}", (unsigned long long)c->memory);
        }
        printf("],\"memory\":\"%016llX\"}\n", (unsigned long long)digest(&image));
    }
    fclose(f);

    {
        printf("DIGEST %016llX\n", (unsigned long long)digest(&image));
    }

    if (argc == 4) {
        FILE *o = fopen(argv[3], "wb");
        if (!o) return 2;
        {
            size_t r;
            for (r = 0; r < image.count; r++)
                if (fwrite(image.regions[r].bytes, 1, image.regions[r].size, o) != image.regions[r].size)
                    return 2;
            if (fclose(o)) return 2;
        }
    }
    return 0;
}
