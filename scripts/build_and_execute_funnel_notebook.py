import json
import subprocess
import os

notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbformat_minor": 2,
            "pygments_lexer": "ipython3",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

def add_md(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

def add_code(code):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    })

# Title & Overview
add_md("""# 📊 Marketing Funnel & Conversion Performance Analysis (Future Interns - Task 3)
### By Future Interns Data Science & Analytics Program
**Author:** Guruveer Singh  
**Project:** Task 3 - Marketing Funnel & Conversion Performance Analysis  
**Scope:** 244,178 Inbound Visitors | 15,000 Captured Leads | 1,819 Won Customers ($10.87M Revenue)  
**Deliverable:** End-to-end analytics notebook, funnel stage drop-off audit, channel unit economics (CAC / ROAS), and growth strategy

> **📌 Data Provenance & Synthetic Data Disclosure:** As permitted by Future Interns project guidelines, this engagement evaluates a synthetically modeled B2B multi-channel growth and conversion dataset (`data/marketing_funnel_summary.csv` and `data/marketing_funnel_leads.csv`). The dataset is engineered to mirror realistic B2B SaaS conversion dynamics, stage drop-offs, sales cycle velocities, and unit economics. All metrics, rates, and sensitivity models are computed directly from these structured data tables.

---

## 🔍 Executive Problem Statement
In digital marketing, SaaS, and high-growth startups, driving top-of-funnel traffic is meaningless if leads fail to convert into paying customers. Optimizing funnel velocity and plugging stage-by-stage conversion leaks directly increases revenue and lowers Customer Acquisition Cost (CAC).

This analysis provides CMOs, VPs of Growth, and Sales Leadership with answers to four core questions:
1. **Where in the funnel are prospects dropping off?**
2. **Which acquisition channels deliver high-quality, high-velocity leads versus vanity traffic?**
3. **What are the true unit economics (CAC, Deal Size, ROAS) across channels?**
4. **What high-impact interventions will maximize pipeline throughput and conversion efficiency?**""")

# Cell 1: Imports
add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['figure.dpi'] = 120
print('Marketing analytics and visualization libraries loaded successfully!')""")

# Cell 2: Data Loading
add_md("""---
## 1. Data Ingestion & Funnel Schema Audit
We load both the granular lead-level dataset (15,000 accounts) and the multi-channel funnel summary dataset (244k visitors).""")

add_code("""# Load datasets
leads = pd.read_csv('data/marketing_funnel_leads.csv')
summary = pd.read_csv('data/marketing_funnel_summary.csv')

print(f"Granular Lead Records: {len(leads):,} leads across {leads['Channel'].nunique()} channels")
print(f"Top-of-Funnel Total Visitors: {summary['Visitors'].sum():,}")
summary[['Channel', 'Visitors', 'Leads', 'MQLs', 'SQLs', 'Customers', 'Marketing_Spend', 'Total_Revenue']]""")

# Cell 3: Full Funnel KPIs
add_md("""---
## 2. Full Funnel Conversion & Drop-off Quantification
We trace prospect volume through all five stages:
1. **Website Visitors** (TOFU)
2. **Captured Leads** (Content downloads, forms, signups)
3. **Marketing Qualified Leads - MQL** (Demographic and intent scoring)
4. **Sales Qualified Leads - SQL** (Product demo, discovery call)
5. **Closed Won Customers** (Paying subscription/contract)""")

add_code("""total_visitors = summary['Visitors'].sum()
total_leads = summary['Leads'].sum()
total_mqls = summary['MQLs'].sum()
total_sqls = summary['SQLs'].sum()
total_customers = summary['Customers'].sum()
total_spend = summary['Marketing_Spend'].sum()
total_revenue = summary['Total_Revenue'].sum()

funnel_df = pd.DataFrame({
    'Funnel Stage': ['1. Website Visitors', '2. Captured Leads', '3. Marketing Qualified (MQL)', '4. Sales Qualified (SQL)', '5. Closed Won Customers'],
    'Volume': [total_visitors, total_leads, total_mqls, total_sqls, total_customers],
    'Stage-to-Stage Conv %': [1.0, total_leads/total_visitors, total_mqls/total_leads, total_sqls/total_mqls, total_customers/total_sqls],
    'Stage Drop-off %': [0.0, 1 - (total_leads/total_visitors), 1 - (total_mqls/total_leads), 1 - (total_sqls/total_mqls), 1 - (total_customers/total_sqls)],
    'Cumulative Conv %': [1.0, total_leads/total_visitors, total_mqls/total_visitors, total_sqls/total_visitors, total_customers/total_visitors]
})

funnel_df['Stage-to-Stage Conv %'] = (funnel_df['Stage-to-Stage Conv %'] * 100).round(2).astype(str) + '%'
funnel_df['Stage Drop-off %'] = (funnel_df['Stage Drop-off %'] * 100).round(2).astype(str) + '%'
funnel_df['Cumulative Conv %'] = (funnel_df['Cumulative Conv %'] * 100).round(3).astype(str) + '%'

