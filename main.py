import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

def get_data(sheet_name):
    # Fetch data from the Google Apps Script API using the specified sheet name
    url = f'https://script.google.com/macros/s/AKfycbyArX-VqTB_BGt_iRJ-2vCPu1mfY4McZw85m7XJu6nOeXvwt1suVoCwAhPdYlNdRrQn/exec?sheet={sheet_name}'
    response = requests.get(url)  # Send a GET request to the API
    return response

# Configure the Streamlit page layout to be wide
st.set_page_config(layout = "wide")

# Title of the dashboard
st.markdown("<h1 style='text-align: center;'>Crypto Breadth & Speculation Index</h1>", unsafe_allow_html=True)

# Separator
st.write("---")

# Subtitle for the Crypto Breadth section
st.markdown("<h1 style='text-align: center;'>Crypto Breadth</h1>", unsafe_allow_html=True)

# Description of Crypto Breadth
st.markdown(
    """
    <p style='text-align: center;'>
        Market Breadth is a measure for strength in equities markets. 
        Crypto Breadth applies the Market Breadth formula for equities to 195 Altcoins. 
        1 indicates all coins are above the corresponding metrics, 
        0 indicates all coins are below the corresponding metrics.
    </p>
    """,
    unsafe_allow_html=True
)

# Create a layout with smaller width for the selectbox
col1, col2, col3 = st.columns([5, 1, 5])  # Define three columns with specified ratios

# Place the selectbox in the center column
with col2:
    option = st.selectbox(
        'Select score calculation type:',  # Dropdown menu for selecting calculation type
        ('SMA', 'EMA', 'RSI')  # Options available in the dropdown
    )

if True:  # Using True to always enter the block (could be removed for clarity)
    try:
        response = get_data("API_data")  # Get data from the API
        data = response.json()  # Parse the response as JSON
        dates = data["date"]  # Extract date values
        sma50 = data["50sma"]  # Extract 50-period SMA values
        sma200 = data["200sma"]  # Extract 200-period SMA values
        ema50 = data["50ema"]  # Extract 50-period EMA values
        ema200 = data["200ema"]  # Extract 200-period EMA values
        rsi50 = data["50rsi"]  # Extract 50-period RSI values
        btc = data["btc"]  # Extract BTC price values

        # Create an interactive plot with Plotly
        fig = go.Figure()

        # Conditional plotting based on the dropdown selection
        if option == 'SMA':
            # Plot SMA50 and SMA200 if SMA is selected
            fig.add_trace(go.Scatter(
                x=dates, y=sma50, 
                mode='lines', 
                name='50 SMA', 
                line=dict(color='green', width=2),  
                yaxis='y1'  # First y-axis
            ))
            fig.add_trace(go.Scatter(
                x=dates, y=sma200, 
                mode='lines', 
                name='200 SMA', 
                line=dict(color='yellow', width=2),  
                yaxis='y1'  # First y-axis
            ))
        elif option == 'EMA':
            # Plot EMA50 and EMA200 if EMA is selected
            fig.add_trace(go.Scatter(
                x=dates, y=ema50, 
                mode='lines', 
                name='50 EMA', 
                line=dict(color='pink', width=2),  
                yaxis='y1'  # First y-axis
            ))
            fig.add_trace(go.Scatter(
                x=dates, y=ema200, 
                mode='lines', 
                name='200 EMA', 
                line=dict(color='purple', width=2),  
                yaxis='y1'  # First y-axis
            ))
        elif option == 'RSI':
            # Plot RSI50 if RSI is selected
            fig.add_trace(go.Scatter(
                x=dates, y=rsi50, 
                mode='lines', 
                name='50 RSI', 
                line=dict(color='white', width=2),  
                yaxis='y1'  # First y-axis
            ))

        # Plot BTC on the secondary y-axis regardless of the selection
        fig.add_trace(go.Scatter(
            x=dates, y=btc, 
            mode='lines', 
            name='BTC', 
            line=dict(color='orange', width=2),  
            yaxis='y2'  # Second y-axis
        ))

        # Customize layout for two y-axes, with the second being logarithmic
        fig.update_layout(
            width=1000,  # Set width of the plot
            height=600,  # Set height of the plot
            xaxis_title="Date",  # Title for the x-axis
            yaxis_title="Crypto Breadth",  # Title for the first y-axis
            xaxis=dict(
                tickformat="%Y-%m-%d",  # Format for x-axis ticks
                tickangle=-45,  # Angle for x-axis tick labels
                rangeslider=dict(
                    visible=True,
                    bgcolor="lightgray",  # Set slider background color to gray
                    thickness=0.1,  # Adjust thickness of the slider
                    borderwidth=1,  # Optionally add border to slider
                    bordercolor="gray",  # Border color to match gray theme
                ),
                type="date",  # Ensure it's a date-based slider
            ),
            yaxis=dict(
                title="Crypto Breadth",  # Title for the first y-axis
                showgrid=True,  # Show grid lines
                zeroline=True  # Show the zero line
            ),
            yaxis2=dict(
                title="BTC Price (Log Scale)",  # Title for the second y-axis
                overlaying='y',  # Overlay on the first y-axis
                side='right',  # Position the second y-axis on the right
                type="log",  # Set y-axis to logarithmic scale
                showgrid=False,  # Hide grid lines for the second y-axis
                zeroline=False  # Hide the zero line for the second y-axis
            ),
        )

        # Display the interactive plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        # Handle any errors that occur during data fetching or processing
        st.error(f"Error fetching data: {e}")

