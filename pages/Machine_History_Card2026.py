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
    "M4": """
    M4 – MACHINE HISTORY
Mechanical Adjustments & Timing Corrections
•	Adjusted and increased crates lifter sledge opening; balanced crates lifter height and fabricated new sledge stopper.
•	Adjusted starwheel timing and corrected timing drift across bottle handling sections.
•	Adjusted filler cylinder shaft to prevent product leakage.
•	Adjusted capper torque pressure and torque settings for capper #2 and #3.
•	Zeroed encoder position multiple times after timing issues and reset stacker faults.
Crates, Pusher & Material Handling
•	Checked and adjusted crates pusher cylinder rod end; replaced broken crates position sensor.
•	Repaired crates pusher assembly and corrected alignment.
•	Fixed detached crates C‑loop pusher cylinder rod end.
•	Regulated crates pusher air cushioner for smoother operation.
•	Repositioned upper crates lifter limit switch and cleared system fault.
•	Rebalanced crates lifter and reset alarms.
Capper, Filler & Bottle Handling Systems
•	Repaired capper head #3; replaced gripper bolts and tightened gripper screws for heads #3, #4, and #6.
•	Repaired cap applicator and cap picker alignment.
•	Replaced damaged cap dispenser bolt and corrected dispenser alignment.
•	Replaced defective spindle and torque limiter (using old spare).
•	Identified torque limiter requiring replacement; temporary adjustments applied.
•	Fixed loose cap gripper and lubricated assembly.
Sensors, Electrical & Control System
•	Checked and rectified divider limit sensor and divider unit sensor.
•	Cleaned and serviced divider servo motor drive; reset servo faults.
•	Cleaned servo driver, reinstalled, and performed manual homing.
•	Repaired encoder coupling and replaced broken encoder coupling.
•	Reset faulty drive, inverter faults, VLT faults, and stacker PLC faults.
•	Troubleshot missing crates lifter signal and corrected encoder coupling.
•	Replaced defective bottle counter sensor and divider homing sensor.
•	Installed new photo sensor and restored detection accuracy.
•	Repaired shorted sensor cable for bottle counter and replaced with new cable.
Conveyor, Gear & Mechanical Repairs
•	Aligned drive sprocket and corrected conveyor belt alignment.
•	Fixed damaged conveyor sections and packer crates conveyor.
•	Removed damaged conveyor links and reconnected conveyor.
•	Repaired labeller servo drive sprocket and loose drive gear.
•	Repaired servo motor drive pulley and restored proper rotation.
•	Removed carriage plate, welded broken parts, and reinstalled.
•	Repaired broken water pipe and replaced damaged filler belt.
Pneumatics & Air System
•	Fixed multiple air leakages and replaced damaged air hoses.
•	Installed air control valve for unitizer crates pusher.
•	Lubricated solenoid valves and spray ball valve; verified spray ball operation.
•	Repaired pusher cylinder and welded crates platform.
General Maintenance & Restorations
•	Cleaned servo drives, removed excess ink, and restored print quality.
•	Checked and opened product valve; verified normal operation.
•	Tightened capper jaw screws and cap gripper bolts.
•	Repaired coupling of encoder due to lack of spare; temporary fix applied.
•	Performed system resets after mechanical or electrical corrections.
•	Continued work on drive gear assembly, secured wiring, added gear oil, and tested.
 

    
    """,
    "M5": """
    no in use
    """,
    "M6": """
        M6 – MACHINE HISTORY
Mechanical Adjustments & Timing Corrections
•	Adjusted and aligned capper center starwheel, capper heads (#1, #4, #5, #8), and filler exit starwheel.
•	Adjusted starwheel timing, transfer starwheel, and corrected timing drift across bottle handling sections.
•	Adjusted film sensor for cutting and aligned film sensor assembly.
•	Adjusted infeed screw drive gear mounting and corrected alignment.
•	Performed dynamic calibration and static scale calibration.
•	Zeroed machine position after timing corrections and mechanical resets.
Capper, Filler & Bottle Handling Systems
•	Repaired capper #1 and capper head #1; replaced finger cams and capper fingers using available spares.
•	Replaced set of capper chucks and tightened capper jaw screws.
•	Corrected loose capping issues and adjusted capping head alignment.
•	Repaired bottle funnel guide, replaced broken funnel lock, and welded bottle funnel.
•	Repaired bottle elevator issues and released stuck elevator.
•	Repaired bottle holder and damaged scale plate; aligned bent starwheel guide after bottle impact.
Sensors, Electrical & Control System
•	Checked and rectified bottle line sensor faults; reset system alarms.
•	Replaced damaged micro valve switch, defective relay for elevator stop, and faulty solenoid valves.
•	Replaced cable and sensor assemblies; further inspection required after production.
•	Cleaned hardened ink from printer head gutter and restored print quality.
•	Replaced printer unit with Citronix printer.
•	Reset faults for VLT, servo drivers, and general machine alarms.
Conveyor, Film & Material Handling
•	Aligned outfeed belt of vacuum conveyor and repaired broken outfeed plastic conveyor.
•	Repaired heating tunnel conveyor guide railings and heating tunnel curtain.
•	Repaired stuck overhead conveyor and replaced damaged links.
•	Removed derailed rubber chain conveyor, replaced damaged rubber, and reduced one link.
•	Repaired cutting clutch and corrected cutting issues.
•	Opened film cutter drive, repaired, reinstalled, and retimed.
•	Reduced link of steam conveyor and restored smooth movement.
Pneumatics & Air System
•	Repaired air leakages and replaced damaged air hoses, including bottle rejector hose.
•	Lubricated product valve and capper assembly shafts.
•	Adjusted carton loading cylinders due to low air pressure.
•	Repaired stuck bottle elevator and restored pneumatic actuation.
Component Replacement
•	Replaced Axon film post shaft bearing (bottom side).
•	Replaced broken nozzle pin and crank shaft (due to excessive wear).
•	Replaced damaged piston spring and installed replacement finger using old spare.
•	Replaced damaged rubber gripper, damaged spring, and worn-out cap sorter drive belt (modified spare installed).
•	Replaced damaged link of S/S conveyor and broken shaft pin at bottle funnel.
•	Replaced solenoid valve and calibrated system.
•	Replaced filling sensor and adjusted infeed starwheel timing.
•	Replaced cap conveyor roller bearings and tensioned tightening belt.
General Maintenance & Restorations
•	Cleaned and aligned print jet; removed stuck bottles and restored bottle flow.
•	Fixed HMI mounting and restored operator interface stability.
•	Fixed bottle guide lock and restored proper bottle handling.
•	Reset faults after mechanical or electrical corrections.
•	Performed lubrication, alignment, and routine mechanical corrections across assemblies.

    """,
    "M7": """
    Not in use
    """,
    "M8": """
M8 – MACHINE HISTORY
Mechanical Adjustments & Bottle Handling
•	Adjusted bottle guides to correct Arnon bottle quality issues and restored smooth bottle flow.
•	Aligned scale bottle holder and corrected bottle chute alignment after repeated bottle jamming.
•	Adjusted crates guide and crates stopper, including crates divider guide toward stacker #2.
•	Installed back crates lifter cylinder rod guide and secured bottle guide locks.
Capper, Filler & Bottle Handling Systems
•	Repaired capper #5 and replaced worn or broken fingers (#2 & #3).
•	Repaired loosened bottle gate and cylinder; fixed nozzle #15 and released stuck filler nozzle.
•	Replaced broken filler rod and welded broken filler piston part before reinstalling.
•	Repaired stacker #2 crates holder cylinder and crates holder mounting.
Sensors, Electrical & Control System
•	Replaced malfunctioning cylinder sensor, busted magnetic sensor, and pusher main cylinder sensor.
•	Reset bottle divider fault, servo drive faults, stepper drive faults, and communication faults.
•	Cleaned and reset divider servo drive, PLC module, and machine modules to clear position errors.
•	Zeroed machine position after sensor resets and encoder corrections.
•	Replaced defective drive sprocket (temporary fix due to no spare available).
•	Replaced valve kit due to strong leakage.
•	Reset tripped breaker and restored power continuity.
Conveyor, Crates & Material Handling
•	Fixed broken overhead conveyor and broken crates conveyor.
•	Repaired conveyor motor and corrected mounting issues.
•	Fixed loose bolt of crates squeezer and secured crates stopper mounting.
•	Removed defective drive sprocket and temporarily repaired until spare becomes available.
Pneumatics & Air System
•	Repaired multiple air leakages and replaced damaged air hoses, including gate unlock hose.
•	Replaced leaking air hose and reconnected cut hoses.
•	Repaired loosened bottle gate cylinder and restored pneumatic actuation.
Multiflow, Valves & Fluid Systems
•	Replaced busted magnetic sensor and pusher cylinder sensor.
•	Replaced valve kit due to leakage and restored sealing.
•	Repaired and cleaned multiflow components; removed clogged rubber from multiflow.
•	Repaired nozzle cylinder and restored proper dispensing.
Servo, Stepper & Drive Systems
•	Rectified servo stepper drive faults and cleaned servo drive assemblies.
•	Reset servo drive faults and restored normal operation.
•	Repaired divider drive fault and restored synchronization.
•	Cleaned filling carbon brushes and collectors to correct intermittent drive issues.
Structural, Fabrication & Welding
•	Welded bottle slider table and stacker guide.
•	Welded broken filler piston part and reinstalled after production.
•	Repaired crates holder mounting and reinforced structural components.
Component Replacement
•	Replaced broken filler rod, broken lock pin, and broken drive sprocket (temporary fix).
•	Replaced busted magnetic sensor and pusher cylinder sensor.
•	Replaced worn suction cups, rubber cups, and vacuum cups.
•	Replaced valve kit, gate air hose, and damaged air hoses.
•	Replaced finger #2 & #3 and cleaned piston assembly #7.
General Maintenance & Restorations
•	Cleaned sensors, modules, servo drives, and PLC modules.
•	Cleaned carbon brushes and collectors.
•	Reset multiple system faults after mechanical or electrical corrections.
•	Fixed loose bolts, restored conveyor alignment, and corrected bottle guide issues.
•	Disabled station #17 during milk production; repaired filler piston and reinstalled after production.

    """,
    "M9": """
M9 – MACHINE HISTORY
Sensors, Guides & Alignment
•	Checked and aligned sensors and guides of stacker #1 to restore proper detection and bottle/crate flow.
•	Fine‑tuned motor brake of stacker #3 and ensured smooth stopping accuracy.
•	Adjusted and aligned bottle and crate guides to eliminate misalignment issues.
Electrical, Control & System Reset
•	Replaced defective sensor and cleaned all push‑button switches to restore reliable operation.
•	Cleaned all electronic modules and performed full system reset to clear accumulated faults.
•	Reset bottle divider and stacker faults after troubleshooting.
Pneumatics & Lubrication
•	Lubricated pneumatic lines of stacker #3 to improve actuator response and reduce friction.
Printing System
•	Set up two printer units (yellow and black ink) and configured them for production use.

    """,
    "M10": """
    Not in use
    """,
    "M11": """
    Not in use
    """,
    "M12": """
    Not in use
    """,
    "M13": """
M13 – MACHINE HISTORY
•	Adjusted chain pusher alignment, carton alignment, and machine homing position.
•	Adjusted chain packer alignment and corrected timing issues.
•	Adjusted and aligned sensors for proper detection.
•	Fine‑tuned printer settings and cleaned inkjet printhead.
•	Cleaned vacuum generator on both sides to improve suction performance.
•	Cleaned glue nozzle and secured solenoid valve socket.
•	Replaced damaged air hose and restored pneumatic connections.
•	Replaced motor #3 and configured motor parameters; machine monitoring confirmed OK.
•	Retimed carton chain pusher and carton forming chain.
•	Corrected pusher sensor alignment to eliminate false activation.
•	Released air lock in pneumatic system and restored operation.
•	Cleaned and serviced inkjet system for print quality improvement.
•	Adjusted pallet conveyor speed for stable pallet movement.
•	Repaired water leakage at union coupling.
•	Performed full machine timing correction; reset all timing points to zero and manually aligned all mechanisms.
•	Performed scale calibration and dynamic calibration.
•	Released air lock of pump and restored product flow.
•	Removed pallet manually to clear jam and reset system.
•	Repaired Lanfranchi bottle guide and restored bottle flow.
•	Repaired bottle gate; replaced detached bolt and hose fitting.
•	Replaced broken bottom plate pin and cleaned bottom plate assembly.
•	Replaced broken carton bar chain pin and retimed carton forming chain.
•	Replaced damaged bottle stopper cylinder and restored operation.
•	Replaced damaged cylinder hose fitting.
•	Replaced positive chuck assembly.
•	Replaced printer with spare due to persistent poor printing.
•	Replaced transport guide in curve area to eliminate bottle jamming.
•	Reset palletizer fault, barrier fault, VFD fault, and WAGO defect.
•	Troubleshot product pusher malfunction and turned over remaining work to night shift.
•	Noted absence of operator during troubleshooting events.

    """,
    "M14": """
M14 – MACHINE HISTORY
Mechanical Adjustments & Timing Corrections
•	Adjusted bottle screw timing, bottle guides, intermediate infeed screw, and overall bottle handling alignment.
•	Corrected timing of bottle screw, starwheel, separation bar, and tray feeding chain.
•	Adjusted Promec height, starwheel-to-filler alignment, and bottle holder alignment.
•	Adjusted opening of air‑conveyor bottle‑neck guides and corrected Lanfranchi bottle guide alignment.
•	Set machine to zero position multiple times after timing drift or mechanical obstruction.
•	Performed homing adjustments after clearing jams or mechanical resets.
Capper, Filler & Capping System Work
•	Aligned capper head and adjusted air pressure for capping.
•	Repaired capper #1, #4, #6, and #13 assemblies.
•	Replaced capper head fingers and micro‑switches; interchanged capper chucks as needed.
•	Fine‑tuned air pressure for cap holding and tightening.
•	Repaired cap holder assembly and replaced broken springs, holders, and pivot components.
Sensor, Electrical & Control System Corrections
•	Adjusted filling sensor sensitivity and corrected sensor alignment across multiple stations.
•	Reset sequence faults, conveyor system faults, head safety faults, temperature faults, and VLT/VFD alarms.
•	Troubleshot and replaced defective solid‑state relays, micro switches, and malfunctioning sensors.
•	Repaired head safety sensor and corrected air‑valve activation signal.
•	Rewired stacker safety relay reset circuit after electrical fault.
•	Checked and corrected encoder belt alignment; replaced encoder bearing due to water ingress.
•	Reset Sipac downline electrical circuits after power fluctuation.
Pneumatics & Air System Repairs
•	Fixed multiple air leakages, replaced damaged hoses, fittings, and leaking cylinders.
•	Repaired micro‑valve assemblies and replaced broken bolts and fittings.
•	Replaced air control regulator for carton folder cylinder.
•	Released air locks in pneumatic lines and restored normal operation.
Conveyor, Bottle Flow & Handling Repairs
•	Repaired bottle holders, replaced broken springs, and corrected bottle holder alignment.
•	Repaired bottle gate, bottle screw coupling, and replaced damaged pins.
•	Cleared clogged bottles at funnel and restored conveyor safety sensor activation.
•	Repaired Promec drier bottle holder and corrected outfeed starwheel alignment.
•	Released stuck conveyors, reconnected conveyor links, and restored bottle flow.
•	Repaired infeed bottle gate and corrected pusher chain issues.
Glue, Printing & Labeling System Work
•	Cleaned and adjusted glue nozzle; rectified glue application issues.
•	Cleaned printhead, adjusted printing parameters, and aligned inkjet system.
•	Replaced malfunctioning printer with standby unit; replaced laminar pre‑filters.
•	Adjusted printer sensor sensitivity and corrected message display issues.
Filler, Rinser & Temperature System
•	Lubricated filler carousel and reduced machine speed for stability.
•	Replaced broken bottom plate springs and damaged holders.
•	Corrected rinser temperature fault and adjusted return valve spring.
•	Replaced damaged steam gauge with new pressure gauge.
Multiflow & Valve System
•	Replaced busted multiflow units, coils, and cables; cleaned sockets and calibrated stations.
•	Manually cycled valves and restored washing mode after malfunction.
Structural, Fabrication & Welding Work
•	Welded broken crates stopper cylinder holder and repaired structural components.
•	Repaired middle bottle screw and secured loose mounting hardware.
•	Replaced damaged transport plastic guide and bottle gripper components.
Calibration & System Reset
•	Performed zeroing of scales and dynamic calibration.
•	Reset machine position after timing corrections and mechanical resets.
•	Reset multiple system alarms including servo driver, orientator conveyor, and safety faults.

    """,
    "M15": """
M15 – MACHINE HISTORY
Mechanical Adjustments & Timing Corrections
•	Adjusted bottle gate #1 and #2, bottle infeed screw, bottle separator belt, and bottle guides.
•	Adjusted orientator exit conveyor belt and mat conveyor tensioner.
•	Adjusted cylinder stroke and installed spacer for bottle gate alignment.
•	Aligned bottle holders to starwheel and corrected bottle funnel swing angle plate.
•	Zeroed machine position after timing drift or mechanical resets.
•	Performed full dynamic scale calibration.
Capping, Filling & Bottle Handling Systems
•	Adjusted air pressure for capping and fine‑tuned torque and holding air regulators.
•	Repaired capper #2 and replaced cap holder fingers.
•	Repaired cap holder assembly and corrected misalignment.
•	Repaired bottle elevator safety actuator and safety sensor; released stuck elevator and reset faults.
•	Repaired bottle stopper and replaced damaged stopper cylinder shaft bolt.
•	Replaced broken bottle holder bushings, plastic grippers, and springs.
Sensors, Electrical & Control System
•	Installed sensor mirror to activate table conveyor flag sensor.
•	Adjusted printer sensor sensitivity and corrected message parameters.
•	Checked and rectified safety sensor faults, stacker limit sensor faults, and missing sensor feedback signals.
•	Reset servo drive faults, VLT faults, orientator servo faults, door safety faults, and general machine faults.
•	Rewired stacker #1 safety relay reset circuit after electrical malfunction.
•	Replaced defective sensor cables for drain pad and other detection points.
•	Reset Sipac downline electrical circuits after power fluctuation.
Conveyor, Crates & Material Handling
•	Repaired outfeed conveyor of stacker #1 and restored belt tracking.
•	Repaired broken crates feeding conveyor and reconnected broken crates conveyor.
•	Repaired belt damage and applied adhesive reinforcement.
•	Replaced damaged belts in orientator and outfeed areas using available spares.
•	Removed rolled plastic from outfeed mesh conveyor roller and restored operation.
Pneumatics & Air System
•	Fixed multiple air leakages and replaced damaged hoses, fittings, and leaking cylinders.
•	Lubricated cylinders, stopper cylinders, and solenoid valve air lines.
•	Filled lubrication oil for packer bottle stopper solenoid valve.
•	Repaired cylinder #3 gate stopper and replaced defective cylinders with new units.
Multiflow, Valves & Fluid Systems
•	Checked multiflow units, replaced grounded cables, busted card fuses, and defective coils.
•	Replaced multiflow coil at station #35 and cleaned socket plugs for stations #6 and #20.
•	Checked valve conditions for product leakage; no issues found.
Printing & Inkjet System
•	Adjusted ink and printer parameters; cleaned and aligned print jet.
•	Replaced malfunctioning printer with standby unit and installed printer from M7 when required.
•	Printer marked for replacement due to recurring issues.
Glue System
•	Cleaned glue nozzles and corrected glue application issues.
•	Adjusted glue nozzle position and secured solenoid valve socket.
Structural, Fabrication & Welding
•	Welded broken crates stopper cylinder holder.
•	Repaired defective funnel and corrected bottle funnel clogging during CIP.
General Maintenance & Restorations
•	Added make‑up solution to correct viscosity.
•	Insulated bottle orientator outfeed belt and tightened cylinder stopper bolts.
•	Fixed conveyor issues and restored smooth movement.
•	Fixed air blower for bottle printing.
•	Repaired air leakage for capper #5.
•	Replaced laminar flow filters.
•	Replaced TES+ card fuse for stations #19 & #20 and restored multiflow circuit.
•	Reset full line crates sensor and restored detection accuracy.

    """,
    "M16": """
    M16 – MACHINE HISTORY
Mechanical Adjustments & Timing Corrections
•	Adjusted bottle screw timing and infeed screw timing to correct bottle flow.
•	Adjusted capper belt tension and fine‑tuned torque pressure for stable capping.
•	Retimed bottle screw guide and corrected cap chute guide alignment.
•	Adjusted plastic roller presser and restored proper pressure settings.
Capper, Valve & Capping System Work
•	Checked and adjusted air pressure for capping operation.
•	Rectified issues on capper #1 and #2, including alignment and torque correction.
•	Replaced broken bearing of capper belt roller.
•	Repaired leaking nozzle #17 and verified sealing performance.
Sensor, Electrical & Control System
•	Aligned pallet wrapper safety barrier sensor and restored safety circuit.
•	Rectified valve faults, glue tank faults, and CIP system faults.
•	Reset VFD faults and general machine faults after troubleshooting.
•	Monitored CIP system operation until completion and restarted CIP cycle when required.
Glue System & Heating/Cooling
•	Cleaned glue nozzles and corrected glue application issues.
•	Replaced damaged plastic cutting drive and restored glue nozzle performance.
•	Cooled down hot‑flush line and corrected cooling step issues.
•	Performed temperature cooldown to transfer cooling to drain system.
Conveyor, Film & Bottle Handling Repairs
•	Repaired bottle gate stopper and restored proper actuation.
•	Removed rolled plastic from outfeed mesh conveyor roller and reinstalled cleaned roller.
•	Repaired stuck film roller and restored smooth film movement.
•	Replaced broken film rise belt and repaired film rise table conveyor during CIP.
•	Replaced broken packer outfeed plastic conveyor and reinstalled assembly.
•	Mounted missing belt on roller, cleaned glue nozzle, adjusted guides, and performed homing.
Pneumatics & Cylinder Work
•	Repaired passage cylinder guide and restored alignment.
•	Fixed air leakage issues and restored pneumatic pressure stability.
General Maintenance & Restorations
•	Checked and rectified glue issues and valve faults.
•	Checked cause of hot‑flush issue and corrected cooling sequence.
•	Cleaned glue nozzles and performed routine nozzle maintenance.
•	Reset machine faults after mechanical or electrical corrections

    """,
   "M17": """
M17 – MACHINE HISTORY
Mechanical Adjustments & Timing Corrections
•	Aligned bottle exit starwheel to guide and corrected bottle entry alignment at rinser holders #10 and #25.
•	Adjusted bottle rejector exit conveyor guide to reduce bottle downing; machine speed temporarily reduced to 180 ppm.
•	Adjusted bottle rejector safety alignment and corrected bottle stopper looseness.
•	Set machine to zero position and synchronized timing after mechanical resets.
Capping, Filling & Bottle Handling Systems
•	Aligned and adjusted bottle filling sensor and corrected sensitivity settings.
•	Repaired capper #5 and #6 assemblies and replaced locator plate for capper #1 using available spare.
•	Removed clogged caps from cap conveyor and restored cap flow.
•	Repaired bottle holder #10 and replaced broken roller shaft and bottle‑neck locator using old spare.
•	Replaced worn‑out gasket and restored sealing performance.
Sensors, Electrical & Control System
•	Adjusted sensor sensitivity and rectified faulty sensor signals.
•	Repaired sensor connections and replaced defective sensor cables for valves and detection points.
•	Fixed door safety switch connection and restored safety circuit.
•	Disabled station #14 for post‑production inspection.
•	Reset machine faults after troubleshooting and restored missing sensor feedback signals.
Conveyor, Pusher & Material Handling
•	Repaired conveyor sections and corrected alignment issues.
•	Released stuck carton pusher, replaced broken chain lock, and straightened bent pusher plate.
•	Removed rolled plastic from outfeed mesh conveyor roller and reinstalled cleaned roller.
•	Repaired bottle entry alignment at rinser and corrected bottle flow issues.
Pneumatics & Air System
•	Eliminated air hose leakages and repaired leaking air lines.
•	Repaired air leakage in multiple stations and restored pneumatic pressure stability.
•	Replaced damaged air hose and fittings for station #7.
Multiflow, Valves & Fluid Systems
•	Opened clogged multiflow and removed rubber obstruction.
•	Repaired detached nozzle tip of multiflow and restored flow accuracy.
•	Replaced filler multiflow coil using repaired spare and calibrated system.
•	Replaced cable and multiflow assembly, followed by calibration.
•	Rectified valve 19V24 and restored proper operation.
Printing & Inkjet System
•	Adjusted print parameters and cleaned/aligned printhead to correct bad printing.
•	Performed nozzle cleaning due to ink misalignment with gutter.
•	Adjusted printer settings after parameter replacement.
Structural, Fabrication & Welding
•	Replaced broken angle support and shaft.
•	Replaced broken lock for bottle swing stopper.
•	Performed welding repairs on structural components as required.
General Maintenance & Restorations
•	Repaired glue system issues and corrected glue application.
•	Repaired air leakage and restored pneumatic stability.
•	Repaired and aligned cap holder and allocator.
•	Replaced worn or damaged components including bottle locator, springs, and gaskets.
•	Set machine to zero position and synchronized system after major adjustments

    """,
    "M18": """
M18 – MACHINE HISTORY
Mechanical Adjustments & Timing Corrections
•	Adjusted timing of infeed bottle screw and bottle screw guide; corrected synchronization issues.
•	Adjusted separation bar, bottle guide, locator alignment, and infeed screw alignment.
•	Zeroed machine position after timing drift and restored synchronization.
•	Corrected bottle holder alignment and replaced fork for juice line; secured locking mechanism.
Capping, Filling & Bottle Handling Systems
•	Aligned cap dispenser and corrected capper lock issues.
•	Identified multiple damaged bottle‑neck locators requiring replacement; several stations temporarily disabled due to no spare availability.
•	Repaired bottle stopper and corrected loose capping issues.
•	Replaced broken bottle holder and broken lock pin using fabricated spare.
•	Repaired damaged angle support at station #14 and replaced neck locators for capper heads #8, #10, and #11.
•	Replaced broken capper bottle stopper fork.
Sensors, Electrical & Control System
•	Activated soda level probe signal.
•	Adjusted sensor sensitivity and rectified faulty sensor signals.
•	Repaired sensor connections and replaced defective sensor cables.
•	Disabled stations with defective locators pending spare availability.
•	Reset CIP plant and corrected tank emptying valve settings.
•	Set up Imaje printer due to solvent shortage for Leibinger unit.
Conveyor, Pusher & Material Handling
•	Checked and aligned carton conveyor guide.
•	Repaired plastic roller and replaced damaged plastic cutter.
•	Released stuck carton pusher, replaced broken chain lock, and straightened bent pusher plate.
•	Repaired bottle entry alignment at rinser and corrected bottle flow issues.
Pneumatics & Air System
•	Repaired multiple air leakages and replaced damaged air hoses and fittings.
•	Rectified air leakage in pallet wrapper air supply.
•	Replaced leaking air hose and secured connections with cable ties.
Multiflow, Valves & Fluid Systems
•	Found broken multiflow pin; scheduled replacement after production.
•	Repaired detached multiflow nozzle tip and restored flow accuracy.
•	Replaced defective multiflow and cable; calibrated system.
•	Replaced filler multiflow coil using repaired spare.
•	Cleaned and drained glue nozzle hose; removed blockages.
•	Replaced acid pump exhaust pipe union gasket.
Printing & Inkjet System
•	Adjusted printer parameters and cleaned inkjet head.
•	Performed ink‑line cleaning and restarted inkjet system.
•	Replaced printer unit with Imaje due to Leibinger viscosity motor fault; later reinstalled Leibinger unit and tested.
•	Set up black Imaje printer due to solvent shortage.
Structural, Fabrication & Welding
•	Repaired damaged angle support and replaced broken shaft.
•	Repaired bottle stopper and reinforced locking components.
General Maintenance & Restorations
•	Changed gasket and replaced worn‑out gaskets where required.
•	Removed clogged caps from cap conveyor.
•	Repaired damaged plastic cutter and restored cutting performance.
•	Performed retiming of infeed bottle screw and corrected capper lock.
•	Noted need to replace bottle‑neck locators and allocator; no spare available.
•	Noted need to top‑up make‑up solution; stock unavailable

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
