from rdflib import URIRef, Namespace
from rdflib.namespace import ClosedNamespace

# this namespace is closed, i.e. it contains _all_ the members of the ProvWF Ontology
# only members listed in _terms_ can be implemented like PROVWF.{member}
PROVWF = ClosedNamespace(
    uri=URIRef("https://data.surroundaustralia.com/def/provworkflow/"),
    terms=[
        "ProvReporter",
        "Workflow",
        "Block",
        "ErrorEntity",
        "Machine",
        "hadBlock",
        "serviceParameters",
    ],
)

# this is the fall-back namespace for Workflow instances
# Workflow instances will be allocated a URI of PWFS.{UUI} if not explicitly given one
PWFS = Namespace("https://data.surroundaustralia.com/dataset/provworkflows/")
