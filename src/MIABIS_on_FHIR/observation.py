from typing import Self

import fhirclient.models.observation as fhir_observation
import simple_icd_10 as icd10
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.meta import Meta

from src.MIABIS_on_FHIR.util._constants import DEFINITION_BASE_URL
from src.MIABIS_on_FHIR.util._parsing_util import get_nested_value
from src.MIABIS_on_FHIR.util._util import create_fhir_identifier
from src.MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException


class Observation:
    """Class representing Observation containing an ICD-10 code of deasese as defined by the MIABIS on FHIR profile."""

    def __init__(self, icd10_code: str, sample_identifier: str):
        """
        :param icd10_code: icd10 code of the disease
        :param sample_identifier: identifier of the sample that this observation is related to
        (this is used as an identifier for the observation)
        """
        if not icd10.is_valid_item(icd10_code):
            raise ValueError("The provided string is not a valid ICD-10 code.")
        self._icd10_code = icd10_code
        if not isinstance(sample_identifier, str):
            raise TypeError("Sample identifier must be a string.")
        self._sample_identifier = sample_identifier
        self._observation_fhir_id = None

    @property
    def icd10_code(self):
        return self._icd10_code

    @icd10_code.setter
    def icd10_code(self, icd10_code: str):
        if not icd10.is_valid_item(icd10_code):
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

    @property
    def observation_fhir_id(self):
        return self._observation_fhir_id

    @classmethod
    def from_json(cls, observation_json: dict) -> Self:
        try:
            observation_fhir_id = get_nested_value(observation_json, ["id"])
            icd10_code = get_nested_value(observation_json, ["code", "coding", 0, "code"])
            identifier = get_nested_value(observation_json, ["identifier", 0, "value"])
            instance = cls(icd10_code, identifier)
            instance._observation_fhir_id = observation_fhir_id
            return instance
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into the MoFObservation")

    def to_fhir(self) -> fhir_observation.Observation:
        """Converts the observation to a FHIR object.
        :return: Observation
        """
        observation = fhir_observation.Observation()
        observation.meta = Meta()
        observation.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Observation"]
        observation.identifier = [create_fhir_identifier(self._sample_identifier)]
        observation.status = "final"
        observation.code = self.__create_sample_diangosis_code()
        observation.valueCodeableConcept = self.__create_icd_10_code()
        return observation

    def _add_fhir_id_to_observation(self, observation: fhir_observation.Observation):
        observation.id = self._observation_fhir_id

    def __create_sample_diangosis_code(self):
        code = CodeableConcept()
        code.coding = [Coding()]
        code.coding[0].code = "sample_diagnosis"
        code.coding[0].system = DEFINITION_BASE_URL + "/observationName"
        return code

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

    def add_fhir_id_to_observation(self, observation: fhir_observation.Observation) -> fhir_observation.Observation:
        """Add FHIR id to the FHIR representation of the Observation. FHIR ID is necessary for updating the
            resource on the server.This method should only be called if the Observation object was created by the
            from_json method. Otherwise,the observation_fhir_id attribute is None,
            as the FHIR ID is generated by the server and is not known in advance."""
        observation.id = self._observation_fhir_id
        return observation