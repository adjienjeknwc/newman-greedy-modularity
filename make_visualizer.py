"""
Generator for interactive_visualizer.html
Reads data.json and builds a standalone, self-contained interactive visualizer.
Removes any "teacher cheat sheet" text and replaces it with a clean, professional
Partition Breakdown analysis panel.
"""

import json
import os

desktop_dir = "/Users/aditi/Desktop/newman_modularity"
artifact_dir = "/Users/aditi/.gemini/antigravity/brain/a983dd73-0451-4397-a8d9-6838886c6e85"

with open(os.path.join(desktop_dir, "data.json")) as f:
    graph_data = json.load(f)

json_str = json.dumps(graph_data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Newman Modularity Optimization Visualizer</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    body {{
      background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 100%);
      color: #f8fafc;
      min-height: 100vh;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .header {{
      text-align: center;
      margin-bottom: 20px;
    }}
    .header h1 {{
      font-size: 2.3rem;
      background: linear-gradient(135deg, #38bdf8 0%, #c084fc 50%, #f472b6 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 6px;
      font-weight: 800;
    }}
    .header p {{
      color: #94a3b8;
      font-size: 1.05rem;
    }}
    .badge-pill {{
      display: inline-block;
      background: rgba(168, 85, 247, 0.2);
      border: 1px solid rgba(168, 85, 247, 0.4);
      color: #c084fc;
      padding: 4px 14px;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-top: 8px;
    }}
    .main-grid {{
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 24px;
      width: 100%;
      max-width: 1220px;
    }}
    .card {{
      background: rgba(30, 41, 59, 0.7);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }}
    /* Controls Bar */
    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 16px;
      background: rgba(15, 23, 42, 0.8);
      padding: 12px 18px;
      border-radius: 14px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .btn-group {{ display: flex; gap: 8px; align-items: center; }}
    .btn {{
      background: #3b82f6;
      color: white;
      border: none;
      padding: 9px 16px;
      border-radius: 10px;
      cursor: pointer;
      font-size: 0.95rem;
      font-weight: 600;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .btn:hover {{ background: #2563eb; transform: translateY(-1px); }}
    .btn-purple {{ background: #8b5cf6; }}
    .btn-purple:hover {{ background: #7c3aed; }}
    .btn-pink {{ background: #ec4899; }}
    .btn-pink:hover {{ background: #db2777; }}
    .btn-outline {{
      background: transparent;
      border: 1px solid #475569;
      color: #cbd5e1;
    }}
    .btn-outline:hover {{ background: #334155; }}
    .btn.active-tab {{
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      color: #0f172a;
      border: none;
    }}
    /* Canvas styling */
    .canvas-container {{
      position: relative;
      width: 100%;
      height: 480px;
      background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid #334155;
    }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    
    /* Stats & Info side */
    .metric-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .metric-box {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 14px;
      text-align: center;
    }}
    .metric-title {{ font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; }}
    .metric-val {{ font-size: 1.8rem; font-weight: 800; color: #38bdf8; margin-top: 4px; }}
    .metric-val.gold {{ color: #f59e0b; }}
    .metric-val.green {{ color: #10b981; }}

    /* Clean Partition Details Box */
    .partition-box {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 16px;
      margin-top: 16px;
      max-height: 195px;
      overflow-y: auto;
    }}
    .partition-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .partition-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #60a5fa;
    }}
    .status-badge {{
      font-size: 0.75rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .status-badge.peak {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.5);
    }}
    .status-badge.normal {{
      background: rgba(148, 163, 184, 0.15);
      color: #94a3b8;
      border: 1px solid rgba(148, 163, 184, 0.2);
    }}
    .comm-list {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .comm-item {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.85rem;
      background: rgba(255, 255, 255, 0.03);
      padding: 7px 12px;
      border-radius: 8px;
      border-left: 3px solid #38bdf8;
    }}
    .comm-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }}
    .comm-text {{
      color: #cbd5e1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      flex: 1;
    }}

    /* Slider bar */
    .slider-wrap {{
      margin-top: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(15, 23, 42, 0.8);
      padding: 10px 16px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    input[type=range] {{
      flex: 1;
      accent-color: #a855f7;
      cursor: pointer;
    }}

    /* Modularity mini curve */
    .chart-box {{
      margin-top: 16px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 12px;
    }}
    .chart-box-title {{
      font-size: 0.85rem;
      color: #94a3b8;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
    }}
  </style>
</head>
<body>

  <div class="header">
    <h1>Newman's Modularity Optimizer Visualizer</h1>
    <p>Real-time Agglomerative Community Clustering and Modularity Trajectory</p>
    <span class="badge-pill">Complex Network Analysis & Validation Tool</span>
  </div>

  <div class="main-grid">
    <!-- LEFT: NETWORK CANVAS -->
    <div class="card">
      <div class="controls-bar">
        <div class="btn-group">
          <button class="btn btn-outline active-tab" id="tabToy" onclick="switchGraph('toy')">6-Node Toy Graph</button>
          <button class="btn btn-outline" id="tabKarate" onclick="switchGraph('karate')">Karate Club (34)</button>
        </div>
        <div class="btn-group">
          <button class="btn btn-purple" id="btnPlay" onclick="togglePlay()">Play Auto-Merge</button>
          <button class="btn btn-outline" onclick="step(-1)">Prev</button>
          <button class="btn btn-outline" onclick="step(1)">Next</button>
          <button class="btn btn-pink" onclick="resetSteps()">Reset</button>
        </div>
      </div>

      <div class="canvas-container">
        <canvas id="netCanvas"></canvas>
      </div>

      <div class="slider-wrap">
        <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">Merge Step:</span>
        <input type="range" id="stepSlider" min="0" max="5" value="0" oninput="onSliderInput(this.value)">
        <span id="stepLabel" style="font-weight: 800; color: #38bdf8; min-width: 45px; text-align: right;">0 / 5</span>
      </div>
    </div>

    <!-- RIGHT: LIVE METRICS & PARTITION DETAILS -->
    <div class="card">
      <h3 style="color: #60a5fa; margin-bottom: 14px; font-size: 1.2rem; font-weight: 700;">Live Network Metrics</h3>

      <div class="metric-row">
        <div class="metric-box">
          <div class="metric-title">Modularity (Q)</div>
          <div class="metric-val" id="valQ">-0.1735</div>
        </div>
        <div class="metric-box">
          <div class="metric-title">Active Communities</div>
          <div class="metric-val green" id="valComms">6</div>
        </div>
      </div>

      <div class="metric-row">
        <div class="metric-box">
          <div class="metric-title">&Delta;Q (Last Gain)</div>
          <div class="metric-val" id="valDeltaQ" style="font-size: 1.4rem;">+0.0000</div>
        </div>
        <div class="metric-box">
          <div class="metric-title">Optimal Peak Q*</div>
          <div class="metric-val gold" id="valPeakQ" style="font-size: 1.4rem;">0.3571</div>
        </div>
      </div>

      <!-- Mini Chart -->
      <div class="chart-box">
        <div class="chart-box-title">
          <span>Modularity Curve (Q vs Step)</span>
          <span id="peakBadge" style="color: #f59e0b;">Peak at Step 4</span>
        </div>
        <canvas id="chartCanvas" height="110" style="width: 100%;"></canvas>
      </div>

      <!-- Partition Details Box -->
      <div class="partition-box">
        <div class="partition-header">
          <span class="partition-title">Community Structure Breakdown</span>
          <span id="partitionStatus" class="status-badge normal">Step 0</span>
        </div>
        <div class="comm-list" id="commListContainer">
          <!-- Dynamically populated -->
        </div>
      </div>
    </div>
  </div>

  <script>
    const DATA = {json_str};
    
    let currentKey = 'toy';
    let currentStep = 0;
    let isPlaying = false;
    let playInterval = null;

    const PALETTE = [
      '#f43f5e', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4',
      '#ec4899', '#84cc16', '#eab308', '#6366f1', '#14b8a6', '#d946ef',
      '#fb923c', '#a855f7', '#2dd4bf', '#f87171', '#60a5fa', '#4ade80'
    ];

    const canvas = document.getElementById('netCanvas');
    const ctx = canvas.getContext('2d');
    const chartCanvas = document.getElementById('chartCanvas');
    const chartCtx = chartCanvas.getContext('2d');

    function resize() {{
      const rect = canvas.parentElement.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
      chartCanvas.width = chartCanvas.parentElement.getBoundingClientRect().width - 24;
      render();
    }}
    window.addEventListener('resize', resize);

    function switchGraph(key) {{
      currentKey = key;
      currentStep = 0;
      pause();
      document.getElementById('tabToy').classList.toggle('active-tab', key === 'toy');
      document.getElementById('tabKarate').classList.toggle('active-tab', key === 'karate');
      
      const maxSteps = DATA[key].history.length - 1;
      const slider = document.getElementById('stepSlider');
      slider.max = maxSteps;
      slider.value = 0;
      render();
    }}

    function togglePlay() {{
      if (isPlaying) {{ pause(); }} else {{ play(); }}
    }}

    function play() {{
      isPlaying = true;
      document.getElementById('btnPlay').innerText = 'Pause';
      document.getElementById('btnPlay').classList.replace('btn-purple', 'btn-pink');
      const maxSteps = DATA[currentKey].history.length - 1;
      playInterval = setInterval(() => {{
        if (currentStep < maxSteps) {{
          step(1);
        }} else {{
          pause();
        }}
      }}, 600);
    }}

    function pause() {{
      isPlaying = false;
      document.getElementById('btnPlay').innerText = 'Play Auto-Merge';
      document.getElementById('btnPlay').classList.replace('btn-pink', 'btn-purple');
      if (playInterval) clearInterval(playInterval);
    }}

    function resetSteps() {{
      pause();
      currentStep = 0;
      document.getElementById('stepSlider').value = 0;
      render();
    }}

    function step(dir) {{
      const maxSteps = DATA[currentKey].history.length - 1;
      currentStep = Math.max(0, Math.min(maxSteps, currentStep + dir));
      document.getElementById('stepSlider').value = currentStep;
      render();
    }}

    function onSliderInput(val) {{
      currentStep = parseInt(val, 10);
      render();
    }}

    function getNodePositions(key, width, height) {{
      const g = DATA[key];
      const positions = {{}};
      if (key === 'toy') {{
        const cx = width / 2;
        const cy = height / 2;
        positions[0] = {{ x: cx - 180, y: cy - 70 }};
        positions[1] = {{ x: cx - 180, y: cy + 70 }};
        positions[2] = {{ x: cx - 60,  y: cy }};
        positions[3] = {{ x: cx + 60,  y: cy }};
        positions[4] = {{ x: cx + 180, y: cy - 70 }};
        positions[5] = {{ x: cx + 180, y: cy + 70 }};
      }} else {{
        const cx = width / 2;
        const cy = height / 2;
        const scaleX = width * 0.42;
        const scaleY = height * 0.42;
        for (const [node, coords] of Object.entries(g.pos)) {{
          positions[node] = {{
            x: cx + coords[0] * scaleX,
            y: cy - coords[1] * scaleY
          }};
        }}
      }}
      return positions;
    }}

    function render() {{
      const g = DATA[currentKey];
      const hist = g.history[currentStep];
      const maxStep = g.history.length - 1;
      const bestStep = g.best_step;

      document.getElementById('stepLabel').innerText = `${{currentStep}} / ${{maxStep}}`;
      document.getElementById('valQ').innerText = hist.q >= 0 ? `+${{hist.q.toFixed(4)}}` : hist.q.toFixed(4);
      document.getElementById('valComms').innerText = hist.partition.length;
      document.getElementById('valDeltaQ').innerText = currentStep > 0 ? (hist.delta_q >= 0 ? `+${{hist.delta_q.toFixed(4)}}` : hist.delta_q.toFixed(4)) : '—';
      document.getElementById('valPeakQ').innerText = g.history[bestStep].q.toFixed(4);
      document.getElementById('peakBadge').innerText = `Peak Q* at Step ${{bestStep}}`;

      updatePartitionDisplay(currentKey, currentStep, bestStep, hist);

      const nodeToComm = {{}};
      hist.partition.forEach((comm, cIdx) => {{
        comm.forEach(node => {{ nodeToComm[node] = cIdx; }});
      }});

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const positions = getNodePositions(currentKey, canvas.width, canvas.height);

      g.edges.forEach(([u, v]) => {{
        const p1 = positions[u];
        const p2 = positions[v];
        if (!p1 || !p2) return;

        const sameComm = nodeToComm[u] === nodeToComm[v];
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        if (sameComm) {{
          ctx.strokeStyle = PALETTE[nodeToComm[u] % PALETTE.length];
          ctx.lineWidth = currentKey === 'toy' ? 4 : 2.5;
          ctx.globalAlpha = 0.9;
        }} else {{
          ctx.strokeStyle = '#475569';
          ctx.lineWidth = currentKey === 'toy' ? 2 : 1;
          ctx.globalAlpha = 0.35;
        }}
        ctx.stroke();
      }});
      ctx.globalAlpha = 1.0;

      const nodeRadius = currentKey === 'toy' ? 24 : 14;
      g.nodes.forEach(u => {{
        const p = positions[u];
        if (!p) return;
        const commIdx = nodeToComm[u];
        const color = PALETTE[commIdx % PALETTE.length];

        ctx.shadowColor = color;
        ctx.shadowBlur = 12;

        ctx.beginPath();
        ctx.arc(p.x, p.y, nodeRadius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();

        ctx.lineWidth = 2;
        ctx.strokeStyle = '#ffffff';
        ctx.stroke();
        ctx.shadowBlur = 0;

        ctx.fillStyle = '#ffffff';
        ctx.font = `bold ${{currentKey === 'toy' ? 14 : 10}}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(u, p.x, p.y);
      }});

      renderChart(g, currentStep, bestStep);
    }}

    function updatePartitionDisplay(key, step, bestStep, hist) {{
      const statusEl = document.getElementById('partitionStatus');
      const listEl = document.getElementById('commListContainer');

      if (step === bestStep) {{
        statusEl.className = 'status-badge peak';
        statusEl.innerText = '★ Optimal Cut (Max Q)';
      }} else {{
        statusEl.className = 'status-badge normal';
        statusEl.innerText = `Step ${{step}} (${{hist.partition.length}} communities)`;
      }}

      listEl.innerHTML = '';
      hist.partition.forEach((comm, idx) => {{
        const item = document.createElement('div');
        item.className = 'comm-item';
        const color = PALETTE[idx % PALETTE.length];
        item.style.borderLeftColor = color;

        const nodesStr = comm.length > 10 
          ? `[${{comm.slice(0, 8).join(', ')}}... +${{comm.length - 8}} more]`
          : `[${{comm.join(', ')}}]`;

        item.innerHTML = `
          <div class="comm-dot" style="background:${{color}};"></div>
          <div class="comm-text"><strong>Community ${{idx + 1}}</strong> (${{comm.length}} nodes): ${{nodesStr}}</div>
        `;
        listEl.appendChild(item);
      }});
    }}

    function renderChart(g, currentStep, bestStep) {{
      const w = chartCanvas.width;
      const h = chartCanvas.height;
      chartCtx.clearRect(0, 0, w, h);

      const hist = g.history;
      const maxSteps = hist.length - 1;
      const qValues = hist.map(item => item.q);
      const minQ = Math.min(...qValues);
      const maxQ = Math.max(...qValues);

      const padX = 25;
      const padY = 15;
      const plotW = w - padX * 2;
      const plotH = h - padY * 2;

      function getX(s) {{ return padX + (s / maxSteps) * plotW; }}
      function getY(q) {{ return padY + (1 - (q - minQ) / (maxQ - minQ || 1)) * plotH; }}

      if (minQ < 0 && maxQ > 0) {{
        chartCtx.beginPath();
        chartCtx.moveTo(padX, getY(0));
        chartCtx.lineTo(w - padX, getY(0));
        chartCtx.strokeStyle = 'rgba(255,255,255,0.15)';
        chartCtx.setLineDash([4, 4]);
        chartCtx.stroke();
        chartCtx.setLineDash([]);
      }}

      chartCtx.beginPath();
      hist.forEach((pt, idx) => {{
        const x = getX(idx);
        const y = getY(pt.q);
        if (idx === 0) chartCtx.moveTo(x, y);
        else chartCtx.lineTo(x, y);
      }});
      chartCtx.strokeStyle = '#38bdf8';
      chartCtx.lineWidth = 2.5;
      chartCtx.stroke();

      const peakX = getX(bestStep);
      const peakY = getY(hist[bestStep].q);
      chartCtx.beginPath();
      chartCtx.arc(peakX, peakY, 6, 0, Math.PI * 2);
      chartCtx.fillStyle = '#f59e0b';
      chartCtx.fill();

      const currX = getX(currentStep);
      const currY = getY(hist[currentStep].q);
      chartCtx.beginPath();
      chartCtx.arc(currX, currY, 7, 0, Math.PI * 2);
      chartCtx.fillStyle = '#ec4899';
      chartCtx.fill();
      chartCtx.lineWidth = 2;
      chartCtx.strokeStyle = '#ffffff';
      chartCtx.stroke();
    }}

    setTimeout(resize, 100);
  </script>
</body>
</html>
"""

# Write to Desktop
out_desktop = os.path.join(desktop_dir, "interactive_visualizer.html")
with open(out_desktop, "w") as f:
    f.write(html_content)

# Write to 2_presentation
out_pres = os.path.join(desktop_dir, "2_presentation", "interactive_visualizer.html")
with open(out_pres, "w") as f:
    f.write(html_content)

# Write to artifact dir
out_artifact = os.path.join(artifact_dir, "interactive_visualizer.html")
with open(out_artifact, "w") as f:
    f.write(html_content)

print("Generated clean visualizer successfully with the requested section removed!")
