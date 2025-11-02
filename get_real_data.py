#!/usr/bin/env python3
"""
Fetch real IDP snap count data for Week 7 and Week 8 of 2025 NFL season
"""

import nfl_data_py as nfl
import pandas as pd

try:
    print("Fetching 2025 NFL snap count data...")
    snap_counts = nfl.import_snap_counts(years=[2025])

    print(f"\nTotal records: {len(snap_counts)}")
    print(f"\nAvailable weeks: {sorted(snap_counts['week'].unique())}")
    print(f"\nColumns: {snap_counts.columns.tolist()}")

    # Filter for weeks 7 and 8
    weeks_data = snap_counts[snap_counts['week'].isin([7, 8])].copy()

    if len(weeks_data) == 0:
        print("\nNo data for weeks 7 and 8 yet")
        print("\nShowing all available data:")
        print(snap_counts.head(20))
    else:
        print(f"\nRecords for weeks 7 and 8: {len(weeks_data)}")

        # Determine the correct team column name
        team_col = None
        for possible_col in ['team', 'tm', 'recent_team', 'opponent']:
            if possible_col in weeks_data.columns:
                team_col = possible_col
                print(f"Using team column: '{team_col}'")
                break

        if team_col is None:
            print("ERROR: Could not find team column. Available columns:")
            print(weeks_data.columns.tolist())
            raise ValueError("No team column found")

        # Determine snap count column - use defense_snaps for IDP
        snap_col = 'defense_snaps' if 'defense_snaps' in weeks_data.columns else 'defense'
        if snap_col not in weeks_data.columns:
            print(f"ERROR: Could not find defensive snap column. Available columns:")
            print(weeks_data.columns.tolist())
            raise ValueError("No defensive snap column found")

        print(f"Using snap count column: '{snap_col}'")

        # Week 7 data
        week7 = weeks_data[weeks_data['week'] == 7].copy()
        week7_snaps = week7.groupby(['player', 'pfr_player_id', 'position', team_col])[snap_col].sum().reset_index()
        week7_snaps.columns = ['player', 'pfr_player_id', 'position', 'team', 'week7_snaps']

        # Week 8 data
        week8 = weeks_data[weeks_data['week'] == 8].copy()
        week8_snaps = week8.groupby(['player', 'pfr_player_id', 'position', team_col])[snap_col].sum().reset_index()
        week8_snaps.columns = ['player', 'pfr_player_id', 'position', 'team', 'week8_snaps']

        # Merge
        merged = pd.merge(week7_snaps, week8_snaps, on=['player', 'pfr_player_id', 'position', 'team'], how='outer')
        merged['week7_snaps'] = merged['week7_snaps'].fillna(0)
        merged['week8_snaps'] = merged['week8_snaps'].fillna(0)
        merged['snap_increase'] = merged['week8_snaps'] - merged['week7_snaps']

        # Filter to players who played in Week 7 (exclude players on bye in preceding week)
        # Allow Week 8 = 0 (players coming off bye or injured)
        merged = merged[merged['week7_snaps'] > 0]

        # Filter for IDP positions only (defensive players)
        idp_positions = ['DT', 'DE', 'DL', 'NT', 'LB', 'MLB', 'OLB', 'ILB', 'ROLB', 'LOLB',
                         'CB', 'S', 'SS', 'FS', 'DB', 'SAF']
        merged = merged[merged['position'].isin(idp_positions)]

        # Add status column
        def get_status(row):
            if row['week8_snaps'] == 0:
                return "⚠️ BYE/INJURED"
            elif row['snap_increase'] >= 15:
                return "📈 MAJOR INCREASE"
            elif row['snap_increase'] >= 10:
                return "⬆️ INCREASE"
            elif row['snap_increase'] <= -15:
                return "📉 MAJOR DECREASE"
            elif row['snap_increase'] <= -10:
                return "⬇️ DECREASE"
            else:
                return "➡️ STEADY"

        merged['status'] = merged.apply(get_status, axis=1)

        # Top 20
        top_20 = merged.nlargest(20, 'snap_increase').reset_index(drop=True)

        print("\n" + "="*80)
        print("TOP 20 IDP PLAYERS BY SNAP COUNT INCREASE (Week 7 → Week 8, 2025 NFL Season)")
        print("(Defensive Players Only - Includes players coming off bye)")
        print("="*80)

        for idx, row in top_20.iterrows():
            print(f"\n{idx + 1}. {row['player']} - {row['position']} ({row['team']}) {row['status']}")
            print(f"   Week 7: {int(row['week7_snaps'])} snaps")
            print(f"   Week 8: {int(row['week8_snaps'])} snaps")
            print(f"   Change: {int(row['snap_increase']):+d} snaps")

        print("\n" + "="*80)

        # Save
        top_20.to_csv('idp_snap_count_increase_week7_to_week8.csv', index=False)
        print("\n✅ Results saved to: idp_snap_count_increase_week7_to_week8.csv")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
