# -*- coding: utf-8 -*-
"""
Wolf-08 
Mineria de Datos
"""
from flask import Flask, redirect, render_template,request,url_for
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os 
app = Flask(__name__)

folder= "C:\\Users\\aleja\\Documents\\ProyectoMD\\static\\files"
ALLOWED_EXTENSIONS = {'txt','csv'}
app.config['UPLOAD_FOLDER'] = folder


def formatos_permitidos(filename):
    formato=filename.rsplit(".",1)[1].lower()
    if formato in ALLOWED_EXTENSIONS:
      return formato
    else:
      return False

@app.route('/upload-file', methods=["GET","POST"])
def files():
  if request.method == "POST":
    print("1")
    if request.files:
      print("2")
      file=request.files["file"]
      formato=formatos_permitidos(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
      #return redirect(url_for('algoritmos',file=file))
      return redirect(request.url)
  return render_template("index.html")

@app.route('/algoritmos/<file>')
def algoritmos(file):
  return 'Here going to algoritms'

if __name__ == '__main__':
  app.run(debug=True)