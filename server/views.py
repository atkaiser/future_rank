from flask import render_template
from server import app
import requests


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traffic/to-work')
def toWork():
    r = requests.get('http://sc2ls.mooo.com:10000/time?origin=5024+Ray+Ave,+Castro+Valley,+CA+94546&destination=777+Mariners+Island+Blvd,+San+Mateo,+CA+94404')
    return r.text

@app.route('/traffic/to-home')
def toHome():
    r = requests.get('http://sc2ls.mooo.com:10000/time?origin=777+Mariners+Island+Blvd,+San+Mateo,+CA+94404&destination=5024+Ray+Ave,+Castro+Valley,+CA+94546')
    return r.text
