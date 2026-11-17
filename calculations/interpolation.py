"""Load a two-input dataset and perform bounded bilinear interpolation."""
import pandas as pd

REQUIRED = [
    "feed_rate_kg_hr", "grind_p80_um", "concentrate_mass_kg_hr",
    "concentrate_hematite_wt_pct", "hematite_recovery_pct",
    "tailings_mass_kg_hr", "tailings_hematite_wt_pct"
]

def load_dataset(path):
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("CSV is missing required columns: " + ", ".join(missing))
    return df

def _bracket(values, x):
    vals = sorted(set(float(v) for v in values))
    if x < vals[0] or x > vals[-1]:
        raise ValueError(f"Input {x:g} is outside the dataset range {vals[0]:g}–{vals[-1]:g}. No extrapolation is performed.")
    lo = max(v for v in vals if v <= x)
    hi = min(v for v in vals if v >= x)
    return lo, hi

def interpolate_results(df, feed, p80):
    flo, fhi = _bracket(df.feed_rate_kg_hr, feed)
    plo, phi = _bracket(df.grind_p80_um, p80)

    def row(f, p):
        match = df[(df.feed_rate_kg_hr == f) & (df.grind_p80_um == p)]
        if match.empty:
            raise ValueError(f"Dataset is missing grid point feed={f:g}, P80={p:g}. Supply a complete rectangular grid.")
        return match.iloc[0]

    corners = [(flo, plo), (fhi, plo), (flo, phi), (fhi, phi)]
    rows = [row(f, p) for f, p in corners]

    if fhi == flo:
        tf = 0.0
    else:
        tf = (feed - flo) / (fhi - flo)
    if phi == plo:
        tp = 0.0
    else:
        tp = (p80 - plo) / (phi - plo)

    weights = [(1-tf)*(1-tp), tf*(1-tp), (1-tf)*tp, tf*tp]
    result = {"feed_rate_kg_hr": float(feed), "grind_p80_um": float(p80)}
    for col in REQUIRED[2:]:
        result[col] = sum(w * float(r[col]) for w, r in zip(weights, rows))
    return result
