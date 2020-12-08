# -*- coding: utf-8 -*-

from flask import current_app as app 
from flask import redirect, render_template,request,url_for

#import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
import os 
from apyori import apriori
#app = Flask(__name__)

folder= "C:\\Users\\aleja\\Documents\\ProyectoMD\\aplicacionMD\\static\\files"
ALLOWED_EXTENSIONS = {'txt','csv'}
app.config['UPLOAD_FOLDER'] = folder


def formatos_permitidos(filename):
    formato=filename.rsplit(".",1)[1].lower()
    if formato in ALLOWED_EXTENSIONS:
      return formato
    else:
      return False

@app.route('/', methods=["GET","POST"])
def files():
  if request.method == "POST":
    print("1")
    if request.files:
      print("2")
      file=request.files["file"]
      filename= file.filename
      formato=formatos_permitidos(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
      #dash1(filename,formato)
      return redirect(url_for('dash1',filename=filename,formato=formato))
      #return redirect(url_for('/dashboard/',filename=filename,formato=formato))
  return render_template("index.html")


@app.route('/dashboard/<filename>/<formato>')
def dash1(filename,formato):
  if formato == 'txt':
    print("no txt")
  if formato == 'csv':
    print(formato) 
    print(filename)


  return redirect('/dashapp/')



# @app.route('/algoritmos/<filename>')
# def algoritmos(filename):
#   archivo=str(filename)
#   print(archivo)
#   rutaFile="C:\\Users\\aleja\\Documents\\ProyectoMD\\aplicacionMD\\static\\files" + archivo
#   Transacciones=[]
#   Datos=pd.read_csv(rutaFile,header=None)
#   for i in range(0,7501):
#     Transacciones.append([str(Datos.values[i,j]) for j in range (0,20)]) 
  
#   Reglas = apriori(Transacciones, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2) 
#   Resultado = list(Reglas) 
#   print(Resultado[0])

#   return render_template("algoritmos.html",
#   Datos=Datos,
#   Transacciones=Transacciones,
#   Reglas=Reglas,
#   Resultado=Resultado)

# if __name__ == '__main__':
#   app.run(debug=True)