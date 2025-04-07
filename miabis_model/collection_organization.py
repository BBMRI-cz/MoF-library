"""Module for handling SampleCollection operations"""
from typing import Self

from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta
from fhirclient.models.organization import Organization

from miabis_model.incorrect_json_format import IncorrectJsonFormatException
from miabis_model.util.config import FHIRConfig
from miabis_model.util.constants import COLLECTION_DESIGN, COLLECTION_SAMPLE_COLLECTION_SETTING, \
    COLLECTION_SAMPLE_SOURCE, COLLECTION_DATASET_TYPE, COLLECTION_USE_AND_ACCESS_CONDITIONS
from miabis_model.util.parsing_util import get_nested_value, parse_contact, parse_reference_id
from miabis_model.util.util import create_country_of_residence, create_contact, create_codeable_concept_extension, \
    create_string_extension, create_fhir_identifier


class _CollectionOrganization:
    """Sample Collection represents a set of samples with at least one common characteristic."""
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
        :param country: Country of the collection.
        :param alias: Alias of the collection.
        :param url: URL of the collection.
        :param description: Description of the collection.
        :param dataset_type: Type of the dataset. Available values in the constants.py file
        :param sample_source: Source of the samples. Available values in the constants.py file
        :param sample_collection_setting: Setting of the sample collection. Available values in the constants.py file
        :param collection_design: Design of the collection. Available values in the constants.py file
        :param use_and_access_conditions: Conditions for use and access of the collection.
         Available values in the constants.py file
        :param publications: Publications related to the collection.
        """

        self.identifier: str = identifier
        self.name: str = name
        self.description: str = description
        self.managing_biobank_id: str = managing_biobank_id
        self.contact_name: str = contact_name
        self.contact_surname: str = contact_surname
        self.contact_email: str = contact_email
        self.country = country
        self.alias: str = alias
        self.url: str = url
        self.dataset_type = dataset_type
        self.sample_source = sample_source
        self.sample_collection_setting = sample_collection_setting
        self.collection_design = collection_design
        self.use_and_access_conditions = use_and_access_conditions
        self.publications = publications
        self._collection_org_fhir_id = None
        self._managing_biobank_fhir_id = None

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
        if collection_design is not None and not isinstance(collection_design, list):
            raise TypeError("Collection design must be a list of strings.")
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
            if not isinstance(use_and_access_conditions, list):
                raise TypeError("Use and access conditions must be a list.")
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

    @property
    def collection_org_fhir_id(self) -> str:
        return self._collection_org_fhir_id

    @property
    def managing_biobank_fhir_id(self) -> str:
        return self._managing_biobank_fhir_id

    @classmethod
    def from_json(cls, collection_json: dict, managing_biobank_id) -> Self:
        """
        Parse a JSON object into a MoFCollection object.
        :param collection_json: json object representing the collection.
        :param managing_biobank_id: id of managing biobank usually given by the institution (not a FHIR id!)
        :return: MoFCollection object
        """
        try:
            collection_org_fhir_id = get_nested_value(collection_json, ["id"])
            identifier = get_nested_value(collection_json, ["identifier", 0, "value"])
            name = get_nested_value(collection_json, ["name"])
            alias = get_nested_value(collection_json, ["alias", 0])
            managing_biobank_fhir_id = parse_reference_id(get_nested_value(collection_json, ["partOf", "reference"]))
            url = get_nested_value(collection_json, ["telecom", 0, "value"])
            contact = parse_contact(collection_json.get("contact", [{}])[0])
            country = get_nested_value(collection_json, ["address", 0, "country"])
            parsed_extensions = cls._parse_extensions(collection_json.get("extension", []))
            instance = cls(identifier, name, managing_biobank_id, contact["name"], contact["surname"], contact["email"],
                           country, alias, url, parsed_extensions["description"], parsed_extensions["dataset_type"],
                           parsed_extensions["sample_source"], parsed_extensions["sample_collection_setting"],
                           parsed_extensions["collection_design"], parsed_extensions["use_and_access_conditions"],
                           parsed_extensions["publications"])
            instance._collection_org_fhir_id = collection_org_fhir_id
            instance._managing_biobank_fhir_id = managing_biobank_fhir_id
            return instance
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into MoFCollection")

    @staticmethod
    def _parse_extensions(extensions: list) -> dict:
        parsed_extensions = {"dataset_type": None, "sample_source": None, "sample_collection_setting": None,
                             "collection_design": [], "use_and_access_conditions": [], "publications": [],
                             "description": None}
        dataset_url = FHIRConfig.get_extension_url("collection_organization", "dataset_type")
        sample_source_url = FHIRConfig.get_extension_url("collection_organization", "sample_source")
        collection_seting_url = FHIRConfig.get_extension_url("collection_organization", "sample_collection_setting")
        collection_design_url = FHIRConfig.get_extension_url("collection_organization", "collection_design")
        use_and_access_url = FHIRConfig.get_extension_url("collection_organization", "use_and_access")
        publications_url = FHIRConfig.get_extension_url("collection_organization", "publications")
        description_url = FHIRConfig.get_extension_url("collection_organization", "description")

        for extension in extensions:
            extension_url = extension["url"]
            if extension_url == dataset_url:
                value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                if value is not None:
                    parsed_extensions["dataset_type"] = value
            elif extension_url == sample_source_url:
                value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                if value is not None:
                    parsed_extensions["sample_source"] = value
            elif extension_url == collection_seting_url:
                value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                if value is not None:
                    parsed_extensions["sample_collection_setting"] = value
            elif extension_url == collection_design_url:
                value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                if value is not None:
                    parsed_extensions["collection_design"].append(value)
            elif extension_url == use_and_access_url:
                value = get_nested_value(extension, ["valueCodeableConcept", "coding", 0, "code"])
                if value is not None:
                    parsed_extensions["use_and_access_conditions"].append(value)
            elif extension_url == publications_url:
                value = get_nested_value(extension, ["valueString"])
                if value is not None:
                    parsed_extensions["publications"].append(value)
            elif extension_url == description_url:
                value = get_nested_value(extension, ["valueString"])
                if value is not None:
                    parsed_extensions["description"] = value
            else:
                continue
        for key, value in parsed_extensions.items():
            if not value:
                parsed_extensions[key] = None
        return parsed_extensions

    def to_fhir(self, managing_organization_fhir_id: str = None) -> Organization:
        """Return collection representation in FHIR
        :param managing_organization_fhir_id: FHIR Identifier of the managing organization"""
        managing_organization_fhir_id = managing_organization_fhir_id or self.managing_biobank_fhir_id
        if managing_organization_fhir_id is None:
            raise ValueError("Managing organization FHIR id must be provided either as an argument or as a property.")
        fhir_org = Organization()
        fhir_org.meta = Meta()
        fhir_org.meta.profile = [FHIRConfig.get_meta_profile_url("collection_organization")]
        fhir_org.identifier = [create_fhir_identifier(self.identifier)]
        # fhir_org.type = [create_codeable_concept(DEFINITION_BASE_URL + "/organizationTypeCS", "Collection")]
        fhir_org.active = True
        fhir_org.name = self.name
        if self.alias is not None:
            fhir_org.alias = [self.alias]
        if self.url is not None:
            fhir_org.telecom = [self.create_url(self.url)]
        if self.contact_name or self.contact_surname or self.contact_email:
            fhir_org.contact = [create_contact(self.contact_name, self._contact_surname, self._contact_email)]
            fhir_org.address = [create_country_of_residence(self.country)]
        fhir_org.partOf = self.__create_managing_entity_reference(managing_organization_fhir_id)
        extensions = []
        if self.dataset_type is not None:
            extensions.append(create_codeable_concept_extension(
                FHIRConfig.get_extension_url("collection_organization", "dataset_type"),
                FHIRConfig.get_code_system_url("collection_organization", "dataset_type"),
                self.dataset_type))
        if self.sample_source is not None:
            extensions.append(create_codeable_concept_extension(
                FHIRConfig.get_extension_url("collection_organization", "sample_source"),
                FHIRConfig.get_code_system_url("collection_organization", "sample_source"),
                self.sample_source))
        if self.sample_collection_setting is not None:
            extensions.append(create_codeable_concept_extension(
                FHIRConfig.get_extension_url("collection_organization", "sample_collection_setting"),
                FHIRConfig.get_code_system_url("collection_organization", "sample_collection_setting"),
                self.sample_collection_setting))
        if self.collection_design is not None:
            for design in self.collection_design:
                extensions.append(create_codeable_concept_extension(
                    FHIRConfig.get_extension_url("collection_organization", "collection_design"),
                    FHIRConfig.get_code_system_url("collection_organization", "collection_design"), design))
        if self.use_and_access_conditions is not None:
            for condition in self.use_and_access_conditions:
                extensions.append(create_codeable_concept_extension(
                    FHIRConfig.get_extension_url("collection_organization", "use_and_access"),
                    FHIRConfig.get_code_system_url("collection_organization", "use_and_access"), condition))
        if self.publications is not None:
            for publication in self.publications:
                extensions.append(create_string_extension(
                    FHIRConfig.get_extension_url("collection_organization", "publications"), publication))
        if self.description is not None:
            extensions.append(create_string_extension(
                FHIRConfig.get_extension_url("collection_organization", "description"), self.description))
        if extensions:
            fhir_org.extension = extensions
        return fhir_org

    def add_fhir_id_to_collection_organization(self, collection_org: Organization) -> Organization:
        """Add FHIR id to the FHIR representation of the CollectionOrganization. FHIR ID is necessary for updating the
                resource on the server.This method should only be called if the CollectionOrganization object
                was created by the from_json method. Otherwise,the diagnosis_report_fhir_id attribute is None,
                as the FHIR ID is generated by the server and is not known in advance."""
        collection_org.id = self.collection_org_fhir_id
        return collection_org

    @staticmethod
    def create_url(url: str) -> ContactPoint:
        contact_point = ContactPoint()
        contact_point.system = "url"
        contact_point.value = url
        return contact_point

    @staticmethod
    def __create_managing_entity_reference(managing_organization_fhir_id: str) -> FHIRReference:
        entity_reference = FHIRReference()
        entity_reference.reference = f"Organization/{managing_organization_fhir_id}"
        return entity_reference

    def __eq__(self, other):
        if not isinstance(other, _CollectionOrganization):
            return False
        return self.identifier == other.identifier and \
            self.name == other.name and \
            self.description == other.description and \
            self.managing_biobank_id == other.managing_biobank_id and \
            self.contact_name == other.contact_name and \
            self.contact_surname == other.contact_surname and \
            self.contact_email == other.contact_email and \
            self.country == other.country and \
            self.alias == other.alias and \
            self.url == other.url and \
            self.dataset_type == other.dataset_type and \
            self.sample_source == other.sample_source and \
            self.sample_collection_setting == other.sample_collection_setting and \
            self.collection_design == other.collection_design and \
            self.use_and_access_conditions == other.use_and_access_conditions and \
            self.publications == other.publications
