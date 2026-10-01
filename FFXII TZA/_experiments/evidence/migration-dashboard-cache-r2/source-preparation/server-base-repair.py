"""server.py - the FF12 database dashboard: read-only, loopback-only (OPUS, 2026-09-29; migration M3).

    python server.py --root <dashboard generation root> [--port 8765]

Serves ONLY the CURRENT generation of a `gfz-scripts/generation.py` store; every view is an output `view-<name>.json`
written by an adapter (see VIEW-SCHEMA.md). It never scans a live source and makes no model call.

  GET /                 the page (vanilla HTML/JS below; polls /api/status every 5 s - a file read, not a scan)
  GET /api/status       generation id, commit time, verification problems, source drift (STALE), last failure,
                        and each required/present view's status
  GET /api/view/<name>  the view as served: {"meta": {...}, "view": {...}} or a status-only record
  anything else         405 (non-GET) / 404

Refusals, not silence:
  - the store's CURRENT fails verification (tampered output, manifest or membership) -> every view is INVALID and no
    data is served; the problems are shown
  - a required view absent from the generation -> UNMEASURED
  - a view whose measures lack numerator / denominator / scope / instrument / as_of / limits, or numerator > denominator
    -> MALFORMED, no numbers from it
Verification runs once per CURRENT pointer content (cached by the pointer's bytes), not per request.
"""
import argparse, datetime, hashlib, http.server, json, os, re, socketserver, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "analysis-kit", "gfz-scripts"))
import generation as G  # noqa: E402

_SERVER_SHA = G.sha256_file(os.path.abspath(__file__))


def reader_stale():
    """True when generation.py or this server file changed on disk since this process loaded them: the running
    reader's verdicts may not follow the current contract, so it must be restarted (2026-09-29 incident)."""
    return G.reader_stale() or G.sha256_file(os.path.abspath(__file__)) != _SERVER_SHA

# 2026-09-29, ASTRA REJECT (cccd7c04c): a stat-only cache key let a same-length, same-mtime edit escape re-verification,
# so /api/status reported no problems over bytes it had not checked. Now the served manifest and outputs are hashed
# against the manifest on EVERY request (under 2 MB), and the input snapshots are re-verified in full at least every
# VERIFY_INPUTS_EVERY seconds. Status states that scope and the time of the last full verification.
VERIFY_INPUTS_EVERY = 60
VERIFICATION = ("served manifest and outputs hashed against the manifest on every request; input snapshots re-verified "
                "in full at least every %d s (verified_at)" % VERIFY_INPUTS_EVERY)

REQUIRED = ("progress", "overview", "systems", "vbf", "executable", "types", "evidence", "fleet")
MEASURE_KEYS = ("numerator", "denominator", "scope", "instrument", "as_of", "limits")
STATUSES = ("OK", "STALE", "UNMEASURED", "FAILED", "PARTIAL")
NAME = re.compile(r"^[a-z0-9-]{1,40}$")


MEANINGS = os.path.join(HERE, "..", "..", "FFXII TZA", "_index", "workflow", "DASHBOARD-MEANINGS.md")
PACKAGES = os.path.join(HERE, "..", "..", "FFXII TZA", "_index", "completion-packages", "README.md")


def load_vocabulary(meanings=MEANINGS, packages=PACKAGES):
    """FABLE's state vocabulary (DASHBOARD-MEANINGS.md sections 1 and 2) plus the package stages (completion-packages
    README section 2), plus FAILED and STALE. None when either file cannot be read or yields nothing - then any view
    that carries node states is MALFORMED (fail closed: an unverifiable state is not shown as if it were checked)."""
    try:
        t = open(meanings, encoding="utf-8").read(); p = open(packages, encoding="utf-8").read()
        s1, s2 = t[t.index("## 1."):t.index("## 2.")], t[t.index("## 2."):t.index("## 3.")]
        st = p[p.index("## 2."):p.index("## 3.")]
    except (OSError, ValueError):
        return None
    vocab = set()
    for line in s1.splitlines():
        c = line.split("|")
        if len(c) > 3 and c[1].strip().startswith("**"):
            vocab |= set(re.findall(r"`([A-Za-z:*-]+)`", c[2]))
    for line in s2.splitlines():
        c = line.split("|")
        if len(c) > 3:
            vocab |= set(re.findall(r"`([A-Z][A-Za-z-]+)`", c[1]))
    stages = set(re.findall(r"^\|\s*`([a-z-]+)`", st, re.M))
    if not vocab or not stages:
        return None
    return vocab | stages | {"FAILED", "STALE"}


