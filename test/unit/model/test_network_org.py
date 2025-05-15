import unittest

from miabis_model import _NetworkOrganization


class TestNetworkOrganization(unittest.TestCase):
    def test_network_org_required_params_init(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        self.assertIsInstance(network_org, _NetworkOrganization)
        self.assertEqual("networkOrgId", network_org.identifier)
        self.assertEqual("networkName", network_org.name)
        self.assertEqual("contactEmail", network_org.contact_email)
        self.assertEqual("CZ", network_org.country)
        self.assertEqual("juristicPerson", network_org.juristic_person.name)

    def test_network_org_optional_params_init(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson",
                                           contact_name="contactName", contact_surname="contactSurname",
                                           common_collaboration_topics=["Charter"], description="Description")
        self.assertIsInstance(network_org, _NetworkOrganization)
        self.assertEqual("networkOrgId", network_org.identifier)
        self.assertEqual("networkName", network_org.name)
        self.assertEqual("contactName", network_org.contact_name)
        self.assertEqual("contactSurname", network_org.contact_surname)
        self.assertEqual("contactEmail", network_org.contact_email)
        self.assertEqual("CZ", network_org.country)
        self.assertEqual(["Charter"], network_org.common_collaboration_topics)
        self.assertEqual("juristicPerson", network_org.juristic_person.name)
        self.assertEqual("Description", network_org.description)

    def test_network_org_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = _NetworkOrganization(identifier=37, name="networkName",
                                               contact_email="contactEmail", country="CZ",
                                               juristic_person="juristicPerson")

    def test_network_org_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = _NetworkOrganization(identifier="networkOrgId", name=37,
                                               contact_email="contactEmail", country="CZ",
                                               juristic_person="juristicPerson")

    def test_network_org_invalid_contact_name_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                               contact_email="contactEmail", country="CZ",
                                               juristic_person="juristicPerson", contact_name=37)

    def test_network_org_invalid_contact_surname_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                               contact_email="contactEmail", country="CZ",
                                               juristic_person="juristicPerson",
                                               contact_surname=37)

    def test_network_org_invalid_contact_email_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                               contact_email=37, country="CZ", juristic_person="juristicPerson")

    def test_network_org_invalid_country_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                               contact_email="contactEmail", country=37,
                                               juristic_person="juristicPerson")

    def test_network_org_invalid_common_collaboration_topics_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                               contact_email="contactEmail", country="CZ",
                                               juristic_person="juristicPerson",
                                               common_collaboration_topics=37)

    def test_network_org_invalid_common_collaboration_topics_value_innit(self):
        with self.assertRaises(ValueError):
            network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                               contact_email="contactEmail", country="CZ",
                                               juristic_person="juristicPerson",
                                               common_collaboration_topics=["invalid"])

    def test_network_org_invalid_juristic_person_type_innit(self):
        with self.assertRaises(TypeError):
            network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                               contact_email="contactEmail", country="CZ", juristic_person=37)

    def test_network_org_set_identifier_ok(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.identifier = "newId"
        self.assertEqual("newId", network_org.identifier)

    def test_network_org_set_identifier_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.identifier = 37

    def test_network_org_set_name_ok(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.name = "newName"
        self.assertEqual("newName", network_org.name)

    def test_network_org_set_name_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.name = 37

    def test_network_org_set_managing_biobank_id_ok(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.managing_biobank_id = "newId"
        self.assertEqual("newId", network_org.managing_biobank_id)

    def test_network_org_set_managing_biobank_id_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.managing_biobank_id = 37

    def test_network_org_set_contact_name_ok(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.contact_name = "newName"
        self.assertEqual("newName", network_org.contact_name)

    def test_network_org_set_contact_name_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.contact_name = 37

    def test_network_org_set_contact_surname_ok(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.contact_surname = "newName"
        self.assertEqual("newName", network_org.contact_surname)

    def test_network_org_set_contact_surname_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.contact_surname = 37

    def test_network_org_set_contact_email_ok(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.contact_email = "newName"
        self.assertEqual("newName", network_org.contact_email)

    def test_network_org_set_contact_email_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.contact_email = 37

    def test_network_org_set_country_ok(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.country = "newName"
        self.assertEqual("newName", network_org.country)

    def test_network_org_set_country_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.country = 37

    def test_network_org_set_common_collaboration_topics_valid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.common_collaboration_topics = ["SOP"]
        self.assertEqual(["SOP"], network_org.common_collaboration_topics)

    def test_network_org_set_common_collaboration_topics_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.common_collaboration_topics = 33

    def test_network_org_set_common_collaboration_topics_invalid_value(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(ValueError):
            network_org.common_collaboration_topics = ["invalidTopic"]

    def test_network_org_set_juristic_person_ok(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org.juristic_person = "newName"
        self.assertEqual("newName", network_org.juristic_person)

    def test_network_org_set_juristic_person_invalid(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        with self.assertRaises(TypeError):
            network_org.juristic_person.name = 37

    def test_network_org_to_fhir(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson")
        network_org_fhir = network_org.to_fhir("jpfi")
        self.assertEqual("networkOrgId", network_org_fhir.identifier[0].value)
        self.assertEqual("networkName", network_org_fhir.name)
        self.assertEqual("contactEmail", network_org_fhir.contact[0].telecom[0].value)
        self.assertEqual("CZ", network_org_fhir.address[0].country)
        self.assertEqual("Organization/jpfi", network_org_fhir.partOf.reference)

    def test_network_org_to_fhir_optional_params(self):
        network_org = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                           contact_email="contactEmail", country="CZ", juristic_person="juristicPerson",
                                           contact_name="contactName", contact_surname="contactSurname",
                                           common_collaboration_topics=["Charter"],
                                           description="description")
        network_org_fhir = network_org.to_fhir("jpfi")
        self.assertEqual("networkOrgId", network_org_fhir.identifier[0].value)
        self.assertEqual("networkName", network_org_fhir.name)
        self.assertEqual("Organization/jpfi", network_org_fhir.partOf.reference)
        self.assertEqual("contactName", network_org_fhir.contact[0].name.given[0])
        self.assertEqual("contactSurname", network_org_fhir.contact[0].name.family)
        self.assertEqual("contactEmail", network_org_fhir.contact[0].telecom[0].value)
        self.assertEqual("CZ", network_org_fhir.address[0].country)
        self.assertEqual("Charter", network_org_fhir.extension[0].valueCodeableConcept.coding[0].code)
        self.assertEqual("description", network_org_fhir.extension[1].valueString)

    def test_network_org_from_json(self):
        example_network = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                               contact_email="contactEmail", country="CZ",
                                               juristic_person="juristicPerson",
                                               contact_name="contactName", contact_surname="contactSurname",
                                               common_collaboration_topics=["Charter"],
                                               description="description")
        example_fhir = example_network.to_fhir("biobankFhirId")
        example_fhir.id = "TestFHIRId"
        juristic_person_fhir = example_network.juristic_person.to_fhir()
        network_org = _NetworkOrganization.from_json(example_fhir.as_json(),
                                                     example_network.juristic_person.to_fhir().as_json())
        self.assertEqual(example_network, network_org)
        self.assertEqual("juristicPerson", network_org.juristic_person.name)
        self.assertEqual("TestFHIRId", network_org.network_org_fhir_id)

    def test_network_org_eq(self):
        network_org_1 = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                             contact_email="contactEmail", country="CZ",
                                             juristic_person="juristicPerson",
                                             contact_name="contactName", contact_surname="contactSurname",
                                             common_collaboration_topics=["Charter"],
                                             description="description")
        network_org_2 = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                             contact_email="contactEmail", country="CZ",
                                             juristic_person="juristicPerson",
                                             contact_name="contactName", contact_surname="contactSurname",
                                             common_collaboration_topics=["Charter"],
                                             description="description")
        self.assertEqual(network_org_1, network_org_2)

    def test_network_org_not_eq(self):
        network_org_1 = _NetworkOrganization(identifier="networkOrgId", name="networkName",
                                             contact_email="contactEmail", country="CZ",
                                             juristic_person="juristicPerson",
                                             contact_name="contactName", contact_surname="contactSurname",
                                             common_collaboration_topics=["Charter"],
                                             description="description")
        network_org_2 = _NetworkOrganization(identifier="DifferentId", name="networkName",
                                             contact_email="contactEmail", country="CZ",
                                             juristic_person="juristicPerson",
                                             contact_name="contactName", contact_surname="contactSurname",
                                             common_collaboration_topics=["Charter"],
                                             description="description")
        self.assertNotEqual(network_org_1, network_org_2)
