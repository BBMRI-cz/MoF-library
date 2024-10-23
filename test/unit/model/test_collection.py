import unittest

from fhirclient.models.group import Group

from src.MIABIS_on_FHIR.collection import Collection
from src.MIABIS_on_FHIR.gender import Gender
from src.MIABIS_on_FHIR.storage_temperature import StorageTemperature


class TestCollection(unittest.TestCase):
    collection_json = {'id': 'NGJKWUEOLKA', 'meta': {'profile': ['http://example.com/StructureDefinition/Collection']},
                       'extension': [{'url': 'http://example.com/StructureDefinition/number-of-subjects-extension',
                                      'valueInteger': 10},
                                     {'url': 'http://example.com/StructureDefinition/inclusion-criteria-extension',
                                      'valueCodeableConcept': {'coding': [{'code': 'HealthStatus',
                                                                           'system': 'http://example.com/inclusionCriteriaCS'}]}},
                                     {
                                         'url': 'http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity',
                                         'valueReference': {'reference': 'Specimen/sampleFhirId1'}}, {
                                         'url': 'http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity',
                                         'valueReference': {'reference': 'Specimen/sampleFhirId2'}}], 'active': True,
                       'actual': True, 'characteristic': [
            {'code': {'coding': [{'code': 'Age', 'system': 'http://example.com/characteristicCS'}]}, 'exclude': False,
             'valueRange': {'high': {'value': 100}, 'low': {'value': 0}}},
            {'code': {'coding': [{'code': 'Sex', 'system': 'http://example.com/characteristicCS'}]}, 'exclude': False,
             'valueCodeableConcept': {'coding': [{'code': 'male', 'system': 'http://example.com/sexCS'}]}},
            {'code': {'coding': [{'code': 'StorageTemperature', 'system': 'http://example.com/characteristicCS'}]},
             'exclude': False, 'valueCodeableConcept': {
                'coding': [{'code': 'LN', 'system': 'http://example.com/storageTemperatureCS'}]}},
            {'code': {'coding': [{'code': 'MaterialType', 'system': 'http://example.com/characteristicCS'}]},
             'exclude': False,
             'valueCodeableConcept': {'coding': [{'code': 'DNA', 'system': 'http://example.com/materialTypeCS'}]}},
            {'code': {'coding': [{'code': 'Diagnosis', 'system': 'http://example.com/characteristicCS'}]},
             'exclude': False,
             'valueCodeableConcept': {'coding': [{'code': 'C51', 'system': 'http://hl7.org/fhir/sid/icd-10'}]}}],
                       'identifier': [{'value': 'collectionId'}],
                       'managingEntity': {'reference': 'Organization/biobankFhirId'}, 'name': 'collectionName',
                       'type': 'person', 'resourceType': 'Group'}

    def test_collection_init(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        self.assertIsInstance(collection, Collection)
        self.assertEqual("collectionId", collection.identifier)
        self.assertEqual("collectionName", collection.name)
        self.assertEqual("collectionOrgId", collection.managing_collection_org_id)
        self.assertEqual(0, collection.age_range_low)
        self.assertEqual(100, collection.age_range_high)
        self.assertEqual([Gender.MALE], collection.genders)
        self.assertEqual([StorageTemperature.TEMPERATURE_LN], collection.storage_temperatures)
        self.assertEqual(["DNA"], collection.material_types)

    def test_collection_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            collection = Collection(37, "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN])

    def test_collection_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            collection = Collection("collectionId", 22, "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN])

    def test_collection_invalid_managing_biobank_id_type_innit(self):
        with self.assertRaises(TypeError):
            collection = Collection("collectionId", "collectionName", 22, [Gender.MALE], ["DNA"], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN])

    def test_collection_invalid_age_range_low_type_innit(self):
        with self.assertRaises(TypeError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], "0",
                                    100,
                                    [StorageTemperature.TEMPERATURE_LN])

    def test_collection_invalid_age_range_high_type_innit(self):
        with self.assertRaises(TypeError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0,
                                    "100",
                                    [StorageTemperature.TEMPERATURE_LN])

    def test_collection_invalid_gender_type_init(self):
        with self.assertRaises(TypeError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", "male", ["DNA"], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN])

    def test_collection_invalid_storage_temperature_type_init(self):
        with self.assertRaises(TypeError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                    "storageTemp")

    def test_collection_invalid_material_type_type_init(self):
        with self.assertRaises(ValueError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], [2], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN])

    def test_collection_set_identifier_ok(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        collection.identifier = "newId"
        self.assertEqual("newId", collection.identifier)

    def test_collection_set_identifier_invalid(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        with self.assertRaises(TypeError):
            collection.identifier = 37

    def test_collection_set_name_ok(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        collection.name = "newName"
        self.assertEqual("newName", collection.name)

    def test_collection_set_name_invalid(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        with self.assertRaises(TypeError):
            collection.name = 37

    def test_collection_set_managing_biobank_id_ok(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        collection.managing_biobank_id = "newBiobankId"
        self.assertEqual("newBiobankId", collection.managing_biobank_id)

    def test_collection_set_managing_biobank_id_invalid(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        with self.assertRaises(TypeError):
            collection.managing_collection_org_id = 37

    def test_collection_set_age_range_low_ok(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        collection.age_range_low = 10
        self.assertEqual(10, collection.age_range_low)

    def test_collection_set_age_range_low_invalid(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        with self.assertRaises(TypeError):
            collection.age_range_low = "10"

    def test_collection_set_age_range_high_ok(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        collection.age_range_high = 10
        self.assertEqual(10, collection.age_range_high)

    def test_collection_set_age_range_high_invalid(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        with self.assertRaises(TypeError):
            collection.age_range_high = "10"

    def test_collection_set_gender_ok(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        collection.genders = [Gender.FEMALE]
        self.assertEqual([Gender.FEMALE], collection.genders)

    def test_collection_set_gender_invalid(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        with self.assertRaises(TypeError):
            collection.genders = [37]

    def test_collection_set_storage_temperature_ok(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        collection.storage_temperatures = [StorageTemperature.TEMPERATURE_LN]
        self.assertEqual([StorageTemperature.TEMPERATURE_LN], collection.storage_temperatures)

    def test_collection_set_storage_temperature_invalid(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        with self.assertRaises(TypeError):
            collection.storage_temperatures = [37]

    def test_collection_set_material_type_ok(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        collection.material_types = ["RNA"]
        self.assertEqual(["RNA"], collection.material_types)

    def test_collection_set_material_type_invalid(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN])
        with self.assertRaises(ValueError):
            collection.material_types = [37]

    def test_collection_optional_args_description_invalid(self):
        with self.assertRaises(TypeError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN],
                                    description=37)

    def test_collection_optional_args_diagnosis(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN], diagnoses=["C51"], number_of_subjects=10,
                                inclusion_criteria=["Sex"], sample_ids=["samID1", "samID2"])
        self.assertEqual(["C51"], collection.diagnoses)
        self.assertEqual(10, collection.number_of_subjects)
        self.assertEqual(["Sex"], collection.inclusion_criteria)
        self.assertEqual(["samID1", "samID2"], collection.sample_ids)

    def test_collection_optional_args_diagnosis_invalid(self):
        with self.assertRaises(ValueError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN],
                                    diagnoses=["C11111"])

    def test_collection_optional_args_inclusion_criteria(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN],
                                inclusion_criteria=["HealthStatus"])
        self.assertEqual(["HealthStatus"], collection.inclusion_criteria)

    def test_collection_optional_args_inclusion_criteria_invalid(self):
        with self.assertRaises(ValueError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN],
                                    inclusion_criteria=["Invalid"])

    def test_collection_optional_args_number_of_subject(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                [StorageTemperature.TEMPERATURE_LN],
                                number_of_subjects=10)
        self.assertEqual(10, collection.number_of_subjects)

    def test_collection_optional_args_number_of_subject_invalid(self):
        with self.assertRaises(TypeError):
            collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"], 0, 100,
                                    [StorageTemperature.TEMPERATURE_LN],
                                    number_of_subjects="10")

    def test_collection_required_args_to_fhir(self):
        collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"])
        collection_fhir = collection.to_fhir("biobankFhirId", ["sampleFhirId1", "sampleFhirId2"])
        self.assertIsInstance(collection_fhir, Group)
        self.assertEqual(collection.identifier, collection_fhir.identifier[0].value)
        self.assertEqual(collection.name, collection_fhir.name)
        self.assertEqual("Organization/biobankFhirId", collection_fhir.managingEntity.reference)
        self.assertEqual(collection.genders[0].name.lower(),
                         collection_fhir.characteristic[0].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection.material_types[0],
                         collection_fhir.characteristic[1].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection_fhir.extension[0].valueReference.reference, "Specimen/sampleFhirId1")
        self.assertEqual(collection_fhir.extension[1].valueReference.reference, "Specimen/sampleFhirId2")

    def test_collection_optional_args_to_fhir(self):
        collection = Collection("collectionId", "collectionName", "managingBiobankId", [Gender.MALE], ["DNA"], 0, 100,
                                storage_temperatures=[StorageTemperature.TEMPERATURE_LN], diagnoses=["C51"],
                                inclusion_criteria=["HealthStatus"], number_of_subjects=10
                                )
        collection_fhir = collection.to_fhir("biobankFhirId", ["sampleFhirId1", "sampleFhirId2"])
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
        self.assertEqual(collection.number_of_subjects, collection_fhir.extension[0].valueInteger)
        self.assertEqual(collection.inclusion_criteria[0],
                         collection_fhir.extension[1].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection_fhir.extension[2].valueReference.reference, "Specimen/sampleFhirId1")
        self.assertEqual(collection_fhir.extension[3].valueReference.reference, "Specimen/sampleFhirId2")

    def test_collection_from_json(self):
        collection = Collection.from_json(self.collection_json, "biobankId", ["sampleId1"])
        self.assertIsInstance(collection, Collection)
        self.assertEqual("collectionId", collection.identifier)
        self.assertEqual("collectionName", collection.name)
        self.assertEqual("biobankId", collection.managing_collection_org_id)
        self.assertEqual(0, collection.age_range_low)
        self.assertEqual(100, collection.age_range_high)
        self.assertEqual([Gender.MALE], collection.genders)
        self.assertEqual([StorageTemperature.TEMPERATURE_LN], collection.storage_temperatures)
        self.assertEqual(["DNA"], collection.material_types)
        self.assertEqual(["C51"], collection.diagnoses)
        self.assertEqual(["HealthStatus"], collection.inclusion_criteria)
        self.assertEqual(10, collection.number_of_subjects)
        self.assertEqual(["sampleId1"], collection.sample_ids)
        self.assertEqual("NGJKWUEOLKA", collection.collection_fhir_id)
        self.assertEqual("biobankFhirId", collection.managing_collection_org_fhir_id)
        self.assertEqual(["sampleFhirId1", "sampleFhirId2"], collection.sample_fhir_ids)

    def test_collection_to_fhir_empty_characteristics(self):
        collection = Collection("collectionId", "collectionName", "managingBiobankId",[], [], 0, 100,
                                 [], diagnoses=[],
                                inclusion_criteria=["HealthStatus"], number_of_subjects=10,
                                )
        collection_fhir = collection.to_fhir("biobankFhirId", ["sampleFhirId1", "sampleFhirId2"])
        self.assertIsInstance(collection_fhir, Group)
        self.assertEqual(collection.identifier, collection_fhir.identifier[0].value)
        self.assertEqual(collection.name, collection_fhir.name)
        self.assertEqual("Organization/biobankFhirId", collection_fhir.managingEntity.reference)
        self.assertEqual(10, collection_fhir.extension[0].valueInteger)
        self.assertEqual("HealthStatus", collection_fhir.extension[1].valueCodeableConcept.coding[0].code)
        self.assertEqual(collection_fhir.extension[2].valueReference.reference, "Specimen/sampleFhirId1")
