<!-- ===================================== -->
<!-- REAL-TIME CUTE BREAKDOWN ENTRY SYSTEM -->
<!-- ===================================== -->

<div style="
  margin-top:50px;
  background:white;
  padding:25px;
  border-radius:18px;
  box-shadow:0 4px 14px rgba(0,0,0,0.15);
">

  <h2 style="color:#003366; text-align:center;">
    🛠 Live Breakdown Entry + Machine Tracker (M1–M18)
  </h2>

  <p style="text-align:center; color:gray; font-size:14px;">
    Add breakdown events daily. Click any machine tile to view total downtime minutes.
    Data saves automatically inside browser (GitHub Pages Ready).
  </p>

  <!-- Button Controls -->
  <div style="text-align:center; margin-top:15px;">
    <button onclick="toggleBreakdownForm()" style="
      background:#003366;
      color:white;
      border:none;
      padding:10px 18px;
      border-radius:12px;
      cursor:pointer;
      font-size:14px;
      margin:6px;
    ">
      ➕ Add Breakdown Entry
    </button>

    <button onclick="exportBreakdownCSV()" style="
      background:#198754;
      color:white;
      border:none;
      padding:10px 18px;
      border-radius:12px;
      cursor:pointer;
      font-size:14px;
      margin:6px;
    ">
      ⬇ Export CSV Report
    </button>
  </div>

  <!-- Hidden Form -->
  <div id="breakdownFormBox" style="
    display:none;
    margin-top:20px;
    padding:18px;
    border-radius:15px;
    background:#f8f9ff;
    max-width:600px;
    margin-left:auto;
    margin-right:auto;
  ">

    <h3 style="text-align:center; color:#003366;">
      Breakdown Data Entry Form
    </h3>

    <label>Date:</label>
    <input type="date" id="bDate" style="width:100%; padding:8px; margin:6px 0;">

    <label>Machine:</label>
    <select id="bMachine" style="width:100%; padding:8px; margin:6px 0;">
      <option>M1</option><option>M2</option><option>M3</option><option>M4</option>
      <option>M5</option><option>M6</option><option>M7</option><option>M8</option>
      <option>M9</option><option>M10</option><option>M11</option><option>M12</option>
      <option>M13</option><option>M14</option><option>M15</option><option>M16</option>
      <option>M17</option><option>M18</option>
    </select>

    <label>Downtime Minutes:</label>
    <input type="number" id="bTime" placeholder="Enter minutes"
      style="width:100%; padding:8px; margin:6px 0;">

    <label>Reason:</label>
    <select id="bReason" style="width:100%; padding:8px; margin:6px 0;">
      <option>Mechanical</option>
      <option>Electrical</option>
      <option>Automation</option>
      <option>Operator Error</option>
    </select>

    <button onclick="saveBreakdownEntry()" style="
      width:100%;
      margin-top:10px;
      background:#003366;
      color:white;
      border:none;
      padding:10px;
      border-radius:12px;
      cursor:pointer;
    ">
      ✅ Save Breakdown Entry
    </button>

  </div>

  <!-- Machine Tiles -->
  <h3 style="text-align:center; margin-top:35px; color:#003366;">
    Machine Downtime Tiles (Click Any Machine)
  </h3>

  <div id="machineTileGrid" style="
    display:grid;
    grid-template-columns:repeat(auto-fit, minmax(120px, 1fr));
    gap:12px;
    margin-top:20px;
  "></div>

  <!-- Breakdown Table -->
  <h3 style="text-align:center; margin-top:40px; color:#003366;">
    📋 Breakdown Log Table (Editable Daily)
  </h3>

  <table style="
    width:100%;
    border-collapse:collapse;
    margin-top:15px;
    font-size:13px;
    text-align:center;
  ">
    <thead>
      <tr style="background:#003366; color:white;">
        <th style="padding:10px;">Date</th>
        <th>Machine</th>
        <th>Minutes</th>
        <th>Reason</th>
      </tr>
    </thead>

    <tbody id="breakdownTableBody"></tbody>
  </table>

</div>

<!-- Popup Box -->
<div id="machinePopup" style="
  display:none;
  position:fixed;
  top:0; left:0;
  width:100%;
  height:100%;
  background:rgba(0,0,0,0.6);
  justify-content:center;
  align-items:center;
">

  <div style="
    background:white;
    padding:25px;
    border-radius:15px;
    width:90%;
    max-width:400px;
    text-align:center;
  ">
    <h2 id="popupMachineName"></h2>
    <p id="popupMachineInfo" style="color:gray;"></p>

    <button onclick="closeMachinePopup()" style="
      background:red;
      color:white;
      border:none;
      padding:8px 15px;
      border-radius:10px;
      cursor:pointer;
    ">
      Close
    </button>
  </div>

</div>

<script>
  let breakdownData =
    JSON.parse(localStorage.getItem("nadec_breakdowns")) || [];

  function toggleBreakdownForm() {
    let box = document.getElementById("breakdownFormBox");
    box.style.display = box.style.display === "none" ? "block" : "none";
  }

  function saveBreakdownEntry() {
    let entry = {
      date: document.getElementById("bDate").value,
      machine: document.getElementById("bMachine").value,
      time: Number(document.getElementById("bTime").value),
      reason: document.getElementById("bReason").value
    };

    breakdownData.push(entry);
    localStorage.setItem("nadec_breakdowns", JSON.stringify(breakdownData));

    renderBreakdownSystem();
  }

  function renderBreakdownSystem() {
    // Table Render
    let table = document.getElementById("breakdownTableBody");
    table.innerHTML = "";

    breakdownData.forEach(e => {
      table.innerHTML += `
        <tr>
          <td style="padding:8px;">${e.date}</td>
          <td>${e.machine}</td>
          <td>${e.time}</td>
          <td>${e.reason}</td>
        </tr>
      `;
    });

    // Machine Tiles Render
    let grid = document.getElementById("machineTileGrid");
    grid.innerHTML = "";

    for (let i = 1; i <= 18; i++) {
      let m = "M" + i;

      let total = breakdownData
        .filter(x => x.machine === m)
        .reduce((sum, x) => sum + x.time, 0);

      grid.innerHTML += `
        <div onclick="openMachinePopup('${m}', ${total})"
          style="
            background:white;
            border-radius:15px;
            padding:15px;
            text-align:center;
            box-shadow:0 3px 10px rgba(0,0,0,0.15);
            cursor:pointer;
          ">
          <h3 style="margin:0; color:#003366;">${m}</h3>
          <p style="margin:5px 0; font-size:13px; color:gray;">
            ${total} min downtime
          </p>
        </div>
      `;
    }
  }

  function openMachinePopup(machine, total) {
    document.getElementById("machinePopup").style.display = "flex";
    document.getElementById("popupMachineName").innerText = machine;
    document.getElementById("popupMachineInfo").innerText =
      "Total Downtime Minutes: " + total;
  }

  function closeMachinePopup() {
    document.getElementById("machinePopup").style.display = "none";
  }

  function exportBreakdownCSV() {
    let csv = "Date,Machine,Minutes,Reason\n";

    breakdownData.forEach(e => {
      csv += `${e.date},${e.machine},${e.time},${e.reason}\n`;
    });

    let blob = new Blob([csv], { type: "text/csv" });
    let link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "NADEC_Breakdown_Report.csv";
    link.click();
  }

  renderBreakdownSystem();
</script>
