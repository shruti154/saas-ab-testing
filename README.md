# SaaS A/B Testing — Free Trial Screener Analysis

> **Can filtering low-intent users improve course completion without hurting revenue?**
> This project analyses a real A/B experiment run by Udacity to find out — and the answer is more nuanced than expected.

---

## The Business Problem

Udacity was losing coach time and resources on students who signed up for a free trial, struggled in week one, and dropped out before paying. Their proposed fix: add a **screener** to the signup flow asking users how many hours per week they could commit.

- Users who said **less than 5 hours** → redirected to free course materials
- Users who said **5 hours or more** → proceeded to checkout as normal

The hypothesis was simple: filter out low-intent students upfront, reduce dropouts, protect coach capacity — without hurting revenue.

---

## What was Measured

Two metrics were chosen to evaluate the experiment:

| Metric | Formula | What it tells us |
|---|---|---|
| **Gross Conversion** | Enrollments / Clicks | Did the screener reduce signups? |
| **Net Conversion** | Payments / Clicks | Did the screener protect revenue? |

For the experiment to justify a launch, gross conversion needed to **decrease** (fewer but better students) and net conversion needed to **stay the same or improve** (revenue protected).

---

## Key Findings

| Metric | Control | Experiment | Difference | Statistically Significant | Practically Significant |
|---|---|---|---|---|---|
| Gross Conversion | 21.89% | 19.83% | −2.06% | ✅ Yes | ✅ Yes |
| Net Conversion | 11.76% | 11.27% | −0.49% | ❌ No | ❌ No |

**Gross conversion fell significantly** — the screener successfully filtered out low-intent users. This result passed both the statistical test (p-value ≈ 0.0) and the practical significance threshold (d_min = 1%).

**Net conversion also fell** — and this is the problem. The drop was small (0.49%) and not statistically significant, but we cannot rule out that the screener was turning away users who would have paid. The 95% confidence interval crosses the practical significance boundary of −0.75%.

---

## Recommendation: Do Not Launch

A product change that reduces enrolments without protecting payments leaves the business worse off. Both metrics must pass for a launch to make business sense — net conversion fails both tests.

**Suggested next steps for Udacity:**
- Reframe the screener as encouragement rather than a gate
- Test the screener on high-dropout courses only
- Explore alternative interventions: week-1 check-ins, better onboarding content, progress nudges

---

## Statistical Method

- **Test:** Two-proportion z-test (two-sided)
- **Significance level:** α = 0.05
- **Practical significance thresholds:** Gross Conversion ±0.01, Net Conversion ±0.0075
- **Data:** 37-day observation window, 23 days used for conversion analysis (last 14 rows excluded — trials not yet complete at experiment end)
- **Sanity check:** Traffic split verified within 95% confidence interval before analysis

---

## Why Only 23 Days?

The experiment ran for 37 days. But payments require a 14-day trial window. Users who enrolled in the final 14 days of the experiment had not yet finished their trial by the time data collection stopped — so their payment data was incomplete. Using those rows would have introduced bias. Only the first 23 days — where both enrolment and payment data were complete — were used for conversion analysis.

This was a deliberate analytical decision, not an oversight.

---

## Stack

- **Python** — pandas, scipy, matplotlib
- **Dataset** — Real experiment data from Udacity (2014), sourced publicly
- **Analysis** — Statistical hypothesis testing, confidence intervals, practical significance


---

## Part 2 — AI Experiment Brief Generator

Inspired by how Optimizely is integrating AI into their experimentation platform, this tool takes a business problem as input and generates a fully structured A/B test brief using Claude.

### How to run it
```bash
python experiment_brief_generator.py
```

You will be prompted for five inputs:
- Business problem
- Metric to improve
- Target user
- Proposed change
- Success criteria

Claude returns a complete experiment brief including hypothesis, primary and secondary metrics, experiment design, risks, and recommendations.

### Why this matters

Most companies run A/B tests with vague hypotheses and wrong metrics. This tool forces rigour into experiment design — the same problem Optimizely's AI tooling is solving at scale.


---

## Skills Demonstrated

- A/B test design and evaluation
- Statistical hypothesis testing (z-test, p-values, confidence intervals)
- Distinguishing statistical vs practical significance
- Data cleaning and handling missing values
- Translating analytical findings into a clear business recommendation
- Python data analysis and visualisation

---

*Shruti M. | [GitHub](https://github.com/shruti154)*