"""Instantiate a Dash app."""
import base64
import datetime
import io
import plotly
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
def init_dashboard2(server):
	"""Create a Plotly Dash dashboard."""
    #app = dash.Dash(__name__)
	app = dash.Dash(__name__,server=server,
	routes_pathname_prefix="/correlacion/",
	external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
	)
	#custom html layout 
	#app.index_string = html_layout
	#Creacion del layout 
	app.layout = html.Div([
		html.H1("Algoritmo de Correlacion"),
		html.H2("Sube tu archivo"),
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
		html.Div([ html.H3("Correlacion")]),	
			# dcc.Tabs(id = 'tabsControlInput',value='tab-1',
			# children=[
			# 	dcc.Dropdown(
			# 		id = 'correlacion',
			# 		options=[
			# 			{'label': 'Pearson', 'value': 'pearson'},
      #       {'label': 'Kendall', 'value': 'kendall'},
      #       {'label': 'Spearman', 'value': 'spearman'}
			# 		],
			# 		value='pearson',style={'width': '50%','margin': '2%'}),
		html.Div( id = 'output-data-upload' ),
		html.Div( id = 'output-data-apriori'),
	])

	def parse_contents(contents, filename):
		content_type, content_string = contents.split(',')
		decoded = base64.b64decode(content_string)
		try:
			if 'csv' in filename:
				df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
			elif 'txt' in filename:
				 df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
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
	@app.callback(Output('output-data-apriori','children'),
							[Input('upload-data','contents'),
							Input('submit_button','n_clicks'),
              State('upload-data', 'filename'),
							State('support','value'),
							State('confidence','value'),
							State('lift','value'),
							State('length','value')])
	def update_data(contents,num_clicks,name,support,confidence,lift,length):
		if contents:
			df = parse_contents(contents,name)
			if (support and confidence and lift and length) is None:
				raise PreventUpdate
			else:
				registros = []
				for i in range(df.shape[0]):
	 	 			registros.append([str(df.values[i,j]) for j in range(0,df.shape[1])])
		
				Reglas = apriori (
				registros,
				min_support = support,
				min_confidence = confidence,
				min_lift = lift ,
				min_length = length,)
				Resultados = list(Reglas)
				print(Resultados[0])
				return html.Div([
					html.H3("Valores registrados para crear las reglas"),
					html.P(str(support)),
					html.P(str(confidence)),
					html.P(str(lift)),
					html.P(str(length)),
					# dash_table.DataTable(
					# 	data =  
					# 	columns = 
					# )
					])
	return app.server
	#-----------------------------------