import unittest

from MIABIS_on_FHIR.network_organization import NetworkOrganization


class TestNetworkOrganization(unittest.TestCase):
    network_org_json = {'meta': {'profile': ['http://example.com/StructureDefinition/Network']}, 'extension': [
        {'url': 'http://example.com/StructureDefinition/common-collaboration-topics', 'valueCodeableConcept': {
            'coding': [{'code': 'Charter', 'system': 'http://example.com/common-collaboration-topics-vs'}]}},
        {'url': 'http://example.com/StructureDefinition/juristic-person', 'valueString': 'juristicPerson'}],
                        'active': True, 'address': [{'country': 'cz'}],
                        'contact': [
                            {'name': {'family': 'contactSurname', 'given': ['contactName']},
                             'telecom': [{'system': 'email', 'value': 'contactEmail'}]}],
                        'identifier': [{'system': 'http://example.com/network', 'value': 'networkOrgId'}],
                        'name': 'networkOrgName', 'partOf': {'reference': 'Organization/biobankFhirId'},
                        'resourceType': 'Organization'}

    def test_network_org_required_params_init(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        self.assertIsInstance(network_org, NetworkOrganization)
        self.assertEqual("networkOrgId", network_org.identifier)
        self.assertEqual("networkOrgName", network_org.name)
        self.assertEqual("biobankId", network_org.managing_biobank_id)

    def test_network_org_optional_params_init(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                          "contactSurname", "contactEmail", "country", ["Charter"], "juristicPerson")
        self.assertIsInstance(network_org, NetworkOrganization)
        self.assertEqual("networkOrgId", network_org.identifier)
        self.assertEqual("networkOrgName", network_org.name)
        self.assertEqual("biobankId", network_org.managing_biobank_id)
        self.assertEqual("contactName", network_org.contact_name)
        self.assertEqual("contactSurname", network_org.contact_surname)
        self.assertEqual("contactEmail", network_org.contact_email)
        self.assertEqual("country", network_org.country)
        self.assertEqual(["Charter"], network_org.common_collaboration_topics)
        self.assertEqual("juristicPerson", network_org.juristic_person)

    def test_network_org_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization(37, "networkOrgName", "biobankId")

    def test_network_org_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization("networkOrgId", 22, "biobankId")

    def test_network_org_invalid_managing_biobank_id_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization("networkOrgId", "networkOrgName", 22)

    def test_network_org_invalid_contact_name_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", 22)

    def test_network_org_invalid_contact_surname_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName", 22)

    def test_network_org_invalid_contact_email_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                              "contactSurname", 22)

    def test_network_org_invalid_country_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                              "contactSurname", "contactEmail", 22)

    def test_network_org_invalid_common_collaboration_topics_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                              "contactSurname", "contactEmail", "country", 22)

    def test_network_org_invalid_common_collaboration_topics_value_innit(self):
        with self.assertRaises(ValueError):
            network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                              "contactSurname", "contactEmail", "country", ["invalidTopic"])

    def test_network_org_invalid_juristic_person_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                              "contactSurname", "contactEmail", "country", ["Charter"], 22)

    def test_network_org_set_identifier_ok(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.identifier = "newId"
        self.assertEqual("newId", network_org.identifier)

    def test_network_org_set_identifier_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.identifier = 37

    def test_network_org_set_name_ok(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.name = "newName"
        self.assertEqual("newName", network_org.name)

    def test_network_org_set_name_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.name = 37

    def test_network_org_set_managing_biobank_id_ok(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.managing_biobank_id = "newId"
        self.assertEqual("newId", network_org.managing_biobank_id)

    def test_network_org_set_managing_biobank_id_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.managing_biobank_id = 37

    def test_network_org_set_contact_name_ok(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.contact_name = "newName"
        self.assertEqual("newName", network_org.contact_name)

    def test_network_org_set_contact_name_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.contact_name = 37

    def test_network_org_set_contact_surname_ok(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.contact_surname = "newName"
        self.assertEqual("newName", network_org.contact_surname)

    def test_network_org_set_contact_surname_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.contact_surname = 37

    def test_network_org_set_contact_email_ok(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.contact_email = "newName"
        self.assertEqual("newName", network_org.contact_email)

    def test_network_org_set_contact_email_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.contact_email = 37

    def test_network_org_set_country_ok(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.country = "newName"
        self.assertEqual("newName", network_org.country)

    def test_network_org_set_country_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.country = 37

    def test_network_org_set_common_collaboration_topics_valid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.common_collaboration_topics = ["SOP"]
        self.assertEqual(["SOP"], network_org.common_collaboration_topics)

    def test_network_org_set_common_collaboration_topics_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.common_collaboration_topics = 33

    def test_network_org_set_common_collaboration_topics_invalid_value(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(ValueError):
            network_org.common_collaboration_topics = ["invalidTopic"]

    def test_network_org_set_juristic_person_ok(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org.juristic_person = "newName"
        self.assertEqual("newName", network_org.juristic_person)

    def test_network_org_set_juristic_person_invalid(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        with self.assertRaises(TypeError):
            network_org.juristic_person = 37

    def test_network_org_to_fhir(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId")
        network_org_fhir = network_org.to_fhir("biobankFhirId")
        self.assertEqual("networkOrgId", network_org_fhir.identifier[0].value)
        self.assertEqual("networkOrgName", network_org_fhir.name)
        self.assertEqual("Organization/biobankFhirId", network_org_fhir.partOf.reference)

    def test_network_org_to_fhir_optional_params(self):
        network_org = NetworkOrganization("networkOrgId", "networkOrgName", "biobankId", "contactName",
                                          "contactSurname", "contactEmail", "country", ["Charter"], "juristicPerson")
        network_org_fhir = network_org.to_fhir("biobankFhirId")
        self.assertEqual("networkOrgId", network_org_fhir.identifier[0].value)
        self.assertEqual("networkOrgName", network_org_fhir.name)
        self.assertEqual("Organization/biobankFhirId", network_org_fhir.partOf.reference)
        self.assertEqual("contactName", network_org_fhir.contact[0].name.given[0])
        self.assertEqual("contactSurname", network_org_fhir.contact[0].name.family)
        self.assertEqual("contactEmail", network_org_fhir.contact[0].telecom[0].value)
        self.assertEqual("country", network_org_fhir.address[0].country)
        self.assertEqual("Charter", network_org_fhir.extension[0].valueCodeableConcept.coding[0].code)
        self.assertEqual("juristicPerson", network_org_fhir.extension[1].valueString)

    def test_network_org_from_json(self):
        network_org = NetworkOrganization.from_json(self.network_org_json, "biobankId")
        self.assertEqual("networkOrgId", network_org.identifier)
        self.assertEqual("networkOrgName", network_org.name)
        self.assertEqual("biobankId", network_org.managing_biobank_id)
        self.assertEqual("contactName", network_org.contact_name)
        self.assertEqual("contactSurname", network_org.contact_surname)
        self.assertEqual("contactEmail", network_org.contact_email)
        self.assertEqual("cz", network_org.country)
        self.assertEqual(["Charter"], network_org.common_collaboration_topics)
        self.assertEqual("juristicPerson", network_org.juristic_person)
