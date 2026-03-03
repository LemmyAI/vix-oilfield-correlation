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
    
    # Find date range
    all_dates = set(vix_dict.keys()) | set(djt_dict.keys()) | set(attacks_dict.keys()) | set(kia_dict.keys()) | set(rrp_dict.keys()) | set(deaths_dict.keys())
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
    
    print(f"\n   ✓ VIX: {sum(1 for v in vix if v is not None)} data points")
    print(f"   ✓ DJT: {sum(1 for v in djt if v is not None)} data points")
    print(f"   ✓ Attacks: {sum(1 for v in attacks if v is not None)} data points")
    print(f"   ✓ KIA: {sum(1 for v in kia if v is not None)} data points")
    print(f"   ✓ RRP: {sum(1 for v in rrp if v is not None)} data points")
    print(f"   ✓ Deaths: {sum(1 for v in deaths if v is not None)} data points")
    
    # Stats
    vix_vals = [v for v in vix if v is not None]
    djt_vals = [v for v in djt if v is not None]
    rrp_vals = [v for v in rrp if v is not None]
    
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
    
    print("\n" + "=" * 70)
    print("📋 SUMMARY - INSPECT BEFORE COMMITTING")
    print("=" * 70)
    print(f"\n   VIX Peak: {vix_peak:.2f} on {vix_peak_date}")
    print(f"   DJT Pump: +{djt_pump:.0f}% (${djt_min:.2f} → ${djt_max:.2f})")
    print(f"   RRP Drop: ${rrp_drop:.1f}B (${rrp_max:.1f}B → ${rrp_min:.1f}B)")
    print(f"   Infrastructure Attacks: {total_attacks}")
    print(f"   US KIA: {total_kia}")
    print(f"   Total Conflict Deaths: {total_deaths:,}")
    print("\n" + "=" * 70)
    
    # Find war start index
    war_start = '2026-02-28'
    war_start_idx = dates.index(war_start) if war_start in dates else 0
    
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
