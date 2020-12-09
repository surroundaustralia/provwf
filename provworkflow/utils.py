import logging
# from franz.openrdf.connect import ag_connect
# from franz.openrdf.rio.rdfformat import RDFFormat
import os
import signal
from typing import Union

import requests
from rdflib import Graph


def to_graphdb(graph: Graph, context="null"):
    """
    generic util to write a given graph to graphdb
    :param context: the named graph to add the triples to
    :param graph:
    :return: a status code
    """

    GRAPH_DB_BASE_URI = os.environ.get("GRAPH_DB_BASE_URI", "http://localhost:7200")
    GRAPH_DB_REPO_ID = os.environ.get("GRAPH_DB_REPO_ID", "sarobot")
    GRAPHDB_USR = os.environ.get("GRAPHDB_USR", "admin")
    GRAPHDB_PWD = os.environ.get("GRAPHDB_PWD", "sortrobot")

    data = graph.serialize(format="turtle", encoding="utf-8")

    # graphdb expects the context (named graph) wrapped in < & >
    if context != "null":
        if context is None:
            context = "null"
        else:
            context = '<'+context+'>'

    r = requests.post(
        GRAPH_DB_BASE_URI + "/repositories/" + GRAPH_DB_REPO_ID + "/statements",
        params={"context": context},
        data=data,
        headers={"Content-Type": "text/turtle"},
        auth=(GRAPHDB_USR, GRAPHDB_PWD)
    )
    logging.info(f'Attempted to write triples to GraphDB and got status code: {r.status_code} returned')
    if r.status_code != 204:
        raise Exception(f"GraphDB says: {r.text}")


def query_sop_sparql(graph_uri, query, update=False):
    """
    Perform read and write SPARQL queries against a Surround Ontology Platform (SOP) instance
    :param graph_uri: the graph to write to within SOP, using it's internal name e.g. "urn:x-evn-master:test-datagraph"
    :param query: SPARQL query to send to the SPARQL endpoint
    :param update: update = write
    :return: HTTP response
    """

    endpoint = os.environ.get("SOP_BASE_URI", "http://localhost:8083")
    username = os.environ.get("GRAPHDB_USR", "Administrator")
    password = os.environ.get("GRAPHDB_PWD", "")

    global saved_session_cookies
    with requests.session() as s:
        site = s.get(endpoint + "/tbl")
        reuse_sessions = False
        ## should be able to check the response contains
        if reuse_sessions and saved_session_cookies:
            s.cookies = saved_session_cookies
        else:
            s.post(endpoint + "/tbl/j_security_check",
                   {"j_username": username, "j_password": password},
                   )
            # detect success!
            if reuse_sessions:
                saved_session_cookies = s.cookies

        data = {
            "default-graph-uri": graph_uri,
        }
        if update:
            data["update"] = query
            data["using-graph-uri"] = graph_uri
        else:
            data["query"] = query
            data["with-imports"] = "true"

        response = s.post(
            endpoint + "/tbl/sparql",
            data=data,
            headers={"Accept": "application/sparql-results+json"},
        )
        ## force logout of session
        s.get(endpoint + "/tbl/purgeuser?app=edg")
        return response
        # .json() if response.text else {}


def make_sparql_insert_data(graph_uri, g):
    nt = g.serialize(format="nt").decode()

    q = """
    INSERT DATA {{
        GRAPH <{}> {{
            {}
        }}
    }}
    """.format(graph_uri, nt)

    return q


def to_sop(graph: Graph, named_graph_uri):
    """
    generic util to write a given graph to graphdb
    :param named_graph_uri: the data graph to add the triples to
    :param graph: the graph to be written out
    :return: a status code
    """

    query = make_sparql_insert_data(named_graph_uri, graph)
    r = query_sop_sparql(named_graph_uri, query, update=True)

    logging.info(f'Attempted to write triples to SOP and got status code: {r.status_code} returned')
    if not r.ok:
        raise Exception(f"SOP HTTP error: {r.text}")


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


def persist_graph(graph, persistence_methods: Union[str, list], named_graph_uri, **persistence_kwargs):
    """
    Persists ProvReporter instance graphs to one or more triplestores, or on disk.
    """

    if type(persistence_methods) == str:
        persistence_methods = [persistence_methods]

    for method in persistence_methods:
        assert method in ['GraphDB', 'SOP', 'TTL']

    # write to one or more persistence layers
    if 'GraphDB' in persistence_methods:
        to_graphdb(graph, named_graph_uri)
    if 'SOP' in persistence_methods:
        to_sop(graph, named_graph_uri)
    if 'TTL_file' in persistence_methods:
        graph.serialize
        if named_graph_uri != None:
            s = graph.serialize(format="trig").decode()
        else:
            s = graph.serialize(format="turtle").decode()
        with open(persistence_kwargs['workflow_graph_file']) as file:
            file.write(s)
        # serialize()