from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')
def files():

  
  return render_template("index.html")

@app.route('/algoritmos')
def algoritmos():
  return 'Here going to algoritms'

if __name__ == '__main__':
  app.run(debug=True)