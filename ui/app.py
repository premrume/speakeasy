import utils
from app import create_app

import logging.config
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

import pymongo
from pymongo import MongoClient
import dash

# dash libs
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go
import pandas as pd
from bson import json_util, ObjectId
from pandas.io.json import json_normalize
import json

def mongo_to_dictionary(mongo_data):
    sanitized = json.loads(json_util.dumps(mongo_data))
    normalized = json_normalize(sanitized, sep='_')
    records = normalized.to_dict('records')
    return records

def mongo_to_dataframe(mongo_data):
    sanitized = json.loads(json_util.dumps(mongo_data))
    normalized = json_normalize(sanitized)
    df = pd.DataFrame(normalized)
    return df

# I dislike mongodb in yet another way.
def get_match_results():
    cursor = nifi_collection.find(
        {}, { '_id': 0, 'model': 1, 'result': 1, 'state': 1, 'input.filename': 1 }
    )
    return mongo_to_dictionary(cursor)

def create_dash(server):
    # I have this commented out of the html, it is failing
    dashapp = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

    # todo bring this into the project - cannot run with http in demo.
    #  found no easy-peasy way to do this in dash
    dashapp.css.append_css({
        "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
    })

    dashapp.layout = html.Div(
      html.Div([
        html.H1('Speakeasy'),
        html.H2('Dashboard'),
        html.H3('** Live Feed every 30 milliseconds **'),
        dt.DataTable(
            rows=[{}], # initialise the rows
            filterable=True,
            sortable=True,
            id='table-results'
        ),
        dcc.Graph(id='graph1'),
        dcc.Interval(
            id='interval-component',
            interval=30*1000, # in milliseconds
            n_intervals=0
        )
      ])
    )

    @dashapp.callback(
        Output('table-results', 'rows'),
        [
            Input('interval-component', 'n_intervals')
        ]
    )
    def load_match_results(ignoreme):
        results = get_match_results()
        return results

    @dashapp.callback(
        Output('graph1', 'figure'),
        [
            Input('interval-component', 'n_intervals')
        ]
    )
    def load_graph1_results(ignoreme):
        dashapp.logger.info('aaaaaaaaaaaaaaaaaaa');
        filtered_results = nifi_collection.find(
            {'metadata.keywords': {'$nin': [ None, '']}},
            {'source': 1, 'metadata.keywords': 1 }
        )
        print(filtered_results)
        print('bbbbbbbbbbbbbbbbb')
        filtered_dict = mongo_to_dictionary(filtered_results)
        print(filtered_dict)
        print('ccccccccccccccccc')
        word_file = pd.DataFrame()
        for record in filtered_dict:
            print('xxxxxxxxxxxx')
            print(record)
            for kw in record['metadata_keywords'].split(','):
               print('yyyyyyyyyyyy')
               print(kw)
               row = {'watch': kw, 'filename': record['source'], 'id': record['_0']} 
               word_file = word_file.append(row, ignore_index=True)

        counts=word_file.groupby(['watch']).size().reset_index(name='count')
        top_10=counts.nlargest(10, 'count')
        watch_list = []
        count_list = []
        file_list = []
        for index, row in top_10.iterrows():
            watch_list.insert(index, row['watch'])
            count_list.insert(index, row['count'])
            matches = []
            for i, r in word_file.iterrows():
              if (row['watch'] == r['watch']): 
                 matches.append( '('+ r['id']+') '+r['filename'] )
            file_list.insert(index, matches)

        barSet = go.Bar(
            x=watch_list,
            y=count_list,
            text=file_list,
            marker=dict(
                color='#17BECF',
            ),
            opacity=0.6
        )
        figure={
            'data': [barSet],
            'layout': go.Layout(
                    title='10 Most Popular Keywords (All Time)'
            )
        }
        return figure

    return dashapp

if __name__ == "__main__":
   server = create_app()
   MONGO_CONNECT = utils.get_env_var_setting('MONGO_CONNECT', 'youloose')
   db = MongoClient(MONGO_CONNECT).get_database()
   nifi_collection = db.nifi
   dashapp = create_dash(server)
   server_name, server_port, flask_debug = utils.get_flask_server_params()
   server.run(debug=flask_debug, host=server_name, port=server_port)
