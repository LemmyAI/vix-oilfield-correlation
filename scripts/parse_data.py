#!/usr/bin/env python3
"""
Data Pipeline for Iran Wars in Strange Numbers Dashboard
Run this locally to validate and generate clean JSON data files.

USAGE:
    python scripts/parse_data.py
    
This will:
1. Parse raw CSV data
2. Validate all values
3. Print summary for manual inspection
4. Generate clean JSON files for the app
"""

import json
import csv
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')

def parse_date(s):
    return datetime.strptime(s, '%Y-%m-%d').strftime('%Y-%m-%d')

def parse_float(s):
    v = float(s)
    if v != v:
        raise ValueError(f"Invalid float: {s}")
    return v

def parse_int(s):
    return int(s)

def parse_vix():
    filepath = os.path.join(DATA_DIR, 'vix_daily.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({'date': parse_date(row['date']), 'vix': parse_float(row['vix'])})
    assert len(data) >= 5, f"VIX: Too few records ({len(data)})"
    for r in data:
        assert 0 < r['vix'] < 100, f"VIX: Suspicious value {r['vix']}"
    return data

def parse_attacks():
    filepath = os.path.join(DATA_DIR, 'oilfield_attacks.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'date': parse_date(row['date']),
                'cumulative': parse_int(row['cumulative_attacks'])
            })
    daily = {}
    for r in data:
        daily[r['date']] = r['cumulative']
    return [{'date': k, 'cumulative': v} for k, v in sorted(daily.items())]

def parse_djt():
    filepath = os.path.join(DATA_DIR, 'djt_stock.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'date': parse_date(row['date']),
                'close': parse_float(row['djt_close']),
                'volume': parse_float(row.get('djt_volume_m', 0))
            })
    assert len(data) >= 3, f"DJT: Too few records"
    for r in data:
        assert 0 < r['close'] < 1000, f"DJT: Suspicious price ${r['close']}"
    return data

def parse_casualties():
    filepath = os.path.join(DATA_DIR, 'us_casualties.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'date': parse_date(row['date']),
                'cumulative': parse_int(row['cumulative_killed'])
            })
    daily = {}
    for r in data:
        daily[r['date']] = r['cumulative']
    return [{'date': k, 'cumulative': v} for k, v in sorted(daily.items())]

def parse_rrp():
    """Parse Fed Reverse Repo Operations data"""
    filepath = os.path.join(DATA_DIR, 'rrp_operations.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'date': parse_date(row['date']),
                'rrp_billion': parse_float(row['rrp_billion']),
                'note': row.get('note', '')
            })
    assert len(data) >= 3, f"RRP: Too few records"
    for r in data:
        assert 0 < r['rrp_billion'] < 3000, f"RRP: Suspicious value ${r['rrp_billion']}B"
    return data

def parse_deaths():
    """Parse conflict deaths data"""
    filepath = os.path.join(DATA_DIR, 'conflict_deaths.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'date': parse_date(row['date']),
                'iran': parse_int(row['iran_deaths']),
                'israel': parse_int(row['israel_deaths']),
                'us': parse_int(row['us_deaths']),
                'civilian': parse_int(row['civilian_deaths']),
                'cumulative': parse_int(row['cumulative_total'])
            })
    assert len(data) >= 1, f"Deaths: No records"
    return data

def main():
    print("=" * 70)
    print("🦾 IRAN WARS IN STRANGE NUMBERS - DATA PIPELINE")
    print("=" * 70)
    
    print("\n📊 Parsing VIX data...")
    vix = parse_vix()
    print(f"   ✓ {len(vix)} records | Range: {vix[0]['vix']:.2f} - {max(v['vix'] for v in vix):.2f}")
    
    print("\n💣 Parsing infrastructure attacks...")
    attacks = parse_attacks()
    print(f"   ✓ {len(attacks)} records | Total: {attacks[-1]['cumulative']}")
    
    print("\n📈 Parsing DJT stock data...")
    djt = parse_djt()
    print(f"   ✓ {len(djt)} records | ${min(d['close'] for d in djt):.2f} - ${max(d['close'] for d in djt):.2f}")
    
    print("\n⚔️ Parsing US casualties...")
    kia = parse_casualties()
    print(f"   ✓ {len(kia)} records | US KIA: {kia[-1]['cumulative']}")
    
    print("\n🏦 Parsing Fed RRP (Reverse Repos)...")
    rrp = parse_rrp()
    print(f"   ✓ {len(rrp)} records | ${min(r['rrp_billion'] for r in rrp):.1f}B - ${max(r['rrp_billion'] for r in rrp):.1f}B")
    
    print("\n💀 Parsing conflict deaths...")
    deaths = parse_deaths()
    print(f"   ✓ {len(deaths)} records | Total: {deaths[-1]['cumulative']:,}")
    
    # Calculate stats
    vix_peak = max(v['vix'] for v in vix)
    vix_peak_date = [v for v in vix if v['vix'] == vix_peak][0]['date']
    djt_min = min(d['close'] for d in djt)
    djt_max = max(d['close'] for d in djt)
    djt_pump = ((djt_max / djt_min - 1) * 100)
    rrp_drop = rrp[0]['rrp_billion'] - min(r['rrp_billion'] for r in rrp)
    rrp_min = min(r['rrp_billion'] for r in rrp)
    total_deaths = deaths[-1]['cumulative']
    
    print("\n" + "=" * 70)
    print("📋 SUMMARY - INSPECT BEFORE COMMITTING")
    print("=" * 70)
    print(f"\n   VIX Peak: {vix_peak:.2f} on {vix_peak_date}")
    print(f"   DJT Pump: +{djt_pump:.0f}% (${djt_min:.2f} → ${djt_max:.2f})")
    print(f"   RRP Drop: ${rrp_drop:.1f}B (drained to ${rrp_min:.1f}B)")
    print(f"   Infrastructure Attacks: {attacks[-1]['cumulative']}")
    print(f"   US KIA: {kia[-1]['cumulative']}")
    print(f"   Total Conflict Deaths: {total_deaths:,}")
    print("\n" + "=" * 70)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output = {
        'vix': vix,
        'attacks': attacks,
        'djt': djt,
        'kia': kia,
        'rrp': rrp,
        'deaths': deaths,
        'stats': {
            'vix_peak': round(vix_peak, 2),
            'vix_peak_date': vix_peak_date,
            'djt_min': round(djt_min, 2),
            'djt_max': round(djt_max, 2),
            'djt_pump_pct': round(djt_pump, 0),
            'rrp_drop': round(rrp_drop, 1),
            'rrp_min': round(rrp_min, 1),
            'total_attacks': attacks[-1]['cumulative'],
            'total_kia': kia[-1]['cumulative'],
            'total_deaths': total_deaths,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    }
    
    output_file = os.path.join(OUTPUT_DIR, 'data.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Data saved to: {output_file}")
    print("\n⚠️  REVIEW THE SUMMARY ABOVE BEFORE COMMITTING!")
    print("   git add . && git commit -m 'Update data'")
    print("   If issues: Fix CSV files and re-run\n")

if __name__ == '__main__':
    main()
