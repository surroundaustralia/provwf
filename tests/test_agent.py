from provworkflow.agent import Agent
from rdflib.namespace import PROV, RDF


def test_prov_to_graph():
    """A basic ProvReporter should prov_to_graph an Activity with a startedAtTime & endedAtTime

    :return: None
    """

    a = Agent()
    g = a.prov_to_graph()

    # check all properties required do exist
    assert (a.uri, RDF.type, PROV.Agent) in g, "g must contain a prov:Agent"

    # actedOnBehalfOf test
    a1 = Agent()
    a2 = Agent(acted_on_behalf_of=a1)
    g = a2.prov_to_graph()
    assert (a2.uri, PROV.actedOnBehalfOf, a1.uri) in g, "g must contain a2 prov:actedOnBehalfOf a1"
