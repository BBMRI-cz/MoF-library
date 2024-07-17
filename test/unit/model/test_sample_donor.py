import unittest
from datetime import datetime

from MIABIS_on_FHIR.MoF_sample_donor import MoFSampleDonor
from MIABIS_on_FHIR.gender import Gender


class TestSampleDonor(unittest.TestCase):
    def test_sample_donor_init(self):
        patient = MoFSampleDonor("testId")
        self.assertIsInstance(patient, MoFSampleDonor)

    def test_sample_donor_id_must_be_str(self):
        with self.assertRaises(TypeError):
            MoFSampleDonor(37)

    def test_get_sample_donor_id(self):
        self.assertEqual(MoFSampleDonor("test").identifier, "test")

    def test_sample_donor_set_gender_ok(self):
        donor = MoFSampleDonor("test")
        self.assertEqual(None, donor.gender)
        donor.gender = Gender.MALE
        self.assertEqual(Gender.MALE, donor.gender)
        donor.gender = Gender.UNKNOWN
        self.assertEqual(Gender.UNKNOWN, donor.gender)

    def test_sample_donor_init_invalid_gender(self):
        with self.assertRaises(TypeError):
           d = MoFSampleDonor("testId", "invalid_gender")

    def test_sample_donor_set_invalid_gender(self):
        donor = MoFSampleDonor("testId")
        with self.assertRaises(TypeError):
            donor.gender = "invalid_gender"

    def test_sample_donor_set_birth_date_ok(self):
        donor = MoFSampleDonor("testId")
        date = datetime(year=2022, month=10, day=20)
        donor.date_of_birth = date
        self.assertEqual(date , donor.date_of_birth)

    def test_sample_donor_set_birth_date_invalid(self):
        donor = MoFSampleDonor("testId")
        with self.assertRaises(TypeError):
            donor.date_of_birth = 2022

    def test_sample_donor_set_dataset_type_ok(self):
        donor = MoFSampleDonor("testId")
        donor.dataset_type = "Lifestyle"
        self.assertEqual("Lifestyle", donor.dataset_type)

    def test_sample_donor_set_dataset_type_invalid_innit(self):
        with self.assertRaises(ValueError):
            donor = MoFSampleDonor("testId", dataset_type="invalid")

    def test_sample_donor_set_dataset_type_invalid(self):
        donor = MoFSampleDonor("testId")
        with self.assertRaises(ValueError):
            donor.dataset_type = "invalid"

    def test_sample_donor_minimum_args_ok(self):
        self.assertIsInstance(MoFSampleDonor("patientId"), MoFSampleDonor)

    def test_sample_donor_minimum_args_to_fhir_ok(self):
        donor = MoFSampleDonor("patientId")
        self.assertEqual("patientId", donor.to_fhir().identifier[0].value)

    def test_sample_donor_with_gender_ok(self):
        donor = MoFSampleDonor("patientId", Gender.MALE)
        self.assertIsInstance(donor, MoFSampleDonor)
        self.assertEqual(donor.gender, Gender.MALE)

    def test_sample_donor_with_gender_to_fhir_ok(self):
        donor = MoFSampleDonor("patientId", Gender.FEMALE)
        self.assertEqual("female", donor.to_fhir().gender)

    def test_sample_donor_with_birth_date_to_fhir_ok(self):
        donor = MoFSampleDonor("patientId", birth_date=datetime(year=2022, month=10, day=20))
        self.assertEqual("2022-10-20", donor.to_fhir().birthDate.date.isoformat())

    def test_sample_donor_with_dataset_type_to_fhir_ok(self):
        donor = MoFSampleDonor("patientId", dataset_type="Lifestyle")
        self.assertEqual("Lifestyle", donor.to_fhir().extension[0].valueCodeableConcept.coding[0].code)

    def test_sample_donor_with_all_args_to_fhir_ok(self):
        donor = MoFSampleDonor("patientId", Gender.FEMALE, datetime(year=2022, month=10, day=20), "Lifestyle")
        donor_fhir = donor.to_fhir()
        self.assertEqual("patientId", donor_fhir.identifier[0].value)
        self.assertEqual("female", donor_fhir.gender)
        self.assertEqual("2022-10-20", donor_fhir.birthDate.date.isoformat())
        self.assertEqual("Lifestyle", donor_fhir.extension[0].valueCodeableConcept.coding[0].code)

