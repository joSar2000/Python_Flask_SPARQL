

import base64
import io
from typing import Dict
from flask import Flask, render_template, request
from SPARQLWrapper import XML, SPARQLWrapper, JSON, N3
import pandas as pd
from sqlalchemy import null
import textrazor
import networkx as nx
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
from rdflib import Graph
import matplotlib.pyplot as plt

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
            limitResults = request.form['limit']
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
                    "} LIMIT " + limitResults
                )
                sparql.setReturnFormat(JSON)
                qres = sparql.query().convert()

                sparql.setReturnFormat(N3)
                qresN3 = sparql.query().convert()
                print(type(qresN3))
                g = Graph()
                g.parse(data=qresN3)
                dg = rdflib_to_networkx_graph(
                    g, True, edge_attrs=lambda s, p, o: {})
                # Draw regulated concept map
                nx.draw(dg, node_color='lightgray', node_size=1000, font_size=8, width=0.75,
                        edgecolors='gray')
                img = io.BytesIO()
                plt.savefig(img, format="png")
                img.seek(0)
                plt.close()
                plot_data = base64.b64encode(img.getbuffer()).decode("ascii")
                if qres:
                    return render_template('responses.html', resultsQuery=qres, plot_url=plot_data)
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
                    "} LIMIT 100"
                )
                sparql.setReturnFormat(JSON)
                qres = sparql.query().convert()
                sparql.setReturnFormat(N3)
                qresN3 = sparql.query().convert()
                g = Graph()
                g.parse(data=qresN3, format="n3")
                dg = rdflib_to_networkx_graph(
                    g, True, edge_attrs=lambda s, p, o: {})
                # Draw regulated concept map
                nx.draw(dg, node_color='lightgray', node_size=100, font_size=7,
                        edgecolors='gray', arrows=True, arrowstyle="->",)
                img = io.BytesIO()
                plt.savefig(img, format="png")
                img.seek(0)
                plt.close()
                plot_data = base64.b64encode(img.getbuffer()).decode("ascii")
                if qres:
                    return render_template('responses.html', resultsQuery=qres, plot_url=plot_data)


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
                return render_template('resultsTextRazor.html', response=response)


app.run(host='localhost', port=8080, debug=True)
