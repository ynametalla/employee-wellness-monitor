
import pandas as pd
from datetime import timedelta

# === Load Data ===
file_path = "SDG 3 - Data.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by=['Employee_ID', 'Date'], inplace=True)

# === Summary Table (Full Period) ===
summary_df = df.groupby(['Employee_ID', 'Employee_Name']).agg({
    'Hours_Worked': 'mean',
    'Emails_Sent': 'mean',
    'Breaks_Per_Day': 'mean'
}).reset_index()
summary_df.columns = ['Employee_ID', 'Employee_Name', 'Avg_Hours_Worked', 'Avg_Emails_Sent', 'Avg_Breaks_Per_Day']
summary_df = summary_df.round(2)

# Add full period range to summary
date_ranges = df.groupby('Employee_ID')['Date'].agg(['min', 'max']).reset_index()
date_ranges['Period'] = date_ranges['min'].dt.date.astype(str) + " to " + date_ranges['max'].dt.date.astype(str)
summary_df = summary_df.merge(date_ranges[['Employee_ID', 'Period']], on='Employee_ID', how='left')
summary_df = summary_df[['Employee_ID', 'Employee_Name', 'Period',
                         'Avg_Hours_Worked', 'Avg_Emails_Sent', 'Avg_Breaks_Per_Day']]

# === Alerts Table (Last 2 Weeks Only) ===
latest_date = df['Date'].max()
cutoff_date = latest_date - timedelta(days=13)
overall_email_avg = df['Emails_Sent'].mean()
grouped = df.groupby('Employee_ID')

alerts = []

for emp_id, data in grouped:
    emp_name = data['Employee_Name'].iloc[0]
    recent_data = data[data['Date'] >= cutoff_date].set_index('Date').sort_index()

    # Overworked Alert
    hours_avg = recent_data['Hours_Worked'].rolling('14D').mean()
    for date in hours_avg[hours_avg > 8].index:
        avg_hours = hours_avg.loc[date]
        start = (date - timedelta(days=13)).date()
        alerts.append({
            "Employee_ID": emp_id,
            "Employee_Name": emp_name,
            "Alert_Type": "Overworked",
            "Period": f"{start} to {date.date()}",
            "Alert_Message": (
                f"{emp_name} averaged {avg_hours:.2f} hours/day from {start} to {date.date()} - "
                "above the healthy limit of 8 hours. Possible stress risk."
            )
        })

    # Low Email Activity
    emails_avg = recent_data['Emails_Sent'].rolling('3D').mean()
    for date in emails_avg[emails_avg < overall_email_avg].index:
        avg_emails = emails_avg.loc[date]
        start = (date - timedelta(days=2)).date()
        alerts.append({
            "Employee_ID": emp_id,
            "Employee_Name": emp_name,
            "Alert_Type": "Low Email Activity",
            "Period": f"{start} to {date.date()}",
            "Alert_Message": (
                f"{emp_name} averaged {avg_emails:.2f} emails/day from {start} to {date.date()} - "
                f"below the team average of {overall_email_avg:.2f}. May need engagement follow-up."
            )
        })

    # Low Breaks
    if not recent_data.empty:
        breaks_avg = recent_data['Breaks_Per_Day'].mean()
        if breaks_avg < 2:
            period_range = f"{recent_data.index.min().date()} to {recent_data.index.max().date()}"
            alerts.append({
                "Employee_ID": emp_id,
                "Employee_Name": emp_name,
                "Alert_Type": "Low Breaks",
                "Period": period_range,
                "Alert_Message": (
                    f"{emp_name} averaged only {breaks_avg:.2f} breaks/day from {period_range} - "
                    "below the recommended 2/day. Encourage short breaks."
                )
            })

# Export to Excel
alerts_df = pd.DataFrame(alerts)
output_path = "Employee_Report_DetailedAlerts2Weeks_SummaryFull.xlsx"
with pd.ExcelWriter(output_path) as writer:
    alerts_df.to_excel(writer, sheet_name='Alerts_2Weeks', index=False)
    summary_df.to_excel(writer, sheet_name='Summary_Full', index=False)
print(f"Report generated: {output_path}")
