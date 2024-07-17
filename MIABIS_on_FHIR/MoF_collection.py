"""Module for handling SampleCollection operations"""
import icd10
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.extension import Extension
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.group import Group, GroupCharacteristic
from fhirclient.models.identifier import Identifier
from fhirclient.models.organization import Organization
from fhirclient.models.quantity import Quantity
from fhirclient.models.range import Range

from MIABIS_on_FHIR.gender import Gender
from MIABIS_on_FHIR.storage_temperature import StorageTemperature
from _constants import COLLECTION_DESIGN, COLLECTION_SAMPLE_COLLECTION_SETTING, COLLECTION_SAMPLE_SOURCE, \
    COLLECTION_DATASET_TYPE, COLLECTION_INCLUSION_CRITERIA, COLLECTION_USE_AND_ACCESS_CONDITIONS


class MoFCollection:
    """Sample Collection represents a set of samples with at least one common characteristic."""

    # TODO age range units
    def __init__(self, identifier: str, name: str, acronym: str, managing_biobank_id: str,
                 age_range_low: int,
                 age_range_high: int, genders: list[Gender], storage_temperatures: list[StorageTemperature],
                 material_types: list[str], description: str = None, diagnoses: list[str] = None,
                 dataset_type: str = None,
                 sample_source: str = None,
                 sample_collection_setting: str = None, collection_design: list[str] = None,
                 use_and_access_conditions: list[str] = None,
                 number_of_subjects: int = None, inclusion_criteria: list[str] = None, publications: list[str] = None):
        """
        :param identifier: Collection identifier same format as in the BBMRI-ERIC directory.
        :param name: Name of the collection.
        :param acronym: Acronym of the collection.
        :param description: Description of the collection.
        :param managing_biobank_id: Identifier of the biobank managing the collection.
        :param age_range_low: Lower bound of the age range of the subjects in the collection.
        :param age_range_high: Upper bound of the age range of the subjects in the collection.
        :param genders: List of genders of the subjects in the collection.
        :param storage_temperatures: List of storage temperatures of the samples in the collection.
        :param material_types: List of material types of the samples in the collection.
        :param diagnoses: List of diagnoses of the subjects in the collection.
        :param dataset_type: Type of the dataset. Available values in the _constants.py file
        :param sample_source: Source of the samples. Available values in the _constants.py file
        :param sample_collection_setting: Setting of the sample collection. Available values in the _constants.py file
        :param collection_design: Design of the collection. Available values in the _constants.py file
        :param use_and_access_conditions: Conditions for use and access of the collection.
         Available values in the _constants.py file
        :param number_of_subjects: Number of subjects in the collection.
        :param inclusion_criteria: Inclusion criteria for the subjects in the collection.
        :param publications: Publications related to the collection.
        """
        self._identifier: str = identifier
        self._name: str = name
        self._acronym: str = acronym
        self._description: str = description
        self._managing_biobank_id: str = managing_biobank_id
        self._age_range_low: int = age_range_low
        self._age_range_high: int = age_range_high
        self._genders = genders
        self._storage_temperatures = storage_temperatures
        self._material_types = material_types
        if diagnoses is not None:
            for diagnosis in diagnoses:
                if not icd10.exists(diagnosis):
                    raise TypeError("The provided string is not a valid ICD-10 code.")
        self._diagnoses = diagnoses

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
            for design in collection_design:
                if design not in COLLECTION_DESIGN:
                    raise ValueError(f"{design} is not a valid code for collection design")
        self._collection_design = collection_design

        if use_and_access_conditions is not None:
            for condition in use_and_access_conditions:
                if condition not in COLLECTION_USE_AND_ACCESS_CONDITIONS:
                    raise ValueError(f"{condition} is not a valid code for use and access conditions")
        self._use_and_access_conditions = use_and_access_conditions
        self._number_of_subjects = number_of_subjects
        if inclusion_criteria is not None:
            for inclusion in inclusion_criteria:
                if inclusion not in COLLECTION_INCLUSION_CRITERIA:
                    raise ValueError(f"{inclusion} is not a valid code for inclusion criteria")
        self._inclusion_criteria = inclusion_criteria
        self._publications = publications

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
    def acronym(self) -> str:
        return self._acronym

    @acronym.setter
    def acronym(self, acronym: str):
        self._acronym = acronym

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def managing_biobank_id(self) -> str:
        return self._managing_biobank_id

    @managing_biobank_id.setter
    def managing_biobank_id(self, managing_biobank_id: str):
        self._managing_biobank_id = managing_biobank_id

    @property
    def age_range_low(self) -> int:
        return self._age_range_low

    @age_range_low.setter
    def age_range_low(self, age_range_low: int):
        self._age_range_low = age_range_low

    @property
    def age_range_high(self) -> int:
        return self._age_range_high

    @age_range_high.setter
    def age_range_high(self, age_range_high: int):
        self._age_range_high = age_range_high

    @property
    def genders(self) -> list[Gender]:
        return self._genders

    @genders.setter
    def genders(self, genders: list[Gender]):
        self._genders = genders

    @property
    def storage_temperatures(self) -> list[StorageTemperature]:
        return self._storage_temperatures

    @storage_temperatures.setter
    def storage_temperatures(self, storage_temperatures: list[StorageTemperature]):
        self._storage_temperatures = storage_temperatures

    @property
    def material_types(self) -> list[str]:
        return self._material_types

    @material_types.setter
    def material_types(self, material_types: list[str]):
        self._material_types = material_types

    @property
    def diagnoses(self) -> list[str]:
        return self._diagnoses

    @diagnoses.setter
    def diagnoses(self, diagnoses: list[str]):
        self._diagnoses = diagnoses

    @property
    def dataset_type(self) -> str:
        return self._dataset_type

    @dataset_type.setter
    def dataset_type(self, dataset_type: str):
        self._dataset_type = dataset_type

    @property
    def sample_source(self) -> str:
        return self._sample_source

    @sample_source.setter
    def sample_source(self, sample_source: str):
        self._sample_source = sample_source

    @property
    def sample_collection_setting(self) -> str:
        return self._sample_collection_setting

    @sample_collection_setting.setter
    def sample_collection_setting(self, sample_collection_setting: str):
        self._sample_collection_setting = sample_collection_setting

    @property
    def collection_design(self) -> list[str]:
        return self._collection_design

    @collection_design.setter
    def collection_design(self, collection_design: list[str]):
        self._collection_design = collection_design

    @property
    def use_and_access_conditions(self) -> list[str]:
        return self._use_and_access_conditions

    @use_and_access_conditions.setter
    def use_and_access_conditions(self, use_and_access_conditions: list[str]):
        self._use_and_access_conditions = use_and_access_conditions

    @property
    def number_of_subjects(self) -> int:
        return self._number_of_subjects

    @number_of_subjects.setter
    def number_of_subjects(self, number_of_subjects: int):
        self._number_of_subjects = number_of_subjects

    @property
    def inclusion_criteria(self) -> list[str]:
        return self._inclusion_criteria

    @inclusion_criteria.setter
    def inclusion_criteria(self, inclusion_criteria: list[str]):
        self._inclusion_criteria = inclusion_criteria

    @property
    def publications(self) -> list[str]:
        return self._publications

    @publications.setter
    def publications(self, publications: list[str]):
        self._publications = publications

    def to_fhir(self, managing_organization_fhir_id: str) -> Organization:
        """Return collection representation in FHIR
        :param managing_organization_fhir_id: FHIR Identifier of the managing organization"""
        fhir_group = Group()
        fhir_group.identifier = [self.__create_fhir_identifier()]
        fhir_group.active = True
        fhir_group.actual = True
        fhir_group.type = "person"
        fhir_group.name = self.name
        fhir_group.managingEntity = self.__create_managing_entity_reference(managing_organization_fhir_id)
        fhir_group.characteristic = []
        fhir_group.characteristic.append(
            self.__create_age_range_characteristic(self.age_range_low, self.age_range_high))
        for gender in self.genders:
            fhir_group.characteristic.append(self.__create_sex_characteristic(gender.name.lower()))
        for storage_temperature in self.storage_temperatures:
            fhir_group.characteristic.append(self.__create_storage_temperature_characteristic(storage_temperature))
        for material in self.material_types:
            fhir_group.characteristic.append(self.__create_material_type_characteristic(material))
        for diagnosis in self.diagnoses:
            fhir_group.characteristic.append(self.__create_diagnosis_characteristic(diagnosis))
        extensions = []
        if self.dataset_type is not None:
            extensions.append(self.__create_codeable_concept_extension(
                "https://example.com/StructureDefinition/dataset-type-extension", "http://example.com/datasetTypeCS",
                self.dataset_type))
        if self.sample_source is not None:
            extensions.append(self.__create_codeable_concept_extension(
                "https://example.com/StructureDefinition/sample-source-extension", "http://example.com/sampleSourceCS",
                self.sample_source))
        if self.sample_collection_setting is not None:
            extensions.append(self.__create_codeable_concept_extension(
                "https://example.com/StructureDefinition/sample-collection-setting-extension",
                "http://example.com/sampleCollectionSettingCS", self.sample_collection_setting))
        if self.collection_design is not None:
            for design in self.collection_design:
                extensions.append(self.__create_codeable_concept_extension(
                    "https://example.com/StructureDefinition/collection-design-extension",
                    "http://example.com/collectionDesignCS", design))
        if self.collection_design is not None:
            for condition in self.use_and_access_conditions:
                extensions.append(self.__create_codeable_concept_extension(
                    "https://example.com/StructureDefinition/use-and-access-conditions-extension",
                    "http://example.com/useAndAccessConditionsCS", condition))
        if self.use_and_access_conditions is not None:
            for condition in self.use_and_access_conditions:
                extensions.append(self.__create_codeable_concept_extension(
                    "https://example.com/StructureDefinition/use-and-access-conditions-extension",
                    "http://example.com/useAndAccessConditionsCS", condition))
        if self.number_of_subjects is not None:
            extensions.append(self.__create_integer_extension(
                "https://example.com/StructureDefinition/number-of-subjects-extension", self.number_of_subjects))
        if self.inclusion_criteria is not None:
            for criteria in self.inclusion_criteria:
                extensions.append(self.__create_codeable_concept_extension(
                    "https://example.com/StructureDefinition/inclusion-criteria-extension",
                    "http://example.com/inclusionCriteriaCS", criteria))
        if self.publications is not None:
            for publication in self.publications:
                extensions.append(self.__create_string_extension(
                    "https://example.com/StructureDefinition/publication-extension", publication))
        if self.description is not None:
            extensions.append(self.__create_string_extension(
                "https://example.com/StructureDefinition/description-extension", self.description))
        if extensions:
            fhir_group.extension = extensions
        return fhir_group

    def __create_age_range_characteristic(self, age_low: int, age_high: int) -> GroupCharacteristic:
        # TODO add age range units
        age_range_characteristic = GroupCharacteristic()
        age_range_characteristic.code = self.__create_codeable_concept("http://example.com/characteristicCS", "Age")
        age_range_characteristic.valueRange = Range()
        age_range_characteristic.valueRange.low = Quantity()
        age_range_characteristic.valueRange.low.value = age_low
        age_range_characteristic.valueRange.high = Quantity()
        age_range_characteristic.valueRange.high.value = age_high
        return age_range_characteristic

    def __create_sex_characteristic(self, code: str) -> GroupCharacteristic:
        sex_characteristic = GroupCharacteristic()
        sex_characteristic.code = self.__create_codeable_concept("http://example.com/characteristicCS", "Sex")
        sex_characteristic.valueCodeableConcept = self.__create_codeable_concept("http://example.com/sexCS", code)
        return sex_characteristic

    def __create_storage_temperature_characteristic(self,
                                                    storageTemperature: StorageTemperature) -> GroupCharacteristic:
        storage_temperature_characteristic = GroupCharacteristic()
        storage_temperature_characteristic.code = self.__create_codeable_concept("http://example.com/characteristicCS",
                                                                                 "StorageTemperature")
        storage_temperature_characteristic.valueCodeableConcept = self.__create_codeable_concept(
            "http://example.com/storageTemperatureCS", storageTemperature.value)
        return storage_temperature_characteristic

    def __create_material_type_characteristic(self, material_type: str) -> GroupCharacteristic:
        material_type_characteristic = GroupCharacteristic()
        material_type_characteristic.code = self.__create_codeable_concept("http://example.com/characteristicCS",
                                                                           "MaterialType")
        material_type_characteristic.valueCodeableConcept = self.__create_codeable_concept(
            "http://example.com/materialTypeCS", material_type)
        return material_type_characteristic

    def __create_diagnosis_characteristic(self, diagnosis: str) -> GroupCharacteristic:
        diagnosis_characteristic = GroupCharacteristic()
        diagnosis_characteristic.code = self.__create_codeable_concept("http://example.com/characteristicCS",
                                                                       "Diagnosis")
        diagnosis_characteristic.valueCodeableConcept = self.__create_codeable_concept("http://hl7.org/fhir/sid/icd-10",
                                                                                       diagnosis)
        return diagnosis_characteristic

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

    def __create_codeable_concept_extension(self, extension_url: str, codeable_concept_url: str,
                                            value: str) -> Extension:
        extension = Extension()
        extension.url = extension_url
        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.coding = [Coding()]
        extension.valueCodeableConcept.coding[0].code = value
        extension.valueCodeableConcept.coding[0].system = codeable_concept_url
        return extension

    def __create_integer_extension(self,extension_url, value) -> Extension:
        extension = Extension()
        extension.url = extension_url
        extension.valueInteger = value
        return extension

    def __create_string_extension(self,extension_url, value) -> Extension:
        extension = Extension()
        extension.url = extension_url
        extension.valueString = value
        return extension