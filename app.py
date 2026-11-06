
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="IMDb Top 250 Movies Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 IMDb Top 250 Movies Dashboard")
st.write("Explore and analyse the Top 250 IMDb movies.")
st.divider()


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

file_path = "Top 250 movies on imdb in 2026.csv"

try:
    df = pd.read_csv(file_path)
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding="latin1")
except FileNotFoundError:
    st.error("CSV file not found. Keep the CSV file in the same folder as app.py.")
    st.stop()

st.success("Dataset loaded successfully!")


# --------------------------------------------------
# FIND COLUMN NAMES AUTOMATICALLY
# --------------------------------------------------

def find_column(possible_names):
    normalized_columns = {
        re.sub(r"[^a-z0-9]", "", str(col).lower()): col
        for col in df.columns
    }

    for name in possible_names:
        key = re.sub(r"[^a-z0-9]", "", name.lower())
        if key in normalized_columns:
            return normalized_columns[key]

    return None


title_col = find_column([
    "primaryTitle", "title", "movieTitle", "movie_name", "name"
])

genre_col = find_column([
    "genres", "genre"
])

rating_col = find_column([
    "averageRating", "rating", "imdbRating", "imdb_rating"
])

votes_col = find_column([
    "numVotes", "votes", "numberOfVotes", "num_votes"
])

gross_col = find_column([
    "grossWorldwide", "gross", "worldwideGross", "gross_worldwide"
])

country_col = find_column([
    "countries", "country", "countryOfOrigin", "origin"
])


# Convert numeric columns to numbers where possible

if rating_col:
    df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")

if votes_col:
    df[votes_col] = pd.to_numeric(df[votes_col], errors="coerce")

if gross_col:
    df[gross_col] = pd.to_numeric(df[gross_col], errors="coerce")


# --------------------------------------------------
# QUESTION 1: DATASET LOADING AND EXPLORATION
# --------------------------------------------------

st.header("1. Dataset Loading and Exploration")

st.subheader("First 10 Rows")
st.dataframe(df.head(10), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Rows", df.shape[0])

with col2:
    st.metric("Total Columns", df.shape[1])

st.subheader("Column Names")
st.write(df.columns.tolist())

st.subheader("Data Types")
st.write(df.dtypes)

st.subheader("Missing Values")
st.write(df.isnull().sum())

st.success("Dataset exploration completed!")

st.divider()


# --------------------------------------------------
# QUESTION 2: KPI METRICS
# --------------------------------------------------

st.header("2. Key Performance Indicators")

if rating_col and votes_col:

    total_movies = len(df)

    average_rating = df[rating_col].mean()

    highest_rating = df[rating_col].max()

    total_votes = df[votes_col].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Movies", f"{total_movies:,}")
    c2.metric("Average Rating", f"{average_rating:.2f}")
    c3.metric("Highest Rating", f"{highest_rating:.2f}")
    c4.metric("Total Votes", f"{total_votes:,.0f}")

else:
    st.warning("Rating or votes column was not found in the dataset.")

st.divider()


# --------------------------------------------------
# QUESTION 3: DATA VISUALIZATION
# --------------------------------------------------

st.header("3. Data Visualizations")


# Chart 1: Genre Bar Chart

st.subheader("Movies by Genre")

if genre_col:

    genre_data = df[genre_col].dropna().astype(str).str.split(r"[,|]")

    genre_data = genre_data.explode().str.strip()

    genre_counts = genre_data.value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 5))

    genre_counts.plot(kind="bar", ax=ax)

    ax.set_xlabel("Genre")
    ax.set_ylabel("Number of Movies")
    ax.set_title("Number of Movies by Genre")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

else:
    st.info("Genre column is not available.")


# Chart 2: Rating Histogram

st.subheader("IMDb Rating Distribution")

if rating_col:

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(df[rating_col].dropna(), bins=15, edgecolor="black")

    ax.set_xlabel("IMDb Rating")
    ax.set_ylabel("Number of Movies")
    ax.set_title("Distribution of IMDb Ratings")

    st.pyplot(fig)
    plt.close(fig)

else:
    st.info("Rating column is not available.")


# Chart 3: Rating vs Votes Scatter Plot

st.subheader("Average Rating vs Number of Votes")

if rating_col and votes_col:

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        df[rating_col],
        df[votes_col],
        alpha=0.6
    )

    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Number of Votes")
    ax.set_title("Rating vs Number of Votes")

    st.pyplot(fig)
    plt.close(fig)

