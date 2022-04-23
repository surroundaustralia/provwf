# ProvWorkflow

This is a Python library for creating workflows of "Blocks", components of "Workflows" that log their actions in RDF, 
according to the [Prov Workflow (ProvWF)](https://data.surroundaustralia.com/def/provworkflow) profile of the 
[PROV-O standard](https://www.w3.org/TR/2013/REC-prov-o-20130430/).

A brief description of what provenance is, and the components used, reproduced from 
[PROV-DM: The PROV Data Model](https://www.w3.org/TR/2013/REC-prov-dm-20130430/):  

> _Provenance is information about entities, activities, and people involved in producing a piece of data or thing, 
which can be used to form assessments about its quality, reliability or trustworthiness. PROV-DM is the conceptual 
data model that forms a basis for the W3C provenance (PROV) family of specifications. PROV-DM distinguishes core 
structures, forming the essence of provenance information, from extended structures catering for more specific uses of 
provenance. PROV-DM is organized in six components, respectively dealing with: (1) entities and activities, and the time
 at which they were created, used, or ended; (2) derivations of entities from entities; (3) agents bearing
  responsibility for entities that were generated and activities that happened; (4) a notion of bundle, a mechanism to
   support provenance of provenance; (5) properties to link entities that refer to the same thing; and, (6) collections
    forming a logical structure for its members._

To use this library, add either of these to a requirements.txt and install, or install directly with pip install:  

* `git+ssh://git@bitbucket.org/surroundbitbucket/provwf.git`  
* `git+https://{USERNAME}@bitbucket.org/surroundbitbucket/provwf.git`

## Use & License
This software is made available for use under the [Creative Common Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See the [LICENSE](LICENSE) file for the deed.

## Contact

**SURROUND Australia Pty Ltd**  
<https://surroundaustralia.com>  
<info@surroundaustralia.com>  