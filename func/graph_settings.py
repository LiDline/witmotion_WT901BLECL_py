import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Шаблон линий графиков
def create_line(fig, row, col=1, showlegend = True):
    names = ['OX', 'OY', 'OZ']
    color = ['red', 'blue', 'green']
    # Сразу вызовем по 3 линии на каждый график
    for i in range(3): 
        fig.add_scatter(line=dict(color=color[i]), mode = 'lines', legendgroup = f'group{i}',
        showlegend=showlegend, name = names[i], row=row, col=col)

# Общие настройки графика
def graph_settings():
    fig = go.FigureWidget(make_subplots(rows=3, cols=1, subplot_titles=("Линейные ускорения", "Угловые скорости", "Углы")))

    # Создадим линии для каждого графика
    create_line(fig, 1) 
    create_line(fig, 2, showlegend = False) 
    create_line(fig, 3, showlegend = False)

    # Оформление
    fig.update_layout(autosize=False, height=650, width=1000,     # Размер окна в пикселях
        margin=dict(l=70,r=50,b=0,t=75,pad=0))

    # Update xaxis properties
    fig.update_xaxes(visible=True, title_text= 't, сек', row=1, col=1)
    fig.update_xaxes(visible=True, title_text= 't, сек', row=2, col=1)
    fig.update_xaxes(visible=True, title_text= 't, сек', row=3, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="a, м/с2", row=1, col=1)
    fig.update_yaxes(title_text="w, °/с", row=2, col=1)
    fig.update_yaxes(title_text="A, °", row=3, col=1)


    fig.update_layout(           #Позиционирование заголовка
               title={
                    'text': f"Получаемые характеристики датчика WT901BLE; дата: {datetime.datetime.now().replace(microsecond=0)}",
                    'y':0.97, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    return fig