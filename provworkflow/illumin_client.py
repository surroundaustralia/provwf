from provworkflow import ProvWorkflowException
from provworkflow import Block
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, XSD


class IlluminClient(Block):
    def __init__(self):
        super().__init__()

        self.query = None
        self.query_start = None  # TODO: put a datetime.now().toisodatetiem thin in here when sent to Illumin
        self.query_end = None
        self.illumin_result = None
        self.illumin_error = None

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((URIRef(self.uri), RDF.type, self.PROVWF.IlluminClient))

        # add in the query
        iq = BNode()
        g.add((
            iq,
            RDF.type,
            self.PROV.Activity
        ))
        g.add((
            iq,
            RDF.type,
            self.PROVWF.IlluminQuering
        ))
        g.add((
            iq,
            self.PROV.startedAtTime,
            Literal(self.query_start, datatype=XSD.dateTime)
        ))
        g.add((
            iq,
            self.PROV.endedAtTime,
            Literal(self.query_start, datatype=XSD.dateTime)
        ))

        # the actual query text
        query_entity = BNode()
        g.add((
            query_entity,
            RDF.type,
            self.PROV.Entity
        ))
        g.add((
            query_entity,
            RDF.type,
            self.PROV.Plan
        ))
        g.add((
            query_entity,
            self.PROV.value,
            Literal(self.query, datatype=XSD.string)
        ))
        g.add((
            iq,
            self.PROV.used,
            query_entity
        ))

        # query results
        query_result = BNode()
        g.add((
            query_result,
            RDF.type,
            self.PROV.Entity
        ))
        if self.illumin_error:
            g.add((
                query_result,
                RDF.type,
                self.PROV.IlluminError
            ))
            g.add((
                query_result,
                self.PROV.value,
                Literal(self.illumin_error, datatype=XSD.string)
            ))
        else:
            g.add((
                query_result,
                RDF.type,
                self.PROV.IlluminResult
            ))
            g.add((
                query_result,
                self.PROV.value,
                Literal(self.illumin_result, datatype=XSD.string)
            ))
        g.add((
            iq,
            self.PROV.generated,
            query_result
        ))

        # link the IlluminClient (a prov:Activity) to the IlluminQuering (prov:Activity)
        g.add((
            URIRef(self.uri),
            self.PROVWF.hadQuerying,
            iq
        ))

        # TODO: store the execution details of the query (when it was lodged, how long it took)

        # TODO: store query result as per storing query

        # TODO: if Illumin exeption, still generate PROV but ensure you store exception

        return g

    def send_query(self, query):
        # store this query for PROV
        self.query = query
        # validate query is GraphQL
        # send to Illumin (SOP)
        # store result somehow
            # for now, store returned JSON? in an instance var
            # store any error messages too
            # e = IlluminException("This is a custom message")
        pass


class IlluminException(Exception):
    pass


if __name__ == "__main__":
    ic = IlluminClient()
    q = """
        PUT IN NICE GraphQL!
        """

    ic.send_query(q)
