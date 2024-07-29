import unittest

from fhirclient.models.group import Group

from MIABIS_on_FHIR.MoF_collection import MoFCollection
from MIABIS_on_FHIR.gender import MoFGender
from MIABIS_on_FHIR.storage_temperature import MoFStorageTemperature


class TestCollection(unittest.TestCase):

    def test_collection_init(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        self.assertIsInstance(collection, MoFCollection)
        self.assertEqual("collectionId", collection.identifier)
        self.assertEqual("collectionName", collection.name)
        self.assertEqual("collectionAcronym", collection.acronym)
        self.assertEqual("managingBiobankId", collection.managing_biobank_id)
        self.assertEqual(0, collection.age_range_low)
        self.assertEqual(100, collection.age_range_high)
        self.assertEqual([MoFGender.MALE], collection.genders)
        self.assertEqual([MoFStorageTemperature.TEMPERATURE_GN], collection.storage_temperatures)
        self.assertEqual(["DNA"], collection.material_types)

    def test_collection_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection(37, "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])

    def test_collection_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", 22, "collectionAcronym", "managingBiobankId", 0, 100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])

    def test_collection_invalid_acronym_type_innit(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", 22, "managingBiobankId", 0, 100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])

    def test_collection_invalid_managing_biobank_id_type_innit(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", 22, 0, 100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])

    def test_collection_invalid_age_range_low_type_innit(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", "0",
                                       100, [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])

    def test_collection_invalid_age_range_high_type_innit(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       "100", [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])

    def test_collection_invalid_gender_type_init(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100, 37, [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])

    def test_collection_invalid_storage_temperature_type_init(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       22, [MoFGender.MALE], [0], ["DNA"])

    def test_collection_invalid_material_type_type_init(self):
        with self.assertRaises(ValueError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       22, [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], [0])

    def test_collection_set_identifier_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.identifier = "newId"
        self.assertEqual("newId", collection.identifier)

    def test_collection_set_identifier_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(TypeError):
            collection.identifier = 37

    def test_collection_set_name_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.name = "newName"
        self.assertEqual("newName", collection.name)

    def test_collection_set_name_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(TypeError):
            collection.name = 37

    def test_collection_set_acronym_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.acronym = "newAcronym"
        self.assertEqual("newAcronym", collection.acronym)

    def test_collection_set_acronym_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(TypeError):
            collection.acronym = 37

    def test_collection_set_managing_biobank_id_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.managing_biobank_id = "newBiobankId"
        self.assertEqual("newBiobankId", collection.managing_biobank_id)

    def test_collection_set_managing_biobank_id_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(TypeError):
            collection.managing_biobank_id = 37

    def test_collection_set_age_range_low_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.age_range_low = 10
        self.assertEqual(10, collection.age_range_low)

    def test_collection_set_age_range_low_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(TypeError):
            collection.age_range_low = "10"

    def test_collection_set_age_range_high_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.age_range_high = 10
        self.assertEqual(10, collection.age_range_high)

    def test_collection_set_age_range_high_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(TypeError):
            collection.age_range_high = "10"

    def test_collection_set_gender_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.genders = [MoFGender.FEMALE]
        self.assertEqual([MoFGender.FEMALE], collection.genders)

    def test_collection_set_gender_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(TypeError):
            collection.genders = [37]

    def test_collection_set_storage_temperature_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.storage_temperatures = [MoFStorageTemperature.TEMPERATURE_LN]
        self.assertEqual([MoFStorageTemperature.TEMPERATURE_LN], collection.storage_temperatures)

    def test_collection_set_storage_temperature_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(TypeError):
            collection.storage_temperatures = [37]

    def test_collection_set_material_type_ok(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection.material_types = ["RNA"]
        self.assertEqual(["RNA"], collection.material_types)

    def test_collection_set_material_type_invalid(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        with self.assertRaises(ValueError):
            collection.material_types = [37]

    def test_collection_optional_args_description(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   description="description")
        self.assertEqual("description", collection.description)

    def test_collection_optional_args_description_invalid(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       description=37)

    def test_collection_optional_args_diagnosis(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"], diagnoses=["C51"])
        self.assertEqual(["C51"], collection.diagnoses)

    def test_collection_optional_args_diagnosis_invalid(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       diagnoses=["C11111"])

    def test_collection_optional_args_dataset_type(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   dataset_type="Genomic")
        self.assertEqual("Genomic", collection.dataset_type)

    def test_collection_optional_args_dataset_type_invalid(self):
        with self.assertRaises(ValueError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       dataset_type="Invalid")

    def test_collection_optional_args_sample_source(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   sample_source="Human")
        self.assertEqual("Human", collection.sample_source)

    def test_collection_optional_args_sample_source_invalid(self):
        with self.assertRaises(ValueError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       sample_source="Invalid")

    def test_collection_optional_args_sample_collection_setting(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   sample_collection_setting="Environment")
        self.assertEqual("Environment", collection.sample_collection_setting)

    def test_collection_optional_args_sample_collection_setting_invalid(self):
        with self.assertRaises(ValueError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       sample_collection_setting="Invalid")

    def test_collection_optional_args_collection_design(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   collection_design=["CaseControl"])
        self.assertEqual(["CaseControl"], collection.collection_design)

    def test_collection_optional_args_collection_design_invalid(self):
        with self.assertRaises(ValueError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       collection_design=["Invalid"])

    def test_collection_optional_args_use_and_access_conditions(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   use_and_access_conditions=["CommercialUse"])
        self.assertEqual(["CommercialUse"], collection.use_and_access_conditions)

    def test_collection_optional_args_use_and_access_conditions_invalid(self):
        with self.assertRaises(ValueError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       use_and_access_conditions=["Invalid"])

    def test_collection_optional_args_inclusion_criteria(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   inclusion_criteria=["HealthStatus"])
        self.assertEqual(["HealthStatus"], collection.inclusion_criteria)

    def test_collection_optional_args_inclusion_criteria_invalid(self):
        with self.assertRaises(ValueError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       inclusion_criteria=["Invalid"])

    def test_collection_optional_args_number_of_subject(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   number_of_subjects=10)
        self.assertEqual(10, collection.number_of_subjects)

    def test_collection_optional_args_number_of_subject_invalid(self):
        with self.assertRaises(TypeError):
            collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0,
                                       100,
                                       [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                       number_of_subjects="10")

    def test_collection_required_args_to_fhir(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"])
        collection_fhir = collection.to_fhir("biobankFhirId")
        self.assertIsInstance(collection_fhir, Group)
        self.assertEqual(collection.identifier, collection_fhir.identifier[0].value)
        self.assertEqual(collection.name, collection_fhir.name)
        self.assertEqual("Organization/biobankFhirId", collection_fhir.managingEntity.reference)
        self.assertEqual(collection.age_range_low, collection_fhir.characteristic[0].valueRange.low.value)
        self.assertEqual(collection.age_range_high, collection_fhir.characteristic[0].valueRange.high.value)
        self.assertEqual(collection.genders[0].name.lower(),
                         collection_fhir.characteristic[1].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.storage_temperatures[0].value,
                         collection_fhir.characteristic[2].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.material_types[0],
                         collection_fhir.characteristic[3].valueCodeableConcept.coding[0].code)

    def test_collection_optional_args_to_fhir(self):
        collection = MoFCollection("collectionId", "collectionName", "collectionAcronym", "managingBiobankId", 0, 100,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_GN], ["DNA"],
                                   description="description", diagnoses=["C51"], dataset_type="Genomic",
                                   sample_source="Human", sample_collection_setting="Environment",
                                   collection_design=["CaseControl"], use_and_access_conditions=["CommercialUse"],
                                   inclusion_criteria=["HealthStatus"], number_of_subjects=10,
                                   publications=["publication"])
        collection_fhir = collection.to_fhir("biobankFhirId")
        self.assertIsInstance(collection_fhir, Group)
        self.assertEqual(collection.identifier, collection_fhir.identifier[0].value)
        self.assertEqual(collection.name, collection_fhir.name)
        self.assertEqual("Organization/biobankFhirId", collection_fhir.managingEntity.reference)
        self.assertEqual(collection.age_range_low, collection_fhir.characteristic[0].valueRange.low.value)
        self.assertEqual(collection.age_range_high, collection_fhir.characteristic[0].valueRange.high.value)
        self.assertEqual(collection.genders[0].name.lower(),
                         collection_fhir.characteristic[1].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.storage_temperatures[0].value,
                         collection_fhir.characteristic[2].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.material_types[0],
                         collection_fhir.characteristic[3].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.diagnoses[0], collection_fhir.characteristic[4].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.dataset_type, collection_fhir.extension[0].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.sample_source, collection_fhir.extension[1].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.sample_collection_setting,
                         collection_fhir.extension[2].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.collection_design[0],
                         collection_fhir.extension[3].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.use_and_access_conditions[0],
                         collection_fhir.extension[4].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.number_of_subjects, collection_fhir.extension[5].valueInteger)
        self.assertEqual(collection.inclusion_criteria[0],
                         collection_fhir.extension[6].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.publications[0], collection_fhir.extension[7].valueString)
        self.assertEqual(collection.description, collection_fhir.extension[8].valueString)
