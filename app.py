You are an expert CMMS developer and Streamlit dashboard engineer.

Build a COMPLETE Streamlit Maintenance Breakdown Dashboard system like NADEC CUTE.

I want ONE single file code: app.py

This dashboard must work for 18 production machines (M1 to M18).

====================================================
MAIN GOAL
====================================================

Create a real-time maintenance KPI system where:

✅ Operators can enter breakdown jobs daily  
✅ Management can track machine status live  
✅ Breakdown types are color-coded  
✅ Clicking machine shows breakdown details  
✅ Dashboard updates automatically  
✅ Export to Excel/CSV/PDF is available  

====================================================
DATA STORAGE
====================================================

Use permanent local storage:

- breakdown_log.csv

The file must auto-create if missing.

====================================================
DATA STRUCTURE
====================================================

Each breakdown record must contain:

- Date  
- Machine No (M1–M18)
- Shift (Day/Night)
- Machine Classification (Filler, Packer, Labeler etc.)
- Job Type (Breakdown B/D or Corrective)
- Breakdown Category (Mechanical, Electrical, Automation)
- Reported Problem
- Description of Work
- Start Time
- End Time
- Time Consumed (auto-calculated)
- Technician / Performed By
- Status (OPEN or CLOSED)

====================================================
REQUIRED DASHBOARD UI STYLE
====================================================

Make UI similar to NADEC CUTE screen:

Top Header Title:

"KUTE – Kazim Utilization & Team Efficiency Dashboard"

Navigation Tabs:

1. Home
2. Breakdown Reports
3. Machine History
4. Team Contribution
5. Data Entry

====================================================
1. HOME TAB – LIVE MACHINE STATUS BARS
====================================================

Show 18 horizontal machine bars (M1–M18):

- Y-axis = Machine name
- X-axis = Total downtime minutes

Bars must be stacked and color-coded:

Red = Mechanical
Blue = Electrical
Green = Automation

Each bar represents current downtime MTD.

Clicking a machine bar must open breakdown detail table
for that machine.

====================================================
2. DATA ENTRY BUTTON (HIDDEN FORM)
====================================================

Show only a button:

➕ Add Breakdown Entry

When clicked → open operator entry form.

After saving → dashboard updates immediately.

====================================================
3. CSV / EXCEL UPLOAD OPTION
====================================================

Add upload section:

📌 Upload Daily Breakdown Excel File

If uploaded, system should automatically:

- detect column names even if spelling differs
- clean the data
- calculate Time Consumed
- append records into breakdown_log.csv

====================================================
4. DAILY LOG TABLE (Editable)
====================================================

Show full breakdown log table:

- Editable in Streamlit
- Each row has Delete button
- Each row has Edit button

====================================================
5. KPI CARDS
====================================================

Show KPI summary:

- Total Downtime Hours
- Total Breakdown Events
- Worst Machine
- Worst Month
- Top Technician Contributor
- Pending Jobs Count

====================================================
6. FILTERS
====================================================

Add filters:

- Date Range
- Machine Selection
- Breakdown Category
- Technician Name
- Job Type

====================================================
7. ANALYTICS CHARTS
====================================================

Include charts:

- Machine-wise downtime ranking (M1–M18)
- Month-wise downtime trend
- Technician workload ranking
- Breakdown category pie chart
- Hour-of-day breakdown heatmap (0–23)

====================================================
8. AUTO REFRESH
====================================================

Dashboard should auto-refresh every 2 minutes
with countdown display.

====================================================
9. EXPORT OPTIONS
====================================================

Provide buttons:

- Download CSV
- Download Excel
- Download PDF Report

====================================================
OUTPUT RULES
====================================================

- Give FULL working Streamlit app.py code
- Must run directly:

streamlit run app.py

- Mobile-friendly layout
- Professional NADEC style UI
- No HTML pasted incorrectly into Python
- Use Plotly for interactive charts
- Use st.dialog or st.expander for breakdown detail popup

Now generate the complete app.py code.
