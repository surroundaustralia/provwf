from provworkflow.activity import Activity
from rdflib.namespace import PROV, RDF


def test_prov_to_graph():
    a = Activity()
    g = a.prov_to_graph()

    # check all properties required do exist
    assert (None, RDF.type, PROV.Activity) in g, "g must contain a prov:Activity"
    # check endedAtTime > startedAtTime
    for p, o in g.predicate_objects(subject=a.uri):
        if p == PROV.startedAtTime:
            sat = o.toPython()
        elif p == PROV.endedAtTime:
            eat = o.toPython()

    assert (
        eat >= sat
    ), "An Activity's endedAtTime must be greater than, or equal to, its startedAtTime"


if __name__ == "__main__":
    test_prov_to_graph()
