# Examples

1. _eg1_ - A simple Workflow with one Block using two Entities, generation one Entity and associated with an Agent
    - the Workflow, rather than the Block, could be associated with that or a different Agent
    - it may often make more sense to associate only the Workflow with an Agent and assume that all Blocks within it are associated with the same Agent
    
2. _eg2_ - A Workflow with a couple of Blocks showing Internal and External Entities. 
    - Entities can be declared as External - i.e. input/output from the Workflow as a whole, even if they appear, by use, to be Internal only. This is done via setting a property on the Entity in the application code.
    
3. _eg3_ - Details of the Workflow and Block `owl:versionIRI` property

4. _eg4_ - Multiple uses of Agent
   - The Workflow indicates it was associated (run on or by) the Agent _Server A_
   - _Server A_, in turn, was run by _Person B_
   - One of the Blocks was run on or by _Web Service C_
   - Remaining _Block Y_, since no Agent info is given, is assumed to share the same agent as its parent, here _Workflow X_ so that is _Server A_ (and, transitively, _Person B_)
   - _Entity S3 data_ can be inferred to be attributed to (`prov:wasAttributedTo`) _Server A_ since that is the Agent that ran the Block (and Workflow) that generated it
   
**Rule of thumb for agents**: record whatever info it likely to be of importance in reviewing/learning from the workflow's provenance.