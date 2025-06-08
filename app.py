
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import holidays

st.title("🔬 Lab Duty Scheduler with Holiday Skipping")

# User input for number of people
num_people = st.selectbox("Select number of lab members (3–5):", [3, 4, 5])

# Name inputs
names = []
st.subheader("Enter names of lab members")
for i in range(num_people):
    name = st.text_input(f"Name {i+1}", key=f"name_{i}")
    if name:
        names.append(name)

# Year and start date input
st.subheader("Schedule Settings")
selected_year = st.selectbox("Select year", [2025, 2026])
start_date = st.date_input("Select start date (Week 1 begins)", datetime(selected_year, 1, 1))

# Ensure 5-week rotation
def rotate_list(lst, shift):
    return lst[shift:] + lst[:shift]

# Schedule generation logic with holiday skipping
def generate_schedule(names, year, start_date):
    schedule = []
    num = len(names)
    us_holidays = holidays.US(years=year)

    for week in range(5):
        week_label = f"Week {week+1}"
        rot = rotate_list(names, week % num)

        # 요일별 날짜 계산
        week_days = {
            "Mon": start_date + timedelta(days=week * 7 + 0),
            "Wed": start_date + timedelta(days=week * 7 + 2),
            "Thu": start_date + timedelta(days=week * 7 + 3),
            "Fri": start_date + timedelta(days=week * 7 + 4),
        }

        for day, date in week_days.items():
            if date in us_holidays:
                continue  # 공휴일이면 건너뛰기

            if day == "Mon":
                auto = ", ".join(rot[:2])
                sink = ", ".join(rot[:2])
                ethanol = rot[2 % num]
            else:
                auto = rot[(["Wed", "Thu", "Fri"].index(day) + 2) % num]
                sink = ", ".join(rot[:2]) if day == "Fri" else ""
                ethanol = ""

            schedule.append({
                "Week": week_label,
                "Date": date.strftime("%Y-%m-%d"),
                "Day": day,
                "Autoclave/Glassware": auto,
                "Sink Cleaning (Tue/Fri)": sink,
                "70% Ethanol Prep (Mon only)": ethanol
            })

    return pd.DataFrame(schedule)

# Generate and display schedule
if len(names) == num_people:
    df_schedule = generate_schedule(names, selected_year, start_date)
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
