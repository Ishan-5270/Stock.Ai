import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

jumbotron = dbc.Jumbotron(
    [
        html.H1("Stock.ai", className="display-3"),
        html.P(
            "Built with average and exponential moving average prediction models. ",
     
            className="lead",
        ),
        html.Hr(className="my-2"),
        
    ]
)

def make_options():
    df = pd.read_csv('listitems.csv')
    # print(df)   
    options_1 = []
    for i, row in df.iterrows():
        row_name = row["0"]
        dictionary_var = {'label': row_name, 'value': row_name}
        options_1.append(dictionary_var)
    return options_1

## function to read selected stock 
## Input: Stock name, Output: df
## 'AAPL'
def read_stock(stock_name):
    file_name = "C:/Users/DELL/OneDrive/Desktop/CS project/stocks/" + stock_name + ".csv"
    df = pd.read_csv(file_name)
    df['Date'] =  pd.to_datetime(df['Date'])
    print(df.head())
    return df
df = read_stock("AAPL")
    # Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['High'],
                    mode='lines',
                    name='high'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Low'],
                    mode='lines',
                    name='Low'))

def stock_predictions(df):
    ma = 0
    gamma = 0.1
    new_array = []
    for index, day in df.iterrows():
        x = day['Mid']
        ma = gamma*x + (1-gamma)*ma
        new_array.append(ma)
    df['Predicted_2'] = new_array
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Mid'],
                    mode='lines',
                    name='mid'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Predicted_2'],
                    mode='lines',
                    name='predicted_2'))
    return fig

app.layout = html.Div(children=[
    jumbotron,    
    dcc.Dropdown(
        id='dropdown',
        options= make_options(),
        value='',
        className="mx-3"
    ), 
    html.Label ([" If you are unsure about the stock name, search the stock ticker symbol on google"]),
    dbc.Card( 
    dbc.CardBody(
        [
            dcc.Graph(
            id = 'graph_id',
            figure=fig),
        
        dcc.Graph(
            id = 'graph_id1',
            figure=fig) ] ),className= "mx-4 my-4")
])


@app.callback(
    [Output(component_id='graph_id', component_property='figure'),
    Output(component_id='graph_id1', component_property='figure')],
    [Input(component_id='dropdown', component_property='value')]
    
)
def update_output_div(input_value):
   print (input_value)
   if (input_value == ""):
       raise dash.exceptions.PreventUpdate
   df = read_stock(input_value)
   df.head()
   fig = go.Figure()
   df['Mid'] = (df['High'] + df['Low'])/2
   fig.add_trace(go.Scatter(x=df['Date'], y=df['High'],
                    mode='lines',
                    name='high'))
   fig.add_trace(go.Scatter(x=df['Date'], y=df['Low'],
                    mode='lines',
                    name='Low'))
   figure_2 = stock_predictions(df)
   return fig,figure_2

if __name__ == '__main__':
    app.run_server(debug=True)