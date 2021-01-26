from flask import Flask
from flask_assets import Environment

def init_app():
  """
  Construccion de una aplicación con core de Flask
  y una app embebida de Dash 
  """
  app = Flask(__name__,instance_relative_config=False)
  #assets = Environment()
  #assets.init_app(app)

  with app.app_context():
    #Importando partes de la app en Flas
    from . import routes 
    #from . assets import compile_static_assets
    #Importando Dash aplication 
    from .plotlydash.dashboard import init_dashboard1
    from .plotlydash.correlacion import init_dashboard2
    from .plotlydash.distancias import init_dashboard3
    from .plotlydash.clustering import init_dashboard4
    from .plotlydash.Rlogistica import init_dashboard5


    app = init_dashboard1(app)
    #Compilando static assets 
    #compile_static_assets(assets)

    return app  