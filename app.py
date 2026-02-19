import streamlit as st
import pandas as pd
import altair as alt
import re
from bs4 import BeautifulSoup

# Original HTML content
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NADEC Breakdown Maintenance Dashboard 2025</title>

  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <!-- Google Font -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

  <style>
    body {
      margin: 0;
      font-family: "Poppins", sans-serif;
      background: linear-gradient(to right, #eef2f3, #ffffff);
    }

    header {
      background: #003366;
      color: white;
      padding: 25px;
      text-align: center;
      font-size: 24px;
      font-weight: 700;
    }

    .subhead {
      font-size: 14px;
      font-weight: 300;
      margin-top: 6px;
      color: #d9e6ff;
    }

    .container {
      max-width: 1600px;
      margin: auto;
      padding: 20px;
    }

    /* KPI Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 15px;
      margin-bottom: 25px;
    }

    .kpi-card {
      background: white;
      padding: 18px;
      border-radius: 15px;
      box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
      text-align: center;
    }

    .kpi-card h2 {
      font-size: 15px;
      margin: 0;
      color: #003366;
    }

    .kpi-card p {
      font-size: 28px;
      font-weight: bold;
      margin: 10px 0 0;
      color: #222;
    }

    /* Charts Grid */
    .chart-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
      gap: 20px;
    }

    .chart-box {
      background: white;
      padding: 15px;
      border-radius: 15px;
      box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
    }

    h3 {
      text-align: center;
      color: #003366;
      margin-top: 45px;
    }

    /* Compact Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
      font-size: 12px;
      background: white;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0px 4px 10px rgba(0,0,0,0.10);
    }

    th {
      background: #003366;
      color: white;
      padding: 8px;
      font-size: 12px;
    }

    td {
      padding: 6px;
      border-bottom: 1px solid #ddd;
      text-align: center;
    }

    tr:hover {
      background: #f2f6ff;
    }

    /* Table Section Box */
    .section-box {
      background: white;
      padding: 20px;
      margin-top: 30px;
      border-radius: 16px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.10);
    }

    footer {
      text-align: center;
      padding: 15px;
      margin-top: 30px;
      font-size: 14px;
      color: gray;
    }

    /* Mobile Friendly */
    @media(max-width:650px){
      header {font-size:18px;}
      .chart-grid {grid-template-columns:1fr;}
      table {font-size:11px;}
    }
  </style>
</head>

<body>

<header>
  NADEC Drinkable Maintenance Performance Report of 2025
  <div class="subhead">
    Breakdown Downtime | Machine Failures | Technician Workload Contribution Dashboard
  </div>
</header>

