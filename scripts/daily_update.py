#!/usr/bin/env python3
"""
Daily Data Update for Iran Wars Dashboard
Fetches data from APIs and updates CSV files.
Run daily at 14:00 Swedish time.
"""

import csv
import json
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__))
FRED_API_KEY = os.getenv('FRED_API_KEY', '')

def get_last_date(csv_file):
    """Get the last date from a CSV file"""
    filepath = os.path.join(DATA_DIR, csv_file)
    if not os.path.exists(filepath):
        return None
    with open(filepath) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            return None
        return rows[-1]['date']

def fetch_vix():
    """Fetch VIX from FRED API"""
    if not FRED_API_KEY:
        print("⚠️  No FRED_API_KEY set, skipping VIX fetch")
        return False
    
    print("📈 Fetching VIX from FRED...")
    
    # Get last date in our CSV
    last_date = get_last_date('vix_daily.csv')
    if last_date:
        start_date = (datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        start_date = '2026-02-18'  # Default start
    
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': 'VIXCLS',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if 'observations' not in data:
            print(f"❌ FRED API error: {data}")
            return False
        
        observations = data['observations']
        if not observations:
            print("✓ VIX already up to date")
            return True
        
        # Append to CSV
        filepath = os.path.join(DATA_DIR, 'vix_daily.csv')
        with open(filepath, 'a') as f:
            writer = csv.writer(f)
            for obs in observations:
                if obs['value'] != '.':  # Skip missing values
                    writer.writerow([obs['date'], obs['value']])
        
        print(f"✓ Added {len(observations)} VIX observations")
        return True
    
    except Exception as e:
        print(f"❌ VIX fetch failed: {e}")
        return False

def fetch_djt():
    """Fetch DJT stock from Yahoo Finance (yfinance)"""
    print("💰 Fetching DJT stock...")
    
    try:
        import yfinance as yf
        
        last_date = get_last_date('djt_stock.csv')
        if last_date:
            start_date = (datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days=1))
        else:
            start_date = datetime(2026, 2, 18)
        
        ticker = yf.Ticker("DJT")
        hist = ticker.history(start=start_date.strftime('%Y-%m-%d'))
        
        if hist.empty:
            print("✓ DJT already up to date")
            return True
        
        # Append to CSV
        filepath = os.path.join(DATA_DIR, 'djt_stock.csv')
        with open(filepath, 'a') as f:
            writer = csv.writer(f)
            for idx, row in hist.iterrows():
                date_str = idx.strftime('%Y-%m-%d')
                close = round(row['Close'], 2)
                volume = round(row['Volume'] / 1e6, 1)  # Volume in millions
                writer.writerow([date_str, close, volume])
        
        print(f"✓ Added {len(hist)} DJT observations")
        return True
    
    except ImportError:
        print("⚠️  yfinance not installed, skipping DJT fetch")
        return False
    except Exception as e:
        print(f"❌ DJT fetch failed: {e}")
        return False

def fetch_rrp():
    """Fetch RRP from NY Fed"""
    print("🏦 Fetching RRP from NY Fed...")
    
    # NY Fed publishes RRP data - we need to scrape or use their API
    # For now, this is a placeholder - would need actual implementation
    print("⚠️  RRP fetch requires NY Fed API (not implemented)")
    print("   Manually update data/rrp_operations.csv")
    return True

def update_manual_data():
    """
    Print reminder for manual data updates.
    These sources require manual entry:
    - oilfield_attacks.csv
    - us_casualties.csv
    - conflict_deaths.csv
    - approval_ratings.csv
    """
    print("\n📋 MANUAL DATA UPDATE REQUIRED:")
    print("   The following files need manual updates:")
    print("   - data/oilfield_attacks.csv (Reuters, AP News)")
    print("   - data/us_casualties.csv (DoD briefings)")
    print("   - data/conflict_deaths.csv (Iran Health Ministry, IDF, UN)")
    print("   - data/approval_ratings.csv (Gallup, FiveThirtyEight)")
    print("   - data/rrp_operations.csv (NY Fed website)")
    print("\n   Edit these files, then run:")
    print("   cd ~/projects/vix-oilfield-correlation")
    print("   python3 scripts/parse_data.py")
    print("   git add . && git commit -m 'Update data' && git push")
    return True

def run_pipeline():
    """Run the data validation pipeline"""
    print("\n🔧 Running data pipeline...")
    
    import subprocess
    
    script_path = os.path.join(SCRIPTS_DIR, 'parse_data.py')
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Pipeline completed successfully")
        print(result.stdout)
        return True
    else:
        print("❌ Pipeline failed:")
        print(result.stderr)
        return False

def commit_and_push():
    """Commit and push changes"""
    print("\n📤 Committing and pushing changes...")
    
    import subprocess
    
    os.chdir(os.path.join(DATA_DIR, '..'))
    
    # Check if there are changes
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("✓ No changes to commit")
        return True
    
    # Commit and push
    today = datetime.now().strftime('%Y-%m-%d')
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', f'Daily data update {today}'], check=True)
    subprocess.run(['git', 'push'], check=True)
    
    print(f"✓ Changes committed and pushed")
    return True

def main():
    print("=" * 60)
    print("🦾 IRAN WARS DASHBOARD - DAILY DATA UPDATE")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Fetch automated data
    vix_ok = fetch_vix()
    djt_ok = fetch_djt()
    rrp_ok = fetch_rrp()
    
    # Reminder for manual data
    update_manual_data()
    
    # Run pipeline to generate JSON
    if vix_ok or djt_ok:
        pipeline_ok = run_pipeline()
        
        if pipeline_ok:
            commit_ok = commit_and_push()
            
            if commit_ok:
                print("\n" + "=" * 60)
                print("✅ DAILY UPDATE COMPLETE")
                print("=" * 60)
            else:
                print("\n❌ Failed to commit changes")
        else:
            print("\n❌ Pipeline failed, skipping commit")
    else:
        print("\n⚠️  No new data fetched, skipping pipeline")

if __name__ == '__main__':
    main()
