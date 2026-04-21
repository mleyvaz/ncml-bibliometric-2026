"""Lotka's law fit for NCML author productivity.

Classical Lotka: n(x) / n(1) = 1 / x^alpha.
We fit alpha via MLE (Newman 2005, eq. 3.1):
   alpha_hat = 1 + N * [ sum_i ln(x_i / x_min) ]^{-1}
and evaluate goodness of fit with a K-S test against the fitted power-law CDF.

Outputs:
  reports/clean/lotka_fit.json      — parameters + K-S stats
  reports/clean/lotka_loglog.png    — visualization
  reports/clean/lotka_fit.md        — narrative summary
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
LOTKA = ROOT / "data" / "author_clusters.csv"
REP = ROOT / "reports" / "clean"
REP.mkdir(exist_ok=True, parents=True)

clusters = pd.read_csv(LOTKA)
# Drop clusters with 0 articles (residual empty-name rows)
x = clusters["articles"].astype(int).to_numpy()
x = x[x >= 1]
N = len(x)
print(f"Authors: {N}")
print(f"Max articles/author: {x.max()}  Mean: {x.mean():.2f}")

# ---------- Fit (MLE, Newman) ----------
def fit_powerlaw_discrete(xs: np.ndarray, xmin: int = 1) -> dict:
    xs = xs[xs >= xmin]
    n = len(xs)
    # Continuous MLE approximation (valid when xmin >= 6). For xmin = 1 on
    # discrete data we use Newman's closed form with half-unit correction.
    # alpha_hat = 1 + n / sum(ln(x_i / (xmin - 0.5)))
    alpha = 1 + n / np.sum(np.log(xs / (xmin - 0.5)))
    # Standard error
    se = (alpha - 1) / np.sqrt(n)
    return {"alpha": float(alpha), "se": float(se), "n": n, "xmin": xmin, "xmax": int(xs.max())}

fit = fit_powerlaw_discrete(x, xmin=1)
print(f"Fit: alpha = {fit['alpha']:.3f} (SE {fit['se']:.3f})  n = {fit['n']}")

# ---------- Empirical vs theoretical distribution (K-S) ----------
# Build empirical PMF and CDF
vals, counts = np.unique(x, return_counts=True)
pmf_emp = counts / counts.sum()
cdf_emp = np.cumsum(pmf_emp)

# Theoretical PMF: p(x) = x^-alpha / Hurwitz zeta(alpha, 1)
from scipy.special import zeta
alpha = fit["alpha"]
xgrid = np.arange(1, x.max() + 1)
pmf_th = xgrid.astype(float) ** (-alpha) / zeta(alpha, 1)
cdf_th = np.cumsum(pmf_th)

# K-S statistic at observed values (interp theoretical CDF)
cdf_th_at_vals = cdf_th[vals - 1]
ks = float(np.max(np.abs(cdf_emp - cdf_th_at_vals)))
# Critical value at 5% for D > 1.36/sqrt(n)
crit_05 = 1.36 / np.sqrt(N)
ks_pass = ks < crit_05
print(f"K-S stat: {ks:.4f}   crit (5%): {crit_05:.4f}   pass (fit OK)? {ks_pass}")

# Expected fractions for key Lotka benchmarks
frac_1 = pmf_th[0]  # fraction of authors with exactly 1 article
# Classical Lotka: ~60% with 1 article when alpha=2
print(f"Theoretical P(x=1): {frac_1:.3f}  Empirical P(x=1): {pmf_emp[0]:.3f}")

# ---------- Plot ----------
fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))

# Left: log-log with fit
vals_plot = vals.astype(float)
ax[0].loglog(vals_plot, counts, "o", label="Empirico")
ax[0].loglog(xgrid, counts.sum() * pmf_th, "r-", label=f"Lotka ajustado alpha = {alpha:.2f}")
ax[0].set_xlabel("Articulos por autor (x)")
ax[0].set_ylabel("Numero de autores n(x)")
ax[0].set_title("Ley de Lotka (NCML 2018-2026)")
ax[0].legend()
ax[0].grid(True, which="both", alpha=0.3)

# Right: CDF comparison
ax[1].step(vals, cdf_emp, where="post", label="Empirica")
ax[1].step(xgrid, cdf_th, where="post", label="Teorica (Lotka)", linestyle="--")
ax[1].set_xlabel("Articulos por autor (x)")
ax[1].set_ylabel("CDF acumulada")
ax[1].set_title(f"Comparacion CDF (K-S = {ks:.3f})")
ax[1].legend()
ax[1].grid(True, alpha=0.3)
ax[1].set_xscale("log")

plt.tight_layout()
plt.savefig(REP / "lotka_loglog.png", dpi=150)
plt.close()

# ---------- Save ----------
out = {
    **fit,
    "ks_stat": ks,
    "ks_crit_05": crit_05,
    "ks_pass": bool(ks_pass),
    "empirical_P_x_1": float(pmf_emp[0]),
    "theoretical_P_x_1": float(frac_1),
}
(REP / "lotka_fit.json").write_text(json.dumps(out, indent=2))

# Narrative summary
md = [
    "# Ajuste de Ley de Lotka — NCML",
    "",
    f"**Autores totales (post desambiguacion):** {N}",
    f"**Maximo articulos por autor:** {x.max()}",
    f"**Media:** {x.mean():.2f} articulos/autor",
    "",
    "## Resultado del ajuste (MLE Newman)",
    "",
    f"- **alpha = {alpha:.3f}** (SE {fit['se']:.3f})",
    f"- Lotka clasica predice alpha = 2.0.",
    f"- Nuestro alpha {'esta por encima' if alpha > 2 else 'esta por debajo'} de la referencia clasica.",
    "",
    "## Bondad de ajuste (K-S)",
    "",
    f"- K-S statistic = {ks:.4f}",
    f"- Valor critico al 5% = {crit_05:.4f}",
    f"- **{'Pasa' if ks_pass else 'No pasa'} el test:** los datos "
    f"{'siguen' if ks_pass else 'NO siguen'} estrictamente una distribucion Lotka pura.",
    "",
    "## Interpretacion",
    "",
    f"- P(autor con 1 articulo) empirica: {pmf_emp[0]:.1%}",
    f"- P teorica segun Lotka ajustado: {frac_1:.1%}",
    "",
    "Un alpha > 2 indica distribucion MAS concentrada que Lotka clasica — la base de ",
    "autores one-shot es proporcionalmente mayor y la cola larga (grandes productores)",
    "mas delgada. Es un perfil tipico de revistas jovenes con alto flujo de autores ",
    "nuevos (estudiantes, tesistas) y un nucleo editorial muy pequeno.",
    "",
    "## Figura",
    "",
    "![Lotka log-log + CDF](lotka_loglog.png)",
]
(REP / "lotka_fit.md").write_text("\n".join(md), encoding="utf-8")
print(f"\nWrote {REP / 'lotka_fit.md'} and {REP / 'lotka_loglog.png'}")
