from provworkflow.machine import Machine
from provworkflow.prov_reporter import PROVWF
from rdflib.namespace import RDF


def test_prov_to_graph():
    """A basic ProvReporter should prov_to_graph an Activity with a startedAtTime & endedAtTime

    :return: None
    """

    m = Machine()
    g = m.prov_to_graph()

    # check all properties required do exist
    assert (m.uri, RDF.type, PROVWF.Machine) in g, "g must contain a prov:Person"
