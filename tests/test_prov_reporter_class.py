from provworkflow import ProvReporter, Workflow, Block
from rdflib import Graph


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

    w = Workflow()
    b = Block()
    w.blocks.append(b)
    print(w.persist(methods="string"))


if __name__ == "__main__":
    test_persist()
