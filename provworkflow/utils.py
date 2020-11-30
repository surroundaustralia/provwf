import logging
import os
from rdflib import Graph
import requests


def to_graphdb(graph: Graph):
    """
    generic util to write a given graph to graphdb
    :param graph:
    :return: a status code
    """

    GRAPH_DB_BASE_URI = os.environ.get("GRAPH_DB_BASE_URI", "http://localhost:7200")
    GRAPH_DB_REPO_ID = os.environ.get("GRAPH_DB_REPO_ID", "sarobot")
    GRAPHDB_USR = os.environ.get("GRAPHDB_USR", "admin")
    GRAPHDB_PWD = os.environ.get("GRAPHDB_PWD", "sortrobot")

    data = graph.serialize(format="turtle", encoding="utf-8")

    r = requests.post(
        GRAPH_DB_BASE_URI + "/repositories/" + GRAPH_DB_REPO_ID + "/statements",
        params={"context": "null"},
        data=data,
        headers={"Content-Type": "text/turtle"},
        auth=(GRAPHDB_USR, GRAPHDB_PWD)
    )
    logging.info(f'Attempted to write triples to GraphDB and got status code: {r.status_code} returned')
    if r.status_code != 204:
        raise Exception("GraphDB says: {}".format(r.text))