<div class="container">

  <!-- KPI Cards -->
  <div class="kpi-grid">
    <div class="kpi-card"><h2>Total Downtime Hours</h2><p>3466</p></div>
    <div class="kpi-card"><h2>Total Breakdown Events</h2><p>8903</p></div>
    <div class="kpi-card"><h2>Worst Downtime Month</h2><p>July</p></div>
    <div class="kpi-card"><h2>Highest Breakdown Machine</h2><p>M15</p></div>
    <div class="kpi-card"><h2>Top Technician Contributor</h2><p>Dante</p></div>
  </div>

  <!-- Charts -->
  <div class="chart-grid">

    <div class="chart-box">
      <h3>Monthly Downtime Hours</h3>
      <canvas id="monthlyChart"></canvas>
    </div>

    <div class="chart-box">
      <h3>Top Machines Breakdown Count</h3>
      <canvas id="machineChart"></canvas>
    </div>

    <div class="chart-box">
      <h3>Technician Contribution Share</h3>
      <canvas id="techChart"></canvas>
    </div>

    <div class="chart-box">
      <h3>Top Technician Workload Ranking</h3>
      <canvas id="techBar"></canvas>
    </div>

  </div>

  <!-- Technician Full Table -->
  <div class="section-box">
    <h3>👷 Full Technician Monthly Breakdown Workload (Jan–Dec)</h3>

    <table>
      <tr>
        <th>Technician</th>
        <th>Jan</th><th>Feb</th><th>Mar</th><th>Apr</th>
        <th>May</th><th>Jun</th><th>Jul</th><th>Aug</th>
        <th>Sep</th><th>Oct</th><th>Nov</th><th>Dec</th>
        <th>Total</th>
      </tr>

      <tr><td>Ali</td><td>50</td><td>54</td><td>65</td><td>65</td><td>70</td><td>68</td><td>78</td><td>90</td><td></td><td>43</td><td>88</td><td>82</td><td>753</td></tr>
      <tr><td>Amgad</td><td>117</td><td>97</td><td>102</td><td></td><td>105</td><td>126</td><td>110</td><td>121</td><td>84</td><td>99</td><td>101</td><td>50</td><td>1112</td></tr>
      <tr><td>Dante</td><td>129</td><td>110</td><td>160</td><td>40</td><td>86</td><td>105</td><td>120</td><td>142</td><td>134</td><td>189</td><td>163</td><td>163</td><td>1541</td></tr>
      <tr><td>Sameer</td><td>216</td><td>98</td><td>91</td><td>129</td><td>81</td><td></td><td>163</td><td>166</td><td>145</td><td>176</td><td>140</td><td>74</td><td>1479</td></tr>
      <tr><td>Gilbert</td><td>132</td><td>128</td><td>115</td><td>113</td><td>152</td><td>128</td><td>125</td><td>126</td><td>118</td><td>147</td><td>111</td><td></td><td>1395</td></tr>
      <tr><td>Lito</td><td>143</td><td>130</td><td>140</td><td>125</td><td>134</td><td>83</td><td>101</td><td>139</td><td>126</td><td>72</td><td>11</td><td>32</td><td>1236</td></tr>
      <tr><td>Husam</td><td>88</td><td>92</td><td>72</td><td></td><td>100</td><td>127</td><td>126</td><td>145</td><td>130</td><td>107</td><td>98</td><td>129</td><td>1214</td></tr>n      <tr><td>Nashwan</td><td>71</td><td>85</td><td>100</td><td>105</td><td>71</td><td></td><td>132</td><td>147</td><td>161</td><td>112</td><td>108</td><td>108</td><td>1200</td></tr>
      <tr><td>Moneef</td><td>61</td><td>99</td><td>110</td><td>143</td><td>111</td><td>97</td><td>107</td><td>138</td><td>6</td><td>80</td><td>102</td><td>57</td><td>1111</td></tr>
      <tr><td>Yousef</td><td>16</td><td>11</td><td>14</td><td>20</td><td>53</td><td>66</td><td>74</td><td>47</td><td>46</td><td>30</td><td>33</td><td>14</td><td>424</td></tr>

    </table>
  </div>

  <!-- Month Downtime Table -->
  <div class="section-box">
    <h3>📅 Month-wise Breakdown Downtime Summary</h3>

    <table>
      <tr><th>Month</th><th>Total Downtime (HH:MM:SS)</th></tr>
      <tr><td>Jan</td><td>285:51:00</td></tr>
      <tr><td>Feb</td><td>241:58:00</td></tr>
      <tr><td>Mar</td><td>312:16:00</td></tr>
      <tr><td>Apr</td><td>222:32:00</td></tr>
      <tr><td>May</td><td>304:34:00</td></tr>
      <tr><td>Jun</td><td>260:13:00</td></tr>
      <tr style="font-weight:bold;background:#fff3cd;"><td>Jul</td><td>446:58:00 (Highest)</td></tr>
      <tr><td>Aug</td><td>277:00:00</td></tr>
      <tr><td>Sep</td><td>260:12:00</td></tr>
      <tr><td>Oct</td><td>327:08:00</td></tr>
      <tr><td>Nov</td><td>270:41:00</td></tr>
      <tr><td>Dec</td><td>257:24:00</td></tr>
    </table>
  </div>

  <!-- Machine Table (FULL ORDER M1 → M18) -->
  <div class="section-box">
    <h3>⚙️ Machine-wise Breakdown Frequency Report</h3>

    <table>
      <tr><th>Machine</th><th>Total Breakdown Count</th></tr>
      <tr><td>Crates Area/Line</td><td>635</td></tr>
      <tr><td>M1</td><td>822</td></tr>
      <tr><td>M2</td><td>621</td></tr>
      <tr><td>M3</td><td>538</td></tr>
      <tr><td>M4</td><td>590</td></tr>
      <tr><td>M5</td><td>1</td></tr>
      <tr><td>M6</td><td>574</td></tr>
      <tr><td>M7</td><td>825</td></tr>
      <tr><td>M8</td><td>614</td></tr>
      <tr><td>M9</td><td>59</td></tr>
      <tr><td>M10</td><td>1</td></tr>
      <tr><td>M12</td><td>366</td></tr>
      <tr><td>M13</td><td>317</td></tr>
      <tr><td>M14</td><td>805</td></tr>
      <tr style="font-weight:bold;background:#f8d7da;"><td>M15</td><td>963 (Highest)</td></tr>
      <tr><td>M16</td><td>214</td></tr>
      <tr><td>M17</td><td>511</td></tr>
      <tr><td>M18</td><td>447</td></tr>
    </table>
  </div>

