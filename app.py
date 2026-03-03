#!/usr/bin/env python3
"""
VIX vs Oil Infrastructure Attacks - 2026 Iran Conflict (ONGOING)
Started February 28, 2026 - Real-time correlation analysis
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc
import os
from datetime import datetime

# Load data
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
vix_df = pd.read_csv(os.path.join(DATA_DIR, 'vix_daily.csv'), parse_dates=['date'])
attacks_df = pd.read_csv(os.path.join(DATA_DIR, 'oilfield_attacks.csv'), parse_dates=['date'])

# Calculate lag correlation
def calculate_lag_correlation(vix, attacks, max_lag=3):
    correlations = []
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            corr = vix['vix'].iloc[:lag].corr(attacks['cumulative_attacks'].iloc[-lag:].reset_index(drop=True))
        elif lag > 0:
            corr = vix['vix'].iloc[lag:].reset_index(drop=True).corr(attacks['cumulative_attacks'].iloc[:-lag].reset_index(drop=True))
        else:
            corr = vix['vix'].corr(attacks['cumulative_attacks'])
        correlations.append({'lag': lag, 'correlation': corr, 'interpretation': 'VIX leads' if lag > 0 else ('Attacks lead' if lag < 0 else 'Simultaneous')})
    return pd.DataFrame(correlations)

# Merge data
merged_df = pd.merge_asof(vix_df.sort_values('date'), 
                           attacks_df[['date', 'cumulative_attacks']].sort_values('date'),
                           on='date', direction='forward')

# Calculate correlations
correlations = calculate_lag_correlation(vix_df, attacks_df)
simultaneous_corr = correlations[correlations['lag'] == 0]['correlation'].values[0]
best_lag = correlations.loc[correlations['correlation'].abs().idxmax()]

# Calculate prediction
x = merged_df['cumulative_attacks'].values
y = merged_df['vix'].values
mask = ~np.isnan(x)
coefs = np.polyfit(x[mask], y[mask], 1)
predicted_vix = np.polyval(coefs, x)

# Create figure
fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{"secondary_y": True, "rowspan": 2}, {"rowspan": 2}],
        [None, None],
        [{"colspan": 2}, None]
    ],
    row_heights=[0.5, 0.25, 0.25],
    horizontal_spacing=0.08,
    vertical_spacing=0.12
)

# VIX line
fig.add_trace(
    go.Scatter(
        x=vix_df['date'],
        y=vix_df['vix'],
        name='VIX Index',
        line=dict(color='#00d4ff', width=3, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.15)',
        hovertemplate='<b>VIX: %{y:.2f}</b><br>%{date|%b %d}<extra></extra>'
    ),
    row=1, col=1, secondary_y=False
)

# Attacks bars
fig.add_trace(
    go.Bar(
        x=attacks_df['date'],
        y=attacks_df['cumulative_attacks'],
        name='Infrastructure Attacks',
        marker=dict(
            color=attacks_df['cumulative_attacks'],
            colorscale='Reds',
            showscale=False,
            line=dict(color='#ff4444', width=1)
        ),
        opacity=0.85,
        hovertemplate='<b>Attacks: %{y}</b><extra></extra>'
    ),
    row=1, col=1, secondary_y=True
)

# Event markers
events = [
    ('2026-02-28', 22.45, "⚔️ WAR", '#ff0000'),
    ('2026-03-01', 23.12, "🛢️ Hormuz Closed", '#ff6600'),
    ('2026-03-02', 21.44, "🔥 Escalation", '#ffaa00'),
]

for date, vix_val, label, color in events:
    fig.add_annotation(
        x=date, y=vix_val + 1,
        text=label, showarrow=True, arrowhead=2,
        arrowcolor=color, arrowwidth=2, ax=0, ay=-35,
        font=dict(color=color, size=11, family='sans-serif'),
        row=1, col=1
    )

# War shading
fig.add_vrect(x0='2026-02-28', x1='2026-03-04', fillcolor='#ff0000', opacity=0.08, layer='below', row=1, col=1)

# Lag correlation
colors = ['#ff4444' if c > 0 else '#4444ff' for c in correlations['correlation']]
fig.add_trace(
    go.Bar(
        x=correlations['lag'],
        y=correlations['correlation'],
        marker_color=colors,
        name='Lag Correlation',
        hovertemplate='Lag: %{x}d | r: %{y:.3f}<extra></extra>'
    ),
    row=1, col=2
)
fig.add_hline(y=best_lag['correlation'], line_dash='dash', line_color='#00ff00', row=1, col=2,
              annotation_text=f"Best: lag={int(best_lag['lag'])}d, r={best_lag['correlation']:.3f}")

# Prediction chart
fig.add_trace(
    go.Scatter(x=merged_df['date'], y=merged_df['vix'], name='Actual VIX',
               line=dict(color='#00d4ff', width=2), mode='lines+markers'),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(x=merged_df['date'], y=predicted_vix, name='Predicted',
               line=dict(color='#ff6b6b', width=2, dash='dash'), mode='lines'),
    row=3, col=1
)

# Layout
fig.update_layout(
    title={
        'text': '<b>🔴 LIVE: VIX vs Oil Infrastructure Attacks</b><br><sup>2026 Iran Conflict (Feb 28 - present) - Strait of Hormuz Crisis</sup>',
        'x': 0.5, 'xanchor': 'center', 'font': dict(size=22)
    },
    height=900,
    paper_bgcolor='#0a0a0a',
    plot_bgcolor='#1a1a1a',
    font=dict(color='white'),
    legend=dict(orientation='h', y=1.02, x=1, xanchor='right', bgcolor='rgba(0,0,0,0.5)'),
    margin=dict(t=100)
)
fig.update_xaxes(gridcolor='#333', zerolinecolor='#333')
fig.update_yaxes(gridcolor='#333', zerolinecolor='#333')
fig.update_yaxes(title_text='VIX Index', row=1, col=1, secondary_y=False, title_font=dict(color='#00d4ff'))
fig.update_yaxes(title_text='Cumulative Attacks', row=1, col=1, secondary_y=True, title_font=dict(color='#ff4444'))
fig.update_yaxes(title_text='Correlation', row=1, col=2)
fig.update_yaxes(title_text='VIX', row=3, col=1)
fig.update_xaxes(title_text='Lag (Days)', row=1, col=2)
fig.update_xaxes(title_text='Date', row=3, col=1)

# Stats card
stats_card = html.Div([
    html.H2('🔴 LIVE: 2026 Iran Conflict Analysis', style={'color': '#ff4444', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H3('Pearson Correlation', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{simultaneous_corr:.3f}', style={'color': '#00ff00' if abs(simultaneous_corr) > 0.7 else 'orange', 'margin': '0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('VIX Peak', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{vix_df["vix"].max():.2f}', style={'color': '#ff4444', 'margin': '0'}),
            html.P('Mar 1, 2026', style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('Infrastructure Attacks', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{int(attacks_df["cumulative_attacks"].max())}', style={'color': '#ffa500', 'margin': '0'}),
            html.P('Oil & Military', style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('Best Lag', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{int(best_lag["lag"])}d', style={'color': '#00ffff', 'margin': '0'}),
            html.P(f'r = {best_lag["correlation"]:.3f}', style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}),
    
    html.Div([
        html.H3('🚨 CRISIS: Strait of Hormuz', style={'color': '#ff4444', 'marginBottom': '10px'}),
        html.P(
            'Iran has CLOSED the Strait of Hormuz - 20% of global oil supply disrupted. '
            'VIX spiked from 18.5 to 23.12 in 24 hours. This is NOT the 2025 Twelve-Day War - this is happening NOW.',
            style={'fontSize': '16px', 'lineHeight': '1.6', 'margin': '0'}
        ),
    ], style={'padding': '20px', 'backgroundColor': '#2a1515', 'borderRadius': '10px', 'border': '2px solid #ff4444', 'marginBottom': '20px'}),
    
    html.Div([
        html.H3('📊 Key Finding', style={'color': '#00d4ff', 'marginBottom': '10px'}),
        html.P(
            f'{"⚠️ VIX LAGS attacks - Market REACTS to events" if best_lag["lag"] < 0 else "✅ VIX LEADS attacks - Market ANTICIPATES events"} (lag={int(best_lag["lag"])}d, r={best_lag["correlation"]:.3f})',
            style={'fontSize': '18px', 'lineHeight': '1.6', 'margin': '0'}
        ),
        html.P(
            f'Each infrastructure attack correlates with ~{abs(coefs[1]):.2f} VIX point change.',
            style={'fontSize': '14px', 'color': '#888', 'marginTop': '10px'}
        ),
    ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'borderLeft': '4px solid #00d4ff'}),
    
    html.Div([
        html.H3('📅 War Timeline (2026)', style={'color': '#00d4ff', 'marginBottom': '15px'}),
        html.Div([
            html.Div([html.Span('⚔️', style={'fontSize': '24px'}),
                html.Div([html.Strong('Feb 28', style={'color': '#ff0000'}), html.Br(),
                    html.Span('War Begins - Khamenei assassinated', style={'color': '#888'})],
                style={'marginLeft': '10px'})], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div([html.Span('🛢️', style={'fontSize': '24px'}),
                html.Div([html.Strong('Mar 1', style={'color': '#ff6600'}), html.Br(),
                    html.Span('Strait of Hormuz CLOSED', style={'color': '#888'})],
                style={'marginLeft': '10px'})], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div([html.Span('🔥', style={'fontSize': '24px'}),
                html.Div([html.Strong('Mar 2', style={'color': '#ffaa00'}), html.Br(),
                    html.Span('Hezbollah joins, VIX peaks 23.12', style={'color': '#888'})],
                style={'marginLeft': '10px'})], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div([html.Span('📡', style={'fontSize': '24px'}),
                html.Div([html.Strong('Mar 3', style={'color': '#00ffff'}), html.Br(),
                    html.Span('Qatar strikes back - ongoing', style={'color': '#888'})],
                style={'marginLeft': '10px'})], style={'display': 'flex', 'alignItems': 'center'}),
        ]),
    ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'marginTop': '20px'}),
    
    html.Div([
        html.H3('📚 Sources', style={'color': '#00d4ff', 'marginBottom': '10px'}),
        html.Ul([
            html.Li('VIX: Federal Reserve Bank of St. Louis (FRED)', style={'color': '#888'}),
            html.Li('Attack Data: Wikipedia, Reuters, AP News', style={'color': '#888'}),
            html.Li('Conflict: 2026 Iran Conflict (Ongoing)', style={'color': '#888'}),
        ], style={'margin': '0', 'paddingLeft': '20px'}),
    ], style={'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'marginTop': '20px', 'fontSize': '14px'}),
], style={'padding': '20px'})

# App
app = Dash(__name__, title='VIX vs Iran Conflict - LIVE')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1('📈 VIX vs Oil Infrastructure Attacks', 
                style={'textAlign': 'center', 'color': '#ff4444', 'margin': '0', 'fontSize': '32px'}),
        html.P('🔴 LIVE: 2026 Iran Conflict - Strait of Hormuz Crisis', 
                style={'textAlign': 'center', 'color': '#ff6600', 'margin': '5px 0 0 0', 'fontSize': '16px', 'fontWeight': 'bold'}),
    ], style={'padding': '20px', 'backgroundColor': '#0a0a0a'}),
    dcc.Graph(figure=fig, style={'padding': '10px'}),
    stats_card,
], style={'backgroundColor': '#0a0a0a', 'minHeight': '100vh', 'fontFamily': 'system-ui, sans-serif'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
