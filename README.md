# Fantasy Football Snap Count Tracker

A Python tool to track and analyze NFL player snap counts week-over-week to identify trending players for fantasy football.

## Features

- Imports snap count data from Pro Football Reference
- Analyzes snap count changes between consecutive weeks
- Identifies top 5 players with the largest snap count increases
- Exports results to CSV for further analysis

## Files

- `snap_count_scraper.py` - Main script that scrapes live data from Pro Football Reference
- `snap_count_analyzer.py` - Alternative using nfl_data_py library (requires library access)
- `snap_count_demo.py` - Demo version with sample data (works offline)
- `requirements.txt` - Python package dependencies

## Usage

### Using Live Data (requires internet access)

```bash
pip install -r requirements.txt
python snap_count_scraper.py
```

Edit the `year` and `weeks_to_fetch` variables in the script to target specific weeks.

### Using Demo Data

```bash
pip install pandas
python snap_count_demo.py
```

## Output

The tool displays:
1. Top 5 players by snap count increase
2. Their snap counts for both weeks
3. The net change in snaps
4. Context about significant increases

Results are saved to CSV files for further analysis.

## Example Output

```
TOP 5 PLAYERS BY SNAP COUNT INCREASE
Week 8 → Week 9
================================================================================

1. Tank Dell - WR (HOU)
   Week 8: 0 snaps
   Week 9: 52 snaps
   Change: +52 snaps
   📈 MAJOR INCREASE - Likely returning from injury or increased role

2. Puka Nacua - WR (LAR)
   Week 8: 15 snaps
   Week 9: 61 snaps
   Change: +46 snaps
   📈 MAJOR INCREASE - Likely returning from injury or increased role
```

## Data Sources

- **Pro Football Reference**: Primary source for snap count data
- **nfl_data_py / nflverse**: Alternative API-based data source

## Dependencies

- pandas
- requests
- beautifulsoup4
- lxml
- nfl_data_py (optional)

## Notes

- Be respectful of web scraping - the script includes delays between requests
- Some environments may have network restrictions that prevent data access
- For demo purposes, use `snap_count_demo.py` which works with sample data