</div>

<footer>
  NADEC Drinkable Plant | Technician Workload + Downtime Dashboard 2025 | GitHub Pages Ready
</footer>

<script>
  new Chart(document.getElementById("monthlyChart"), {
    type: "bar",
    data: {
      labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
      datasets: [{
        label: "Downtime Hours",
        data: [285,241,312,222,304,260,446,277,260,327,270,257]
      }]
    }
  });

  new Chart(document.getElementById("machineChart"), {
    type: "bar",
    data: {
      labels: ["M15","M7","M1","M14","M2"],
      datasets: [{
        label: "Breakdown Count",
        data: [963,825,822,805,621]
      }]
    },
    options: { indexAxis: "y" }
  });

  new Chart(document.getElementById("techChart"), {
    type: "pie",
    data: {
      labels: ["Dante","Sameer","Gilbert","Lito","Husam","Ali"],
      datasets: [{
        data: [1541,1479,1395,1236,1214,753]
      }]
    }
  });

  new Chart(document.getElementById("techBar"), {
    type: "bar",
    data: {
      labels: ["Dante","Sameer","Gilbert","Lito","Husam","Amgad","Ali"],
      datasets: [{
        label: "Total Contribution",
        data: [1541,1479,1395,1236,1214,1112,753]
      }]
    },
    options: { indexAxis: "y" }
  });
</script>

