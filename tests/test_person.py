from provworkflow.person import Person
from rdflib import URIRef
from rdflib.namespace import PROV, RDF, SDO


def test_prov_to_graph():
    """A basic ProvReporter should prov_to_graph an Activity with a startedAtTime & endedAtTime

    :return: None
    """

    p = Person()
    g = p.prov_to_graph()

    # check all properties required do exist
    assert (p.uri, RDF.type, PROV.Person) in g, "g must contain a prov:Person"

    # actedOnBehalfOf test
    p = Person()
    p.email = URIRef("mailto:nicholas.car@surroundaustralia.com")
    g = p.prov_to_graph()
    assert (
        p.uri,
        SDO.email,
        URIRef("mailto:nicholas.car@surroundaustralia.com"),
    ) in g, "g must contain {} sdo:email {}".format(
        p.uri, URIRef("mailto:nicholas.car@surroundaustralia.com")
    )
