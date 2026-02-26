import streamlit as st

# Define the machine maintenance history data
MACHINE_HISTORY = {
    "CRATES AREA": [
        "Aligned the drive sprocket and corrected conveyor tracking.",
        "Secured lifter roller guide by installing missing bolt.",
        "Reconnected multiple cut or damaged conveyor sections and restored conveyor continuity.",
        "Rectified conveyor line faults, including derailed and jammed sections.",
        "Checked and corrected stacker and destacker operational faults.",
        "Repaired and realigned crates lifter arm assemblies.",
        "Removed worn bearings and broken bolts; installed new bearings and hardware.",
        "Removed drive motor and sprocket, replenished shaft, and reinstalled complete drive assembly.",
        "Repaired damaged overhead conveyors, including link replacement and structural welding.",
        "Repaired damaged inclined conveyor and restored chain tension.",
        "Replaced damaged or broken sensors (crates detection, destacker, safety, infeed).",
        "Replaced damaged drive sprocket and overhead conveyor sprocket.",
        "Replaced crates lifter arm base block bearings and spindle shaft swing arm bearings.",
        "Replaced damaged plastic guide on S/S infeed conveyor and corrected loose links.",
        "Replaced defective cables, photo sensors, and wiring connections.",
        "Reset conveyor system faults, VFD alarms, and motor protection trips.",
        "Cleaned motor terminals and restored electrical continuity.",
        "Repaired broken rods and welded damaged components as required.",
        "Removed broken conveyor links and reconnected overhead crates divider conveyor; reset drive motor fault.",
        "Removed damaged drive shaft and sprocket for machining and rebuild.",
        "Installed new drive motor and restored system operation.",
        "Secured mounting of destacker crates presence sensor and corrected conveyor derailment.",
        "Tightened chain tensioner; noted requirement for sprocket replacement.",
        "Replaced busted fuse and restored panel breaker operation.",
        "Repaired and adjusted crates conveyor system to eliminate repeated stoppages.",
        "Replaced damaged overhead crates conveyor sections and restored full movement.",
        "Performed general welding, fabrication, and mechanical corrections across conveyor assemblies.",
        "Logged condition: one side running manually; replacement sprocket machining required.",
        "Noted damaged arm bearings for day shift follow-up."
    ],
    "M1": [
        "Adjusted capper mechanisms including cap chute, cap dispenser, cap sorter, and overall capper alignment.",
        "Fine-tuned torque settings and air regulators for stable capping performance.",
        "Aligned capping heads and cap applicator assemblies to correct misalignment and improve cap placement accuracy.",
        "Checked and adjusted filler cylinder rod and product regulating valve to stabilize filling operation.",
        "Rectified capper #1 and #4 issues, including height adjustment of cap dispenser and replacement of capper finger pin.",
        "Repaired and adjusted cap holder assembly; noted finger cam replacement requirement.",
        "Replaced broken filler piston, broken nozzle pin, and defective sensors/cables.",
        "Replaced capper spindle using available spare and fine-tuned jaw air pressure.",
        "Replaced defective torque limiter and restored proper torque control.",
        "Replaced capper piston assembly and corrected timing after detachment from the mechanism.",
        "Installed new air regulator to stabilize jaw air pressure.",
        "Lubricated capper assembly and performed routine mechanical adjustments.",
        "Fabricated and installed capper bottle guide to correct bottle flow issues.",
        "Repaired overhead conveyor sprocket and reconnected broken overhead conveyor sections.",
        "Removed broken conveyor links, replaced damaged links, and restored conveyor operation.",
        "Removed sliding plate bracket, extracted broken bolt, replaced hardware, and reinstalled assembly.",
        "Reset VLT/VFD drive faults, motor faults, stacker faults, and circuit breaker trips.",
        "Troubleshot auto-mode failure; found solenoid valves contaminated with water, cleaned and replaced corroded coils.",
        "Troubleshot carriage plate not opening and resolved mechanical obstruction.",
        "Troubleshot automatic operation failure; corrected loose selector switch connection.",
        "Released air lock and restored pneumatic operation.",
        "Repaired stacker system issues and reset crates stacker system fault.",
        "Welded cap applicator lock to eliminate excessive movement and prevent misalignment.",
        "Repaired damaged crates conveyor and restored overhead conveyor alignment.",
        "Rebalanced crates lifter and cleared system fault.",
        "Updated machine message display due to corrupted characters."
    ],
    # Add additional machine histories (M13, M14, etc.) here...
}

# Streamlit app layout
st.title("Machine Maintenance History")
st.sidebar.title("Select a Maintenance History")

# Button for each machine
for machine in MACHINE_HISTORY:
    if st.sidebar.button(machine):
        st.subheader(f"{machine} Maintenance History")
        st.write("\n".join(MACHINE_HISTORY[machine]))
