from dash import Dash,dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('projet_dash\creditcard_cleaned.csv', low_memory=False)
data = df[['V1', 'V2', 'V3', 'V4', 'V5']]
app = Dash(__name__)

#a WATERFALL chart
waterfall_fig = go.Figure(go.Waterfall(
    x=["V1", "V2", "V3", "V4", "V5"],
    y=[df['V1'].mean(), df['V2'].mean(), df['V3'].mean(), df['V4'].mean(), df['V5'].mean()],
    connector=dict(line=dict(color="rgb(63, 63, 63)"))
))
waterfall_fig.update_layout(
    title="Waterfall Chart",
    waterfallgap=0.3
)

#the layout of the application
app.layout = html.Div(children=[
    html.H1("Credit Card Data Visualization"),
    dcc.Graph(id='plot', figure=waterfall_fig),
    html.Label("Transactions (TOP 5):"),
    html.Div(id='output'),

    html.H3(
        "Polar Scatter Plot :",
        style={'font-family': 'Arial',   #we put in the style.css file not here
               'text-shadow': '2px 2px #FF0000',  #we put in the style.css file not here
               'text-align': 'center'}  #we put in the style.css file not here
    ),
    dcc.Graph(id='scatterpolar-plot'),
    html.Button('Toggle ScatterPolar', id='toggle-button', n_clicks=0)
])

#ScatterPolar chart setup
r_values = df.mean(axis=0)[:5] 
theta_values = ['V1', 'V2', 'V3', 'V4', 'V5']

polar_fig = go.Figure()
polar_fig.add_trace(go.Scatterpolar(
    r=r_values,
    theta=theta_values,
    mode='markers+lines',
    marker=dict(size=10, color='blue'),
    fill='toself'
))

polar_fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[min(r_values), max(r_values)]),
    ),
    showlegend=False
)

#callback for the visibility of the ScatterPolar
@app.callback(
    Output('scatterpolar-plot', 'figure'),
    Input('toggle-button', 'n_clicks')
)
def toggle_scatterpolar(n_clicks):
    if n_clicks % 2 == 0:
        return {}
    else:
        return polar_fig


if __name__ == '__main__':
    app.run_server(debug=True)
