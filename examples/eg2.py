from rdflib import URIRef
from provworkflow import Workflow, Block, Entity, Agent

# set up the Workflow and Block
w = Workflow(label="My Simple Workflow 2")
b = Block()

# Block 1
b.used = [
    Entity(value="local data"),
    Entity(access_uri="http://example.com/endpoint", service_parameters="x=42"),
]
e_int = Entity(label="Internal Entity")
e_ext = Entity(label="External Entity", external=True)
b.generated = [e_int, e_ext]
w.blocks.append(b)

# Block 2
b2 = Block()
b2.used = [Entity(value="other local data"), e_int, e_ext]
b2.generated.append(
    Entity(access_uri="http://somewhere-on-s3/d/e/f", label="Final Workflow Output")
)
w.blocks.append(b2)

# print out
print(w.persist("string"))
