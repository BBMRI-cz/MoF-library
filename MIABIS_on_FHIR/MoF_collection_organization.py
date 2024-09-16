"""Module for handling SampleCollection operations"""
from typing import Self

from fhirclient.models.address import Address
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.extension import Extension
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.meta import Meta
from fhirclient.models.organization import Organization, OrganizationContact

from MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException
from MIABIS_on_FHIR._constants import COLLECTION_DESIGN, COLLECTION_SAMPLE_COLLECTION_SETTING, COLLECTION_SAMPLE_SOURCE, \
    COLLECTION_DATASET_TYPE, COLLECTION_USE_AND_ACCESS_CONDITIONS, DEFINITION_BASE_URL


class MoFCollectionOrganization:
    """Sample Collection represents a set of samples with at least one common characteristic."""

    # TODO age range units
    def __init__(self, identifier: str, name: str, managing_biobank_id: str,
                 contact_name: str, contact_surname: str,
                 contact_email: str,
                 country: str,
                 alias: str = None,
                 url: str = None,
                 description: str = None,
                 dataset_type: str = None,
                 sample_source: str = None,
                 sample_collection_setting: str = None, collection_design: list[str] = None,
                 use_and_access_conditions: list[str] = None,
                 publications: list[str] = None):
        """
        :param identifier: Collection identifier same format as in the BBMRI-ERIC directory.
        :param name: Name of the collection.
        :param managing_biobank_id: Identifier of the biobank managing the collection.
        :param contact_name: Name of the contact person for the collection.
        :param contact_surname: Surname of the contact person for the collection.
        :param contact_email: Email of the contact person for the collection.
        :param alias: Alias of the collection.
        :param url: URL of the collection.
        :param description: Description of the collection.
        :param dataset_type: Type of the dataset. Available values in the _constants.py file
        :param sample_source: Source of the samples. Available values in the _constants.py file
        :param sample_collection_setting: Setting of the sample collection. Available values in the _constants.py file
        :param collection_design: Design of the collection. Available values in the _constants.py file
        :param use_and_access_conditions: Conditions for use and access of the collection.
         Available values in the _constants.py file
        :param publications: Publications related to the collection.
        """
        if not isinstance(identifier, str):
            raise TypeError("Collection identifier must be a string.")
        if not isinstance(name, str):
            raise TypeError("Collection name must be a string.")
        if description is not None and not isinstance(description, str):
            raise TypeError("Collection description must be a string.")
        if not isinstance(managing_biobank_id, str):
            raise TypeError("Managing biobank identifier must be a string.")
        if not isinstance(contact_name, str):
            raise TypeError("Contact name must be a string.")
        if not isinstance(contact_surname, str):
            raise TypeError("Contact surname must be a string.")
        if not isinstance(contact_email, str):
            raise TypeError("Contact email must be a string.")
        if not isinstance(country, str):
            raise TypeError("Country must be a string.")
        if alias is not None and not isinstance(alias, str):
            raise TypeError("Collection alias must be a string.")
        if url is not None and not isinstance(url, str):
            raise TypeError("Collection URL must be a string.")
        if publications is not None:
            if not isinstance(publications, list):
                raise TypeError("Publications must be a list.")
            for publication in publications:
                if not isinstance(publication, str):
                    raise TypeError("Publications must be a list of strings.")

        self._identifier: str = identifier
        self._name: str = name
        self._description: str = description
        self._managing_biobank_id: str = managing_biobank_id
        self._contact_name: str = contact_name
        self._contact_surname: str = contact_surname
        self._contact_email: str = contact_email
        self._country = country
        self._alias: str = alias
        self._url: str = url

        if dataset_type is not None and dataset_type not in COLLECTION_DATASET_TYPE:
            raise ValueError(f"{dataset_type} is not a valid code for dataset type")
        self._dataset_type = dataset_type

        if sample_source is not None and sample_source not in COLLECTION_SAMPLE_SOURCE:
            raise ValueError(f"{sample_source} is not a valid code for sample source")
        self._sample_source = sample_source

        if sample_collection_setting is not None and sample_collection_setting \
                not in COLLECTION_SAMPLE_COLLECTION_SETTING:
            raise ValueError(f"{sample_collection_setting} is not a valid code for sample collection setting")
        self._sample_collection_setting = sample_collection_setting

        if collection_design is not None:
            if not isinstance(collection_design, list):
                raise TypeError("Collection design must be a list")
            for design in collection_design:
                if design not in COLLECTION_DESIGN:
                    raise ValueError(f"{design} is not a valid code for collection design")
        self._collection_design = collection_design

        if use_and_access_conditions is not None:
            if not isinstance(use_and_access_conditions, list):
                raise TypeError("Use and access conditions must be a list.")
            for condition in use_and_access_conditions:
                if condition not in COLLECTION_USE_AND_ACCESS_CONDITIONS:
                    raise ValueError(f"{condition} is not a valid code for use and access conditions")
        self._use_and_access_conditions = use_and_access_conditions
        self._publications = publications

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        if not isinstance(identifier, str):
            raise TypeError("Collection identifier must be a string.")
        self._identifier = identifier

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Collection name must be a string.")
        self._name = name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        if description is not None and not isinstance(description, str):
            raise TypeError("Collection description must be a string.")
        self._description = description

    @property
    def managing_biobank_id(self) -> str:
        return self._managing_biobank_id

    @managing_biobank_id.setter
    def managing_biobank_id(self, managing_biobank_id: str):
        if not isinstance(managing_biobank_id, str):
            raise TypeError("Managing biobank identifier must be a string.")
        self._managing_biobank_id = managing_biobank_id

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
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, country: str):
        if not isinstance(country, str):
            raise TypeError("Country must be a string.")
        self._country = country

    @property
    def alias(self) -> str:
        return self._alias

    @alias.setter
    def alias(self, alias: str):
        if alias is not None and not isinstance(alias, str):
            raise TypeError("Collection alias must be a string.")
        self._alias = alias

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        if url is not None and not isinstance(url, str):
            raise TypeError("Collection URL must be a string.")
        self._url = url

    @property
    def dataset_type(self) -> str:
        return self._dataset_type

    @dataset_type.setter
    def dataset_type(self, dataset_type: str):
        if dataset_type is not None and dataset_type not in COLLECTION_DATASET_TYPE:
            raise ValueError(f"{dataset_type} is not a valid code for dataset type")
        self._dataset_type = dataset_type

    @property
    def sample_source(self) -> str:
        return self._sample_source

    @sample_source.setter
    def sample_source(self, sample_source: str):
        if sample_source is not None and sample_source not in COLLECTION_SAMPLE_SOURCE:
            raise ValueError(f"{sample_source} is not a valid code for sample source")
        self._sample_source = sample_source

    @property
    def sample_collection_setting(self) -> str:
        return self._sample_collection_setting

    @sample_collection_setting.setter
    def sample_collection_setting(self, sample_collection_setting: str):
        if sample_collection_setting is not None and \
                sample_collection_setting not in COLLECTION_SAMPLE_COLLECTION_SETTING:
            raise ValueError(f"{sample_collection_setting} is not a valid code for sample collection setting")
        self._sample_collection_setting = sample_collection_setting

    @property
    def collection_design(self) -> list[str]:
        return self._collection_design

    @collection_design.setter
    def collection_design(self, collection_design: list[str]):
        if collection_design is not None:
            for design in collection_design:
                if design not in COLLECTION_DESIGN:
                    raise ValueError(f"{design} is not a valid code for collection design")
        self._collection_design = collection_design

    @property
    def use_and_access_conditions(self) -> list[str]:
        return self._use_and_access_conditions

    @use_and_access_conditions.setter
    def use_and_access_conditions(self, use_and_access_conditions: list[str]):
        if use_and_access_conditions is not None:
            for condition in use_and_access_conditions:
                if condition not in COLLECTION_USE_AND_ACCESS_CONDITIONS:
                    raise ValueError(f"{condition} is not a valid code for use and access conditions")
        self._use_and_access_conditions = use_and_access_conditions

    @property
    def publications(self) -> list[str]:
        return self._publications

    @publications.setter
    def publications(self, publications: list[str]):
        if publications is not None:
            if not isinstance(publications, list):
                raise TypeError("Publications must be a list.")
            for publication in publications:
                if not isinstance(publication, str):
                    raise TypeError("Publications must be a list of strings.")
        self._publications = publications

    @classmethod
    def from_json(cls, collection_json: dict, managing_biobank_id) -> Self:
        """
        Parse a JSON object into a MoFCollection object.
        :param collection_json: json object representing the collection.
        :param managing_biobank_id: id of managing biobank usually given by the institution (not a FHIR id!)
        :return: MoFCollection object
        """
        try:
            identifier = collection_json["identifier"][0]["value"]
            name = collection_json["name"]
            url = None
            contact_name = None
            contact_surname = None
            contact_email = None
            country = None
            dataset_type = None
            sample_source = None
            sample_collection_setting = None
            collection_design = None
            use_and_access_conditions = None
            publications = None
            description = None
            alias = collection_json.get("alias")[0]
            if collection_json.get("telecom") is not None:
                url = collection_json["telecom"][0]["value"]

            if collection_json.get("contact") is not None:
                contact_name = collection_json["contact"][0]["name"]["given"][0]
                contact_surname = collection_json["contact"][0]["name"]["family"]
                contact_email = collection_json["contact"][0]["telecom"][0]["value"]
                country = collection_json["contact"][0]["address"]["country"]
            extension = collection_json.get("extension", [])
            for ext in extension:
                match ext["url"].replace(f"{DEFINITION_BASE_URL}/StructureDefinition/", "", 1):
                    case "dataset-type-extension":
                        dataset_type = ext["valueCodeableConcept"]["coding"][0]["code"]
                    case "sample-source-extension":
                        sample_source = ext["valueCodeableConcept"]["coding"][0]["code"]
                    case "sample-collection-setting-extension":
                        sample_collection_setting = ext["valueCodeableConcept"]["coding"][0]["code"]
                    case "collection-design-extension":
                        if collection_design is None:
                            collection_design = []
                        collection_design.append(ext["valueCodeableConcept"]["coding"][0]["code"])
                    case "use-and-access-conditions-extension":
                        if use_and_access_conditions is None:
                            use_and_access_conditions = []
                        use_and_access_conditions.append(ext["valueCodeableConcept"]["coding"][0]["code"])
                    case "publication-extension":
                        if publications is None:
                            publications = []
                        publications.append(ext["valueString"])
                    case "description-extension":
                        description = ext["valueString"]
                    case _:
                        pass
            return cls(identifier, name, managing_biobank_id, contact_name, contact_surname, contact_email, country,
                       alias, url, description, dataset_type, sample_source, sample_collection_setting,
                       collection_design, use_and_access_conditions, publications)
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into MoFCollection")

    def to_fhir(self, managing_organization_fhir_id: str) -> Organization:
        """Return collection representation in FHIR
        :param managing_organization_fhir_id: FHIR Identifier of the managing organization"""
        fhir_org = Organization()
        fhir_org.meta = Meta()
        fhir_org.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Collection"]
        fhir_org.identifier = [self.__create_fhir_identifier()]
        fhir_org.type = [self.__create_codeable_concept(DEFINITION_BASE_URL + "/organizationTypeCS", "Collection")]
        fhir_org.active = True
        fhir_org.name = self.name
        if self.alias is not None:
            fhir_org.alias = [self.alias]
        if self.url is not None:
            fhir_org.telecom = [self.create_url(self.url)]
        if self.contact_name or self.contact_surname or self.contact_email:
            fhir_org.contact = [self.__create_contact()]
        fhir_org.partOf = self.__create_managing_entity_reference(managing_organization_fhir_id)
        extensions = []
        if self.dataset_type is not None:
            extensions.append(self.__create_codeable_concept_extension(
                DEFINITION_BASE_URL + "/StructureDefinition/dataset-type-extension",
                DEFINITION_BASE_URL + "/datasetTypeCS",
                self.dataset_type))
        if self.sample_source is not None:
            extensions.append(self.__create_codeable_concept_extension(
                DEFINITION_BASE_URL + "/StructureDefinition/sample-source-extension",
                DEFINITION_BASE_URL + "/sampleSourceCS",
                self.sample_source))
        if self.sample_collection_setting is not None:
            extensions.append(self.__create_codeable_concept_extension(
                DEFINITION_BASE_URL + "/StructureDefinition/sample-collection-setting-extension",
                DEFINITION_BASE_URL + "/sampleCollectionSettingCS", self.sample_collection_setting))
        if self.collection_design is not None:
            for design in self.collection_design:
                extensions.append(self.__create_codeable_concept_extension(
                    DEFINITION_BASE_URL + "/StructureDefinition/collection-design-extension",
                    DEFINITION_BASE_URL + "/collectionDesignCS", design))
        if self.use_and_access_conditions is not None:
            for condition in self.use_and_access_conditions:
                extensions.append(self.__create_codeable_concept_extension(
                    DEFINITION_BASE_URL + "/StructureDefinition/use-and-access-conditions-extension",
                    DEFINITION_BASE_URL + "/useAndAccessConditionsCS", condition))
        if self.publications is not None:
            for publication in self.publications:
                extensions.append(self.__create_string_extension(
                    DEFINITION_BASE_URL + "/StructureDefinition/publication-extension", publication))
        if self.description is not None:
            extensions.append(self.__create_string_extension(
                DEFINITION_BASE_URL + "/StructureDefinition/description-extension", self.description))
        if extensions:
            fhir_org.extension = extensions
        return fhir_org

    def create_url(self, url: str) -> ContactPoint:
        contact_point = ContactPoint()
        contact_point.system = "url"
        contact_point.value = url
        return contact_point

    def __create_contact(self) -> OrganizationContact:
        contact = OrganizationContact()
        contact.name = HumanName()
        contact.name.given = [self.contact_name]
        contact.name.family = self.contact_surname
        contact.telecom = [ContactPoint()]
        contact.telecom[0].system = "email"
        contact.telecom[0].value = self.contact_email
        contact.address = Address()
        contact.address.country = self._country
        return contact

    @staticmethod
    def __create_codeable_concept(url: str, code: str):
        codeable_concept = CodeableConcept()
        codeable_concept.coding = [Coding()]
        codeable_concept.coding[0].code = code
        codeable_concept.coding[0].system = url
        return codeable_concept

    @staticmethod
    def __create_managing_entity_reference(managing_ogranization_fhir_id: str) -> FHIRReference:
        entity_reference = FHIRReference()
        entity_reference.reference = f"Organization/{managing_ogranization_fhir_id}"
        return entity_reference

    def __create_fhir_identifier(self) -> Identifier:
        """Create fhir identifier."""
        fhir_identifier = Identifier()
        fhir_identifier.value = self._identifier
        return fhir_identifier

    @staticmethod
    def __create_codeable_concept_extension(extension_url: str, codeable_concept_url: str,
                                            value: str) -> Extension:
        extension = Extension()
        extension.url = extension_url
        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.coding = [Coding()]
        extension.valueCodeableConcept.coding[0].code = value
        extension.valueCodeableConcept.coding[0].system = codeable_concept_url
        return extension

    @staticmethod
    def __create_integer_extension(extension_url, value) -> Extension:
        extension = Extension()
        extension.url = extension_url
        extension.valueInteger = value
        return extension

    @staticmethod
    def __create_string_extension(extension_url, value) -> Extension:
        extension = Extension()
        extension.url = extension_url
        extension.valueString = value
        return extension
