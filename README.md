# WHOOP Membership Services Analytics (Portfolio Project)

This project simulates a scaled wearable + membership business (WHOOP-inspired) to analyze:
- Member support performance (KPIs like CSAT, FCR, repeat contacts, escalation rate)
- Root causes of high-volume issues
- Operational improvements
- Retention impact (churn analysis)

## Data
Synthetic data generated via Python:
- `members.csv` (200k+ members)
- `tickets.csv` (~10k support tickets)
- `member_support_summary.csv` (aggregated support metrics per member)

## How to run
1) Create a virtual environment
2) Install requirements
3) Generate data
4) Load into Power BI

## Project structure
- `src/` Python generation code
- `data/generated/` output CSVs
- `sql/` analysis queries
- `powerbi/` Power BI setup + exports
- `reports/` executive-style written summary