#!/usr/bin/env python3
"""
VIX vs Oilfield Attacks Correlation Visualization
Twelve-Day War (June 13-24, 2025) - Iran-Israel Conflict
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc
import os

# Load data
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
vix_df = pd.read_csv(os.path.join(DATA_DIR, 'vix_daily.csv'), parse_dates=['date'])
attacks_df = pd.read_csv(os.path.join(DATA_DIR, 'oilfield_attacks.csv'), parse_dates=['date'])

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add VIX line
fig.add_trace(
    go.Scatter(
        x=vix_df['date'],
        y=vix_df['vix'],
        name='VIX Index',
        line=dict(color='#00d4ff', width=3),
        hovertemplate='VIX: %{y:.2f}<br>Date: %{date}<extra></extra>'
    ),
    secondary_y=False
)

# Add cumulative attacks as bars
fig.add_trace(
    go.Bar(
        x=attacks_df['date'],
        y=attacks_df['cumulative_attacks'],
        name='Cumulative Attacks',
        marker_color='#ff4444',
        opacity=0.7,
        hovertemplate='Attacks: %{y}<extra></extra>'
    ),
    secondary_y=True
)

# Annotate key events
annotations = [
    dict(x='2025-06-13', y=21, text="⚠️ War Starts", showarrow=True, arrowhead=2, ax=0, ay=-40, font=dict(color='yellow')),
    dict(x='2025-06-19', y=22.5, text="📈 Peak VIX (22.17)", showarrow=True, arrowhead=2, ax=0, ay=-40, font=dict(color='#00ff00')),
    dict(x='2025-06-24', y=18, text="🕊️ Ceasefire", showarrow=True, arrowhead=2, ax=0, ay=-40, font=dict(color='cyan')),
]

for ann in annotations:
    fig.add_annotation(ann)

# Update layout
fig.update_layout(
    title={
        'text': '<b>VIX Index vs Oilfield Attacks</b><br><sup>Twelve-Day War (June 13-24, 2025) - Iran-Israel Conflict</sup>',
        'x': 0.5,
        'xanchor': 'center',
        'font': dict(size=20)
    },
    xaxis_title='Date',
    yaxis_title='VIX Index',
    yaxis2_title='Cumulative Attacks',
    hovermode='x unified',
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.5)'),
    template='plotly_dark',
    height=700,
    paper_bgcolor='#0a0a0a',
    plot_bgcolor='#1a1a1a'
)

fig.update_yaxes(title_text="VIX Index", secondary_y=False, gridcolor='#333')
fig.update_yaxes(title_text="Cumulative Attacks", secondary_y=True, gridcolor='#333')

# Calculate correlation
merged = pd.merge_asof(vix_df.sort_values('date'), 
                        attacks_df[['date', 'cumulative_attacks']].sort_values('date'),
                        on='date',
                        direction='forward')
correlation = merged['vix'].corr(merged['cumulative_attacks'])

# Create summary stats
stats = html.Div([
    html.H3('📊 Correlation Analysis', style={'color': '#00d4ff'}),
    html.P(f'Pearson Correlation Coefficient: {correlation:.3f}', style={'fontSize': '18px', 'color': '#00ff00' if correlation > 0.7 else 'orange'}),
    html.P(f'VIX Peak: {vix_df["vix"].max():.2f} (June 19, 2025)'),
    html.P(f'VIX at War Start: 20.82 (June 13, 2025)'),
    html.P(f'VIX at Ceasefire: 17.48 (June 24, 2025)'),
    html.P(f'Total Energy Infrastructure Attacks: {attacks_df["cumulative_attacks"].max()}'),
    html.H3('📅 Key Events', style={'color': '#00d4ff', 'marginTop': '20px'}),
    html.Ul([
        html.Li('June 13: IDF launches Operation Rising Lion - strikes Natanz'),
        html.Li('June 14-17: Escalation - multiple energy targets hit'),
        html.Li('June 19: VIX peaks at 22.17'),
        html.Li('June 22: US B-2 bombers strike Fordow'),
        html.Li('June 24: Ceasefire declared'),
    ], style={'lineHeight': '1.8'})
], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '20px'})

# Dash app
app = Dash(__name__, title='VIX vs Oilfield Attacks')
server = app.server  # For gunicorn

app.layout = html.Div([
    html.H1('📈 VIX vs Oilfield Attacks Correlation', 
            style={'textAlign': 'center', 'color': '#00d4ff', 'marginBottom': '10px'}),
    html.P('Twelve-Day War (June 2025) - Analysis of market volatility correlation with energy infrastructure attacks', 
            style={'textAlign': 'center', 'color': '#888'}),
    dcc.Graph(figure=fig),
    html.Div([
        stats
    ], style={'display': 'flex', 'justifyContent': 'center'}),
    html.Div([
        html.H3('📚 Data Sources', style={'color': '#00d4ff'}),
        html.Ul([
            html.Li('VIX Data: Federal Reserve Bank of St. Louis (FRED)'),
            html.Li('Attack Data: Wikipedia, News Reports, Official Statements'),
            html.Li('Conflict: 2025 Iran-Israel War (Twelve-Day War)'),
        ])
    ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'marginTop': '20px'})
], style={'backgroundColor': '#0a0a0a', 'color': 'white', 'minHeight': '100vh', 'padding': '20px', 'fontFamily': 'sans-serif'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
