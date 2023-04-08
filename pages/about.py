import dash
from dash import html
import re


dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1(children='''
        This is about page content.
    '''),
    html.Br(),
    html.H4('''
            1. This application was created as part of an introduction to connecting to a sensor and creating a web application on plotly dash.
            '''),
    html.H4('''
            2. The application includes searching for WT901 sensors, connection, basic settings, graphical output of the converted results and saving them in res.csv.
        '''),
    html.H4('''
            3. Connecting via Bluetooth has a slight delay, so please take your time when using this method (bug: the work of the field for selecting available sensors is not working. Solution: Don't click the Start button right away). USB connection works without problems.
        '''),
])