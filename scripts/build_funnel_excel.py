import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

leads = pd.read_csv('data/marketing_funnel_leads.csv')
summary = pd.read_csv('data/marketing_funnel_summary.csv')

wb = openpyxl.Workbook()
wb.remove(wb.active)

# Aesthetics Palette
HEADER_BG = '0F172A'       # Slate 900
TABLE_HEADER = '1E293B'    # Slate 800
SUB_HEADER = '334155'      # Slate 700
CARD_BG = 'F8FAFC'         # Off white
BORDER_COLOR = 'CBD5E1'    # Slate 300

thin_border = Border(
    left=Side(style='thin', color=BORDER_COLOR),
    right=Side(style='thin', color=BORDER_COLOR),
    top=Side(style='thin', color=BORDER_COLOR),
    bottom=Side(style='thin', color=BORDER_COLOR)
)

# ==============================================================================
# TAB 1: EXECUTIVE DASHBOARD
# ==============================================================================
ws_dash = wb.create_sheet(title='Executive Dashboard')
ws_dash.views.sheetView[0].showGridLines = True

# Title Banner (Rows 1-3, Cols A-N)
ws_dash.merge_cells('A1:N2')
banner = ws_dash['A1']
banner.value = "📈 EXECUTIVE MARKETING FUNNEL & CONVERSION PERFORMANCE DASHBOARD"
banner.font = Font(name='Segoe UI', size=16, bold=True, color='FFFFFF')
banner.fill = PatternFill(start_color=HEADER_BG, end_color=HEADER_BG, fill_type='solid')
banner.alignment = Alignment(horizontal='center', vertical='center')

ws_dash.merge_cells('A3:N3')
sub_banner = ws_dash['A3']
sub_banner.value = "Multi-Channel Growth Analytics | Total Traffic: 244,178 Visitors | 15,000 Leads | 1,819 Won Customers | $10.87M Pipeline Revenue"
sub_banner.font = Font(name='Segoe UI', size=10, italic=True, color='E2E8F0')
sub_banner.fill = PatternFill(start_color='334155', end_color='334155', fill_type='solid')
sub_banner.alignment = Alignment(horizontal='center', vertical='center')

# KPI Cards Helper
def create_kpi_card(ws, start_col, start_row, end_col, end_row, title, value, subtext, val_color='1E293B'):
    ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=end_col)
    c_title = ws.cell(row=start_row, column=start_col)
    c_title.value = title
    c_title.font = Font(name='Segoe UI', size=9, bold=True, color='475569')
    c_title.alignment = Alignment(horizontal='center', vertical='center')
    c_title.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type='solid')
    
    ws.merge_cells(start_row=start_row+1, start_column=start_col, end_row=start_row+1, end_column=end_col)
    c_val = ws.cell(row=start_row+1, column=start_col)
    c_val.value = value
    c_val.font = Font(name='Segoe UI', size=18, bold=True, color=val_color)
    c_val.alignment = Alignment(horizontal='center', vertical='center')
    c_val.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type='solid')
    
    ws.merge_cells(start_row=start_row+2, start_column=start_col, end_row=start_row+2, end_column=end_col)
    c_sub = ws.cell(row=start_row+2, column=start_col)
    c_sub.value = subtext
    c_sub.font = Font(name='Segoe UI', size=8, italic=True, color='64748B')
    c_sub.alignment = Alignment(horizontal='center', vertical='center')
    c_sub.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type='solid')
    
    for r in range(start_row, end_row+1):
        for c in range(start_col, end_col+1):
            ws.cell(row=r, column=c).border = thin_border

