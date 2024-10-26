import datetime
import unittest

from src.MIABIS_on_FHIR.observation import Observation


class TestObservation(unittest.TestCase):
    def test_observation_args_ok(self):
        observation = Observation("C51", "sampleId", "patientId")
        self.assertIsInstance(observation, Observation)
        self.assertEqual("C51", observation.icd10_code)
        self.assertEqual("sampleId", observation.sample_identifier)

    def test_observation_invalid_icd10_code_value_innit(self):
        with self.assertRaises(ValueError):
            Observation("C0000", "sampleId", "patientId")

    def test_observation_invalid_sample_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            Observation("C51", 37, "patientId")

    def test_observation_set_icd10_code_ok(self):
        observation = Observation("C51", "sampleId", "patientId")
        observation.icd10_code = "C50"
        self.assertEqual("C50", observation.icd10_code)

    def test_observation_set_icd10_code_invalid(self):
        observation = Observation("C51", "sampleId", "patientId")
        with self.assertRaises(ValueError):
            observation.icd10_code = "C0000"

    def test_observation_set_sample_identifier_ok(self):
        observation = Observation("C51", "sampleId", "patientId")
        observation.sample_identifier = "newId"
        self.assertEqual("newId", observation.sample_identifier)

    def test_observation_set_sample_identifier_invalid(self):
        observation = Observation("C51", "sampleId", "patientId")
        with self.assertRaises(TypeError):
            observation.sample_identifier = 37

    def test_observation_to_fhir_ok(self):
        observation = Observation("C51", "sampleId", "patientId", datetime.datetime(year=2022, month=10, day=10),
                                  "obsId")
        obs_fhir = observation.to_fhir("patientFhirId", "sampleFhirId")
        self.assertEqual("C51", obs_fhir.valueCodeableConcept.coding[0].code)
        self.assertEqual("obsId", obs_fhir.identifier[0].value)
        self.assertEqual("final", obs_fhir.status)
        self.assertEqual("Patient/patientFhirId", obs_fhir.subject.reference)
        self.assertEqual("Specimen/sampleFhirId", obs_fhir.specimen.reference)
        self.assertEqual(datetime.datetime(year=2022, month=10, day=10).date(), obs_fhir.effectiveDateTime.date)

    def test_observation_from_json(self):
        example_observation = Observation("C51", "sampleId", "patientId",
                                          datetime.datetime(year=2022, month=10, day=10))
        example_fhir = example_observation.to_fhir("patientFhirId", "sampleFhirId")
        example_fhir.id = "TestFHIRId"
        observation = Observation.from_json(example_fhir.as_json(), "patientId", "sampleId")
        self.assertEqual(example_observation.icd10_code, observation.icd10_code)
        self.assertEqual(example_observation.sample_identifier, observation.sample_identifier)
        self.assertEqual(example_observation.patient_identifier, observation.patient_identifier)
        self.assertEqual(example_observation.diagnosis_observed_datetime.date(),
                         observation.diagnosis_observed_datetime.date())
        self.assertEqual("TestFHIRId", observation.observation_fhir_id)
        self.assertEqual("sampleFhirId", observation.sample_fhir_id)
        self.assertEqual("patientFhirId", observation.patient_fhir_id)

