MIABIS is focused on standardizing the data elements used to describe biobanks, research on samples, and related data.
The goal of MIABIS is to enhance interoperability among biobanks that share valuable data and samples. MIABIS Core 2.0,
introduced in 2016, established general attributes at an aggregated/metadata level for describing biobanks, sample
collections, and (research) studies. This version has already been implemented as a FHIR profile.

MIABIS on FHIR is designed to provide a FHIR implementation for MIABIS Core 3.0, its latest version, as well as MIABIS
individual-level components, which describe information about samples and their donors.

The foundation for this FHIR profile (all the attributes defined by MIABIS) is available on MIABIS github.

The MIABIS on FHIR profile full specification along with the guide is available on the [simplifier platform](https://simplifier.net/miabis). 

This Python package provides a set of classes that can be used to create, read, and validate MIABIS on FHIR resources, as well as to convert them to and from JSON format.
This package aims to allow developers to easily work with MIABIS on FHIR resources in Python, while ensuring that the resources are compliant with the MIABIS on FHIR profile.

## Installation
```bash 
pip install MIABIS_on_FHIR
```
## How to use
Here is how you can create a MIABIS on FHIR sample resource:

```python
from MIABIS_on_FHIR.MoF_sample import Sample
from MIABIS_on_FHIR.storage_temperature import StorageTemperature

sample = Sample("sampleId", "donorId", "Blood", storage_temperature=StorageTemperature.TEMPERATURE_GN,
                use_restrictions="No restrictions")
# Convert the MoFSample object to a FHIR resource
sample_resource = sample.to_fhir("donorId")
# Convert the FHIR resource to a JSON string
sample_json = sample_resource.to_json()
```