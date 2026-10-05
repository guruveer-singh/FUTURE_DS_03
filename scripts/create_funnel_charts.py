import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

out_dir = 'visualizations/funnel'
os.makedirs(out_dir, exist_ok=True)

leads = pd.read_csv('data/marketing_funnel_leads.csv')
summary = pd.read_csv('data/marketing_funnel_summary.csv')

# -------------------------------------------------------------
# Chart 1: Marketing Funnel Overview & Stage Drop-offs
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6.5), facecolor='white')

stages = ['1. Website Visitors', '2. Captured Leads', '3. Marketing Qualified (MQL)', '4. Sales Qualified (SQL)', '5. Closed Won Customers']
counts = [
    summary['Visitors'].sum(),
    summary['Leads'].sum(),
    summary['MQLs'].sum(),
    summary['SQLs'].sum(),
    summary['Customers'].sum()
]

colors_funnel = ['#1E293B', '#334155', '#2563EB', '#0D9488', '#10B981']
y_pos = np.arange(len(stages))[::-1]

bars = ax.barh(y_pos, counts, color=colors_funnel, height=0.55, edgecolor='#0F172A')
ax.set_yticks(y_pos)
ax.set_yticklabels(stages, fontsize=11, fontweight='bold', color='#1E293B')
ax.set_xlabel('Volume of Accounts / Users', fontsize=11, fontweight='bold', color='#334155')
ax.set_xlim(0, max(counts) * 1.25)

