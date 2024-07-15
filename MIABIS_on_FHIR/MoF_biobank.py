from fhirclient.models.address import Address
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.extension import Extension
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.organization import Organization, OrganizationContact

from _constants import INFRASTRUCTURAL_CAPABILITIES, ORGANISATIONAL_CAPABILITIES, \
    BIOPROCESSING_AND_ANALYTICAL_CAPABILITIES


class MoFBiobank():
    def __init__(self, identifier: str, name: str, alias: str, country: str, contact_name: str, contact_surname: str,
                 contact_email: str, infrastructural_capabilities: list[str] = None,
                 organisational_capabilities: list[str] = None,
                 bioprocessing_and_analysis_capabilities: list[str] = None,
                 quality__management_standards: list[str] = None):
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
        Available values in the _constants.py file
        """
        self._identifier = identifier
        self._name = name
        self._alias = alias
        self._country = country
        self._contact_name = contact_name
        self._contact_surname = contact_surname
        self._contact_email = contact_email
        if infrastructural_capabilities is not None:
            for capability in infrastructural_capabilities:
                if capability not in INFRASTRUCTURAL_CAPABILITIES:
                    raise ValueError(f"{capability} is not a valid code for infrastructural capabilities")
            self._infrastructural_capabilities = infrastructural_capabilities
        if organisational_capabilities is not None:
            for capability in organisational_capabilities:
                if capability not in ORGANISATIONAL_CAPABILITIES:
                    raise ValueError(f"{capability} is not a valid code for organisational capabilities")
            self._organisational_capabilities = organisational_capabilities
        if bioprocessing_and_analysis_capabilities is not None:
            for capability in bioprocessing_and_analysis_capabilities:
                if capability not in BIOPROCESSING_AND_ANALYTICAL_CAPABILITIES:
                    raise ValueError(f"{capability} is not a valid code for bioprocessing and analysis capabilities")
            self._bioprocessing_and_analysis_capabilities = bioprocessing_and_analysis_capabilities
        self._quality__management_standards = quality__management_standards

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        self._identifier = identifier

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def alias(self) -> str:
        return self._alias

    @alias.setter
    def alias(self, alias: str):
        self._alias = alias

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, country: str):
        self._country = country

    @property
    def contact_name(self) -> str:
        return self._contact_name

    @contact_name.setter
    def contact_name(self, contact_name: str):
        self._contact_name = contact_name

    @property
    def contact_surname(self) -> str:
        return self._contact_surname

    @contact_surname.setter
    def contact_surname(self, contact_surname: str):
        self._contact_surname = contact_surname

    @property
    def contact_email(self) -> str:
        return self._contact_email

    @contact_email.setter
    def contact_email(self, contact_email: str):
        self._contact_email = contact_email

    @property
    def infrastructural_capabilities(self) -> list[str]:
        return self._infrastructural_capabilities

    @infrastructural_capabilities.setter
    def infrastructural_capabilities(self, infrastructural_capabilities: list[str]):
        self._infrastructural_capabilities = infrastructural_capabilities

    @property
    def organisational_capabilities(self) -> list[str]:
        return self._organisational_capabilities

    @organisational_capabilities.setter
    def organisational_capabilities(self, organisational_capabilities: list[str]):
        self._organisational_capabilities = organisational_capabilities

    @property
    def bioprocessing_and_analysis_capabilities(self) -> list[str]:
        return self._bioprocessing_and_analysis_capabilities

    @bioprocessing_and_analysis_capabilities.setter
    def bioprocessing_and_analysis_capabilities(self, bioprocessing_and_analysis_capabilities: list[str]):
        self._bioprocessing_and_analysis_capabilities = bioprocessing_and_analysis_capabilities

    @property
    def quality__management_standards(self) -> list[str]:
        return self._quality__management_standards

    @quality__management_standards.setter
    def quality__management_standards(self, quality__management_standards: list[str]):
        self._quality__management_standards = quality__management_standards

    def to_fhir(self):
        """Return biobank representation in FHIR"""
        fhir_organization = Organization()
        fhir_organization.identifier = [self.__create_fhir_identifier()]
        fhir_organization.name = self.name
        fhir_organization.alias = [self.alias]
        fhir_organization.contact = [self.__create_contact()]
        fhir_organization.address = [self.__create_country_of_residence()]
        extensions = []
        if self.infrastructural_capabilities is not None:
            for capability in self.infrastructural_capabilities:
                extensions.append(self._create_extension("http://example.com/infrastructural-capabilities", capability))
        if self.organisational_capabilities is not None:
            for capability in self.organisational_capabilities:
                extensions.append(self._create_extension("http://example.com/organisational-capabilities", capability))
        if self.bioprocessing_and_analysis_capabilities is not None:
            for capability in self.bioprocessing_and_analysis_capabilities:
                extensions.append(
                    self._create_extension("http://example.com/bioprocessing-and-analysis-capabilities", capability))
        if self.quality__management_standards is not None:
            for standard in self.quality__management_standards:
                extensions.append(self._create_extension("http://example.com/quality-management-standards", standard))
        if extensions:
            fhir_organization.extension = extensions
        return fhir_organization

    def _create_extension(self, url: str, value: str) -> Extension:
        extension = Extension()
        extension.url = url
        extension.valueString = value
        return extension

    def __create_fhir_identifier(self) -> Identifier:
        """Create fhir identifier."""
        fhir_identifier = Identifier()
        fhir_identifier.value = self._identifier
        return fhir_identifier

    def __create_contact(self) -> OrganizationContact:
        contact = OrganizationContact()
        contact.name = HumanName()
        contact.name.given = [self.contact_name]
        contact.name.family = self.contact_surname
        contact.telecom = [ContactPoint()]
        contact.telecom[0].system = "email"
        contact.telecom[0].value = self.contact_email
        return contact

    def __create_country_of_residence(self) -> Address:
        address = Address()
        address.country = self.country
        return address
