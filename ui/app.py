import utils
from app import create_app

import pymongo
from pymongo import MongoClient
import dash

# dash libs
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import plotly.graph_objs as go
import pandas as pd
from bson import json_util, ObjectId
from pandas.io.json import json_normalize
import json

def mongo_to_dataframe(mongo_data):
    sanitized = json.loads(json_util.dumps(mongo_data))
    print(sanitized)
    normalized = json_normalize(sanitized)
    print(normalized)
    df = pd.DataFrame(normalized)
    return df

def get_lang_models():
    cursor = nifi_collection.distinct( 'model' )
    # this is stupid
    lang_models = pd.DataFrame(cursor, columns = ['model'])
    lang_models = list(lang_models['model'].sort_values(ascending=True))
    return lang_models 

# I dislike mongodb in yet another way.
def get_match_results(lang_model):
    cursor = nifi_collection.find(
       { 'model': lang_model },{ '_id' : 0,'model': 1, 'state': 1, 'input.fileSize': 1, 'input.filename': 1 } 
    )
    return mongo_to_dataframe(cursor)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def onLoad_lang_model_options():
    lang_model_options = (
        [{'label': model, 'value': model}
         for model in get_lang_models()]
    )
    return lang_model_options


def create_shit(server):
    dashapp = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')
    dashapp.css.append_css({
        "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
    })

    dashapp.layout = html.Div([

    # Page Header
    html.Div([
        html.H1('Dashboard - Frankenstein Lives')
    ]),

    # Dropdown Grid
    html.Div([
        html.Div([
            # Select Model Dropdown
            html.Div([
                html.Div('Select Language Model', className='three columns'),
                html.Div(dcc.Dropdown(id='lang_model-selector',
                                      options=onLoad_lang_model_options()),
                         className='nine columns')
            ])

        ], className='six columns'),

        # Empty
        html.Div(className='six columns'),
    ], className='twleve columns'),

    # Match Results Grid
    html.Div([

        # Match Results Table
        html.Div(
            html.Table(id='match-results'),
            className='six columns'
        )

        ], className='six columns')
    ])

    @dashapp.callback(
        Output(component_id='match-results', component_property='children'),
        [
            Input(component_id='lang_model-selector', component_property='value')
        ]
    )
    def load_match_results(lang_model):
        results = get_match_results(lang_model)
        return generate_table(results, max_rows=50)

    return dashapp

if __name__ == "__main__":
   server = create_app()
   MONGO_CONNECT='mongodb://speakeasy:ua8Loo5ux8sax8T@speakeasy-mongo.supermicro5.opswerx.org:65017/speakeasy?authSource=admin'
   db = MongoClient(MONGO_CONNECT).get_database()
   nifi_collection = db.nifi
   dashapp = create_shit(server)
   server_name, server_port, flask_debug = utils.get_flask_server_params()
   server.run(debug=flask_debug, host=server_name, port=server_port)
