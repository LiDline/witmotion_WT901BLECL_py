from dash_extensions.enrich import html, DashProxy
import dash_bootstrap_components as dbc
import dash
import os
from dash import DiskcacheManager, CeleryManager


from func.components.callbacks import buttons_main_callback


# Для background
if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)
else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)


from func.components.app_content import  button_page

'''App'''

app = DashProxy(name="WT901BLE", external_stylesheets=[dbc.themes.BOOTSTRAP],
                use_pages=True,
                background_callback_manager=background_callback_manager,
                suppress_callback_exceptions=True # Если не все объекты, на которые ссылаются, сейчас существуют
                )
#___________________________________________________________________________________________________

'''Layout'''

app.layout = html.Div([
	# Header
    dbc.Row([
            dbc.Col(html.H1('WT901BLE'))
            ], className='app-header'),
    # Nav
    dbc.Row([button_page()
            ], className='app-button'),
    dbc.Row([], className='app-hor-line'),
    # Pages
    dbc.Row([dash.page_container
            ], className='app-pages')
    ])

'''callback'''

# Гасим невыбранные кнопки
buttons_main_callback(dash)
    

if __name__ == "__main__":
    app.run_server(port=8050, 
                   debug=True, 
                #    dev_tools_hot_reload=False   # Не проверяет каждые 3 сек: https://question-it.com/questions/13805722/kak-ostanovit-http-zapros-ot-dash_renderer
                   )