from typing import Self

from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta
from fhirclient.models.organization import Organization

from miabis_model.incorrect_json_format import IncorrectJsonFormatException
from miabis_model.juristic_person import _JuristicPerson
from miabis_model.util.config import FHIRConfig
from miabis_model.util.constants import NETWORK_COMMON_COLLAB_TOPICS
from miabis_model.util.parsing_util import get_nested_value, parse_contact, parse_reference_id
from miabis_model.util.util import create_fhir_identifier, create_contact, create_country_of_residence, \
    create_codeable_concept_extension, create_string_extension


class _NetworkOrganization:
    """Network Organization represent a formal part of a network member,
     like ist name, contact information, url, etc."""

    def __init__(self, identifier: str, name: str, contact_email: str, country: str,
                 juristic_person: str, url: str = None, contact_name: str = None, contact_surname: str = None,
                 common_collaboration_topics: list[str] = None, description: str = None):
        """
        :param identifier: network organizational identifier
        :param name: name of the network
        :param managing_biobank_id: biobank which is managing this Network
        ( for the purposes of having a contact person for this network)
        :param common_collaboration_topics: Topics that the network partners collaborate on.
        :param juristic_person: The legal entity that is responsible for the network.
        """
        self.identifier = identifier
        self.name = name
        self.contact_name = contact_name
        self.contact_surname = contact_surname
        self.contact_email = contact_email
        self.country = country
        self.url = url
        self.juristic_person = _JuristicPerson(juristic_person)
        self.common_collaboration_topics = common_collaboration_topics
        self.description = description
        self._network_org_fhir_id = None

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be string")
        self._identifier = identifier

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        self._name = name

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        if url is not None and not isinstance(url, str):
            raise TypeError("url must be a string")
        self._url = url

    @property
    def contact_name(self) -> str:
        return self._contact_name

    @contact_name.setter
    def contact_name(self, contact_name: str):
        if contact_name is not None and not isinstance(contact_name, str):
            raise TypeError("Contact name must be string")
        self._contact_name = contact_name

    @property
    def contact_surname(self) -> str:
        return self._contact_surname

    @contact_surname.setter
    def contact_surname(self, contact_surname: str):
        if contact_surname is not None and not isinstance(contact_surname, str):
            raise TypeError("Contact surname must be string")
        self._contact_surname = contact_surname

    @property
    def contact_email(self) -> str:
        return self._contact_email

    @contact_email.setter
    def contact_email(self, contact_email: str):
        if contact_email is not None and not isinstance(contact_email, str):
            raise TypeError("Contact email must be string")
        self._contact_email = contact_email

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, country: str):
        if country is not None and not isinstance(country, str):
            raise TypeError("Country must be string")
        self._country = country

    @property
    def managing_biobank_id(self) -> str:
        return self._managing_biobank_id

    @managing_biobank_id.setter
    def managing_biobank_id(self, managing_biobank_id: str):
        if managing_biobank_id is not None and not isinstance(managing_biobank_id, str):
            raise TypeError("Managing biobank id must be string")
        self._managing_biobank_id = managing_biobank_id

    @property
    def common_collaboration_topics(self) -> list[str]:
        return self._common_collaboration_topics

    @common_collaboration_topics.setter
    def common_collaboration_topics(self, common_collaboration_topics: list[str]):
        if common_collaboration_topics is not None and not isinstance(common_collaboration_topics, list):
            raise TypeError("Common collaboration topics must be a list")
        for topic in common_collaboration_topics if common_collaboration_topics is not None else []:
            if topic not in NETWORK_COMMON_COLLAB_TOPICS:
                raise ValueError(f"{topic} is not a valid code for common collaboration")
        self._common_collaboration_topics = common_collaboration_topics

    @property
    def network_org_fhir_id(self) -> str:
        return self._network_org_fhir_id

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        if description is not None and not isinstance(description, str):
            raise TypeError("Description must be string")
        self._description = description

    @classmethod
    def from_json(cls, network_json: dict, juristic_person_json: dict) -> Self:
        try:
            network_org_fhir_id = get_nested_value(network_json, ["id"])
            identifier = get_nested_value(network_json, ["identifier", 0, "value"])
            name = get_nested_value(network_json, ["name"])
            managing_biobank_fhir_id = parse_reference_id(get_nested_value(network_json, ["partOf", "reference"]))
            contact = parse_contact(network_json.get("contact", [{}])[0])
            url = get_nested_value(network_json, ["telecom", 0, "value"])
            country = get_nested_value(network_json, ["address", 0, "country"])
            parsed_extensions = cls._parse_extensions(network_json.get("extension", []))
            juristic_person_fhir_id = get_nested_value(juristic_person_json, ["id"])
            juristic_person_name = get_nested_value(juristic_person_json, ["name"])
            instance = cls(identifier=identifier, name=name,
                           contact_name=contact["name"],
                           contact_surname=contact["surname"], contact_email=contact["email"], country=country,
                           common_collaboration_topics=parsed_extensions["common_collaboration_topics"],
                           juristic_person=juristic_person_name,
                           description=parsed_extensions["description"],
                           url=url)
            instance._network_org_fhir_id = network_org_fhir_id
            instance._managing_biobank_fhir_id = managing_biobank_fhir_id
            instance.juristic_person._fhir_id = juristic_person_fhir_id
            return instance
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into the MoFNetwork")

    @staticmethod
    def _parse_extensions(extensions: dict) -> dict:
        parsed_extension = {"common_collaboration_topics": [], "juristic_person": None, "description": None}
        common_coll_topic_extension: str = FHIRConfig.get_extension_url("network_organization",
                                                                        "common_collaboration_topics")
        description_extension: str = FHIRConfig.get_extension_url("network_organization", "description")
        for extension in extensions:
            extension_url = extension["url"]
            if extension_url == common_coll_topic_extension:
                value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                if value is not None:
                    parsed_extension["common_collaboration_topics"].append(value)
            elif extension_url == description_extension:
                value = get_nested_value(extension, ["valueString"])
                parsed_extension["description"] = value
            else:
                continue
        if not parsed_extension["common_collaboration_topics"]:
            parsed_extension["common_collaboration_topics"] = None
        return parsed_extension

    def to_fhir(self, juristic_person_fhir_id: str = None) -> Organization:
        juristic_person_fhir_id = juristic_person_fhir_id or self.juristic_person.fhir_id
        if juristic_person_fhir_id is None:
            raise ValueError("Juristic Person FHIR ID must be provided either as an argument or as an property.")
        network = Organization()
        network.meta = Meta()
        network.meta.profile = [FHIRConfig.get_meta_profile_url("network_organization")]
        network.identifier = [create_fhir_identifier(self.identifier)]
        network.name = self._name
        network.active = True
        network.partOf = FHIRReference()
        network.partOf.reference = f"Organization/{juristic_person_fhir_id}"
        network.contact = [create_contact(self._contact_name, self._contact_surname, self._contact_email)]
        network.address = [create_country_of_residence(self._country)]
        if self.url is not None:
            network.telecom = [self.create_url(self.url)]
        extensions = []
        if self._common_collaboration_topics is not None:
            for topic in self._common_collaboration_topics:
                extensions.append(
                    create_codeable_concept_extension(
                        FHIRConfig.get_extension_url("network_organization", "common_collaboration_topics"),
                        FHIRConfig.get_code_system_url("network_organization", "common_collaboration_topics"), topic))
        if self._description is not None:
            extensions.append(
                create_string_extension(FHIRConfig.get_extension_url("network_organization", "description"),
                                        self._description))
        network.extension = extensions
        return network

    @staticmethod
    def create_url(url: str) -> ContactPoint:
        contact_point = ContactPoint()
        contact_point.system = "url"
        contact_point.value = url
        return contact_point

    def add_fhir_id_to_network(self, network: Organization) -> Organization:
        """Add FHIR id to the FHIR representation of the NetworkOrganization. FHIR ID is necessary for updating the
                resource on the server.This method should only be called if the NetworkOrganization object was created by the
                from_json method. Otherwise,the network_org_fhir_id attribute is None,
                as the FHIR ID is generated by the server and is not known in advance."""
        network.id = self._network_org_fhir_id
        return network

    def __eq__(self, other):
        if not isinstance(other, _NetworkOrganization):
            return False
        return self.identifier == other.identifier and \
            self.name == other.name and \
            self.contact_name == other.contact_name and \
            self.contact_surname == other.contact_surname and \
            self.contact_email == other.contact_email and \
            self.country == other.country and \
            self.juristic_person.name == other.juristic_person.name and \
            self.common_collaboration_topics == other.common_collaboration_topics and \
            self.description == other.description
