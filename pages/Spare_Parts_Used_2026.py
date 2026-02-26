import streamlit as st

st.title("Spare Parts Used – Jan 1 to Feb 26, 2026")

SPARE_PARTS = {
    "CRATES AREA/LINE": [
        "1 pc cable",
        "1 pc new sprocket",
        "1 pc photo sensor",
        "1 pc sensor",
        "1 pc sensor & sensor cable",
        "1 unit motor",
        "2 pcs bearing",
        "3 meters plastic guide",
        "4 pcs 606 ball bearing",
        "4 pcs bearing",
        "As per IR 1129477",
        "Spare conveyor",
        "Spare conveyor 10 meters",
        "Spare sprocket"
    ],

    "M1": [
        "1 pc nozzle pin",
        "1 pc sensor & cable",
        "As per IR# 1106208",
        "Spare limiter"
    ],

    "M12": [
        "1 pc clevis",
        "1 pc multiflow",
        "1 pc sensor cable",
        "1 pc sprocket",
        "1 unit motor + gearbox",
        "4 meters air hose",
        "Repaired",
        "Spare micro valve"
    ],

    "M13": [
        "0.5 meter hose 6mm",
        "1 pc chain link",
        "1 pc cylinder",
        "1 pc pin",
        "Spare chuck",
        "Spare printer unit",
        "Spare transport guide"
    ],

    "M14": [
        "1 pc couple pad",
        "1 pc gauge",
        "1 pc holder",
        "1 pc micro switch",
        "1 pc multiflow",
        "1 pc sensor",
        "1 pc spring",
        "1 pc spring/finger (old)",
        "1 pc spring",
        "1 pc spring pad",
        "1 set finger",
        "2 pcs air regulator",
        "3 pcs solid state relay",
        "Spare guides",
        "Spare spring",
        "1 pc shaft manifold"
    ],

    "M15": [
        "1 pc cylinder",
        "1 pc encoder",
        "1 pc fuse",
        "1 pc multiflow",
        "1 pc new cylinder",
        "1 pc old spring",
        "1 pc sensor/cable",
        "2 pcs belt",
        "2 pcs fuse",
        "2 pcs hose fitting + 2 meters hose 8mm",
        "6 pcs capper fingers",
        "8 pcs filters",
        "Spare bushing, spring & fork",
        "Spare finger",
        "Spare fittings",
        "Spare fuse & cable",
        "Spare multiflow + 1 pc fuse",
        "Spare pivot bushing",
        "Spare plastic holder",
        "Spare spring/bushing"
    ],

    "M16": [
        "1 pc belt",
        "2 pcs bearing",
        "5 pcs belt",
        "Spare conveyor link"
    ],

    "M17": [
        "1 pc cable",
        "1 pc gasket",
        "1 pc locator",
        "1 pc multiflow and cable",
        "2 pcs chain lock",
        "2 pcs lock"
    ],

    "M18": [
        "1 pc multiflow and cable",
        "1 pc servo motor",
        "2 pcs lock pin",
        "5 meters hose #14",
        "5 meters 6mm hose",
        "Spare gasket",
        "Spare lock pin + 3 pcs locator",
        "Spare nozzle",
        "Spare shaft + spare locator"
    ],

    "M2": [
        "1 pc bearing",
        "1 pc holder",
        "1 pc micro valve switch",
        "1 pc sensor",
        "1 pc solenoid valve",
        "1 pc spare cylinder",
        "3 pcs suction head",
        "Spare torque limiter"
    ],

    "M3": [
        "1 pc contactor",
        "1 pc cylinder",
        "1 pc sensor",
        "1 pc sensor/cable + bracket",
        "1 pc solenoid valve",
        "1 pc spring",
        "1 pc toggle switch",
        "1 pc torque limiter",
        "1 pc transmission board",
        "3.5 meters toothed belt",
        "Sensor and cable"
    ],

    "M4": [
        "1 pc cylinder",
        "1 pc photo cell",
        "1 pc photo sensor",
        "1 pc sensor",
        "1 pc sensor + cable",
        "1 pc solenoid valve",
        "1 pc throttle valve + 2 pcs fitting",
        "2 pcs belt",
        "Old coupling",
        "Old torque limiter",
        "Spare air hose"
    ],

    "M5": [
        "1 pc shaft seal"
    ],

    "M6": [
        "1 pc 7A fuse + 1 pc MAC solenoid valve",
        "1 pc bearing",
        "1 pc cable + 1 pc sensor",
        "1 pc MAC solenoid valve",
        "1 pc nozzle pin",
        "1 pc relay",
        "1 pc spring",
        "1 pc toothed belt",
        "1 set finger cam",
        "2 pcs ball bearing",
        "2 pcs bearing + 1 set epoxy steel",
        "2 pcs conveyor links",
        "Spare chuck",
        "Spare crank shaft",
        "Spare finger cams",
        "Spare gripper rubber pads",
        "Spare micro valve switch",
        "Spare solenoid valve"
    ],

    "M7": [
        "1 pc filler gasket",
        "1 pc key bar",
        "1 pc MAC solenoid",
        "1 pc new scale",
        "1 pc old sensor",
        "1 pc rubber suction cup",
        "1 pc Siemens Micromaster 420",
        "1 pc spare suction",
        "1 pc suction cup",
        "1 pc TES+ card",
        "1 pc transformer",
        "15 meters Profibus cable",
        "2 pcs rubber cup",
        "2 pcs spring",
        "2 pcs suction cup",
        "2 sets fingers",
        "3 pcs rubber suction cup",
        "3 pcs vacuum cups",
        "3 sets finger cam",
        "5 pcs suction cup",
        "6 pcs finger cam",
        "Finger cam set",
        "Spare crank shaft",
        "Spare micro valve",
        "Spare Siemens drive",
        "Spare suction cup"
    ],

    "M8": [
        "1 pc magnetic sensor",
        "1 seal kit",
        "2 pcs bearing 33018 (IR#1102737)",
        "2 pcs hose clamp",
        "3 pcs sensors",
        "9 pcs finger cam"
    ],

    "M9": []
}

machine = st.selectbox("Select Machine", sorted(SPARE_PARTS.keys()))

st.subheader(f"Machine: {machine}")

parts = SPARE_PARTS[machine]

if not parts:
    st.info("No spare parts recorded for this machine.")
else:
    for item in parts:
        st.markdown(f"- {item}")

st.markdown("---")
st.caption("Spare parts usage extracted from maintenance log sheets (Jan–Feb 2026).")
