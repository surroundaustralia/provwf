from rdflib import URIRef
from provworkflow import Workflow, Block, Entity, Agent

# set up the Workflow and Block
w = Workflow(label="My Simple Workflow")
nick = Agent(uri=URIRef("https://orcid.org/0000-0002-8742-7730"), label="Nick")
b = Block(was_associated_with=nick)

# do some (fake) work
fake_data = "local data"
fake_web_service = "http://example.com/endpoint"
params = """
{
    "a": 42,
    "q": "unknown"
}

Accept: application/json
"""
b.used = [
    Entity(value=fake_data),
    Entity(access_uri=fake_web_service, service_parameters=params)
]

b.generated.append(
    Entity(access_uri="http://fake-s3-in-aws.com/object/x", was_attributed_to=nick)
)

w.blocks.append(b)

# print out
print(w.persist("string"))