import requests
import csv
from bs4 import BeautifulSoup

# URLs of the player statistics for each year
urls = {
    2022: 'https://cod-esports.fandom.com/wiki/Call_of_Duty_League_Championship_2022/Player_Statistics',
    2023: 'https://cod-esports.fandom.com/wiki/Call_of_Duty_League_Championship_2023/Player_Statistics',
    2024: 'https://cod-esports.fandom.com/wiki/Call_of_Duty_League_Championship_2024/Player_Statistics'
}

# Function to write the data to a CSV file
def write_to_csv(year, mode, data):
    filename = f"cod_stats_{year}_{mode}.csv"
    header = ['Player Name', 'Kills', 'Deaths', 'K/D Ratio', '+/-', 'Maps Played']
    
    # Open the CSV file in append mode to add data
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write the header if it's a new file
        if f.tell() == 0:
            writer.writerow(header)
        
        # Write the statistics data
        writer.writerows(data)

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
                        k = columns[2].get_text(strip=True)  # Kills
                        d = columns[3].get_text(strip=True)  # Deaths
                        kdr = columns[4].get_text(strip=True)  # K/D Ratio
                        plus_minus = columns[5].get_text(strip=True)  # +/- (Adjust if necessary)
                        maps = columns[6].get_text(strip=True)  # Maps played (Adjust if necessary)
                        
                        # Store the data for the current mode
                        mode_data.append([player_name, k, d, kdr, plus_minus, maps])
                
                # Write the data for the current mode to CSV
                write_to_csv(year, mode, mode_data)
        else:
            print(f"Table not found for {year}")
    else:
        print(f"Failed to retrieve data for {year} - Status code: {response.status_code}")