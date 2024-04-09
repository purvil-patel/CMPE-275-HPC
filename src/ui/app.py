import glob
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, send_file, render_template_string
import matplotlib
from flask import url_for

matplotlib.use('Agg')  # This line is crucial for non-GUI backend
app = Flask(__name__)


def clean_csv(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            corrected_line = line.strip()  # Remove leading/trailing whitespace
            # Simple check for unmatched quotes (very basic, might need adjustment)
            if corrected_line.count('"') % 2 != 0:
                corrected_line = corrected_line.replace('"', '')
            outfile.write(corrected_line + '\n')

input_file_path = '../../final_data/combined_cleaned_data.csv'
output_file_path = '../../final_data/cleaned_file.csv'
clean_csv(input_file_path, output_file_path)
# Load your CSV data
# Assuming this file path is accessible, adjust accordingly or use an uploaded file method
df = pd.read_csv('../../final_data/cleaned_file.csv', low_memory=False, on_bad_lines='skip')


@app.route('/')
def index():
    # HTML content with links to the plot sections
    return '''
    <html>
        <head>
            <title>Plot Server</title>
        </head>
        <body>
            <h1>Welcome to the Plot Server!</h1>
            <p>Select a category to view related plots:</p>
            <ul>
                <li><a href="/timeplot">Time Analysis</a></li>
                <li><a href="/geoplot">Geographic Analysis</a></li>
                <li><a href="/performance">Performance Analysis</a></li>
            </ul>
        </body>
    </html>
    '''


@app.route('/timeplot')
def timeplot():
    # HTML template for displaying time analysis plots and explanations
    time_analysis_html = '''
    <html>
        <head>
            <title>Time Analysis Plots</title>
        </head>
        <body>
            <h1>Time Analysis Plots</h1>
            <!-- Placeholders for plot images and explanations -->
            <div>
    <h2>Monthly Analysis</h2>
    <img src="/time/month" alt="Monthly Violations Plot">
    <p>Brief explanation of violations by month.</p>
</div>
<div>
    <h2>Weekly Analysis</h2>
    <img src="/time/week" alt="Weekly Violations Plot">
    <p>Brief explanation of violations by week number.</p>
</div>
<div>
    <h2>Daily Analysis</h2>
    <img src="/time/day" alt="Daily Violations Plot">
    <p>Brief explanation of violations by day of the week.</p>
</div>

            <a href="/">Back to Homepage</a>
        </body>
    </html>
    '''
    return render_template_string(time_analysis_html)


@app.route('/geoplot')
def geoplot():
    # HTML template for displaying geographic analysis plots and explanations
    geo_analysis_html = '''
    <html>
        <head>
            <title>Geographic Analysis Plots</title>
        </head>
        <body>
            <h1>Geographic Analysis Plots</h1>
            <!-- Placeholders for plot images and explanations -->
            <div>
                <h2>Violation Location Analysis</h2>
                <img src="/geo/location" alt="Violation Location Analysis Plot">
                <p>Brief explanation of the Violation Location Analysis Plot.</p>
            </div>
            <div>
                <h2>Borough Comparison</h2>
                <img src="/geo/borough" alt="Borough Comparison Plot">
                <p>Brief explanation of the Borough Comparison Plot.</p>
            </div>
            <a href="/">Back to Homepage</a>
        </body>
    </html>
    '''
    return render_template_string(geo_analysis_html)


@app.route('/performance')
def performance():
    # Get a list of csv files to process, excluding 'processed.csv'
    csv_files = get_csv_files('.')
    plot_data = []

    static_folder = 'static'
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    # Process each csv file
    for idx, file_path in enumerate(csv_files):
        # Load the dataframe and determine the number of processes
        dataframe, num_processes = load_csv(file_path)

        # Generate the plot and store it in a BytesIO buffer
        plot_buf = plot_records_vs_time(dataframe, num_processes)

        # Create a unique endpoint for this particular plot
        plot_endpoint = f'performance_plot_{idx}'

        # Define the endpoint function that will serve the plot
        app.view_functions[plot_endpoint] = lambda: send_file(
            io.BytesIO(plot_buf.getvalue()),
            attachment_filename=f"plot{idx}.png",
            mimetype='image/png'
        )

        # Inside the loop, use this block to save the images
        plot_filename = f'plot{idx}.png'
        plot_path = os.path.join(static_folder, plot_filename)
        with open(plot_path, 'wb') as plot_file:
            plot_file.write(plot_buf.getbuffer())

        # Add the URL for the static plot image to the list
        plot_data.append(url_for('static', filename=plot_filename))

    # Render the template with the list of plot urls
    return render_template_string(performance_analysis_html, plot_urls=plot_data)


# HTML template for the performance analysis page
performance_analysis_html = '''
<html>
    <head>
        <title>Performance Analysis Plots</title>
    </head>
    <body>
        <h1>Performance Analysis Plots</h1>
        <div>
            {% for plot_url in plot_urls %}
            <img src="{{ plot_url }}" alt="Performance Plot">
            {% endfor %}
        </div>
        <a href="/">Back to Homepage</a>
    </body>
</html>
'''


def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

# Trend Analysis: Monthly, Weekly, Daily


@app.route('/time/month')
def plot_month():
    local_df = df.copy()
    local_df['Issue Date'] = pd.to_datetime(
        local_df['Issue Date'], errors='coerce')
    # Filter out NaT values
    local_df = local_df.dropna(subset=['Issue Date'])
    local_df['Month'] = local_df['Issue Date'].dt.month
    monthly_counts = local_df.groupby('Month').size()

    fig, ax = plt.subplots()
    monthly_counts.plot(kind='bar', ax=ax)
    ax.set_title('Violations by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Violations')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')


@app.route('/time/week')
def plot_week():
    local_df = df.copy()
    local_df['Issue Date'] = pd.to_datetime(
        local_df['Issue Date'], errors='coerce')
    # Filter out NaT values
    local_df = local_df.dropna(subset=['Issue Date'])
    local_df['Week'] = local_df['Issue Date'].dt.isocalendar().week
    weekly_counts = local_df.groupby('Week').size()

    fig, ax = plt.subplots()
    weekly_counts.plot(kind='bar', ax=ax)
    ax.set_title('Violations by Week Number')
    ax.set_xlabel('Week Number')
    ax.set_ylabel('Number of Violations')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')


@app.route('/time/day')
def plot_day():
    local_df = df.copy()
    local_df['Issue Date'] = pd.to_datetime(
        local_df['Issue Date'], errors='coerce')
    # Filter out NaT values
    local_df = local_df.dropna(subset=['Issue Date'])
    local_df['Day'] = local_df['Issue Date'].dt.dayofweek
    daily_counts = local_df.groupby('Day').size()

    fig, ax = plt.subplots()
    daily_counts.plot(kind='bar', ax=ax)
    ax.set_title('Violations by Day of the Week')
    ax.set_xlabel('Day of the Week (0=Monday, 6=Sunday)')
    ax.set_ylabel('Number of Violations')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')

# Geographic Analysis: Locations, Streets, Boroughs


@app.route('/geo/location')
def plot_location():
    top_locations = df['Violation Location'].value_counts().head(10)

    fig, ax = plt.subplots()
    top_locations.plot(kind='bar', ax=ax)
    ax.set_title('Top 10 Violation Locations')
    ax.set_xlabel('Location')
    ax.set_ylabel('Number of Violations')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')


@app.route('/geo/street')
def plot_street():
    top_streets = df['Street Name'].value_counts().head(10)

    fig, ax = plt.subplots()
    top_streets.plot(kind='bar', ax=ax)
    ax.set_title('Top 10 Violation Streets')
    ax.set_xlabel('Street Name')
    ax.set_ylabel('Number of Violations')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')


@app.route('/geo/borough')
def plot_borough():
    top_boroughs = df['Violation County'].value_counts().head(10)

    fig, ax = plt.subplots()
    top_boroughs.plot(kind='bar', ax=ax)
    ax.set_title('Top 10 Violation Boroughs')
    ax.set_xlabel('Borough')
    ax.set_ylabel('Number of Violations')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')

# Performance Analysis: Records Processed Over Time


def get_csv_files(directory, exclude_file='processed.csv'):
    # This function will find all csv files in the given directory excluding the 'processed.csv'
    return [f for f in glob.glob(f"{directory}/*.csv") if exclude_file not in f]


def determine_number_of_processes(dataframe):
    # The number of processes will be one less than the number of columns
    # because the first column is for seconds
    return dataframe.shape[1] - 1


def plot_records_vs_time(dataframe, num_processes):
    # Plotting function suitable for Flask, which saves the plot to a BytesIO buffer and returns it
    fig, ax = plt.subplots()
    for i in range(num_processes):
        ax.plot(dataframe['Seconds'],
                dataframe[f'RecordsProcessed-P{i}'], label=f'Process P{i}')
    ax.set_xlabel('Time (Seconds)')
    ax.set_ylabel('Number of Records Processed')
    ax.set_title('Records Processed Over Time by Each Process')
    ax.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


def load_csv(file_path):
    dataframe = pd.read_csv(file_path, low_memory=False)
    num_processes = determine_number_of_processes(dataframe)
    return dataframe, num_processes


if __name__ == '__main__':
    app.run(debug=True)
