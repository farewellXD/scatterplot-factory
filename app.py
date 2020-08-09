import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


# app setting

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = '桃園工業區分析做圖'


# 資料處理：7月份PM2.5的Scatter Plot，x軸為時間(每日的24小時)，y軸為濃度值

url = 'https://raw.githubusercontent.com/farewellXD/scatterplot-factory/master/combine_select_point.csv'
df = pd.read_csv(url, encoding='big5')


df.TIME = pd.to_datetime(df.TIME)
df['HOUR'] = df.TIME.dt.hour

data_g = df.groupby('HOUR').agg({'VALUE': np.median}).reset_index()

factory_name = df['FNAME'].unique()



app.layout = html.Div([
    html.Label('請選擇工業區'),
    dcc.Dropdown(
        id = 'factory_input',
        options=[{'label': i, 'value': i} for i in factory_name],
        value=[factory_name[0], factory_name[1], factory_name[2]],
        multi=True
    ),

    dcc.Graph(
        id='air_pm2_5',
    ),
    
    html.Div(
        [
            dt.DataTable(
            rows=data_g.to_dict('records'),
            columns=data_g.columns,
            row_selectable=True,
            filterable=True,
            sortable=True,
            max_rows_in_viewport=5,
            #selected_row_indices=list(data_g.index),  # all rows selected by default
            )
        ]
    )
]
)

@app.callback(
    Output(component_id='air_pm2_5', component_property='figure'),
    [Input(component_id='factory_input', component_property='value')]
)

def update_graph(value):

    fig = px.scatter(df[df['FNAME'].isin(value)] , x='HOUR', y='VALUE')
    fig.update_layout(
        yaxis=dict(range=[0,200]),
        xaxis=dict(range=[0,24])

    )
    fig.update_xaxes(tick0=0, dtick=1)

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)