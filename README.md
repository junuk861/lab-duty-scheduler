🔬 Lab Duty Scheduler with Holiday Skipping
This Streamlit app is designed to automatically generate weekly lab duty schedules, rotating assignments among lab members while skipping U.S. federal holidays. It also supports adding custom tasks with flexible weekly frequencies.

🧩 Features
Dynamic Member Input: Choose the number of lab members (2–8) and input their names.

Custom Task Assignment: Add additional tasks (e.g., "Clean Sink, 2") with specified frequencies per week.

Automatic Rotation: Rotates responsibilities weekly to distribute workload fairly.

Holiday Awareness: Automatically skips U.S. holidays based on the selected start date.

Export to Excel: Download the final schedule as an .xlsx file for easy sharing or printing.

🛠️ How It Works
User Input Section

Choose the number of lab members using a dropdown.

Enter each member’s name in individual text fields.

Add extra tasks in the format:

arduino
Copy
Edit
Task Name, Times per Week
Schedule Configuration

Select a start date, which defines "Week 1".

Input the total number of weeks for the schedule.

Schedule Generation Logic

Uses a rotating list to evenly distribute duties week by week.

Built-in task "Autoclave/Glassware" is assigned to specific weekdays (Mon, Wed, Thu, Fri).

For each valid weekday:

If it's a U.S. holiday, that day is skipped.

Tasks are assigned to rotating members, respecting specified task frequencies.

Output

A preview of the full schedule is displayed as a DataFrame.

A downloadable Excel file (Lab_Duty_Schedule.xlsx) is generated using openpyxl.

📦 Dependencies
streamlit

pandas

holidays

openpyxl

Install requirements with:

bash
Copy
Edit
pip install streamlit pandas holidays openpyxl
🚀 Run the App
bash
Copy
Edit
streamlit run app.py
Replace app.py with your actual filename if different.

