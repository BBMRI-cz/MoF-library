import datetime
import unittest

import requests

from MIABIS_on_FHIR.MoF_biobank import MoFBiobank
from MIABIS_on_FHIR.MoF_collection import MoFCollection
from MIABIS_on_FHIR.MoF_condition import MoFCondition
from MIABIS_on_FHIR.MoF_diagnosis_report import MoFDiagnosisReport
from MIABIS_on_FHIR.MoF_network import MoFNetwork
from MIABIS_on_FHIR.MoF_network_members import MoFNetworkMembers
from MIABIS_on_FHIR.MoF_observation import MoFObservation
from MIABIS_on_FHIR.MoF_sample import MoFSample
from MIABIS_on_FHIR.MoF_sample_donor import MoFSampleDonor
from MIABIS_on_FHIR.MoF_sample_list import MoFSampleList
from MIABIS_on_FHIR.gender import MoFGender
from MIABIS_on_FHIR.storage_temperature import MoFStorageTemperature

blaze_url = "http://localhost:8080/fhir"


class TestBlazeStore(unittest.TestCase):
    """Note: this is meant to be run with the blaze server running locally. Blaze server can be started with the command
    docker run --name blaze --rm -d -e JAVA_TOOL_OPTIONS=-Xmx2g -p 8080:8080 samply/blaze:latest. these tests should run
    in the specified order, as they depend on each other."""

    def test_upload_donor(self):
        donor = MoFSampleDonor("donorId", MoFGender.MALE, datetime.datetime(year=2022, month=10, day=20), "Other")
        donor_json = donor.to_fhir().as_json()
        resp = requests.post(blaze_url + "/Patient", json=donor_json)
        self.assertEqual(resp.status_code, 201)
        get_response_json = requests.get(blaze_url + "/Patient" + f"?identifier={donor.identifier}").json()
        # id = get_response_json["id"]
        # del_resp = requests.delete(blaze_url + "/Patient/" + id)
        # self.assertEqual(del_resp.status_code, 204)

    def test_upload_sample(self):
        get_response_json = requests.get(blaze_url + "/Patient?identifier=donorId").json()
        donor_fhir_id = get_response_json["entry"][0]["resource"]["id"]
        sample = MoFSample("sampleId2", "donorId", "DNA", datetime.datetime(year=2022, month=10, day=20),
                           body_site="Arm", body_site_system="bsSystem",
                           storage_temperature=MoFStorageTemperature.TEMPERATURE_ROOM,use_restrictions="use_restric")
        sample_json = sample.to_fhir(donor_fhir_id).as_json()
        resp = requests.post(blaze_url + "/Specimen", json=sample_json)
        self.assertEqual(resp.status_code, 201)

    def test_upload_full_condition_chain(self):
        sample_fhir_id = requests.get(blaze_url + "/Specimen" + f"?identifier=sampleId").json()["entry"][0]["resource"][
            "id"]
        donor_fhir_id = requests.get(blaze_url + "/Patient" + f"?identifier=donorId").json()["entry"][0]["resource"][
            "id"]
        observation = MoFObservation("C51", "sampleId")
        diagnosis_report = MoFDiagnosisReport("sampleId", ["sampleId"])
        observation_json = observation.to_fhir().as_json()
        observation_response = requests.post(blaze_url + "/Observation", json=observation_json)
        self.assertEqual(observation_response.status_code, 201)
        observation_fhir_id = observation_response.json()["id"]
        diagnosis_report_json = diagnosis_report.to_fhir(sample_fhir_id, [observation_fhir_id]).as_json()
        diagnosis_report_response = requests.post(blaze_url + "/DiagnosticReport", json=diagnosis_report_json)
        diagnosis_report_fhir_id = diagnosis_report_response.json()["id"]
        self.assertEqual(diagnosis_report_response.status_code, 201)
        condition = MoFCondition("donorId")
        condition_json = condition.to_fhir(donor_fhir_id, [diagnosis_report_fhir_id]).as_json()
        condition_response = requests.post(blaze_url + "/Condition", json=condition_json)
        self.assertEqual(condition_response.status_code, 201)

    def test_upload_biobank(self):
        biobank = MoFBiobank("biobankId", "biobankName", "biobankAlias", "CZ", "Jozef", "Mrkva", "jozefmrkva@email.com",
                             infrastructural_capabilities=["SampleStorage"], organisational_capabilities=["Other"],
                             bioprocessing_and_analysis_capabilities=["Other"])
        biobank_json = biobank.to_fhir().as_json()
        resp = requests.post(blaze_url + "/Organization", json=biobank_json)
        self.assertEqual(resp.status_code, 201)

    def test_upload_collection(self):
        biobank_fhir_id = \
            requests.get(blaze_url + "/Organization" + f"?identifier=biobankId").json()["entry"][0]["resource"]["id"]
        collection = MoFCollection("collectionId", "collectionName", "collectionAlias", "biobankId", 0, 0,
                                   [MoFGender.MALE], [MoFStorageTemperature.TEMPERATURE_LN], ["DNA"], diagnoses=["C51"],
                                   dataset_type="Other", sample_source="Human", sample_collection_setting="Other",
                                   collection_design=["Other"], use_and_access_conditions=["CommercialUse"],
                                   number_of_subjects=10, inclusion_criteria=["Sex"])
        collection_json = collection.to_fhir(biobank_fhir_id).as_json()
        resp = requests.post(blaze_url + "/Group", json=collection_json)
        self.assertEqual(resp.status_code, 201)

    def test_upload_sample_list(self):
        collection_fhir_id = requests.get(blaze_url + "/Group?identifier=collectionId").json()["entry"][0]["resource"][
            "id"]
        sample_fhir_id = requests.get(blaze_url + "/Specimen?identifier=sampleId").json()["entry"][0]["resource"]["id"]
        sample_list = MoFSampleList("collectionId", ["sampleId"])
        sample_list_json = sample_list.to_fhir(collection_fhir_id, [sample_fhir_id]).as_json()
        resp = requests.post(blaze_url + "/List", json=sample_list_json)
        self.assertEqual(resp.status_code, 201)

    def test_upload_network(self):
        network = MoFNetwork("networkId", "networkName", ["SOP"])
        network_json = network.to_fhir().as_json()
        resp = requests.post(blaze_url + "/Group", json=network_json)
        self.assertEqual(resp.status_code, 201)

    def test_network_members(self):
        network_fhir_id = requests.get(blaze_url + "/Group?identifier=networkId").json()["entry"][0]["resource"]["id"]
        biobank_fhir_id = requests.get(blaze_url + "/Organization?identifier=biobankId").json()["entry"][0]["resource"][
            "id"]
        collection_fhir_id = requests.get(blaze_url + "/Group?identifier=collectionId").json()["entry"][0]["resource"][
            "id"]
        network_members = MoFNetworkMembers("networkId", "networkmemb", ["collectionId", "biobankId"])
        network_members_json = network_members.to_fhir(network_fhir_id, [collection_fhir_id],
                                                       [biobank_fhir_id]).as_json()
        resp = requests.post(blaze_url + "/List", json=network_members_json)
        self.assertEqual(resp.status_code, 201)
