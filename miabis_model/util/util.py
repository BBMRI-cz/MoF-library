from fhirclient.models.address import Address
from fhirclient.models.bundle import BundleEntry, BundleEntryRequest, Bundle
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.extension import Extension
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.organization import OrganizationContact


def create_codeable_concept_extension(extension_url: str, codeable_concept_url, value: str) -> Extension:
    extension = Extension()
    extension.url = extension_url
    extension.valueCodeableConcept = create_codeable_concept(codeable_concept_url, value)
    return extension


def create_codeable_concept(url: str, code: str) -> CodeableConcept:
    codeable_concept = CodeableConcept()
    codeable_concept.coding = [Coding()]
    codeable_concept.coding[0].system = url
    codeable_concept.coding[0].code = code
    return codeable_concept


def create_integer_extension(extension_url: str, value: int) -> Extension:
    extension = Extension()
    extension.url = extension_url
    extension.valueInteger = value
    return extension


def create_string_extension(extension_url: str, value: str) -> Extension:
    extension = Extension()
    extension.url = extension_url
    extension.valueString = value
    return extension


def create_fhir_identifier(identifier: str) -> Identifier:
    """Create fhir identifier."""
    fhir_identifier = Identifier()
    fhir_identifier.value = identifier
    return fhir_identifier


def create_contact(name: str, surname: str, email: str) -> OrganizationContact:
    contact = OrganizationContact()

    contact.name = HumanName()
    if name is not None:
        contact.name.given = [name]
    contact.name.family = surname
    contact.telecom = [ContactPoint()]
    contact.telecom[0].system = "email"
    contact.telecom[0].value = email
    return contact


def create_country_of_residence(country: str) -> Address:
    address = Address()
    address.country = country
    return address


def create_post_bundle_entry(resource_type: str, resource, temporary_id: str) -> BundleEntry:
    entry = BundleEntry()
    entry.request = BundleEntryRequest()
    entry.fullUrl = temporary_id
    entry.resource = resource
    entry.request.method = "POST"
    entry.request.url = f"/{resource_type}"
    return entry


def create_bundle(entries: list[BundleEntry]) -> Bundle:
    """Create a bundle used for deleting multiple FHIR resources in a transaction"""
    bundle = Bundle()
    bundle.type = "transaction"
    bundle.entry = entries
    return bundle
