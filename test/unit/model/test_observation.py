import unittest

from MIABIS_on_FHIR.observation import Observation


class TestObservation(unittest.TestCase):
    observation_json = {'meta': {'versionId': '3', 'lastUpdated': '2024-07-30T07:48:06.014Z'},
                        'resourceType': 'Observation', 'status': 'final', 'id': 'DEICTRLPII7QE2LD',
                        'code': {'coding': [{'system': 'http://hl7.org/fhir/sid/icd-10', 'code': 'C51'}]},
                        'identifier': [{'value': 'sampleId'}]}

    def test_observation_args_ok(self):
        observation = Observation("C51", "sampleId")
        self.assertIsInstance(observation, Observation)
        self.assertEqual("C51", observation.icd10_code)
        self.assertEqual("sampleId", observation.sample_identifier)

    def test_observation_invalid_icd10_code_value_innit(self):
        with self.assertRaises(ValueError):
            Observation("C0000", "sampleId")

    def test_observation_invalid_sample_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            Observation("C51", 37)

    def test_observation_set_icd10_code_ok(self):
        observation = Observation("C51", "sampleId")
        observation.icd10_code = "C50"
        self.assertEqual("C50", observation.icd10_code)

    def test_observation_set_icd10_code_invalid(self):
        observation = Observation("C51", "sampleId")
        with self.assertRaises(ValueError):
            observation.icd10_code = "C0000"

    def test_observation_set_sample_identifier_ok(self):
        observation = Observation("C51", "sampleId")
        observation.sample_identifier = "newId"
        self.assertEqual("newId", observation.sample_identifier)

    def test_observation_set_sample_identifier_invalid(self):
        observation = Observation("C51", "sampleId")
        with self.assertRaises(TypeError):
            observation.sample_identifier = 37

    def test_observation_to_fhir_ok(self):
        observation = Observation("C51", "sampleId")
        obs_fhir = observation.to_fhir()
        self.assertEqual("C51", obs_fhir.valueCodeableConcept.coding[0].code)
        self.assertEqual("sampleId", obs_fhir.identifier[0].value)
        self.assertEqual("final", obs_fhir.status)

    def test_observation_from_json(self):
        observation = Observation.from_json(self.observation_json)
        self.assertEqual("C51", observation.icd10_code)
        self.assertEqual("sampleId", observation.sample_identifier)
        self.assertEqual("DEICTRLPII7QE2LD", observation.observation_fhir_id)
