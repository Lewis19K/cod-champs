from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)

# Route for the homepage
@app.route('/', methods=['GET'])
def index():
    # Get the list of CSV files from the 'data' directory, excluding the accumulated file
    files = [f for f in os.listdir('data') if f.endswith('.csv') and 'accumulated' not in f]
    
    # Extract years and modes from the filenames
    years = sorted(set([file.split('_')[2] for file in files]))  # Extract the year
    modes = sorted(set([file.split('_')[3].split('.')[0] 
                        for file in os.listdir('data') 
                        if file.endswith('.csv') and len(file.split('_')) > 3
    ]))
    
    # Check if "All Years" is selected
    if request.args.get('year') == 'all':  # If 'All Years' is selected
        # Load accumulated data
        accumulated_data = pd.read_csv('data/cod_stats_accumulated.csv')

        # Reset the index and add 1 to the index to start from 1
        accumulated_data.reset_index(drop=True, inplace=True)
        accumulated_data.index += 1
        return render_template('index.html', years=years, modes=modes, data=accumulated_data.to_html(classes='table'))
    
    # If a specific year and mode are selected
    year = request.args.get('year')
    mode = request.args.get('mode')
    
    if year and mode:
        file = f"data/cod_stats_{year}_{mode}.csv"
        if os.path.exists(file):
            data = pd.read_csv(file)
            
            # Reset the index and add 1 to the index to start from 1
            data.reset_index(drop=True, inplace=True)
            data.index += 1
            
            return render_template('index.html', years=years, modes=modes, data=data.to_html(classes='table'))

if __name__ == '__main__':
    app.run(debug=True)