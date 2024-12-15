## Introduction

MIABIS is focused on standardizing the data elements used to describe biobanks, research on samples, and related data.
The goal of MIABIS is to enhance interoperability among biobanks that share valuable data and samples. MIABIS Core 2.0,
introduced in 2016, established general attributes at an aggregated/metadata level for describing biobanks, sample
collections, and (research) studies. This version has already been implemented as a FHIR profile.

MIABIS on FHIR is designed to provide a FHIR implementation for MIABIS Core 3.0, its latest version, as well as MIABIS
individual-level components, which describe information about samples and their donors.

The foundation for this FHIR profile (all the attributes defined by MIABIS) is available on MIABIS github.

The MIABIS on FHIR profile full specification along with the guide is available on the [simplifier platform](https://simplifier.net/miabis). 

## Modules

### 1. `miabis_model`
The `miabis_model` module includes a set of classes to help developers:
- **Create** MIABIS on FHIR resources.
- **Read** and **validate** these resources.
- **Convert** resources to and from JSON format.

This module ensures compliance with the MIABIS on FHIR profile, allowing developers to handle MIABIS resources confidently and efficiently in Python.

### 2. `blaze_client`
The `blaze_client` module simplifies communication with the [Samply.blaze](https://github.com/samply/blaze) FHIR storage server. Samply.blaze is a FHIR-compliant database designed for managing and storing FHIR resources. This module provides:
- **Streamlined communication** with Samply.blaze, abstracting away the need for direct JSON response handling.
- **BlazeClient** methods that simplify operations with the server, focusing on ease of use and minimizing boilerplate code.

## Key Features
- **Compliance**: Ensures MIABIS on FHIR resources meet the profile standards.
- **Ease of Use**: Abstracts complex JSON interactions for a streamlined experience.
- **Blaze Integration**: Seamless integration with Samply.blaze for FHIR resource management.

This package is ideal for developers looking to work with MIABIS on FHIR resources and interact with FHIR storage servers using Python.


## Installation
```bash 
pip install MIABIS-on-FHIR
```
## How to use
Here is how you can create a MIABIS on FHIR sample resource:

```python
from miabis_model import Sample
from miabis_model import StorageTemperature

sample = Sample("sampleId", "donorId", "Urine", storage_temperature=StorageTemperature.TEMPERATURE_ROOM,
                use_restrictions="No restrictions")
# Convert the Sample object to a FHIR resource
sample_resource = sample.to_fhir("donorId")
# Convert the FHIR resource to a JSON string
sample_json = sample_resource.as_json()
```

Here is an example on how to communicate with blaze server via the BlazeClient:

```python
import datetime
from miabis_model import Gender
from blaze_client import BlazeClient
from miabis_model import SampleDonor

client = BlazeClient("example_url", "username", "password")

donor = SampleDonor("donorId", Gender.MALE, birth_date=datetime.datetime(year=2000, month=12, day=12))
donor_fhir_id = client.upload_donor(donor)
```
