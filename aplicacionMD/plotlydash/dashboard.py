"""Instantiate a Dash app."""
import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

def init_dashboard(server):
	"""Create a Plotly Dash dashboard."""
    #app = dash.Dash(__name__)
	app = dash.Dash(__name__,server=server,
	routes_pathname_prefix="/dashapp/",
	external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
	)

	#Creacion del layout 
	app.layout = html.Div([
		html.H1("Algoritmo a priori"),
		html.H2("Subir archivos"),
		dcc.Upload(
			id = 'upload-data',
			children = html.Div([
				'Arrastra y suelta los archivos o ',
				html.A('Selecciona el archivo')
			]),
			style= {
				'width': '98%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
			}, 
			multiple = False,
		),
		html.Div( id = 'output-data-upload' ),
	])
	
	def parse_contents(contents, filename,date):
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
		return html.Div([
			html.H5(filename),
			html.H6(datetime.datetime.fromtimestamp(date)),

			dash_table.DataTable(
				data = df.to_dict('records'),
				columns = [{'name': i, 'id': i } for i in df.columns]
			),

			html.Hr(), #Linea Horizontal 
			html.Div('Raw Content'),
      html.Pre(contents[0:200] + '...', 
				style={
          'whiteSpace': 'pre-wrap',
          'wordBreak': 'break-all'
        })
		])
	@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
	def update_output(list_of_contents, list_of_names, list_of_dates):
		if list_of_contents is not None:
			children = [
      parse_contents(list_of_contents,list_of_names,list_of_dates) 
			]
			return children
	return app.server
	#-----------------------------------