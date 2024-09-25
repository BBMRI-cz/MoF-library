from typing import Self
import fhirclient.models.condition as fhir_condition
import simple_icd_10 as icd10
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta

from MIABIS_on_FHIR._constants import DEFINITION_BASE_URL
from MIABIS_on_FHIR._parsing_util import get_nested_value, parse_reference_id
from MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException


class Condition:
    """Class representing a patients medical condition as defined by the MIABIS on FHIR profile."""

    def __init__(self, patient_identifier: str, icd_10_code: str = None):
        """
        :param icd_10_code: code of the diagnosis.
        THIS DIAGNOSIS REPRESENT CONDITION OF PATIENT THAT BIOBANK DOES NOT HAVE SPECIMEN FOR.
        It could be for example diabetes, which was not diagnosed by the biobank.
        :param patient_identifier: patient identifier given by the organization.
        """
        self.icd_10_code = icd_10_code
        self.patient_identifier = patient_identifier
        self._condition_fhir_id = None
        self._patient_fhir_id = None
        self._diagnosis_report_fhir_ids = None

    @property
    def icd_10_code(self) -> str:
        return self._icd_10_code

    @icd_10_code.setter
    def icd_10_code(self, icd_10_code):
        if icd_10_code is not None and not icd10.is_valid_item(icd_10_code):
            raise ValueError(f"The provided string {icd_10_code} is not a valid ICD-10 code.")
        self._icd_10_code = icd_10_code

    @property
    def patient_identifier(self) -> str:
        return self._patient_identifier

    @patient_identifier.setter
    def patient_identifier(self, patient_identifier: str):
        if not isinstance(patient_identifier, str):
            raise TypeError("Patient identifier must be a string.")
        self._patient_identifier = patient_identifier

    @property
    def condition_fhir_id(self) -> str:
        return self._condition_fhir_id

    @property
    def patient_fhir_id(self) -> str:
        return self._patient_fhir_id

    @property
    def diagnosis_report_fhir_ids(self) -> list[str]:
        return self._diagnosis_report_fhir_ids

    @classmethod
    def from_json(cls, condition_json: dict, patient_identifier: str) -> Self:
        try:
            condition_id = get_nested_value(condition_json, ["id"])
            patient_fhir_identifier = parse_reference_id(get_nested_value(condition_json, ["subject", "reference"]))
            diagnosis_report_fhir_ids = cls.parse_diagnosis_reports(
                get_nested_value(condition_json, ["stage", 0, "assessment"]))
            icd_10_code = get_nested_value(condition_json, ["code", "coding", 0, "code"])
            instance = cls(patient_identifier, icd_10_code)
            instance._condition_fhir_id = condition_id
            instance._patient_fhir_id = patient_fhir_identifier
            instance._diagnosis_report_fhir_ids = diagnosis_report_fhir_ids
            return instance
        except KeyError as e:
            raise IncorrectJsonFormatException(f"Condition is missing required field: {e}")

    @staticmethod
    def parse_diagnosis_reports(assessments: list[dict]) -> list[str]:
        """Parses diagnosis reports ids from json representation.
        :param assessments: list of assessments containing diagnosis reports ids.
        """
        diagnosis_ids = []
        for assessment in assessments:
            diagnosis_report_fhir_id = parse_reference_id(get_nested_value(assessment, ["reference"]))
            diagnosis_ids.append(diagnosis_report_fhir_id)
        return diagnosis_ids

    def to_fhir(self, patient_fhir_id: str = None, diagnosis_report_fhir_ids: list[str] = None):
        """Return condition's representation as a FHIR resource.
        @patient_id: FHIR Resource ID of the patient.
        @diagnosis_report_id: FHIR Resource ID of the diagnosis report."""
        patient_fhir_id = patient_fhir_id or self.patient_fhir_id
        if patient_fhir_id is None:
            raise ValueError("Patient FHIR ID must be provided either as an argument or as an property.")

        diagnosis_report_fhir_ids = diagnosis_report_fhir_ids or self.diagnosis_report_fhir_ids
        if not diagnosis_report_fhir_ids:
            raise ValueError("Diagnosis report FHIR IDs must be provided either as an argument or as an property.")

        condition = fhir_condition.Condition()
        condition.meta = Meta()
        condition.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Condition"]
        if self.icd_10_code is not None:
            condition.code = self.__create_icd_10_code()
        condition.subject = FHIRReference()
        condition.subject.reference = f"Patient/{patient_fhir_id}"
        condition.stage = [fhir_condition.ConditionStage()]
        condition.stage[0].assessment = []
        for diagnosis_report_id in diagnosis_report_fhir_ids:
            condition.stage[0].assessment.append(self.__create_diagnostic_report_reference(diagnosis_report_id))

        return condition

    @staticmethod
    def __create_diagnostic_report_reference(diagnosis_report_id: str) -> FHIRReference:
        """Creates a reference to the diagnostic report.
        :param diagnosis_report_id: FHIR identifier of the diagnostic report.
        :return: FHIRReference
        """
        reference = FHIRReference()
        reference.reference = f"DiagnosticReport/{diagnosis_report_id}"
        return reference

    def __create_icd_10_code(self):
        code = CodeableConcept()
        code.coding = [Coding()]
        code.coding[0].code = self.__diagnosis_with_period()
        code.coding[0].system = "http://hl7.org/fhir/sid/icd-10"
        return code

    def __diagnosis_with_period(self, ) -> str:
        """Returns icd-10 code with a period, e.g., C188 to C18.8"""
        code = self.icd_10_code
        if len(code) == 4 and "." not in code:
            return code[:3] + '.' + code[3:]
        return code
