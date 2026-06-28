# 🧪 Lift Lab: Mobile UA Incrementality

[![▶ Live Demo](https://img.shields.io/badge/▶_Live_Demo-stonedhawk.github.io-7aa2f7?style=for-the-badge)](https://stonedhawk.github.io/mobile-ua-incrementality-lab/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![No dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)
[![Single file](https://img.shields.io/badge/build-none%20·%20single%20file-blue.svg)](#)

**Design incrementality tests, read the results honestly, and reconcile the conflicting numbers your platforms, MMP, and finance team all report.** Built for post-ATT mobile UA, where last-click attribution quietly lies. Everything runs in the browser. No SDK, no backend, nothing leaves the page.

### ▶ Try it live: **[stonedhawk.github.io/mobile-ua-incrementality-lab](https://stonedhawk.github.io/mobile-ua-incrementality-lab/)**

---

## 🎯 Three tools in one

**1. Design a test.** Pick a metric (conversion rate or revenue), the smallest lift worth catching, your confidence and power, and your daily traffic. It returns the sample size per arm, the total, the duration, and a blunt verdict when your traffic simply can't prove a lift that small. No false confidence.

**2. Read the results.** Feed it control vs test and it returns the lift, a frequentist p-value, the Bayesian probability the variant is actually better (8,000-sample Monte Carlo over Beta posteriors), the full posterior distribution, and the punchline: naive CPI and ROAS vs the true incremental ones, with the over-counting multiple. The default case shows a platform claiming 862% ROAS while the real incremental is 112%, a 7.7x over-credit.

**3. Reconcile the numbers.** When you can't run a holdout, your platform, MMP, SKAN, and finance figures disagree wildly. Give each a trust weight and a bias correction and it blends them into one defensible ROAS with a disagreement band, so you stop arguing over which dashboard to believe.

Every stat, metric, and widget has a tooltip explaining the jargon in plain terms, and the full methods are documented inside the tool.

---

## 🧮 What's under the hood

| Step | Method |
|------|--------|
| **Sample size (rates)** | Two-proportion normal approximation; unequal splits inflated by `1/(4·s·(1-s))` |
| **Sample size (revenue)** | `n/arm = 2·(z₁₋α/2+z₁₋β)²·CV²/MDE²`, since revenue is skewed and CV does the work |
| **Reading a test** | Lift, standard error, two-sided z, p-value, and a 95% confidence interval |
| **Bayesian readout** | `Beta(conv+1, non-conv+1)` posteriors, 8,000 Monte-Carlo draws for P(better) and the credible interval |
| **Incremental economics** | Incremental conversions = (rate_test − rate_control)·n_test; from there iCPI and iROAS |
| **Reconciliation** | Trust-weighted average of bias-corrected sources, with the spread as the band |

The statistics are validated against scipy and statsmodels (sample sizes within 0.05% of statsmodels; p-values match scipy).

---

## ⚠️ The honest limit

A calculator designs and reads tests. It can't run a clean holdout for you, and a contaminated test/control split produces confident nonsense. At very low spend, no test can detect a realistic lift, and the tool says so out loud instead of pretending otherwise. The reconcile tab is a disciplined way to combine conflicting numbers, not a substitute for actually measuring.

---

## 🚀 Run it

Use the **[hosted version](https://stonedhawk.github.io/mobile-ua-incrementality-lab/)**, or run it locally. It's one file, no build step:

```bash
git clone https://github.com/stonedhawk/mobile-ua-incrementality-lab.git
open mobile-ua-incrementality-lab/index.html
```

---

## 📄 License

[MIT](LICENSE). Use it inside your studio or fork it freely.

---

Companion to the [LTV &amp; ROAS Modeler](https://stonedhawk.github.io/mobile-ltv-roas-modeler/): model the LTV, measure the incrementality, trust one number. Built by [Rahul Shah](https://github.com/stonedhawk), 16 years producing mobile games by day, packaging producer problems into tools by night.
