
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import holidays

st.title("🔬 Lab Duty Scheduler with Holiday Skipping")

# User input for number of lab members
num_people = st.selectbox("Select number of lab members (2–8):", list(range(2, 9)), index=1)

# Name inputs
names = []
st.subheader("Enter names of lab members")
for i in range(num_people):
    name = st.text_input(f"Name {i+1}", key=f"name_{i}")
    if name:
        names.append(name)

# Task input
st.subheader("Add Additional Tasks (format: Task Name, Times per Week)")
default_tasks = ["Autoclave/Glassware"]
additional_input = st.text_area("Enter tasks (one per line):", "")
task_lines = [line.strip() for line in additional_input.splitlines() if line.strip()]
custom_tasks = []
for line in task_lines:
    try:
        task_name, freq = line.split(",")
        custom_tasks.append((task_name.strip(), int(freq.strip())))
    except:
        st.warning(f"Invalid format: {line}")

# Year and start date input
st.subheader("Schedule Settings")
selected_year = st.selectbox("Select year", [2025, 2026])
start_date = st.date_input("Select start date (Week 1 begins)", datetime(selected_year, 1, 1))
total_weeks = st.number_input("Enter total number of weeks", min_value=1, max_value=52, value=5)


# Ensure 5-week rotation
def rotate_list(lst, shift):
    return lst[shift:] + lst[:shift]

# Schedule generation logic with holiday skipping and custom task frequency
def generate_schedule(names, year, start_date, custom_tasks, total_weeks):
    schedule = []
    num = len(names)
    us_holidays = holidays.US(years=year)

    fixed_tasks = [
        ("Autoclave/Glassware", ["Mon", "Wed", "Thu", "Fri"])
    ]

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri"]

    for week in range(total_weeks):
        week_label = f"Week {week+1}"
        rot = rotate_list(names, week % num)

        for i, day in enumerate(weekdays):
            date = start_date + timedelta(days=week * 7 + i)
            if date in us_holidays:
                continue

            entry = {
                "Week": week_label,
                "Date": date.strftime("%Y-%m-%d"),
                "Day": day,
            }

            # Fixed tasks
            for task, days in fixed_tasks:
                if day in days:
                    entry[task] = ", ".join(rot[:2]) if day == "Mon" else rot[(i + 1) % num]
                else:
                    entry[task] = ""

            # Custom tasks by frequency
            for task_name, freq in custom_tasks:
                if freq >= 5 or i < freq:
                    entry[task_name] = rot[i % num]
                else:
                    entry[task_name] = ""

            schedule.append(entry)

    return pd.DataFrame(schedule)

# Generate and display schedule
if len(names) == num_people:
    df_schedule = generate_schedule(names, selected_year, start_date, custom_tasks, total_weeks)
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
