import unittest
from datetime import datetime

from MIABIS_on_FHIR.sample_donor import SampleDonor
from MIABIS_on_FHIR.gender import Gender


class TestSampleDonor(unittest.TestCase):
    donor_json = {'meta': {'versionId': '1', 'lastUpdated': '2024-07-30T07:47:50.796Z',
                           'profile': ['https://fhir.bbmri.de/StructureDefinition/Patient']}, 'birthDate': '2022-10-20',
                  'resourceType': 'Patient', 'extension': [
            {'url': 'https://example.org/StructureDefinition/datasetType',
             'valueCodeableConcept': {'coding': [{'code': 'Other'}]}}], 'id': 'DEICTQNW6TXY6FFC',
                  'identifier': [{'value': 'donorId'}], 'gender': 'male'}

    def test_sample_donor_init(self):
        patient = SampleDonor("testId")
        self.assertIsInstance(patient, SampleDonor)

    def test_sample_donor_id_must_be_str(self):
        with self.assertRaises(TypeError):
            SampleDonor(37)

    def test_get_sample_donor_id(self):
        self.assertEqual(SampleDonor("test").identifier, "test")

    def test_sample_donor_set_gender_ok(self):
        donor = SampleDonor("test")
        self.assertEqual(None, donor.gender)
        donor.gender = Gender.MALE
        self.assertEqual(Gender.MALE, donor.gender)
        donor.gender = Gender.UNKNOWN
        self.assertEqual(Gender.UNKNOWN, donor.gender)

    def test_sample_donor_init_invalid_gender(self):
        with self.assertRaises(TypeError):
            d = SampleDonor("testId", "invalid_gender")

    def test_sample_donor_set_invalid_gender(self):
        donor = SampleDonor("testId")
        with self.assertRaises(TypeError):
            donor.gender = "invalid_gender"

    def test_sample_donor_set_birth_date_ok(self):
        donor = SampleDonor("testId")
        date = datetime(year=2022, month=10, day=20)
        donor.date_of_birth = date
        self.assertEqual(date, donor.date_of_birth)

    def test_sample_donor_set_birth_date_invalid(self):
        donor = SampleDonor("testId")
        with self.assertRaises(TypeError):
            donor.date_of_birth = 2022

    def test_sample_donor_set_dataset_type_ok(self):
        donor = SampleDonor("testId")
        donor.dataset_type = "Lifestyle"
        self.assertEqual("Lifestyle", donor.dataset_type)

    def test_sample_donor_set_dataset_type_invalid_innit(self):
        with self.assertRaises(ValueError):
            donor = SampleDonor("testId", dataset_type="invalid")

    def test_sample_donor_set_dataset_type_invalid(self):
        donor = SampleDonor("testId")
        with self.assertRaises(ValueError):
            donor.dataset_type = "invalid"

    def test_sample_donor_minimum_args_ok(self):
        self.assertIsInstance(SampleDonor("patientId"), SampleDonor)

    def test_sample_donor_minimum_args_to_fhir_ok(self):
        donor = SampleDonor("patientId")
        self.assertEqual("patientId", donor.to_fhir().identifier[0].value)

    def test_sample_donor_with_gender_ok(self):
        donor = SampleDonor("patientId", Gender.MALE)
        self.assertIsInstance(donor, SampleDonor)
        self.assertEqual(donor.gender, Gender.MALE)

    def test_sample_donor_with_gender_to_fhir_ok(self):
        donor = SampleDonor("patientId", Gender.FEMALE)
        self.assertEqual("female", donor.to_fhir().gender)

    def test_sample_donor_with_birth_date_to_fhir_ok(self):
        donor = SampleDonor("patientId", birth_date=datetime(year=2022, month=10, day=20))
        self.assertEqual("2022-10-20", donor.to_fhir().birthDate.date.isoformat())

    def test_sample_donor_with_dataset_type_to_fhir_ok(self):
        donor = SampleDonor("patientId", dataset_type="Lifestyle")
        self.assertEqual("Lifestyle", donor.to_fhir().extension[0].valueCodeableConcept.coding[0].code)

    def test_sample_donor_with_all_args_to_fhir_ok(self):
        donor = SampleDonor("patientId", Gender.FEMALE, datetime(year=2022, month=10, day=20), "Lifestyle")
        donor_fhir = donor.to_fhir()
        self.assertEqual("patientId", donor_fhir.identifier[0].value)
        self.assertEqual("female", donor_fhir.gender)
        self.assertEqual("2022-10-20", donor_fhir.birthDate.date.isoformat())
        self.assertEqual("Lifestyle", donor_fhir.extension[0].valueCodeableConcept.coding[0].code)

    def test_sample_donor_from_json(self):
        donor = SampleDonor.from_json(self.donor_json)
        self.assertEqual("donorId", donor.identifier)
        self.assertEqual(Gender.MALE, donor.gender)
        self.assertEqual(datetime(year=2022, month=10, day=20), donor.date_of_birth)
        self.assertEqual("Other", donor.dataset_type)
        self.assertEqual("DEICTQNW6TXY6FFC", donor.donor_fhir_id)
