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
aux  = 1
folder= "C:\\Users\\aleja\\Documents\\ProyectoMD\\aplicacionMD\\static\\files"

def init_dashboard5(server):
	"""Create a Plotly Dash dashboard."""
    #app = dash.Dash(__name__)
	app = dash.Dash(__name__,server=server,
	routes_pathname_prefix="/clasificacion/",
	external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
	)

	#custom html layout 
	#app.index_string = html_layout
	#Creacion del layout 
	app.layout = html.Div([
		html.H1("Algoritmo de Clasificacion "),
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
		html.Div([ html.H3("Clasificación con Regresion Logistica"),
      #html.Button('Cargar Archivo', id='loadFile', n_clicks=0,style={'width': '25%','margin': '3%'}),
	  html.Div( id = 'output-data-upload'),
		]),
		html.Div(),
		dcc.Tabs(id = 'tabs',value = 'tab-1', children=[
			#dcc.Tab(label = 'Datos',value = 'tab1',children=[
				dcc.Tab(label='Clasificacion', value='tab',children=[
					  html.Button('Diagnosticar', id='executeSigmoide', n_clicks=0,
                    style={'width': '25%','margin': '3%','background-color':'black','color':'white'}),
                html.Div([
                    html.Div([
                        "Compactividad",
                        dcc.Input(
                            id="compactividad",  type="number", value= 0.04362,
                            placeholder="Compactividad",style={'margin': '5%','textAlign': 'center'}),
                    ],className="three columns"),
                    html.Div([
                        "Textura",    
                        dcc.Input(
                            id="textura",     type="number", value=24.54,
                            placeholder="Textura",style={'margin': '5%','textAlign': 'center'}),
                    ],className="three columns"),
                ],className="row"),
                html.Div([
                    html.Div([
                        "Area",       
                        dcc.Input(
                            id="area",        type="number", value=181.0,
                            placeholder="Area",style={'margin': '5%','textAlign': 'center'}),
                    ],className="three columns"),
                    html.Div([
                        "Concavidad", 
                        dcc.Input(
                            id="concavidad",  type="number",value = 0, 
                            placeholder="Concavidad",style={'margin': '5%','textAlign': 'center'}),
                    ],className="three columns"),
                ],className="row"),

                html.Div([
                    html.Div([
                        "Simetria",   
                        dcc.Input(
                            id="simetria",  type="number", value=0.1587,
                            placeholder="Simetria",style={'margin': '5%','textAlign': 'center'}),
                    ],className="three columns"),
                    html.Div([
                        "Dimensión fractal", 
                        dcc.Input(
                            id="dimensionFractal",type="number", value=1.0,
                            placeholder="Dimensión Fractal",style={'margin': '5%','textAlign': 'center'}),
                    ],className="three columns"),
                ],className="row"),

                    html.Div(id='sigmoide',style={'textAlign': 'center'}),

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
	@app.callback(
    Output('sigmoide', 'children'),
    [
        Input('compactividad','value'),
        Input('textura','value'),
        Input('area','value'),
        Input('concavidad','value'),
        Input('simetria','value'),
        Input('dimensionFractal','value'),
        Input('upload-data', 'contents'),
        Input('executeSigmoide', 'n_clicks'),
				State('upload-data', 'filename')
    ]
)
	def update_data(compactividad,textura,area,concavidad,simetria,dimensionFractal,contents,n_clicks, filename):
		mensaje = html.Div()
		global aux
		if contents:
			aux = aux + 1
			df = parse_contents(contents,filename)
			df = df.set_index(df.columns[0])
			X = np.array(df[['Texture', 'Area', 'Compactness','Concavity', 'Symmetry', 'FractalDimension']])	
			Y = np.array(df[['Diagnosis']])

			Clasificacion = linear_model.LogisticRegression()
			validation_size = 0.2
			seed = 1234
			X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(
                                X, Y, test_size=validation_size, random_state=seed, shuffle = True)
			Clasificacion.fit(X_train, Y_train)
			Probabilidad = Clasificacion.predict_proba(X_train)
			Predicciones = Clasificacion.predict(X_train)
			Clasificacion.score(X_train, Y_train)
			PrediccionesNuevas = Clasificacion.predict(X_validation)
			confusion_matrix = pd.crosstab(Y_validation.ravel(), PrediccionesNuevas, 
                                rownames=['Real'], colnames=           ['Predicción'])
			v = Clasificacion.score(X_validation, Y_validation)
			NuevoPaciente = pd.DataFrame({  'Texture': [textura],           'Area': [area], 
                                            'Compactness': [compactividad], 'Concavity': [concavidad], 
                                            'Symmetry': [simetria],         'FractalDimension': [dimensionFractal]})

			print(Clasificacion.predict(NuevoPaciente))
			if  Clasificacion.predict(NuevoPaciente) == "B":
				mensaje = html.Div(
                        html.H5("Con una confianza de " + str(format(v*100, '.2f') ) +"% Se diagnostica positivo ")
                )
			else:
				mensaje = html.Div(
                        html.H5("Con una confianza de  " + str(format(v*100, '.2f'))  +"% Se diagnostica negativo "))
		return mensaje
	return app.server
	#-----------------------------------