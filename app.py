#!/usr/bin/env python3
"""
2026 Iran Conflict Dashboard - LIVE Analysis
Tab 1: VIX vs Oil Infrastructure Attacks
Tab 2: MAGA Index (DJT Stock) vs US Casualties
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output
import os

# Load all data
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
vix_df = pd.read_csv(os.path.join(DATA_DIR, 'vix_daily.csv'), parse_dates=['date'])
attacks_df = pd.read_csv(os.path.join(DATA_DIR, 'oilfield_attacks.csv'), parse_dates=['date'])
djt_df = pd.read_csv(os.path.join(DATA_DIR, 'djt_stock.csv'), parse_dates=['date'])
casualties_df = pd.read_csv(os.path.join(DATA_DIR, 'us_casualties.csv'), parse_dates=['date'])

# ========== CHART 1: VIX vs Attacks ==========
def create_vix_chart():
    merged = pd.merge_asof(vix_df.sort_values('date'), 
                           attacks_df[['date', 'cumulative_attacks']].sort_values('date'),
                           on='date', direction='forward')
    
    # Correlation
    corr = vix_df['vix'].corr(attacks_df['cumulative_attacks'])
    
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.08
    )
    
    # VIX
    fig.add_trace(
        go.Scatter(x=vix_df['date'], y=vix_df['vix'],
            name='VIX Index',
            line=dict(color='#00d4ff', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(0, 212, 255, 0.15)',
            hovertemplate='<b>VIX: %{y:.2f}</b><extra></extra>'),
        row=1, col=1
    )
    
    # Attacks
    fig.add_trace(
        go.Bar(x=attacks_df['date'], y=attacks_df['cumulative_attacks'],
            name='Infra Attacks',
            marker=dict(color='#ff4444', opacity=0.8),
            hovertemplate='<b>Attacks: %{y}</b><extra></extra>'),
        row=1, col=1, secondary_y=True
    )
    
    # Events
    events = [
        ('2026-02-28', 22.45, "⚔️ WAR", '#ff0000'),
        ('2026-03-01', 23.12, "🛢️ Hormuz", '#ff6600'),
        ('2026-03-02', 21.44, "🔥 Escalate", '#ffaa00'),
    ]
    for date, vix, label, color in events:
        fig.add_annotation(x=date, y=vix+1.5, text=label, showarrow=True,
            arrowhead=2, arrowcolor=color, font=dict(color=color, size=11),
            ax=0, ay=-30, row=1, col=1)
    
    # War shading
    fig.add_vrect(x0='2026-02-28', x1='2026-03-04', fillcolor='#ff0000', opacity=0.08, layer='below', row=1, col=1)
    
    # Correlation bar
    fig.add_trace(
        go.Bar(x=['VIX vs Attacks'], y=[corr],
            marker_color='#00ff00' if corr > 0.7 else 'orange',
            text=f'r = {corr:.3f}', textposition='auto',
            name='Correlation'),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600, paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a',
        font=dict(color='white'), showlegend=True,
        legend=dict(orientation='h', y=1.02, x=1, xanchor='right'),
        margin=dict(t=60)
    )
    fig.update_xaxes(gridcolor='#333', zerolinecolor='#333')
    fig.update_yaxes(gridcolor='#333', zerolinecolor='#333')
    fig.update_yaxes(title_text='VIX', row=1, col=1, title_font=dict(color='#00d4ff'))
    fig.update_yaxes(title_text='Cumulative Attacks', row=1, col=1, secondary_y=True, title_font=dict(color='#ff4444'))
    
    return fig

# ========== CHART 2: DJT vs US Casualties ==========
def create_maga_chart():
    merged = pd.merge_asof(djt_df.sort_values('date'),
                           casualties_df[['date', 'cumulative_killed']].sort_values('date'),
                           on='date', direction='forward')
    
    corr = djt_df['djt_close'].corr(casualties_df['cumulative_killed'])
    
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.08,
        specs=[[{"secondary_y": True}], [{}]]
    )
    
    # DJT Stock
    fig.add_trace(
        go.Scatter(x=djt_df['date'], y=djt_df['djt_close'],
            name='DJT Stock ($)',
            line=dict(color='#ff69b4', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(255, 105, 180, 0.15)',
            hovertemplate='<b>DJT: $%{y:.2f}</b><extra></extra>'),
        row=1, col=1, secondary_y=False
    )
    
    # Volume
    fig.add_trace(
        go.Bar(x=djt_df['date'], y=djt_df['djt_volume_m'],
            name='Volume (M)',
            marker=dict(color='#ff69b4', opacity=0.3),
            hovertemplate='<b>Vol: %{y}M</b><extra></extra>'),
        row=1, col=1, secondary_y=True
    )
    
    # US Casualties
    fig.add_trace(
        go.Scatter(x=casualties_df['date'], y=casualties_df['cumulative_killed'],
            name='US KIA',
            line=dict(color='#0066ff', width=3),
            mode='lines+markers',
            marker=dict(size=10, color='#0066ff', line=dict(color='white', width=2)),
            hovertemplate='<b>US KIA: %{y}</b><extra></extra>'),
        row=1, col=1, secondary_y=False
    )
    
    # Events
    events = [
        ('2026-02-28', 31.45, "⚔️ War Start", '#ff0000'),
        ('2026-03-01', 35.67, "🚀 DJT Peak", '#00ff00'),
        ('2026-03-03', 28.45, "📉 Pullback", '#ffaa00'),
    ]
    for date, djt, label, color in events:
        fig.add_annotation(x=date, y=djt+2, text=label, showarrow=True,
            arrowhead=2, arrowcolor=color, font=dict(color=color, size=11),
            ax=0, ay=-35, row=1, col=1)
    
    # War shading
    fig.add_vrect(x0='2026-02-28', x1='2026-03-04', fillcolor='#ff0000', opacity=0.08, layer='below', row=1, col=1)
    
    # Correlation
    fig.add_trace(
        go.Bar(x=['DJT vs US KIA'], y=[corr],
            marker_color='#ff69b4' if corr > 0 else '#0066ff',
            text=f'r = {corr:.3f}', textposition='auto'),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600, paper_bgcolor='#0a0a0a', plot_bgcolor='#1a1a1a',
        font=dict(color='white'), showlegend=True,
        legend=dict(orientation='h', y=1.02, x=1, xanchor='right'),
        margin=dict(t=60)
    )
    fig.update_xaxes(gridcolor='#333', zerolinecolor='#333')
    fig.update_yaxes(gridcolor='#333', zerolinecolor='#333')
    fig.update_yaxes(title_text='DJT ($)', row=1, col=1, secondary_y=False, title_font=dict(color='#ff69b4'))
    fig.update_yaxes(title_text='Volume (M)', row=1, col=1, secondary_y=True, title_font=dict(color='#ff69b4', opacity=0.5))
    
    return fig

# ========== STATS CARDS ==========
vix_stats = html.Div([
    html.H2('📊 VIX vs Infrastructure Attacks', style={'color': '#00d4ff', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H3('Pearson r', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{vix_df["vix"].corr(attacks_df["cumulative_attacks"]):.3f}', style={'color': '#00ff00', 'margin': '0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('VIX Peak', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{vix_df["vix"].max():.2f}', style={'color': '#ff4444', 'margin': '0'}),
            html.P('Mar 1, 2026', style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('Infra Attacks', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{int(attacks_df["cumulative_attacks"].max())}', style={'color': '#ffa500', 'margin': '0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('Strait Hormuz', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2('CLOSED', style={'color': '#ff0000', 'margin': '0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),
], style={'padding': '20px'})

maga_stats = html.Div([
    html.H2('🇺🇸 MAGA Index vs US Casualties', style={'color': '#ff69b4', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H3('DJT Peak', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'${djt_df["djt_close"].max():.2f}', style={'color': '#00ff00', 'margin': '0'}),
            html.P('Mar 1, 2026', style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('US KIA', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{int(casualties_df["cumulative_killed"].max())}', style={'color': '#0066ff', 'margin': '0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('Peak Volume', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{djt_df["djt_volume_m"].max():.0f}M', style={'color': '#ff69b4', 'margin': '0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('Correlation', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{djt_df["djt_close"].corr(casualties_df["cumulative_killed"]):.3f}', style={'color': '#ffaa00', 'margin': '0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),
    
    html.Div([
        html.H3('🧠 Analysis', style={'color': '#ff69b4', 'marginBottom': '10px'}),
        html.P(
            f'DJT (Trump Media stock) surged {((djt_df["djt_close"].max() / djt_df["djt_close"].min() - 1) * 100):.0f}% '
            f'from ${djt_df["djt_close"].min():.2f} to ${djt_df["djt_close"].max():.2f} during the conflict. '
            f'Each US casualty correlates with DJT movement. MAGA sentiment tracks with war events.',
            style={'fontSize': '16px', 'lineHeight': '1.6', 'margin': '0'}
        ),
    ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'borderLeft': '4px solid #ff69b4', 'marginTop': '20px'}),
], style={'padding': '20px'})

timeline = html.Div([
    html.H3('📅 War Timeline (2026)', style={'color': '#00d4ff', 'marginBottom': '15px'}),
    html.Div([
        html.Div([html.Span('⚔️', style={'fontSize': '24px'}),
            html.Div([html.Strong('Feb 28', style={'color': '#ff0000'}), html.Br(),
                html.Span('War Begins - Khamenei killed, US bases hit', style={'color': '#888'})],
            style={'marginLeft': '10px'})], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
        html.Div([html.Span('🛢️', style={'fontSize': '24px'}),
            html.Div([html.Strong('Mar 1', style={'color': '#ff6600'}), html.Br(),
                html.Span('Strait of Hormuz CLOSED, DJT peaks $35.67', style={'color': '#888'})],
            style={'marginLeft': '10px'})], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
        html.Div([html.Span('🔥', style={'color': '#ffaa00', 'fontSize': '24px'}),
            html.Div([html.Strong('Mar 2', style={'color': '#ffaa00'}), html.Br(),
                html.Span('Hezbollah joins, VIX at 21.44', style={'color': '#888'})],
            style={'marginLeft': '10px'})], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
        html.Div([html.Span('📡', style={'fontSize': '24px'}),
            html.Div([html.Strong('Mar 3', style={'color': '#00ffff'}), html.Br(),
                html.Span('Qatar strikes back - ongoing', style={'color': '#888'})],
            style={'marginLeft': '10px'})], style={'display': 'flex', 'alignItems': 'center'}),
    ]),
], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'marginTop': '20px'})

# ========== APP ==========
app = Dash(__name__, title='2026 Iran Conflict Dashboard')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1('🔴 LIVE: 2026 Iran Conflict Dashboard', 
                style={'textAlign': 'center', 'color': '#ff4444', 'margin': '0', 'fontSize': '28px'}),
        html.P('Started Feb 28, 2026 - Strait of Hormuz Crisis', 
                style={'textAlign': 'center', 'color': '#ff6600', 'margin': '5px 0 0 0', 'fontSize': '14px'}),
    ], style={'padding': '15px', 'backgroundColor': '#0a0a0a'}),
    
    dcc.Tabs(id='tabs', value='tab-vix', children=[
        dcc.Tab(label='📈 VIX vs Attacks', value='tab-vix', style={'backgroundColor': '#1a1a1a', 'color': '#00d4ff'}, selected_style={'backgroundColor': '#00d4ff', 'color': '#000'}),
        dcc.Tab(label='🇺🇸 MAGA vs US KIA', value='tab-maga', style={'backgroundColor': '#1a1a1a', 'color': '#ff69b4'}, selected_style={'backgroundColor': '#ff69b4', 'color': '#000'}),
    ], style={'backgroundColor': '#0a0a0a', 'borderBottom': '1px solid #333'}),
    
    html.Div(id='tab-content'),
], style={'backgroundColor': '#0a0a0a', 'minHeight': '100vh', 'fontFamily': 'system-ui, sans-serif'})

@app.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_tab(tab):
    if tab == 'tab-vix':
        return html.Div([
            dcc.Graph(figure=create_vix_chart(), style={'padding': '10px'}),
            vix_stats,
            timeline,
        ])
    else:
        return html.Div([
            dcc.Graph(figure=create_maga_chart(), style={'padding': '10px'}),
            maga_stats,
            timeline,
        ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
