import pandas as pd
from datetime import datetime, timedelta

if __name__ == '__main__':

    df = pd.read_csv('export.csv', index_col=0)

    # Convert the 'Time' column to datetime format
    df['Time'] = pd.to_datetime(df['Time'])

    # Get the current time and calculate the time 4 hours ago
    current_time = datetime.now()
    four_hours_ago = current_time - timedelta(hours=4)

    # Filter the DataFrame to include only rows from the past 4 hours
    df_filtered_time = df[df['Time'] >= four_hours_ago]

    # Further filter out rows where 'HL_Volume' is below 200000
    df_filtered = df_filtered_time[df_filtered_time['HL_Volume'] >= 200000]

    pair_stats = df_filtered.groupby(['Pair', 'Exchanges']).agg(
        Count=('Pair', 'size'),  # Count occurrences
        Avg_HL_Spread=('HL_Spread', 'mean'),  # Calculate average HL_Spread
        Avg_LL_Spread=('LL_Spread', 'mean'),  # Calculate average LL_Spread
        Avg_HL_Volume=('HL_Volume', 'mean'),  # Calculate average LL_Spread
        Avg_LL_Volume=('LL_Volume', 'mean'),  # Calculate average LL_Spread
        # Exchanges=('Exchanges', lambda x: ', '.join(x.unique()))  # Show unique exchanges as a comma-separated string

    ).reset_index()

    # Sort by number of occurrences

    pair_stats_sorted = pair_stats.sort_values(by=['Count', 'Avg_LL_Volume'], ascending=False)
    pair_stats_sorted['Spread_differential'] = pair_stats_sorted['Avg_LL_Spread'] - pair_stats_sorted['Avg_HL_Spread']



    print(pair_stats_sorted.head(20))
    # print(df)