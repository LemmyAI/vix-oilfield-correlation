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

# Correlations are pre-calculated from war start date in pipeline
CORR = DATA['correlations']

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
        
        .tabs {{ display: flex; gap: 6px; margin: 15px 0; flex-wrap: wrap; }}
        .tab {{ flex: 1; min-width: 140px; padding: 10px 8px; background: #1a1a1a; border: 2px solid #333; border-radius: 10px; cursor: pointer; text-align: center; transition: all 0.3s; }}
        .tab:hover {{ border-color: #555; transform: translateY(-2px); }}
        .tab.active {{ transform: translateY(-2px); }}
        .tab-title {{ font-size: 13px; font-weight: bold; margin-bottom: 2px; }}
        .tab-desc {{ font-size: 9px; color: #888; }}
        #tab-vix.active {{ border-color: #00d4ff; background: linear-gradient(135deg, #1a2a3a 0%, #1a1a2a 100%); }}
        #tab-vix.active .tab-title {{ color: #00d4ff; }}
        #tab-djt.active {{ border-color: #ff69b4; background: linear-gradient(135deg, #2a1a2a 0%, #1a1a2a 100%); }}
        #tab-djt.active .tab-title {{ color: #ff69b4; }}
        #tab-maga.active {{ border-color: #ff4444; background: linear-gradient(135deg, #2a1a1a 0%, #1a1a2a 100%); }}
        #tab-maga.active .tab-title {{ color: #ff4444; }}
        #tab-rrp.active {{ border-color: #ffa502; background: linear-gradient(135deg, #2a2a1a 0%, #1a1a2a 100%); }}
        #tab-rrp.active .tab-title {{ color: #ffa502; }}
        
        .stats {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; }}
        .stat-box {{ flex: 1; min-width: 110px; background: rgba(26, 26, 26, 0.8); border-radius: 10px; padding: 12px; text-align: center; border: 1px solid #333; }}
        .stat-label {{ color: #888; font-size: 10px; margin-bottom: 3px; }}
        .stat-value {{ font-size: 22px; font-weight: bold; margin: 0; }}
        .stat-sub {{ color: #666; font-size: 9px; margin-top: 3px; }}
        
        .chart-container {{ background: rgba(26, 26, 26, 0.9); border-radius: 10px; padding: 15px; margin: 15px 0; display: none; border: 1px solid #333; }}
        .chart-container.active {{ display: block; }}
        .chart-title {{ margin-top: 0; margin-bottom: 10px; font-size: 15px; }}
        .chart-explain {{ color: #aaa; font-size: 11px; margin-bottom: 10px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 5px; line-height: 1.5; }}
        canvas {{ max-height: 280px; }}
        
        .corr-box {{ background: rgba(255, 165, 2, 0.1); border: 1px solid #ffa502; border-radius: 8px; padding: 10px; margin: 10px 0; }}
        .corr-title {{ color: #ffa502; font-size: 11px; font-weight: bold; margin-bottom: 5px; }}
        .corr-text {{ color: #ccc; font-size: 10px; line-height: 1.5; }}
        
        .sources {{ background: rgba(26, 26, 26, 0.6); border-radius: 8px; padding: 10px 15px; margin: 15px 0; border-left: 3px solid #555; }}
        .sources-title {{ color: #888; font-size: 11px; font-weight: bold; margin-bottom: 5px; }}
        .sources-list {{ color: #666; font-size: 10px; line-height: 1.6; }}
        .sources-list a {{ color: #ffa502; }}
        
        .section {{ background: rgba(26, 26, 26, 0.8); border-radius: 10px; padding: 15px; margin: 15px 0; border: 1px solid #333; }}
        .section h3 {{ color: #ffa502; margin-top: 0; font-size: 14px; }}
        .timeline-item {{ margin-bottom: 10px; padding-left: 20px; position: relative; }}
        .timeline-item::before {{ content: "X"; position: absolute; left: 0; font-size: 8px; color: #666; }}
        .timeline-date {{ font-size: 13px; font-weight: bold; }}
        
        .cynical {{ background: linear-gradient(135deg, #2a1a1a 0%, #1a1a2a 100%); border-radius: 10px; padding: 15px; margin: 15px 0; border-left: 3px solid #ff6b6b; }}
        .cynical h4 {{ color: #ff6b6b; margin: 0 0 10px 0; font-size: 13px; }}
        .cynical p {{ color: #aaa; font-size: 12px; margin: 0; line-height: 1.6; }}
        
        .footer {{ text-align: center; color: #555; font-size: 11px; margin-top: 20px; padding: 15px; border-top: 1px solid #222; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="lemmy">🦾</div>
        <h1>Iran Wars in Strange Numbers</h1>
        <p class="subtitle">Looney hallucinations by the AI Lemmy</p>
        
        <div class="tabs">
            <div class="tab active" id="tab-vix" onclick="showTab('vix')">
                <div class="tab-title">📈 VIX vs Attacks</div>
                <div class="tab-desc">Volatility and destruction</div>
            </div>
            <div class="tab" id="tab-djt" onclick="showTab('djt')">
                <div class="tab-title">💰 $DJT vs KIA</div>
                <div class="tab-desc">Stock and casualties</div>
            </div>
            <div class="tab" id="tab-maga" onclick="showTab('maga')">
                <div class="tab-title">🇺🇸 MAGA Metrics</div>
                <div class="tab-desc">Approval and war</div>
            </div>
            <div class="tab" id="tab-rrp" onclick="showTab('rrp')">
                <div class="tab-title">🏦 Hidden QE vs Deaths</div>
                <div class="tab-desc">Fed magic and mortality</div>
            </div>
        </div>
        
        <div class="corr-box">
            <div class="corr-title">📊 Correlation Index (r-value)</div>
            <div class="corr-text">
                <strong>What it means:</strong> r ranges from -1 (perfect inverse) to +1 (perfect correlation). 
                • <strong>|r| > 0.7</strong> = Strong relationship 
                • <strong>|r| 0.4-0.7</strong> = Moderate 
                • <strong>|r| < 0.4</strong> = Weak/no relationship.<br>
                <strong>Calculated from war start (Feb 28) only</strong> - measures conflict-period relationships, not pre-war noise.
            </div>
        </div>
        
        <div class="stats" id="stats-vix">
            <div class="stat-box">
                <div class="stat-label">VIX Peak</div>
                <p class="stat-value" style="color: #ff4444;">{DATA['stats']['vix_peak']:.2f}</p>
                <div class="stat-sub">Fear index max</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Energy Infra</div>
                <p class="stat-value" style="color: #ffa500;">{DATA['stats']['total_attacks']}</p>
                <div class="stat-sub">Oil, gas, refineries</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Hormuz</div>
                <p class="stat-value" style="color: #ff0000;">CLOSED</p>
                <div class="stat-sub">20% oil supply</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Correlation</div>
                <p class="stat-value" style="color: #00ff00;">r={CORR['vix_attacks']:.2f}</p>
                <div class="stat-sub">Negative: fear peaks early</div>
            </div>
        </div>
        
        <div class="stats" id="stats-djt" style="display:none;">
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
                <p class="stat-value" style="color: #ffaa00;">r={CORR['djt_kia']:.2f}</p>
                <div class="stat-sub">Weak positive</div>
            </div>
        </div>
        
        <div class="stats" id="stats-maga" style="display:none;">
            <div class="stat-box">
                <div class="stat-label">Trump Approval</div>
                <p class="stat-value" style="color: #ff4444;">{DATA['stats']['trump_peak']:.1f}%</p>
                <div class="stat-sub">+{DATA['stats']['trump_change']:.1f}pts rally</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Right Track</div>
                <p class="stat-value" style="color: #ffa502;">38.7%</p>
                <div class="stat-sub">Up from 28%</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Iran Approval</div>
                <p class="stat-value" style="color: #00d4ff;">61.3%</p>
                <div class="stat-sub">War support</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Correlation</div>
                <p class="stat-value" style="color: #ff69b4;">r={CORR['righttrack_kia']:.2f}</p>
                <div class="stat-sub">Strong: rally effect</div>
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
                <div class="stat-label">Correlation</div>
                <p class="stat-value" style="color: #ff69b4;">r={CORR['rrp_deaths']:.2f}</p>
                <div class="stat-sub">Near zero: unrelated</div>
            </div>
        </div>
        
        <div class="chart-container active" id="chart-vix">
            <h3 class="chart-title" style="color: #00d4ff;">📈 VIX Volatility vs Energy Infrastructure Attacks</h3>
            <div class="chart-explain">
                <strong>Fear vs Fire</strong> Energy infrastructure includes oil fields, refineries, pipelines, export terminals. VIX spiked to 23.12 when Hormuz closed (Mar 1), then declined while attacks accumulated. 
                The <strong>r={CORR['vix_attacks']:.2f}</strong> correlation is negative because fear peaked early, then markets adapted to the "new normal" of daily strikes.
            </div>
            <canvas id="vixCanvas"></canvas>
            <div class="sources">
                <div class="sources-title">📚 Data Sources</div>
                <div class="sources-list">
                    <strong>VIX:</strong> <a href="https://fred.stlouisfed.org/series/VIXCLS" target="_blank">FRED - VIXCLS</a> |
                    <strong>Attacks:</strong> Reuters, AP News, Wikipedia conflict timeline
                </div>
            </div>
        </div>
        
        <div class="chart-container" id="chart-djt">
            <h3 class="chart-title" style="color: #ff69b4;">💰 $DJT Stock vs American Casualties</h3>
            <div class="chart-explain">
                <strong>War Profiteering:</strong> Trump Media stock surged 93% during the conflict. The weak positive correlation 
                <strong>r={CORR['djt_kia']:.2f}</strong> suggests both moved together, but DJT peaked early (Mar 1) while casualties accumulated through Mar 3.
            </div>
            <canvas id="djtCanvas"></canvas>
            <div class="sources">
                <div class="sources-title">📚 Data Sources</div>
                <div class="sources-list">
                    <strong>DJT Stock:</strong> Trump Media and Technology Group (NASDAQ: DJT) - Yahoo Finance |
                    <strong>US Casualties:</strong> DoD briefings, Reuters, AP News
                </div>
            </div>
        </div>
        
        <div class="chart-container" id="chart-maga">
            <h3 class="chart-title" style="color: #ff4444;">🇺🇸 Approval Ratings During War</h3>
            <div class="chart-explain">
                <strong>Rally Round the Flag:</strong> Classic effect - presidential approval spikes during military action. 
                Trump gained +{DATA['stats']['trump_change']:.1f}pts, "Right Track" surged from 28% to 39%. 
                The <strong>r={CORR['righttrack_kia']:.2f}</strong> correlation is STRONG - Americans rallied as casualties mounted.
            </div>
            <canvas id="magaCanvas"></canvas>
            <div class="sources">
                <div class="sources-title">📚 Data Sources</div>
                <div class="sources-list">
                    <strong>Approval:</strong> Gallup, FiveThirtyEight aggregate polls |
                    <strong>Right Track:</strong> RealClearPolitics average |
                    <strong>Iran Support:</strong> YouGov/Harris polling
                </div>
            </div>
        </div>
        
        <div class="chart-container" id="chart-rrp">
            <h3 class="chart-title" style="color: #ffa502;">🏦 Hidden QE vs Conflict Deaths</h3>
            <div class="chart-explain">
                <strong>Liquidity Injection:</strong> The Fed's Reverse Repo dropped ${DATA['stats']['rrp_drop']:.0f}B in days - that cash flooded markets as covert QE. 
                The near-zero <strong>r={CORR['rrp_deaths']:.2f}</strong> correlation suggests this was pre-planned liquidity management, not death-driven.
            </div>
            <canvas id="rrpCanvas"></canvas>
            <div class="sources">
                <div class="sources-title">📚 Data Sources</div>
                <div class="sources-list">
                    <strong>RRP:</strong> <a href="https://www.newyorkfed.org/markets/omo_transaction_data#reverse-repo" target="_blank">NY Fed</a> |
                    <strong>Deaths:</strong> Iran Health Ministry, IDF, US Central Command, UN
                </div>
            </div>
        </div>
        
        <div class="cynical">
            <h4>🦾 Lemmy's Cynical Take</h4>
            <p>
                VIX spikes, DJT pumps {DATA['stats']['djt_pump_pct']:.0f}%, approval surges +{DATA['stats']['trump_change']:.1f}pts, the Fed drains ${DATA['stats']['rrp_drop']:.0f}B from reverse repos 
                during the same conflict that killed {DATA['stats']['total_deaths']:,} people. 
                "Right Track" sentiment shows an 0.81 correlation with body count. Make of that what you will.
            </p>
        </div>
        
        <div class="section">
            <h3>📅 War Timeline (Feb 28 - Mar 3, 2026)</h3>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ff0000;">Feb 28</span>
                <span style="color: #aaa;">War starts - Khamenei assassinated, missiles fly</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ff6600;">Mar 1</span>
                <span style="color: #aaa;">Hormuz CLOSED - DJT ${DATA['stats']['djt_max']:.2f}, Trump approval {DATA['stats']['trump_peak']:.1f}%</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #ffaa00;">Mar 2</span>
                <span style="color: #aaa;">Hezbollah joins - 1,544 total deaths</span>
            </div>
            <div class="timeline-item">
                <span class="timeline-date" style="color: #00ffff;">Mar 3</span>
                <span style="color: #aaa;">Qatar strikes back - {DATA['stats']['total_deaths']:,} dead total</span>
            </div>
        </div>
        
        <div class="footer">
            Data compiled from public sources | Updated: {DATA['stats']['last_updated']} | 🦾 Powered by cynicism and charts
        </div>
    </div>
    
    <script>
        const dates = {json.dumps(DATA['dates'])};
        const vixData = {json.dumps(DATA['vix'])};
        const djtData = {json.dumps(DATA['djt'])};
        const attacksData = {json.dumps(DATA['attacks'])};
        const kiaData = {json.dumps(DATA['kia'])};
        const rrpData = {json.dumps(DATA['rrp'])};
        const deathsData = {json.dumps(DATA['deaths'])};
        const trumpApp = {json.dumps(DATA['trump_approval'])};
        const bidenApp = {json.dumps(DATA['biden_approval'])};
        const rightTrack = {json.dumps(DATA['right_track'])};
        const iranApp = {json.dumps(DATA['iran_approval'])};
        
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
        
        // DJT Chart
        new Chart(document.getElementById('djtCanvas').getContext('2d'), {{
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
        
        // MAGA Chart
        new Chart(document.getElementById('magaCanvas').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: dates,
                datasets: [
                    {{ label: 'Trump Approval', data: trumpApp, borderColor: '#ff4444', backgroundColor: 'rgba(255, 68, 68, 0.1)', fill: true, tension: 0.4, yAxisID: 'y', spanGaps: true }},
                    {{ label: 'Right Track', data: rightTrack, borderColor: '#ffa502', backgroundColor: 'rgba(255, 165, 2, 0.1)', fill: true, tension: 0.4, yAxisID: 'y', spanGaps: true }},
                    {{ label: 'US KIA', data: kiaData, borderColor: '#0066ff', borderWidth: 3, pointRadius: 6, pointBackgroundColor: '#0066ff', yAxisID: 'y1', spanGaps: true }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#888', maxRotation: 45 }}, grid: {{ color: '#333' }} }},
                    y: {{ type: 'linear', position: 'left', min: 25, max: 70, ticks: {{ color: '#ff4444' }}, grid: {{ color: '#333' }}, title: {{ display: true, text: 'Approval %', color: '#ff4444' }} }},
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
