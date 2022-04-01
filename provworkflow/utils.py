# from franz.openrdf.connect import ag_connect
# from franz.openrdf.rio.rdfformat import RDFFormat
import os
from pathlib import Path
import git
import requests
from typing import Union
from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import DCTERMS, PROV, RDF, XSD
from datetime import datetime


def query_sop_sparql(named_graph_uri, query, update=False):
    """
    Perform read and write SPARQL queries against a Surround Ontology Platform (SOP) instance
    :param named_graph_uri: the graph to write to within SOP, using it's internal name e.g.
    "urn:x-evn-master:test-datagraph"
    :param query: SPARQL query to send to the SPARQL endpoint
    :param update: update = write
    :return: HTTP response
    """

    endpoint = os.environ.get("SOP_BASE_URI", "http://localhost:8083")
    username = os.environ.get("SOP_USR", "Administrator")
    password = os.environ.get("SOP_PWD", "")

    global saved_session_cookies
    with requests.session() as s:
        s.get(endpoint + "/tbl")
        reuse_sessions = False
        # should be able to check the response contains
        if reuse_sessions and saved_session_cookies:
            s.cookies = saved_session_cookies
        else:
            s.post(
                endpoint + "/tbl/j_security_check",
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
        # force logout of session
        s.get(endpoint + "/tbl/purgeuser?app=edg")
        return response
        # .json() if response.text else {}


def make_sparql_insert_data(graph_uri, g):
    """Places RDF into a SPARQL INSERT DATA query"""
    nt = g.serialize(format="nt").decode()

    q = """
    INSERT DATA {{
        GRAPH <{}> {{
            {}
        }}
    }}
    """.format(
        graph_uri, nt
    )

    return q


def is_git_repo(path):
    """Determine whether the path is a Git repo"""
    try:
        _ = git.Repo(path).git_dir
        return path
    except git.exc.InvalidGitRepositoryError:
        return False


def get_git_repo(starting_dir: Path = None):
    """Finds the Git repo location (folder) if a given file is within one, however deep"""

    if starting_dir is not None:
        p = starting_dir
    else:
        p = Path.cwd().resolve()

    if p == Path("/"):
        return None

    if is_git_repo(p):
        return p
    else:
        return get_git_repo(p.parent.resolve())


def get_tag_or_commit(only_commit=False):
    """Gets a file's Git commit or Tag. Can be forced to get only the commit"""
    repo = git.Repo(get_git_repo())
    if only_commit:
        return repo.heads.master.commit

    if repo.tags:
        return repo.tags[0]
    else:
        return repo.heads.master.commit


def get_repo_uri():
    """Gets the URI of a file's repo's origin"""
    repo_dir = get_git_repo()
    if repo_dir is None:
        return None
    repo = git.Repo(repo_dir)
    origin_uri_with_user = repo.remotes.origin.url
    if origin_uri_with_user.find("@") >= 0:
        origin_uri_with_user = "https://" + origin_uri_with_user.split("@")[1]
    return origin_uri_with_user


def get_version_uri():
    """Gets the URI of a file's origin's commit or tag"""
    repo_uri = get_repo_uri()
    if repo_uri is None:
        return None
    id_ = str(get_tag_or_commit())

    if "bitbucket" in repo_uri:
        if len(id_) < 10:  # tag
            path = "/commits/tag/"
        else:  # commit
            path = "/commits/"
    elif "github" in repo_uri:
        if len(id_) < 10:  # tag
            path = "/releases/tag/"
        else:  # commit
            path = "/commit/"
    # TODO: David to add
    # elif "??" in repo_uri: # CodeCommit
    #     pass
    else:
        raise Exception("Only GitHub & BitBucket repos are supported")

    return repo_uri.replace(".git", "") + path + id_


def add_with_provenance(
    s: Union[URIRef, BNode],
    p: URIRef,
    o: Union[URIRef, BNode, Literal],
    block_uri: URIRef,
) -> Graph:
    """Creates a small graph, adds the given triple and also adds reified provenances for that triple"""
    g = Graph()
    # add the triple
    g.add((s, p, o))

    # add reified provenance
    x = BNode()
    g.add((x, RDF.type, RDF.Statement))
    g.add((x, RDF.subject, s))
    g.add((x, RDF.predicate, p))
    g.add((x, RDF.object, o))
    g.add(
        (
            x,
            DCTERMS.created,
            Literal(
                datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime
            ),
        )
    )
    g.add((x, PROV.wasAssociatedWith, block_uri))

    return g