# Add stage-to-stage conversion and drop-off text
for i, (bar, cnt) in enumerate(zip(bars[::-1], counts)):
    x_val = bar.get_width()
    y_val = bar.get_y() + bar.get_height() / 2.0
    if i == 0:
        label = f"{cnt:,}  (100% Baseline Traffic)"
    else:
        prev = counts[i-1]
        conv = (cnt / prev) * 100
        drop = 100 - conv
        label = f"{cnt:,}  ({conv:.1f}% Stage Conv | -{drop:.1f}% Drop-off)"
    ax.text(x_val + 3000, y_val, label, ha='left', va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

ax.set_title('END-TO-END MARKETING & SALES FUNNEL CONVERSION BENCHMARKS\nTotal Traffic: 244.2K Visitors | 15.0K Leads | 1,819 Won Customers (0.74% Overall Conversion)', fontsize=12, fontweight='bold', color='#0F172A', pad=15)
ax.grid(axis='x', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig(f'{out_dir}/01_marketing_funnel_overview.png', dpi=300, bbox_inches='tight')
plt.close()
print('Chart 1 complete.')

# -------------------------------------------------------------
# Chart 2: Channel Conversion Rates (Traffic-to-Lead vs Lead-to-Customer)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='white')
sum_sorted = summary.sort_values(by='Lead_to_Customer_Rate', ascending=True)

y_indices = np.arange(len(sum_sorted))

# Panel 1: Traffic to Lead Rate
bars1 = ax1.barh(y_indices, sum_sorted['Traffic_to_Lead_Rate'] * 100, color='#2563EB', height=0.55, edgecolor='#1E3A8A')
ax1.set_yticks(y_indices)
ax1.set_yticklabels(sum_sorted['Channel'], fontsize=10, fontweight='bold', color='#1E293B')
ax1.set_xlabel('Traffic-to-Lead Rate (%)', fontsize=11, fontweight='bold', color='#334155')
ax1.set_xlim(0, 14)
for bar in bars1:
    xval = bar.get_width()
    ax1.text(xval + 0.3, bar.get_y() + bar.get_height()/2.0, f"{xval:.1f}%", ha='left', va='center', fontsize=9.5, fontweight='bold')
ax1.set_title('Top-of-Funnel: Traffic-to-Lead Conversion Rate', fontsize=11, fontweight='bold', color='#1E293B')
ax1.grid(axis='x', linestyle=':', alpha=0.6)

# Panel 2: Lead to Customer Rate
bars2 = ax2.barh(y_indices, sum_sorted['Lead_to_Customer_Rate'] * 100, color='#0D9488', height=0.55, edgecolor='#115E59')
ax2.set_yticks(y_indices)
ax2.set_yticklabels([]) # Hide redundant labels
ax2.set_xlabel('Lead-to-Customer Rate (%)', fontsize=11, fontweight='bold', color='#334155')
ax2.set_xlim(0, 35)
for bar in bars2:
    xval = bar.get_width()
    ax2.text(xval + 0.6, bar.get_y() + bar.get_height()/2.0, f"{xval:.1f}%", ha='left', va='center', fontsize=9.5, fontweight='bold')
ax2.set_title('Bottom-of-Funnel: Lead-to-Customer Conversion Rate', fontsize=11, fontweight='bold', color='#1E293B')
ax2.grid(axis='x', linestyle=':', alpha=0.6)

plt.suptitle('CHANNEL CONVERSION DISPARITY: REFERRAL & LINKEDIN DRIVE PREMIUM BOTTOM-FUNNEL EFFICIENCY', fontsize=13, fontweight='bold', color='#0F172A', y=1.02)
plt.tight_layout()
plt.savefig(f'{out_dir}/02_channel_conversion_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print('Chart 2 complete.')

# -------------------------------------------------------------
# Chart 3: CAC vs Average Deal Size & ROAS
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='white')

deal_sizes = leads[leads['Is_Customer'] == 1].groupby('Channel')['Deal_Revenue'].mean().reindex(summary['Channel'])

x = np.arange(len(summary))
width = 0.35

bars_cac = ax1.bar(x - width/2, summary['CAC'], width, label='CAC ($ / Customer)', color='#E11D48', edgecolor='#9F1239')
bars_deal = ax1.bar(x + width/2, deal_sizes, width, label='Avg Deal Size ($)', color='#10B981', edgecolor='#047857')

ax1.set_xticks(x)
ax1.set_xticklabels(summary['Channel'], rotation=25, ha='right', fontsize=9, fontweight='bold')
ax1.set_ylabel('Cost / Revenue ($)', fontsize=11, fontweight='bold')
ax1.set_title('Customer Acquisition Cost (CAC) vs. Average Deal Value', fontsize=11, fontweight='bold', color='#1E293B')
ax1.legend(loc='upper left', frameon=True)
ax1.grid(axis='y', linestyle=':', alpha=0.6)

for bar in bars_deal:
    y = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, y + 100, f"${y:,.0f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

# ROAS Bar Chart
bars_roas = ax2.bar(summary['Channel'], summary['ROAS'], color='#6366F1', width=0.5, edgecolor='#4338CA')
ax2.set_xticklabels(summary['Channel'], rotation=25, ha='right', fontsize=9, fontweight='bold')
ax2.set_ylabel('ROAS (x Return)', fontsize=11, fontweight='bold')
ax2.set_title('Return on Ad Spend (ROAS) by Marketing Channel', fontsize=11, fontweight='bold', color='#1E293B')
ax2.set_ylim(0, 110)
ax2.grid(axis='y', linestyle=':', alpha=0.6)

for bar in bars_roas:
    y = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, y + 2, f"{y:.1f}x", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

plt.suptitle('UNIT ECONOMICS & CAPITAL EFFICIENCY: REFERRAL (91.4x) AND SEO (46.4x) DELIVER HIGHEST ROI', fontsize=13, fontweight='bold', color='#0F172A', y=1.02)
plt.tight_layout()
plt.savefig(f'{out_dir}/03_cac_vs_ltv_roas_by_channel.png', dpi=300, bbox_inches='tight')
plt.close()
print('Chart 3 complete.')

# -------------------------------------------------------------
# Chart 4: Funnel Stage Drop-off Waterfall
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')

waterfall_labels = ['Total Visitors', 'Drop-off (TOFU)', 'Captured Leads', 'Drop-off (Lead->MQL)', 'Reached MQL', 'Drop-off (MQL->SQL)', 'Reached SQL', 'Drop-off (Closing)', 'Won Customers']
waterfall_values = [
    244178,
    -(244178 - 15000),
    15000,
    -(15000 - 10533),
    10533,
    -(10533 - 5388),
    5388,
    -(5388 - 1819),
    1819
]

colors_wf = ['#1E293B', '#F43F5E', '#2563EB', '#F43F5E', '#0EA5E9', '#F43F5E', '#0D9488', '#F43F5E', '#10B981']

bars_wf = ax.bar(range(len(waterfall_labels)), [abs(v) for v in waterfall_values], color=colors_wf, width=0.55, edgecolor='#0F172A')
ax.set_xticks(range(len(waterfall_labels)))
ax.set_xticklabels(waterfall_labels, rotation=30, ha='right', fontsize=9, fontweight='bold')
ax.set_ylabel('Account Volume', fontsize=11, fontweight='bold')
ax.set_title('FUNNEL DROP-OFF WATERFALL: ISOLATING THE 5,145 ACCOUNT LEAK AT THE MQL-TO-SQL STAGE', fontsize=12, fontweight='bold', color='#0F172A', pad=15)
ax.grid(axis='y', linestyle=':', alpha=0.6)

for bar, val in zip(bars_wf, waterfall_values):
    y = bar.get_height()
    prefix = "-" if val < 0 else ""
    ax.text(bar.get_x() + bar.get_width()/2, y + 2500, f"{prefix}{abs(val):,}", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{out_dir}/04_funnel_stage_dropoff_waterfall.png', dpi=300, bbox_inches='tight')
plt.close()
print('Chart 4 complete.')

# -------------------------------------------------------------
# Chart 5: Sales Cycle Velocity (Days to Convert)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='white')

cust_leads = leads[leads['Is_Customer'] == 1]
ch_velocity = cust_leads.groupby('Channel')['Sales_Cycle_Days'].mean().sort_values(ascending=True)

bars_v1 = ax1.barh(ch_velocity.index, ch_velocity.values, color='#0D9488', height=0.55, edgecolor='#134E4A')
ax1.set_xlabel('Average Sales Cycle (Days)', fontsize=11, fontweight='bold')
ax1.set_title('Sales Velocity by Acquisition Channel (Won Customers)', fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_xlim(0, 60)
ax1.grid(axis='x', linestyle=':', alpha=0.6)
for bar in bars_v1:
    xval = bar.get_width()
    ax1.text(xval + 1, bar.get_y() + bar.get_height()/2, f"{xval:.1f} Days", ha='left', va='center', fontsize=9.5, fontweight='bold')

# Velocity by Company Size
size_velocity = cust_leads.groupby('Company_Size')['Sales_Cycle_Days'].mean().reindex(['1-50 (Startup)', '51-200 (Mid-Market)', '201-1000 (Commercial)', '1000+ (Enterprise)'])
bars_v2 = ax2.bar(size_velocity.index, size_velocity.values, color=['#10B981', '#0EA5E9', '#F59E0B', '#E11D48'], width=0.5, edgecolor='#334155')
ax2.set_ylabel('Average Sales Cycle (Days)', fontsize=11, fontweight='bold')
ax2.set_title('Sales Velocity by Target Customer Segment', fontsize=11, fontweight='bold', color='#1E293B')
ax2.set_xticklabels(['Startup', 'Mid-Market', 'Commercial', 'Enterprise'], fontsize=10, fontweight='bold')
ax2.set_ylim(0, 65)
ax2.grid(axis='y', linestyle=':', alpha=0.6)
for bar in bars_v2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 1.2, f"{yval:.1f} Days", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

plt.suptitle('LEAD VELOCITY ANALYSIS: REFERRAL CLOSES IN 35 DAYS WHILE ENTERPRISE REQUIRES 52 DAYS', fontsize=13, fontweight='bold', color='#0F172A', y=1.02)
plt.tight_layout()
plt.savefig(f'{out_dir}/05_sales_cycle_velocity_by_channel.png', dpi=300, bbox_inches='tight')
plt.close()
print('Chart 5 complete.')

# -------------------------------------------------------------
# Chart 6: Campaign Performance Matrix (Spend vs Revenue vs ROAS)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6.5), facecolor='white')

camp_stats = leads.groupby('Campaign').agg(
    Leads=('Lead_ID', 'count'),
    Customers=('Is_Customer', 'sum'),
    Revenue=('Deal_Revenue', 'sum'),
    Spend=('Acquisition_Cost', 'sum')
).reset_index()

camp_stats['Conv_Rate'] = (camp_stats['Customers'] / camp_stats['Leads']) * 100
camp_stats['ROAS'] = camp_stats['Revenue'] / camp_stats['Spend']

scatter = ax.scatter(camp_stats['Spend'] / 1000, camp_stats['Conv_Rate'], s=camp_stats['Revenue'] / 1500, 
                     c=camp_stats['ROAS'], cmap='viridis', alpha=0.75, edgecolors='black', linewidth=1.5)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Return on Ad Spend (ROAS x)', fontsize=10, fontweight='bold')

ax.set_xlabel('Marketing Spend ($K)', fontsize=11, fontweight='bold')
ax.set_ylabel('Lead-to-Customer Conversion Rate (%)', fontsize=11, fontweight='bold')
ax.set_title('CAMPAIGN EFFICIENCY MATRIX (Bubble Size = Total Revenue Generated)', fontsize=12, fontweight='bold', color='#0F172A', pad=15)
ax.grid(True, linestyle=':', alpha=0.6)

# Annotate top campaigns
for _, r in camp_stats.iterrows():
    if r['Revenue'] > 1000000 or r['Conv_Rate'] > 25:
        ax.annotate(r['Campaign'].split(' - ')[-1], (r['Spend']/1000 + 1.5, r['Conv_Rate'] + 0.5), fontsize=8.5, fontweight='bold', color='#0F172A')

plt.tight_layout()
plt.savefig(f'{out_dir}/06_campaign_performance_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print('Chart 6 complete.')

# -------------------------------------------------------------
# Chart 7: Executive Funnel Dashboard Summary
# -------------------------------------------------------------
fig, ((p1, p2), (p3, p4)) = plt.subplots(2, 2, figsize=(16, 12), facecolor='white')

# Panel 1: Funnel Volume
p1.bar(['Visitors', 'Leads', 'MQL', 'SQL', 'Won'], [244.2, 15.0, 10.5, 5.4, 1.8], color=['#1E293B', '#334155', '#2563EB', '#0D9488', '#10B981'], width=0.5)
p1.set_title('1. Full Funnel Volume Progression (Thousands)', fontsize=11, fontweight='bold')
p1.set_ylabel('Accounts (K)')
p1.set_ylim(0, 270)
for i, v in enumerate([244.2, 15.0, 10.5, 5.4, 1.8]):
    p1.text(i, v + 5, f"{v}K", ha='center', fontweight='bold')
p1.grid(axis='y', linestyle=':', alpha=0.5)

# Panel 2: Channel Revenue
p2.barh(summary['Channel'], summary['Total_Revenue'] / 1e6, color='#2563EB', height=0.5)
p2.set_title('2. Pipeline Revenue by Channel ($ Millions)', fontsize=11, fontweight='bold')
p2.set_xlabel('Revenue ($M)')
p2.set_xlim(0, 4.2)
for i, v in enumerate(summary['Total_Revenue'] / 1e6):
    p2.text(v + 0.08, i, f"${v:.2f}M", ha='left', va='center', fontweight='bold')
p2.grid(axis='x', linestyle=':', alpha=0.5)

# Panel 3: Lead-to-Customer Conversion Rate
p3.bar(summary['Channel'], summary['Lead_to_Customer_Rate'] * 100, color='#0D9488', width=0.5)
p3.set_title('3. Lead-to-Customer Conversion Rate (%)', fontsize=11, fontweight='bold')
p3.set_ylabel('Conversion Rate (%)')
p3.set_xticklabels(summary['Channel'], rotation=25, ha='right', fontsize=8.5, fontweight='bold')
p3.set_ylim(0, 35)
for i, v in enumerate(summary['Lead_to_Customer_Rate'] * 100):
    p3.text(i, v + 1, f"{v:.1f}%", ha='center', fontweight='bold')
p3.grid(axis='y', linestyle=':', alpha=0.5)

# Panel 4: ROAS by Channel
p4.bar(summary['Channel'], summary['ROAS'], color=['#4338CA', '#10B981', '#0EA5E9', '#F59E0B', '#8B5CF6', '#64748B'], width=0.5)
p4.set_title('4. Capital Efficiency (ROAS Multiple)', fontsize=11, fontweight='bold')
p4.set_ylabel('ROAS (x Return)')
p4.set_xticklabels(summary['Channel'], rotation=25, ha='right', fontsize=8.5, fontweight='bold')
p4.set_ylim(0, 110)
for i, v in enumerate(summary['ROAS']):
    p4.text(i, v + 2.5, f"{v:.1f}x", ha='center', fontweight='bold')
p4.grid(axis='y', linestyle=':', alpha=0.5)

plt.suptitle('EXECUTIVE MARKETING FUNNEL & CONVERSION PERFORMANCE DASHBOARD', fontsize=15, fontweight='bold', color='#0F172A', y=0.99)
plt.tight_layout()
plt.savefig(f'{out_dir}/07_executive_funnel_dashboard_summary.png', dpi=300, bbox_inches='tight')
plt.close()
print('Chart 7 complete. All 7 funnel charts successfully generated!')
