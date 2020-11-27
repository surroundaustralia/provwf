from provworkflow import ProvReporter, ProvWorkflowException
from rdflib.namespace import RDF
from rdflib import Graph, URIRef
from utils import to_graphdb
# from franz.openrdf.connect import ag_connect
# from franz.openrdf.rio.rdfformat import RDFFormat
import os
import signal
import requests


class Workflow(ProvReporter):
    def __init__(self, uri_str=None, label=None, blocks=None, named_graph_uri=None):
        super().__init__(uri_str=uri_str, label=label, named_graph_uri=named_graph_uri)
        self.blocks = blocks
        if self.blocks is None:
            self.blocks = []

    def prov_to_graph(self, g=None):
        if self.blocks is None or len(self.blocks) < 1:
            raise ProvWorkflowException(
                "A Workflow must have at least one Block within it"
            )

        if g is None:
            if self.named_graph_uri is not None:
                g = Graph(identifier=URIRef(self.named_graph_uri))
            else:
                g = Graph()

        # add in type
        g.add((self.uri, RDF.type, self.PROVWF.Workflow))

        # add the prov graph of each block to this Workflow's prov graph
        for block in self.blocks:
            block.prov_to_graph(g)
            # associate this Block with this Workflow
            g.add((self.uri, self.PROVWF.hadBlock, block.uri))

        # build all the details for the Workflow itself
        g = super().prov_to_graph(g)

        return g

    # see http://192.168.0.132:10035/doc/python/tutorial/example006.html
    def send_file_to_allegro(self, turtle_file_path, context_uri=None):
        """Sends an RDF file, with or without a given Context URI to AllegroGraph.

        The function will error out if connection & transfer not complete after 5 seconds.

        Environment variables are required for connection details."""

        vars = [
            os.environ.get('ALLEGRO_REPO'),
            os.environ.get('ALLEGRO_HOST'),
            os.environ.get('ALLEGRO_PORT'),
            os.environ.get('ALLEGRO_USER'),
            os.environ.get('ALLEGRO_PASSWORD')
        ]
        assert all(v is not None for v in vars), "You must set the following environment variables: " \
                                             "ALLEGRO_REPO, ALLEGRO_HOST, ALLEGRO_PORT, ALLEGRO_USER & " \
                                             "ALLEGRO_PASSWORD"

        def connect_and_send():
            with ag_connect(
                os.environ['ALLEGRO_REPO'],
                host=os.environ['ALLEGRO_HOST'],
                port=int(os.environ['ALLEGRO_PORT']),
                user=os.environ['ALLEGRO_USER'],
                password=os.environ['ALLEGRO_PASSWORD'],
            ) as conn:
                conn.addFile(
                    turtle_file_path,
                    rdf_format=RDFFormat.TURTLE,
                    context=conn.createURI(context_uri) if context_uri is not None else None,
                )

        def handler(signum, frame):
            raise Exception("Connecting to AllegroGraph failed")

        signal.signal(signal.SIGALRM, handler)

        signal.alarm(5)

        try:
            connect_and_send()
        except Exception as exc:
            print(exc)

    def prov_to_allegro(self):
        """Sends the provenance graph of this Workflow to an AllegroGraph instance as a Turtle string

        The URI assigned to the Workflow us used for AllegroGraph context (graph URI) or a Blank Node is generated, if
        one is not given.

        The function will error out if connection & transfer not complete after 5 seconds.

        Environment variables are required for connection details.

        :return: None
        :rtype: None
        """

        vars = [
            os.environ.get('ALLEGRO_REPO'),
            os.environ.get('ALLEGRO_HOST'),
            os.environ.get('ALLEGRO_PORT'),
            os.environ.get('ALLEGRO_USER'),
            os.environ.get('ALLEGRO_PASSWORD')
        ]
        assert all(v is not None for v in vars), "You must set the following environment variables: " \
                                             "ALLEGRO_REPO, ALLEGRO_HOST, ALLEGRO_PORT, ALLEGRO_USER & " \
                                             "ALLEGRO_PASSWORD"

        def connect_and_send():
            with ag_connect(
                os.environ['ALLEGRO_REPO'],
                host=os.environ['ALLEGRO_HOST'],
                port=int(os.environ['ALLEGRO_PORT']),
                user=os.environ['ALLEGRO_USER'],
                password=os.environ['ALLEGRO_PASSWORD'],
            ) as conn:
                conn.addData(
                    self.prov_to_graph().serialize(format="turtle").decode("utf-8"),
                    rdf_format=RDFFormat.TURTLE,
                    context=conn.createURI(self.uri) if self.uri is not None else None,
                )

        def handler(signum, frame):
            raise Exception("Connecting to AllegroGraph failed")

        signal.signal(signal.SIGALRM, handler)

        signal.alarm(5)

        try:
            connect_and_send()
        except Exception as exc:
            print(exc)

    def prov_to_graphdb(self):

        to_graphdb(self.prov_to_graph())
