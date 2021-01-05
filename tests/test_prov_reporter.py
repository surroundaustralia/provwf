from provworkflow.prov_reporter import ProvReporter
from provworkflow import ProvWorkflowException
from provworkflow.namespace import PROVWF
from rdflib import URIRef, Graph, Literal
from rdflib.namespace import DCTERMS, RDF, RDFS, XSD
import os
import requests
import pytest
from _graphdb_utils import setup_graphdb


def test_prov_to_graph():
    pr = ProvReporter()
    g = pr.prov_to_graph()

    assert (
        pr.uri,
        RDF.type,
        PROVWF.ProvReporter,
    ) in g, "g must contain a provwf:ProvReporter"

    assert (
        pr.uri,
        DCTERMS.created,
        None,
    ) in g, (
        "g must contain a dcterms:created property for the provwf:ProvReporter instance"
    )

    pr2 = ProvReporter(label="Test PR")
    g2 = pr2.prov_to_graph()

    assert (
        pr2.uri,
        RDFS.label,
        Literal("Test PR", datatype=XSD.string),
    ) in g2, "g must contain the label 'Test PR'"


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
    pr.persist(methods="file", rdf_file_path=p)
    with open(p + ".ttl") as f:
        assert str(f.read()).startswith("@prefix")
    os.unlink(p + ".ttl")


def test_persist_to_graphdb():
    gdb_error = setup_graphdb()
    if gdb_error is not None:
        pytest.skip(gdb_error)

    GRAPH_DB_SYSTEM_URI = os.environ.get("GRAPH_DB_SYSTEM_URI", "http://localhost:7200")
    GRAPHDB_USR = os.environ.get("GRAPHDB_USR", "")
    GRAPHDB_PWD = os.environ.get("GRAPHDB_PWD", "")
    os.environ["GRAPH_DB_REPO_ID"] = "provwftesting"

    pr = ProvReporter()
    ttl = pr.persist(methods=["graphdb", "string"])
    pr_uri = None
    for s in (
        Graph()
        .parse(data=ttl, format="turtle")
        .subjects(predicate=RDF.type, object=PROVWF.ProvReporter)
    ):
        pr_uri = str(s)

    q = """
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX provwf: <{}>
        SELECT ?pr_uri
        WHERE {{
            ?pr_uri a provwf:ProvReporter .
        }}
        LIMIT 1
        """.format(
        PROVWF
    )
    r = requests.get(
        GRAPH_DB_SYSTEM_URI + "/repositories/" + os.environ["GRAPH_DB_REPO_ID"],
        params={"query": q},
        headers={"Accept": "application/sparql-results+json"},
        auth=(GRAPHDB_USR, GRAPHDB_PWD),
    )
    gdb_pr_uri = r.json()["results"]["bindings"][0]["pr_uri"]["value"]
    assert gdb_pr_uri == pr_uri


# TODO: David to test
# def test_persist_to_sop():
#     pr = ProvReporter()
#     pr.persist("sop")


# TODO: implement as needed
# def test_persist_to_allegro():
#     pr = ProvReporter()


def test_persist_unknown():
    pr = ProvReporter()
    with pytest.raises(ProvWorkflowException):
        pr.persist(methods="unknown")


if __name__ == "__main__":
    test_prov_to_graph()
    # test_persist_to_string()
    # test_persist_to_file()
    # test_persist_to_graphdb()
    # # test_persist_to_sop()
    # # test_persist_to_allegro()
    # test_persist_unknown()
