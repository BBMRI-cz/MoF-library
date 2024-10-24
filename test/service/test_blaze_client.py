import datetime
import unittest

import pytest as pytest

from src.MIABIS_on_FHIR.biobank import Biobank
from src.MIABIS_on_FHIR.collection import Collection
from src.MIABIS_on_FHIR.collection_organization import CollectionOrganization
from src.MIABIS_on_FHIR.condition import Condition
from src.MIABIS_on_FHIR.diagnosis_report import DiagnosisReport
from src.MIABIS_on_FHIR.gender import Gender
from src.MIABIS_on_FHIR.network import Network
from src.MIABIS_on_FHIR.network_organization import NetworkOrganization
from src.MIABIS_on_FHIR.observation import Observation
from src.MIABIS_on_FHIR.sample import Sample
from src.MIABIS_on_FHIR.sample_donor import SampleDonor
from src.MIABIS_on_FHIR.storage_temperature import StorageTemperature
from src.client.NonExistentResourceException import NonExistentResourceException
from src.client.blaze_client import BlazeClient


class TestBlazeService(unittest.TestCase):
    example_donor = SampleDonor("donorId", Gender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
    example_samples = [Sample("sampleId", "donorId", "Urine", datetime.datetime(year=2022, month=10, day=20),
                              storage_temperature=StorageTemperature.TEMPERATURE_LN),
                       Sample("sampleId2", "donorId", "Nail", datetime.datetime(year=2020, month=11, day=21),
                              storage_temperature=StorageTemperature.TEMPERATURE_ROOM)
                       ]
    example_observations = [Observation("C50", "sampleId", "donorId", datetime.datetime(year=2022, month=10, day=20)),
                            Observation("C51", "sampleId", "donorId", datetime.datetime(year=2022, month=10, day=20)),
                            Observation("C50", "sampleId2", "donorId", datetime.datetime(year=2020, month=11, day=21)),
                            Observation("C45", "sampleId2", "donorId", datetime.datetime(year=2020, month=11, day=21))]

    example_diagnosis_reports = [DiagnosisReport("sampleId", "donorId"),
                                 DiagnosisReport("sampleId2", "donorId")]

    example_condition = Condition("donorId")

    example_biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                              "email", infrastructural_capabilities=["SampleStorage"],
                              organisational_capabilities=["RecontactDonors"],
                              bioprocessing_and_analysis_capabilities=["Genomics"])

    example_collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                    "contactSurname", "contactEmail", "cz", "alias", "url",
                                                    "description",
                                                    "LifeStyle", "Human", "Environment", ["CaseControl"],
                                                    ["CommercialUse"], ["publication"])
    example_collection = Collection("collectionId", "collectionName", "collectionOrgId", [Gender.MALE], ["DNA"],
                                    inclusion_criteria=["HealthStatus"])

    example_network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                              "contactSurname", "contactEmail", "country", ["Charter"],
                                              "juristicPerson")

    example_network = Network("networkId", "networkName", "networkOrgId", ["collectionId"], ["biobankId"])

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        self.blaze_service = BlazeClient("http://localhost:8080/fhir", "", "")
        yield
        try:
            pass
            donor_fhir_id = self.blaze_service.get_fhir_id("Patient", self.example_donor.identifier)
            if donor_fhir_id is not None:
                if not self.blaze_service.delete_donor(donor_fhir_id):
                    raise Exception("could not delete patient")
            # for observation in self.example_observations:
            # observation_fhir_id
            for sample in self.example_samples:
                sample_fhir_id = self.blaze_service.get_fhir_id("Specimen", sample.identifier)
                if sample_fhir_id is not None:
                    self.blaze_service.delete_sample(sample_fhir_id)
            # condition_fhir_id = self.blaze_service.get_condition_fhir_id_by_donor_fhir_id()
            biobank_fhir_id = self.blaze_service.get_fhir_id("Organization", self.example_biobank.identifier)
            collection_org_fhir_id = self.blaze_service.get_fhir_id("Organization",
                                                                    self.example_collection_org.identifier)
            if collection_org_fhir_id is not None:
                if not self.blaze_service.delete_collection_organization(collection_org_fhir_id):
                    raise Exception("could not delete collection organization")
            network_org_fhir_id = self.blaze_service.get_fhir_id("Organization", self.example_network_org.identifier)
            if network_org_fhir_id is not None:
                if not self.blaze_service.delete_network_organization(network_org_fhir_id):
                    raise Exception("could not delete network organization")
            if biobank_fhir_id is not None:
                if not self.blaze_service.delete_biobank(biobank_fhir_id):
                    raise Exception("could not delete biobank")
        except NonExistentResourceException:
            pass

    def test_is_resource_present_in_blaze_true(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Patient", donor_fhir_id))

    def test_is_resource_present_in_blaze_false(self):
        self.assertFalse(self.blaze_service.is_resource_present_in_blaze("Patient", "nonexistentId"))

    def test_get_fhir_resource_as_json_existing(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        donor_json = self.blaze_service.get_fhir_resource_as_json("Patient", donor_fhir_id)
        self.assertIsNotNone(donor_json)

    def test_get_fhir_resource_as_json_non_existing(self):
        non_existing_json = self.blaze_service.get_fhir_resource_as_json("Patient", "nonexistentId")
        self.assertIsNone(non_existing_json)

    def test_get_fhir_id_existing(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        donor_fhir_id_from_function = self.blaze_service.get_fhir_id("Patient", self.example_donor.identifier)
        self.assertEqual(donor_fhir_id, donor_fhir_id_from_function)

    def test_get_fhir_id_non_existing(self):
        non_existent_fhir_id = self.blaze_service.get_fhir_id("Patient", "nonexistentId")
        self.assertIsNone(non_existent_fhir_id)

    def test_get_identifier_by_fhir_id_existing(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        donor_identifier = self.blaze_service.get_identifier_by_fhir_id("Patient", donor_fhir_id)
        self.assertEqual(self.example_donor.identifier, donor_identifier)

    def test_get_identifier_by_fhir_id_non_existing(self):
        donor_identifier = self.blaze_service.get_identifier_by_fhir_id("Patient", "NonexistentId")
        self.assertIsNone(donor_identifier)

    def test_upload_donor(self):
        donor_id = self.blaze_service.upload_donor(self.example_donor)
        self.assertIsNotNone(donor_id)

    def test_donor_from_json(self):
        donor_id = self.blaze_service.upload_donor(self.example_donor)
        donor = self.blaze_service.build_donor_from_json(donor_id)
        self.assertEqual(donor.identifier, self.example_donor.identifier)
        self.assertEqual(donor.gender, self.example_donor.gender)
        self.assertEqual(donor.date_of_birth, self.example_donor.date_of_birth)
        self.assertEqual(donor.dataset_type, self.example_donor.dataset_type)
        self.assertEqual(donor.donor_fhir_id, donor_id)

    def test_update_donor(self):
        donor_id = self.blaze_service.upload_donor(self.example_donor)
        self.assertIsNotNone(donor_id)
        updated_donor = SampleDonor("new_donor_identifier", Gender.MALE, datetime.datetime(year=2022, month=10, day=20),
                                    "Other")
        updated_donor._donor_fhir_id = donor_id
        updated_donor_fhir = updated_donor.to_fhir()
        updated_donor_fhir = updated_donor.add_fhir_id_to_donor(updated_donor_fhir)
        updated_bool = self.blaze_service.update_fhir_resource("Patient", donor_id, updated_donor_fhir.as_json())
        self.assertTrue(updated_bool)
        updated_donor_resource = self.blaze_service.build_donor_from_json(donor_id)
        self.assertEqual(updated_donor.identifier, updated_donor_resource.identifier)
        self.blaze_service.delete_donor(donor_id)

    def test_delete_donor(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        deleted = self.blaze_service.delete_donor(donor_fhir_id)
        self.assertTrue(deleted)

    def test_upload_sample(self):
        # donor = SampleDonor("donorId", Gender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
        self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        sample_fhir_id2 = self.blaze_service.upload_sample(self.example_samples[1])
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Specimen", sample_fhir_id))
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Specimen", sample_fhir_id2))
        self.assertIsNotNone(sample_fhir_id)

    def test_build_sample_from_json(self):
        self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        build_sample = self.blaze_service.build_sample_from_json(sample_fhir_id)
        self.assertEqual(build_sample.identifier, self.example_samples[0].identifier)
        self.assertEqual(build_sample.donor_identifier, self.example_samples[0].donor_identifier)
        self.assertEqual(build_sample.sample_fhir_id, sample_fhir_id)
        self.assertEqual(build_sample.material_type, self.example_samples[0].material_type)
        self.assertEqual(build_sample.storage_temperature, self.example_samples[0].storage_temperature)
        self.assertEqual(build_sample.collected_datetime, self.example_samples[0].collected_datetime)

    def test_update_sample(self):
        self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        update_sample = self.blaze_service.build_sample_from_json(sample_fhir_id)
        update_sample.identifier = "new_sample_id"
        update_sample_fhir = update_sample.add_fhir_id_to_fhir_representation(update_sample.to_fhir())
        updated = self.blaze_service.update_fhir_resource("Specimen", sample_fhir_id, update_sample_fhir.as_json())
        updated_resource = self.blaze_service.build_sample_from_json(sample_fhir_id)
        self.assertTrue(updated)
        self.assertEqual(updated_resource.identifier, update_sample.identifier)
        self.blaze_service.delete_sample(sample_fhir_id)

    def test_delete_sample(self):
        self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        deleted = self.blaze_service.delete_sample(sample_fhir_id)
        self.assertFalse(self.blaze_service.is_resource_present_in_blaze("Specimen", "sampleId", "identifier"))
        self.assertTrue(deleted)

    def test_upload_observation(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        obs_fhir_id1 = self.blaze_service.upload_observation(self.example_observations[0])
        obs_fhir_id2 = self.blaze_service.upload_observation(self.example_observations[1])
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Observation", obs_fhir_id1))
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Observation", obs_fhir_id2))

    def test_build_observation_from_json(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        obs_fhir_id1 = self.blaze_service.upload_observation(self.example_observations[0])
        build_observation = self.blaze_service.build_observation_from_json(obs_fhir_id1)
        self.assertEqual(build_observation.observation_fhir_id, obs_fhir_id1)
        self.assertEqual(build_observation.sample_fhir_id, sample_fhir_id)
        self.assertEqual(build_observation.patient_fhir_id, donor_fhir_id)
        self.assertEqual(build_observation.diagnosis_observed_datetime,
                         self.example_observations[0].diagnosis_observed_datetime)
        self.assertEqual(build_observation.icd10_code, self.example_observations[0].icd10_code)

    def test_update_observation(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        obs_fhir_id1 = self.blaze_service.upload_observation(self.example_observations[0])
        update_observation = self.blaze_service.build_observation_from_json(obs_fhir_id1)
        update_observation.icd10_code = "C34"
        update_observation_fhir = update_observation.add_fhir_id_to_observation(update_observation.to_fhir())
        updated = self.blaze_service.update_fhir_resource("Observation", obs_fhir_id1,
                                                          update_observation_fhir.as_json())
        self.assertTrue(updated)
        updated_observation = self.blaze_service.build_observation_from_json(obs_fhir_id1)
        self.assertEqual(updated_observation.icd10_code, update_observation.icd10_code)
        self.blaze_service.delete_observation(obs_fhir_id1)

    def test_delete_observation(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        observation_fhir_id = self.blaze_service.upload_observation(self.example_observations[0])
        deleted = self.blaze_service.delete_observation(observation_fhir_id)
        self.assertTrue(deleted)
        self.assertFalse(self.blaze_service.is_resource_present_in_blaze("Observation", observation_fhir_id))

    def test_upload_diagnosis_report(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        self.assertIsNotNone(diagnosis_report_fhir_id)

    def test_build_diagnosis_report_from_json(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        build_diagnosis_report = self.blaze_service.build_diagnosis_report_from_json(diagnosis_report_fhir_id)
        self.assertEqual(build_diagnosis_report.sample_fhir_id, sample_fhir_id)
        self.assertEqual(build_diagnosis_report.patient_fhir_id, donor_fhir_id)

    def test_upload_diagnosis_report_along_with_observations(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        self.blaze_service.upload_sample(self.example_samples[1])
        self.blaze_service.upload_observation(self.example_observations[0])
        self.blaze_service.upload_observation(self.example_observations[1])
        self.blaze_service.upload_observation(self.example_observations[2])
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        diagnosis_report_fhir_id2 = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[1])
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("DiagnosticReport", diagnosis_report_fhir_id))
        self.assertIsNotNone(
            self.blaze_service.get_observation_fhir_ids_belonging_to_diagnosis_report(diagnosis_report_fhir_id))

    def test_build_diagnosis_report_along_with_observations_from_json(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        obs1_fhir_id = self.blaze_service.upload_observation(self.example_observations[0])
        obs2_fhir_id = self.blaze_service.upload_observation(self.example_observations[1])
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        build_diagnosis_report = self.blaze_service.build_diagnosis_report_from_json(diagnosis_report_fhir_id)
        self.assertEqual(build_diagnosis_report.sample_fhir_id, sample_fhir_id)
        self.assertEqual(build_diagnosis_report.patient_fhir_id, donor_fhir_id)
        self.assertIn(obs1_fhir_id, build_diagnosis_report.observations_fhir_identifiers)
        self.assertIn(obs2_fhir_id, build_diagnosis_report.observations_fhir_identifiers)

    def test_delete_diagnosis_report_without_observations(self):
        self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        deleted = self.blaze_service.delete_diagnosis_report(diagnosis_report_fhir_id)
        self.assertTrue(deleted)

    # def test_add_existing_observation_to_diagnosis_report(self):
    #     self.blaze_service.upload_
    def test_delete_diagnosis_report_with_observations(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        self.blaze_service.upload_observation(self.example_observations[0])
        self.blaze_service.upload_observation(self.example_observations[1])
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        deleted = self.blaze_service.delete_diagnosis_report(diagnosis_report_fhir_id)
        self.assertTrue(deleted)
        self.assertFalse(self.blaze_service.is_resource_present_in_blaze("DiagnosticReport", diagnosis_report_fhir_id))

    def test_delete_diagnosis_report_referenced_in_condition(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        self.blaze_service.upload_observation(self.example_observations[0])
        self.blaze_service.upload_observation(self.example_observations[1])
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        condition_fhir_id = self.blaze_service.upload_condition(self.example_condition)
        condition = self.blaze_service.build_condition_from_json(condition_fhir_id)
        self.assertIn(diagnosis_report_fhir_id, condition.diagnosis_report_fhir_ids)
        deleted = self.blaze_service.delete_diagnosis_report(diagnosis_report_fhir_id)
        self.assertTrue(deleted)
        condition_without_diagnosis_report = self.blaze_service.build_condition_from_json(condition_fhir_id)
        self.assertNotIn(diagnosis_report_fhir_id, condition_without_diagnosis_report.diagnosis_report_fhir_ids)

    def test_upload_condition(self):
        self.blaze_service.upload_donor(self.example_donor)
        condition_fhir_id = self.blaze_service.upload_condition(self.example_condition)
        self.assertIsNotNone(condition_fhir_id)

    def test_build_condition_from_json(self):
        donor_id = self.blaze_service.upload_donor(self.example_donor)
        condition_fhir_id = self.blaze_service.upload_condition(self.example_condition)
        self.assertIsNotNone(condition_fhir_id)
        build_condition = self.blaze_service.build_condition_from_json(condition_fhir_id)
        self.assertEqual(build_condition.condition_fhir_id, condition_fhir_id)
        self.assertEqual(build_condition.patient_fhir_id, donor_id)

    def test_update_condition(self):
        self.blaze_service.upload_donor(self.example_donor)
        condition_fhir_id = self.blaze_service.upload_condition(self.example_condition)
        self.assertIsNotNone(condition_fhir_id)
        update_condition = self.blaze_service.build_condition_from_json(condition_fhir_id)
        update_condition.icd_10_code = "C51"
        update_condition_fhir = update_condition.add_fhir_id_to_condition(update_condition.to_fhir())
        updated = self.blaze_service.update_fhir_resource("Condition", condition_fhir_id,
                                                          update_condition_fhir.as_json())
        self.assertTrue(updated)
        updated_condition = self.blaze_service.build_condition_from_json(condition_fhir_id)
        self.assertEqual(update_condition.icd_10_code, updated_condition.icd_10_code)
        self.blaze_service.delete_condition(condition_fhir_id)

    def test_delete_condition_with_no_diagnosis_reports(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        condition_fhir_id = self.blaze_service.upload_condition(self.example_condition)
        deleted = self.blaze_service.delete_condition(condition_fhir_id)
        self.assertTrue(deleted)
        self.assertFalse(self.blaze_service.is_resource_present_in_blaze("Condition", condition_fhir_id))

    def test_add_diagnosis_report_to_already_present_condition(self):
        self.blaze_service.upload_donor(self.example_donor)
        self.blaze_service.upload_sample(self.example_samples[0])
        # diagnosis_report_fhir_id = self.blaze_service.get_diagnosis_report_fhir_id_belonging_to_sample(sample_fhir_id)
        condition_fhir_id = self.blaze_service.upload_condition(self.example_condition)
        diagnosis_report_fhir_id = self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        dig_rep_added = self.blaze_service.add_diagnosis_reports_to_condition(condition_fhir_id,
                                                                              [diagnosis_report_fhir_id])
        self.assertTrue(dig_rep_added)

    def test_get_observation_fhir_ids_belonging_to_sample(self):
        self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id = self.blaze_service.upload_sample(self.example_samples[0])
        obs_fhir_id1 = self.blaze_service.upload_observation(self.example_observations[0])
        obs_fhir_id2 = self.blaze_service.upload_observation(self.example_observations[1])
        obs_fhir_ids = self.blaze_service.get_observation_fhir_ids_belonging_to_sample(sample_fhir_id)
        self.assertTrue(len(obs_fhir_ids) != 0)
        self.assertIn(obs_fhir_id1, obs_fhir_ids)
        self.assertIn(obs_fhir_id2, obs_fhir_ids)

    def test_upload_donor_and_sample_full_chain(self):
        donor_fhir_id = self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_ids = []
        for sample in self.example_samples:
            sample_fhir_ids.append(self.blaze_service.upload_sample(sample))
        observation_fhir_ids = []
        for observation in self.example_observations:
            observation_fhir_ids.append(self.blaze_service.upload_observation(observation))
        diagnosis_reports_fhir_ids = []
        for diagnosis_report in self.example_diagnosis_reports:
            diagnosis_reports_fhir_ids.append(self.blaze_service.upload_diagnosis_report(diagnosis_report))
        condition_fhir_id = self.blaze_service.upload_condition(self.example_condition)
        self.assertIsNotNone(donor_fhir_id)
        for sample_fhir_id in sample_fhir_ids:
            self.assertIsNotNone(sample_fhir_id)
        for observation_fhir_id in observation_fhir_ids:
            self.assertIsNotNone(observation_fhir_id)
        for diagnosis_report_fhir_id in diagnosis_reports_fhir_ids:
            self.assertIsNotNone(diagnosis_report_fhir_id)
        self.assertIsNotNone(condition_fhir_id)
        diag_report_for_first_sample = self.blaze_service.get_diagnosis_report_fhir_id_belonging_to_sample(
            sample_fhir_ids[0])
        diag_report_for_second_sample = self.blaze_service.get_diagnosis_report_fhir_id_belonging_to_sample(
            sample_fhir_ids[1])
        observations_for_first_sample = self.blaze_service.get_observation_fhir_ids_belonging_to_sample(
            sample_fhir_ids[0])
        observations_for_second_sample = self.blaze_service.get_observation_fhir_ids_belonging_to_sample(
            sample_fhir_ids[1])
        for obs_sample_1 in observations_for_first_sample:
            self.assertIn(obs_sample_1, observation_fhir_ids)
        for obs_sample_2 in observations_for_second_sample:
            self.assertIn(obs_sample_2, observation_fhir_ids)
        self.assertEqual(diag_report_for_first_sample, diagnosis_reports_fhir_ids[0])
        self.assertEqual(diag_report_for_second_sample, diagnosis_reports_fhir_ids[1])

    def test_get_identifier_by_fhir_id(self):
        fhir_id = "NonExistentId"
        identifier = self.blaze_service.get_identifier_by_fhir_id("Patient", fhir_id)

    def test_upload_biobank(self):
        biobank_fhir_id = self.blaze_service.upload_biobank(self.example_biobank)
        self.assertIsNotNone(biobank_fhir_id)
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Organization", biobank_fhir_id))

    def test_build_biobank_from_json(self):
        biobank_fhir_id = self.blaze_service.upload_biobank(self.example_biobank)
        biobank = self.blaze_service.build_biobank_from_json(biobank_fhir_id)
        self.assertEqual(biobank_fhir_id, biobank.biobank_fhir_id)
        self.assertEqual(self.example_biobank.identifier, biobank.identifier)
        self.assertEqual(self.example_biobank.name, biobank.name)
        self.assertEqual(self.example_biobank.contact_surname, biobank.contact_surname)
        self.assertEqual(self.example_biobank.country, biobank.country)
        self.assertEqual(self.example_biobank.contact_email, biobank.contact_email)
        self.assertEqual(self.example_biobank.juristic_person, biobank.juristic_person)
        self.assertEqual(self.example_biobank.contact_name, biobank.contact_name)
        self.assertEqual(self.example_biobank.alias, biobank.alias)
        self.assertEqual(self.example_biobank.description, biobank.description)
        self.assertEqual(self.example_biobank.organisational_capabilities, biobank.organisational_capabilities)

    def test_upload_collection_organization(self):
        self.blaze_service.upload_biobank(self.example_biobank)
        collection_organization_id = self.blaze_service.upload_collection_organization(self.example_collection_org)
        self.assertIsNotNone(collection_organization_id)
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Organization", collection_organization_id))

    def test_upload_collection(self):
        self.blaze_service.upload_biobank(self.example_biobank)
        self.blaze_service.upload_collection_organization(self.example_collection_org)
        collection_fhir_id = self.blaze_service.upload_collection(self.example_collection)
        self.assertIsNotNone(collection_fhir_id)
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Group", collection_fhir_id))

    def test_upload_network_organization(self):
        self.blaze_service.upload_biobank(self.example_biobank)
        network_org_fhir_id = self.blaze_service.upload_network_organization(self.example_network_org)
        self.assertIsNotNone(network_org_fhir_id)
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Organization", network_org_fhir_id))

    def test_upload_network(self):
        self.blaze_service.upload_biobank(self.example_biobank)
        self.blaze_service.upload_collection_organization(self.example_collection_org)
        self.blaze_service.upload_collection(self.example_collection)
        self.blaze_service.upload_network_organization(self.example_network_org)
        network_fhir_id = self.blaze_service.upload_network(self.example_network)
        self.assertIsNotNone(network_fhir_id)
        self.assertTrue(self.blaze_service.is_resource_present_in_blaze("Group", network_fhir_id))

    def test_delete_biobank(self):
        biobank_fhir_id = self.blaze_service.get_fhir_id("Organization", self.example_biobank.identifier)
        if biobank_fhir_id is not None:
            deleted = self.blaze_service.delete_biobank(biobank_fhir_id)
            self.assertTrue(deleted)

    def test_add_existing_sample_to_collection(self):
        self.blaze_service.upload_donor(self.example_donor)
        sample_fhir_id1 = self.blaze_service.upload_sample(self.example_samples[0])
        sample_fhir_id2 = self.blaze_service.upload_sample(self.example_samples[1])
        self.blaze_service.upload_observation(self.example_observations[0])
        self.blaze_service.upload_observation(self.example_observations[1])
        self.blaze_service.upload_diagnosis_report(self.example_diagnosis_reports[0])
        self.blaze_service.upload_biobank(self.example_biobank)
        self.blaze_service.upload_collection_organization(self.example_collection_org)
        collection_fhir_id = self.blaze_service.upload_collection(self.example_collection)
        # sample_fhir_id = self.blaze_service.get_fhir_id("Specimen", "sampleId")
        # sample_json = self.blaze_service.get_fhir_resource_as_json("Specimen", sample_fhir_id)
        # sample = Sample.from_json(sample_json, "donorId")
        updated = self.blaze_service.add_already_present_samples_to_existing_collection(
            [sample_fhir_id1, sample_fhir_id2], collection_fhir_id)
        self.assertTrue(updated)
        updated_collection = self.blaze_service.build_collection_from_json(collection_fhir_id)
        self.assertEqual(updated_collection.number_of_subjects, 1)
        self.assertIn(sample_fhir_id1, updated_collection.sample_fhir_ids)
        self.assertIn(sample_fhir_id2, updated_collection.sample_fhir_ids)
        self.assertIn(self.example_samples[0].storage_temperature, updated_collection.storage_temperatures)
        self.assertIn(self.example_samples[1].storage_temperature, updated_collection.storage_temperatures)
        self.assertIn(self.example_donor.gender, updated_collection.genders)