create_kpi_card(ws_dash, 1, 5, 3, 7, "TOTAL WEBSITE TRAFFIC", "244,178", "100% Baseline Inbound Sessions", '0F172A')
create_kpi_card(ws_dash, 4, 5, 6, 7, "CAPTURED LEADS", "15,000", "Traffic-to-Lead: 6.14%", '2563EB')
create_kpi_card(ws_dash, 7, 5, 9, 7, "WON CUSTOMERS", "1,819", "Lead-to-Customer: 12.13%", '0D9488')
create_kpi_card(ws_dash, 10, 5, 11, 7, "PIPELINE REVENUE", "$10.87M", "Average Won Deal: $5,975", '10B981')
create_kpi_card(ws_dash, 12, 5, 14, 7, "BLENDED CAC & ROAS", "$313 / 19.1x", "$569.1K Spend | 19.1x Return", '6366F1')

# Table A: Funnel Stages & Drop-off (Cols A to E, Rows 9 to 16)
ws_dash.merge_cells('A9:E9')
sec_a = ws_dash['A9']
sec_a.value = "1. FULL FUNNEL STAGE PROGRESSION & DROP-OFF AUDIT"
sec_a.font = Font(name='Segoe UI', size=10, bold=True, color='FFFFFF')
sec_a.fill = PatternFill(start_color=TABLE_HEADER, end_color=TABLE_HEADER, fill_type='solid')

headers_a = ["Funnel Stage", "Accounts", "Stage Conv %", "Stage Drop %", "Cumulative Conv %"]
for col_idx, h in enumerate(headers_a, start=1):
    c = ws_dash.cell(row=10, column=col_idx, value=h)
    c.font = Font(name='Segoe UI', size=9, bold=True, color='FFFFFF')
    c.fill = PatternFill(start_color=SUB_HEADER, end_color=SUB_HEADER, fill_type='solid')
    c.alignment = Alignment(horizontal='center')
    c.border = thin_border

stage_rows = [
    ["1. Website Visitors", 244178, 1.0, 0.0, 1.0],
    ["2. Captured Leads", 15000, 0.0614, 0.9386, 0.0614],
    ["3. Marketing Qualified (MQL)", 10533, 0.7022, 0.2978, 0.0431],
    ["4. Sales Qualified (SQL)", 5388, 0.5115, 0.4885, 0.0221],
    ["5. Closed Won Customers", 1819, 0.3376, 0.6624, 0.0074]
]

for row_idx, r in enumerate(stage_rows, start=11):
    for col_idx, val in enumerate(r, start=1):
        c = ws_dash.cell(row=row_idx, column=col_idx, value=val)
        c.font = Font(name='Segoe UI', size=9)
        c.border = thin_border
        if col_idx == 1:
            c.alignment = Alignment(horizontal='left')
        elif col_idx == 2:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '#,##0'
        else:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '0.0%'
            if col_idx == 4 and val > 0.4 and row_idx > 11:
                c.font = Font(name='Segoe UI', size=9, bold=True, color='BE123C')

# Table B: Channel Performance & ROI (Cols G to N, Rows 9 to 17)
ws_dash.merge_cells('G9:N9')
sec_b = ws_dash['G9']
sec_b.value = "2. MARKETING CHANNEL CONVERSION & CAPITAL EFFICIENCY"
sec_b.font = Font(name='Segoe UI', size=10, bold=True, color='FFFFFF')
sec_b.fill = PatternFill(start_color=TABLE_HEADER, end_color=TABLE_HEADER, fill_type='solid')

headers_b = ["Acquisition Channel", "Visitors", "Leads", "Customers", "Spend ($)", "Revenue ($)", "CAC ($)", "ROAS"]
for col_idx, h in enumerate(headers_b, start=7):
    c = ws_dash.cell(row=10, column=col_idx, value=h)
    c.font = Font(name='Segoe UI', size=9, bold=True, color='FFFFFF')
    c.fill = PatternFill(start_color=SUB_HEADER, end_color=SUB_HEADER, fill_type='solid')
    c.alignment = Alignment(horizontal='center')
    c.border = thin_border

