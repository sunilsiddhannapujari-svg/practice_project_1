# -----------------------------------------
# Olympic Data Analysis - Streamlit App
# -----------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# -----------------------------------------
# SETTINGS
# -----------------------------------------
sns.set(style="whitegrid")
st.set_page_config(page_title="Olympic Dashboard", layout="wide")

st.title("🏅 Olympic Data Analysis Dashboard")

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
df = pd.read_csv("athlete_events.csv")

# Fill missing values
df['Medal'].fillna("No Medal", inplace=True)
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Height'].fillna(df['Height'].median(), inplace=True)
df['Weight'].fillna(df['Weight'].median(), inplace=True)

st.write("### Dataset Preview")
st.dataframe(df.head(10))

# -----------------------------------------
# INTERACTIVE FILTERS
# -----------------------------------------
st.sidebar.header("Filters")
year_selected = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
sport_selected = st.sidebar.selectbox("Select Sport", sorted(df['Sport'].unique()))
country_selected = st.sidebar.selectbox("Select Country", sorted(df['Team'].unique()))

# Apply filters
filtered_df = df[
    (df['Year'] == year_selected) &
    (df['Sport'] == sport_selected) &
    (df['Team'] == country_selected)
]

# Check if filtered data is empty
if filtered_df.empty:
    st.warning(f"No data found for Year={year_selected}, Sport={sport_selected}, Country={country_selected}")
else:
    st.write(f"### Showing {len(filtered_df)} records for Year={year_selected}, Sport={sport_selected}, Country={country_selected}")
    st.dataframe(filtered_df.head(10))

    # -----------------------------------------
    # MEDAL DISTRIBUTION
    # -----------------------------------------
    st.write("### Medal Distribution")
    medal_counts = filtered_df['Medal'].value_counts()
    fig, ax = plt.subplots()
    medal_counts.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

    # -----------------------------------------
    # GENDER DISTRIBUTION
    # -----------------------------------------
    st.write("### Gender Participation")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x='Sex', ax=ax)
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # -----------------------------------------
    # AGE DISTRIBUTION
    # -----------------------------------------
    st.write("### Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['Age'], bins=30, kde=True, ax=ax)
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # -----------------------------------------
    # HEIGHT vs WEIGHT
    # -----------------------------------------
    st.write("### Height vs Weight")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=filtered_df.sample(min(1000, len(filtered_df))),
        x='Height',
        y='Weight',
        hue='Sex',
        ax=ax
    )
    ax.set_title("Height vs Weight Scatter")
    st.pyplot(fig)

# -----------------------------------------
# ALL TIME ANALYSIS (Not filtered)
# -----------------------------------------
st.write("## All-Time Insights")

# Top 10 Medal Winning Countries
st.write("### Top 10 Medal Winning Countries (All Time)")
top_countries = df[df['Medal'] != "No Medal"].groupby('Team')['Medal'].count().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax)
ax.set_xlabel("Total Medals")
ax.set_ylabel("Country")
st.pyplot(fig)

# Top 10 Sports by Medals
st.write("### Top 10 Sports by Medals (All Time)")
top_sports = df[df['Medal'] != "No Medal"].groupby('Sport')['Medal'].count().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_sports.values, y=top_sports.index, ax=ax)
ax.set_xlabel("Total Medals")
ax.set_ylabel("Sport")
st.pyplot(fig)

# Year-wise Participation
st.write("### Year-wise Athlete Participation")
year_participation = df.groupby('Year')['ID'].count()
fig, ax = plt.subplots()
year_participation.plot(ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Athletes")
st.pyplot(fig)

# -----------------------------------------
# SAVE CLEANED DATA
# -----------------------------------------
df.to_csv("cleaned_athlete_events.csv", index=False)
st.success("✅ ")