print("="*70)
print("             EXECUTIVE FUNNEL AUDIT & BENCHMARKS")
print("="*70)
print(f"Total Visitors:           {total_visitors:,}")
print(f"Traffic-to-Lead Rate:     {total_leads/total_visitors:.2%}")
print(f"Lead-to-Customer Rate:    {total_customers/total_leads:.2%}")
print(f"Overall End-to-End Conv:  {total_customers/total_visitors:.3%}")
print(f"Total Pipeline Revenue:   ${total_revenue:,.2f}")
print(f"Blended CAC:              ${total_spend/total_customers:,.2f}")
print(f"Blended ROAS:             {total_revenue/total_spend:.2f}x")
print("="*70)
funnel_df""")

# Cell 4: Funnel Plot
add_code("""# Visualize Funnel Progression
plt.figure(figsize=(10, 5))
stages_short = ['Visitors', 'Leads', 'MQL', 'SQL', 'Customers']
volumes = [total_visitors, total_leads, total_mqls, total_sqls, total_customers]
colors = ['#1E293B', '#334155', '#2563EB', '#0D9488', '#10B981']

bars = plt.bar(stages_short, volumes, color=colors, width=0.5, edgecolor='#0F172A')
plt.title('Funnel Stage Account Volume (Log Scale Progression)', fontsize=13, fontweight='bold', pad=12)
plt.ylabel('Accounts (Log Scale)', fontsize=11, fontweight='bold')
plt.yscale('log')

for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, y * 1.15, f"{int(y):,}", ha='center', fontsize=9.5, fontweight='bold')

plt.tight_layout()
plt.show()""")

# Cell 5: Channel Comparison
add_md("""---
## 3. Marketing Channel Performance: Traffic-to-Lead vs Lead-to-Customer
Not all channels are created equal. Channels with high visitor traffic may attract low-intent prospects, while targeted channels yield superior closing rates.""")

add_code("""channel_metrics = summary[['Channel', 'Visitors', 'Leads', 'Customers', 'Traffic_to_Lead_Rate', 'Lead_to_Customer_Rate', 'Overall_Conversion_Rate']].copy()
channel_metrics['Traffic_to_Lead_%'] = (channel_metrics['Traffic_to_Lead_Rate'] * 100).round(2).astype(str) + '%'
channel_metrics['Lead_to_Customer_%'] = (channel_metrics['Lead_to_Customer_Rate'] * 100).round(2).astype(str) + '%'
channel_metrics['Overall_Conv_%'] = (channel_metrics['Overall_Conversion_Rate'] * 100).round(3).astype(str) + '%'
channel_metrics.sort_values(by='Lead_to_Customer_Rate', ascending=False)""")

# Cell 6: Unit Economics
add_md("""---
## 4. Unit Economics: Customer Acquisition Cost (CAC) & ROAS
We evaluate capital efficiency by comparing marketing spend against closed revenue.""")

add_code("""unit_econ = summary[['Channel', 'Marketing_Spend', 'Total_Revenue', 'Customers', 'CAC', 'ROAS']].copy()
unit_econ['Avg_Deal_Value'] = (unit_econ['Total_Revenue'] / unit_econ['Customers']).round(2)
unit_econ = unit_econ.sort_values(by='ROAS', ascending=False)
unit_econ""")

# Cell 7: Plot Unit Economics
add_code("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# CAC Plot
bars1 = ax1.barh(unit_econ['Channel'], unit_econ['CAC'], color='#E11D48', edgecolor='#9F1239', height=0.55)
ax1.set_title('Customer Acquisition Cost (CAC) by Channel', fontweight='bold')
ax1.set_xlabel('CAC ($ / Customer)')
for bar in bars1:
    x = bar.get_width()
    ax1.text(x + 10, bar.get_y() + bar.get_height()/2, f"${x:,.0f}", va='center', fontweight='bold')

# ROAS Plot
bars2 = ax2.barh(unit_econ['Channel'], unit_econ['ROAS'], color='#10B981', edgecolor='#047857', height=0.55)
ax2.set_title('Return on Ad Spend (ROAS Multiple)', fontweight='bold')
ax2.set_xlabel('ROAS (x Return)')
for bar in bars2:
    x = bar.get_width()
    ax2.text(x + 1.5, bar.get_y() + bar.get_height()/2, f"{x:.1f}x", va='center', fontweight='bold')

plt.tight_layout()
plt.show()""")

# Cell 8: Mid-Funnel Leak Diagnostic
add_md("""---
## 5. Mid-Funnel Bottleneck Diagnostic: The MQL-to-SQL Leak
Across all channels, the single largest conversion drop-off occurs between **Marketing Qualified Leads (MQL)** and **Sales Qualified Leads (SQL)**, where **48.85% of leads drop off** (5,145 leads lost).""")

