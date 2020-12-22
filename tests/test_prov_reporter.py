from provworkflow import ProvReporter, ProvReporterException
from rdflib import URIRef, Graph
from rdflib.namespace import PROV, RDF
import os
import requests
import pytest


def test_prov_to_graph():
    """A basic ProvReporter should prov_to_graph an Activity with a startedAtTime & endedAtTime

    :return: None
    """

    pr = ProvReporter()
    g = pr.prov_to_graph()

    # check all properties required do exist
    assert (None, RDF.type, PROV.Activity) in g, "g must contain a prov:Activity"
    assert (None, PROV.startedAtTime, None) in g, "g must contain a prov:startedAtTime"
    assert (None, PROV.endedAtTime, None) in g, "g must contain a prov:endedAtTime"

    # check endedAtTime > startedAtTime
    q = """
        ASK {
            ?a  prov:startedAtTime ?s ;
                prov:endedAtTime ?e .
            FILTER (?e > ?s) 
        }
        
    """
    assert g.query(q), "startedAtTime must be less than endedAtTime"


def test_persist_to_string():
    pr = ProvReporter()
    p = pr.persist("string")
    assert p.startswith("@prefix")

    # trig test
    pr2 = ProvReporter(named_graph_uri=URIRef("http://example.com/provreporter/x"))
    p = pr2.persist("string")
    assert "{" in p


def test_persist_to_file():
    p = "/tmp/prov_reporter_x"
    pr = ProvReporter()
    pr.persist("file", rdf_file_path=p)
    with open(p + ".ttl") as f:
        assert str(f.read()).startswith("@prefix")
    os.unlink(p + ".ttl")


def test_persist_to_graphdb():
    os.environ["GRAPH_DB_REPO_ID"] = "provwf"
    pr = ProvReporter()
    ttl = pr.persist(["graphdb", "string"])
    activity_uri = None
    for s in (
        Graph()
        .parse(data=ttl, format="turtle")
        .subjects(predicate=RDF.type, object=PROV.Activity)
    ):
        activity_uri = str(s)

    GRAPH_DB_BASE_URI = os.environ.get("GRAPH_DB_BASE_URI", "http://localhost:7200")
    GRAPH_DB_REPO_ID = os.environ.get("GRAPH_DB_REPO_ID", "wf")
    GRAPHDB_USR = os.environ.get("GRAPHDB_USR", "")
    GRAPHDB_PWD = os.environ.get("GRAPHDB_PWD", "")
    q = """
        PREFIX prov: <http://www.w3.org/ns/prov#>
        SELECT ?activity_uri
        WHERE {
            ?activity_uri a prov:Activity ;
                          prov:startedAtTime ?st .
        }
        ORDER BY DESC(?st)
        LIMIT 1
        """
    r = requests.get(
        GRAPH_DB_BASE_URI + "/repositories/" + GRAPH_DB_REPO_ID,
        params={"query": q},
        headers={"Accept": "application/sparql-results+json"},
        auth=(GRAPHDB_USR, GRAPHDB_PWD),
    )
    gdb_activity_uri = r.json()["results"]["bindings"][0]["activity_uri"]["value"]
    assert gdb_activity_uri == activity_uri


def test_persist_to_sop():
    pr = ProvReporter()
    pr.persist("sop")


# TODO: implement as needed
# def test_persist_to_allegro():
#     pr = ProvReporter()


def test_persist_unknown():
    pr = ProvReporter()
    with pytest.raises(ProvReporterException):
        pr.persist("unknown")


if __name__ == "__main__":
    test_prov_to_graph()
    test_persist_to_string()
    test_persist_to_file()
    test_persist_to_graphdb()
    test_persist_to_sop()
    # test_persist_to_allegro()
    test_persist_unknown()
