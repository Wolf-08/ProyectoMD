"""Instantiate a Dash app."""
import base64
import datetime
import io
import plotly
import plotly.express as px
from scipy.spatial import distance
import plotly.graph_objects as go
import numpy as np


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from dash.exceptions import PreventUpdate
#from .layout import html_layout
import pandas as pd
aux  = 1
folder= "C:\\Users\\aleja\\Documents\\ProyectoMD\\aplicacionMD\\static\\files"

def init_dashboard3(server):
	"""Create a Plotly Dash dashboard."""
    #app = dash.Dash(__name__)
	app = dash.Dash(__name__,server=server,
	routes_pathname_prefix="/distancias/",
	external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
	)

	#custom html layout 
	#app.index_string = html_layout
	#Creacion del layout 
	app.layout = html.Div([
		html.H1("Algoritmo de Distancias"),
		html.H2("Subir archivos"),
		dcc.Upload(
			id = 'upload-data',
			children = html.Div([
				'Arrastra y suelta los archivos o ',
				html.A('Selecciona el archivo')
			]),
			style= {
				'width': '50%',
        'height': '50px',
        'lineHeight': '50px',
        'borderWidth': '2px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
			}, 
			multiple = False,
		),
		#html.Div([
		#	html.Button(id = 'submit', n_clicks = 0, children = 'Mostrar datos'),
		#]),
		html.Div([ html.H3("Distancias"),
      #html.Button('Cargar Archivo', id='loadFile', n_clicks=0,style={'width': '25%','margin': '3%'}),
	  html.Div( id = 'output-data-upload'),
		]),
		dcc.Tabs(id = 'tabs',value = 'tab-1', children=[
			#dcc.Tab(label = 'Datos',value = 'tab1',children=[
				dcc.Tab(label='Distancias', value='tab',children=[
					dcc.Dropdown(id='distancia',
					options=[
						      {'label': 'Chebyshev', 'value': 'chebyshev'},
									{'label': 'Cityblock', 'value': 'cityblock'},
                  {'label': 'Euclidean', 'value': 'euclidean'}
					],
          value='euclidean',style={'width': '50%','margin': '2%'}),
          html.Button('Mostrar Matriz', id='executeCorr', n_clicks=0,style={'width': '25%','margin': '3%','background-color':'black','color':'white'}),
					html.Div(id="distanciaMatrix"),
				]),     	
		]),

	])
	
	def parse_contents(contents, filename):
		content_type, content_string = contents.split(',')
		decoded = base64.b64decode(content_string)
		try:
			if 'csv' in filename:
				df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
			elif 'txt' in filename:
				df = pd.read_table(io.StringIO(decoded.decode('utf-8')))
		except Exception as e:
			print(e)
			return html.Div([
				'Hubo un error cargando el archivo, Formatos permitidos .csv, .txt'
			])
		return df
	#def rules(df,support,confidence,lift,length):
	#Callback recibe el archivo y saca los datos,contenido,nombre
	@app.callback(Output('output-data-upload', 'children'),
							[Input('upload-data','contents'),
              State('upload-data', 'filename')])
	def update_output(content, name):
		if content is not None:
			datos = parse_contents(content,name)
			return html.Div([
			html.H5(name),
			dash_table.DataTable(
				#create a dictionary 
				data = datos.to_dict('records'),
				columns = [{'name': i, 'id': i } for i in datos.columns],
				page_size = 20,
				style_table={'overflowX': 'auto'},
				style_cell={
        'height': 'auto',
        # all three widths are needed
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'normal',
				'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'},
				fixed_rows={'headers': True},
				style_header={'backgroundColor': 'rgb(30, 30, 30)'},
			),
			html.Div([
			html.P("Numero total de Datos: Rows " + str(datos.shape[0]) + " Column: " + str(datos.shape[1]))
			])
		])
			
	# #Callback para recibir valores 
	@app.callback(Output('distanciaMatrix','children'),
							[
							Input('upload-data','contents'),
							Input('distancia','value'),
							Input('executeCorr','num_clicks'),
							State('upload-data','filename'),
							]
							)
	def update_data(contents,distancia,num_clicks,filename):
		table = html.Div()
		#figure = dcc.Graph()
		global aux
		if contents:
			aux = aux + 1
		
			df = parse_contents(contents,filename)
			df = df.set_index(df.columns[0])

			index = df.index[:].tolist()
			df = df.values.tolist()
			df= [df[i] + [index[i]]  for i in range(0,len(df))]

			l = []
			for i in df :
				ll = []
				for j in df:
					if distancia == 'euclidean':
						ll.append(round(distance.euclidean(i,j),2))
					elif distancia == 'cityblock':
						ll.append(round(distance.cityblock(i,j),2))
					elif distancia == 'chebyshev':
						ll.append(round(distance.chebyshev(i,j),2))
				l.append(ll)
      
			df = pd.DataFrame(l)
			table = html.Div (
				[
					dash_table.DataTable(
						data = df.to_dict("rows"),
            columns=[{"name": str(i), "id": str(i),"type":"numeric"} for i in df.columns],
            fixed_rows={'headers': True},
						style_table={'overflowX': 'auto','overflowY': 'auto'},
						style_cell={
						'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
						'overflow': 'scroll'  }
					),
				]
			)
		return table
	return app.server
	#-----------------------------------