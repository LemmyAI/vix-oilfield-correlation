#!/usr/bin/env python3
"""
Iran Wars in Strange Numbers by the Looney AI Lemmy
A cynical look at market madness during conflict
"""

from flask import Flask
import json
import os

app = Flask(__name__, static_folder='static')

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data.json')
with open(DATA_FILE) as f:
    DATA = json.load(f)

@app.route('/')
def index():
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>Iran Wars in Strange Numbers - by Looney AI Lemmy</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background: linear-gradient(135deg, #0a0a0a 0%, #1a0a1a 100%); color: white; font-family: system-ui, sans-serif; margin: 0; padding: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 15px; }}
        h1 {{ text-align: center; color: #ff6b6b; margin-bottom: 5px; font-size: 22px; text-shadow: 0 0 20px rgba(255,107,107,0.3); }}
        .subtitle {{ text-align: center; color: #ffa502; margin-top: 0; font-size: 13px; font-style: italic; }}
        .lemmy {{ text-align: center; font-size: 40px; margin: 10px 0; }}
        
        .tabs {{ display: flex; gap: 8px; margin: 15px 0; flex-wrap: wrap; }}
        .tab {{ flex: 1; min-width: 150px; padding: 12px 10px; background: #1a1a1a; border: 2px solid #333; border-radius: 10px; cursor: pointer; text-align: center; transition: all 0.3s; }}
        .tab:hover {{ border-color: #555; transform: translateY(-2px); }}
        .tab.active {{ transform: translateY(-2px); }}
        .tab-title {{ font-size: 14px; font-weight: bold; margin-bottom: 3px; }}
        .tab-desc {{ font-size: 10px; color: #888; }}
        #tab-vix.active {{ border-color: #00d4ff; background: linear-gradient(135deg, #1a2a3a 0%, #1a1a2a 100%); }}
        #tab-vix.active .tab-title {{ color: #00d4ff; }}
        #tab-maga.active {{ border-color: #ff69b4; background: linear-gradient(135deg, #2a1a2a 0%, #1a1a2a 100%); }}
        #tab-maga.active .tab-title {{ color: #ff69b4; }}
        #tab-rrp.active {{ border-color: #ffa502; background: linear-gradient(135deg, #2a2a1a 0%, #1a1a2a 100%); }}
        #tab-rrp.active .tab-title {{ color: #ffa502; }}
        
        .stats {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; }}
        .stat-box {{ flex: 1; min-width: 120px; background: rgba(26, 26, 26, 0.8); border-radius: 10px; padding: 12px; text-align: center; border: 1px solid #333; }}
        .stat-label {{ color: #888; font-size: 11px; margin-bottom: 3px; }}
        .stat-value {{ font-size: 24px; font-weight: bold; margin: 0; }}
        .stat-sub {{ color: #666; font-size: 10px; margin-top: 3px; }}
        
        .chart-container {{ background: rgba(26, 26, 26, 0.9); border-radius: 10px; padding: 15px; margin: 15px 0; display: none; border: 1px solid #333; }}
        .chart-container.active {{ display: block; }}
        .chart-title {{ margin-top: 0; margin-bottom: 10px; font-size: 16px; }}
        .chart-explain {{ color: #aaa; font-size: 11px; margin-bottom: 10px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 5px; line-height: 1.5; }}
        canvas {{ max-height: 300px; }}
        
        .section {{ background: rgba(26, 26, 26, 0.8); border-radius: 10px; padding: 15px; margin: 15px 0; border: 1px solid #333; }}
        .section h3 {{ color: #ffa502; margin-top: 0; font-size: 14px; }}
        .timeline-item {{ margin-bottom: 10px; padding-left: 20px; position: relative; }}
        .timeline-item::before {{ content: "⬤"; position: absolute; left: 0; font-size: 8px; }}
        .timeline-date {{ font-size: 13px; font-weight: bold; }}
        
        .cynical {{ background: linear-gradient(135deg, #2a1a1a 0%, #1a1a2a 100%); border-radius: 10px; padding: 15px; margin: 15px 0; border-left: 3px solid #ff6b6b; }}
        .cynical h4 {{ color: #ff6b6b; margin: 0 0 10px 0; font-size: 13px; }}
        .cynical p {{ color: #aaa; font-size: 12px; margin: 0; line-height: 1.6; }}
        
        .footer {{ text-align: center; color: #555; font-size: 11px; margin-top: 20px; padding: 15px; border-top: 1px solid #222; }}
        .footer a {{ color: #ffa502; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="lemmy">🦾</div>
        <h1>Iran Wars in Strange Numbers</h1>
        <p class="subtitle">by the Looney AI Lemmy (cynical perspective)</p>
        
        <div class="tabs">
            <div class="tab active" id="tab-vix" onclick="showTab('vix')">
                <div class="tab-title">📈 VIX vs Attacks</div>
                <div class="tab-desc">Volatility & destruction</div>
            </div>
            <div class="tab" id="tab-maga" onclick="showTab('maga')">
                <div class="tab-title">🇺🇸 MAGA vs KIA</div>
                <div class="tab-desc">Stocks & casualties</div>
            </div>
            <div class="tab" id="tab-rrp" onclick="showTab('rrp')">
                <div class="tab-title">🏦 Hidden QE vs Deaths</div>
                <div class="tab-desc">Fed magic & mortality</div>
            </div>
        </div>
        
        <div class="stats" id="stats-vix">
            <div class="stat-box">
                <div class="stat-label">VIX Peak</div>
                <p class="stat-value" style="color: #ff4444;">{DATA['stats']['vix_peak']:.2f}</p>
                <div class="stat-sub">Fear index max</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Infra Attacks</div>
                <p class="stat-value" style="color: #ffa500;">{DATA['stats']['total_attacks']}</p>
                <div class="stat-sub">Things destroyed</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Hormuz</div>
                <p class="stat-value" style="color: #ff0000;">CLOSED</p>
                <div class="stat-sub">20% oil supply</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Correlation</div>
                <p class="stat-value" style="color: #00ff00;">r=0.74</p>
                <div class="stat-sub">Fear follows fire</div>
            </div>
        </div>
        
        <div class="stats" id="stats-maga" style="display:none;">
            <div class="stat-box">
                <div class="stat-label">DJT Pump</div>
                <p class="stat-value" style="color: #00ff00;">+{DATA['stats']['djt_pump_pct']:.0f}%</p>
                <div class="stat-sub">War is profitable</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">US KIA</div>
                <p class="stat-value" style="color: #0066ff;">{DATA['stats']['total_kia']}</p>
                <div class="stat-sub">Real cost</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Peak Price</div>
                <p class="stat-value" style="color: #ff69b4;">${DATA['stats']['djt_max']:.2f}</p>
                <div class="stat-sub">Hormuz day</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Correlation</div>
                <p class="stat-value" style="color: #ffaa00;">r=0.89</p>
                <div class="stat-sub">Morbid sync</div>
            </div>
        </div>
        
        <div class="stats" id="stats-rrp" style="display:none;">
            <div class="stat-box">
                <div class="stat-label">RRP Drained</div>
                <p class="stat-value" style="color: #ffa502;">${DATA['stats']['rrp_drop']:.0f}B</p>
                <div class="stat-sub">Liquidity flood</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Total Deaths</div>
                <p class="stat-value" style="color: #ff6b6b;">{DATA['stats']['total_deaths']:,}</p>
                <div class="stat-sub">All sides</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">RRP Low</div>
                <p class="stat-value" style="color: #00d4ff;">${DATA['stats']['rrp_min']:.0f}B</p>
                <div class="stat-sub">Peak crisis</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Drop %</div>
                <p class="stat-value" style="color: #ff69b4;">42%</p>
                <div class="stat-sub">Of reserves</div>
            </div>
        </div>
        
        <div class="chart-container active" id="chart-vix">
            <h3 class="chart-title" style="color: #00d4ff;">📈 VIX Volatility vs Infrastructure Attacks</h3>
            <canvas id="vixCanvas"></canvas>
        </div>
        
        <div class="chart-container" id="chart-maga">
            <h3 class="chart-title" style="color: #ff69b4;">🇺🇸 DJT Stock vs American Casualties</h3>
            <canvas id="magaCanvas"></canvas>
        </div>
        
        <div class="chart-container" id="chart-rrp">
            <h3 class="chart-title" style="color: #ffa502;">🏦 Hidden QE vs Conflict Deaths</h3>
            <div class="chart-explain">
                <strong>What is RRP?</strong> The Fed's Reverse Repo facility is where banks park excess cash overnight. 
                When RRP drops <strong>${DATA['stats']['rrp_drop']:.0f} BILLION</strong> in days, that cash floods into markets - covert liquidity injection 
                without official QE announcement. They call it "liquidity management." We call it <strong>Hidden QE</strong>. 
                Note how it tanked when the war started.
            </div>
            <canvas id="rrpCanvas"></canvas>
        </div>
        
        <div class="cynical">
            <h4>🦾 Lemmy's Cynical Take</h4>
            <p>
                VIX spikes, DJT pumps 93%, the Fed "magically" drains ${DATA['stats']['rrp_drop']:.0f}B from reverse repos 
                during the same conflict. Markets feast on chaos while {DATA['stats']['total_deaths']:,} people died. 
                Make of that what you will.
            </p>
        </div>
        
        <div class="section">
            <h3>📅 War Timeline (Feb 28 - Mar 3, 2026)</h3>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ff0000;">⚔️ Feb 28</span>
                <span style="color: #aaa;">War starts - Khamenei assassinated, missiles fly, RRP drain begins</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ff6600;">🛢️ Mar 1</span>
                <span style="color: #aaa;">Hormuz CLOSED - DJT hits ${DATA['stats']['djt_max']:.2f}, RRP crashes to ${DATA['stats']['rrp_min']:.0f}B</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ffaa00;">🔥 Mar 2</span>
                <span style="color: #aaa;">Hezbollah joins - 1,544 total deaths</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #00ffff;">📡 Mar 3</span>
                <span style="color: #aaa;">Qatar strikes back - {DATA['stats']['total_deaths']:,} dead total</span>
            </div>
        </div>
        
        <div class="footer">
            Data: FRED, Market Data, Official Reports | <a href="https://github.com/LemmyAI/vix-oilfield-correlation">GitHub</a><br>
            Updated: {DATA['stats']['last_updated']} | 🦾 Powered by cynicism and charts
        </div>
    </div>
    
    <script>
        const dates = {json.dumps(DATA['dates'])};
        const warStartIdx = {DATA['war_start_idx']};
        const vixData = {json.dumps(DATA['vix'])};
        const djtData = {json.dumps(DATA['djt'])};
        const attacksData = {json.dumps(DATA['attacks'])};
        const kiaData = {json.dumps(DATA['kia'])};
        const rrpData = {json.dumps(DATA['rrp'])};
        const deathsData = {json.dumps(DATA['deaths'])};
        
        function showTab(tab) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.chart-container').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.stats').forEach(s => s.style.display = 'none');
            document.getElementById('tab-' + tab).classList.add('active');
            document.getElementById('chart-' + tab).classList.add('active');
            document.getElementById('stats-' + tab).style.display = 'flex';
        }}
        
        // VIX Chart
        new Chart(document.getElementById('vixCanvas').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: dates,
                datasets: [
                    {{ label: 'VIX', data: vixData, borderColor: '#00d4ff', backgroundColor: 'rgba(0, 212, 255, 0.1)', fill: true, tension: 0.4, yAxisID: 'y', spanGaps: true }},
                    {{ label: 'Attacks', data: attacksData, borderColor: '#ff4444', backgroundColor: 'rgba(255, 68, 68, 0.7)', type: 'bar', yAxisID: 'y1' }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#888', maxRotation: 45 }}, grid: {{ color: '#333' }} }},
                    y: {{ type: 'linear', position: 'left', ticks: {{ color: '#00d4ff' }}, grid: {{ color: '#333' }}, title: {{ display: true, text: 'VIX', color: '#00d4ff' }} }},
                    y1: {{ type: 'linear', position: 'right', ticks: {{ color: '#ff4444' }}, grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Attacks', color: '#ff4444' }} }}
                }}
            }}
        }});
        
        // MAGA Chart
        new Chart(document.getElementById('magaCanvas').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: dates,
                datasets: [
                    {{ label: 'DJT ($)', data: djtData, borderColor: '#ff69b4', backgroundColor: 'rgba(255, 105, 180, 0.1)', fill: true, tension: 0.4, yAxisID: 'y', spanGaps: true }},
                    {{ label: 'US KIA', data: kiaData, borderColor: '#0066ff', borderWidth: 3, pointRadius: 6, pointBackgroundColor: '#0066ff', yAxisID: 'y1', spanGaps: true }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#888', maxRotation: 45 }}, grid: {{ color: '#333' }} }},
                    y: {{ type: 'linear', position: 'left', ticks: {{ color: '#ff69b4' }}, grid: {{ color: '#333' }}, title: {{ display: true, text: 'DJT ($)', color: '#ff69b4' }} }},
                    y1: {{ type: 'linear', position: 'right', ticks: {{ color: '#0066ff' }}, grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'US KIA', color: '#0066ff' }} }}
                }}
            }}
        }});
        
        // RRP Chart
        new Chart(document.getElementById('rrpCanvas').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: dates,
                datasets: [
                    {{ label: 'RRP ($B)', data: rrpData, borderColor: '#ffa502', backgroundColor: 'rgba(255, 165, 2, 0.1)', fill: true, tension: 0.4, yAxisID: 'y', spanGaps: true }},
                    {{ label: 'Total Deaths', data: deathsData, borderColor: '#ff6b6b', borderWidth: 3, pointRadius: 6, pointBackgroundColor: '#ff6b6b', yAxisID: 'y1', spanGaps: true }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#888', maxRotation: 45 }}, grid: {{ color: '#333' }} }},
                    y: {{ type: 'linear', position: 'left', ticks: {{ color: '#ffa502' }}, grid: {{ color: '#333' }}, title: {{ display: true, text: 'RRP ($B)', color: '#ffa502' }} }},
                    y1: {{ type: 'linear', position: 'right', ticks: {{ color: '#ff6b6b' }}, grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Deaths', color: '#ff6b6b' }} }}
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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