def _states(nodes):
    for n in nodes or []:
        if "state" in n:
            yield n.get("id"), n["state"]
        yield from _states(n.get("children"))


def check_view(v, vocab=None):
    """None, or why the view is MALFORMED."""
    if not isinstance(v, dict) or not isinstance(v.get("view"), str):
        return "not a view object"
    if v.get("status") not in STATUSES:
        return "status %r not one of %s" % (v.get("status"), STATUSES)
    for m in v.get("measures", []):
        miss = [k for k in MEASURE_KEYS if k not in m]
        if miss:
            return "measure %r lacks %s" % (m.get("id"), miss)
        n, d = m["numerator"], m["denominator"]
        if not isinstance(n, (int, float)) or (d is not None and not isinstance(d, (int, float))):
            return "measure %r: numerator/denominator not numbers" % m.get("id")
        if d is not None and (d < 0 or n > d):
            return "measure %r: numerator %s exceeds denominator %s" % (m.get("id"), n, d)
    if v["view"] == "progress":
        why = check_progress(v)
        if why:
            return why
    states = list(_states(v.get("tree")))
    if states:
        if vocab is None:
            return "node states present but the state vocabulary (DASHBOARD-MEANINGS.md) could not be read"
        bad = [(i, x) for i, x in states if x not in vocab]
        if bad:
            return "node state(s) outside DASHBOARD-MEANINGS.md's vocabulary: %s" % bad[:3]
    return None


def check_progress(v):
    """My Progress may show only numbers the measures carry: the headline scopes and every category row must equal
    their validated measures, and DATABASE READY needs every scope complete and all terminal passes accepted."""
    p = v.get("progress")
    if not isinstance(p, dict) or not p.get("version"):
        return "progress view without its versioned progress block"
    ms = {m["id"]: m for m in v.get("measures", [])}
    for k in ("union", "L1", "L2"):
        s, m = (p.get("scopes") or {}).get(k), ms.get(k)
        if not s or not m or (s["accepted"], s["total"]) != (m["numerator"], m["denominator"]):
            return "progress scope %s disagrees with its measure" % k
    for c in p.get("categories", []):
        m = ms.get("cat-" + c.get("code", ""))
        if not m or (c["accepted"], c["total"]) != (m["numerator"], m["denominator"]):
            return "progress category %s disagrees with its measure" % c.get("code")
    rs = (p.get("reconstruction") or {}).get("state", "")
    if rs.startswith("DATABASE READY"):
        t = p.get("terminal") or {}
        if (not p.get("measured") or any(p["scopes"][k]["accepted"] != p["scopes"][k]["total"] for k in ("union", "L1", "L2"))
                or t.get("accepted") != t.get("required")):
            return "DATABASE READY claimed while requirements remain or a family is unmeasured"
    return None


