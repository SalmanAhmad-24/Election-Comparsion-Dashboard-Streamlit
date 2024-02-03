
import pandas as pd
import streamlit as st
import plotly.express as px

# Load the Excel data
excel_path = 'SWAT_National Assembly Polling Scheme_salman.xlsx'

# Initialize session state for df
if 'df' not in st.session_state:
    st.session_state.df = pd.read_excel(excel_path).dropna(subset=["No. and Name of Polling Station"])

# Ensure consistent data type for "No. and Name of Polling Station"
st.session_state.df["No. and Name of Polling Station"] = st.session_state.df["No. and Name of Polling Station"].astype(str)
polling_stations = st.session_state.df["No. and Name of Polling Station"].unique().tolist()
# Replace NaN or null values in "No. and Name of Polling Station" with a default value
# st.session_state.df["No. and Name of Polling Station"] = st.session_state.df["No. and Name of Polling Station"].fillna("Unknown")

# Define the list of companies
companies = ["ANP", "JUI", "PTI-P", "PTI", "PML-N"]

# Define colors for each political party
party_colors = {
    "ANP": "red",
    "JUI":  "black",
    "PTI-P": "blue",
    "PTI": "lightgreen",
    "PML-N": "darkgreen"
}

# Initialize session state for filtered_df
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = pd.DataFrame()

# Create a Streamlit web app
st.title("Election Comparison Dashboard")

# Search for the polling station
# selected_polling_stations = st.multiselect("Select Polling Stations:", polling_stations)
# if selected_polling_stations:
#     st.session_state.filtered_df2 = st.session_state.df[st.session_state.df["No. and Name of Polling Station"].isin(selected_polling_stations)]
# else:
#     st.session_state.filtered_df2 = st.session_state.df

# Selectbox widget to choose a specific polling station from the filtered results
selected_polling_station = st.selectbox("Select or Search Polling Station:", [""] + polling_stations, key="polling_station_selectbox")
# Update the search_query text_input based on the selected polling station
# search_query = st.text_input("Search Polling Station:", value=selected_polling_station)
if selected_polling_station:
    st.session_state.filtered_df2 = st.session_state.df[st.session_state.df["No. and Name of Polling Station"].str.extract(f'({selected_polling_station})', expand=False)]

# Display the final filtered DataFrame
# st.write("Filtered DataFrame:", st.session_state.filtered_df2)

st.session_state.filtered_df = st.session_state.df[st.session_state.df["No. and Name of Polling Station"].str.strip() == selected_polling_station.strip()]

# Display error message if no matching polling station is found or if search query is empty
if st.session_state.filtered_df.empty and selected_polling_station:
    st.error("No matching polling station found. Please enter a valid name.")
else:
    # Allow the user to input values for each company
    st.write("Enter Values for Each Company:")
    values = {}
    for company in companies:
        values[company] = st.number_input(f"{company} Value", key=company)
        values[company] = values[company]

    # Update the DataFrame with user-input values
    for company in companies:
        st.session_state.df.loc[st.session_state.df["No. and Name of Polling Station"].str.strip() == selected_polling_station.strip(), company] = values[company]

    # Calculate the sum of values for each company
    df_sum = st.session_state.df[companies].sum().astype(int)

    # Display the comparison bar chart using Plotly Express
    fig = px.bar(df_sum, x=df_sum.index, y=df_sum.values, labels={"y": "Total Votes", "x": "Political Parties"},
                 title="Comparison of Votes for Political Parties", color=df_sum.index, color_discrete_map=party_colors)
    st.plotly_chart(fig)

    # Display the updated DataFrame with user-input values
    st.write("Updated DataFrame:")
    st.dataframe(st.session_state.df)
    st.write("Total Votes")
    st.table(df_sum)
    
    selected_parties = st.multiselect("Select two parties to compare", df_sum.index)

# Calculate and display the difference in total votes between the selected parties
    if len(selected_parties) == 2:
        difference = df_sum[selected_parties[0]] - df_sum[selected_parties[1]]
        st.write(f"Difference in total votes between {selected_parties[0]} and {selected_parties[1]}: {abs(difference)}")
    else:
        st.warning("Please select exactly two parties to compare.")