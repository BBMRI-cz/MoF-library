from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.diagnosticreport import DiagnosticReport
from fhirclient.models.fhirreference import FHIRReference


class MoFDiagnosisReport:
    """Class representing a diagnosis report in order to link a specimen to a Condition through this diagnosis report.
    as defined by the MIABIS on FHIR profile.
    :param sample_identifier: The identifier of the sample.
    """
    def __init__(self, sample_identifier: str, donor_identifier: str):
        self._sample_identifier = sample_identifier
        self._donor_identifier = donor_identifier

    @property
    def sample_id(self) -> str:
        return self._sample_identifier

    @property
    def donor_id(self) -> str:
        return self._donor_identifier

    def to_fhir(self, sample_id: str, observation_ids: list[str]) -> DiagnosticReport:
        """Converts the diagnosis report to a FHIR object.
        :param sample_id: FHIR identifier of the sample (often given by the server).
        :param observation_ids: List of FHIR observation identifiers.
        :return: DiagnosticReport
        """
        diagnosis_report = DiagnosticReport()
        diagnosis_report.specimen = [self.__create_specimen_reference(sample_id)]
        diagnosis_report.status = "final"
        diagnosis_report.result = self._create_result_reference(observation_ids)
        diagnosis_report.code = self.__create_code_multiple_diagnosis_bool(len(observation_ids) > 1)
        return diagnosis_report

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
