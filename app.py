
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("🔬 Lab Duty Scheduler")

# User input for number of people
num_people = st.selectbox("Select number of lab members (3–5):", [3, 4, 5])

# Name inputs
names = []
st.subheader("Enter names of lab members")
for i in range(num_people):
    name = st.text_input(f"Name {i+1}", key=f"name_{i}")
    if name:
        names.append(name)

# Ensure 5-week rotation
def rotate_list(lst, shift):
    return lst[shift:] + lst[:shift]

# Schedule generation logic
def generate_schedule(names):
    schedule = []
    num = len(names)
    for week in range(5):
        week_label = f"Week {week+1}"
        rot = rotate_list(names, week % num)

        # Assign autoclave/glassware
        monday = ", ".join(rot[:2])
        wed, thu, fri = rot[2 % num], rot[3 % num], rot[4 % num]

        # Sink cleaning (2 people)
        sink = ", ".join(rot[:2])

        # Ethanol (1 person)
        ethanol = rot[2 % num]

        # Create daily breakdown
        for day, auto in zip(["Mon", "Wed", "Thu", "Fri"], [rot[:2], [wed], [thu], [fri]]):
            schedule.append({
                "Week": week_label,
                "Day": day,
                "Autoclave/Glassware": ", ".join(auto),
                "Sink Cleaning (Tue/Fri)": sink if day in ["Tue", "Fri"] else "",
                "70% Ethanol Prep (Mon only)": ethanol if day == "Mon" else ""
            })

    return pd.DataFrame(schedule)

# Generate and display schedule
if len(names) == num_people:
    df_schedule = generate_schedule(names)
    st.success("Schedule generated successfully!")
    st.dataframe(df_schedule, use_container_width=True)

    # Download option
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_schedule.to_excel(writer, index=False, sheet_name="Lab Schedule")
    st.download_button(
        label="📥 Download Excel",
        data=output.getvalue(),
        file_name="Lab_Duty_Schedule.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
