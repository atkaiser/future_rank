from flask import render_template
from server import app
import requests


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traffic/to-work')
def toWork():
    with open("/home/akaiser/traffic/to-work.txt", "r") as f:
        for line in f:
            return line     
#    return "1"
#    r = requests.get('http://sc2ls.mooo.com:10000/time?origin=5024+Ray+Ave,+Castro+Valley,+CA+94546&destination=777+Mariners+Island+Blvd,+San+Mateo,+CA+94404')
#    return r.text

@app.route('/traffic/to-home')
def toHome():
    with open("/home/akaiser/traffic/to-home.txt", "r") as f:
        for line in f:
            return line
#    return "2"
#    r = requests.get('http://sc2ls.mooo.com:10000/time?origin=777+Mariners+Island+Blvd,+San+Mateo,+CA+94404&destination=5024+Ray+Ave,+Castro+Valley,+CA+94546')
#    return r.text

@app.route('/stocks')
def sotcks():
    with open("/home/akaiser/traffic/stocks.txt", "r") as f:
        for line in f:
            return line