from typing import Self

from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.diagnosticreport import DiagnosticReport
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta

from src.MIABIS_on_FHIR.util._constants import DEFINITION_BASE_URL
from src.MIABIS_on_FHIR.util._parsing_util import get_nested_value, parse_reference_id
from src.MIABIS_on_FHIR.util._util import create_fhir_identifier
from src.MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException


class DiagnosisReport:
    """Class representing a diagnosis report in order to link a specimen to a Condition through this diagnosis report.
    as defined by the MIABIS on FHIR profile.
    """

    def __init__(self, sample_identifier: str, observations_identifiers: list[str]):
        """
        :param sample_identifier: The identifier of the sample (this is used as a diagnosis report identifier).
        :param observations_identifiers: List of identifiers of the observations that are related to this diagnosis report.f
        """
        self.sample_identifier = sample_identifier
        self.observations_identifiers = observations_identifiers
        self._diagnosis_report_fhir_id = None
        self._observations_fhir_identifiers = None
        self._sample_fhir_id = None

    @property
    def sample_identifier(self) -> str:
        return self._sample_identifier

    @sample_identifier.setter
    def sample_identifier(self, sample_id: str):
        if sample_id is not None and not isinstance(sample_id, str):
            raise TypeError("Sample identifier must be a string.")
        self._sample_identifier = sample_id

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
    def diagnosis_report_fhir_id(self) -> str:
        return self._diagnosis_report_fhir_id

    @property
    def observations_fhir_identifiers(self) -> list[str]:
        return self._observations_fhir_identifiers

    @property
    def sample_fhir_id(self) -> str:
        return self._sample_fhir_id

    @classmethod
    def from_json(cls, diagnosis_report: dict, observations_identifiers: list[str]) -> Self:
        """
        parse the json into the MoFDiagnosisReport object.
        :param diagnosis_report: json representing the diagnosis report.
        :param observations_identifiers: observations_identifiers (not FHIR ids) that are related to this diagnosis report.
        :return: MoFDiagnosisReport object.
        """
        try:
            diagnosis_report_fhir_id = get_nested_value(diagnosis_report, ["id"])
            identifier = get_nested_value(diagnosis_report, ["identifier", 0, "value"])
            observations_fhir_identifiers = cls._parse_observation_ids(get_nested_value(diagnosis_report, ["result"]))
            sample_fhir_id = parse_reference_id(get_nested_value(diagnosis_report, ["specimen", 0, "reference"]))
            instance = cls(identifier, observations_identifiers)
            instance._diagnosis_report_fhir_id = diagnosis_report_fhir_id
            instance._observations_fhir_identifiers = observations_fhir_identifiers
            instance._sample_fhir_id = sample_fhir_id
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

    def to_fhir(self, sample_fhir_id: str = None, observation_fhir_ids: list[str] = None) -> DiagnosticReport:
        """Converts the diagnosis report to a FHIR object.
        :param sample_fhir_id: FHIR identifier of the sample (often given by the server).
        :param observation_fhir_ids: List of FHIR observation identifiers.
        :return: DiagnosticReport
        """
        sample_fhir_id = sample_fhir_id or self.sample_fhir_id
        observation_fhir_ids = observation_fhir_ids or self.observations_fhir_identifiers
        if sample_fhir_id is None:
            raise ValueError("Sample FHIR identifier must be provided either as an argument or as a property.")
        if observation_fhir_ids is None:
            raise ValueError("Observation FHIR identifiers must be provided either as an argument or as a property.")

        diagnosis_report = DiagnosticReport()
        diagnosis_report.meta = Meta()
        diagnosis_report.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/DiagnosisReport"]
        diagnosis_report.identifier = [create_fhir_identifier(self.sample_identifier)]
        diagnosis_report.specimen = [self.__create_specimen_reference(sample_fhir_id)]
        diagnosis_report.status = "final"
        diagnosis_report.result = self._create_result_reference(observation_fhir_ids)
        diagnosis_report.code = self.__create_code_multiple_diagnosis_bool(len(observation_fhir_ids) > 1)
        return diagnosis_report

    def add_fhir_id_to_diagnosis_report(self, diagnosis_report: DiagnosticReport) -> DiagnosticReport:
        """Add FHIR id to the FHIR representation of the DiagnosisReport. FHIR ID is necessary for updating the
                        resource on the server.This method should only be called if the DiagnosisReport object was created by the
                        from_json method. Otherwise,the diagnosis_report_fhir_id attribute is None,
                        as the FHIR ID is generated by the server and is not known in advance."""
        diagnosis_report.id = self.diagnosis_report_fhir_id
        return diagnosis_report

    @staticmethod
    def __create_code_multiple_diagnosis_bool(multiple_diagnosis: bool):
        code = CodeableConcept()
        code.coding = [Coding()]
        code.coding[0].code = multiple_diagnosis.__str__()
        code.coding[0].system = DEFINITION_BASE_URL + "/multipleDiagnosis"
        return code

    @staticmethod
    def __create_specimen_reference(sample_id: str) -> FHIRReference:
        """Creates a reference to the specimen.
        :param sample_id: FHIR identifier of the sample.
        :return: FHIRReference
        """
        reference = FHIRReference()
        reference.reference = f"Specimen/{sample_id}"
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
