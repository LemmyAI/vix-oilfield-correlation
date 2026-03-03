# VIX vs Oilfield Attacks Correlation

Visualizes the correlation between the VIX volatility index and oil infrastructure attacks during the **Twelve-Day War** (June 13-24, 2025) between Iran and Israel.

## Live Demo

Deployed at: http://38.242.159.27:10880/vix-oilfield/

## Data Sources

- **VIX**: Federal Reserve Bank of St. Louis (FRED) - CBOE Volatility Index
- **Attack Data**: Wikipedia, news reports, official statements

## Key Findings

- **Correlation Coefficient**: ~0.85 (strong positive correlation)
- **VIX Peak**: 22.17 on June 19, 2025
- **Total Energy Infrastructure Attacks**: 20 documented

## Timeline

| Date | Event | VIX |
|------|-------|-----|
| June 13 | War begins - IDF strikes Natanz | 20.82 |
| June 17 | Escalation continues | 21.60 |
| June 19 | VIX peaks | 22.17 |
| June 22 | US B-2 strikes Fordow | 19.98 |
| June 24 | Ceasefire declared | 17.48 |

## Running Locally

```bash
docker-compose up -d
# Open http://localhost:8050
```

## Tech Stack

- Python 3.11
- Dash/Plotly for visualization
- Pandas for data processing
- Docker for deployment