for r_idx, r in summary.iterrows():
    curr_row = 11 + r_idx
    row_vals = [
        r['Channel'], r['Visitors'], r['Leads'], r['Customers'],
        r['Marketing_Spend'], r['Total_Revenue'], r['CAC'], r['ROAS']
    ]
    for c_idx, val in enumerate(row_vals, start=7):
        c = ws_dash.cell(row=curr_row, column=c_idx, value=val)
        c.font = Font(name='Segoe UI', size=9)
        c.border = thin_border
        if c_idx == 7:
            c.alignment = Alignment(horizontal='left')
        elif c_idx in [8, 9, 10]:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '#,##0'
        elif c_idx in [11, 12, 13]:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '$#,##0'
        elif c_idx == 14:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '0.0"x"'
            if val > 40:
                c.font = Font(name='Segoe UI', size=9, bold=True, color='047857')

# Total row for Table B
ws_dash.cell(row=17, column=7, value="TOTAL / PORTFOLIO BLENDED").font = Font(name='Segoe UI', size=9, bold=True)
ws_dash.cell(row=17, column=8, value="=SUM(H11:H16)").number_format = '#,##0'
ws_dash.cell(row=17, column=9, value="=SUM(I11:I16)").number_format = '#,##0'
ws_dash.cell(row=17, column=10, value="=SUM(J11:J16)").number_format = '#,##0'
ws_dash.cell(row=17, column=11, value="=SUM(K11:K16)").number_format = '$#,##0'
ws_dash.cell(row=17, column=12, value="=SUM(L11:L16)").number_format = '$#,##0'
ws_dash.cell(row=17, column=13, value="=K17/J17").number_format = '$#,##0'
ws_dash.cell(row=17, column=14, value="=L17/K17").number_format = '0.0"x"'

for c_i in range(7, 15):
    cell = ws_dash.cell(row=17, column=c_i)
    cell.font = Font(name='Segoe UI', size=9, bold=True)
    cell.border = thin_border
    cell.fill = PatternFill(start_color='E2E8F0', end_color='E2E8F0', fill_type='solid')

# Add Native Excel Charts below tables
# Chart 1: Funnel Drop-off Bar Chart (A19:E33)
chart_funnel = BarChart()
chart_funnel.type = "bar"
chart_funnel.style = 10
chart_funnel.title = "Account Volume Across Funnel Stages"
chart_funnel.x_axis.title = "Volume"
chart_funnel.y_axis.title = "Stage"
chart_funnel.legend = None
chart_funnel.width = 16
chart_funnel.height = 9

data_ref1 = Reference(ws_dash, min_col=2, min_row=10, max_row=15)
cats_ref1 = Reference(ws_dash, min_col=1, min_row=11, max_row=15)
chart_funnel.add_data(data_ref1, titles_from_data=True)
chart_funnel.set_categories(cats_ref1)
ws_dash.add_chart(chart_funnel, "A19")

# Chart 2: Channel Revenue Bar Chart (G19:J33)
chart_rev = BarChart()
chart_rev.type = "col"
chart_rev.style = 11
chart_rev.title = "Pipeline Revenue by Channel ($)"
chart_rev.y_axis.title = "Revenue ($)"
chart_rev.y_axis.number_format = '$#,##0'
chart_rev.legend = None
chart_rev.width = 16
chart_rev.height = 9

data_ref2 = Reference(ws_dash, min_col=12, min_row=10, max_row=16)
cats_ref2 = Reference(ws_dash, min_col=7, min_row=11, max_row=16)
chart_rev.add_data(data_ref2, titles_from_data=True)
chart_rev.set_categories(cats_ref2)
ws_dash.add_chart(chart_rev, "G19")

# Chart 3: ROAS by Channel (K19:N33)
chart_roas = BarChart()
chart_roas.type = "col"
chart_roas.style = 13
chart_roas.title = "Capital Efficiency: ROAS by Channel"
chart_roas.y_axis.title = "ROAS (x Return)"
chart_roas.legend = None
chart_roas.width = 16
chart_roas.height = 9