class State:
    def __init__(self, root):
        self.store, self.lock, self.key, self.cache = G.Store(root), threading.Lock(), None, None
        self.full_at, self.verified_at = 0.0, None
        self.vocab = load_vocabulary()

    def _stats(self, gen):
        out = []
        for dp, _, fs in os.walk(os.path.join(self.store.root, gen or "")):
            for f in fs:
                q = os.path.join(dp, f); st = os.stat(q); out.append((q, st.st_size, st.st_mtime_ns))
        return sorted(out)

    def _key(self):
        """The pointer's bytes, (name, size, mtime) of every file in the CURRENT generation and in the generation being
        served as a fallback, and the history log's stat: any change forces re-verification. A stat, not a hash."""
        p = os.path.join(self.store.root, G.CURRENT)
        if not os.path.exists(p):
            return b""
        ptr = open(p, "rb").read()
        try:
            gen = json.loads(ptr).get("generation") or ""
        except ValueError:
            return ptr
        hp = os.path.join(self.store.root, G.HISTORY)
        hist = os.stat(hp).st_mtime_ns if os.path.exists(hp) else 0
        fb = (self.cache or {}).get("serve_gen") if (self.cache or {}).get("historical") else None
        return ptr + repr((self._stats(gen), self._stats(fb) if fb else [], hist)).encode()

    def _last_verified(self, exclude, limit=20):
        """The newest generation in history.jsonl, other than `exclude`, that passes open_generation with its recorded
        manifest hash - or None. Never a rejected candidate: rejected ones are not in the success history."""
        hp = os.path.join(self.store.root, G.HISTORY)
        if not os.path.exists(hp):
            return None
        rows = [json.loads(l) for l in open(hp, encoding="utf-8") if l.strip()]
        for r in reversed(rows[-limit:]):
            if r.get("generation") == exclude:
                continue
            m, d, probs = self.store.open_generation(r.get("generation"), r.get("manifest_sha256"))
            if not probs:
                return m, d
        return None

    def _content_ok(self):
        """The served generation's manifest and outputs still hash to what was verified. Cheap; every request."""
        c = self.cache or {}
        sm, sd = c.get("serve_man"), c.get("serve_dir")
        if not sm:
            return True
        try:
            if hashlib.sha256(open(os.path.join(sd, G.MANIFEST), "rb").read()).hexdigest() != c.get("serve_manifest_sha"):
                return False
            return all(G.sha256_file(os.path.join(sd, "outputs", o)) == sm["outputs"][o]["sha256"] for o in sm["outputs"])
        except OSError:
            return False

    def snapshot(self):
        key = self._key()
        with self.lock:
            due = time.monotonic() - self.full_at >= VERIFY_INPUTS_EVERY
            if key != self.key or self.cache is None or due or not self._content_ok():
                man, d, probs = self.store.open_current()
                sm, sd, hist = (man, d, False) if not probs else (None, None, False)
                if probs:
                    fb = self._last_verified((man or {}).get("generation"))
                    if fb:
                        sm, sd, hist = fb[0], fb[1], True
                views = {}
                if sm:
                    for o in sm["outputs"]:
                        m = re.match(r"^view-([a-z0-9-]+)\.json$", o)
                        if m:
                            try:
                                v = json.load(open(os.path.join(sd, "outputs", o), encoding="utf-8"))
                                why = check_view(v, self.vocab)
                            except ValueError as e:
                                v, why = None, "not JSON: %s" % e
                            views[m.group(1)] = {"view": v, "malformed": why}
                msha = None
                if sd:
                    msha = hashlib.sha256(open(os.path.join(sd, G.MANIFEST), "rb").read()).hexdigest()
                self.cache = {"man": man, "problems": probs, "serve_man": sm, "serve_dir": sd, "serve_gen": (sm or {}).get("generation"),
                              "historical": hist, "views": views, "serve_manifest_sha": msha}
                self.key = self._key()
                self.full_at = time.monotonic()
                self.verified_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            c = dict(self.cache)
        c["drift"] = self.store.drift(c["serve_man"]) if c["serve_man"] else {}
        fp = os.path.join(self.store.root, G.FAILURE)
        c["failure"] = json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else None
        if c["failure"]:
            ref = (c["man"] or {}).get("committed_at")
            c["failure"]["resolved"] = bool(ref and c["failure"].get("failed_at", "") < ref and not c["problems"])
        c["reader_stale"] = reader_stale()
        return c

    def status(self):
        c = self.snapshot()
        names = list(REQUIRED) + sorted(n for n in c["views"] if n not in REQUIRED)
        sm = c["serve_man"] or {}
        vol = {n for n, i in (sm.get("inputs") or {}).items() if i.get("volatile")}
        strict = {k: v for k, v in c["drift"].items() if k not in vol}     # a volatile input moving is expected; shown, not STALE
        bad = "UNSUPPORTED" if any(p.startswith("UNSUPPORTED") for p in c["problems"]) else "INVALID"
        vs = {}
        for n in names:
            if not c["serve_man"]:
                vs[n] = bad
            elif n not in c["views"]:
                vs[n] = "UNMEASURED"
            elif c["views"][n]["malformed"]:
                vs[n] = "MALFORMED"
            elif c["historical"]:
                vs[n] = "HISTORICAL"
            else:
                vs[n] = "STALE" if strict else c["views"][n]["view"]["status"]
        cur = c["man"] or {}
        return {"generation": sm.get("generation"), "committed_at": sm.get("committed_at"), "historical": c["historical"],
                "current": {"generation": cur.get("generation"), "committed_at": cur.get("committed_at"), "problems": c["problems"]},
                "problems": c["problems"], "no_verified_generation": not c["serve_man"],
                "drift": strict, "volatile_drift": {k: v for k, v in c["drift"].items() if k in vol},
                "failure": c["failure"], "reader_stale": c["reader_stale"], "views": vs, "required": list(REQUIRED),
                "verified_at": self.verified_at, "verification": VERIFICATION}

    def view(self, name):
        c = self.snapshot()
        sm = c["serve_man"] or {}
        meta = {"generation": sm.get("generation"), "committed_at": sm.get("committed_at"), "drift": c["drift"],
                "historical": c["historical"], "current_problems": c["problems"]}
        if not c["serve_man"]:
            bad = "UNSUPPORTED" if any(p.startswith("UNSUPPORTED") for p in c["problems"]) else "INVALID"
            return dict(meta, status=bad, problems=c["problems"], why="no verified generation is available")
        if name not in c["views"]:
            return dict(meta, status="UNMEASURED", why="no view-%s.json in the served generation" % name)
        if c["views"][name]["malformed"]:
            return dict(meta, status="MALFORMED", why=c["views"][name]["malformed"])
        return {"meta": meta, "view": c["views"][name]["view"]}


