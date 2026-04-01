import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt 

control = pd.read_csv('data/control_data.csv')
experiment = pd.read_csv('data/experiment_data.csv')

print(control.head())
print(experiment.head())

print(control.shape)
print(experiment.shape)

print(control.isnull().sum())

control_clean = control.dropna(subset = ['Enrollments', 'Payments'])
experiment_clean = experiment.dropna(subset = ['Enrollments', 'Payments'])
print(control_clean.shape)
print(experiment_clean.shape)

gross_conversion_ctrl = control_clean['Enrollments'].sum()/ control_clean['Clicks'].sum()
net_conversion_ctrl = control_clean['Payments'].sum()/ control_clean['Clicks'].sum()

gross_conversion_exp = experiment_clean['Enrollments'].sum()/ experiment_clean ['Clicks'].sum()
net_conversion_exp = experiment_clean['Payments'].sum()/ experiment_clean['Clicks'].sum()

print("Gross Conversion - Control:", round(gross_conversion_ctrl,4))
print("Gross Conversion - Experiment:", round(gross_conversion_exp,4))
print("Net Conversion - Control:", round(net_conversion_ctrl,4))
print("Net Conversion - Experiment:", round(net_conversion_exp,4))

## Two-proportion z-test
ctrl_clicks = control_clean['Clicks'].sum()
exp_clicks = experiment_clean ['Clicks'].sum()

ctrl_enrollments = control_clean ['Enrollments'].sum()
exp_enrollments = experiment_clean ['Enrollments'].sum()

ctrl_payments = control_clean ['Payments'].sum()
exp_payments = experiment_clean ['Payments'].sum()

print("Control clicks:", ctrl_clicks)
print("Experiment clicks:", exp_clicks)
print("Control enrollments:", ctrl_enrollments)
print("Experiment enrollments:", exp_enrollments)
print("Control payments:", ctrl_payments)
print("Experiment payments:", exp_payments)

from scipy import stats
import numpy as np

def z_test(successes_ctrl, n_ctrl, successes_exp, n_exp):
    p_ctrl = successes_ctrl / n_ctrl
    p_exp = successes_exp / n_exp
    p_pool = (successes_ctrl + successes_exp) / (n_ctrl + n_exp)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n_ctrl + 1/n_exp))
    z = (p_exp - p_ctrl) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value
    
gc_z, gc_p = z_test(ctrl_enrollments, ctrl_clicks, exp_enrollments, exp_clicks)
nc_z, nc_p = z_test(ctrl_payments, ctrl_clicks, exp_payments, exp_clicks)

print("Gross Conversion z-score:", round(gc_z, 4))
print("Gross Conversion p-value:", round(gc_p, 4))
print("Net Conversion z-score:", round(nc_z, 4))
print("Net Conversion p-value:", round(nc_p, 4))

d_min_gross = 0.01
d_min_net = 0.0075

gc_diff = gross_conversion_exp - gross_conversion_ctrl
nc_diff = net_conversion_exp - net_conversion_ctrl

print("gross Conversion difference:", round(gc_diff,4))
print("Practically significant:",abs(gc_diff) >= d_min_gross)

print("Net Conversion difference:", round(nc_diff, 4))
print("Practically significant:", abs(nc_diff) >= d_min_net)

import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Udacity Free Trial Screener — A/B Test Results',
             fontsize=14, fontweight='bold', y=1.02)
fig.patch.set_facecolor('#F8F8F8')

for ax in axes:
    ax.set_facecolor('#F8F8F8')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Chart 1 - Gross Conversion
bars1 = axes[0].bar(['Control', 'Experiment'],
                    [gross_conversion_ctrl, gross_conversion_exp],
                    color=['#4C72B0', '#DD8452'], width=0.5)
axes[0].set_title('Gross Conversion Rate\n(Enrollments / Clicks)', fontsize=11)
axes[0].set_ylabel('Conversion Rate')
axes[0].set_ylim(0, 0.30)
for bar in bars1:
    axes[0].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.005,
                 f'{bar.get_height():.4f}',
                 ha='center', fontsize=10, fontweight='bold')
axes[0].text(0.5, 0.05, '✓ Statistically & Practically Significant',
             transform=axes[0].transAxes, ha='center',
             fontsize=9, color='#3B6D11')

# Chart 2 - Net Conversion
bars2 = axes[1].bar(['Control', 'Experiment'],
                    [net_conversion_ctrl, net_conversion_exp],
                    color=['#4C72B0', '#DD8452'], width=0.5)
axes[1].set_title('Net Conversion Rate\n(Payments / Clicks)', fontsize=11)
axes[1].set_ylabel('Conversion Rate')
axes[1].set_ylim(0, 0.15)
for bar in bars2:
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.002,
                 f'{bar.get_height():.4f}',
                 ha='center', fontsize=10, fontweight='bold')
axes[1].text(0.5, 0.05, '✗ Not Statistically Significant',
             transform=axes[1].transAxes, ha='center',
             fontsize=9, color='#A32D2D')

from matplotlib.patches import Patch
legend = [Patch(color='#4C72B0', label='Control'),
          Patch(color='#DD8452', label='Experiment')]
fig.legend(handles=legend, loc='upper right', frameon=False)

plt.tight_layout()
plt.savefig('conversion_charts.png', dpi=150, bbox_inches='tight')
print("Chart saved")

print("=" * 60)
print("BUSINESS RECOMMENDATION")
print("=" * 60)
print("""
Udacity tested a screener asking users how many hours per week
they could commit before starting a free trial.

GROSS CONVERSION:
- Control: 21.89% | Experiment: 19.83% | Difference: -2.06%
- Statistically significant: YES
- Practically significant: YES
- The screener successfully reduced low-intent enrolments.

NET CONVERSION:
- Control: 11.76% | Experiment: 11.27% | Difference: -0.49%
- Statistically significant: NO
- Practically significant: NO
- We cannot confirm revenue was protected.

RECOMMENDATION: DO NOT LAUNCH
The screener reduced enrolments but failed to protect payments.
Since both metrics must pass for a launch decision, and net
conversion fails both tests, the risk to revenue is too high.
""")
print("=" * 60)