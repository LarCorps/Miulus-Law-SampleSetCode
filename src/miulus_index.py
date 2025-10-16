import numpy as np
import pandas as pd

def robust_scale01(s, clip=True):
    s = pd.to_numeric(s, errors="coerce")
    # If this group is all-NaN, return 0.5 constants without calling nanpercentile
    if s.notna().sum() == 0:
        out = pd.Series([0.5]*len(s), index=s.index)
        return out
    vals = s.dropna().values
    lo, hi = np.nanpercentile(vals, 5), np.nanpercentile(vals, 95)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi == lo:
        out = pd.Series([0.5]*len(s), index=s.index)
    else:
        out = (s - lo) / (hi - lo)
    if clip:
        out = out.clip(0, 1)
    return out

def compute_E(df, s_col, n_col, r_col, by="year"):
    d = df.copy()
    d["_S"] = d.groupby(by)[s_col].transform(robust_scale01)
    d["_N_raw"] = d.groupby(by)[n_col].transform(robust_scale01)
    d["_N"] = d["_N_raw"].clip(1e-9, None)
    d["_R"] = d.groupby(by)[r_col].transform(robust_scale01)
    d["E"] = (d["_S"] / d["_N"]) * d["_R"]
    d["E"] = d["E"].clip(0, 1.5)
    return d

def hazard_transform(E, Ec, gamma):
    E = np.asarray(E, dtype=float)
    E = np.where(E <= 1e-9, 1e-9, E)
    return (Ec / E) ** gamma

def fit_hazard_gamma(E, crisis, Ec=None, grid=(1.2, 4.1, 0.1)):
    E = np.asarray(E, dtype=float)
    y = np.asarray(crisis, dtype=float)
    y = (y - np.nanmin(y)) / (np.nanmax(y) - np.nanmin(y) + 1e-9)
    if Ec is None:
        Ec = float(np.nanpercentile(E, 25))
    best = None
    gstart, gend, gstep = grid
    for g in np.arange(gstart, gend, gstep):
        pred = (Ec / np.maximum(E, 1e-9)) ** g
        pred = (pred - np.nanmin(pred)) / (np.nanmax(pred) - np.nanmin(pred) + 1e-9)
        se = float(np.nanmean((pred - y) ** 2))
        if best is None or se < best[0]:
            best = (se, float(g), float(Ec))
    return {"mse": best[0], "gamma": best[1], "Ec": best[2]}
