import unittest

from miabis_model import Network
from miabis_model.network_organization import _NetworkOrganization


class TestNetwork(unittest.TestCase):
    def test_network_init(self):
        network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                          contact_email="contactEmail", country="CZ", juristic_person="juristicPerson",
                          members_collections_ids=["collMemID1, collemMemID2"],
                          members_biobanks_ids=["bioMemID1, bioMemID2"], contact_name="contactName",
                          contact_surname="contactSurname", common_collaboration_topics=["Charter"],
                          description="description")
        self.assertIsInstance(network, Network)
        self.assertEqual("networkId", network.identifier)
        self.assertEqual("networkName", network.name)
        self.assertEqual("managingBiobankId", network.managing_biobank_id)
        self.assertEqual("contactEmail", network.contact_email)
        self.assertEqual("CZ", network.country)
        self.assertEqual("juristicPerson", network.juristic_person)
        self.assertEqual(["collMemID1, collemMemID2"], network.members_collections_ids)
        self.assertEqual(["bioMemID1, bioMemID2"], network.members_biobanks_ids)
        self.assertEqual("contactSurname", network.contact_surname)
        self.assertEqual("contactName", network.contact_name)
        self.assertEqual(["Charter"], network.common_collaboration_topics)
        self.assertEqual("description", network.description)

    def test_network_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            network = Network(identifier=37, name="networkName", managing_biobank_id="managingBiobankId",
                              contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")

    def test_network_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            network = Network(identifier="networkId", name=37, managing_biobank_id="managingBiobankId",
                              contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")

    def test_network_members_collection_ids_invalid_type(self):
        with self.assertRaises(TypeError):
            network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                              contact_email="contactEmail", country="CZ", juristic_person="juristicPerson",
                              members_collections_ids=[5])

    def test_network_members_biobanks_ids_invalid_type(self):
        with self.assertRaises(TypeError):
            network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                              contact_email="contactEmail", country="CZ", juristic_person="juristicPerson",
                              members_biobanks_ids=[47])

    def test_network_set_identifier_ok(self):
        network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                          contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network.identifier = "newId"
        self.assertEqual("newId", network.identifier)

    def test_network_set_identifier_invalid(self):
        network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                          contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network.identifier = 37

    def test_network_set_name_ok(self):
        network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                          contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network.name = "newName"
        self.assertEqual("newName", network.name)

    def test_network_set_name_invalid(self):
        network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                          contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network.name = 37

    def test_network_set_collection_ids_invalid(self):
        network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                          contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network.members_collections_ids = [5]

    def test_network_to_fhir(self):
        network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                          contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
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
        example_network = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                                  contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        example_fhir = example_network.to_fhir("biobankFhirId", ["collfhirid1", "collfhirid2"],
                                               ["biobankFhirId1", "biobankFhirId2"])
        example_fhir.id = "TestFHIRId"
        network_org_fhir = example_network._network_org.to_fhir("biobankFhirId")
        network_org_fhir.id = "TestNetworkOrgFhirId"
        network = Network.from_json(example_fhir.as_json(), network_org_fhir.as_json(), "managingBiobankId")
        self.assertIsInstance(network, Network)
        eq = example_network == network
        self.assertEqual(example_network, network)
        self.assertEqual("TestFHIRId", network.network_fhir_id)
        self.assertEqual("biobankFhirId", network.managing_network_org_fhir_id)
        self.assertEqual(["collfhirid1", "collfhirid2"], network.members_collections_fhir_ids)
        self.assertEqual(["biobankFhirId1", "biobankFhirId2"], network.members_biobanks_fhir_ids)

    def test_network_eq(self):
        network1 = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network2 = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        self.assertEqual(network1, network2)

    def test_network_not_eq(self):
        network1 = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network2 = Network(identifier="networkId", name="networkName", managing_biobank_id="managingBiobankId",
                           contact_email="DifferentEmail", country="CZ", juristic_person="juristicPerson")
        self.assertNotEqual(network2, network1)
