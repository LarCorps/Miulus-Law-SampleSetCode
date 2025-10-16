# Miulus Law — Auto-Compile Dataset & Analysis Toolkit

This package fetches public indicators (World Bank API), compiles a composite dataset for
S, N, R, and Crisis, computes the Epistemic Fitness index **E = (S/N) * R**, fits the hazard
curve **h(E) ∝ (E_c / E)^γ**, and runs Granger-causality tests (ΔE → ΔCrisis, 1–3 lags).
It saves publication-ready figures and CSVs in `outputs/`.

## Quick start

```bash
python -m venv .venv && . .venv/bin/activate   # (Windows: .\.venv\Scripts\activate)
pip install -r requirements.txt
python run.py
```
