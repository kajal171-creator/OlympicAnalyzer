import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    country = country.strip()  # Remove leading/trailing spaces
    country = country.title()  # Convert to title case (e.g., 'uk' -> 'UK')

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['Region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['Region'] == country)]

    x = temp_df.groupby('Region' if country == 'Overall' else 'Year').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def medal_tally(df):
    # Remove duplicates based on specific columns
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    # Group by region and sum the medal counts
    medal_tally = medal_tally.groupby('Region')[['Gold', 'Silver', 'Bronze']].sum()

    # Sort the results by Gold medals in descending order
    medal_tally = medal_tally.sort_values('Gold', ascending=False).reset_index()

    # Calculate the total medal count
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['Region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time.columns = ['Edition', col]
    return nations_over_time.sort_values('Edition')


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    temp_df = temp_df['Name'].value_counts().reset_index()
    temp_df.columns = ['Name', 'Medals']

    x = temp_df.merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'Medals', 'Sport', 'Region']].drop_duplicates('Name')
    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['Region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['Region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


# top 10 person in each country
def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['Region'] == country]

    if temp_df.empty:
        return pd.DataFrame(columns=['Name', 'Sport'])  # return an empty DataFrame with the desired columns

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, on='Name', how='left').loc[:, ['Name', 'Sport']]

    if x.empty:
        return x  # return the empty DataFrame

    x.drop_duplicates(subset='Name', inplace=True)
    return x

