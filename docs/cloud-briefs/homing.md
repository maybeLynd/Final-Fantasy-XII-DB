# Brief: homing drafts (stream H, FABLE)

You are a cloud session working for FABLE on the FF12 TZA knowledge database (this private repo, a text-only snapshot).
Read `docs/CLOUD_PROGRAM.md`, then `docs/cloud-briefs/f-interior.md` (its sentence and anchor rules apply here
unchanged), then this brief, then your pack(s) in `cloud-input/homing/`.

## The task

Each pack names one **host page** and a list of functions that **no page cites yet**. Each function is called directly
from a function the host page already cites. The pack gives, for each function:
- its call sites, written `<caller entry>` + 0xNN;
- a short excerpt of the host page around the caller;
- the function's annotated disassembly.

For every function, write:
- `entered_from`: one of the listed call sites, copied exactly as given (for example "`002CB8D0` + 0x49");
- `text`: one sentence on what the body does, under the f-interior rules (access and representation, not purpose; every
  path stated; every 8-hex-digit address must appear in the function's listing; no `|`; under 600 characters unless
  needed, hard limit 1,200);
- `anchors`: 1 to 5 interior anchors with their mnemonics, strictly inside the body, never the entry.

The host is fixed. Do not move a function to another page. If a function cannot be stated under the rules, skip it
with the reason.

**Two rules learned from earlier waves.** Neither is optional:
1. When the sentence mentions a call to a function the host page excerpt does not name, cite the call by its site
   (`<function entry>` + 0xNN, the call instruction's address minus the function's entry). Do not cite the callee's
   own address: that imports the callee's whole call graph into the page.
2. Never write the address of a jump table or other data that sits right after a function's code. Never write the image
   base as an 8-hex-digit number. Describe the cases instead.

## Output

Write `cloud-reports/homing/<slug>.json` (the pack's slug):

```json
{
 "page": "<the host page path the pack names, relative to FFXII TZA/>",
 "session": "<your session id if you know it>",
 "rows": [
  {"fn": "0029AE50", "entered_from": "`00297170` + 0x8C",
   "text": "bounds-checks `edx` against dword `+0x40` of qword `rcx+0xB50`, ...",
   "anchors": [["0029AE77", "cmp"]]}
 ],
 "skipped": [{"fn": "002F1CD0", "why": "its whole work is the entry instruction"}],
 "notes": "doubts per function, listings you could not read"
}
```

Re-read each sentence against the listing before you write it. FABLE re-reads every row against the real executable,
and a wrong sentence costs more than a skip.

## Git

Use the branch named in your task. Commit and push after **each** pack. Use the git author `maybeLynd` with an empty
email, and no Co-Authored-By trailer. Edit nothing outside `cloud-reports/`. Never push to `main`. When done, open a
pull request to `main` with the counts (rows, skipped, doubts) in its body.
