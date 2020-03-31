from provworkflow import ProvReporter
from rdflib import Namespace
from rdflib.namespace import RDF


def test_ProvReporter_prov_to_graph():
    """A basic ProvReporter should prov_to_graph an Activity with a startedAtTime & endedAtTime

    :return: None
    """

    PROV = Namespace("http://www.w3.org/ns/prov#")

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


if __name__ == "__main__":
    test_ProvReporter_prov_to_graph()
