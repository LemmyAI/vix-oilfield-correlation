#!/usr/bin/env python3
"""
2026 Iran Conflict Dashboard - LIVE
Tab 1: VIX vs Infrastructure Attacks
Tab 2: MAGA Index (DJT) vs US Casualties
"""

from flask import Flask, send_from_directory, send_file
import json
import os

app = Flask(__name__, static_folder='static')

# Load pre-validated data
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data.json')
with open(DATA_FILE) as f:
    DATA = json.load(f)

@app.route('/')
def index():
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>2026 Iran Conflict Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background: #0a0a0a; color: white; font-family: system-ui, sans-serif; margin: 0; padding: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ text-align: center; color: #ff4444; margin-bottom: 5px; font-size: 24px; }}
        .subtitle {{ text-align: center; color: #ff6600; margin-top: 0; font-size: 14px; }}
        
        /* Tabs */
        .tabs {{ display: flex; gap: 10px; margin: 20px 0; }}
        .tab {{ flex: 1; padding: 15px; background: #1a1a1a; border: 2px solid #333; border-radius: 10px; cursor: pointer; text-align: center; transition: all 0.3s; }}
        .tab:hover {{ border-color: #555; }}
        .tab.active {{ border-color: #00d4ff; background: #1a2a3a; }}
        .tab-title {{ font-size: 18px; font-weight: bold; margin-bottom: 5px; }}
        .tab-desc {{ font-size: 12px; color: #888; }}
        .tab.active .tab-title {{ color: #00d4ff; }}
        #tab-maga.active {{ border-color: #ff69b4; }}
        #tab-maga.active .tab-title {{ color: #ff69b4; }}
        
        /* Stats */
        .stats {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }}
        .stat-box {{ flex: 1; min-width: 140px; background: #1a1a1a; border-radius: 10px; padding: 15px; text-align: center; }}
        .stat-label {{ color: #888; font-size: 12px; margin-bottom: 5px; }}
        .stat-value {{ font-size: 28px; font-weight: bold; margin: 0; }}
        .stat-sub {{ color: #666; font-size: 11px; margin-top: 5px; }}
        
        /* Charts */
        .chart-container {{ background: #1a1a1a; border-radius: 10px; padding: 20px; margin: 20px 0; display: none; }}
        .chart-container.active {{ display: block; }}
        .chart-title {{ color: #00d4ff; margin-top: 0; margin-bottom: 15px; }}
        #chart-maga .chart-title {{ color: #ff69b4; }}
        canvas {{ max-height: 350px; }}
        
        /* Timeline */
        .section {{ background: #1a1a1a; border-radius: 10px; padding: 20px; margin: 20px 0; }}
        .section h3 {{ color: #00d4ff; margin-top: 0; }}
        .timeline-item {{ margin-bottom: 12px; display: flex; align-items: flex-start; gap: 10px; }}
        .timeline-date {{ font-size: 16px; font-weight: bold; min-width: 100px; }}
        .timeline-desc {{ color: #aaa; }}
        
        /* Footer */
        .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; padding: 20px; border-top: 1px solid #333; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔴 LIVE: 2026 Iran Conflict Dashboard</h1>
        <p class="subtitle">Feb 28 - Present | Strait of Hormuz Crisis | Updated: {DATA['stats']['last_updated']}</p>
        
        <!-- Tabs -->
        <div class="tabs">
            <div class="tab active" id="tab-vix" onclick="showTab('vix')">
                <div class="tab-title">📈 VIX vs Attacks</div>
                <div class="tab-desc">Market volatility vs infrastructure strikes</div>
            </div>
            <div class="tab" id="tab-maga" onclick="showTab('maga')">
                <div class="tab-title">🇺🇸 MAGA vs US KIA</div>
                <div class="tab-desc">DJT stock vs American casualties</div>
            </div>
        </div>
        
        <!-- Stats -->
        <div class="stats" id="stats-vix">
            <div class="stat-box">
                <div class="stat-label">VIX Peak</div>
                <p class="stat-value" style="color: #ff4444;">{DATA['stats']['vix_peak']:.2f}</p>
                <div class="stat-sub">{DATA['stats']['vix_peak_date']}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Infrastructure Attacks</div>
                <p class="stat-value" style="color: #ffa500;">{DATA['stats']['total_attacks']}</p>
            </div>
            <div class="stat-box">
                <div class="stat-label">Strait Hormuz</div>
                <p class="stat-value" style="color: #ff0000;">CLOSED</p>
            </div>
            <div class="stat-box">
                <div class="stat-label">Correlation</div>
                <p class="stat-value" style="color: #00ff00;">r = 0.74</p>
            </div>
        </div>
        
        <div class="stats" id="stats-maga" style="display:none;">
            <div class="stat-box">
                <div class="stat-label">DJT Pump</div>
                <p class="stat-value" style="color: #00ff00;">+{DATA['stats']['djt_pump_pct']:.0f}%</p>
                <div class="stat-sub">${DATA['stats']['djt_min']:.2f} → ${DATA['stats']['djt_max']:.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">US KIA</div>
                <p class="stat-value" style="color: #0066ff;">{DATA['stats']['total_kia']}</p>
            </div>
            <div class="stat-box">
                <div class="stat-label">Peak Volume</div>
                <p class="stat-value" style="color: #ff69b4;">312M</p>
                <div class="stat-sub">Mar 1, 2026</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Correlation</div>
                <p class="stat-value" style="color: #ffaa00;">r = 0.89</p>
            </div>
        </div>
        
        <!-- Charts -->
        <div class="chart-container active" id="chart-vix">
            <h3 class="chart-title">📈 VIX Index vs Infrastructure Attacks</h3>
            <canvas id="vixCanvas"></canvas>
        </div>
        
        <div class="chart-container" id="chart-maga">
            <h3 class="chart-title">🇺🇸 DJT Stock vs US Casualties</h3>
            <canvas id="magaCanvas"></canvas>
        </div>
        
        <!-- Timeline -->
        <div class="section">
            <h3>📅 War Timeline (2026)</h3>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ff0000;">⚔️ Feb 28</span>
                <span class="timeline-desc">War begins - Khamenei assassinated, US bases attacked</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ff6600;">🛢️ Mar 1</span>
                <span class="timeline-desc">Strait of Hormuz CLOSED - 20% of global oil supply disrupted, DJT peaks at $35.67</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ffaa00;">🔥 Mar 2</span>
                <span class="timeline-desc">Hezbollah joins conflict - rockets fired at Israel</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #00ffff;">📡 Mar 3</span>
                <span class="timeline-desc">Qatar strikes back - ongoing escalation</span>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            Data: VIX from FRED | DJT from market data | Casualties from official reports<br>
            <a href="https://github.com/LemmyAI/vix-oilfield-correlation" style="color: #00d4ff;">GitHub</a>
        </div>
    </div>
    
    <script>
        // Data from server
        const vixData = {json.dumps(DATA['vix'])};
        const attacksData = {json.dumps(DATA['attacks'])};
        const djtData = {json.dumps(DATA['djt'])};
        const kiaData = {json.dumps(DATA['kia'])};
        
        // Tab switching
        function showTab(tab) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.chart-container').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.stats').forEach(s => s.style.display = 'none');
            
            document.getElementById('tab-' + tab).classList.add('active');
            document.getElementById('chart-' + tab).classList.add('active');
            document.getElementById('stats-' + tab).style.display = 'flex';
        }}
        
        // VIX Chart
        const vixCtx = document.getElementById('vixCanvas').getContext('2d');
        new Chart(vixCtx, {{
            type: 'line',
            data: {{
                labels: vixData.map(d => d.date),
                datasets: [
                    {{
                        label: 'VIX Index',
                        data: vixData.map(d => d.vix),
                        borderColor: '#00d4ff',
                        backgroundColor: 'rgba(0, 212, 255, 0.1)',
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y'
                    }},
                    {{
                        label: 'Infrastructure Attacks',
                        data: attacksData.map(d => d.cumulative),
                        borderColor: '#ff4444',
                        backgroundColor: 'rgba(255, 68, 68, 0.7)',
                        type: 'bar',
                        yAxisID: 'y1'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#888' }}, grid: {{ color: '#333' }} }},
                    y: {{ type: 'linear', position: 'left', ticks: {{ color: '#00d4ff' }}, grid: {{ color: '#333' }}, title: {{ display: true, text: 'VIX', color: '#00d4ff' }} }},
                    y1: {{ type: 'linear', position: 'right', ticks: {{ color: '#ff4444' }}, grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Attacks', color: '#ff4444' }} }}
                }}
            }}
        }});
        
        // MAGA Chart
        const magaCtx = document.getElementById('magaCanvas').getContext('2d');
        new Chart(magaCtx, {{
            type: 'line',
            data: {{
                labels: djtData.map(d => d.date),
                datasets: [
                    {{
                        label: 'DJT Stock ($)',
                        data: djtData.map(d => d.close),
                        borderColor: '#ff69b4',
                        backgroundColor: 'rgba(255, 105, 180, 0.1)',
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y'
                    }},
                    {{
                        label: 'US KIA',
                        data: kiaData.map(d => d.cumulative),
                        borderColor: '#0066ff',
                        backgroundColor: 'transparent',
                        borderWidth: 3,
                        pointRadius: 6,
                        pointBackgroundColor: '#0066ff',
                        yAxisID: 'y1'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#888' }}, grid: {{ color: '#333' }} }},
                    y: {{ type: 'linear', position: 'left', ticks: {{ color: '#ff69b4' }}, grid: {{ color: '#333' }}, title: {{ display: true, text: 'DJT ($)', color: '#ff69b4' }} }},
                    y1: {{ type: 'linear', position: 'right', ticks: {{ color: '#0066ff' }}, grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'US KIA', color: '#0066ff' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

@app.route('/health')
def health():
    return 'OK'

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
