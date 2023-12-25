# Import necessary libraries
import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import plotly.figure_factory as ff

# Read the Olympic data from CSV files
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Preprocess the data to clean and organize it
df = preprocessor.preprocess(df,region_df)

# Sidebar creation for user interaction
st.sidebar.title("Olympics Analysis")# Sidebar title
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(# Radio buttons for user options
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

# Handling user selections
if user_menu == 'Medal Tally':
    # Display medal tally based on selected year and country
    st.sidebar.header("Medal Tally") # Sidebar header

    # Fetch years and countries for selection
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years) # Select year
    selected_country = st.sidebar.selectbox("Select Country", country) # Select country

    # Fetch and display medal tally based on user selections
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    # Display different titles based on selected options
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    # Other conditional titles based on selected options
    st.table(medal_tally)# Display medal tally in a table format

if user_menu == 'Overall Analysis':
    # Calculating various statistics based on the Olympic dataset
    editions = df['Year'].unique().shape[0] - 1  # Count of unique years (excluding 'Overall')
    cities = df['City'].unique().shape[0]  # Count of unique host cities
    sports = df['Sport'].unique().shape[0]  # Count of unique sports
    events = df['Event'].unique().shape[0]  # Count of unique events
    athletes = df['Name'].unique().shape[0]  # Count of unique athlete names
    nations = df['region'].unique().shape[0]  # Count of unique regions (countries)

    # Displaying top statistics using Streamlit columns
    st.title("Top Statistics")  # Title for the statistics section
    col1, col2, col3 = st.columns(3)  # Creating three columns for layout

    # Displaying statistics in three columns
    with col1:
        st.header("Editions")  # Header for the 'Editions' statistic
        st.title(editions)  # Displaying the count of editions

    with col2:
        st.header("Hosts")  # Header for the 'Hosts' statistic
        st.title(cities)  # Displaying the count of host cities

    with col3:
        st.header("Sports")  # Header for the 'Sports' statistic
        st.title(sports)  # Displaying the count of sports

    # Another set of statistics displayed in three columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")  # Header for the 'Events' statistic
        st.title(events)  # Displaying the count of events

    with col2:
        st.header("Nations")  # Header for the 'Nations' statistic
        st.title(nations)  # Displaying the count of nations

    with col3:
        st.header("Athletes")  # Header for the 'Athletes' statistic
        st.title(athletes)  # Displaying the count of athletes

    # Visualizing participation trends over time using Plotly line charts
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="No of countries")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)  # Displaying the participation trend of nations

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="No of countries")
    st.title("Events over the years")
    st.plotly_chart(fig)  # Displaying the event count trend over years

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="No of countries")
    st.title("Athletes over the years")
    st.plotly_chart(fig)  # Displaying the athlete count trend over years

    # Visualizing the number of events over time for each sport using a heatmap
    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))  # Creating a heatmap figure
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])  # Removing duplicate events
    # Generating a heatmap showing event counts for each sport over years
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count')
                     .fillna(0).astype('int'), annot=True)
    st.pyplot(fig)  # Displaying the heatmap in the Streamlit app

    # Displaying a table of the most successful athletes based on user-selected sport
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()  # Creating a list of unique sports
    sport_list.sort()  # Sorting the sports list alphabetically
    sport_list.insert(0, 'Overall')  # Inserting 'Overall' at the beginning of the list

    selected_sport = (st.selectbox('Select a Sport', sport_list))  # Dropdown for sport selection
    x = helper.most_successful(df, selected_sport)  # Fetching most successful athletes
    st.table(x)  # Displaying the table of most successful athletes


if user_menu == 'Country-wise Analysis':
    # Setting up the sidebar title for 'Country-wise Analysis'
    st.sidebar.title('Country-wise Analysis')

    # Generating a sorted list of unique countries from the dataset
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    # Creating a dropdown menu in the sidebar to select a country
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    # Retrieving and displaying the medal tally of the selected country over the years using Plotly
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)  # Displaying the medal tally chart for the selected country

    # Displaying the sports in which the selected country excels using a heatmap
    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)  # Displaying the heatmap showing the country's performance in sports

    # Displaying a table of the top 10 athletes from the selected country
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)  # Displaying the table of top athletes from the selected country

if user_menu == 'Athlete wise Analysis':
    # Creating a DataFrame of unique athletes considering their name and region
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Data extraction for age distribution
    x1 = athlete_df['Age'].dropna()  # All ages
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()  # Ages of Gold medalists
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()  # Ages of Silver medalists
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()  # Ages of Bronze medalists

    # Creating a distribution plot for age distribution using Plotly
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)  # Displaying the age distribution plot

    # Data extraction for age distribution with respect to sports
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']  # List of various sports
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]  # Filtering athletes by sport
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())  # Ages of Gold medalists in specific sports
        name.append(sport)  # Storing sport names

    # Creating a distribution plot for age distribution of Gold Medalists based on sports using Plotly
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports (Gold Medalist)")
    st.plotly_chart(fig)  # Displaying the age distribution plot for Gold Medalists in different sports

    # Selection of sport for height-weight comparison
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    # Visualization of height versus weight for athletes based on selected sport
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)  # Data extraction for height-weight comparison

    fig, ax = plt.subplots()
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60, ax=ax)
    st.pyplot(fig)  # Displaying the scatterplot for height versus weight

    # Visualization of men versus women participation over the years
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)  # Data extraction for men vs women participation
    fig = px.line(final, x="Year", y=["Male", "Female"])  # Creating a line chart using Plotly
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)  # Displaying the line chart for men vs women participation




