

from typing import Dict
from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON
from sqlalchemy import null
import json
import ast

app = Flask(__name__)

dbpedia_sparq = "http://dbpedia.org/sparql"
dbpedia_idioma = "es"

def __init__(self, query):
    self.query = query

@app.route('/')
def init():
    return render_template('home.html')


@app.route('/homeSearchQuery', methods=['POST'])
def homeSearchQuery():
    if request.method == 'POST':
        if 'Sparq' in request.form:
            return render_template('index.html')


@app.route('/searchQuery', methods=['POST'])
def searchQuery():
    if request.method == 'POST':
        if 'buscar' in request.form:
            item = request.form['querySparq']
            #filtersQuery = request.form['filterResource']
            #filterBase = request.form['filterBase']
            if item != "":
                sparql = SPARQLWrapper(dbpedia_sparq)
                sparql.setQuery(
                    "SELECT ?resource ?query\n WHERE {\n"
                    "?resource dbo:country dbr:"+item+".\n"
                    "?resource rdfs:label ?query FILTER REGEX (?query, '" +
                    item+"', 'i').\n"
                    "FILTER (LANG(?query) = '"+dbpedia_idioma+"')"
                    "} limit 100"
                )
                sparql.setReturnFormat(JSON)
                qres = sparql.query().convert()
                if qres:
                    return render_template('responses.html', resultsQuery=qres)


@app.route('/searchQuery', methods=['POST', 'GET'])
def details (query):
    return query

@app.route('/detailsSearch/<int:id>/<path:query>')
def detailsSearch(query, id=None):
    #res = json.dumps(query)
    #newQuery = json.loads(res)
    Dict = eval(query)
    return render_template('details.html', id = id, queryRes = Dict)



app.run(host='localhost', port=8080, debug=True)
