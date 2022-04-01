from rdflib import URIRef
from provworkflow import Workflow, Block, Entity, Agent

# set up the Workflow and Block
w = Workflow(label="My Simple Workflow")
nick = Agent(uri=URIRef("https://orcid.org/0000-0002-8742-7730"), label="Nick")
b = Block(was_associated_with=nick)

# do some (fake) work
fake_data = "local data"
params = """
{
    "a": 42,
    "q": "unknown"
}

Accept: application/json
"""
b.used = [
    Entity(value=fake_data),
    Entity(uri="http://example.com/endpoint", value=params),
]

b.generated.append(Entity(was_attributed_to=nick, uri="http://somewhere-on-s3/a/b/c"))

w.blocks.append(b)

# print out
print(w.persist("string"))
