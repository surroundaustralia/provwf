from provworkflow.data_service import DataService
from provworkflow.entity import Entity
from provworkflow.activity import Activity
from provworkflow.prov_reporter import PROVWF
from rdflib import URIRef, Literal
from rdflib.namespace import DCAT, PROV, RDF, RDFS, XSD


def test_prov_to_graph():
    """A basic ProvReporter should prov_to_graph an Activity with a startedAtTime & endedAtTime

    :return: None
    """

    ds = DataService()
    g = ds.prov_to_graph()

    # check basic typing
    assert (ds.uri, RDF.type, DCAT.DataService) in g, "g must contain a dcat:DataService"

    ds = DataService(was_used_by=Activity(uri=URIRef("https://something.com/x")))
    g = ds.prov_to_graph()

    assert (
        URIRef("https://something.com/x"),
        PROV.used,
        ds.uri,
    ) in g, "g must contain a prov:Activity with URI <https://something.com/x>"

    dataset_label = "Some Dataset"
    ds = DataService(
        service_parameters="{'param1':'val1', 'param2':'val2'}",
        serves_datasets=[Entity(label=dataset_label)]
    )
    g = ds.prov_to_graph()
    for o in g.objects(subject=ds.uri, predicate=DCAT.servesDataset):
        assert (o, RDFS.label, Literal("Some Dataset", datatype=XSD.string)) in g, \
            "g must contain <{}> dcat:servesDataset/rdfs:label \"{}\"".format(ds.uri, dataset_label)


if __name__ == "__main__":
    test_prov_to_graph()
