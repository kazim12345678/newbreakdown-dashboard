import streamlit as st

st.set_page_config(page_title="Machine History Card", layout="wide")

st.title("Machine History Card (MHC)")

# -----------------------------
# MACHINE SELECTION
# -----------------------------
machines = [
    "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9",
    "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18",
    "Crates Area/Line"
]

machine = st.selectbox("Select Machine", machines)

st.markdown("---")

# -----------------------------
# MACHINE HISTORY DATA STORAGE
# -----------------------------
history_data = {
    "M2": {
        "summary": """
### **M2 – Machine History Summary**

#### **Capping System**
- Frequent alignment of capper heads, plates, spindles, and starwheels.
- Repeated torque adjustments (pressure, limiter, grip air pressure).
- Repaired/replaced torque limiters, springs, lock bolts, cap holder assemblies.
- Multiple capper finger replacements (spare shortage noted).
- Timing corrections for cap dispenser, cap chute, cap applicator.
- Full alignment of capper carousel and capper assembly.
- Resolved cross‑capping and bottle stopper issues.

#### **Sensors & Electrical**
- Reset multiple machine faults.
- Adjusted/activated hopper, crates stopper, and packer sensors.
- Replaced micro valve switch, solenoid valve, safety sensors.
- Fixed missing signals and restored filler air supply.

#### **Conveyors & Mechanical**
- Repaired packer head and dispenser issues.
- Fixed bottle guide, bottle elevator, air sprayer.
- Repaired broken conveyors, roller housings, drive chains.
- Rebalanced crates lifter and adjusted stoppers.

#### **Filler System**
- Repaired filler #2, #3, #8 (air leaks, rod pins, cylinder locks).
- Corrected product level issues.

#### **General Maintenance**
- Applied grease on torque limiter gear drive (replacement recommended).
- Zeroed encoder position.
- Removed clogged bottles.
- Routine timing adjustments across systems.
        """,

        "raw": """
Alligned the capper head.
Adjusted torque pressure and alligned.
Reset the fault.
Adjusted and activated crates hooper sensor.
Aligned the capper heads.
Adjusted the torque.
Adjusted the packer sensor to activate.
"to be updated"
Adjusted the timing, capper #2 need to replace finger cams.
Alligned cap conveyor height to cap chute.
Need to replaced finger cams, no spare available.
Adjusted torque limitor.
Replaced defective cylinder of crates stopper.
Adjusted the timing of capper.
Cleaned the printhead.
Finger cam need to replace, no spare available.
Checked and replaced capper finger using old spare due to cross capping issue.
Adjusted the cap applicator cap chunk.
Repaired cap holder assembly, need to replace finger.
Increased capper jaw air pressure, need to change capper fingers.
Adjusted the cap chute stopper.
Adjusted timing of cap dispenser.
Adjusted torque pressure of capper #2&4.
Repaired the cap dispenser due to some caps always down, make adjustment on the cap chute.
Repaired packer head problem.
Done possible adjustment/allignment, capper fingers need replacement, no spare available.
Repaired the bottle air sprayer.
Adjusted alignment of capper assembly and cap applicator.
Checked and adjusted hopper level sensor.
Checked and adjusted scale #2.
Repaired cap holder assembly.
Checked and alligned capper head #2 then adjusted torque of capper #4.
Checked and alligned capper starwheel.
Checked and alligned capper starwheel.
Checked and replaced damaged lock bolt.
Repaired cap applicator, adjusted timing of applicator.
Replaced cap gripper spring, adjusted the cap applicator timing.
Checked and repaired capper #2&3.
Fix the disconnected connection of solenoid valve.
Checked and adjusted torque for capper #4.
Replaced torque limitor due to defective one way bearing.
Adjusted cap dispenser due to cap missing.
Done adjusted the torque.
Replaced defective suction head.
Installed back detached filler air supply.
Adjusted the alignment of capper assembly.
Done allignment of capper carousel.
Done allignment of capper carousel.
Replaced broken lock bolt and retiming.
Checked the capper issue.
Adjusted the cap plate timing and repaired cap dispenser.
Alligned the capper head.
Alligned capper plate and spindle #3&4.
Repaired torque limitor and cap holder assembly.
Checked and repaired capper #4.
Applied grease on the gear drive of torque limitor, need to replace the gear drive.
Repaired torque limitor.
Tightened loose capper torque limitor holder bolts.
Adjusted the torque pressure and cap grip air pressure.
Troubleshoot stopping problem and replaced defective infeed safety sensor.
Adjusted the timing of bottle screw.
Removed the roller assy and bring to weld broken parts, handed over to day shift to continue works.
Checked and again cut again roller housing, replaced free wheel gear and alligned, welded and installed, monitor ok.
Alligned crates stacker lifter, both sides.
Checked and retiming cap dispenser.
Rebalanced crates lifter and afjusted lifter stopper.
Done zeroing of encoder position.
Replaced defective micro valve switch.
Checked and repaired bottle elevator.
Removed clogged  plastic bottle at the capper.
Done reset the fault.
Checked and rectified product level isue.
Replaced solenoid valve and test, ok.
Replaced defective torque limitor.
Checked and repaired capper  head #4.
Checked and rectified the missing signal of crates stopper.
Fix the bottle guide.
Jointed broken conveyor.
Replaced bottle picker.
Fix detached drive chain of conveyor.
Checked and repaired filler #3&8.
Checked and rectified bottle stopper.
Fix detached pin of filler rod to cylinder.
Checked and repaired air leakage and rectified hopper level sensor.
Repaired defective torque limiter.
Checked and provided lock pin for cylinder clevis.
Fix the cylinder lock for nozzle.
        """
    }
}

# -----------------------------
# DISPLAY SELECTED MACHINE DATA
# -----------------------------
if machine in history_data:
    st.subheader(f"Machine: {machine}")
    st.markdown(history_data[machine]["summary"])

    with st.expander("Show Raw Description of Work"):
        st.text(history_data[machine]["raw"])
else:
    st.info("Machine history not added yet. Please provide data.")
