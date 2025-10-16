# Miulus Law – Global Panel Analysis (Sample Set)

Reproducible code accompanying:

> **Lauri Korpela (2025)**
> *The Miulus Law: Epistemic Fitness as a Universal Constraint on Self-Referential Systems*
> [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17365378.svg)](https://doi.org/10.5281/zenodo.17365378)

This repository demonstrates how to compute **epistemic fitness $${E}$$** and fit the **hazard curve** described in the paper using publicly available global indicators.
It also serves as a template for testing the Miulus Law in other datasets and domains.

> ⚠️ The included sample dataset and configuration are illustrative. Replace them with your own indicators or domain data to reproduce the law empirically.

---

## 🔹 What It Does

1. Fetches **World Bank indicators** for a list of countries (signal, noise, reach, crisis proxies).
2. Compiles them into a unified panel dataset.
3. Computes **epistemic fitness** $${E}$$ and fits the **hazard model** to derive instability parameters $${E_c}$$ and $${\gamma}$$.
4. Exports processed data, figures, and summary statistics.

---

## 🔹 Core Formulas

### Epistemic Fitness

$$
E = \frac{S}{N}R
$$

Where:

* $${S}$$ = verified or grounded signal
* $${N}$$ = informational noise
* $${R}$$ = feedback reach (the system’s capacity to self-correct)

Epistemic fitness quantifies how well a system maintains meaningful correlation with reality.

---

### Hazard Model

$$
h(E) = \left(\frac{E_c}{E}\right)^{\gamma}, \qquad E_c>0,\ \gamma>1
$$

Where:

* $${E_c}$$ is the **instability threshold** — below this, collapse probability rises steeply.
* $${\gamma}$$ is the **hazard curvature** — how sharply the risk accelerates near or below $${E_c}$$.

Parameter estimation is done by minimizing the log-space squared error:

$$
\min_{E_c,\gamma}\ \sum_i w_i\Big(\log \hat h_i - \log \big[(E_c/E_i)^{\gamma}\big]\Big)^2
$$

*(Implemented via grid search or nonlinear least squares.)*

$$
E = \frac{S}{N}R
$$

$$
h(E) = \left(\frac{E_c}{E}\right)^{\gamma}
$$


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
source .venv/bin/activate     # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# run full pipeline (uses data/compiled_panel.csv by default)
python run.py
```

Outputs appear under `outputs/`:

* `compiled_panel_with_E.csv` – dataset with computed E
* `hazard_fit.json` – fitted parameters (`E_c`, `γ`)
* `hazard_curve.png`, `scatter_E_vs_crisis.png` – plots
* `granger_summary.json` – causality diagnostics

---

## 🔹 Configuration (`config.yaml`)

Defines:

* Which indicators represent **signal $${S}$$**, **noise (N)**, **reach (R)**, and **crisis**
* Country list and date range
* Fitting and plotting options

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

   * Use `src/compile.py` with your chosen country list or dataset.
2. Update `config.yaml` with new column names or indicators.
3. Run `python run.py`.

**Domain examples:**

* **AI training:** verified-to-synthetic ratio $${S/N}$$, and audit frequency $${R}$$.
* **Neuroscience:** sensory precision $${S}$$, neural noise $${N}$$, and feedback gain $${R}$$.
* **Sociology:** fact-checked share $${S}$$, misinformation share $${N}$$, media reach $${R}$$.

---

## 🔹 Outputs Overview

| File                        | Description                           |
| --------------------------- | ------------------------------------- |
| `compiled_panel_with_E.csv` | Data with computed epistemic fitness  |
| `hazard_fit.json`           | Fitted parameters (`E_c`, `γ`)        |
| `hazard_curve.png`          | Hazard vs. E plot                     |
| `scatter_E_vs_crisis.png`   | Scatterplot of E vs. crisis intensity |
| `granger_summary.json`      | Lagged causality results              |

---

## 🔹 Citation

If you use this repository, please cite:

> **Korpela, L.** (2025). *The Miulus Law: Epistemic Fitness as a Universal Constraint on Self-Referential Systems.* [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17365378.svg)](https://doi.org/10.5281/zenodo.17365378)

---

## 🔹 License

* **Code:** MIT
* **Sample data:** CC BY 4.0

---
