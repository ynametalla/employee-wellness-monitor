
# Employee Wellness Monitoring

This project analyzes employee productivity and wellness data to detect early signs of overwork, disengagement, or unhealthy work habits. It generates alerts based on specific criteria and exports a detailed PDF report.

## Features

- 📊 Calculates 2-week average hours worked to identify overwork.
- 📧 Monitors 3-day email activity for engagement issues.
- 🚶 Checks daily breaks to encourage healthy habits.
- 📝 Exports alerts in a clean, readable PDF report.

## How to Use

1. Place your Excel data file as `SDG 3 - Data.xlsx` in the same directory.
2. Run the script:

```bash
python analyze_alerts.py
```

3. The script will create a `Employee_Alerts_Report.pdf` file with all relevant alerts.

## Requirements

- Python 3.x
- pandas
- fpdf

Install dependencies with:

```bash
pip install pandas fpdf
```

## Customization

- Modify alert thresholds directly in the script.
- Extend analysis by adding new metrics or conditions.

## License

MIT License
