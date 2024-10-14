import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

if __name__ == '__main__':

    # Set streamlit settings to wide
    # st.set_page_config(layout="wide")

    # Create slider for lookback
    hours_to_filter = st.slider('hours', 1, 48, 4)


    df = pd.read_csv('export.csv', index_col=0)

    # Convert the 'Time' column to datetime format
    df['Time'] = pd.to_datetime(df['Time'])

    # Get the current time and calculate the time 4 hours ago
    current_time = datetime.now()
    four_hours_ago = current_time - timedelta(hours=hours_to_filter)

    # Filter the DataFrame to include only rows from the past 4 hours
    df_filtered_time = df[df['Time'] >= four_hours_ago]

    # Further filter out rows where 'HL_Volume' is below 200000
    df_filtered_volume = df_filtered_time[(df_filtered_time['HL_Volume'] >= 200000) & (df_filtered_time['LL_Volume'] >= 100000)]

    # Filter out rows where 'Exchanges' contains 'Bitmart'
    df_filtered = df_filtered_volume[df_filtered_volume['Exchanges'] != 'Gate.io / BitMart']

    pair_stats = df_filtered.groupby(['Pair', 'Exchanges']).agg(
        Count=('Pair', 'size'),  # Count occurrences
        Avg_HL_Spread=('HL_Spread', 'mean'),  # Calculate average HL_Spread
        Avg_LL_Spread=('LL_Spread', 'mean'),  # Calculate average LL_Spread
        Avg_Spread_Differential=('Spread_Differential', 'mean'),  # Calculate average LL_Spread
        Avg_HL_Volume=('HL_Volume', 'mean'),  # Calculate average LL_Spread
        Avg_LL_Volume=('LL_Volume', 'mean'),  # Calculate average LL_Spread
        # Exchanges=('Exchanges', lambda x: ', '.join(x.unique()))  # Show unique exchanges as a comma-separated string

    ).reset_index()

    # Sort by number of occurrences

    pair_stats_sorted = pair_stats.sort_values(by=['Count', 'Avg_LL_Volume'], ascending=False)

    pair_stats_sorted.reset_index(drop=True, inplace=True)
    # print(pair_stats_sorted.head(25))
    # print(df)

    st.dataframe(pair_stats_sorted.head(25))

    st.subheader('Evolution of the top 5.')

    # st.line_chart(df.loc[df['Pair'] == 'REEF/USDT']['LL_Spread'])

    # Trying to reference the chart above
    top_5 = pair_stats_sorted.iloc[0:5]

    # st.line_chart(df.loc[df['Pair'] == pair_stats_sorted.iloc[0]['Pair']]['LL_Spread'])

    st.write(top_5)
    st.line_chart(top_5['Spread_differential'])
