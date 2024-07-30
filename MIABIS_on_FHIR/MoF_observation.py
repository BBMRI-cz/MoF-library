import icd10
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.identifier import Identifier
from fhirclient.models.observation import Observation


class MoFObservation:
    """Class representing Observation containing an ICD-10 code of deasese as defined by the MIABIS on FHIR profile."""

    def __init__(self, icd10_code: str, sample_identifier: str):
        """
        :param icd10_code: icd10 code of the disease
        :param sample_identifier: identifier of the sample that this observation is related to
        (this is used as an identifier for the observation)
        """
        if not icd10.exists(icd10_code):
            raise ValueError("The provided string is not a valid ICD-10 code.")
        self._icd10_code = icd10_code
        if not isinstance(sample_identifier, str):
            raise TypeError("Sample identifier must be a string.")
        self._sample_identifier = sample_identifier

    @property
    def icd10_code(self):
        return self._icd10_code

    @icd10_code.setter
    def icd10_code(self, icd10_code: str):
        if not icd10.exists(icd10_code):
            raise ValueError("The provided string is not a valid ICD-10 code.")
        self._icd10_code = icd10_code

    @property
    def sample_identifier(self):
        return self._sample_identifier

    @sample_identifier.setter
    def sample_identifier(self, donor_identifier: str):
        if not isinstance(donor_identifier, str):
            raise TypeError("Sample identifier must be a string.")
        self._sample_identifier = donor_identifier

    def to_fhir(self) -> Observation:
        """Converts the observation to a FHIR object.
        :param sample_fhir_id: FHIR identifier of the sample (often given by the server).
        :return: Observation
        """
        observation = Observation()
        observation.identifier = self.__create_fhir_identifier(self._sample_identifier)
        observation.status = "final"
        observation.code = self.__create_icd_10_code()
        # observation.valueCodeableConcept = self.__create_icd_10_code()
        return observation

    def __create_icd_10_code(self):
        code = CodeableConcept()
        code.coding = [Coding()]
        code.coding[0].code = self.__diagnosis_with_period()
        code.coding[0].system = "http://hl7.org/fhir/sid/icd-10"
        return code

    def __diagnosis_with_period(self, ) -> str:
        """Returns icd-10 code with a period, e.g., C188 to C18.8"""
        code = self.icd10_code
        if len(code) == 4 and "." not in code:
            return code[:3] + '.' + code[3:]
        return code

    def __create_fhir_identifier(self, sample_fhir_id: str) -> list[Identifier]:
        """Create fhir identifier."""
        fhir_identifier = Identifier()
        fhir_identifier.value = sample_fhir_id
        return [fhir_identifier]
