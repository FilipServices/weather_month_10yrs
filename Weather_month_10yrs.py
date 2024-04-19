import calendar
import datetime
from IPython.display import HTML, Javascript

# Initialize Open-Meteo API client
import openmeteo_requests
import requests_cache
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# URL for Open-Meteo API
url = "https://archive-api.open-meteo.com/v1/archive"

# ... (latitude/longitude input or place name input code) ...

# Input month name
month_name = input("Enter month name (e.g., January): ")


# Convert month name to number
month_number = list(calendar.month_name).index(month_name.capitalize())

if month_number == 0:
    print("Invalid month name.")
else:
    # Get current date and calculate start year
    current_date = datetime.date.today()
    current_year = current_date.year
    start_year = current_year - 10

    # ... (rest of the code for data retrieval and processing using month_number, start_year, and current_year) ...

# ... (previous code for user input and setting time period) ...

# Lists to store daily maximum temperatures for each year
all_max_temperatures = []

# Choose one of the following options for location input:

# Option 1: Latitude/Longitude Input
print("Right-click on google maps, left-click copies (eg. 50.08402, 19.96261) to clipboard")
print()
latitude = float(input("Enter latitude (eg. 50.08402): "))
longitude = float(input("Enter longitude (eg. 19.96261): "))

# Option 2: Place Name Input (Requires Geocoding)
# ... (code for place name input using geopy) ...

# Loop through each year
for year in range(start_year, current_year + 1):
    # Construct start and end dates for the month
    start_date = f"{year}-{month_number:02}-01"
    end_date = f"{year}-{month_number:02}-{calendar.monthrange(year, month_number)[1]}"

    # Open-Meteo API parameters
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max"],
        "timezone": "UTC",  # Using UTC for consistency
    }

    # Send API request
    response = openmeteo.weather_api(url, params=params)

    # Extract daily maximum temperatures and store in a list
    daily_data = response[0].Daily().Variables(0).ValuesAsNumpy()
    all_max_temperatures.append(daily_data)

# ... (code for data processing and visualization) ...


import matplotlib.pyplot as plt
import numpy as np

# Create a figure and axes
plt.figure(figsize=(10, 6))  # Adjust figure size as needed
ax = plt.axes()

# Set up colors for each year's line
colors = plt.cm.viridis(np.linspace(0, 1, len(all_max_temperatures)))

# Plot each year's data
for i, year_data in enumerate(all_max_temperatures):
    # Create x-axis values (days of the month)
    x_values = range(1, len(year_data) + 1)
    
    # Plot the line
    ax.plot(x_values, year_data, color=colors[i], label=f"{start_year + i}")

# Add labels and title
ax.set_xlabel("Day of Month")
ax.set_ylabel("Maximum Temperature (°C)")
ax.set_title(f"Daily Maximum Temperatures for {month_name} (Past 10 Years)")

# Add legend
plt.legend()

# Show the plot
plt.show()
