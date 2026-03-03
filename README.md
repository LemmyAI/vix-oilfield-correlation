# 2026 Iran Conflict Dashboard

🔴 LIVE tracking of VIX volatility, DJT stock, and conflict metrics.

**Live URL:** https://vix-oilfield-correlation.onrender.com

## Tabs

1. **📈 VIX vs Attacks** - Market volatility vs infrastructure strikes
2. **🇺🇸 MAGA vs US KIA** - DJT stock (Trump Media) vs American casualties

## Data Update Process

### ⚠️ IMPORTANT: Always follow this process when updating data

```bash
# 1. Edit the raw CSV files in data/
#    - data/vix_daily.csv        (date, vix)
#    - data/oilfield_attacks.csv (date, cumulative_attacks, attack_type, target)
#    - data/djt_stock.csv        (date, djt_close, djt_volume_m)
#    - data/us_casualties.csv    (date, us_killed, cumulative_killed)

# 2. Run the data pipeline to validate and generate JSON
python3 scripts/parse_data.py

# 3. ⚠️ INSPECT THE OUTPUT CAREFULLY!
#    The script will print a summary like:
#
#    VIX Peak: 23.12 on 2026-03-01
#    DJT Pump: +93% ($18.45 → $35.67)
#    Infrastructure Attacks: 15
#    US KIA: 6
#
#    If these values look wrong, STOP and fix the CSV files!
#    Do NOT commit until the summary is verified.

# 4. If correct, commit and push
git add .
git commit -m "Update data: <brief description>"
git push

# 5. Render will auto-deploy
```

## Data Sources

- **VIX:** Federal Reserve Bank of St. Louis (FRED)
- **DJT Stock:** Market data
- **Casualties:** Official reports, news agencies
- **Attack Data:** Wikipedia, Reuters, AP News

## Architecture

```
├── data/                    # Raw CSV files (edit these)
│   ├── vix_daily.csv
│   ├── oilfield_attacks.csv
│   ├── djt_stock.csv
│   └── us_casualties.csv
├── scripts/
│   └── parse_data.py        # Data pipeline (validate → JSON)
├── static/
│   └── data.json            # Generated JSON (do NOT edit)
├── app.py                   # Flask app
├── Dockerfile
└── requirements.txt         # Only flask + gunicorn (lightweight)
```

## Tech Stack

- **Backend:** Flask (lightweight, no pandas/plotly to avoid build timeouts)
- **Frontend:** Chart.js (loaded from CDN)
- **Deploy:** Render.com free tier

## Adding New Data Points

### VIX (daily)
```csv
date,vix
2026-03-04,21.50
```

### Infrastructure Attacks
```csv
date,attack_type,target,location,cumulative_attacks,description
2026-03-04,missile,Oil terminal,Abqaiq,16,New strike on Saudi facility
```

### DJT Stock
```csv
date,djt_close,djt_volume_m
2026-03-04,27.80,145.2
```

### US Casualties
```csv
date,us_killed,us_injured,cumulative_killed,description
2026-03-04,0,2,6,IED attack on convoy
```

---

Built for tracking the 2026 Iran-Israel conflict (Strait of Hormuz crisis).
