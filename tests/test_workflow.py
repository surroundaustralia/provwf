from provworkflow import Workflow, PROVWF, ProvWorkflowException
import provworkflow.block
from rdflib import Literal
from rdflib.namespace import OWL, RDF, PROV, XSD
from datetime import datetime


def test_prov_to_graph():
    """A basic Workflow should prov_to_graph an Activity which is specialised as provwf:Workflow and has at least
    1 Block within it

    :return: None
    """

    w = Workflow()
    b1 = provworkflow.block.Block()
    b2 = provworkflow.block.Block()
    w.blocks.append(b1)
    w.blocks.append(b2)
    g = w.prov_to_graph()

    # check both generic and specific typing
    assert (w.uri, RDF.type, PROV.Activity) in g, "g must contain a prov:Activity"
    assert (w.uri, RDF.type, PROVWF.Workflow) in g, "g must contain a provwf:Workflow"

    assert (
        w.uri,
        OWL.versionIRI,
        Literal(w.version_uri, datatype=XSD.anyURI),
    ) in g, "g must contain an owl:versionIRI property for a provwf:Workflow instance"

    # check it contains 2 Blocks
    count = 0
    for o in g.subject_objects(PROVWF.hadBlock):
        count += 1

    assert count == 2, "This Workflow must contain 2 Blocks"

    # check start/end times of Blocks are within Workflow's
    for o in g.objects(subject=w.uri, predicate=PROV.startedAtTime):
        w_sat = datetime.strptime(str(o), "%Y-%m-%dT%H:%M:%S%z")

    for o in g.objects(subject=w.uri, predicate=PROV.endedAtTime):
        w_eat = datetime.strptime(str(o), "%Y-%m-%dT%H:%M:%S%z")

    for s in g.subjects(predicate=RDF.type, object=PROVWF.Block):
        for o in g.objects(subject=s, predicate=PROV.startedAtTime):
            if datetime.strptime(str(o), "%Y-%m-%dT%H:%M:%S%z") < w_sat:
                raise ProvWorkflowException(
                    "The started at times of all Blocks within a workflow must be greater than, or equal to, "
                    "the started at time of the Workflow"
                )

        for o in g.objects(subject=s, predicate=PROV.endedAtTime):
            if datetime.strptime(str(o), "%Y-%m-%dT%H:%M:%S%z") > w_eat:
                raise ProvWorkflowException(
                    "The ended at times of all Blocks within a workflow must be greater than, or equal to, "
                    "the ended at time of the Workflow"
                )


if __name__ == "__main__":
    test_prov_to_graph()
