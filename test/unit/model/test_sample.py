import unittest
from datetime import datetime

from MIABIS_on_FHIR.MoF_sample import Sample
from MIABIS_on_FHIR.storage_temperature import StorageTemperature


class TestSample(unittest.TestCase):
    sample_json = {'meta': {'versionId': '2', 'lastUpdated': '2024-08-06T08:14:08.062Z',
                            'profile': ['http://example.com/StructureDefinition/Specimen']},
                   'processing': [{
                       'extension': [
                           {
                               'url': 'http://example.com/StructureDefinition/StorageTemperature',
                               'valueCodeableConcept': {
                                   'coding': [
                                       {
                                           'code': 'temperatureRoom'}]}}]}],
                   'type': {
                       'coding': [{'system': 'http://example.com/ValueSet/miabis-material-type-VS', 'code': 'DNA'}]},
                   'resourceType': 'Specimen', 'note': [{'text': 'use_restric'}], 'id': 'DEJGYCYLDDUJKNVW',
                   'identifier': [{'value': 'sampleId'}], 'collection': {'collectedDateTime': '2022-10-20',
                                                                         'bodySite': {'coding': [
                                                                             {'system': 'bsSystem', 'code': 'Arm'}]}},
                   'subject': {'reference': 'Patient/DEJGYCPFDABXEMWV'}}

    def test_sample_necessary_args(self):
        sample = Sample("sampleId", "donorId", "Blood")
        self.assertIsInstance(sample, Sample)
        self.assertEqual("sampleId", sample.identifier)
        self.assertEqual("donorId", sample.donor_identifier)
        self.assertEqual("Blood", sample.material_type)

    def test_sample_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            sample = Sample(37, "donorId", "Blood")

    def test_sample_invalid_donor_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            sample = Sample("sampleId", 37, "Blood")

    def test_sample_invalid_material_type_type_innit(self):
        with self.assertRaises(ValueError):
            sample = Sample("sampleId", "donorId", "invalid_code")

    def test_sample_set_identifier_ok(self):
        sample = Sample("sampleId", "donorId", "Blood")
        sample.identifier = "newId"
        self.assertEqual("newId", sample.identifier)

    def test_sample_set_identifier_invalid(self):
        sample = Sample("sampleId", "donorId", "Blood")
        with self.assertRaises(TypeError):
            sample.identifier = 37

    def test_sample_set_donor_identifier_ok(self):
        sample = Sample("sampleId", "donorId", "Blood")
        sample.donor_identifier = "newId"
        self.assertEqual("newId", sample.donor_identifier)

    def test_sample_set_donor_identifier_invalid(self):
        sample = Sample("sampleId", "donorId", "Blood")
        with self.assertRaises(TypeError):
            sample.donor_identifier = 37

    def test_sample_set_material_type_ok(self):
        sample = Sample("sampleId", "donorId", "Blood")
        sample.material_type = "DNA"
        self.assertEqual("DNA", sample.material_type)

    def test_sample_set_material_type_invalid(self):
        sample = Sample("sampleId", "donorId", "Blood")
        with self.assertRaises(ValueError):
            sample.material_type = "invalid_code"

    def test_sample_body_site_and_body_system_ok(self):
        sample = Sample("sampleId", "donorId", "Blood")
        sample.body_site = "arm"
        sample.body_site_system = "http://www.example.com"
        self.assertEqual("arm", sample.body_site)
        self.assertEqual("http://www.example.com", sample.body_site_system)

    def test_sample_body_site_and_body_system_invalid(self):
        sample = Sample("sampleId", "donorId", "Blood")
        with self.assertRaises(TypeError):
            sample.body_site = 37
        with self.assertRaises(TypeError):
            sample.body_site_system = 37

    def test_sample_collected_datetime_ok(self):
        sample = Sample("sampleId", "donorId", "Blood")
        collected_date = datetime(year=2022, month=10, day=20)
        sample.collected_datetime = collected_date
        self.assertEqual(collected_date, sample.collected_datetime)

    def test_sample_collected_datetime_invalid(self):
        sample = Sample("sampleId", "donorId", "Blood")
        with self.assertRaises(TypeError):
            sample.collected_datetime = "2022-10-20"

    def test_sample_storage_temperature_ok(self):
        sample = Sample("sampleId", "donorId", "Blood", storage_temperature=StorageTemperature.TEMPERATURE_GN)
        self.assertEqual(StorageTemperature.TEMPERATURE_GN, sample.storage_temperature)

    def test_sample_storage_temperature_invalid(self):
        with self.assertRaises(TypeError):
            sample = Sample("sampleId", "donorId", "Blood", storage_temperature="invalid")

    def test_sample_use_restrictions_ok(self):
        sample = Sample("sampleId", "donorId", "Blood", use_restrictions="No restrictions")
        self.assertEqual("No restrictions", sample.use_restrictions)

    def test_sample_use_restrictions_invalid(self):
        with self.assertRaises(TypeError):
            sample = Sample("sampleId", "donorId", "Blood", use_restrictions=37)

    def test_sample_to_fhir_necessary_args_ok(self):
        sample = Sample("sampleId", "donorId", "Blood")
        sample_fhir = sample.to_fhir("donorFhirId")
        self.assertEqual("sampleId", sample_fhir.identifier[0].value)
        self.assertEqual("Patient/donorFhirId", sample_fhir.subject.reference)
        self.assertEqual("Blood", sample_fhir.type.coding[0].code)

    def test_sample_to_fhir_all_args_ok(self):
        sample = Sample("sampleId", "donorId", "Blood", storage_temperature=StorageTemperature.TEMPERATURE_GN,
                        use_restrictions="No restrictions")
        sample_fhir = sample.to_fhir("donorFhirId")
        self.assertEqual("sampleId", sample_fhir.identifier[0].value)
        self.assertEqual("Patient/donorFhirId", sample_fhir.subject.reference)
        self.assertEqual("Blood", sample_fhir.type.coding[0].code)
        self.assertEqual("temperatureGN", sample_fhir.processing[0].extension[0].valueCodeableConcept.coding[0].code)
        self.assertEqual("No restrictions", sample_fhir.note[0].text)

    def test_sample_from_json(self):
        sample = Sample.from_json(self.sample_json, "donorId")
        self.assertEqual("sampleId", sample.identifier)
        self.assertEqual("donorId", sample.donor_identifier)
        self.assertEqual("DNA", sample.material_type)
        self.assertEqual(datetime(year=2022, month=10, day=20), sample.collected_datetime)
        self.assertEqual("Arm", sample.body_site)
        self.assertEqual("bsSystem", sample.body_site_system)
        self.assertEqual(StorageTemperature.TEMPERATURE_ROOM, sample.storage_temperature)
        self.assertEqual("use_restric", sample.use_restrictions)
