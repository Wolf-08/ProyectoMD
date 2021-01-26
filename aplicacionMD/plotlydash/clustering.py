import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table


import pandas as pd
import plotly.express as px

from apyori import apriori
from scipy.spatial import distance
import plotly.graph_objects as go
import numpy as np
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator   
ncd  = 1
folder= "C:\\Users\\aleja\\Documents\\ProyectoMD\\aplicacionMD\\static\\files"

def init_dashboard4(server):
	"""Create a Plotly Dash dashboard."""
    #app = dash.Dash(__name__)
	app = dash.Dash(__name__,server=server,
	routes_pathname_prefix="/clustering/",
	external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
	)

	#custom html layout 
	#app.index_string = html_layout
	#Creacion del layout 
	app.layout = html.Div([
		html.H1("Algoritmo de Clustering Particional "),
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
		html.Div([ html.H3("Clustering Particional "),
      #html.Button('Cargar Archivo', id='loadFile', n_clicks=0,style={'width': '25%','margin': '3%'}),
	  html.Div( id = 'output-data-upload'),
		]),
		dcc.Tabs(id = 'tabs',value = 'tab-1', children=[
			#dcc.Tab(label = 'Datos',value = 'tab1',children=[
				dcc.Tab(label='Clustering', value='tab',children=[
					html.Button('Monstrar Graficas', id='executeCluster', n_clicks=0,style={'width': '25%','margin': '3%','background-color':'black','color':'white'}),
					dcc.Tabs(id='clus',value='tab2',children=[
						dcc.Tab(label='Grafica del codo',value='subtab',children=[
							html.Div(id='elbow'),
						]),
						dcc.Tab(label='Grafica del cluster',value='subtab1',children=[
							html.Div(id='cluster'),
						]),
					])
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
	@app.callback([Output('elbow','children'),
								Output('cluster','children')],
							[
							Input('upload-data','contents'),
							Input('executeCluster','num_clicks'),
							State('upload-data','filename'),
							]
							)
	def update_data(contents,num_clicks,filename):
		table = html.Div()
		figure1= dcc.Graph()
		figure2 = dcc.Graph()
		global ncd
		if contents:
			ncd = ncd + 1
			#contents = contents[0]
			#filename = filename[0]
			df = parse_contents(contents,filename)
			VariablesModelo = df.iloc[:,:].values
			SSE = []
			for i in range(2, 16):
				km = KMeans(n_clusters=i)
				km.fit(VariablesModelo)
				SSE.append(km.inertia_)
			
			x = np.arange(len(SSE))
			fig = go.Figure( data=   go.Scatter(x=x,y=SSE))
			kl = KneeLocator(range(2, 16), SSE, curve="convex", direction="decreasing")
			MParticional = KMeans(n_clusters=kl.elbow, random_state=0).fit(VariablesModelo)
			model = KMeans(n_clusters = kl.elbow, init = "k-means++", max_iter = 300, n_init = 10, random_state =   0)
			y_clusters = model.fit_predict(VariablesModelo)
			labels = model.labels_
			trace = go.Scatter3d(x=VariablesModelo[:, 0], y=VariablesModelo[:, 1], z=VariablesModelo[:, 2],     mode='markers',marker=dict(color = labels, size= 3,line=dict(color= 'black',width = 3)))
			layout = go.Layout(margin=dict(l=0,r=0))
			data = [trace]
			fig2 = go.Figure(data = data, layout = layout)

			figure1 = html.Div(
			[
				dcc.Graph(
					id='kind',
					figure=fig
				),
			]
		)
			figure2 = html.Div(
			[
				dcc.Graph(
					id='kind2',
					figure=fig2
					)
			]
		) 
		return figure1,figure2
	return app.server
	#-----------------------------------