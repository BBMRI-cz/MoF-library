"""Module for handling SampleCollection operations"""
from typing import Self

import simple_icd_10 as icd10
from fhirclient.models.extension import Extension
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.group import Group, GroupCharacteristic
from fhirclient.models.meta import Meta
from fhirclient.models.quantity import Quantity
from fhirclient.models.range import Range

from MIABIS_on_FHIR._constants import COLLECTION_INCLUSION_CRITERIA, MATERIAL_TYPE_CODES, DEFINITION_BASE_URL
from MIABIS_on_FHIR._util import create_fhir_identifier, create_integer_extension, create_codeable_concept_extension, \
    create_codeable_concept
from MIABIS_on_FHIR.gender import Gender
from MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException
from MIABIS_on_FHIR.storage_temperature import StorageTemperature


class MoFCollection:
    """Sample Collection represents a set of samples with at least one common characteristic."""

    # TODO age range units
    def __init__(self, identifier: str, name: str, managing_collection_org_id: str,
                 age_range_low: int,
                 age_range_high: int, genders: list[Gender], storage_temperatures: list[StorageTemperature],
                 material_types: list[str], diagnoses: list[str] = None, number_of_subjects: int = None,
                 inclusion_criteria: list[str] = None, sample_ids: list[str] = None, ):
        """
        :param identifier: Collection identifier same format as in the BBMRI-ERIC directory.
        :param name: Name of the collection.
        :param description: Description of the collection.
        :param managing_biobank_id: Identifier of the collection-organization resource.
        :param age_range_low: Lower bound of the age range of the subjects in the collection.
        :param age_range_high: Upper bound of the age range of the subjects in the collection.
        :param genders: List of genders of the subjects in the collection.
        :param storage_temperatures: List of storage temperatures of the samples in the collection.
        :param material_types: List of material types of the samples in the collection.
        :param diagnoses: List of diagnoses of the subjects in the collection.
         Available values in the _constants.py file
        :param number_of_subjects: Number of subjects in the collection.
        :param inclusion_criteria: Inclusion criteria for the subjects in the collection.
        :param sample_ids: List of sample identifiers belonging to the collection.
        """
        if not isinstance(identifier, str):
            raise TypeError("Collection identifier must be a string.")
        if not isinstance(name, str):
            raise TypeError("Collection name must be a string.")
        if not isinstance(managing_collection_org_id, str):
            raise TypeError("Managing biobank identifier must be a string.")
        if not isinstance(age_range_low, int):
            raise TypeError("Age range low must be an integer.")
        if not isinstance(age_range_high, int):
            raise TypeError("Age range high must be an integer.")
        for gender in genders:
            if not isinstance(gender, Gender):
                raise TypeError("Gender in the list must be an instance of MoFGender.")
        for storage_temperature in storage_temperatures:
            if not isinstance(storage_temperature, StorageTemperature):
                raise TypeError("Storage temperature in the list must be an instance of MoFStorageTemperature.")
        for material_type in material_types:
            if material_type not in MATERIAL_TYPE_CODES:
                raise ValueError(f"{material_type} is not a valid code for material type")
        if sample_ids is not None:
            for sample_id in sample_ids:
                if not isinstance(sample_id, str):
                    raise TypeError("Sample id must be a string.")

        if diagnoses is not None:
            for diagnosis in diagnoses:
                if not icd10.is_valid_item(diagnosis):
                    raise TypeError("The provided string is not a valid ICD-10 code.")

        if number_of_subjects is not None and not isinstance(number_of_subjects, int):
            raise TypeError("Number of subjects must be an integer.")

        if inclusion_criteria is not None:
            for inclusion in inclusion_criteria:
                if inclusion not in COLLECTION_INCLUSION_CRITERIA:
                    raise ValueError(f"{inclusion} is not a valid code for inclusion criteria")

        self._identifier: str = identifier
        self._name: str = name
        self._managing_collection_org_id: str = managing_collection_org_id
        self._age_range_low: int = age_range_low
        self._age_range_high: int = age_range_high
        self._genders = genders
        self._storage_temperatures = storage_temperatures
        self._diagnoses = diagnoses
        self._material_types = material_types
        self._number_of_subjects = number_of_subjects
        self._sample_ids = sample_ids
        self._inclusion_criteria = inclusion_criteria

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
    def managing_collection_org_id(self) -> str:
        return self._managing_collection_org_id

    @managing_collection_org_id.setter
    def managing_collection_org_id(self, managing_collection_org_id: str):
        if not isinstance(managing_collection_org_id, str):
            raise TypeError("Managing biobank identifier must be a string.")
        self._managing_collection_org_id = managing_collection_org_id

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
    def genders(self) -> list[Gender]:
        return self._genders

    @genders.setter
    def genders(self, genders: list[Gender]):
        for gender in genders:
            if not isinstance(gender, Gender):
                raise TypeError("Gender must be an MoFGender")
        self._genders = genders

    @property
    def storage_temperatures(self) -> list[StorageTemperature]:
        return self._storage_temperatures

    @storage_temperatures.setter
    def storage_temperatures(self, storage_temperatures: list[StorageTemperature]):
        for storage_temperature in storage_temperatures:
            if not isinstance(storage_temperature, StorageTemperature):
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
            if not icd10.is_valid_item(diagnosis):
                raise ValueError("The provided string is not a valid ICD-10 code.")
        self._diagnoses = diagnoses

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
    def sample_ids(self) -> list[str]:
        return self._sample_ids

    @sample_ids.setter
    def sample_ids(self, sample_ids: list[str]):
        for sample_id in sample_ids:
            if not isinstance(sample_id, str):
                raise TypeError("Sample id must be a string.")
        self._sample_ids = sample_ids

    @classmethod
    def from_json(cls, collection_json: dict, managing_collection_organization_id: str, sample_ids: list[str]) -> Self:
        """
        Parse a JSON object into a MoFCollection object.
        :param collection_json: json object representing the collection.
        :param managing_collection_organization_id: id of collection-organization usually given by the institution (not a FHIR id!)
        :param sample_ids: list of sample ids belonging to the collection, given by the institution (not FHIR ids!)
        :return: MoFCollection object
        """
        try:
            identifier = collection_json["identifier"][0]["value"]
            age_range_low = None
            age_range_high = None
            name = collection_json["name"]
            genders = []
            storage_temperatures = []
            material_types = []
            diagnoses = None
            number_of_subjects = None
            inclusion_criteria = None
            for characteristic in collection_json["characteristic"]:
                match characteristic["code"]["coding"][0]["code"]:
                    case "Age":
                        age_range_low = characteristic["valueRange"]["low"]["value"]
                        age_range_high = characteristic["valueRange"]["high"]["value"]
                    case "Sex":
                        genders.append(
                            Gender.from_string(characteristic["valueCodeableConcept"]["coding"][0]["code"]))
                    case "StorageTemperature":
                        storage_temperatures.append(StorageTemperature(
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
                    case "number-of-subjects-extension":
                        number_of_subjects = ext["valueInteger"]
                    case "inclusion-criteria-extension":
                        if inclusion_criteria is None:
                            inclusion_criteria = []
                        inclusion_criteria.append(ext["valueCodeableConcept"]["coding"][0]["code"])
                    case _:
                        pass
            return cls(identifier, name, managing_collection_organization_id, age_range_low, age_range_high, genders,
                       storage_temperatures, material_types, diagnoses, number_of_subjects, inclusion_criteria,
                       sample_ids)
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into MoFCollection")

    def to_fhir(self, managing_organization_fhir_id: str, sample_fhir_ids: list[str]) -> Group:
        """Return collection representation in FHIR
        :param managing_organization_fhir_id: FHIR Identifier of the managing organization
        :param sample_fhir_ids: List of FHIR identifiers of the samples in the collection"""
        fhir_group = Group()
        fhir_group.meta = Meta()
        fhir_group.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Collection"]
        fhir_group.identifier = [create_fhir_identifier(self.identifier)]
        fhir_group.active = True
        fhir_group.actual = True
        fhir_group.type = "person"
        fhir_group.name = self.name
        fhir_group.managingEntity = self.__create_managing_entity_reference(managing_organization_fhir_id)
        fhir_group.characteristic = []
        fhir_group.characteristic.append(
            self.__create_age_range_characteristic(self.age_range_low, self.age_range_high))
        for gender in self.genders:
            fhir_group.characteristic.append(
                self.__create_codeable_concept_characteristic("Sex", DEFINITION_BASE_URL + "/sexCS",
                                                              gender.name.lower()))
        for storage_temperature in self.storage_temperatures:
            fhir_group.characteristic.append(
                self.__create_codeable_concept_characteristic("StorageTemperature",
                                                              DEFINITION_BASE_URL + "/storageTemperatureCS",
                                                              storage_temperature.value))
        for material in self.material_types:
            fhir_group.characteristic.append(
                self.__create_codeable_concept_characteristic("MaterialType", DEFINITION_BASE_URL + "/materialTypeCS",
                                                              material))
        if self.diagnoses is not None:
            for diagnosis in self.diagnoses:
                fhir_group.characteristic.append(
                    self.__create_codeable_concept_characteristic("Diagnosis", "http://hl7.org/fhir/sid/icd-10",
                                                                  diagnosis))
        extensions = []
        if self.number_of_subjects is not None:
            extensions.append(create_integer_extension(
                DEFINITION_BASE_URL + "/StructureDefinition/number-of-subjects-extension", self.number_of_subjects))
        if self.inclusion_criteria is not None:
            for criteria in self.inclusion_criteria:
                extensions.append(create_codeable_concept_extension(
                    DEFINITION_BASE_URL + "/StructureDefinition/inclusion-criteria-extension",
                    DEFINITION_BASE_URL + "/inclusionCriteriaCS", criteria))
        for sample_fhir_id in sample_fhir_ids:
            extensions.append(self.__create_member_extension(sample_fhir_id))
        if extensions:
            fhir_group.extension = extensions
        return fhir_group

    @staticmethod
    def __create_member_extension(sample_fhir_id: str):
        extension = Extension()
        extension.url = "http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity"
        extension.valueReference = FHIRReference()
        extension.valueReference.reference = f"Specimen/{sample_fhir_id}"
        return extension

    @staticmethod
    def __create_age_range_characteristic(age_low: int, age_high: int) -> GroupCharacteristic:
        age_range_characteristic = GroupCharacteristic()
        age_range_characteristic.exclude = False
        age_range_characteristic.code = create_codeable_concept(DEFINITION_BASE_URL + "/characteristicCS", "Age")
        age_range_characteristic.valueRange = Range()
        age_range_characteristic.valueRange.low = Quantity()
        age_range_characteristic.valueRange.low.value = age_low
        age_range_characteristic.valueRange.high = Quantity()
        age_range_characteristic.valueRange.high.value = age_high
        return age_range_characteristic

    @staticmethod
    def __create_sex_characteristic(code: str) -> GroupCharacteristic:
        sex_characteristic = GroupCharacteristic()
        sex_characteristic.exclude = False
        sex_characteristic.code = create_codeable_concept(DEFINITION_BASE_URL + "/characteristicCS", "Sex")
        sex_characteristic.valueCodeableConcept = create_codeable_concept(DEFINITION_BASE_URL + "/sexCS", code)
        return sex_characteristic

    @staticmethod
    def __create_codeable_concept_characteristic(characteristic_code: str, codeable_concept_url: str,
                                                 value: str) -> GroupCharacteristic:
        characteristic = GroupCharacteristic()
        characteristic.exclude = False
        characteristic.code = create_codeable_concept(DEFINITION_BASE_URL + "/characteristicCS",
                                                      characteristic_code)
        characteristic.valueCodeableConcept = create_codeable_concept(codeable_concept_url, value)
        return characteristic

    @staticmethod
    def __create_managing_entity_reference(managing_ogranization_fhir_id: str) -> FHIRReference:
        entity_reference = FHIRReference()
        entity_reference.reference = f"Organization/{managing_ogranization_fhir_id}"
        return entity_reference