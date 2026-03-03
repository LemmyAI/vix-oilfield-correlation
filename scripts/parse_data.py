#!/usr/bin/env python3
"""
Data Pipeline for Iran Wars in Strange Numbers Dashboard
Run locally to validate and generate clean JSON data files.
"""

import json
import csv
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')

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
    """Generate all dates between start and end"""
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

def main():
    print("=" * 70)
    print("🦾 IRAN WARS IN STRANGE NUMBERS - DATA PIPELINE")
    print("=" * 70)
    
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
    
    print(f"   Date range: {dates[0]} to {dates[-1]} ({len(dates)} days)")
    
    # Build aligned arrays (null for missing data)
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
        
        # Cumulative metrics - carry forward last known value
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
        
        # Approval ratings
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
    
    print(f"\n   ✓ VIX: {sum(1 for v in vix if v is not None)} data points")
    print(f"   ✓ DJT: {sum(1 for v in djt if v is not None)} data points")
    print(f"   ✓ Attacks: {sum(1 for v in attacks if v is not None)} data points")
    print(f"   ✓ KIA: {sum(1 for v in kia if v is not None)} data points")
    print(f"   ✓ RRP: {sum(1 for v in rrp if v is not None)} data points")
    print(f"   ✓ Deaths: {sum(1 for v in deaths if v is not None)} data points")
    print(f"   ✓ Approval: {sum(1 for v in trump_app if v is not None)} data points")
    
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
    
    # Approval stats
    trump_start = trump_app[0] if trump_app[0] is not None else trump_vals[0]
    trump_peak = max(trump_vals)
    trump_change = trump_peak - trump_start if trump_vals else 0
    
    biden_start = biden_app[0] if biden_app[0] is not None else [v for v in biden_app if v is not None][0]
    biden_low = min([v for v in biden_app if v is not None])
    
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
    print(f"   'Right Track': {right_track[0]:.1f}% → {max([v for v in right_track if v is not None]):.1f}%")
    print("\n" + "=" * 70)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output = {
        'dates': dates,
        'war_start_idx': dates.index('2026-02-28') if '2026-02-28' in dates else 0,
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
            'biden_low': round(biden_low, 1),
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
