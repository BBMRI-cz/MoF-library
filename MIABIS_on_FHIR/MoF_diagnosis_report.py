from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.diagnosticreport import DiagnosticReport
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.identifier import Identifier


class MoFDiagnosisReport:
    """Class representing a diagnosis report in order to link a specimen to a Condition through this diagnosis report.
    as defined by the MIABIS on FHIR profile.
    :param sample_identifier: The identifier of the sample (this is used as a diagnosis report identifier).
    :param donor_identifier: The identifier of the donor.
    """
    def __init__(self, sample_identifier: str, observations_identifiers: list[str]):
        if not isinstance(sample_identifier, str):
            raise TypeError("Sample identifier must be a string.")
        self._sample_identifier = sample_identifier
        for observation_id in observations_identifiers:
            if not isinstance(observation_id, str):
                raise TypeError("Observation identifier must be a string.")
        self._observations_identifiers = observations_identifiers

    @property
    def sample_identifier(self) -> str:
        return self._sample_identifier

    @sample_identifier.setter
    def sample_identifier(self, sample_id: str):
        if not isinstance(sample_id, str):
            raise TypeError("Sample identifier must be a string.")
        self._sample_identifier = sample_id

    @property
    def observations_identifiers(self) -> list[str]:
        return self._observations_identifiers

    @observations_identifiers.setter
    def observations_identifiers(self, observations_ids: list[str]):
        for observation_id in observations_ids:
            if not isinstance(observation_id, str):
                raise TypeError("Observation identifier must be a string.")
        self._observations_identifiers = observations_ids

    def to_fhir(self, sample_fhir_id: str, observation_fhir_ids: list[str]) -> DiagnosticReport:
        """Converts the diagnosis report to a FHIR object.
        :param sample_fhir_id: FHIR identifier of the sample (often given by the server).
        :param observation_fhir_ids: List of FHIR observation identifiers.
        :return: DiagnosticReport
        """
        diagnosis_report = DiagnosticReport()
        diagnosis_report.identifier = [self.__create_identifier()]
        diagnosis_report.specimen = [self.__create_specimen_reference(sample_fhir_id)]
        diagnosis_report.status = "final"
        diagnosis_report.result = self._create_result_reference(observation_fhir_ids)
        diagnosis_report.code = self.__create_code_multiple_diagnosis_bool(len(observation_fhir_ids) > 1)
        return diagnosis_report

    def __create_identifier(self,) -> Identifier:
        """Creates a FHIR identifier for the diagnosis report.
        :param sample_id: FHIR identifier of the sample.
        :return: Identifier
        """
        identifier = Identifier()
        identifier.system = "http://example.com/diagnosisReport"
        identifier.value = self.sample_identifier
        return identifier
    @staticmethod
    def __create_code_multiple_diagnosis_bool(multiple_diagnosis: bool):
        code = CodeableConcept()
        code.coding = [Coding()]
        code.coding[0].code = multiple_diagnosis.__str__()
        code.coding[0].system = "http://example.com/multipleDiagnosis"
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
