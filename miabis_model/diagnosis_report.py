from typing import Self

from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.diagnosticreport import DiagnosticReport
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta

from miabis_model.incorrect_json_format import IncorrectJsonFormatException
from miabis_model.util.config import FHIRConfig
from miabis_model.util.parsing_util import get_nested_value, parse_reference_id
from miabis_model.util.util import create_fhir_identifier


class DiagnosisReport:
    """Class representing a diagnosis report in order to link a specimen to a Condition through this diagnosis report.
    as defined by the MIABIS on FHIR profile.
    """

    def __init__(self, sample_identifier: str, patient_identifier: str, observations_identifiers: list[str] = None,
                 diagnosis_report_identifier: str = None):
        """
        :param sample_identifier: The identifier of the sample that this diagnosis report is linked to.
        :param patient_identifier: The identifier of the patient that this diagnosis report is linked to.
        :param observations_identifiers: List of identifiers of the observations that are related to this diagnosis report.
        There is no need to specify this list, as the observations do not have required ids
        :param diagnosis_report_identifier: The identifier of this diagnosis report (if such exists)
        """
        self.sample_identifier = sample_identifier
        self.patient_identifier = patient_identifier
        self.observations_identifiers = observations_identifiers
        self.diagnosis_report_identifier = diagnosis_report_identifier
        self._diagnosis_report_fhir_id = None
        self._observations_fhir_identifiers = None
        self._sample_fhir_id = None
        self._patient_fhir_id = None

    @property
    def sample_identifier(self) -> str:
        return self._sample_identifier

    @sample_identifier.setter
    def sample_identifier(self, sample_id: str):
        if sample_id is not None and not isinstance(sample_id, str):
            raise TypeError("Sample identifier must be a string.")
        self._sample_identifier = sample_id

    @property
    def patient_identifier(self) -> str:
        return self._patient_identifier

    @patient_identifier.setter
    def patient_identifier(self, patient_identifier: str):
        if not isinstance(patient_identifier, str):
            raise TypeError("Patient identifier must be a string.")
        self._patient_identifier = patient_identifier

    @property
    def observations_identifiers(self) -> list[str]:
        return self._observations_identifiers

    @observations_identifiers.setter
    def observations_identifiers(self, observations_ids: list[str]):
        if observations_ids is not None:
            if not isinstance(observations_ids, list):
                raise TypeError("Observation identifiers must be a list.")
            for observation_id in observations_ids:
                if not isinstance(observation_id, str):
                    raise TypeError("Observation identifier must be a string.")
        self._observations_identifiers = observations_ids

    @property
    def diagnosis_report_identifier(self) -> str:
        return self._diagnosis_report_identifier

    @diagnosis_report_identifier.setter
    def diagnosis_report_identifier(self, diagnosis_report_identifier: str):
        if diagnosis_report_identifier is not None and not isinstance(diagnosis_report_identifier, str):
            raise TypeError("Diagnosis report identifier must be a string")
        self._diagnosis_report_identifier = diagnosis_report_identifier

    @property
    def diagnosis_report_fhir_id(self) -> str:
        return self._diagnosis_report_fhir_id

    @property
    def observations_fhir_identifiers(self) -> list[str]:
        return self._observations_fhir_identifiers

    @property
    def sample_fhir_id(self) -> str:
        return self._sample_fhir_id

    @property
    def patient_fhir_id(self) -> str:
        return self._patient_fhir_id

    @classmethod
    def from_json(cls, diagnosis_report: dict, sample_identifier: str, patient_identifier: str,
                  observations_identifiers: list[str] = None) -> Self:
        """
        parse the json into the MoFDiagnosisReport object.
        :param diagnosis_report: json representing the diagnosis report.
        :param sample_identifier: id of sample that this diagnosis report is linked to.
        :param patient_identifier: id of patient that this diagnosis report is linked to.
        :param observations_identifiers: observations_identifiers (not FHIR ids) that are related to this diagnosis report.
        :return: MoFDiagnosisReport object.
        """
        try:
            diagnosis_report_fhir_id = get_nested_value(diagnosis_report, ["id"])
            identifier = get_nested_value(diagnosis_report, ["identifier", 0, "value"])
            result_references = get_nested_value(diagnosis_report, ["result"])
            observations_fhir_identifiers = None
            if result_references is not None:
                observations_fhir_identifiers = cls._parse_observation_ids(get_nested_value(diagnosis_report, ["result"]))
            sample_fhir_id = parse_reference_id(get_nested_value(diagnosis_report, ["specimen", 0, "reference"]))
            patient_fhir_id = parse_reference_id(get_nested_value(diagnosis_report, ["subject", "reference"]))
            instance = cls(sample_identifier, patient_identifier, observations_identifiers, identifier)
            instance._diagnosis_report_fhir_id = diagnosis_report_fhir_id
            instance._observations_fhir_identifiers = observations_fhir_identifiers
            instance._sample_fhir_id = sample_fhir_id
            instance._patient_fhir_id = patient_fhir_id
            return instance
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into the MoFDiagnosisReport")

    @staticmethod
    def _parse_observation_ids(observations: list[dict]) -> list[str]:
        """
        Parse the observations into a list of observation identifiers.
        :param observations: list of observations.
        :return: list of observation identifiers.
        """
        observations_identifiers = []
        for observation in observations:
            observation_id = parse_reference_id(get_nested_value(observation, ["reference"]))
            observations_identifiers.append(observation_id)
        return observations_identifiers

    def to_fhir(self, sample_fhir_id: str = None, patient_fhir_id: str = None,
                observation_fhir_ids: list[str] = None) -> DiagnosticReport:
        """Converts the diagnosis report to a FHIR object.
        :param sample_fhir_id: FHIR identifier of the sample (often given by the server).
        :param observation_fhir_ids: List of FHIR observation identifiers.
        :return: DiagnosticReport
        """
        sample_fhir_id = sample_fhir_id or self.sample_fhir_id
        patient_fhir_id = patient_fhir_id or self.patient_fhir_id
        observation_fhir_ids = observation_fhir_ids or self.observations_fhir_identifiers
        if sample_fhir_id is None:
            raise ValueError("Sample FHIR identifier must be provided either as an argument or as a property.")
        if observation_fhir_ids is None:
            observation_fhir_ids = []
            # raise ValueError("Observation FHIR identifiers must be provided either as an argument or as a property.")
        if patient_fhir_id is None:
            raise ValueError("Patient FHIR identifier must be provided either as an argument or as a property.")

        diagnosis_report = DiagnosticReport()
        diagnosis_report.meta = Meta()
        diagnosis_report.meta.profile = [FHIRConfig.get_meta_profile_url("diagnosis_report")]
        if self.diagnosis_report_identifier is not None:
            diagnosis_report.identifier = [create_fhir_identifier(self.diagnosis_report_identifier)]
        diagnosis_report.specimen = [self.__create_reference("Specimen", sample_fhir_id)]
        diagnosis_report.subject = self.__create_reference("Patient", patient_fhir_id)
        diagnosis_report.status = "final"
        diagnosis_report.result = self._create_result_reference(observation_fhir_ids)
        diagnosis_report.code = self.__create_loinc_code()
        return diagnosis_report

    def add_fhir_id_to_diagnosis_report(self, diagnosis_report: DiagnosticReport) -> DiagnosticReport:
        """Add FHIR id to the FHIR representation of the DiagnosisReport. FHIR ID is necessary for updating the
                        resource on the server.This method should only be called if the DiagnosisReport object was created by the
                        from_json method. Otherwise,the diagnosis_report_fhir_id attribute is None,
                        as the FHIR ID is generated by the server and is not known in advance."""
        diagnosis_report.id = self.diagnosis_report_fhir_id
        return diagnosis_report

    @staticmethod
    def __create_loinc_code() -> CodeableConcept:
        code = CodeableConcept()
        code.coding = [Coding()]
        code.coding[0].code = "52797-8"
        code.coding[0].system = "http://loinc.org"
        return code

    @staticmethod
    def __create_reference(resource_type: str, sample_id: str) -> FHIRReference:
        """Creates a reference to the specimen.
        :param sample_id: FHIR identifier of the sample.
        :return: FHIRReference
        """
        reference = FHIRReference()
        reference.reference = f"{resource_type.capitalize()}/{sample_id}"
        return reference

    @staticmethod
    def _create_result_reference(sample_id: list[str]) -> list[FHIRReference]:
        """Creates a list of FHIR references to the observations.
        :param sample_id: List of FHIR observation identifiers.
        :return: List of FHIRReference
        """
        result = []
        for observation_id in sample_id:
            reference = FHIRReference()
            reference.reference = f"Observation/{observation_id}"
            result.append(reference)
        return result
