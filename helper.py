import numpy as np

# Function to fetch the medal tally based on year and country
def fetch_medal_tally(df, year, country):
    # Remove duplicate entries based on specific columns
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    # Filtering based on year and country
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    # Grouping data by year or country and summing up medal counts
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    # Calculating total medals won
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Converting medal counts to integer values
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

# Function to generate lists of unique years and countries available in the dataset
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

# Function to analyze the number of nations participating over different years
def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': 'No of countries'}, inplace=True)
    return nations_over_time

# Function to retrieve information about the most successful athletes in a particular sport or overall
def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Counting medals per athlete
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']

    # Merge the medal counts back to the original DataFrame
    merged_df = medal_counts.head(15).merge(df, on='Name', how='left').drop_duplicates('Name')
    selected_cols = merged_df[['Name', 'Medals', 'Sport', 'region']]

    return selected_cols

# Function to calculate the yearwise medal tally for a specific country
def yearwise_medal_tally(df,country):
    # Drop rows with missing medal information and remove duplicates based on specific columns
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    # Filter data for the specified country and compute medal counts per year
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

# Function to generate a heatmap of medals won in different sports by a country over the years
def country_event_heatmap(df,country):
    # Drop rows with missing medal information and remove duplicates based on specific columns
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    # Filter data for the specified country and create a pivot table for sports vs. years with medal counts
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

# Function to retrieve information about the most successful athletes in a specific country
def most_successful_countrywise(df, country):
    # Drop rows with missing medal information
    temp_df = df.dropna(subset=['Medal'])

    # Filter data for the specified country (if not 'All') and count medals for each athlete
    if country != 'All':
        temp_df = temp_df[temp_df['region'] == country]

    # Counting medals per athlete
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']

    # Merge the medal counts back to the original DataFrame
    merged_df = medal_counts.head(10).merge(df, on='Name', how='left').drop_duplicates('Name')
    selected_cols = merged_df[['Name', 'Medals', 'Sport', 'region']]

    return selected_cols

# Function to analyze weight versus height of athletes, filtering by a specific sport or considering all athletes
def weight_v_height(df,sport):
    # Drop duplicate entries based on athlete's name and country
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    # Filter data for a specific sport or return all athletes if 'Overall' is chosen
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

# Function to compare the participation of male and female athletes over the years
def men_vs_women(df):
    # Drop duplicate entries based on athlete's name and country
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Count male and female athletes participating each year and merge counts into a final DataFrame
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    # Fill missing counts with zeros
    final.fillna(0, inplace=True)

    return final