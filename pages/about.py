import dash
from dash import html
import re
from dash_extensions import WebSocket


from func.components.app_content import header_page


dash.register_page(__name__, path='/')

layout = html.Div([
    header_page(re.sub(r'\w+\.', '', __name__)),

    html.Div(children='''
        This is about page content.
    ''')
])