data_ref3 = Reference(ws_dash, min_col=14, min_row=10, max_row=16)
cats_ref3 = Reference(ws_dash, min_col=7, min_row=11, max_row=16)
chart_roas.add_data(data_ref3, titles_from_data=True)
chart_roas.set_categories(cats_ref3)
ws_dash.add_chart(chart_roas, "K19")

# Strategic Action Plan (Rows 36 to 48)
ws_dash.merge_cells('A36:N36')
takeaway_title = ws_dash['A36']
takeaway_title.value = "🚀 EXECUTIVE CONVERSION OPTIMIZATION PLAYBOOK & STRATEGIC RECOMMENDATIONS"
takeaway_title.font = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
takeaway_title.fill = PatternFill(start_color=HEADER_BG, end_color=HEADER_BG, fill_type='solid')

takeaways = [
    ("1. Fix the Mid-Funnel Leak: Optimize MQL-to-SQL Qualification (-48.9% Drop-off):",
     "The sharpest drop-off in the pipeline occurs between MQL and SQL, where 5,145 qualified leads (48.9%) stall before a sales demo. Implement automated lead scoring, fast-response SDR routing (<5 min response SLA), and interactive self-serve product demos to capture intent immediately."),
    
    ("2. Scale Capital-Efficient Channels (Referral at 91.4x ROAS & SEO at 46.4x ROAS):",
     "Referral/Partner delivers an industry-leading 28.0% lead-to-customer conversion and $78.61 CAC, yet represents only 7.8% of lead volume. Formalize a structured co-marketing and partner referral tier with 20% revenue share to 3x partner lead volume."),
    
    ("3. Rebalance Paid Search to Eliminate Low-Intent Budget Drain ($535 CAC, 8.5x ROAS):",
     "Paid Search consumes 38.4% of total budget ($218.7K) but yields the lowest ROAS (8.5x) and an 8.98% lead-to-customer rate. Shift 25% of generic PPC budget into high-intent competitor displacement keywords and LinkedIn Enterprise retargeting."),
    
    ("4. Accelerate Enterprise Velocity (52-Day Sales Cycle on $8.5K Deals):",
     "Enterprise leads take 52 days to close compared to 28 days for mid-market. Deploy customized ROI calculators, security compliance packages, and executive sponsor outreach early in the evaluation stage to compress deal velocity by 10-14 days.")
]

curr_r = 37
for heading, body in takeaways:
    ws_dash.merge_cells(start_row=curr_r, start_column=1, end_row=curr_r, end_column=14)
    h_cell = ws_dash.cell(row=curr_r, column=1, value=heading)
    h_cell.font = Font(name='Segoe UI', size=9.5, bold=True, color='0F766E')
    h_cell.fill = PatternFill(start_color='F1F5F9', end_color='F1F5F9', fill_type='solid')
    curr_r += 1
    
    ws_dash.merge_cells(start_row=curr_r, start_column=1, end_row=curr_r+1, end_column=14)
    b_cell = ws_dash.cell(row=curr_r, column=1, value=body)
    b_cell.font = Font(name='Segoe UI', size=8.5, color='334155')
    b_cell.alignment = Alignment(wrap_text=True, vertical='center')
    curr_r += 2

# Adjust column widths
col_widths = {'A': 24, 'B': 13, 'C': 13, 'D': 13, 'E': 16, 'F': 3, 'G': 22, 'H': 12, 'I': 12, 'J': 12, 'K': 14, 'L': 15, 'M': 12, 'N': 10}
for col_letter, width in col_widths.items():
    ws_dash.column_dimensions[col_letter].width = width

# ==============================================================================
# TAB 2: FUNNEL STAGE MATRIX
# ==============================================================================
ws_matrix = wb.create_sheet(title='Funnel Stage Matrix')
ws_matrix.views.sheetView[0].showGridLines = True

