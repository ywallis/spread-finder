import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px


if __name__ == '__main__':

    # Set streamlit settings to wide
    # st.set_page_config(layout="wide")

    # Create slider for lookback
    hours_to_filter = st.slider('hours', 1, 48, 4)
    pairs_to_show = st.slider('pairs', 10, 50, 25)

    df = pd.read_csv('.Data/export.csv', index_col=0)

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
        HL_Spread=('HL_Spread', 'mean'),  # Calculate average HL_Spread
        LL_Spread=('LL_Spread', 'mean'),  # Calculate average LL_Spread
        Differential=('Spread_Differential', 'mean'),  # Calculate average LL_Spread
        # HL_Volume=('HL_Volume', 'mean'),  # Calculate average LL_Spread
        LL_Volume=('LL_Volume', 'mean'),  # Calculate average LL_Spread
        # Exchanges=('Exchanges', lambda x: ', '.join(x.unique()))  # Show unique exchanges as a comma-separated string

    ).reset_index()

    # Sort by number of occurrences

    pair_stats_sorted = pair_stats.sort_values(by=['Count', 'LL_Volume'], ascending=False)

    pair_stats_sorted.reset_index(drop=True, inplace=True)

    top_pairs = pair_stats_sorted.head(pairs_to_show)

    st.dataframe(top_pairs)

    # Select a pair
    selected_pair = st.selectbox("Select a pair", top_pairs['Pair'].unique())

    # Filter exchanges based on the selected pair
    filtered_exchanges = top_pairs[top_pairs['Pair'] == selected_pair]['Exchanges'].unique()

    # Select an exchange (filtered by the selected pair)
    selected_exchange = st.selectbox("Select an exchange combination", filtered_exchanges)

    data = df.loc[(df['Pair'] == selected_pair) & (df['Exchanges'] == selected_exchange)]

    # Plotly chart with custom labels
    fig = px.line(data, x='Time', y='Spread_Differential', labels={'x': 'Time', 'y': 'Spread Differential'})
    fig.update_layout(title='Custom Line Chart Title')

    st.plotly_chart(fig)