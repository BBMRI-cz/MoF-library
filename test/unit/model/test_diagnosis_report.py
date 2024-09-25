import unittest

from MIABIS_on_FHIR.diagnosis_report import DiagnosisReport


class TestDiagnosisReport(unittest.TestCase):
    diagnosis_report_json = {'id': 'ASCXXEDSKHGO',
                             'meta': {'profile': ['http://example.com/StructureDefinition/DiagnosisReport']},
                             'code': {'coding': [{'code': 'True', 'system': 'http://example.com/multipleDiagnosis'}]},
                             'identifier': [{'value': 'sampleId'}], 'result': [{'reference': 'Observation/obsFhirId1'},
                                                                               {'reference': 'Observation/ObsFhirId2'}],
                             'specimen': [{'reference': 'Specimen/sampleFhirId'}], 'status': 'final',
                             'resourceType': 'DiagnosticReport'}

    def test_diagnosis_report_init(self):
        diagnosis_report = DiagnosisReport("sampleId", ["obsId"])
        self.assertIsInstance(diagnosis_report, DiagnosisReport)
        self.assertEqual("sampleId", diagnosis_report.sample_identifier)
        self.assertEqual(["obsId"], diagnosis_report.observations_identifiers)

    def test_diagnosis_report_invalid_sample_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            DiagnosisReport(37, ["obsId"])

    def test_diagnosis_report_invalid_observations_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            DiagnosisReport("sampleId", 37)

    def test_diagnosis_report_set_sample_identifier_ok(self):
        diagnosis_report = DiagnosisReport("sampleId", ["obsId"])
        diagnosis_report.sample_identifier = "newId"
        self.assertEqual("newId", diagnosis_report.sample_identifier)

    def test_diagnosis_report_set_sample_identifier_invalid(self):
        diagnosis_report = DiagnosisReport("sampleId", ["obsId"])
        with self.assertRaises(TypeError):
            diagnosis_report.sample_identifier = 37

    def test_diagnosis_report_set_observations_identifier_ok(self):
        diagnosis_report = DiagnosisReport("sampleId", ["obsId"])
        diagnosis_report.observations_identifiers = ["newIds"]
        self.assertEqual(["newIds"], diagnosis_report.observations_identifiers)

    def test_diagnosis_report_set_observations_identifier_invalid(self):
        diagnosis_report = DiagnosisReport("sampleId", ["obsId"])
        with self.assertRaises(TypeError):
            diagnosis_report.observations_identifiers = 37

    def test_diagnosis_report_to_fhir_ok(self):
        diagnosis_report = DiagnosisReport("sampleId", ["obsId"])
        diagnosis_report_fhir = diagnosis_report.to_fhir("sampleFhirId", ["obsFhirId"])
        self.assertEqual("sampleId", diagnosis_report_fhir.identifier[0].value)
        self.assertEqual("Observation/obsFhirId", diagnosis_report_fhir.result[0].reference)
        self.assertEqual("final", diagnosis_report_fhir.status)

    def test_diagnosis_report_multiple_observations_ok(self):
        diagnosis_report = DiagnosisReport("sampleId", ["obsId", "obsId2"])
        self.assertEqual("obsId", diagnosis_report.observations_identifiers[0])
        self.assertEqual("obsId2", diagnosis_report.observations_identifiers[1])

    def test_diagnosis_report_multiple_observations_to_fhir_ok(self):
        diagnosis_report = DiagnosisReport("sampleId", ["obsId", "obsId2"])
        diagnosis_report_fhir = diagnosis_report.to_fhir("sampleFhirId", ["obsFhirId", "obsFhirId2"])
        self.assertEqual("Observation/obsFhirId", diagnosis_report_fhir.result[0].reference)
        self.assertEqual("Observation/obsFhirId2", diagnosis_report_fhir.result[1].reference)
        self.assertEqual("final", diagnosis_report_fhir.status)

    def test_diagnosis_report_from_json(self):
        diagnosis_report = DiagnosisReport.from_json(self.diagnosis_report_json, ["obsId", "obsId2"])
        self.assertEqual("sampleId", diagnosis_report.sample_identifier)
        self.assertEqual(["obsId", "obsId2"], diagnosis_report.observations_identifiers)
        self.assertEqual("ASCXXEDSKHGO", diagnosis_report.diagnosis_report_fhir_id)
        self.assertEqual(["obsFhirId1", "ObsFhirId2"], diagnosis_report.observations_fhir_identifiers)
