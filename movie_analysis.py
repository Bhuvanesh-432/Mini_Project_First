import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="movies_db"
)
cursor = conn.cursor()

# 1️⃣ Fetch Movie Data
query = "SELECT title, rating, votes, duration, genre FROM movies;"
df = pd.read_sql(query, conn)

# Close connection
cursor.close()
conn.close()

# 2️⃣ Show First Few Rows
print(df.head())

# 3️⃣ Plot Top 10 Rated Movies
top_movies = df.nlargest(10, 'rating')

plt.figure(figsize=(10, 5))
sns.barplot(x="rating", y="title", data=top_movies, palette="viridis")
plt.xlabel("IMDb Rating")
plt.ylabel("Movie Title")
plt.title("Top 10 Highest Rated Movies")
plt.show()

# 4️⃣ Plot Movie Count by Genre
plt.figure(figsize=(12, 6))
sns.countplot(y=df["genre"], order=df["genre"].value_counts().index, palette="coolwarm")
plt.xlabel("Count")
plt.ylabel("Genre")
plt.title("Number of Movies per Genre")
plt.show()


###### Movie_Analysis_Part

import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# MySQL Connection Function
def get_movie_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="movies_db"
    )
    query = "SELECT title, rating, votes, duration, genre FROM movies;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load Data
df = get_movie_data()

# Streamlit Layout
st.title("🎬 Movie Data Analysis & Visualization")
st.sidebar.header("Filters")

# Filters
min_rating = st.sidebar.slider("Minimum Rating", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
min_votes = st.sidebar.number_input("Minimum Votes", min_value=0, value=1000, step=1000)
selected_genres = st.sidebar.multiselect("Select Genres", df["genre"].unique(), default=df["genre"].unique())

# Duration Filter
duration_range = st.sidebar.slider("Select Duration Range (minutes)", min_value=int(df["duration"].min()), max_value=int(df["duration"].max()), value=(int(df["duration"].min()), int(df["duration"].max())))

df_filtered = df[(df["rating"] >= min_rating) & (df["votes"] >= min_votes) & (df["genre"].isin(selected_genres)) & (df["duration"] >= duration_range[0]) & (df["duration"] <= duration_range[1])]

# Display Data
st.write("### Filtered Movie Data", df_filtered)

# Top 10 Movies by Rating and Votes
st.write("### Top 10 Movies by Rating and Votes")
top_movies = df_filtered.nlargest(10, ["rating", "votes"])
st.bar_chart(top_movies.set_index("title")["rating"])

# Genre Distribution
st.write("### Genre Distribution")
genre_count = df_filtered["genre"].value_counts()
st.bar_chart(genre_count)

# Average Duration by Genre
st.write("### Average Duration by Genre")
avg_duration = df_filtered.groupby("genre")["duration"].mean().sort_values()
st.bar_chart(avg_duration)

# Voting Trends by Genre
st.write("### Voting Trends by Genre")
avg_votes = df_filtered.groupby("genre")["votes"].mean().sort_values()
st.bar_chart(avg_votes)

# Rating Distribution
st.write("### Rating Distribution")
fig, ax = plt.subplots()
sns.histplot(df_filtered["rating"], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# Genre-Based Rating Leaders
st.write("### Genre-Based Rating Leaders")
leader_movies = df_filtered.loc[df_filtered.groupby("genre")["rating"].idxmax()][["genre", "title", "rating"]]
st.dataframe(leader_movies)

# Most Popular Genres by Voting
st.write("### Most Popular Genres by Voting")
popular_genres = df_filtered.groupby("genre")["votes"].sum().sort_values(ascending=False)
fig = px.pie(popular_genres.reset_index(), names="genre", values="votes", title="Most Popular Genres")
st.plotly_chart(fig)

# Duration Extremes
st.write("### Duration Extremes")
shortest_movie = df_filtered.nsmallest(1, "duration")[["title", "duration"]]
longest_movie = df_filtered.nlargest(1, "duration")[["title", "duration"]]
st.write("Shortest Movie:", shortest_movie)
st.write("Longest Movie:", longest_movie)

# Ratings by Genre Heatmap
st.write("### Ratings by Genre")
rating_heatmap = df_filtered.pivot_table(index="genre", values="rating", aggfunc="mean")
fig, ax = plt.subplots()
sns.heatmap(rating_heatmap, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Correlation Analysis
st.write("### Correlation Analysis")
numeric_df = df_filtered.select_dtypes(include=['number'])
fig, ax = plt.subplots()
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)