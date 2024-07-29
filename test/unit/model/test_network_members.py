import unittest

from MIABIS_on_FHIR.MoF_network_members import MoFNetworkMembers


class TestNetworkMembers(unittest.TestCase):

    def test_network_members_init(self):
        network_members = MoFNetworkMembers("networkId", "networkName", ["memberId1", "memberId2"])
        self.assertIsInstance(network_members, MoFNetworkMembers)
        self.assertEqual("networkId", network_members.network_id)
        self.assertEqual("networkName", network_members.title)
        self.assertEqual(["memberId1", "memberId2"], network_members.members)

    def test_network_members_invalid_network_id_type_innit(self):
        with self.assertRaises(TypeError):
            network_members = MoFNetworkMembers(37, "networkName", ["memberId1", "memberId2"])

    def test_network_members_invalid_title_type_innit(self):
        with self.assertRaises(TypeError):
            network_members = MoFNetworkMembers("networkId", 22, ["memberId1", "memberId2"])

    def test_network_members_invalid_members_type_innit(self):
        with self.assertRaises(TypeError):
            network_members = MoFNetworkMembers("networkId", "networkName", 22)

    def test_network_members_set_network_id_ok(self):
        network_members = MoFNetworkMembers("networkId", "networkName", ["memberId1", "memberId2"])
        network_members.network_id = "newId"
        self.assertEqual("newId", network_members.network_id)

    def test_network_members_set_network_id_invalid(self):
        network_members = MoFNetworkMembers("networkId", "networkName", ["memberId1", "memberId2"])
        with self.assertRaises(TypeError):
            network_members.network_id = 37

    def test_network_members_set_title_ok(self):
        network_members = MoFNetworkMembers("networkId", "networkName", ["memberId1", "memberId2"])
        network_members.title = "newName"
        self.assertEqual("newName", network_members.title)

    def test_network_members_set_title_invalid(self):
        network_members = MoFNetworkMembers("networkId", "networkName", ["memberId1", "memberId2"])
        with self.assertRaises(TypeError):
            network_members.title = 37

    def test_network_members_set_members_ok(self):
        network_members = MoFNetworkMembers("networkId", "networkName", ["memberId1", "memberId2"])
        network_members.members = ["memberId3", "memberId4"]
        self.assertEqual(["memberId3", "memberId4"], network_members.members)

    def test_network_members_set_members_invalid(self):
        network_members = MoFNetworkMembers("networkId", "networkName", ["memberId1", "memberId2"])
        with self.assertRaises(TypeError):
            network_members.members = 37

    def test_network_to_fhir_ok(self):
        network_members = MoFNetworkMembers("networkId", "networkName", ["memberId1", "memberId2"])
        network_fhir = network_members.to_fhir("networkFhirId", ["collectionMemberFhirId1", "collectionMemberFhirId2"],
                                       ["biobankMemberFhirId3", "biobankMemberFhirId4"])
        self.assertEqual(network_members.title,network_fhir.title)
        self.assertEqual("current",network_fhir.status)
        self.assertEqual("working",network_fhir.mode)
        self.assertEqual("Group/networkFhirId",network_fhir.subject.reference)
        self.assertEqual("Group/collectionMemberFhirId1",network_fhir.entry[0].item.reference)
        self.assertEqual("Group/collectionMemberFhirId2",network_fhir.entry[1].item.reference)
        self.assertEqual("Organization/biobankMemberFhirId3",network_fhir.entry[2].item.reference)
        self.assertEqual("Organization/biobankMemberFhirId4",network_fhir.entry[3].item.reference)
