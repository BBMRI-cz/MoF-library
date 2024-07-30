import unittest

from MIABIS_on_FHIR.MoF_network import MoFNetwork


class TestNetwork(unittest.TestCase):

    def test_network_init(self):
        network = MoFNetwork("networkId", "networkName", ["Charter"])
        self.assertIsInstance(network, MoFNetwork)
        self.assertEqual("networkId", network.identifier)
        self.assertEqual("networkName", network.name)
        self.assertEqual(["Charter"], network.common_collaboration_topics)

    def test_network_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            network = MoFNetwork(37, "networkName", ["Charter"])

    def test_network_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            network = MoFNetwork("networkId", 22, ["Charter"])

    def test_network_invalid_common_collaboration_topics_type_innit(self):
        with self.assertRaises(TypeError):
            network = MoFNetwork("networkId", "networkName", 22)

    def test_network_common_collaboration_topics_invalid(self):
        with self.assertRaises(ValueError):
            network = MoFNetwork("networkId", "networkName", ["invalid"])

    def test_network_set_identifier_ok(self):
        network = MoFNetwork("networkId", "networkName", ["Charter"])
        network.identifier = "newId"
        self.assertEqual("newId", network.identifier)

    def test_network_set_identifier_invalid(self):
        network = MoFNetwork("networkId", "networkName", ["Charter"])
        with self.assertRaises(TypeError):
            network.identifier = 37

    def test_network_set_name_ok(self):
        network = MoFNetwork("networkId", "networkName", ["Charter"])
        network.name = "newName"
        self.assertEqual("newName", network.name)

    def test_network_set_name_invalid(self):
        network = MoFNetwork("networkId", "networkName", ["Charter"])
        with self.assertRaises(TypeError):
            network.name = 37

    def test_network_set_common_collaboration_topics_ok(self):
        network = MoFNetwork("networkId", "networkName", ["Charter"])
        network.common_collaboration_topics = ["SOP"]
        self.assertEqual(["SOP"], network.common_collaboration_topics)

    def test_network_set_common_collaboration_topics_invalid(self):
        network = MoFNetwork("networkId", "networkName", ["Charter"])
        with self.assertRaises(ValueError):
            network.common_collaboration_topics = ["invalid"]

    def test_network_to_fhir(self):
        network = MoFNetwork("networkId", "networkName", ["Charter"])
        network_fhir = network.to_fhir()
        self.assertTrue(network_fhir.active)
        self.assertEqual("person", network_fhir.type)
        self.assertEqual("networkName", network_fhir.name)
        self.assertEqual("Charter", network_fhir.extension[0].valueCodeableConcept.coding[0].code)

