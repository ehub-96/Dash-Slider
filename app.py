#Libraries

from signal import set_wakeup_fd
import pandas as pd     
import plotly           
import plotly.express as px
import dash         
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc 
import math

# Dataset

df = pd.read_csv("df.csv")
df ['Bands Formed'].astype(int)
df['Year'].astype(int)




# App

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
  

# Layout

app.layout = html.Div(
    [
        html.H1("Number of Bands Formed by Year", style={'textAlign': 'center'}),

        html.Label("Years"),
        dcc.Slider(min=df['Year'].min(),
                   max=df['Year'].max(),
                   step=3,
                   tooltip={"placement": "bottom", "always_visible": True},
                   updatemode='drag',
                   persistence=True,
                   persistence_type='session', # 'memory' or 'local'
                   id="my-slider"
        ),

        html.Label("Bands Formed"),
        dcc.RangeSlider(min=df['Bands Formed'].min(),
                        max=math.ceil(df['Bands Formed'].max()),
                        step=1,
                        value=[1,8],
                        tooltip={"placement": "bottom", "always_visible": True},
                        updatemode='drag',
                        id="my-rangeslider"
        ),

        dcc.Graph(id='my-graph')
    ],
    style={"margin": 30}
)


@app.callback(
    Output('my-graph', 'figure'),
    Input('my-slider', 'value'),
    Input('my-rangeslider', 'value')
)
def update_graph(n_storms, dollar_range):
    bool_series = df['Year'].between(0, n_storms, inclusive='both')
    df_filtered = df[bool_series]
    fig = px.bar(data_frame=df_filtered,
                 x='Year',
                 y='Bands Formed',
                 range_x=[df['Year'].min(), df['Year'].max()],
                 range_y=[df['Bands Formed'].min()-1, df['Bands Formed'].max()+1])

    bool_series2 = df['Bands Formed'].between(dollar_range[0], dollar_range[1], inclusive='both')
    filtered_year = df[bool_series2]['Year'].values
    fig["data"][0]["marker"]["color"] = ["black" if c in filtered_year else "red" for c in fig["data"][0]["x"]]

    return fig


if __name__ == '__main__':
	app.run_server()
