# Call of Duty Champions Player Statistics from 2022 to 2024

## Description

Project to analyse the call of duty world champions player data.

## Features

1. A scraping.py script:
   - Fetch player statistics from the Call of Duty Esports Wiki
2. Flask App (app.py) and HTML template (templates/index.html):
   - Filters data by year and mode
   - Displays player statistics in a table

## Requirements

- Python 3.x
- BeautifulSoup
- Requests
- Pandas
- Flask
- Bootstrap

## Usage

1. Clone the repository to your local machine.
2. Install the required Python packages using pip.
3. (Not necessary because the data is already included) run the scraping.py script to fetch the player statistics.
4. Run the app.py script to start the Flask app.
5. Open the browser and navigate to [http://localhost:5000] to view the player statistics.
6. You can filter the data by year and mode using the dropdown menus.

## Next Steps

- Add sorting functionality to the table.
- Add visualizations using Plotly or Matplotlib.
- Analyze the data further to gain insights into the player performance.
- Improve frontend design and user experience.
