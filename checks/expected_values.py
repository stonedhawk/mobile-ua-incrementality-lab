"""Independent expected values for Lift Lab's worked examples.

Written from the formulas in the README and the in-tool Methods section,
not from index.html, so the two share no code. Compare the printed values
with what the page shows for the same inputs (see "Checking the math" in
the README).

    pip install numpy scipy statsmodels
    python checks/expected_values.py
"""
import json
import math

from scipy import stats, integrate
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import samplesize_proportions_2indep_onetail

out = {}

def design_prop(p1, mde, conf, power, split):
    p2 = p1 * (1 + mde)
    za, zb = stats.norm.ppf(1 - (1 - conf) / 2), stats.norm.ppf(power)
    pb = (p1 + p2) / 2
    n_arm = (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2
    total = 2 * n_arm / (4 * split * (1 - split))
    # statsmodels cross-check (equal split, per arm)
    sm = samplesize_proportions_2indep_onetail(diff=p2 - p1, prop2=p1, power=power, ratio=1, alpha=1 - conf, alternative="two-sided")
    return dict(n_arm_equal=n_arm, statsmodels_n_arm_equal=sm, total=total, test=total * split, control=total * (1 - split))


def design_rev(cv, mde, conf, power, split):
    za, zb = stats.norm.ppf(1 - (1 - conf) / 2), stats.norm.ppf(power)
    n_arm = 2 * (za + zb) ** 2 * cv ** 2 / mde ** 2
    sm = NormalIndPower().solve_power(effect_size=mde / cv, alpha=1 - conf, power=power, ratio=1, alternative="two-sided")
    total = 2 * n_arm / (4 * split * (1 - split))
    return dict(n_arm_equal=n_arm, statsmodels_n_arm_equal=sm, total=total, test=total * split, control=total * (1 - split))


d1 = design_prop(0.02, 0.10, 0.95, 0.80, 0.50)
d1["days"] = d1["total"] / 20000
d2 = design_rev(4, 0.05, 0.90, 0.90, 0.30)
d2["days"] = d2["total"] / 50000
d3 = design_prop(0.05, 0.03, 0.99, 0.95, 0.20)
d3["days"] = d3["total"] / 10000
out["lift_design"] = {"conv_default": d1, "rev_cv4_mde5_90_90_split30_50k": d2, "conv_5pct_mde3_99_95_split20_10k": d3}


def p_better_beta(cc, nc, ct, nt):
    a_c, b_c, a_t, b_t = cc + 1, nc - cc + 1, ct + 1, nt - ct + 1
    lo = min(stats.beta.ppf(1e-9, a_c, b_c), stats.beta.ppf(1e-9, a_t, b_t))
    hi = max(stats.beta.ppf(1 - 1e-9, a_c, b_c), stats.beta.ppf(1 - 1e-9, a_t, b_t))
    f = lambda x: stats.beta.pdf(x, a_c, b_c) * stats.beta.sf(x, a_t, b_t)
    v, _ = integrate.quad(f, lo, hi, limit=400, points=[cc / nc, ct / nt])
    return v


def read_conv(nc, cc, nt, ct, spend, rev, conf):
    rc, rt = cc / nc, ct / nt
    se = math.sqrt(rc * (1 - rc) / nc + rt * (1 - rt) / nt)
    z = (rt - rc) / se
    p = 2 * stats.norm.sf(abs(z))
    inc = (rt - rc) * nt
    zc = stats.norm.ppf(1 - (1 - conf) / 2)
    return dict(rel_lift=(rt - rc) / rc, p=p, p_better=p_better_beta(cc, nc, ct, nt),
                ci_abs=[rt - rc - zc * se, rt - rc + zc * se],
                inc_conv=inc, naive_cpi=spend / ct, icpi=spend / inc,
                naive_roas=ct * rev / spend, iroas=inc * rev / spend, over=ct / inc)


def read_rev(nc, mc, cvc, nt, mt, cvt, spend):
    se = math.sqrt((cvc * mc) ** 2 / nc + (cvt * mt) ** 2 / nt)
    z = (mt - mc) / se
    return dict(rel_lift=(mt - mc) / mc, p=2 * stats.norm.sf(abs(z)), p_better_normal=stats.norm.cdf(z),
                inc_rev=(mt - mc) * nt, iroas=(mt - mc) * nt / spend)


out["lift_read"] = {
    "conv_default": read_conv(50000, 1000, 50000, 1150, 8000, 60, 0.95),
    "conv_20k_400_vs_430": read_conv(20000, 400, 20000, 430, 3000, 25, 0.95),
    "rev_default": read_rev(50000, 0.50, 4, 50000, 0.56, 4, 8000),
}


def reconcile(rows):
    corr = [(v / b, w) for v, w, b in rows]
    blend = sum(v * w for v, w in corr) / sum(w for _, w in corr)
    vals = [v for v, _ in corr]
    return dict(corrected=vals, blend=blend, lo=min(vals), hi=max(vals))


out["lift_reconcile"] = {
    "default": reconcile([(145, 35, 1.30), (78, 80, 1.0), (95, 55, 1.0), (105, 100, 1.0)]),
    "custom": reconcile([(220, 20, 1.6), (90, 70, 1.1), (60, 40, 0.8), (88, 100, 1.0)]),
}

print(json.dumps(out, indent=1, default=float))
