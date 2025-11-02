#!/usr/bin/env python3
"""
Fantasy Football Snap Count Tracker
Imports snap count data from the most recent two weeks and shows top 5 players by snap count increase
"""

import nfl_data_py as nfl
import pandas as pd
from datetime import datetime


def get_recent_weeks_data():
    """Import snap count data for the current NFL season"""
    # Try current year first, fall back to 2024 if not available
    current_year = datetime.now().year

    for year in [current_year, 2024, 2023]:
        try:
            print(f"Importing snap count data for {year} season...")
            snap_counts = nfl.import_snap_counts(years=[year])
            print(f"Successfully loaded {year} data")
            return snap_counts
        except Exception as e:
            print(f"Could not load {year} data: {e}")
            continue

    raise Exception("Could not load snap count data for any recent season")


def calculate_snap_count_increase(snap_counts):
    """
    Calculate snap count increase from the two most recent weeks
    Returns top 5 players by increase
    """
    # Get the most recent two weeks
    available_weeks = sorted(snap_counts['week'].unique())
    print(f"\nAvailable weeks: {available_weeks}")

    if len(available_weeks) < 2:
        print("Not enough weeks of data available yet.")
        return None

    # Get the two most recent weeks
    recent_week = available_weeks[-1]
    previous_week = available_weeks[-2]

    print(f"\nAnalyzing snap count changes between Week {previous_week} and Week {recent_week}")

    # Filter data for these two weeks
    week1_data = snap_counts[snap_counts['week'] == previous_week].copy()
    week2_data = snap_counts[snap_counts['week'] == recent_week].copy()

    # Merge on player identifier
    # Group by player_id and pfr_player_id to get their snap counts
    week1_snaps = week1_data.groupby(['player', 'pfr_player_id', 'position'])['offense_snaps'].sum().reset_index()
    week1_snaps.columns = ['player', 'pfr_player_id', 'position', 'week1_snaps']

    week2_snaps = week2_data.groupby(['player', 'pfr_player_id', 'position'])['offense_snaps'].sum().reset_index()
    week2_snaps.columns = ['player', 'pfr_player_id', 'position', 'week2_snaps']

    # Merge the two weeks
    merged = pd.merge(week1_snaps, week2_snaps, on=['player', 'pfr_player_id', 'position'], how='outer')

    # Fill NaN with 0 (players who didn't play one week)
    merged['week1_snaps'] = merged['week1_snaps'].fillna(0)
    merged['week2_snaps'] = merged['week2_snaps'].fillna(0)

    # Calculate increase
    merged['snap_increase'] = merged['week2_snaps'] - merged['week1_snaps']

    # Sort by increase and get top 5
    top_5 = merged.nlargest(5, 'snap_increase')

    return top_5, previous_week, recent_week


def display_results(top_5, previous_week, recent_week):
    """Display the top 5 players by snap count increase"""
    print("\n" + "="*80)
    print(f"TOP 5 PLAYERS BY SNAP COUNT INCREASE (Week {previous_week} → Week {recent_week})")
    print("="*80)

    for idx, row in top_5.iterrows():
        print(f"\n{row.name + 1}. {row['player']} ({row['position']})")
        print(f"   Week {previous_week}: {int(row['week1_snaps'])} snaps")
        print(f"   Week {recent_week}: {int(row['week2_snaps'])} snaps")
        print(f"   Increase: +{int(row['snap_increase'])} snaps")

    print("\n" + "="*80)


def main():
    """Main execution function"""
    print("Fantasy Football Snap Count Tracker")
    print("-" * 40)

    try:
        # Import data
        snap_counts = get_recent_weeks_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Calculate increases
    result = calculate_snap_count_increase(snap_counts)

    if result:
        top_5, previous_week, recent_week = result

        # Display results
        display_results(top_5, previous_week, recent_week)

        # Save to CSV for reference
        output_file = f'snap_count_increase_week{previous_week}_to_week{recent_week}.csv'
        top_5.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
