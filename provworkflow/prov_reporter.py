import uuid
from datetime import datetime
from typing import Union

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import PROV, RDF, RDFS, XSD

from provworkflow.utils import to_graphdb, to_sop


class ProvReporter:
    def __init__(self, uri_str=None, label=None, named_graph_uri=None):
        self.PROVWF = Namespace("https://data.surroundaustralia.com/def/profworkflow#")
        self.PWF = Namespace("https://data.surroundaustralia.com/dataset/provworkflow/")

        # give it an opaque UUID URI if one not given
        if uri_str is not None:
            self.uri = URIRef(uri_str)
        else:
            self.uri = URIRef(self.PWF + str(uuid.uuid1()))
        self.label = label

        self.started_at_time = datetime.now()
        self.ended_at_time = None

        self.named_graph_uri = named_graph_uri

    def prov_to_graph(self, g=None):
        """Reports self (instance properties and class type) to an in-memory graph using PROV-O

        :param g: rdflib Graph. If given, this function will add its contents to g. If not, it will create new
        :return: rdflib Graph
        """
        if g is None:
            if self.named_graph_uri is not None:
                g = Graph(identifier=URIRef(self.named_graph_uri))
            else:
                g = Graph()
        g.bind("prov", PROV)
        g.bind("provwf", self.PROVWF)

        # this instance's URI
        g.add((self.uri, RDF.type, PROV.Activity))

        # add a label if this Activity has one
        if self.label is not None:
            g.add((
                self.uri,
                RDFS.label,
                Literal(self.label, datatype=XSD.string),
            ))

        # all Activities have a startedAtTime
        # made at __init__() time
        g.add((
            self.uri,
            PROV.startedAtTime,
            Literal(self.started_at_time.isoformat(), datatype=XSD.dateTime),
        ))

        # if we don't yet have an endedAtTime recorded, make it now
        if self.ended_at_time is None:
            self.ended_at_time = datetime.now()

        # all Activities have a endedAtTime
        g.add((
            self.uri,
            PROV.endedAtTime,
            Literal(self.ended_at_time.isoformat(), datatype=XSD.dateTime),
        ))

        return g

    def serialize(self, file_path_str=None):
        # only print a graph-aware RDF serialization (trig) if the graph has a URI, not a Blank Node as an identifier
        if self.named_graph_uri is not None:
            s = self.prov_to_graph().serialize(format="trig").decode()
        else:
            s = self.prov_to_graph().serialize(format="turtle").decode()

        if file_path_str is None:
            return s
        else:
            try:
                with open(file_path_str, "w") as f:
                    f.write(s)
            except IOError as e:
                raise e

    def persist(self, persistence_methods: Union[str, list], **persistence_kwargs):
        """
        Persists ProvReporter instance graphs to one or more triplestores, or on disk.
        """

        if type(persistence_methods) == str:
            persistence_methods = [persistence_methods]

        for method in persistence_methods:
            assert method in ['GraphDB', 'SOP', 'TTL']

        # generate the graph to write
        g = self.prov_to_graph()
        # write to one or more persistence layers
        if 'GraphDB' in persistence_methods:
            to_graphdb(g, self.named_graph_uri)
        if 'SOP' in persistence_methods:
            to_sop(g, self.named_graph_uri)
        if 'TTL_file' in persistence_methods:
            self.serialize(persistence_kwargs['workflow_graph_file'])


class ProvWorkflowException(Exception):
    pass

