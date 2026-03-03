#!/usr/bin/env python3
"""
Data Pipeline for Iran Wars in Strange Numbers Dashboard
Run locally to validate and generate clean JSON data files.

IMPORTANT: Correlations are calculated from WAR START DATE (Feb 28) only,
not from the full dataset. This ensures we're measuring conflict-period relationships.
"""

import json
import csv
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')

WAR_START = '2026-02-28'  # CORRELATIONS CALCULATED FROM THIS DATE ONLY

def parse_date(s):
    return datetime.strptime(s, '%Y-%m-%d')

def format_date(d):
    return d.strftime('%Y-%m-%d')

def parse_float(s):
    v = float(s)
    if v != v:
        return None
    return v

def parse_int(s):
    return int(s)

def get_date_range(start_date, end_date):
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    return dates

def parse_vix():
    filepath = os.path.join(DATA_DIR, 'vix_daily.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[format_date(parse_date(row['date']))] = parse_float(row['vix'])
    return data

def parse_attacks():
    filepath = os.path.join(DATA_DIR, 'oilfield_attacks.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[format_date(parse_date(row['date']))] = parse_int(row['cumulative_attacks'])
    return data

def parse_djt():
    filepath = os.path.join(DATA_DIR, 'djt_stock.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[format_date(parse_date(row['date']))] = {
                'close': parse_float(row['djt_close']),
                'volume': parse_float(row.get('djt_volume_m', 0))
            }
    return data

def parse_casualties():
    filepath = os.path.join(DATA_DIR, 'us_casualties.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[format_date(parse_date(row['date']))] = parse_int(row['cumulative_killed'])
    return data

def parse_rrp():
    filepath = os.path.join(DATA_DIR, 'rrp_operations.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[format_date(parse_date(row['date']))] = parse_float(row['rrp_billion'])
    return data

def parse_deaths():
    filepath = os.path.join(DATA_DIR, 'conflict_deaths.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[format_date(parse_date(row['date']))] = parse_int(row['cumulative_total'])
    return data

def parse_approval():
    filepath = os.path.join(DATA_DIR, 'approval_ratings.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[format_date(parse_date(row['date']))] = {
                'trump': parse_float(row['trump_approval']),
                'biden': parse_float(row['biden_approval']),
                'right_track': parse_float(row['right_track']),
                'iran': parse_float(row['iran_approval'])
            }
    return data

def calc_corr_from_war_start(x_list, y_list, dates, war_start_idx):
    """
    Calculate Pearson correlation ONLY from war start date.
    This ensures we measure conflict-period relationships, not pre-war noise.
    
    Parameters:
        x_list, y_list: Full data arrays (may contain None for missing values)
        dates: Date labels for each index
        war_start_idx: Index where war started (Feb 28)
    
    Returns:
        Correlation coefficient (-1 to 1)
    """
    # Filter to war period only
    war_x = x_list[war_start_idx:]
    war_y = y_list[war_start_idx:]
    
    # Get non-null pairs
    pairs = [(x, y) for x, y in zip(war_x, war_y) if x is not None and y is not None]
    
    if len(pairs) < 2:
        return 0
    
    n = len(pairs)
    sum_x = sum(p[0] for p in pairs)
    sum_y = sum(p[1] for p in pairs)
    sum_xy = sum(p[0] * p[1] for p in pairs)
    sum_x2 = sum(p[0] ** 2 for p in pairs)
    sum_y2 = sum(p[1] ** 2 for p in pairs)
    
    num = n * sum_xy - sum_x * sum_y
    den = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
    
    return num / den if den != 0 else 0

def main():
    print("=" * 70)
    print("🦾 IRAN WARS IN STRANGE NUMBERS - DATA PIPELINE")
    print("=" * 70)
    print(f"\n⚠️  CORRELATIONS CALCULATED FROM WAR START: {WAR_START}")
    print("    (Feb 28, 2026 - conflict period only)")
    
    # Load all data as dicts first
    print("\n📊 Loading data files...")
    vix_dict = parse_vix()
    djt_dict = parse_djt()
    attacks_dict = parse_attacks()
    kia_dict = parse_casualties()
    rrp_dict = parse_rrp()
    deaths_dict = parse_deaths()
    approval_dict = parse_approval()
    
    # Find date range
    all_dates = set(vix_dict.keys()) | set(djt_dict.keys()) | set(attacks_dict.keys()) | set(kia_dict.keys()) | set(rrp_dict.keys()) | set(deaths_dict.keys()) | set(approval_dict.keys())
    min_date = min(parse_date(d) for d in all_dates)
    max_date = max(parse_date(d) for d in all_dates)
    
    # Generate aligned data for ALL dates
    date_range = get_date_range(min_date, max_date)
    dates = [format_date(d) for d in date_range]
    war_start_idx = dates.index(WAR_START) if WAR_START in dates else 0
    
    print(f"   Date range: {dates[0]} to {dates[-1]} ({len(dates)} days)")
    print(f"   War start index: {war_start_idx} ({dates[war_start_idx]})")
    
    # Build aligned arrays
    vix = []
    djt = []
    djt_vol = []
    attacks = []
    kia = []
    rrp = []
    deaths = []
    trump_app = []
    biden_app = []
    right_track = []
    iran_app = []
    
    # Track last known values for cumulative metrics
    last_attack = 0
    last_kia = 0
    last_death = 0
    
    for d in dates:
        vix.append(vix_dict.get(d))
        djt.append(djt_dict.get(d, {}).get('close'))
        djt_vol.append(djt_dict.get(d, {}).get('volume'))
        
        if d in attacks_dict:
            last_attack = attacks_dict[d]
        attacks.append(last_attack if last_attack > 0 else None)
        
        if d in kia_dict:
            last_kia = kia_dict[d]
        kia.append(last_kia if last_kia > 0 else None)
        
        rrp.append(rrp_dict.get(d))
        
        if d in deaths_dict:
            last_death = deaths_dict[d]
        deaths.append(last_death if last_death > 0 else None)
        
        if d in approval_dict:
            trump_app.append(approval_dict[d]['trump'])
            biden_app.append(approval_dict[d]['biden'])
            right_track.append(approval_dict[d]['right_track'])
            iran_app.append(approval_dict[d]['iran'])
        else:
            trump_app.append(None)
            biden_app.append(None)
            right_track.append(None)
            iran_app.append(None)
    
    # Calculate correlations FROM WAR START ONLY
    print("\n📈 Calculating correlations (war period only)...")
    corr_vix_attacks = calc_corr_from_war_start(vix, attacks, dates, war_start_idx)
    corr_djt_kia = calc_corr_from_war_start(djt, kia, dates, war_start_idx)
    corr_rrp_deaths = calc_corr_from_war_start(rrp, deaths, dates, war_start_idx)
    corr_trump_kia = calc_corr_from_war_start(trump_app, kia, dates, war_start_idx)
    corr_righttrack_kia = calc_corr_from_war_start(right_track, kia, dates, war_start_idx)
    
    print(f"   VIX vs Attacks: r={corr_vix_attacks:.2f}")
    print(f"   DJT vs KIA: r={corr_djt_kia:.2f}")
    print(f"   RRP vs Deaths: r={corr_rrp_deaths:.2f}")
    print(f"   Trump Approval vs KIA: r={corr_trump_kia:.2f}")
    print(f"   Right Track vs KIA: r={corr_righttrack_kia:.2f}")
    
    # Stats
    vix_vals = [v for v in vix if v is not None]
    djt_vals = [v for v in djt if v is not None]
    rrp_vals = [v for v in rrp if v is not None]
    trump_vals = [v for v in trump_app if v is not None]
    
    vix_peak = max(vix_vals)
    vix_peak_date = dates[vix.index(vix_peak)]
    djt_min = min(djt_vals)
    djt_max = max(djt_vals)
    djt_pump = ((djt_max / djt_min - 1) * 100)
    rrp_max = max(rrp_vals)
    rrp_min = min(rrp_vals)
    rrp_drop = rrp_max - rrp_min
    total_attacks = max(a for a in attacks if a is not None)
    total_kia = max(k for k in kia if k is not None)
    total_deaths = max(d for d in deaths if d is not None)
    
    trump_start = trump_app[0] if trump_app[0] is not None else trump_vals[0]
    trump_peak = max(trump_vals)
    trump_change = trump_peak - trump_start if trump_vals else 0
    
    print(f"\n   ✓ VIX: {sum(1 for v in vix if v is not None)} data points")
    print(f"   ✓ DJT: {sum(1 for v in djt if v is not None)} data points")
    print(f"   ✓ Attacks: {sum(1 for v in attacks if v is not None)} data points")
    print(f"   ✓ KIA: {sum(1 for v in kia if v is not None)} data points")
    print(f"   ✓ RRP: {sum(1 for v in rrp if v is not None)} data points")
    print(f"   ✓ Deaths: {sum(1 for v in deaths if v is not None)} data points")
    print(f"   ✓ Approval: {sum(1 for v in trump_app if v is not None)} data points")
    
    print("\n" + "=" * 70)
    print("📋 SUMMARY - INSPECT BEFORE COMMITTING")
    print("=" * 70)
    print(f"\n   VIX Peak: {vix_peak:.2f} on {vix_peak_date}")
    print(f"   DJT Pump: +{djt_pump:.0f}% (${djt_min:.2f} → ${djt_max:.2f})")
    print(f"   RRP Drop: ${rrp_drop:.1f}B (${rrp_max:.1f}B → ${rrp_min:.1f}B)")
    print(f"   Infrastructure Attacks: {total_attacks}")
    print(f"   US KIA: {total_kia}")
    print(f"   Total Conflict Deaths: {total_deaths:,}")
    print(f"\n   Trump Approval: {trump_start:.1f}% → {trump_peak:.1f}% (+{trump_change:.1f}pts)")
    print("=" * 70)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output = {
        'dates': dates,
        'war_start_idx': war_start_idx,
        'vix': vix,
        'djt': djt,
        'djt_volume': djt_vol,
        'attacks': attacks,
        'kia': kia,
        'rrp': rrp,
        'deaths': deaths,
        'trump_approval': trump_app,
        'biden_approval': biden_app,
        'right_track': right_track,
        'iran_approval': iran_app,
        'correlations': {
            'vix_attacks': round(corr_vix_attacks, 2),
            'djt_kia': round(corr_djt_kia, 2),
            'rrp_deaths': round(corr_rrp_deaths, 2),
            'trump_kia': round(corr_trump_kia, 2),
            'righttrack_kia': round(corr_righttrack_kia, 2)
        },
        'stats': {
            'vix_peak': round(vix_peak, 2),
            'vix_peak_date': vix_peak_date,
            'djt_min': round(djt_min, 2),
            'djt_max': round(djt_max, 2),
            'djt_pump_pct': round(djt_pump, 0),
            'rrp_max': round(rrp_max, 1),
            'rrp_min': round(rrp_min, 1),
            'rrp_drop': round(rrp_drop, 1),
            'total_attacks': total_attacks,
            'total_kia': total_kia,
            'total_deaths': total_deaths,
            'trump_start': round(trump_start, 1),
            'trump_peak': round(trump_peak, 1),
            'trump_change': round(trump_change, 1),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    }
    
    output_file = os.path.join(OUTPUT_DIR, 'data.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Data saved to: {output_file}")
    print("\n⚠️  REVIEW THE SUMMARY ABOVE BEFORE COMMITTING!\n")

if __name__ == '__main__':
    main()
