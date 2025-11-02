#!/usr/bin/env python3
"""
Fantasy Football Snap Count Tracker - Demo with Sample Data
This demonstrates the functionality with realistic sample data
"""

import pandas as pd


def create_sample_data():
    """
    Create sample snap count data for two weeks
    Based on realistic NFL snap count patterns
    """
    # Week 8 data
    week8_data = [
        {'player': 'CeeDee Lamb', 'team': 'DAL', 'position': 'WR', 'week': 8, 'offense_snaps': 58},
        {'player': 'Tyreek Hill', 'team': 'MIA', 'position': 'WR', 'week': 8, 'offense_snaps': 52},
        {'player': 'Christian McCaffrey', 'team': 'SF', 'position': 'RB', 'week': 8, 'offense_snaps': 45},
        {'player': 'Bijan Robinson', 'team': 'ATL', 'position': 'RB', 'week': 8, 'offense_snaps': 35},
        {'player': 'Travis Kelce', 'team': 'KC', 'position': 'TE', 'week': 8, 'offense_snaps': 48},
        {'player': 'Amon-Ra St. Brown', 'team': 'DET', 'position': 'WR', 'week': 8, 'offense_snaps': 54},
        {'player': 'Stefon Diggs', 'team': 'HOU', 'position': 'WR', 'week': 8, 'offense_snaps': 47},
        {'player': 'Derrick Henry', 'team': 'BAL', 'position': 'RB', 'week': 8, 'offense_snaps': 42},
        {'player': 'Puka Nacua', 'team': 'LAR', 'position': 'WR', 'week': 8, 'offense_snaps': 15},
        {'player': 'Rashee Rice', 'team': 'KC', 'position': 'WR', 'week': 8, 'offense_snaps': 0},
        {'player': 'Mike Evans', 'team': 'TB', 'position': 'WR', 'week': 8, 'offense_snaps': 56},
        {'player': 'Garrett Wilson', 'team': 'NYJ', 'position': 'WR', 'week': 8, 'offense_snaps': 51},
        {'player': 'Saquon Barkley', 'team': 'PHI', 'position': 'RB', 'week': 8, 'offense_snaps': 46},
        {'player': 'Jahmyr Gibbs', 'team': 'DET', 'position': 'RB', 'week': 8, 'offense_snaps': 38},
        {'player': 'De\'Von Achane', 'team': 'MIA', 'position': 'RB', 'week': 8, 'offense_snaps': 28},
        {'player': 'Tank Dell', 'team': 'HOU', 'position': 'WR', 'week': 8, 'offense_snaps': 0},
        {'player': 'Sam LaPorta', 'team': 'DET', 'position': 'TE', 'week': 8, 'offense_snaps': 44},
        {'player': 'Mark Andrews', 'team': 'BAL', 'position': 'TE', 'week': 8, 'offense_snaps': 41},
        {'player': 'DJ Moore', 'team': 'CHI', 'position': 'WR', 'week': 8, 'offense_snaps': 55},
        {'player': 'Kyren Williams', 'team': 'LAR', 'position': 'RB', 'week': 8, 'offense_snaps': 40},
    ]

    # Week 9 data - with some significant changes
    week9_data = [
        {'player': 'CeeDee Lamb', 'team': 'DAL', 'position': 'WR', 'week': 9, 'offense_snaps': 62},
        {'player': 'Tyreek Hill', 'team': 'MIA', 'position': 'WR', 'week': 9, 'offense_snaps': 55},
        {'player': 'Christian McCaffrey', 'team': 'SF', 'position': 'RB', 'week': 9, 'offense_snaps': 48},
        {'player': 'Bijan Robinson', 'team': 'ATL', 'position': 'RB', 'week': 9, 'offense_snaps': 58},
        {'player': 'Travis Kelce', 'team': 'KC', 'position': 'TE', 'week': 9, 'offense_snaps': 51},
        {'player': 'Amon-Ra St. Brown', 'team': 'DET', 'position': 'WR', 'week': 9, 'offense_snaps': 57},
        {'player': 'Stefon Diggs', 'team': 'HOU', 'position': 'WR', 'week': 9, 'offense_snaps': 49},
        {'player': 'Derrick Henry', 'team': 'BAL', 'position': 'RB', 'week': 9, 'offense_snaps': 44},
        {'player': 'Puka Nacua', 'team': 'LAR', 'position': 'WR', 'week': 9, 'offense_snaps': 61},
        {'player': 'Rashee Rice', 'team': 'KC', 'position': 'WR', 'week': 9, 'offense_snaps': 0},
        {'player': 'Mike Evans', 'team': 'TB', 'position': 'WR', 'week': 9, 'offense_snaps': 58},
        {'player': 'Garrett Wilson', 'team': 'NYJ', 'position': 'WR', 'week': 9, 'offense_snaps': 53},
        {'player': 'Saquon Barkley', 'team': 'PHI', 'position': 'RB', 'week': 9, 'offense_snaps': 49},
        {'player': 'Jahmyr Gibbs', 'team': 'DET', 'position': 'RB', 'week': 9, 'offense_snaps': 41},
        {'player': 'De\'Von Achane', 'team': 'MIA', 'position': 'RB', 'week': 9, 'offense_snaps': 31},
        {'player': 'Tank Dell', 'team': 'HOU', 'position': 'WR', 'week': 9, 'offense_snaps': 52},
        {'player': 'Sam LaPorta', 'team': 'DET', 'position': 'TE', 'week': 9, 'offense_snaps': 47},
        {'player': 'Mark Andrews', 'team': 'BAL', 'position': 'TE', 'week': 9, 'offense_snaps': 43},
        {'player': 'DJ Moore', 'team': 'CHI', 'position': 'WR', 'week': 9, 'offense_snaps': 57},
        {'player': 'Kyren Williams', 'team': 'LAR', 'position': 'RB', 'week': 9, 'offense_snaps': 43},
    ]

    # Combine into single dataframe
    df = pd.DataFrame(week8_data + week9_data)
    return df


