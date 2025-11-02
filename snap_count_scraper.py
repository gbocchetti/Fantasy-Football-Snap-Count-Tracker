#!/usr/bin/env python3
"""
Fantasy Football Snap Count Tracker
Scrapes snap count data from Pro Football Reference for the most recent weeks
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_weekly_snap_counts(year, week):
    """
    Scrape snap count data for a specific week from Pro Football Reference
    """
    url = f"https://www.pro-football-reference.com/years/{year}/snapcounts/week_{week}.htm"
    print(f"Fetching data from: {url}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # Find the offensive snap counts table
        table = soup.find('table', {'id': 'snap_counts'})

        if not table:
            print(f"No snap count table found for Week {week}")
            return None

        # Parse table into dataframe
        rows = []
        tbody = table.find('tbody')

        if not tbody:
            return None

        for row in tbody.find_all('tr'):
            # Skip header rows
            if 'thead' in row.get('class', []):
                continue

            cols = row.find_all(['th', 'td'])
            if len(cols) < 5:
                continue

            try:
                player_elem = cols[0].find('a')
                player_name = player_elem.text if player_elem else cols[0].text.strip()

                team = cols[1].text.strip()
                position = cols[2].text.strip()
                offense_snaps = cols[3].text.strip()
                offense_pct = cols[4].text.strip()

                # Convert snaps to integer
                try:
                    offense_snaps = int(offense_snaps) if offense_snaps else 0
                except ValueError:
                    offense_snaps = 0

                rows.append({
                    'player': player_name,
                    'team': team,
                    'position': position,
                    'week': week,
                    'offense_snaps': offense_snaps,
                    'offense_pct': offense_pct
                })
            except Exception as e:
                continue

        if rows:
            df = pd.DataFrame(rows)
            print(f"Successfully scraped {len(df)} players for Week {week}")
            return df
        else:
            print(f"No data found for Week {week}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Week {week}: {e}")
        return None


def get_recent_weeks_data(year, weeks):
    """
    Get snap count data for multiple weeks
    """
    all_data = []

    for week in weeks:
        df = scrape_weekly_snap_counts(year, week)
        if df is not None:
            all_data.append(df)
        time.sleep(2)  # Be respectful to the server

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        return combined
    else:
        return None


def calculate_snap_count_increase(snap_counts):
    """
    Calculate snap count increase between the two weeks
    Returns top 5 players by increase
    """
    available_weeks = sorted(snap_counts['week'].unique())
    print(f"\nWeeks loaded: {available_weeks}")

    if len(available_weeks) < 2:
        print("Not enough weeks of data available.")
        return None

    previous_week = available_weeks[0]
    recent_week = available_weeks[1]

    print(f"\nAnalyzing snap count changes: Week {previous_week} → Week {recent_week}")

    # Get data for each week
    week1_data = snap_counts[snap_counts['week'] == previous_week].copy()
    week2_data = snap_counts[snap_counts['week'] == recent_week].copy()

    # Prepare for merge
    week1_snaps = week1_data[['player', 'team', 'position', 'offense_snaps']].copy()
    week1_snaps.columns = ['player', 'team', 'position', 'week1_snaps']

    week2_snaps = week2_data[['player', 'team', 'position', 'offense_snaps']].copy()
    week2_snaps.columns = ['player', 'team', 'position', 'week2_snaps']

    # Merge on player and team
    merged = pd.merge(week1_snaps, week2_snaps, on=['player', 'team', 'position'], how='outer')

    # Fill NaN with 0
    merged['week1_snaps'] = merged['week1_snaps'].fillna(0)
    merged['week2_snaps'] = merged['week2_snaps'].fillna(0)

    # Calculate increase
    merged['snap_increase'] = merged['week2_snaps'] - merged['week1_snaps']

    # Filter to only players who played in week 2
    merged = merged[merged['week2_snaps'] > 0]

    # Sort by increase and get top 5
    top_5 = merged.nlargest(5, 'snap_increase').reset_index(drop=True)

    return top_5, previous_week, recent_week


def display_results(top_5, previous_week, recent_week):
    """Display the top 5 players by snap count increase"""
    print("\n" + "="*80)
    print(f"TOP 5 PLAYERS BY SNAP COUNT INCREASE")
    print(f"Week {previous_week} → Week {recent_week}")
    print("="*80)

    for idx, row in top_5.iterrows():
        print(f"\n{idx + 1}. {row['player']} - {row['position']} ({row['team']})")
        print(f"   Week {previous_week}: {int(row['week1_snaps'])} snaps")
        print(f"   Week {recent_week}: {int(row['week2_snaps'])} snaps")
        print(f"   Change: {int(row['snap_increase']):+d} snaps")

    print("\n" + "="*80)


def main():
    """Main execution function"""
    print("Fantasy Football Snap Count Tracker")
    print("="*40)

    # Fetch Week 7 and Week 8 of 2025 NFL season
    year = 2025
    weeks_to_fetch = [7, 8]

    print(f"\nFetching snap count data for {year} NFL season")
    print(f"Weeks: {weeks_to_fetch}\n")

    snap_counts = get_recent_weeks_data(year, weeks_to_fetch)

    if snap_counts is None or len(snap_counts) == 0:
        print("\nNo data could be retrieved. Try adjusting the year and weeks.")
        print("\nTrying alternative weeks...")

        # Try weeks 7 and 8 as fallback
        weeks_to_fetch = [7, 8]
        print(f"Trying weeks: {weeks_to_fetch}\n")
        snap_counts = get_recent_weeks_data(year, weeks_to_fetch)

    if snap_counts is not None and len(snap_counts) > 0:
        print(f"\nTotal records loaded: {len(snap_counts)}")

        # Calculate increases
        result = calculate_snap_count_increase(snap_counts)

        if result:
            top_5, previous_week, recent_week = result

            # Display results
            display_results(top_5, previous_week, recent_week)

            # Save to CSV
            output_file = f'snap_count_increase_week{previous_week}_to_week{recent_week}.csv'
            top_5.to_csv(output_file, index=False)
            print(f"\nResults saved to: {output_file}")

            # Also save full dataset
            full_output = f'snap_counts_weeks_{previous_week}_{recent_week}_full.csv'
            snap_counts.to_csv(full_output, index=False)
            print(f"Full data saved to: {full_output}")
    else:
        print("\nCould not retrieve any snap count data.")
        print("This may be due to:")
        print("- The weeks not being available yet")
        print("- Network restrictions")
        print("- Changes to the Pro Football Reference website structure")


if __name__ == "__main__":
    main()
