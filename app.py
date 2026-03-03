#!/usr/bin/env python3
"""
2026 Iran Conflict Dashboard - LIVE Analysis
"""

from flask import Flask, send_from_directory
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

app = Flask(__name__)

# Load data
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
vix_df = pd.read_csv(os.path.join(DATA_DIR, 'vix_daily.csv'), parse_dates=['date'])
attacks_df = pd.read_csv(os.path.join(DATA_DIR, 'oilfield_attacks.csv'), parse_dates=['date'])
djt_df = pd.read_csv(os.path.join(DATA_DIR, 'djt_stock.csv'), parse_dates=['date'])
casualties_df = pd.read_csv(os.path.join(DATA_DIR, 'us_casualties.csv'), parse_dates=['date'])

# Stats
vix_peak = vix_df['vix'].max()
djt_peak = djt_df['djt_close'].max()
djt_pump = ((djt_peak / djt_df['djt_close'].min() - 1) * 100)
us_kia = int(casualties_df['cumulative_killed'].max())
infra_attacks = int(attacks_df['cumulative_attacks'].max())
corr_vix = vix_df['vix'].corr(attacks_df['cumulative_attacks'])
corr_djt = djt_df['djt_close'].corr(casualties_df['cumulative_killed'])

def create_figure():
    fig = make_subplots(
        rows=3, cols=1,
        row_heights=[0.4, 0.3, 0.3],
        vertical_spacing=0.08,
        specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{}]]
    )
    
    # ROW 1: VIX + Attacks
    fig.add_trace(go.Scatter(x=vix_df['date'], y=vix_df['vix'],
        name='VIX', line=dict(color='#00d4ff', width=3),
        fill='tozeroy', fillcolor='rgba(0, 212, 255, 0.1)'),
        row=1, col=1, secondary_y=False)
    fig.add_trace(go.Bar(x=attacks_df['date'], y=attacks_df['cumulative_attacks'],
        name='Attacks', marker_color='#ff4444', opacity=0.7),
        row=1, col=1, secondary_y=True)
    
    # ROW 2: DJT + US KIA
    fig.add_trace(go.Scatter(x=djt_df['date'], y=djt_df['djt_close'],
        name='DJT ($)', line=dict(color='#ff69b4', width=3),
        fill='tozeroy', fillcolor='rgba(255, 105, 180, 0.1)'),
        row=2, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=casualties_df['date'], y=casualties_df['cumulative_killed'],
        name='US KIA', line=dict(color='#0066ff', width=3), mode='lines+markers',
        marker=dict(size=10, color='#0066ff', line=dict(color='white', width=2))),
        row=2, col=1, secondary_y=True)
    
    # ROW 3: DJT Volume
    fig.add_trace(go.Bar(x=djt_df['date'], y=djt_df['djt_volume_m'],
        name='DJT Vol (M)', marker_color='#ff69b4', opacity=0.5),
        row=3, col=1)
    
    # Events
    for date, y, label, color in [
        ('2026-02-28', 22.45, "WAR", '#ff0000'),
        ('2026-03-01', 23.12, "Hormuz", '#ff6600'),
        ('2026-03-02', 21.44, "Escalate", '#ffaa00'),
    ]:
        fig.add_annotation(x=date, y=y+1.5, text=label, showarrow=True,
            arrowhead=2, arrowcolor=color, font=dict(color=color, size=10),
            ax=0, ay=-25, row=1, col=1)
    
    fig.add_vrect(x0='2026-02-28', x1='2026-03-04', fillcolor='#ff0000', opacity=0.05, layer='below')
    
    fig.update_layout(
        title=dict(text='<b>🔴 LIVE: 2026 Iran Conflict Dashboard</b><br><sup>Feb 28 - Present | Strait of Hormuz Crisis</sup>', x=0.5),
        height=800, paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a',
        font=dict(color='white'), showlegend=True,
        legend=dict(orientation='h', y=1.02, x=1, xanchor='right')
    )
    fig.update_xaxes(gridcolor='#333', zerolinecolor='#333')
    fig.update_yaxes(gridcolor='#333', zerolinecolor='#333')
    fig.update_yaxes(title_text='VIX', row=1, col=1, title_font=dict(color='#00d4ff'))
    fig.update_yaxes(title_text='Attacks', row=1, col=1, secondary_y=True, title_font=dict(color='#ff4444'))
    fig.update_yaxes(title_text='DJT ($)', row=2, col=1, title_font=dict(color='#ff69b4'))
    fig.update_yaxes(title_text='US KIA', row=2, col=1, secondary_y=True, title_font=dict(color='#0066ff'))
    fig.update_yaxes(title_text='Volume (M)', row=3, col=1)
    
    return fig

@app.route('/')
def index():
    fig = create_figure()
    plot_html = fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>2026 Iran Conflict Dashboard</title>
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
        .timeline-item {{ margin-bottom: 10px; }}
        .timeline-date {{ font-size: 18px; font-weight: bold; }}
        .correlations {{ font-size: 16px; line-height: 1.8; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔴 LIVE: 2026 Iran Conflict Dashboard</h1>
        <p class="subtitle">Feb 28 - Present | Strait of Hormuz Crisis</p>
        
        {plot_html}
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">VIX Peak</div>
                <p class="stat-value" style="color: #ff4444;">{vix_peak:.2f}</p>
                <div class="stat-sub">Mar 1, 2026</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">DJT Pump</div>
                <p class="stat-value" style="color: #00ff00;">+{djt_pump:.0f}%</p>
                <div class="stat-sub">Peak: ${djt_peak:.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">US KIA</div>
                <p class="stat-value" style="color: #0066ff;">{us_kia}</p>
            </div>
            <div class="stat-box">
                <div class="stat-label">Infra Attacks</div>
                <p class="stat-value" style="color: #ffa500;">{infra_attacks}</p>
            </div>
        </div>
        
        <div class="section">
            <h3>📈 Correlations</h3>
            <div class="correlations">
                <p>VIX vs Attacks: r = {corr_vix:.3f}</p>
                <p>DJT vs US KIA: r = {corr_djt:.3f}</p>
            </div>
        </div>
        
        <div class="section">
            <h3>📅 Timeline</h3>
            <div class="timeline-item"><span class="timeline-date" style="color: #ff0000;">⚔️ Feb 28</span> - War begins, Khamenei assassinated</div>
            <div class="timeline-item"><span class="timeline-date" style="color: #ff6600;">🛢️ Mar 1</span> - Strait of Hormuz CLOSED, DJT peaks</div>
            <div class="timeline-item"><span class="timeline-date" style="color: #ffaa00;">🔥 Mar 2</span> - Hezbollah joins conflict</div>
            <div class="timeline-item"><span class="timeline-date" style="color: #00ffff;">📡 Mar 3</span> - Qatar strikes back, ongoing</div>
        </div>
    </div>
</body>
</html>'''

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
