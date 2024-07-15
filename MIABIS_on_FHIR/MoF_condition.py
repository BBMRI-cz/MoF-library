import icd10
import fhirclient.models.condition as fhir_condition
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta


class MoFCondition:
    """Class representing a patients medical condition as defined by the MIABIS on FHIR profile."""

    def __init__(self,patient_identifier: str, icd_10_code: str = None):
        """
        :param icd_10_code: code of the diagnosis.
        THIS DIAGNOSIS REPRESENT CONDITION OF PATIENT THAT BIOBANK DOES NOT HAVE SPECIMEN FOR.
        It could be for example diabetes, which was not diagnosed by the biobank.
        :param patient_identifier: patient identifier given by the organization.
        :param diagnosis_report_fhir_id: diagnosis report identifier given by the FHIR storage.
        """
        if icd_10_code is not None and not icd10.exists(icd_10_code):
            raise TypeError(f"The provided string {icd_10_code} is not a valid ICD-10 code.")
        self._icd_10_code = icd_10_code
        self._patient_identifier = patient_identifier

    @property
    def icd_10_code(self) -> str:
        return self._icd_10_code

    @property
    def patient_identifier(self) -> str:
        return self._patient_identifier

    def to_fhir(self, patient_id: str, diagnosis_report_ids: list[str]):
        """Return condition's representation as a FHIR resource.
        @patient_id: FHIR Resource ID of the patient.
        @diagnosis_report_id: FHIR Resource ID of the diagnosis report."""
        condition = fhir_condition.Condition()
        condition.meta = Meta()
        condition.meta.profile = ["https://example.org/StructureDefinition/Condition"]
        if self.icd_10_code is not None:
            condition.code = self.__create_icd_10_code()
        condition.subject = FHIRReference()
        condition.subject.reference = f"Patient/{patient_id}"
        condition.stage = [fhir_condition.ConditionStage()]
        condition.stage[0].assessment = []
        for diagnosis_report_id in diagnosis_report_ids:
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
