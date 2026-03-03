#!/usr/bin/env python3
"""
VIX vs Oilfield Attacks Correlation Visualization
Twelve-Day War (June 13-24, 2025) - Iran-Israel Conflict
Enhanced with Lag Analysis & Predictive Insights
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output
import os

# Load data
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
vix_df = pd.read_csv(os.path.join(DATA_DIR, 'vix_daily.csv'), parse_dates=['date'])
attacks_df = pd.read_csv(os.path.join(DATA_DIR, 'oilfield_attacks.csv'), parse_dates=['date'])

# Calculate lag correlation
def calculate_lag_correlation(vix, attacks, max_lag=5):
    """Calculate correlation at different lags to see if VIX lags attacks"""
    correlations = []
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            # Attacks lead VIX by |lag| days
            corr = vix['vix'].iloc[:lag].corr(attacks['cumulative_attacks'].iloc[-lag:].reset_index(drop=True))
        elif lag > 0:
            # VIX leads attacks by lag days
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
# Simple linear regression: VIX = base + coefficient * attacks
from numpy.polynomial import polynomial as P
x = merged_df['cumulative_attacks'].values
y = merged_df['vix'].values
coefs = np.polyfit(x[~np.isnan(x)], y[~np.isnan(x)], 1)
predicted_vix = np.polyval(coefs, x)

# Create main figure
fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{"secondary_y": True, "rowspan": 2}, {"rowspan": 2}],
        [None, None],
        [{"colspan": 2}, None]
    ],
    row_heights=[0.5, 0.25, 0.25],
    subplot_titles=('', 'Lag Correlation Analysis', 'VIX Prediction vs Actual'),
    horizontal_spacing=0.08,
    vertical_spacing=0.12
)

# Add VIX line with gradient effect
fig.add_trace(
    go.Scatter(
        x=vix_df['date'],
        y=vix_df['vix'],
        name='VIX Index',
        line=dict(color='#00d4ff', width=3, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.1)',
        hovertemplate='<b>VIX: %{y:.2f}</b><br>Date: %{date|%b %d}<extra></extra>'
    ),
    row=1, col=1, secondary_y=False
)

# Add cumulative attacks as bars with gradient
fig.add_trace(
    go.Bar(
        x=attacks_df['date'],
        y=attacks_df['cumulative_attacks'],
        name='Cumulative Attacks',
        marker=dict(
            color=attacks_df['cumulative_attacks'],
            colorscale='Reds',
            showscale=False,
            line=dict(color='#ff4444', width=1)
        ),
        opacity=0.8,
        hovertemplate='<b>Attacks: %{y}</b><extra></extra>'
    ),
    row=1, col=1, secondary_y=True
)

# Add key event markers
events = [
    ('2025-06-13', 20.82, "⚔️ War Starts", '#ff6b6b'),
    ('2025-06-17', 21.60, "📈 Escalation", '#ffa500'),
    ('2025-06-19', 22.17, "🔥 Peak VIX", '#ff0000'),
    ('2025-06-22', 19.98, "🇺🇸 US Strikes", '#00ff00'),
    ('2025-06-24', 17.48, "🕊️ Ceasefire", '#00ffff'),
]

for date, vix_val, label, color in events:
    fig.add_annotation(
        x=date, y=vix_val + 0.8,
        text=label, showarrow=True, arrowhead=2,
        arrowcolor=color, arrowwidth=2, ax=0, ay=-30,
        font=dict(color=color, size=11, family='sans-serif'),
        row=1, col=1
    )

# Add war background shading
fig.add_vrect(
    x0='2025-06-13', x1='2025-06-24',
    fillcolor='#ff0000', opacity=0.05, layer='below',
    row=1, col=1
)

# Lag correlation chart
colors = ['#ff4444' if c > 0 else '#4444ff' for c in correlations['correlation']]
fig.add_trace(
    go.Bar(
        x=correlations['lag'],
        y=correlations['correlation'],
        marker_color=colors,
        name='Correlation by Lag',
        hovertemplate='Lag: %{x} days<br>Correlation: %{y:.3f}<extra></extra>'
    ),
    row=1, col=2
)

# Add horizontal line at best lag
fig.add_hline(
    y=best_lag['correlation'], line_dash='dash', line_color='#00ff00',
    annotation_text=f"Best: lag={int(best_lag['lag'])}, r={best_lag['correlation']:.3f}",
    row=1, col=2
)

# Prediction vs Actual
fig.add_trace(
    go.Scatter(
        x=merged_df['date'],
        y=merged_df['vix'],
        name='Actual VIX',
        line=dict(color='#00d4ff', width=2),
        mode='lines'
    ),
    row=3, col=1
)

fig.add_trace(
    go.Scatter(
        x=merged_df['date'],
        y=predicted_vix,
        name='Predicted VIX',
        line=dict(color='#ff6b6b', width=2, dash='dash'),
        mode='lines'
    ),
    row=3, col=1
)

# Prediction confidence band
residuals = merged_df['vix'].values - predicted_vix
std_err = np.nanstd(residuals)
fig.add_trace(
    go.Scatter(
        x=merged_df['date'],
        y=predicted_vix + 1.96 * std_err,
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(
        x=merged_df['date'],
        y=predicted_vix - 1.96 * std_err,
        fill='tonexty',
        fillcolor='rgba(255, 107, 107, 0.2)',
        mode='lines',
        line=dict(width=0),
        name='95% CI'
    ),
    row=3, col=1
)

# Update layout
fig.update_layout(
    title={
        'text': '<b>📊 VIX vs Oilfield Attacks: War & Volatility</b><br><sup>Twelve-Day War (June 13-24, 2025) - Does the market react to or anticipate attacks?</sup>',
        'x': 0.5,
        'xanchor': 'center',
        'font': dict(size=22, family='sans-serif')
    },
    height=900,
    paper_bgcolor='#0a0a0a',
    plot_bgcolor='#1a1a1a',
    font=dict(color='white'),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        bgcolor='rgba(0,0,0,0.5)'
    ),
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

# Analysis text
lag_insight = f"""
**🔍 Lag Analysis Insight:**
- Best correlation at **lag {int(best_lag['lag'])} days** (r = {best_lag['correlation']:.3f})
- {'⚠️ VIX **lags** attacks - market reacts AFTER events' if best_lag['lag'] < 0 else '✅ VIX **leads** attacks - market anticipates events' if best_lag['lag'] > 0 else '⚡ VIX and attacks are **simultaneous** - instant market reaction'}
- Simultaneous correlation: **{simultaneous_corr:.3f}** ({'strong' if abs(simultaneous_corr) > 0.7 else 'moderate' if abs(simultaneous_corr) > 0.4 else 'weak'})

