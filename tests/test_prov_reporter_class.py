from provworkflow.prov_reporter import ProvReporter
from rdflib import URIRef, Graph, Literal


def test_persist():
    g = Graph()
    dummy_ttl_data = """
        PREFIX dcterms: <http://purl.org/dc/terms/>
         
        <a:> <b:> <c:> .
        <a:> <d:> <e:> .
        <a:> dcterms:title "Fake thing" .
    """
    g.parse(data=dummy_ttl_data, format="turtle")

    s = ProvReporter.persist(g, ["string"])
    assert "title" in s


if __name__ == "__main__":
    test_persist()