def make_handler(state):
    class H(http.server.BaseHTTPRequestHandler):
        server_version = "ff12-dashboard/1"

        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype="application/json"):
            b = body if isinstance(body, bytes) else json.dumps(body).encode()
            self.send_response(code); self.send_header("Content-Type", ctype + "; charset=utf-8")
            self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(b))); self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            try:
                if path == "/":
                    return self._send(200, PAGE.encode(), "text/html")
                if path == "/api/status":
                    return self._send(200, state.status())
                m = re.match(r"^/api/view/([^/]+)$", path)
                if m and NAME.match(m.group(1)):
                    return self._send(200, state.view(m.group(1)))
                return self._send(404, {"error": "not found"})
            except Exception as e:   # a broken source is reported, never served as empty
                return self._send(500, {"status": "FAILED", "error": "%s: %s" % (type(e).__name__, e)})

        def _refuse(self):
            self._send(405, {"error": "read-only dashboard"})
        do_POST = do_PUT = do_DELETE = do_PATCH = _refuse
    return H


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def serve(root, port=8765):
    """Bind 127.0.0.1 only; broader exposure needs the user's permission and is not offered here."""
    return Server(("127.0.0.1", port), make_handler(State(root)))


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FF12 database dashboard</title><style>
:root{--bg:#fff;--fg:#1d1d1f;--mut:#666;--line:#ddd;--soft:#f3f4f6;--ok:#1a7f37;--warn:#9a6700;--bad:#cf222e;--unk:#6e7781;--bar:#2f81f7}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--mut:#9da7b3;--line:#30363d;--soft:#161b22;--ok:#3fb950;--warn:#d29922;--bad:#f85149;--unk:#8b949e;--bar:#58a6ff}}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif}header{padding:12px 16px;border-bottom:1px solid var(--line)}
nav{display:flex;flex-wrap:wrap;gap:4px;padding:8px 16px;border-bottom:1px solid var(--line)}nav button{border:1px solid var(--line);background:none;color:var(--fg);padding:4px 10px;border-radius:6px;cursor:pointer}
nav button.on{border-color:var(--fg)}main{padding:12px 16px;overflow-x:auto}.st{font-weight:600}.OK{color:var(--ok)}.STALE,.PARTIAL{color:var(--warn)}
.INVALID,.FAILED,.MALFORMED,.UNSUPPORTED{color:var(--bad)}.HISTORICAL{color:var(--warn)}.UNMEASURED{color:var(--unk)}table{border-collapse:collapse;margin:8px 0}td,th{border:1px solid var(--line);padding:3px 8px;text-align:left;vertical-align:top}
.mut{color:var(--mut)}ul{margin:2px 0 2px 18px;padding:0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:8px 0 14px}.card{border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.card h3{margin:0 0 4px;font-size:13px;font-weight:600}.big{font-size:22px;font-weight:650}.bar{height:7px;background:var(--soft);border:1px solid var(--line);border-radius:4px;overflow:hidden;margin:6px 0 2px}
.bar>i{display:block;height:100%;background:var(--bar)}.cat td.n{text-align:right;white-space:nowrap}tr.cat{cursor:pointer}tr.cat:hover{background:var(--soft)}tr.drill>td{background:var(--soft)}
details>summary{cursor:pointer}.pbar{display:inline-block;width:80px;height:6px;background:var(--soft);border:1px solid var(--line);border-radius:3px;vertical-align:middle;margin-right:6px;overflow:hidden}.pbar>i{display:block;height:100%;background:var(--bar)}
.addr{font-family:ui-monospace,monospace;font-size:12px;word-break:break-all}</style></head><body>
<header><b>FF12 database dashboard</b> <span class="mut">read-only; serves the verified CURRENT generation only</span><div id="gen" class="mut"></div></header>
<nav id="tabs"></nav><main id="main"></main><script>
let cur="progress",lastStatus=null,openCat={};const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const LABEL={progress:"My Progress"};
function pct(m){return (m.denominator? (100*m.numerator/m.denominator).toFixed(1)+"% ":"")+esc(m.numerator)+(m.denominator!=null?" / "+esc(m.denominator):"")}
function pc(n,d){if(!d)return null;let a=Math.floor(n*1000/d)/10;if(n<d&&a>=100)a=99.9;return {a:a.toFixed(1),r:(n<d?(100-a).toFixed(1):"0.0"),w:Math.min(100,a)}}
function tree(ns){return "<ul>"+ns.map(n=>"<li>"+esc(n.label)+(n.state?" <span class='st "+esc(n.state)+"'>"+esc(n.state)+"</span>":"")+
 (n.counts?" <span class=mut>"+Object.entries(n.counts).map(([k,v])=>esc(k)+" "+esc(v)).join(", ")+"</span>":"")+
 (n.links||[]).map(l=>" <a href='#' title='"+esc(l.href)+"'>"+esc(l.label)+"</a>").join("")+(n.children&&n.children.length?tree(n.children):"")+"</li>").join("")+"</ul>"}
function card(title,s,unit,extra){const p=pc(s.accepted,s.total);if(!p)return "<div class=card><h3>"+esc(title)+"</h3><div class='big UNMEASURED'>UNMEASURED</div></div>";
 return "<div class=card title='"+esc(s.accepted+" of "+s.total+" requirements accepted; "+(s.total-s.accepted)+" remaining. "+unit)+"'><h3>"+esc(title)+"</h3><div class=big>"+p.a+"%</div>"+
 "<div class=bar><i style='width:"+p.w+"%'></i></div><div class=mut>"+p.a+"% accepted &middot; "+p.r+"% remaining</div><div class=mut>"+esc(s.accepted)+" / "+esc(s.total)+(extra||"")+"</div></div>"}
function chg(c,p){if(!c)return "<span class=mut>"+esc(p.change&&!p.change.comparable?p.change.why:"no prior checkpoint yet")+"</span>";if(c.new)return "new";
 const s=v=>(v>0?"+":"")+v;let t=s(c.accepted)+" accepted";if(c.scope)t+=" &middot; scope "+s(c.scope);return t+" <span class=mut>("+s(c.pct.toFixed(2))+" pts)</span>"}
function fam(p,f){return (p.families[f]||{}).label||f}
function drill(c,p){let h="";const byf={};c.items.forEach(i=>(byf[i.f]=byf[i.f]||[]).push(i));
 if(!c.items.length&&!c.functions.length)return "<p class=mut>Nothing remains in this category.</p>";
 h+="<p class=mut>remaining here: "+Object.entries(c.remaining_by_family).map(([f,n])=>esc(n)+" "+esc(fam(p,f))).join("; ")+"</p>";
 for(const [f,xs] of Object.entries(byf)){h+="<details"+(xs.length<=25?" open":"")+"><summary><b>"+esc(fam(p,f))+"</b> - "+xs.length+"</summary><table><tr><th>requirement</th><th>state</th><th>owner</th><th>next action</th><th>evidence</th></tr>"+
  xs.map(i=>"<tr><td>"+esc(i.k)+"</td><td>"+esc(i.st)+"</td><td>"+esc(i.o||"unassigned")+"</td><td>"+esc(i.n)+"</td><td>"+esc(i.e)+"</td></tr>").join("")+"</table></details>"}
 if(c.functions.length){h+="<details><summary><b>"+esc(fam(p,"F"))+"</b> - "+c.functions.reduce((a,g)=>a+g[1],0)+" functions, by state and owner/domain</summary>"+
  "<p class=mut>next action: explain each on a page, or declare it in a B/C family (check_dispositions.py); evidence: functions.tsv</p>"+
  c.functions.map(g=>"<details><summary>"+esc(g[0])+" - "+g[1]+"</summary><div class=addr>"+esc(g[2])+"</div></details>").join("")+"</details>"}
 return h}
function renderProgress(r){const v=r.view,p=v.progress,m=document.getElementById("main"),st=(lastStatus&&lastStatus.views&&lastStatus.views.progress)||v.status;
 let h="<h2>My Progress <span class='st "+esc(st)+"'>"+esc(st)+"</span></h2><p class=mut>generation "+esc(r.meta.generation)+", last update "+esc(r.meta.committed_at)+
  " &middot; freshness <span class='st "+esc(st)+"'>"+esc(st)+"</span>"+(r.meta.historical?" (HISTORICAL: the last verified generation, not CURRENT)":"")+" &middot; metric "+esc(p.version)+"</p>";
 const u=p.unit,T=p.terminal||{},R=p.reconstruction||{};
 h+="<div class=cards>"+(p.measured?card("Database L1+L2",p.scopes.union,u):"<div class=card><h3>Database L1+L2</h3><div class='big UNMEASURED'>UNMEASURED</div><div class=mut>known requirements only: "+
   esc(p.scopes.union.accepted)+" / "+esc(p.scopes.union.total)+"; unmeasured: "+esc(Object.keys(p.failed).join(", "))+"</div></div>")+
  card("L1 (modding grade)",p.scopes.L1,u)+card("L2 (reconstruction grade)",p.scopes.L2,u)+
  "<div class=card title='"+esc("Thirty consecutive clean passes of FINAL-AUDIT-PROTOCOL, counted from the governing gate. They run only after everything else is accepted.")+"'><h3>Final certification</h3><div class=big>"+esc(T.accepted??"?")+" / "+esc(T.required)+"</div><div class=mut>accepted terminal passes / required</div></div>"+
  "<div class=card title='"+esc(R.why||"")+"'><h3>Reconstruction status</h3><div class='big "+(R.state==="NOT READY"?"UNMEASURED":"OK")+"' style='font-size:16px'>"+esc(R.state)+"</div><div class=mut>"+esc(R.why||"")+"</div></div></div>";
 h+="<details><summary>How these numbers are counted</summary><p>"+esc(u)+"</p><p class=mut>Combined L1+L2 is the deduplicated union: a shared requirement counts once. "+
  "Accepted % rounds down and remaining % rounds up, so 100% is never shown while anything remains. Change compares with the prior checkpoint "+
  "(the last verified generation before today, "+esc(p.change&&p.change.generation||"none yet")+"), with accepted work and scope changes kept apart. "+
  "Definitions: "+esc(p.definitions)+"; category map: "+esc(p.map)+".</p><table><tr><th>requirement family</th><th>accepted</th><th>remaining</th></tr>"+
  Object.entries(p.families).map(([k,f])=>"<tr><td>"+esc(f.label)+"</td><td>"+esc(f.accepted)+" / "+esc(f.total)+"</td><td>"+esc(f.total-f.accepted)+"</td></tr>").join("")+"</table>"+
  "<p class=mut>Not requirements (excluded, listed so none is silently dropped): "+esc(p.excluded.map(x=>x[0]+" ("+x[1]+")").join("; ")||"none")+"</p>"+
  (p.unplaced.length?"<p class=STALE>Mapping gap: "+p.unplaced.length+" requirement(s) not placed in a category: "+esc(p.unplaced.slice(0,30).join(", "))+"</p>":"")+"</details>";
 h+="<table class=cat><tr><th>Category</th><th title='accepted / total requirements placed in this category'>Accepted %</th><th>Remaining %</th><th title='"+esc("since "+(p.change&&p.change.committed_at||"no prior checkpoint"))+"'>Change since prior checkpoint</th></tr>";
 p.categories.forEach(c=>{if(!c.total&&c.code!=="untied")return;const q=pc(c.accepted,c.total)||{a:"-",r:"-",w:0};
  h+="<tr class=cat data-c='"+esc(c.code)+"' onclick='tog(this.dataset.c)' title='"+esc(c.accepted+" of "+c.total+" requirements; click for what remains")+"'><td>"+(openCat[c.code]?"&#9662; ":"&#9656; ")+esc(c.label)+
   "</td><td class=n><span class=pbar><i style='width:"+q.w+"%'></i></span>"+q.a+"%</td><td class=n>"+q.r+"%</td><td>"+chg(c.change,p)+"</td></tr>";
  if(openCat[c.code])h+="<tr class=drill><td colspan=4>"+drill(c,p)+"</td></tr>"});
 h+="</table>";m.innerHTML=h}
let lastView=null;function tog(c){openCat[c]=!openCat[c];if(lastView)renderProgress(lastView)}
async function show(name){cur=name;document.querySelectorAll("nav button").forEach(b=>b.classList.toggle("on",b.dataset.v==name));
 const r=await (await fetch("/api/view/"+name)).json();const m=document.getElementById("main");
 if(!r.view){m.innerHTML="<p class='st "+esc(r.status)+"'>"+esc(r.status)+"</p><p>"+esc(r.why||(r.problems||[]).join("; ")||r.error)+"</p>";return}
 if(r.view.view==="progress"&&r.view.progress){lastView=r;return renderProgress(r)}
 const v=r.view;let h="<h2>"+esc(v.title||v.view)+" <span class='st "+esc(v.status)+"'>"+esc(v.status)+"</span></h2>";
 h+="<p class=mut>source "+esc(JSON.stringify(v.source||{}))+"</p>";
 if(v.measures&&v.measures.length){h+="<table><tr><th>measure</th><th>value</th><th>scope</th><th>instrument</th><th>as of</th><th>limits</th></tr>"+
  v.measures.map(x=>"<tr><td>"+esc(x.label||x.id)+"</td><td>"+pct(x)+"</td><td>"+esc(x.scope)+"</td><td>"+esc(x.instrument)+"</td><td>"+esc(x.as_of)+"</td><td>"+esc(x.limits)+"</td></tr>").join("")+"</table>"}
 if(v.tree)h+=tree(v.tree);if(v.rows)h+="<table><tr>"+v.rows.columns.map(c=>"<th>"+esc(c)+"</th>").join("")+"</tr>"+v.rows.data.map(r=>"<tr>"+r.map(c=>"<td>"+esc(c)+"</td>").join("")+"</tr>").join("")+"</table>";
 m.innerHTML=h}
let lastGen=null;
async function poll(){try{const s=await (await fetch("/api/status")).json();lastStatus=s;
 if(lastGen!==null&&s.generation!==lastGen)show(cur);lastGen=s.generation;
 const cp=(s.current&&s.current.problems)||[];
 document.getElementById("gen").textContent=
  (s.reader_stale?"RESTART REQUIRED: the dashboard server's code changed on disk since it started; its verdicts may not follow the current contract | ":"")+
  (s.no_verified_generation?"NO VERIFIED GENERATION AVAILABLE - CURRENT "+(s.current.generation||"none")+" rejected: "+cp.join("; ")
   :(s.historical?"SHOWING LAST VERIFIED generation "+s.generation+" (committed "+s.committed_at+") - CURRENT "+s.current.generation+" was rejected: "+cp.join("; ")
     :"generation "+s.generation+" committed "+s.committed_at))+
  (Object.keys(s.drift).length?" | STALE: sources moved "+JSON.stringify(s.drift):"")+(Object.keys(s.volatile_drift||{}).length?" | since the snapshot: "+Object.keys(s.volatile_drift).join(", ")+" moved (live sources; next build picks it up)":"")+
  (s.failure?(s.failure.resolved?" | earlier failure, resolved by the current generation: ":" | LATEST BUILD FAILED ("+s.failure.failed_at+"): ")+s.failure.reason:"");
 document.getElementById("tabs").innerHTML=Object.entries(s.views).map(([k,st])=>"<button data-v='"+esc(k)+"' onclick='show(this.dataset.v)'>"+esc(LABEL[k]||k)+" <span class='st "+esc(st)+"'>"+esc(st)+"</span></button>").join("");
 document.querySelectorAll("nav button").forEach(b=>b.classList.toggle("on",b.dataset.v==cur))}catch(e){document.getElementById("gen").textContent="dashboard server unreachable: "+e}}
poll().then(()=>show(cur));setInterval(poll,5000);
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="read-only loopback dashboard over a generation store")
    ap.add_argument("--root", required=True); ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    srv = serve(a.root, a.port)
    print("dashboard: http://127.0.0.1:%d/  (root %s)" % (a.port, a.root), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
