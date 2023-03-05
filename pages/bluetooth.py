import dash
from dash import html
import re


from func.func_dash.app_content import header_page

dash.register_page(__name__)

layout = html.Div([
    header_page(re.sub(r'\w+\.', '', __name__)),

    html.Div(children='''
        This is our Bluetooth page content.
    '''),
])