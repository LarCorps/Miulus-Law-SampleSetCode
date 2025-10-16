# src/compile.py
import pandas as pd
import numpy as np
import requests, time
from typing import List, Dict, Optional

BASE = "https://api.worldbank.org/v2"

def _get_json(url: str, params: dict, retries: int = 3, backoff: float = 0.6) -> Optional[list]:
    """Robust JSON GET with simple retries."""
    for i in range(retries):
        r = requests.get(url, params=params, timeout=60)
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                pass
        # for 400/5xx, back off and retry
        time.sleep(backoff * (2 ** i))
    raise RuntimeError(f"Failed fetching {url} with params {params} (last status {r.status_code})")

def fetch_indicator_country(indicator: str, country: str, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Fetch a single indicator for a single country across a year range.
    Handles pagination properly (World Bank returns 'pages' in the first element).
    """
    url = f"{BASE}/country/{country}/indicator/{indicator}"
    params = {"date": f"{start_year}:{end_year}", "format": "json", "per_page": 2000, "page": 1}
    data = _get_json(url, params)
    if not isinstance(data, list) or len(data) < 2 or data[0] is None:
        return pd.DataFrame(columns=["country","year",indicator])

    pages = int(data[0].get("pages", 1))
    rows = []
    # page 1
    for rec in data[1]:
        c = rec.get("countryiso3code") or (rec.get("country",{}) or {}).get("id")
        year = rec.get("date")
        val = rec.get("value")
        if c and year:
            rows.append({"country": c, "year": int(year), indicator: val})

    # additional pages
    for p in range(2, pages + 1):
        params["page"] = p
        data_p = _get_json(url, params)
        if not isinstance(data_p, list) or len(data_p) < 2:
            break
        for rec in data_p[1]:
            c = rec.get("countryiso3code") or (rec.get("country",{}) or {}).get("id")
            year = rec.get("date")
            val = rec.get("value")
            if c and year:
                rows.append({"country": c, "year": int(year), indicator: val})

    df = pd.DataFrame(rows)
    return df

def fetch_indicator(indicator: str, countries: List[str], start_year: int, end_year: int) -> pd.DataFrame:
    """
    Fetch an indicator for a list of countries by calling the API per-country
    (avoids 400 errors that sometimes happen with long multi-country queries).
    """
    frames = []
    for idx, c in enumerate(countries, 1):
        try:
            df_c = fetch_indicator_country(indicator, c, start_year, end_year)
            frames.append(df_c)
        except Exception as e:
            print(f"[WARN] {indicator} for {c}: {e}")
        # be gentle with the API
        time.sleep(0.2)
    if not frames:
        return pd.DataFrame(columns=["country","year",indicator])
    return pd.concat(frames, ignore_index=True)

def compile_panel(countries: List[str], start_year: int, end_year: int, indicators: Dict[str,str]) -> pd.DataFrame:
    # Fetch each indicator separately, then merge on country,year
    dfs = []
    for label, code in indicators.items():
        print(f"[INFO] Fetching {label} ({code}) …")
        df = fetch_indicator(code, countries, start_year, end_year)
        df = df.rename(columns={code: label})
        dfs.append(df)

    out = dfs[0]
    for df in dfs[1:]:
        out = pd.merge(out, df, on=["country","year"], how="outer")

    # Transform Crisis from inflation (FP.CPI.TOTL.ZG) to a stress proxy:
    # stress = |inflation - 2%| clipped at 20% => 0..1
    if "Crisis" in out.columns:
        x = pd.to_numeric(out["Crisis"], errors="coerce")
        out["Crisis"] = (np.abs(x - 2.0)).clip(0, 20) / 20.0

    return out