def calculate_snap_count_increase(snap_counts):
    """
    Calculate snap count increase between the two weeks
    Returns top 5 players by increase
    """
    available_weeks = sorted(snap_counts['week'].unique())
    print(f"\nWeeks in dataset: {available_weeks}")

    if len(available_weeks) < 2:
        print("Not enough weeks of data available.")
        return None

    previous_week = available_weeks[0]
    recent_week = available_weeks[1]

    print(f"Analyzing snap count changes: Week {previous_week} → Week {recent_week}")

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
        increase = int(row['snap_increase'])
        sign = '+' if increase >= 0 else ''

        print(f"\n{idx + 1}. {row['player']} - {row['position']} ({row['team']})")
        print(f"   Week {previous_week}: {int(row['week1_snaps'])} snaps")
        print(f"   Week {recent_week}: {int(row['week2_snaps'])} snaps")
        print(f"   Change: {sign}{increase} snaps")

        # Add context for significant changes
        if increase >= 40:
            print(f"   📈 MAJOR INCREASE - Likely returning from injury or increased role")
        elif increase >= 20:
            print(f"   ⬆️  SIGNIFICANT INCREASE - Expanding role in offense")

    print("\n" + "="*80)


def main():
    """Main execution function"""
    print("="*80)
    print("FANTASY FOOTBALL SNAP COUNT TRACKER - DEMO")
    print("="*80)
    print("\nNOTE: Using sample data to demonstrate functionality")
    print("The real version will fetch live data from Pro Football Reference\n")

    # Create sample data
    snap_counts = create_sample_data()

    print(f"Sample dataset contains {len(snap_counts)} player-week records")

    # Calculate increases
    result = calculate_snap_count_increase(snap_counts)

    if result:
        top_5, previous_week, recent_week = result

        # Display results
        display_results(top_5, previous_week, recent_week)

        # Save to CSV
        output_file = f'snap_count_increase_week{previous_week}_to_week{recent_week}_demo.csv'
        top_5.to_csv(output_file, index=False)
        print(f"\n✅ Results saved to: {output_file}")

        # Also save full dataset
        full_output = f'snap_counts_weeks_{previous_week}_{recent_week}_full_demo.csv'
        snap_counts.to_csv(full_output, index=False)
        print(f"✅ Full data saved to: {full_output}")

        print("\n" + "="*80)
        print("KEY INSIGHTS:")
        print("="*80)
        print("\n• Puka Nacua (+46 snaps): Likely returning from injury - huge fantasy pickup!")
        print("• Tank Dell (+52 snaps): Returned from injury, immediate WR2 role")
        print("• Bijan Robinson (+23 snaps): Increased usage, trending up in Atlanta offense")
        print("\n" + "="*80)


if __name__ == "__main__":
    main()
