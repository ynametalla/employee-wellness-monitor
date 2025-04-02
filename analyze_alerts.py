
import pandas as pd
from fpdf import FPDF

# === Load and Prepare Data ===
file_path = "SDG 3 - Data.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by=['Employee_ID', 'Date'], inplace=True)
overall_email_avg = df['Emails_Sent'].mean()

# === Group Data and Initialize Alert List ===
alerts = []
grouped = df.groupby('Employee_ID')

# === Analyze Each Employee ===
for emp_id, data in grouped:
    emp_name = data['Employee_Name'].iloc[0]
    data = data.set_index('Date').sort_index()

    # -- Overworked Alert --
    hours_avg = data['Hours_Worked'].rolling('14D').mean()
    for date in hours_avg[hours_avg > 8].index:
        avg_hours = hours_avg.loc[date]
        start = (date - pd.Timedelta(days=13)).date()
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

    # -- Low Email Activity Alert --
    emails_avg = data['Emails_Sent'].rolling('3D').mean()
    for date in emails_avg[emails_avg < overall_email_avg].index:
        avg_emails = emails_avg.loc[date]
        start = (date - pd.Timedelta(days=2)).date()
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

    # -- Low Breaks Alert --
    breaks_avg = data['Breaks_Per_Day'].mean()
    if breaks_avg < 2:
        period_range = f"{data.index.min().date()} to {data.index.max().date()}"
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

# === Export Alerts to PDF ===
alert_df = pd.DataFrame(alerts)
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Employee Alert Report", ln=True, align='C')
pdf.ln(10)

for _, row in alert_df.iterrows():
    pdf.set_font("Arial", 'B', size=11)
    pdf.cell(200, 10, txt=f"{row['Alert_Type']} - {row['Employee_Name']} ({row['Period']})", ln=True)
    pdf.set_font("Arial", size=10)
    message = row["Alert_Message"].replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'")
    pdf.multi_cell(0, 10, txt=message)
    pdf.ln(5)

pdf.output("Employee_Alerts_Report.pdf")
