"""Module for handling SampleCollection operations"""
from typing import Self

import icd10
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.extension import Extension
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.group import Group, GroupCharacteristic
from fhirclient.models.identifier import Identifier
from fhirclient.models.meta import Meta
from fhirclient.models.quantity import Quantity
from fhirclient.models.range import Range

from MIABIS_on_FHIR.gender import MoFGender
from MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException
from MIABIS_on_FHIR.storage_temperature import MoFStorageTemperature
from _constants import COLLECTION_DESIGN, COLLECTION_SAMPLE_COLLECTION_SETTING, COLLECTION_SAMPLE_SOURCE, \
    COLLECTION_DATASET_TYPE, COLLECTION_INCLUSION_CRITERIA, COLLECTION_USE_AND_ACCESS_CONDITIONS, MATERIAL_TYPE_CODES, \
    DEFINITION_BASE_URL


class MoFCollection:
    """Sample Collection represents a set of samples with at least one common characteristic."""

    # TODO age range units
    def __init__(self, identifier: str, name: str, managing_biobank_id: str,
                 age_range_low: int,
                 age_range_high: int, genders: list[MoFGender], storage_temperatures: list[MoFStorageTemperature],
                 material_types: list[str], description: str = None, diagnoses: list[str] = None,
                 dataset_type: str = None,
                 sample_source: str = None,
                 sample_collection_setting: str = None, collection_design: list[str] = None,
                 use_and_access_conditions: list[str] = None,
                 number_of_subjects: int = None, inclusion_criteria: list[str] = None, publications: list[str] = None):
        """
        :param identifier: Collection identifier same format as in the BBMRI-ERIC directory.
        :param name: Name of the collection.
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
        if not isinstance(identifier, str):
            raise TypeError("Collection identifier must be a string.")
        if not isinstance(name, str):
            raise TypeError("Collection name must be a string.")
        if description is not None and not isinstance(description, str):
            raise TypeError("Collection description must be a string.")
        if not isinstance(managing_biobank_id, str):
            raise TypeError("Managing biobank identifier must be a string.")
        if not isinstance(age_range_low, int):
            raise TypeError("Age range low must be an integer.")
        if not isinstance(age_range_high, int):
            raise TypeError("Age range high must be an integer.")
        for gender in genders:
            if not isinstance(gender, MoFGender):
                raise TypeError("Gender in the list must be an instance of MoFGender.")
        for storage_temperature in storage_temperatures:
            if not isinstance(storage_temperature, MoFStorageTemperature):
                raise TypeError("Storage temperature in the list must be an instance of MoFStorageTemperature.")
        for material_type in material_types:
            if material_type not in MATERIAL_TYPE_CODES:
                raise ValueError(f"{material_type} is not a valid code for material type")

        self._identifier: str = identifier
        self._name: str = name
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
        if number_of_subjects is not None and not isinstance(number_of_subjects, int):
            raise TypeError("Number of subjects must be an integer.")
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
    def age_range_low(self) -> int:
        return self._age_range_low

    @age_range_low.setter
    def age_range_low(self, age_range_low: int):
        if not isinstance(age_range_low, int):
            raise TypeError("Age range low must be an integer.")
        self._age_range_low = age_range_low

    @property
    def age_range_high(self) -> int:
        return self._age_range_high

    @age_range_high.setter
    def age_range_high(self, age_range_high: int):
        if not isinstance(age_range_high, int):
            raise TypeError("Age range high must be an integer.")
        self._age_range_high = age_range_high

    @property
    def genders(self) -> list[MoFGender]:
        return self._genders

    @genders.setter
    def genders(self, genders: list[MoFGender]):
        for gender in genders:
            if not isinstance(gender, MoFGender):
                raise TypeError("Gender must be an MoFGender")
        self._genders = genders

    @property
    def storage_temperatures(self) -> list[MoFStorageTemperature]:
        return self._storage_temperatures

    @storage_temperatures.setter
    def storage_temperatures(self, storage_temperatures: list[MoFStorageTemperature]):
        for storage_temperature in storage_temperatures:
            if not isinstance(storage_temperature, MoFStorageTemperature):
                raise TypeError("Storage temperature must be an MoFStorageTemperature")
        self._storage_temperatures = storage_temperatures

    @property
    def material_types(self) -> list[str]:
        return self._material_types

    @material_types.setter
    def material_types(self, material_types: list[str]):
        for material_type in material_types:
            if material_type not in MATERIAL_TYPE_CODES:
                raise ValueError(f"{material_type} is not a valid code for material type")
        self._material_types = material_types

    @property
    def diagnoses(self) -> list[str]:
        return self._diagnoses

    @diagnoses.setter
    def diagnoses(self, diagnoses: list[str]):
        for diagnosis in diagnoses:
            if not icd10.exists(diagnosis):
                raise ValueError("The provided string is not a valid ICD-10 code.")
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

    @classmethod
    def from_json(cls, collection_json: dict, managing_biobank_id) -> Self:
        try:
            identifier = collection_json["identifier"][0]["value"]
            age_range_low = None
            age_range_high = None
            name = collection_json["name"]
            genders = []
            storage_temperatures = []
            material_types = []
            diagnoses = None
            dataset_type = None
            sample_source = None
            sample_collection_setting = None
            collection_design = None
            use_and_access_conditions = None
            number_of_subjects = None
            inclusion_criteria = None
            publications = None
            description = None
            for characteristic in collection_json["characteristic"]:
                match characteristic["code"]["coding"][0]["code"]:
                    case "Age":
                        age_range_low = characteristic["valueRange"]["low"]["value"]
                        age_range_high = characteristic["valueRange"]["high"]["value"]
                    case "Sex":
                        genders.append(
                            MoFGender.from_string(characteristic["valueCodeableConcept"]["coding"][0]["code"]))
                    case "StorageTemperature":
                        storage_temperatures.append(MoFStorageTemperature(
                            characteristic["valueCodeableConcept"]["coding"][0]["code"]))
                    case "MaterialType":
                        material_types.append(characteristic["valueCodeableConcept"]["coding"][0]["code"])
                    case "Diagnosis":
                        if diagnoses is None:
                            diagnoses = []
                        diagnoses.append(characteristic["valueCodeableConcept"]["coding"][0]["code"])
                    case _:
                        pass
            if age_range_low is None or age_range_high is None:
                raise IncorrectJsonFormatException("Age range is missing in the collection json.")

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
                    case "number-of-subjects-extension":
                        number_of_subjects = ext["valueInteger"]
                    case "inclusion-criteria-extension":
                        if inclusion_criteria is None:
                            inclusion_criteria = []
                        inclusion_criteria.append(ext["valueCodeableConcept"]["coding"][0]["code"])
                    case "publication-extension":
                        if publications is None:
                            publications = []
                        publications.append(ext["valueString"])
                    case "description-extension":
                        description = ext["valueString"]
                    case _:
                        pass
            return cls(identifier, name, managing_biobank_id, age_range_low, age_range_high, genders,
                       storage_temperatures, material_types, description, diagnoses, dataset_type, sample_source,
                       sample_collection_setting, collection_design, use_and_access_conditions, number_of_subjects,
                       inclusion_criteria, publications)



        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into MoFCollection")

    def to_fhir(self, managing_organization_fhir_id: str) -> Group:
        """Return collection representation in FHIR
        :param managing_organization_fhir_id: FHIR Identifier of the managing organization"""
        fhir_group = Group()
        fhir_group.meta = Meta()
        fhir_group.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Collection"]
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
        if self.diagnoses is not None:
            for diagnosis in self.diagnoses:
                fhir_group.characteristic.append(self.__create_diagnosis_characteristic(diagnosis))
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
        if self.number_of_subjects is not None:
            extensions.append(self.__create_integer_extension(
                DEFINITION_BASE_URL + "/StructureDefinition/number-of-subjects-extension", self.number_of_subjects))
        if self.inclusion_criteria is not None:
            for criteria in self.inclusion_criteria:
                extensions.append(self.__create_codeable_concept_extension(
                    DEFINITION_BASE_URL + "/StructureDefinition/inclusion-criteria-extension",
                    DEFINITION_BASE_URL + "/inclusionCriteriaCS", criteria))
        if self.publications is not None:
            for publication in self.publications:
                extensions.append(self.__create_string_extension(
                    DEFINITION_BASE_URL + "/StructureDefinition/publication-extension", publication))
        if self.description is not None:
            extensions.append(self.__create_string_extension(
                DEFINITION_BASE_URL + "/StructureDefinition/description-extension", self.description))
        if extensions:
            fhir_group.extension = extensions
        return fhir_group

    def __create_age_range_characteristic(self, age_low: int, age_high: int) -> GroupCharacteristic:
        # TODO add age range units
        age_range_characteristic = GroupCharacteristic()
        age_range_characteristic.exclude = False
        age_range_characteristic.code = self.__create_codeable_concept(DEFINITION_BASE_URL + "/characteristicCS", "Age")
        age_range_characteristic.valueRange = Range()
        age_range_characteristic.valueRange.low = Quantity()
        age_range_characteristic.valueRange.low.value = age_low
        age_range_characteristic.valueRange.high = Quantity()
        age_range_characteristic.valueRange.high.value = age_high
        return age_range_characteristic

    def __create_sex_characteristic(self, code: str) -> GroupCharacteristic:
        sex_characteristic = GroupCharacteristic()
        sex_characteristic.exclude = False
        sex_characteristic.code = self.__create_codeable_concept(DEFINITION_BASE_URL + "/characteristicCS", "Sex")
        sex_characteristic.valueCodeableConcept = self.__create_codeable_concept(DEFINITION_BASE_URL + "/sexCS", code)
        return sex_characteristic

    def __create_storage_temperature_characteristic(self,
                                                    storage_temperature: MoFStorageTemperature) -> GroupCharacteristic:
        storage_temperature_characteristic = GroupCharacteristic()
        storage_temperature_characteristic.exclude = False
        storage_temperature_characteristic.code = self.__create_codeable_concept(
            DEFINITION_BASE_URL + "/characteristicCS",
            "StorageTemperature")
        storage_temperature_characteristic.valueCodeableConcept = self.__create_codeable_concept(
            DEFINITION_BASE_URL + "/storageTemperatureCS", storage_temperature.value)
        return storage_temperature_characteristic

    def __create_material_type_characteristic(self, material_type: str) -> GroupCharacteristic:
        material_type_characteristic = GroupCharacteristic()
        material_type_characteristic.exclude = False
        material_type_characteristic.code = self.__create_codeable_concept(DEFINITION_BASE_URL + "/characteristicCS",
                                                                           "MaterialType")
        material_type_characteristic.valueCodeableConcept = self.__create_codeable_concept(
            DEFINITION_BASE_URL + "/materialTypeCS", material_type)
        return material_type_characteristic

    def __create_diagnosis_characteristic(self, diagnosis: str) -> GroupCharacteristic:
        diagnosis_characteristic = GroupCharacteristic()
        diagnosis_characteristic.exclude = False
        diagnosis_characteristic.code = self.__create_codeable_concept(DEFINITION_BASE_URL + "/characteristicCS",
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
