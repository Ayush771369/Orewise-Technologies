# OreWise Technologies — Mineral Processing Website

A Streamlit educational prototype for a preliminary hematite–quartz beneficiation concept.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Important data warning
`data/aspen_results_sample.csv` is **illustrative placeholder data**, not Aspen Plus output and not validated plant performance. Replace it with a CSV exported from Aspen Plus V14 using the same column names:

- `feed_rate_kg_hr`
- `grind_p80_um`
- `concentrate_mass_kg_hr`
- `concentrate_hematite_wt_pct`
- `hematite_recovery_pct`
- `tailings_mass_kg_hr`
- `tailings_hematite_wt_pct`

The simulator uses bounded bilinear interpolation and refuses inputs outside the dataset range. The data must form a complete rectangular grid of feed rate and grind P80 values.

## Engineering limitations
The settling model represents an isolated spherical particle in a Newtonian fluid. It is not a spiral-concentrator model and should not be used to claim actual spiral recovery. Validate assumptions, liberation size, water balance, equipment sizing and separation performance before making engineering claims.

## Deploy
Push this folder to a GitHub repository, then create a Streamlit Community Cloud app pointing to `app.py`.
# Orewise-Technologies
