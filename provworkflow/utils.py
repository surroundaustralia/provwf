import os
from rdflib import Graph
import requests

GRAPH_DB_BASE_URI = os.environ.get("GRAPH_DB_BASE_URI", "http://localhost:7200")
GRAPH_DB_REPO_ID = os.environ.get("GRAPH_DB_REPO_ID", "sortrobot")
GRAPHDB_USR = os.environ.get("GRAPHDB_USR", "admin")
GRAPHDB_PWD = os.environ.get("GRAPHDB_PWD", "sortrobot")

def to_graphdb(self, graph : Graph):
    """
    generic util to write a given graph to graphdb
    :param self:
    :param graph:
    :return:
    """

    data = graph.serialize(format="turtle").decode("utf-8")

    r = requests.post(
        GRAPH_DB_BASE_URI + "/repositories/" + GRAPH_DB_REPO_ID + "/statements",
        params={"context": "null"},
        data=data,
        headers={"Content-Type": "text/turtle"},
        auth=(GRAPHDB_USR, GRAPHDB_PWD)
    )
    print(r.status_code)
    if r.status_code != 204:
        raise Exception("GraphDB says: {}".format(r.text))