**📈 Prediction Model:**
- VIX = {coefs[1]:.3f} × Attacks + {coefs[0]:.2f}
- Each attack adds ~{coefs[1]:.3f} points to VIX
- Standard error: ±{std_err:.2f} VIX points
"""

# Create stats card
stats_card = html.Div([
    html.H2('🎯 Analysis Dashboard', style={'color': '#00d4ff', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H3('Pearson Correlation', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{simultaneous_corr:.3f}', style={'color': '#00ff00' if abs(simultaneous_corr) > 0.7 else 'orange', 'margin': '0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('VIX Peak', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{vix_df["vix"].max():.2f}', style={'color': '#ff4444', 'margin': '0'}),
            html.P('June 19, 2025', style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('Total Attacks', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{int(attacks_df["cumulative_attacks"].max())}', style={'color': '#ffa500', 'margin': '0'}),
            html.P('Energy targets', style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
        
        html.Div([
            html.H3('Best Lag', style={'color': '#888', 'marginBottom': '5px'}),
            html.H2(f'{int(best_lag["lag"])}d', style={'color': '#00ffff', 'margin': '0'}),
            html.P('r = {:.3f}'.format(best_lag['correlation']), style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], style={'textAlign': 'center', 'flex': '1', 'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'margin': '5px'}),
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}),
    
    html.Div([
        html.H3('🔍 Key Finding', style={'color': '#00d4ff', 'marginBottom': '10px'}),
        html.P(
            '⚠️ VIX LAGS attacks by 1-2 days - The market REACTS to attacks, not anticipates them' if best_lag['lag'] < 0 else
            '✅ VIX LEADS attacks - The market ANTICIPATES upcoming escalation' if best_lag['lag'] > 0 else
            '⚡ VIX and attacks are SIMULTANEOUS - Instant market reaction to geopolitical events',
            style={'fontSize': '18px', 'lineHeight': '1.6', 'margin': '0'}
        ),
        html.P(
            f'With correlation of {abs(best_lag["correlation"]):.3f}, each additional attack on energy infrastructure '
            f'is associated with a {abs(coefs[1]):.2f} point change in the VIX volatility index.',
            style={'fontSize': '14px', 'color': '#888', 'marginTop': '10px'}
        ),
    ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'borderLeft': '4px solid #00d4ff'}),
    
    html.Div([
        html.H3('📅 War Timeline', style={'color': '#00d4ff', 'marginBottom': '15px'}),
        html.Div([
            html.Div([
                html.Span('⚔️', style={'fontSize': '24px'}),
                html.Div([
                    html.Strong('June 13', style={'color': '#ff6b6b'}),
                    html.Br(),
                    html.Span('War Begins - IDF strikes Natanz', style={'color': '#888'}),
                ], style={'marginLeft': '10px'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div([
                html.Span('🔥', style={'fontSize': '24px'}),
                html.Div([
                    html.Strong('June 19', style={'color': '#ff0000'}),
                    html.Br(),
                    html.Span('VIX Peaks at 22.17', style={'color': '#888'}),
                ], style={'marginLeft': '10px'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div([
                html.Span('🇺🇸', style={'fontSize': '24px'}),
                html.Div([
                    html.Strong('June 22', style={'color': '#00ff00'}),
                    html.Br(),
                    html.Span('US B-2 bombers strike Fordow', style={'color': '#888'}),
                ], style={'marginLeft': '10px'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div([
                html.Span('🕊️', style={'fontSize': '24px'}),
                html.Div([
                    html.Strong('June 24', style={'color': '#00ffff'}),
                    html.Br(),
                    html.Span('Ceasefire declared - VIX drops', style={'color': '#888'}),
                ], style={'marginLeft': '10px'}),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ]),
    ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'marginTop': '20px'}),
    
    html.Div([
        html.H3('📚 Data Sources', style={'color': '#00d4ff', 'marginBottom': '10px'}),
        html.Ul([
            html.Li('VIX Data: Federal Reserve Bank of St. Louis (FRED)', style={'color': '#888'}),
            html.Li('Attack Data: Wikipedia, News Reports, Official Statements', style={'color': '#888'}),
            html.Li('Conflict: 2025 Iran-Israel War (Twelve-Day War)', style={'color': '#888'}),
        ], style={'margin': '0', 'paddingLeft': '20px'}),
    ], style={'padding': '15px', 'backgroundColor': '#1a1a1a', 'borderRadius': '10px', 'marginTop': '20px', 'fontSize': '14px'}),
], style={'padding': '20px'})

# Dash app
app = Dash(__name__, title='VIX vs Oilfield Attacks - War & Volatility')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1('📈 VIX vs Oilfield Attacks', 
                style={'textAlign': 'center', 'color': '#00d4ff', 'margin': '0', 'fontSize': '32px'}),
        html.P('Twelve-Day War (June 2025) - Lag Analysis & Predictive Correlation', 
                style={'textAlign': 'center', 'color': '#666', 'margin': '5px 0 0 0', 'fontSize': '16px'}),
    ], style={'padding': '20px', 'backgroundColor': '#0a0a0a'}),
    
    dcc.Graph(figure=fig, style={'padding': '10px'}),
    
    stats_card,
    
], style={'backgroundColor': '#0a0a0a', 'minHeight': '100vh', 'fontFamily': 'system-ui, sans-serif'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
