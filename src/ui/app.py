import io
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, send_file, render_template_string
import matplotlib
matplotlib.use('Agg')  # This line is crucial for non-GUI backend
app = Flask(__name__)

# Load your CSV data
# Assuming this file path is accessible, adjust accordingly or use an uploaded file method
df = pd.read_csv('processed.csv', low_memory=False)


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


if __name__ == '__main__':
    app.run(debug=True)
