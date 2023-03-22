import dash_bootstrap_components as dbc
from dash_extensions.enrich import html
import dash


# Переключение страниц
def button_group():
    bg = dbc.ButtonGroup(
    [
        dbc.Button(f"{page['name']}", outline=True, color="primary", href=page["relative_path"]) 
        for page in dash.page_registry.values()
    ]
)
    return bg


# Заглавный текст страниц
def header_page(name):
    if name.lower() != 'home':
        return html.H2(f'This is the page for connecting via {name}')
    return html.H2(f'This is our {name} page')
