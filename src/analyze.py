import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.stattools import grangercausalitytests
from src.miulus_index import compute_E, fit_hazard_gamma, hazard_transform, robust_scale01

def run_analysis(panel_csv: str, outdir: str):
    outd = Path(outdir); outd.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(panel_csv)
    # Invert Political Stability (PV.EST) into Noise (higher = worse)
    df["_N_stability"] = df.groupby("year")["N_proxy"].transform(robust_scale01)
    df["N_noise"] = 1.0 - df["_N_stability"]
    dE = compute_E(df, s_col="S_proxy", n_col="N_noise", r_col="R_proxy", by="year")
    dE["Crisis"] = df["Crisis"].values

    fit = fit_hazard_gamma(dE["E"], dE["Crisis"], Ec=None, grid=(1.2,4.1,0.1))
    Ec, gamma = fit["Ec"], fit["gamma"]
    with open(outd/"hazard_fit.json","w") as f:
        json.dump(fit, f, indent=2)

    # Scatter
    import matplotlib
    plt.figure()
    plt.scatter(dE["E"], dE["Crisis"], alpha=0.35)
    plt.xlabel("Epistemic Fitness E")
    plt.ylabel("Crisis (scaled)")
    plt.title("E vs Crisis (all country-years)")
    plt.tight_layout()
    plt.savefig(outd/"scatter_E_vs_crisis.png", dpi=160)

    # Hazard curve
    xs = np.linspace(max(0.01, np.nanmin(dE["E"])), max(0.75, np.nanmax(dE["E"])), 200)
    h = hazard_transform(xs, Ec, gamma)
    h = (h - np.nanmin(h)) / (np.nanmax(h) - np.nanmin(h) + 1e-9)
    plt.figure()
    plt.plot(xs, h)
    plt.axvline(Ec, linestyle="--")
    plt.xlabel("E")
    plt.ylabel("Scaled hazard ~ (Ec/E)^gamma")
    plt.title(f"Hazard curve fit: Ec={Ec:.2f}, gamma={gamma:.2f}")
    plt.tight_layout()
    plt.savefig(outd/"hazard_curve.png", dpi=160)

    # Granger pooled Δ tests (1..3 lags)
    dd = dE[["country","year","E","Crisis"]].dropna().sort_values(["country","year"]).copy()
    dd["dE"] = dd.groupby("country")["E"].diff()
    dd["dC"] = dd.groupby("country")["Crisis"].diff()
    gmat = dd[["dC","dE"]].dropna()
    results = {}
    if len(gmat) > 10:
        gr = grangercausalitytests(gmat[["dC","dE"]], maxlag=3, verbose=False)
        for lag, res in gr.items():
            F, p = res[0]["ssr_ftest"][:2]
            results[str(lag)] = {"F": float(F), "p": float(p)}  # <-- stringify key
    with open(outd/"granger_summary.json","w") as f:
        json.dump(results, f, indent=2)


    dE.to_csv(outd/"compiled_panel_with_E.csv", index=False)
    return fit, results
