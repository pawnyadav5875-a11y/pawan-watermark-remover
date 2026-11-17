import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

app = FastAPI(title="Pawan Studio - Pro Video Watermark Remover", docs_url=None, redoc_url=None)


@app.middleware("http")
async def isolation_headers(request: Request, call_next):
    response = await call_next(request)
    # Required for SharedArrayBuffer (FFmpeg.wasm) to work in Chrome & Android
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "ok"


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(PAGE)


PAGE = r"""<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Pawan Studio | Pro Video Watermark Remover (Free & Unlimited)</title>
<meta name="description" content="Remove watermarks from any length video 100% free in your browser. No upload, HD quality, instant MP4 download.">
<style>
:root{
  --bg:#070b14; --card:#101726; --card2:#162035; --line:#24314d;
  --txt:#f1f5f9; --mut:#94a3b8; --acc:#f43f5e; --pri:#6366f1; --ok:#10b981;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{
  margin:0; background:radial-gradient(1000px 500px at 50% -10%, #1e1b4b 0%, var(--bg) 65%);
  color:var(--txt); font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans Devanagari",sans-serif;
  min-height:100vh; line-height:1.5;
}
.nav{
  border-bottom:1px solid var(--line); background:rgba(16,23,38,0.85);
  backdrop-filter:blur(10px); padding:12px 16px; position:sticky; top:0; z-index:50;
}
.nav-in{max-width:920px; margin:0 auto; display:flex; align-items:center; justify-content:space-between}
.brand{font-weight:800; font-size:1.15rem; display:flex; align-items:center; gap:8px; letter-spacing:-0.3px}
.badge{background:rgba(99,102,241,0.18); color:#a5b4fc; border:1px solid rgba(99,102,241,0.4); font-size:0.72rem; padding:3px 8px; border-radius:99px; font-weight:700}
.wrap{max-width:920px; margin:0 auto; padding:18px 14px 70px}
.hero{text-align:center; padding:10px 0 18px}
.hero h1{font-size:1.55rem; margin:0 0 6px; background:linear-gradient(90deg,#fff,#a5b4fc); -webkit-background-clip:text; -webkit-text-fill-color:transparent}
.hero p{color:var(--mut); font-size:0.9rem; margin:0}
.pills{display:flex; flex-wrap:wrap; justify-content:center; gap:8px; margin-top:12px}
.pill{background:var(--card); border:1px solid var(--line); padding:5px 11px; border-radius:99px; font-size:0.78rem; color:#cbd5e1}

.card{background:var(--card); border:1px solid var(--line); border-radius:16px; padding:16px; margin-bottom:16px; box-shadow:0 8px 30px rgba(0,0,0,0.35)}
.sec-title{font-size:0.92rem; font-weight:700; color:#e2e8f0; margin-bottom:10px; display:flex; align-items:center; justify-content:space-between}

.upload-zone{
  border:2px dashed #334155; border-radius:14px; padding:26px 16px; text-align:center;
  background:rgba(22,32,53,0.5); cursor:pointer; display:block; transition:all 0.2s;
}
.upload-zone:hover{border-color:var(--pri); background:rgba(99,102,241,0.08)}
.upload-icon{font-size:2rem; margin-bottom:6px; display:block}
.btn{
  display:inline-flex; align-items:center; justify-content:center; gap:8px; border:0; border-radius:12px;
  padding:14px 20px; font-size:1rem; font-weight:700; color:#fff;
  background:linear-gradient(135deg,var(--pri),#8b5cf6); cursor:pointer; width:100%; transition:transform 0.1s;
}
.btn:active{transform:scale(0.99)}
.btn.red{background:linear-gradient(135deg,#e11d48,#f97316)}
.btn.green{background:linear-gradient(135deg,#059669,#10b981)}
.btn:disabled{opacity:0.5; cursor:not-allowed}
input[type=file]{display:none}

.stage{position:relative; width:100%; background:#000; border-radius:12px; overflow:hidden; line-height:0; user-select:none; border:1px solid var(--line)}
.stage video{width:100%; display:block; max-height:68vh; background:#000}
.ov{position:absolute; inset:0; touch-action:none; pointer-events:none}
.box{
  position:absolute; border:2px solid var(--acc); background:rgba(244,63,94,0.25);
  touch-action:none; cursor:move; box-shadow:0 0 0 9999px rgba(0,0,0,0.38); pointer-events:auto;
}
.hd{position:absolute; width:24px; height:24px; background:var(--acc); border:2px solid #fff; border-radius:50%; touch-action:none}
.hd[data-h=nw]{left:-12px; top:-12px; cursor:nwse-resize}
.hd[data-h=ne]{right:-12px; top:-12px; cursor:nesw-resize}
.hd[data-h=sw]{left:-12px; bottom:-12px; cursor:nesw-resize}
.hd[data-h=se]{right:-12px; bottom:-12px; cursor:nwse-resize}

.presets{display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-top:12px}
@media(max-width:520px){.presets{grid-template-columns:repeat(2,1fr)}}
.pbtn{
  background:var(--card2); border:1px solid var(--line); color:#e2e8f0; padding:8px 10px;
  border-radius:10px; font-size:0.8rem; font-weight:600; cursor:pointer;
}
.pbtn:hover{border-color:var(--pri)}

.grid{display:grid; grid-template-columns:1fr 1fr; gap:12px 18px}
@media(max-width:520px){.grid{grid-template-columns:1fr}}
label.l{display:flex; justify-content:space-between; font-size:0.84rem; color:var(--mut); margin-bottom:2px}
label.l b{color:var(--txt)}
input[type=range]{width:100%; accent-color:var(--acc); height:26px}

.modes{display:grid; grid-template-columns:1fr 1fr; gap:10px}
.mode{border:1px solid var(--line); border-radius:12px; padding:11px; cursor:pointer; font-size:0.88rem; background:var(--card2); display:block}
.mode input{margin-right:6px; accent-color:var(--acc)}
.mode.sel{border-color:var(--pri); background:rgba(99,102,241,0.15)}
.mode small{display:block; color:var(--mut); margin-top:3px; font-size:0.78rem}

.bar{height:14px; background:#070b14; border-radius:99px; overflow:hidden; border:1px solid var(--line)}
.bar>i{display:block; height:100%; width:0; background:linear-gradient(90deg,var(--pri),var(--ok)); transition:width 0.2s}
.msg{font-size:0.86rem; margin-top:8px; color:var(--mut); word-break:break-word}
.err{color:#fda4af; background:#2e1018; border:1px solid #881337; padding:11px; border-radius:10px; margin-top:10px; font-size:0.88rem}
.warn{color:#fde68a; background:#29200e; border:1px solid #78350f; padding:11px; border-radius:10px; margin-bottom:14px; font-size:0.86rem}
.hide{display:none}
.row{display:flex; gap:12px; align-items:center; margin-top:14px}
.compare{margin-top:14px; border-top:1px solid var(--line); padding-top:14px}
.compare video{width:100%; border-radius:12px; border:1px solid var(--ok); max-height:60vh; background:#000}
.footer{text-align:center; color:#64748b; font-size:0.8rem; margin-top:30px}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-in">
    <div class="brand">🎬 Pawan Studio <span class="badge">PRO 100% FREE</span></div>
    <div style="font-size:0.8rem; color:var(--mut)">No Upload • Unlimited</div>
  </div>
</nav>

<div class="wrap">
  <div class="hero">
    <h1>AI Video Watermark Remover</h1>
    <p>किसी भी लंबाई (Unlimited Length) के वीडियो से वॉटरमार्क हटाएं — 100% सुरक्षित और मुफ़्त</p>
    <div class="pills">
      <span class="pill">⚡ 100% Browser Processing</span>
      <span class="pill">🎞️ Any Video Length</span>
      <span class="pill">🔊 Original Audio Safe</span>
      <span class="pill">📱 Mobile & PC Ready</span>
    </div>
  </div>

  <div id="isoWarn" class="warn hide"></div>

  <div class="card">
    <label class="upload-zone" for="file">
      <span class="upload-icon">📁</span>
      <strong style="font-size:1.05rem; color:#fff">वीडियो चुनें / Select Video File</strong>
      <div style="color:var(--mut); font-size:0.82rem; margin-top:4px">MP4, MOV, MKV, WEBM (आपका वीडियो कहीं अपलोड नहीं होता)</div>
    </label>
    <input id="file" type="file" accept="video/*">
    <div id="fname" class="msg" style="text-align:center; color:#a5b4fc; font-weight:600"></div>
  </div>

  <div id="editor" class="hide">
    <div class="card">
      <div class="sec-title">
        <span>1. वॉटरमार्क की जगह चुनें (Select Area)</span>
        <span id="dim" style="font-size:0.78rem; color:var(--mut); font-weight:500"></span>
      </div>
      <div class="stage" id="stage">
        <video id="video" controls playsinline preload="metadata"></video>
        <div class="ov" id="ov">
          <div class="box" id="box">
            <div class="hd" data-h="nw"></div><div class="hd" data-h="ne"></div>
            <div class="hd" data-h="sw"></div><div class="hd" data-h="se"></div>
          </div>
        </div>
      </div>

      <div class="presets">
        <button type="button" class="pbtn" data-pos="br">↘️ नीचे दाएं (Bottom-Right)</button>
        <button type="button" class="pbtn" data-pos="bl">↙️ नीचे बाएं (Bottom-Left)</button>
        <button type="button" class="pbtn" data-pos="tr">↗️ ऊपर दाएं (Top-Right)</button>
        <button type="button" class="pbtn" data-pos="tl">↖️ ऊपर बाएं (Top-Left)</button>
      </div>
    </div>

    <div class="card">
      <div class="sec-title"><span>2. बारीक एडजस्टमेंट (Fine-Tune Position)</span></div>
      <div class="grid">
        <div><label class="l"><span>X (बायां / Left)</span><b id="vx">0</b></label><input id="sx" type="range"></div>
        <div><label class="l"><span>Y (ऊपर / Top)</span><b id="vy">0</b></label><input id="sy" type="range"></div>
        <div><label class="l"><span>Width (चौड़ाई)</span><b id="vw">0</b></label><input id="sw" type="range"></div>
        <div><label class="l"><span>Height (ऊंचाई)</span><b id="vh">0</b></label><input id="sh" type="range"></div>
      </div>
    </div>

    <div class="card">
      <div class="sec-title"><span>3. रिमूवल मोड और क्वालिटी (Mode & Speed)</span></div>
      <div class="modes" style="margin-bottom:10px">
        <label class="mode sel"><input type="radio" name="mode" value="delogo" checked>✨ Smooth Blend (Recommended)
          <small>आस-पास के रंगों से मिलाकर लोगो गायब करे</small></label>
        <label class="mode"><input type="radio" name="mode" value="blur">💧 Clean Blur
          <small>वॉटरमार्क वाले हिस्से को स्मूद ब्लर करे</small></label>
      </div>
      <div class="modes">
        <label class="mode sel"><input type="radio" name="speed" value="ultrafast" checked>⚡ Super Fast Mode
          <small>तेज़ प्रोसेसिंग (लंबे वीडियो के लिए बेस्ट)</small></label>
        <label class="mode"><input type="radio" name="speed" value="fast">💎 High Quality Mode
          <small>बेहतर शार्पनेस और क्लैरिटी</small></label>
      </div>
    </div>

    <div class="card">
      <button class="btn red" id="go">🚀 वॉटरमार्क हटाएं / Remove Watermark</button>
      <div class="row">
        <div style="flex:1">
          <div class="bar"><i id="pb"></i></div>
          <div class="msg" id="status">तैयार है / Ready to process</div>
        </div>
        <div id="pct" style="min-width:50px; text-align:right; font-weight:800; font-size:1.05rem; color:#a5b4fc">0%</div>
      </div>
      <div id="err" class="err hide"></div>

      <div id="done" class="compare hide">
        <div class="sec-title" style="color:var(--ok)"><span>✅ साफ वीडियो तैयार है (Preview & Download)</span></div>
        <video id="outVideo" controls playsinline></video>
        <div style="margin-top:12px">
          <a id="dl" class="btn green" style="text-decoration:none">⬇️ साफ MP4 डाउनलोड करें / Download Clean MP4</a>
        </div>
      </div>
    </div>
  </div>

  <div class="footer">Built by Pawan Studio • 100% Client-Side Privacy Protected</div>
</div>

<script src="https://unpkg.com/@ffmpeg/ffmpeg@0.11.6/dist/ffmpeg.min.js" crossorigin="anonymous"></script>
<script>
(function(){
"use strict";
const $ = id => document.getElementById(id);
const CORE = "https://unpkg.com/@ffmpeg/core@0.11.0/dist/ffmpeg-core.js";
const M = 2;
const MAX_BYTES = 2 * 1024 * 1024 * 1024 - 64 * 1024 * 1024;
const S = {file:null, url:null, vw:0, vh:0, x:0, y:0, w:0, h:0, ff:null, busy:false, outUrl:null};
const logs = [];
const video = $("video"), box = $("box");

(function(){
  const w = $("isoWarn");
  if (typeof SharedArrayBuffer === "undefined" || !window.crossOriginIsolated) {
    w.textContent = "⚠️ ब्राउज़र आइसोलेशन सक्रिय नहीं है। पेज रीलोड करें या Google Chrome का उपयोग करें।";
    w.classList.remove("hide");
  }
  if (typeof FFmpeg === "undefined") {
    w.textContent = "⚠️ FFmpeg इंजन लोड नहीं हो सका। इंटरनेट चेक करें और रीलोड करें।";
    w.classList.remove("hide");
  }
})();

const cl = (v, a, b) => Math.min(Math.max(v, a), b);
const minW = () => Math.min(16, Math.max(2, S.vw - 2*M));
const minH = () => Math.min(16, Math.max(2, S.vh - 2*M));

function clampBox(){
  const maxW = Math.max(2, S.vw - 2*M), maxH = Math.max(2, S.vh - 2*M);
  S.w = Math.round(cl(S.w, minW(), maxW));
  S.h = Math.round(cl(S.h, minH(), maxH));
  S.x = Math.round(cl(S.x, M, S.vw - M - S.w));
  S.y = Math.round(cl(S.y, M, S.vh - M - S.h));
}

function render(){
  if (!S.vw || !video.clientWidth) return;
  const k = video.clientWidth / S.vw;
  box.style.left = (S.x * k) + "px";
  box.style.top = (S.y * k) + "px";
  box.style.width = (S.w * k) + "px";
  box.style.height = (S.h * k) + "px";
  $("sx").value = S.x; $("sy").value = S.y; $("sw").value = S.w; $("sh").value = S.h;
  $("vx").textContent = S.x + "px"; $("vy").textContent = S.y + "px";
  $("vw").textContent = S.w + "px"; $("vh").textContent = S.h + "px";
}

function setupSliders(){
  const set = (id, min, max) => { const e = $(id); e.min = min; e.max = max; e.step = 1; };
  set("sx", M, S.vw - M - minW());
  set("sy", M, S.vh - M - minH());
  set("sw", minW(), S.vw - 2*M);
  set("sh", minH(), S.vh - 2*M);
  $("dim").textContent = S.vw + " × " + S.vh + " px";
}

// One-click corner presets (great for Pollinations, TikTok, KineMaster logos)
document.querySelectorAll(".pbtn").forEach(btn => {
  btn.addEventListener("click", () => {
    if (!S.vw) return;
    const pos = btn.dataset.pos;
    S.w = Math.round(S.vw * 0.24);
    S.h = Math.round(S.vh * 0.11);
    const padX = Math.round(S.vw * 0.02);
    const padY = Math.round(S.vh * 0.02);
    if (pos === "br") { S.x = S.vw - S.w - padX; S.y = S.vh - S.h - padY; }
    if (pos === "bl") { S.x = padX; S.y = S.vh - S.h - padY; }
    if (pos === "tr") { S.x = S.vw - S.w - padX; S.y = padY; }
    if (pos === "tl") { S.x = padX; S.y = padY; }
    clampBox(); render();
  });
});

["sx","sy","sw","sh"].forEach(id => {
  $(id).addEventListener("input", e => {
    const key = {sx:"x", sy:"y", sw:"w", sh:"h"}[id];
    S[key] = parseInt(e.target.value, 10) || 0;
    clampBox(); render();
  });
});

document.querySelectorAll('input[name=mode], input[name=speed]').forEach(r => r.addEventListener("change", () => {
  const name = r.name;
  document.querySelectorAll(`input[name=${name}]`).forEach(x => x.parentElement.classList.toggle("sel", x.checked));
}));

function showErr(t){ const e = $("err"); e.textContent = "❌ " + t; e.classList.remove("hide"); }
function clearErr(){ $("err").classList.add("hide"); $("err").textContent = ""; }
function setProg(p, txt){
  p = cl(Math.round(p), 0, 100);
  $("pb").style.width = p + "%"; $("pct").textContent = p + "%";
  if (txt !== undefined) $("status").textContent = txt;
}

$("file").addEventListener("change", e => {
  const f = e.target.files && e.target.files[0];
  if (!f) return;
  clearErr(); $("done").classList.add("hide"); setProg(0, "तैयार है / Ready");
  if (!f.type.startsWith("video/") && !/\.(mp4|mov|mkv|webm|avi|m4v|3gp)$/i.test(f.name)) {
    showErr("कृपया एक मान्य वीडियो फ़ाइल चुनें।"); return;
  }
  if (f.size > MAX_BYTES) {
    $("fname").textContent = f.name;
    showErr("फ़ाइल 2GB से बड़ी है। कृपया वीडियो को छोटे हिस्सों में बांटें।");
    return;
  }
  S.file = f;
  $("fname").textContent = "🎞️ " + f.name + " (" + (f.size / 1048576).toFixed(1) + " MB)";
  if (S.url) URL.revokeObjectURL(S.url);
  S.url = URL.createObjectURL(f);
  video.src = S.url;
  $("editor").classList.remove("hide");
});

video.addEventListener("loadedmetadata", () => {
  S.vw = video.videoWidth; S.vh = video.videoHeight;
  if (!S.vw || !S.vh) { showErr("वीडियो पढ़ा नहीं जा सका।"); return; }
  S.w = Math.round(S.vw * 0.24); S.h = Math.round(S.vh * 0.11);
  S.x = S.vw - S.w - Math.round(S.vw * 0.02);
  S.y = S.vh - S.h - Math.round(S.vh * 0.02);
  setupSliders(); clampBox(); render();
});
window.addEventListener("resize", render);
video.addEventListener("loadeddata", render);

let drag = null;
box.addEventListener("pointerdown", e => {
  if (S.busy) return;
  drag = {mode: (e.target.dataset && e.target.dataset.h) || "move", sx: e.clientX, sy: e.clientY,
          ox: S.x, oy: S.y, ow: S.w, oh: S.h};
  try { box.setPointerCapture(e.pointerId); } catch(_){}
  e.preventDefault();
});
box.addEventListener("pointermove", e => {
  if (!drag || !video.clientWidth) return;
  const k = S.vw / video.clientWidth;
  const dx = (e.clientX - drag.sx) * k, dy = (e.clientY - drag.sy) * k;
  const m = drag.mode;
  let L = drag.ox, T = drag.oy, R = drag.ox + drag.ow, B = drag.oy + drag.oh;
  if (m === "move") {
    L = cl(drag.ox + dx, M, S.vw - M - drag.ow); T = cl(drag.oy + dy, M, S.vh - M - drag.oh);
    R = L + drag.ow; B = T + drag.oh;
  } else {
    if (m.indexOf("w") >= 0) L = cl(drag.ox + dx, M, R - minW());
    if (m.indexOf("e") >= 0) R = cl(drag.ox + drag.ow + dx, L + minW(), S.vw - M);
    if (m.indexOf("n") >= 0) T = cl(drag.oy + dy, M, B - minH());
    if (m.indexOf("s") >= 0) B = cl(drag.oy + drag.oh + dy, T + minH(), S.vh - M);
  }
  S.x = Math.round(L); S.y = Math.round(T); S.w = Math.round(R - L); S.h = Math.round(B - T);
  clampBox(); render();
  e.preventDefault();
});
const endDrag = () => { drag = null; };
box.addEventListener("pointerup", endDrag);
box.addEventListener("pointercancel", endDrag);
box.addEventListener("lostpointercapture", endDrag);

async function loadFF(){
  if (S.ff) return S.ff;
  if (typeof FFmpeg === "undefined") throw new Error("FFmpeg लोड नहीं हुआ। इंटरनेट चेक करें।");
  if (typeof SharedArrayBuffer === "undefined" || !window.crossOriginIsolated)
    throw new Error("SharedArrayBuffer उपलब्ध नहीं है। पेज रीलोड करें।");
  const ff = FFmpeg.createFFmpeg({log: true, corePath: CORE});
  ff.setLogger(({message}) => { logs.push(String(message)); if (logs.length > 40) logs.shift(); });
  await ff.load();
  S.ff = ff;
  return ff;
}

function buildArgs(inName, outName, audioArgs){
  clampBox();
  const x = S.x, y = S.y, w = S.w, h = S.h;
  const mode = document.querySelector('input[name=mode]:checked').value;
  const preset = document.querySelector('input[name=speed]:checked').value;
  const crf = preset === "fast" ? "20" : "23";
  const even = "scale=trunc(iw/2)*2:trunc(ih/2)*2";
  let args;
  if (mode === "delogo") {
    args = ["-i", inName, "-vf", "delogo=x=" + x + ":y=" + y + ":w=" + w + ":h=" + h + "," + even,
            "-map", "0:v:0", "-map", "0:a?"];
  } else {
    const bw = Math.max(2, w - (w % 2)), bh = Math.max(2, h - (h % 2));
    const bx = x - (x % 2), by = y - (y % 2);
    const r = cl(Math.floor(Math.min(bw, bh) / 4), 1, 12);
    const fc = "[0:v:0]split[a][b];[b]crop=" + bw + ":" + bh + ":" + bx + ":" + by + ",boxblur=" + r + ":2[c];" +
               "[a][c]overlay=" + bx + ":" + by + "," + even + "[v]";
    args = ["-i", inName, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?"];
  }
  return args.concat(["-c:v", "libx264", "-preset", preset, "-crf", crf, "-pix_fmt", "yuv420p"],
                     audioArgs, ["-sn", "-y", outName]);
}

function fileSize(ff, name){ try { return ff.FS("stat", name).size || 0; } catch(_) { return 0; } }
function safeUnlink(ff, name){ try { ff.FS("unlink", name); } catch(_) {} }

async function runJob(){
  if (S.busy || !S.file) return;
  S.busy = true; clearErr(); $("done").classList.add("hide");
 
