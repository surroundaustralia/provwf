from provworkflow.entity import Entity
from provworkflow.activity import Activity
from rdflib import URIRef
from rdflib.namespace import PROV, RDF


def test_prov_to_graph():
    """A basic ProvReporter should prov_to_graph an Activity with a startedAtTime & endedAtTime

    :return: None
    """

    pr = Entity()
    g = pr.prov_to_graph()

    # check basic typing
    assert (pr.uri, RDF.type, PROV.Entity) in g, "g must contain a prov:Entity"

    pr = Entity(was_used_by=Activity(uri=URIRef("https://something.com/x")))
    g = pr.prov_to_graph()

    assert (
        URIRef("https://something.com/x"),
        PROV.used,
        pr.uri,
    ) in g, "g must contain a prov:Activity with URI <https://something.com/x>"


if __name__ == "__main__":
    test_prov_to_graph()
