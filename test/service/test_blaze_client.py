import datetime
import unittest

import pytest as pytest

from src.MIABIS_on_FHIR.gender import Gender
from src.MIABIS_on_FHIR.sample import Sample
from src.MIABIS_on_FHIR.sample_donor import SampleDonor
from src.MIABIS_on_FHIR.storage_temperature import StorageTemperature
from src.client.blaze_client import BlazeClient


class TestBlazeService(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        self.blaze_service = BlazeClient("http://localhost:8080/fhir", "", "")

    def test_upload_donor(self):
        donor = SampleDonor("donorId", Gender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
        donor_id = self.blaze_service.upload_donor(donor)
        self.assertIsNotNone(donor_id)

    def test_delete_donor(self):
        donor_fhir_id = self.blaze_service.get_fhir_id("Patient", "donorId")
        self.assertTrue(self.blaze_service.delete_donor(donor_fhir_id))


    def test_upload_sample(self):
        sample = Sample("sampleId", "donorId", "Urine", datetime.datetime(year=2022, month=10, day=20),
                        storage_temperature=StorageTemperature.TEMPERATURE_GN)
        sample_id = self.blaze_service.upload_sample(sample)
        self.assertIsNotNone(sample_id)

    def test_upload_sample_chain(self):
        sample = Sample("sampleId", "donorId", "Urine", datetime.datetime(year=2022, month=10, day=20),
                        storage_temperature=StorageTemperature.TEMPERATURE_GN)

    def test_get_identifier_by_fhir_id(self):
        fhir_id = "NonExistentId"
        identifier = self.blaze_service.get_identifier_by_fhir_id("Patient", fhir_id)
