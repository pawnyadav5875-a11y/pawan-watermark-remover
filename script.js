(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const cl = (v, a, b) => Math.max(a, Math.min(b, v));

  const state = {
    mode: "photo", file: null, url: null, W: 0, H: 0,
    rect: { x: 0, y: 0, w: 0, h: 0, name: "Bottom-Right" },
    busy: false, runId: 0
  };

  const photoTab = $("photoTab"), videoTab = $("videoTab"), fileInput = $("fileInput");
  const photoPreview = $("photoPreview"), videoPreview = $("videoPreview"), outputCanvas = $("outputCanvas");
  const selLayer = $("selectionLayer"), selHandle = $("selectionHandle");

  function setMode(m) {
    state.mode = m;
    photoTab.classList.toggle("active", m === "photo");
    videoTab.classList.toggle("active", m === "video");
    $("uploadTitle").textContent = m === "photo" ? "Choose Your Photo" : "Choose Your Video";
    $("uploadDescription").textContent = m === "photo"
      ? "यहाँ टैप करके फोटो चुनें — तुरंत ऑटो-रिमूव शुरू होगा"
      : "यहाँ टैप करके वीडियो चुनें — तुरंत ऑटो-रिमूव शुरू होगा";
    fileInput.accept = m === "photo" ? "image/*" : "video/*";
    $("workspace").classList.remove("show");
    $("result").classList.remove("show");
    $("fileInfo").textContent = "";
  }
  photoTab.onclick = () => setMode("photo");
  videoTab.onclick = () => setMode("video");

  $("threshold").oninput = e => $("thresholdValue").textContent = e.target.value;
  $("grain").oninput = e => $("grainValue").textContent = e.target.value + "%";
  $("manualToggle").onchange = e => { selLayer.classList.toggle("active", e.target.checked); syncBox(); };
  $("manualBtn").onclick = () => {
    $("manualToggle").checked = !$("manualToggle").checked;
    selLayer.classList.toggle("active", $("manualToggle").checked);
    syncBox();
  };

  function syncBox() {
    if (!state.W || !state.H) return;
    const activeEl = outputCanvas.classList.contains("visible") ? outputCanvas : (state.mode === "photo" ? photoPreview : videoPreview);
    const sR = $("previewStage").getBoundingClientRect();
    const eR = activeEl.getBoundingClientRect();
    if (!eR.width || !eR.height) return;
    selLayer.style.left = ((eR.left - sR.left) + (state.rect.x / state.W) * eR.width) + "px";
    selLayer.style.top = ((eR.top - sR.top) + (state.rect.y / state.H) * eR.height) + "px";
    selLayer.style.width = ((state.rect.w / state.W) * eR.width) + "px";
    selLayer.style.height = ((state.rect.h / state.H) * eR.height) + "px";
  }
  window.addEventListener("resize", syncBox);

  selLayer.onpointerdown = e => {
    e.preventDefault();
    const activeEl = outputCanvas.classList.contains("visible") ? outputCanvas : (state.mode === "photo" ? photoPreview : videoPreview);
    const eR = activeEl.getBoundingClientRect();
    if (!eR.width) return;
    const resizing = e.target === selHandle;
    const sx = e.clientX, sy = e.clientY, ox = state.rect.x, oy = state.rect.y, ow = state.rect.w, oh = state.rect.h;
    selLayer.setPointerCapture(e.pointerId);
    selLayer.onpointermove = ev => {
      const dx = ((ev.clientX - sx) / eR.width) * state.W;
      const dy = ((ev.clientY - sy) / eR.height) * state.H;
      if (resizing) {
        state.rect.w = Math.round(cl(ow + dx, 14, state.W - state.rect.x - 2));
        state.rect.h = Math.round(cl(oh + dy, 14, state.H - state.rect.y - 2));
      } else {
        state.rect.x = Math.round(cl(ox + dx, 2, state.W - state.rect.w - 2));
        state.rect.y = Math.round(cl(oy + dy, 2, state.H - state.rect.h - 2));
      }
      syncBox();
    };
    selLayer.onpointerup = selLayer.onpointercancel = () => { selLayer.onpointermove = null; runClean(false); };
  };

  function autoDetect(ctx, W, H) {
    const zw = Math.max(24, Math.round(W * 0.34)), zh = Math.max(18, Math.round(H * 0.16));
    const zones = [
      { name: "Bottom-Right", x: W - zw - Math.round(W * 0.01), y: H - zh - Math.round(H * 0.01), w: zw, h: zh },
      { name: "Bottom-Left",  x: Math.round(W * 0.01),          y: H - zh - Math.round(H * 0.01), w: zw, h: zh },
      { name: "Top-Right",    x: W - zw - Math.round(W * 0.01), y: Math.round(H * 0.01),          w: zw, h: zh },
      { name: "Top-Left",     x: Math.round(W * 0.01),          y: Math.round(H * 0.01),          w: zw, h: zh }
    ];
    let best = zones[0], bestScore = -1, bestTight = null;
    for (const z of zones) {
      const d = ctx.getImageData(z.x, z.y, z.w, z.h).data;
      let bgS = 0, bgC = 0;
      for (let j = 0; j < z.h; j++) for (let i = 0; i < z.w; i++) {
        if (i < 2 || i >= z.w - 2 || j < 2 || j >= z.h - 2) {
          const p = (j * z.w + i) * 4;
          bgS += 0.299 * d[p] + 0.587 * d[p + 1] + 0.114 * d[p + 2]; bgC++;
        }
      }
      const bgL = bgS / Math.max(1, bgC);
      let minX = z.w, minY = z.h, maxX = 0, maxY = 0, hits = 0;
      for (let j = 2; j < z.h - 2; j++) for (let i = 2; i < z.w - 2; i++) {
        const p = (j * z.w + i) * 4, pR = p + 4, pD = ((j + 1) * z.w + i) * 4;
        const l = 0.299 * d[p] + 0.587 * d[p + 1] + 0.114 * d[p + 2];
        const edge = Math.abs(l - (0.299 * d[pR] + 0.587 * d[pR + 1] + 0.114 * d[pR + 2])) +
                     Math.abs(l - (0.299 * d[pD] + 0.587 * d[pD + 1] + 0.114 * d[pD + 2]));
        if (edge > 34 && Math.abs(l - bgL) > 20) {
          hits++;
          if (i < minX) minX = i; if (i > maxX) maxX = i;
          if (j < minY) minY = j; if (j > maxY) maxY = j;
        }
      }
      const density = hits / Math.max(1, (z.w - 4) * (z.h - 4));
      const score = (density > 0.01 && density < 0.55) ? hits : hits * 0.15;
      if (score > bestScore) {
        bestScore = score; best = z;
        if (hits > 10 && maxX > minX && maxY > minY) {
          const pad = 6, rx = cl(z.x + minX - pad, 2, W - 12), ry = cl(z.y + minY - pad, 2, H - 12);
          bestTight = { name: z.name, x: rx, y: ry, w: cl((maxX - minX) + pad * 2, 12, W - rx - 2), h: cl((maxY - minY) + pad * 2, 12, H - ry - 2) };
        } else bestTight = { ...z };
      }
    }
    return bestTight || best;
  }

  function reconstruct(ctx, W, H, rect) {
    const x = cl(Math.round(rect.x), 2, W - 6), y = cl(Math.round(rect.y), 2, H - 6);
    const w = cl(Math.round(rect.w), 4, W - x - 2), h = cl(Math.round(rect.h), 4, H - y - 2);
    const pad = 4, bx = x - pad, by = y - pad, bw = w + pad * 2, bh = h + pad * 2;
    const img = ctx.getImageData(bx, by, bw, bh), d = img.data;
    const mask = new Uint8Array(bw * bh);
    const sens = parseInt($("threshold").value, 10) || 38;
    const grainAmt = (parseInt($("grain").value, 10) || 0) / 100;

    let rS = 0, gS = 0, bS = 0, cnt = 0;
    for (let j = 0; j < bh; j++) for (let i = 0; i < bw; i++) {
      if (i < pad || i >= bw - pad || j < pad || j >= bh - pad) {
        const p = (j * bw + i) * 4; rS += d[p]; gS += d[p + 1]; bS += d[p + 2]; cnt++;
      }
    }
    const bgR = rS / cnt, bgG = gS / cnt, bgB = bS / cnt;

    let mCount = 0;
    for (let j = pad; j < bh - pad; j++) for (let i = pad; i < bw - pad; i++) {
      const p = (j * bw + i) * 4;
      if (Math.abs(d[p] - bgR) + Math.abs(d[p + 1] - bgG) + Math.abs(d[p + 2] - bgB) > sens) {
        mask[j * bw + i] = 1; mCount++;
      }
    }
    if (mCount < 10) {
      for (let j = pad; j < bh - pad; j++) for (let i = pad; i < bw - pad; i++) mask[j * bw + i] = 1;
    } else {
      const cp = new Uint8Array(mask);
      for (let j = pad; j < bh - pad; j++) for (let i = pad; i < bw - pad; i++) {
        if (!cp[j * bw + i] && (cp[(j - 1) * bw + i] || cp[(j + 1) * bw + i] || cp[j * bw + i - 1] || cp[j * bw + i + 1])) mask[j * bw + i] = 1;
      }
    }

    let left = true, guard = 0;
    while (left && guard++ < 140) {
      left = false;
      const next = new Uint8Array(mask);
      for (let j = pad; j < bh - pad; j++) for (let i = pad; i < bw - pad; i++) {
        const idx = j * bw + i;
        if (!mask[idx]) continue;
        left = true;
        let wr = 0, wg = 0, wb = 0, wt = 0;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
          if (!dx && !dy) continue;
          const nIdx = (j + dy) * bw + (i + dx);
          if (!mask[nIdx]) {
            const wtVal = (dx === 0 || dy === 0) ? 1.45 : 0.85;
            const p = nIdx * 4;
            wr += d[p] * wtVal; wg += d[p + 1] * wtVal; wb += d[p + 2] * wtVal; wt += wtVal;
          }
        }
        if (wt > 0) {
          const gNoise = (((i * 73 + j * 151) & 15) - 7.5) * grainAmt;
          const p = idx * 4;
          d[p] = cl(Math.round(wr / wt + gNoise), 0, 255);
          d[p + 1] = cl(Math.round(wg / wt + gNoise), 0, 255);
          d[p + 2] = cl(Math.round(wb / wt + gNoise), 0, 255);
          next[idx] = 0;
        }
      }
      mask.set(next);
    }
    ctx.putImageData(img, bx, by);
  }

  fileInput.onchange = e => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    if (state.url) URL.revokeObjectURL(state.url);
    state.file = f; state.url = URL.createObjectURL(f);
    $("fileInfo").textContent = "📁 " + f.name + " (" + (f.size / 1048576).toFixed(2) + " MB)";
    $("workspace").classList.add("show"); $("result").classList.remove("show");
    photoPreview.classList.remove("visible"); videoPreview.classList.remove("visible"); outputCanvas.classList.remove("visible");

    if (state.mode === "photo") {
      photoPreview.onload = () => {
        state.W = photoPreview.naturalWidth; state.H = photoPreview.naturalHeight;
        $("dimensions").textContent = state.W + " × " + state.H + " px";
        runClean(true);
      };
      photoPreview.src = state.url; photoPreview.classList.add("visible");
    } else {
      videoPreview.onloadeddata = () => {
        const sc = Math.min(1, 1920 / Math.max(videoPreview.videoWidth, videoPreview.videoHeight));
        state.W = Math.max(2, Math.round(videoPreview.videoWidth * sc) & ~1);
        state.H = Math.max(2, Math.round(videoPreview.videoHeight * sc) & ~1);
        $("dimensions").textContent = state.W + " × " + state.H + " px";
        runClean(true);
      };
      videoPreview.src = state.url; videoPreview.classList.add("visible");
    }
  };

  $("autoBtn").onclick = () => runClean(true);
  $("resetBtn").onclick = () => { $("workspace").classList.remove("show"); $("result").classList.remove("show"); fileInput.value = ""; };

  async function runClean(autoScan) {
    if (!state.url || !state.W) return;
    if (state.mode === "photo") {
      outputCanvas.width = state.W; outputCanvas.height = state.H;
      const ctx = outputCanvas.getContext("2d", { willReadFrequently: true });
      ctx.drawImage(photoPreview, 0, 0, state.W, state.H);
      if (autoScan) {
        state.rect = autoDetect(ctx, state.W, state.H);
        $("previewType").textContent = "✅ Auto-Detected: " + state.rect.name;
      }
      reconstruct(ctx, state.W, state.H, state.rect);
      photoPreview.classList.remove("visible"); outputCanvas.classList.add("visible");
      requestAnimationFrame(syncBox);

      const cleanUrl = outputCanvas.toDataURL("image/png");
      $("result").classList.add("show");
      $("resultMedia").innerHTML = `<img src="${cleanUrl}" alt="Clean Photo">`;
      $("downloadLink").href = cleanUrl;
      $("downloadLink").download = (state.file.name.replace(/\.[^.]+$/, "") || "photo") + "_clean.png";
      return;
    }

    const runId = ++state.runId;
    state.busy = true; $("progressArea").classList.add("show"); $("result").classList.remove("show");
    let ac = null, wl = null, rec = null;
    const stopAll = () => { try { ac && ac.close(); } catch (_) {} try { wl && wl.release(); } catch (_) {} };

    try {
      const v = document.createElement("video");
      v.src = state.url; v.playsInline = true; v.preload = "auto";
      await new Promise((res, rej) => { v.onloadeddata = res; v.onerror = () => rej(new Error("Video load failed")); });
      if (runId !== state.runId) { stopAll(); return; }

      outputCanvas.width = state.W; outputCanvas.height = state.H;
      const ctx = outputCanvas.getContext("2d", { willReadFrequently: true });
      ctx.drawImage(v, 0, 0, state.W, state.H);
      if (autoScan) {
        state.rect = autoDetect(ctx, state.W, state.H);
        $("previewType").textContent = "✅ Auto-Detected: " + state.rect.name;
      }
      videoPreview.classList.remove("visible"); outputCanvas.classList.add("visible");
      requestAnimationFrame(syncBox);

      const stream = outputCanvas.captureStream(30);
      if ($("preserveAudio").checked) {
        try {
          ac = new (window.AudioContext || window.webkitAudioContext)();
          const src = ac.createMediaElementSource(v), dst = ac.createMediaStreamDestination();
          src.connect(dst); dst.stream.getAudioTracks().forEach(t => stream.addTrack(t));
          await ac.resume();
        } catch (_) {}
      }

      const mt = ["video/mp4;codecs=avc1.42E01E,mp4a.40.2", "video/mp4", "video/webm;codecs=vp9,opus", "video/webm"].find(t => MediaRecorder.isTypeSupported(t));
      const bps = Math.round(cl(state.W * state.H * 5, 3e6, 14e6));
      rec = new MediaRecorder(stream, mt ? { mimeType: mt, videoBitsPerSecond: bps } : { videoBitsPerSecond: bps });
      const chunks = [];
      rec.ondataavailable = e => { if (e.data && e.data.size) chunks.push(e.data); };
      rec.onstop = () => {
        stopAll();
        if (runId !== state.runId) return;
        state.busy = false;
        const type = mt ? mt.split(";")[0] : "video/webm";
        const blob = new Blob(chunks, { type }), outUrl = URL.createObjectURL(blob);
        const ext = type.includes("mp4") ? "mp4" : "webm";
        $("progressBar").style.width = "100%"; $("progressPercent").textContent = "100%";
        $("status").textContent = "✅ वीडियो तैयार है!";
        $("result").classList.add("show");
        $("resultMedia").innerHTML = `<video src="${outUrl}" controls playsinline></video>`;
        $("downloadLink").href = outUrl;
        $("downloadLink").download = (state.file.name.replace(/\.[^.]+$/, "") || "video") + "_clean." + ext;
      };

      try { wl = await navigator.wakeLock.request("screen"); } catch (_) {}
      let active = true;
      const loop = () => {
        if (!active || runId !== state.runId) {
          active = false; try { if (rec.state !== "inactive") rec.stop(); } catch (_) {} return;
        }
        ctx.drawImage(v, 0, 0, state.W, state.H);
        reconstruct(ctx, state.W, state.H, state.rect);
        const pct = v.duration ? Math.min(99, Math.round((v.currentTime / v.duration) * 100)) : 0;
        $("progressBar").style.width = pct + "%"; $("progressPercent").textContent = pct + "%";
        $("status").textContent = `ऑटो-क्लीनिंग चल रही है… ${pct}%`;
        requestAnimationFrame(loop);
      };

      v.onended = () => {
        ctx.drawImage(v, 0, 0, state.W, state.H);
        reconstruct(ctx, state.W, state.H, state.rect);
        active = false; setTimeout(() => { if (rec.state !== "inactive") rec.stop(); }, 250);
      };

      rec.start(800); v.currentTime = 0; await v.play(); loop();
    } catch (err) {
      stopAll(); state.busy = false;
      $("status").textContent = "❌ Error: " + (err.message || "Try again");
    }
  }
})();
    
