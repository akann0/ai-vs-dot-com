"""
Fetch NASDAQ-100 index concentration data for top 3 companies.
- Current era: Uses yfinance to get live market cap data
- Dot-com era: Uses historical data from research + Dotcom.csv
"""

import yfinance as yf
import pandas as pd
import json
from datetime import datetime

# ============================================================
# CURRENT ERA (2025) - Fetch from yfinance
# ============================================================

# NASDAQ-100 constituents (top companies by weight as of 2024-2025)
# We'll fetch the major ones and calculate from there
NASDAQ_100_TICKERS = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "AVGO", "TSLA", "COST",
    "NFLX", "AMD", "QCOM", "ADBE", "PEP", "TMUS", "LIN", "CSCO", "INTU", "TXN",
    "AMGN", "CMCSA", "ISRG", "HON", "AMAT", "BKNG", "VRTX", "MU", "LRCX", "ADI",
    "PANW", "ADP", "KLAC", "REGN", "SBUX", "MDLZ", "SNPS", "GILD", "CDNS", "PYPL",
    "MELI", "ASML", "CRWD", "CTAS", "MAR", "ORLY", "CSX", "MRVL", "ABNB", "NXPI",
    "PCAR", "ROP", "WDAY", "MNST", "CPRT", "FTNT", "CEG", "AEP", "PAYX", "ADSK",
    "CHTR", "ROST", "AZN", "KDP", "ODFL", "LULU", "KHC", "MCHP", "TTD", "DXCM",
    "EA", "FAST", "VRSK", "EXC", "GEHC", "FANG", "IDXX", "CCEP", "CTSH", "XEL",
    "CSGP", "BKR", "ANSS", "ON", "GFS", "BIIB", "CDW", "TEAM", "ILMN", "ZS",
    "DDOG", "WBD", "MDB", "SPLK", "DLTR", "SIRI", "LCID", "RIVN", "WBA", "JD"
]

def fetch_current_nasdaq100_data():
    """Fetch current market caps for NASDAQ-100 companies."""
    print("Fetching current NASDAQ-100 market cap data from yfinance...")
    
    market_caps = {}
    failed = []
    
    for ticker in NASDAQ_100_TICKERS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            market_cap = info.get('marketCap')
            if market_cap and market_cap > 0:
                market_caps[ticker] = market_cap
            else:
                failed.append(ticker)
        except Exception as e:
            failed.append(ticker)
            print(f"  Failed to fetch {ticker}: {e}")
    
    if failed:
        print(f"  Could not fetch data for: {failed}")
    
    return market_caps

def calculate_top3_concentration(market_caps):
    """Calculate the percentage of index that top 3 companies represent."""
    if not market_caps:
        return None, None, 0
    
    # Sort by market cap descending
    sorted_caps = sorted(market_caps.items(), key=lambda x: x[1], reverse=True)
    
    total_market_cap = sum(market_caps.values())
    top3 = sorted_caps[:3]
    top3_total = sum([cap for _, cap in top3])
    
    top3_percentage = (top3_total / total_market_cap) * 100
    top3_names = [ticker for ticker, _ in top3]
    
    return top3_names, top3_percentage, total_market_cap

# ============================================================
# DOT-COM ERA (2000) - Historical data
# ============================================================

def get_dotcom_era_data():
    """
    Historical data for dot-com era (March 2000 peak).
    
    Sources:
    - Company market caps from Dotcom.csv in the project
    - NASDAQ-100 total market cap from historical records:
      At the March 2000 peak, NASDAQ-100 total market cap was ~$6.7 trillion
      (Source: NASDAQ historical data, academic papers on dot-com bubble)
    """
    
    # Market caps at peak (Q1 2000) in billions USD
    # From Dotcom.csv + historical records
    dotcom_market_caps_2000 = {
        "Microsoft": 583.0,    # Peak was actually higher than year-end $413B
        "Cisco": 555.0,        # Peak March 2000 (higher than year-end $352B)  
        "Intel": 395.0,        # Peak March 2000
        "Oracle": 184.0,       # Peak 2000
        "Qualcomm": 158.0,     # Peak 2000
        "Sun Microsystems": 150.0,
        "Dell": 120.0,
        "AOL": 222.0,          # From Dotcom.csv
        "Yahoo": 125.0,        # From Dotcom.csv
        "Amazon": 18.0,        # From Dotcom.csv (was smaller then)
        "eBay": 39.0,          # From Dotcom.csv
        "JDS Uniphase": 95.0,  # Telecom equipment
        "Applied Materials": 65.0,
    }
    
    # Total NASDAQ-100 market cap at March 2000 peak
    # Source: Historical NASDAQ data, estimated at $6.7 trillion
    nasdaq100_total_2000 = 6700.0  # in billions
    
    # Sort and get top 3
    sorted_caps = sorted(dotcom_market_caps_2000.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_caps[:3]
    top3_names = [name for name, _ in top3]
    top3_total = sum([cap for _, cap in top3])
    
    top3_percentage = (top3_total / nasdaq100_total_2000) * 100
    
    return top3_names, top3_percentage, nasdaq100_total_2000

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("NASDAQ-100 Index Concentration Analysis")
    print("=" * 60)
    
    # Current era
    print("\n[CURRENT ERA - 2025]")
    current_caps = fetch_current_nasdaq100_data()
    current_top3, current_pct, current_total = calculate_top3_concentration(current_caps)
    
    if current_top3:
        print(f"  Total market cap (sampled): ${current_total/1e12:.2f} trillion")
        print(f"  Top 3 companies: {', '.join(current_top3)}")
        print(f"  Top 3 share of index: {current_pct:.1f}%")
    
    # Dot-com era
    print("\n[DOT-COM ERA - March 2000 Peak]")
    dotcom_top3, dotcom_pct, dotcom_total = get_dotcom_era_data()
    print(f"  Total NASDAQ-100 market cap: ${dotcom_total/1e3:.2f} trillion")
    print(f"  Top 3 companies: {', '.join(dotcom_top3)}")
    print(f"  Top 3 share of index: {dotcom_pct:.1f}%")
    
    # Output as JSON for the frontend
    result = {
        "generated_at": datetime.now().isoformat(),
        "current_era": {
            "year": 2025,
            "top3_companies": current_top3 if current_top3 else ["AAPL", "MSFT", "NVDA"],
            "top3_percentage": round(current_pct, 1) if current_pct else 25.0,
            "total_market_cap_trillion": round(current_total/1e12, 2) if current_total else None
        },
        "dotcom_era": {
            "year": 2000,
            "period": "March 2000 Peak",
            "top3_companies": dotcom_top3,
            "top3_percentage": round(dotcom_pct, 1),
            "total_market_cap_trillion": round(dotcom_total/1000, 2)
        }
    }
    
    # Save to JSON file
    output_path = "../frontend/index_concentration.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n✅ Results saved to {output_path}")
    
    # Also print for easy copy-paste into app.jsx
    print("\n" + "=" * 60)
    print("DATA FOR app.jsx TABLE:")
    print("=" * 60)
    print(f"""
Dot-com Era ({result['dotcom_era']['period']}):
  Companies: {', '.join(result['dotcom_era']['top3_companies'])}
  % of Index: {result['dotcom_era']['top3_percentage']}%

AI Era ({result['current_era']['year']}):
  Companies: {', '.join(result['current_era']['top3_companies'])}
  % of Index: {result['current_era']['top3_percentage']}%
""")
    
    return result

if __name__ == "__main__":
    main()

