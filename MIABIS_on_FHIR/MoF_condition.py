import simple_icd_10 as icd10
import fhirclient.models.condition as fhir_condition
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta

from MIABIS_on_FHIR._constants import DEFINITION_BASE_URL


class MoFCondition:
    """Class representing a patients medical condition as defined by the MIABIS on FHIR profile."""

    def __init__(self, patient_identifier: str, icd_10_code: str = None):
        """
        :param icd_10_code: code of the diagnosis.
        THIS DIAGNOSIS REPRESENT CONDITION OF PATIENT THAT BIOBANK DOES NOT HAVE SPECIMEN FOR.
        It could be for example diabetes, which was not diagnosed by the biobank.
        :param patient_identifier: patient identifier given by the organization.
        """
        if icd_10_code is not None and not icd10.is_valid_item(icd_10_code):
            raise ValueError(f"The provided string {icd_10_code} is not a valid ICD-10 code.")
        self._icd_10_code = icd_10_code
        if not isinstance(patient_identifier, str):
            raise TypeError("Patient identifier must be a string.")
        self._patient_identifier = patient_identifier

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

    def to_fhir(self, patient_fhir_id: str, diagnosis_report_fhir_ids: list[str]):
        """Return condition's representation as a FHIR resource.
        @patient_id: FHIR Resource ID of the patient.
        @diagnosis_report_id: FHIR Resource ID of the diagnosis report."""
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