ws_matrix.merge_cells('A1:J2')
m_banner = ws_matrix['A1']
m_banner.value = "📊 DETAILED FUNNEL STAGE CONVERSION MATRIX BY CHANNEL"
m_banner.font = Font(name='Segoe UI', size=14, bold=True, color='FFFFFF')
m_banner.fill = PatternFill(start_color=HEADER_BG, end_color=HEADER_BG, fill_type='solid')
m_banner.alignment = Alignment(horizontal='center', vertical='center')

matrix_headers = [
    "Acquisition Channel", "Visitors", "Leads", "MQLs", "SQLs", "Customers",
    "Visitor->Lead %", "Lead->MQL %", "MQL->SQL %", "SQL->Customer %"
]
for col_idx, h in enumerate(matrix_headers, start=1):
    c = ws_matrix.cell(row=4, column=col_idx, value=h)
    c.font = Font(name='Segoe UI', size=9.5, bold=True, color='FFFFFF')
    c.fill = PatternFill(start_color=TABLE_HEADER, end_color=TABLE_HEADER, fill_type='solid')
    c.alignment = Alignment(horizontal='center')
    c.border = thin_border

for r_idx, r in summary.iterrows():
    row_num = 5 + r_idx
    row_vals = [
        r['Channel'], r['Visitors'], r['Leads'], r['MQLs'], r['SQLs'], r['Customers'],
        r['Traffic_to_Lead_Rate'], r['Lead_to_MQL_Rate'], r['MQL_to_SQL_Rate'], r['SQL_to_Customer_Rate']
    ]
    for c_idx, val in enumerate(row_vals, start=1):
        c = ws_matrix.cell(row=row_num, column=c_idx, value=val)
        c.font = Font(name='Segoe UI', size=9)
        c.border = thin_border
        if c_idx == 1:
            c.alignment = Alignment(horizontal='left')
        elif c_idx in range(2, 7):
            c.alignment = Alignment(horizontal='right')
            c.number_format = '#,##0'
        else:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '0.0%'

for col in ws_matrix.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws_matrix.column_dimensions[col_letter].width = max(max_len + 3, 14)

# ==============================================================================
# TAB 3: CAMPAIGN ROI BREAKDOWN
# ==============================================================================
ws_camp = wb.create_sheet(title='Campaign ROI Breakdown')
ws_camp.views.sheetView[0].showGridLines = True

ws_camp.merge_cells('A1:I2')
c_banner = ws_camp['A1']
c_banner.value = "🎯 CAMPAIGN EFFICIENCY & REVENUE ATTRIBUTION"
c_banner.font = Font(name='Segoe UI', size=14, bold=True, color='FFFFFF')
c_banner.fill = PatternFill(start_color=HEADER_BG, end_color=HEADER_BG, fill_type='solid')
c_banner.alignment = Alignment(horizontal='center', vertical='center')

camp_headers = ["Channel", "Campaign Name", "Leads Generated", "Customers Won", "Conversion %", "Marketing Spend ($)", "Pipeline Revenue ($)", "CAC ($)", "ROAS Multiple"]
for col_idx, h in enumerate(camp_headers, start=1):
    c = ws_camp.cell(row=4, column=col_idx, value=h)
    c.font = Font(name='Segoe UI', size=9.5, bold=True, color='FFFFFF')
    c.fill = PatternFill(start_color=TABLE_HEADER, end_color=TABLE_HEADER, fill_type='solid')
    c.alignment = Alignment(horizontal='center')
    c.border = thin_border

camp_df = leads.groupby(['Channel', 'Campaign']).agg(
    Leads=('Lead_ID', 'count'),
    Customers=('Is_Customer', 'sum'),
    Spend=('Acquisition_Cost', 'sum'),
    Revenue=('Deal_Revenue', 'sum')
).reset_index()

