from typing import List
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DCAT, PROV, RDF, XSD

from .namespace import PROVWF
from .prov_reporter import ProvReporter
from .agent import Agent
from .entity import Entity

# from .activity import Activity


class DataService(Entity):
    """dcat:DataService

    :param uri: A URI you assign to the DataService instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to None
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign, defaults to None
    :type named_graph_uri: Union[URIRef, str], optional

    :param access_uri: (dcat:accessURL) should be used to contain links used to access the content of the Entity, e.g. a
        Google Cloud Services API call or an S2 Bucket link.
    :type access_uri: str, optional

    :param service_parameters: (provwf:serviceParameters) should be used to contain any parameters used for web
        services accessed via access_uri that are not contained within the URI itself.
    :type service_parameters: str, optional

    :param was_used_by: The inverse of prov:used: this indicates which Activities prov:used this Entity
    :type was_used_by: Activity, optional

    :param was_generated_by: Generation is the completion of production of a new entity by an activity. This entity
        did not exist before generation and becomes available for usage after this generation.
    :type was_generated_by: Activity, optional

    :param was_attributed_to: An Agent that this Entity is ascribed to (created by). Note "this Entity" refers to this
    occurence of use of the DataService, not the DataService in general, so it's the Agent that specified DataService
     use at this time, with these parameters.
    :type was_attributed_to: Agent, optional

    :param serves_datasets: Dataset Entities that this DataServise provides access to.
    This is a form of dcat:distribution
    :type serves_datasets: Entity, optional

    :param external: Whether or not this Entity exists outside the workflow
    :type external: bool, optional
    """

    def __init__(
        self,
        uri: URIRef = None,
        label: str = None,
        named_graph_uri: URIRef = None,
        value: str = None,
        access_uri: str = None,
        service_parameters: str = None,
        was_used_by=None,
        was_generated_by=None,
        was_attributed_to: Agent = None,
        serves_datasets: List[Entity] = None,
        external: bool = None,
    ):
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

        self.value = Literal(value) if value is not None else None
        self.access_uri = (
            Literal(access_uri, datatype=XSD.anyURI) if access_uri is not None else None
        )
        self.service_parameters = (
            Literal(service_parameters) if service_parameters is not None else None
        )
        if type(was_used_by) != list:
            self.was_used_by = [was_used_by]
        else:
            self.was_used_by = was_used_by
        if type(was_generated_by) != list:
            self.was_generated_by = [was_generated_by]
        else:
            self.was_used_by = was_used_by
        self.was_attributed_to = was_attributed_to
        self.serves_datasets = serves_datasets
        self.external = external

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        g.bind("dcat", DCAT)

        # add in type
        g.add((self.uri, RDF.type, DCAT.DataService))
        g.remove((self.uri, RDF.type, PROV.Entity))

        if self.serves_datasets is not None:
            for d in self.serves_datasets:
                d.prov_to_graph(g)
                g.add((self.uri, DCAT.servesDataset, d.uri))

        return g
