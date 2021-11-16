import logging
import os

# import signal
import uuid
from _datetime import datetime
from typing import Union

import requests

# from franz.openrdf.connect import ag_connect
# from franz.openrdf.rio.rdfformat import RDFFormat
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DCTERMS, PROV, OWL, RDF, RDFS, XSD

from .exceptions import ProvWorkflowException
from .namespace import PROVWF, PWFS
from .utils import make_sparql_insert_data, query_sop_sparql, get_version_uri


class class_or_instance_method(classmethod):
    def __get__(self, instance, type_):
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)


class ProvReporter:
    """Created provwf:ProvReporter instances.

    For its Semantic Web definition, see https://data.surroundaustralia.com/def/provworkflow/ProvReporter
     (not available yet)

    ProvReporter is a superclass of all PROV classes (Entity, Activity, Agent) and is created here just to facilitate
    logging. You should NOT directly instantiate this class - it is essentially abstract. Use instead, Entity, Activity
    etc., including grandchildren such as Block & Workflow.

    ProvReporters automatically record created times (dcterms:created) and an instance version IRI which is collected
    from the instance's Git version (URI of the Git origin repo, not local).

    :param uri: A URI you assign to the ProvReporter instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to None
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign, defaults to None
    :type named_graph_uri: Union[URIRef, str], optional
    """

    def __init__(
        self,
        uri: Union[URIRef, str] = None,
        label: Union[Literal, str] = None,
        named_graph_uri: Union[URIRef, str] = None,
        class_uri: Union[URIRef, str] = None,
    ):
        # give it an opaque UUID-based URI if one not given
        if uri is not None:
            self.uri = URIRef(uri) if type(uri) == str else uri
        else:
            self.uri = URIRef(PWFS + str(uuid.uuid1()))
        self.label = Literal(label) if type(label) == str else label
        self.named_graph_uri = (
            URIRef(named_graph_uri) if type(named_graph_uri) == str else named_graph_uri
        )

        # class specialisations
        if class_uri is not None:
            self.class_uri = URIRef(class_uri) if type(class_uri) == str else class_uri

            known_classes = ["Entity", "Activity", "Agent", "Workflow", "Block"]
            if self.__class__.__name__ in known_classes and self.class_uri is not None:
                raise ProvWorkflowException(
                    "If a ProvWorkflow-defined class is used without specialisation, class_uri must not be set"
                )
            elif (
                self.__class__.__name__ not in known_classes and self.class_uri is None
            ):
                raise ProvWorkflowException(
                    "A specialised Block must have a class_uri instance variable supplied"
                )
            elif self.class_uri is not None and not self.class_uri.startswith("http"):
                raise ProvWorkflowException(
                    "If supplied, a class_uri must start with http"
                )

        # from Git info
        uri_str = get_version_uri()
        if uri_str is not None:
            self.version_uri = URIRef(uri_str)

        # fallback version
        if not hasattr(self, "version_uri"):
            self.version_uri = self.uri

        self.created = Literal(
            datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"),
            datatype=XSD.dateTimeStamp,
        )

    def prov_to_graph(self, g: Graph = None) -> Graph:
        if g is None:
            if self.named_graph_uri is not None:
                g = Graph(identifier=URIRef(self.named_graph_uri))
            else:
                g = Graph()
        g.bind("prov", PROV)
        g.bind("provwf", PROVWF)
        g.bind("pwfs", PWFS)
        g.bind("owl", OWL)
        g.bind("dcterms", DCTERMS)

        # this instance's URI
        g.add((self.uri, RDF.type, PROVWF.ProvReporter))
        g.add((self.uri, DCTERMS.created, self.created))

        # add a label if this Activity has one
        if self.label is not None:
            g.add((self.uri, RDFS.label, Literal(self.label, datatype=XSD.string)))

        return g
