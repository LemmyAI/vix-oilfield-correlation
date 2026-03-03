#!/usr/bin/env python3
"""
2026 Iran Conflict Dashboard - Lightweight version
"""

from flask import Flask
import json

app = Flask(__name__)

# Hardcoded data (lighter than pandas)
VIX_DATA = [
    {"date": "2026-02-18", "vix": 18.52},
    {"date": "2026-02-19", "vix": 18.75},
    {"date": "2026-02-20", "vix": 19.09},
    {"date": "2026-02-21", "vix": 19.88},
    {"date": "2026-02-23", "vix": 21.01},
    {"date": "2026-02-24", "vix": 19.55},
    {"date": "2026-02-25", "vix": 17.93},
    {"date": "2026-02-26", "vix": 18.63},
    {"date": "2026-02-27", "vix": 19.86},
    {"date": "2026-02-28", "vix": 22.45},
    {"date": "2026-03-01", "vix": 23.12},
    {"date": "2026-03-02", "vix": 21.44},
    {"date": "2026-03-03", "vix": 20.87},
]

ATTACKS_DATA = [
    {"date": "2026-02-28", "cumulative": 4},
    {"date": "2026-03-01", "cumulative": 10},
    {"date": "2026-03-02", "cumulative": 13},
    {"date": "2026-03-03", "cumulative": 15},
]

DJT_DATA = [
    {"date": "2026-02-18", "close": 18.45, "volume": 45.2},
    {"date": "2026-02-19", "close": 18.92, "volume": 52.1},
    {"date": "2026-02-20", "close": 19.15, "volume": 48.7},
    {"date": "2026-02-21", "close": 19.88, "volume": 61.3},
    {"date": "2026-02-24", "close": 21.22, "volume": 89.5},
    {"date": "2026-02-25", "close": 22.05, "volume": 112.4},
    {"date": "2026-02-26", "close": 21.88, "volume": 95.2},
    {"date": "2026-02-27", "close": 24.12, "volume": 178.6},
    {"date": "2026-02-28", "close": 31.45, "volume": 245.8},
    {"date": "2026-03-01", "close": 35.67, "volume": 312.4},
    {"date": "2026-03-02", "close": 32.18, "volume": 198.5},
    {"date": "2026-03-03", "close": 28.45, "volume": 167.3},
]

US_KIA = [
    {"date": "2026-02-28", "cumulative": 3},
    {"date": "2026-03-01", "cumulative": 6},
    {"date": "2026-03-02", "cumulative": 6},
    {"date": "2026-03-03", "cumulative": 6},
]

@app.route('/')
def index():
    vix_json = json.dumps(VIX_DATA)
    attacks_json = json.dumps(ATTACKS_DATA)
    djt_json = json.dumps(DJT_DATA)
    kia_json = json.dumps(US_KIA)
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>2026 Iran Conflict Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background: #0a0a0a; color: white; font-family: system-ui, sans-serif; margin: 0; padding: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ text-align: center; color: #ff4444; margin-bottom: 5px; }}
        .subtitle {{ text-align: center; color: #ff6600; margin-top: 0; }}
        .stats {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }}
        .stat-box {{ flex: 1; min-width: 150px; background: #1a1a1a; border-radius: 10px; padding: 15px; text-align: center; }}
        .stat-label {{ color: #888; font-size: 14px; margin-bottom: 5px; }}
        .stat-value {{ font-size: 28px; font-weight: bold; margin: 0; }}
        .stat-sub {{ color: #666; font-size: 12px; margin-top: 5px; }}
        .section {{ background: #1a1a1a; border-radius: 10px; padding: 20px; margin: 20px 0; }}
        .section h3 {{ color: #00d4ff; margin-top: 0; }}
        .chart-container {{ background: #1a1a1a; border-radius: 10px; padding: 20px; margin: 20px 0; }}
        canvas {{ max-height: 300px; }}
        .timeline-item {{ margin-bottom: 10px; }}
        .timeline-date {{ font-size: 18px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔴 LIVE: 2026 Iran Conflict Dashboard</h1>
        <p class="subtitle">Feb 28 - Present | Strait of Hormuz Crisis</p>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">VIX Peak</div>
                <p class="stat-value" style="color: #ff4444;">23.12</p>
                <div class="stat-sub">Mar 1, 2026</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">DJT Pump</div>
                <p class="stat-value" style="color: #00ff00;">+93%</p>
                <div class="stat-sub">Peak: $35.67</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">US KIA</div>
                <p class="stat-value" style="color: #0066ff;">6</p>
            </div>
            <div class="stat-box">
                <div class="stat-label">Infra Attacks</div>
                <p class="stat-value" style="color: #ffa500;">15</p>
            </div>
        </div>
        
        <div class="chart-container">
            <h3 style="color: #00d4ff; margin-top: 0;">📈 VIX vs Infrastructure Attacks</h3>
            <canvas id="vixChart"></canvas>
        </div>
        
        <div class="chart-container">
            <h3 style="color: #ff69b4; margin-top: 0;">🇺🇸 DJT Stock vs US Casualties</h3>
            <canvas id="djtChart"></canvas>
        </div>
        
        <div class="section">
            <h3>📅 Timeline</h3>
            <div class="timeline-item"><span class="timeline-date" style="color: #ff0000;">⚔️ Feb 28</span> - War begins, Khamenei assassinated</div>
            <div class="timeline-item"><span class="timeline-date" style="color: #ff6600;">🛢️ Mar 1</span> - Strait of Hormuz CLOSED, DJT peaks</div>
            <div class="timeline-item"><span class="timeline-date" style="color: #ffaa00;">🔥 Mar 2</span> - Hezbollah joins conflict</div>
            <div class="timeline-item"><span class="timeline-date" style="color: #00ffff;">📡 Mar 3</span> - Qatar strikes back, ongoing</div>
        </div>
    </div>
    
    <script>
        // VIX Chart
        const vixCtx = document.getElementById('vixChart').getContext('2d');
        const vixData = {vix_json};
        const attacksData = {attacks_json};
        
        new Chart(vixCtx, {{
            type: 'line',
            data: {{
                labels: vixData.map(d => d.date),
                datasets: [
                    {{
                        label: 'VIX',
                        data: vixData.map(d => d.vix),
                        borderColor: '#00d4ff',
                        backgroundColor: 'rgba(0, 212, 255, 0.1)',
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y'
                    }},
                    {{
                        label: 'Attacks',
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
        
        // DJT Chart
        const djtCtx = document.getElementById('djtChart').getContext('2d');
        const djtData = {djt_json};
        const kiaData = {kia_json};
        
        new Chart(djtCtx, {{
            type: 'line',
            data: {{
                labels: djtData.map(d => d.date),
                datasets: [
                    {{
                        label: 'DJT ($)',
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

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
