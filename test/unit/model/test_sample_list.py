import unittest

from MIABIS_on_FHIR.MoF_sample_list import SampleList


class TestSampleList(unittest.TestCase):

    def test_sample_list_init(self):
        sample_list = SampleList("collectionId", ["sampleId"])
        self.assertIsInstance(sample_list, SampleList)
        self.assertEqual("collectionId", sample_list.collection_identifier)
        self.assertEqual(["sampleId"], sample_list.samples_identifiers)

    def test_sample_list_invalid_collection_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            SampleList(37, ["sampleId"])

    def test_sample_list_invalid_samples_identifiers_type_innit(self):
        with self.assertRaises(TypeError):
            SampleList("collectionId", 37)

    def test_sample_list_to_fhir(self):
        sample_list = SampleList("collectionId", ["sampleId"])
        sample_list_fhir = sample_list.to_fhir("collectionFhirId", ["sampleFhirId1", "sampleFhirId2"])
        self.assertEqual("current", sample_list_fhir.status)
        self.assertEqual("working",sample_list_fhir.mode)
        self.assertEqual("Group/collectionFhirId", sample_list_fhir.subject.reference)
        self.assertEqual("Specimen/sampleFhirId1", sample_list_fhir.entry[0].item.reference)
        self.assertEqual("Specimen/sampleFhirId2", sample_list_fhir.entry[1].item.reference)