add_code("""mql_leak = summary[['Channel', 'MQLs', 'SQLs', 'MQL_to_SQL_Rate']].copy()
mql_leak['Drop_Off_Volume'] = mql_leak['MQLs'] - mql_leak['SQLs']
mql_leak['Drop_Off_Rate_%'] = ((1 - mql_leak['MQL_to_SQL_Rate']) * 100).round(2).astype(str) + '%'
mql_leak.sort_values(by='Drop_Off_Volume', ascending=False)""")

# Cell 9: Sales Velocity
add_md("""---
## 6. Lead Velocity & Sales Cycle Duration
How many days does it take for a prospect to move from initial lead capture to Closed Won Customer?""")

add_code("""won_leads = leads[leads['Is_Customer'] == 1]
velocity_summary = won_leads.groupby('Channel')['Sales_Cycle_Days'].agg(
    Won_Customers='count',
    Mean_Days='mean',
    Median_Days='median',
    Min_Days='min',
    Max_Days='max'
).round(1).sort_values(by='Mean_Days')
velocity_summary""")

# Cell 10: Financial Simulation
add_md("""---
## 7. Financial Sensitivity Model: Revenue Impact of Conversion Lifts
What is the incremental revenue impact if we improve MQL-to-SQL conversion by **+2%**, **+5%**, or **+10%** through automated qualification and faster SDR outreach?

> **Note on Methodology:** Incremental pipeline revenue is modeled based on the portfolio's observed average won deal value ($5,975.06). In high-growth SaaS environments, incremental revenue carries substantial valuation leverage; however, because this cross-sectional dataset models contract deal revenue rather than establishing a multi-year recurring SaaS subscription basis, projections reflect scenario-based sensitivity benchmarks rather than an audit-grade ARR valuation.""")

add_code("""current_sqls = total_sqls
current_customers = total_customers
avg_deal = total_revenue / total_customers

lift_scenarios = [0.02, 0.05, 0.08, 0.10]
sim_records = []

for lift in lift_scenarios:
    new_mql_to_sql = (total_sqls / total_mqls) + lift
    additional_sqls = int(total_mqls * lift)
    additional_customers = int(additional_sqls * (total_customers / total_sqls))
    additional_revenue = additional_customers * avg_deal
    sim_records.append({
        'MQL->SQL Rate Lift': f'+{lift:.0%}',
        'New SQLs Added': f'+{additional_sqls:,}',
        'Additional Customers Won': f'+{additional_customers:,}',
        'Incremental Revenue Generated': f'${additional_revenue:,.2f}'
    })

sim_df = pd.DataFrame(sim_records)
print("="*65)
print("      FUNNEL OPTIMIZATION REVENUE SENSITIVITY MODEL")
print("="*65)
print(sim_df.to_string(index=False))
print("="*65)""")

# Cell 11: Strategic Playbook
add_md("""---
## 8. Strategic Recommendations for Growth & Sales Leadership

### 🎯 1. Plug the Mid-Funnel Leak (-48.9% MQL-to-SQL Drop-off)
- **The Issue:** Over 5,145 marketing qualified leads stall before booking a sales demo.
- **Action:** Implement automated calendar booking links in nurture emails and establish a strict **<5-minute SDR outreach SLA** on high-intent inbound inquiries.

### 🚀 2. Scale Referral & Partner Acquisition (91.4x ROAS, 28.0% Conversion)
- **The Issue:** Referrals have the highest conversion (28.0%) and lowest CAC ($78.61), but account for only 7.8% of lead volume.
- **Action:** Launch a formal Partner Channel with a 20% first-year revenue share, co-hosted webinars, and agency certifications.

### 💰 3. Shift Budget from Generic PPC to Account-Based LinkedIn
- **The Issue:** Paid Search consumes 38.4% of spend ($218.7K of $569.1K) at an 8.46x ROAS, while LinkedIn Ads targets enterprise accounts yielding $8.5K average deal sizes.
- **Action:** Reallocate $50K from broad PPC search terms into LinkedIn ABM campaigns targeting 500+ employee tech and healthcare enterprises.

### ⚡ 4. Compress Enterprise Sales Cycles (52 Days to Close)
- **The Issue:** Enterprise deals take nearly twice as long to close as mid-market accounts (52 days vs. 28 days).
- **Action:** Provide pre-packaged security audit packets, automated ROI business cases, and executive sponsor discovery sessions by Day 14.""")

# Save file
with open('marketing_funnel_and_conversion_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print('Notebook structure written. Now executing natively via nbconvert...')
res = subprocess.run(['python', '-m', 'nbconvert', '--execute', '--inplace', 'marketing_funnel_and_conversion_analysis.ipynb'], capture_output=True, text=True)
print(res.stdout)
if res.returncode == 0:
    print('Notebook marketing_funnel_and_conversion_analysis.ipynb built and natively executed successfully!')
else:
    print('Error executing notebook:', res.stderr)
