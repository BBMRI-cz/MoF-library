import unittest

from miabis_model import _DiagnosisReport


class TestDiagnosisReport(unittest.TestCase):
    def test_diagnosis_report_init(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId")
        self.assertIsInstance(diagnosis_report, _DiagnosisReport)
        self.assertEqual("sampleId", diagnosis_report.sample_identifier)
        self.assertEqual("donorId", diagnosis_report.patient_identifier)

    def test_diagnosis_report_init_optional_params(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId", ["obsId"], "diagId")
        self.assertIsInstance(diagnosis_report, _DiagnosisReport)
        self.assertEqual("sampleId", diagnosis_report.sample_identifier)
        self.assertEqual("donorId", diagnosis_report.patient_identifier)
        self.assertEqual(["obsId"], diagnosis_report.observations_identifiers)
        self.assertEqual("diagId", diagnosis_report.diagnosis_report_identifier)

    def test_diagnosis_report_invalid_sample_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            _DiagnosisReport(37, "donorId")

    def test_diagnosis_report_invalid_patient_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            _DiagnosisReport("sampleId", 37)

    def test_diagnosis_report_set_sample_identifier_ok(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId")
        diagnosis_report.sample_identifier = "newId"
        self.assertEqual("newId", diagnosis_report.sample_identifier)

    def test_diagnosis_report_set_sample_identifier_invalid(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId")
        with self.assertRaises(TypeError):
            diagnosis_report.sample_identifier = 37

    def test_diagnosis_report_set_patient_identifier_ok(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId")
        diagnosis_report.patient_identifier = "newDonorId"
        self.assertEqual("newDonorId", diagnosis_report.patient_identifier)

    def test_diagnosis_report_set_patient_identifier_invalid(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId")
        with self.assertRaises(TypeError):
            diagnosis_report.observations_identifiers = 37

    def test_diagnosis_report_to_fhir_ok(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId", diagnosis_report_identifier="diagnosisReportId")
        diagnosis_report_fhir = diagnosis_report.to_fhir("sampleFhirId", "donorFhirId", ["obsFhirId"])
        self.assertEqual("diagnosisReportId", diagnosis_report_fhir.identifier[0].value)
        self.assertEqual("Observation/obsFhirId", diagnosis_report_fhir.result[0].reference)
        self.assertEqual("Patient/donorFhirId", diagnosis_report_fhir.subject.reference)
        self.assertEqual("Specimen/sampleFhirId", diagnosis_report_fhir.specimen[0].reference)
        self.assertEqual("final", diagnosis_report_fhir.status)

    def test_diagnosis_report_multiple_observations_ok(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId", observations_identifiers=["obsId", "obsId2"])
        self.assertEqual("obsId", diagnosis_report.observations_identifiers[0])
        self.assertEqual("obsId2", diagnosis_report.observations_identifiers[1])

    def test_diagnosis_report_multiple_observations_to_fhir_ok(self):
        diagnosis_report = _DiagnosisReport("sampleId", "donorId")
        diagnosis_report_fhir = diagnosis_report.to_fhir("sampleFhirId", "donorFhirId", ["obsFhirId", "obsFhirId2"])
        self.assertEqual("Patient/donorFhirId", diagnosis_report_fhir.subject.reference)
        self.assertEqual("Specimen/sampleFhirId", diagnosis_report_fhir.specimen[0].reference)
        self.assertEqual("Observation/obsFhirId", diagnosis_report_fhir.result[0].reference)
        self.assertEqual("Observation/obsFhirId2", diagnosis_report_fhir.result[1].reference)
        self.assertEqual("final", diagnosis_report_fhir.status)

    def test_diagnosis_report_from_json(self):
        example_diagnosis_report = _DiagnosisReport("sampleId", "donorId")
        example_fhir = example_diagnosis_report.to_fhir("sampleFhirId", "donorFhirId", ["obsFhirId", "obsFhirId2"])
        example_fhir.id = "TestFHIRId"
        diagnosis_report = _DiagnosisReport.from_json(example_fhir.as_json(), "sampleId", "donorId")
        # self.assertEqual(example_diagnosis_report.sample_identifier, diagnosis_report.sample_identifier)
        self.assertEqual(example_diagnosis_report, diagnosis_report)
        self.assertEqual("TestFHIRId", diagnosis_report.diagnosis_report_fhir_id)
        self.assertEqual(["obsFhirId", "obsFhirId2"], diagnosis_report.observations_fhir_identifiers)
        self.assertEqual("sampleFhirId", diagnosis_report.sample_fhir_id)
        self.assertEqual("donorFhirId", diagnosis_report.patient_fhir_id)

    def test_diagnosis_report_eq(self):
        dr_1 = _DiagnosisReport("sampleId", "donorId")
        dr_2 = _DiagnosisReport("sampleId", "donorId")
        self.assertEqual(dr_2, dr_1)

    def test_diagnosis_report_not_eq(self):
        dr_1 = _DiagnosisReport("sampleId", "donorId")
        dr_2 = _DiagnosisReport("different_sample_id", "donorId")
        self.assertNotEqual(dr_2,dr_1)