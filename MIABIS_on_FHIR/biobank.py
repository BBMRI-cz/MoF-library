from typing import Self

from fhirclient.models.meta import Meta
from fhirclient.models.organization import Organization

from MIABIS_on_FHIR._constants import BIOBANK_BIOPROCESSING_AND_ANALYTICAL_CAPABILITIES, \
    BIOBANK_INFRASTRUCTURAL_CAPABILITIES, \
    BIOBANK_ORGANISATIONAL_CAPABILITIES, DEFINITION_BASE_URL
from MIABIS_on_FHIR._parsing_util import get_nested_value, parse_contact
from MIABIS_on_FHIR._util import create_fhir_identifier, create_contact, create_country_of_residence, \
    create_codeable_concept_extension, create_string_extension
from MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException


class Biobank:
    """Class representing a biobank as defined by the MIABIS on FHIR profile."""

    def __init__(self, identifier: str, name: str, alias: str, country: str, contact_name: str, contact_surname: str,
                 contact_email: str, infrastructural_capabilities: list[str] = None,
                 organisational_capabilities: list[str] = None,
                 bioprocessing_and_analysis_capabilities: list[str] = None,
                 quality__management_standards: list[str] = None, juristic_person: str = None):
        """
        :param identifier: Biobank identifier same format as in the BBMRI-ERIC directory.
        :param name: name of the biobank
        :param alias: acronym of the biobank
        :param country: country of residence of the biobank
        :param contact_name: name of the contact person
        :param contact_surname: surname of the contact person
        :param contact_email: email of the contact person
        :param infrastructural_capabilities: The technical infrastructural capabilities that
        the biobank can offer to the clients. Available values in the _constants.py file
        :param organisational_capabilities: The organisational capabilities and services that
        the biobank can provide to support clients. Available values in the _constants.py file
        :param bioprocessing_and_analysis_capabilities: The bioprocessing and analytical services
        that the biobank can offer to the clients. Available values in the _constants.py file
        :param quality__management_standards: The standards that the biobank is certified or accredited for.
        :param juristic_person: The legal entity that is responsible for the biobank.
        Available values in the _constants.py file
        """
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be a string.")
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(alias, str):
            raise TypeError("Alias must be a string.")
        if not isinstance(country, str):
            raise TypeError("Country must be a string.")
        if not isinstance(contact_name, str):
            raise TypeError("Contact name must be a string.")
        if not isinstance(contact_surname, str):
            raise TypeError("Contact surname must be a string.")
        if not isinstance(contact_email, str):
            raise TypeError("Contact email must be a string.")
        self._identifier = identifier
        self._name = name
        self._alias = alias
        self._country = country
        self._contact_name = contact_name
        self._contact_surname = contact_surname
        self._contact_email = contact_email
        self._juristic_person = juristic_person
        self._quality__management_standards = quality__management_standards
        if infrastructural_capabilities is not None:
            for capability in infrastructural_capabilities:
                if capability not in BIOBANK_INFRASTRUCTURAL_CAPABILITIES:
                    raise ValueError(f"{capability} is not a valid code for infrastructural capabilities")
        self._infrastructural_capabilities = infrastructural_capabilities
        if organisational_capabilities is not None:
            for capability in organisational_capabilities:
                if capability not in BIOBANK_ORGANISATIONAL_CAPABILITIES:
                    raise ValueError(f"{capability} is not a valid code for organisational capabilities")
        self._organisational_capabilities = organisational_capabilities
        if bioprocessing_and_analysis_capabilities is not None:
            for capability in bioprocessing_and_analysis_capabilities:
                if capability not in BIOBANK_BIOPROCESSING_AND_ANALYTICAL_CAPABILITIES:
                    raise ValueError(f"{capability} is not a valid code for bioprocessing and analysis capabilities")
        self._bioprocessing_and_analysis_capabilities = bioprocessing_and_analysis_capabilities
        if quality__management_standards is not None:
            self._quality__management_standards = quality__management_standards
        if juristic_person is not None:
            if not isinstance(juristic_person, str):
                raise TypeError("Juristic person must be a string.")
            self._juristic_person = juristic_person

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be a string.")
        self._identifier = identifier

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        self._name = name

    @property
    def alias(self) -> str:
        return self._alias

    @alias.setter
    def alias(self, alias: str):
        if not isinstance(alias, str):
            raise TypeError("Alias must be a string.")
        self._alias = alias

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, country: str):
        if not isinstance(country, str):
            raise TypeError("Country must be a string.")
        self._country = country

    @property
    def contact_name(self) -> str:
        return self._contact_name

    @contact_name.setter
    def contact_name(self, contact_name: str):
        if not isinstance(contact_name, str):
            raise TypeError("Contact name must be a string.")
        self._contact_name = contact_name

    @property
    def contact_surname(self) -> str:
        return self._contact_surname

    @contact_surname.setter
    def contact_surname(self, contact_surname: str):
        if not isinstance(contact_surname, str):
            raise TypeError("Contact surname must be a string.")
        self._contact_surname = contact_surname

    @property
    def contact_email(self) -> str:
        return self._contact_email

    @contact_email.setter
    def contact_email(self, contact_email: str):
        if not isinstance(contact_email, str):
            raise TypeError("Contact email must be a string.")
        self._contact_email = contact_email

    @property
    def infrastructural_capabilities(self) -> list[str]:
        return self._infrastructural_capabilities

    @infrastructural_capabilities.setter
    def infrastructural_capabilities(self, infrastructural_capabilities: list[str]):
        for capability in infrastructural_capabilities:
            if capability not in BIOBANK_INFRASTRUCTURAL_CAPABILITIES:
                raise ValueError(f"{capability} is not a valid code for infrastructural capabilities")
        self._infrastructural_capabilities = infrastructural_capabilities

    @property
    def organisational_capabilities(self) -> list[str]:
        return self._organisational_capabilities

    @organisational_capabilities.setter
    def organisational_capabilities(self, organisational_capabilities: list[str]):
        for capability in organisational_capabilities:
            if capability not in BIOBANK_ORGANISATIONAL_CAPABILITIES:
                raise ValueError(f"{capability} is not a valid code for organisational capabilities")
        self._organisational_capabilities = organisational_capabilities

    @property
    def bioprocessing_and_analysis_capabilities(self) -> list[str]:
        return self._bioprocessing_and_analysis_capabilities

    @bioprocessing_and_analysis_capabilities.setter
    def bioprocessing_and_analysis_capabilities(self, bioprocessing_and_analysis_capabilities: list[str]):
        for capability in bioprocessing_and_analysis_capabilities:
            if capability not in BIOBANK_BIOPROCESSING_AND_ANALYTICAL_CAPABILITIES:
                raise ValueError(f"{capability} is not a valid code for bioprocessing and analysis capabilities")
        self._bioprocessing_and_analysis_capabilities = bioprocessing_and_analysis_capabilities

    @property
    def quality__management_standards(self) -> list[str]:
        return self._quality__management_standards

    @quality__management_standards.setter
    def quality__management_standards(self, quality__management_standards: list[str]):
        self._quality__management_standards = quality__management_standards

    @property
    def juristic_person(self) -> str:
        return self._juristic_person

    @juristic_person.setter
    def juristic_person(self, juristic_person: str):
        if not isinstance(juristic_person, str):
            raise TypeError("Juristic person must be a string.")
        self._juristic_person = juristic_person

    @classmethod
    def from_json(cls, biobank_json: dict) -> Self:
        """
        Parse a json into a MoFBiobank object.
        :param biobank_json: json representation of the biobank.
        :return: MoFBiobank object.
        """
        try:
            identifier = get_nested_value(biobank_json, ["identifier", 0, "value"])
            name = get_nested_value(biobank_json, ["name"])
            alias = get_nested_value(biobank_json, ["alias", 0])
            country = get_nested_value(biobank_json, ["address", 0, "country"])
            contact = parse_contact(biobank_json.get("contact", [{}])[0])
            extensions = get_nested_value(biobank_json, ["extension"])
            parsed_extension = cls.__parse_extensions(extensions)
            infrastructural_capabilities = parsed_extension["infrastructural_capabilities"]
            organisational_capabilities = parsed_extension["organisational_capabilities"]
            bioprocessing = parsed_extension["bioprocessing_and_analysis_capabilities"]
            quality_standards = parsed_extension["quality_management_standards"]
            juristic_person = parsed_extension["juristic_person"]

            return cls(identifier, name, alias, country, contact["name"], contact["surname"], contact["email"],
                       infrastructural_capabilities, organisational_capabilities, bioprocessing, quality_standards,
                       juristic_person)
        except KeyError:
            raise IncorrectJsonFormatException("Error occurred when parsing json into MoFBiobank")

    @staticmethod
    def __parse_extensions(extensions: list) -> dict:

        """
        Parse the extensions from the json into a dictionary.
        :param extensions: list of extensions in the json.
        :return: dictionary with the extensions.
        """

        parsed_extension = {"infrastructural_capabilities": [], "organisational_capabilities": [],
                            "bioprocessing_and_analysis_capabilities": [], "quality_management_standards": [],
                            "juristic_person": None}

        for extension in extensions:
            ext_type = extension["url"].replace(f"{DEFINITION_BASE_URL}/", "", 1)
            match ext_type:
                case "infrastructural-capabilities":
                    value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                    if value is not None:
                        parsed_extension["infrastructural_capabilities"].append(value)
                case "organisational-capabilities":
                    value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                    if value is not None:
                        parsed_extension["organisational_capabilities"].append(value)
                case "bioprocessing-and-analysis-capabilities":
                    value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                    if value is not None:
                        parsed_extension["bioprocessing_and_analysis_capabilities"].append(value)
                case "quality-management-standards":
                    value = get_nested_value(extension, ["valueString"])
                    if value is not None:
                        parsed_extension["quality_management_standards"].append(extension["valueString"])
                case "juristic-person":
                    value = get_nested_value(extension, ["valueString"])
                    if value is not None:
                        parsed_extension["juristic_person"] = extension["valueString"]
                case _:
                    pass
        return parsed_extension


    def to_fhir(self) -> Organization:
        """Return biobank representation in FHIR"""
        fhir_organization = Organization()
        fhir_organization.meta = Meta()
        fhir_organization.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Biobank"]
        fhir_organization.identifier = [create_fhir_identifier(self.identifier)]
        fhir_organization.name = self.name
        fhir_organization.alias = [self.alias]
        fhir_organization.contact = [create_contact(self.contact_name, self.contact_surname, self.contact_email)]
        fhir_organization.address = [create_country_of_residence(self.country)]
        extensions = []
        if self.infrastructural_capabilities is not None:
            for capability in self.infrastructural_capabilities:
                extensions.append(
                    create_codeable_concept_extension(DEFINITION_BASE_URL + "/infrastructural-capabilities",
                                                      DEFINITION_BASE_URL + "/infrastructural-capabilities-vs",
                                                      capability))
        if self.organisational_capabilities is not None:
            for capability in self.organisational_capabilities:
                extensions.append(
                    create_codeable_concept_extension(DEFINITION_BASE_URL + "/organisational-capabilities",
                                                      DEFINITION_BASE_URL + "/organisational-capabilities-vs",
                                                      capability))
        if self.bioprocessing_and_analysis_capabilities is not None:
            for capability in self.bioprocessing_and_analysis_capabilities:
                extensions.append(
                    create_codeable_concept_extension(
                        DEFINITION_BASE_URL + "/bioprocessing-and-analysis-capabilities",
                        DEFINITION_BASE_URL + "/bioprocessing-and-analysis-capabilities-vs", capability))
        if self.quality__management_standards is not None:
            for standard in self.quality__management_standards:
                extensions.append(
                    create_string_extension(DEFINITION_BASE_URL + "/quality-management-standards", standard))
        if self.juristic_person is not None:
            extensions.append(
                create_string_extension(DEFINITION_BASE_URL + "/juristic-person", self.juristic_person))
        if extensions:
            fhir_organization.extension = extensions
        return fhir_organization
