Excellent — now that I’ve seen your real code and config, here’s the **final README.md** that matches your actual implementation.
It’s shorter, cleaner, and exactly mirrors what the project does — including World Bank data compilation, E-index computation, and hazard curve analysis.

---

# Miulus Law – Global Panel Analysis (Sample Set)

Reproducible code accompanying:

> **Lauri Korpela (2025)**
> *The Miulus Law: Epistemic Fitness as a Universal Constraint on Self-Referential Systems*
> Zenodo DOI: **https://zenodo.org/records/17365378**

This repository demonstrates how to compute **epistemic fitness (E)** and fit the **hazard curve** described in the paper using publicly available global indicators.
It also serves as a template for testing the Miulus Law in any other dataset or domain.

> ⚠️ The included sample dataset and configuration are illustrative. Replace them with your own indicators or domain data to reproduce the law in other systems.

---

## 🔹 What It Does

1. Fetches **World Bank indicators** for a list of countries (signal, noise, reach, crisis proxies).
2. Compiles them into a unified panel dataset.
3. Computes **epistemic fitness E = (S/N)·R** using robust scaling.
4. Fits the **hazard curve** to estimate the instability threshold `E_c` and exponent `γ`.
5. Exports processed data, figures, and basic causality diagnostics.

---

## 🔹 Project Structure

```
Miulus-Law-Panel/
├── config.yaml               # Indicator mapping and fit parameters
├── data/
│   └── compiled_panel.csv    # Pre-fetched sample dataset (replaceable)
├── outputs/
│   ├── compiled_panel_with_E.csv
│   ├── hazard_curve.png
│   ├── hazard_fit.json
│   ├── scatter_E_vs_crisis.png
│   └── granger_summary.json
├── requirements.txt
├── run.py                    # Main entry point
└── src/
    ├── compile.py            # Fetches and compiles World Bank data
    ├── miulus_index.py       # Computes E and fits hazard model
    └── analyze.py            # Orchestrates full analysis and plotting
```

---

## 🔹 Setup & Execution

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# run full pipeline (uses data/compiled_panel.csv by default)
python run.py
```

Outputs are saved under `outputs/`:

* `compiled_panel_with_E.csv` – data with computed epistemic fitness
* `hazard_fit.json` – fitted parameters (`E_c`, `γ`)
* `hazard_curve.png`, `scatter_E_vs_crisis.png` – figures
* `granger_summary.json` – pooled lag causality results

---

## 🔹 Configuration (`config.yaml`)

Defines:

* Which indicators represent **signal**, **noise**, **reach**, and **crisis**
* Country list and date range
* Fitting parameters and plotting options

Example:

```yaml
countries: [FIN, SWE, NOR, DNK, ISL]
years: [1996, 2024]
indicators:
  S_proxy: NY.GDP.PCAP.KD.ZG
  N_proxy: PV.EST
  R_proxy: IT.NET.USER.ZS
  Crisis: FP.CPI.TOTL.ZG
fit:
  Ec_percentile: 25
  gamma_grid: [1.2, 4.1, 0.1]
plots:
  dpi: 200
```

---

## 🔹 Replace with Your Own Data

To analyze a different system:

1. Replace or regenerate `data/compiled_panel.csv`.

   * Use `src/compile.py` with your country list or local dataset.
2. Update `config.yaml` with your column names or new proxies.
3. Run `python run.py` — all derived files update automatically.

**Examples of reuse:**

* **AI training:** verified vs. synthetic data ratio (S/N) and validation frequency (R).
* **Neuroscience:** sensory precision vs. noise vs. feedback gain.
* **Sociology:** fact-checked vs. unverified information and media reach.

---

## 🔹 Outputs Overview

| File                        | Description                            |
| --------------------------- | -------------------------------------- |
| `compiled_panel_with_E.csv` | Final dataset with computed E values   |
| `hazard_fit.json`           | Fitted parameters for the hazard model |
| `hazard_curve.png`          | Normalized hazard vs. E plot           |
| `scatter_E_vs_crisis.png`   | Scatterplot of E vs. crisis intensity  |
| `granger_summary.json`      | F-test results for lagged causality    |

---

## 🔹 Citation

If you use this repository, please cite:

> **Korpela, L.** (2025). *The Miulus Law: Epistemic Fitness as a Universal Constraint on Self-Referential Systems.* Zenodo. DOI: **https://zenodo.org/records/17365378**

---

## 🔹 License

* **Code:** MIT
* **Sample data:** CC BY 4.0

---