import unittest

from src.MIABIS_on_FHIR.network import Network


class TestNetwork(unittest.TestCase):
    network_json = {'id': 'SKJAOWSQEMJ', 'meta': {'profile': ['http://example.com/StructureDefinition/Network']},
                    'extension': [{'url': 'http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity',
                                   'valueReference': {'reference': 'Group/collFhirId1'}},
                                  {'url': 'http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity',
                                   'valueReference': {'reference': 'Group/collFhirId2'}}, {
                                      'url': 'http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity'
                                      , 'valueReference': {'reference': 'Organization/bioFhirId1'}}, {
                                      'url': 'http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity'
                                      , 'valueReference': {'reference': 'Organization/bioFhirId2'}}], 'active': True,
                    'actual': True, 'identifier': [{'value': 'networkId'}],
                    'managingEntity': {'reference': 'Organization/bioFhirId'}, 'name': 'networkName', 'type': 'person',
                    'resourceType': 'Group'}

    def test_network_init(self):
        network = Network("networkId", "networkName", "biobankId", ["collMemID1, collemMemID2"],
                          ["bioMemID1, bioMemID2"])
        self.assertIsInstance(network, Network)
        self.assertEqual("networkId", network.identifier)
        self.assertEqual("networkName", network.name)
        self.assertEqual(["collMemID1, collemMemID2"], network.members_collections_ids)
        self.assertEqual(["bioMemID1, bioMemID2"], network.members_biobanks_ids)

    def test_network_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            network = Network(37, "networkName", "biobankId")

    def test_network_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            network = Network("networkId", 22, "biobankId")

    def test_network_members_collection_ids_invalid_type(self):
        with self.assertRaises(TypeError):
            network = Network("networkId", "networkName", "biobankId", [5])

    def test_network_members_biobanks_ids_invalid_type(self):
        with self.assertRaises(TypeError):
            network = Network("networkId", "networkName", "biobankId", ["collid"], [5])

    def test_network_set_identifier_ok(self):
        network = Network("networkId", "networkName", "biobankId", ["Charter"])
        network.identifier = "newId"
        self.assertEqual("newId", network.identifier)

    def test_network_set_identifier_invalid(self):
        network = Network("networkId", "networkName", "biobankId", ["collid"])
        with self.assertRaises(TypeError):
            network.identifier = 37

    def test_network_set_name_ok(self):
        network = Network("networkId", "networkName", "biobankId", ["collid"])
        network.name = "newName"
        self.assertEqual("newName", network.name)

    def test_network_set_name_invalid(self):
        network = Network("networkId", "networkName", "biobankId", ["collid"])
        with self.assertRaises(TypeError):
            network.name = 37

    def test_network_set_collection_ids_valid(self):
        network = Network("networkId", "networkName", "biobankId", ["cllid"])
        network.common_collaboration_topics = ["SOP"]
        self.assertEqual(["SOP"], network.common_collaboration_topics)

    def test_network_set_collection_ids_invalid(self):
        network = Network("networkId", "networkName", "biobankId", ["collId"])
        with self.assertRaises(TypeError):
            network.members_collections_ids = [5]

    def test_network_to_fhir(self):
        network = Network("networkId", "networkName", "biobankId", ["collid"])
        network_fhir = network.to_fhir("biobankFhirId", ["collfhirid1", "collfhirid2"],
                                       ["biobankFhirId1", "biobankFhirId2"])
        self.assertTrue(network_fhir.active)
        self.assertEqual("person", network_fhir.type)
        self.assertEqual("networkName", network_fhir.name)
        self.assertEqual("Organization/biobankFhirId", network_fhir.managingEntity.reference)
        self.assertEqual("Group/collfhirid1", network_fhir.extension[0].valueReference.reference)
        self.assertEqual("Group/collfhirid2", network_fhir.extension[1].valueReference.reference)
        self.assertEqual("Organization/biobankFhirId1", network_fhir.extension[2].valueReference.reference)
        self.assertEqual("Organization/biobankFhirId2", network_fhir.extension[3].valueReference.reference)

    def test_network_from_json(self):
        network = Network.from_json(self.network_json, "biobankId", ["collid1", "collid2"],
                                    ["biobankid1", "biobankid2"])
        self.assertIsInstance(network, Network)
        self.assertEqual("networkId", network.identifier)
        self.assertEqual("networkName", network.name)
        self.assertEqual("biobankId", network.managing_network_org_id)
        self.assertEqual(["collid1", "collid2"], network.members_collections_ids)
        self.assertEqual(["biobankid1", "biobankid2"], network.members_biobanks_ids)
        self.assertEqual("SKJAOWSQEMJ", network.network_fhir_id)
        self.assertEqual("bioFhirId", network.managing_network_org_fhir_id)
        self.assertEqual(["collFhirId1", "collFhirId2"], network.members_collections_fhir_ids)
        self.assertEqual(["bioFhirId1", "bioFhirId2"], network.members_biobanks_fhir_ids)
