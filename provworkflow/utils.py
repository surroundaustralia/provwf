# from franz.openrdf.connect import ag_connect
# from franz.openrdf.rio.rdfformat import RDFFormat
import os
import requests


def query_sop_sparql(named_graph_uri, query, update=False):
    """
    Perform read and write SPARQL queries against a Surround Ontology Platform (SOP) instance
    :param named_graph_uri: the graph to write to within SOP, using it's internal name e.g. "urn:x-evn-master:test-datagraph"
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
            "default-graph-uri": named_graph_uri,
        }
        if update:
            data["update"] = query
            data["using-graph-uri"] = named_graph_uri
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
