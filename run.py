import argparse, yaml
from pathlib import Path
from src.compile import compile_panel
from src.analyze import run_analysis

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--outdir", default="outputs")
    ap.add_argument("--datadir", default="data")
    args = ap.parse_args()

    with open(args.config,"r") as f:
        cfg = yaml.safe_load(f)

    countries = cfg["countries"]
    start_year = cfg["start_year"]
    end_year = cfg["end_year"]
    indicators = cfg["indicators"]

    datadir = Path(args.datadir); datadir.mkdir(parents=True, exist_ok=True)
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    panel = compile_panel(countries, start_year, end_year, indicators)
    panel_path = datadir/"compiled_panel.csv"
    panel.to_csv(panel_path, index=False)
    print(f"[OK] Saved panel to {panel_path} ({len(panel)} rows)")

    fit, granger = run_analysis(str(panel_path), str(outdir))
    print("[OK] Hazard fit:", fit)
    print("[OK] Granger summary:", granger)
    print(f"[DONE] Outputs in {outdir}")

if __name__ == "__main__":
    main()
