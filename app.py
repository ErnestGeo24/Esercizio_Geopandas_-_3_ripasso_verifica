import io
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, Response
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/input', methods=['GET'])
def input():
    return render_template('input.html')

@app.route('/farmacia', methods=['GET'])
def farmacia():
    input = request.args.get('input')
    return render_template('risultato.html', table = table.html())

@app.route('/grafico', methods=['GET'])
def grafico():
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)