</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Machine Data Table</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f9f9f9;
        }
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
            background-color: #fff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: center;
        }
        th {
            background-color: #0077cc;
            color: white;
        }
        tr:nth-child(even){
            background-color: #f2f2f2;
        }
        caption {
            caption-side: top;
            font-size: 1.5em;
            margin-bottom: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<table>
    <caption>Machine Area Wise Repeted Issue</caption>
    <thead>
        <tr>
            <th>Machine No</th>
            <th>Area</th>
            <th>Count</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>M1</td><td>Filling & Capping</td><td>543</td></tr>
        <tr><td>M1</td><td>Downline</td><td>231</td></tr>
        <tr><td>M1</td><td>Crates Area /Line</td><td>12</td></tr>
        <tr><td>M2</td><td>Filling & Capping</td><td>434</td></tr>
        <tr><td>M2</td><td>Downline</td><td>169</td></tr>
        <tr><td>M2</td><td>Upstream</td><td>18</td></tr>
        <tr><td>M3</td><td>Filling & Capping</td><td>250</td></tr>
        <tr><td>M3</td><td>Upstream</td><td>50</td></tr>
        <tr><td>M3</td><td>Downline</td><td>237</td></tr>
        <tr><td>M3</td><td>Crates Area /Line</td><td>1</td></tr>
        <tr><td>M4</td><td>Filling & Capping</td><td>283</td></tr>
        <tr><td>M4</td><td>Downline</td><td>289</td></tr>
        <tr><td>M4</td><td>Upstream</td><td>16</td></tr>
        <tr><td>M4</td><td>Crates Area /Line</td><td>1</td></tr>
        <tr><td>M5</td><td>Filling & Capping</td><td>1</td></tr>
        <tr><td>M6</td><td>Filling & Capping</td><td>396</td></tr>n        <tr><td>M6</td><td>Upstream</td><td>115</td></tr>
        <tr><td>M6</td><td>Downline</td><td>63</td></tr>
        <tr><td>M7</td><td>Filling & Capping</td><td>324</td></tr>
        <tr><td>M7</td><td>Upstream</td><td>88</td></tr>
        <tr><td>M7</td><td>Downline</td><td>413</td></tr>
        <tr><td>M8</td><td>Upstream</td><td>56</td></tr>n        <tr><td>M8</td><td>Downline</td><td>329</td></tr>
        <tr><td>M8</td><td>Filling & Capping</td><td>229</td></tr>
        <tr><td>M9</td><td>Upstream</td><td>6</td></tr>
        <tr><td>M9</td><td>Filling & Capping</td><td>35</td></tr>
        <tr><td>M9</td><td>Downline</td><td>18</td></tr>
        <tr><td>M10</td><td>Downline</td><td>1</td></tr>
        <tr><td>M12</td><td>Filling & Capping</td><td>115</td></tr>
        <tr><td>M12</td><td>Downline</td><td>223</td></tr>
        <tr><td>M12</td><td>Upstream</td><td>28</td></tr>n        <tr><td>M13</td><td>Upstream</td><td>65</td></tr>
        <tr><td>M13</td><td>Downline</td><td>94</td></tr>n        <tr><td>M13</td><td>Filling & Capping</td><td>158</td></tr>
        <tr><td>M14</td><td>Filling & Capping</td><td>546</td></tr>
        <tr><td>M14</td><td>Downline</td><td>226</td></tr>
        <tr><td>M14</td><td>Upstream</td><td>33</td></tr>
        <tr><td>M15</td><td>Downline</td><td>378</td></tr>
        <tr><td>M15</td><td>Upstream</td><td>178</td></tr>
        <tr><td>M15</td><td>Filling & Capping</td><td>405</td></tr>
        <tr><td>M15</td><td>Crates Area /Line</td><td>2</td></tr>
        <tr><td>M16</td><td>Filling & Capping</td><td>123</td></tr>
        <tr><td>M16</td><td>Upstream</td><td>9</td></tr>
        <tr><td>M16</td><td>Downline</td><td>82</td></tr>n        <tr><td>M17</td><td>Filling & Capping</td><td>314</td></tr>
        <tr><td>M17</td><td>Upstream</td><td>50</td></tr>
        <tr><td>M17</td><td>Downline</td><td>147</td></tr>n        <tr><td>M18</td><td>Filling & Capping</td><td>259</td></tr>
        <tr><td>M18</td><td>Upstream</td><td>24</td></tr>
        <tr><td>M18</td><td>Downline</td><td>164</td></tr>
        <tr><td>Crates Area/Line</td><td>Crates Area /Line</td><td>633</td></tr>
        <tr><td>Crates Area/Line</td><td>Downline</td><td>2</td></tr>
    </tbody>
</table>
  <!-- ================== BREAKDOWN DASHBOARD ADD-ON ================== -->

<div class="card">
  <h2>🔥 Hourly Breakdown Heatmap (Hour vs Month)</h2>
  <div style="overflow-x:auto;">
    <table id="heatmapTable" style="width:100%; border-collapse:collapse;"></table>
  </div>
</div>

<div class="card">
  <h2>📈 Monthly Breakdown Trend (Total per Month)</h2>
  <canvas id="monthlyTrendChart"></canvas>
</div>

<div class="card">
  <h2>📊 Total Breakdown by Hour (0–23)</h2>
  <canvas id="hourlyTotalChart"></canvas>
</div>


<script>
/* ===================== DATA ===================== */
const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

const breakdownData = [
 [14.4,13.4,11.0,10.9,18.8,9.3,13.3,16.9,10.3,11.6,9.2,10.0],
 [11.0,11.2,17.3,9.9,10.1,13.2,11.8,11.7,11.5,19.5,12.3,15.7],
 [7.9,15.4,10.9,6.7,10.9,7.8,22.4,9.3,10.0,7.0,9.4,11.8],
 [5.9,11.0,8.8,8.8,9.5,8.0,8.9,10.9,5.8,4.4,7.0,9.5],
 [6.6,10.7,10.0,8.0,7.0,5.0,123.1,9.3,8.1,9.5,9.4,8.2],
 [1.5,1.7,18.0,5.8,2.5,0.9,4.1,3.3,1.4,0.7,1.3,2.6],
 [21.0,14.7,19.3,16.7,18.4,22.5,34.0,16.0,14.2,27.1,11.3,11.9],
 [14.6,14.7,14.0,8.0,20.0,19.3,15.0,21.5,22.5,22.0,24.4,17.3],
 [18.0,11.3,8.4,9.8,23.8,10.5,17.6,15.5,13.5,32.6,27.6,16.1],
 [10.0,11.3,15.5,9.6,15.2,16.9,16.6,14.3,10.8,28.5,9.4,9.0],
 [6.1,4.3,6.0,8.4,12.0,18.5,13.1,11.5,12.6,7.8,15.5,6.7],
 [3.8,3.9,12.4,1.7,3.2,5.6,0.8,6.0,1.8,2.4,4.5,3.3],
 [7.5,10.5,14.8,11.1,5.6,7.8,18.3,10.1,12.0,10.8,8.5,8.2],
 [12.3,9.9,13.5,8.7,20.3,13.7,17.1,21.7,11.5,17.1,17.7,14.0],
 [15.5,11.2,11.9,8.7,12.4,13.6,20.9,13.1,10.5,15.7,14.6,21.2],
 [8.4,12.0,7.0,13.5,10.7,8.2,12.6,9.0,17.8,15.3,11.0,10.4],
 [26.6,8.5,2.8,5.5,11.8,10.7,9.7,7.4,12.8,14.8,10.7,8.1],
 [17.8,4.3,18.2,1.9,4.4,5.6,8.3,3.0,2.6,3.1,3.6,3.7],
 [24.4,12.2,19.1,11.1,24.5,14.1,15.9,18.0,13.6,17.3,13.4,12.0],
 [4.7,4.4,18.2,13.4,12.8,1.4,4.5,3.8,1.4,4.4,6.9,1.0],
 [14.8,6.0,11.8,9.5,9.5,16.1,6.4,11.3,11.2,12.1,10.9,16.7],
 [14.8,14.8,14.2,8.5,12.9,12.1,12.1,14.0,11.9,13.4,9.8,15.1],
 [9.0,13.9,10.3,9.4,13.0,9.7,20.0,9.7,14.4,20.7,16.0,14.6],
 [9.3,10.4,19.1,16.7,15.0,9.8,20.6,9.8,18.0,9.5,6.0,10.0]
];


/* ===================== HEATMAP TABLE ===================== */
let heatmapHTML = "<tr><th style='background:black;color:white;'>Hour</th>";

months.forEach(m=>{
  heatmapHTML += `<th style='background:black;color:white;'>${m}</th>`;
});
heatmapHTML += "</tr>";

breakdownData.forEach((row,hour)=>{
  heatmapHTML += `<tr><th style='background:#222;color:white;'>${hour}</th>`;

  row.forEach(val=>{
    let intensity = Math.min(val/35,1);
    heatmapHTML += `\n      <td style="padding:6px;border:1px solid #ddd;\n      background:rgba(255,0,0,${intensity});\n      font-weight:bold;">\n      ${val.toFixed(1)}\n      </td>`;
  });

  heatmapHTML += "</tr>";
});

document.getElementById("heatmapTable").innerHTML = heatmapHTML;


/* ===================== MONTHLY TREND ===================== */
const monthlyTotals = months.map((m,i)=>
  breakdownData.reduce((sum,row)=> sum + row[i], 0)
);

new Chart(document.getElementById("monthlyTrendChart"), {
  type: "line",
  data: {
    labels: months,
    datasets: [{
      label: "Total Breakdown Hours per Month",
      data: monthlyTotals,
      borderWidth: 3,
      tension: 0.3
    }]
  }
});


/* ===================== HOURLY TOTAL ===================== */
const hourlyTotals = breakdownData.map(row =>
  row.reduce((a,b)=> a+b, 0)
);

new Chart(document.getElementById("hourlyTotalChart"), {
  type: "bar",
  data: {
    labels: [...Array(24).keys()],
    datasets: [{
      label: "Total Breakdown Hours (Yearly Total)",
      data: hourlyTotals,
      borderWidth: 1
    }]
  }
});
</script>

<!-- ================== END ADD-ON ================== -->'''

# 1. Data Extraction
soup = BeautifulSoup(html_content, 'html.parser')

# 1.1 Extract KPI Data
kpi_cards = soup.find_all('div', class_='kpi-card')
kpi_data = {}

for card in kpi_cards:
    kpi_name = card.find('h2').get_text(strip=True)
    kpi_value = card.find('p').get_text(strip=True)
    kpi_data[kpi_name] = kpi_value

total_downtime_hours = kpi_data.get('Total Downtime Hours')
total_breakdown_events = kpi_data.get('Total Breakdown Events')
worst_downtime_month = kpi_data.get('Worst Downtime Month')
highest_breakdown_machine = kpi_data.get('Highest Breakdown Machine')
top_technician_contributor = kpi_data.get('Top Technician Contributor')

# 1.2 Extract Monthly Downtime Data
script_tags = soup.find_all('script')
monthly_chart_script = None
for script in script_tags:
    if script.string and 'monthlyChart' in script.string:
        monthly_chart_script = script.string
        break

monthly_downtime_labels = []
monthly_downtime_data = []

if monthly_chart_script:
    labels_match = re.search(r'labels:\s*\[([^\]]+)\]', monthly_chart_script)
    if labels_match:
        labels_str = labels_match.group(1).replace('"', '').replace("'", '').split(',')
        monthly_downtime_labels = [label.strip() for label in labels_str]

    data_match = re.search(r'data:\s*\[([^\]]+)\]', monthly_chart_script)
    if data_match:
        data_str = data_match.group(1).split(',')
        monthly_downtime_data = [int(val.strip()) for val in data_str]

# 1.3 Extract Machine Breakdown Data
machine_chart_config_str = None
for script in script_tags:
    if script.string:
        match = re.search(r'new Chart\(document\.getElementById\("machineChart"\),\s*(\{.*?\})\);', script.string, re.DOTALL)
        if match:
            machine_chart_config_str = match.group(1)
            break

machine_breakdown_labels = []
machine_breakdown_data = []

if machine_chart_config_str:
    labels_match = re.search(r'labels:\s*\[([^\]]+)\]', machine_chart_config_str)
    if labels_match:
        labels_str = labels_match.group(1).replace('"', '').replace("'", '').split(',')
        machine_breakdown_labels = [label.strip() for label in labels_str]

    data_match = re.search(r'data:\s*\[([^\]]+)\]', machine_chart_config_str)
    if data_match:
        data_str = data_match.group(1).split(',')
        machine_breakdown_data = [int(val.strip()) for val in data_str]

# 1.4 Extract Technician Contribution Share
tech_chart_config_str = None
for script in script_tags:
    if script.string:
        match = re.search(r'new Chart\(document\.getElementById\("techChart"\),\s*\{.*?data:\s*\{.*?labels:\s*\[([^\]]+)\].*?datasets:\s*\[\{.*?data:\s*\[([^\]]+)\]', script.string, re.DOTALL)
        if match:
            tech_contribution_labels_str = match.group(1)
            tech_contribution_data_str = match.group(2)
            break

tech_contribution_labels = []
tech_contribution_data = []

if tech_contribution_labels_str and tech_contribution_data_str:
    labels_list = tech_contribution_labels_str.replace('"', '').replace("'", '').split(',')
    tech_contribution_labels = [label.strip() for label in labels_list]

    data_list = tech_contribution_data_str.split(',')
    tech_contribution_data = [int(val.strip()) for val in data_list]

# 1.5 Extract Top Technician Workload Ranking
tech_bar_config_str = None
for script in script_tags:
    if script.string:
        match = re.search(r'new Chart\(document\.getElementById\("techBar"\),\s*\{.*?data:\s*\{.*?labels:\s*\[([^\]]+)\].*?datasets:\s*\[\{.*?data:\s*\[([^\]]+)\]', script.string, re.DOTALL)
        if match:
            tech_bar_labels_str = match.group(1)
            tech_bar_data_str = match.group(2)
            break

tech_bar_labels = []
tech_bar_data = []

if tech_bar_labels_str and tech_bar_data_str:
    labels_list = tech_bar_labels_str.replace('"', '').replace("'", '').split(',')
    tech_bar_labels = [label.strip() for label in labels_list]

    data_list = tech_bar_data_str.split(',')
    tech_bar_data = [int(val.strip()) for val in data_list]


# 1.6 Extract Monthly Breakdown Trend and Hourly Breakdown Heatmap Data
main_script_content = None
for script in script_tags:
    if script.string and 'breakdownData' in script.string:
        main_script_content = script.string
        break

months_trend = []
breakdown_data_raw = []

if main_script_content:
    months_match = re.search(r'const months = \[(.*?)\];', main_script_content)
    if months_match:
        months_str_raw = months_match.group(1)
        months_trend = [month.strip().strip('"') for month in months_str_raw.split(',')]

    breakdown_data_match = re.search(r'const breakdownData = \[\s*((?:\[[\d\.,\s]+\](?:,\s*)?)+)\s*\];', main_script_content, re.DOTALL)

    if breakdown_data_match:
        breakdown_data_str = breakdown_data_match.group(1)
        rows_raw = re.findall(r'\[[\d\.,\s]+\]', breakdown_data_str)
        for row_str in rows_raw:
            clean_row = row_str.replace('[', '').replace(']', '').strip()
            if clean_row:
                breakdown_data_raw.append([float(val.strip()) for val in clean_row.split(',')])

monthly_breakdown_trend_data = []
if months_trend and breakdown_data_raw:
    if breakdown_data_raw and len(breakdown_data_raw[0]) == len(months_trend):
        for i in range(len(months_trend)):
            month_total = sum(row[i] for row in breakdown_data_raw)
            monthly_breakdown_trend_data.append(month_total)

hourly_labels = list(range(24))
hourly_total_breakdown_data = []

if breakdown_data_raw:
    for i in range(len(breakdown_data_raw)):
        hourly_total = sum(breakdown_data_raw[i])
        hourly_total_breakdown_data.append(hourly_total)


# 1.7 Extract Table Data

# Technician Full Table
technician_table_h3 = soup.find('h3', string='👷 Full Technician Monthly Breakdown Workload (Jan–Dec)')
technician_workload_df = pd.DataFrame()
if technician_table_h3:
    technician_table = technician_table_h3.find_next_sibling('table')
    if technician_table:
        headers = [th.get_text(strip=True) for th in technician_table.find('tr').find_all('th')]
        rows = []
        for tr in technician_table.find_all('tr')[1:]:
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            rows.append(cells)
        technician_workload_df = pd.DataFrame(rows, columns=headers)

# Month Downtime Table
month_downtime_h3 = soup.find('h3', string='📅 Month-wise Breakdown Downtime Summary')
month_downtime_df = pd.DataFrame()
if month_downtime_h3:
    month_downtime_table = month_downtime_h3.find_next_sibling('table')
    if month_downtime_table:
        headers = [th.get_text(strip=True) for th in month_downtime_table.find('tr').find_all('th')]
        rows = []
        for tr in month_downtime_table.find_all('tr')[1:]:
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            rows.append(cells)
        month_downtime_df = pd.DataFrame(rows, columns=headers)

# Machine Breakdown Frequency Report
machine_frequency_h3 = soup.find('h3', string='⚙️ Machine-wise Breakdown Frequency Report')
machine_frequency_df = pd.DataFrame()
if machine_frequency_h3:
    machine_frequency_table = machine_frequency_h3.find_next_sibling('table')
    if machine_frequency_table:
        headers = [th.get_text(strip=True) for th in machine_frequency_table.find('tr').find_all('th')]
        rows = []
        for tr in machine_frequency_table.find_all('tr')[1:]:
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            rows.append(cells)
        machine_frequency_df = pd.DataFrame(rows, columns=headers)

# Machine Area Wise Repeated Issue
machine_area_table_caption = soup.find('caption', string='Machine Area Wise Repeted Issue')
machine_area_df = pd.DataFrame()
if machine_area_table_caption:
    machine_area_table = machine_area_table_caption.find_parent('table')
    if machine_area_table:
        headers = [th.get_text(strip=True) for th in machine_area_table.find('thead').find('tr').find_all('th')]
        rows = []
        for tr in machine_area_table.find('tbody').find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            rows.append(cells)
        machine_area_df = pd.DataFrame(rows, columns=headers)

# Hourly Breakdown Heatmap DataFrame
heatmap_df = pd.DataFrame(breakdown_data_raw, columns=months_trend, index=hourly_labels)


# 2. Streamlit Dashboard Layout
st.set_page_config(layout="wide", page_title="NADEC Breakdown Maintenance Dashboard 2025")
st.title("NADEC Drinkable Maintenance Performance Report of 2025")
st.markdown("<h3 style='text-align: center; color: grey;'>Breakdown Downtime | Machine Failures | Technician Workload Contribution Dashboard</h3>", unsafe_allow_html=True)

# KPI Section
st.subheader("Key Performance Indicators")
kpi_cols = st.columns(5)

# Charts Section
st.subheader("Visual Insights")
chart_row_1 = st.columns(2)
chart_row_2 = st.columns(2)

# Tables Section
st.subheader("Detailed Data Tables")

# Containers for tables and additional charts
technician_table_container = st.container()
month_downtime_table_container = st.container()
machine_frequency_table_container = st.container()
machine_area_table_container = st.container()
heatmap_container = st.container()
monthly_trend_chart_container = st.container()
hourly_total_chart_container = st.container()

# 3. Populate Streamlit Dashboard

# 3.1 Populate KPIs
kpi_labels = list(kpi_data.keys())
kpi_values = list(kpi_data.values())

for i, col in enumerate(kpi_cols):
    with col:
        st.metric(label=kpi_labels[i], value=kpi_values[i])

# 3.2 Populate Charts

# Monthly Downtime Hours
with chart_row_1[0]:
    st.subheader("Monthly Downtime Hours")
    monthly_downtime_df = pd.DataFrame({
        'Month': monthly_downtime_labels,
        'Downtime Hours': monthly_downtime_data
    })
    st.bar_chart(monthly_downtime_df.set_index('Month'))

# Top Machines Breakdown Count
with chart_row_1[1]:
    st.subheader("Top Machines Breakdown Count")
    machine_breakdown_df = pd.DataFrame({
        'Machine': machine_breakdown_labels,
        'Breakdown Count': machine_breakdown_data
    })
    chart = alt.Chart(machine_breakdown_df).mark_bar().encode(
        x='Breakdown Count',
        y=alt.Y('Machine', sort='-x')
    ).properties(title='Top Machines Breakdown Count')
    st.altair_chart(chart, width='stretch')

# Technician Contribution Share (Pie Chart)
with chart_row_2[0]:
    st.subheader("Technician Contribution Share")
    tech_contribution_df = pd.DataFrame({
        'Technician': tech_contribution_labels,
        'Contribution': tech_contribution_data
    })
    chart = alt.Chart(tech_contribution_df).mark_arc().encode(
        theta=alt.Theta(field="Contribution", type="quantitative"),
        color=alt.Color(field="Technician", type="nominal", title="Technician"),
        order=alt.Order("Contribution", sort="descending"),
        tooltip=["Technician", "Contribution"]
    ).properties(title='Technician Contribution Share')
    st.altair_chart(chart, width='stretch')

# Top Technician Workload Ranking
with chart_row_2[1]:
    st.subheader("Top Technician Workload Ranking")
    tech_workload_df = pd.DataFrame({
        'Technician': tech_bar_labels,
        'Total Contribution': tech_bar_data
    })
    chart = alt.Chart(tech_workload_df).mark_bar().encode(
        x='Total Contribution',
        y=alt.Y('Technician', sort='-x')
    ).properties(title='Top Technician Workload Ranking')
    st.altair_chart(chart, width='stretch')

# Monthly Breakdown Trend
with monthly_trend_chart_container:
    st.subheader("Monthly Breakdown Trend (Total per Month)")
    monthly_trend_df = pd.DataFrame({
        'Month': months_trend,
        'Total Breakdown Hours': monthly_breakdown_trend_data
    })
    st.line_chart(monthly_trend_df.set_index('Month'))

# Total Breakdown by Hour
with hourly_total_chart_container:
    st.subheader("Total Breakdown by Hour (0–23)")
    hourly_breakdown_df = pd.DataFrame({
        'Hour': hourly_labels,
        'Total Breakdown Hours': hourly_total_breakdown_data
    })
    st.bar_chart(hourly_breakdown_df.set_index('Hour'))


# 3.3 Populate Tables

# Display "Full Technician Monthly Breakdown Workload (Jan–Dec)"
with technician_table_container:
    st.markdown("#### ⚒⚒ Full Technician Monthly Breakdown Workload (Jan–Dec)")
    st.dataframe(technician_workload_df, width='stretch')

# Display "Month-wise Breakdown Downtime Summary"
with month_downtime_table_container:
    st.markdown("#### 📆 Month-wise Breakdown Downtime Summary")
    st.dataframe(month_downtime_df, width='stretch')

# Display "Machine-wise Breakdown Frequency Report"
with machine_frequency_table_container:
    st.markdown("#### ⚙️ Machine-wise Breakdown Frequency Report")
    st.dataframe(machine_frequency_df, width='stretch')

# Display "Machine Area Wise Repeated Issue"
with machine_area_table_container:
    st.markdown("#### Machine Area Wise Repeated Issue")
    st.dataframe(machine_area_df, width='stretch')

# Display "Hourly Breakdown Heatmap (Hour vs Month)"
with heatmap_container:
    st.markdown("#### 🔥 Hourly Breakdown Heatmap (Hour vs Month)")
    st.dataframe(heatmap_df, width='stretch')
