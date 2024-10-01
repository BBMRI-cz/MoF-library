import requests
from requests.adapters import HTTPAdapter, Retry

from src.MIABIS_on_FHIR.biobank import Biobank
from src.MIABIS_on_FHIR.collection import Collection
from src.MIABIS_on_FHIR.collection_organization import CollectionOrganization
from src.MIABIS_on_FHIR.condition import Condition
from src.MIABIS_on_FHIR.diagnosis_report import DiagnosisReport
from src.MIABIS_on_FHIR.network import Network
from src.MIABIS_on_FHIR.network_organization import NetworkOrganization
from src.MIABIS_on_FHIR.observation import Observation
from src.MIABIS_on_FHIR.sample import Sample
from src.MIABIS_on_FHIR.sample_donor import SampleDonor
from src.MIABIS_on_FHIR.util._parsing_util import get_nested_value, parse_reference_id


# TODO add update collection, update network
# TODO update methods- if there is no fhir_id (even when using the get_fhir_id method), throw an ValueException (or a custom one)

class BlazeClient:
    """Class for handling communication with a blaze server, be it for CRUD operations, search or other operations."""

    def __init__(self, blaze_url: str, blaze_username: str, blaze_password: str):
        self._blaze_url = blaze_url
        self._blaze_username = blaze_username
        self._blaze_password = blaze_password
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.auth = (blaze_username, blaze_password)
        self._session = session

    def get_fhir_resource_as_json(self, resource_type: str, resource_fhir_id: str) -> dict:
        """Get a FHIR resource from blaze as a json.
        :param resource_type: the type of the resource
        :param resource_fhir_id: the fhir id of the resource
        :return: json representation of the resource
        :raises HTTPError: if the request to blaze fails
        """
        response = self._session.get(f"{self._blaze_url}/{resource_type}/{resource_fhir_id}")
        response.raise_for_status()
        return response.json()

    def update_fhir_resource(self, resource_type: str, resource_fhir_id: str, resource_json: dict) -> bool:
        """Update a FHIR resource in blaze.
        :param resource_type: the type of the resource
        :param resource_fhir_id: the fhir id of the resource
        :param resource_json: the json representation of the resource
        :return: True if the resource was updated successfully
        :raises HTTPError: if the request to blaze fails
        """
        response = self._session.put(f"{self._blaze_url}/{resource_type}/{resource_fhir_id}", json=resource_json)
        response.raise_for_status()
        return response.status_code == 200 or response.status_code == 201

    def get_fhir_id(self, resource_type: str, resource_identifier: str) -> str | None:
        """get the fhir id of a resource in blaze.
            :param resource_type: the type of the resource
            :param resource_identifier: the identifier of the resource (usually given by the organization)
            :return: the fhir id of the resource in blaze, or None if the resource was not found
            :raises HTTPError: if the request to blaze fails
            """
        response = self._session.get(f"{self._blaze_url}/{resource_type.capitalize()}?identifier={resource_identifier}")
        response.raise_for_status()
        response_json = response.json()
        if response_json["total"] == 0:
            return None
        return response_json["entry"][0]["resource"]["id"]

    def get_identifier_by_fhir_id(self, resource_type: str, resource_fhir_id: str) -> str:
        """get the identifier of a resource in blaze.
            :param resource_type: the type of the resource
            :param resource_fhir_id: the fhir id of the resource
            :return: the identifier of the resource in blaze
            :raises HTTPError: if the request to blaze fails
            """
        response = self._session.get(f"{self._blaze_url}/{resource_type}/{resource_fhir_id}")
        response.raise_for_status()
        response_json = response.json()
        if response_json["total"] == 0:
            raise ValueError(f"Resource with type \"{resource_type}\" and fhir id \"{resource_fhir_id}\" not found.")
        return response_json["identifier"][0]["value"]

    def upload_donor(self, donor: SampleDonor) -> str:
        """Upload a donor to blaze.
            :param donor: the donor to upload
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded donor
            """

        response = self._session.post(f"{self._blaze_url}/Patient", json=donor.to_fhir().as_json())
        response.raise_for_status()
        return response.json()["id"]

    def upload_sample(self, sample: Sample) -> str:
        """Upload a sample to blaze.
            :param sample: the sample to upload
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded sample
            """
        donor_fhir_id = sample.subject_fhir_id
        if donor_fhir_id is None:
            donor_fhir_id = self.get_fhir_id("Patient", sample.donor_identifier)
        response = self._session.post(f"{self._blaze_url}/Specimen", json=sample.to_fhir(donor_fhir_id).as_json())
        response.raise_for_status()
        return response.json()["id"]

    def upload_observation(self, observation: Observation) -> str:
        """Upload an observation to blaze.
            :param observation: the observation to upload
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded observation
            """
        response = self._session.post(f"{self._blaze_url}/Observation", json=observation.to_fhir().as_json())
        response.raise_for_status()
        return response.json()["id"]

    def upload_diagnosis_report(self, diagnosis_report: DiagnosisReport) -> str:
        """Upload a diagnosis report to blaze.
            :param diagnosis_report: the diagnosis report to upload
            :param sample_fhir_id: the fhir id of the sample the diagnosis report is about
            :param observation_fhir_ids: the fhir ids of the observations in the diagnosis report
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded diagnosis report
            """
        sample_fhir_id = diagnosis_report.sample_fhir_id
        observation_fhir_ids = diagnosis_report.observations_fhir_identifiers
        if sample_fhir_id is None:
            sample_fhir_id = self.get_fhir_id("Specimen", diagnosis_report.sample_identifier)
        if observation_fhir_ids is None:
            observation_fhir_ids = [self.get_fhir_id("Observation", observation_id) for observation_id in
                                    diagnosis_report.observations_identifiers]
        diagnosis_report_json = diagnosis_report.to_fhir(sample_fhir_id, observation_fhir_ids).as_json()
        response = self._session.post(f"{self._blaze_url}/DiagnosticReport", json=diagnosis_report_json)
        response.raise_for_status()
        return response.json()["id"]

    def upload_condition(self, condition: Condition, diagnosis_reports_fhir_ids: list[str]) -> str:
        """Upload a condition to blaze.
            :param condition: the condition to upload
            :param diagnosis_reports_fhir_ids: the fhir ids of the diagnosis reports in the condition
            :raises HTTPError: if the request to blaze fails
            :return: the fhir id of the uploaded condition
            """
        donor_fhir_id = condition.patient_fhir_id
        if donor_fhir_id is None:
            donor_fhir_id = self.get_fhir_id("Patient", condition.patient_identifier)
        condition_json = condition.to_fhir(donor_fhir_id, diagnosis_reports_fhir_ids).as_json()
        response = self._session.post(f"{self._blaze_url}/Condition", json=condition_json)
        response.raise_for_status()
        return response.json()["id"]

    def upload_biobank(self, biobank: Biobank) -> str:
        """Upload a biobank to blaze.
        :param biobank: the biobank to upload
        :raises HTTPError: if the request to blaze fails
        :return: the fhir id of the uploaded biobank"""

        biobank_json = biobank.to_fhir().as_json()
        response = self._session.post(f"{self._blaze_url}/Organization", json=biobank_json)
        response.raise_for_status()
        return response.json()["id"]

    def upload_collection_organization(self, collection_org: CollectionOrganization,
                                       managing_biobank_fhir_id: str = None) -> str:
        """Upload a collection organization resource to a blaze
        :param collection_org: collection organization resource to upload
        :param managing_biobank_fhir_id: fhir id of the biobank responsible for this collection
        :raises: HTTPError: if the request to blaze fails
        :return: the fhir id of the uploaded collection organization"""

        managing_biobank_fhir_id = managing_biobank_fhir_id or collection_org.managing_biobank_fhir_id
        if managing_biobank_fhir_id is None:
            managing_biobank_fhir_id = self.get_fhir_id("Organization", collection_org.managing_biobank_id)
        collection_org_json = collection_org.to_fhir(managing_biobank_fhir_id).as_json()
        response = self._session.post(f"{self._blaze_url}/Organization", json=collection_org_json)
        response.raise_for_status()
        return response.json()["id"]

    def upload_collection(self, collection: Collection, managing_collection_org_fhir_id: str = None,
                          sample_fhir_ids: list[str] = None) -> str:
        """
        Upload a collection resource to blaze.
        :param collection: collection resource to upload
        :param managing_collection_org_fhir_id: fhir id of the collection organization that is linked to this collection
        :param sample_fhir_ids: list of sample fhir ids that belong to this collection
        :raises: HTTPError: if the request to blaze fails
        :return: the fhir id of the uploaded collection
        """

        managing_collection_org_fhir_id = managing_collection_org_fhir_id or collection.managing_collection_org_fhir_id
        sample_fhir_ids = sample_fhir_ids or collection.sample_fhir_ids
        if managing_collection_org_fhir_id is None:
            managing_collection_org_fhir_id = self.get_fhir_id("Organization", collection.managing_collection_org_id)
        if sample_fhir_ids is None:
            sample_fhir_ids = [self.get_fhir_id("Specimen", sample_id) for sample_id in collection.sample_ids]
        collection_json = collection.to_fhir(managing_collection_org_fhir_id, sample_fhir_ids)
        response = self._session.post(f"{self._blaze_url}/Group", json=collection_json)
        response.raise_for_status()
        return response.json()["id"]

    def upload_network_organization(self, network_org: NetworkOrganization,
                                    managing_biobank_fhir_id: str = None) -> str:
        """
        Upload a network organization resource to blaze.
        :param network_org: network organization resource to upload
        :param managing_biobank_fhir_id: fhir id of the biobank responsible for this network
        :raises: HTTPError: if the request to blaze fails
        :return: the fhir id of uploaded network organization
        """
        managing_biobank_fhir_id = managing_biobank_fhir_id or network_org.managing_biobank_fhir_id
        if managing_biobank_fhir_id is None:
            managing_biobank_fhir_id = self.get_fhir_id("Organization", network_org.managing_biobank_id)
        network_org_json = network_org.to_fhir(managing_biobank_fhir_id)
        response = self._session.post(f"{self._blaze_url}/Organization", json=network_org_json)
        response.raise_for_status()
        return response.json()["id"]

    def upload_network(self, network: Network, managing_network_org_fhir_id: str = None) -> str:
        """
        Upload a network resource to blaze.
        :param network: network resource to upload
        :param managing_network_org_fhir_id: fhir id of the network_org that is linked to this network resource
        :raises: HTTPError: if the request to blaze fails
        :return: the fhir id of uploaded network
        """

        managing_network_org_fhir_id = managing_network_org_fhir_id or network.managing_network_org_fhir_id
        if managing_network_org_fhir_id is None:
            managing_network_org_fhir_id = self.get_fhir_id("Organization", network.managing_network_org_id)
        biobank_members_fhir_ids = network.members_biobanks_fhir_ids
        collection_members_fhir_ids = network.members_collections_fhir_ids
        if biobank_members_fhir_ids is None:
            biobank_members_fhir_ids = [self.get_fhir_id("Organization", biobank_id) for biobank_id in
                                        network.members_biobanks_ids]
        if collection_members_fhir_ids is None:
            collection_members_fhir_ids = [self.get_fhir_id("Group", collection_id) for collection_id in
                                           network.members_collections_ids]
        network_org_json = network.to_fhir(managing_network_org_fhir_id, collection_members_fhir_ids,
                                           biobank_members_fhir_ids).as_json()
        response = self._session.post(f"{self._blaze_url}/Group", json=network_org_json)
        response.raise_for_status()
        return response.json()["entry"][0]["resource"]["id"]

    def delete_donor(self, donor_fhir_id: str) -> bool:
        """Delete a donor from blaze. BEWARE: Deleting a donor will also delete all related samples and diagnosis reports.
        :param donor_fhir_id: the fhir id of the donor to delete
        :return: True if the donor was deleted successfully
        :raises HTTPError: if the request to blaze fails
        """
        donor = self.get_fhir_resource_as_json("Patient", donor_fhir_id)
        sample_fhir_ids = [get_nested_value(link, ["target", "reference"]) for link in donor["link"]]
        condition_fhir_id = self.__get_condition_fhir_id_by_patient_identifier(donor_fhir_id)
        for sample_fhir_id in sample_fhir_ids:
            if self.delete_sample(sample_fhir_id):
                return False
        if condition_fhir_id is not None:
            self.delete_condition(condition_fhir_id)
        response = self._session.delete(f"{self._blaze_url}/Patient/{donor_fhir_id}")
        response.raise_for_status()
        return response.status_code == 200 or response.status_code == 204

    def delete_condition(self, condition_fhir_id: str) -> bool:
        """Delete a condition from blaze.
        :param condition_fhir_id: the fhir id of the condition to delete
        :return: True if the condition was deleted successfully
        :raises HTTPError: if the request to blaze fails
        """
        response = self._session.delete(f"{self._blaze_url}/Condition/{condition_fhir_id}")
        response.raise_for_status()
        return response.status_code == 200 or response.status_code == 204

    def delete_sample(self, sample_fhir_id: str) -> bool:
        """Delete a sample from blaze. BEWARE: Deleting a sample will also delete all related diagnosis reports and
        observations.
        :param sample_fhir_id: the fhir id of the sample to delete
        :return: True if the sample was deleted successfully
        :raises HTTPError: if the request to blaze fails
        """
        sample = self.get_fhir_resource_as_json("Specimen", sample_fhir_id)
        patient_fhir_id = (get_nested_value(sample, ["subject", "reference"]))
        condition_fhir_id = self.__get_condition_fhir_id_by_patient_identifier(patient_fhir_id)
        diagnosis_reports_fhir_ids = self.__get_diagnosis_reports_fhir_id_by_sample_identifier(sample_fhir_id)
        for diagnosis_report_fhir_id in diagnosis_reports_fhir_ids:

            if self.__delete_diagnosis_report_reference_from_condition(condition_fhir_id, diagnosis_report_fhir_id):
                return False
            self.delete_diagnosis_report(diagnosis_report_fhir_id)
            if self.delete_diagnosis_report(diagnosis_report_fhir_id):
                return False
        response = self._session.delete(f"{self._blaze_url}/Specimen/{sample_fhir_id}")
        response.raise_for_status()
        return response.status_code == 200 or response.status_code == 204

    def delete_diagnosis_report(self, diagnosis_report_fhir_id: str) -> bool:
        """Delete a diagnosis report from blaze.
        :param diagnosis_report_fhir_id: the fhir id of the diagnosis report to delete
        :param patient_fhir_identifier: the fhir identifier of the patient
        :return: True if the diagnosis report was deleted successfully
        :raises HTTPError: if the request to blaze fails
        """
        diagnosis_report = self.get_fhir_resource_as_json("DiagnosticReport", diagnosis_report_fhir_id)
        observation_fhir_ids = [get_nested_value(result, ["reference"]) for result in diagnosis_report["result"]]
        for observation_fhir_id in observation_fhir_ids:
            self.delete_observation(observation_fhir_id)
        response = self._session.delete(f"{self._blaze_url}/DiagnosticReport/{diagnosis_report_fhir_id}")
        response.raise_for_status()
        return response.status_code == 200 or response.status_code == 204

    def delete_observation(self, observation_fhir_id: str) -> bool:
        """Delete an observation from blaze.
        :param observation_fhir_id: the fhir id of the observation to delete
        :return: True if the observation was deleted successfully
        :raises HTTPError: if the request to blaze fails
        """
        response = self._session.delete(f"{self._blaze_url}/Observation/{observation_fhir_id}")
        response.raise_for_status()
        return response.status_code == 200 or response.status_code == 204

    def __get_diagnosis_reports_fhir_id_by_sample_identifier(self, sample_identifier: str) -> list[str]:
        response = self._session.get(f"{self._blaze_url}/DiagnosticReport?specimen=Specimen/{sample_identifier}")
        response.raise_for_status()
        response_json = response.json()
        diagnosis_reports_fhir_ids = []
        for entry in response_json["entry"]:
            diagnosis_report = entry["resource"]
            diagnosis_report_fhir_id = get_nested_value(diagnosis_report, ["id"])
            if diagnosis_report_fhir_id is not None:
                diagnosis_reports_fhir_ids.append(diagnosis_report_fhir_id)
        return diagnosis_reports_fhir_ids

    def __get_condition_fhir_id_by_patient_identifier(self, patient_identifier: str) -> str:
        response = self._session.get(f"{self._blaze_url}/Condition?subject=Patient/{patient_identifier}")
        response.raise_for_status()
        return response.json()["entry"][0]["resource"]["id"]

    def __delete_diagnosis_report_reference_from_condition(self, condition_fhir_id: str,
                                                           diagnosis_report_fhir_id: str) -> bool:
        condition_response = self._session.get(f"{self._blaze_url}/Condition/{condition_fhir_id}")
        if condition_response.status_code != 200:
            raise requests.HTTPError(
                f"Failed to fetch condition with id {condition_fhir_id}. Check if the id is correct")
        condition_json = condition_response.json()["entry"][0]["resource"]
        resource_type, patient_fhir_id = condition_json["subject"]["reference"].split("/")
        patient_identifier = self.get_identifier_by_fhir_id(resource_type, patient_fhir_id)
        condition = Condition.from_json(condition_json, patient_identifier)
        for diagnosis_report in condition.diagnosis_report_fhir_ids:
            if diagnosis_report == diagnosis_report_fhir_id:
                condition._diagnosis_report_fhir_ids.remove(diagnosis_report)
        condition_fhir = condition.add_fhir_id_to_condition(condition.to_fhir())
        return self.update_fhir_resource("Condition", condition_fhir_id, condition_fhir.as_json())
