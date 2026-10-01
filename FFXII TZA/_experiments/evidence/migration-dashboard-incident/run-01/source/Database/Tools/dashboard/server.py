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
import argparse, http.server, json, os, re, socketserver, sys, threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "analysis-kit", "gfz-scripts"))
import generation as G  # noqa: E402

_SERVER_SHA = G.sha256_file(os.path.abspath(__file__))


def reader_stale():
    """True when generation.py or this server file changed on disk since this process loaded them: the running
    reader's verdicts may not follow the current contract, so it must be restarted (2026-09-29 incident)."""
    return G.reader_stale() or G.sha256_file(os.path.abspath(__file__)) != _SERVER_SHA

REQUIRED = ("overview", "systems", "vbf", "executable", "types", "evidence", "fleet")
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
    states = list(_states(v.get("tree")))
    if states:
        if vocab is None:
            return "node states present but the state vocabulary (DASHBOARD-MEANINGS.md) could not be read"
        bad = [(i, x) for i, x in states if x not in vocab]
        if bad:
            return "node state(s) outside DASHBOARD-MEANINGS.md's vocabulary: %s" % bad[:3]
    return None


class State:
    def __init__(self, root):
        self.store, self.lock, self.key, self.cache = G.Store(root), threading.Lock(), None, None
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

    def snapshot(self):
        key = self._key()
        with self.lock:
            if key != self.key or self.cache is None:
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
                self.cache = {"man": man, "problems": probs, "serve_man": sm, "serve_dir": sd, "serve_gen": (sm or {}).get("generation"),
                              "historical": hist, "views": views}
                self.key = self._key()
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
                "failure": c["failure"], "reader_stale": c["reader_stale"], "views": vs, "required": list(REQUIRED)}

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
:root{--bg:#fff;--fg:#1d1d1f;--mut:#666;--line:#ddd;--ok:#1a7f37;--warn:#9a6700;--bad:#cf222e;--unk:#6e7781}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--mut:#9da7b3;--line:#30363d;--ok:#3fb950;--warn:#d29922;--bad:#f85149;--unk:#8b949e}}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif}header{padding:12px 16px;border-bottom:1px solid var(--line)}
nav{display:flex;flex-wrap:wrap;gap:4px;padding:8px 16px;border-bottom:1px solid var(--line)}nav button{border:1px solid var(--line);background:none;color:var(--fg);padding:4px 10px;border-radius:6px;cursor:pointer}
nav button.on{border-color:var(--fg)}main{padding:12px 16px}.st{font-weight:600}.OK{color:var(--ok)}.STALE,.PARTIAL{color:var(--warn)}
.INVALID,.FAILED,.MALFORMED,.UNSUPPORTED{color:var(--bad)}.HISTORICAL{color:var(--warn)}.UNMEASURED{color:var(--unk)}table{border-collapse:collapse;margin:8px 0}td,th{border:1px solid var(--line);padding:3px 8px;text-align:left;vertical-align:top}
.mut{color:var(--mut)}ul{margin:2px 0 2px 18px;padding:0}</style></head><body>
<header><b>FF12 database dashboard</b> <span class="mut">read-only; serves the verified CURRENT generation only</span><div id="gen" class="mut"></div></header>
<nav id="tabs"></nav><main id="main"></main><script>
let cur="overview";const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function pct(m){return (m.denominator? (100*m.numerator/m.denominator).toFixed(1)+"% ":"")+esc(m.numerator)+(m.denominator!=null?" / "+esc(m.denominator):"")}
function tree(ns){return "<ul>"+ns.map(n=>"<li>"+esc(n.label)+(n.state?" <span class='st "+esc(n.state)+"'>"+esc(n.state)+"</span>":"")+
 (n.counts?" <span class=mut>"+Object.entries(n.counts).map(([k,v])=>esc(k)+" "+esc(v)).join(", ")+"</span>":"")+
 (n.links||[]).map(l=>" <a href='#' title='"+esc(l.href)+"'>"+esc(l.label)+"</a>").join("")+(n.children&&n.children.length?tree(n.children):"")+"</li>").join("")+"</ul>"}
async function show(name){cur=name;document.querySelectorAll("nav button").forEach(b=>b.classList.toggle("on",b.dataset.v==name));
 const r=await (await fetch("/api/view/"+name)).json();const m=document.getElementById("main");
 if(!r.view){m.innerHTML="<p class='st "+esc(r.status)+"'>"+esc(r.status)+"</p><p>"+esc(r.why||(r.problems||[]).join("; ")||r.error)+"</p>";return}
 const v=r.view;let h="<h2>"+esc(v.title||v.view)+" <span class='st "+esc(v.status)+"'>"+esc(v.status)+"</span></h2>";
 h+="<p class=mut>source "+esc(JSON.stringify(v.source||{}))+"</p>";
 if(v.measures&&v.measures.length){h+="<table><tr><th>measure</th><th>value</th><th>scope</th><th>instrument</th><th>as of</th><th>limits</th></tr>"+
  v.measures.map(x=>"<tr><td>"+esc(x.label||x.id)+"</td><td>"+pct(x)+"</td><td>"+esc(x.scope)+"</td><td>"+esc(x.instrument)+"</td><td>"+esc(x.as_of)+"</td><td>"+esc(x.limits)+"</td></tr>").join("")+"</table>"}
 if(v.tree)h+=tree(v.tree);if(v.rows)h+="<table><tr>"+v.rows.columns.map(c=>"<th>"+esc(c)+"</th>").join("")+"</tr>"+v.rows.data.map(r=>"<tr>"+r.map(c=>"<td>"+esc(c)+"</td>").join("")+"</tr>").join("")+"</table>";
 m.innerHTML=h}
let lastGen=null;
async function poll(){try{const s=await (await fetch("/api/status")).json();
 if(lastGen!==null&&s.generation!==lastGen)show(cur);lastGen=s.generation;
 const cp=(s.current&&s.current.problems)||[];
 document.getElementById("gen").textContent=
  (s.reader_stale?"RESTART REQUIRED: the dashboard server's code changed on disk since it started; its verdicts may not follow the current contract | ":"")+
  (s.no_verified_generation?"NO VERIFIED GENERATION AVAILABLE - CURRENT "+(s.current.generation||"none")+" rejected: "+cp.join("; ")
   :(s.historical?"SHOWING LAST VERIFIED generation "+s.generation+" (committed "+s.committed_at+") - CURRENT "+s.current.generation+" was rejected: "+cp.join("; ")
     :"generation "+s.generation+" committed "+s.committed_at))+
  (Object.keys(s.drift).length?" | STALE: sources moved "+JSON.stringify(s.drift):"")+(Object.keys(s.volatile_drift||{}).length?" | since the snapshot: "+Object.keys(s.volatile_drift).join(", ")+" moved (live sources; next build picks it up)":"")+
  (s.failure?(s.failure.resolved?" | earlier failure, resolved by the current generation: ":" | LATEST BUILD FAILED ("+s.failure.failed_at+"): ")+s.failure.reason:"");
 document.getElementById("tabs").innerHTML=Object.entries(s.views).map(([k,st])=>"<button data-v='"+esc(k)+"' onclick='show(this.dataset.v)'>"+esc(k)+" <span class='st "+esc(st)+"'>"+esc(st)+"</span></button>").join("");
 document.querySelectorAll("nav button").forEach(b=>b.classList.toggle("on",b.dataset.v==cur))}catch(e){document.getElementById("gen").textContent="dashboard server unreachable: "+e}}
poll();show(cur);setInterval(poll,5000);
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
