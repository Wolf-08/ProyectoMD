"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from aplicacionMD import routes 
#from .data import create_dataframe
#from .layout import html_layout



def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
    )
    #formato,filename=routes.dash1
    # Load DataFrame
    # archivo=str(filename)
    # print(archivo)
    # rutaFile="C:\\Users\\aleja\\Documents\\ProyectoMD\\aplicacionMD\\static\\files" + archivo
    # Transacciones=[]
    # Datos=pd.read_csv(rutaFile,header=None)
    # for i in range(0,7501):
    #  Transacciones.append([str(Datos.values[i,j]) for j in range (0,20)]) 
  
    # Reglas = apriori(Transacciones, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2) 
    # Resultado = list(Reglas) 
    # print(Resultado[0])
    #df = create_dataframe()

    # Custom HTML layout
    #dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[
        html.H2(children='Hello Dash'),
        dcc.Graph (
          id = 'mi_primer_Grafico',
          figure = {
            'data' : [
              {'x': [1,2,3], 'y':[8,12,21], 'type':'bar', 'name':'bar'}
            ],
            'layout' : {
              'title':'Mi primer grafico'
            }
          }
        )
        ]
  
    )
    return dash_app.server


# def create_data_table(df):
#     """Create Dash datatable from Pandas DataFrame."""
#     table = dash_table.DataTable(
#         id="database-table",
#         columns=[{"name": i, "id": i} for i in df.columns],
#         data=df.to_dict("records"),
#         sort_action="native",
#         sort_mode="native",
#         page_size=300,
#     )
#     return table