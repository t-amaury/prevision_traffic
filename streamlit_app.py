import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Prévision du traffic',
    page_icon=':airplane:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_prevision_data():
    DATA_FILENAME = Path(__file__).parent/'data/prevision_data.csv'
    raw_prevision_df = pd.read_csv(DATA_FILENAME)
    MIN_YEAR = 2024
    MAX_YEAR = 2030
    prevision_df = raw_prevision_df.melt(
        ['pair'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'prevision',
    )
    # Convert years from string to integers
    prevision_df['Year'] = pd.to_numeric(prevision_df['Year'])
    return prevision_df

@st.cache_data
def get_eurocontrol_data():
    DATA_FILENAME = Path(__file__).parent/'data/eurocontrol_data.csv'
    raw_eurocontrol_df = pd.read_csv(DATA_FILENAME)
    MIN_YEAR = 2019
    MAX_YEAR = 2030
    eurocontrol_df = raw_eurocontrol_df.melt(
        ['pair'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'prevision',
    )
    # Convert years from string to integers
    eurocontrol_df['Year'] = pd.to_numeric(eurocontrol_df['Year'])
    return eurocontrol_df

prevision_df = get_prevision_data()
eurocontrol_df = get_eurocontrol_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :airplane: Prévision du traffic

Utilisation de data de prévision de 2024 à 2030.
'''

# Add some spacing
''
''
min_value = prevision_df['Year'].min()
max_value = prevision_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = prevision_df['pair'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['LF_LF'])

include_eurocontrol = st.checkbox('Include Eurocontrol data')

''
''
''

filtered_prevision_df = prevision_df[
    (prevision_df['pair'].isin(selected_countries))
    & (prevision_df['Year'] <= to_year)
    & (from_year <= prevision_df['Year'])
]

if include_eurocontrol:
    filtered_eurocontrol_df = eurocontrol_df[
        (eurocontrol_df['Year'] <= to_year)
        & (from_year <= eurocontrol_df['Year'])
    ]
    filtered_prevision_df = pd.concat([filtered_prevision_df, filtered_eurocontrol_df])

filtered_prevision_df['Year'] = filtered_prevision_df['Year'].astype(str)

st.header('Prévision over time', divider='gray')

''
''
st.line_chart(
    filtered_prevision_df,
    x='Year',
    y='prevision',
    color='pair',
)

# Optionally, add a download button for the filtered data
csv = filtered_prevision_df.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='filtered_prevision_data.csv',
    mime='text/csv',
)
