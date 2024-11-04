from typing import Generator, Any

import requests
from fhirclient.models.bundle import Bundle, BundleEntry, BundleEntryRequest
from requests import Response
from requests.adapters import HTTPAdapter, Retry

from miabis_model.biobank import Biobank
from miabis_model.collection import Collection
from miabis_model.collection_organization import CollectionOrganization
from miabis_model.condition import Condition
from miabis_model.diagnosis_report import DiagnosisReport
from miabis_model.network import Network
from miabis_model.network_organization import NetworkOrganization
from miabis_model.observation import Observation
from miabis_model.sample import Sample
from miabis_model.sample_donor import SampleDonor
from miabis_model.util.parsing_util import get_nested_value, parse_reference_id, \
    get_material_type_from_detailed_material_type
from blaze_client.NonExistentResourceException import NonExistentResourceException


class BlazeClient:
    """Class for handling communication with a blaze server,
    be it for CRUD operations, creating objects from json, etc."""

    def __init__(self, blaze_url: str, blaze_username: str, blaze_password: str):
        """
        :param blaze_url: url of the blaze server
        :param blaze_username: blaze username
        :param blaze_password: blaze password
        """
        self._blaze_url = blaze_url
        self._blaze_username = blaze_username
        self._blaze_password = blaze_password
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=retries))
        header = {"Prefer": "handling=strict"}
        session.headers.update(header)
        session.auth = (blaze_username, blaze_password)
        self._session = session

    def is_resource_present_in_blaze(self, resource_type: str, search_value: str, search_param: str = None) -> bool:
        """Check if a resource is present in the blaze.
        The search parameter needs to confront to the searchable parameters defined by FHIR for each resource.
        if search_param is None, this method checks the existence of resource by FHIR id.
        :param resource_type: type of the resource
        :param search_param: parameter by which the resource is searched
        :param search_value: actual value by which the search is done
        :return True if the resource is present, false otherwise
        :raises HTTPError: if the request to blaze fails"""
        if search_param is None:
            response = self._session.get(f"{self._blaze_url}/{resource_type}/{search_value}")
            if response.status_code < 200 or response.status_code > 200:
                return False
            if response.status_code == 200:
                return True
        response = self._session.get(f"{self._blaze_url}/{resource_type}?{search_param}={search_value}")
        self.__raise_for_status_extract_diagnostics_message(response)
        if response.json()["total"] == 0:
            return False
        return True

    def get_fhir_resource_as_json(self, resource_type: str, resource_fhir_id: str) -> dict | None:
        """Get a FHIR resource from blaze as a json.
        :param resource_type: the type of the resource
        :param resource_fhir_id: the fhir id of the resource
        :return: json representation of the resource, or None if such resource is not present.
        :raises HTTPError: if the request to blaze fails
        """
        response = self._session.get(f"{self._blaze_url}/{resource_type}/{resource_fhir_id}")
        if response.status_code == 404:
            return None
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()

    def get_fhir_id(self, resource_type: str, resource_identifier: str) -> str | None:
        """get the fhir id of a resource in blaze.
            :param resource_type: the type of the resource
            :param resource_identifier: the identifier of the resource (usually given by the organization)
            :return: the fhir id of the resource in blaze, or None if the resource was not found
            :raises HTTPError: if the request to blaze fails
            """
        response = self._session.get(f"{self._blaze_url}/{resource_type.capitalize()}?identifier={resource_identifier}")
        self.__raise_for_status_extract_diagnostics_message(response)
        response_json = response.json()
        if response_json["total"] == 0:
            return None
        return get_nested_value(response_json, ["entry", 0, "resource", "id"])

    def get_identifier_by_fhir_id(self, resource_type: str, resource_fhir_id: str) -> str | None:
        """get the identifier of a resource in blaze.
            :param resource_type: the type of the resource
            :param resource_fhir_id: the fhir id of the resource
            :return: the identifier of the resource in blaze, None if resource with resource_fhir_id does not exists
            :raises HTTPError: if the request to blaze fails
            """
        response = self._session.get(f"{self._blaze_url}/{resource_type}/{resource_fhir_id}")
        if response.status_code == 404:
            return None
        self.__raise_for_status_extract_diagnostics_message(response)
        response_json = response.json()
        return get_nested_value(response_json, ["identifier", 0, "value"])

    def get_observation_fhir_ids_belonging_to_sample(self, sample_fhir_id: str) -> list[str]:
        """get all observations linked to a specific sample
        :param sample_fhir_id: fhir id of a sample for which the observations should be retrieved
        :return list of fhir ids linked to a specific sample
        :raises HTTPError: if the request to blaze fails"""
        response = self._session.get(f"{self._blaze_url}/Observation?specimen={sample_fhir_id}")
        self.__raise_for_status_extract_diagnostics_message(response)
        observations_fhir_ids = []
        response_json = response.json()
        if response_json["total"] == 0:
            return observations_fhir_ids
        for entry in response_json["entry"]:
            obs_fhir_id = get_nested_value(entry, ["resource", "id"])
            if obs_fhir_id is not None:
                observations_fhir_ids.append(obs_fhir_id)
        return observations_fhir_ids

    def get_diagnosis_report_fhir_id_belonging_to_sample(self, sample_fhir_id: str) -> str | None:
        """get diagnosis report which belongs to a specific sample
        :param sample_fhir_id: fhir id of sample that this diagnosis report belongs to
        :return fhir id of the diagnosis report
        :raises HTTPError: if the request to blaze fails"""
        response = self._session.get(f"{self._blaze_url}/DiagnosticReport?specimen={sample_fhir_id}")
        self.__raise_for_status_extract_diagnostics_message(response)
        diagnosis_report_json = response.json()
        return get_nested_value(diagnosis_report_json, ["entry", 0, "resource", "id"])

    def get_diagnosis_report_fhir_ids_belonging_to_patient(self, donor_fhir_id: str) -> list[str]:
        """get diagnosis reports fhir ids, which belong to a specific donor
        :param donor_fhir_id: fhir id of donor that these diagnosis reports belong to
        :return list of  diagnosis fhir ids belonging to a specified donor
        :raises HTTPError: if the request to blaze fails"""
        diagnosis_report_fhir_ids = []
        response = self._session.get(f"{self._blaze_url}/DiagnosticReport?subject={donor_fhir_id}")
        self.__raise_for_status_extract_diagnostics_message(response)
        diagnosis_reports_json = response.json()
        if diagnosis_reports_json["total"] == 0:
            return diagnosis_report_fhir_ids
        for entry in diagnosis_reports_json.get("entry", []):
            diagnosis_report_fhir_id = get_nested_value(entry, ["resource", "id"])
            diagnosis_report_fhir_ids.append(diagnosis_report_fhir_id)
        return diagnosis_report_fhir_ids

    def get_condition_by_patient_fhir_id(self, patient_fhir_id: str):
        response = self._session.get(f"{self._blaze_url}/Condition?subject={patient_fhir_id}")
        self.__raise_for_status_extract_diagnostics_message(response)
        response_json = response.json()
        if response_json["total"] == 0:
            return None
        return get_nested_value(response_json, ["entry", 0, "resource", "id"])

    def update_fhir_resource(self, resource_type: str, resource_fhir_id: str, resource_json: dict) -> bool:
        """Update a FHIR resource in blaze.
        :param resource_type: the type of the resource
        :param resource_fhir_id: the fhir id of the resource
        :param resource_json: the json representation of the resource
        :return: True if the resource was updated successfully
        :raises NonExistentResourceException: if the resource cannot be found
        :raises HTTPError: if the request to blaze fails
        """
        response = self._session.put(f"{self._blaze_url}/{resource_type}/{resource_fhir_id}", json=resource_json)
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 201

    def upload_donor(self, donor: SampleDonor) -> str:
        """Upload a donor to blaze.
            :param donor: the donor to upload
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded donor
            :raises HTTPError: if the request to blaze fails
            """
        response = self._session.post(f"{self._blaze_url}/Patient", json=donor.to_fhir().as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_sample(self, sample: Sample) -> str:
        """Upload a sample to blaze.
            :param sample: the sample to upload
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded sample
            :raises HTTPError: if the request to blaze fails
            """
        donor_fhir_id = sample.subject_fhir_id or self.get_fhir_id("Patient", sample.donor_identifier)
        if donor_fhir_id is None:
            raise NonExistentResourceException(
                f"Cannot upload sample. Donor with (organizational) "
                f"identifier: {sample.donor_identifier} is not present in the blaze store.")
        response = self._session.post(f"{self._blaze_url}/Specimen", json=sample.to_fhir(donor_fhir_id).as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_observation(self, observation: Observation) -> str:
        """Upload an observation to blaze.
            :param observation: the observation to upload
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded observation
            """
        patient_fhir_id = observation.patient_fhir_id or self.get_fhir_id("Patient", observation.patient_identifier)
        sample_fhir_id = observation.sample_fhir_id or self.get_fhir_id("Specimen", observation.sample_identifier)
        if patient_fhir_id is None:
            raise NonExistentResourceException(f"Cannot upload observation. Donor with (organizational) identifier: "
                                               f"{observation.patient_identifier} is not present in the blaze store.")
        if sample_fhir_id is None:
            raise NonExistentResourceException(f"Cannot upload observation. Sample with (organizational) identifier: "
                                               f"{observation.sample_identifier} is not present in the blaze store.")
        response = self._session.post(f"{self._blaze_url}/Observation",
                                      json=observation.to_fhir(patient_fhir_id, sample_fhir_id).as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_diagnosis_report(self, diagnosis_report: DiagnosisReport) -> str:
        """Upload a diagnosis report to blaze.
            :param diagnosis_report: the diagnosis report to upload
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded diagnosis report
            """
        sample_fhir_id = diagnosis_report.sample_fhir_id or self.get_fhir_id("Specimen",
                                                                             diagnosis_report.sample_identifier)
        patient_fhir_id = diagnosis_report.patient_fhir_id or self.get_fhir_id("Patient",
                                                                               diagnosis_report.patient_identifier)
        observation_fhir_ids = diagnosis_report.observations_fhir_identifiers or \
                               self.get_observation_fhir_ids_belonging_to_sample(sample_fhir_id)
        if sample_fhir_id is None:
            raise NonExistentResourceException(
                f"Cannot upload diagnosis report. Sample with (organizational) identifier: "
                f"{diagnosis_report.sample_identifier} is not present in the blaze store.")
        if patient_fhir_id is None:
            raise NonExistentResourceException(
                f"Cannot upload diagnosis report. Donor with (organizational) identifier: "
                f"{diagnosis_report.patient_identifier} is not present in the blaze store.")
        diagnosis_report_json = diagnosis_report.to_fhir(sample_fhir_id, patient_fhir_id,
                                                         observation_fhir_ids).as_json()
        response = self._session.post(f"{self._blaze_url}/DiagnosticReport", json=diagnosis_report_json)
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_condition(self, condition: Condition) -> str:
        """Upload a condition to blaze.
            :param condition: the condition to upload
            :raises HTTPError: if the request to blaze fails
            :raises NonExistentResourceException: if the resource cannot be found
            :return: the fhir id of the uploaded condition
            """
        donor_fhir_id = condition.patient_fhir_id or self.get_fhir_id("Patient", condition.patient_identifier)
        diagnosis_reports_fhir_ids = \
            condition.diagnosis_report_fhir_ids or self.get_diagnosis_report_fhir_ids_belonging_to_patient(
                donor_fhir_id)
        if donor_fhir_id is None:
            raise NonExistentResourceException(
                f"Cannot upload Condition. Donor with (organizational) identifier: "
                f"{condition.patient_identifier} is not present in the blaze store.")
        condition_json = condition.to_fhir(donor_fhir_id, diagnosis_reports_fhir_ids).as_json()
        response = self._session.post(f"{self._blaze_url}/Condition", json=condition_json)
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_biobank(self, biobank: Biobank) -> str:
        """Upload a biobank to blaze.
        :param biobank: the biobank to upload
        :raises HTTPError: if the request to blaze fails
        :return: the fhir id of the uploaded biobank"""

        biobank_json = biobank.to_fhir().as_json()
        response = self._session.post(f"{self._blaze_url}/Organization", json=biobank_json)
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_collection_organization(self, collection_org: CollectionOrganization) -> str:
        """
        Upload a collection organization resource to a blaze
        :param collection_org: collection organization resource to upload
        :raises: HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return: the fhir id of the uploaded collection organization"""

        managing_biobank_fhir_id = collection_org.managing_biobank_fhir_id or \
                                   self.get_fhir_id("Organization", collection_org.managing_biobank_id)
        if managing_biobank_fhir_id is None:
            raise NonExistentResourceException(
                f"Cannot upload Collection Organization. Biobank with (organizational) identifier: "
                f"{collection_org.managing_biobank_fhir_id} is not present in the blaze store.")
        collection_org_json = collection_org.to_fhir(managing_biobank_fhir_id).as_json()
        response = self._session.post(f"{self._blaze_url}/Organization", json=collection_org_json)
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_collection(self, collection: Collection) -> str:
        """
        Upload a collection resource to blaze.
        :param collection: collection resource to upload
        :raises: HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return: the fhir id of the uploaded collection
        """

        managing_collection_org_fhir_id = collection.managing_collection_org_fhir_id \
                                          or self.get_fhir_id("Organization", collection.managing_collection_org_id)
        sample_fhir_ids = collection.sample_fhir_ids
        if managing_collection_org_fhir_id is None:
            raise NonExistentResourceException(
                f"Cannot upload Collection. Collection Organization with (organizational) identifier: "
                f"{collection.managing_collection_org_fhir_id} is not present in the blaze store.")
        if sample_fhir_ids is None:
            sample_fhir_ids = []
            if collection.sample_ids is not None:
                for sample_id in collection.sample_ids:
                    sample_fhir_id = self.get_fhir_id("Specimen", sample_id)
                    if sample_fhir_id is None:
                        raise NonExistentResourceException(
                            f"Cannot upload Collection. Sample with (organizational) identifier: "
                            f"{sample_id} is not present in the blaze store.")
                    sample_fhir_ids.append(sample_fhir_id)

        collection_json = collection.to_fhir(managing_collection_org_fhir_id, sample_fhir_ids).as_json()
        response = self._session.post(f"{self._blaze_url}/Group", json=collection_json)
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_network_organization(self, network_org: NetworkOrganization) -> str:
        """
        Upload a network organization resource to blaze.
        :param network_org: network organization resource to upload
        :raises: HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return: the fhir id of uploaded network organization
        """
        managing_biobank_fhir_id = network_org.managing_biobank_fhir_id \
                                   or self.get_fhir_id("Organization", network_org.managing_biobank_id)
        if managing_biobank_fhir_id is None:
            raise NonExistentResourceException(
                f"Cannot upload Network Organization. Biobank with (organizational) identifier: "
                f"{network_org.managing_biobank_fhir_id} is not present in the blaze store.")
        network_org_json = network_org.to_fhir(managing_biobank_fhir_id).as_json()
        response = self._session.post(f"{self._blaze_url}/Organization", json=network_org_json)
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def upload_network(self, network: Network) -> str:
        """
        Upload a network resource to blaze.
        :param network: network resource to upload
        :raises NonExistentResourceException: if the resource cannot be found
        :raises: HTTPError: if the request to blaze fails
        :return: the fhir id of uploaded network
        """

        managing_network_org_fhir_id = network.managing_network_org_fhir_id or \
                                       self.get_fhir_id("Organization", network.managing_network_org_id)
        if managing_network_org_fhir_id is None:
            raise NonExistentResourceException(
                f"Cannot upload Network. Network Organization with (organizational) identifier: "
                f"{network.managing_network_org_fhir_id} is not present in the blaze store.")
        biobank_members_fhir_ids = network.members_biobanks_fhir_ids
        collection_members_fhir_ids = network.members_collections_fhir_ids
        biobank_ids = network.members_biobanks_ids or []
        if biobank_members_fhir_ids is None:
            biobank_members_fhir_ids = []
            for biobank_member_id in biobank_ids:
                member_fhir_id = self.get_fhir_id("Organization", biobank_member_id)
                if member_fhir_id is None:
                    raise NonExistentResourceException(
                        f"Cannot upload Network. Biobank with (organizational) identifier: "
                        f"{member_fhir_id} is not present in the blaze store.")
                biobank_members_fhir_ids.append(member_fhir_id)
        collection_ids = network.members_collections_ids or []
        if collection_members_fhir_ids is None:
            collection_members_fhir_ids = []
            for collection_member_id in collection_ids:
                member_fhir_id = self.get_fhir_id("Group", collection_member_id)
                if member_fhir_id is None:
                    raise NonExistentResourceException(
                        f"Cannot upload Network. Collection with (organizational) identifier: "
                        f"{member_fhir_id} is not present in the blaze store.")
                collection_members_fhir_ids.append(member_fhir_id)

        network_org_json = network.to_fhir(managing_network_org_fhir_id, collection_members_fhir_ids,
                                           biobank_members_fhir_ids).as_json()
        response = self._session.post(f"{self._blaze_url}/Group", json=network_org_json)
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.json()["id"]

    def build_donor_from_json(self, donor_fhir_id: str) -> SampleDonor:
        """Build Donor Object from json representation
        :param donor_fhir_id: FHIR ID of the Patient resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return SampleDonor Object"""
        if not self.is_resource_present_in_blaze("Patient", donor_fhir_id):
            raise NonExistentResourceException(f"Patient with fhir id {donor_fhir_id} is not present in blaze store")
        donor_json = self.get_fhir_resource_as_json("Patient", donor_fhir_id)
        donor = SampleDonor.from_json(donor_json)
        return donor

    def build_sample_from_json(self, sample_fhir_id: str) -> Sample:
        """Build Sample Object from json representation
        :param sample_fhir_id: FHIR ID of the Specimen resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return Sample Object"""
        if not self.is_resource_present_in_blaze("Specimen", sample_fhir_id):
            raise NonExistentResourceException(f"Sample with FHIR ID {sample_fhir_id} is not present in blaze store")
        sample_json = self.get_fhir_resource_as_json("Specimen", sample_fhir_id)
        donor_fhir_id = parse_reference_id(get_nested_value(sample_json, ["subject", "reference"]))
        donor_id = self.get_identifier_by_fhir_id("Patient", donor_fhir_id)
        sample = Sample.from_json(sample_json, donor_id)
        return sample

    def build_observation_from_json(self, observation_fhir_id: str) -> Observation:
        """Build Observation Object from json representation
        :param observation_fhir_id: FHIR ID of the Observation resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return Observation Object"""
        if not self.is_resource_present_in_blaze("Observation", observation_fhir_id):
            raise NonExistentResourceException(
                f"Observation with FHIR ID {observation_fhir_id} is not present in blaze store")
        observation_json = self.get_fhir_resource_as_json("Observation", observation_fhir_id)
        patient_fhir_id = parse_reference_id(get_nested_value(observation_json, ["subject", "reference"]))
        sample_fhir_id = parse_reference_id(get_nested_value(observation_json, ["specimen", "reference"]))
        patient_identifier = self.get_identifier_by_fhir_id("Patient", patient_fhir_id)
        sample_identifier = self.get_identifier_by_fhir_id("Specimen", sample_fhir_id)
        observation = Observation.from_json(observation_json, patient_identifier, sample_identifier)
        return observation

    def build_diagnosis_report_from_json(self, diagnosis_report_fhir_id: str) -> DiagnosisReport:
        """Build DiagnosisReport object from json representation
        :param diagnosis_report_fhir_id: FHIR ID of the DiagnosticReport resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return DiagnosisReport Object"""
        if not self.is_resource_present_in_blaze("DiagnosticReport", diagnosis_report_fhir_id):
            raise NonExistentResourceException(
                f"DiagnosisReport with FHIR ID {diagnosis_report_fhir_id} is not present in blaze store")
        diagnosis_report_json = self.get_fhir_resource_as_json("DiagnosticReport", diagnosis_report_fhir_id)
        sample_fhir_id = parse_reference_id(get_nested_value(diagnosis_report_json, ["specimen", 0, "reference"]))
        donor_fhir_id = parse_reference_id(get_nested_value(diagnosis_report_json, ["subject", "reference"]))
        observation_fhir_ids = []
        observation_references = get_nested_value(diagnosis_report_json, ["result"])
        if observation_references is not None:
            for observation_reference in observation_references:
                observation_fhir_id = parse_reference_id(get_nested_value(observation_reference, ["reference"]))
                observation_fhir_ids.append(observation_fhir_id)

        sample_identifier = self.get_identifier_by_fhir_id("Specimen", sample_fhir_id)
        donor_identifier = self.get_identifier_by_fhir_id("Patient", donor_fhir_id)
        observation_identifiers = []
        for observation_fhir_id in observation_fhir_ids:
            observation_id = self.get_identifier_by_fhir_id("Observation", observation_fhir_id)
            if observation_id is not None:
                observation_identifiers.append(observation_id)

        diagnosis_report = DiagnosisReport.from_json(diagnosis_report_json, sample_identifier, donor_identifier,
                                                     observation_identifiers)
        return diagnosis_report

    def build_condition_from_json(self, condition_fhir_id: str) -> Condition:
        """Build Condition object from json representation
        :param condition_fhir_id: FHIR ID of the Condition resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return Condition Object"""
        if not self.is_resource_present_in_blaze("Condition", condition_fhir_id):
            raise NonExistentResourceException(
                f"Condition with FHIR ID {condition_fhir_id} is not present in blaze store")
        condition_json = self.get_fhir_resource_as_json("Condition", condition_fhir_id)
        patient_fhir_id = parse_reference_id(get_nested_value(condition_json, ["subject", "reference"]))
        patient_identifier = self.get_identifier_by_fhir_id("Patient", patient_fhir_id)
        condition = Condition.from_json(condition_json, patient_identifier)
        return condition

    def build_collection_from_json(self, collection_fhir_id: str) -> Collection:
        """Build a collection object from a json representation.
        Does not add samples which are alredy deleted from blaze
        :param collection_fhir_id: FHIR ID of the Collection resource
        :return: Collection object
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        """
        if not self.is_resource_present_in_blaze("Group", collection_fhir_id):
            raise NonExistentResourceException(
                f"Collection with FHIR ID {collection_fhir_id} is not present in blaze store")
        collection_json = self.get_fhir_resource_as_json("Group", collection_fhir_id)
        managing_collection_org_fhir_id = parse_reference_id(
            get_nested_value(collection_json, ["managingEntity", "reference"]))
        managing_collection_id = self.get_identifier_by_fhir_id("Organization", managing_collection_org_fhir_id)
        already_present_sample_fhir_ids = self.__get_all_sample_fhir_ids_belonging_to_collection(collection_fhir_id)
        only_existing_samples = list(
            filter(lambda s: self.is_resource_present_in_blaze("Specimen", s), already_present_sample_fhir_ids))
        already_present_sample_ids = [self.get_identifier_by_fhir_id("Specimen", sample_fhir_id) for sample_fhir_id in
                                      only_existing_samples]
        collection = Collection.from_json(collection_json, managing_collection_id, already_present_sample_ids)
        collection._sample_fhir_ids = only_existing_samples
        return collection

    def build_collection_organization_from_json(self, collection_organization_fhir_id: str) -> CollectionOrganization:
        """Build a CollectionOrganization object from a json representation
        :param collection_organization_fhir_id: FHIR ID of the collection resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return CollectionOrganization Object"""
        if not self.is_resource_present_in_blaze("Organization", collection_organization_fhir_id):
            raise NonExistentResourceException(
                f"CollectionOrganization with FHIR ID {collection_organization_fhir_id} is not present in blaze store")
        collection_org_json = self.get_fhir_resource_as_json("Organization", collection_organization_fhir_id)
        managing_biobank_fhir_id = parse_reference_id(get_nested_value(collection_org_json, ["partOf", "reference"]))
        managing_biobank_identifier = self.get_identifier_by_fhir_id("Organization", managing_biobank_fhir_id)
        collection_organization = CollectionOrganization.from_json(collection_org_json, managing_biobank_identifier)
        return collection_organization

    def build_network_from_json(self, network_fhir_id: str) -> Network:
        """Build a Network object form a json representation
        :param network_fhir_id: FHIR ID of the network resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return Network Object"""
        if not self.is_resource_present_in_blaze("Group", network_fhir_id):
            raise NonExistentResourceException(f"Network with FHIR ID {network_fhir_id} is not present in blaze store")
        network_json = self.get_fhir_resource_as_json("Group", network_fhir_id)
        managing_network_org_fhir_id = parse_reference_id(
            get_nested_value(network_json, ["managingEntity", "reference"]))
        managing_network_identifier = self.get_identifier_by_fhir_id("Organization", managing_network_org_fhir_id)
        collection_fhir_ids, biobank_fhir_ids = self.__get_all_members_belonging_to_network(network_json)
        collection_identifiers = [self.get_identifier_by_fhir_id("Group", collection_fhir_id) for collection_fhir_id in
                                  collection_fhir_ids]
        biobank_identifiers = [self.get_identifier_by_fhir_id("Organization", biobank_fhir_id) for biobank_fhir_id in
                               biobank_fhir_ids]
        network = Network.from_json(network_json, managing_network_identifier, collection_identifiers,
                                    biobank_identifiers)
        return network

    def build_network_org_from_json(self, network_org_fhir_id: str) -> NetworkOrganization:
        """Build a NetworkOrganization object from a json representation
        :param network_org_fhir_id: FHIR ID of the network organization resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return NetworkOrganisation object"""
        if not self.is_resource_present_in_blaze("Organization", network_org_fhir_id):
            raise NonExistentResourceException(
                f"NetworkOrganization with FHIR ID {network_org_fhir_id} is not present in blaze store")
        network_org_json = self.get_fhir_resource_as_json("Organization", network_org_fhir_id)
        managing_biobank_fhir_id = parse_reference_id(get_nested_value(network_org_json, ["partOf", "reference"]))
        managing_biobank_identifier = self.get_identifier_by_fhir_id("Organization", managing_biobank_fhir_id)
        network_org = NetworkOrganization.from_json(network_org_json, managing_biobank_identifier)
        return network_org

    def build_biobank_from_json(self, biobank_fhir_id: str) -> Biobank:
        """Build a Biobank object from a json representation
        :param biobank_fhir_id: FHIR ID of the biobank resource
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return Biobank object"""
        if not self.is_resource_present_in_blaze("Organization", biobank_fhir_id):
            raise NonExistentResourceException(f"Biobank with FHIR ID {biobank_fhir_id} is not present in blaze store")
        biobank_json = self.get_fhir_resource_as_json("Organization", biobank_fhir_id)
        biobank = Biobank.from_json(biobank_json)
        return biobank

    def add_diagnosis_reports_to_condition(self, condition_fhir_id: str, diagnosis_report_fhir_ids: list[str]) -> bool:
        """add new diagnosis to already present condition in the blaze store
        :param condition_fhir_id: FHIR ID of the condition
        :param diagnosis_report_fhir_ids: FHIR IDs of the diagnosis reports
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :returns: True if the diagnosis reports were added successfully, false otherwise"""
        condition = self.build_condition_from_json(condition_fhir_id)
        for diagnosis_report_fhir_id in diagnosis_report_fhir_ids:
            if diagnosis_report_fhir_id not in condition.diagnosis_report_fhir_ids:
                condition.diagnosis_report_fhir_ids.append(diagnosis_report_fhir_id)
        updated_condition_fhir = condition.to_fhir()
        condition.add_fhir_id_to_condition(updated_condition_fhir)
        self.update_fhir_resource("Condition", condition_fhir_id, updated_condition_fhir.as_json())
        return True

    def add_existing_observations_to_diagnosis_report(self, observation_fhir_ids: list[str],
                                                      diagnosis_report_fhir_id: str) -> bool:
        """Add an existing observation to an existing diagnosis report in blaze.
        :param observation_fhir_ids: FHIR ID of the observation
        :param diagnosis_report_fhir_id: FHIR ID of the diagnosis report
        :return: True if the observation was added successfully
        :raises HTTPError: if the request to blaze fails
        """
        diagnosis_report = self.build_diagnosis_report_from_json(diagnosis_report_fhir_id)
        for observation_fhir_id in observation_fhir_ids:
            if not self.is_resource_present_in_blaze("Observation", observation_fhir_id):
                raise NonExistentResourceException(f"Cannot add observation "
                                                   f"with FHIR ID: {observation_fhir_id} to diagnosis"
                                                   f"report because this observation is not present in blaze store")
            if observation_fhir_id not in diagnosis_report.observations_fhir_identifiers:
                diagnosis_report.observations_fhir_identifiers.append(observation_fhir_id)
        diagnosis_report_json = diagnosis_report.add_fhir_id_to_diagnosis_report(diagnosis_report.to_fhir())
        return self.update_fhir_resource("DiagnosticReport", diagnosis_report_fhir_id, diagnosis_report_json.as_json())

    def add_already_present_samples_to_existing_collection(self, sample_fhir_ids: list[str],
                                                           collection_fhir_id: str) -> bool:
        """Add samples already present in blaze to the collection
        :param sample_fhir_ids: FHIR IDs of samples to add to collection
        :param collection_fhir_id: FHIR ID of collection
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return: Bool indicating outcome of this operation"""
        collection = self.build_collection_from_json(collection_fhir_id)
        sample_generator_for_characteristics = (self.build_sample_from_json(sample_fhir_id) for sample_fhir_id in
                                                sample_fhir_ids)

        collection = self.__update_collection_characteristics_from_samples(sample_generator_for_characteristics,
                                                                           collection)
        already_present_samples_set = set(collection.sample_fhir_ids)
        for sample_fhir_id in sample_fhir_ids:
            if sample_fhir_id not in already_present_samples_set:
                already_present_samples_set.add(sample_fhir_id)
        collection._sample_fhir_ids = list(already_present_samples_set)
        collection = collection.add_fhir_id_to_collection(collection.to_fhir())
        return self.update_fhir_resource("Group", collection_fhir_id, collection.as_json())

    def update_collection_values(self, collection_fhir_id) -> bool:
        """Removes samples FHIR IDs that are not present in the blaze store from collection,and
        recalculates characteristics:
        :param collection_fhir_id: FHIR ID of collection
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return: Bool indicating if the collection was updated or not"""
        collection = self.build_collection_from_json(collection_fhir_id)
        sample_fhir_ids = collection.sample_fhir_ids
        present_samples = (self.build_sample_from_json(sample_fhir_id) for sample_fhir_id in collection.sample_fhir_ids)
        collection._sample_fhir_ids = []
        collection.age_range_low = 0
        collection.age_range_high = 0
        collection.storage_temperatures = []
        collection.material_types = []
        collection.genders = []
        collection.diagnoses = []
        collection.number_of_subjects = 0
        collection = self.__update_collection_characteristics_from_samples(present_samples, collection)
        collection._sample_fhir_ids = sample_fhir_ids
        collection_fhir = collection.add_fhir_id_to_collection(collection.to_fhir())
        return self.update_fhir_resource("Group", collection.collection_fhir_id, collection_fhir.as_json())

    def __update_collection_characteristics_from_samples(self, samples: Generator[Sample, Any, None],
                                                         collection: Collection) -> Collection:
        """update the characteristics for collection with new values from the samples.
        :param samples: the samples to calculate the characteristics from
        :param collection_fhir_id: the fhir id of the collection
        :return: updated collection object
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        """
        already_present_samples = (self.build_sample_from_json(sample_fhir_id) for sample_fhir_id in
                                   collection.sample_fhir_ids)
        donor_fhir_ids = set([sample.subject_fhir_id for sample in already_present_samples])
        count_of_new_subjects = 0

        for sample in samples:
            sample_fhir_id = self.get_fhir_id("Specimen", sample.identifier)
            if sample.donor_identifier not in donor_fhir_ids:
                count_of_new_subjects += 1
                donor_fhir_ids.add(sample.donor_identifier)
            donor = self.build_donor_from_json(sample.subject_fhir_id)
            sample_material_type = get_material_type_from_detailed_material_type(sample.material_type)
            if donor.gender not in collection.genders:
                collection.genders.append(donor.gender)
            if sample.storage_temperature is not None and \
                    sample.storage_temperature not in collection.storage_temperatures:
                collection.storage_temperatures.append(sample.storage_temperature)
            if sample_material_type is not None and sample_material_type not in collection.material_types:
                collection.material_types.append(sample_material_type)
            sample_diagnoses = self.__get_diagnoses_of_sample(sample_fhir_id)
            for diagnosis in sample_diagnoses:
                if diagnosis is not None and diagnosis not in collection.diagnoses:
                    collection.diagnoses.append(diagnosis)
            ages_at_diagnosis = self.__get_age_at_the_time_of_diagnosis(sample_fhir_id, donor.donor_fhir_id)
            for age in ages_at_diagnosis:
                if collection.age_range_low is None:
                    collection.age_range_low = age
                else:
                    collection.age_range_low = min(age, collection.age_range_low)
                if collection.age_range_high is None:
                    collection.age_range_high = age
                else:
                    collection.age_range_high = max(age, collection.age_range_high)
        if collection.number_of_subjects is None:
            collection.number_of_subjects = count_of_new_subjects
        else:
            collection.number_of_subjects += count_of_new_subjects
        return collection

    def get_collection_fhir_id_by_sample_fhir_identifier(self, sample_fhir_id: str) -> str | None:
        """Get Collection FHIR id which contains provided sample FHIR ID, if there is one
        :param sample_fhir_id: FHIR ID of the sample
        :return: collection FHIR id if there is collection which contains this sample, None otherwise"""
        return self.__get_group_fhir_id_by_resource_fhir_identifier(sample_fhir_id)

    def get_network_fhir_id_by_member_fhir_identifier(self, member_fhir_id: str) -> str | None:
        """Get Network FHIR id which contains provided member FHIR ID (either collection resource of biobank resource),
         if there is one
        :param member_fhir_id: FHIR ID of the member of network
        :return: network FHIR id if there is network which contains this member, None otherwise"""
        return self.__get_group_fhir_id_by_resource_fhir_identifier(member_fhir_id)

    def __get_group_fhir_id_by_resource_fhir_identifier(self, resource_fhir_id: str) -> str | None:
        """Get Group FHIR id which contains provided FHIR_ID or resource, if there is one
        :param resource_fhir_id: FHIR ID of the resource
        :return: Group resource FHIR ID if there is group which
        contains reference to resource_fhir_id, none otherwise"""
        response = self._session.get(f"{self._blaze_url}/Group?groupMember={resource_fhir_id}")
        self.__raise_for_status_extract_diagnostics_message(response)
        response_json = response.json()
        return get_nested_value(response_json, ["entry", 0, "resource", "id"])

    def get_observation_fhir_ids_belonging_to_diagnosis_report(self, diagnosis_report_fhir_id: str) -> list[str]:
        """Get observation FHIR IDs belonging to a diagnosis report
        :param diagnosis_report_fhir_id: FHIR ID of diagnosis report
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found"""
        diagnosis_report = self.build_diagnosis_report_from_json(diagnosis_report_fhir_id)
        if diagnosis_report.observations_fhir_identifiers is None:
            return []
        return diagnosis_report.observations_fhir_identifiers

    def __get_diagnoses_of_sample(self, sample_fhir_id: str) -> list[str]:
        """Get all diagnoses that are linked to a sample
        :param sample_fhir_id: FHIR ID of sample
        :raises HTTPError: if the request to blaze fails
        :raises NonExistentResourceException: if the resource cannot be found
        :return: List of diagnoses codes"""
        diagnoses = []
        observation_fhir_ids = self.get_observation_fhir_ids_belonging_to_sample(sample_fhir_id)
        for observation_fhir_id in observation_fhir_ids:
            observation = self.build_observation_from_json(observation_fhir_id)
            if observation.icd10_code is not None:
                diagnoses.append(observation.icd10_code)
        return diagnoses

    def __get_age_at_the_time_of_diagnosis(self, sample_fhir_id: str, donor_fhir_id: str) -> list[int]:
        """get age of donor at the tame tha the diagnosis was set"""
        ages_at_diagnosis = []
        diagnosis_report_fhir_id = self.get_diagnosis_report_fhir_id_belonging_to_sample(sample_fhir_id)
        if diagnosis_report_fhir_id is None:
            return ages_at_diagnosis
        donor = self.build_donor_from_json(donor_fhir_id)
        if donor.date_of_birth is None:
            return ages_at_diagnosis
        donor_birthdate = donor.date_of_birth

        observation_fhir_ids = self.get_observation_fhir_ids_belonging_to_diagnosis_report(diagnosis_report_fhir_id)
        observations = [self.build_observation_from_json(observation_fhir_id) for observation_fhir_id in
                        observation_fhir_ids]

        for observation in observations:
            effective_time = observation.diagnosis_observed_datetime
            if effective_time is None:
                continue
            age_at_diagnosis = effective_time.year - donor_birthdate.year
            ages_at_diagnosis.append(age_at_diagnosis)
        return ages_at_diagnosis

    def delete_donor(self, donor_fhir_id: str, part_of_bundle: bool = False) -> list[BundleEntry] | bool:
        """Delete a donor from blaze.
        BEWARE: Deleting a donor will also delete all related samples and diagnosis reports.
        :param donor_fhir_id: the fhir id of the donor to delete
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise
        :raises HTTPError: if the request to blaze fails
        """
        entries = []
        if not self.is_resource_present_in_blaze("Patient", donor_fhir_id):
            raise NonExistentResourceException(
                f"Cannot delete Donor with FHIR id {donor_fhir_id} because donor is not present in the blaze store.")
        patient_entry = self.__create_delete_bundle_entry("Patient", donor_fhir_id)
        entries.append(patient_entry)
        sample_fhir_ids = self.__get_all_sample_fhir_ids_belonging_to_patient(donor_fhir_id)
        delete_from_collection = self.__delete_sample_references_from_collections(sample_fhir_ids)
        condition_fhir_id = self.__get_condition_fhir_id_by_donor_identifier(donor_fhir_id)
        for sample_fhir_id in sample_fhir_ids:
            sample_entries = self.delete_sample(sample_fhir_id, True, True)
            entries.extend(sample_entries)
        if condition_fhir_id is not None:
            condition_entries = self.delete_condition(condition_fhir_id, True)
            entries.extend(condition_entries)
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def __delete_sample_references_from_collections(self, sample_fhir_ids: list[str]) -> bool:
        """
        :param sample_fhir_ids:
        :return:
        """
        entries = []
        collection_sample_fhir_ids_map = {}
        for sample_fhir_id in sample_fhir_ids:
            collection_fhir_id = self.get_collection_fhir_id_by_sample_fhir_identifier(sample_fhir_id)
            if collection_fhir_id is None:
                continue
            if collection_fhir_id not in collection_sample_fhir_ids_map:

                collection_sample_fhir_ids_map[collection_fhir_id] = set()
                collection_sample_fhir_ids_map[collection_fhir_id].add(sample_fhir_id)
            else:
                collection_sample_fhir_ids_map[collection_fhir_id].add(sample_fhir_id)
        for collection_fhir_id, sample_fhir_ids_set in collection_sample_fhir_ids_map.items():
            updated_collection = self.__delete_samples_from_collection(collection_fhir_id, list(sample_fhir_ids_set))
            entries.append(self.__create_bundle_entry_for_updating_collection(updated_collection))
        if entries is None:
            return True
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return 200 <= response.status_code < 300

    def delete_condition(self, condition_fhir_id: str, part_of_bundle: bool = False) -> list[BundleEntry] | bool:
        """Delete a condition from blaze.
        :param condition_fhir_id: the fhir id of the condition to delete
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise
        :raises HTTPError: if the request to blaze fails
        """
        entries = []
        if not self.is_resource_present_in_blaze("Condition", condition_fhir_id):
            raise NonExistentResourceException(
                f"Cannot delete Condition with FHIR id {condition_fhir_id} because "
                f"condition is not present in the blaze store.")
        condition_entry = self.__create_delete_bundle_entry("Condition", condition_fhir_id)
        entries.append(condition_entry)
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def delete_sample(self, sample_fhir_id: str, part_of_bundle: bool = False,
                      part_of_deleting_patient: bool = False) -> list[BundleEntry] | bool:
        """Delete a sample from blaze. BEWARE: Deleting a sample will also delete all related diagnosis reports and
        observations.
        :param sample_fhir_id: the fhir id of the sample to delete
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :param part_of_deleting_patient: bool indicating if deleting sample is part of
        deleting patient(and his condition), or not.
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise
        :raises HTTPError: if the request to blaze fails
        """
        entries = []
        if not self.is_resource_present_in_blaze("Specimen", sample_fhir_id):
            raise NonExistentResourceException(
                f"Cannot delete Sample with FHIR id {sample_fhir_id} because"
                f"sample is not present in the blaze store.")
        specimen_entry = self.__create_delete_bundle_entry("Specimen", sample_fhir_id)
        entries.append(specimen_entry)
        if not part_of_deleting_patient:
            self.__delete_sample_references_from_collections([sample_fhir_id])
        observations_linked_to_sample_fhir_ids = self.get_observation_fhir_ids_belonging_to_sample(sample_fhir_id)
        set_observations_linked_to_sample = set(observations_linked_to_sample_fhir_ids)
        diagnosis_reports_fhir_ids = self.__get_diagnosis_reports_fhir_id_by_sample_identifier(sample_fhir_id)
        for diagnosis_report_fhir_id in diagnosis_reports_fhir_ids:
            observation_fhir_ids = self.get_observation_fhir_ids_belonging_to_diagnosis_report(diagnosis_report_fhir_id)
            diagnosis_report_entries = self.delete_diagnosis_report(diagnosis_report_fhir_id, True,
                                                                    part_of_deleting_patient)
            entries.extend(diagnosis_report_entries)
            for observation_fhir_id in observation_fhir_ids:
                if observation_fhir_id not in set_observations_linked_to_sample:
                    observation_entries = self.delete_observation(observation_fhir_id, True)
                    entries.extend(observation_entries)
        for observation_fhir_id in observations_linked_to_sample_fhir_ids:
            observation_entries = self.delete_observation(observation_fhir_id, True)
            entries.extend(observation_entries)
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def delete_diagnosis_report(self, diagnosis_report_fhir_id: str, part_of_bundle: bool = False,
                                part_of_deleting_patient: bool = False) -> list[BundleEntry] | bool:
        """Delete a diagnosis report from blaze.
        :param diagnosis_report_fhir_id: the fhir identifier of the diagnosis report
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :param part_of_deleting_patient: bool indicating if the diagnosis report reference should be deleted from
        condition( if set to false), or not (deleting patient will result in deleting condition,
         so there is no need to update the condition if it is to be deleted)
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise
        :raises HTTPError: if the request to blaze fails
        """
        entries = []
        if not self.is_resource_present_in_blaze("DiagnosticReport", diagnosis_report_fhir_id):
            raise NonExistentResourceException(
                f"Cannot delete DiagnosisReport with FHIR id {diagnosis_report_fhir_id} because "
                f"diagnosis report is not present in the blaze store.")
        diagnosis_report_entry = self.__create_delete_bundle_entry("DiagnosticReport", diagnosis_report_fhir_id)
        entries.append(diagnosis_report_entry)
        diagnosis_report_json = self.get_fhir_resource_as_json("DiagnosticReport", diagnosis_report_fhir_id)
        patient_fhir_id = parse_reference_id(get_nested_value(diagnosis_report_json, ["subject", "reference"]))
        if not part_of_deleting_patient:
            condition_fhir_id = self.__get_condition_fhir_id_by_donor_identifier(patient_fhir_id)
            if condition_fhir_id is not None:
                condition_entries = self.__delete_diagnosis_report_reference_from_condition(condition_fhir_id,
                                                                                            diagnosis_report_fhir_id,
                                                                                            True)
                entries.extend(condition_entries)
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def delete_observation(self, observation_fhir_id: str, part_of_bundle: bool = False) -> list[BundleEntry] | bool:
        """Delete an observation from blaze.
        :param observation_fhir_id: the fhir id of the observation to delete
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise
        :raises HTTPError: if the request to blaze fails
        """
        entries = []
        if not self.is_resource_present_in_blaze("Observation", observation_fhir_id):
            raise NonExistentResourceException(
                f"Cannot delete Observation with FHIR id {observation_fhir_id} "
                f"because observation is not present in the blaze store.")
        entry = self.__create_delete_bundle_entry("Observation", observation_fhir_id)
        entries.append(entry)
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def delete_collection(self, collection_fhir_id: str, part_of_bundle: bool = False) -> list[BundleEntry] | bool:
        """Delete collection from blaze.
        :param collection_fhir_id: FHIR ID of the collection to be deleted
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise """
        entries = []
        if not self.is_resource_present_in_blaze("Group", collection_fhir_id):
            raise NonExistentResourceException(
                f"Cannot delete Collection with FHIR ID {collection_fhir_id} "
                f"because collection is not present in the blaze store")
        collection_entry = self.__create_delete_bundle_entry("Group", collection_fhir_id)
        entries.append(collection_entry)
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def __delete_collection_reference_from_network(self, network_fhir_id: str, collection_fhir_id: str) -> bool:
        """Delete a collection reference from network
        :param network_fhir_id: FHIR ID of the network
        :param collection_fhir_id: FHIR ID of the collection to be deleted
        :return: True if the reference was deleted sucessfully, false otherwise"""
        network = self.build_network_from_json(network_fhir_id)
        if collection_fhir_id in network.members_collections_fhir_ids:
            network.members_collections_fhir_ids.remove(collection_fhir_id)
        update_network_fhir = network.add_fhir_id_to_network(network.to_fhir())
        return self.update_fhir_resource("Group", network_fhir_id, update_network_fhir.as_json())

    def __delete_samples_from_collection(self, collection_fhir_id: str, sample_fhir_ids: list[str]) -> Collection:
        collection = self.build_collection_from_json(collection_fhir_id)
        sample_fhir_ids_set = set(collection.sample_fhir_ids)
        for sample_fhir_id in sample_fhir_ids:
            if sample_fhir_id in sample_fhir_ids_set:
                sample_fhir_ids_set.remove(sample_fhir_id)
        collection._sample_fhir_ids = list(sample_fhir_ids_set)
        return collection

    def delete_collection_organization(self, collection_organization_fhir_id: str, part_of_bundle: bool = False) \
            -> list[BundleEntry] | bool:
        """delete collection organization from blaze store. WARNING: deleting collection organization
        will result in deleting collection resource as well
        :param collection_organization_fhir_id: FHIR ID of collection organization resource to be deleted
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise """
        entries = []
        if not self.is_resource_present_in_blaze("Organization", collection_organization_fhir_id):
            raise NonExistentResourceException(f"Cannot delete CollectionOrganization with FHIR ID "
                                               f"{collection_organization_fhir_id} because this resource is not "
                                               f"present in the blaze store")
        collection_org_entry = self.__create_delete_bundle_entry("Organization", collection_organization_fhir_id)
        entries.append(collection_org_entry)
        collection_response = self._session.get(
            f"{self._blaze_url}/Group?managing-entity={collection_organization_fhir_id}")
        response_json = collection_response.json()
        if response_json["total"] != 0:
            for entry in response_json["entry"]:
                collection_fhir_id = get_nested_value(entry, ["resource", "id"])
                collection_entries = self.delete_collection(collection_fhir_id, True)
                entries.extend(collection_entries)
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def delete_network(self, network_fhir_id: str, part_of_bundle: bool = False) -> list[BundleEntry] | bool:
        """delete network from blaze store.
        :param network_fhir_id: FHIR ID of network resource to be deleted
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise """
        entries = []
        if not self.is_resource_present_in_blaze("Group", network_fhir_id):
            raise NonExistentResourceException(f"Cannot delete Network with FHIR ID {network_fhir_id} because "
                                               f"this resource is not present in the blaze store")
        network_entry = self.__create_delete_bundle_entry("Group", network_fhir_id)
        entries.append(network_entry)

        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def delete_network_organization(self, network_organization_fhir_id: str, part_of_bundle: bool = False) \
            -> list[BundleEntry] | bool:
        """delete network organization from blaze store. BEWARE: deleting network organization will
        result in deleting network resource as well
        :param network_organization_fhir_id: FHIR ID of network organization resource to be deleted
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise """
        entries = []
        if not self.is_resource_present_in_blaze("Organization", network_organization_fhir_id):
            raise NonExistentResourceException(f"Cannot delete Network Organization with FHIR ID"
                                               f" {network_organization_fhir_id} because this resource is not present "
                                               f"in the blaze store")
        network_org_entry = self.__create_delete_bundle_entry("Organization", network_organization_fhir_id)
        entries.append(network_org_entry)
        network_response = self._session.get(
            f"{self._blaze_url}/Group?managing-entity={network_organization_fhir_id}")
        response_json = network_response.json()
        if response_json["total"] != 0:
            for entry in response_json["entry"]:
                network_fhir_id = get_nested_value(entry, ["resource", "id"])
                network_entries = self.delete_network(network_fhir_id, True)
                entries.extend(network_entries)
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    def delete_biobank(self, biobank_fhir_id: str, part_of_bundle: bool = False) -> list[BundleEntry] | bool:
        """delete biobank from blaze store. BEWARE: deleting biobank will result in
        deleting all connected collections and networks asw well
        :param biobank_fhir_id: FHIR ID of biobank resource to be deleted
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise """
        entries = []
        if not self.is_resource_present_in_blaze("Organization", biobank_fhir_id):
            raise NonExistentResourceException(f"Cannot delete Biobank with FHIR ID"
                                               f" {biobank_fhir_id} because this resource is not present "
                                               f"in the blaze store")
        biobank_entry = self.__create_delete_bundle_entry("Organization", biobank_fhir_id)
        entries.append(biobank_entry)
        response = self._session.get(f"{self._blaze_url}/Organization?partof={biobank_fhir_id}")
        response_json = response.json()
        if response_json["total"] != 0:
            for entry in response_json["entry"]:
                resource = entry["resource"]
                resource_type: str = get_nested_value(resource, ["meta", "profile", 0])
                if resource_type.endswith("collection-organization"):
                    entries.extend(self.delete_collection_organization(resource["id"], True))
                else:
                    entries.extend(self.delete_network_organization(resource["id"], True))
        if part_of_bundle:
            return entries
        bundle = self.__create_bundle(entries)
        response = self._session.post(f"{self._blaze_url}", json=bundle.as_json())
        self.__raise_for_status_extract_diagnostics_message(response)
        return response.status_code == 200 or response.status_code == 204

    @staticmethod
    def __get_all_members_belonging_to_network(network_json: dict) -> tuple[list[str], list[str]]:
        """Get all members which belong to the network
        :param network_json: json representation of network
        :return tuple containing list of collection FHIR IDs,
        and list of organization FHIR ids belonging to this network"""
        collection_fhir_ids = []
        biobank_fhir_ids = []
        for extension in network_json.get("extension", []):
            if extension["url"] == "http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity":
                resource_type, reference = get_nested_value(extension, ["valueReference", "reference"]).split("/")
                if resource_type == "Group":
                    collection_fhir_ids.append(reference)
                else:
                    biobank_fhir_ids.append(reference)
        return collection_fhir_ids, biobank_fhir_ids

    def __get_all_sample_fhir_ids_belonging_to_collection(self, collection_fhir_id: str) -> list[str]:
        """Get all sample fhir ids which belong to collection.
        :param collection_fhir_id: id of collection from which we want to get samples.
        :raises: HTTPError if the requests to blaze fails
        :return: list of FHIR ids of samples that belong to this collection."""
        sample_fhir_ids = []
        collection_json = self.get_fhir_resource_as_json("Group", collection_fhir_id)
        for extension in collection_json.get("extension", []):
            if extension["url"] == "http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity":
                reference = get_nested_value(extension, ["valueReference", "reference"])
                if reference is not None:
                    sample_fhir_ids.append(parse_reference_id(reference))
        return sample_fhir_ids

    def __get_all_sample_fhir_ids_belonging_to_patient(self, patient_fhir_id: str) -> list[str]:
        """Get all sample fhir ids which belong to patient.
        :param patient_fhir_id: id of patient from which we want to get samples.
        :raises: HTTPError if the requests to blaze fails
        :return: list of FHIR ids of samples that belong to this patient."""
        sample_fhir_ids = []
        response = self._session.get(f"{self._blaze_url}/Specimen?patient={patient_fhir_id}")
        self.__raise_for_status_extract_diagnostics_message(response)
        response_json = response.json()
        if response_json["total"] == 0:
            return sample_fhir_ids
        for entry in response_json['entry']:
            sample_fhir_id = get_nested_value(entry["resource"], ["id"])
            sample_fhir_ids.append(sample_fhir_id)
        return sample_fhir_ids

    def __get_diagnosis_reports_fhir_id_by_sample_identifier(self, sample_identifier: str) -> list[str]:
        response = self._session.get(f"{self._blaze_url}/DiagnosticReport?specimen=Specimen/{sample_identifier}")
        self.__raise_for_status_extract_diagnostics_message(response)
        response_json = response.json()
        diagnosis_reports_fhir_ids = []
        if response_json["total"] == 0:
            return diagnosis_reports_fhir_ids
        for entry in response_json["entry"]:
            diagnosis_report = entry["resource"]
            diagnosis_report_fhir_id = get_nested_value(diagnosis_report, ["id"])
            if diagnosis_report_fhir_id is not None:
                diagnosis_reports_fhir_ids.append(diagnosis_report_fhir_id)
        return diagnosis_reports_fhir_ids

    def __get_condition_fhir_id_by_donor_identifier(self, patient_identifier: str) -> str | None:
        response = self._session.get(f"{self._blaze_url}/Condition?subject={patient_identifier}")
        self.__raise_for_status_extract_diagnostics_message(response)
        response_json = response.json()
        if response_json["total"] == 0:
            return None
        return get_nested_value(response_json, ["entry", 0, "resource", "id"])

    def __delete_diagnosis_report_reference_from_condition(self, condition_fhir_id: str, diagnosis_report_fhir_id: str,
                                                           part_of_bundle: bool = False) \
            -> list[BundleEntry] | bool:
        """Delete diagnosis_report_reference_from condition
        :param condition_fhir_id: FHIR ID of condition from which the reference should be deleted
        :param diagnosis_report_fhir_id: FHIR ID of diagnosis report to be deleted from condition
        :param part_of_bundle: bool indicating if this operation is part of larger bundle or not
        :return: if part_of_bundle = True, this function returns list of BundleEntries to be using in a larger Bundle.
        otherwise, it will create its own bundle, and return True if deletion was successful, False otherwise """
        entries = []
        condition_json = self.get_fhir_resource_as_json("Condition", condition_fhir_id)
        if not self.is_resource_present_in_blaze("Condition", condition_fhir_id):
            raise NonExistentResourceException(
                f"Cannot delete diagnosis report reference from condition with FHIR ID {condition_fhir_id}"
                f"because this condition is not present in blaze store")
        condition = self.build_condition_from_json(condition_fhir_id)
        for diagnosis_report in condition.diagnosis_report_fhir_ids:
            if diagnosis_report == diagnosis_report_fhir_id:
                condition._diagnosis_report_fhir_ids.remove(diagnosis_report)

        condition_fhir = condition.add_fhir_id_to_condition(condition.to_fhir())
        if part_of_bundle:
            condition_entry = BundleEntry()
            condition_entry.resource = condition_fhir
            condition_entry.request = BundleEntryRequest()
            condition_entry.request.method = "PUT"
            condition_entry.request.url = f"Condition/{condition_fhir_id}"
            entries.append(condition_entry)
            return entries
        return self.update_fhir_resource("Condition", condition_fhir_id, condition_fhir.as_json())

    @staticmethod
    def __raise_for_status_extract_diagnostics_message(response: Response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            try:
                error_details = response.json()
                if 'issue' in error_details:
                    for issue in error_details['issue']:
                        diagnostics = issue.get('diagnostics', 'No diagnostics available')
                        http_err.args = (f"{http_err.args[0]} - Diagnostics: {diagnostics}",)
            except ValueError:
                pass
            raise

    @staticmethod
    def __create_bundle(entries: list[BundleEntry]) -> Bundle:
        """Create a bundle used for deleting multiple FHIR resources in a transaction"""
        bundle = Bundle()
        bundle.type = "transaction"
        bundle.entry = entries
        return bundle

    @staticmethod
    def __create_delete_bundle_entry(resource_type: str, resource_fhir_id: str) -> BundleEntry:
        entry = BundleEntry()
        entry.request = BundleEntryRequest()
        entry.request.method = "DELETE"
        entry.request.url = f"{resource_type}/{resource_fhir_id}"
        return entry

    @staticmethod
    def __create_bundle_entry_for_updating_collection(collection: Collection) -> BundleEntry:
        collection_fhir = collection.add_fhir_id_to_collection(collection.to_fhir())
        collection_entry = BundleEntry()
        collection_entry.resource = collection_fhir
        collection_entry.request = BundleEntryRequest()
        collection_entry.request.method = "PUT"
        collection_entry.request.url = f"Group/{collection.collection_fhir_id}"
        return collection_entry
