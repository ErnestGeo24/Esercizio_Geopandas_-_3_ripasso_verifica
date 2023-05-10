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

comuni = gpd.read_file('https://github.com/SimoneFinessi/Dati/raw/main/istat2022/Com01012022_g.zip')
province = gpd.read_file('https://github.com/SimoneFinessi/Dati/raw/main/istat2022/ProvCM01012022_g.zip')

def convertikm(km):
  return km / 2.59

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/input', methods=['GET'])
def input():
    input = request.args.get('input')
    return render_template('input.html')

@app.route('/input2', methods=['GET'])
def input2():
    return render_template('input2.html')

@app.route('/input3', methods=['GET'])
def input3():
    return render_template('input3.html')
    
@app.route('/input4', methods=['GET'])
def input4():
    return render_template('input4.html')
    
@app.route('/input5', methods=['GET'])
def input5():
    return render_template('input5.html')

@app.route('/input6', methods=['GET'])
def input6():
    return render_template('input6.html')

@app.route('/input7', methods=['GET'])
def input7():
    return render_template('input7.html')

@app.route('/input8', methods=['GET'])
def input8():
    return render_template('input8.html')

@app.route('/input9', methods=['GET'])
def input9():
    return render_template('input9.html')

@app.route('/risultato1', methods=['GET'])
def risultato1():
    province3857 = province.to_crs(3857)
    pu = request.args.get('input')
    fig, ax = plt.subplots()
    province3857[province3857['DEN_UTS'] == pu].plot(facecolor = 'None',ax = ax)
    ctx.add_basemap(ax = ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/risultato2', methods=['GET'])
def risultato2():
    pu = request.args.get('input')
    comuniDi = comuni[comuni.within(province[province['DEN_UTS'] == pu].geometry.item())]
    return render_template('risultato2.html', table = comuniDi.to_html())

@app.route('/risultato3', methods=['GET'])
def risultato3():
    pu = request.args.get('input')
    comuniDi = comuni[comuni.within(province[province['DEN_UTS'] == pu].geometry.item())]
    comuniOr = comuniDi['COMUNE'].reset_index().sort_values(by = 'COMUNE')
    return render_template('risultato3.html', table = comuniOr.to_html())

@app.route('/risultato4', methods=['GET'])
def risultato4():
    pu = request.args.get('input')
    comuniDi = comuni[comuni.within(province[province['DEN_UTS'] == pu].geometry.item())]
    dictiCo = comuniDi.set_index('COMUNE')['Shape_Area'].to_dict()
    return render_template('risultato3.html', table = pd.Series(dictiCo).reset_index().to_html())

@app.route('/risultato5', methods=['GET'])
def risultato5():
    pu = request.args.get('input')
    comuniDi = comuni[comuni.within(province[province['DEN_UTS'] == pu].geometry.item())]
    comuniDi['superficeInMigliaQuadrate'] = convertikm(comuniDi['Shape_Area']/1000000)
    return render_template('risultato5.html', table = comuniDi.to_html())

@app.route('/risultato6', methods=['GET'])
def risultato6():
    pu = request.args.get('input')
    comuniconf = comuni[comuni.touches(province[province['DEN_UTS'] == pu].geometry.item())]
    return render_template('risultato6.html', table = comuniconf.to_html())

@app.route('/risultato7', methods=['GET'])
def risultato7():
    pu = request.args.get('input') 
    comuniconf = comuni[comuni.touches(province[province['DEN_UTS'] == pu].geometry.item())]
    comuniconf['superficeInMigliaQuadrate'] = convertikm(comuniconf['Shape_Area']/1000000)
    comunisum = comuniconf['superficeInMigliaQuadrate'].sum()
    return render_template('risultato7.html', table = comunisum)

@app.route('/risultato8', methods=['GET'])
def risultato8():
    pu = request.args.get('input')
    comuniconf = comuni[comuni.touches(province[province['DEN_UTS'] == pu].geometry.item())]
    comuneconfmax = comuniconf[comuniconf['Shape_Area'] == comuniconf['Shape_Area'].max()]
    return render_template('risultato8.html', table = comuneconfmax.to_html())

@app.route('/risultato9', methods=['GET'])
def risultato9():
    pu = request.args.get('input')
    distanza = comuni[comuni['COMUNE'] == pu].distance(comuni[comuni['COMUNE']== 'Milano'].geometry.item())
    return render_template('risultato9.html', table = distanza)
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)