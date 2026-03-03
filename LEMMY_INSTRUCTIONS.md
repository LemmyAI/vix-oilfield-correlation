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

---

## Correlation Index (r-value)

All tabs show correlation coefficients calculated **from war start date only** (Feb 28, 2026). This ensures we measure conflict-period relationships, not pre-war noise.

### How Correlations Are Calculated

The pipeline (`scripts/parse_data.py`) includes a `calc_corr_from_war_start()` function that:

1. Filters data to war period only (Feb 28 onwards)
2. Pairs non-null values from both datasets
3. Calculates Pearson correlation coefficient

```python
# From parse_data.py:
WAR_START = '2026-02-28'  # CORRELATIONS CALCULATED FROM THIS DATE ONLY

def calc_corr_from_war_start(x_list, y_list, dates, war_start_idx):
    # Filter to war period only
    war_x = x_list[war_start_idx:]
    war_y = y_list[war_start_idx:]
    # ... Pearson formula
```

### Interpreting r-values

| Range | Meaning |
|-------|---------|
| **\|r\| > 0.7** | Strong relationship (same direction or inverse) |
| **\|r\| = 0.4-0.7** | Moderate relationship |
| **\|r\| < 0.4** | Weak or no relationship |
| **r > 0** | Positive correlation (both go up together) |
| **r < 0** | Negative/inverse correlation (one up, other down) |

### Current Correlations (War Period)

| Metric Pair | r | Interpretation |
|-------------|---|----------------|
| VIX vs Attacks | -0.69 | Negative - fear peaked early while attacks accumulated |
| DJT vs KIA | +0.11 | Weak - DJT up, casualties up but timing differs |
| RRP vs Deaths | -0.06 | Near zero - unrelated, liquidity injection was pre-planned |
| Trump Approval vs KIA | +0.41 | Moderate rally effect |
| Right Track vs KIA | **+0.81** | STRONG - Americans rally as body count rises |

### Adding New Correlations

When adding a new tab with data, add correlation calculation to pipeline:

1. Add raw data to `data/` as CSV
2. Add parser function (e.g., `parse_new_metric()`)
3. Add to aligned arrays in main()
4. Calculate correlation: `corr_new = calc_corr_from_war_start(new_data, kia_data, dates, war_start_idx)`
5. Add to output JSON: `'correlations': {'new_kia': round(corr_new, 2), ...}`
6. Display in stats box and explanation

---

## Chart Explanation Boxes

Each chart tab includes an explanation box explaining the relationship shown. This is critical for users to understand what the data means.

Example from VIX tab:
> **Fear vs Fire:** VIX spiked to 23.12 when Hormuz closed (Mar 1), then declined while attacks accumulated. The r=-0.69 correlation is negative because fear peaked early, then markets adapted to the "new normal" of daily strikes.

All explanations should:
1. Name the relationship (e.g., "Fear vs Fire", "War Profiteering")
2. Highlight key data points
3. Explain the correlation value
4. Add context about why the relationship exists (or doesn't)

---

## Automated Daily Updates

A cron job is configured to run at **14:00 Swedish time (Europe/Stockholm) daily** to:
1. Fetch automated data (VIX from FRED, DJT from Yahoo Finance)
2. Run the data pipeline (`scripts/parse_data.py`)
3. Commit and push changes
4. Trigger auto-deploy on Render

### Cron Job Details

- **Job ID**: `iran-wars-dashboard-update`
- **Schedule**: `0 14 * * *` (14:00 Europe/Stockholm daily)
- **Location**: `~/.openclaw/cron/jobs.json`
- **Delivery**: Telegram LemmySpace topic:387 (Financial Reports thread)

### Manual vs Automated Data

| Data Source | Automated? | How to Update |
|-------------|------------|---------------|
| VIX | ✅ Yes | FRED API (requires `FRED_API_KEY` env var) |
| DJT Stock | ✅ Yes | Yahoo Finance (requires `yfinance` package) |
| Energy Attacks | ❌ Manual | Edit `data/oilfield_attacks.csv` |
| US Casualties | ❌ Manual | Edit `data/us_casualties.csv` |
| Conflict Deaths | ❌ Manual | Edit `data/conflict_deaths.csv` |
| Approval Ratings | ❌ Manual | Edit `data/approval_ratings.csv` |
| RRP Operations | ❌ Manual | Edit `data/rrp_operations.csv` |

### Setup Environment (One-time)

```bash
# Install yfinance for stock data
pip install yfinance --user

# Set FRED API key (get free key at https://fredaccount.stlouisfed.org/apikeys)
echo 'FRED_API_KEY=your_key_here' >> ~/projects/vix-oilfield-correlation/.env
```

### Manual Data Update

To manually update data:

```bash
cd ~/projects/vix-oilfield-correlation

# Edit CSV files in data/ directory
# Then run pipeline:
python3 scripts/parse_data.py

# Review output, then commit:
git add . && git commit -m "Update data" && git push
```
