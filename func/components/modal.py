import dash_bootstrap_components as dbc
from dash_extensions.enrich import html


# Кнопка калибровки магн
def modal():    
    modal = html.Div(
    [
        dbc.Button("Magnetometer calibration", id="magnetometer_calibration", n_clicks=0, outline=True, color="primary",
                   disabled=False),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Magnetometer calibrate")),
                dbc.ModalBody("To calibrate the magnetometer, it is necessary to rotate the sensor along EACH axis (starting with OZ) by 360 degrees 3 times."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="button_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)
    return modal