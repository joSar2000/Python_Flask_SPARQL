

from typing import Dict
from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON
from sqlalchemy import null
import json
import ast
import textrazor
import re

app = Flask(__name__)

dbpedia_sparq = "http://dbpedia.org/sparql"
dbpedia_idioma = "es"
TEXTRAZOR_API_KEY = '270e581e58ed691956c3b44654930f4f76f3c61c9caed4e8a6205a14'
textrazor.api_key = TEXTRAZOR_API_KEY

###############################################


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


@app.route('/searchTextRazor', methods=['POST'])
def searchTextRazor():
    if request.method == 'POST':
        if 'TextRazer' in request.form:
            return render_template('textRazor.html')


@app.route('/searchQuery', methods=['POST'])
def searchQuery():
    if request.method == 'POST':
        if 'buscar' in request.form:
            item = request.form['querySparq']
            filtersQuery = request.form['filterSparq']
            filters = request.form['filter']
            #filterBase = request.form['filterBase']
            splitItem = item.split(':')
            # print(filterBase)
            if item != "" and filters == "":
                print("no hay filtros")
                sparql = SPARQLWrapper(dbpedia_sparq)
                sparql.setQuery(
                    "PREFIX wikibase: <http://wikiba.se/ontology#>\n"
                    "PREFIX bd: <http://www.bigdata.com/rdf#>\n"
                    "SELECT ?resource ?query ?abstract ?image\n WHERE {\n"
                    "?resource " + filtersQuery + " "+item+".\n"
                    "?resource rdfs:label ?query.\n"
                    "?resource dbo:abstract ?abstract.\n"
                    "OPTIONAL {?resource dbo:thumbnail ?image}.\n"
                    "FILTER (LANG(?query) = '"+dbpedia_idioma+"').\n"
                    "FILTER (LANG(?abstract) = '"+dbpedia_idioma+"').\n"
                    "} LIMIT 200"
                )
                sparql.setReturnFormat(JSON)
                qres = sparql.query().convert()
                if qres:
                    return render_template('responses.html', resultsQuery=qres)
            else:
                if item != "" and filters != "":
                    print(filters)
                    sparql = SPARQLWrapper(dbpedia_sparq)
                sparql.setQuery(
                    "PREFIX wikibase: <http://wikiba.se/ontology#>\n"
                    "PREFIX bd: <http://www.bigdata.com/rdf#>\n"
                    "SELECT ?resource ?query ?abstract ?image\n WHERE {\n"
                    "?resource " + filtersQuery + " "+item+".\n"
                    "?resource rdfs:label ?query.\n"
                    "?resource dbo:abstract ?abstract.\n"
                    "?resource rdfs:label ?query FILTER REGEX (?query, '" +
                    filters + "', 'i').\n"
                    "OPTIONAL {?resource dbo:thumbnail ?image}.\n"
                    "FILTER (LANG(?query) = '"+dbpedia_idioma+"').\n"
                    "FILTER (LANG(?abstract) = '"+dbpedia_idioma+"').\n"
                    "} LIMIT 200"
                )
                sparql.setReturnFormat(JSON)
                qres = sparql.query().convert()
                if qres:
                    return render_template('responses.html', resultsQuery=qres)


@app.route('/detailsSearch/<int:id>/<path:query>')
def detailsSearch(query, id=None):
    Dict = eval(query+"'}}")
    return render_template('details.html', id=id, queryRes=Dict)


@app.route('/resultsTextRazor', methods=['POST'])
def resultsTextRazor():
    if request.method == 'POST':
        if 'buscarTextRazor' in request.form:
            itemText = request.form['queryText']
            if itemText != '':
                client = textrazor.TextRazor(extractors=["entities", "topics"])
                response = client.analyze(itemText)
                return render_template('resultsTextRazor.html', response = response)

app.run(host='localhost', port=8080, debug=True)
