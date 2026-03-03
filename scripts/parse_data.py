#!/usr/bin/env python3
"""
Data Pipeline for 2026 Iran Conflict Dashboard
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
    """Parse date string to ISO format"""
    return datetime.strptime(s, '%Y-%m-%d').strftime('%Y-%m-%d')

def parse_float(s):
    """Parse float, raise on error"""
    v = float(s)
    if v != v:  # NaN check
        raise ValueError(f"Invalid float: {s}")
    return v

def parse_int(s):
    """Parse int, raise on error"""
    return int(s)

def parse_vix():
    """Parse VIX daily data"""
    filepath = os.path.join(DATA_DIR, 'vix_daily.csv')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                'date': parse_date(row['date']),
                'vix': parse_float(row['vix'])
            }
            data.append(record)
    
    # Validation
    assert len(data) >= 5, f"VIX: Too few records ({len(data)})"
    for r in data:
        assert 0 < r['vix'] < 100, f"VIX: Suspicious value {r['vix']} on {r['date']}"
    
    return data

def parse_attacks():
    """Parse infrastructure attacks data"""
    filepath = os.path.join(DATA_DIR, 'oilfield_attacks.csv')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                'date': parse_date(row['date']),
                'cumulative': parse_int(row['cumulative_attacks']),
                'type': row.get('attack_type', 'unknown'),
                'target': row.get('target', 'unknown')
            }
            data.append(record)
    
    # Validation
    assert len(data) >= 1, f"Attacks: No records"
    
    # Get last cumulative per date
    daily = {}
    for r in data:
        daily[r['date']] = r['cumulative']
    
    return [{'date': k, 'cumulative': v} for k, v in sorted(daily.items())]

def parse_djt():
    """Parse DJT stock data"""
    filepath = os.path.join(DATA_DIR, 'djt_stock.csv')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                'date': parse_date(row['date']),
                'close': parse_float(row['djt_close']),
                'volume': parse_float(row.get('djt_volume_m', 0))
            }
            data.append(record)
    
    # Validation
    assert len(data) >= 3, f"DJT: Too few records ({len(data)})"
    for r in data:
        assert 0 < r['close'] < 1000, f"DJT: Suspicious price ${r['close']} on {r['date']}"
    
    return data

def parse_casualties():
    """Parse US casualties data"""
    filepath = os.path.join(DATA_DIR, 'us_casualties.csv')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing: {filepath}")
    
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                'date': parse_date(row['date']),
                'killed': parse_int(row['us_killed']),
                'injured': parse_int(row.get('us_injured', 0)),
                'cumulative': parse_int(row['cumulative_killed'])
            }
            data.append(record)
    
    # Validation
    assert len(data) >= 1, f"Casualties: No records"
    
    # Get daily cumulative
    daily = {}
    for r in data:
        daily[r['date']] = r['cumulative']
    
    return [{'date': k, 'cumulative': v} for k, v in sorted(daily.items())]

def main():
    print("=" * 60)
    print("2026 IRAN CONFLICT - DATA PIPELINE")
    print("=" * 60)
    
    # Parse all data
    print("\n📊 Parsing VIX data...")
    vix = parse_vix()
    print(f"   ✓ {len(vix)} records | Range: {vix[0]['vix']:.2f} - {max(v['vix'] for v in vix):.2f}")
    
    print("\n💣 Parsing infrastructure attacks...")
    attacks = parse_attacks()
    print(f"   ✓ {len(attacks)} records | Total attacks: {attacks[-1]['cumulative']}")
    
    print("\n📈 Parsing DJT stock data...")
    djt = parse_djt()
    print(f"   ✓ {len(djt)} records | Range: ${min(d['close'] for d in djt):.2f} - ${max(d['close'] for d in djt):.2f}")
    
    print("\n⚔️ Parsing US casualties...")
    kia = parse_casualties()
    print(f"   ✓ {len(kia)} records | Total KIA: {kia[-1]['cumulative']}")
    
    # Calculate stats
    vix_peak = max(v['vix'] for v in vix)
    vix_peak_date = [v for v in vix if v['vix'] == vix_peak][0]['date']
    djt_min = min(d['close'] for d in djt)
    djt_max = max(d['close'] for d in djt)
    djt_pump = ((djt_max / djt_min - 1) * 100)
    total_attacks = attacks[-1]['cumulative']
    total_kia = kia[-1]['cumulative']
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY - INSPECT BEFORE COMMITTING")
    print("=" * 60)
    print(f"\n   VIX Peak: {vix_peak:.2f} on {vix_peak_date}")
    print(f"   DJT Pump: +{djt_pump:.0f}% (${djt_min:.2f} → ${djt_max:.2f})")
    print(f"   Infrastructure Attacks: {total_attacks}")
    print(f"   US KIA: {total_kia}")
    print("\n" + "=" * 60)
    
    # Generate output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output = {
        'vix': vix,
        'attacks': attacks,
        'djt': djt,
        'kia': kia,
        'stats': {
            'vix_peak': round(vix_peak, 2),
            'vix_peak_date': vix_peak_date,
            'djt_min': round(djt_min, 2),
            'djt_max': round(djt_max, 2),
            'djt_pump_pct': round(djt_pump, 0),
            'total_attacks': total_attacks,
            'total_kia': total_kia,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    }
    
    output_file = os.path.join(OUTPUT_DIR, 'data.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Data saved to: {output_file}")
    print("\n⚠️  REVIEW THE SUMMARY ABOVE BEFORE COMMITTING!")
    print("   If values look correct: git add . && git commit -m 'Update data'")
    print("   If issues: Fix CSV files and re-run this script\n")

if __name__ == '__main__':
    main()
