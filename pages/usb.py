import dash


from func.components.layout import layout
from func.components.callbacks import callback


dash.register_page(__name__)
# ___________________________________________________________________________________________________

'''layout'''

layout = layout(__name__)
# ___________________________________________________________________________________________________

'''Callback'''

callback(dash)