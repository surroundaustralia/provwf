from provworkflow import ProvReporter, ProvWorkflowException
from provworkflow import _config as config
from rdflib.namespace import RDF
from rdflib import Graph
from franz.openrdf.connect import ag_connect
from franz.openrdf.rio.rdfformat import RDFFormat


class Workflow(ProvReporter):
    def __init__(self, uri=None, label=None, blocks=None):
        super().__init__(uri=uri, label=label)
        self.blocks = blocks
        if self.blocks is None:
            self.blocks = []

    def prov_to_graph(self, g=None, graph_uri=None):
        if self.blocks is None or len(self.blocks) < 1:
            raise ProvWorkflowException(
                "A Workflow must have at least one Block within it"
            )

        # TODO: can I do the g2 test here?
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, self.PROVWF.Workflow))

        # add the prov graph of each block to this Workflow's prov graph
        for block in self.blocks:
            block.prov_to_graph(g)
            # associate this Block with this Workflow
            g.add((self.uri, self.PROVWF.hadBlock, block.uri))

        if graph_uri is not None:
            g2 = Graph(identifier=graph_uri)
            g2.bind("prov", self.PROV)
            g2.bind("provwf", self.PROVWF)
            g2 += g

            return g2
        else:
            return g

    # see http://192.168.0.132:10035/doc/python/tutorial/example006.html
    def send_file_to_allegro(self, turtle_file_path, context_uri=None):
        """Sends an RDF file, with or without a given Context URI to AllegroGraph"""

        with ag_connect(
            config.ALLEGRO_REPO,
            host=config.ALLEGRO_HOST,
            port=config.ALLEGRO_PORT,
            user=config.ALLEGRO_USER,
            password=config.ALLEGRO_PASSWORD,
        ) as conn:
            conn.addFile(
                turtle_file_path,
                rdf_format=RDFFormat.TURTLE,
                context=conn.createURI(context_uri) if context_uri is not None else None,
            )

    def prov_to_allegro(self):
        """Sends the provenance graph of this Workflow to an AllegroGraph instance as a Turtle string

        The URI assigned to the Workflow us used for AllegroGraph context (graph URI) or a Blank Node is generated, if
        one is not given.

        :return: None
        :rtype: None
        """
        with ag_connect(
                config.ALLEGRO_REPO,
                host=config.ALLEGRO_HOST,
                port=config.ALLEGRO_PORT,
                user=config.ALLEGRO_USER,
                password=config.ALLEGRO_PASSWORD,
        ) as conn:
            conn.addData(
                self.prov_to_graph().serialize(format="turtle").decode("utf-8"),
                rdf_format=RDFFormat.TURTLE,
                context=conn.createURI(self.uri) if self.uri is not None else None,
            )