else:
    st.info("Rating or votes column is not available.")


# Chart 4: Top 10 Grossing Movies

st.subheader("Top 10 Movies by Worldwide Gross")

if gross_col:

    top_gross = df.nlargest(10, gross_col)

    if title_col:
        display_columns = [title_col, gross_col]
    else:
        display_columns = [gross_col]

    st.dataframe(
        top_gross[display_columns],
        use_container_width=True
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    if title_col:
        ax.bar(
            top_gross[title_col].astype(str),
            top_gross[gross_col]
        )
        ax.set_xticklabels(
            top_gross[title_col].astype(str),
            rotation=45,
            ha="right"
        )
    else:
        ax.bar(
            range(len(top_gross)),
            top_gross[gross_col]
        )

    ax.set_xlabel("Movie")
    ax.set_ylabel("Worldwide Gross")
    ax.set_title("Top 10 Movies by Worldwide Gross")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

else:
    st.info("Worldwide gross column is not available in this dataset.")

st.divider()


# --------------------------------------------------
# QUESTION 4: STREAMLIT LAYOUT
# --------------------------------------------------

st.header("4. Streamlit Layout Components")

tab1, tab2, tab3 = st.tabs([
    "Movie Details",
    "Dataset Information",
    "About"
])

with tab1:
    st.subheader("Movie Details")
    st.dataframe(df.head(10), use_container_width=True)

with tab2:
    st.subheader("Dataset Information")

    with st.expander("View Dataset Description"):
        st.write("This dataset contains IMDb movie information.")
        st.write("Rows:", df.shape[0])
        st.write("Columns:", df.shape[1])
        st.write("Available columns:", df.columns.tolist())

with tab3:
    st.subheader("About This Dashboard")
    st.info("This dashboard analyses the Top 250 IMDb movies.")
    st.success("Explore movies using the interactive filters.")

st.divider()


# --------------------------------------------------
# QUESTION 5: INTERACTIVE MOVIE EXPLORER
# --------------------------------------------------

st.header("5. Interactive Movie Explorer")

if not title_col:
    st.warning("Movie title column was not found. The movie explorer needs a title column.")
else:

    # Create genre options

    if genre_col:
        genre_values = (
            df[genre_col]
            .dropna()
            .astype(str)
            .str.split(r"[,|]")
            .explode()
            .str.strip()
        )

        genre_options = sorted([
            x for x in genre_values.unique()
            if x and x.lower() != "nan"
        ])
    else:
        genre_options = []

    # Create country options

    if country_col:
        country_values = (
            df[country_col]
            .dropna()
            .astype(str)
            .str.split(r"[,|]")
            .explode()
            .str.strip()
        )

        country_options = sorted([
            x for x in country_values.unique()
            if x and x.lower() != "nan"
        ])
    else:
        country_options = []

    if country_col is None:
        st.info("Country filtering is unavailable because the CSV has no recognised country column.")

    # Rating range

    if rating_col and df[rating_col].notna().any():
        min_rating = float(df[rating_col].min())
        max_rating = float(df[rating_col].max())
    else:
        min_rating = 0.0
        max_rating = 10.0

    # Initialise reset values

    if "genre_filter" not in st.session_state:
        st.session_state.genre_filter = "All"

    if "country_filter" not in st.session_state:
        st.session_state.country_filter = []

    if "rating_filter" not in st.session_state:
        st.session_state.rating_filter = (min_rating, max_rating)

    if "votes_filter" not in st.session_state:
        st.session_state.votes_filter = 0

    if "title_filter" not in st.session_state:
        st.session_state.title_filter = ""

    if "sort_filter" not in st.session_state:
        st.session_state.sort_filter = "Descending"

    col1, col2 = st.columns(2)

    with col1:
        selected_genre = st.selectbox(
            "Select Genre",
            ["All"] + genre_options,
            key="genre_filter"
        )

    with col2:
        selected_countries = st.multiselect(
            "Select Countries",
            country_options,
            key="country_filter",
            disabled=(country_col is None)
        )

    selected_rating = st.slider(
        "Select IMDb Rating Range",
        min_value=min_rating,
        max_value=max_rating,
        value=(min_rating, max_rating),
        key="rating_filter",
        disabled=(rating_col is None)
    )

    minimum_votes = st.number_input(
        "Minimum Number of Votes",
        min_value=0,
        value=0,
        step=1000,
        key="votes_filter",
        disabled=(votes_col is None)
    )

    movie_search = st.text_input(
        "Search Movie by Title",
        key="title_filter"
    )

    sort_order = st.radio(
        "Sort Movies",
        ["Ascending", "Descending"],
        horizontal=True,
        key="sort_filter"
    )

    # Apply filters

    filtered_df = df.copy()

    if genre_col and selected_genre != "All":
        filtered_df = filtered_df[
            filtered_df[genre_col]
            .fillna("")
            .astype(str)
            .str.contains(selected_genre, case=False, regex=False)
        ]

    if country_col and selected_countries:
        filtered_df = filtered_df[
            filtered_df[country_col].apply(
                lambda x: any(
                    country.lower() in str(x).lower()
                    for country in selected_countries
                )
            )
        ]

    if rating_col:
        filtered_df = filtered_df[
            filtered_df[rating_col].between(
                selected_rating[0],
                selected_rating[1]
            )
        ]

    if votes_col:
        filtered_df = filtered_df[
            filtered_df[votes_col].fillna(0) >= minimum_votes
        ]

    if movie_search:
        filtered_df = filtered_df[
            filtered_df[title_col]
            .fillna("")
            .astype(str)
            .str.contains(movie_search, case=False, regex=False)
        ]

    if rating_col:
        filtered_df = filtered_df.sort_values(
            by=rating_col,
            ascending=(sort_order == "Ascending")
        )

    st.subheader("Filtered Movie Results")

    st.metric("Number of Movies Found", len(filtered_df))

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    if st.button("Reset All Filters"):
        st.session_state.genre_filter = "All"
        st.session_state.country_filter = []
        st.session_state.rating_filter = (min_rating, max_rating)
        st.session_state.votes_filter = 0
        st.session_state.title_filter = ""
        st.session_state.sort_filter = "Descending"
        st.rerun()

st.divider()


# --------------------------------------------------
# QUESTION 6: SESSION STATE AND FORM HANDLING
# --------------------------------------------------

st.header("6. Session State and Form Handling")

# Store selected movie and preference

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = ""

if "movie_preference" not in st.session_state:
    st.session_state.movie_preference = "Action"

st.subheader("Movie Selection")

if title_col:

    movie_list = (
        df[title_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_movie = st.selectbox(
        "Choose Your Favourite Movie",
        movie_list,
        key="selected_movie_widget"
    )

    st.session_state.selected_movie = selected_movie

preference_options = genre_options if genre_col and genre_options else ["Action", "Comedy", "Drama"]

movie_preference = st.selectbox(
    "Choose Your Preferred Genre",
    preference_options,
    key="preference_widget"
)

st.session_state.movie_preference = movie_preference

st.write("Selected Movie:", st.session_state.selected_movie)
st.write("Your Preference:", st.session_state.movie_preference)


# Movie details form

st.subheader("Movie Details Form")

with st.form("movie_form"):

    form_title = st.text_input("Enter Movie Title")

    form_genre = st.text_input("Enter Movie Genre")

    form_rating = st.number_input(
        "Minimum IMDb Rating",
        min_value=0.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )

    submitted = st.form_submit_button("Submit Movie Details")

    if submitted:

        st.session_state.form_title = form_title
        st.session_state.form_genre = form_genre
        st.session_state.form_rating = form_rating

        st.success("Movie details submitted successfully!")

if "form_title" in st.session_state:

    st.subheader("Submitted Movie Details")

    st.write("Movie Title:", st.session_state.form_title)
    st.write("Genre:", st.session_state.form_genre)
    st.write("Minimum IMDb Rating:", st.session_state.form_rating)

    if title_col and rating_col and votes_col:

        matching_movies = df[
            df[title_col]
            .fillna("")
            .astype(str)
            .str.contains(
                st.session_state.form_title,
                case=False,
                regex=False
            )
            &
            (df[rating_col] >= st.session_state.form_rating)
        ]

        if not matching_movies.empty:
            st.write("Matching Movies:")
            st.dataframe(
                matching_movies[
                    [title_col, rating_col, votes_col]
                ],
                use_container_width=True
            )
        else:
            st.info("No matching movies found for the submitted details.")

st.success("IMDb Movie Dashboard Completed!")
