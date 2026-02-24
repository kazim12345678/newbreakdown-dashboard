import streamlit as st

st.set_page_config(page_title="Machine History Card", layout="wide")

st.title("Machine History Card (MHC)")

# -----------------------------
# MACHINE SELECTION
# -----------------------------
machines = ["M1", "M2"]
machine = st.selectbox("Select Machine", machines)

st.markdown("---")

# -----------------------------
# MACHINE HISTORY DATA
# -----------------------------
history_data = {

    "M1": {
        "summary": """
### **M1 – Machine History Summary**

#### **Capping System**
- Multiple capper head alignments and timing adjustments.
- Repaired/replaced capper fingers, finger cams, cap holder assemblies, and capper piston springs.
- Adjusted torque limiter, torque pressure, and starwheel timing (#5 and outfeed).
- Repaired cap dispenser, cap chute, cap applicator, and bottle stopper guides.
- Installed and lubricated solenoid valves for capper operations.
- Replaced torque limiters (multiple instances).
- Corrected capper #1 issues and retimed capper assemblies.

#### **Sensors & Electrical**
- Replaced defective sensors, cables, and crates gate sensors.
- Reset stacker faults and breaker trips.
- Replaced magnetic contactor and fixed shorted motor cable.
- Cleaned and lubricated solenoid valves; fixed air leaks.
- Repaired TES net card communication and downloaded program.
- Replaced stacker door switch and bottle stopper cylinder bracket.

#### **Conveyors & Mechanical**
- Repaired broken conveyors, damaged links, sprockets, and derailed outfeed conveyors.
- Reconnected packer crates conveyor and fixed crates lifter plate.
- Aligned drive sprocket and adjusted conveyor belts.
- Welded broken carriage plate parts and reinstalled.
- Repaired C‑loop pusher and packer crates conveyor.

#### **Filler & Bottle Handling**
- Repaired nozzle leakage and removed clogged gasket.
- Checked and replaced filler pistons and adjusted cylinder rods.
- Fixed bottle stopper and bottle sensor alignment.

#### **General Maintenance**
- Cleaned carbon brushes, adjusted brush length, and reinstalled collectors.
- Fixed air hose leaks and replaced hose fittings.
- Reset multiple faults (stacker, capper, general).
- Attempted VFD installation (drive failed; pending rectification).
- Installed back detached mechanical components (rollers, brackets, cylinders).
        """,

        "raw": """
"to be updated"
"to be updated"
Make solution on the side of pulley due to adjustment already touch on the plate, removed the side of plate to adjust the tension.
Need to replace finger.
Reconnected packer crates conveyor.
Done tensioning of bottle cable conveyor.
"to be updated"
Repaired the broken conveyor.
Replaced defective crates gate sensor.
Alligned bottle sensor.
Reset crates stacker fault.
Checked and need to replace finger cam but no spare available.
Make remedy on the cap holder finger, no spare finger cam.
Adjusted the conveyor belt.
Fix plastic guide and installed back derailed outfeed conveyor.
Repaired nozzle leakage, removed clogged gasket.
Adjusted the sensor.
Fix the crates lifter plate.
Replaced damaged hose fitting of stopper cylinder.
Checked and replaced solenoid valve using old spare.
Checked and lubricated all solenoid valve.
Fix air leakage.
Adjusted the timing of starwheel #5.
Fix the air leakage.
Lubricated the solenoid valve for bottle stopper.
Checked and replaced damaged cable sensor.
Removed damaged link then reconnected conveyor.
Alligned the drive sprocket.
Replaced torque limitor.
Replaced torque limitor.
Tried to install VFD to reduce speed of conveyor but faiield to run drive, for rectifiecation.
Replaced defective sensor.
Replaced defective stacker door switch.
Replaced cut stacker left side lifting belt.
Checked and installed back detached crates pusher and replaced busted sensor.
Checked and repaired labelling machine.
Fix damaged conveyor.
Fix damaged packer crates conveyor.
Adjusted the divider sensor to activate.
Repaired cap holder assembly.
Removed carriage plate and bring to workshop to weld broken part, fix back.
Checked and reset stacker fault.
Cleaned carbon brushes and adjusted the carbon brushes length.
Replaced worn out capper piston spring.
Fix air leakage.
Work continuation, installed back detached/fell down carbon brushes and collectors assembly.
Checked and cleaned carbon brushes.
Checked and repaired packer bottle stopper.
Checked and found motor overload of cap elevator, checked the motor condition, secured connection of the motor.
Reset the breaker.
Replaced the magnetic contactor.
Reset the breaker.
Fix the shorted wire of motor cable.
Troubleshoot the cause of not filling all station, checked carbon brushes & communication cables then cleaned, change also TES net card, downloaded program and test.
Replaced defective sensor and cable.
Done fix air hose.
Adjusted the timing of starwheel.
Replaced the printer by spare printer from M9 due to pressure fault.
Replaced sensor cable and sensor, also bracker of cylinder for bottle stopper.
Fix the detached cylinder end of carriage.
Checked and retiming outfeed starwheel.
Checked and installed back detached roller bracket.
Repaired c-loop pusher.
        """
    },

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
    st.info("Machine history not added yet.")
