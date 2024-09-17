import unittest

from MIABIS_on_FHIR.condition import Condition


class TestCondition(unittest.TestCase):

    def test_condition_init(self):
        condition = Condition("patientId")
        self.assertIsInstance(condition, Condition)
        self.assertEqual("patientId", condition.patient_identifier)

    def test_condition_invalid_patient_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            Condition(37)

    def test_condition_set_patient_identifier_ok(self):
        condition = Condition("patientId")
        condition.patient_identifier = "newId"
        self.assertEqual("newId", condition.patient_identifier)

    def test_condition_set_patient_identifier_invalid(self):
        condition = Condition("patientId")
        with self.assertRaises(TypeError):
            condition.patient_identifier = 37


    def test_condition_with_diagnosis_code_ok(self):
        condition = Condition("patientId", "C51")
        self.assertEqual("C51", condition.icd_10_code)

    def test_condition_with_wrong_diagnosis_code(self):
        with self.assertRaises(ValueError):
            condition = Condition("patientId", "C0000")

    def test_condition_set_diagnosis_code_ok(self):
        condition = Condition("patientId", "C51")
        condition.icd_10_code = "C50"
        self.assertEqual("C50", condition.icd_10_code)

    def test_condition_set_diagnosis_code_invalid(self):
        condition = Condition("patientId", "C51")
        with self.assertRaises(ValueError):
            condition.icd_10_code = "C0000"

    def test_condition_to_fhir_ok(self):
        condition = Condition("patientId", "C51")
        condition_fhir = condition.to_fhir("patientFhirId",["diagnosisFhirId"])
        self.assertEqual("C51", condition_fhir.code.coding[0].code)
        self.assertEqual("Patient/patientFhirId", condition_fhir.subject.reference)
        self.assertEqual("DiagnosticReport/diagnosisFhirId", condition_fhir.stage[0].assessment[0].reference)

    def test_condition_to_fhir_multiple_diagnosis_reports_ok(self):
        condition = Condition("patientId", "C51")
        condition_fhir = condition.to_fhir("patientFhirId",["diagnosisFhirId", "diagnosisFhirId2"])
        self.assertEqual("DiagnosticReport/diagnosisFhirId", condition_fhir.stage[0].assessment[0].reference)
        self.assertEqual("DiagnosticReport/diagnosisFhirId2", condition_fhir.stage[0].assessment[1].reference)