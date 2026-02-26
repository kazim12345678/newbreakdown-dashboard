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
M2 HISTORY
Capper System Adjustments & Timing Corrections
•	Adjusted alignment of capper assembly, cap applicator, cap chute stopper, and cap dispenser.
•	Corrected timing of bottle screw, capper heads, cap plate, and cap dispenser.
•	Fine‑tuned torque pressure, torque limiter settings, and cap grip air pressure for stable capping.
•	Aligned capper heads, capper plate, spindle #3 & #4, and cap conveyor height to cap chute.
•	Adjusted capper #2 and #4 torque settings; noted finger cams and capper fingers require replacement (no spare available).
•	Zeroed encoder position and restored capper carousel alignment.
Crates, Hopper & Bottle Handling
•	Adjusted and activated crates hopper sensor; aligned crates stacker lifter on both sides.
•	Checked and rectified bottle stopper issues and restored proper bottle flow.
•	Removed clogged plastic bottles from capper area.
•	Repaired bottle elevator and corrected mechanical alignment.
Sensors, Electrical & Control System
•	Checked and adjusted hopper level sensor and packer sensor activation.
•	Rectified missing signal of crates stopper and repaired micro valve switch.
•	Replaced defective infeed safety sensor and restored machine stopping logic.
•	Reset machine faults and restored encoder zero position.
•	Cleaned printhead and restored print quality.
Mechanical Repairs & Component Replacement
•	Repaired capper heads #2, #3, and #4; replaced capper fingers using old spare to correct cross‑capping.
•	Repaired torque limiter, cap holder assembly, and cap applicator timing.
•	Repaired packer head and bottle air sprayer.
•	Repaired detached filler rod pin, cylinder lock for nozzle, and disconnected solenoid valve wiring.
•	Repaired roller assembly, welded broken parts, and reinstalled.
•	Repaired detached drive chain of conveyor and rejoined broken conveyor sections.
•	Rebalanced crates lifter and adjusted lifter stopper.
Pneumatics & Air System
•	Repaired air leakage and rectified hopper level sensor issues.
•	Installed back detached filler air supply.
•	Increased capper jaw air pressure (capper fingers still require replacement).
•	Replaced defective cylinder of crates stopper and defective suction head.
Component Replacement
•	Replaced damaged lock bolt, cap gripper spring, and torque limiter (due to defective one‑way bearing).
•	Replaced solenoid valve and tested operation.
•	Replaced bottle picker and defective micro valve switch.
•	Replaced damaged lock bolt and retimed assembly.
•	Replaced defective torque limiter and restored torque control.
General Maintenance & Restorations
•	Applied grease on torque limiter gear drive; gear drive requires replacement.
•	Checked and rectified product level issues.
•	Checked and repaired cap dispenser due to caps falling.
•	Performed alignment and timing corrections across capper and filler assemblies.
•	Completed multiple resets after mechanical or electrical corrections.
 

""",

    "M3": """
M3 – MACHINE HISTORY
Mechanical Adjustments & Timing Corrections
•	Adjusted conveyor belt alignment and tension, including bottle cable conveyor tensioning.
•	Adjusted divider sensor activation and corrected general sensor alignment.
•	Adjusted timing of starwheel #5 and retimed outfeed starwheel.
•	Aligned bottle sensor, drive sprocket, and capper starwheel.
•	Corrected bottle stopper alignment and restored proper bottle flow.
Capper, Filler & Bottle Handling Systems
•	Identified finger cam wear; replacement required but no spare available.
•	Repaired cap holder assembly and corrected cap holder finger issues.
•	Repaired packer bottle stopper and C‑loop pusher.
•	Repaired filler #3 and #8 assemblies and corrected mechanical alignment.
•	Repaired bottle air sprayer and restored proper operation.
Sensors, Electrical & Control System
•	Replaced damaged sensor cables, defective sensors, and faulty stacker door switch.
•	Replaced magnetic contactor and restored electrical continuity.
•	Reset stacker faults, breaker trips, and system alarms.
•	Repaired shorted motor cable and restored safe operation.
•	Installed back detached crates pusher and replaced busted sensor.
•	Repaired solenoid valve wiring and lubricated solenoid valves.
•	Troubleshot filling station communication issues; cleaned carbon brushes, checked communication cables, replaced TES net card, downloaded program, and tested.
•	Reinstalled detached carbon brushes and collector assembly.
Conveyor, Crates & Material Handling
•	Repaired damaged conveyor sections and packer crates conveyor.
•	Removed damaged conveyor links and reconnected conveyor.
•	Installed back detached roller bracket and corrected outfeed conveyor derailment.
•	Repaired crates lifter plate and restored lifting function.
•	Reconnected packer crates conveyor after mechanical failure.
Pneumatics & Air System
•	Fixed multiple air leakages and replaced damaged hose fittings for stopper cylinder.
•	Repaired detached cylinder end of carriage and restored pneumatic actuation.
•	Lubricated solenoid valves for bottle stopper and restored smooth operation.
Structural, Fabrication & Welding
•	Removed carriage plate, welded broken parts in workshop, and reinstalled.
•	Modified pulley side plate to allow proper tension adjustment.
•	Welded and repaired roller housing; replaced free‑wheel gear and aligned assembly.
Component Replacement
•	Replaced cut stacker left‑side lifting belt.
•	Replaced defective crates gate sensor and sensor cable assemblies.
•	Replaced worn‑out capper piston spring.
•	Replaced torque limiter and restored torque control.
•	Replaced solenoid valve using available spare.
•	Replaced printer with spare unit from M9 due to pressure fault.
General Maintenance & Restorations
•	Cleaned carbon brushes and adjusted brush length.
•	Cleaned printhead and restored print quality.
•	Fixed detached drive chain of conveyor and restored operation.
•	Performed routine lubrication and mechanical adjustments across assemblies.
•	Reset faults after mechanical or electrical corrections.
 

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
