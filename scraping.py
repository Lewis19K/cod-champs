import os
import requests
import csv
from bs4 import BeautifulSoup
from collections import defaultdict

# URLs of the player statistics for each year
urls = {
    2022: 'https://cod-esports.fandom.com/wiki/Call_of_Duty_League_Championship_2022/Player_Statistics',
    2023: 'https://cod-esports.fandom.com/wiki/Call_of_Duty_League_Championship_2023/Player_Statistics',
    2024: 'https://cod-esports.fandom.com/wiki/Call_of_Duty_League_Championship_2024/Player_Statistics'
}

# Create a directory for storing CSV files if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Function to write the data to a CSV file for each year and mode
def write_to_csv(year, mode, data):
    filename = f"data/cod_stats_{year}_{mode}.csv"
    header = ['Player Name', 'Kills', 'Deaths', 'K/D Ratio', '+/-', 'Maps Played']
    
    # Open the CSV file in append mode to add data
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write the header if it's a new file
        if f.tell() == 0:
            writer.writerow(header)
        
        # Write the statistics data
        writer.writerows(data)

# Dictionary to accumulate data for the overall CSV
accumulated_data = defaultdict(lambda: {'kills': 0, 'deaths': 0, 'kd_ratio': 0, 'plus_minus': 0, 'maps': 0, 'count': 0})

# Loop through each URL for the player statistics of each year
for year, url in urls.items():
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing the player statistics (adjust the selector if needed)
        table = soup.find('table', {'class': 'wikitable'})
        
        if table:
            # Loop through each row of the table to extract player statistics
            rows = table.find_all('tr')[1:]  # Skip the header row
            game_modes = ['General', 'Search and Destroy', 'Hardpoint', 'Control']  # Example modes, adjust as necessary
            
            # Loop through different game modes (modify this list based on the actual modes you want to extract)
            for mode in game_modes:
                mode_data = []
                for row in rows:
                    columns = row.find_all('td')
                    
                    # Ensure that the row has the correct number of columns
                    if len(columns) >= 7:  # Adjust this condition based on the number of columns you want to extract
                        player_name = columns[1].get_text(strip=True)  # Extract player name (adjust index if necessary)
                        k = int(columns[2].get_text(strip=True))  # Kills
                        d = int(columns[3].get_text(strip=True))  # Deaths
                        kdr = float(columns[4].get_text(strip=True))  # K/D Ratio
                        
                        # Handle the +/-
                        plus_minus_str = columns[5].get_text(strip=True)
                        plus_minus_str = plus_minus_str.replace('−', '-')  # Replacing the 'minus' character
                        
                        try:
                            plus_minus = int(plus_minus_str)
                        except ValueError:
                            plus_minus = 0  # Default to 0 if the value can't be converted
                        
                        maps = int(columns[6].get_text(strip=True))  # Maps played (Adjust if necessary)
                        
                        # Store the data for the current mode
                        mode_data.append([player_name, k, d, kdr, plus_minus, maps])
                        
                        # Accumulate data for the overall CSV (sum the statistics for each player)
                        accumulated_data[player_name]['kills'] += k
                        accumulated_data[player_name]['deaths'] += d
                        accumulated_data[player_name]['kd_ratio'] += kdr
                        accumulated_data[player_name]['plus_minus'] += plus_minus
                        accumulated_data[player_name]['maps'] += maps
                        accumulated_data[player_name]['count'] += 1
                
                # Write the data for the current mode to CSV
                write_to_csv(year, mode, mode_data)
        else:
            print(f"Table not found for {year}")
    else:
        print(f"Failed to retrieve data for {year} - Status code: {response.status_code}")

# After all the data is processed, write the accumulated data to a separate CSV
def write_accumulated_data():
    filename = "data/cod_stats_accumulated.csv"
    header = ['Player Name', 'Total Kills', 'Total Deaths', 'Average K/D Ratio', 'Total +/-', 'Total Maps Played']
    
    # Open the accumulated CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write the header
        writer.writerow(header)
        
        # Write the accumulated data
        for player_name, stats in accumulated_data.items():
            avg_kdr = stats['kd_ratio'] / stats['count'] if stats['count'] > 0 else 0
            writer.writerow([
                player_name,
                stats['kills'],
                stats['deaths'],
                avg_kdr,
                stats['plus_minus'],
                stats['maps']
            ])

# Write the accumulated data to the CSV file
write_accumulated_data()