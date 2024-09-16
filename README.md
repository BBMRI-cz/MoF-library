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

## How to use