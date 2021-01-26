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
import dash_bootstrap_components as dbc
import dash_table
from dash.exceptions import PreventUpdate
import pandas as pd

aux  = 1
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
		html.Div([ html.H3("Correlacion"),
      #html.Button('Cargar Archivo', id='loadFile', n_clicks=0,style={'width': '25%','margin': '3%'}),
	  html.Div( id = 'output-data-upload'),
		]),
		dcc.Tabs(id = 'tabs',value = 'tab-1', children=[
			#dcc.Tab(label = 'Datos',value = 'tab1',children=[
				dcc.Tab(label='Correlacion', value='tab-1',children=[
					dcc.Dropdown(id='metodoCorr',
					options=[
						      {'label': 'Pearson', 'value': 'pearson'},
									{'label': 'Kendall', 'value': 'kendall'},
                  {'label': 'Spearman', 'value': 'spearman'}
					],
          value='pearson',style={'width': '50%','margin': '2%'}),
          html.Button('Gráfica', id='executeCorr', n_clicks=0,style={'width': '25%','margin': '3%','background-color':'black','color':'white'}),
					dcc.Tabs(id='display-call',value = 'subtab',
					children=[
						dcc.Tab(label = 'Matriz de Correlacion',value = 'matriz',children=[
							html.Div(id = "crossMatrix")]),
						dcc.Tab(label = 'Grafica de Calor', value = 'grafica', children= [
							html.Div(id="graphCrossMatrix")]),
					]),

				]),     	
		]),
		# html.Button('Ejecutar', id='executeCorr', n_clicks=0,style={'width': '25%','margin': '3%'}),
		# dcc.Tabs(id="subtabs-1",value="subtab-1",
		# children = [
    #             dcc.Tab(label='Matriz de correlación',value='subtab-5',children=[
    #             html.Div(id="crossMatrix"),]),                            
    #             dcc.Tab(label='Grafica', value='subtab-2',children=[
    #             html.Div(id="graphCrossMatrix"),]),
    #             ]),
		# ),

		#html.Div( id = 'output-data-apriori'),
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
	@app.callback(
							[ Output('graphCrossMatrix','children'),
        			  Output('crossMatrix', 'children'),],
							[
							Input('upload-data','contents'),
							Input('metodoCorr','value'),
							Input('executeCorr','num_clicks'),
							State('upload-data','filename'),
							]
							)
	def update_data(contents,metodoCorr,num_clicks,filename):
		table= html.Div()
		figure = dcc.Graph()
		global aux
		if contents:
			aux = aux + 1
			
			df = parse_contents(contents,filename)
			df = df.set_index(df.columns[0])
			df = df.corr(method=metodoCorr) 
			table = html.Div(
					[
						dash_table.DataTable(
							data = df.to_dict("rows"),
							columns = [{"name": i, "id": i} for i in df.columns],
						),
					]
				),
				
			fig = px.imshow(df)
			figure = html.Div(
					[
						dcc.Graph(
							id = 'kind',
							figure = fig
						),
					]
				)
		return figure,table
			

	return app.server
	#-----------------------------------