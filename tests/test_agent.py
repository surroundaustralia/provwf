from provworkflow.agent import Agent
from rdflib.namespace import PROV, RDF


def test_prov_to_graph():
    """A basic ProvReporter should prov_to_graph an Activity with a startedAtTime & endedAtTime

    :return: None
    """

    pr = Agent()
    g = pr.prov_to_graph()

    # check all properties required do exist
    assert (None, RDF.type, PROV.Agent) in g, "g must contain a prov:Agent"


if __name__ == "__main__":
    pass
