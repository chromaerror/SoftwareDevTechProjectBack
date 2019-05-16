from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, support_credentials=True)
import csv

CAPITA_FILE = 'csvfolder/vakiluvut/vakiluku_tiedosto.csv'
EMISSION_FILE = 'csvfolder/pastot/paastotiedosto.csv'

@app.route("/getCountries", methods=['GET'])
def returnAllCountries():
    countries = []
    with open(EMISSION_FILE) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for line in csv_reader:
            if csv_reader.line_num <= 5:
                continue
            else:
                countries.append(line[0])

    returnObject = {
        "countries": countries
    }
    resp = jsonify(returnObject)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return(resp)

@app.route("/getPopulation", methods=['GET'])
def returnPopulation():
    returnedListOfCountries = {}
    with open(CAPITA_FILE) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for line in csv_reader:
            if csv_reader.line_num < 5:
                continue
            else:
                returnedListOfCountries = line

    returnObject = {
        "data": {
            "country": returnedListOfCountries[0],
            "shorthand": returnedListOfCountries[1],
            "populationByYear": {
                "population": returnedListOfCountries
            }
        }
    }
    resp = jsonify(returnObject)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return(resp)


@app.route("/getEmissionByCountry", methods=['POST'])
def returnEmissionByCountry():
    requested_line = "ERROR OCCURRED"
    requestJSON = request.get_json()
    selected_country = requestJSON['selected_country']
    shorthand = "NaN"
    with open(EMISSION_FILE) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for line in csv_reader:
            if type(line) is list:
                if len(line) is not 0:
                    if line[0] == selected_country:
                        shorthand = line[1]
                        del line[0:4]
                        requested_line = line
    returnObject = {
        "data": {
            "country": selected_country,
            "shorthand": shorthand,
            "emissionsByYear": {
                "emissions": requested_line
            }
        }
    }
    resp = jsonify(returnObject)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    if requested_line == "ERROR OCCURRED":
        return Response("{'text': 'error occurred'}", status=400, mimetype='application/json')
    else:
        return(resp)


@app.route("/getPopulationByCountry", methods=['POST'])
def returnPopulationByCountry():
    requested_line = "ERROR OCCURRED"
    requestJSON = request.get_json()
    selected_country = requestJSON['selected_country']
    shorthand = "NaN"
    with open(CAPITA_FILE) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for line in csv_reader:
            if type(line) is list:
                if len(line) is not 0:
                    if line[0] == selected_country:
                        shorthand = line[1]
                        del line[0:4]
                        requested_line = line
    returnObject = {
        "data": {
            "country": selected_country,
            "shorthand": shorthand,
            "populationByYear": {
                "population": requested_line
            }
        }
    }
    resp = jsonify(returnObject)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return(resp)



# Unused at the moment
@app.route("/getPopulationByCountryAndYear", methods=['POST'])
def hello():
    selected_country = request.form.get('selected_country')
    selected_year = request.form.get('selected_year')
    index = 0
    requested_line = 0
    with open(CAPITA_FILE ) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for line in csv_reader:
            if csv_reader.line_num is 5:
                for x in line:
                    if selected_year == x:
                        index = line.index(selected_year)
            if type(line) is list:
                if len(line) is not 0:
                    if line[0] == selected_country:
                        requested_line = line[index]

    returnObject = {
        "population": requested_line
    }
    resp = jsonify(returnObject)
    return(resp)