camp_df['Conv_Rate'] = camp_df['Customers'] / camp_df['Leads']
camp_df['CAC'] = camp_df['Spend'] / camp_df['Customers']
camp_df['ROAS'] = camp_df['Revenue'] / camp_df['Spend']
camp_df = camp_df.sort_values(by='Revenue', ascending=False)

for r_idx, r in camp_df.iterrows():
    row_num = 5 + len(ws_camp['A']) - 4
    row_vals = [
        r['Channel'], r['Campaign'], r['Leads'], r['Customers'],
        r['Conv_Rate'], r['Spend'], r['Revenue'], r['CAC'], r['ROAS']
    ]
    for c_idx, val in enumerate(row_vals, start=1):
        c = ws_camp.cell(row=row_num, column=c_idx, value=val)
        c.font = Font(name='Segoe UI', size=9)
        c.border = thin_border
        if c_idx in [1, 2]:
            c.alignment = Alignment(horizontal='left')
        elif c_idx in [3, 4]:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '#,##0'
        elif c_idx == 5:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '0.0%'
        elif c_idx in [6, 7, 8]:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '$#,##0'
        elif c_idx == 9:
            c.alignment = Alignment(horizontal='right')
            c.number_format = '0.0"x"'

for col in ws_camp.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws_camp.column_dimensions[col_letter].width = max(max_len + 3, 14)

# ==============================================================================
# TAB 4: GRANULAR LEAD DATA (15,000 Records)
# ==============================================================================
ws_data = wb.create_sheet(title='Lead Journey Data')
ws_data.views.sheetView[0].showGridLines = True

lead_cols = [
    'Lead_ID', 'Channel', 'Campaign', 'Industry', 'Company_Size', 'Device',
    'Reached_MQL', 'Reached_SQL', 'Is_Customer', 'Final_Funnel_Stage',
    'Sales_Cycle_Days', 'Acquisition_Cost', 'Deal_Revenue'
]

# Write headers
for col_idx, col_name in enumerate(lead_cols, start=1):
    c = ws_data.cell(row=1, column=col_idx, value=col_name)
    c.font = Font(name='Segoe UI', size=9, bold=True, color='FFFFFF')
    c.fill = PatternFill(start_color=TABLE_HEADER, end_color=TABLE_HEADER, fill_type='solid')
    c.alignment = Alignment(horizontal='center')

# Write first 5,000 rows to keep workbook responsive and fast
for r_idx, row in leads[lead_cols].iloc[:5000].iterrows():
    row_num = r_idx + 2
    for c_idx, val in enumerate(row, start=1):
        c = ws_data.cell(row=row_num, column=c_idx, value=val)
        c.font = Font(name='Segoe UI', size=8.5)
        if lead_cols[c_idx-1] in ['Acquisition_Cost', 'Deal_Revenue']:
            c.number_format = '$#,##0.00'
            c.alignment = Alignment(horizontal='right')
        elif lead_cols[c_idx-1] in ['Reached_MQL', 'Reached_SQL', 'Is_Customer', 'Sales_Cycle_Days']:
            c.number_format = '#,##0'
            c.alignment = Alignment(horizontal='right')
        elif lead_cols[c_idx-1] == 'Final_Funnel_Stage':
            c.alignment = Alignment(horizontal='center')
            if 'Won' in str(val):
                c.font = Font(name='Segoe UI', size=8.5, bold=True, color='047857')
            elif 'SQL' in str(val):
                c.font = Font(name='Segoe UI', size=8.5, color='0D9488')
            elif 'MQL' in str(val):
                c.font = Font(name='Segoe UI', size=8.5, color='2563EB')
        else:
            c.alignment = Alignment(horizontal='left')

ws_data.auto_filter.ref = f"A1:{get_column_letter(len(lead_cols))}5001"
for col in ws_data.columns:
    col_letter = get_column_letter(col[0].column)
    ws_data.column_dimensions[col_letter].width = 15

wb.save('Marketing_Funnel_Dashboard.xlsx')
print('Marketing_Funnel_Dashboard.xlsx created successfully!')
