
# Employee Wellness Monitoring

This project analyzes employee productivity and wellness data to detect early signs of overwork, disengagement, or unhealthy work habits. It generates alerts based on a 2-week window and provides a full-period summary of key metrics.

## Features

- 📊 **Summary Report** (Full Period): Average hours worked, emails sent, and breaks taken per employee.
- ⚠️ **Alerts Report** (Last 2 Weeks):
  - **Overworked**: > 8 hours/day average
  - **Low Email Activity**: Below team email average
  - **Low Breaks**: Less than 2 breaks/day

## How to Use

1. Ensure your Excel file is named `SDG 3 - Data.xlsx` and placed in the same directory as the script.
2. Run the script:

```bash
python analyze_alerts_final.py
```

3. Output will be saved as:

```
Employee_Report_DetailedAlerts2Weeks_SummaryFull.xlsx
```

## Requirements

- Python 3.x
- pandas

Install dependencies with:

```bash
pip install pandas openpyxl
```

## Output Structure

- `Alerts_2Weeks`: Alerts triggered from the most recent 14-day period.
- `Summary_Full`: Employee metrics aggregated across the full available time span.

## License

MIT License
