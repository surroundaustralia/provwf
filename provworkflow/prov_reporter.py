import logging
import os
import signal
import uuid
from typing import Union

import requests
from franz.openrdf.connect import ag_connect
from franz.openrdf.rio.rdfformat import RDFFormat
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import PROV, RDF, RDFS, XSD

from .namespace import PROVWF, PWFS
from .utils import make_sparql_insert_data, query_sop_sparql


class ProvReporter:
    def __init__(
        self, uri: URIRef = None, label: str = None, named_graph_uri: URIRef = None,
    ):
        # give it an opaque UUID URI if one not given
        if uri is not None:
            self.uri = uri
        else:
            self.uri = URIRef(PWFS + str(uuid.uuid1()))
        self.label = label

        self.named_graph_uri = named_graph_uri

    def prov_to_graph(self, g: Graph = None) -> Graph:
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
        g.bind("provwf", PROVWF)
        g.bind("pwfs", PWFS)

        # this instance's URI
        g.add((self.uri, RDF.type, PROVWF.ProvReporter))

        # add a label if this Activity has one
        if self.label is not None:
            g.add((self.uri, RDFS.label, Literal(self.label, datatype=XSD.string),))

        return g

    def _persist_to_file(self, g: Graph = None, rdf_file_path: str = "prov_reporter"):
        if g is None:
            g = self.prov_to_graph()

        # remove file extension if added as system will add appropriate one
        rdf_file_path = rdf_file_path.replace(".ttl", "")
        rdf_file_path = rdf_file_path.replace(".trig", "")

        if self.named_graph_uri is None:
            g.serialize(destination=rdf_file_path + ".ttl", format="turtle")
        else:
            g.serialize(destination=rdf_file_path + ".trig", format="trig")

    def _persist_to_graphdb(self, g: Graph = None):
        """
        generic util to write a given graph to graphdb
        :param context: the named graph to add the triples to
        :param graph:
        :return: a status code
        """
        if g is None:
            g = self.prov_to_graph()

        GRAPH_DB_BASE_URI = os.environ.get("GRAPH_DB_BASE_URI", "http://localhost:7200")
        GRAPH_DB_REPO_ID = os.environ.get("GRAPH_DB_REPO_ID", "provwftesting")
        GRAPHDB_USR = os.environ.get("GRAPHDB_USR", "")
        GRAPHDB_PWD = os.environ.get("GRAPHDB_PWD", "")

        data = g.serialize(format="turtle", encoding="utf-8")

        # graphdb expects the context (named graph) wrapped in < & >
        if self.named_graph_uri != "null":
            if self.named_graph_uri is None:
                context = "null"
            else:
                context = "<" + self.named_graph_uri + ">"

        r = requests.post(
            GRAPH_DB_BASE_URI + "/repositories/" + GRAPH_DB_REPO_ID + "/statements",
            params={"context": context},
            data=data,
            headers={"Content-Type": "text/turtle"},
            auth=(GRAPHDB_USR, GRAPHDB_PWD),
        )
        logging.info(
            f"Attempted to write triples to GraphDB and got status code: {r.status_code} returned"
        )
        if r.status_code != 204:
            raise Exception(f"GraphDB says: {r.text}")

    def _persist_to_sop(self, g: Graph = None):
        """
        generic util to write a given graph to graphdb
        :param named_graph_uri: the data graph to add the triples to
        :param graph: the graph to be written out
        :return: a status code
        """
        if g is None:
            g = self.prov_to_graph()

        # TODO: determine if we need to set a default SOP graph ID
        # if self.named_graph_uri is None:
        #     self.named_graph_uri = "http://example.com"
        query = make_sparql_insert_data(self.named_graph_uri, g)
        r = query_sop_sparql(self.named_graph_uri, query, update=True)

        logging.info(
            f"Attempted to write triples to SOP and got status code: {r.status_code} returned"
        )
        if not r.ok:
            raise Exception(f"SOP HTTP error: {r.text}")

    # TODO: retest this method as needed
    def _persist_to_allegro(self, g: Graph = None):
        """Sends the provenance graph of this Workflow to an AllegroGraph instance as a Turtle string

        The URI assigned to the Workflow us used for AllegroGraph context (graph URI) or a Blank Node is generated, if
        one is not given.

        The function will error out if connection & transfer not complete after 5 seconds.

        Environment variables are required for connection details.

        :return: None
        :rtype: None
        """
        if g is None:
            g = self.prov_to_graph()

        vars = [
            os.environ.get("ALLEGRO_REPO"),
            os.environ.get("ALLEGRO_HOST"),
            os.environ.get("ALLEGRO_PORT"),
            os.environ.get("ALLEGRO_USER"),
            os.environ.get("ALLEGRO_PASSWORD"),
        ]
        assert all(v is not None for v in vars), (
            "You must set the following environment variables: "
            "ALLEGRO_REPO, ALLEGRO_HOST, ALLEGRO_PORT, ALLEGRO_USER & "
            "ALLEGRO_PASSWORD"
        )

        def connect_and_send():
            with ag_connect(
                os.environ["ALLEGRO_REPO"],
                host=os.environ["ALLEGRO_HOST"],
                port=int(os.environ["ALLEGRO_PORT"]),
                user=os.environ["ALLEGRO_USER"],
                password=os.environ["ALLEGRO_PASSWORD"],
            ) as conn:
                conn.addData(
                    g.serialize(format="turtle").decode("utf-8"),
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

    # # see http://192.168.0.132:10035/doc/python/tutorial/example006.html
    # def send_file_to_allegro(self, turtle_file_path, context_uri=None):
    #     """Sends an RDF file, with or without a given Context URI to AllegroGraph.
    #
    #     The function will error out if connection & transfer not complete after 5 seconds.
    #
    #     Environment variables are required for connection details."""
    #
    #     vars = [
    #         os.environ.get('ALLEGRO_REPO'),
    #         os.environ.get('ALLEGRO_HOST'),
    #         os.environ.get('ALLEGRO_PORT'),
    #         os.environ.get('ALLEGRO_USER'),
    #         os.environ.get('ALLEGRO_PASSWORD')
    #     ]
    #     assert all(v is not None for v in vars), "You must set the following environment variables: " \
    #                                              "ALLEGRO_REPO, ALLEGRO_HOST, ALLEGRO_PORT, ALLEGRO_USER & " \
    #                                              "ALLEGRO_PASSWORD"
    #
    #     def connect_and_send():
    #         with ag_connect(
    #                 os.environ['ALLEGRO_REPO'],
    #                 host=os.environ['ALLEGRO_HOST'],
    #                 port=int(os.environ['ALLEGRO_PORT']),
    #                 user=os.environ['ALLEGRO_USER'],
    #                 password=os.environ['ALLEGRO_PASSWORD'],
    #         ) as conn:
    #             conn.addFile(
    #                 turtle_file_path,
    #                 rdf_format=RDFFormat.TURTLE,
    #                 context=conn.createURI(context_uri) if context_uri is not None else None,
    #             )
    #
    #     def handler(signum, frame):
    #         raise Exception("Connecting to AllegroGraph failed")
    #
    #     signal.signal(signal.SIGALRM, handler)
    #
    #     signal.alarm(5)
    #
    #     try:
    #         connect_and_send()
    #     except Exception as exc:
    #         print(exc)

    def persist(
        self, methods: Union[str, list], rdf_file_path: str = "prov_reporter"
    ) -> Union[None, str]:
        if type(methods) == str:
            methods = [methods]

        known_methods = ["graphdb", "sop", "allegro", "file", "string"]
        for method in methods:
            if method not in known_methods:
                raise ProvReporterException(
                    "A persistent method you selected, {}, is not in the list of known methods, '{}'".format(
                        method, "', '".join(known_methods)
                    )
                )

        # write to one or more persistence layers
        g = self.prov_to_graph()
        if "file" in methods:
            self._persist_to_file(g, rdf_file_path)
        if "graphdb" in methods:
            self._persist_to_graphdb(g)
        if "sop" in methods:
            self._persist_to_sop(g)
        if "allegro" in methods:
            self._persist_to_allegro(g)

        # final persistent option
        if "string" in methods:
            if self.named_graph_uri is None:
                return g.serialize(format="turtle").decode()
            else:
                return g.serialize(format="trig").decode()


class ProvReporterException(Exception):
    pass
