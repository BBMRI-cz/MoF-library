from datetime import datetime
from typing import Self

import fhirclient.models.observation as fhir_observation
import simple_icd_10 as icd10
from dateutil import parser as date_parser
from dateutil.parser import ParserError
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.fhirdatetime import FHIRDateTime
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta

from miabis_model.incorrect_json_format import IncorrectJsonFormatException
from miabis_model.util.config import FHIRConfig
from miabis_model.util.parsing_util import get_nested_value, parse_reference_id
from miabis_model.util.util import create_fhir_identifier


class _Observation:
    """Class representing Observation containing an ICD-10 code of deasese as defined by the MIABIS on FHIR profile."""

    def __init__(self, icd10_code: str, sample_identifier: str, patient_identifier: str,
                 diagnosis_observed_datetime: datetime = None, observation_identifier: str = None):
        """
        :param icd10_code: icd10 code of the disease
        :param sample_identifier: identifier of the sample that this observation is related to
        :param diagnosis_observed_datetime: date and time when the diagnosis was made
        :param observation_identifier: identifier of the observation. Not all institutes provide this, so it is optional
        """
        self.icd10_code = icd10_code
        self.sample_identifier = sample_identifier
        self.patient_identifier = patient_identifier
        self.diagnosis_observed_datetime = diagnosis_observed_datetime
        self._observation_identifier = observation_identifier
        self._observation_fhir_id = None
        self._patient_fhir_id = None
        self._sample_fhir_id = None

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
    def patient_identifier(self):
        return self._patient_identifier

    @patient_identifier.setter
    def patient_identifier(self, patient_identifier: str):
        if not isinstance(patient_identifier, str):
            raise TypeError("Patient identifier must be a string.")
        self._patient_identifier = patient_identifier

    @property
    def diagnosis_observed_datetime(self):
        return self._diagnosis_observed_datetime

    @diagnosis_observed_datetime.setter
    def diagnosis_observed_datetime(self, diagnosis_observed_datetime: datetime):
        if diagnosis_observed_datetime is not None and not isinstance(diagnosis_observed_datetime, datetime):
            raise TypeError("Diagnosis observed datetime must be a datetime.")
        self._diagnosis_observed_datetime = diagnosis_observed_datetime

    @property
    def observation_identifier(self):
        return self._observation_identifier

    @observation_identifier.setter
    def observation_identifier(self, observation_identifier: str):
        if observation_identifier is not None and not isinstance(observation_identifier, str):
            raise TypeError("Observation identifier must be a string")
        self._observation_identifier = observation_identifier

    @property
    def observation_fhir_id(self):
        return self._observation_fhir_id

    @property
    def patient_fhir_id(self):
        return self._patient_fhir_id

    @property
    def sample_fhir_id(self):
        return self._sample_fhir_id

    @classmethod
    def from_json(cls, observation_json: dict, patient_identifier: str, sample_identifier: str) -> Self:
        try:
            observation_fhir_id = get_nested_value(observation_json, ["id"])
            icd10_code = get_nested_value(observation_json, ["valueCodeableConcept", "coding", 0, "code"])
            identifier = get_nested_value(observation_json, ["identifier", 0, "value"])
            observation_datetime = cls.__parse_datetime(observation_json)
            patient_fhir_id = parse_reference_id(get_nested_value(observation_json, ["subject", "reference"]))
            sample_fhir_id = parse_reference_id(get_nested_value(observation_json, ["specimen", "reference"]))
            instance = cls(icd10_code, sample_identifier, patient_identifier, observation_datetime, identifier)
            instance._patient_fhir_id = patient_fhir_id
            instance._observation_fhir_id = observation_fhir_id
            instance._sample_fhir_id = sample_fhir_id
            return instance
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into the Observation")
        except ParserError:
            raise IncorrectJsonFormatException("Error occured when parsing effectiveDatetime into the Observation")

    @staticmethod
    def __parse_datetime(observation_json: dict) -> datetime:
        observation_datetime = get_nested_value(observation_json, ["effectiveDateTime"])
        if observation_datetime is not None:
            observation_datetime = date_parser.parse(observation_datetime)
        return observation_datetime

    def to_fhir(self, patient_fhir_id: str = None, sample_fhir_id: str = None) -> fhir_observation.Observation:
        """Converts the observation to a FHIR object.
        patient_fhir_id and sample_fhir_id is not needed if this Observation object was created by from_json method
        (the fhir ids were already taken from the json representation)
        :param patient_fhir_id: FHIR ID of a patient this observation is linked to.
        :param sample_fhir_id: FHIR ID of a sample this observation is linked to.
        :return: Observation
        """
        patient_fhir_id = patient_fhir_id or self.patient_fhir_id
        if patient_fhir_id is None:
            raise ValueError("Patient FHIR ID must be provided either as an argument or as a property")

        sample_fhir_id = sample_fhir_id or self.sample_fhir_id
        if sample_fhir_id is None:
            raise ValueError("Sample FHIR ID must be provided either as an argument or as a property")

        observation = fhir_observation.Observation()
        observation.meta = Meta()
        observation.meta.profile = [FHIRConfig.get_meta_profile_url("observation")]
        if self.observation_identifier is not None:
            observation.identifier = [create_fhir_identifier(self.observation_identifier)]
        observation.subject = self.__create_patient_reference(patient_fhir_id)
        observation.status = "final"
        observation.specimen = self.__create_specimen_reference(sample_fhir_id)
        if self.diagnosis_observed_datetime is not None:
            observation.effectiveDateTime = FHIRDateTime()
            observation.effectiveDateTime.date = self.diagnosis_observed_datetime.date()
        observation.code = self.__create_loinc_code()
        observation.valueCodeableConcept = self.__create_icd_10_code()
        return observation

    @staticmethod
    def __create_patient_reference(patient_fhir_id: str) -> FHIRReference:
        patient_reference = FHIRReference()
        patient_reference.reference = f"Patient/{patient_fhir_id}"
        return patient_reference

    @staticmethod
    def __create_specimen_reference(sample_fhir_id: str) -> FHIRReference:
        specimen_reference = FHIRReference()
        specimen_reference.reference = f"Specimen/{sample_fhir_id}"
        return specimen_reference

    def _add_fhir_id_to_observation(self, observation: fhir_observation.Observation):
        observation.id = self._observation_fhir_id

    @staticmethod
    def __create_loinc_code() -> CodeableConcept:
        code = CodeableConcept()
        code.coding = [Coding()]
        code.coding[0].code = "52797-8"
        code.coding[0].system = "http://loinc.org"
        return code

    def __create_icd_10_code(self) -> CodeableConcept:
        code = CodeableConcept()
        code.coding = [Coding()]
        code.coding[0].code = self.__diagnosis_with_period()
        code.coding[0].system = FHIRConfig.DIAGNOSIS_CODE_SYSTEM
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

    def __eq__(self, other):
        """Check if two observations are equal
        :param other: Observation to compare with"""
        if not isinstance(other, _Observation):
            return False
        return self.icd10_code == other.icd10_code and \
            self.sample_identifier == other.sample_identifier and \
            self.patient_identifier == other.patient_identifier and \
            self.diagnosis_observed_datetime == other.diagnosis_observed_datetime \
            and self._observation_identifier == other.observation_identifier

    def __hash__(self):
        return hash((self.patient_identifier, self.sample_identifier))
