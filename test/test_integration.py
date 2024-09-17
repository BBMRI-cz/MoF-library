import datetime
import unittest
import time

import requests

from MIABIS_on_FHIR.MoF_biobank import Biobank
from MIABIS_on_FHIR.MoF_collection import MoFCollection
from MIABIS_on_FHIR.MoF_collection_organization import CollectionOrganization
from MIABIS_on_FHIR.MoF_condition import Condition
from MIABIS_on_FHIR.MoF_diagnosis_report import DiagnosisReport
from MIABIS_on_FHIR.MoF_network import Network
from MIABIS_on_FHIR.MoF_network_members import MoFNetworkMembers
from MIABIS_on_FHIR.MoF_network_organization import NetworkOrganization
from MIABIS_on_FHIR.MoF_observation import Observation
from MIABIS_on_FHIR.MoF_sample import Sample
from MIABIS_on_FHIR.MoF_sample_donor import SampleDonor
from MIABIS_on_FHIR.MoF_sample_list import SampleList
from MIABIS_on_FHIR.gender import Gender
from MIABIS_on_FHIR.storage_temperature import StorageTemperature

blaze_url = "http://localhost:8080/fhir"


class TestBlazeStore(unittest.TestCase):
    """Note: this is meant to be run with the blaze server running locally. Blaze server can be started with the command
    docker run --name blaze --rm -d -e JAVA_TOOL_OPTIONS=-Xmx2g -p 8080:8080 samply/blaze:latest. these tests should run
    in the specified order, as they depend on each other."""

    def test_upload_donor(self):
        donor = SampleDonor("donorId", Gender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
        donor_json = donor.to_fhir().as_json()
        resp = requests.post(blaze_url + "/Patient", json=donor_json)
        self.assertEqual(resp.status_code, 201)
        get_response_json = requests.get(blaze_url + "/Patient" + f"?identifier={donor.identifier}").json()
        time.sleep(0.1)
        # id = get_response_json["id"]
        # del_resp = requests.delete(blaze_url + "/Patient/" + id)
        # self.assertEqual(del_resp.status_code, 204)

    def test_upload_sample(self):
        get_response_json = requests.get(blaze_url + "/Patient?identifier=donorId").json()
        donor_fhir_id = get_response_json["entry"][0]["resource"]["id"]
        sample = Sample("sampleId", "donorId", "DNA", datetime.datetime(year=2022, month=10, day=20),
                        body_site="Arm", body_site_system="bsSystem",
                        storage_temperature=StorageTemperature.TEMPERATURE_ROOM, use_restrictions="use_restric")
        sample_json = sample.to_fhir(donor_fhir_id).as_json()
        resp = requests.post(blaze_url + "/Specimen", json=sample_json)
        self.assertEqual(resp.status_code, 201)
        time.sleep(0.1)

    def test_upload_full_condition_chain(self):
        sample_fhir_id = requests.get(blaze_url + "/Specimen" + f"?identifier=sampleId").json()["entry"][0]["resource"][
            "id"]
        donor_fhir_id = requests.get(blaze_url + "/Patient" + f"?identifier=donorId").json()["entry"][0]["resource"][
            "id"]
        observation = Observation("C51", "sampleId")
        diagnosis_report = DiagnosisReport("sampleId", ["sampleId"])
        observation_json = observation.to_fhir().as_json()
        observation_response = requests.post(blaze_url + "/Observation", json=observation_json)
        self.assertEqual(observation_response.status_code, 201)
        observation_fhir_id = observation_response.json()["id"]
        diagnosis_report_json = diagnosis_report.to_fhir(sample_fhir_id, [observation_fhir_id]).as_json()
        diagnosis_report_response = requests.post(blaze_url + "/DiagnosticReport", json=diagnosis_report_json)
        diagnosis_report_fhir_id = diagnosis_report_response.json()["id"]
        self.assertEqual(diagnosis_report_response.status_code, 201)
        condition = Condition("donorId")
        condition_json = condition.to_fhir(donor_fhir_id, [diagnosis_report_fhir_id]).as_json()
        condition_response = requests.post(blaze_url + "/Condition", json=condition_json)
        self.assertEqual(condition_response.status_code, 201)
        time.sleep(0.1)

    def test_upload_biobank(self):
        biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "Jozef", "Mrkva", "jozefmrkva@email.com",
                          infrastructural_capabilities=["SampleStorage"], organisational_capabilities=["Other"],
                          bioprocessing_and_analysis_capabilities=["Other"])
        biobank_json = biobank.to_fhir().as_json()
        resp = requests.post(blaze_url + "/Organization", json=biobank_json)
        self.assertEqual(resp.status_code, 201)
        time.sleep(0.1)

    def test_upload_collection_organization(self):
        biobank_fhir_id = \
            requests.get(blaze_url + "/Organization" + f"?identifier=biobankId").json()["entry"][0]["resource"]["id"]
        collection_org = CollectionOrganization("collectionId", "collectionName", "biobankId", "Jozef", "Mrkva",
                                                   "jozefmrkva@email.com", "cz", "collectionAlias", "url",
                                                   "description", dataset_type="Other", sample_source="Human",
                                                sample_collection_setting="Other",
                                                collection_design=["Other"],
                                                use_and_access_conditions=["CommercialUse"],
                                                publications=["publication"])
        collection_org_json = collection_org.to_fhir(biobank_fhir_id).as_json()
        resp = requests.post(blaze_url + "/Organization", json=collection_org_json)
        self.assertEqual(resp.status_code, 201)

    def test_upload_collection(self):
        biobank_fhir_id = \
            requests.get(blaze_url + "/Organization" + f"?identifier=collectionId").json()["entry"][0]["resource"]["id"]
        sample_fhir_id = requests.get(blaze_url + "/Specimen" + f"?identifier=sampleId").json()["entry"][0]["resource"][
            "id"]
        collection = MoFCollection("collectionId", "collectionName", "biobankId", 0, 100,
                                   [Gender.MALE, Gender.FEMALE],
                                   [StorageTemperature.TEMPERATURE_GN, StorageTemperature.TEMPERATURE_ROOM],
                                   ["Urine"], ["C50", "C51"], 2, inclusion_criteria=["HealthStatus"],
                                   sample_ids=["sampleId"])
        collection_json = collection.to_fhir(biobank_fhir_id, [sample_fhir_id]).as_json()
        resp = requests.post(blaze_url + "/Group", json=collection_json)
        self.assertEqual(resp.status_code, 201)
        time.sleep(0.1)

    def test_upload_sample_list(self):
        collection_fhir_id = requests.get(blaze_url + "/Group?identifier=collectionId").json()["entry"][0]["resource"][
            "id"]
        sample_fhir_id = requests.get(blaze_url + "/Specimen?identifier=sampleId").json()["entry"][0]["resource"]["id"]
        sample_list = SampleList("collectionId", ["sampleId"])
        sample_list_json = sample_list.to_fhir(collection_fhir_id, [sample_fhir_id]).as_json()
        resp = requests.post(blaze_url + "/List", json=sample_list_json)
        self.assertEqual(resp.status_code, 201)

    def test_upload_network_organization(self):
        biobank_fhir_id = \
            requests.get(blaze_url + "/Organization" + f"?identifier=collectionId").json()["entry"][0]["resource"]["id"]

        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                             "contactSurname", "contactEmail", "country", ["Charter"], "juristicPerson")
        network_org_fhir = network_org.to_fhir(biobank_fhir_id).as_json()
        resp = requests.post(blaze_url + "/Organization", json=network_org_fhir)
        self.assertEqual(resp.status_code, 201)

    def test_upload_network(self):
        biobank_fhir_id = \
            requests.get(blaze_url + "/Organization" + f"?identifier=biobankId").json()["entry"][0]["resource"]["id"]
        collection_fhir_id = \
            requests.get(blaze_url + "/Group" + f"?identifier=collectionId").json()["entry"][0]["resource"]["id"]
        network_org_fhir_id = \
            requests.get(blaze_url + "/Organization" + f"?identifier=networkOrgId").json()["entry"][0]["resource"]["id"]
        network = Network("networkId", "networkName", "networkOrgId", ["collectionId"], ["biobankId"])
        network_json = network.to_fhir(network_org_fhir_id, [collection_fhir_id], [biobank_fhir_id]).as_json()
        resp = requests.post(blaze_url + "/Group", json=network_json)
        self.assertEqual(resp.status_code, 201)
        time.sleep(0.1)

    def test_network_members(self):
        network_fhir_id = requests.get(blaze_url + "/Group?identifier=networkId").json()["entry"][0]["resource"]["id"]
        biobank_fhir_id = requests.get(blaze_url + "/Organization?identifier=biobankId").json()["entry"][0]["resource"][
            "id"]
        collection_fhir_id = requests.get(blaze_url + "/Group?identifier=collectionId").json()["entry"][0]["resource"][
            "id"]
        network_members = MoFNetworkMembers("networkId", "networkmembers", ["collectionId", "biobankId"])
        network_members_json = network_members.to_fhir(network_fhir_id, [collection_fhir_id],
                                                       [biobank_fhir_id]).as_json()
        resp = requests.post(blaze_url + "/List", json=network_members_json)
        self.assertEqual(resp.status_code, 201)
