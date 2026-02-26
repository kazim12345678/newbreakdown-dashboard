import streamlit as st

st.set_page_config(page_title="Machine History", layout="wide")

st.title("Machine History (M1 – M18)")
st.caption("Machine-wise history exactly as per maintenance sheet")

# ==========================================================
# 🔴 PASTE YOUR MACHINE HISTORY BELOW (WORD BY WORD)
# ==========================================================

MACHINE_HISTORY = {

    "CRATES AREA / LINE": """
CRATES AREA / LINE – MACHINE HISTORY (Technical Summary)

• Aligned the drive sprocket and corrected conveyor tracking.
• Secured lifter roller guide by installing missing bolt.
• Reconnected multiple cut or damaged conveyor sections and restored conveyor continuity.
• Rectified conveyor line faults, including derailed and jammed sections.
• Checked and corrected stacker and destacker operational faults.
• Repaired and realigned crates lifter arm assemblies.
• Removed worn bearings and broken bolts; installed new bearings and hardware.
• Removed drive motor and sprocket, replenished shaft, and reinstalled complete drive assembly.
• Repaired damaged overhead conveyors, including link replacement and structural welding.
• Repaired damaged inclined conveyor and restored chain tension.
• Replaced damaged or broken sensors (crates detection, destacker, safety, infeed).
• Reset conveyor system faults, VFD alarms, and motor protection trips.
• Logged condition: one side running manually; replacement sprocket machining required.
""",

    "M1": """
M1 – MACHINE HISTORY
•	Adjusted capper mechanisms including cap chute, cap dispenser, cap sorter, bottle stopper guide, and overall capper alignment.
•	Adjusted and fine‑tuned torque settings, torque limiters, and air regulators for stable capping performance.
•	Aligned capping heads and cap applicator assemblies to correct misalignment and improve cap placement accuracy.
•	Checked and adjusted filler cylinder rod and product regulating valve to stabilize filling operation.
•	Rectified capper #1 and #4 issues, including height adjustment of cap dispenser and replacement of capper finger pin.
•	Repaired and adjusted cap holder assembly; noted finger cam replacement requirement.
•	Replaced broken filler piston, broken nozzle pin, and defective sensors/cables.
•	Replaced capper spindle using available spare and fine‑tuned jaw air pressure.
•	Replaced defective torque limiter and restored proper torque control.
•	Replaced capper piston assembly and corrected timing after detachment from the mechanism.
•	Installed new air regulator to stabilize jaw air pressure.
•	Lubricated capper assembly and performed routine mechanical adjustments.
•	Fabricated and installed capper bottle guide to correct bottle flow issues.
•	Repaired overhead conveyor sprocket and reconnected broken overhead conveyor sections.
•	Removed broken conveyor links, replaced damaged links, and restored conveyor operation.
•	Removed sliding plate bracket, extracted broken bolt, replaced hardware, and reinstalled assembly.
•	Reset VLT/VFD drive faults, motor faults, stacker faults, and circuit breaker trips.
•	Troubleshot auto‑mode failure; found solenoid valves contaminated with water, cleaned and replaced corroded coils.
•	Troubleshot carriage plate not opening and resolved mechanical obstruction.
•	Troubleshot automatic operation failure; corrected loose selector switch connection.
•	Released air lock and restored pneumatic operation.
•	Repaired stacker system issues and reset crates stacker system fault.
•	Welded cap applicator lock to eliminate excessive movement and prevent misalignment.
•	Repaired damaged crates conveyor and restored overhead conveyor alignment.
•	Rebalanced crates lifter and cleared system fault.
•	Updated machine message display due to corrupted characters

""",

    "M2": """
M2 – MACHINE HISTORY (Technical Summary)

• Adjusted capper assembly alignment and timing.
• Checked bottle stopper operation and restored bottle flow.
• Repaired packer head and bottle air sprayer.
• Reset encoder position and restored capper carousel alignment.
""",

    "M3": """
M3 – MACHINE HISTORY (Technical Summary)

• Adjusted conveyor belt alignment and tension.
• Repaired cap holder assembly and corrected cap holder finger issues.
• Replaced damaged sensor cables and magnetic contactor.
• Reset stacker faults and system alarms.
""",

    # ⛔ CONTINUE SAME WAY ⛔
    # COPY EACH MACHINE HISTORY FROM YOUR CURRENT SHEET
    # EXACT WORDING – NO CHANGES
    # M4 ... M18
}

# ==========================================================
# ✅ UI
# ==========================================================

if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = "M1"

left, right = st.columns([1, 3])

with left:
    st.subheader("Machines")

    if st.button("CRATES AREA / LINE", use_container_width=True):
        st.session_state.selected_machine = "CRATES AREA / LINE"

    cols = st.columns(3)
    for i in range(1, 19):
        with cols[(i - 1) % 3]:
            if st.button(f"M{i}", use_container_width=True):
                st.session_state.selected_machine = f"M{i}"

with right:
    key = st.session_state.selected_machine
    st.subheader(f"{key} – Machine History")

    history = MACHINE_HISTORY.get(key)

    if history:
        st.text_area(
            label="",
            value=history.strip(),
            height=600
        )

        st.download_button(
            label=f"Download {key} History (TXT)",
            data=history.encode("utf-8"),
            file_name=f"{key}_machine_history.txt",
            mime="text/plain"
        )
    else:
        st.warning("Machine history not added yet.")