st.write("---")

# Subtitle for the Robust Speculation Index section
st.markdown("<h1 style='text-align: center;'>Robust Speculation Index</h1>", unsafe_allow_html=True)

# Description of the Robust Speculation Index
st.markdown("<p style='text-align: center;'>Robust Speculation Index is calculated as the percentage of altcoins with 75-day, 80-day, 85-day, 90-day, 95-day, 100-day, 105-day returns greater than Bitcoin. High readings suggest mounting speculation. Lower readings suggest capitulation, and potentially greater investment opportunities in altcoins. 1 = all periods have greater returns than BTC, 0 = not all periods have greater returns than BTC.</p>", unsafe_allow_html=True)

if True:  # Using True to always enter the block (could be removed for clarity)
    try:
        response = get_data("API_data")  # Get data from the API
        data = response.json()  # Parse the response as JSON
        dates = data["date"]  # Extract date values
        spec = data["spec"]  # Extract speculation index values
        btc = data["btc"]  # Extract BTC price values

        # Create an interactive plot for the Robust Speculation Index
        fig2 = go.Figure()

        # Plot the Speculation Index on the primary y-axis
        fig2.add_trace(go.Scatter(
            x=dates, y=spec, 
            mode='lines', 
            name='Speculation Index', 
            line=dict(color='red', width=2),  
            yaxis='y1'  # First y-axis
        ))

        # Plot BTC on the secondary y-axis
        fig2.add_trace(go.Scatter(
            x=dates, y=btc, 
            mode='lines', 
            name='BTC', 
            line=dict(color='orange', width=2),  
            yaxis='y2'  # Second y-axis
        ))

        # Customize layout for two y-axes, with the second being logarithmic
        fig2.update_layout(
            width=1000,  # Set width of the plot
            height=600,  # Set height of the plot
            xaxis_title="Date",  # Title for the x-axis
            yaxis_title="Speculation Index",  # Title for the first y-axis
            xaxis=dict(
                tickformat="%Y-%m-%d",  # Format for x-axis ticks
                tickangle=-45,  # Angle for x-axis tick labels
                rangeslider=dict(
                    visible=True,
                    bgcolor="lightgray",  # Set slider background color to gray
                    thickness=0.1,  # Adjust thickness of the slider
                    borderwidth=1,  # Optionally add border to slider
                    bordercolor="gray",  # Border color to match gray theme
                ),
                type="date",  # Ensure it's a date-based slider
            ),
            yaxis=dict(
                title="Speculation Index",  # Title for the first y-axis
                showgrid=True,  # Show grid lines
                zeroline=True  # Show the zero line
            ),
            yaxis2=dict(
                title="BTC Price (Log Scale)",  # Title for the second y-axis
                overlaying='y',  # Overlay on the first y-axis
                side='right',  # Position the second y-axis on the right
                type="log",  # Set y-axis to logarithmic scale
                showgrid=False,  # Hide grid lines for the second y-axis
                zeroline=False  # Hide the zero line for the second y-axis
            ),
        )

        # Display the interactive plot in Streamlit
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        # Handle any errors that occur during data fetching or processing
        st.error(f"Error fetching data: {e}")

st.write("---")

# Prepare data for CSV download
df = pd.DataFrame({
    "Date": dates,  # Date column
    "BTC Price": btc,  # BTC price column
    "50 SMA": sma50,  # 50-period SMA column
    "200 SMA": sma200,  # 200-period SMA column
    "50 EMA": ema50,  # 50-period EMA column
    "200 EMA": ema200,  # 200-period EMA column
    "50 RSI": rsi50  # 50-period RSI column
})

# Provide the option to download the data as a CSV file
csv = df.to_csv(index=False)  # Convert DataFrame to CSV format without index

# Create columns for the download button layout
col2_1, col2_2, col2_3 = st.columns([3, 1, 3])

# Place the download button in the center column
with col2_2:
    st.download_button(
        label="Download data as CSV",  # Button label
        data=csv,  # Data to download
        file_name='crypto_data.csv',  # Name of the downloaded file
        mime='text/csv',  # MIME type for CSV
    )
