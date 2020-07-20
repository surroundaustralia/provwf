from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, XSD
from datetime import datetime, timezone


class ProvReporter:
    def __init__(self, uri_str=None, label=None):
        self.PROV = Namespace("http://www.w3.org/ns/prov#")
        self.PROVWF = Namespace("https://data.surroundaustralia.com/def/profworkflow#")

        # give it a Blank Node if one not given
        if uri_str is not None:
            self.uri = URIRef(uri_str)
        else:
            self.uri = BNode()
        self.label = label

        self.started_at_time = datetime.now()
        self.ended_at_time = None

    def prov_to_graph(self, g=None):
        """Reports self (instance properties and class type) to an in-memory graph using PROV-O

        :param g: rdflib Graph. If given, this function will add its contents to g. If not, it will create new
        :return: rdflib Graph
        """
        """

        :return: 
        """
        if g is None:
            g = Graph()

        g.bind("prov", self.PROV)
        g.bind("provwf", self.PROVWF)

        # this instance's URI
        g.add((self.uri, RDF.type, self.PROV.Activity))

        # add a label if this Activity has one
        if self.label is not None:
            g.add(
                (
                    self.uri,
                    RDFS.label,
                    Literal(self.label, datatype=XSD.string),
                )
            )

        # all Activities have a startedAtTime
        # made at __init__() time
        g.add(
            (
                self.uri,
                self.PROV.startedAtTime,
                Literal(self.started_at_time.isoformat(), datatype=XSD.dateTime),
            )
        )

        # if we don't yet have an endedAtTime recorded, make it now
        if self.ended_at_time is None:
            self.ended_at_time = datetime.now()

        # all Activities have a endedAtTime
        g.add(
            (
                self.uri,
                self.PROV.endedAtTime,
                Literal(self.ended_at_time.isoformat(), datatype=XSD.dateTime),
            )
        )

        return g

    def serialize(self, graph, file_path_str=None):
        if file_path_str is None:
            return graph.serialize(format="trig").decode("utf-8")
        else:
            try:
                with open(file_path_str, "w") as f:
                    f.write(graph.serialize(format="trig").decode("utf-8"))
            except IOError as e:
                raise e


class ProvWorkflowException(Exception):
    pass

