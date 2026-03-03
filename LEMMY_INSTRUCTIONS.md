# Iran Wars Dashboard - Lemmy Instructions

> **For Lemmy (AI Assistant)**: This file contains all instructions for maintaining and updating this dashboard.

## Project Overview

**Live URL**: https://vix-oilfield-correlation.onrender.com
**Local Path**: `~/projects/vix-oilfield-correlation/`

A cynical data visualization dashboard tracking strange correlations during the 2026 Iran Conflict:
- **VIX vs Attacks**: Market volatility vs infrastructure destruction
- **MAGA vs KIA**: DJT stock vs American casualties  
- **Hidden QE vs Deaths**: Fed RRP operations vs conflict mortality

---

## Daily Data Update Workflow

### 1. Update CSV Files

All data lives in `data/` directory as CSV files:

| File | Columns | Source |
|------|---------|--------|
| `vix_daily.csv` | `date,vix` | https://fred.stlouisfed.org/series/VIXCLS |
| `oilfield_attacks.csv` | `date,attack_type,target,location,cumulative_attacks,description` | News reports (Reuters, AP) |
| `djt_stock.csv` | `date,djt_close,djt_volume_m` | Yahoo Finance (DJT), MarketWatch |
| `us_casualties.csv` | `date,killed,cumulative_killed` | DoD briefings, Reuters |
| `rrp_operations.csv` | `date,rrp_billion` | https://www.newyorkfed.org/markets/omo_transaction_data#reverse-repo |
| `conflict_deaths.csv` | `date,iran_deaths,israel_deaths,us_deaths,civilian_deaths,cumulative_total,notes` | Iran Health Ministry, IDF, UN |

### 2. Run Data Pipeline

```bash
cd ~/projects/vix-oilfield-correlation
python3 scripts/parse_data.py
```

This validates all CSVs and generates `static/data.json` with aligned data.

### 3. Review Output

The script prints a summary like:
```
VIX Peak: 23.12 on 2026-03-01
DJT Pump: +93% ($18.45 → $35.67)
RRP Drop: $177.9B ($423.5B → $245.6B)
Infrastructure Attacks: 15
US KIA: 6
Total Conflict Deaths: 1,772
```

### 4. Deploy

```bash
git add . && git commit -m "Update data to YYYY-MM-DD" && git push
```

Render auto-deploys on push. Verify at live URL.

---

## Adding a New Tab

To add a 4th tab (e.g., "Oil Price vs Inflation"):

### 1. Create Data CSV

Create `data/oil_price.csv`:
```csv
date,price_brent,price_wti
2026-02-18,78.50,74.20
...
```

### 2. Add Parser Function

Edit `scripts/parse_data.py`, add:
```python
def parse_oil():
    filepath = os.path.join(DATA_DIR, 'oil_price.csv')
    data = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[format_date(parse_date(row['date']))] = {
                'brent': parse_float(row['price_brent']),
                'wti': parse_float(row['price_wti'])
            }
    return data
```

Call it in `main()`, add to aligned arrays, include in output JSON.

### 3. Add HTML Tab

In `app.py`, add to `.tabs` div:
```html
<div class="tab" id="tab-oil" onclick="showTab('oil')">
    <div class="tab-title">🛢️ Oil vs Inflation</div>
    <div class="tab-desc">Commodity chaos</div>
</div>
```

### 4. Add Stats Section

Add `<div class="stats" id="stats-oil">...</div>` with 4 stat boxes.

### 5. Add Chart Container

Add `<div class="chart-container" id="chart-oil">...</div>` with canvas and sources.

### 6. Add JavaScript Chart

In the `<script>` section:
```javascript
// Oil Chart
new Chart(document.getElementById('oilCanvas').getContext('2d'), {
    type: 'line',
    data: {
        labels: dates,
        datasets: [
            { label: 'Brent', data: oilData, ... },
            { label: 'WTI', data: wtiData, ... }
        ]
    },
    options: { ... }
});
```

### 7. Deploy

Test locally first:
```bash
python3 app.py
# Open http://localhost:10000
# Check all tabs work
```

Then push to deploy.

---

## Key Files

```
├── app.py                      # Main Flask app + all HTML/JS
├── scripts/parse_data.py       # Data validation pipeline
├── data/*.csv                   # Raw data (EDIT THESE)
├── static/data.json            # Generated (DO NOT EDIT)
├── requirements.txt            # Just flask + gunicorn
├── Dockerfile                   # Python 3.11 slim
└── LEMMY_INSTRUCTIONS.md        # This file
```

---

## Current Stats (Mar 3, 2026)

| Metric | Value |
|--------|-------|
| VIX Peak | 23.12 |
| DJT Pump | +93% |
| RRP Drop | $178B |
| Attacks | 15 |
| US KIA | 6 |
| Total Deaths | 1,772 |

---

## Troubleshooting

**Charts not showing?** Check browser console for JS errors. Usually a missing data variable or typo.

**Tab switching broken?** Ensure `showTab()` function exists and tab IDs match (`tab-vix`, `tab-maga`, `tab-rrp`).

**Data mismatch?** Run `python3 scripts/parse_data.py` to regenerate `data.json`.

**Deploy failed?** Check Render logs. Usually dependency issue or Python syntax error.

---

## Reminder

This dashboard tracks a real conflict. People are dying. Keep it cynical but respectful - the goal is truth, not entertainment.
