from typing import List, Union

from rdflib import URIRef
from rdflib.namespace import RDF, RDFS

from .activity import Activity
from .agent import Agent
from .entity import Entity
from .namespace import PROVWF
from .exceptions import ProvWorkflowException


class Block(Activity):
    """A specialised type of prov:Activity that must live within a Workflow.

    For its Semantic Web definition, see https://data.surroundaustralia.com/def/provworkflow/Block (not available yet)

    :param uri: A URI you assign to the ProvReporter instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to None
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign, defaults to None
    :type named_graph_uri: Union[URIRef, str], optional

    :param used: A list of Entities used (prov:used) by this Block
    :type used: List[Block], optional

    :param generated: A list of Entities used (prov:generated) by this Block
    :type generated: List[Block], optional

    :param was_associated_with: An Agent that ran this Block (prov:wasAssociatedWith), may or may not be the same as
        the one associated with the Workflow, defaults to None
    :type was_associated_with: Agent, optional

    :param class_uri: A URI for the class of this specialised type of Block. Instances of this class will be typed
        (rdf:type) with this URI as well as being subclassed (rdfs:subClassOf) provwf:Block
    :type class_uri: Union[URIRef, str], optional
    """
    def __init__(
        self,
        uri: Union[URIRef, str] = None,
        label: str = None,
        named_graph_uri: URIRef = None,
        used: List[Entity] = None,
        generated: List[Entity] = None,
        was_associated_with: Agent = None,
        class_uri: Union[URIRef, str] = None,
    ):
        super().__init__(
            uri=uri,
            label=label,
            named_graph_uri=named_graph_uri,
            used=used,
            generated=generated,
            was_associated_with=was_associated_with,
        )

        self.class_uri = URIRef(class_uri) if type(class_uri) == str else class_uri

        if self.__class__.__name__ == "Block" and self.class_uri is not None:
            raise ProvWorkflowException(
                "If the class Block is used directly, i.e. without specialisation, class_uri must not be set")
        elif self.__class__.__name__ != "Block" and self.class_uri is None:
            raise ProvWorkflowException("A specialised Block must have a class_uri instance variable supplied")
        elif self.class_uri is not None and not self.class_uri.startswith("http"):
            raise ProvWorkflowException("If supplied, a class_uri must start with http")

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        g.add((self.uri, RDF.type, PROVWF.Block))

        # add in type
        if self.__class__.__name__ != "Block":
            g.add((self.uri, RDFS.subClassOf, PROVWF.Block))
            g.add((self.uri, RDF.type, self.class_uri))

        return g
