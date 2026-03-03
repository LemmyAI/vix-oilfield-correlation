#!/usr/bin/env python3
"""
2026 Iran Conflict Dashboard - LIVE Analysis
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc
import os

# Load data
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

try:
    vix_df = pd.read_csv(os.path.join(DATA_DIR, 'vix_daily.csv'), parse_dates=['date'])
    attacks_df = pd.read_csv(os.path.join(DATA_DIR, 'oilfield_attacks.csv'), parse_dates=['date'])
    djt_df = pd.read_csv(os.path.join(DATA_DIR, 'djt_stock.csv'), parse_dates=['date'])
    casualties_df = pd.read_csv(os.path.join(DATA_DIR, 'us_casualties.csv'), parse_dates=['date'])
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")
    raise

# ========== VIX + MAGA Combined Chart ==========
fig = make_subplots(
    rows=3, cols=1,
    row_heights=[0.4, 0.3, 0.3],
    vertical_spacing=0.08,
    specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{}]]
)

# ROW 1: VIX + Attacks
fig.add_trace(
    go.Scatter(x=vix_df['date'], y=vix_df['vix'],
        name='VIX', line=dict(color='#00d4ff', width=3),
        fill='tozeroy', fillcolor='rgba(0, 212, 255, 0.1)'),
    row=1, col=1, secondary_y=False
)
fig.add_trace(
    go.Bar(x=attacks_df['date'], y=attacks_df['cumulative_attacks'],
        name='Attacks', marker_color='#ff4444', opacity=0.7),
    row=1, col=1, secondary_y=True
)

# ROW 2: DJT + US KIA
fig.add_trace(
    go.Scatter(x=djt_df['date'], y=djt_df['djt_close'],
        name='DJT ($)', line=dict(color='#ff69b4', width=3),
        fill='tozeroy', fillcolor='rgba(255, 105, 180, 0.1)'),
    row=2, col=1, secondary_y=False
)
fig.add_trace(
    go.Scatter(x=casualties_df['date'], y=casualties_df['cumulative_killed'],
        name='US KIA', line=dict(color='#0066ff', width=3), mode='lines+markers',
        marker=dict(size=10, color='#0066ff', line=dict(color='white', width=2))),
    row=2, col=1, secondary_y=True
)

# ROW 3: DJT Volume
fig.add_trace(
    go.Bar(x=djt_df['date'], y=djt_df['djt_volume_m'],
        name='DJT Vol (M)', marker_color='#ff69b4', opacity=0.5),
    row=3, col=1
)

# Events
for date, y, label, color in [
    ('2026-02-28', 22.45, "WAR", '#ff0000'),
    ('2026-03-01', 23.12, "Hormuz", '#ff6600'),
    ('2026-03-02', 21.44, "Escalate", '#ffaa00'),
]:
    fig.add_annotation(x=date, y=y+1.5, text=label, showarrow=True,
        arrowhead=2, arrowcolor=color, font=dict(color=color, size=10),
        ax=0, ay=-25, row=1, col=1)

# War zone shading
fig.add_vrect(x0='2026-02-28', x1='2026-03-04', fillcolor='#ff0000', opacity=0.05, layer='below')

# Layout
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

# Stats
vix_peak = vix_df['vix'].max()
djt_peak = djt_df['djt_close'].max()
djt_pump = ((djt_peak / djt_df['djt_close'].min() - 1) * 100)
us_kia = int(casualties_df['cumulative_killed'].max())
infra_attacks = int(attacks_df['cumulative_attacks'].max())
corr_vix_attacks = vix_df['vix'].corr(attacks_df['cumulative_attacks'])
corr_djt_kia = djt_df['djt_close'].corr(casualties_df['cumulative_killed'])

stats = html.Div([
    html.H2('📊 Conflict Statistics', style={'color': '#00d4ff', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([html.H3('VIX Peak', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{vix_peak:.2f}', style={'color': '#ff4444', 'margin': '0'}),
            html.P('Mar 1, 2026', style={'color': '#666', 'margin': '5px 0 0 0'})],
            style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([html.H3('DJT Pump', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'+{djt_pump:.0f}%', style={'color': '#00ff00', 'margin': '0'}),
            html.P(f'Peak: ${djt_peak:.2f}', style={'color': '#666', 'margin': '5px 0 0 0'})],
            style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([html.H3('US KIA', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{us_kia}', style={'color': '#0066ff', 'margin': '0'})],
            style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([html.H3('Infra Attacks', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{infra_attacks}', style={'color': '#ffa500', 'margin': '0'})],
            style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),
    
    html.Div([
        html.H3('📈 Correlations', style={'color': '#00d4ff', 'marginBottom': '10px'}),
        html.P(f'VIX vs Attacks: r = {corr_vix_attacks:.3f}', style={'margin': '5px 0', 'fontSize': '16px'}),
        html.P(f'DJT vs US KIA: r = {corr_djt_kia:.3f}', style={'margin': '5px 0', 'fontSize': '16px'}),
    ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'marginTop': '20px'}),
    
    html.Div([
        html.H3('📅 Timeline', style={'color': '#00d4ff', 'marginBottom': '15px'}),
        html.Div([html.Span('⚔️ Feb 28', style={'color': '#ff0000', 'fontSize': '18px'}), ' - War begins, Khamenei assassinated'], style={'marginBottom': '8px'}),
        html.Div([html.Span('🛢️ Mar 1', style={'color': '#ff6600', 'fontSize': '18px'}), ' - Strait of Hormuz CLOSED, DJT peaks'], style={'marginBottom': '8px'}),
        html.Div([html.Span('🔥 Mar 2', style={'color': '#ffaa00', 'fontSize': '18px'}), ' - Hezbollah joins conflict'], style={'marginBottom': '8px'}),
        html.Div([html.Span('📡 Mar 3', style={'color': '#00ffff', 'fontSize': '18px'}), ' - Qatar strikes back, ongoing'], style={'marginBottom': '8px'}),
    ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'marginTop': '20px'}),
], style={'padding': '20px'})

# App
app = Dash(__name__, title='2026 Iran Conflict')
server = app.server

app.layout = html.Div([
    dcc.Graph(figure=fig, style={'padding': '10px'}),
    stats,
], style={'backgroundColor': '#0a0a0a', 'minHeight': '100vh', 'fontFamily': 'system-ui, sans-serif'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
