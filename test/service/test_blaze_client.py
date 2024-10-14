import datetime
import unittest

import pytest as pytest

from src.MIABIS_on_FHIR.condition import Condition
from src.MIABIS_on_FHIR.diagnosis_report import DiagnosisReport
from src.MIABIS_on_FHIR.gender import Gender
from src.MIABIS_on_FHIR.observation import Observation
from src.MIABIS_on_FHIR.sample import Sample
from src.MIABIS_on_FHIR.sample_donor import SampleDonor
from src.MIABIS_on_FHIR.storage_temperature import StorageTemperature
from src.client.blaze_client import BlazeClient


class TestBlazeService(unittest.TestCase):
    example_donor = SampleDonor("donorId", Gender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
    example_sample = Sample("sampleId", "donorId", "Urine", datetime.datetime(year=2022, month=10, day=20),
                            storage_temperature=StorageTemperature.TEMPERATURE_LN)
    example_observation = Observation("C50", "sampleId", "donorId", datetime.datetime(year=2022, month=10, day=20))

    # example_diagnosis_report =

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        self.blaze_service = BlazeClient("http://localhost:8080/fhir", "", "")

    def test_is_resource_present_in_blaze_true(self):
        pass

    def test_is_resource_present_in_blaze_false(self):
        pass

    def test_get_fhir_resource_as_json_existing(self):
        pass

    def test_get_fhir_resource_as_json_non_existing(self):
        pass

    def test_get_fhir_id_existing(self):
        pass

    def test_get_fhir_id_non_existing(self):
        pass

    def test_get_identifier_by_fhir_id_existing(self):
        pass

    def test_get_identifier_by_fhir_id_non_existing(self):
        pass

    def test_upload_donor(self):
        donor = SampleDonor("donorId", Gender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
        donor_id = self.blaze_service.upload_donor(donor)
        self.assertIsNotNone(donor_id)

    def test_delete_donor(self):
        donor_fhir_id = self.blaze_service.get_fhir_id("Patient", "donorId")
        deleted = self.blaze_service.delete_donor(donor_fhir_id)
        self.assertTrue(deleted)

    def test_upload_sample(self):
        donor = SampleDonor("donorId", Gender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
        self.blaze_service.upload_donor(donor)
        sample = Sample("sampleId", "donorId", "Urine", datetime.datetime(year=2022, month=10, day=20),
                        storage_temperature=StorageTemperature.TEMPERATURE_LN)
        sample_id = self.blaze_service.upload_sample(sample)
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Specimen", sample_id))
        self.assertIsNotNone(sample_id)

    def test_delete_sample(self):
        sample_fhir_id = self.blaze_service.get_fhir_id("Specimen", "sampleId")
        deleted = self.blaze_service.delete_sample(sample_fhir_id)
        self.assertFalse(self.blaze_service.is_resource_present_in_blaze("Specimen", "sampleId", "identifier"))
        self.assertTrue(deleted)

    def test_upload_observation(self):
        # sample = Sample("sampleId", "donorId", "Urine", datetime.datetime(year=2022, month=10, day=20),
        #                 storage_temperature=StorageTemperature.TEMPERATURE_LN)
        # self.blaze_service.upload_sample(sample)
        # donor_fhir_id = self.blaze_service.get_fhir_id("Patient", "donorId")
        observation = Observation("C51", "sampleId", "donorId", datetime.datetime(year=2022, month=10, day=20))
        observation_id = self.blaze_service.upload_observation(observation)
        # self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Observation", observation_id))
        self.assertIsNotNone(observation_id)

    def test_delete_observation(self):
        observation_fhir_id = self.blaze_service.get_fhir_id("Observation", "sampleId")
        deleted = self.blaze_service.delete_observation(observation_fhir_id)
        self.assertTrue(deleted)
        self.assertFalse(self.blaze_service.is_resource_present_in_blaze("Observation", observation_fhir_id))

    def test_upload_diagnosis_report(self):
        diagnosis_report = DiagnosisReport("sampleId", "donorId")
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(diagnosis_report)
        self.assertIsNotNone(diagnosis_report_fhir_id)

    def test_delete_diagnosis_report(self):
        sample_fhir_id = self.blaze_service.get_fhir_id("Specimen", "sampleId")
        diagnosis_report_fhir_id = self.blaze_service.get_diagnosis_report_fhir_id_belonging_to_sample(sample_fhir_id)
        deleted = self.blaze_service.delete_diagnosis_report(diagnosis_report_fhir_id)
        self.assertTrue(deleted)

    def test_upload_condition(self):
        condition = Condition("donorId")
        condition_fhir_id = self.blaze_service.upload_condition(condition)
        self.assertIsNotNone(condition_fhir_id)

    def test_add_diagnosis_report_to_already_present_condition(self):
        sample_fhir_id = self.blaze_service.get_fhir_id("Specimen", "sampleId")
        donor_fhir_id = self.blaze_service.get_fhir_id("Patient", "donorId")
        diagnosis_report_fhir_id = self.blaze_service.get_diagnosis_report_fhir_id_belonging_to_sample(sample_fhir_id)
        condition_fhir_id = self.blaze_service.get_condition_fhir_id_by_donor_fhir_id(donor_fhir_id)
        dig_rep_added = self.blaze_service.add_diagnosis_reports_to_condition(condition_fhir_id,
                                                                              [diagnosis_report_fhir_id])
        self.assertTrue(dig_rep_added)

    def test_get_observation_fhir_ids_belonging_to_sample(self):
        # observation = Observation("C50", "sampleId", "donorId", datetime.datetime(year=2022, month=10, day=20))
        # observation = Observation("C51", "sampleId", "donorId", datetime.datetime(year=2022, month=10, day=20))
        sample_fhir_id = self.blaze_service.get_fhir_id("Specimen", "sampleId")
        obs_fhir_ids = self.blaze_service.get_observation_fhir_ids_belonging_to_sample(sample_fhir_id)
        self.assertTrue(len(obs_fhir_ids) != 0)

    def test_upload_sample_with_diagnosis_chain(self):
        donor = SampleDonor("donorId", Gender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
        sample = Sample("sampleId", "donorId", "Urine", datetime.datetime(year=2022, month=10, day=20),
                        storage_temperature=StorageTemperature.TEMPERATURE_LN)
        observation1 = Observation("C51", "sampleId", "donorId", datetime.datetime(year=2022, month=10, day=20))
        observation2 = Observation("C52", "sampleId", "donorId", datetime.datetime(year=2022, month=10, day=20))
        diagnosis_report = DiagnosisReport("sampleId", ["sampleId", "sampleId"])
        donor_fhir_id = self.blaze_service.get_fhir_id("Patient", "donorId")
        condition = Condition("donorId")
        observation1_fhir_id = self.blaze_service.upload_observation(observation1, donor_fhir_id)
        observation2_fhir_id = self.blaze_service.upload_observation(observation2, donor_fhir_id)
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report()
        condition.to_fhir()

    def test_get_identifier_by_fhir_id(self):
        fhir_id = "NonExistentId"
        identifier = self.blaze_service.get_identifier_by_fhir_id("Patient", fhir_id)
